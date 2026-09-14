---
title: 为什么企业知识库总是"能演示、不能用"
---

# 为什么企业知识库总是"能演示、不能用"

> 约 8 分钟 · 关键词：企业知识库、五个死结、投入产出

## 演示阶段的三个"作弊"

很多团队都经历过同一个剧本：花两周做个知识库 demo，挑 50 份格式规整的文档，问几个提前想好的问题，答得挺漂亮，领导点头。三个月后再看——没人用了。

Demo 之所以好看，是因为它偷偷做对了三件事，而这三件事在生产环境全都不成立：

  1. **挑过数据**：只喂了干净的 PDF 和 Word，没碰扫描件、Excel 合并单元格、以及"截图贴在文档里的表格"。
  2. **挑过问题**：问题是出题人自己想的，用词和文档高度一致——而真实用户从不这么问。
  3. **没考虑权限**：所有人查所有文档，而真实场景里"销售不该看到人事的薪酬方案"。

所以"能演示"到"能用"之间，差的往往不是模型，是工程。换更强的模型救不了切分错误，也救不了权限漏洞。

## 五个真实死结

先看全貌——文档到答案之间要过五道关，每道关都会扣分：

  <figure class="figure">
    <svg viewBox="0 0 720 350" xmlns="http://www.w3.org/2000/svg">
      <g font-size="13">
        <line x1="60" y1="45" x2="60" y2="305" stroke-width="2" class="cell-stroke"/>
        <circle cx="60" cy="60" r="5" class="accent-blue-fill"/>
        <text x="80" y="55" font-weight="bold">第 1 关 · 数据接入</text>
        <text x="80" y="72" font-size="11" class="dim">PDF 丢版式、扫描件要 OCR、表格散架——文档里有，系统说没有</text>
        <circle cx="60" cy="116" r="5" class="accent-orange-fill"/>
        <text x="80" y="111" font-weight="bold">第 2 关 · 切分冻结</text>
        <text x="80" y="128" font-size="11" class="dim">段落被切断、标题层级丢失——答案缺半句，条款张冠李戴</text>
        <circle cx="60" cy="172" r="5" class="accent-purple-fill"/>
        <text x="80" y="167" font-weight="bold">第 3 关 · 检索命中</text>
        <text x="80" y="184" font-size="11" class="dim">用户说"报销上限"，文档写"差旅标准"——换个说法就搜不到</text>
        <circle cx="60" cy="228" r="5" class="accent-red-fill"/>
        <text x="80" y="223" font-weight="bold">第 4 关 · 权限隔离</text>
        <text x="80" y="240" font-size="11" class="dim">检索层不做过滤，只在前端藏——越权内容被拼进答案</text>
        <circle cx="60" cy="284" r="5" class="accent-green-fill"/>
        <text x="80" y="279" font-weight="bold">第 5 关 · 持续维护</text>
        <text x="80" y="296" font-size="11" class="dim">文档改了没人同步索引——三个月后开始一本正经地答过期信息</text>
        <text x="640" y="332" text-anchor="end" font-size="11" class="dim">演示只需走通前三关，生产环境每一关都在扣分</text>
      </g>
    </svg>
    <figcaption>图 1：企业知识库的五道关——演示与生产的差距就藏在这条链上</figcaption>
  </figure>

逐关拆开说：

  <table>
    <tr><th>关卡</th><th>卡在哪</th><th>最容易忽略的细节</th></tr>
    <tr><td><strong>数据接入</strong></td><td>解析器把内容读丢了</td><td>跨页表格、页眉页脚、扫描件方向、中文全半角</td></tr>
    <tr><td><strong>切分</strong></td><td>固定字数切，语义被切断</td><td>表格被切成两半、条款的"但书"跑到另一块</td></tr>
    <tr><td><strong>检索</strong></td><td>问法与文档用词对不上</td><td>缩写、别名、口语化提问、跨文档多跳</td></tr>
    <tr><td><strong>权限</strong></td><td>过滤做在了错误的位置</td><td>检索前过滤 vs 拿到结果再筛，前者才算安全</td></tr>
    <tr><td><strong>维护</strong></td><td>没有增量更新机制</td><td>删除是最大的坑——旧版本还在被检索到</td></tr>
  </table>

其中真正致命的往往是**第 4 关和第 5 关**：前三个出问题只是"答得不准"，用户抱怨两句还能忍；后两个出问题，一个是合规事故，一个是信任崩塌——一次答错的关键信息，足够让全员停止使用。

## 先别急着选向量库

做知识库的人有一半时间花在选型上：Milvus 还是 pgvector？要不要上 Rerank 模型？而这些问题的重要性，被严重高估了。

真实经验是：**换向量库带来的效果差异，通常小于"文档解析和切分做得好不好"带来的差异**。同一批文档，切分策略从固定字数改成按标题层级切，召回率的变化往往比换一个更强的 Embedding 模型还大。

所以更合理的投入顺序是这样：

  <table>
    <tr><th>顺序</th><th>做什么</th><th>为什么排这个位置</th></tr>
    <tr><td>①</td><td>拿最脏的 100 份文档跑通解析</td><td>它是后面一切的地基，脏数据永远救不回来</td></tr>
    <tr><td>②</td><td>定切分与元数据规范</td><td>决定了检索的天花板，且改起来要重建索引</td></tr>
    <tr><td>③</td><td>建评测集（哪怕只有 50 条）</td><td>没有它，后面所有优化都是凭感觉</td></tr>
    <tr><td>④</td><td>选检索方案：向量 → 混合 → Rerank</td><td>逐层加，每加一层用评测集确认收益</td></tr>
    <tr><td>⑤</td><td>最后才纠结向量库品牌</td><td>到这一步，你的数据量多半还没到需要纠结的规模</td></tr>
  </table>

注意第 ③ 步的位置。很多人把评测放到最后，结果前面几个月都在"感觉变好了"。**评测集不是验收工具，是开发工具。**

::: tip
知识库的效果上限，在你把文档喂进去之前就已经定了一大半。别用"换个更强的模型"去治一个数据工程问题。
:::

## 这个系列怎么走

后面十篇沿着那五道关逐关拆解，每一篇都尽量给出可落地的做法和取舍：

  <table>
    <tr><th>篇目</th><th>主题</th></tr>
    <tr><td>02</td><td>数据接入第一关：PDF、扫描件与表格解析</td></tr>
    <tr><td>03</td><td>切分策略：chunk 怎么切才不丢信息</td></tr>
    <tr><td>04</td><td>元数据设计：让检索能按部门、时间、类型过滤</td></tr>
    <tr><td>05</td><td>Embedding 选型：中文场景怎么挑模型</td></tr>
    <tr><td>06</td><td>混合检索：BM25 + 向量 + Rerank 三件套</td></tr>
    <tr><td>07</td><td>检索调优：查询改写、多路召回与 badcase 闭环</td></tr>
    <tr><td>08</td><td>权限与多租户：谁能看哪些文档</td></tr>
    <tr><td>09</td><td>增量更新与版本管理：文档改了、删了怎么办</td></tr>
    <tr><td>10</td><td>评测与上线：怎么证明它"答得准"</td></tr>
    <tr><td>11</td><td>进阶：GraphRAG / Agentic RAG 的适用边界</td></tr>
  </table>

第一篇就从不那么性感、但决定生死的一步开始——下一篇：**数据接入第一关：PDF、扫描件与表格解析**。
