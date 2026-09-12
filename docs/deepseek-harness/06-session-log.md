---
title: Session Log：模型看见的一切，都必须有据可查
---

# Session Log：模型看见的一切，都必须有据可查

> 约 6 分钟 · 关键词：Session Log、deriveMessages、Model-visible means logged、JSONL

## 核心不变量：一句话的宪法

dsh 的会话系统建立在一条"宪法级"不变量上：

  > **"Model-visible means logged"**——凡是能到达模型请求的内容，都必须能从会话日志（Session Log）重建出来。运行时会自动断言这一点。

换句话说：**模型看到的上下文不是"现场拼出来的"，而是从日志里"投影"出来的。**日志是唯一事实源（Single Source of Truth）。

  <figure class="figure">
    <svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg">
      <g font-size="13">
        <!-- 日志 -->
        <rect x="250" y="30" width="220" height="230" rx="12" stroke-width="2" class="cell link"/>
        <text x="360" y="58" text-anchor="middle" font-weight="bold">Session Log</text>
        <text x="360" y="76" text-anchor="middle" font-size="11" class="dim">JSONL，append-only</text>
        <g font-size="12">
          <rect x="270" y="92" width="180" height="26" rx="6" class="cell"/>
          <text x="360" y="109" text-anchor="middle">user/message</text>
          <rect x="270" y="126" width="180" height="26" rx="6" class="cell"/>
          <text x="360" y="143" text-anchor="middle">assistant/message</text>
          <rect x="270" y="160" width="180" height="26" rx="6" class="cell"/>
          <text x="360" y="177" text-anchor="middle">tool/call · tool/result</text>
          <rect x="270" y="194" width="180" height="26" rx="6" class="cell"/>
          <text x="360" y="211" text-anchor="middle">assistant/attempt（失败尝试）</text>
          <rect x="270" y="228" width="180" height="26" rx="6" class="cell"/>
          <text x="360" y="245" text-anchor="middle">system/message</text>
        </g>
        <!-- 右侧派生物 -->
        <rect x="540" y="60" width="160" height="44" rx="9" class="cell link-green"/>
        <text x="620" y="80" text-anchor="middle">模型历史</text>
        <text x="620" y="96" text-anchor="middle" font-size="11" class="dim">deriveMessages() 投影</text>
        <rect x="540" y="130" width="160" height="44" rx="9" class="cell link-green"/>
        <text x="620" y="150" text-anchor="middle">UI 实时增量</text>
        <text x="620" y="166" text-anchor="middle" font-size="11" class="dim">agent/assistant-stream</text>
        <rect x="540" y="200" width="160" height="44" rx="9" class="cell link-green"/>
        <text x="620" y="220" text-anchor="middle">Fork / Resume / 遥测</text>
        <text x="620" y="236" text-anchor="middle" font-size="11" class="dim">全部从日志派生</text>
        <g stroke-width="1.8" marker-end="url(#a)" class="link">
          <line x1="470" y1="82" x2="538" y2="82"/>
          <line x1="470" y1="152" x2="538" y2="152"/>
          <line x1="470" y1="222" x2="538" y2="222"/>
        </g>
        <defs><marker id="a" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
        <text x="135" y="150" font-size="12" transform="rotate(0)" class="dim">append-only：</text>
        <text x="135" y="170" font-size="12" class="dim">只追加，不修改。</text>
        <text x="135" y="190" font-size="12" class="dim">每条 assistant 消息</text>
        <text x="135" y="210" font-size="12" class="dim">内嵌产生它的</text>
        <text x="135" y="230" font-size="12" class="dim">精确流式时间线</text>
      </g>
    </svg>
    <figcaption>图 6：一个日志，多个投影——模型历史、UI、Fork/Resume 全部派生自同一份事实</figcaption>
  </figure>

## 为什么这样设计？

  - **可回放**：Fork（分叉会话）、Resume（恢复会话）、导出聊天记录、遥测统计，全都是"换个角度读日志"，零额外状态。
- **可审计**：每条 `assistant/message` 内嵌了产生它的**精确压缩流式时间线**；失败的尝试记在 `assistant/attempt` 里供排查，但不会混进模型历史。
- **防漂移**：因为"看到＝已记录"，模型不可能"脑补"出一段没发生过的对话——上下文永远有据可查。

## 工程上的讲究

  - **格式**：v0 用 `session.jsonl`（可 zstd 压缩），v1 起升级为 `session.vN.jsonl`；已提交的历史文件**永不重命名、替换或删除**，迁移只能一格一格 `vN → vN+1`。
- **投影接缝**：`dsh-session-projection` 包对日志做**增量 fold**，宿主用 `stateOf()` 读类型化状态——UI 不用每次全量重算。
- **扩展纪律**：想让模型"看见"新的东西？必须先扩展 `SessionEventMap`（即先给它一个日志事件类型），没有例外。

::: tip
把 Session Log 想成"飞行记录仪 + 唯一账本"：模型看到的一切都先记账；想改账，只能追加新条目，不能涂改旧条目。
:::

理论讲完了，下一篇是动手环节：**10 分钟跑起你的第一个 dsh**。
