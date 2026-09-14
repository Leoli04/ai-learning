---
title: 进阶：GraphRAG / Agentic RAG 的适用边界
---

# 进阶：GraphRAG / Agentic RAG 的适用边界

> 约 10 分钟 · 关键词：GraphRAG、Agentic RAG、多跳、方案选型

## 先说结论

前九篇做完，一个知识库已经能解决绝大多数企业问题。剩下这两类"高级方案"，经常被当成升级必选项，但真实情况是：

**多数企业知识库停在第 06 篇那套混合检索就够了。** GraphRAG 和 Agentic RAG 不是"更高级的版本"，而是**为特定类型的问题设计的专用工具**——用错了地方，只会付出几倍的延迟和成本，换来几乎为零的收益。

判断依据不是技术潮流，而是你 badcase 库里的问题类型（第 07 篇）。下面分别说清楚它们各自解决什么。

## GraphRAG：为"关系"和"全局"而生

GraphRAG 的核心思路在第 16 篇《进阶 RAG》里讲过：先把文档变成实体—关系图，再在图上做归纳。在企业场景里，它真正能发挥价值的场景很具体：

  <table>
    <tr><th>适合</th><th>为什么图结构有帮助</th></tr>
    <tr><td>组织架构与汇报关系</td><td>"这个岗位的上级部门是哪个""这个项目归谁管"——答案本身就是一条路径</td></tr>
    <tr><td>法规 / 制度之间的引用链</td><td>"这条规定依据的是哪份文件""哪些条款被废除了"——引用关系是显式存在的</td></tr>
    <tr><td>供应链与产品结构</td><td>"这个型号的替代料号有哪些"——多跳关系查询</td></tr>
    <tr><td>跨文档归纳类问题</td><td>"这批合同的主要风险点集中在哪几类"——答案不落在任何一段里，需要全局统计</td></tr>
  </table>

  <table>
    <tr><th>不适合</th><th>原因</th></tr>
    <tr><td>日常制度问答（"年假几天""报销流程"）</td><td>单跳事实查询，混合检索已经足够，图结构增加不了任何信息</td></tr>
    <tr><td>频繁变动的文档（会议纪要、日报）</td><td>实体抽取要重跑，维护成本远高于收益</td></tr>
    <tr><td>关系稀疏的散文档</td><td>抽出来的图又碎又断，还不如原样检索</td></tr>
  </table>

成本必须提前算清：**建图要对全部文档额外跑一遍 LLM 做实体与关系抽取**（还有社区摘要生成），这是一次性的大额开销，且每次文档更新都要增量重跑。所以它适合**静态、高价值**的语料——法规库、合同库、行业研究，而不是每天都在变的运营文档。

**一个务实的中间态**：如果只想要"跨文档关系"这类收益，不必上完整的图。可以只在元数据层面做轻量关系——给文档和 chunk 标注 `实体标签`（部门名、产品线、项目代号），检索时按标签扩展召回。这能覆盖相当一部分"关系查询"，成本几乎可以忽略。真正的图只在关系特别密集时才值得。

## Agentic RAG：为"多跳"和"要动手"而生

Agentic RAG 是把检索变成 Agent 可以反复调用的工具：它先判断要查什么，看完结果发现不够就改写查询再查一轮，凑齐了才作答（第 16 篇有完整对比图）。它在企业场景里真正必要的场合是：

  <table>
    <tr><th>场景</th><th>例子</th></tr>
    <tr><td>多跳问答</td><td>"我们对接的那家供应商，它的母公司去年营收多少"——先定位供应商，再查母公司，再查财报</td></tr>
    <tr><td>需要配合其他工具</td><td>"本季度超期工单里，金额最大的是哪几个"——要同时查知识库和业务数据库，还要排序</td></tr>
    <tr><td>问题指向不明确</td><td>用户问"这个流程有问题"——Agent 需要先确认"哪个流程"再检索</td></tr>
  </table>

代价同样实在：

  <table>
    <tr><th>代价</th><th>具体表现</th></tr>
    <tr><td>延迟倍增</td><td>一次问答可能变成 5～6 次模型调用，响应从 2 秒变成 10 秒以上</td></tr>
    <tr><td>成本不可预测</td><td>简单问题也可能触发多轮检索，账单波动大</td></tr>
    <tr><td>链路不可复现</td><td>同一个问题两次可能走不同路径，出问题难排查</td></tr>
  </table>

所以正确姿势是**分级启用**：默认走单跳混合检索，只在命中特定特征时才升级到多轮——比如问题里含多个实体、含比较或归因词（"为什么""哪个更"）、或者首轮检索的最高分偏低。这样既拿到多跳能力，又把成本控制在可预期范围内。

  <figure class="figure">
    <svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg">
      <g font-size="12">
        <text x="30" y="34">按问题类型选方案——不是按技术新旧选</text>
        <rect x="30" y="52" width="190" height="120" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="125" y="78" text-anchor="middle">基础混合检索</text>
        <text x="125" y="104" text-anchor="middle" font-size="11" class="dim">单跳事实查询</text>
        <text x="125" y="124" text-anchor="middle" font-size="11" class="dim">问法相对规范</text>
        <text x="125" y="152" text-anchor="middle" font-size="11" class="accent-green">九成问题在这里解决</text>
        <rect x="235" y="52" width="190" height="120" rx="9" class="cell"/>
        <text x="330" y="78" text-anchor="middle">GraphRAG</text>
        <text x="330" y="104" text-anchor="middle" font-size="11" class="dim">关系密集 + 全局归纳</text>
        <text x="330" y="124" text-anchor="middle" font-size="11" class="dim">文档静态、价值高</text>
        <text x="330" y="152" text-anchor="middle" font-size="11" class="accent-orange">抽取成本高，慎上</text>
        <rect x="440" y="52" width="190" height="120" rx="9" class="cell"/>
        <text x="535" y="78" text-anchor="middle">Agentic RAG</text>
        <text x="535" y="104" text-anchor="middle" font-size="11" class="dim">多跳 + 需要调工具</text>
        <text x="535" y="124" text-anchor="middle" font-size="11" class="dim">延迟可以放宽</text>
        <text x="535" y="152" text-anchor="middle" font-size="11" class="accent-orange">要分级，别全量启用</text>
        <text x="30" y="200" font-size="11" class="dim">判断依据只有一个：badcase 库里有没有对应的提问类型</text>
      </g>
    </svg>
    <figcaption>图 11：三种方案的适用边界——先看 badcase 类型，再决定要不要升级</figcaption>
  </figure>

## 决策表

把前面的判断收成一张表，遇到具体需求时直接对照：

  <table>
    <tr><th>你的 badcase 长什么样</th><th>该做什么</th><th>不该做什么</th></tr>
    <tr><td>关键词搜不到、换个说法就失效</td><td>补 BM25、加查询改写</td><td>上 Agentic RAG</td></tr>
    <tr><td>答案缺半句、条款张冠李戴</td><td>回第 03 篇改切分</td><td>换 Embedding 模型</td></tr>
    <tr><td>要跨两三份文档才能答</td><td>多查询扩展 + 提升 Top-K，先试轻量方案</td><td>直接上 GraphRAG</td></tr>
    <tr><td>要问"整体上是什么情况"</td><td>GraphRAG，或预先跑一遍生成摘要/统计</td><td>加大 Top-K（取不到"全局答案"）</td></tr>
    <tr><td>要边查知识库边查业务数据库、还要算数</td><td>Agentic RAG + 工具调用</td><td>把数据导进知识库硬查</td></tr>
    <tr><td>该拒答的问了都敢答</td><td>改提示词约束 + 补"应拒答"评测题</td><td>加任何检索组件（治不了编造）</td></tr>
  </table>

注意最后一行：**编造问题不能靠检索组件解决**。它属于生成层的约束问题，加多少召回手段都没用——这也再次说明"先定位环节、再动手"（第 07 篇）比堆技术重要。

::: tip
进阶方案的正确引入方式是**被 badcase 推着走**，而不是被技术潮流拉着走。当你发现评测集里"需要多跳"的题目占比超过 10%，且轻量手段都试过了——那时候再上 Agentic RAG，才是有依据的决定。
:::

## 这个系列的路线回顾

十篇走完，回到第 01 篇那张图——五道关各有一篇对应，外加两个收口：

  <table>
    <tr><th>关卡</th><th>篇目</th><th>一句话结论</th></tr>
    <tr><td>数据接入</td><td>02</td><td>解析丢了的信息，后面再也补不回来</td></tr>
    <tr><td>切分</td><td>03</td><td>块单独拿出来读不懂，就是切错了</td></tr>
    <tr><td>检索</td><td>05 / 06 / 07</td><td>先建评测集，再逐层加召回与重排，靠 badcase 驱动</td></tr>
    <tr><td>权限</td><td>04 / 08</td><td>过滤必须在检索之前，且要能扛住绕过前端的调用</td></tr>
    <tr><td>维护</td><td>09</td><td>删除是最容易做漏的一环；用 hash 判重 + 别名原子切换</td></tr>
    <tr><td>验收</td><td>10</td><td>评测集是开发工具；上线先灰度、先给片段不给结论</td></tr>
    <tr><td>进阶</td><td>11</td><td>GraphRAG 与 Agentic RAG 由 badcase 决定，不由趋势决定</td></tr>
  </table>

如果只能记住一句话，就记这条：**企业知识库的效果上限，在你把文档喂进去之前就已经定了大半；它能不能持续变好，取决于你有没有一个每周在看 badcase 的闭环。** 技术选型的重要程度，远低于这两件事。

想看看别人是怎么做这些事、又能从哪里持续获取新进展？下一篇我们换个视角——去逛一圈值得长期关注的 AI 站点。
