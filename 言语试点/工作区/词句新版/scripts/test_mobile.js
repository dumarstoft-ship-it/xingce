// 手机实测：node test_mobile.js <网页绝对路径> <截图目录>
const { chromium } = require('playwright');
const ok = [], bad = [];
function assert(c, m) { (c ? ok : bad).push(m); console.log((c ? 'ok   ' : 'FAIL ') + m); }
(async () => {
  const [file, out] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  const errs = []; page.on('pageerror', e => errs.push(String(e)));
  page.on('request', r => { if (!r.url().startsWith('file:')) errs.push('外部请求 ' + r.url()); });
  await page.goto('file://' + file);
  await page.waitForSelector('article');
  const shot = n => page.screenshot({ path: `${out}/${n}.png` });
  assert(!(await page.isVisible('nav')), '打开时目录收起，不占屏幕');
  assert(await page.isVisible('#mbar'), '顶上有窄栏');
  await shot('m1_open');
  // 目录抽屉
  await page.tap('#mbar .mb-menu');
  assert(await page.isVisible('nav'), '点“目录”打开抽屉');
  const navH = await page.evaluate(() => document.querySelector('nav').getBoundingClientRect().height);
  assert(navH >= 840, '抽屉占满屏幕');
  await shot('m2_nav');
  // 返回键关抽屉
  await page.goBack();
  await page.waitForTimeout(300);
  assert(!(await page.isVisible('nav')) && page.url().startsWith('file:'), '按返回键关掉抽屉，页面还在');
  // 从抽屉选一篇有语句填空的
  await page.tap('#mbar .mb-menu');
  await page.tap('[data-src="all"]'); await page.waitForTimeout(200);
  const id = await page.evaluate(() => (DATA.find(a => (a.z || []).length && a.q.some(q => q.kind === '语句填空') && a.q.some(q => q.kind === '选词填空') && a.q.length >= 5) || DATA.find(a => a.q.some(q => q.kind === '语句填空') && a.q.some(q => q.kind === '选词填空') && a.q.length >= 5)).id);
  await page.locator(`.item[href="#${id}"]`).scrollIntoViewIfNeeded();
  await page.tap(`.item[href="#${id}"]`);
  await page.waitForTimeout(300);
  assert(!(await page.isVisible('nav')) && await page.evaluate(id => current === id, id), '在抽屉里点一篇，抽屉收起、打开这篇');
  assert(await page.evaluate(() => window.scrollY === 0), '新打开的文章从顶上开始');
  await page.locator('[data-mode="word"]').tap(); await page.waitForTimeout(200);
  await shot('m3_article');
  // 下一空
  const t0 = await page.textContent('#mbar .mb-next');
  assert(/^下一空 0\/\d+$/.test(t0.trim()), '窄栏显示“下一空 0/N”（' + t0.trim() + '）');
  await page.tap('#mbar .mb-next');
  await page.waitForTimeout(700);
  assert(await page.isVisible('.qsheet'), '点“下一空”弹出选项面板');
  const pos = await page.evaluate(() => {
    const q = sheetCtl.q; const slot = document.querySelector(`button.blank[data-q="${q.id}"]`);
    const r = slot.getBoundingClientRect(), s = document.querySelector('.qsheet').getBoundingClientRect(), m = document.getElementById('mbar').getBoundingClientRect();
    return { top: r.top, bottom: r.bottom, sheetTop: s.top, bar: m.bottom };
  });
  assert(pos.top >= pos.bar && pos.bottom <= pos.sheetTop, `空格露在窄栏和面板之间（${Math.round(pos.top)}–${Math.round(pos.bottom)}，面板顶 ${Math.round(pos.sheetTop)}）`);
  await shot('m4_sheet');
  const nOpt = await page.$$eval('.qsheet .opts button', els => els.length);
  assert(nOpt === 4, '面板里有 4 个选项');
  const h44 = await page.$$eval('.qsheet .opts button', els => els.every(e => e.getBoundingClientRect().height >= 44));
  assert(h44, '选项按钮够大，好点');
  // 选一个
  const ansIdx = await page.evaluate(() => sheetCtl.q.answer);
  await page.locator('.qsheet .opts button').nth(ansIdx === 0 ? 1 : 0).tap();
  await page.waitForTimeout(500);
  const res = await page.textContent('.qsheet .res');
  assert(/原文是/.test(res), '选完面板里显示对错（' + res.trim() + '）');
  assert(await page.isVisible('.qsheet .note'), '面板里显示说明');
  await shot('m5_result');
  const pos2 = await page.evaluate(() => {
    const q = sheetCtl.q; const mk = document.querySelector(`.qcard[data-q="${q.id}"]`).closest('.para').querySelector('mark.wrev');
    const r = mk.getBoundingClientRect(), s = document.querySelector('.qsheet').getBoundingClientRect();
    return { top: r.top, sheetTop: s.top };
  });
  assert(pos2.top > 40 && pos2.top < pos2.sheetTop, '揭开的原文露在面板上方');
  const qid1 = await page.evaluate(() => sheetCtl.q.id);
  assert(await page.evaluate(q => document.querySelector(`.qcard[data-q="${q}"]`).hidden, qid1), '面板开着时，段落下方不再重复一张卡');
  const y0 = await page.evaluate(() => scrollY);
  await page.tap('.qsheet .qs-go');
  await page.waitForTimeout(600);
  assert(!(await page.isVisible('.qsheet')), '点“继续读”收起面板');
  const y1 = await page.evaluate(() => scrollY);
  assert(Math.abs(y1 - y0) < 5, `收起面板时页面不跳（${Math.round(y0)} → ${Math.round(y1)}）`);
  assert(await page.isVisible(`.qcard[data-q="${qid1}"]`), '收起后段落下方留下这题的结果和说明');
  assert(await page.evaluate(() => document.body.style.paddingBottom === ''), '收起后页面底部不留空白');
  const t1 = await page.textContent('#mbar .mb-next');
  assert(/^下一空 1\//.test(t1.trim()), '窄栏进度变成 1/N');
  // 语句填空：选项单列；用返回键关面板
  const sid = await page.evaluate(() => byId[current].q.find(q => q.kind === '语句填空' && st(current).qans[q.id] == null).id);
  await page.locator(`button.blank[data-q="${sid}"]`).first().tap();
  await page.waitForTimeout(700);
  const cols = await page.$eval('.qsheet .opts', e => getComputedStyle(e).gridTemplateColumns.split(' ').length);
  assert(cols === 1, '语句填空的长选项单列排');
  await shot('m6_long');
  await page.goBack(); await page.waitForTimeout(300);
  assert(!(await page.isVisible('.qsheet')) && page.url().startsWith('file:'), '按返回键收起面板，页面还在');
  // 主旨理解（这篇有主旨题时）
  const nz = await page.evaluate(() => (byId[current].z || []).length);
  if (nz) {
    await page.locator('[data-mode="zz"]').tap(); await page.waitForTimeout(200);
    const t2 = await page.textContent('#mbar .mb-next');
    assert(t2.trim() === `下一题 0/${nz}`, '切到主旨理解，窄栏变成“下一题 0/N”（' + t2.trim() + '）');
    await page.tap('#mbar .mb-next'); await page.waitForTimeout(700);
    const top = await page.evaluate(() => document.querySelector('.zcard:not(.done)').getBoundingClientRect().top);
    assert(top >= 40 && top < 140, `点“下一题”跳到题卡，题卡顶在窄栏下面（${Math.round(top)}）`);
    await shot('m7_zz');
    await page.locator('.zcard:not(.done) .opts button').first().tap(); await page.waitForTimeout(400);
    assert(await page.$$eval('.zcard.done .zorig', els => els.length) === 1, '主旨题答完显示原文对照');
    await shot('m7b_zz_done');
  } else console.log('skip 这篇没有主旨题');
  // 读到一半，从抽屉换一篇：新的一篇要从顶上开始
  await page.evaluate(() => window.scrollTo(0, 1500)); await page.waitForTimeout(200);
  const other = await page.evaluate(() => { const l = ordered(); const i = l.findIndex(x => x.id === current); return l[(i + 1) % l.length].id; });
  await page.tap('#mbar .mb-menu'); await page.waitForTimeout(200);
  await page.locator(`.item[href="#${other}"]`).scrollIntoViewIfNeeded();
  await page.tap(`.item[href="#${other}"]`); await page.waitForTimeout(700);
  assert(await page.evaluate(o => current === o && scrollY === 0, other), '读到一半从抽屉换一篇，新的一篇从顶上开始');
  await page.evaluate(id => openArticle(id), id); await page.waitForTimeout(200);
  // 文末
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight)); await page.waitForTimeout(200);
  await shot('m8_end');
  // 我的记录
  await page.tap('#mbar .mb-menu'); await page.tap('#go-stats'); await page.waitForTimeout(700);
  assert(!(await page.isVisible('nav')) && await page.isVisible('.stats'), '从抽屉进“我的记录”');
  assert(await page.evaluate(() => scrollY === 0), '“我的记录”从顶上开始');
  assert((await page.textContent('#mbar .mb-title')).trim() === '我的记录' && (await page.textContent('#mbar .mb-next')).trim() === '回到文章', '记录页窄栏有“回到文章”');
  await shot('m9_stats');
  await page.tap('#mbar .mb-next'); await page.waitForTimeout(300);
  assert(await page.isVisible('article'), '点“回到文章”回到刚才那篇');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1);
  assert(!overflow, '没有横向滚动');
  // 暗色
  const dark = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: 'dark' });
  const dp = await dark.newPage(); await dp.goto('file://' + file + '#' + id); await dp.waitForSelector('article');
  await dp.locator('[data-mode="word"]').tap(); await dp.waitForTimeout(200);
  await dp.locator('button.blank').first().tap(); await dp.waitForTimeout(600);
  await dp.screenshot({ path: `${out}/m10_dark.png` });
  assert(errs.length === 0, '无报错、无外部请求' + (errs.length ? '：' + errs.join(' | ') : ''));
  console.log(`\n${ok.length} 项通过，${bad.length} 项失败`);
  await b.close();
  process.exit(bad.length ? 1 : 0);
})();
