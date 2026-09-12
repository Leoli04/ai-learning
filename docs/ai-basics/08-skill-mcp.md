---
title: Skill 与 MCP：经验怎么沉淀，工具怎么标准化
---

# Skill 与 MCP：经验怎么沉淀，工具怎么标准化

> 约 7 分钟 · 关键词：Agent Skills、SKILL.md、MCP、渐进式披露

## Skill：写给模型看的"操作手册"

Agent 会调工具后，新问题是：**流程性经验每次都要现场重教**。比如"发一篇公众号文章"涉及排版规范、图片上传、接口细节——写进每次对话又贵又容易漏。

**Skill（技能）**的解法是把方法论打包成文件夹，核心是一个 `SKILL.md`：

```text
my-skill/
├── SKILL.md          # 入口：名称、描述、何时触发、操作步骤
├── references/       # 详细文档：API 说明、规范细则
└── scripts/          # 可选：配套可执行脚本
```

它不是代码插件，而是**按需加载的说明书**。关键设计是**渐进式披露（Progressive Disclosure）**：平时只有名称和一句话描述占着上下文（几十 token），任务匹配时才读正文，需要细节再翻 references——三层按需加载，几乎不浪费窗口。这套规范由 Anthropic 在 2025 年提出，开源社区（包括各 Harness 框架）迅速跟进，团队可以把技能库放进 git 共享。

## MCP：工具世界的 USB-C

Function Calling 是各家 API 的私有格式，M 工具接到 A 框架要写一份适配，接到 B 框架再写一份。2024 年底 Anthropic 发布 **MCP（Model Context Protocol）**，把"模型 ↔ 工具/数据源"的接口标准化：

  <figure class="figure">
    <svg viewBox="0 0 720 300" xmlns="http://www.w3.org/2000/svg">
      <g font-size="12">
        <rect x="30" y="100" width="180" height="100" rx="12" stroke-width="2" class="cell-em link"/>
        <text x="120" y="130" text-anchor="middle" font-weight="bold" font-size="14">MCP Host</text>
        <text x="120" y="152" text-anchor="middle" class="dim">Agent 应用本体</text>
        <text x="120" y="170" text-anchor="middle" class="dim">（Claude / Cursor / dsh…）</text>
        <text x="120" y="188" text-anchor="middle" class="dim">内置 MCP Client</text>
        <rect x="290" y="100" width="140" height="100" rx="12" stroke-width="2" class="cell link-orange"/>
        <text x="360" y="130" text-anchor="middle" font-weight="bold" font-size="14">MCP 协议</text>
        <text x="360" y="152" text-anchor="middle" class="dim">标准消息格式</text>
        <text x="360" y="170" text-anchor="middle" class="dim">stdio / HTTP 传输</text>
        <rect x="510" y="30" width="180" height="52" rx="10" class="cell link-green"/>
        <text x="600" y="52" text-anchor="middle">Server：GitHub</text>
        <text x="600" y="70" text-anchor="middle" font-size="11" class="dim">读仓库 / 提 PR</text>
        <rect x="510" y="124" width="180" height="52" rx="10" class="cell link-green"/>
        <text x="600" y="146" text-anchor="middle">Server：数据库</text>
        <text x="600" y="164" text-anchor="middle" font-size="11" class="dim">查 SQL / 建表</text>
        <rect x="510" y="218" width="180" height="52" rx="10" class="cell link-green"/>
        <text x="600" y="240" text-anchor="middle">Server：浏览器</text>
        <text x="600" y="258" text-anchor="middle" font-size="11" class="dim">截图 / 操作页面</text>
        <g stroke-width="1.8" class="link-orange">
          <line x1="210" y1="140" x2="288" y2="140"/>
          <path d="M 430 140 C 470 140 470 56 508 56"/>
          <line x1="430" y1="150" x2="508" y2="150"/>
          <path d="M 430 160 C 470 160 470 244 508 244"/>
        </g>
        <text x="360" y="290" text-anchor="middle" class="dim">工具方实现一次 MCP Server，所有支持 MCP 的 Agent 即插即用</text>
      </g>
    </svg>
    <figcaption>图 8：MCP 架构——Host（Agent）经协议连接任意数量的 Server（工具方）</figcaption>
  </figure>

Server 可以暴露三类东西：**Tools**（可执行的操作）、**Resources**（可读取的数据）、**Prompts**（预置提示模板）。2025 年起 OpenAI、Google 等相继宣布支持，MCP 成为事实标准——这解决的是**生态复用**问题：写一个 MCP Server，全行业的 Agent 都能用。

## Skill vs MCP vs Function Calling：一张表分清

  <table>
    <tr><th></th><th>Function Calling</th><th>MCP</th><th>Skill</th></tr>
    <tr><td>本质</td><td>API 能力：模型输出调用意图</td><td>传输标准：工具的通用接口</td><td>知识资产：打包的方法论文档</td></tr>
    <tr><td>解决</td><td>模型怎么"点菜"</td><td>工具怎么跨框架复用</td><td>经验怎么沉淀复用</td></tr>
    <tr><td>形态</td><td>请求里的 JSON schema</td><td>独立进程 / 服务</td><td>Markdown 文件夹</td></tr>
  </table>

::: tip
**Function Calling 是动作，MCP 是插座标准，Skill 是操作手册。**三者叠加 = 模型能点菜（FC）、菜谱全行业通用（MCP）、老师傅的手艺可以装订成册随取随用（Skill）。
:::

工具与经验都齐了，还差一块拼图：不改模型的前提下，怎么让它更"对味"？下一篇：**微调与对齐**。
