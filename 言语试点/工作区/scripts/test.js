const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const file = process.argv[2];
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => chromium.launch());
  const page = await browser.newPage({ viewport: { width: 1280, height: 860 } });
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  page.on('request', r => { if (!r.url().startsWith('file:')) errors.push('external request: ' + r.url()); });
  await page.goto('file://' + file + (process.argv[3] ? '#' + process.argv[3] : ''));
  await page.waitForSelector('article');
  const navItems = await page.$$eval('.item', els => els.length);
  const tapes = await page.$$eval('button.tape', els => els.length);
  await page.screenshot({ path: file.replace(/\.html$/, '_1.png') });
  // reveal first mask, tag it, answer a judgment if any
  await page.click('button.tape');
  await page.click('.chips button:nth-child(2)');
  const tagged = await page.$$eval('.chips button[aria-pressed="true"]', els => els.length);
  const jbtn = await page.$('.judg .row button');
  if (jbtn) await jbtn.click();
  await page.fill('#words', '测试措辞');
  await page.waitForTimeout(700);
  await page.screenshot({ path: file.replace(/\.html$/, '_2.png'), fullPage: false });
  // reload to check persistence
  await page.reload();
  await page.waitForSelector('article');
  const persisted = await page.$$eval('mark.rev', els => els.length);
  const words = await page.$eval('#words', e => e.value);
  // keyboard nav
  await page.keyboard.press('ArrowRight');
  const title2 = await page.$eval('h1', e => e.textContent);
  await page.click('#go-stats');
  await page.waitForSelector('.stats');
  await page.screenshot({ path: file.replace(/\.html$/, '_3.png') });
  await page.click('#go-1310');
  await page.click('[data-order="date"]');
  await page.click('[data-src="南方日报"]');
  const nfCount = await page.$$eval('.item', els => els.length);
  await page.click('[data-src="常识"]');
  const csCount = await page.$$eval('.item', els => els.length);
  const csGroups = await page.$$eval('.grp', els => els.map(e => e.textContent));
  let csHead = null, csJudg = 0, csTapes = 0;
  if (csCount) {
    await page.click('.item');
    await page.waitForSelector('article');
    csHead = await page.$$eval('section.block h2', els => els.map(e => e.textContent).join(' | '));
    csJudg = await page.$$eval('.judg', els => els.length);
    csTapes = await page.$$eval('button.tape', els => els.length);
    const jb = await page.$('.judg .row button'); if (jb) await jb.click();
    await page.screenshot({ path: file.replace(/\.html$/, '_5.png'), fullPage: true });
    await page.click('#go-stats'); await page.waitForSelector('.stats');
  }
  const statLabels = await page.$$eval('.stat .l', els => els.map(e => e.textContent));
  // dark mode + narrow
  const p2 = await browser.newPage({ viewport: { width: 400, height: 800 }, colorScheme: 'dark' });
  await p2.goto('file://' + file);
  await p2.waitForSelector('article');
  const overflow = await p2.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  await p2.screenshot({ path: file.replace(/\.html$/, '_4.png') });
  console.log(JSON.stringify({ navItems, tapes, tagged, persisted, words, title2, nfCount, csCount, csGroups, csHead, csJudg, csTapes, statLabels, overflow, errors }, null, 1));
  await browser.close();
})();
