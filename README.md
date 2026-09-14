# ai-learning

AI 学习笔记站点，基于 **VitePress**（Vue 官方文档同款）构建，两个系列共 34 篇图解文章。

## 系列一：AI 基础——发展与技术全景（`docs/ai-basics/`，20 篇）

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
| 14 | 生成式视觉：扩散模型怎么"画"出一张图 | `docs/ai-basics/14-generative-vision.md` |
| 15 | 评测与可观测性：怎么证明 AI 真的变好了 | `docs/ai-basics/15-eval-observability.md` |
| 16 | 进阶 RAG：从"查得到"到"查得准" | `docs/ai-basics/16-advanced-rag.md` |
| 17 | 语音栈：让 AI 能听会说 | `docs/ai-basics/17-speech-stack.md` |
| 18 | Agent 安全：提示注入与权限边界 | `docs/ai-basics/18-agent-security.md` |
| 19 | 多智能体：什么时候值得，什么时候是负担 | `docs/ai-basics/19-multi-agent.md` |
| 20 | 本地化部署与开源模型：把模型搬回自己机房 | `docs/ai-basics/20-local-models.md` |

## 系列二：DeepSeek Harness 通俗图解（`docs/deepseek-harness/`，14 篇）

基于 [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) 官方 README、架构文档、子系统文档与插件开发指南整理。

| # | 文章 | 文件 |
|---|------|------|
| 01 | 什么是 Agent Harness？ | `docs/deepseek-harness/01-what-is-agent-harness.md` |
| 02 | 一切皆插件：没有特权核心 | `docs/deepseek-harness/02-everything-is-a-plugin.md` |
| 03 | 启动分层：Profile / Bundle / Patch | `docs/deepseek-harness/03-profile-bundle-patch.md` |
| 04 | 能力接缝（Capability Seam） | `docs/deepseek-harness/04-capability-seam.md` |
| 05 | 事件三域与 Turn 执行流 | `docs/deepseek-harness/05-events-and-turn-flow.md` |
| 06 | Session Log：唯一事实源 | `docs/deepseek-harness/06-session-log.md` |
| 07 | 动手实践：10 分钟跑起来 | `docs/deepseek-harness/07-hands-on.md` |
| 08 | 写一个真实插件：从最小插件到能用的工具 | `docs/deepseek-harness/08-first-plugin.md` |
| 09 | 权限与审批：谁允许它动手 | `docs/deepseek-harness/09-permissions-approval.md` |
| 10 | 接入你自己的模型：Provider、协议与请求形状 | `docs/deepseek-harness/10-model-providers.md` |
| 11 | Skill：把"这件事该怎么做"写进仓库 | `docs/deepseek-harness/11-skills-and-conventions.md` |
| 12 | 多形态运行：Web、headless、SDK 与网关 | `docs/deepseek-harness/12-run-modes.md` |
| 13 | 横向对比：dsh 和其他 Agent Harness 的取舍 | `docs/deepseek-harness/13-comparison.md` |
| 14 | 源码导读：这个仓库长什么样 | `docs/deepseek-harness/14-source-tour.md` |

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
- 写完后跑 `python scripts/health-check.py` 自检（frontmatter、meta 行、代码围栏与容器配对、figure 配对、SVG 闭合、禁止硬编码 SVG 颜色等 10 项）。

### 候选选题（尚未开写）

| 方向 | 定位 |
|------|------|
| AI 工程实战 | 评测集搭建、CI 里跑回归、成本与延迟看板、灰度与回滚 |
| Agentic Coding 实践 | 规格驱动开发、上下文管理、人机分工的代码评审 |
| 企业知识库实战 | PDF/表格解析、分块与元数据、权限与多租户、调优闭环 |
| 论文精读（图解版） | Attention Is All You Need、LoRA、ReAct、DPO、MCP 规范等 |
| 站点番外 | 术语表中英对照、按角色的学习路线图、一页速查卡 |

系列二可继续下钻的方向：subagent 与 agent-team 的多智能体实现、compaction / spill 的上下文压缩机制、tool-execution-pipeline 的分段与记忆化、hooks 协议与第三方 Agent 互操作。
