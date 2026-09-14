---
title: Embedding 选型：中文场景怎么挑模型
---

# Embedding 选型：中文场景怎么挑模型

> 约 9 分钟 · 关键词：Embedding、中文语义、维度成本、索引迁移

## 它决定了召回的上限

Embedding 模型把文本变成向量，检索就是在这个向量空间里找"离得近"的邻居。它有个特点：**只要选错了，后面所有环节都补不回来**。

原因在于，检索的本质是"算距离"。如果模型没把"报销上限"和"差旅标准"放到相近的位置，那么无论后面的 Rerank 多强、模型多聪明，这段内容都不会进入候选集——它在第一道筛子里就被淘汰了。Rerank 只能在"已经召回的候选"里重新排序，救不了没被召回的东西。

所以第 04 篇讲过滤、这一篇讲召回，两者共同决定了上游的天花板；下游的生成模型只能在这个天花板之下发挥。

## 中文场景要看五个维度

通用榜单的分数不能直接搬过来用，中文企业文档有它的特殊性：

  <table>
    <tr><th>维度</th><th>为什么重要</th><th>怎么确认</th></tr>
    <tr><td><strong>中文语义能力</strong></td><td>简称、成语、行业黑话、同义改写，中文的"近义"比英文更依赖训练语料</td><td>拿本行业的同义问法实测，别用通用句子</td></tr>
    <tr><td><strong>最长输入长度</strong></td><td>模型有上下文上限，超过就被截断——这直接限制了你 chunk 能切多大</td><td>查文档确认；注意"支持 8k"有时指模型能力而非训练时见过</td></tr>
    <tr><td><strong>是否区分 query / passage</strong></td><td>不少模型要求检索时给查询加前缀（如 <code>query: </code>），入库时不加或加另一种</td><td>看模型卡说明；加错前缀会明显掉效果且很难排查</td></tr>
    <tr><td><strong>向量维度</strong></td><td>决定存储成本和检索速度，不是越高越好</td><td>算一下你的规模能不能承受（见下节）</td></tr>
    <tr><td><strong>部署方式</strong></td><td>数据能不能出内网，直接砍掉一半候选</td><td>先问合规，再谈效果</td></tr>
  </table>

## 先过合规，再过实测

选型流程不要从"哪个效果最好"开始，而是从"哪些我根本没得选"开始：

  <figure class="figure">
    <svg viewBox="0 0 720 350" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a5" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <rect x="250" y="32" width="220" height="44" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="360" y="59" text-anchor="middle">文档数据能出企业内网吗？</text>
        <path d="M 360 76 L 360 96 L 210 96 L 210 114" fill="none" stroke-width="1.5" class="link-dim"/>
        <text x="222" y="92" font-size="11" class="dim">不能</text>
        <path d="M 360 76 L 360 96 L 510 96 L 510 114" fill="none" stroke-width="1.5" class="link-dim"/>
        <text x="522" y="92" font-size="11" class="dim">能</text>
        <rect x="90" y="118" width="240" height="52" rx="9" class="cell"/>
        <text x="210" y="140" text-anchor="middle">只能本地部署</text>
        <text x="210" y="158" text-anchor="middle" font-size="11" class="dim">显存与 CPU 决定可选范围</text>
        <rect x="390" y="118" width="240" height="52" rx="9" class="cell"/>
        <text x="510" y="140" text-anchor="middle">API 或本地都可以</text>
        <text x="510" y="158" text-anchor="middle" font-size="11" class="dim">按成本、延迟、数据边界权衡</text>
        <path d="M 210 170 L 210 190 L 360 190 L 360 200" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 510 170 L 510 190 L 360 190" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 360 190 L 360 200" fill="none" stroke-width="1.8" marker-end="url(#a5)" class="link"/>
        <rect x="210" y="204" width="300" height="44" rx="9" class="cell link-green"/>
        <text x="360" y="231" text-anchor="middle">用你自己的评测集实测召回率</text>
        <path d="M 360 248 L 360 276" fill="none" stroke-width="1.8" marker-end="url(#a5)" class="link"/>
        <rect x="210" y="280" width="300" height="44" rx="9" class="cell"/>
        <text x="360" y="307" text-anchor="middle">定模型 + 定维度，冻结版本号</text>
      </g>
    </svg>
    <figcaption>图 5：选型顺序——先被合规砍一刀，再用自己的数据实测，最后才是成本与延迟</figcaption>
  </figure>

第二步"用你自己的评测集实测"是关键，也是最容易被跳过的一步。做法很直接：

  1. 从真实文档里挑 **200~300 个 chunk**，覆盖各类文档；
  2. 人工写 **50 条真实问法**（要包含口语化、缩写、跨章节的提问），并标出每条问题**应该命中哪个 chunk**；
  3. 用 3~5 个候选模型分别跑一遍，比较 **Recall@10**（正确答案有没有进前 10）；
  4. 只有回到第 1 步时才发现问题——**这个评测集会一直用到最后一篇**。

**榜单分数和你的实际效果的相关系数，远低于你的直觉。** 因为榜单测的是通用语料，而你的库里有大量行业术语、内部简称、ERP 里的字段名。

## 维度不是越高越好

维度决定了向量占多少空间。算一下就知道为什么要在意：

  <table>
    <tr><th>规模</th><th>1024 维 float32</th><th>1024 维 int8 量化</th></tr>
    <tr><td>10 万 chunk</td><td>约 400 MB</td><td>约 100 MB</td></tr>
    <tr><td>100 万 chunk</td><td>约 3.8 GB</td><td>约 1 GB</td></tr>
    <tr><td>1000 万 chunk</td><td>约 38 GB</td><td>约 10 GB</td></tr>
  </table>

（算法：`向量数 × 维度 × 每维字节数`，float32 每维 4 字节、int8 每维 1 字节。真实占用还要加上索引结构本身的开销。）

这张表说明两件事：一是**大部分企业知识库在几十万 chunk 的量级，1024 维完全够用**，不必追求 3072 维的"最强模型"；二是**量化能把成本降一个数量级**，而召回率通常只掉一两个点——这个取舍在存储吃紧时非常划算。

另外值得留意的是**支持降维的模型**（如 Matryoshka 结构）：同一个模型可以只取前 256 维使用，效果下降有限，但存储和检索速度明显变好。这让"先定模型、后调维度"成为可能。

## 换模型的代价：全量重建

这是选型时最该记住的一条：**更换 Embedding 模型 = 全量重新嵌入 + 重建索引**。

向量空间是模型专属的——A 模型产出的向量和 B 模型产出的向量放在一起算距离，结果没有意义。所以一旦上线后要换模型，就得把全部文档重新跑一遍，而且在这期间新旧两套索引不能混用。

这带来两个实务建议：

  1. **上线前就把模型定死**，把评测集跑扎实，别抱着"先用着，不好再换"的心态；
  2. 架构上**把 Embedding 调用抽象成一个接口**（输入文本、输出向量），并在元数据里记录 `embedding_model` 和 `embedding_version`。真到要换的那天，你能按版本分批重建，而不是全库黑屏。

::: tip
选 Embedding 模型有个反直觉的结论：**在中文企业场景里，"选一个中等偏上、稳定、能本地部署"的模型，通常比"选榜单第一但调用受限"的模型效果更好。** 因为前者你能随时重跑、随时调参、随时补数据，而后者受制于别人的配额和版本变更。
:::

有了语义检索还不够——合同编号、产品型号、人名这类精确匹配，向量天生不擅长。下一篇：**混合检索：BM25 + 向量 + Rerank 三件套**。
