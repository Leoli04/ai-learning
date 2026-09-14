---
title: 数据接入第一关：PDF、扫描件与表格解析
---

# 数据接入第一关：PDF、扫描件与表格解析

> 约 10 分钟 · 关键词：文档解析、OCR、版面还原、表格抽取

## 解析做不好，后面全白做

有个现象很能说明问题：团队反馈"知识库搜不到这个规定"，你去查原始文档，那条规定明明就在第 12 页。再去看解析出来的文本——第 12 页的内容变成了三段乱序的文字，条款编号和正文分家了。

这不是检索问题，是**解析问题**。而且它有个残酷的特点：**后面任何环节都补不回来**。切分、Embedding、Rerank 都是在解析结果上做加工，输入丢了信息，输出不可能凭空长出来。

所以数据接入这一步的验收标准只有一个：**解析出来的文本，人工读一遍能不能读懂**。听起来很低，实际很多项目连这条都没过。

## 四类文档，四种坑

企业文档放到一起，基本能分成四类，处理路径完全不同：

  <figure class="figure">
    <svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a2" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <rect x="30" y="40" width="140" height="52" rx="9" class="cell"/>
        <text x="100" y="62" text-anchor="middle">文本型 PDF</text>
        <text x="100" y="80" text-anchor="middle" font-size="11" class="dim">自带文字层</text>
        <rect x="185" y="40" width="140" height="52" rx="9" class="cell"/>
        <text x="255" y="62" text-anchor="middle">扫描件 / 拍照</text>
        <text x="255" y="80" text-anchor="middle" font-size="11" class="dim">整页是图像</text>
        <rect x="340" y="40" width="140" height="52" rx="9" class="cell"/>
        <text x="410" y="62" text-anchor="middle">Office 文档</text>
        <text x="410" y="80" text-anchor="middle" font-size="11" class="dim">docx / xlsx / pptx</text>
        <rect x="495" y="40" width="140" height="52" rx="9" class="cell"/>
        <text x="565" y="62" text-anchor="middle">图片与截图</text>
        <text x="565" y="80" text-anchor="middle" font-size="11" class="dim">表格截图最常见</text>
        <path d="M 100 92 L 100 112 L 360 112 L 360 130" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 255 92 L 255 112" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 410 92 L 410 112" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 565 92 L 565 112 L 360 112" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 360 112 L 360 130" fill="none" stroke-width="1.8" marker-end="url(#a2)" class="link"/>
        <rect x="220" y="132" width="280" height="44" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="360" y="160" text-anchor="middle">先判断：有没有可提取的文字层？</text>
        <path d="M 360 176 L 360 195 L 205 195 L 205 212" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 360 176 L 360 195 L 515 195 L 515 212" fill="none" stroke-width="1.5" class="link-dim"/>
        <rect x="80" y="214" width="250" height="60" rx="9" class="cell link-green"/>
        <text x="205" y="238" text-anchor="middle">直接抽取文本</text>
        <text x="205" y="256" text-anchor="middle" font-size="11" class="dim">按版面顺序拼接，保留标题层级</text>
        <rect x="390" y="214" width="250" height="60" rx="9" class="cell link-orange"/>
        <text x="515" y="232" text-anchor="middle">OCR + 版面分析</text>
        <text x="515" y="250" text-anchor="middle" font-size="11" class="dim">识别文字区块，重建阅读顺序</text>
        <text x="515" y="266" text-anchor="middle" font-size="11" class="dim">拍照件先做纠偏与去噪</text>
        <path d="M 205 274 L 205 292 L 360 292 L 360 310" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 515 274 L 515 292 L 360 292" fill="none" stroke-width="1.5" class="link-dim"/>
        <path d="M 360 292 L 360 310" fill="none" stroke-width="1.8" marker-end="url(#a2)" class="link"/>
        <rect x="220" y="312" width="280" height="46" rx="9" class="cell"/>
        <text x="360" y="332" text-anchor="middle">结构化文本 + 元数据</text>
        <text x="360" y="349" text-anchor="middle" font-size="11" class="dim">标题层级 / 页码 / 表格 / 来源文件</text>
      </g>
    </svg>
    <figcaption>图 2：文档解析的两条路径——先判断有无文字层，再决定抽取还是 OCR</figcaption>
  </figure>

四类文档各自的坑：

  <table>
    <tr><th>类型</th><th>典型坑</th><th>处理要点</th></tr>
    <tr><td>文本型 PDF</td><td>双栏排版被按行打乱、页眉页脚混进正文、连字符断词</td><td>用带版面分析的解析器，别用纯文本抽取；页眉页脚按位置规则剔除</td></tr>
    <tr><td>扫描件 / 拍照</td><td>倾斜、阴影、印章遮挡、分辨率过低</td><td>先纠偏去噪再 OCR；低质量件宁可退回人工，别硬识别</td></tr>
    <tr><td>Office 文档</td><td>docx 里嵌的图片和文本框被漏掉、xlsx 多 sheet 只取第一个</td><td>解析时保留批注与内嵌对象；xlsx 逐 sheet 处理并记录 sheet 名</td></tr>
    <tr><td>图片与截图</td><td>内容在任何文件里都查不到——它只在钉钉群里</td><td>单独建一个"截图入库"通道，OCR 后标注来源人、时间</td></tr>
  </table>

## 表格是重灾区

如果只能盯一个点，盯表格。原因很简单：**企业文档里最值钱的信息往往在表格里**——价格表、审批额度、SLA 指标、组织架构。而表格恰恰是解析最容易垮的地方。

三类表格问题，按难度递增：

  1. **无边框表格**（靠空格对齐）：文本抽取出来是散的，"金额"和"数字"分家。这类靠位置聚类重建，简单表格能救。
  2. **合并单元格**：一个"2024 年度"横跨三列，抽取后变成只属于第一列。必须补全——**记住一个原则：合并单元格要"拆开填满"**，让每一行的每一格都能独立读懂。
  3. **跨页表格**：第 5 页的表头在第 6 页没了。处理方式是**检测续表并补回表头**，否则第 6 页的数据全成了没有列名的裸数字。

一个务实的建议：**表格解析出来后，单独存一份结构化数据（Markdown 表格或 JSON），而不是只留在文本流里。** 后面检索时，表格行往往是最精准的召回单元——一行"审批额度｜500 万以上｜需董事长批准"，比整段文字命中率高得多。

## 解析质量怎么验收

别用"看起来还行"验收。给一份可执行的检查清单，抽 20 份最难解析的文档逐条过：

  <table>
    <tr><th>检查项</th><th>通过标准</th></tr>
    <tr><td>阅读顺序</td><td>把解析文本连起来读，逻辑通顺，没有段落错位</td></tr>
    <tr><td>标题层级</td><td>一、二、三级标题能被识别出来（后面切分全靠它）</td></tr>
    <tr><td>页眉页脚</td><td>没有混进正文，也没把正文误删</td></tr>
    <tr><td>表格完整性</td><td>行数、列数对得上；合并单元格已展开；续表已补表头</td></tr>
    <tr><td>数字保真</td><td>金额、百分比、日期与原文逐字一致（重点查 0 和 O、1 和 l）</td></tr>
    <tr><td>元数据可溯源</td><td>每一段都能答出"来自哪个文件、第几页、哪一节"</td></tr>
  </table>

其中**数字保真**最容易出事：OCR 把"3.5%"认成"35%"或把"￥1,000"认成"￥1000"（少个零），检索照样命中、答案照样生成，但结果是错的——而且没人会发现。这类错误建议加一道校验：**抽取出的数字在原文里能否二次匹配到**，匹配不上就标记待人工确认。

::: tip
解析阶段的投入产出比是全流程最高的：**在这里多花一周，比在后面调三个月检索参数都有效**。而且它不依赖模型能力，纯工程活，做得踏实就能看见回报。
:::

解析出来的是"一团结构化文本"，还要切成能检索的单元。切分策略决定了检索的天花板——下一篇：**切分策略：chunk 怎么切才不丢信息**。
