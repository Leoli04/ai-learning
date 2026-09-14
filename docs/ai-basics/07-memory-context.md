---
title: 记忆与上下文工程：窗口有限，记忆分层
---

# 记忆与上下文工程：窗口有限，记忆分层

> 约 6 分钟 · 关键词：记忆分层、上下文工程、窗口预算

## 为什么模型需要记忆？

模型是**无状态**的：它不"记得"你。每次调用都是把一整段文字重新喂进去算一遍，会话一关，之前聊过的全部消失。

那把所有该记的东西都塞进这段文字里？也不现实——**上下文窗口是有限且昂贵的资源**：装不下整个公司文档库，开销随长度上涨，塞得越多，模型反而越容易抓不住重点。

工程上的解法很自然：**该记住的东西分层存起来，等需要哪一层、哪一段，再按需注入。**

## 记忆分四层，各管一段

  <figure class="figure">
    <svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg">
      <g font-size="13">
        <rect x="40" y="30" width="640" height="52" rx="10" stroke-width="2" class="cell-em link"/>
        <text x="80" y="52" font-weight="bold">工作记忆</text>
        <text x="200" y="52" font-size="12">＝ 当前上下文窗口：这轮对话的全部内容</text>
        <text x="80" y="72" font-size="11" class="dim">快，但窗口有限，会话结束即失</text>
        <rect x="40" y="102" width="640" height="52" rx="10" class="cell link-green"/>
        <text x="80" y="124" font-weight="bold">会话记忆</text>
        <text x="200" y="124" font-size="12">＝ Session Log / 摘要：本会话的事实账本，可恢复、可分叉</text>
        <text x="80" y="144" font-size="11" class="dim">断线重连、回到历史节点，靠它</text>
        <rect x="40" y="174" width="640" height="52" rx="10" class="cell link-purple"/>
        <text x="80" y="196" font-weight="bold">长期记忆</text>
        <text x="200" y="196" font-size="12">＝ 用户偏好 / 项目约定：跨会话持久，常以向量库或文件存储</text>
        <text x="80" y="216" font-size="11" class="dim">"记住我喜欢简洁回复"就存在这一层</text>
        <rect x="40" y="246" width="640" height="44" rx="10" class="cell link-orange"/>
        <text x="80" y="266" font-weight="bold">技能库（Skill）</text>
        <text x="240" y="266" font-size="12">＝"被教会的方法"：按需加载的操作手册，下一篇细讲</text>
        <text x="80" y="283" font-size="11" class="dim">前三层记事实，这一层存能力</text>
      </g>
    </svg>
    <figcaption>图 7：记忆四层——工作记忆、会话记忆、长期记忆、技能库</figcaption>
  </figure>

关键洞察是这条分界线：**前两层是"这次任务的现场"，后两层是"跨任务攒下来的资产"**。越往下越持久，也越不需要一直占着当前窗口——用的时候才捞上来。

## 上下文工程：新的主战场

Prompt 工程管"一句话怎么写"，**上下文工程（Context Engineering）**管"整个窗口装什么"：系统指令、检索到的资料、工具说明、记忆片段、当前任务——每一样都占 token，也都在争夺模型有限的注意力。

核心取舍只有一句话：**窗口是稀缺资源，放对东西比放多东西重要。**

  <table>
    <tr><th>手段</th><th>做法</th></tr>
    <tr><td>按需加载</td><td>Skill 先只留名称和一句话描述，任务匹配上再读正文</td></tr>
    <tr><td>记忆压缩</td><td>老对话折叠成摘要，原文落到会话日志里备查</td></tr>
    <tr><td>检索注入</td><td>RAG 只取 Top-K 片段，不把整库塞进窗口</td></tr>
    <tr><td>工具瘦身</td><td>工具说明按场景分组，这次用不到的先摘出去</td></tr>
  </table>

::: tip
RAG 是"临时查资料"，记忆是"攒经验"——一个补外部知识，一个补跨会话的连续性。两者解决的是同一个问题：**模型的窗口太小、生命周期太短。**
:::

记忆管"经历过的事"，但"被教会的方法"要单独沉淀——下一篇：**Skill 与 MCP**。
