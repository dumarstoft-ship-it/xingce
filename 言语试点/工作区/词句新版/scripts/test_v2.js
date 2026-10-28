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
  const hasZ = await page.evaluate(() => DATA.some(a => (a.z || []).length));
  const pilotTotal = await page.evaluate(z => DATA.filter(a => z ? (a.z || []).length : a.pilot).length, hasZ);
  assert(pilotN === pilotTotal, `首次打开只列${hasZ ? '做了主旨题' : '新版'}的文章（${pilotN}/${pilotTotal}）`);
  if (hasZ) assert(await page.$$eval('.zcard', els => els.length) > 0, '首次打开停在主旨理解，有题卡');
  // 先到第一篇有新版遮词句的文章（有主旨题的优先），切到遮词句
  await page.evaluate(() => { mode = "word"; saveUi(); const l = ordered(); const a = l.find(x => (x.q || []).length && (x.z || []).length) || l.find(x => (x.q || []).length); if (a) openArticle(a.id); });
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
  // 切换模式：主旨理解
  assert(!(await page.$('[data-mode="sent"]')), '没有遮点题句模式了');
  if (await page.evaluate(() => (byId[current].z || []).length)) {
    await page.click('[data-mode="zz"]');
    const nz = await page.evaluate(() => byId[current].z.length);
    assert(await page.$$eval('.zcard', els => els.length) === nz, `切到主旨理解，有 ${nz} 张题卡`);
    assert(await page.$$eval('.zcard .zpass', els => els.length) === nz && await page.$$eval('.zcard .zorig', els => els.length) === 0, '答之前只给截好的题干，不给原文');
    const nh = await page.evaluate(() => new Set(byId[current].z.flatMap(z => z.hide || [])).size);
    assert(await page.$$eval('.zhide', els => els.length) === nh, `会露答案的 ${nh} 段先收起`);
    const za = await page.evaluate(() => byId[current].z[0].answer);
    await (await page.$$('.zcard:not(.done) .opts button'))[za].click();
    const left = await page.evaluate(() => { const s = st(current); return new Set(byId[current].z.filter(z => s.zans[z.id] == null).flatMap(z => z.hide || [])).size; });
    assert(await page.$$eval('.zhide', els => els.length) === left, '做完那道题，为它收起的段落展开');
    assert(await page.$$eval('.zcard.done .res .ok', els => els.length) === 1, '主旨题选对显示"选对了"');
    assert(await page.$$eval('.zcard.done .zorig', els => els.length) === 1, '答完题干换成原文对照');
    const dels = await page.evaluate(() => byId[current].z[0].diff.filter(d => d[0] === '-').length);
    assert(await page.$$eval('.zcard.done .zorig del', els => els.length) === dels, `原文对照里标出命题人删去的 ${dels} 处`);
    await page.screenshot({ path: shots + '/v2_3b_zz.png', fullPage: true });
    if (nz > 1) {
      await page.keyboard.press(' ');
      const zb = await page.evaluate(() => byId[current].z[1].answer);
      await page.keyboard.press('ABCD'[zb === 0 ? 1 : 0]);
      assert(await page.$$eval('.zcard.done .res .bad', els => els.length) === 1, '空格跳到下一题、按字母键作答，选错显示答案');
    }
  }
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
  assert(/词句题答对/.test(statText), '我的记录有词句题统计');
  if (hasZ) assert(/主旨题答对/.test(statText) && !/点题句/.test(statText), '我的记录有主旨题统计，没有点题句了');
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
  // 换了新版本：接着上次读到的那篇往后，停在第一篇还没做完的主旨题，筛选不变
  if (hasZ) {
    const c2 = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    const p2 = await c2.newPage();
    p2.on('pageerror', e => errors.push('pageerror: ' + e.message));
    await p2.goto('file://' + file); await p2.waitForSelector('article');
    const [x, y] = await p2.evaluate(() => { const l = sorted(DATA.filter(a => (a.z || []).length)); return [l[0].id, l[1].id]; });
    await p2.evaluate(x => {
      const s = {}; s[x] = { open: {}, tags: {}, words: "", judg: {}, zans: Object.fromEntries(byId[x].z.map(z => [z.id, z.answer])) };
      localStorage.setItem(KEY, JSON.stringify(s));
      localStorage.setItem(KEY + ':ui', JSON.stringify({ order: 'theme', src: 'all', cur: x, mode: 'word', ver: 'old' }));
    }, x);
    await p2.reload(); await p2.waitForSelector('article');
    const r = await p2.evaluate(() => [current, mode, srcFilter]);
    assert(r[0] === y && r[1] === 'zz' && r[2] === 'all', `换新版本后接着往下：停在下一篇没做的主旨题，筛选不变（${r.join(', ')}）`);
    await c2.close();
  }
  // 手机宽度
  const m = await ctx.newPage(); await m.setViewportSize({ width: 390, height: 844 });
  await m.goto('file://' + file + '#' + qid); await m.waitForSelector('article');
  const overflow = await m.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  assert(!overflow, '手机宽度没有横向滚动');
  await m.screenshot({ path: shots + '/v2_5_mobile.png' });
  assert(errors.length === 0, '无报错、无外部请求' + (errors.length ? '：' + errors.join(' | ') : ''));
  await browser.close();
})();
