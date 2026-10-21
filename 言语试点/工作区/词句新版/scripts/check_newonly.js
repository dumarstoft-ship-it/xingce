// 抽查铺开批次里的文章（有新版遮词句、文末仍是旧判断题）
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await b.newPage(); const errs = [];
  page.on('pageerror', e => errs.push(String(e)));
  await page.goto('file://' + process.argv[2]);
  const ids = ['20251214_30120296', 'nf20251009_10149560', 'nf20260429_10169309', '20260911_30180489', 'nf20260914_10181306'];
  for (const id of ids) {
    await page.evaluate(id => openArticle(id), id);
    const r = await page.evaluate(id => {
      const a = byId[id];
      return { nq: a.q.length, nb: a.q.reduce((s, q) => s + q.blanks.length, 0), items: (a.items || []).length,
        blanks: document.querySelectorAll('button.blank').length, judg: document.querySelectorAll('.judg').length,
        title: a.title };
    }, id);
    await page.click('button.blank');
    const nopt = await page.$$eval('.qcard:not([hidden]) .opts button', els => els.length);
    console.log(id, r.title, `题 ${r.nq}，空 ${r.nb}，页面空格 ${r.blanks}，选项 ${nopt}，新题 ${r.items}，旧判断题块 ${r.judg}`);
  }
  console.log(errs.length ? '报错：' + errs.join(' | ') : '无报错');
  await b.close();
})();
