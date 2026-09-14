---
title: 本地化部署与开源模型：把模型搬回自己机房
---

# 本地化部署与开源模型：把模型搬回自己机房

> 约 9 分钟 · 关键词：Ollama、llama.cpp、vLLM、量化、私有化

## 什么时候该自己跑

自己部署模型从来不是为了"更强"，而是为了另外四件事：

  - **数据不能出网**：金融、医疗、政企、涉密场景，文档和对话就不允许离开内网；
  - **成本要可控**：调用量足够大时，固定硬件的摊薄成本会低于按 token 计费；
  - **离线可用**：网络不稳、现场无外网，或者要求断网运行；
  - **深度定制**：要微调自己的模型、改推理逻辑、蒸馏一个专用小模型。

反过来，两种情况别自己上：**追求最强能力**（顶级闭源模型仍在前面），以及**需要紧跟最新能力**（自部署等于把自己锁在某个版本上，半年后可能就落后了）。

## 一条从笔记本到集群的路径

  <figure class="figure">
    <svg viewBox="0 0 720 250" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a20" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <rect x="30" y="36" width="200" height="66" rx="10" class="cell"/>
        <text x="130" y="58" text-anchor="middle" font-weight="bold">Ollama</text>
        <text x="130" y="78" text-anchor="middle" font-size="11" class="dim">一行命令拉起模型</text>
        <text x="130" y="94" text-anchor="middle" font-size="11" class="dim">底层 llama.cpp · GGUF</text>
        <rect x="250" y="36" width="200" height="66" rx="10" class="cell link"/>
        <text x="350" y="58" text-anchor="middle" font-weight="bold">本地服务化</text>
        <text x="350" y="78" text-anchor="middle" font-size="11" class="dim">llama.cpp server / LM Studio</text>
        <text x="350" y="94" text-anchor="middle" font-size="11" class="dim">对外给 OpenAI 兼容接口</text>
        <rect x="470" y="36" width="200" height="66" rx="10" stroke-width="2" class="cell-em link-green"/>
        <text x="570" y="58" text-anchor="middle" font-weight="bold">生产并发</text>
        <text x="570" y="78" text-anchor="middle" font-size="11" class="dim">vLLM / SGLang</text>
        <text x="570" y="94" text-anchor="middle" font-size="11" class="dim">连续批处理，吞吐上一个量级</text>
        <g stroke-width="1.8" marker-end="url(#a20)" class="link">
          <line x1="230" y1="69" x2="246" y2="69"/>
          <line x1="450" y1="69" x2="466" y2="69"/>
        </g>
        <text x="30" y="134" class="dim">同一个 7B 模型，量化档位不同，显存需求能差 4 倍</text>
        <text x="40" y="162" class="dim">FP16</text>
        <rect x="130" y="146" width="420" height="22" rx="5" class="accent-red-fill"/>
        <text x="562" y="162" font-size="11" class="dim">≈ 14 GB</text>
        <text x="40" y="192" class="dim">INT8</text>
        <rect x="130" y="176" width="210" height="22" rx="5" class="accent-orange-fill"/>
        <text x="352" y="192" font-size="11" class="dim">≈ 7 GB</text>
        <text x="40" y="222" class="dim">INT4</text>
        <rect x="130" y="206" width="105" height="22" rx="5" class="accent-green-fill"/>
        <text x="247" y="222" font-size="11" class="dim">≈ 3.5 GB</text>
      </g>
    </svg>
    <figcaption>图 20：三个部署阶段——试用、服务化、生产并发；以及量化带来的显存差异</figcaption>
  </figure>

  1. **试用**：**Ollama** 最省事，一条命令就能把开源模型跑起来（底层是 llama.cpp，模型格式是 GGUF）。适合验证效果、做概念验证。
2. **服务化**：要让自己的应用调用，就用 llama.cpp 自带的 server 或 LM Studio，它们对外提供 **OpenAI 兼容接口**——业务代码几乎不用改，把 base_url 换个地址就接上了。
3. **生产并发**：多人同时用的时候，前者就不够了。**vLLM / SGLang** 靠 PagedAttention 和连续批处理，把"同时服务多个请求"的吞吐拉高一个量级。这是线上形态和实验形态的分水岭。

## 显存怎么估：一个够用的公式

  > 显存 ≈ 参数量 × 每参数字节数 + KV Cache

  - **FP16**：每参数约 2 字节，7B 模型 ≈ 14 GB，得配张像样的卡；
  - **INT8**：约 1 字节，7B ≈ 7 GB，一张消费级卡就能跑；
  - **INT4**：约 0.5 字节，7B ≈ 3.5 GB，笔记本都能跑。

经验上，量化到 INT4 通常还能保住大部分通用能力，但**长上下文与复杂推理掉得最明显**——这类任务建议实测后再决定档位。

还有一项常被忽略的开销：**KV Cache**。它随"并发数 × 上下文长度"线性增长。所以真正吃爆显存的往往不是模型本身，而是"长上下文 + 高并发"——这也是为什么长文档场景要格外克制的理由。

## 选模型：先看尺寸和授权

  <table>
    <tr><th>尺寸</th><th>够干什么</th></tr>
    <tr><td>3B 以下</td><td>分类、抽取、路由、改写——当"打杂小工"用，便宜且够快</td></tr>
    <tr><td>7B~14B</td><td>通用对话、摘要、代码补全、RAG 里的问答环节</td></tr>
    <tr><td>30B 以上</td><td>复杂推理、长文档分析，接近"能当主力"的水平</td></tr>
    <tr><td>推理模型</td><td>数学、复杂代码、多步规划——贵但值得，按需调用</td></tr>
  </table>

选型前务必确认两件事：**许可证是否允许商用**（有的模型有月活或营收门槛），以及**中文能力的实测表现**——榜单分数和你的业务语料往往不是一回事。

## 混着用：分层路由

现实中很少"全本地"或"全云端"，更常见的是混着用：

  - **本地跑**：脱敏、分类、抽取、格式转换、简单问答——高频、便宜、数据不出网；
  - **云端跑**：复杂推理、创意写作、长文档分析——低频、贵、但对能力要求高。

关键在于让本地那一层同时充当**脱敏网关**：敏感字段先在本地处理干净再上云，能不出网的就不出网。

::: tip
把模型搬回自己机房，换来的不是"最强的能力"，而是**可控的数据边界、可预测的成本、可定制的自由**。能力之外，这一层决定了你的系统到底攥在谁手里。
:::

::: tip
到这里，这个系列 20 篇走完了完整一圈：模型怎么炼成（01–02）→ 怎么指挥它（03）→ 补知识与检索（04–05、16）→ 补手脚与范式（06）→ 补记忆与经验（07–09）→ 压成本提速度（10）→ 扩边界（11、14、17）→ 拼成系统与生态（12、19）→ 补上评测与安全（13、15、18）→ 最后决定它跑在哪（20）。
:::

接下来有两条路可以走：想看一个真实的 Agent 框架怎么把这些能力组装成能用的产品，接着读系列二 **DeepSeek Harness 通俗图解**；想知道这套东西在企业里真正落地时卡在哪——文档解析、切分、检索调优、权限、评测——接着读系列三 **企业知识库实战**。两者其实是同一件事的两面：一面是框架怎么搭，一面是业务怎么用。
