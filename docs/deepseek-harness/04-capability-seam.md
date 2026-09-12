---
title: 能力接缝：为什么"换一个零件，改的是整个产品"
---

# 能力接缝：为什么"换一个零件，改的是整个产品"

> 约 6 分钟 · 关键词：Seam、Definition / Provider / Consumer、Subagent、Agent Teams

## 什么是 Seam（接缝）？

衣服的"接缝"是两块布料拼接的地方——拆开缝线，就能换一块布。dsh 里的 **Seam（能力接缝）**同理：它是系统里**可整体替换的一段能力**。每个 Seam 由三种角色构成，缺一不可：

  1. **Service Definition（接口声明）**——规定"这个能力长什么样"；
2. **Service Provider（提供者）**——真正干活的人；
3. **Consumer（消费者）**——使用能力的一方，通常是模型能调用的 tool。

  > 官方特别强调：一个包可以身兼多角，但**单一角色构不成 Seam**。想新增一种能力，三个角色必须设计齐全。

  <figure class="figure">
    <svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg">
      <g font-size="14">
        <!-- 左：消费者们 -->
        <rect x="40" y="50" width="180" height="44" rx="9" class="cell"/>
        <text x="130" y="78" text-anchor="middle">tool: 读文件</text>
        <rect x="40" y="120" width="180" height="44" rx="9" class="cell"/>
        <text x="130" y="148" text-anchor="middle">tool: 跑终端命令</text>
        <rect x="40" y="190" width="180" height="44" rx="9" class="cell"/>
        <text x="130" y="218" text-anchor="middle">tool: LSP 代码诊断</text>
        <!-- 中：接缝 -->
        <rect x="270" y="105" width="180" height="80" rx="12" stroke-width="2" class="cell-em link-purple"/>
        <text x="360" y="138" text-anchor="middle" font-weight="bold">Seam：执行环境</text>
        <text x="360" y="162" text-anchor="middle" font-size="12" class="dim">统一接口声明</text>
        <!-- 右：提供者 -->
        <rect x="510" y="50" width="170" height="44" rx="9" class="cell link-green"/>
        <text x="595" y="70" text-anchor="middle">Provider A</text>
        <text x="595" y="86" text-anchor="middle" font-size="11" class="dim">本机 Filesystem</text>
        <rect x="510" y="190" width="170" height="44" rx="9" class="cell link-green"/>
        <text x="595" y="210" text-anchor="middle">Provider B</text>
        <text x="595" y="226" text-anchor="middle" font-size="11" class="dim">远程 Sandbox</text>
        <!-- 连线 -->
        <g stroke-width="1.6" opacity="0.75" class="link">
          <line x1="220" y1="72" x2="270" y2="125"/>
          <line x1="220" y1="142" x2="270" y2="145"/>
          <line x1="220" y1="212" x2="270" y2="165"/>
          <line x1="450" y1="130" x2="510" y2="80"/>
          <line x1="450" y1="160" x2="510" y2="205"/>
        </g>
        <text x="360" y="272" text-anchor="middle" font-size="12" class="dim">换 Provider：把接缝指向远程 Sandbox，读文件/终端/LSP 全部跟着搬到云上</text>
      </g>
    </svg>
    <figcaption>图 4：消费者只认接缝不认人——换 Provider 即整体换能力</figcaption>
  </figure>

## 为什么这个设计厉害？看官方给的例子

架构文档里有个精彩的案例：**Filesystem（文件系统）和 Subprocess（子进程）共享同一个"执行世界"**。因为它们挂在同一条 Seam 后面，所以只要把这条 Seam 的 Provider 从"本机"指到"远程沙箱"，Bash、PTY 终端、LSP 代码服务**全部连带迁移到云端**——不用改任何工具代码。这就是"换一个零件，改的是整个产品"。

## 同一个 Seam，多种实现

Subagent（子智能体）也是一条 Seam：接口后面既可以是"从零启动一个全新的子 Agent"，也可以是"把任务委托给其他产品"。上层消费者完全无感。实验性的 **Agent Teams** 则是在 subagent 之上叠加的进阶 Seam：持久的花名册（roster）、任务看板（task board）和邮箱（mailbox），让多个 Agent 长期协作。

::: tip
Seam = 接口（Definition）+ 干活的（Provider）+ 用功能的（Consumer）。设计新能力时三个都要有；想让能力可替换，就让它只通过 Seam 暴露。
:::

能力怎么"接"上了？靠的是事件系统。下一篇拆解 dsh 的**事件三域**和一次完整任务的执行流水线。
