---
title: 语音栈：让 AI 能听会说
---

# 语音栈：让 AI 能听会说

> 约 8 分钟 · 关键词：ASR、TTS、端到端语音、VAD、打断

## 两条路线：级联还是端到端

  <table>
    <tr><th></th><th>级联（Cascaded）</th><th>端到端（Speech-to-Speech）</th></tr>
    <tr><td>链路</td><td>ASR 转文字 → LLM 理解生成 → TTS 合成</td><td>音频 token 直接进，音频 token 直接出</td></tr>
    <tr><td>延迟</td><td>三段串行，首字常要 1.5~3 秒</td><td>可压到几百毫秒，最接近真人通话</td></tr>
    <tr><td>副语言</td><td>语气、情绪、停顿在转文字时被丢掉</td><td>保留语气、笑声、迟疑</td></tr>
    <tr><td>可观测</td><td>中间有完整文字稿，能审、能查、能插规则</td><td>黑盒，出问题难定位</td></tr>
    <tr><td>代价</td><td>拼装复杂，但每段都可替换可优化</td><td>优雅但生态少，成本高、可控性差</td></tr>
  </table>

选型其实取决于业务：**要审计、要能插业务规则、要换模型自由，就选级联；追求"像打电话"的自然感，才值得上端到端。**大多数企业场景里，级联仍是默认答案。

## 一条实时语音链路的四件事

  <figure class="figure">
    <svg viewBox="0 0 720 216" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a17" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <text x="40" y="24" class="dim">级联管线：三段串行，延迟叠加</text>
        <rect x="60" y="34" width="180" height="34" rx="8" class="cell link-purple"/>
        <text x="150" y="56" text-anchor="middle">ASR 转文字</text>
        <rect x="240" y="34" width="150" height="34" rx="8" class="cell link"/>
        <text x="315" y="56" text-anchor="middle">LLM 生成</text>
        <rect x="390" y="34" width="150" height="34" rx="8" class="cell link-green"/>
        <text x="465" y="56" text-anchor="middle">TTS 合成</text>
        <text x="560" y="56" font-size="11" class="dim">首字 1.5~3s</text>
        <text x="40" y="112" class="dim">流式 + 端点检测：边听边出，重叠执行</text>
        <rect x="60" y="122" width="140" height="34" rx="8" class="cell link-purple"/>
        <text x="130" y="144" text-anchor="middle">ASR（流式）</text>
        <rect x="170" y="122" width="170" height="34" rx="8" class="cell link"/>
        <text x="255" y="144" text-anchor="middle">LLM（流式）</text>
        <rect x="310" y="122" width="140" height="34" rx="8" class="cell link-green"/>
        <text x="380" y="144" text-anchor="middle">TTS（流式）</text>
        <text x="470" y="144" font-size="11" class="dim">首字 &lt; 1s</text>
        <line x1="60" y1="176" x2="660" y2="176" stroke-width="1.2" marker-end="url(#a17)" class="link-dim"/>
        <text x="668" y="180" font-size="11" class="dim">时间</text>
        <text x="40" y="200" font-size="11" class="dim">打断（barge-in）：用户插话 → VAD 立刻上报 → 停止播放与生成，重新开始听</text>
      </g>
    </svg>
    <figcaption>图 17：级联 vs 流式——把三段重叠起来，首字延迟能降一半以上</figcaption>
  </figure>

  1. **VAD（端点检测）**：判断"用户说完了没"。它是整条链路的总开关——切早了把一句话截断，切晚了用户干等。
2. **流式 ASR**：边说边出字，不等整句说完。这样 LLM 可以提前启动。
3. **LLM 生成**：同样流式输出，第一句话一出来就往下游送。
4. **流式 TTS + 打断**：边合成边播放，不必等全部生成完；用户一插话要能立刻闭嘴——这就是**打断（barge-in）**。

## 延迟预算：为什么"像打电话"这么难

人类对话里，接话的间隔通常只有两三百毫秒。一旦超过 1 秒，"机器味"立刻出来；超过 2 秒，用户就开始怀疑是不是卡了。

于是整条链路的每一环都要抠：

  <table>
    <tr><th>环节</th><th>常用优化</th></tr>
    <tr><td>端点检测</td><td>更灵敏的 VAD、允许"嗯""那个"这类填充词作为未结束信号</td></tr>
    <tr><td>识别</td><td>流式输出中间结果，不等最终句</td></tr>
    <tr><td>生成</td><td>首句优先（先出第一句再继续）、小模型兜底、缓存常见问答</td></tr>
    <tr><td>合成</td><td>首包延迟优先于音质；短句合并成一次请求</td></tr>
    <tr><td>整体</td><td>本地部署省掉网络往返；按场景分级路由（闲聊用快模型）</td></tr>
  </table>

## 三个容易被忽略的工程细节

  - **采样率与格式统一**：语音模型常见的输入是 16kHz 单声道，链路上每一跳的采样率、编码不一致，就会出现"识别得好好的，一接 TTS 就变调"。
2. **远场与噪声**：真实会议室、车里、门店的拾音，需要**降噪 + 回声消除（AEC）**，否则 VAD 会误判、ASR 会连篇错字。这也是"演示机很准、上线后很差"最常见的原因。
3. **时间戳与说话人分离**：会议纪要、客服质检这类场景，光有文字不够，还要"谁在第几分钟说了什么"——**diarization（说话人分离）**是刚需。

::: tip
语音的难点从来不是"识别准不准"，而是**延迟与轮次管理**。判断准"什么时候该听、什么时候该说、什么时候该闭嘴"，体验才像对话——这三件事全都要靠 VAD 和打断机制撑起来。
:::

语音助手还有一个新麻烦：它听得见、也动得了手。这就把安全问题的级别整个抬高了——下一篇：**Agent 安全：提示注入与权限边界**。
