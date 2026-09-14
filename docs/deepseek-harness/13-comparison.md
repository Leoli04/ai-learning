---
title: 横向对比：dsh 和其他 Agent Harness 的取舍
---

# 横向对比：dsh 和其他 Agent Harness 的取舍

> 约 9 分钟 · 关键词：架构取舍、可替换性、开箱即用、生态

## 先划清战场：四类玩家

"Agent 工具"这个词下面其实混着四类东西，混着比较只会得出"各有千秋"这种废话。先分开：

  <table>
    <tr><th>类别</th><th>代表形态</th><th>你买到的是什么</th></tr>
    <tr><td><strong>闭源一体化 CLI</strong></td><td>各家模型厂商自带的命令行 Agent</td><td>开箱即用的最强体验，改造空间有限</td></tr>
    <tr><td><strong>IDE 集成型</strong></td><td>编辑器插件形态的编码助手</td><td>贴着编辑器的低摩擦体验，边界在编辑器内</td></tr>
    <tr><td><strong>开源 Harness</strong></td><td>dsh、OpenHands 一类</td><td>可读、可改、可自部署的完整 Agent 运行时</td></tr>
    <tr><td><strong>框架 / 编排库</strong></td><td>LangGraph、CrewAI、AutoGen 一类</td><td>搭积木，你自己写业务逻辑和产品外壳</td></tr>
    <tr><td><strong>低代码平台</strong></td><td>Dify、n8n、扣子一类</td><td>画布上拼流程，交付快、深度定制受限</td></tr>
  </table>

**dsh 属于第三类**，而且它的定位很明确：不是"给你一个能用的 Agent"，而是"给你一个能被你改到底的 Agent 运行时"。

  <figure class="figure">
    <svg viewBox="0 0 720 282" xmlns="http://www.w3.org/2000/svg">
      <g font-size="12">
        <text x="76" y="34" font-size="11" class="dim">平台 / 生态</text>
        <text x="76" y="232" font-size="11" class="dim">单机工具</text>
        <line x1="70" y1="42" x2="70" y2="240" stroke-width="1.5" class="cell-stroke"/>
        <line x1="70" y1="240" x2="660" y2="240" stroke-width="1.5" class="cell-stroke"/>
        <text x="70" y="262" font-size="11" class="dim">开箱即用</text>
        <text x="660" y="262" font-size="11" class="dim" text-anchor="end">可深度改造</text>
        <circle cx="150" cy="150" r="6" class="accent-blue-fill"/>
        <text x="164" y="154" font-size="11">闭源一体化 CLI</text>
        <circle cx="110" cy="205" r="6" class="accent-blue-fill"/>
        <text x="124" y="209" font-size="11">IDE 集成型</text>
        <circle cx="240" cy="72" r="6" class="accent-orange-fill"/>
        <text x="254" y="76" font-size="11">低代码平台</text>
        <circle cx="470" cy="165" r="6" class="accent-purple-fill"/>
        <text x="484" y="169" font-size="11">框架 / 编排库</text>
        <circle cx="556" cy="80" r="7" class="accent-green-fill"/>
        <text x="572" y="84" font-size="11">开源 Harness（dsh）</text>
      </g>
    </svg>
    <figcaption>图 13：四类玩家的位置——dsh 选在了"要读代码，但换来控制权"的那个角</figcaption>
  </figure>

## 逐条比设计取向

下面这张表比的是**架构取向**，不是功能清单——具体产品会随版本变化，取向则相对稳定，也更容易判断"适不适合我"。

  <table>
    <tr><th>维度</th><th>dsh 的取向</th><th>另一种常见取向</th></tr>
    <tr><td><strong>内核</strong></td><td>没有特权核心，连 UI 侧都靠插件拼</td><td>一个稳定内核 + 若干固定扩展点</td></tr>
    <tr><td><strong>扩展方式</strong></td><td>配置即组合（profile → bundle → patch），改配置不改代码</td><td>写插件代码，或改开关</td></tr>
    <tr><td><strong>状态</strong></td><td>Session Log 是唯一事实源，一切可回放可分叉</td><td>状态分散在内存与多个存储里</td></tr>
    <tr><td><strong>工具契约</strong></td><td>先返回**规范值**，再单独渲染给模型看</td><td>工具直接拼一段字符串给模型</td></tr>
    <tr><td><strong>授权</strong></td><td>结果闭合、失败时拒绝、一次授权只覆盖一次操作</td><td>"记住这个选择""本次会话都允许"</td></tr>
    <tr><td><strong>沙箱</strong></td><td>逐调用策略，且只用 full / partial 诚实上报完整度</td><td>全局开关或容器级隔离</td></tr>
    <tr><td><strong>多智能体</strong></td><td>拆成两套：subagent（单次子任务）与 agent-team（持久队友 + 共享任务 DAG）</td><td>一个笼统的"多 Agent 协作"抽象</td></tr>
    <tr><td><strong>交付形态</strong></td><td>web / headless / sdk / acp 同源，靠 profile 切换</td><td>CLI 优先，SDK 另起一套</td></tr>
    <tr><td><strong>可观测</strong></td><td>审计事件与模型可见记录严格分离</td><td>日志与对话记录常常混在一起</td></tr>
  </table>

其中有两行最值得展开，因为它们直接决定"出事时你能不能救回来"：

  - **审计与模型记录分离**。第 9 篇讲过，审批问答会成对写进日志，但**不进模型的 transcript**。这意味着事后审计拿到的是全量事实，而模型不会被"刚才有人点了允许"这类信息污染判断。混在一起的系统就做不到这一点——你很难既给审计全量，又不让模型看到。
  - **一次授权只覆盖一次操作**。绝大多数工具会提供"本次会话内不再询问"这种便利选项。dsh 的取向是**不提供**：只有 `allowed-once` 一种放行。短期体验"更啰嗦"，长期换来的是"不可能因为一次误点而放开一整段会话"。

## 代价：dsh 不是白拿的

取向决定了成本，这篇必须说清：

  - **要先懂 Cordis**。Context、Service、Effect、Fiber 这套模型不通，稍复杂的插件就写不下去。它继承的是 Cordis 那套"时空可组合"的编程范式，不是普通的依赖注入。
2. **文档量大**。官方文档按子系统成页，五六十个页面，读完能懂，但要读。它假设读者愿意读代码。
3. **developer preview**。README 里明确写着**会有破坏性兼容变更**——生产使用要跟版本、要留回滚余地。
4. **生态年轻**。相比已经跑了很久的闭源产品和老牌框架，第三方插件、教程、踩坑帖都少。遇到怪问题多半得自己读源码。
5. **不是给"只想用、不想读代码"的人准备的**。如果你的需求是"给我一个能用的编码助手"，闭源一体化 CLI 的上手体验会好得多。

## 怎么选：三个问题

与其记功能表，不如问自己三个问题：

  <table>
    <tr><th>问题</th><th>偏开源 Harness</th><th>偏闭源 / 低代码</th></tr>
    <tr><td>数据能出内网吗？</td><td>不能，或不想</td><td>可以</td></tr>
    <tr><td>需要改内核行为吗？</td><td>需要：改工具契约、改授权策略、改事件流</td><td>不需要，配置够用</td></tr>
    <tr><td>出事要能回溯到每一步吗？</td><td>要，且有合规要求</td><td>常规日志够用</td></tr>
  </table>

三个问题里有两个偏左边，开源 Harness 值得投入学习成本；两个偏右边，直接用现成产品，把精力放在业务上——**这不是技术高下的问题，是成本放在哪里的问题。**

::: tip
选型的本质是选**你打算在哪儿付钱**：付给"学习与维护"，换内核级的可控与可审计；或者付给"订阅与等待"，换开箱即用。**两边都不便宜，别指望免费的那个。**
:::

最后一篇，我们回到代码本身：**这个仓库到底长什么样？**
