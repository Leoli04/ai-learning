---
title: 进阶 RAG：从"查得到"到"查得准"
---

# 进阶 RAG：从"查得到"到"查得准"

> 约 10 分钟 · 关键词：查询改写、Agentic RAG、GraphRAG、多跳

## 基础 RAG 的三个漏点

第 4、5 篇把标准流水线走了一遍：切分、Embedding、ANN 索引、混合检索、Rerank。全做了，效果还是不稳，通常卡在这三类问题上：

  1. **问法 ≠ 文档说法**：用户问"报销最多能报多少"，文档里写的是"差旅费管理办法第三十二条"。专有名词、缩写、指代一多，向量相似度也救不回来。
2. **一次检索只够一跳**：问"我们对接的那家供应商，它的母公司去年营收多少"——得先查供应商是谁，再查母公司，再查财报，一次性检索抓不全。
3. **全局性问题没有"答案所在段"**："这批合同的主要风险点是什么""本季度客诉集中在哪几类"——答案不在任何一段里，而在整片的统计和归纳里，Top-K 再怎么取也取不到。

对应的三招，从便宜到昂贵。

## 第一招：查询改写与路由

同一件事，用户和文档用的是两套词。改写就是在检索前先做一层"翻译"：

  <table>
    <tr><th>手段</th><th>做法</th><th>适合</th></tr>
    <tr><td><strong>同义扩展</strong></td><td>把口语问法改写成文档里的术语和全称</td><td>术语、缩写、行话多的库</td></tr>
    <tr><td><strong>多查询扩展</strong></td><td>一个问题改写成 3~5 个子查询，分别检索后合并去重</td><td>问得笼统、一个查询覆盖不全</td></tr>
    <tr><td><strong>HyDE</strong></td><td>先让模型"假设一个答案"，再拿这段假设去检索</td><td>问题和文档表述风格差异大</td></tr>
    <tr><td><strong>查询路由</strong></td><td>先判断该查哪个库，或者根本不需要查</td><td>多知识库、含闲聊与寒暄的入口</td></tr>
  </table>

核心原则一句话：**改写要让查询说"文档的语言"，而不是"用户的语言"。**

## 第二招：把检索交给 Agent

  <figure class="figure">
    <svg viewBox="0 0 720 268" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a16" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <text x="30" y="24" class="dim">基础 RAG：一次检索定生死</text>
        <rect x="30" y="36" width="140" height="52" rx="9" class="cell"/>
        <text x="100" y="58" text-anchor="middle">用户问题</text>
        <text x="100" y="76" text-anchor="middle" font-size="11" class="dim">原样直接查</text>
        <rect x="200" y="36" width="140" height="52" rx="9" class="cell"/>
        <text x="270" y="58" text-anchor="middle">检索一次</text>
        <text x="270" y="76" text-anchor="middle" font-size="11" class="dim">取 Top-K</text>
        <rect x="370" y="36" width="140" height="52" rx="9" class="cell"/>
        <text x="440" y="58" text-anchor="middle">塞进提示词</text>
        <text x="440" y="76" text-anchor="middle" font-size="11" class="dim">一次机会</text>
        <rect x="540" y="36" width="140" height="52" rx="9" class="cell"/>
        <text x="610" y="58" text-anchor="middle">作答</text>
        <text x="610" y="76" text-anchor="middle" font-size="11" class="dim">资料不足也只能编</text>
        <g stroke-width="1.8" marker-end="url(#a16)" class="link">
          <line x1="170" y1="62" x2="196" y2="62"/>
          <line x1="340" y1="62" x2="366" y2="62"/>
          <line x1="510" y1="62" x2="536" y2="62"/>
        </g>
        <text x="30" y="112" font-size="11" class="dim">漏点：问法对不上、需要多跳、以及"答案不落在任何一段"的全局性问题</text>
        <text x="30" y="146" class="dim">Agentic RAG：检索变成工具，查几轮由模型自己判断</text>
        <rect x="30" y="158" width="130" height="52" rx="9" class="cell"/>
        <text x="95" y="188" text-anchor="middle">用户问题</text>
        <rect x="195" y="158" width="170" height="52" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="280" y="180" text-anchor="middle">Agent 决定查什么</text>
        <text x="280" y="198" text-anchor="middle" font-size="11" class="dim">选库 / 改写法 / 拆子问题</text>
        <rect x="400" y="158" width="140" height="52" rx="9" class="cell link-green"/>
        <text x="470" y="180" text-anchor="middle">检索并判读</text>
        <text x="470" y="198" text-anchor="middle" font-size="11" class="dim">够不够？缺什么？</text>
        <rect x="575" y="158" width="115" height="52" rx="9" class="cell link-orange"/>
        <text x="632" y="188" text-anchor="middle">作答</text>
        <g stroke-width="1.8" marker-end="url(#a16)" class="link">
          <line x1="160" y1="184" x2="191" y2="184"/>
          <line x1="365" y1="184" x2="396" y2="184"/>
        </g>
        <line x1="540" y1="184" x2="571" y2="184" stroke-width="1.8" marker-end="url(#a16)" class="link-orange"/>
        <path d="M 470 210 C 470 240 280 240 280 214" fill="none" stroke-width="1.8" marker-end="url(#a16)" class="link-orange"/>
        <text x="375" y="256" text-anchor="middle" font-size="11" class="dim">不够就再来一轮：改写查询、换个库、拆成子问题</text>
      </g>
    </svg>
    <figcaption>图 16：单跳 RAG vs Agentic RAG——后者自己决定查几轮、怎么查</figcaption>
  </figure>

做法是把检索包装成工具交给 Agent：它先判断"这个问题我需要查什么"，查完读一遍结果，发现不够就改写查询再查一轮，凑齐了才作答。这一步顺带解决了前两个漏点——改写、多跳都变成了循环里的自然动作。

代价也很实在：**延迟和成本成倍上涨**（一次问答可能变成五六次模型调用），而且链路不再确定，出问题更难复现。所以务实的做法是分级：简单问题走单跳，命中某些特征（含多个实体、含比较/归因词、检索得分偏低）才升级到多轮。

## 第三招：GraphRAG，把文档变成关系网

处理"全局性问题"的思路完全不同——**先把知识库变成一张关系图，再在图上做归纳**：

  1. 用 LLM 从文档里抽取**实体和关系**（公司、人、产品、条款，以及它们之间的从属、供应、引用关系）；
2. 把这些点连成图，对图做**社区划分**，为每个社区生成一段摘要；
3. 回答时先看社区摘要定位"大方向"，再顺着关系链追到具体节点。

它擅长的是两类问题："谁属于谁、谁和谁有关"（多跳），以及"整体上看主要是什么情况"（全局归纳）。

代价同样明显：抽取要额外跑一遍 LLM（一次性成本高）、图需要维护更新、实现复杂度远高于向量检索。所以它适合**静态、高价值**的知识库（法规、合同、行业研究报告），不适合每天变动的日志类数据。

## 效果不好时，按这个顺序排查

  <table>
    <tr><th>症状</th><th>先查哪里</th></tr>
    <tr><td>关键词搜得到，语义搜不到</td><td>Embedding 模型选型、是否上了混合检索</td></tr>
    <tr><td>该有的段落压根没被召回</td><td>切分策略 → Top-K → 查询改写</td></tr>
    <tr><td>召回了，但答案没用上</td><td>Rerank、片段在上下文里的顺序、强制引用来源</td></tr>
    <tr><td>问法绕、一句话里好几个问题</td><td>查询改写、多查询扩展</td></tr>
    <tr><td>要跨文档、要全局结论</td><td>GraphRAG、或预先跑一遍生成摘要</td></tr>
  </table>

::: tip
RAG 的功夫不在"接一个向量库"，而在**分层排查**：切分 → 改写 → 混合检索 → 重排 → 多跳。越靠前的环节越便宜，越靠后的越贵——所以永远从便宜的开始查。
:::

到这里讲的都是"文字"。但真实用户更想张嘴直接问——下一篇：**语音栈：让 AI 能听会说**。
