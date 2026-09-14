---
title: 评测与可观测性：怎么证明 AI 真的变好了
---

# 评测与可观测性：怎么证明 AI 真的变好了

> 约 9 分钟 · 关键词：Benchmark、自建评测集、LLM-as-judge、Trace

## 为什么"感觉变好了"不算数

传统软件改完代码跑一遍测试就知道有没有坏。LLM 应用不行，因为它有三个麻烦：

  - **输出不确定**：同一个问题问两次，答案措辞可能不同——那这次变差是"改动导致"还是"随机波动"？
  - **变量太多**：改一句 Prompt、换个模型版本、调整一次温度，整条链的输出全变了，没有一个固定考题就没法横向比。
  - **公开基准不靠谱**：榜单会被针对性优化（刷榜）；题目往往离你的业务很远；更隐蔽的是**数据污染**——训练语料里混进过考题，分数高不代表你的场景能好。

结论很直接：**没有自己的评测集，所有"优化"都是凭感觉。**

## 三层评测体系

  <figure class="figure">
    <svg viewBox="0 0 720 274" xmlns="http://www.w3.org/2000/svg">
      <g font-size="12">
        <rect x="30" y="30" width="420" height="56" rx="10" stroke-width="2" class="cell-em link"/>
        <text x="55" y="54" font-weight="bold">① 离线评测</text>
        <text x="55" y="74" font-size="11" class="dim">公开基准 + 自建评测集，每次改动必跑一遍</text>
        <rect x="480" y="30" width="210" height="56" rx="10" class="cell"/>
        <text x="585" y="54" text-anchor="middle">快、便宜、可复现</text>
        <text x="585" y="74" text-anchor="middle" font-size="11" class="dim">负责拦住明显退步</text>
        <rect x="30" y="104" width="420" height="56" rx="10" class="cell link-green"/>
        <text x="55" y="128" font-weight="bold">② 在线观测</text>
        <text x="55" y="148" font-size="11" class="dim">trace / 成本 / 延迟 / 用户反馈，盯真实流量</text>
        <rect x="480" y="104" width="210" height="56" rx="10" class="cell"/>
        <text x="585" y="128" text-anchor="middle">在真实分布里找新问题</text>
        <text x="585" y="148" text-anchor="middle" font-size="11" class="dim">线上永远是"惊喜"来源</text>
        <rect x="30" y="178" width="420" height="56" rx="10" class="cell link-orange"/>
        <text x="55" y="202" font-weight="bold">③ 人工评审</text>
        <text x="55" y="222" font-size="11" class="dim">抽检标注、成对比较，定"什么算好"</text>
        <rect x="480" y="178" width="210" height="56" rx="10" class="cell"/>
        <text x="585" y="202" text-anchor="middle">最贵，但负责定标准</text>
        <text x="585" y="222" text-anchor="middle" font-size="11" class="dim">可借 LLM 裁判放大产能</text>
        <text x="30" y="258" font-size="11" class="dim">闭环：②里抓到的坏例子 → 人工确认后变成①里的新用例 → 之后每次改动自动回归。</text>
      </g>
    </svg>
    <figcaption>图 15：三层评测体系——离线拦退步、在线找问题、人工定标准</figcaption>
  </figure>

## 自建评测集：最土也最有效

做法没有技术含量，但回报最高：

  1. 从线上日志里捞出 50~200 条**真实请求**；
2. 人工写下"标准答案"或评分标准（可以是"必须包含这三点，且不能出现编造的条款号"）；
3. 每次改动跑一遍，只看**总分趋势**，不看单个用例的起伏。

四条容易踩的坑：

  - **用例必须来自真实分布**，别自己"编"题——你编的题恰好不会暴露真实问题；
  - **一定要有陷阱用例**：该拒答的、该说"不知道"的、格式边界、超长输入、带错别字的口语问法；
  - **用例冻结后做版本管理**，新增要有理由，更不能为了分数好看悄悄删掉难例；
  - **别盯着单个用例反复调 Prompt**，那是过拟合——在 60 条上反复打磨，第 61 条照样翻车。

## LLM-as-judge：用一个模型当裁判

开放题（翻译、摘要、文案）没有唯一答案，人工标注又贵，于是让强模型当裁判。能让它变可靠的三件事：

  <table>
    <tr><th>做法</th><th>为什么</th></tr>
    <tr><td><strong>成对比较 &gt; 绝对打分</strong></td><td>问"这两份哪个更好"比让模型打 1~10 分稳定得多</td></tr>
    <tr><td><strong>交换位置跑两遍</strong></td><td>模型有位置偏差（偏向选前面那个），交换后结果不一致的样本单独看</td></tr>
    <tr><td><strong>评分标准写进提示词</strong></td><td>不写清标准，模型会偏爱"更长、更漂亮、更像自己"的答案</td></tr>
    <tr><td><strong>人工校准 20% 样本</strong></td><td>先算裁判与人的一致率，一致性不过关就不能拿它当门禁</td></tr>
  </table>

## 可观测性：线上到底发生了什么

Agent 的一次请求，内部可能是几十次模型调用加工具调用。没有 trace，你只能看到一个总耗时和一句"答案不对"，无从下手。

要记下的东西：

  - 每一步的**输入输出摘要**、token 数、耗时；
  - 工具调用命中情况、失败与重试；
  - 最终状态（成功 / 拒答 / 被审批拦下 / 超时）；
  - 用户的显式反馈（点赞、点"没用"），挂到同一条 **trace ID** 上。

这一步最值钱的地方在于闭环：**用户点了一次"没用" → 顺着 trace 看到底哪一步崩了 → 人工确认后把它变成评测集里的新用例。**线上不会白跑，问题会自己变成考题。工具层面，Langfuse、LangSmith、Phoenix 一类都能用；数据不出内网的话，一张表加几个打点也能起步。

::: tip
评测不是一次性的"考试"，而是**一条流水线**：离线评测拦退步，在线观测找新问题，人工评审定标准——三者互相供料。**先有评测集，再谈优化。**
:::

评测能告诉你"答案不准"，但如果是"根本没查到该查的资料"呢？下一篇：**进阶 RAG——从"查得到"到"查得准"**。
