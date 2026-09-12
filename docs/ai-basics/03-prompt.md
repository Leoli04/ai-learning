---
title: Prompt 工程与上下文学习：不训练，也能"教"模型
---

# Prompt 工程与上下文学习：不训练，也能"教"模型

> 约 6 分钟 · 关键词：Zero/Few-shot、CoT、上下文学习

## 最省钱的能力获取方式

想让模型干一件新的事，通常有三条路，成本天差地别：

  1. **重新训练**：几百万到几亿，只有大厂玩得起；
2. **微调（Fine-tuning）**：几千到几万，改模型的"参数"；
3. **Prompt（提示词）**：几乎免费——不改参数，只在**输入上下文里做文章**。

第三条路有效的原因是 GPT-3 论文命名的现象：**上下文学习（In-Context Learning, ICL）**——模型在提示里看到几个例子，就能"现学现卖"，即使参数一个都没改。

  <figure class="figure">
    <svg viewBox="0 0 720 340" xmlns="http://www.w3.org/2000/svg">
      <g font-size="13">
        <!-- 上下文长条 -->
        <rect x="40" y="40" width="640" height="90" rx="12" stroke-width="2" class="cell-em link"/>
        <text x="360" y="64" text-anchor="middle" font-weight="bold">模型一次看到的"上下文窗口"</text>
        <rect x="60" y="80" width="130" height="34" rx="7" class="cell"/>
        <text x="125" y="102" text-anchor="middle" font-size="12">系统指令</text>
        <rect x="205" y="80" width="130" height="34" rx="7" class="cell link-green"/>
        <text x="270" y="102" text-anchor="middle" font-size="12">示例（few-shot）</text>
        <rect x="350" y="80" width="130" height="34" rx="7" class="cell link-purple"/>
        <text x="415" y="102" text-anchor="middle" font-size="12">检索到的资料</text>
        <rect x="495" y="80" width="165" height="34" rx="7" class="cell link-orange"/>
        <text x="577" y="102" text-anchor="middle" font-size="12">用户当前的问题</text>
        <!-- 三种技巧 -->
        <rect x="40" y="170" width="195" height="120" rx="12" class="cell"/>
        <text x="137" y="200" text-anchor="middle" font-weight="bold">Zero-shot</text>
        <text x="137" y="226" text-anchor="middle" font-size="12" class="dim">只给指令不给例子</text>
        <text x="137" y="250" text-anchor="middle" font-size="12" class="dim">"把这些评论分类为好评/差评"</text>
        <rect x="262" y="170" width="195" height="120" rx="12" class="cell"/>
        <text x="360" y="200" text-anchor="middle" font-weight="bold">Few-shot</text>
        <text x="360" y="226" text-anchor="middle" font-size="12" class="dim">给 3~5 个输入→输出示例</text>
        <text x="360" y="250" text-anchor="middle" font-size="12" class="dim">模型模仿例子的格式与标准</text>
        <rect x="484" y="170" width="195" height="120" rx="12" class="cell"/>
        <text x="581" y="200" text-anchor="middle" font-weight="bold">CoT 思维链</text>
        <text x="581" y="226" text-anchor="middle" font-size="12" class="dim">"请一步步思考再回答"</text>
        <text x="581" y="250" text-anchor="middle" font-size="12" class="dim">把推理摊开，正确率明显提升</text>
        <line x1="360" y1="130" x2="360" y2="166" stroke-width="2" class="link"/>
        <polygon points="360,170 355,160 365,160" fill="#5b8cff"/>
      </g>
    </svg>
    <figcaption>图 2：上下文 = 指令 + 示例 + 资料 + 问题；三种经典写法由弱到强</figcaption>
  </figure>

## 几条最划算的 Prompt 实践

  - **给角色**："你是一名资深 Java 后端工程师"——比直接提问效果好；
- **给例子**：格式类任务（抽取、分类、转 JSON）放 2~3 个示例，比千言万语都管用；
- **给步骤**：复杂推理要求"先列出步骤，再给答案"（思维链）；
- **给约束**：明确"不确定就说不知道，不要编造"——虽然不能根除幻觉，但能显著减少。

  ::: warning
上下文窗口装不下整个公司文档库，模型也记不住两次会话之间的约定。而且不管 Prompt 写得多好，**模型仍可能一本正经地编造**。这两个问题分别催生了下一篇的 **RAG** 和后面要讲的**记忆机制**。
:::
