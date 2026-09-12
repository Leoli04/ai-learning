---
title: 事件三域与 Turn 执行流：一次任务是怎么跑完的
---

# 事件三域与 Turn 执行流：一次任务是怎么跑完的

> 约 7 分钟 · 关键词：session / agent / capability 事件、Turn、Step、Waterfall

## 事件是第一扩展点

在 dsh 里，"改行为"的第一选择不是改代码，而是**监听事件**。但事件分三个"域"，选错域是新手最常见的坑：

  <table>
    <tr><th>域</th><th>性质</th><th>什么时候用</th></tr>
    <tr><td><strong>Session 事件</strong></td><td>持久事实，追加进日志，重启后还在</td><td>需要跨重启存活的"事实"（消息、工具结果）</td></tr>
    <tr><td><strong>Agent 事件</strong>（<code>agent/*</code>）</td><td>实时状态，携带活的 Agent 对象</td><td>观察/拦截进行中的工作（收件箱、步骤、请求）</td></tr>
    <tr><td><strong>Capability 事件</strong>（<code>fs/*</code>、<code>tools/*</code> 等）</td><td>策略挂载点</td><td>给某条 Seam 附加策略或适配器，不必导入主循环</td></tr>
  </table>

## Turn 和 Step：两个节拍器

一次完整的用户请求叫一个 **Turn（轮）**。一个 Turn 里可能发生多轮"模型思考 + 工具调用"，每一小步叫一个 **Step（步）**。完整流水线如下：

  <figure class="figure">
    <svg viewBox="0 0 720 420" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#5b8cff"/></marker></defs>
      <g font-size="13">
        <rect x="90" y="20" width="540" height="40" rx="9" fill="#161b22" stroke="#5b8cff"/>
        <text x="360" y="45" text-anchor="middle" class="svg-text">turn/start → 认领输入（单收件箱）</text>
        <rect x="90" y="80" width="540" height="40" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="360" y="105" text-anchor="middle" class="svg-text">组装 prompt 区块 + 工具 schema → agent/pre-step 闸门</text>
        <rect x="90" y="140" width="540" height="40" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="360" y="165" text-anchor="middle" class="svg-text">step/start → agent/request → 发出不可变模型请求</text>
        <rect x="90" y="200" width="540" height="40" rx="9" fill="#161b22" stroke="#bc8cff"/>
        <text x="360" y="225" text-anchor="middle" class="svg-text">流式返回：llm/stream → agent/assistant-stream</text>
        <rect x="90" y="260" width="540" height="40" rx="9" fill="#161b22" stroke="#3fb950"/>
        <text x="360" y="285" text-anchor="middle" class="svg-text">tool/call → tools/pre-execute → execute → post-execute → result</text>
        <rect x="90" y="320" width="540" height="40" rx="9" fill="#161b22" stroke="#f0883e"/>
        <text x="360" y="345" text-anchor="middle" class="svg-text">step/end → 还要继续？认领输入进入下一步</text>
        <rect x="190" y="376" width="340" height="34" rx="9" fill="rgba(240,136,62,0.10)" stroke="#f0883e"/>
        <text x="360" y="398" text-anchor="middle" class="svg-text">agent/turn-stopping → turn/end</text>
        <g stroke="#5b8cff" stroke-width="1.8" fill="none" marker-end="url(#a)">
          <line x1="360" y1="60" x2="360" y2="78"/>
          <line x1="360" y1="120" x2="360" y2="138"/>
          <line x1="360" y1="180" x2="360" y2="198"/>
          <line x1="360" y1="240" x2="360" y2="258"/>
          <line x1="360" y1="300" x2="360" y2="318"/>
          <line x1="360" y1="360" x2="360" y2="374"/>
          <path d="M 630 340 C 690 340 690 100 632 100" marker-end="url(#a)"/>
        </g>
        <text x="706" y="225" text-anchor="middle" class="svg-dim" font-size="11" transform="rotate(90 706 225)">循环：继续 Step</text>
      </g>
    </svg>
    <figcaption>图 5：一个 Turn 的完整流水线——Step 循环直到无需更多请求</figcaption>
  </figure>

## 两个容易忽略的细节

### 瀑布（Waterfall）事件要放行

`agent/pre-step`、`agent/request`、`llm/stream` 和三个 `tools/*` 事件是"瀑布式"的：**监听者必须调用 `next()` 把水放下去**，否则整条链路停在你这里。这既是拦截点（审批、审计），也是责任（忘了放行系统就卡死）。

### 单收件箱

所有输入都从一个**单一 inbox** 进入驱动：新消息立刻唤醒 Agent；而"注入的上下文"会安静地在 inbox 里排队，直到下一条真消息到来才一起被消化——避免上下文碎片反复打断模型。

  ::: tip
持久事实进 Session 域，实时状态走 Agent 域，策略附加用 Capability 域；Turn 由若干 Step 组成，瀑布事件记得 `next()`。
:::

流水线里反复出现"追加进日志"——那个日志为什么如此重要？下一篇讲 dsh 的基石设计：**Session Log，唯一事实源**。
