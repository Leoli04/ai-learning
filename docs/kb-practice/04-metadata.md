---
title: 元数据设计：让检索能按部门、时间、类型过滤
---

# 元数据设计：让检索能按部门、时间、类型过滤

> 约 9 分钟 · 关键词：元数据、前置过滤、有效期、溯源

## 向量相似度只回答了"像不像"

纯向量检索有个根本局限：它只算"这段内容和问题像不像"，完全不知道"这段内容该不该被这个人看到""这条规定是不是已经作废了"。

举个企业里天天发生的例子：用户问"年假能休几天"。库里同时躺着 2019 版和 2024 版的《考勤管理办法》，两段文字向量相似度几乎一样。**纯向量检索会把两条都捞出来，然后模型可能引用作废的那条。** 结果不是"答得不准"，是"答错了还理直气壮"。

补救办法就是元数据——给每个 chunk 挂上结构化的标签，让检索多出一个维度的判断依据。

## 三类元数据

  <figure class="figure">
    <svg viewBox="0 0 720 310" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a4" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <text x="30" y="54" class="dim">先检索，再过滤</text>
        <rect x="190" y="32" width="140" height="48" rx="9" class="cell"/>
        <text x="260" y="61" text-anchor="middle">向量检索 Top-100</text>
        <line x1="334" y1="56" x2="366" y2="56" stroke-width="1.8" marker-end="url(#a4)" class="link"/>
        <rect x="370" y="32" width="140" height="48" rx="9" class="cell link-orange"/>
        <text x="440" y="61" text-anchor="middle">按权限过滤</text>
        <line x1="514" y1="56" x2="546" y2="56" stroke-width="1.8" marker-end="url(#a4)" class="link-orange"/>
        <rect x="550" y="32" width="110" height="48" rx="9" class="cell link-orange"/>
        <text x="605" y="61" text-anchor="middle">只剩 3 条</text>
        <text x="190" y="96" font-size="11" class="accent-orange">合法的文档可能压根没进前 100 → 用户以为系统"不知道该规定"</text>
        <text x="30" y="152" class="dim">先过滤，再检索</text>
        <rect x="190" y="130" width="140" height="48" rx="9" class="cell link-green"/>
        <text x="260" y="159" text-anchor="middle">按权限过滤</text>
        <line x1="334" y1="154" x2="366" y2="154" stroke-width="1.8" marker-end="url(#a4)" class="link-green"/>
        <rect x="370" y="130" width="140" height="48" rx="9" class="cell"/>
        <text x="440" y="159" text-anchor="middle">向量检索 Top-10</text>
        <line x1="514" y1="154" x2="546" y2="154" stroke-width="1.8" marker-end="url(#a4)" class="link"/>
        <rect x="550" y="130" width="110" height="48" rx="9" stroke-width="2" class="cell-em link-green"/>
        <text x="605" y="159" text-anchor="middle">10 条全可用</text>
        <text x="190" y="194" font-size="11" class="accent-green">在合法子集里检索：召回数量有保证，且不会把越权内容送进答案</text>
        <rect x="30" y="228" width="200" height="56" rx="9" class="cell"/>
        <text x="130" y="250" text-anchor="middle">来源元数据</text>
        <text x="130" y="269" text-anchor="middle" font-size="11" class="dim">文件名 页码 章节 版本</text>
        <rect x="245" y="228" width="200" height="56" rx="9" class="cell"/>
        <text x="345" y="250" text-anchor="middle">业务元数据</text>
        <text x="345" y="269" text-anchor="middle" font-size="11" class="dim">部门 文档类型 产品线</text>
        <rect x="460" y="228" width="200" height="56" rx="9" class="cell"/>
        <text x="560" y="250" text-anchor="middle">权限元数据</text>
        <text x="560" y="269" text-anchor="middle" font-size="11" class="dim">可见范围 密级 所有者</text>
      </g>
    </svg>
    <figcaption>图 4：过滤必须在检索之前——顺序颠倒会同时损失召回和安全性</figcaption>
  </figure>

三类元数据各管一件事：

  <table>
    <tr><th>类别</th><th>典型字段</th><th>它解决的问题</th></tr>
    <tr><td><strong>来源元数据</strong></td><td>文件名、页码、章节路径、版本、上传时间</td><td>答案能不能溯源；出问题时能不能定位到原文件</td></tr>
    <tr><td><strong>业务元数据</strong></td><td>部门、文档类型、产品线、标签、密级</td><td>检索时能不能"只查我关心的范围"</td></tr>
    <tr><td><strong>权限元数据</strong></td><td>可见范围（角色/部门/用户组）、所有者、密级</td><td>谁能看到哪些内容——安全底线</td></tr>
  </table>

## 过滤顺序：一个方向性错误

这是本篇最值得记住的一条：**过滤必须发生在检索之前，不能检索完再筛。**

原因有两层：

  <table>
    <tr><th>做法</th><th>问题</th></tr>
    <tr><td>先检索 Top-100，再按权限筛</td><td>① 合法文档可能排在第 200 位，压根进不了候选集 → 大量"系统不知道"的漏答；② 越权内容短暂经过了应用层，日志、审计、缓存都可能留痕</td></tr>
    <tr><td>先按权限圈定合法子集，再在子集里检索</td><td>召回有保证，且越权内容从头到尾没被读出过</td></tr>
  </table>

实现上要注意一个坑：**部分向量库的过滤是"事后过滤"（post-filter）**——它先按向量取 Top-K，再筛掉不满足条件的，返回数量就少了。这类引擎要么开启"过度取回"（oversampling，先取 5～10 倍再筛），要么改用支持前置过滤（pre-filter）或分区（partition）的方案。选型时必须确认这一点，因为它直接决定第 08 篇讲的权限方案能不能落地。

## 时间：让过期文档自动失效

企业文档最怕的不是"没写"，是"写过了但作废了"。所以元数据里必须有时间概念：

  <table>
    <tr><th>字段</th><th>取值</th><th>检索时的用法</th></tr>
    <tr><td>生效日期</td><td>2024-01-01</td><td>还没生效的文档默认不返回</td></tr>
    <tr><td>失效日期</td><td>2026-12-31 或空</td><td>已过期的默认不返回，除非用户显式要求"查历史"</td></tr>
    <tr><td>版本 / 状态</td><td>v3 / 现行 · 已作废 · 草案</td><td>同主题多版本时只取"现行"</td></tr>
    <tr><td>更新时间</td><td>2025-08-20</td><td>可作为排序权重：同等相关度下优先更新的</td></tr>
  </table>

这里有个容易被忽略的配套问题：**作废的文档不能物理删除，只能标记状态。** 因为用户有时确实要查"当年那版是怎么规定的"（审计、法务、争议处理都需要）。正确做法是元数据标 `state: 已作废` + 默认过滤掉，而不是从库里删干净。

## 元数据从哪来

指望人工逐条填写是不现实的，实际做法是三层叠加：

  <table>
    <tr><th>来源</th><th>能拿到什么</th><th>可靠性</th></tr>
    <tr><td>解析阶段自动带出</td><td>文件名、页码、章节路径、文档格式</td><td>高（机器天然知道）</td></tr>
    <tr><td>规则推断</td><td>从目录结构推部门（`/人事制度/` → 人事部）；从文件名推类型与年份</td><td>中（要允许人工纠正）</td></tr>
    <tr><td>人工 / 系统对接补录</td><td>密级、可见范围、所有者</td><td>必须有人负责，不能猜</td></tr>
  </table>

**密级和可见范围绝对不能让模型猜。** 这两项一旦猜错就是权限事故，宁可让上传者在下拉框里多选一次，也不要"智能推断"。

::: tip
元数据设计的检验标准很朴素：**当用户提问时，你有没有能力把检索范围圈到"他能看的那一小块"。** 如果做不到，说明元数据还停留在"记录信息"的层面，没有变成"检索能力"。
:::

数据地基到这里就搭完了：解析、切分、元数据。接下来进入检索环节，第一件事是选对 Embedding 模型——下一篇：**Embedding 选型：中文场景怎么挑模型**。
