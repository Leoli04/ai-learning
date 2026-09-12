const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  const URL = 'http://127.0.0.1:5180/ai-learning/ai-basics/02-transformer-training';
  const OUT = 'F:/lixiaofei/WorkBuddy/技术/ai-learning/shots';
  try {
    // 亮主题
    const ctx1 = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
    const p1 = await ctx1.newPage();
    await p1.goto(URL, { waitUntil: 'networkidle' });
    await p1.waitForTimeout(1200);
    // 滚到第一个 tip 容器
    const tip = p1.locator('.vp-doc .tip').first();
    await tip.scrollIntoViewIfNeeded();
    await p1.evaluate(() => window.scrollBy(0, -120));
    await p1.waitForTimeout(400);
    await p1.screenshot({ path: `${OUT}/02-tip-light.png` });
    console.log('OK light');

    // 暗主题
    const ctx2 = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
    const p2 = await ctx2.newPage();
    await p2.addInitScript(() => { try { localStorage.setItem('vitepress-theme-appearance','dark'); } catch(e){} });
    await p2.goto(URL, { waitUntil: 'networkidle' });
    await p2.waitForTimeout(1200);
    const tip2 = p2.locator('.vp-doc .tip').first();
    await tip2.scrollIntoViewIfNeeded();
    await p2.evaluate(() => window.scrollBy(0, -120));
    await p2.waitForTimeout(400);
    await p2.screenshot({ path: `${OUT}/02-tip-dark.png` });
    console.log('OK dark');
  } finally {
    await browser.close();
  }
})().catch(e => { console.error(e.message); process.exit(1); });