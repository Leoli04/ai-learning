---
title: 工作流编排与主流 Agent 技术全景
---

# 工作流编排与主流 Agent 技术全景

> 约 9 分钟 · 关键词：n8n / Dify、LangGraph、编码 Agent、技术栈分层

## 编排：确定性流水线 + AI 节点

Agent 擅长开放性任务，但企业里大量需求是**固定流程**：每天汇总舆情 → AI 分类打标 → 推送企微群。这类事要的是稳定、可审计、可重跑——工作流编排工具的领地：

  <table>
    <tr><th>工具</th><th>定位</th></tr>
    <tr><td><strong>n8n</strong></td><td>开源可自部署，几百个节点生态，AI 只是画布上的节点之一</td></tr>
    <tr><td><strong>Dify</strong></td><td>偏 LLM 应用：RAG 知识库 + 工作流 + 应用发布一站式</td></tr>
    <tr><td><strong>Coze / 扣子</strong></td><td>字节系低代码 Bot 平台，上手最快</td></tr>
    <tr><td><strong>LangGraph</strong></td><td>代码级编排：把 Agent 流程画成状态图，节点可循环可回退</td></tr>
  </table>

选型准则一句话：**能画清楚流程的用编排，画不清楚的才交给自主 Agent**。两者正在融合——n8n 里可以嵌 AI Agent 节点，Agent 框架里也能调用固定工作流。

## 主流 Agent 产品与技术盘点（2025–2026）

  <table>
    <tr><th>阵营</th><th>代表</th><th>关键技术组合</th></tr>
    <tr><td><strong>编码 Agent</strong></td><td>Claude Code、Cursor、GitHub Copilot、OpenAI Codex、Devin</td><td>Agent 循环 + 文件/终端/搜索工具 + 沙箱隔离 + 计划与子智能体 + Skill 沉淀项目规范</td></tr>
    <tr><td><strong>通用框架</strong></td><td>LangChain / LangGraph、CrewAI、AutoGen、OpenAI Agents SDK</td><td>可编排的 Agent 循环、多角色协作、记忆与工具抽象、可观测性</td></tr>
    <tr><td><strong>开源 Harness</strong></td><td>DeepSeek Harness (dsh)、OpenHands</td><td>插件化架构、会话日志、权限审批、多种运行形态（web/headless/SDK）</td></tr>
    <tr><td><strong>浏览器/操作类</strong></td><td>Manus、OpenAI Operator、Computer Use</td><td>视觉理解 + 屏幕操作（看图点鼠标）+ 虚拟机沙箱 + 任务回放</td></tr>
    <tr><td><strong>低代码平台</strong></td><td>Dify、Coze、n8n</td><td>节点画布 + RAG 内置 + 触发器生态</td></tr>
  </table>

## 共性技术栈：所有 Agent 都长这样

  <figure class="figure">
    <svg viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg">
      <g font-size="12">
        <rect x="60" y="24" width="600" height="52" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="90" y="46" font-weight="bold">交互层</text>
        <text x="200" y="46" font-size="11">CLI / Web UI / IDE 插件 / API</text>
        <text x="90" y="66" font-size="10" class="dim">人下指令、看进度、做审批</text>
        <rect x="60" y="84" width="600" height="52" rx="9" class="cell"/>
        <text x="90" y="106" font-weight="bold">编排层</text>
        <text x="200" y="106" font-size="11">Agent 循环（ReAct/Plan）· 多智能体协作 · 人工介入点</text>
        <text x="90" y="126" font-size="10" class="dim">决定"下一步干什么"</text>
        <rect x="60" y="144" width="600" height="52" rx="9" class="cell link-green"/>
        <text x="90" y="166" font-weight="bold">工具层</text>
        <text x="200" y="166" font-size="11">Function Calling · MCP · 文件/终端/浏览器 · Skill 操作手册</text>
        <text x="90" y="186" font-size="10" class="dim">真正"动手"的地方</text>
        <rect x="60" y="204" width="600" height="52" rx="9" class="cell link-purple"/>
        <text x="90" y="226" font-weight="bold">记忆层</text>
        <text x="200" y="226" font-size="11">会话日志 · 长期记忆 · RAG / 向量库</text>
        <text x="90" y="246" font-size="10" class="dim">知道什么、记住了什么</text>
        <rect x="60" y="264" width="600" height="52" rx="9" class="cell link-orange"/>
        <text x="90" y="286" font-weight="bold">模型层</text>
        <text x="200" y="286" font-size="11">LLM / VLM / 推理模型 · 量化部署 · 分层路由</text>
        <text x="90" y="306" font-size="10" class="dim">思考的引擎，可替换可分层</text>
        <rect x="60" y="324" width="600" height="52" rx="9" class="cell"/>
        <text x="90" y="346" font-weight="bold">安全层（纵切所有层）</text>
        <text x="330" y="346" font-size="11">沙箱隔离 · 权限审批 · 输出校验 · 审计日志</text>
        <text x="90" y="366" font-size="10" class="dim">不是一层，是贯穿每一层的约束</text>
      </g>
    </svg>
    <figcaption>图 12：Agent 技术栈六层 + 贯穿式安全层——换任何一层的产品，结构都类似</figcaption>
  </figure>

::: tip
把任意一个主流 Agent 拆开，都是这六层的不同实现组合。**差异通常不在"有没有"，而在"哪一层做得好"**——编码 Agent 强在工具与沙箱，低代码平台强在编排与生态，开源 Harness 强在可定制与透明。
:::

全景看完，最后回头冷静盘一盘：**哪些问题至今没解决**？
