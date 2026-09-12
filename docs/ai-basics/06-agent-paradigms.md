---
title: Agent 核心范式：ReAct、规划、反思与多智能体
---

# Agent 核心范式：ReAct、规划、反思与多智能体

> 约 9 分钟 · 关键词：Function Calling、ReAct、Plan-and-Execute、Reflexion、Multi-Agent

## 底座机制：Function Calling（工具调用）

一切 Agent 的地基。你把工具的"说明书"（名称、参数 schema、用途描述）随请求发给模型，模型需要时输出一段**结构化的调用意图**：

  <pre><code>{"name": "get_weather", "arguments": {"city": "上海"}}</code></pre>

注意：**模型自己不执行任何东西**，它只"点名"。真正执行的是你的程序，执行结果再喂回给模型。模型 ↔ 程序之间就是这一来一回的"点菜—上菜"循环。

## 范式演进：从"边想边做"到"团队作战"

  <figure class="figure">
    <svg viewBox="0 0 720 430" xmlns="http://www.w3.org/2000/svg">
      <g font-size="12">
        <!-- ReAct -->
        <rect x="30" y="30" width="330" height="150" rx="12" stroke-width="2" class="cell-em link-purple"/>
        <text x="195" y="54" text-anchor="middle" font-weight="bold" font-size="14">ReAct（2022）· 鼻祖范式</text>
        <text x="195" y="76" text-anchor="middle" class="dim">想 → 动 → 看，边干边决定下一步</text>
        <text x="195" y="98" text-anchor="middle" class="dim">✅ 简单通用，仍是绝大多数框架的默认</text>
        <text x="195" y="120" text-anchor="middle" class="dim">⚠️ 走一步看一步：容易绕路、死循环</text>
        <text x="195" y="150" text-anchor="middle" font-size="11">思考(Reason) → 行动(Act) → 观察(Observe) 循环</text>
        <!-- Plan-and-Execute -->
        <rect x="390" y="30" width="300" height="150" rx="12" class="cell"/>
        <text x="540" y="54" text-anchor="middle" font-weight="bold" font-size="14">Plan-and-Execute · 先规划后执行</text>
        <text x="540" y="76" text-anchor="middle" class="dim">先让模型列出完整步骤清单</text>
        <text x="540" y="98" text-anchor="middle" class="dim">再逐步执行，失败才重新规划</text>
        <text x="540" y="120" text-anchor="middle" class="dim">✅ 长任务更稳、更省 token</text>
        <text x="540" y="142" text-anchor="middle" class="dim">⚠️ 计划赶不上变化时需重规划</text>
        <!-- Reflection -->
        <rect x="30" y="210" width="330" height="150" rx="12" class="cell"/>
        <text x="195" y="234" text-anchor="middle" font-weight="bold" font-size="14">Reflexion · 自我复盘</text>
        <text x="195" y="256" text-anchor="middle" class="dim">执行后让模型自查："哪步错了？为什么？"</text>
        <text x="195" y="278" text-anchor="middle" class="dim">把教训写进记忆，下一轮改进</text>
        <text x="195" y="300" text-anchor="middle" class="dim">✅ 显著提升复杂任务成功率</text>
        <text x="195" y="322" text-anchor="middle" class="dim">⚠️ 多一轮 LLM 调用，更慢更贵</text>
        <!-- Multi-Agent -->
        <rect x="390" y="210" width="300" height="150" rx="12" stroke-width="2" class="cell-em link"/>
        <text x="540" y="234" text-anchor="middle" font-weight="bold" font-size="14">Multi-Agent · 多智能体协作</text>
        <text x="540" y="256" text-anchor="middle" class="dim">编排者(Orchestrator)拆任务派活</text>
        <text x="540" y="278" text-anchor="middle" class="dim">执行者(Subagent)各干一摊，上下文隔离</text>
        <text x="540" y="300" text-anchor="middle" class="dim">✅ 擅长大型、可并行的任务</text>
        <text x="540" y="322" text-anchor="middle" class="dim">⚠️ 通信成本高，调试复杂</text>
        <text x="360" y="400" text-anchor="middle" class="dim">四者不互斥：现代 Agent 常是 ReAct 打底 + 计划 + 复盘 + 子智能体按需启用</text>
      </g>
    </svg>
    <figcaption>图 6：Agent 四大范式——从单循环到团队协作</figcaption>
  </figure>

## ReAct 循环长什么样？

  <pre><code>用户：帮我把仓库里的 TODO 整理成清单。
Thought: 我需要先找到所有 TODO 标记。
Action: grep(pattern="TODO", path="src/")
Observation: src/api.py:12 TODO 校验分页参数；src/db.py:40 TODO 加索引
Thought: 找到 2 处，直接汇总即可，无需更多工具。
Final Answer: 共 2 个 TODO：1) api.py 校验分页参数 2) db.py 加索引</code></pre>

## 成熟 Agent 还标配四样"护栏"

  - **最大步数 / 预算限制**：防死循环烧钱；
- **沙箱 + 权限审批**：文件写入、命令执行先隔离或先问人；
- **结构化输出校验**：JSON 不合法就重试；
- **人工介入点（human-in-the-loop）**：关键决策停下等确认——企业落地的刚需。

::: tip
Agent = **LLM + 工具 + 循环**。范式只回答一个问题：**循环里"下一步"由谁、按什么策略决定**——ReAct 走一步看一步，Plan 先定清单，Reflexion 错了复盘，Multi-Agent 拉团队。
:::

会干活了，但会话一关就失忆——下一篇：**记忆与上下文工程**。
