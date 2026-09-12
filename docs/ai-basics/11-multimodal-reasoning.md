---
title: 多模态与推理模型：能看图，会"先想后答"
---

# 多模态与推理模型：能看图，会"先想后答"

> 约 8 分钟 · 关键词：VLM、Test-time Compute、o1 / DeepSeek-R1、思考模式

## 多模态：给语言模型接上眼睛和耳朵

纯文本 LLM 看不懂图。解决方案的思路很直接：**把其他模态也翻译成"token"**：

  - **视觉**：一张图先过视觉编码器（如 ViT），切成图块转为向量，与文本向量对齐后一起送入 LLM——GPT-4V、Gemini、Qwen-VL 都是这个思路；
- **语音**：或走"语音转文字 → LLM → 文字转语音"的传统管线，或端到端直接处理音频 token（GPT-4o、Qwen-Audio）；
- **生成侧**：扩散模型（Diffusion）负责图像/视频生成，与 LLM 形成分工——LLM 管"理解与规划"，扩散模型管"画"。

多模态打开的应用面：截图问答、UI 自动化操作（看屏幕点鼠标）、票据识别录入、视频理解。对 Agent 意义重大——**没有视觉，Agent 只能操作 API；有了视觉，它能操作人类操作的一切界面。**

## 推理模型：用"思考时间"换聪明程度

2024 年 9 月 OpenAI 发布 o1，2025 年 1 月 DeepSeek 开源 R1，标志着新范式的到来：**让模型在给出答案前先生成一条很长的思考链（思维 token）**——自我提问、尝试、发现矛盾、回退重来。

  <figure class="figure">
    <svg viewBox="0 0 720 280" xmlns="http://www.w3.org/2000/svg">
      <g font-size="12">
        <!-- 普通模型 -->
        <rect x="40" y="40" width="300" height="90" rx="12" class="cell"/>
        <text x="190" y="66" text-anchor="middle" font-weight="bold">普通模式</text>
        <text x="190" y="90" text-anchor="middle" class="dim">问题 → 直接生成答案</text>
        <text x="190" y="112" text-anchor="middle" font-size="11" class="dim">快、便宜；难题正确率有天花板</text>
        <!-- 推理模型 -->
        <rect x="380" y="40" width="300" height="90" rx="12" stroke-width="2" class="cell-em link-purple"/>
        <text x="530" y="66" text-anchor="middle" font-weight="bold">推理模式（思考）</text>
        <text x="530" y="90" text-anchor="middle" class="dim">问题 → 长思考链 → 答案</text>
        <text x="530" y="112" text-anchor="middle" font-size="11" class="dim">慢 5~50 倍、贵数倍；难题正确率大涨</text>
        <!-- 关键洞察 -->
        <rect x="40" y="160" width="640" height="90" rx="12" stroke-width="2" class="cell-em link-orange"/>
        <text x="360" y="188" text-anchor="middle" font-weight="bold" font-size="14">关键洞察：Test-time Compute 缩放</text>
        <text x="360" y="214" text-anchor="middle" class="dim">性能不只随训练算力增长（Scaling Laws），也随"推理时多想"而增长</text>
        <text x="360" y="236" text-anchor="middle" class="dim">于是出现了新旋钮：难题多给思考 token，简单题秒答——按题分配"脑力预算"</text>
      </g>
    </svg>
    <figcaption>图 11：普通模式 vs 推理模式——新旋钮"思考预算"按题分配</figcaption>
  </figure>

### DeepSeek-R1 的两个启示

  1. **训练方法开源验证**：R1 证明主要靠强化学习（可验证奖励：数学题对错、代码能否通过测试）就能激发出长思考链，辅以少量 SFT 修格式——路线被开源社区复现；
2. **蒸馏有效**：R1 的思考数据微调出的 7B/14B 小模型也获得显著推理提升——再次验证"大模型生成数据教小模型"。

## 什么时候用推理模型？

  <table>
    <tr><th>✅ 用推理模型</th><th>❌ 用普通模型</th></tr>
    <tr><td>数学 / 逻辑 / 竞赛题</td><td>闲聊、翻译、摘要</td></tr>
    <tr><td>复杂代码调试、架构设计</td><td>格式转换、简单抽取</td></tr>
    <tr><td>多步规划、Agent 的关键决策点</td><td>高频大批量的简单调用</td></tr>
  </table>

::: tip
多模态扩**输入输出**的边界（图/音/视频都是 token），推理模型扩**思考**的边界（先想后答，思考预算可调）。两者叠加，正是 Agent 能看屏幕、会规划的物质基础。
:::

单点技术齐了，怎么拼成真正落地的系统？下一篇：**工作流编排与主流 Agent 技术全景**。
