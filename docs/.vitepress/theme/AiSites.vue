<script setup>
import { ref, computed } from 'vue'
import { sites, categories, lastVerified } from './ai-sites.js'

const q = ref('')
const cat = ref('all')
const lang = ref('all')
const access = ref('all')

const countBy = (fn) => sites.filter(fn).length

const filtered = computed(() => {
  const kw = q.value.trim().toLowerCase()
  return sites.filter((s) => {
    if (cat.value !== 'all' && s.cat !== cat.value) return false
    if (lang.value !== 'all' && s.lang !== lang.value) return false
    if (access.value !== 'all' && s.access !== access.value) return false
    if (kw && !`${s.name} ${s.note} ${s.url}`.toLowerCase().includes(kw)) return false
    return true
  })
})

const groups = computed(() => {
  const map = new Map()
  for (const s of filtered.value) {
    if (!map.has(s.cat)) map.set(s.cat, [])
    map.get(s.cat).push(s)
  }
  return categories.filter((c) => map.has(c.key)).map((c) => ({ ...c, list: map.get(c.key) }))
})

const hasFilter = computed(
  () => q.value || cat.value !== 'all' || lang.value !== 'all' || access.value !== 'all'
)

function reset() {
  q.value = ''
  cat.value = 'all'
  lang.value = 'all'
  access.value = 'all'
}

const pretty = (u) => u.replace(/^https?:\/\//, '').replace(/\/$/, '')
</script>

<template>
  <div class="ais">
    <div class="ais-bar">
      <input
        v-model="q"
        class="ais-search"
        type="search"
        placeholder="搜索站点名、说明或域名…"
        aria-label="搜索站点"
      />
      <button v-if="hasFilter" class="ais-reset" type="button" @click="reset">清空条件</button>
    </div>

    <div class="ais-tabs">
      <button :class="['ais-tab', { on: cat === 'all' }]" type="button" @click="cat = 'all'">
        全部 {{ sites.length }}
      </button>
      <button
        v-for="c in categories"
        :key="c.key"
        :class="['ais-tab', { on: cat === c.key }]"
        type="button"
        @click="cat = c.key"
      >
        {{ c.label }} {{ countBy((s) => s.cat === c.key) }}
      </button>
    </div>

    <div class="ais-tabs sub">
      <span class="ais-label">语言</span>
      <button :class="['ais-tab sm', { on: lang === 'all' }]" type="button" @click="lang = 'all'">不限</button>
      <button :class="['ais-tab sm', { on: lang === 'zh' }]" type="button" @click="lang = 'zh'">中文</button>
      <button :class="['ais-tab sm', { on: lang === 'en' }]" type="button" @click="lang = 'en'">英文</button>
      <span class="ais-label ml">访问</span>
      <button :class="['ais-tab sm', { on: access === 'all' }]" type="button" @click="access = 'all'">不限</button>
      <button :class="['ais-tab sm', { on: access === 'direct' }]" type="button" @click="access = 'direct'">
        国内直连
      </button>
      <button :class="['ais-tab sm', { on: access === 'proxy' }]" type="button" @click="access = 'proxy'">
        需代理
      </button>
    </div>

    <p class="ais-count">
      命中 {{ filtered.length }} 个站点<span v-if="lastVerified"> · 最近核实 {{ lastVerified }}</span>
    </p>

    <div v-if="!filtered.length" class="ais-empty">
      没有匹配的站点。换个关键词，或者点「清空条件」。
    </div>

    <section v-for="g in groups" :key="g.key" class="ais-group">
      <h3 class="ais-h3">
        {{ g.label }}
        <span class="ais-desc">{{ g.desc }}</span>
      </h3>
      <div class="ais-grid">
        <a
          v-for="s in g.list"
          :key="s.url"
          class="ais-card"
          :href="s.url"
          target="_blank"
          rel="noopener"
        >
          <span class="ais-head">
            <span class="ais-name">{{ s.name }}</span>
            <span :class="['ais-tag', s.access === 'proxy' ? 'warn' : 'ok']">
              {{ s.access === 'proxy' ? '需代理' : '直连' }}
            </span>
          </span>
          <span class="ais-note">{{ s.note }}</span>
          <span class="ais-url">{{ pretty(s.url) }}</span>
        </a>
      </div>
    </section>
  </div>
</template>

<style scoped>
.ais {
  margin: 26px 0 10px;
}
.ais .ais-bar {
  display: flex;
  gap: 10px;
  align-items: center;
}
.ais .ais-search {
  flex: 1;
  min-width: 0;
  padding: 9px 12px;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-size: 14px;
}
.ais .ais-search:focus {
  outline: none;
  border-color: var(--vp-c-brand-1);
}
.ais .ais-reset {
  padding: 9px 12px;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  font-size: 13px;
  cursor: pointer;
  white-space: nowrap;
}
.ais .ais-reset:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
.ais .ais-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-top: 12px;
}
.ais .ais-tabs.sub {
  margin-top: 8px;
}
.ais .ais-label {
  font-size: 12px;
  color: var(--vp-c-text-3);
}
.ais .ais-label.ml {
  margin-left: 10px;
}
.ais .ais-tab {
  padding: 5px 11px;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  background: transparent;
  color: var(--vp-c-text-2);
  font-size: 13px;
  line-height: 1.5;
  cursor: pointer;
  transition: border-color 0.18s, color 0.18s, background 0.18s;
}
.ais .ais-tab.sm {
  font-size: 12px;
  padding: 3px 9px;
}
.ais .ais-tab:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
.ais .ais-tab.on {
  background: var(--vp-c-brand-soft);
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}
.ais .ais-count {
  margin: 14px 0 0;
  font-size: 13px;
  color: var(--vp-c-text-3);
}
.ais .ais-empty {
  margin-top: 20px;
  padding: 22px;
  text-align: center;
  border: 1px dashed var(--vp-c-divider);
  border-radius: 10px;
  color: var(--vp-c-text-3);
  font-size: 14px;
}
.ais .ais-group {
  margin-top: 26px;
}
.ais .ais-h3 {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 10px;
  margin: 0 0 12px;
  padding: 0 0 8px;
  border-top: none;
  border-bottom: 1px solid var(--vp-c-divider);
  font-size: 15px;
  font-weight: 600;
  color: var(--vp-c-text-1);
}
.ais .ais-desc {
  font-size: 12px;
  font-weight: 400;
  color: var(--vp-c-text-3);
}
.ais .ais-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}
@media (min-width: 640px) {
  .ais .ais-grid {
    grid-template-columns: 1fr 1fr;
  }
}
.ais .ais-card {
  display: flex;
  flex-direction: column;
  padding: 12px 14px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft);
  text-decoration: none;
  transition: border-color 0.18s, transform 0.18s;
}
.ais .ais-card:hover {
  border-color: var(--vp-c-brand-1);
  transform: translateY(-1px);
}
.ais .ais-head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}
.ais .ais-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--vp-c-text-1);
}
.ais .ais-tag {
  padding: 1px 7px;
  border-radius: 999px;
  border: 1px solid var(--vp-c-divider);
  font-size: 11px;
  line-height: 1.7;
  color: var(--vp-c-text-3);
}
.ais .ais-tag.warn {
  border-color: var(--vp-c-warning-1);
  color: var(--vp-c-warning-1);
}
.ais .ais-note {
  margin: 7px 0 6px;
  font-size: 13px;
  line-height: 1.65;
  color: var(--vp-c-text-2);
}
.ais .ais-url {
  font-family: var(--vp-font-family-mono);
  font-size: 12px;
  color: var(--vp-c-text-3);
  word-break: break-all;
}
</style>
