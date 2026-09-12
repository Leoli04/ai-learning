---
title: RAG：开卷考试——给模型外挂一个知识库
---

# RAG：开卷考试——给模型外挂一个知识库

> 约 7 分钟 · 关键词：RAG、向量检索、Embedding、幻觉治理

## RAG 解决什么问题？

模型的三个天生缺陷：

  - **知识过期**：训练数据有截止日期，问"昨天的新闻"它只能瞎猜；
- **没有私有数据**：它没读过你公司的产品手册和数据库；
- **幻觉**：不知道的事，它会"编"一个听起来很像回事的答案。

**RAG（Retrieval-Augmented Generation，检索增强生成）**的思路朴素而有效：**别让模型背书，让它开卷考试**——先从你的知识库里查到相关资料，把资料塞进提示词，再让模型基于资料作答。

  <figure class="figure">
    <svg viewBox="0 0 720 360" xmlns="http://www.w3.org/2000/svg">
      <g font-size="13">
        <defs><marker id="ra" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#5b8cff"/></marker></defs>
        <!-- 离线入库 -->
        <text x="130" y="30" class="svg-dim" font-size="12">离线：建库（一次性）</text>
        <rect x="40" y="46" width="120" height="46" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="100" y="74" text-anchor="middle" class="svg-text" font-size="12">文档切分</text>
        <rect x="190" y="46" width="130" height="46" rx="9" fill="#161b22" stroke="#bc8cff"/>
        <text x="255" y="67" text-anchor="middle" class="svg-text" font-size="12">Embedding</text>
        <text x="255" y="83" text-anchor="middle" class="svg-dim" font-size="10">文本→向量</text>
        <rect x="350" y="46" width="140" height="46" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="420" y="74" text-anchor="middle" class="svg-text" font-size="12">向量数据库</text>
        <g stroke="#5b8cff" stroke-width="1.6" fill="none" marker-end="url(#ra)">
          <line x1="160" y1="69" x2="188" y2="69"/>
          <line x1="320" y1="69" x2="348" y2="69"/>
        </g>
        <!-- 在线问答 -->
        <text x="360" y="130" class="svg-dim" font-size="12">在线：每次提问都走这条链</text>
        <rect x="40" y="150" width="130" height="50" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="105" y="172" text-anchor="middle" class="svg-text" font-size="12">用户提问</text>
        <text x="105" y="189" text-anchor="middle" class="svg-dim" font-size="10">"报销标准是多少？"</text>
        <rect x="210" y="150" width="150" height="50" rx="9" fill="#161b22" stroke="#bc8cff"/>
        <text x="285" y="172" text-anchor="middle" class="svg-text" font-size="12">问题转向量</text>
        <text x="285" y="189" text-anchor="middle" class="svg-dim" font-size="10">在库里找最相似的段落</text>
        <rect x="400" y="150" width="140" height="50" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="470" y="172" text-anchor="middle" class="svg-text" font-size="12">取回 Top-K 段落</text>
        <text x="470" y="189" text-anchor="middle" class="svg-dim" font-size="10">塞进提示词</text>
        <rect x="580" y="150" width="110" height="50" rx="9" fill="rgba(91,140,255,0.10)" stroke="#5b8cff" stroke-width="2"/>
        <text x="635" y="172" text-anchor="middle" class="svg-text" font-size="12">LLM</text>
        <text x="635" y="189" text-anchor="middle" class="svg-dim" font-size="10">基于资料作答</text>
        <g stroke="#5b8cff" stroke-width="1.8" fill="none" marker-end="url(#ra)">
          <line x1="170" y1="175" x2="208" y2="175"/>
          <line x1="360" y1="175" x2="398" y2="175"/>
          <line x1="540" y1="175" x2="578" y2="175"/>
          <path d="M 420 96 C 420 130 350 130 295 148" marker-end="url(#ra)"/>
        </g>
        <!-- 答案 -->
        <rect x="200" y="250" width="320" height="60" rx="12" fill="rgba(63,185,80,0.08)" stroke="#3fb950"/>
        <text x="360" y="275" text-anchor="middle" class="svg-text" font-size="13">✅ 有据可依的回答 + 引用来源</text>
        <text x="360" y="296" text-anchor="middle" class="svg-dim" font-size="11">答不上来时说"资料里没有"，而不是编一个</text>
        <line x1="635" y1="200" x2="525" y2="248" stroke="#3fb950" stroke-width="1.8" marker-end="url(#ra)"/>
      </g>
    </svg>
    <figcaption>图 3：RAG 两阶段——离线建库 + 在线"检索→塞进提示词→作答"</figcaption>
  </figure>

## 两个关键词

### Embedding（向量化）

把一段文字变成一串数字（如 1024 维向量），**意思相近的文字，向量距离就近**。于是"找相关资料"就变成数学题：算向量夹角，取最近的几段。这就是**语义检索**——搜"报销"，能找到写着"差旅费管理办法"的文档，不需要关键词完全命中。

### 切分（Chunking）

文档要先切成合适大小的段落再入库。切太大：检索不准、占上下文；切太小：丢失上下文。这是 RAG 效果好坏的第一个分水岭。

  ::: tip
RAG = **先查后答**。它把"模型不知道"转化为"检索没检索到"——一个可以用工程手段持续优化的确定性问题。这也正是它成为企业落地 AI 第一站的原因：私有数据不出内网，答案可溯源。
:::

RAG 解决"知道什么"，但"能做什么"还差一步——下一篇：**Agent 与工具调用**。
