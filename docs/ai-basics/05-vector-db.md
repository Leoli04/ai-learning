---
title: 向量数据库与检索栈：RAG 的发动机舱
---

# 向量数据库与检索栈：RAG 的发动机舱

> 约 8 分钟 · 关键词：Embedding 模型、Chunking、ANN 索引、混合检索、Rerank

## 上一篇说 RAG"先查后答"，这一篇拆"查"这个动作

RAG 的效果好坏，八成取决于检索质量。一条完整的检索流水线如下，每个环节都有成熟技术：

  <figure class="figure">
    <svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg">
      <g font-size="12">
        <defs><marker id="va" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
        <text x="40" y="28" class="dim">① 切分 Chunking</text>
        <rect x="40" y="40" width="200" height="60" rx="9" class="cell"/>
        <text x="140" y="62" text-anchor="middle">文档 → 段落块</text>
        <text x="140" y="82" text-anchor="middle" font-size="11" class="dim">固定长度 / 递归 / 按语义边界</text>
        <text x="300" y="28" class="dim">② 向量化 Embedding</text>
        <rect x="300" y="40" width="200" height="60" rx="9" class="cell link-purple"/>
        <text x="400" y="62" text-anchor="middle">每个块 → 高维向量</text>
        <text x="400" y="82" text-anchor="middle" font-size="11" class="dim">bge / m3e / OpenAI text-embedding</text>
        <text x="560" y="28" class="dim">③ 建索引</text>
        <rect x="560" y="40" width="130" height="60" rx="9" class="cell"/>
        <text x="625" y="62" text-anchor="middle">向量数据库</text>
        <text x="625" y="82" text-anchor="middle" font-size="11" class="dim">Milvus / Qdrant / pgvector</text>
        <g stroke-width="1.8" marker-end="url(#va)" class="link">
          <line x1="240" y1="70" x2="298" y2="70"/>
          <line x1="500" y1="70" x2="558" y2="70"/>
        </g>
        <!-- 查询侧 -->
        <text x="40" y="150" class="dim">④ 查询（在线）</text>
        <rect x="40" y="162" width="130" height="52" rx="9" class="cell"/>
        <text x="105" y="184" text-anchor="middle">用户问题</text>
        <text x="105" y="202" text-anchor="middle" font-size="11" class="dim">同样转向量</text>
        <rect x="220" y="162" width="170" height="52" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="305" y="184" text-anchor="middle">ANN 近似最近邻搜索</text>
        <text x="305" y="202" text-anchor="middle" font-size="11" class="dim">HNSW / IVF，毫秒级取 Top-K</text>
        <rect x="440" y="162" width="120" height="52" rx="9" class="cell link-orange"/>
        <text x="500" y="184" text-anchor="middle">Rerank 重排</text>
        <text x="500" y="202" text-anchor="middle" font-size="11" class="dim">精排模型精选</text>
        <rect x="600" y="162" width="90" height="52" rx="9" class="cell-em link-green"/>
        <text x="645" y="192" text-anchor="middle">喂给 LLM</text>
        <g stroke-width="1.8" marker-end="url(#va)" class="link">
          <line x1="170" y1="188" x2="218" y2="188"/>
          <line x1="390" y1="188" x2="438" y2="188"/>
          <line x1="560" y1="188" x2="598" y2="188"/>
        </g>
        <text x="360" y="250" text-anchor="middle" font-size="11" class="dim">入库三步（离线、一次性）→ 查询四步（在线、每次提问）</text>
        <!-- 对比 -->
        <g font-size="11">
          <rect x="40" y="280" width="300" height="24" rx="5" class="cell link-green"/>
          <text x="190" y="296" text-anchor="middle">向量检索：懂语义，"报销"≈"差旅费办法"</text>
          <rect x="380" y="280" width="300" height="24" rx="5" class="cell"/>
          <text x="530" y="296" text-anchor="middle" class="dim">关键词 BM25：懂精确，型号/编号必须字对字</text>
          <rect x="40" y="312" width="640" height="52" rx="9" class="cell-em link-orange"/>
          <text x="360" y="334" text-anchor="middle" font-size="12">✅ 主流做法 = 混合检索：两路都查，结果合并（RRF），再交给 Rerank 精选</text>
          <text x="360" y="354" text-anchor="middle" font-size="11" class="dim">各补对方的短板：向量防"字对字搜不到"，关键词防"专有名词被稀释"</text>
        </g>
      </g>
    </svg>
    <figcaption>图 5：检索流水线——切分 → 向量化 → 建索引 → ANN 召回 → 重排 → 交付</figcaption>
  </figure>

## 四个关键技术点

### 1. ANN 索引：用"近似"换"速度"

百万级向量里逐一算距离（暴力搜索）太慢。**ANN（近似最近邻）**算法把向量组织成可快速导航的结构——最常用 **HNSW**（分层小世界图，像先走高速再走小路）和 **IVF**（先聚类分区，只在最近几个区里找）。牺牲一点点召回率，换来毫秒级响应。

### 2. 切分是效果的第一分水岭

主流策略：**递归切分**（先按段落、再按句子，带 10%~20% 重叠窗口防截断）、**按语义边界**（Embedding 相似度变化处下刀）、结构化文档按标题/表格整块切。切错了，后面全白搭。

### 3. 选型一览

  <table>
    <tr><th>产品</th><th>定位</th></tr>
    <tr><td><strong>FAISS</strong></td><td>Meta 的向量检索库（非数据库），原型验证首选</td></tr>
    <tr><td><strong>Chroma</strong></td><td>轻量嵌入式，学习/小项目开箱即用</td></tr>
    <tr><td><strong>pgvector</strong></td><td>PostgreSQL 插件——已有 PG 就别引入新组件</td></tr>
    <tr><td><strong>Milvus / Qdrant / Weaviate</strong></td><td>生产级专用向量库：分布式、标量过滤、混合检索齐全</td></tr>
  </table>

### 4. 进阶方向

  - **Agentic RAG**：让 Agent 决定"查不查、查什么、查几轮"，检索本身成为工具调用；
- **GraphRAG**：抽取实体关系建知识图谱，回答"跨文档、多跳"问题（如"A 公司的供应商的母公司是谁"）。

  ::: tip
检索栈五件套——**切分定上限、Embedding 定语义、ANN 定速度、混合检索补短板、Rerank 定精度**。RAG 效果不好时，按这个顺序逐层排查。
:::

知识问题解决完，接下来是让模型"动手"——下一篇：**Agent 核心范式**。
