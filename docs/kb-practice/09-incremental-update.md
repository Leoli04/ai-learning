---
title: 增量更新与版本管理：文档改了、删了怎么办
---

# 增量更新与版本管理：文档改了、删了怎么办

> 约 9 分钟 · 关键词：增量索引、删除、原子切换、幂等

## 文档是活的，索引不能是死的

上线那天索引是准的，三个月后就变质了。这是知识库从"能用"走向"不能用"最典型的路径，而且过程很安静——**没人报错，只是答案慢慢开始不对劲。**

变质的来源有四种，处理难度完全不一样：

  <table>
    <tr><th>变更</th><th>难度</th><th>坑在哪</th></tr>
    <tr><td>新增文档</td><td>低</td><td>基本无害，只是别忘了把它也走一遍解析与切分</td></tr>
    <tr><td>修改文档</td><td>中</td><td>旧版本的 chunk 必须清掉，否则新旧两版同时被检索到</td></tr>
    <tr><td><strong>删除文档</strong></td><td><strong>高</strong></td><td>最容易做漏；且系统可能"凭记忆"继续回答已删除的内容</td></tr>
    <tr><td>改名 / 移动目录</td><td>中</td><td>如果部门信息是从目录路径推断的，移动会改变权限归属（第 04 篇）</td></tr>
  </table>

## 删除是最大的坑

删除之所以最难，是因为它有三层，漏掉任何一层都会出问题：

  <table>
    <tr><th>层次</th><th>要做什么</th><th>漏掉的后果</th></tr>
    <tr><td>原始存储</td><td>文件从文档库里移除</td><td>不严重，最多占空间</td></tr>
    <tr><td>索引层</td><td>该文档所有 chunk 从向量库与 BM25 索引中删除</td><td><strong>已被删除的内容还会被检索到并生成答案</strong></td></tr>
    <tr><td>缓存与摘要</td><td>清掉引用该文档的答案缓存、已生成的摘要</td><td>缓存里还留着旧答案，用户照样看得到</td></tr>
  </table>

第二层尤其容易漏，因为删除 chunk 不像删除文件那样直观——你得先查"这篇文档一共切了多少块、块 ID 是什么"，再批量删。**务实的做法是在元数据里给每个 chunk 打上 `doc_id`，删除时按 `doc_id` 一次性清空**，而不是靠文件名匹配（文件改名后就匹配不上了）。

还有一个更隐蔽的问题：**模型可能"凭记忆"回答已删除的内容。** 因为那条信息在之前的对话里出现过，或者模型的预训练数据里本来就有。这种"幻觉残留"没办法从索引层根治，只能在提示词里明确约束：**答案必须基于检索到的片段，检索不到就说不知道。** 这也让第 10 篇要讲的"忠实度"评测变得必要。

另外提醒一点：**多数情况下应该"标记作废"而不是物理删除**（第 04 篇提过）。审计、法务、争议处理都可能需要查"当年那版是怎么规定的"。正确做法是元数据标 `state: 已作废`，检索时默认过滤掉，但保留在库里。

## 更新怎么触发

  <table>
    <tr><th>方式</th><th>做法</th><th>优点</th><th>代价</th><th>适合</th></tr>
    <tr><td>定时全量重建</td><td>每晚 / 每周全库重跑一遍</td><td>实现最简单、状态最干净</td><td>贵、慢，且重建期间数据是旧的</td><td>文档量小（万级以下）、变更不频繁</td></tr>
    <tr><td><strong>增量监听</strong></td><td>监听文件系统事件 / 数据库 binlog / 定时扫 mtime，只处理变化的文档</td><td>快、省，接近实时</td><td>要处理并发与重复触发</td><td>文档量大、变更频繁</td></tr>
    <tr><td>手动上传触发</td><td>用户在界面上传，上传动作即触发处理</td><td>最可控，状态清晰</td><td>遗漏"非上传渠道"的变更</td><td>初期阶段，或文档由专人维护</td></tr>
  </table>

比较稳的组合是**增量监听为主 + 定期全量重建兜底**：日常靠增量，每月跑一次全量校准，防止增量逻辑长期运行后出现"漏了某几次变更"的漂移。

## 幂等与原子切换

增量更新最容易出问题的两个地方，各有一个成熟解法：

  <table>
    <tr><th>问题</th><th>解法</th></tr>
    <tr><td>同一份文档被重复触发处理（改一次触发了两遍）</td><td><strong>用内容 hash 判断</strong>：算文档内容的哈希值，与库中记录的一致就跳过。这样重复触发天然安全</td></tr>
    <tr><td>重建期间用户查不到内容（索引被清空或正在写入）</td><td><strong>写新索引 + 原子切换别名</strong>：新数据写进一个独立的物理索引，写完再用别名（alias）一次性指过去</td></tr>
  </table>

第二种做法是搜索领域的老套路，但在知识库里同样关键：

  <figure class="figure">
    <svg viewBox="0 0 720 420" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a9" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <rect x="165" y="32" width="120" height="48" rx="9" class="cell"/>
        <text x="225" y="61" text-anchor="middle">新增文档</text>
        <rect x="300" y="32" width="120" height="48" rx="9" class="cell"/>
        <text x="360" y="61" text-anchor="middle">修改文档</text>
        <rect x="435" y="32" width="120" height="48" rx="9" class="cell"/>
        <text x="495" y="61" text-anchor="middle">删除文档</text>
        <path d="M 225 80 L 225 100 L 495 100" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 495 80 L 495 100" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 360 80 L 360 116" fill="none" stroke-width="1.8" marker-end="url(#a9)" class="link"/>
        <rect x="210" y="120" width="300" height="44" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="360" y="147" text-anchor="middle">比对内容 hash，判断是否真的变了</text>
        <path d="M 360 164 L 360 192" fill="none" stroke-width="1.8" marker-end="url(#a9)" class="link"/>
        <rect x="210" y="196" width="300" height="44" rx="9" class="cell"/>
        <text x="360" y="223" text-anchor="middle">只重建受影响的 chunk，不清空全库</text>
        <path d="M 360 240 L 360 268" fill="none" stroke-width="1.8" marker-end="url(#a9)" class="link"/>
        <rect x="210" y="272" width="300" height="44" rx="9" class="cell link-green"/>
        <text x="360" y="299" text-anchor="middle">写入新索引 → 原子切换别名</text>
        <rect x="140" y="348" width="440" height="44" rx="9" class="cell link-orange"/>
        <text x="360" y="375" text-anchor="middle" font-size="11">删除单独走一条路：标记作废 + 清 chunk + 清缓存</text>
      </g>
    </svg>
    <figcaption>图 9：增量更新链路——hash 判重、局部重建、原子切换，删除单独处理</figcaption>
  </figure>

别名切换这个动作能带来一个很实际的好处：**切换前的旧索引可以继续服务**。也就是说重建过程对用户完全无感，不需要"维护窗口"——这对企业内部系统很重要，你不可能让 HR 早上九点登不上系统。

## 版本管理的三个层次

  <table>
    <tr><th>层次</th><th>做法</th><th>用途</th></tr>
    <tr><td>文档版本</td><td>同一份文档保留 v1 / v2 / v3，元数据记录当前版本</td><td>看历史、做审计、对比变化</td></tr>
    <tr><td>chunk 归属</td><td>每个 chunk 带 <code>doc_id</code> + <code>doc_version</code></td><td>按文档精确删除、按版本过滤</td></tr>
    <tr><td>模型与索引版本</td><td>记录 <code>embedding_model</code>、<code>embedding_version</code>、索引构建时间</td><td>换模型时能分批重建（第 05 篇）</td></tr>
  </table>

第三层最容易被忽略，但在换 Embedding 模型那天会救你一命——没有版本标记，你无法判断库里哪些向量是旧模型产的，只能全量重跑。

::: tip
判断增量方案是否合格，用一个场景测：**把一份文档改一个字、再删掉一份文档，多久之后系统能正确反映这两个变化？** 如果答案是"下次全量重建时"，那这套索引在真实使用中迟早会误导人。
:::

索引能持续保持新鲜，系统就算"活着"了。但怎么证明它答得准、敢不敢让全员用——下一篇：**评测与上线：怎么证明它"答得准"**。
