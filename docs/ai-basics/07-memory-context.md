---
title: 记忆与上下文工程：把"老司机的经验"固化下来
---

# 记忆与上下文工程：把"老司机的经验"固化下来

> 约 7 分钟 · 关键词：Skill、记忆分层、上下文工程

## 为什么需要 Skill？

会了工具调用之后，新问题来了：同一个任务，每次都要在提示词里从头教一遍"该怎么干"。比如"发布微信公众号文章"涉及排版、上传图片、调用 API 的十几步细节——写进每次对话既贵又容易漏。

**Skill（技能）**的解法：把一套**可复用的方法论打包成文件**（通常是一个带说明的 SKILL.md 文件夹），平时安静地放着，**任务匹配时才加载**。它不是代码插件，而是"写给模型看的操作手册"。

  - **解决什么**：经验复用——一次沉淀，处处生效，团队可共享；
- **为什么可行**：模型读文档就能学会流程，就像新员工拿着 SOP 也能干老员工的活；
- **代表实践**：Claude 的 Agent Skills 规范、各类开源 Agent 的 skills 目录（本站 DeepSeek Harness 系列里的 `.agents/skills` 就是同类设计）。

## 记忆：分层的，不是一块

模型本身"金鱼记忆"（关掉会话就忘）。工程上的解法是把记忆**分层存储，按需注入上下文**：

  <figure class="figure">
    <svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg">
      <g font-size="13">
        <rect x="40" y="30" width="640" height="52" rx="10" fill="rgba(91,140,255,0.10)" stroke="#5b8cff" stroke-width="2"/>
        <text x="80" y="52" class="svg-text" font-weight="bold">工作记忆</text>
        <text x="200" y="52" class="svg-text" font-size="12">＝ 当前上下文窗口：这轮对话的全部内容</text>
        <text x="80" y="72" class="svg-dim" font-size="11">快，但窗口有限，会话结束即失</text>
        <rect x="40" y="102" width="640" height="52" rx="10" fill="#161b22" stroke="#3fb950"/>
        <text x="80" y="124" class="svg-text" font-weight="bold">会话记忆</text>
        <text x="200" y="124" class="svg-text" font-size="12">＝ Session Log / 摘要：本会话的事实账本，可恢复、可分叉</text>
        <text x="80" y="144" class="svg-dim" font-size="11">断线重连、回到历史节点，靠它</text>
        <rect x="40" y="174" width="640" height="52" rx="10" fill="#161b22" stroke="#bc8cff"/>
        <text x="80" y="196" class="svg-text" font-weight="bold">长期记忆</text>
        <text x="200" y="196" class="svg-text" font-size="12">＝ 用户偏好 / 项目约定：跨会话持久，常以向量库或文件存储</text>
        <text x="80" y="216" class="svg-dim" font-size="11">"记住我喜欢简洁回复"就存在这一层</text>
        <rect x="40" y="246" width="640" height="44" rx="10" fill="#161b22" stroke="#f0883e"/>
        <text x="80" y="266" class="svg-text" font-weight="bold">技能库（Skill）</text>
        <text x="240" y="266" class="svg-text" font-size="12">＝ 不是"经历过的事"，而是"被教会的方法"：按需加载的操作手册</text>
        <text x="80" y="283" class="svg-dim" font-size="11">前三层记事实，这一层存能力</text>
      </g>
    </svg>
    <figcaption>图 5：记忆四层——工作记忆、会话记忆、长期记忆、技能库</figcaption>
  </figure>

## 上下文工程：新的主战场

Prompt 工程管"一句话怎么写"，**上下文工程（Context Engineering）**管"整个窗口装什么"：系统指令、检索到的资料、工具说明、记忆片段、当前任务——每一样都占 token，都要争夺模型有限的注意力。核心取舍就一句话：**窗口是稀缺资源，放对东西比放多东西重要。**常见的手段包括按需加载（Skill 的懒加载）、记忆压缩（老对话折叠成摘要）、检索注入（RAG 只取 Top-K）等。

  ::: tip
RAG 是"临时查资料"，记忆是"攒经验"，Skill 是"抄作业"——三者共同解决同一个问题：**模型的窗口太小、生命周期太短。**
:::

记忆管"经历过的事"，但"被教会的方法"要单独沉淀——下一篇：**Skill 与 MCP**。
