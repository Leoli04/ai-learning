---
title: 启动分层：Profile / Bundle / Patch，像叠千层饼一样组装系统
---

# 启动分层：Profile / Bundle / Patch，像叠千层饼一样组装系统

> 约 6 分钟 · 关键词：Profile、Bundle、Patch、分层叠加

## 一个问题：几十个插件，启动时怎么排？

上一篇说"一切皆插件"，那一个运行中的 dsh 到底装了哪些插件、按什么顺序装？答案是一棵**启动时逐层叠加的插件树**，由三个概念组成：

### 1️⃣ Profile（配置档案）＝ 套餐

Profile 是一组**命名的组合**，声明这次启动要用哪些 Bundle。内置五种：`web`、`headless`、`sdk`、`sdk-minimal`、`acp`。你运行 `dsh web` 时，其实就是在用 `web` 这个套餐。

### 2️⃣ Bundle（捆绑包）＝ 配菜包

Bundle 是插件配置的**分发格式**，每个包在 `package.json` 的 `dsh` 字段里声明自己提供什么。最底层的 `dsh-base` 包含所有形态共享的能力：模型适配器、工具、持久化、沙箱与审批策略等。上面的 Bundle 再往叠：web 加浏览器界面、sdk 加 JSON-RPC 服务……

### 3️⃣ Patch（补丁）＝ 你说了算的最后一笔

Patch 通过**插件 id 定位一行配置，整行替换或插入新行**。叠加顺序固定为：Profile 里的 Bundle 依次铺底 → Profile 自己的 patch → 用户 home 目录的 patch → 命令行 `--patch`。越往后优先级越高，所以**你永远可以覆盖官方配置，而不用改任何源码**。

  <figure class="figure">
    <svg viewBox="0 0 720 320" xmlns="http://www.w3.org/2000/svg">
      <g font-size="14">
        <!-- 层1 -->
        <rect x="60" y="240" width="600" height="52" rx="9" class="cell"/>
        <text x="90" y="272">① dsh-base（共享底座：模型/工具/持久化/沙箱）</text>
        <!-- 层2 -->
        <rect x="60" y="180" width="600" height="52" rx="9" class="cell"/>
        <text x="90" y="212">② dsh-web-app（浏览器界面）</text>
        <!-- 层3 -->
        <rect x="60" y="120" width="600" height="52" rx="9" class="cell"/>
        <text x="90" y="152">③ Profile 自带 patch</text>
        <!-- 层4 -->
        <rect x="60" y="60" width="600" height="52" rx="9" stroke-width="2" class="cell-em link-green"/>
        <text x="90" y="92">④ 你的 patch（home 级 / 命令行 --patch，优先级最高）</text>
        <!-- 侧标注 -->
        <text x="30" y="272" font-size="12" class="dim">底层</text>
        <text x="30" y="92" font-size="12" class="dim">顶层</text>
        <path d="M 680 300 L 680 40" stroke-width="2" marker-end="url(#arrowO)" class="link-orange"/>
        <defs><marker id="arrowO" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-orange-fill"/></marker></defs>
        <text x="694" y="170" font-size="12" transform="rotate(90 694 170)" class="dim">覆盖方向：上层覆盖下层</text>
      </g>
    </svg>
    <figcaption>图 3：<code>dsh web</code> 的叠加过程——上层 patch 可整行替换下层配置</figcaption>
  </figure>

## 热重载：改配置不用重启

自定义 Profile 和内置 `web` Profile 默认支持 **live patch reload**——patch 一保存，插件树原地热更新。而 `headless`、`sdk` 等"一次性"形态只在启动时应用一次（一次性任务跑一半换依赖，会把生命周期搞坏，官方干脆禁止）。

  ::: tip
想看你的 dsh 实际加载了什么树？跑一条命令： <pre>`dsh --profile web --dump-config`</pre> 它会把最终生效的完整配置打印出来，是调试 patch 的第一工具。
:::

分层解决的是"怎么组装"，那插件之间"怎么交换能力"？下一篇讲 dsh 最核心的抽象：**Capability Seam（能力接缝）**。
