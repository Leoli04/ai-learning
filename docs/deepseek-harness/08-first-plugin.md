---
title: 写一个真实插件：从最小插件到一个能用的工具
---

# 写一个真实插件：从最小插件到一个能用的工具

> 约 10 分钟 · 关键词：apply(ctx)、cordis.yml、defineTool、effect、HMR

## 插件长什么样：一个导出 apply 的函数

在 dsh 里，插件就是一个导出 `apply` 函数的 TypeScript 模块：

```ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'my-plugin'

export function apply(ctx: Context) {
  // 在这里注册能力
}
```

就这么点东西——**没有基类、没有必需清单、没有 manifest**。框架在加载时调用 `apply`，把 `ctx`（上下文对象）递给你，你通过 `ctx` 把能力挂上去。

除了函数形式，还支持另外两种写法：

  <table>
    <tr><th>形态</th><th>写法</th><th>什么时候用</th></tr>
    <tr><td><strong>函数</strong></td><td><code>export function apply(ctx)</code></td><td>默认选择，覆盖绝大多数场景</td></tr>
    <tr><td><strong>对象</strong></td><td><code>export default { name, inject, apply }</code></td><td>想把元信息与逻辑写在一起</td></tr>
    <tr><td><strong>类</strong></td><td><code>class MyService extends Service</code></td><td>要对外提供服务、供别的插件注入时</td></tr>
  </table>

## 把它挂进 cordis.yml

dsh 用 **patch 文件**做"插入式覆盖"。新建一个 `cordis.yml`：

```yaml
- insert:
    - id: hello
      name: '/absolute/path/to/scratch-plugin/src/my-plugin.ts'
```

启动时用 `--patch` 指过去：

```sh
pnpm dsh web --patch ./scratch-plugin/cordis.yml
```

启动过程中，终端会打印插件里的 `console.log`——加载成功。

::: warning
`name` 必须是**绝对路径**（或可解析的包名）。patch 只贡献配置，**不会**改变 loader 解析模块路径时使用的基准目录——所以相对路径是这里最容易踩的坑。
:::

## 三个必须知道的机制

### 1. 注册即自动清理

通过 `ctx` 注册的任何东西——事件监听、工具、定时器——在插件卸载时都会被框架自动回收，你不需要手写 `removeListener` 或 `clearInterval`。

确有需要手动释放的资源（比如一条网络连接），用 `ctx.effect()` 把清理方式交回给框架：

```ts
import type { Context } from '@deepseek-ai/cordis'

export function apply(ctx: Context) {
  ctx.effect(() => {
    const timer = setInterval(() => {
      console.log('heartbeat')
    }, 5000)

    // 返回的函数会在插件卸载时执行
    return () => clearInterval(timer)
  })
}
```

这条约定是"一切皆插件"能成立的地基——第 2 篇讲过的**可逆 Effect**，在写插件时就是你天天要用的东西。

### 2. 依赖要显式声明

要用别的服务（`tools`、`llm` 之类），导出 `inject`：

```ts
export const inject = ['tools']
```

框架会确保这些服务就绪后才加载你的插件。**不声明就取不到**——这也是解决"启动顺序"问题的唯一正经办法，而不是靠 `setTimeout` 猜。

### 3. 配置变更会触发热替换

修改 `cordis.yml` 里某个插件的 `config`，框架会卸载旧实例、加载新实例。因为注册都是 effect、会自动清理，替换后不会残留旧实例的注册——第 3 篇讲的 profile → bundle → patch 分层，在开发时就是这个体验。

## 写一个真正能用的工具

骨架搭好了，工具才是 Agent 能"动手"的地方。dsh 提供了 `defineTool` 这个 DSL：

```ts
import type { Context } from '@deepseek-ai/cordis'
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'greet-tool'
export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'greet',
    description: 'Greet someone by name.',
    parameters: {
      name: { type: 'string', required: true, description: 'The name to greet' },
    },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    async execute(args) {
      return `Hello, ${args.name}!`
    },
  }))
}
```

启动后直接对它说 `Use the greet tool to greet Ada.`，模型就会调用 `greet` 并拿到 `Hello, Ada!`。

这个 DSL 最值得学的是**三层职责分离**：

  <table>
    <tr><th>字段</th><th>职责</th></tr>
    <tr><td><code>parameters</code></td><td>模型看到的"调用说明"——schema 会据此推导并校验 <code>args</code></td></tr>
    <tr><td><code>execute</code></td><td>真正干活，返回 <code>output.schema</code> 声明的**规范值**（结构化数据，不是拼给模型看的字符串）</td></tr>
    <tr><td><code>output.render</code></td><td>把规范值转成面向模型的内容；同一份数据还可以另做界面卡片</td></tr>
  </table>

把"执行结果"和"给模型看的样子"拆开，是 dsh 工具设计里很关键的一刀：同一份规范值，一边喂给模型、一边渲染成 UI，互不干扰。

## 让插件可配置

dsh 有一条硬约定：**凡是不同部署可能取不同值的参数，都必须做成配置字段，不允许硬编码。**

```ts
import type { Context } from '@deepseek-ai/cordis'
import Schema from '@deepseek-ai/schemastery'

export interface Config {
  greeting: string
  maxRetries: number
}

export const Config: Schema<Config> = Schema.object({
  greeting: Schema.string().default('Hello'),
  maxRetries: Schema.number().default(3),
})

export function apply(ctx: Context, config: Config) {
  console.log(config.greeting)  // 用户值或 schema 默认值
}
```

配套的 yml：

```yaml
- insert:
    - id: hello
      name: './src/my-plugin.ts'
      config:
        greeting: 'Hi there'
```

自检标准只有一句话：**这个值能不能只改 `cordis.yml` 就变，而不用动代码？** 不能，就说明它该被提出来做配置。另外别导出普通对象当 `Config`——它不满足 Cordis 要求的 Standard Schema 接口。

还有一个设计原则值得偷师：**配置错误要响亮**。在 schema 里把自身完备的约束表达清楚，让不合法配置在加载时就失败，而不是带着坏配置一路跑下去。

  <figure class="figure">
    <svg viewBox="0 0 720 156" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a08" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" class="accent-blue-fill"/></marker></defs>
      <g font-size="12">
        <rect x="30" y="30" width="145" height="64" rx="9" class="cell"/>
        <text x="102" y="50" text-anchor="middle" font-weight="bold">cordis.yml</text>
        <text x="102" y="70" text-anchor="middle" font-size="11" class="dim">路径 + config</text>
        <text x="102" y="86" text-anchor="middle" font-size="11" class="dim">insert 覆盖层</text>
        <rect x="200" y="30" width="145" height="64" rx="9" stroke-width="2" class="cell-em link-orange"/>
        <text x="272" y="50" text-anchor="middle" font-weight="bold">Schema 校验</text>
        <text x="272" y="70" text-anchor="middle" font-size="11" class="dim">加载时执行</text>
        <text x="272" y="86" text-anchor="middle" font-size="11" class="dim">不合法 → 直接失败</text>
        <rect x="370" y="30" width="145" height="64" rx="9" stroke-width="2" class="cell-em link"/>
        <text x="442" y="50" text-anchor="middle" font-weight="bold">apply(ctx)</text>
        <text x="442" y="70" text-anchor="middle" font-size="11" class="dim">注册能力</text>
        <text x="442" y="86" text-anchor="middle" font-size="11" class="dim">工具 / 事件 / 服务</text>
        <rect x="540" y="30" width="150" height="64" rx="9" stroke-width="2" class="cell-em link-green"/>
        <text x="615" y="50" text-anchor="middle" font-weight="bold">effect 托管</text>
        <text x="615" y="70" text-anchor="middle" font-size="11" class="dim">卸载自动回收</text>
        <text x="615" y="86" text-anchor="middle" font-size="11" class="dim">热替换不留残渣</text>
        <g stroke-width="1.8" marker-end="url(#a08)" class="link">
          <line x1="175" y1="62" x2="196" y2="62"/>
          <line x1="345" y1="62" x2="366" y2="62"/>
          <line x1="515" y1="62" x2="536" y2="62"/>
        </g>
        <text x="30" y="126" font-size="11" class="dim">你只负责第三步——加载顺序、配置校验、卸载清理、热替换，框架全兜住了。</text>
      </g>
    </svg>
    <figcaption>图 8：一个插件从声明到生效——配置校验、注册、生命周期托管</figcaption>
  </figure>

## 下一步：把插件发出去

  - **打包成可安装包**：官方提供了打包与安装指南，让插件以 npm 包的形式交付；
- **打上话题标签**：给插件仓库加上 `dsh-plugin` 话题，社区就能搜到你；
- **确认加载链路**：用 `dsh --profile web --dump-config` 查看你的插件是被哪一层 patch 插进来的。

::: tip
写 dsh 插件的心智模型一句话就够：**你只管往 `ctx` 上挂东西，剩下的——加载顺序、配置校验、卸载清理、热替换——框架全包了。**
:::

插件会写了，但一个能读写文件、跑命令的插件本身就很危险。下一篇：**权限与审批——谁允许它动手**。
