---
title: Skill：把"这件事该怎么做"写进仓库
---

# Skill：把"这件事该怎么做"写进仓库

> 约 10 分钟 · 关键词：SKILL.md、发现优先级、渐进式披露、AGENTS.md

## Skill 的定性：它是"可选的指令"，不是会话事件

dsh 文档里有一句定性很关键：**skill 是可选的指令，而不是会话事件**。也就是说，它不参与会话状态机，不改变轮次与步骤的流转——它只是在需要的时候，被当成一段指令加载进来。

在实现上它被拆成一个能力族，正好是第 4 篇讲的三层结构：

  - **Service Definition**（`ctx.skills`）：注册表，负责合并各提供方的目录、裁决重名；
  - **Service Provider**：本地文件系统提供方（扫目录）、随包徽章提供方；
  - **Consumer**：一个面向模型的 **`skill` 工具**——它是模型"取用技能"的唯一入口。

## 放哪里：一张优先级表（这篇最实用的部分）

本地提供方按 rank 从小到大扫描这几个根目录：

  <table>
    <tr><th>Rank</th><th>来源</th><th>根目录</th></tr>
    <tr><td>100</td><td><code>project-dsh</code></td><td><code>&lt;项目根&gt;/.dsh/skills</code></td></tr>
    <tr><td>200</td><td><code>project-agents</code></td><td><code>&lt;项目根&gt;/.agents/skills</code></td></tr>
    <tr><td>300</td><td><code>custom</code></td><td>配置里的 <code>customSkillDirs</code></td></tr>
    <tr><td>400</td><td><code>user-dsh</code></td><td><code>&lt;DSH_HOME&gt;/skills</code></td></tr>
    <tr><td>500</td><td><code>user-agents</code></td><td><code>&lt;agentsHome&gt;/skills</code></td></tr>
    <tr><td>600</td><td><code>bundled</code></td><td>随包内置的 skill 目录</td></tr>
  </table>

两条规则值得记住：

  - **项目根**定义为包含 `.git` 的最近祖先目录（找不到时退到当前 cwd）。所以"项目级 skill"跟着仓库走——**换个分支、换个仓库，技能集就跟着换。**
  - **rank 越小优先级越高**：项目里的覆盖用户级的，用户级的覆盖随包内置的。这和 `git config`、`.editorconfig` 的层叠思路完全一致。

同一个层级内部如果出现重名，依次按 rank、提供方注册顺序、本地顺序裁决——**最近的那一层赢**。

## 文件长什么样

形态只有两种，都很朴素：

  - **目录包**：`<name>/SKILL.md`（可以带 `references/`、`scripts/` 等兄弟目录）；
  - **扁平文件**：`<name>.md`。

名字必须是 kebab-case（`^[a-z0-9]+(?:-[a-z0-9]+)*$`）。另外注意：**递归发现 `**/SKILL.md` 不受支持**——skill 必须直接躺在上面那六个根目录的下面，别指望它自己去深挖子目录。

目录里给模型看的摘要包含：`name`、`description`，以及可选的 `whenToUse`（额外的路由提示）。

## 渐进式披露：模型只看到"目录"

  <figure class="figure">
    <svg viewBox="0 0 720 188" xmlns="http://www.w3.org/2000/svg">
      <g font-size="12">
        <text x="30" y="22" class="dim">① 会话前缀目录：只有名字与一句话描述常驻上下文（几十 token 级别）</text>
        <rect x="30" y="32" width="150" height="32" rx="8" class="cell"/>
        <text x="105" y="52" text-anchor="middle" font-size="11">pdf-export</text>
        <rect x="200" y="32" width="150" height="32" rx="8" class="cell"/>
        <text x="275" y="52" text-anchor="middle" font-size="11">db-migrate</text>
        <rect x="370" y="32" width="150" height="32" rx="8" class="cell"/>
        <text x="445" y="52" text-anchor="middle" font-size="11">release-notes</text>
        <rect x="540" y="32" width="150" height="32" rx="8" class="cell"/>
        <text x="615" y="52" text-anchor="middle" font-size="11">onboard-guide</text>
        <text x="30" y="92" class="dim">② 命中任务：模型调用 skill 工具，把正文加载进来</text>
        <rect x="180" y="102" width="360" height="46" rx="10" stroke-width="2" class="cell-em link-green"/>
        <text x="360" y="122" text-anchor="middle">SKILL.md 正文</text>
        <text x="360" y="140" text-anchor="middle" font-size="11" class="dim">只在被取用的那一刻进窗口</text>
        <text x="30" y="176" font-size="11" class="dim">没命中的 skill，正文永远不占窗口——这就是"目录常驻、正文按需"的价值。</text>
      </g>
    </svg>
    <figcaption>图 11：渐进式披露——常驻的只有目录，正文按需加载</figcaption>
  </figure>

关键约束在这里：模型会话目录**只使用模型可调用 skill 的 `name` 和 `description`，从不使用正文，也从不使用绝对文件路径**。

想一下如果不这么做会怎样：一个项目里放 20 份 skill，每份正文 2000 字，光目录就把上下文窗口吃掉一大块。所以"目录常驻 + 正文按需"不是优化，是必需——这正是 AI 基础系列第 7 篇讲的**上下文工程**落到具体实现上的样子。

## 调用控制：谁能用这个技能

dsh 把调用权限拆成两个**独立**开关，并保留全部四种组合：

  <table>
    <tr><th>组合</th><th>谁能调用</th><th>典型场景</th></tr>
    <tr><td>两个都为 <code>true</code>（默认）</td><td>模型和人</td><td>常规操作手册</td></tr>
    <tr><td><code>disable-model-invocation</code></td><td>只给人用</td><td>高危操作：模型不许自己触发，必须你显式点名</td></tr>
    <tr><td><code>user-invocable: false</code></td><td>只给模型用</td><td>纯内部路由逻辑，不想出现在人的命令列表里</td></tr>
    <tr><td>两个都为 <code>false</code></td><td>都不行</td><td>只能由受信的代码通过 <code>ctx.skills.get()</code> 取</td></tr>
  </table>

在文件里就是 frontmatter 的两个键：`disable-model-invocation` 和 `user-invocable`，省略都默认为 `true`。

这个设计的价值在于：**同一个技能，改的只是"谁能用它"，而不是改写内容。**安全边界和能力描述因此在结构上分开了——这比"在正文里写一句'请勿自动执行'"可靠得多。

## 另一种约定：AGENTS.md 指令链

Skill 解决的是"某类任务怎么做"。还有一类约定是"始终要守的规则"——代码风格、目录约定、禁止事项。dsh 为它准备了另一条通道：**与 `AGENTS.md` 兼容的工作区指令文件**，由 `dsh-agent-instructions` 插件负责，`dsh-base` 默认启用（预算 65,536 字节）。

加载顺序很有讲究：

  1. **用户全局**：`$DSH_HOME/AGENTS.md`，最宽泛；
2. **项目指令链**：从**项目根目录到会话工作目录**，沿途每个目录里的候选文件，由宽泛到具体。

候选文件名默认两组：基础文件 `AGENTS.md` 与 `CLAUDE.md`，以及叠加的本地文件 `AGENTS.local.md` 与 `CLAUDE.local.md`。项目根以 `.git` 为标记（可配置），找不到标记就不上溯。

几个细节做得很细：

  - **内容一致的同级文件只渲染一次**——把 `CLAUDE.md` 复制成 `AGENTS.md`，不会被重复加载；
  - **预算不够时，先丢弃整个较宽泛的文件，再截断最具体的那一个**，并给出可见通知，指名被省略与被截断的路径。也就是说：**越具体越优先保留**——这条取舍很符合直觉，越靠近当前工作的规则越重要；
  - 内容变化的文件会发 `Updated instructions from: <path>`，消失或变成重复项会发移除通知。

和 Skill 的分工，一句话说清：

  <table>
    <tr><th></th><th>AGENTS.md 指令链</th><th>Skill</th></tr>
    <tr><td>生命周期</td><td>常驻：首轮注入一次，之后增量刷新</td><td>按需：只用时才把正文加载进来</td></tr>
    <tr><td>适合写什么</td><td>始终要守的规则</td><td>特定任务的操作手册</td></tr>
    <tr><td>粒度</td><td>目录级（越深越具体，越具体越优先）</td><td>任务级</td></tr>
    <tr><td>谁触发</td><td>自动</td><td>模型或人显式取用</td></tr>
  </table>

::: warning
有两个安全细节值得记住。一是：注入的指令内容里如果出现字面的 `</system-reminder>`，会被**转义**——防止仓库里的文本反过来关掉插件控制的框架。二是：**符号链接的指令文件会跟随目标读取**，所以克隆一个不可信仓库，可能把仓库外的文件内容当成"低优先级工作区指引"读进来（它不会覆盖系统、开发者或用户直接下达的指令）。加载不可信仓库时，请用文件系统策略或系统沙箱把 `ctx.fs` 限制住。
:::

两个已知限制也别踩：刷新是由**结构化文件操作**驱动的，没有文件监视——而且，**改目录的 `bash` 命令不会触发嵌套指令发现**（每次 shell 调用都是新进程，解析任意 shell 语法不是可靠的文件系统接缝）。另外它不解释小写文件名、`.claude/rules/` 和 `@path` 导入，候选语义刻意保持简单。

## 热更新：目录是活的

本地提供方用文件监视盯住各个根目录：新增或删除 skill、改动直属条目，都会让目录失效并重建。模型的 `write` / `edit` 命中 skill 相关路径时，也会同步失效——写一份新技能不用重启。

（一个边界：bundle 下的**资源文件**变更不算目录变更，因为技能集本身没变。）

::: tip
两种约定各管一段：**`AGENTS.md` 指令链管"始终要守的规则"**（常驻、目录级、越具体越优先），**Skill 管"某类任务怎么做"**（按需、任务级、只在用时进窗口）。共同点是它们都只是**仓库里的一份文件**——和代码一起提交、一起评审、一起回滚。能写进文件的事，就别每次在对话里重讲一遍。
:::

经验能沉淀了。但这些能力到底跑在什么形态里？下一篇：**多形态运行——Web、headless、SDK 与网关**。
