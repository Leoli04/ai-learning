---
title: 评测与榜单：分数怎么读，坑在哪里
---

# 评测与榜单：分数怎么读，坑在哪里

> 约 10 分钟 · 关键词：LMArena、SWE-bench、榜单污染、中文评测

## 先摆正态度：榜单是观测，不是事实

榜单很有用，但它的本质是**一次带口径的观测**：在特定题目集上、按特定规则打分、在特定时间点得到的排名。换题目集、换打分规则、换时间，结果可能完全不同。

真正危险的不是"榜单不准"，而是**把榜单当结论**——"它第一，所以用它"。域名会换、版本会迭代，但读榜单的方法一直管用。下面这张表是各类榜单各自擅长回答的问题：

  <table>
    <tr><th>类型</th><th>代表站点</th><th>它擅长回答</th><th>它回答不了</th></tr>
    <tr><td>人类盲测</td><td>LMArena</td><td>真实体感上谁更讨人喜欢</td><td>复杂任务上谁更可靠</td></tr>
    <tr><td>多轴横向对比</td><td>Artificial Analysis</td><td>质量、价格、速度之间怎么权衡</td><td>你的私有语料上谁更好</td></tr>
    <tr><td>抗污染基准</td><td>LiveBench</td><td>去掉"训练时见过"的水分后还剩多少</td><td>工程场景的端到端效果</td></tr>
    <tr><td>领域基准</td><td>SWE-bench</td><td>代码 Agent 能不能真的把 bug 改对</td><td>其他领域的能力</td></tr>
    <tr><td>中文评测</td><td>OpenCompass 司南 / SuperCLUE</td><td>中文任务上的相对位置</td><td>海外模型的实际差距</td></tr>
  </table>

## 关键判断：先问这五个问题

看到任何一个榜单分数，动手之前先在心里过一遍这五个问题。它们能过滤掉大部分误导。

  <figure class="figure">
    <svg viewBox="0 0 720 280" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a3" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <text x="30" y="28">从"它第一"到"我该用哪个"，中间隔着五个追问</text>
        <rect x="30" y="56" width="180" height="96" rx="9" class="cell"/>
        <text x="120" y="84" text-anchor="middle" font-weight="bold">榜单名次</text>
        <text x="120" y="110" text-anchor="middle" font-size="11" class="dim">它领先 0.3 分</text>
        <text x="120" y="132" text-anchor="middle" font-size="11" class="dim">看起来很确定</text>
        <rect x="270" y="56" width="180" height="96" rx="9" class="cell link"/>
        <text x="360" y="84" text-anchor="middle" font-weight="bold">追问五件事</text>
        <text x="360" y="110" text-anchor="middle" font-size="11" class="dim">口径、污染、方差</text>
        <text x="360" y="132" text-anchor="middle" font-size="11" class="dim">版本、成本</text>
        <rect x="510" y="56" width="180" height="96" rx="9" class="cell-em link-green"/>
        <text x="600" y="84" text-anchor="middle" font-weight="bold">你自己的评测集</text>
        <text x="600" y="110" text-anchor="middle" font-size="11" class="dim">几十道真实题目</text>
        <text x="600" y="132" text-anchor="middle" font-size="11" class="dim">才是最终依据</text>
        <g stroke-width="1.8" marker-end="url(#a3)" class="link">
          <line x1="214" y1="104" x2="262" y2="104"/>
          <line x1="454" y1="104" x2="502" y2="104"/>
        </g>
        <text x="30" y="190" font-size="11" class="dim">① 这些题目，它在训练时见过吗</text>
        <text x="30" y="214" font-size="11" class="dim">② 领先 0.3 分，是真的差还是在误差范围里</text>
        <text x="30" y="238" font-size="11" class="dim">③ 拿第一的那个版本，和你实际调得到的是同一个吗</text>
        <text x="30" y="262" font-size="11" class="dim">④ 价格和速度差多少——榜单不会帮你算这笔账</text>
      </g>
    </svg>
    <figcaption>图 3：读榜单的五个追问——分数只是起点，评测集才是终点</figcaption>
  </figure>

## 五个坑，逐个说清

### 坑一：训练数据污染

这是最普遍也最难察觉的问题。基准题目公开在网络上，模型训练时很可能"见过答案"。表现是：模型在经典基准上分数惊人，一换新题就掉一截。

**LiveBench** 的设计就是为了对抗这一点——它持续用新发布的题目替换旧题，并尽量让题目难以从公开语料中检索到答案。所以当你看到某个模型在经典基准上遥遥领先，值得先去 LiveBench 看它在"没见过的题"上表现如何。

### 坑二：人类盲测偏好的是"讨喜"，不是"正确"

**LMArena** 让用户盲测两个模型的回答并投票，是很接近真实体感的信号。但它的偏差也很明确：**投票人偏好长回答、排版漂亮、语气确定的答案**。一个把不确定的地方老实说出来的模型，反而容易输给一个自信地胡说的模型。

所以 LMArena 适合判断"用户会不会喜欢它"，不适合判断"它可不可靠"。做客服、做写作可以多看它；做数据分析、做代码生成，别只看它。

### 坑三：平均分会掩盖方差

一个模型总分领先，但它可能在你的场景类型上恰好是弱项。**榜单给你的是平均表现，你要的是特定分布上的表现。**

处理方式很简单：在榜单上找到**和你场景最接近的那个子项**（比如代码、数学、长文本、指令跟随），按子项而不是总分来选。

### 坑四：榜单上的版本和你拿到的不一样

榜单常跑的是**官方最强配置**——最大的尺寸、最高的推理预算、最新的内部版本。而你通过 API 拿到的可能是量化版、被限流的版本，或者默认关闭了推理模式。**同一模型不同配置的差距，经常比榜单上第一和第十的差距还大。**

### 坑五：忽略成本结构

榜单很少把价格和速度放在显眼位置，但它们对落地决策的影响往往更大。这时候 **Artificial Analysis** 特别实用：它把质量、价格、速度三条轴放在同一张表里，让你直接看到"多花三倍钱能换来多少质量提升"。**如果提升只有一两个点，那这个选择本身就错了。**

## 中文场景：多看一眼本土榜单

中文任务有自己的难点：分词、成语与俗语、行业术语、长文档里的表格。海外榜单上的排名不能直接迁移过来。**OpenCompass 司南**（国内大模型评测体系，方法与榜单都可查）与 **SuperCLUE**（专注中文能力的榜单）是这一层最实用的两个入口。

但要留意一点：**中文榜单里样本以国产模型为主，和海外模型的可比性有限**。它们的正确用法是"在国产模型之间选型"，而不是"证明国产已经超越谁"。

::: tip
最省事的做法：**先看 Artificial Analysis 把候选缩到三个，再用你自己那几十道真实题目跑一遍**。自建评测集的门槛比想象中低——几十道来自真实业务的题就够用了，而这几十道题的判断力，超过任何公开榜单。
:::

## 一张决策顺序表

  <table>
    <tr><th>你的阶段</th><th>用哪个榜单</th><th>看什么</th></tr>
    <tr><td>完全不了解，先缩小范围</td><td>Artificial Analysis</td><td>质量 / 价格 / 速度的三角权衡</td></tr>
    <tr><td>怕被榜单骗</td><td>LiveBench</td><td>换新题后排名有没有大变</td></tr>
    <tr><td>做代码 Agent</td><td>SWE-bench</td><td>真实仓库里的修复成功率</td></tr>
    <tr><td>做面向用户的产品</td><td>LMArena</td><td>真实体感偏好</td></tr>
    <tr><td>中文业务</td><td>OpenCompass / SuperCLUE</td><td>中文子项排名</td></tr>
    <tr><td>准备上线</td><td>自己的评测集</td><td>这才是唯一有决定权的一票</td></tr>
  </table>

看到这里，站点、论文、榜单三件事都齐了。最后一篇换个方向：**当你需要从零学起，或者想持续跟上这个领域时，该看谁的博客、进哪个社区。**
