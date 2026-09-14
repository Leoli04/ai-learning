---
title: 权限与审批：谁允许它动手
---

# 权限与审批：谁允许它动手

> 约 9 分钟 · 关键词：审批策略、权限预设、沙箱模式、fail-closed

## 两个旋钮，一套预设

dsh 把"Agent 能干什么"拆成两个**相互独立**的强制执行旋钮：

  <table>
    <tr><th>旋钮</th><th>管什么</th><th>取值</th></tr>
    <tr><td><strong>沙箱模式</strong></td><td>能碰哪些文件</td><td><code>read-only</code> / <code>workspace-write</code> / <code>danger-full-access</code></td></tr>
    <tr><td><strong>审批策略</strong></td><td>动手前要不要问人</td><td><code>ask</code> / <code>never</code></td></tr>
  </table>

两个旋钮组合起来就是**权限预设**，默认表里自带两个：

  - **`workspace-write`** = `workspace-write` + `ask`：能在工作区里写，但每次都问一下——日常开发的默认档；
  - **`danger-full-access`** = `danger-full-access` + `never`：不隔离、也不问——只该用在隔离垃圾箱里。

客户端把这张表呈现成一个**权限选择器**，多了一个派生的 `custom` 状态（当两个旋钮被人为调成表里没有的组合时）。`custom` 只能被显示，永远不能作为切换目标。

有一个设计细节很值得注意：**预设层自己不拥有任何强制执行**。它只记录"用户选的是哪个预设"，真正生效值仍然由两个旋钮各自的折叠结果决定。所以预设只是**意图的记账**，不是权限的开关——这样回放、审计、和并发会话才不会打架。

## 旋钮一：沙箱模式（只管文件系统）

  - **`read-only`**：后端拒绝写入，只保留 shell 必需的出口（比如 `/dev/null`）；
  - **`workspace-write`**：允许在工作区根目录、以及后端承诺的临时区域里写；
  - **`danger-full-access`**：绕过隔离，直接 spawn 原始 argv——注意它根本不会走沙箱服务。

后端是一组平台实现：Linux 用 **bwrap / Landlock**，macOS 用 **Seatbelt**，Windows 用 **ACL 受限令牌**。

这里有一件事 dsh 做得很诚实：**强制执行的完整性是后端"上报的事实"**，只有 `full` 和 `partial` 两个取值。老内核的 Landlock ABI、Windows ACL 的 Everyone 边界与硬链接边界，都只能算 `partial`——也就是说"这个模式承诺的文件效果，当前后端只管控住了其中一部分"。文档明确要求：**需要绝对保证的消费方必须拒绝，或把这个差别向上暴露**，而不是假装它是 full。

还有一个边界必须记住：**沙箱模式只承诺文件效果**。网络访问、进程可见性都不在这个词汇的管辖范围内——别指望 `read-only` 能顺带把网络也锁上。

## 旋钮二：审批策略（要不要问人）

  - **`ask`**（默认）：交给应答者链决定；如果链上没有任何应答者，落到 `unavailable`（也就是拒绝）；
  - **`never`**：**不问任何人**，每一次请求确定性地返回 `rejected`。这是无人值守场景（CI、定时任务）的严格姿态，也是"结果不需要问就能知道"的策略。

生效值取**会话日志里最后一条 `approval/policy` 事件**，回退到服务配置。写入路径只有一条，所以回放能完整重建当时的策略——这一点在第 6 篇"Session Log 是唯一事实源"里讲过，这里就是它的落地。

## 审批流的三个设计细节

  <figure class="figure">
    <svg viewBox="0 0 720 210" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a09" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <rect x="30" y="20" width="130" height="56" rx="9" class="cell"/>
        <text x="95" y="42" text-anchor="middle">工具要动手</text>
        <text x="95" y="62" text-anchor="middle" font-size="11" class="dim">写文件 / 跑命令</text>
        <rect x="190" y="20" width="140" height="56" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="260" y="42" text-anchor="middle">会话策略</text>
        <text x="260" y="62" text-anchor="middle" font-size="11" class="dim">ask / never</text>
        <rect x="360" y="20" width="160" height="56" rx="9" class="cell link-purple"/>
        <text x="440" y="42" text-anchor="middle">应答者链</text>
        <text x="440" y="62" text-anchor="middle" font-size="11" class="dim">UI 人工 / ACP 机器</text>
        <rect x="550" y="20" width="140" height="56" rx="9" class="cell link-green"/>
        <text x="620" y="42" text-anchor="middle">闭合结果</text>
        <text x="620" y="62" text-anchor="middle" font-size="11" class="dim">四种取值之一</text>
        <g stroke-width="1.8" marker-end="url(#a09)" class="link">
          <line x1="160" y1="48" x2="186" y2="48"/>
          <line x1="330" y1="48" x2="356" y2="48"/>
          <line x1="520" y1="48" x2="546" y2="48"/>
        </g>
        <text x="30" y="100" class="dim">结果集是闭合的，只有一个是"放行"</text>
        <rect x="30" y="110" width="145" height="34" rx="8" stroke-width="2" class="cell accent-green-stroke"/>
        <text x="102" y="131" text-anchor="middle">allowed-once</text>
        <rect x="190" y="110" width="145" height="34" rx="8" stroke-width="2" class="cell accent-red-stroke"/>
        <text x="262" y="131" text-anchor="middle">rejected</text>
        <rect x="350" y="110" width="145" height="34" rx="8" stroke-width="2" class="cell accent-red-stroke"/>
        <text x="422" y="131" text-anchor="middle">cancelled</text>
        <rect x="510" y="110" width="180" height="34" rx="8" stroke-width="2" class="cell accent-red-stroke"/>
        <text x="600" y="131" text-anchor="middle">unavailable</text>
        <text x="30" y="170" class="dim">✅ 只有 allowed-once 算放行，而且仅授权"所问的那一次"操作，不存在"本次会话永久允许"</text>
        <text x="30" y="192" class="dim">❌ 其余三种一律拒绝：没有应答者、应答者抛异常、返回值不在词汇表里，全都 fail-closed</text>
      </g>
    </svg>
    <figcaption>图 9：审批流——闭合的四种结果，只有 allowed-once 是放行</figcaption>
  </figure>

  1. **失败时拒绝，而不是放行（fail-closed）**。这是最关键的一条。审批服务拿不到应答者、应答者抛异常、甚至应答者返回了一个不在词汇表里的值——全部被归一成 `unavailable`，调用方**一律拒绝**。现实里大量系统在"鉴权服务挂了"时会选择放行，dsh 反过来：**不确定就等于不同意。**
2. **一次授权只覆盖一次操作**。`allowed-once` 的字面意思就是"仅授权所问的那一个操作"。没有"记住这个选择""今天都允许"这类模糊状态。
3. **审批留痕在日志里，但不进对话里**。每次问答会成对写入会话日志（`approval/asked` + `approval/decided`），靠一个全新的 `ApprovalRequestId` 把两条事件配起来；同时它**不进入模型的 transcript**——模型只看到调用方派生的工具结果，不会看到"刚才有人点了允许"。审计侧拿全量，模型侧保持干净。

::: tip
三个机制合起来，就是一套**可以放心交给无人值守环境**的授权模型：策略可回放（日志里），授权最小化（一次一授权），失败最保守（不确定就拒绝）。
:::

插件也写了、权限也定了。下一个问题很实际：模型跑在哪？——下一篇：**接入你自己的模型：Provider 与能力接缝**。
