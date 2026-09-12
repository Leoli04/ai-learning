---
title: 微调与对齐：Prompt 搞不定时，动模型的参数
---

# 微调与对齐：Prompt 搞不定时，动模型的参数

> 约 8 分钟 · 关键词：SFT、LoRA / QLoRA、RLHF / DPO、蒸馏

## 什么时候才需要微调？

先把最重要的决策表放在前面——**大部分场景不该微调**：

  <table>
    <tr><th>需求</th><th>正确手段</th></tr>
    <tr><td>补充知识（文档、产品信息）</td><td>✅ RAG（知识可更新、可溯源）</td></tr>
    <tr><td>固定输出格式 / JSON</td><td>✅ Prompt + Few-shot + JSON Mode</td></tr>
    <tr><td>稳定的语气风格 / 领域话术（医疗、法律）</td><td>✅ 微调（把风格"焊"进参数）</td></tr>
    <tr><td>小模型学会特定任务、省推理成本</td><td>✅ 微调 + 蒸馏</td></tr>
  </table>

口诀：**知识用 RAG，风格靠微调**。知识天天变，塞参数里就"过期"；风格相对稳定，才值得烧训练费。

## LoRA：微调界的"贴膜"革命

全参微调一个 70B 模型要几百 GB 显存，个人和企业玩不起。**2021 年的 LoRA** 彻底改变了这件事：

  - **思路**：冻结原模型全部权重，只在旁边加一对很小的"低秩矩阵"（记作 B×A）承载学习内容。原权重 W 不动，实际使用时是 `W + B×A`；
- **代价**：可训练参数量降到原来的 0.1%~1%，单卡消费级显卡也能微调；
- **额外红利**：一个底座模型 + 多个几十 MB 的 LoRA 适配器 = 按需切换的"模型皮肤"，拔掉适配器，底座毫发无损；
- **QLoRA**：把底座再量化到 4bit 加载，显存进一步砍到几分之一——2023 年后开源社区微调爆发的直接推手。

  <figure class="figure">
    <svg viewBox="0 0 720 280" xmlns="http://www.w3.org/2000/svg">
      <g font-size="12">
        <rect x="60" y="60" width="220" height="120" rx="12" fill="#161b22" stroke="#30363d"/>
        <text x="170" y="100" text-anchor="middle" class="svg-text" font-weight="bold">底座模型 W</text>
        <text x="170" y="126" text-anchor="middle" class="svg-dim">❄️ 全部冻结（不训练）</text>
        <text x="170" y="150" text-anchor="middle" class="svg-dim">几十 GB，共享复用</text>
        <rect x="420" y="46" width="220" height="52" rx="10" fill="rgba(91,140,255,0.10)" stroke="#5b8cff" stroke-width="2"/>
        <text x="530" y="68" text-anchor="middle" class="svg-text">B 矩阵 + A 矩阵</text>
        <text x="530" y="86" text-anchor="middle" class="svg-dim" font-size="11">🔥 唯一被训练的部分（几十 MB）</text>
        <rect x="420" y="140" width="220" height="40" rx="10" fill="rgba(63,185,80,0.08)" stroke="#3fb950"/>
        <text x="530" y="165" text-anchor="middle" class="svg-text" font-size="11">输出 = W + B×A（低秩增量）</text>
        <rect x="420" y="200" width="220" height="44" rx="10" fill="#161b22" stroke="#30363d"/>
        <text x="530" y="218" text-anchor="middle" class="svg-dim" font-size="11">同一个底座可插多个适配器：</text>
        <text x="530" y="235" text-anchor="middle" class="svg-dim" font-size="11">医疗版 / 法务版 / 客服版 随时切换</text>
        <line x1="280" y1="100" x2="418" y2="72" stroke="#5b8cff" stroke-width="1.8" fill="none"/>
        <line x1="280" y1="150" x2="418" y2="160" stroke="#5b8cff" stroke-width="1.8" fill="none"/>
        <text x="360" y="262" text-anchor="middle" class="svg-dim">LoRA：只训贴在旁边的小矩阵，底座零改动</text>
      </g>
    </svg>
    <figcaption>图 9：LoRA 原理——底座冻结，只训低秩增量，一个底座配多块"皮肤"</figcaption>
  </figure>

## 对齐技术速览

  - **RLHF（人类反馈强化学习）**：人给回答排序 → 训练一个"奖励模型" → 用强化学习让模型朝高分方向走。效果好但流程复杂、训练不稳；
- **DPO（直接偏好优化）**：跳过奖励模型，拿"好答案/坏答案"成对数据直接调参——效果接近 RLHF，工程上简单得多，开源微调事实上的默认选择；
- **蒸馏（Distillation）**：让大模型（教师）生成大量高质量输出，拿去微调小模型（学生）。学生学到教师的风格和部分能力，推理成本低一个数量级——"大模型生成数据教小模型"已是行业标准做法。

  ::: tip
先穷尽 Prompt 和 RAG，再考虑微调；微调首选 **LoRA/QLoRA**，对齐用 **DPO**，降本用**蒸馏**。微调改的是"怎么说话"，不是"知道什么"。
:::

模型调好了，怎么跑得又快又省？下一篇：**推理优化与部署**。
