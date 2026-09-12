---
title: 大模型这几年：一条时间线看懂范式转移
---

# 大模型这几年：一条时间线看懂范式转移

> 约 7 分钟 · 关键词：Transformer、GPT 时刻、范式转移

## 八年，三次"换脑子"

2017 年之前，AI 还是"一个任务一个模型"：识别图片是一个模型，翻译是另一个模型，互不相通。2017 年 Google 发表论文《Attention Is All You Need》，提出 **Transformer** 架构——它的核心思想是**注意力机制**：处理每个词时，同时"看到"上下文里所有词，并给重要的词更高权重。

关键是：Transformer 是**通用的**。同一个架构，喂文本就懂语言，喂图片就懂视觉，喂代码就懂编程。之后的发展，本质上是"同一条路越走越宽"：

  <figure class="figure">
    <svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg">
      <g font-size="13">
        <line x1="60" y1="40" x2="60" y2="370" stroke-width="2" class="cell"/>
        <!-- 2017 -->
        <circle cx="60" cy="60" r="5" class="accent-blue-fill"/>
        <text x="80" y="55" font-weight="bold">2017 · Transformer</text>
        <text x="80" y="72" class="dim">注意力机制，统一架构的起点</text>
        <!-- 2018-2020 -->
        <circle cx="60" cy="110" r="5" class="accent-blue-fill"/>
        <text x="80" y="105" font-weight="bold">2018–2020 · 预训练时代</text>
        <text x="80" y="122" class="dim">BERT / GPT：先海量阅读，再微调；GPT-3 证明"大就是不同"</text>
        <!-- 2022 -->
        <circle cx="60" cy="165" r="5" class="accent-orange-fill"/>
        <text x="80" y="160" font-weight="bold">2022.11 · ChatGPT 时刻</text>
        <text x="80" y="177" class="dim">对话即产品，两个月一亿用户；RLHF 对齐走进大众视野</text>
        <!-- 2023 -->
        <circle cx="60" cy="220" r="5" class="accent-green-fill"/>
        <text x="80" y="215" font-weight="bold">2023 · 外挂与工具年</text>
        <text x="80" y="232" class="dim">GPT-4 + Function Calling + RAG 爆发：模型开始"动手"和"查资料"</text>
        <!-- 2024 -->
        <circle cx="60" cy="275" r="5" class="accent-purple-fill"/>
        <text x="80" y="270" font-weight="bold">2024 · 推理与协议年</text>
        <text x="80" y="287" class="dim">o1 / DeepSeek-R1（思考链推理）；MCP 协议统一工具接口</text>
        <!-- 2025+ -->
        <circle cx="60" cy="330" r="5" class="accent-red-fill"/>
        <text x="80" y="325" font-weight="bold">2025+ · Agent 时代</text>
        <text x="80" y="342" class="dim">编码 Agent、开源 Harness、Skill / 多 Agent 协作成为主线</text>
        <text x="640" y="380" font-size="11" class="dim">自下而上：能力越来越强，离"干活"越来越近</text>
      </g>
    </svg>
    <figcaption>图 1：大模型发展时间线——从"会聊天"到"会干活"</figcaption>
  </figure>

## 三次范式转移，各解决一个死结

  1. **预训练（2018–2020）**：解决"数据不够"。先在互联网规模的海量文本上自监督学习（猜下一个词），少量标注数据微调即可用——从此 AI 能力随数据和算力**可扩展**。
2. **对齐与对话（2022）**：解决"能力有了但不好用"。RLHF（人类反馈强化学习）让模型学会"像助手一样回答人话"，ChatGPT 因此出圈。
3. **外挂生态（2023 至今）**：解决"模型本身做不到的"。知识会过期、没有私有数据、不能操作软件——于是 RAG 外挂知识、Function Calling 外挂工具、Agent 框架外挂执行力。模型从"大脑"变成"大脑 + 手脚 + 图书馆"。

  ::: tip
这几年 AI 的主线不是"一个更强的模型"，而是**模型不动，外挂不停**——RAG 补知识、工具补手脚、Skill 补经验、编排补流程。后面几篇就挨个拆这些外挂。
:::
