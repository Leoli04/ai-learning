---
title: 多智能体：什么时候值得，什么时候是负担
---

# 多智能体：什么时候值得，什么时候是负担

> 约 8 分钟 · 关键词：多智能体、主管-工人、上下文隔离、A2A

## 一个 Agent 不够用的两种情形

"多智能体"听着高级，但它不是默认答案。真正需要它的理由只有两个：

  1. **上下文装不下**。"把这个模块重构一遍并补上测试"这类任务，如果全放在一个会话里做，中间过程（读过的文件、试过的方案、失败的日志）很快就把窗口塞满，模型开始丢关键信息。拆给几个各自独立上下文的 Agent，每个只拿自己那一小份，反而干净。
2. **需要不同立场互相检查**。让同一个模型"检查自己刚写的东西"，效果通常很差——它会沿着刚才的思路继续讲。换一个角色、换一段提示词的另一个实例来挑错，才真的能挑出来。

反过来也成立：**如果一个任务能在一个上下文里完成，也不需要独立验证，那多智能体只是把成本乘以几倍。**这是最常见的过度设计。

## 四种常见协作形态

  <table>
    <tr><th>形态</th><th>结构</th><th>适合</th></tr>
    <tr><td><strong>主管-工人</strong></td><td>一个主管拆任务、派活、汇总，工人只干被派的活</td><td>最常用、最好调试、最好控成本</td></tr>
    <tr><td><strong>流水线</strong></td><td>A 的输出直接喂给 B，串行推进</td><td>工序明确的流程：抓取 → 清洗 → 标注 → 入库</td></tr>
    <tr><td><strong>评审 / 辩论</strong></td><td>一个产出、一个挑错，来回几轮收敛</td><td>没有标准答案的写作、方案设计</td></tr>
    <tr><td><strong>群体 / 黑板</strong></td><td>多个 Agent 读写同一块共享工作区，无中心</td><td>探索性任务；最灵活也最容易失控</td></tr>
  </table>

  <figure class="figure">
    <svg viewBox="0 0 720 274" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a19" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <text x="50" y="22" font-size="11" class="dim">只有主管持有全局上下文，工人各自只拿到自己那一份——这就是拆分的意义</text>
        <rect x="270" y="34" width="180" height="52" rx="10" stroke-width="2" class="cell-em link-purple"/>
        <text x="360" y="58" text-anchor="middle" font-weight="bold">主管 Agent</text>
        <text x="360" y="76" text-anchor="middle" font-size="11" class="dim">拆任务 · 派活 · 裁决冲突</text>
        <rect x="50" y="126" width="180" height="68" rx="10" class="cell"/>
        <text x="140" y="152" text-anchor="middle">工人 1</text>
        <text x="140" y="176" text-anchor="middle" font-size="11" class="dim">独立上下文</text>
        <rect x="270" y="126" width="180" height="68" rx="10" class="cell"/>
        <text x="360" y="152" text-anchor="middle">工人 2</text>
        <text x="360" y="176" text-anchor="middle" font-size="11" class="dim">独立上下文</text>
        <rect x="490" y="126" width="180" height="68" rx="10" class="cell"/>
        <text x="580" y="152" text-anchor="middle">工人 3</text>
        <text x="580" y="176" text-anchor="middle" font-size="11" class="dim">独立上下文</text>
        <g stroke-width="1.8" marker-end="url(#a19)" class="link">
          <line x1="325" y1="86" x2="150" y2="122"/>
          <line x1="360" y1="86" x2="360" y2="122"/>
          <line x1="395" y1="86" x2="570" y2="122"/>
        </g>
        <g stroke-width="1.8" marker-end="url(#a19)" class="link-green">
          <line x1="140" y1="194" x2="140" y2="206"/>
          <line x1="360" y1="194" x2="360" y2="206"/>
          <line x1="580" y1="194" x2="580" y2="206"/>
        </g>
        <rect x="50" y="210" width="620" height="44" rx="10" class="cell link-green"/>
        <text x="360" y="228" text-anchor="middle">汇总 → 校验 → 交付</text>
        <text x="360" y="246" text-anchor="middle" font-size="11" class="dim">工人之间互不可见，结果冲突由主管裁决</text>
      </g>
    </svg>
    <figcaption>图 19：主管-工人形态——并行换来速度，上下文隔离换来干净</figcaption>
  </figure>

## 通信：从函数调用到协议

Agent 之间怎么"说话"，分两个层面：

  - **框架内部的通信**：消息传递（直接传文本或结构化消息）、共享工作区（文件、数据库、会话日志）。前者清晰但更容易丢背景，后者共享得彻底但容易互相踩。
  - **跨系统的通信**：**MCP** 解决的是"Agent ↔ 工具/数据源"；而 **A2A** 一类协议想解决"Agent ↔ Agent"——让不同厂商、不同服务里的 Agent 能互相发现、委托任务、回传结果。协议刚起步，生态还在长。

一句务实的提醒：生产环境里大量所谓"多智能体系统"，本质上就是**一个主 Agent 加若干次子任务调用**。看起来是多个 Agent 在协作，实际上调度权牢牢握在主 Agent 手里——这样延迟可控、成本可算、出问题可追。真正去中心化的群体协作，目前更多出现在研究和小规模实验里。

## 代价与决策准则

  <table>
    <tr><th>换来什么</th><th>付出什么</th></tr>
    <tr><td>上下文隔离：不被中间过程污染</td><td>信息传递有损耗，关键背景容易丢</td></tr>
    <tr><td>并行：墙钟时间下降</td><td>token 成本成倍，协调开销、结果冲突要合并</td></tr>
    <tr><td>独立验证：抓出单 Agent 的盲区</td><td>要提前想清楚"结论冲突时谁说了算"</td></tr>
  </table>

所以正确的顺序是从便宜到贵，一层层加：

  1. 先加**工具**——很多"能力不足"其实是没给它合适的工具；
2. 再加**评测**——没有评测集，多智能体只会让"变差了"更难被发现；
3. 再加**记忆与上下文管理**——多数"上下文装不下"是压缩和检索没做好；
4. 最后才加 **Agent 数量**。

判断标准只有一句：**单 Agent 在评测集上成绩够用，就不要上多智能体。**

::: tip
多智能体的真正价值是**两件事**：上下文隔离与独立验证。如果拆开之后既没隔离也没验证，只是把同一件事重复做了几遍，那它带来的只有账单。
:::

协作讲完了，还剩最后一公里：模型到底跑在谁的机器上。下一篇：**本地化部署与开源模型生态**。
