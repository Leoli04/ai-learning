# ai-learning

AI 学习笔记站点，两个系列：

## 系列一：AI 基础——发展与技术全景（`ai-basics/`，13 篇）

讲述 AI 这几年的发展脉络、模型怎么炼成、中间出现的技术（Prompt、RAG、向量数据库、Agent 范式、Skill/MCP、LoRA 微调、推理优化、多模态与推理模型、工作流编排等）各自解决的问题，以及主流 Agent 产品技术盘点与当前未解难题。

| # | 文章 | 文件 |
|---|------|------|
| 01 | 大模型这几年：时间线与范式转移 | `ai-basics/01-llm-era.html` |
| 02 | Transformer 与训练三部曲 | `ai-basics/02-transformer-training.html` |
| 03 | Prompt 工程与上下文学习 | `ai-basics/03-prompt.html` |
| 04 | RAG：外挂知识库 | `ai-basics/04-rag.html` |
| 05 | 向量数据库与检索栈 | `ai-basics/05-vector-db.html` |
| 06 | Agent 核心范式（ReAct / 规划 / 反思 / 多智能体） | `ai-basics/06-agent-paradigms.html` |
| 07 | 记忆与上下文工程 | `ai-basics/07-memory-context.html` |
| 08 | Skill 与 MCP | `ai-basics/08-skill-mcp.html` |
| 09 | 微调与对齐（SFT / LoRA / RLHF / DPO） | `ai-basics/09-finetuning.html` |
| 10 | 推理优化与部署（KV Cache / 量化 / vLLM） | `ai-basics/10-inference-optimization.html` |
| 11 | 多模态与推理模型（o1 / R1） | `ai-basics/11-multimodal-reasoning.html` |
| 12 | 工作流编排与主流 Agent 技术全景 | `ai-basics/12-orchestration-agents.html` |
| 13 | 当前还没解决的六个问题 | `ai-basics/13-open-problems.html` |

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