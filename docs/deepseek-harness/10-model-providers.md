---
title: 接入你自己的模型：Provider、协议与请求形状
---

# 接入你自己的模型：Provider、协议与请求形状

> 约 10 分钟 · 关键词：Provider、API 协议、settings.yaml、LLM 适配器

## 换模型不用重启

打开**设置 → 模型**，DeepSeek 卡片上填 API 密钥、保存即可。**变更在下一次请求就生效，不需要重启服务器。**

一个值得注意的细节是**密钥的存储方式**：它是只写的。保存之后，页面只会收到脱敏描述符，永远不会拿到明文；密钥落在 `$DSH_HOME/.credentials.yaml` 里，settings 只保留一个凭据引用。这正好是第 4 篇讲的**能力接缝**在凭据上的体现——界面、配置、密钥三者各管一段，谁都不持有全部。

接入模型有三条路：

  1. **内置提供方**：dsh 自带一份提供方目录，列出来的是提供方 id（比如 `anthropic`、`openai`、Kimi 对应 `moonshotai`、GLM 对应 `zai`）。选一个、填密钥就行——端点、协议、模型列表都由目录提供。
2. **自定义提供方**：公司网关、自建服务器走这条。要填的是：小写 Provider ID、基础 URL、API 协议、凭据，以及至少一个模型。
3. 走 OAuth 登录的提供方（例如 Codex）目前**暂不支持**——它拿不到可填的密钥字段。

## 最容易踩的坑：一个提供方只认一种协议

自定义提供方表单里的**API 协议**必须选网关实际使用的那一种，只有三选一：

  <table>
    <tr><th>协议</th><th>对应</th></tr>
    <tr><td><code>openai-completions</code></td><td>OpenAI Chat Completions</td></tr>
    <tr><td><code>openai-responses</code></td><td>OpenAI Responses API</td></tr>
    <tr><td><code>anthropic-messages</code></td><td>Anthropic Messages API</td></tr>
  </table>

**一个提供方只使用一种协议**。网关如果同时提供两种，就得建两个提供方——这不是可以自动识别的东西，必须由你声明。

另一条要记住：**Provider ID 是永久的**。请求、已保存的会话、模型默认值、凭据引用全都会用到它。想改名没有捷径——新建一个提供方，再把旧的删掉。

## 表单之外：settings.yaml 才是主场

模型页刻意保持精简，只开放"让一条路由得以存在"所必需的字段：API 密钥、显示名称、API 地址、API 协议，以及每个模型的 ID、显示名、上下文窗口和最大输出 token 数。

其余全部落在 `$DSH_HOME/settings.yaml`：推理等级、图片输入、请求兼容性开关、请求头、超时、重试策略。它和模型页写的是同一份文件，可以直接编辑（浏览器与服务器同机时，设置页顶部还有"打开配置文件"按钮）。**适配器会在下一次请求重新读取，不用重启任何东西。**

## 为什么"密钥和地址都对，网关还是拒绝一切"

  <figure class="figure">
    <svg viewBox="0 0 720 216" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a10" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <rect x="30" y="30" width="150" height="64" rx="9" class="cell link-purple"/>
        <text x="105" y="52" text-anchor="middle" font-weight="bold">Harness</text>
        <text x="105" y="72" text-anchor="middle" font-size="11" class="dim">提供方无关请求</text>
        <text x="105" y="88" text-anchor="middle" font-size="11" class="dim">messages / tools / 参数</text>
        <rect x="210" y="30" width="170" height="64" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="295" y="52" text-anchor="middle" font-weight="bold">适配器（pi-ai）</text>
        <text x="295" y="72" text-anchor="middle" font-size="11" class="dim">翻译成具体 API 形状</text>
        <text x="295" y="88" text-anchor="middle" font-size="11" class="dim">角色 / 字段 / 思考等级</text>
        <rect x="410" y="30" width="130" height="64" rx="9" class="cell"/>
        <text x="475" y="52" text-anchor="middle" font-weight="bold">网关端点</text>
        <text x="475" y="72" text-anchor="middle" font-size="11" class="dim">按形状校验</text>
        <text x="475" y="88" text-anchor="middle" font-size="11" class="dim">不合规就拒收</text>
        <rect x="570" y="30" width="120" height="64" rx="9" class="cell link-green"/>
        <text x="630" y="62" text-anchor="middle" font-weight="bold">模型</text>
        <g stroke-width="1.8" marker-end="url(#a10)" class="link">
          <line x1="180" y1="62" x2="206" y2="62"/>
          <line x1="380" y1="62" x2="406" y2="62"/>
          <line x1="540" y1="62" x2="566" y2="62"/>
        </g>
        <rect x="30" y="118" width="660" height="58" rx="10" class="cell link-orange"/>
        <text x="50" y="140" font-size="11">❌ 形状从哪来：依据端点 URL 推断；无法识别的地址一律按 OpenAI 本身处理</text>
        <text x="50" y="162" font-size="11" class="dim">❌ 于是多数 OpenAI 兼容网关，至少会拒绝 OpenAI 所接受的某一样东西</text>
        <text x="30" y="200" font-size="11">✅ 两个开关能救掉绝大多数情况：<tspan class="dim">compat.supportsDeveloperRole: false</tspan> 与 <tspan class="dim">compat.maxTokensField: max_tokens</tspan></text>
      </g>
    </svg>
    <figcaption>图 10：请求形状由适配器决定——识别不了的地址按 OpenAI 处理，兼容开关负责纠偏</figcaption>
  </figure>

原因在这里：适配器**依据端点的 URL 决定请求的形状**——系统提示词由哪个角色承载、输出上限写在哪个字段、思考级别如何传输。而它无法识别的地址，会被当作 OpenAI 本身来对待。问题是，**多数 OpenAI 兼容网关至少会拒绝 OpenAI 所接受的某一样东西**。

最常见的两样：

  - 声明了推理能力的模型，系统提示词会以 `role: "developer"` 发出，很多网关直接拒绝 → 设 `compat.supportsDeveloperRole: false`；
  - 输出上限写成了 `max_completion_tokens`，只认 `max_tokens` 的服务端会拒绝 → 设 `compat.maxTokensField: max_tokens`。

另外两个手动录入模型的常见需求：

  - **图片输入**：手动录入的模型默认按纯文本对待，附图片会在发送前就被拒绝。给该模型加 `input: [text, image]`；如果整条路由的模型都支持图片，就在路由上设一次 `defaultInput`（默认 `[text]`）。内置提供方没有可填的模型列表，改写 `modelOverrides`。
  - **推理等级**：手动录入的模型不声明任何等级，所以选择器里没有菜单。用 `reasoningEfforts` 声明（键是菜单项，值就是协议上 `reasoning_effort` 的写法）。对于"不明确关闭就会思考"的模型（比如 OpenAI 兼容网关后面的 DeepSeek），还要加 `compat.thinkingFormat: deepseek`——它会让 `off` 真的发出 `thinking: {type: disabled}`。

::: warning
这些字段是**对你端点的断言，不是对它的检查**。声明了端点其实不提供的图片能力，这里不会拦你——改由提供方在运行时拒绝该请求。所以写完最好真发一次带图的请求验证。
:::

## 如果连适配器都要自己写

自定义提供方不够用时（协议特殊、要接内部推理服务），可以自己写一个 **LLM 适配器**：继承 `LlmAdapter`、实现 `stream()`，把提供的无关请求翻译成具体 API 调用，再把响应翻译回统一的**分片（StreamChunk）**序列。

契约要点值得记下来：

  - 每个 `block-start` 必须有配对的 `block-end`，`index` 从 0 递增；
  - `finish` 必须是最后一个分片，`usage` 要在 `finish` 之前；
  - **无法支持的字段要抛带稳定 code 的 `LlmError`，不许静默丢弃**——静默丢弃只会把故障推到更远、更难查的地方；
  - 注册方式是把提供方路由列表交给 `ctx.llm.registerAdapter(['my-provider'], adapter)`。

仓库里有两个完整参考实现（`llm-deepseek`、`llm-pi-ai`），对比它们就能看出同一套契约如何落在不同的提供方 SDK 上。

::: tip
这一篇其实是第 4 篇**能力接缝**的落地形态：上层永远只说"给我一个 stream"，完全不关心后端是谁。换模型、换网关、换自建服务，改的都是接缝下面的 Provider——**上层一行代码都不用动。**
:::

模型通了，接下来是另一个问题：怎么让 Agent 记住"这件事该怎么做"——下一篇：**Skill 与项目约定**。
