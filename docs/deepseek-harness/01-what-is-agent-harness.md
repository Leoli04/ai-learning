---
title: 什么是 Agent Harness？——给大模型装上"底盘和方向盘"
---

# 什么是 Agent Harness？——给大模型装上"底盘和方向盘"

> 约 5 分钟 · 关键词：Agent、Harness、dsh、DeepSeek

## 先说结论

**大模型（LLM）只会"说话"，不会"做事"。**它没法自己打开文件、跑命令、记住上一步干了什么。要让它真正像一个"智能体（Agent）"一样干活，外面必须套一层"工作服"——这层工作服就叫 **Harness**（马具/挽具，寓意"套上缰绳才能驾驭"）。

  > DeepSeek Harness（命令叫 `dsh`）就是 DeepSeek 官方开源的一个 Agent Harness，口号非常直白：**Everything is a Plugin（一切皆插件）**。

## 一个通俗的类比：发动机 vs 整车

把 LLM 想成一台**发动机**：动力很强，但你不能开着发动机上路。你需要：

  - **底盘和方向盘**——决定动力往哪使（工具调用、任务规划）
- **仪表盘**——让你知道它干到哪一步了（会话记录、状态展示）
- **安全带和刹车**——防止它乱来（权限审批、沙箱隔离）

Harness 就是把这些东西全部装好，交付给你一辆"能开的车"。

  <figure class="figure">
    <svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg">
      <!-- 用户 -->
      <rect x="20" y="110" width="130" height="70" rx="12" class="cell"/>
      <text x="85" y="140" text-anchor="middle" font-size="16">你（用户）</text>
      <text x="85" y="162" text-anchor="middle" font-size="12" class="dim">提需求、做审批</text>
      <line x1="150" y1="145" x2="210" y2="145" stroke-width="2" class="link"/>
      <polygon points="210,145 200,140 200,150" class="accent-blue-fill"/>
      <!-- Harness 大框 -->
      <rect x="215" y="40" width="290" height="220" rx="14" stroke-width="2" class="cell-em link"/>
      <text x="360" y="68" text-anchor="middle" font-size="17" font-weight="bold">Harness（dsh）</text>
      <rect x="235" y="85" width="250" height="36" rx="8" class="cell"/>
      <text x="360" y="108" text-anchor="middle" font-size="13">会话管理 · 记住每一步</text>
      <rect x="235" y="130" width="250" height="36" rx="8" class="cell"/>
      <text x="360" y="153" text-anchor="middle" font-size="13">工具调用 · 读文件/跑命令</text>
      <rect x="235" y="175" width="250" height="36" rx="8" class="cell"/>
      <text x="360" y="198" text-anchor="middle" font-size="13">权限审批 · 沙箱隔离</text>
      <text x="360" y="240" text-anchor="middle" font-size="12" class="dim">Agent 循环：想 → 做工具调用 → 看 → 再想</text>
      <line x1="505" y1="145" x2="565" y2="145" stroke-width="2" class="link"/>
      <polygon points="565,145 555,140 555,150" class="accent-blue-fill"/>
      <!-- LLM -->
      <rect x="570" y="110" width="130" height="70" rx="12" class="cell link-purple"/>
      <text x="635" y="140" text-anchor="middle" font-size="16">LLM</text>
      <text x="635" y="162" text-anchor="middle" font-size="12" class="dim">"大脑"：只负责推理</text>
      <!-- 底部工具 -->
      <rect x="235" y="270" width="70" height="24" rx="6" class="cell link-green"/>
      <text x="270" y="286" text-anchor="middle" font-size="11">文件系统</text>
      <rect x="315" y="270" width="70" height="24" rx="6" class="cell link-green"/>
      <text x="350" y="286" text-anchor="middle" font-size="11">终端</text>
      <rect x="395" y="270" width="70" height="24" rx="6" class="cell link-green"/>
      <text x="430" y="286" text-anchor="middle" font-size="11">浏览器</text>
    </svg>
    <figcaption>图 1：LLM 是发动机，Harness 是整台车——负责干活、管状态、保安全</figcaption>
  </figure>

## dsh 能以什么形态跑？

同一个内核，dsh 提供了几种"套餐"（官方叫 Profile）：

  <table>
    <tr><th>形态</th><th>一句话说明</th></tr>
    <tr><td><code>dsh web</code></td><td>启动本地 Web 界面（默认 <code>http://127.0.0.1:3080</code>），最常用的上手方式</td></tr>
    <tr><td><code>headless</code></td><td>无界面，一次性跑完任务就退出，适合脚本/自动化</td></tr>
    <tr><td><code>sdk</code> / <code>sdk-minimal</code></td><td>把 Agent 能力嵌到你自己的程序里（有 Python SDK）</td></tr>
    <tr><td><code>acp</code></td><td>纯自动化协议服务，给别的软件当"后端大脑"</td></tr>
  </table>

::: tip
用户提需求 → Harness 安排 LLM 推理 → 调用工具干活 → 结果记进会话 → 循环直到完成。所有工程难题（记忆、安全、工具）都在 Harness 这一层解决。
:::

## 那"一切皆插件"是什么意思？

这是 dsh 最有意思的设计——下一篇文章专门讲。
