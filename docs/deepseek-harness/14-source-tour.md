---
title: 源码导读：这个仓库长什么样
---

# 源码导读：这个仓库长什么样

> 约 10 分钟 · 关键词：packages 分组、能力三件套、vendor、文档图

## 先看骨架：仓库分六层

  <table>
    <tr><th>目录</th><th>放什么</th></tr>
    <tr><td><code>apps/</code></td><td>可执行应用，比如 CLI</td></tr>
    <tr><td><code>packages/</code></td><td>真正的代码：几十个包，按 <code>packages/&lt;组&gt;/&lt;包&gt;</code> 分层</td></tr>
    <tr><td><code>python/</code></td><td>Python SDK 与示例</td></tr>
    <tr><td><code>vendor/</code></td><td>以源码形式随仓分发的底层框架</td></tr>
    <tr><td><code>docs/</code></td><td>文档站源文件（含一批**从源码生成的图**）</td></tr>
    <tr><td><code>scripts/</code></td><td>生成与校验脚本（文档图、目录、连改名都是脚本驱动的）</td></tr>
  </table>

重点全在 `packages/`。它按**职能**分成 50 个组，看上去吓人，其实有规律可循。

## packages 的分组规律

  <table>
    <tr><th>类别</th><th>典型组</th><th>管什么</th></tr>
    <tr><td><strong>地基</strong></td><td><code>util</code>、<code>core</code>、<code>typert</code>、<code>scope</code></td><td>工具函数、agent 循环、跨进程协议、作用域</td></tr>
    <tr><td><strong>模型</strong></td><td><code>llm</code></td><td>对话与分片类型、适配器契约、各提供方实现</td></tr>
    <tr><td><strong>会话</strong></td><td><code>session</code></td><td>日志格式与**版本迁移**、持久化、投影、遥测</td></tr>
    <tr><td><strong>能力族</strong></td><td><code>fs</code>、<code>shell</code>、<code>web</code>、<code>skill</code>、<code>sandbox</code>、<code>subagent</code>、<code>jobs</code>、<code>workflow</code>、<code>spill</code></td><td>每一种"能动手的地方"</td></tr>
    <tr><td><strong>交互与治理</strong></td><td><code>interaction</code>、<code>credentials</code>、<code>settings</code>、<code>guard</code></td><td>审批、权限预设、凭据、设置、护栏</td></tr>
    <tr><td><strong>上下文</strong></td><td><code>context</code></td><td>指令文件、文件引用、会话引用、时间与环境</td></tr>
    <tr><td><strong>组合与交付</strong></td><td><code>bundle</code>、<code>boot</code>、<code>preset</code></td><td>各 profile 的组合包、启动、预设</td></tr>
    <tr><td><strong>界面</strong></td><td><code>client</code></td><td>浏览器侧：连接、资源、UI slot、各功能面板</td></tr>
    <tr><td><strong>前端未稳</strong></td><td><code>experimental</code></td><td>Agent Teams 一类还在演化的东西</td></tr>
  </table>

有一条特别值得注意：**会话组里有多个 `session-format-v0-to-v1`、`v1-to-v2`、`v2-to-v3` 这样的包**。这说明会话日志格式是**带版本、带迁移链**的——第 6 篇说"Session Log 是唯一事实源"，这里就是这句话的工程代价：既然一切都能回放，格式演进就必须能迁移旧日志。

## 最值得学的一刀：能力三件套

  <figure class="figure">
    <svg viewBox="0 0 720 190" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a14" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <rect x="30" y="30" width="180" height="66" rx="10" stroke-width="2" class="cell-em link"/>
        <text x="120" y="52" text-anchor="middle" font-weight="bold">dsh-fs</text>
        <text x="120" y="72" text-anchor="middle" font-size="11" class="dim">Service Definition</text>
        <text x="120" y="88" text-anchor="middle" font-size="11" class="dim">只定义接口与类型</text>
        <rect x="270" y="30" width="180" height="66" rx="10" class="cell link-purple"/>
        <text x="360" y="52" text-anchor="middle" font-weight="bold">dsh-fs-local</text>
        <text x="360" y="72" text-anchor="middle" font-size="11" class="dim">Service Provider</text>
        <text x="360" y="88" text-anchor="middle" font-size="11" class="dim">本地文件系统实现</text>
        <rect x="510" y="30" width="180" height="66" rx="10" class="cell link-green"/>
        <text x="600" y="52" text-anchor="middle" font-weight="bold">dsh-tool-fs</text>
        <text x="600" y="72" text-anchor="middle" font-size="11" class="dim">Consumer</text>
        <text x="600" y="88" text-anchor="middle" font-size="11" class="dim">面向模型的工具</text>
        <g stroke-width="1.8" marker-end="url(#a14)" class="link">
          <line x1="214" y1="63" x2="266" y2="63"/>
          <line x1="454" y1="63" x2="506" y2="63"/>
        </g>
        <rect x="30" y="122" width="660" height="50" rx="10" class="cell link-orange"/>
        <text x="360" y="144" text-anchor="middle">同一个形状反复出现：shell · web · sandbox · skill · subagent · spill · workflow …</text>
        <text x="360" y="163" text-anchor="middle" font-size="11" class="dim">看懂一个组，就看懂了一大半</text>
      </g>
    </svg>
    <figcaption>图 14：能力三件套——定义接缝的包、实现接缝的包、消费接缝的包</figcaption>
  </figure>

以 `fs` 组为例，它由三个包组成：`dsh-fs`（定义接缝）、`dsh-fs-local`（本地实现）、`dsh-tool-fs`（面向模型的工具）。这正是第 4 篇讲的**能力接缝**落到目录结构上的样子。

而这个形状在仓库里**反复出现**：`shell` 组是 `shell` + `bash-local` / `pwsh-local` + `tool-bash`；`web` 组是 `web` + `web-fetch-http` / `web-search-*` + `tool-web`；`sandbox`、`skill`、`subagent`、`jobs` 都是同样的切法。

**结论很实用：想快速看懂这个仓库，找任何一个能力组，把三件套读一遍就够了。**剩下的组都是同一套模板换了个领域。

## vendor 目录：Cordis 是从哪来的

`packages/` 里到处 `import` 的那个 `Context`，来自 `vendor/`。

Cordis 框架及其基础插件（loader、include、group、timer、hmr、logger-console）以**源码形式随仓分发**，并以 `@deepseek-ai` 作用域发布——也就是 `cordis` 变成了 `@deepseek-ai/cordis`，`schemastery` 变成了 `@deepseek-ai/schemastery`。

原因在文档里写得很直白：每个 harness 包都把框架声明为 peer dependency，**发布 harness 就会连带发布这一层；用上游的名字发布，等于在 registry 上占用别人的名字。**

有几样东西**刻意不改名**，值得注意：

  - `cordis.yml` 这套配置文件名（含 `*.cordis.yml`、`cordis.patch.yml`）；
  - loader 的 `cordis:` 内建协议前缀（`cordis:include`、`cordis:group`）；
  - 名字里带这个词的 harness 包，比如 `dsh-tool-cordis`。

还有一点工程味道很足：**改名不靠手改**，而是由脚本承载一份映射表，能 `--apply` 执行、能 `:check` 断言、也能 `--reverse` 回退。文档里同步说明"哪些地方要跟着改"——因为上游是持续同步的，手工改名一定会漏。

## 文档本身也是产物

`docs/` 里有一组专门的"图"文档，用来表达生成的目录覆盖不到的关系：

  <table>
    <tr><th>图</th><th>维护方式</th><th>看什么</th></tr>
    <tr><td>模块依赖图</td><td>生成</td><td>包之间的 peer 依赖关系</td></tr>
    <tr><td>能力 seam 与核心服务</td><td>混合</td><td>接缝与服务的映射</td></tr>
    <tr><td>事件生产方／消费方矩阵</td><td>混合</td><td>谁发事件、谁听事件</td></tr>
    <tr><td>工具 schema 目录与包映射</td><td>生成</td><td>模型能用哪些工具</td></tr>
    <tr><td>agent 轮次与步骤生命周期</td><td>人工维护</td><td>一个 Turn 怎么走</td></tr>
    <tr><td>工具执行流水线</td><td>人工维护</td><td>一次工具调用经过哪些环节</td></tr>
  </table>

再加上每个子系统一页、页面里带一段**从源码生成的 Cordis API 小节**（有校验命令保证它不落后于源码）。这套做法的价值在长期：**文档不是"另外写的"，而是"生成 + 人工维护关键判断"的混合体**——人只负责写"为什么"，"是什么"交给源码生成。

## 一条务实的阅读路线

  1. `README.md` → `docs/architecture.md`：先搞清跨子系统的行为（服务映射、生命周期、事件分类）；
2. `docs/subsystems/README.md` 的子系统总表：挑你关心的那一页深入；
3. 要动手写插件：`docs/user/develop/basic/` → `docs/user/develop/framework/` → `docs/cordis-tutorial/`；
4. 找包的位置：看模块依赖图，别在文件树里瞎翻；
5. 要核实 API：读子系统页里生成的 `cordis-surface` 小节，以源码为准；
6. 准备提改动：先读仓库根目录的 `AGENTS.md` 与 `docs/development.md`。

::: tip
读开源 Harness 的顺序建议是：**先读"为什么这么分"，再读"怎么实现"。**这个仓库最值得偷的不是某段代码，而是它的三条纪律——**接缝**（能力可替换）、**清单**（配置即组合）、**映射表加脚本**（改名、生成、校验都不靠人肉同步）。
:::

::: tip
系列二到这里结束，14 篇的路径是：**01–06 理解架构**（Harness 是什么 → 一切皆插件 → 启动分层 → 能力接缝 → 事件与 Turn → Session Log）→ **07–12 动手**（跑起来 → 写插件 → 权限与审批 → 接入模型 → Skill 与约定 → 多形态运行）→ **13–14 定位**（横向对比 → 源码导读）。建议的读法是先通读 01–06 建立整体图景，之后按需跳到具体章节。
:::
