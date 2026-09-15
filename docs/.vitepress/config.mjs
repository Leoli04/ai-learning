import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: 'AI 学习笔记',
  description: 'AI 基础与 Agent 技术通俗图解系列：从 Transformer 到 Agent 时代',
  base: '/ai-learning/',
  ignoreDeadLinks: true,
  themeConfig: {
    siteTitle: 'AI 学习笔记',
    darkModeSwitchLabel: '外观',
    sidebarMenuLabel: '目录',
    returnToTopLabel: '回到顶部',
    outline: { level: [2, 3], label: '本页目录' },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Leoli04/ai-learning' }
    ],
    nav: [
      { text: 'AI 基础', link: '/ai-basics/01-llm-era' },
      { text: '企业知识库', link: '/kb-practice/01-why-hard' },
      { text: 'DeepSeek Harness', link: '/deepseek-harness/01-what-is-agent-harness' },
      { text: 'AI 资源地图', link: '/ai-sites/' }
    ],
    sidebar: {
      '/ai-basics/': [
        {
          text: '模块一 · 模型层',
          collapsed: false,
          items: [
            { text: '01 · 大模型这几年', link: '/ai-basics/01-llm-era' },
            { text: '02 · Transformer 与训练三部曲', link: '/ai-basics/02-transformer-training' },
            { text: '03 · Prompt 工程与上下文学习', link: '/ai-basics/03-prompt' }
          ]
        },
        {
          text: '模块二 · 知识与检索',
          collapsed: false,
          items: [
            { text: '04 · RAG：外挂一个大脑', link: '/ai-basics/04-rag' },
            { text: '05 · 向量数据库与检索栈', link: '/ai-basics/05-vector-db' }
          ]
        },
        {
          text: '模块三 · Agent 技术',
          collapsed: false,
          items: [
            { text: '06 · Agent 核心范式', link: '/ai-basics/06-agent-paradigms' },
            { text: '07 · 记忆与上下文工程', link: '/ai-basics/07-memory-context' },
            { text: '08 · Skill 与 MCP', link: '/ai-basics/08-skill-mcp' }
          ]
        },
        {
          text: '模块四 · 模型工程',
          collapsed: false,
          items: [
            { text: '09 · 微调与对齐', link: '/ai-basics/09-finetuning' },
            { text: '10 · 推理优化与部署', link: '/ai-basics/10-inference-optimization' },
            { text: '11 · 多模态与推理模型', link: '/ai-basics/11-multimodal-reasoning' }
          ]
        },
        {
          text: '模块五 · 系统与全局',
          collapsed: false,
          items: [
            { text: '12 · 编排与主流 Agent 全景', link: '/ai-basics/12-orchestration-agents' },
            { text: '13 · 当前还没解决的问题', link: '/ai-basics/13-open-problems' }
          ]
        },
        {
          text: '模块六 · 生成与评测',
          collapsed: false,
          items: [
            { text: '14 · 生成式视觉：扩散模型', link: '/ai-basics/14-generative-vision' },
            { text: '15 · 评测与可观测性', link: '/ai-basics/15-eval-observability' }
          ]
        },
        {
          text: '模块七 · 检索进阶与语音',
          collapsed: false,
          items: [
            { text: '16 · 进阶 RAG', link: '/ai-basics/16-advanced-rag' },
            { text: '17 · 语音栈：能听会说', link: '/ai-basics/17-speech-stack' }
          ]
        },
        {
          text: '模块八 · 安全与协作',
          collapsed: false,
          items: [
            { text: '18 · Agent 安全与权限边界', link: '/ai-basics/18-agent-security' },
            { text: '19 · 多智能体协作', link: '/ai-basics/19-multi-agent' }
          ]
        },
        {
          text: '模块九 · 落地与部署',
          collapsed: false,
          items: [
            { text: '20 · 本地化部署与开源模型', link: '/ai-basics/20-local-models' }
          ]
        }
      ],
      '/deepseek-harness/': [
        {
          text: '第一部分 · 架构拆解',
          collapsed: false,
          items: [
            { text: '01 · 什么是 Agent Harness', link: '/deepseek-harness/01-what-is-agent-harness' },
            { text: '02 · 一切皆插件', link: '/deepseek-harness/02-everything-is-a-plugin' },
            { text: '03 · 启动分层：Profile/Bundle/Patch', link: '/deepseek-harness/03-profile-bundle-patch' },
            { text: '04 · 能力接缝（Capability Seam）', link: '/deepseek-harness/04-capability-seam' },
            { text: '05 · 事件三域与 Turn 执行流', link: '/deepseek-harness/05-events-and-turn-flow' },
            { text: '06 · Session Log：唯一事实源', link: '/deepseek-harness/06-session-log' }
          ]
        },
        {
          text: '第二部分 · 动手扩展',
          collapsed: false,
          items: [
            { text: '07 · 动手实践：10 分钟跑起来', link: '/deepseek-harness/07-hands-on' },
            { text: '08 · 写一个真实插件', link: '/deepseek-harness/08-first-plugin' },
            { text: '09 · 权限与审批', link: '/deepseek-harness/09-permissions-approval' },
            { text: '10 · 接入你自己的模型', link: '/deepseek-harness/10-model-providers' },
            { text: '11 · Skill 与项目约定', link: '/deepseek-harness/11-skills-and-conventions' }
          ]
        },
        {
          text: '第三部分 · 形态与全景',
          collapsed: false,
          items: [
            { text: '12 · 多形态运行', link: '/deepseek-harness/12-run-modes' },
            { text: '13 · 横向对比其他 Harness', link: '/deepseek-harness/13-comparison' },
            { text: '14 · 源码导读', link: '/deepseek-harness/14-source-tour' }
          ]
        }
      ],
      '/kb-practice/': [
        {
          text: '第一部分 · 数据地基',
          collapsed: false,
          items: [
            { text: '01 · 为什么总是"能演示、不能用"', link: '/kb-practice/01-why-hard' },
            { text: '02 · 数据接入第一关', link: '/kb-practice/02-parsing' },
            { text: '03 · 切分策略', link: '/kb-practice/03-chunking' },
            { text: '04 · 元数据设计', link: '/kb-practice/04-metadata' }
          ]
        },
        {
          text: '第二部分 · 检索调优',
          collapsed: false,
          items: [
            { text: '05 · Embedding 选型', link: '/kb-practice/05-embedding' },
            { text: '06 · 混合检索三件套', link: '/kb-practice/06-hybrid-retrieval' },
            { text: '07 · 检索调优与 badcase 闭环', link: '/kb-practice/07-tuning-loop' }
          ]
        },
        {
          text: '第三部分 · 工程刚需',
          collapsed: false,
          items: [
            { text: '08 · 权限与多租户', link: '/kb-practice/08-permissions' },
            { text: '09 · 增量更新与版本管理', link: '/kb-practice/09-incremental-update' }
          ]
        },
        {
          text: '第四部分 · 验收与进阶',
          collapsed: false,
          items: [
            { text: '10 · 评测与上线', link: '/kb-practice/10-evaluation-launch' },
            { text: '11 · 进阶：GraphRAG / Agentic RAG', link: '/kb-practice/11-advanced-rag-choices' }
          ]
        }
      ],
      '/ai-sites/': [
        {
          text: '导航',
          collapsed: false,
          items: [
            { text: '资源地图（可搜索 · 按标签筛选）', link: '/ai-sites/' }
          ]
        },
        {
          text: '分类指南',
          collapsed: false,
          items: [
            { text: '01 · 模型与数据', link: '/ai-sites/01-model-hub' },
            { text: '02 · 论文与前沿', link: '/ai-sites/02-papers-frontier' },
            { text: '03 · 评测与榜单', link: '/ai-sites/03-benchmarks' },
            { text: '04 · 学习、资讯与社区', link: '/ai-sites/04-learn-community' },
            { text: '05 · Skill：去哪找，装之前查什么', link: '/ai-sites/05-skills' }
          ]
        }
      ]
    },
    footer: {
      message: 'AI 学习笔记 · 通俗图解系列，仅供学习交流',
      copyright: 'Copyright © 2026 Leoli04'
    }
  }
})
