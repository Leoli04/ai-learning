# ai-learning

AI 学习笔记站点，两个系列：

## 系列一：AI 基础——发展与技术全景（`ai-basics/`，7 篇）

讲述 AI 这几年的发展脉络、中间出现的技术（Prompt、RAG、Agent/工具调用、Skill、n8n 编排等）各自解决的问题，以及当前仍未解决的难题。

| # | 文章 | 文件 |
|---|------|------|
| 01 | 大模型这几年：时间线与范式转移 | `ai-basics/01-llm-era.html` |
| 02 | Prompt 工程与上下文学习 | `ai-basics/02-prompt.html` |
| 03 | RAG：外挂知识库 | `ai-basics/03-rag.html` |
| 04 | Agent 与工具调用（ReAct / MCP） | `ai-basics/04-agent-tools.html` |
| 05 | Skill、记忆与上下文工程 | `ai-basics/05-skill-memory.html` |
| 06 | n8n 与工作流编排 | `ai-basics/06-n8n-workflow.html` |
| 07 | 当前还没解决的六个问题 | `ai-basics/07-open-problems.html` |

## 系列二：DeepSeek Harness 通俗图解（`deepseek-harness/`，7 篇）

基于 [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) 官方 README 与架构文档整理。

| # | 文章 | 文件 |
|---|------|------|
| 01 | 什么是 Agent Harness？ | `deepseek-harness/01-what-is-agent-harness.html` |
| 02 | 一切皆插件：没有特权核心 | `deepseek-harness/02-everything-is-a-plugin.html` |
| 03 | 启动分层：Profile / Bundle / Patch | `deepseek-harness/03-profile-bundle-patch.html` |
| 04 | 能力接缝（Capability Seam） | `deepseek-harness/04-capability-seam.html` |
| 05 | 事件三域与 Turn 执行流 | `deepseek-harness/05-events-and-turn-flow.html` |
| 06 | Session Log：唯一事实源 | `deepseek-harness/06-session-log.html` |
| 07 | 动手实践：10 分钟跑起来 | `deepseek-harness/07-hands-on.html` |

## 本地预览

纯静态站点，零构建、零依赖，双击 `index.html` 即可，或：

```sh
python -m http.server 8080
# 打开 http://localhost:8080
```

## GitHub Actions 部署

工作流：`.github/workflows/deploy-pages.yml`，推送到 `main` 分支自动部署到 GitHub Pages。

首次使用需开启一次 Pages：

1. 仓库 **Settings → Pages**
2. **Build and deployment → Source** 选择 **GitHub Actions**
3. 之后每次 push 到 `main` 自动部署（也可在 Actions 页手动 Run workflow）

## 后续扩展

- 每学一个新主题，在根目录新建子目录（如 `xxx/`），并把首页 `index.html` 加一个入口卡片。