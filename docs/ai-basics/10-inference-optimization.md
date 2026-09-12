---
title: 推理优化与部署：让模型跑得快、装得下、花得少
---

# 推理优化与部署：让模型跑得快、装得下、花得少

> 约 8 分钟 · 关键词：KV Cache、量化、vLLM / PagedAttention、投机解码、Ollama

## 为什么推理贵？先看瓶颈在哪

生成是逐 token 接龙：每生成一个字，都要把整段上下文过一遍模型。两个直接后果——

  - **算力瓶颈**：上下文越长，每个 token 的计算量越大；
- **显存瓶颈**：模型权重 + 中间结果都要装进显存。70B 模型 FP16 精度要约 140GB 显存，单卡根本放不下。

工程界对症下药，形成了一套标准优化组合拳：

  <figure class="figure">
    <svg viewBox="0 0 720 330" xmlns="http://www.w3.org/2000/svg">
      <g font-size="12">
        <rect x="30" y="30" width="210" height="120" rx="10" class="cell"/>
        <text x="135" y="56" text-anchor="middle" font-weight="bold">KV Cache</text>
        <text x="135" y="78" text-anchor="middle" class="dim">把算过的注意力中间结果缓存</text>
        <text x="135" y="98" text-anchor="middle" class="dim">新 token 只算增量</text>
        <text x="135" y="120" text-anchor="middle" font-size="11" class="dim">代价：长上下文的显存大户</text>
        <rect x="255" y="30" width="210" height="120" rx="10" stroke-width="2" class="cell-em link"/>
        <text x="360" y="56" text-anchor="middle" font-weight="bold">量化 Quantization</text>
        <text x="360" y="78" text-anchor="middle" class="dim">FP16 → INT8 / INT4</text>
        <text x="360" y="98" text-anchor="middle" class="dim">显存 ÷2 再 ÷2，损失极小</text>
        <text x="360" y="120" text-anchor="middle" font-size="11" class="dim">GGUF(AWQ/GPTQ) 本地部署标配</text>
        <rect x="480" y="30" width="210" height="120" rx="10" class="cell"/>
        <text x="585" y="56" text-anchor="middle" font-weight="bold">投机解码</text>
        <text x="585" y="78" text-anchor="middle" class="dim">小模型先猜一串</text>
        <text x="585" y="98" text-anchor="middle" class="dim">大模型一次验收多个</text>
        <text x="585" y="120" text-anchor="middle" font-size="11" class="dim">结果不变，速度 ×2~3</text>
        <rect x="140" y="185" width="440" height="110" rx="12" stroke-width="2" class="cell-em link-green"/>
        <text x="360" y="212" text-anchor="middle" font-weight="bold" font-size="14">vLLM / PagedAttention（2023，吞吐革命）</text>
        <text x="360" y="238" text-anchor="middle" class="dim">把 KV Cache 像内存分页一样管理，碎片几乎为零</text>
        <text x="360" y="260" text-anchor="middle" class="dim">+ Continuous Batching：新请求随时插队进批次</text>
        <text x="360" y="282" text-anchor="middle" class="dim">同卡吞吐提升数倍~数十倍，自托管服务的事实标准</text>
      </g>
    </svg>
    <figcaption>图 10：推理优化四件套——KV Cache、量化、投机解码、vLLM 服务化</figcaption>
  </figure>

## 部署形态怎么选？

  <table>
    <tr><th>形态</th><th>适合</th><th>代表</th></tr>
    <tr><td><strong>云端 API</strong></td><td>多数业务：零运维、按量付费</td><td>DeepSeek / OpenAI / 各云厂商</td></tr>
    <tr><td><strong>自托管推理服务</strong></td><td>数据不出内网、量大摊薄成本</td><td>vLLM、SGLang、TGI + 开源权重</td></tr>
    <tr><td><strong>本机 / 边缘</strong></td><td>个人、离线、隐私极端敏感</td><td>Ollama、llama.cpp（量化小模型）</td></tr>
  </table>

经验值：7B 模型 4bit 量化后约 4~5GB，一台笔记本就能跑；70B 级别 4bit 也要 40GB+，需要多卡或专用推理机。

## 省钱的另一个杠杆：模型分层路由

  - **简单步骤用小模型**：分类、抽取、格式转换交给 7B 级别，只有复杂推理才请出大模型；
- **Prefix Caching（前缀缓存）**：固定不变的系统提示词、长文档只算一次，多轮复用直接打折；
- **结果缓存**：相同/相似问题直接命中缓存。

  ::: tip
推理优化三板斧——**省算力（KV Cache / 投机解码）、省显存（量化 / PagedAttention）、省金钱（路由小模型 / 前缀缓存）**。部署先 API 起步，量大了再自托管，隐私敏感就 Ollama 本地跑。
:::

效率和成本压住了，模型还能更"聪明"吗？下一篇：**多模态与推理模型**。
