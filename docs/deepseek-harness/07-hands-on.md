---
title: 动手实践：10 分钟跑起你的第一个 dsh
---

# 动手实践：10 分钟跑起你的第一个 dsh

> 约 5 分钟 · 关键词：npx、Web UI、API Key、工作区、--dump-config

## 方式一：npm 一把梭（推荐新手）

前提：装好 <a href="https://nodejs.org" target="_blank">Node.js</a>。然后一行命令：

```bash
npx @deepseek-ai/dsh web
```

默认会在 `http://127.0.0.1:3080` 启动 Web UI，并自动打开浏览器。加 `--no-open` 可以只启动服务不开浏览器（比如在 SSH 远程服务器上跑）。

## 方式二：从源码跑（想读代码的话）

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```
::: warning
运行前建议先读一遍仓库里的 SAFETY 说明——它毕竟是一个能读写文件、执行命令的 Agent 框架。
:::

## 启动后的三步走

  1. **配模型**：设置 → 模型，填入 <a href="https://platform.deepseek.com/" target="_blank">DeepSeek API 密钥</a>并保存，模型路由立即生效，**不用重启**。想接 OpenAI 兼容端点也支持（见官方 providers 指南）。
2. **选工作区**：点击"选择工作区"，添加 `dsh` 启动时所在的目录。注意：不选工作区，输入框是灰的。
3. **发任务**：开一个会话，比如让它 *"Summarize this repository and identify its main packages."* 涉及敏感操作时会先弹审批，你点头它才动手。

  <figure class="figure">
    <svg viewBox="0 0 720 160" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="13">
        <rect x="20" y="50" width="150" height="56" rx="10" class="cell link"/>
        <text x="95" y="73" text-anchor="middle">npx dsh web</text>
        <text x="95" y="93" text-anchor="middle" font-size="11" class="dim">:3080</text>
        <rect x="200" y="50" width="150" height="56" rx="10" class="cell"/>
        <text x="275" y="73" text-anchor="middle">填 API Key</text>
        <text x="275" y="93" text-anchor="middle" font-size="11" class="dim">即时生效</text>
        <rect x="380" y="50" width="150" height="56" rx="10" class="cell"/>
        <text x="455" y="73" text-anchor="middle">选工作区</text>
        <text x="455" y="93" text-anchor="middle" font-size="11" class="dim">解锁输入框</text>
        <rect x="560" y="50" width="140" height="56" rx="10" class="cell-em link-green"/>
        <text x="630" y="73" text-anchor="middle">发任务 ✅</text>
        <text x="630" y="93" text-anchor="middle" font-size="11" class="dim">审批后执行</text>
        <g stroke-width="1.8" marker-end="url(#a)" class="link">
          <line x1="170" y1="78" x2="198" y2="78"/>
          <line x1="350" y1="78" x2="378" y2="78"/>
          <line x1="530" y1="78" x2="558" y2="78"/>
        </g>
      </g>
    </svg>
    <figcaption>图 7：上手四步——启动 → 配模型 → 选工作区 → 发任务</figcaption>
  </figure>

## 三个值得马上试的命令

```bash
# 看 web Profile 实际加载的完整插件树（调试 patch 神器）
dsh --profile web --dump-config

# 无界面跑一次性任务
dsh --profile headless

# 插件管理
dsh plugin --help
```

## 下一步去哪？

  - 官方文档站：<a href="https://deepseek-harness.github.io/deepseek-harness/" target="_blank">deepseek-harness.github.io/deepseek-harness</a>
- 架构文档（本系列 3~6 篇的原始出处）：`docs/architecture.zh.md`
- 插件开发指南：`docs/user/develop/basic/`
- 给插件仓库打上 `dsh-plugin` 话题，可以被社区发现

::: tip
第一部分（架构）读完了：01 Harness 是什么 → 02 一切皆插件 → 03 Profile/Bundle/Patch 分层 → 04 Capability Seam → 05 事件三域与 Turn 流 → 06 Session Log 唯一事实源 → 07 动手实践。现在去看 `--dump-config` 的输出，你会发现每一层都眼熟了。接下来进入第二部分（动手扩展）：**08 写一个真实插件** → 09 权限与审批 → 10 接入模型 → 11 Skill 与约定；再到第三部分：12 多形态运行 → 13 横向对比 → 14 源码导读。
:::
