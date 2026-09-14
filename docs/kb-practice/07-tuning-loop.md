---
title: 检索调优：查询改写、多路召回与 badcase 闭环
---

# 检索调优：查询改写、多路召回与 badcase 闭环

> 约 10 分钟 · 关键词：查询改写、badcase、环节定位、回归测试

## 从症状反推动作

调优最容易犯的错是"先想到一个技术就往上加"。正确的顺序是**先看症状，再决定动哪一环**：

  <table>
    <tr><th>症状</th><th>大概率原因</th><th>该做的动作</th></tr>
    <tr><td>换个说法就搜不到</td><td>问法与文档用词不一致</td><td>查询改写、同义词扩充</td></tr>
    <tr><td>编号 / 型号 / 人名搜不到</td><td>纯向量检索的先天盲区</td><td>补 BM25 那一路（第 06 篇）</td></tr>
    <tr><td>该段落压根没进候选集</td><td>切分把关键内容切散了</td><td>回到第 03 篇改切分，别在检索层硬调</td></tr>
    <tr><td>召回了但排在 20 名开外</td><td>排序不够精细</td><td>上 Rerank；检查融合权重</td></tr>
    <tr><td>召回的内容对，但答案没用上</td><td>提示词或上下文组织问题</td><td>强制引用来源、调整片段顺序——这已不属检索问题</td></tr>
    <tr><td>答案里出现了旧版本</td><td>元数据的有效期没生效</td><td>回到第 04 篇补时间过滤</td></tr>
  </table>

这张表的价值在于：**它把一半的问题挡在"加技术"之外**。很多团队上来就折腾 Rerank 模型，实际病灶在切分——换三个模型也不会好。

## 查询改写：让问题说"文档的语言"

用户提问和文档表述之间隔着一道翻译。改写就是补这道翻译，手段按成本从低到高：

  <table>
    <tr><th>手段</th><th>做法</th><th>成本</th><th>适合</th></tr>
    <tr><td>同义词表</td><td>维护一份"口语 → 术语"映射（报销上限 → 差旅标准）</td><td>零模型调用</td><td>高频词固定、行业术语有限的场景</td></tr>
    <tr><td>多查询扩展</td><td>一个问题让模型改写成 3～5 种说法，分别检索后融合</td><td>一次模型调用 + N 次检索</td><td>问得笼统、单一表述覆盖不全</td></tr>
    <tr><td>HyDE</td><td>先让模型"假设一个答案"，拿这段假设去检索</td><td>一次模型调用</td><td>问法与文档风格差异极大</td></tr>
    <tr><td>查询路由</td><td>先判断该查哪个库，或根本不用查</td><td>一次轻量调用</td><td>多库并存、入口混杂闲聊</td></tr>
  </table>

两条实践提醒：

  1. **改写一定要保留原始查询。** 改写本身会出错——模型把"离职补偿"改写成"辞退赔偿"，方向就偏了。稳妥做法是**原查询和改写查询同时检索，一起融合**，改写只作为增量而不是替代。
  2. **改写不要贪多。** 一次扩成 5 个以上变体，延迟和成本直线上升，还会引入无关噪声把真正相关的内容挤出候选集。3 个变体通常够用。

## badcase 闭环：真正拉开差距的地方

技术手段是公开的，能不能持续变好取决于一件很朴素的事：**你有没有把用户答错的那些问题攒起来。**

具体做法：

  <table>
    <tr><th>步骤</th><th>做什么</th><th>要点</th></tr>
    <tr><td>① 收集</td><td>记录每一个"回答不满意"的问题</td><td>在界面上放一个显式反馈按钮，比事后挖日志有效得多</td></tr>
    <tr><td>② 标注</td><td>记下问题、期望命中的文档与章节、实际召回内容、错误类型</td><td>「期望出处」是最关键的一列——没有它，无法判断是检索问题还是文档本身就没写</td></tr>
    <tr><td>③ 定位</td><td>判断问题出在解析 / 切分 / 检索 / 生成哪一环</td><td>用下面的诊断表，不要凭感觉</td></tr>
    <tr><td>④ 修复</td><td>改配置或改数据，然后重跑全部 badcase</td><td>必须全量重跑，防止"修好一个坏掉三个"</td></tr>
    <tr><td>⑤ 归档</td><td>把已修复的 badcase 转成评测用例，永久留在回归集里</td><td>这一步是闭环的关键，很多人漏掉</td></tr>
  </table>

  <figure class="figure">
    <svg viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a7" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <rect x="30" y="40" width="140" height="56" rx="9" class="cell"/>
        <text x="100" y="62" text-anchor="middle">用户反馈答错</text>
        <text x="100" y="81" text-anchor="middle" font-size="11" class="dim">或压根答不上来</text>
        <line x1="172" y1="68" x2="182" y2="68" stroke-width="1.8" marker-end="url(#a7)" class="link"/>
        <rect x="185" y="40" width="140" height="56" rx="9" class="cell"/>
        <text x="255" y="62" text-anchor="middle">记录 badcase</text>
        <text x="255" y="81" text-anchor="middle" font-size="11" class="dim">问题 + 期望出处</text>
        <line x1="327" y1="68" x2="337" y2="68" stroke-width="1.8" marker-end="url(#a7)" class="link"/>
        <rect x="340" y="40" width="140" height="56" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="410" y="62" text-anchor="middle">定位到哪一环</text>
        <text x="410" y="81" text-anchor="middle" font-size="11" class="dim">解析 / 切分 / 检索 / 生成</text>
        <line x1="482" y1="68" x2="492" y2="68" stroke-width="1.8" marker-end="url(#a7)" class="link"/>
        <rect x="495" y="40" width="140" height="56" rx="9" class="cell link-green"/>
        <text x="565" y="62" text-anchor="middle">修复并归档</text>
        <text x="565" y="81" text-anchor="middle" font-size="11" class="dim">沉淀为评测用例</text>
        <path d="M 565 96 C 565 145 100 145 100 100" fill="none" stroke-width="1.8" marker-end="url(#a7)" class="link-orange"/>
        <text x="30" y="178" font-size="11" class="dim">每转一圈，评测集变厚一层——三个月后它就是你最值钱的资产</text>
      </g>
    </svg>
    <figcaption>图 7：badcase 闭环——修复的动作会把评测集越攒越厚</figcaption>
  </figure>

## 怎么判断问题出在哪一环

这是闭环里最需要方法的一步。给一套可执行的诊断手法：

  <table>
    <tr><th>判断</th><th>验证方法</th><th>结论</th></tr>
    <tr><td>文档里到底有没有这句话？</td><td>直接 grep 原始文件</td><td>没有 → 不是检索问题，是文档缺失或权限问题</td></tr>
    <tr><td>解析出来的文本里有吗？</td><td>搜解析产物</td><td>原文有、解析没 → 解析问题（第 02 篇）</td></tr>
    <tr><td>切出来的 chunk 里有吗？</td><td>搜 chunk 库</td><td>解析有、chunk 没 → 切分问题（第 03 篇）</td></tr>
    <tr><td>chunk 被召回了吗？</td><td>看检索原始结果（带分数与排名）</td><td>没召回 → 检索问题；召回了但排名靠后 → 排序问题</td></tr>
    <tr><td>召回的内容进上下文了吗？</td><td>打印最终拼给模型的完整提示词</td><td>进了但答错 → 生成问题，不是检索问题</td></tr>
  </table>

关键是**一步步往下查，不跳步**。用"打印最终提示词"这一招可以过滤掉大量误判——很多被当成"检索不准"的问题，实际是检索结果正确、但被后来的过滤逻辑丢掉了。

## 每次调优都要有一次自检

这也是评测集真正的用法：**任何配置变更，都拿同一批问题跑一遍做对照。**

  <table>
    <tr><th>纪律</th><th>为什么</th></tr>
    <tr><td>一次只改一个变量</td><td>同时改切分和 Rerank，效果变好了你也不知道是谁的功劳</td></tr>
    <tr><td>改动前先记录当前基线</td><td>没有基线，"变好了"只是感觉</td></tr>
    <tr><td>全量跑，不抽样</td><td>检索调优的典型陷阱是"修好一条坏掉三条"</td></tr>
    <tr><td>记录指标而非印象</td><td>Recall@10 涨了几个点、badcase 从 30 条降到 22 条</td></tr>
  </table>

::: tip
知识库项目的分水岭不在技术选型，而在**有没有 badcase 库**。有它的团队，每周都在变好；没有它的团队，三个月后还在原地讨论"要不要换个向量库"。
:::

检索链路到这里已经完整了。但企业场景还有一道绕不过去的关：**同一个库，不同的人该看到不同的东西**——下一篇：**权限与多租户：谁能看哪些文档**。
