// 浏览器实测新版网页：node test_v2.js <网页绝对路径> <截图目录>
const { chromium } = require('playwright');
const assert = (c, m) => { if (!c) { console.error('FAIL ' + m); process.exitCode = 1; } else console.log('ok   ' + m); };
(async () => {
  const file = process.argv[2], shots = process.argv[3] || '/tmp';
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => chromium.launch());
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  page.on('request', r => { if (!r.url().startsWith('file:')) errors.push('external request: ' + r.url()); });
  await page.goto('file://' + file);
  await page.waitForSelector('article');
  const pilotN = await page.$$eval('.item', els => els.length);
  const pilotTotal = await page.evaluate(() => DATA.filter(a => a.pilot).length);
  assert(pilotN === pilotTotal, `首次打开只列新版文章（${pilotN}/${pilotTotal}）`);
  // 先到第一篇有新版遮词句的文章
  await page.evaluate(() => { const a = ordered().find(x => (x.q || []).length); if (a) openArticle(a.id); });
  await page.waitForSelector('article');
  const qid = await page.evaluate(() => current);
  const nq = await page.evaluate(() => byId[current].q.length);
  const nb = await page.evaluate(() => byId[current].q.reduce((s, q) => s + q.blanks.length, 0));
  assert(await page.$$eval('button.blank', els => els.length) === nb, `空格数 = ${nb}`);
  await page.screenshot({ path: shots + '/v2_1_open.png' });
  // 第一处：点空格，按键选正确项
  await page.click('button.blank');
  assert(await page.$$eval('.qcard:not([hidden]) .opts button', els => els.length) === 4, '点空格出现 4 个选项');
  const ans0 = await page.evaluate(() => byId[current].q[0].answer);
  await page.keyboard.press('ABCD'[ans0]);
  assert(await page.$$eval('.qcard .res .ok', els => els.length) === 1, '按字母键选对，显示"选对了"');
  // 第二处：点错误选项
  await page.click('button.blank');
  const card2 = await page.$('.qcard:not([hidden]) .opts button:not([disabled])');
  const wrongIdx = await page.evaluate(() => { const q = byId[current].q.find(q => !st(current).qans.hasOwnProperty(q.id)); return q.answer === 0 ? 1 : 0; });
  const btns = await page.$$('.qcard:not([hidden]) .opts button:not([disabled])');
  await btns[wrongIdx].click();
  assert(await page.$$eval('.qcard .res .bad', els => els.length) === 1, '选错显示"选了X，原文是Y"');
  await page.screenshot({ path: shots + '/v2_2_answered.png' });
  // 空格键打开下一处，再"不选了"
  await page.keyboard.press(' ');
  const skip = await page.$('.qcard:not([hidden]) .linkish');
  if (skip) await skip.click();
  const answered = await page.evaluate(() => Object.keys(st(current).qans).length);
  assert(answered === Math.min(3, nq), `已作答 ${answered} 题`);
  // 政治常识题
  const items = await page.evaluate(() => (byId[current].items || []).map(x => x.type));
  for (let i = 0; i < items.length; i++) {
    const box = (await page.$$('section.block .judg'))[i];
    if (items[i] === '判断') { await (await box.$('.row button')).click(); }
    else if (items[i] === '单选') { await (await box.$$('.opts button'))[0].click(); }
    else { const bs = await box.$$('.opts button'); await bs[0].click(); await bs[2].click(); await (await box.$('.submit')).click(); }
  }
  const iqa = await page.evaluate(() => Object.keys(st(current).iqa).length);
  assert(iqa === items.length, `政治常识题作答 ${iqa}/${items.length}`);
  await page.screenshot({ path: shots + '/v2_3_items.png', fullPage: true });
  // 切换模式
  await page.click('[data-mode="sent"]');
  assert(await page.$$eval('button.tape', els => els.length) > 0, '切到遮点题句有灰条');
  const hasOld = await page.$('[data-mode="wold"]');
  if (hasOld) { await hasOld.click(); assert(await page.$$eval('button.blank', els => els.length) > 0, '旧版遮词对照可用'); }
  await page.click('[data-mode="word"]');
  // 刷新看记录还在
  await page.reload(); await page.waitForSelector('article');
  assert(await page.evaluate(() => current) === qid, '刷新后停在同一篇');
  const marks = await page.$$eval('mark.wrev', els => els.length);
  assert(marks >= 3, `刷新后揭开的空仍是原文（${marks} 处）`);
  // 我的记录
  await page.click('#go-stats');
  const statText = await page.$eval('.stats', e => e.innerText);
  assert(/新版词句题答对/.test(statText), '我的记录有新版词句题统计');
  assert(await page.$$eval('.review .it', els => els.length) >= 1, '选错的题进了复习列表');
  await page.screenshot({ path: shots + '/v2_4_stats.png' });
  // 全部 / 常识 筛选和旧文章
  await page.click('[data-src="all"]');
  assert(await page.$$eval('.item', els => els.length) === 151, '"全部"列出 151 篇');
  // 全部做成新版以后就没有旧文章可点了，这项跳过
  if (await page.$('.item:not(:has(.badge))')) {
    await page.click('.item:not(:has(.badge))');
    await page.waitForSelector('article');
    assert(await page.$$eval('button.blank, button.tape', els => els.length) > 0, '未做新版的文章照旧可用');
  } else console.log('skip 没有未做新版的文章');
  // 手机宽度
  const m = await ctx.newPage(); await m.setViewportSize({ width: 390, height: 844 });
  await m.goto('file://' + file + '#' + qid); await m.waitForSelector('article');
  const overflow = await m.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  assert(!overflow, '手机宽度没有横向滚动');
  await m.screenshot({ path: shots + '/v2_5_mobile.png' });
  assert(errors.length === 0, '无报错、无外部请求' + (errors.length ? '：' + errors.join(' | ') : ''));
  await browser.close();
})();
