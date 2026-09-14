---
title: 混合检索：BM25 + 向量 + Rerank 三件套
---

# 混合检索：BM25 + 向量 + Rerank 三件套

> 约 10 分钟 · 关键词：BM25、混合检索、RRF、Rerank

## 纯向量检索的两个盲区

Embedding 模型很强，但它有两类事情天生做不好：

  1. **精确标识符**：合同编号 `HT-2024-0871`、产品型号 `FG-2200B`、工单号、员工工号。这些字符串的"语义"就是它本身，而向量化会把它们编码成一堆相似的模式——**不同编号在向量空间里离得很近，根本分不开**。
  2. **训练语料里没有的词**：新产品的名字、内部项目代号、行业内的特有缩写。模型没见过，编码质量自然差。

反过来，传统的关键词检索（BM25）有完全对称的盲区：**用户说"报销上限"，文档写"差旅标准"，一个词都不重合，BM25 得零分。**

所以这不是"新方法取代旧方法"的故事——**两者互补，且互补得很彻底**：

  <table>
    <tr><th>对比项</th><th>BM25（关键词）</th><th>向量（语义）</th></tr>
    <tr><td>匹配依据</td><td>词是否出现、出现频率、词有多罕见</td><td>两段文字在高维空间里的距离</td></tr>
    <tr><td>擅长</td><td>编号、专名、术语、精确短语</td><td>同义改写、口语化提问、跨表述的语义</td></tr>
    <tr><td>短板</td><td>换个说法就搜不到</td><td>精确字符串分不开、生僻词编码差</td></tr>
    <tr><td>可解释性</td><td>高（能指出命中哪个词）</td><td>低（只能说"像"）</td></tr>
    <tr><td>成本</td><td>极低，几乎零延迟</td><td>需要向量化 + ANN 索引</td></tr>
  </table>

企业场景里两者的需求都很硬：员工既会问"年假怎么算"（语义），也会问"HT-2024-0871 这个合同什么情况"（精确）。**只上一种，另一半问题就永远答不好。**

## 合起来用：先并行召回，再融合

  <figure class="figure">
    <svg viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a6" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <rect x="30" y="58" width="110" height="52" rx="9" class="cell"/>
        <text x="85" y="84" text-anchor="middle">用户问题</text>
        <text x="85" y="101" text-anchor="middle" font-size="11" class="dim">原样出发</text>
        <path d="M 140 84 L 160 84 L 160 46 L 186 46" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 140 84 L 160 84 L 160 122 L 186 122" fill="none" stroke-width="1.5" class="link-dim"/>
        <rect x="190" y="20" width="150" height="52" rx="9" class="cell link-green"/>
        <text x="265" y="42" text-anchor="middle">BM25 · 关键词</text>
        <text x="265" y="60" text-anchor="middle" font-size="11" class="dim">取 Top-20</text>
        <rect x="190" y="96" width="150" height="52" rx="9" class="cell link-purple"/>
        <text x="265" y="118" text-anchor="middle">向量 · 语义</text>
        <text x="265" y="136" text-anchor="middle" font-size="11" class="dim">取 Top-20</text>
        <path d="M 340 46 L 360 46 L 360 84" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 340 122 L 360 122 L 360 84" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 360 84 L 376 84" fill="none" stroke-width="1.8" marker-end="url(#a6)" class="link"/>
        <rect x="380" y="58" width="120" height="52" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="440" y="80" text-anchor="middle">RRF 融合</text>
        <text x="440" y="98" text-anchor="middle" font-size="11" class="dim">合并去重 → 30</text>
        <path d="M 500 84 L 526 84" fill="none" stroke-width="1.8" marker-end="url(#a6)" class="link"/>
        <rect x="530" y="58" width="110" height="52" rx="9" class="cell link-orange"/>
        <text x="585" y="80" text-anchor="middle">Rerank</text>
        <text x="585" y="98" text-anchor="middle" font-size="11" class="dim">精排 → Top-5</text>
        <text x="30" y="178" font-size="11" class="dim">两路并行召回，按排名融合而不调分数尺度；Rerank 只处理 30 条，延迟可控</text>
      </g>
    </svg>
    <figcaption>图 6：混合检索管道——并行召回、排名融合、最后精排</figcaption>
  </figure>

## 融合方式：为什么推荐 RRF

两路结果的分数不能直接相加，因为**尺度不一样**：BM25 的分数没有上界（几到几十都有可能），向量相似度通常在 0～1 之间（且不同模型的分布还不同）。硬要加权，就得先归一化——而归一化参数会随着查询变化，很难调稳。

RRF（Reciprocal Rank Fusion，倒数排名融合）绕开了这个问题：**它完全不用分数，只看排名。**

  <table>
    <tr><th>方式</th><th>做法</th><th>优点</th><th>缺点</th></tr>
    <tr><td>加权求和</td><td>归一化两边分数后按权重相加</td><td>理论上更精细</td><td>权重和归一化方式都要调，换数据就失效</td></tr>
    <tr><td><strong>RRF</strong></td><td>每个结果得分为 <code>1 / (k + 排名)</code>，两路得分相加（k 常取 60）</td><td>无需调参、鲁棒、跨引擎通用</td><td>丢掉了分数差距的信息</td></tr>
    <tr><td>各取 Top-N 合并去重</td><td>简单拼起来</td><td>实现最简单</td><td>没有真正的排序逻辑</td></tr>
  </table>

RRF 有个副作用要预期到：某条内容只要在两路里都排进前 20，它的融合得分就会很高，于是"两边都认可"的内容被推到前面。这在多数场景里是好事（一致性即置信度），但如果你明确希望偏向语义结果，就需要给两路设不同的 k 值来微调。

## Rerank：把最强的模型放在最后一步

Rerank 是这套管道里效果提升最明显的一环，原因是它的计算方式更"奢侈"：

  <table>
    <tr><th></th><th>双塔模型（Embedding）</th><th>交叉编码器（Rerank）</th></tr>
    <tr><td>怎么算</td><td>query 和文档<strong>分别</strong>编码成向量，再算距离</td><td>query 和文档<strong>拼在一起</strong>送进模型，直接输出相关度</td></tr>
    <tr><td>能否预计算</td><td>能——文档向量可以离线算好</td><td>不能——每次查询都要重算</td></tr>
    <tr><td>速度</td><td>快（毫秒级）</td><td>慢（与候选数成正比）</td></tr>
    <tr><td>准确度</td><td>较好</td><td>更好（能看到两边的交互）</td></tr>
  </table>

正因为"慢"，它不能用来搜全库，只能用来**给前面的候选重新排序**。这也决定了它的位置在管道最后：召回 20+20 → 融合 30 → **rerank 这 30 条** → 取前 5 喂给模型。这个规模的 rerank 通常增加几十到几百毫秒，属于可接受的成本。

## 一套可以直接抄的默认配置

  1. 查询**不做改写**，原样分发给两路（改写在下一篇讲，先跑通基线）；
  2. BM25 取 **Top-20**、向量取 **Top-20**（取 20 而不是 10，是为了给融合留出空间）；
  3. **RRF 融合**，k 取 60，合并去重后保留 30 条；
  4. **Rerank 这 30 条**，取前 5 条；
  5. 把 5 条连同来源元数据（文件名、页码、章节）一起拼进提示词。

延迟预算大致是：BM25 几毫秒 → 向量检索几十毫秒 → RRF 可忽略 → Rerank 几十到几百毫秒。**总耗时基本由 Rerank 决定**，所以它也是调优时第一个该考虑降级的地方（比如只对前 15 条做重排）。

## 什么时候不需要这么复杂

混合检索不是教条。以下情况可以省掉某些环节：

  <table>
    <tr><th>场景</th><th>可以省掉</th><th>原因</th></tr>
    <tr><td>小库 + 问法规范</td><td>Rerank</td><td>候选本来就只有几十条，精排收益小</td></tr>
    <tr><td>纯语义查询为主（总结、归纳）</td><td>BM25 那一整路</td><td>没有精确匹配需求，关键词路只会引入噪声</td></tr>
    <tr><td>延迟极度敏感（语音实时对话）</td><td>Rerank 或降级为小模型</td><td>几百毫秒的延迟在语音场景里很致命</td></tr>
    <tr><td>冷启动阶段</td><td>Rerank，用规则打分替代</td><td>先跑通链路拿到 badcase，再加环节</td></tr>
  </table>

::: tip
判断要不要加一个环节，永远问同一个问题：**它能解决我评测集里的哪几条 badcase？** 评测集里没有对应问题的环节，加了只是增加延迟和故障面。这也是下一篇要讲的——没有 badcase 库，你根本不知道该加什么。
:::

管道搭好了，但"召回了却排不到前面"依然常见。下一步是让查询本身变得更聪明，并建立一套能持续改进的闭环——下一篇：**检索调优：查询改写、多路召回与 badcase 闭环**。
