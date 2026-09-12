const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true, channel: 'msedge' });
  try {
    const ctx1 = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
    const page1 = await ctx1.newPage();
    await page1.goto('http://127.0.0.1:5180/ai-learning/deepseek-harness/02-everything-is-a-plugin', { waitUntil: 'networkidle' });
    await page1.waitForTimeout(1200);
    // 滚动到第一个 SVG（figure 1）
    const handle1 = await page1.locator('figure.figure').nth(0).elementHandle();
    await handle1.scrollIntoViewIfNeeded();
    await page1.evaluate(() => window.scrollBy(0, -80));
    await page1.waitForTimeout(400);
    await page1.screenshot({ path: 'F:/lixiaofei/WorkBuddy/技术/ai-learning/docs/02-fig1-light.png' });
    console.log('OK fig1 light');

    // 图 2
    const handle2 = await page1.locator('figure.figure').nth(1).elementHandle();
    await handle2.scrollIntoViewIfNeeded();
    await page1.evaluate(() => window.scrollBy(0, -80));
    await page1.waitForTimeout(400);
    await page1.screenshot({ path: 'F:/lixiaofei/WorkBuddy/技术/ai-learning/docs/02-fig2-light.png' });
    console.log('OK fig2 light');

    // 图 3
    const handle3 = await page1.locator('figure.figure').nth(2).elementHandle();
    await handle3.scrollIntoViewIfNeeded();
    await page1.evaluate(() => window.scrollBy(0, -80));
    await page1.waitForTimeout(400);
    await page1.screenshot({ path: 'F:/lixiaofei/WorkBuddy/技术/ai-learning/docs/02-fig3-light.png' });
    console.log('OK fig3 light');
    await ctx1.close();

    // 暗主题
    const ctx2 = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
    const page2 = await ctx2.newPage();
    await page2.addInitScript(() => { try { localStorage.setItem('vitepress-theme-appearance','dark'); } catch(e){} });
    await page2.goto('http://127.0.0.1:5180/ai-learning/deepseek-harness/02-everything-is-a-plugin', { waitUntil: 'networkidle' });
    await page2.waitForTimeout(1200);
    const dh1 = await page2.locator('figure.figure').nth(1).elementHandle();
    await dh1.scrollIntoViewIfNeeded();
    await page2.evaluate(() => window.scrollBy(0, -80));
    await page2.waitForTimeout(400);
    await page2.screenshot({ path: 'F:/lixiaofei/WorkBuddy/技术/ai-learning/docs/02-fig2-dark.png' });
    console.log('OK fig2 dark');
    await ctx2.close();
  } finally {
    await browser.close();
  }
})().catch(e => { console.error(e.message); process.exit(1); });
