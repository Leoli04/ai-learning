---
title: 多形态运行：Web、headless、SDK 与网关
---

# 多形态运行：Web、headless、SDK 与网关

> 约 9 分钟 · 关键词：Profile、headless、Python SDK、ACP、API Gateway

## 同一个内核，四种外壳

  <figure class="figure">
    <svg viewBox="0 0 720 196" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a12" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <text x="30" y="26" class="dim">四种外壳，同一内核的不同装配</text>
        <rect x="30" y="38" width="150" height="56" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="105" y="60" text-anchor="middle" font-weight="bold">web</text>
        <text x="105" y="80" text-anchor="middle" font-size="11" class="dim">本地 Web UI</text>
        <rect x="200" y="38" width="150" height="56" rx="9" class="cell"/>
        <text x="275" y="60" text-anchor="middle" font-weight="bold">headless</text>
        <text x="275" y="80" text-anchor="middle" font-size="11" class="dim">脚本 / CI，跑完即退</text>
        <rect x="370" y="38" width="150" height="56" rx="9" class="cell"/>
        <text x="445" y="60" text-anchor="middle" font-weight="bold">sdk / sdk-minimal</text>
        <text x="445" y="80" text-anchor="middle" font-size="11" class="dim">嵌进你自己的程序</text>
        <rect x="540" y="38" width="150" height="56" rx="9" class="cell"/>
        <text x="615" y="60" text-anchor="middle" font-weight="bold">acp</text>
        <text x="615" y="80" text-anchor="middle" font-size="11" class="dim">给别的软件当后端</text>
        <g stroke-width="1.8" marker-end="url(#a12)" class="link-dim">
          <line x1="105" y1="94" x2="105" y2="116"/>
          <line x1="275" y1="94" x2="275" y2="116"/>
          <line x1="445" y1="94" x2="445" y2="116"/>
          <line x1="615" y1="94" x2="615" y2="116"/>
        </g>
        <rect x="30" y="120" width="660" height="56" rx="12" stroke-width="2" class="cell-em link-purple"/>
        <text x="360" y="142" text-anchor="middle" font-weight="bold">同一份内核</text>
        <text x="360" y="162" text-anchor="middle" font-size="11" class="dim">Agent 循环 · Session Log · 能力接缝 · 插件系统</text>
      </g>
    </svg>
    <figcaption>图 12：四种运行形态共享同一内核，差别只在 profile 与 patch</figcaption>
  </figure>

第 1 篇里列过这张形态表，这里把它讲透：

  <table>
    <tr><th>形态</th><th>用途</th><th>特点</th></tr>
    <tr><td><code>web</code></td><td>日常开发</td><td>本地 Web UI，默认 <code>127.0.0.1:3080</code></td></tr>
    <tr><td><code>headless</code></td><td>脚本、CI</td><td>无界面，一次性跑完就退出</td></tr>
    <tr><td><code>sdk</code> / <code>sdk-minimal</code></td><td>嵌进你的程序</td><td>有 Python SDK，把 Agent 当库调用</td></tr>
    <tr><td><code>acp</code></td><td>给别的软件用</td><td>纯自动化协议服务，被当作"后端大脑"</td></tr>
  </table>

它们**不是四套代码**，而是同一内核配上不同的 **profile（组合包）**——第 3 篇的 profile / bundle / patch 分层，在这里变成了产品交付方式。

## Web 形态：不只是个页面

Web 侧本身也被拆得很细：服务端是一层 HTTP 载体（路由、index 渲染挂接点），客户端则管启动、与 Remote 通信、配对的 Client model、会话视图组装、**slot（类型化 UI 组合）**和断线重连语义。

关键在于：插件可以在客户端声明 `dsh.client` 与 UI slot，也就是说——**"一切皆插件"在界面层面同样成立**。加一个插件，可以顺带多出一块 UI 面板，而不必去改前端主程序。

## headless 与 ACP：给自动化和别的程序用

  - **headless**：无界面跑一次性任务，跑完退出。放进 CI 或定时脚本里最合适。
  - **acp**：Agent Client Protocol 服务，定位是"给别的软件当后端大脑"。它还负责一件事：为它自己拥有的 agent 提供**一次性的机器审批决策**——正好对应第 9 篇讲的应答者链：UI 通道给人当应答者，ACP 通道给机器当应答者。

## Python SDK：把 Agent 当库用

```sh
python -m pip install deepseek-harness-sdk
```

装完之后你会同时拿到匹配的原生运行时 wheel 和 `dsh` 命令，而且——**普通 SDK 运行不需要系统 Node.js。**

```python
from pathlib import Path

from deepseek_harness import DeepSeekHarness

workspace = Path("/absolute/path/to/disposable-workspace").resolve()
dsh_home = Path("/absolute/path/to/example-dsh-home").resolve()
with DeepSeekHarness(
    provider="deepseek-official",
    model="deepseek-v4-flash",
    max_tokens=49_152,
    cwd=str(workspace),
    dsh_home=str(dsh_home),
    profile="sdk-minimal",
) as harness:
    result = harness.run(
        "Inspect the repository and fix the failing tests.",
        session_id="example-001",
    )

print(result.final_response)
```

实现上它并**没有另写一套运行时**：SDK 会延迟启动一个内置的 `dsh --profile sdk-minimal` 进程，并复用到上下文管理器退出。应用配置 = profile + 它的持久 patch + home patch + 你传入的 `patches` 元组——还是那套分层。

### `sdk-minimal` 到底有多"小"

  <table>
    <tr><th>属性</th><th>值</th></tr>
    <tr><td>系统提示词</td><td><code>DSH_SYSTEM_PROMPT</code>，未设置时是 <code>You are a helpful software engineer assistant.</code></td></tr>
    <tr><td>模型</td><td>默认 <code>deepseek-v4-flash</code>，可由参数或环境变量覆盖</td></tr>
    <tr><td>面向模型的工具</td><td>Linux / macOS 一个持久 <code>bash</code>，Windows 是 <code>pwsh</code></td></tr>
    <tr><td>Shell 超时</td><td>300 秒</td></tr>
    <tr><td>运行时上下文与 compaction</td><td><strong>不存在</strong></td></tr>
    <tr><td>会话持久化</td><td><code>&lt;dsh_home&gt;/sessions</code> 下未压缩的 JSONL</td></tr>
  </table>

它是在一个**空根**之上插入完整配置树的，**不包含 `dsh-base`**。这意味着基础 profile 以后新增的工具，不会"自动"出现在极简 profile 里——第 2 篇说的"组合优于继承"，好处在这里变得可观测：**你的运行环境不会因为上游升级而悄悄多出能力。**

::: warning
`sdk-minimal` **固定使用 `danger-full-access`**——按平台选出的持久 shell 能修改运行时可见的任何路径。官方因此明确要求：**用一次性 checkout 或容器跑**。这正是第 9 篇那句"`danger-full-access` 只该用在隔离垃圾箱里"的实例。
:::

几条隔离约定值得照着做：隔离 profile、插件、凭据、设置与会话，就**用一个新 home**；独立任务用**新的 session id**；只有要继续同一段对话和会话资源时，才同时复用同一个 harness、home 和 id。另外——示例与 SDK **绝不会静默读取 `~/.dsh`**，所有路径都要显式给出。

## API Gateway：给"宿主 / 客户端分离"留的缝

要让别的软件把 dsh 当后端用，走的是 API Gateway 这条缝，而不是去改内核。做法是业务服务用 `@Remote` / `@RemoteScope` 显式声明"哪些方法对客户端开放"：

  - **未标记的方法**不会进入生成的 Client 类型，也不能通过 `ctx.remote` 调用——**默认不开放**；
  - 复杂的宿主对象不能直接跨线上传输：业务包要声明它与 wire identity 的关联。例如 `Agent` 在宿主签名里叫 `agent`，过线时是 `agentId`，网关在调用业务方法前把 id 解析回宿主对象。

这条缝的存在说明了一件事：**Web UI 只是众多客户端之一。**内核不需要知道"现在是谁在用它"。

::: tip
四种形态是同一套内核的**不同装配**：从"让我用"（web）到"让程序用"（headless / SDK / ACP），改的始终是 profile 与 patch。
:::

一个东西好不好用，是比出来的。下一篇：**横向对比——dsh 与其他 Agent Harness**。
