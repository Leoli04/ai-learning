# ai-learning

AI 学习笔记站点，第一辑：**DeepSeek Harness（dsh）通俗图解系列**，共 7 篇，基于 [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) 官方 README 与架构文档整理，配自绘 SVG 图解。

## 目录

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
