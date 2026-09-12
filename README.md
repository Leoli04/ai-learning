# ai-learning

AI 学习笔记站点，基于 **VitePress**（Vue 官方文档同款）构建，两个系列共 20 篇图解文章。

## 系列一：AI 基础——发展与技术全景（`docs/ai-basics/`，13 篇）

讲述 AI 这几年的发展脉络、模型怎么炼成、中间出现的技术（Prompt、RAG、向量数据库、Agent 范式、Skill/MCP、LoRA 微调、推理优化、多模态与推理模型、工作流编排等）各自解决的问题，以及主流 Agent 产品技术盘点与当前未解难题。

| # | 文章 | 文件 |
|---|------|------|
| 01 | 大模型这几年：时间线与范式转移 | `docs/ai-basics/01-llm-era.md` |
| 02 | Transformer 与训练三部曲 | `docs/ai-basics/02-transformer-training.md` |
| 03 | Prompt 工程与上下文学习 | `docs/ai-basics/03-prompt.md` |
| 04 | RAG：外挂知识库 | `docs/ai-basics/04-rag.md` |
| 05 | 向量数据库与检索栈 | `docs/ai-basics/05-vector-db.md` |
| 06 | Agent 核心范式（ReAct / 规划 / 反思 / 多智能体） | `docs/ai-basics/06-agent-paradigms.md` |
| 07 | 记忆与上下文工程 | `docs/ai-basics/07-memory-context.md` |
| 08 | Skill 与 MCP | `docs/ai-basics/08-skill-mcp.md` |
| 09 | 微调与对齐（SFT / LoRA / RLHF / DPO） | `docs/ai-basics/09-finetuning.md` |
| 10 | 推理优化与部署（KV Cache / 量化 / vLLM） | `docs/ai-basics/10-inference-optimization.md` |
| 11 | 多模态与推理模型（o1 / R1） | `docs/ai-basics/11-multimodal-reasoning.md` |
| 12 | 工作流编排与主流 Agent 技术全景 | `docs/ai-basics/12-orchestration-agents.md` |
| 13 | 当前还没解决的六个问题 | `docs/ai-basics/13-open-problems.md` |

## 系列二：DeepSeek Harness 通俗图解（`docs/deepseek-harness/`，7 篇）

基于 [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) 官方 README 与架构文档整理。

| # | 文章 | 文件 |
|---|------|------|
| 01 | 什么是 Agent Harness？ | `docs/deepseek-harness/01-what-is-agent-harness.md` |
| 02 | 一切皆插件：没有特权核心 | `docs/deepseek-harness/02-everything-is-a-plugin.md` |
| 03 | 启动分层：Profile / Bundle / Patch | `docs/deepseek-harness/03-profile-bundle-patch.md` |
| 04 | 能力接缝（Capability Seam） | `docs/deepseek-harness/04-capability-seam.md` |
| 05 | 事件三域与 Turn 执行流 | `docs/deepseek-harness/05-events-and-turn-flow.md` |
| 06 | Session Log：唯一事实源 | `docs/deepseek-harness/06-session-log.md` |
| 07 | 动手实践：10 分钟跑起来 | `docs/deepseek-harness/07-hands-on.md` |

## 本地开发

需要 Node.js ≥ 18：

```sh
npm install        # 首次安装依赖
npm run dev        # 本地开发，http://localhost:5173
npm run build      # 构建产物到 docs/.vitepress/dist
npm run preview    # 本地预览构建产物
```

新文章写法：在 `docs/ai-basics/`（或 `docs/deepseek-harness/`）新建 `.md` 文件，然后在 `docs/.vitepress/config.mjs` 的 sidebar 里加一行即可。

## GitHub Actions 部署

工作流：`.github/workflows/deploy-pages.yml`（Node 22 + `npm ci` + `vitepress build`），推送到 `main` 分支自动部署到 GitHub Pages：https://leoli04.github.io/ai-learning/

首次使用需开启一次 Pages：

1. 仓库 **Settings → Pages**
2. **Build and deployment → Source** 选择 **GitHub Actions**
3. 之后每次 push 到 `main` 自动部署（也可在 Actions 页手动 Run workflow）

## 后续扩展

- 每学一个新主题，在 `docs/` 下新建子目录写 Markdown，并在 `config.mjs` 注册 nav/sidebar 入口。
