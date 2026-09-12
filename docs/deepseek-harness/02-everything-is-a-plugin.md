---
title: 一切皆插件：没有"特权阶级"的架构
---

# 一切皆插件：没有"特权阶级"的架构

> 约 6 分钟 · 关键词：插件、Cordis、ctx、可逆 effect

## 传统框架的问题：核心是"硬"的

大多数软件框架都有一条"特权核心"：核心代码说了算，你只能围着它写扩展点。想换掉核心里的某个行为？改源码，或者等官方开个口子。

dsh 反其道而行：**它没有特权核心**。模型适配器、工具注册表、会话日志，甚至**驱动 Agent 干活的那个主循环（agent loop）本身**，全都是插件。官方架构文档的原话是：产品的每个部分都是插件，均可通过配置替换。

  <figure class="figure">
    <svg viewBox="0 0 720 340" xmlns="http://www.w3.org/2000/svg">
      <!-- 中心 ctx -->
      <circle cx="360" cy="170" r="64" fill="rgba(91,140,255,0.12)" stroke="#5b8cff" stroke-width="2"/>
      <text x="360" y="163" text-anchor="middle" class="svg-text" font-size="18" font-weight="bold">ctx</text>
      <text x="360" y="185" text-anchor="middle" class="svg-dim" font-size="12">共享上下文</text>
      <!-- 周围插件 -->
      <g font-size="13">
        <rect x="40" y="40" width="170" height="44" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="125" y="60" text-anchor="middle" class="svg-text">模型适配器</text>
        <text x="125" y="76" text-anchor="middle" class="svg-dim" font-size="11">ctx.llm</text>
        <rect x="510" y="40" width="170" height="44" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="595" y="60" text-anchor="middle" class="svg-text">工具注册表</text>
        <text x="595" y="76" text-anchor="middle" class="svg-dim" font-size="11">ctx.tools</text>
        <rect x="40" y="148" width="170" height="44" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="125" y="168" text-anchor="middle" class="svg-text">会话日志</text>
        <text x="125" y="184" text-anchor="middle" class="svg-dim" font-size="11">ctx.sessions</text>
        <rect x="510" y="148" width="170" height="44" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="595" y="168" text-anchor="middle" class="svg-text">Agent 主循环</text>
        <text x="595" y="184" text-anchor="middle" class="svg-dim" font-size="11">ctx.agentLoop</text>
        <rect x="40" y="256" width="170" height="44" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="125" y="276" text-anchor="middle" class="svg-text">系统提示词组装</text>
        <text x="125" y="292" text-anchor="middle" class="svg-dim" font-size="11">ctx.systemPrompt</text>
        <rect x="510" y="256" width="170" height="44" rx="9" fill="#161b22" stroke="#30363d"/>
        <text x="595" y="276" text-anchor="middle" class="svg-text">你的自定义插件</text>
        <text x="595" y="292" text-anchor="middle" class="svg-dim" font-size="11">想装什么装什么</text>
      </g>
      <!-- 连线 -->
      <g stroke="#5b8cff" stroke-width="1.6" fill="none" opacity="0.7">
        <line x1="210" y1="62" x2="310" y2="130"/>
        <line x1="510" y1="62" x2="410" y2="130"/>
        <line x1="210" y1="170" x2="296" y2="170"/>
        <line x1="510" y1="170" x2="424" y2="170"/>
        <line x1="210" y1="278" x2="310" y2="210"/>
        <line x1="510" y1="278" x2="410" y2="210"/>
      </g>
    </svg>
    <figcaption>图 2：所有能力都是挂在 ctx 上的插件，包括"主循环"自己</figcaption>
  </figure>

## 靠什么做到的？Cordis 框架

dsh 构建在开源框架 <a href="https://github.com/cordiverse/cordis" target="_blank">Cordis</a> 之上。Cordis 的核心思路可以用三个词概括：

  1. **服务（Service）**：每个插件向共享上下文 `ctx` 贡献服务，比如 `ctx.tools`（工具）、`ctx.llm`（模型）。
2. **事件（Event）**：插件之间不直接调用，而是通过事件互相感知——谁关心什么事件，就监听什么。
3. **可逆 effect**：插件注册进来的任何东西，卸载插件时会**自动回退**。装了就生效、卸了就还原，不会留下"残留物"。

  ::: tip
ctx 像一块"多孔插座板"，每个插件是插上去的电器。拔掉任何一个，插座板本身不受影响；再插一个同型号的，功能无缝替换。
:::

## 这对使用者意味着什么？

  - **换模型**＝换一个 LLM adapter 插件；
- **加工具**＝注册一个 tool 插件；
- **改行为**（比如拦截每次工具调用做审计）＝监听对应事件，不动核心一行代码；
- **改主循环**＝替换 `ctx.agentLoop` 上的实现——这在别的框架里通常想都不敢想。

  ::: warning
dsh 目前处于开发者预览（Developer Preview）阶段，官方明确说后续会有破坏性变更，生产使用需谨慎。
:::

那这些插件在启动时是怎么"叠"起来的？这就是下一篇要讲的 **Profile → Bundle → Patch** 分层机制。
