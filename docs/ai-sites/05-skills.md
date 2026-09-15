---
title: Skill：去哪找，装之前查什么
---

# Skill：去哪找，装之前查什么

> 约 11 分钟 · 关键词：Agent Skills、技能市场、SKILL.md、安全核验

前面四篇讲的是"信息从哪来"：模型、论文、榜单、课程。这一篇讲的是**能力从哪来**。

这两件事的差别很大。模型和数据是**原料**，你拿回来还得自己组织；论文和榜单是**判断依据**，用来决定做什么；而 Skill 是**已经封装好的做法**——别人把一件事该怎么做、分几步、哪一步容易错，写成了 Agent 能直接执行的说明书。装一个 Skill，本质上是在借用别人的经验。

也正因为如此，Skill 是这个地图里**唯一需要先看安全再谈好不好用**的一类。

## 先搞清一个 Skill 长什么样

一个 Skill 不是一段提示词，而是一个**目录**：

  <table>
    <tr><th>组成</th><th>放什么</th><th>什么时候被读取</th></tr>
    <tr><td><code>SKILL.md</code></td><td>YAML 头写 <code>name</code> 与 <code>description</code>，正文是给 Agent 的指令、流程与判断规则</td><td>技能被匹配到时读全文</td></tr>
    <tr><td><code>scripts/</code></td><td>可执行的确定性操作，比如解析、转换、调用接口</td><td>某一步真的需要时才执行</td></tr>
    <tr><td><code>references/</code>、<code>assets/</code></td><td>参考资料、模板、素材</td><td>指令里点到时才打开</td></tr>
  </table>

关键在于它是**渐进式加载**的：会话开始时，Agent 只看到所有已安装技能的 `name` 加一句 `description`；匹配到任务了才去读 `SKILL.md` 全文；真正需要某个文件时才打开它。所以装几十个技能，也不会把上下文塞满。

  <figure class="figure">
    <svg viewBox="0 0 720 250" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a5" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <text x="30" y="28">Agent 先只看到名字和一句话，用到才一层层展开</text>
        <rect x="30" y="50" width="200" height="110" rx="9" class="cell"/>
        <text x="130" y="76" text-anchor="middle" font-size="11" class="dim">第一层 · 会话开始</text>
        <text x="130" y="98" text-anchor="middle" font-weight="bold">只暴露一行</text>
        <text x="130" y="124" text-anchor="middle" font-size="11" class="dim">name + description</text>
        <text x="130" y="144" text-anchor="middle" font-size="11" class="dim">装得再多也不占满</text>
        <rect x="260" y="50" width="200" height="110" rx="9" class="cell link"/>
        <text x="360" y="76" text-anchor="middle" font-size="11" class="dim">第二层 · 命中了</text>
        <text x="360" y="98" text-anchor="middle" font-weight="bold">读完整指令</text>
        <text x="360" y="124" text-anchor="middle" font-size="11" class="dim">SKILL.md 全文</text>
        <text x="360" y="144" text-anchor="middle" font-size="11" class="dim">流程与判断规则</text>
        <rect x="490" y="50" width="200" height="110" rx="9" class="cell-em link-green"/>
        <text x="590" y="76" text-anchor="middle" font-size="11" class="dim">第三层 · 要用到</text>
        <text x="590" y="98" text-anchor="middle" font-weight="bold">才打开附件</text>
        <text x="590" y="124" text-anchor="middle" font-size="11" class="dim">references 资料</text>
        <text x="590" y="144" text-anchor="middle" font-size="11" class="dim">scripts 脚本</text>
        <g stroke-width="1.8" marker-end="url(#a5)" class="link">
          <line x1="232" y1="105" x2="256" y2="105"/>
          <line x1="462" y1="105" x2="486" y2="105"/>
        </g>
        <text x="30" y="198" font-size="11" class="dim">代价是 description 变成了最要紧的字段：它同时决定要不要用、什么时候用</text>
        <text x="30" y="224" font-size="11" class="dim">写不清 description 的技能，等于没装——Agent 根本想不到要用它</text>
      </g>
    </svg>
    <figcaption>图 5：一个 Skill 的三层加载——只暴露一行，命中读全文，用到才展开附件</figcaption>
  </figure>

这里有个容易被忽略的推论：**`description` 是 Skill 里最值钱的一行**。它写不清，这个技能就永远不会被触发——你装了，但等于没装。

## 去哪找：按可信度分四层

  <table>
    <tr><th>层</th><th>站点</th><th>怎么用</th></tr>
    <tr><td>规范</td><td><code>agentskills.io</code></td><td>自己写之前必读。字段定义、目录约定、命名限制都在这定死，别凭感觉编</td></tr>
    <tr><td>官方仓库</td><td>Anthropic 官方 Skill 仓库</td><td>抄最权威的写法。含文档四件套（docx/pdf/pptx/xlsx）、最简模板与规范原文</td></tr>
    <tr><td>分发与市场</td><td>skills.sh · ClawHub · 腾讯云 SkillHub · 复旦 DataHub Skills</td><td>要现成能力时用。前两个在海外需代理，后两个国内直连且带中文搜索</td></tr>
    <tr><td>精选集</td><td>Awesome Agent Skills · Superpowers · Hugging Face · Trail of Bits</td><td>想成体系地装一套：开发方法论、模型与数据处理、安全审计各有专攻</td></tr>
  </table>

几个判断，帮你少走弯路：

- **市场越大，越要靠筛选机制**。ClawHub 规模最大（两万多个技能），也最杂；腾讯云 SkillHub 是国内镜像，带官方精选 Top 50 与安全审计，中文搜索体验好；复旦 DataHub 则是用**质量加安全双维度打分**排序，适合"不想一个个看"的时候。
- **官方仓库里的文档四件套值得单独留意**。它们就是 Claude 生成 Word、Excel、PPT、PDF 时真正在跑的那套 Skill，属于"生产环境在用"的参考实现——但注意它们是 source-available，不是开源，主要是给你当范本。
- **第一次装，先装元技能**。也就是 `skill-creator` 这类"帮你写 Skill 的 Skill"：它会反过来问你流程、生成目录、把 `SKILL.md` 写好。与其装十个别人的，不如先学会写一个自己的，因为**你自己重复做三次的那件事，才是最值得封装的**。

## 挑的时候，别只看下载量

下载量高说明它解决的问题普遍，**不说明它解决的问题和你的一样**。真正该看的四件事：

- **它到底要不要跑代码**：打开 `scripts/` 看一眼。如果只是"整理文档"却带了网络请求和文件遍历，就该警惕。
- **它依赖什么**：需要外部 API、密钥、特定二进制、特定操作系统的，装上也可能跑不通。
- **它对什么场景说话**：好的 Skill 会在正文里写"什么时候**不**该用它"。只讲优点的，多半没在真实场景里磨过。
- **最近动过没有**：长期停更的 Skill 未必坏，但它描述的接口可能早就变了。

## 装之前，必须过的四关

这一节是整篇最该记住的部分。

**Skill 的风险比提示词高一个量级**：提示词再离谱，最坏结果是回答不好；而 Skill 可以携带可执行代码，Agent 会真的去运行它。一个名字叫"帮我整理文档"的 Skill，如果脚本里藏了读取凭据或者批量删除，从名字上是完全看不出来的。

所以装之前至少过这四关：

  1. **看有没有扫描结果**。ClawHub 与 SkillHub 都提供病毒扫描与"良性"标记，优先选带标记的；没有扫描结果的第三方技能，新手一律不装。
  2. **看权限是否相称**。申请了跟功能无关的高风险权限（文档处理却要全盘读写），这就是红旗，直接放弃。
  3. **看来源与更新**。优先官方或高星开发者，优先稳定版，优先近期有维护的。
  4. **自己再审一遍**。本机装了安全审计类技能的话，装之前先跑一次，成本很低，收益很高。

可信度的优先级记一下，遇到拿不准的情况就按这个顺序退守：

::: tip
**客户端内置技能市场 > 国内官方社区 > 官方注册中心 > 其他第三方渠道**
:::

前两者的共同点是**有官方审核环节**，等于有人替你先筛过一遍；而开放注册中心的技能是社区投稿，规模最大、质量方差也最大。

## 装进来之后：管住数量

技能装多了会出两类问题。

一是**同质冲突**：两个技能都声称能处理 Excel，Agent 匹配到哪个不确定，输出就会不稳定。装之前先查一遍有没有功能重叠的，有就只留一个。

二是**选择噪音**：渐进式加载确实让成本变低——每个技能只占一行，但**几十行 description 同样是噪音**。技能列表越长，Agent 挑错的概率越高。

一个实用的做法：**按项目配置，而不是全局堆**。做完的项目把技能摘掉，留下半年没用过的就删。技能库和代码库一样，需要定期清理。

## 自己写第一个：从二十行开始

写 Skill 最常见的错误，是第一版就写得很大。更靠谱的路径是：

  1. **先写 `description`**，而且要用"什么时候该用"的口吻写。比如"当用户需要把 Excel 里的多表合并并核对重复项时使用"，比"强大的表格处理工具"有用得多。
  2. **正文只写流程与判断规则**，不写背景知识。背景知识属于 `references/`，别让它占用每次加载的上下文。
  3. **把确定性的操作交给脚本**。凡是"每次都得算对"的事，写成代码比让模型生成可靠得多。
  4. **跑不通就回来改 `description`**。多数"技能不触发"的问题，根因都在描述写得不够具体。

写完之后，把它放进版本控制——团队分发 Skill 最好的方式就是进仓库，评审、回溯、回滚都跟代码一样。

## 这个系列的收尾

五篇走下来，回到那张地图：**模型与数据**决定了你能用什么，**论文与前沿**决定了你知道什么，**评测与榜单**决定了你怎么判断真假，**Skill** 决定了你能直接借用多少别人的经验，**学习与社区**决定了你能走多远。

地图上每一条都写着核实日期。这个领域的站点会关停、会改名（Papers with Code 的关停与重建就在那张地图里），所以**别把它当收藏夹，当成一个说明"为什么值得看"的索引**。真正跟着你的不是那些链接，而是这几套动作习惯：先筛后读、先定位再动手、用自建评测集投票、装能力之前先做安全核验。

想把这几种能力串成能交付的东西，接着读三个系列长文：**《AI 基础》** 第 8 篇讲清 Skill 与 MCP 的分工，**《DeepSeek Harness 通俗图解》** 第 11 篇讲一个真实框架里技能与项目约定怎么落地，**《企业知识库实战》** 十一篇讲从文档解析到上线验收的完整链路。
