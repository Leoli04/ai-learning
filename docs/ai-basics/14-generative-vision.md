---
title: 生成式视觉：扩散模型怎么"画"出一张图
---

# 生成式视觉：扩散模型怎么"画"出一张图

> 约 9 分钟 · 关键词：扩散模型、Latent Diffusion、DiT、文生视频

## 先纠一个常见误解：模型不是"从草稿开始画"

很多人以为生成图片像画画：先勾线，再上色。主流做法恰恰相反——**从一张纯噪声出发，一点点把噪声擦掉。**

这条路线叫**扩散模型（Diffusion）**。它的训练目标朴素得出奇：拿一张图不断加噪直到变成一片雪花，再让模型学会"看着这片雪花和当前噪声强度，预测出被加进去的那份噪声"。学会之后把这个过程倒着跑，就能从噪声里"洗"出一张图。

在它之前的主流是 **GAN**（生成对抗网络）：一个网络造假图、一个网络做鉴别，互相博弈。GAN 出图快，但训练极不稳定，还容易"模式崩溃"（翻来覆去只会画那几类图）。扩散模型用"预测噪声"这个简单回归任务替换了对抗博弈，训练稳得多，代价是采样慢——要多跑很多轮。

## 生成一张图，走了三步

  <figure class="figure">
    <svg viewBox="0 0 720 270" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a14" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <rect x="30" y="30" width="180" height="66" rx="10" class="cell link-purple"/>
        <text x="120" y="54" text-anchor="middle" font-weight="bold">① 文本编码</text>
        <text x="120" y="74" text-anchor="middle" font-size="11" class="dim">Prompt → 语义向量</text>
        <text x="120" y="90" text-anchor="middle" font-size="11" class="dim">（CLIP / T5）</text>
        <rect x="270" y="30" width="180" height="66" rx="10" stroke-width="2" class="cell-em link"/>
        <text x="360" y="54" text-anchor="middle" font-weight="bold">② 潜空间去噪</text>
        <text x="360" y="74" text-anchor="middle" font-size="11" class="dim">噪声 → 一轮轮去噪</text>
        <text x="360" y="90" text-anchor="middle" font-size="11" class="dim">（UNet / DiT 骨干）</text>
        <rect x="510" y="30" width="180" height="66" rx="10" class="cell link-green"/>
        <text x="600" y="54" text-anchor="middle" font-weight="bold">③ 解码回像素</text>
        <text x="600" y="74" text-anchor="middle" font-size="11" class="dim">潜变量 → 图像</text>
        <text x="600" y="90" text-anchor="middle" font-size="11" class="dim">（VAE 解码器）</text>
        <g stroke-width="1.8" marker-end="url(#a14)" class="link">
          <line x1="210" y1="63" x2="266" y2="63"/>
          <line x1="450" y1="63" x2="506" y2="63"/>
        </g>
        <text x="360" y="124" text-anchor="middle" font-size="11" class="dim">文本向量在每一轮去噪中"指路"——这就是它"听话"的原因</text>
        <text x="30" y="160" class="dim">反向过程：每一步都预测并减掉一点噪声，逐步逼近图像</text>
        <rect x="30" y="174" width="110" height="46" rx="8" stroke-width="2" class="cell accent-red-stroke"/>
        <text x="85" y="194" text-anchor="middle">纯噪声</text>
        <text x="85" y="211" text-anchor="middle" font-size="11" class="dim">t = 1000</text>
        <rect x="160" y="174" width="110" height="46" rx="8" stroke-width="2" class="cell accent-orange-stroke"/>
        <text x="215" y="194" text-anchor="middle">还看不清</text>
        <text x="215" y="211" text-anchor="middle" font-size="11" class="dim">t = 750</text>
        <rect x="290" y="174" width="110" height="46" rx="8" stroke-width="2" class="cell accent-purple-stroke"/>
        <text x="345" y="194" text-anchor="middle">轮廓浮现</text>
        <text x="345" y="211" text-anchor="middle" font-size="11" class="dim">t = 500</text>
        <rect x="420" y="174" width="110" height="46" rx="8" stroke-width="2" class="cell accent-blue-stroke"/>
        <text x="475" y="194" text-anchor="middle">细节成型</text>
        <text x="475" y="211" text-anchor="middle" font-size="11" class="dim">t = 250</text>
        <rect x="550" y="174" width="120" height="46" rx="8" stroke-width="2" class="cell accent-green-stroke"/>
        <text x="610" y="194" text-anchor="middle">成品图像</text>
        <text x="610" y="211" text-anchor="middle" font-size="11" class="dim">t = 0</text>
        <text x="30" y="252" font-size="11" class="dim">训练时学的是"加噪的逆过程"，生成时按同样的节奏倒着走——"扩散"这名字就是这么来的。</text>
      </g>
    </svg>
    <figcaption>图 14：扩散生成三步——文本编码 → 潜空间多轮去噪 → 解码回像素</figcaption>
  </figure>

  1. **文本编码**：Prompt 先过一个文本编码器（CLIP、T5 一类），变成一串语义向量。它不画图，只负责指方向。
2. **潜空间去噪**：真正的画布不在像素上，而在被压缩过的"潜空间"里。VAE 编码器先把图像压成小得多的潜变量，去噪在这个小空间内完成——这是 **Latent Diffusion** 的关键一步，算力需求因此降了一个量级，消费级显卡才跑得动。骨干网络早期用 **UNet**，后来换成 Transformer 骨干，也就是 **DiT**。
3. **解码回像素**：去噪完毕的潜变量交给 VAE 解码器，还原成你看到的图像。

两个常被追问的细节：

  - **怎么让它"更听话"**：每一轮去噪都同时看潜变量和文本向量，文本相当于全程在旁边指路。想让结果更贴 Prompt，就调高**引导强度（guidance）**——代价是画面多样性下降，也更容易过曝。
  - **为什么现在只要几秒**：原始扩散要跑几十上百步。现在用蒸馏（一致性模型、Turbo / LCM 一类）把步数压到 4~8 步，速度直接上一个量级。

## 为什么忽然能生成视频了

视频 = 一连串图像 + 时间轴。把这套搬到视频上，核心改动是**把"图块"换成"时空图块"**：一段视频切出来的不是二维 patch，而是带时间维度的三维 patch，让模型在一次去噪里同时照顾空间和时间。

DiT 这类 Transformer 骨干在这里成为主流——它对序列长度的扩展性，比 UNet 更适合吃下"多帧 × 高分辨率"这种超长输入。剩下的还是老三样：**算力、数据、时序一致性约束**（物体不能一帧一个样）。早期视频生成常见的"物体变形""多长一只手"，本质上是时序一致性问题，不是画质问题。

## 可控生成：不止一句 Prompt

纯文本控制太粗糙，工程上通常叠加几种"外挂"：

  <table>
    <tr><th>手段</th><th>解决什么</th></tr>
    <tr><td><strong>ControlNet</strong></td><td>用骨架 / 深度 / 线稿约束构图——"姿势我定，画风你出"</td></tr>
    <tr><td><strong>参考图（IP-Adapter 类）</strong></td><td>保持主体或风格一致，用于角色复用、商品图</td></tr>
    <tr><td><strong>LoRA</strong></td><td>一个底座配多块"风格皮肤"，低成本定制画风</td></tr>
    <tr><td><strong>局部重绘 / 扩图</strong></td><td>只改指定区域，或把画布往外扩</td></tr>
  </table>

::: tip
一句话总结这条路线：**扩散模型把"生成"变成了"去噪"。**从噪声里洗出图像、洗出视频、洗出音频，都是同一套思路的不同实现——区别只在潜空间长什么样、骨干用什么网络。
:::

不过生成出来的东西好不好、值不值得信，光靠肉眼判断不了——下一篇聊**评测与可观测性**：怎么证明 AI 真的变好了。
