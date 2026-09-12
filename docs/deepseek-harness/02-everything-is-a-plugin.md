---
title: 一切皆插件：没有"特权阶级"的架构
---

# 一切皆插件：没有"特权阶级"的架构

> 约 15 分钟 · 关键词：插件、Cordis、ctx、Service、Event、可逆 Effect

读完你会得到三样东西：

1. **看清** dsh 的"插件化"到底在革谁的命——不是 React/Vue 那种 UI 组件，而是**框架内部每条核心路径**都有可能被替换。
2. **理解** Cordis 三件套（Service / Event / Effect）的协作方式，特别是 Effect 的"可逆性"为什么是分布式友好的关键。
3. **会写** 一个最小 dsh 插件，并知道它和 Spring DI / Koa middleware / Express plugin 在**能力维度**上的差别。

---

## 一、传统框架的痛点：特权核心

如果你用过任何"主流框架"——不管前端、后端、AI——你应该都见过这种结构：

```text
       用户代码（业务、扩展点）
            │
            ▼
  ┌────────────────────────────┐
  │      框架核心 kernel        │  ←─ 特权代码
  │   (引擎、调度、I/O 主循环)  │
  └────────────────────────────┘
            │
            ▼
        调用系统资源
```

图 1 把"特权核心"和"一切皆插件"两种思路直接放在一起对比：

<figure class="figure">
  <svg viewBox="0 0 760 280" xmlns="http://www.w3.org/2000/svg">
    <rect x="20" y="20" width="340" height="240" rx="12" class="cell"/>
    <text x="190" y="46" text-anchor="middle" font-size="15" class="em">传统框架：有特权核心</text>
    <rect x="60" y="80" width="260" height="48" rx="8" class="cell-em"/>
    <text x="190" y="104" text-anchor="middle" font-size="14" class="em">kernel / engine（硬）</text>
    <text x="190" y="120" text-anchor="middle" font-size="11" class="dim">负责调度、I/O、主循环</text>
    <rect x="50" y="160" width="80" height="32" rx="6" class="cell"/>
    <text x="90" y="180" text-anchor="middle" font-size="12">hook A</text>
    <rect x="150" y="160" width="80" height="32" rx="6" class="cell"/>
    <text x="190" y="180" text-anchor="middle" font-size="12">hook B</text>
    <rect x="250" y="160" width="80" height="32" rx="6" class="cell"/>
    <text x="290" y="180" text-anchor="middle" font-size="12">hook C</text>
    <text x="190" y="225" text-anchor="middle" font-size="11" class="dim">想替换调度？改源码或等官方 PR</text>
    <text x="190" y="243" text-anchor="middle" font-size="11" class="dim">⚠ 扩展点由框架决定</text>
    <line x1="380" y1="20" x2="380" y2="260" stroke-dasharray="4 4" class="link-dim"/>
    <text x="380" y="140" text-anchor="middle" font-size="22" class="em">vs</text>
    <rect x="400" y="20" width="340" height="240" rx="12" class="cell-em"/>
    <text x="570" y="46" text-anchor="middle" font-size="15" class="em accent-blue">dsh：一切皆插件</text>
    <g font-size="11">
      <rect x="430" y="78"  width="120" height="32" rx="6" class="cell"/>
      <text x="490" y="98"  text-anchor="middle">模型 adapter</text>
      <rect x="590" y="78"  width="120" height="32" rx="6" class="cell"/>
      <text x="650" y="98"  text-anchor="middle">工具注册表</text>
      <rect x="430" y="120" width="120" height="32" rx="6" class="cell"/>
      <text x="490" y="140" text-anchor="middle">会话日志</text>
      <rect x="590" y="120" width="120" height="32" rx="6" class="cell"/>
      <text x="650" y="140" text-anchor="middle">Agent 主循环 ←自己</text>
      <rect x="430" y="162" width="120" height="32" rx="6" class="cell"/>
      <text x="490" y="182" text-anchor="middle">系统 prompt 组装</text>
      <rect x="590" y="162" width="120" height="32" rx="6" class="cell"/>
      <text x="650" y="182" text-anchor="middle">你的自定义插件</text>
    </g>
    <circle cx="570" cy="220" r="18" class="cell-em link"/>
    <text x="570" y="225" text-anchor="middle" font-size="12" class="em">ctx</text>
    <text x="570" y="248" text-anchor="middle" font-size="11" class="dim">上下文总线</text>
  </svg>
  <figcaption>图 1：传统"特权核心" vs dsh 的"上下文总线"</figcaption>
</figure>

它带来的真实痛苦是：

- **替换某条核心路径**：只能在源码上 fork，或者等框架作者开 PR，你的进度被别人的发布节奏锁死。
- **测试某条核心路径**：你甚至不能独立加载它——因为它依赖一整条主流程。
- **"扩展点"看起来很多，但真要的那些都没开**：比如你想拦截每条 LLM 调用做审计，往往没有官方钩子，只能 monkey-patch。

dsh 想解的是**根本问题**：让"框架提供的每一块肌肉"都成可拆卸的部件——你能换它、测它、组合它。**它**没有内置的"调度引擎"。它自己就是**一撮插件的容器**。

> 一句话总结：**dsh 里没有特权代码，连驱动 Agent 干活的主循环也是一个名为 `ctx.agentLoop` 的插件。**

---

## 二、Cordis 三件套：Service / Event / Effect

dsh 不是从零造轮子，它构建在开源框架 [Cordis](https://github.com/cordiverse/cordis) 之上。Cordis 把"插件"这件事拆成三件互不耦合的机制：

| 机制 | 干什么 | 对应代码里常见的东西 |
|------|--------|--------------------|
| **Service** | 往共享上下文 `ctx` 上挂载可被其他插件调用的能力 | `ctx.llm`、`ctx.tools`、`ctx.sessions` |
| **Event** | 插件之间**不直接调用**，而是发/听消息 | `ctx.on('llm:call', handler)` |
| **可逆 Effect** | 插件注册进来的任何资源（事件订阅、计时器、文件、连接）**卸载时自动回收** | `ctx.effect(() => startTimer(...))` |

图 2 直观展示这套三件套怎么围绕 `ctx` 工作。

<figure class="figure">
  <svg viewBox="0 0 760 320" xmlns="http://www.w3.org/2000/svg">
    <rect x="320" y="120" width="120" height="80" rx="10" class="cell-em"/>
    <text x="380" y="152" text-anchor="middle" font-size="18" class="em accent-blue">ctx</text>
    <text x="380" y="172" text-anchor="middle" font-size="11" class="dim">共享上下文</text>
    <text x="380" y="190" text-anchor="middle" font-size="10" class="dim">（Service 挂在它上面）</text>
    <g font-size="12">
      <rect x="40" y="40" width="180" height="60" rx="8" class="cell"/>
      <text x="130" y="62" text-anchor="middle" class="em">① Service</text>
      <text x="130" y="80" text-anchor="middle" class="dim">能力注册表</text>
      <text x="130" y="94" text-anchor="middle" class="dim">ctx.llm / ctx.tools</text>
      <line x1="220" y1="70" x2="320" y2="140" class="link"/>
      <rect x="540" y="40" width="180" height="60" rx="8" class="cell"/>
      <text x="630" y="62" text-anchor="middle" class="em">② Event</text>
      <text x="630" y="80" text-anchor="middle" class="dim">解耦消息</text>
      <text x="630" y="94" text-anchor="middle" class="dim">ctx.on / ctx.emit</text>
      <line x1="540" y1="70" x2="440" y2="140" class="link"/>
      <rect x="40" y="220" width="180" height="60" rx="8" class="cell"/>
      <text x="130" y="242" text-anchor="middle" class="em">③ Effect（可逆）</text>
      <text x="130" y="260" text-anchor="middle" class="dim">注册即生效</text>
      <text x="130" y="274" text-anchor="middle" class="dim">卸载即回收</text>
      <line x1="220" y1="250" x2="320" y2="180" class="link-green"/>
      <rect x="540" y="220" width="180" height="60" rx="8" class="cell"/>
      <text x="630" y="242" text-anchor="middle" class="em">④ 你写的插件</text>
      <text x="630" y="260" text-anchor="middle" class="dim">本地工程化代码</text>
      <text x="630" y="274" text-anchor="middle" class="dim">装/卸如拔插</text>
      <line x1="540" y1="250" x2="440" y2="180" class="link-green"/>
    </g>
  </svg>
  <figcaption>图 2：Cordis 三件套围绕 ctx 协作（Service 写、Event 传、Effect 管生命周期）</figcaption>
</figure>

### 2.1 Service — 把能力挂到 ctx 上

每个插件最常见的动作是**贡献一个服务**。比如内置的 `model-adapter` 插件会往 `ctx` 上挂 `ctx.llm`，外部插件就能 `await ctx.llm.chat(...)` 调模型。Service 没有强制接口——你能往 ctx 上挂任何东西，名字约定而已。

```ts
ctx.service('llm', {
  async chat(messages) {
    return await callProvider(this.provider, messages)
  },
})
```

`ctx.service(name, value)` 只是个花式赋值。**真正的解耦来自 Event 和 Effect**。

### 2.2 Event — 插件间不直接调用

如果 A 插件想"知道" B 插件的某次操作，**不要**写 `await b.doSomething()`。B 发事件，A 订阅：

```ts
// B 插件：发
await ctx.emit('tool:call', { name, input })

// A 插件：监听（可以多个订阅者）
ctx.on('tool:call', async (e) => {
  await auditLog.write(e)
})
```

好处是双重的：

1. **A 完全不知道 B 的存在**——加 A 不需要改 B 的代码。
2. **可以叠加多个监听者**——A 做审计、C 做限流、D 做埋点，互不干扰。

dsh 自己内部也是这么用的：工具调用、模型调用、会话开始/结束，都是事件而不是同步函数。

### 2.3 可逆 Effect — 这是 Cordis 的灵魂

Cordis 最精髓的发明是 **Effect**：你声明"我想做什么"，框架记下来"卸载我的时候**自动反向操作**"。**完全不用手写清理代码**。

图 3 展示一个可逆 effect 的生命周期。

<figure class="figure">
  <svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg">
    <line x1="40" y1="100" x2="700" y2="100" stroke-width="2" class="link"/>
    <polygon points="700,100 690,95 690,105" class="accent-blue-fill"/>
    <text x="380" y="85" text-anchor="middle" font-size="12" class="dim">时间轴</text>
    <g font-size="12">
      <rect x="30" y="110" width="100" height="50" rx="6" class="cell-em"/>
      <text x="80" y="132" text-anchor="middle" class="em">注册</text>
      <text x="80" y="148" text-anchor="middle" class="dim">插件装上</text>
      <rect x="170" y="110" width="140" height="50" rx="6" class="cell"/>
      <text x="240" y="132" text-anchor="middle" class="em">effect 跑起来</text>
      <text x="240" y="148" text-anchor="middle" class="dim">订阅 / 计时器 / 连接</text>
      <rect x="350" y="110" width="100" height="50" rx="6" class="cell"/>
      <text x="400" y="132" text-anchor="middle" class="em">使用中</text>
      <text x="400" y="148" text-anchor="middle" class="dim">业务消耗资源</text>
      <rect x="490" y="110" width="100" height="50" rx="6" class="cell-stroke"/>
      <text x="540" y="132" text-anchor="middle" class="em">dispose</text>
      <text x="540" y="148" text-anchor="middle" class="dim">插件被卸</text>
      <rect x="630" y="110" width="120" height="50" rx="6" class="cell-stroke"/>
      <text x="690" y="132" text-anchor="middle" class="em">自动回滚</text>
      <text x="690" y="148" text-anchor="middle" class="dim">资源全部释放</text>
    </g>
    <text x="40" y="40" font-size="13" class="em accent-green">正向生命周期</text>
    <line x1="40" y1="50" x2="370" y2="50" stroke-width="1.5" class="link-green"/>
    <text x="490" y="40" font-size="13" class="em accent-orange">反向生命周期</text>
    <line x1="490" y1="50" x2="750" y2="50" stroke-width="1.5" class="link-orange"/>
  </svg>
  <figcaption>图 3：可逆 Effect 让"注册 = 自动释放"成为框架内建</figcaption>
</figure>

具体长什么样？比如下面这段代码，开发者**没有一行手动 cleanup**，但 3 个副作用都会在插件卸载时被自动清掉：

```ts
ctx.plugin(function myPlugin(ctx) {
  // ① 文件系统副作用
  ctx.effect(() => watchFile('./config.json', (e) => reload(e)))

  // ② 计时器
  const id = setInterval(() => heartbeat(), 1000)
  ctx.effect(() => () => clearInterval(id))

  // ③ RPC 连接
  const conn = openTCPSocket(8080)
  ctx.effect(() => () => conn.close())
})
```

当 `ctx.dispose(myPlugin)` 被调用——也就是这个插件下线的时候——3 个注册过的 effect 全部反向触发：**文件系统观察器停止订阅、定时器清掉、TCP 连接关闭**。

这种"我声明正向副作用、卸载时反向自动跑"的设计，你大概在 **Rust 的 Drop trait**、**Go 的 defer**、**Java 的 try-with-resources** 里见过类似思想。Cordis 把这个能力下放到了插件生命周期里——**整个 dsh 进程的"安全下线"也靠它**。这是为什么 dsh 把可逆 effect 提到这么高的优先级：它支持比如"按用户临时加载/卸载某段 LLM 流程"、"热重载某个 bundle 而不丢状态"这种需求。

> 易踩的坑：如果你用了**裸的 Node API**（`setInterval`、`fs.watch`、`net.connect`）而不是包在 `ctx.effect(...)` 里，卸载时这些资源会**泄漏**——这是 Cordis 用户最常问的问题。

---

## 三、对比：Cordis vs 你见过的"插件体系"

不是所有"插件"都做到 Cordis 这个深度。下面把它和几个常见框架摆在一起对比：

| 维度 | Cordis/dsh | Spring (DI) | Koa middleware | Express plugin | VS Code ext |
|------|------------|-------------|----------------|----------------|------------|
| 替换**框架核心** | ✅ 主循环可换 | ❌ | ❌ | ❌ | 部分 |
| 跨插件通信 | Event（解耦） | 直接注入 | `ctx.next()` 串联 | 同 Koa | API 调用 |
| 自动资源回收 | **可逆 Effect** | Bean 生命周期 | 需手动 | 需手动 | dispose API |
| 热重载单元 | 单个插件 | 整个容器 | 整个进程 | 整个进程 | 扩展 |
| 学习曲线 | 中 | 陡 | 缓 | 缓 | 中 |

重点解释两个差最大的：

- **Spring DI 是"装配期"的插件化**——你换 `DataSource` 实现，但不能让 Spring 反过来"不听 ApplicationContext 的话"。**dsh 是"运行期"的插件化**——主循环本身可以换，这意味着你甚至能写一个"完全不同的 Agent 循环策略"作为插件分发出去。
- **Koa 中间件是请求级生命周期**——它依赖 Koa 引擎。而 dsh 的 Effect 是**插件级生命周期**——一个插件可以套另一个插件，卸载顺序自动维护（后注册先释放）。

所以 dsh 的"插件"不是说它做了 React 那种组件化，它**根本就是在重新回答"框架的边界应该画在哪里"这个问题**。

---

## 四、动手：写一个最小 dsh 插件

下面是骨架级别的最小可运行例子（伪代码，基于官方 demo 简化）。

```ts
// plugins/hello.ts
import { Context } from '@cordis/core'

export function helloPlugin(ctx: Context) {
  // 1. 注册一个 service
  ctx.service('hello', {
    greet(name: string) {
      return `Hi, ${name}!`
    },
  })

  // 2. 发个事件让别人能感知
  ctx.emit('plugin:loaded', { name: 'hello' })

  // 3. 监听别人的事件（如果关心的话）
  ctx.on('session:start', () => {
    console.log('[hello] session started')
  })
}
```

启动并验证：

```ts
// app.ts
import { Context } from '@cordis/core'
import { helloPlugin } from './plugins/hello'

const ctx = new Context()
ctx.plugin(helloPlugin)

console.log(ctx.hello.greet('Alice'))   // → "Hi, Alice!"
console.log(Object.keys(ctx))           // → [..., 'hello']

ctx.dispose()                           // 卸载 hello 插件
console.log(ctx.hello)                  // → undefined
```

卸载时即使你没写任何 `removeListener`，`session:start` 的订阅也会**自动消失**——这是 Effect 系统干的。

---

## 五、反模式：什么**不**该插件化

"一切皆插件"听起来很美，但**过犹不及**。官方仓库 `docs/` 下也专门提醒过：

- **把"业务核心算法"当插件分发 = 性能 + 复杂度双输**。插件机制是为了让能力可替换，**不是为了把每段业务都拆成可拆卸**。如果一段算法 100 行且只会被一种方式调用，包进 plugin 反而增加间接层和加载成本。
- **过度细颗粒拆分**。把一个本来该是一个对象的方法拆成 6 个 Service + 7 个 Event，再做胶水——这是把简单问题搞复杂。**好的插件是边界清晰的"能力"，而不是"工具函数搬家"。**
- **把 Effect 当 try/catch 用**。Effect 是资源生命周期，不是错误处理。需要 try/catch 的地方直接 try/catch。

记住一句话：**插件化解决的是"我哪天要换掉这块"的问题**——如果不会换，就别拆。

---

## 六、自检清单

打开手机或者心里默念，回答这 5 个问题。答不全没关系，回头找答案。

1. dsh 里**驱动 Agent 干活的主循环**叫什么 service？答：`ctx.agentLoop`。
2. 插件之间不直接调用，而是发——  答：发"事件"（`ctx.emit`），靠订阅（`ctx.on`）协作。
3. 三个 `setInterval`、`fs.watch`、`net.connect` 没用 `ctx.effect` 包，结果卸载后会怎样？答：会泄漏，进程上下文不干净。
4. dsh 是构建在 ___ 框架之上的？答：[Cordis](https://github.com/cordiverse/cordis)。
5. 一句话解释为什么 dsh 选"可逆 Effect"而不是用 try/finally 手写 cleanup？答：手动 cleanup 在多层插件叠加时容易漏，且出错时容易留半资源；可逆 Effect 把"释放"内建到框架卸载流程里，**多插件任意嵌套都不会漏**。

---

## 小结

| 记住 | 含义 |
|------|------|
| **没有特权核心** | 连主循环都是 `ctx.agentLoop` 插件 |
| **Service / Event / Effect 三件套** | 写能力、走消息、管生命周期 |
| **可逆 Effect 是灵魂** | 卸载一行调用，所有副作用自动反向，**可放心做热重载** |
| **不适合把业务核心也拆** | 插件是为"将来要换"留的能力边界 |

那这一堆插件，启动时是怎么"叠成"一个真正能跑的 dsh 进程的？背后那个 `profile → bundle → patch` 三层加载机制就是**下一篇**要拆的事。
