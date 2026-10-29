"use strict";
const DATA = JSON.parse(document.getElementById("data").textContent);
const REF = JSON.parse(document.getElementById("ref1310").textContent);
const META = JSON.parse(document.getElementById("meta").textContent);
const KEY = "gaiju-v1";
let store = {};
try { store = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { store = {}; }
function save() { try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {} }
function st(id) {
  const s = store[id] || (store[id] = { open: {}, tags: {}, words: "", judg: {} });
  s.wopen = s.wopen || {}; s.wconf = s.wconf || {}; s.whit = s.whit || {};
  s.qans = s.qans || {}; s.iqa = s.iqa || {}; s.zans = s.zans || {};
  return s;
}

let order = "theme", srcFilter = "all", query = "", current = null, view = "article", mode = "word", resumeZ = false;
try {
  const u = JSON.parse(localStorage.getItem(KEY + ":ui") || "{}");
  order = u.order || order; srcFilter = u.src || srcFilter; current = u.cur || null;
  if (u.mode === "word" || u.mode === "zz" || u.mode === "wold") mode = u.mode;
  else if (u.mode === "sent") mode = "zz";
  // 换了新版本：有主旨题时列出做了主旨题的文章，停在主旨理解，从上次读到的那篇往后找还没做的主旨题
  if (u.ver !== META.ver && DATA.some(a => (a.z || []).length)) { if (!u.ver || srcFilter !== "all") srcFilter = "主旨"; mode = "zz"; resumeZ = true; }
  else if (u.ver !== META.ver && DATA.some(a => a.pilot)) { srcFilter = "试点"; mode = "word"; current = null; }
} catch (e) {}
function saveUi() { try { localStorage.setItem(KEY + ":ui", JSON.stringify({ order, src: srcFilter, cur: current, mode, ver: META.ver })); } catch (e) {} }

const byId = Object.fromEntries(DATA.map(a => [a.id, a]));
const LETTERS = "ABCD";
// 手机：目录收进抽屉，顶上一条窄栏；点空格从底部弹出选项
const PHONE = matchMedia("(max-width: 760px)");
function isPhone() { return PHONE.matches; }
const SMOOTH = matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";
function circ(n) { return n >= 1 && n <= 20 ? String.fromCharCode(0x2460 + n - 1) : "(" + n + ")"; }
function masksOf(a) { return a.paras.flat().filter(x => x.m); }
function hasQ(a) { return (a.q || []).length > 0; }
function hasZ(a) { return (a.z || []).length > 0; }
// 标题先遮住：主旨理解里，写了 htitle 的题没做完之前，顶上、目录、手机窄栏、我的记录都不露文章标题
function titleHidden(a) {
  if (mode !== "zz" || !hasZ(a)) return false;
  const s = store[a.id];
  if (s && s.tshow) return false;
  return a.z.some(z => z.htitle && !(s && s.zans && s.zans[z.id] != null));
}
function titleOf(a) { return titleHidden(a) ? "（标题先遮住）" : a.title; }
function statusOf(a) {
  const s = store[a.id]; if (!s) return "";
  if (hasQ(a)) {
    const n = a.q.length, t = a.q.filter(q => s.qans && s.qans[q.id] != null).length;
    const zn = (a.z || []).length, zt = (a.z || []).filter(z => s.zans && s.zans[z.id] != null).length;
    if (t >= n && zt >= zn) return "done";
    return (t || zt || Object.keys(s.tags || {}).length || Object.keys(s.open || {}).length) ? "part" : "";
  }
  const n = masksOf(a).length, t = Object.keys(s.tags || {}).length;
  if (n && t >= n) return "done";
  return (t || Object.keys(s.open || {}).length) ? "part" : "";
}
function visible() {
  const q = query.trim();
  return DATA.filter(a => {
    if (srcFilter === "试点") { if (!a.pilot) return false; }
    else if (srcFilter === "主旨") { if (!hasZ(a)) return false; }
    else if (srcFilter === "常识") { if (a.kind !== "cs") return false; }
    else if (srcFilter !== "all") { if (a.kind === "cs" || a.src !== srcFilter) return false; }
    return !q || (a.title + a.group + a.col).includes(q);
  });
}
function rank(a) { return a.kind === "cs" ? 2 : a.src === "南方日报" ? 1 : 0; }
function sorted(list) {
  if (order === "date") return list.sort((x, y) => x.date.localeCompare(y.date) || x.id.localeCompare(y.id));
  return list.sort((x, y) => rank(x) - rank(y) || x.gidx - y.gidx || x.date.localeCompare(y.date));
}
function ordered() { return sorted(visible().slice()); }
function zLeft(a) { const s = store[a.id]; return (a.z || []).some(z => !(s && s.zans && s.zans[z.id] != null)); }

function renderNav() {
  const list = ordered();
  const box = document.getElementById("navlist");
  box.replaceChildren();
  let last = null;
  for (const a of list) {
    const g = order === "date" ? a.date.slice(0, 7).replace("-", " 年 ") + " 月" : (a.kind === "cs" ? "常识 · " : a.src === "南方日报" ? "南方日报 · " : "") + a.gname;
    if (g !== last) { const h = document.createElement("div"); h.className = "grp"; h.textContent = g; box.append(h); last = g; }
    const it = document.createElement("a");
    it.className = "item"; it.href = "#" + a.id; it.tabIndex = 0;
    if (a.id === current && view === "article") it.setAttribute("aria-current", "true");
    const dot = document.createElement("span"); dot.className = "dot " + statusOf(a);
    const txt = document.createElement("span");
    const t = document.createElement("div"); t.className = "t" + (titleHidden(a) ? " tmasked" : ""); t.textContent = titleOf(a);
    if (hasZ(a)) t.append(el("span", "badge", "主旨"));
    const m = document.createElement("div"); m.className = "m";
    const s = document.createElement("span"); s.className = a.src === "南方日报" ? "nf" : ""; s.textContent = a.src;
    m.append(s, document.createTextNode(" · " + a.col + " · " + a.date.slice(5)));
    txt.append(t, m); it.append(dot, txt);
    it.addEventListener("click", e => { e.preventDefault(); openArticle(a.id); });
    box.append(it);
  }
  const done = DATA.filter(a => statusOf(a) === "done").length;
  const np = DATA.filter(a => a.pilot).length;
  document.getElementById("navstat").textContent = `显示 ${list.length} 篇 · 已读完 ${done} / ${DATA.length}` + (np ? ` · 新版 ${np} 篇` : "");
  document.getElementById("count").textContent = `${DATA.length} 篇`;
  for (const b of document.querySelectorAll("[data-order]")) b.setAttribute("aria-pressed", b.dataset.order === order ? "true" : "false");
  for (const b of document.querySelectorAll("[data-src]")) b.setAttribute("aria-pressed", b.dataset.src === srcFilter ? "true" : "false");
}

function openArticle(id) {
  if (!byId[id]) return;
  closeNav(); closeSheet();
  current = id; view = "article"; saveUi();
  renderArticle(byId[id]); renderNav();
  document.getElementById("main").scrollTop = 0; window.scrollTo(0, 0);
  const cur = document.querySelector('.item[aria-current="true"]'); if (cur) cur.scrollIntoView({ block: "nearest" });
}

function el(tag, cls, text) { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

// 当前文章实际用哪种模式：zz 主旨理解；q 新版遮词句；w 旧版遮词；plain 不遮
function effMode(a) {
  if (mode === "zz") return hasZ(a) ? "zz" : hasQ(a) ? "q" : (a.w || []).length ? "w" : "plain";
  if (mode === "wold") return (a.w || []).length ? "w" : hasQ(a) ? "q" : "plain";
  return hasQ(a) ? "q" : (a.w || []).length ? "w" : "plain";
}

let activeQ = null, activeZ = null;

function renderArticle(a) {
  const s = st(a.id);
  const em = effMode(a);
  closeSheet();
  activeQ = null; activeZ = null;
  const ph = isPhone();
  const main = document.getElementById("main");
  const wrap = el("div", "wrap");
  const how = el("div", "how");
  const legend = el("div", "legend");
  let brief;
  if (em === "q") {
    how.innerHTML = "读到空格，先<b>自己想原文用了什么词、什么句</b>，再点空格看选项、选一个。选完揭开原文和说明。空格前的 ①② 是题号，题号相同的几个空是同一道题，依次填入。";
    const nw = a.q.filter(q => q.kind === "选词填空").length, ns = a.q.length - nw;
    legend.innerHTML = `<span>本篇：选词填空 <b>${nw}</b> 题、语句填空 <b>${ns}</b> 题</span><span>选错的题会收进“我的记录”</span>`;
    brief = `本篇选词填空 ${nw} 题、语句填空 ${ns} 题`;
  } else if (em === "w") {
    how.innerHTML = "读到遮住的词句，先<b>想想自己会怎样接</b>，再选“有把握”或“没把握”揭开。对照原文的措辞和语气，点“对上了”或“没对上”；不必一字不差。";
    legend.innerHTML = "<span><b>有把握却没对上</b>的词会收进“我的记录”，留着重点复习</span>";
    brief = `本篇遮了 ${a.w.length} 处词句`;
  } else if (em === "zz") {
    how.innerHTML = "读到命题人会出题的那几段，先像在考场上一样，<b>只看截好的题干</b>，选一个答案。选完揭开原文：<b>划掉的是命题人删去的</b>，加下划线的是命题人改写或添上的。对照着看，命题人删了哪句、为什么这样配选项。";
    legend.innerHTML = `<span>本篇：主旨类题 <b>${a.z.length}</b> 道</span><span>选错的题会收进“我的记录”</span>`;
    brief = `本篇主旨类题 ${a.z.length} 道`;
  } else {
    how.innerHTML = "这篇还没有出题，先通读。";
    brief = "这篇还没有出题";
  }
  // 手机上说明收起来，只露一行
  let intro = [how, legend];
  if (ph) { const d = el("details", "howd"); d.append(el("summary", "", "怎么做 · " + brief), how, legend); intro = [d]; }
  const art = el("article");
  const meta = el("div", "meta");
  const src = el("span", "src" + (a.src === "南方日报" ? " nf" : ""), a.src);
  meta.append(src, el("span", "", a.col), el("span", "", a.date), el("span", "", a.page || ""));
  const h = titleBox(a, s);
  const by = el("div", "byline");
  if (a.author) by.append(el("span", "", a.author));
  const link = el("a", "", "原文链接（需联网）"); link.href = a.url; link.target = "_blank"; link.rel = "noopener";
  const prog = el("span", "progress"); prog.id = "prog";
  by.append(link, prog);
  const grp = el("div", "group", (a.kind === "cs" ? "考点：" : a.src === "南方日报" ? "覆盖：" : "主题：") + a.group);
  art.append(meta, h, by, grp);
  if (hasZ(a) || hasQ(a) || (a.w || []).length) {
    const mb = el("div", "modebar");
    const seg = el("div", "seg"); seg.setAttribute("role", "group"); seg.setAttribute("aria-label", "练习方式");
    const modes = [];
    if (hasZ(a)) modes.push(["zz", ph ? "主旨 " + a.z.length + " 题" : "主旨理解（" + a.z.length + " 题）"]);
    if (hasQ(a)) modes.push(["word", ph ? "词句 " + a.q.length + " 题" : "遮词句（" + a.q.length + " 题）"]);
    else if ((a.w || []).length) modes.push(["word", ph ? "遮词 " + a.w.length : "遮词句（" + a.w.length + "）"]);
    if (hasQ(a) && (a.w || []).length) modes.push(["wold", ph ? "旧版对照" : "旧版遮词（对照）"]);
    const cur = em === "zz" ? "zz" : em === "q" ? "word" : em === "w" && hasQ(a) ? "wold" : "word";
    for (const [k, name] of modes) {
      const b = el("button", "", name); b.type = "button"; b.dataset.mode = k;
      b.setAttribute("aria-pressed", cur === k ? "true" : "false");
      b.addEventListener("click", () => { if (mode !== k) { mode = k; saveUi(); renderArticle(a); } });
      seg.append(b);
    }
    mb.append(seg);
    art.append(mb);
  }
  const qn = hasQ(a) ? Object.fromEntries(a.q.map((q, i) => [q.id, i + 1])) : {};

  // 主旨理解：出题的那几段换成题卡；会露出答案的段落（如提要）先收起，做完那道题再展开；其余段落照常显示
  const zAt = em === "zz" ? Object.fromEntries(a.z.map((z, i) => [z.from, [z, i + 1]])) : {};
  const hideBy = {};
  if (em === "zz") for (const z of a.z) if (s.zans[z.id] == null) for (const h of z.hide || []) (hideBy[h] = hideBy[h] || []).push(z);
  for (let pi = 0; pi < a.paras.length; pi++) {
    const para = a.paras[pi];
    if (zAt[pi + 1]) { const [z, n] = zAt[pi + 1]; art.append(zCard(a, s, z, n)); pi = z.to - 1; continue; }
    if (hideBy[pi + 1]) { art.append(zHidden(a, s, para, pi, hideBy[pi + 1])); continue; }
    const box = el("div", "para");
    const p = el("p", para.length === 1 && para[0].sub ? "sub" : "");
    p.append(el("span", "pno", "[" + (pi + 1) + "]"));
    const checks = el("div", "checks");
    if (em === "q") renderQPara(a, s, para, pi, p, checks, qn);
    else if (em === "w") renderWordPara(a, s, para, pi, p, checks);
    else p.append(document.createTextNode(paraText(para)));
    box.append(p, checks);
    art.append(box);
  }

  const w = el("section", "block");
  w.append(el("h2", "", "意外的措辞"), el("div", "hint", "读到“换我会写别的”的地方就记下来，攒一批再回看。"));
  const ta = el("textarea"); ta.id = "words"; ta.placeholder = "例：充斥着较量；固守过去的经验"; ta.value = s.words || "";
  let tmr; ta.addEventListener("input", () => { clearTimeout(tmr); tmr = setTimeout(() => { s.words = ta.value; save(); }, 500); });
  w.append(ta);
  art.append(w);

  if ((a.items || []).length) renderItems(a, s, art);
  else if (a.judgments && a.judgments.length) art.append(oldJudgments(a, s, (a.kind === "cs" ? "常识" : "政治理论") + " · 判断题"));

  const tools = el("div", "tools");
  const again = el("button", "", em === "zz" ? "清掉作答，再做一遍" : "重新遮住，再读一遍"); again.type = "button";
  again.addEventListener("click", () => {
    if (em === "q") s.qans = {}; else if (em === "w") s.wopen = {}; else if (em === "zz") { s.zans = {}; s.tshow = false; }
    save(); renderArticle(a); renderNavLite();
  });
  tools.append(again, el("span", "kbd", em === "q" || em === "zz" ? "快捷键：空格 跳到下一题 · A–D 或 1–4 选项 · ← → 上一篇 / 下一篇" : "快捷键：空格 揭开下一处 · ← → 上一篇 / 下一篇"));
  art.append(tools);

  const list = ordered(); const i = list.findIndex(x => x.id === a.id);
  const pager = el("div", "pager");
  const prev = el("button", "", "← 上一篇"); prev.type = "button"; prev.disabled = i <= 0;
  const next = el("button", "", "下一篇 →"); next.type = "button"; next.disabled = i < 0 || i >= list.length - 1;
  prev.addEventListener("click", () => openArticle(list[i - 1].id));
  next.addEventListener("click", () => openArticle(list[i + 1].id));
  pager.append(prev, next);

  wrap.append(...intro, art, pager);
  main.replaceChildren(wrap);
  updateProg(a);
}

function updateProg(a) {
  updateMbar();
  const s = st(a.id); const p = document.getElementById("prog"); if (!p) return;
  const em = effMode(a);
  if (em === "q") {
    const done = a.q.filter(q => s.qans[q.id] != null);
    const ok = done.filter(q => s.qans[q.id] === q.answer).length;
    p.textContent = "词句题已答 " + done.length + " / " + a.q.length + (done.length ? " · 答对 " + ok : "");
    return;
  }
  if (em === "w") { const t = a.w.filter(w => s.whit[w.id] != null).length; p.textContent = "词句已对照 " + t + " / " + a.w.length; return; }
  if (em === "zz") {
    const done = a.z.filter(z => s.zans[z.id] != null);
    const ok = done.filter(z => s.zans[z.id] === z.answer).length;
    p.textContent = "主旨题已答 " + done.length + " / " + a.z.length + (done.length ? " · 答对 " + ok : "");
    return;
  }
  p.textContent = "";
}
function paraText(para) { return para.map(x => x.t != null ? x.t : x.m).join(""); }

// ---------- 新版遮词句 ----------
function renderQPara(a, s, para, pi, p, cards, qn) {
  const full = paraText(para);
  const qs = a.q.filter(q => q.p === pi + 1);
  const bl = [];
  for (const q of qs) q.blanks.forEach((b, bi) => bl.push({ q, b, bi }));
  bl.sort((x, y) => x.b.b - y.b.b);
  let pos = 0;
  const slots = {};
  for (const { q, b, bi } of bl) {
    if (b.b > pos) p.append(document.createTextNode(full.slice(pos, b.b)));
    const slot = el("span", "qslot");
    p.append(slot);
    (slots[q.id] = slots[q.id] || []).push({ slot, text: full.slice(b.b, b.e), bi });
    pos = b.e;
  }
  if (pos < full.length) p.append(document.createTextNode(full.slice(pos)));
  for (const q of qs) {
    const card = el("div", "qcard"); card.dataset.q = q.id; card.hidden = true;
    cards.append(card);
    paintQ(a, s, { q, slots: slots[q.id] || [], card, n: qn[q.id] });
  }
}
function paintQ(a, s, ctl) {
  const { q, slots, card, n } = ctl;
  const done = s.qans[q.id] != null;
  for (const { slot, text, bi } of slots) {
    const no = el("span", "qno", circ(n));
    if (done) { slot.replaceChildren(no, el("mark", "wrev", text)); continue; }
    const b = el("button", "blank", q.kind === "语句填空" ? "＿＿＿＿＿＿" : "＿＿＿＿"); b.type = "button"; b.dataset.q = q.id;
    b.setAttribute("aria-label", "第" + n + "题" + (slots.length > 1 ? "第" + (bi + 1) + "空" : "的空") + "，点开看选项");
    b.addEventListener("click", () => openCard(a, s, ctl));
    slot.replaceChildren(no, b);
  }
  if (done) { card.hidden = false; fillCard(a, s, ctl, true); }
}
function fillCard(a, s, ctl, revealed) {
  const { q, card, n } = ctl;
  card.replaceChildren();
  const head = el("div", "qh");
  head.append(el("b", "", circ(n) + " " + q.kind), el("span", "", q.blanks.length > 1 ? q.blanks.length + " 个空，依次填入" : "第 " + q.p + " 段"));
  card.append(head);
  const long = q.kind === "语句填空" || q.options.some(o => o.length > 11);
  const opts = el("div", "opts" + (long ? " long" : ""));
  const chosen = s.qans[q.id];
  q.options.forEach((o, i) => {
    const b = el("button"); b.type = "button";
    b.append(el("span", "k", LETTERS[i]), el("span", "t", o));
    if (revealed) {
      b.disabled = true;
      if (i === q.answer) b.classList.add("right");
      if (chosen === i && i !== q.answer) b.classList.add("wrong");
    } else b.addEventListener("click", () => answerQ(a, s, ctl, i));
    opts.append(b);
  });
  card.append(opts);
  if (!revealed) {
    const skip = el("button", "linkish", "不选了，直接看原文"); skip.type = "button";
    skip.addEventListener("click", () => answerQ(a, s, ctl, -1));
    card.append(skip);
    return;
  }
  const res = el("div", "res");
  if (chosen === -1) res.append(el("span", "", "没有作答。原文是 " + LETTERS[q.answer] + "。"));
  else if (chosen === q.answer) res.append(el("span", "ok", "选对了。"));
  else res.append(el("span", "bad", "选了 " + LETTERS[chosen] + "，原文是 " + LETTERS[q.answer] + "。"));
  card.append(res, el("div", "note", q.note));
}
function openCard(a, s, ctl) {
  if (isPhone()) { openSheet(a, s, ctl); return; }
  ctl.card.hidden = false; fillCard(a, s, ctl, false);
  activeQ = { a, s, ctl };
  const first = ctl.card.querySelector(".opts button"); if (first) first.focus({ preventScroll: true });
  ctl.card.scrollIntoView({ block: "nearest" });
}
function answerQ(a, s, ctl, i) {
  const c = ctl.orig || ctl;
  s.qans[c.q.id] = i; save(); activeQ = null;
  paintQ(a, s, c); updateProg(a); renderNavLite();
  // 面板开着时，段落下方那张同样的卡先藏起来，收起面板再露出
  if (sheetCtl === c) { c.card.hidden = true; fillSheet(a, s, c, true); placeSheet(c); }
}

// 手机底部的选项面板：句子留在上方看得见，选完在面板里看说明，再“继续读”
const sheet = el("div", "qsheet"); sheet.hidden = true;
sheet.setAttribute("role", "dialog"); sheet.setAttribute("aria-label", "选项");
const sheetBar = el("div", "qs-bar"); const sheetX = el("button", "qs-x", "收起"); sheetX.type = "button";
const sheetBody = el("div", "qcard");
sheetBar.append(sheetX); sheet.append(sheetBar, sheetBody); document.body.append(sheet);
sheetX.addEventListener("click", () => closeSheet());
let sheetCtl = null;
function fillSheet(a, s, ctl, revealed) {
  const view = Object.assign({}, ctl, { card: sheetBody, orig: ctl });
  fillCard(a, s, view, revealed);
  if (revealed) {
    const go = el("button", "qs-go", "继续读"); go.type = "button";
    go.addEventListener("click", () => closeSheet());
    sheetBody.append(go);
  } else activeQ = { a, s, ctl: view };
  sheetBody.scrollTop = 0;
}
function openSheet(a, s, ctl) {
  sheetCtl = ctl;
  fillSheet(a, s, ctl, s.qans[ctl.q.id] != null);
  sheet.hidden = false; layerOpened();
  placeSheet(ctl);
}
// 把空格挪到面板上方的可见处
function placeSheet(ctl) {
  requestAnimationFrame(() => {
    if (sheet.hidden) return;
    const h = sheet.offsetHeight;
    document.body.style.paddingBottom = h + "px";
    const slot = ctl.slots[0] && ctl.slots[0].slot; if (!slot) return;
    const top = mbar.offsetHeight + 12;
    const want = top + Math.max(0, (innerHeight - h - top) * 0.3);
    window.scrollBy({ top: slot.getBoundingClientRect().top - want, behavior: SMOOTH });
  });
}
function closeSheet(keepHistory) {
  if (sheet.hidden) return;
  if (sheetCtl && sheetCtl.card.childNodes.length) sheetCtl.card.hidden = false;
  sheet.hidden = true; sheetCtl = null; activeQ = null; sheetBody.replaceChildren();
  document.body.style.paddingBottom = "";
  if (!keepHistory) layerClosed();
}

// 目录抽屉和选项面板打开时占一条历史记录，按手机的返回键先关掉它们，而不是离开页面
const root = document.documentElement;
let layerPushed = false, skipPop = false;
// 关抽屉、关面板时退回那条历史记录，别让浏览器顺手把滚动位置也还原回去
try { history.scrollRestoration = "manual"; } catch (e) {}
function layerOpened() { if (layerPushed) return; try { history.pushState({ gaiju: 1 }, ""); layerPushed = true; } catch (e) {} }
function layerClosed() {
  if (!layerPushed || root.classList.contains("nav-open") || !sheet.hidden) return;
  layerPushed = false; skipPop = true;
  try { history.back(); } catch (e) { skipPop = false; }
}
window.addEventListener("popstate", () => {
  if (skipPop) { skipPop = false; return; }
  layerPushed = false; closeSheet(true); closeNav(true);
});
function openNav() {
  closeSheet(true);
  root.classList.add("nav-open"); layerOpened();
  const cur = document.querySelector('.item[aria-current="true"]'); if (cur) cur.scrollIntoView({ block: "center" });
}
function closeNav(keepHistory) {
  if (!root.classList.contains("nav-open")) return;
  root.classList.remove("nav-open");
  if (!keepHistory) layerClosed();
}

// 顶上的窄栏：目录、标题、下一处
const mbar = el("div"); mbar.id = "mbar";
const mbMenu = el("button", "mb-menu", "目录"); mbMenu.type = "button";
const mbTitle = el("span", "mb-title", "");
const mbNext = el("button", "mb-next", ""); mbNext.type = "button";
mbar.append(mbMenu, mbTitle, mbNext);
document.querySelector(".app").prepend(mbar);
mbMenu.addEventListener("click", openNav);
mbTitle.addEventListener("click", () => window.scrollTo({ top: 0, behavior: SMOOTH }));
mbNext.addEventListener("click", () => {
  if (view !== "article") { if (current) openArticle(current); return; }
  if (nextTarget()) { goNext(); return; }
  const list = ordered(); const i = list.findIndex(x => x.id === current);
  if (i >= 0 && i < list.length - 1) openArticle(list[i + 1].id);
});
function updateMbar() {
  const a = byId[current];
  if (view !== "article" || !a) {
    mbTitle.textContent = view === "stats" ? "我的记录" : view === "ref" ? "广东“1310”" : "";
    mbNext.textContent = "回到文章"; mbNext.hidden = !a; return;
  }
  mbTitle.textContent = titleOf(a); mbNext.hidden = false;
  const s = st(a.id), em = effMode(a);
  let total, left;
  if (em === "q") { total = a.q.length; left = a.q.filter(q => s.qans[q.id] == null).length; }
  else if (em === "w") { total = a.w.length; left = a.w.filter(w => !s.wopen[w.id]).length; }
  else if (em === "zz") { total = a.z.length; left = a.z.filter(z => s.zans[z.id] == null).length; }
  else { total = 0; left = 0; }
  mbNext.textContent = left ? (em === "zz" ? "下一题 " : "下一空 ") + (total - left) + "/" + total : "下一篇 →";
}
// 下一处还没做的空格或主旨题
function nextTarget() {
  const a = byId[current]; if (!a || view !== "article") return null;
  return document.querySelector(effMode(a) === "zz" ? ".zcard:not(.done)" : "button.blank");
}
function goNext() {
  const b = nextTarget(); if (!b) return;
  if (b.matches(".zcard")) {
    b.scrollIntoView({ block: "start", behavior: SMOOTH });
    activeZ = b._ctl;
    const first = b.querySelector(".opts button"); if (first) first.focus({ preventScroll: true });
    return;
  }
  b.click();
}

// ---------- 主旨理解 ----------
// 题卡：答之前只给截好的题干；答完给对错、说明，题干换成原文对照（划掉的是命题人删的，下划线是改写或添上的）
function zCard(a, s, z, n) {
  const box = el("div", "zcard"); box.dataset.z = z.id;
  box._ctl = { a, s, z, n, box };
  paintZ(box._ctl);
  return box;
}
function zRange(z) { return z.from === z.to ? "第 " + z.from + " 段" : "第 " + z.from + "–" + z.to + " 段"; }
function paintZ(ctl) {
  const { a, s, z, n, box } = ctl;
  const chosen = s.zans[z.id], done = chosen != null;
  box.replaceChildren(); box.classList.toggle("done", done);
  const head = el("div", "qh");
  head.append(el("b", "", "主旨题 " + circ(n)), el("span", "", zRange(z) + (z.type ? " · " + z.type : "")));
  box.append(head);
  if (!done) {
    const ps = el("div", "zpass");
    for (const line of z.passage.split("\n")) ps.append(el("p", "", line));
    box.append(ps);
  } else box.append(zDiff(z));
  box.append(el("div", "zstem", z.stem));
  const opts = el("div", "opts long");
  z.options.forEach((o, i) => {
    const b = el("button"); b.type = "button";
    b.append(el("span", "k", LETTERS[i]), el("span", "t", o));
    if (done) {
      b.disabled = true;
      if (i === z.answer) b.classList.add("right");
      if (chosen === i && i !== z.answer) b.classList.add("wrong");
    } else b.addEventListener("click", () => answerZ(ctl, i));
    opts.append(b);
  });
  box.append(opts);
  if (!done) {
    const skip = el("button", "linkish", "不选了，直接看答案"); skip.type = "button";
    skip.addEventListener("click", () => answerZ(ctl, -1));
    box.append(skip);
    return;
  }
  const res = el("div", "res");
  if (chosen === -1) res.append(el("span", "", "没有作答。答案是 " + LETTERS[z.answer] + "。"));
  else if (chosen === z.answer) res.append(el("span", "ok", "选对了。"));
  else res.append(el("span", "bad", "选了 " + LETTERS[chosen] + "，答案是 " + LETTERS[z.answer] + "。"));
  box.append(res);
  if (z.contested) box.append(el("div", "zdisp", "争议题：另一项也说得通，看说明里命题人为什么判这一项。"));
  box.append(el("div", "note", z.note));
}
function zDiff(z) {
  const d = el("div", "zorig");
  d.append(el("div", "zlab", "原文" + zRange(z).replace("第 ", "第").replace(" 段", "段") + "：划掉的是命题人删去的，加下划线的是命题人改写或添上的"));
  let pno = z.from;
  let p = el("p"); p.append(el("span", "pno", "[" + pno + "]")); d.append(p);
  for (const [op, t] of z.diff) {
    t.split("\n").forEach((seg, k) => {
      if (k > 0 && op !== "+") { pno++; p = el("p"); p.append(el("span", "pno", "[" + pno + "]")); d.append(p); }
      if (!seg) return;
      p.append(op === "=" ? document.createTextNode(seg) : el(op === "-" ? "del" : "ins", "", seg));
    });
  }
  return d;
}
function answerZ(ctl, i) {
  const { a, s, z, box } = ctl;
  s.zans[z.id] = i; save(); activeZ = null;
  paintZ(ctl); updateProg(a); renderNavLite();
  unhideZ(s, box);
  if (box.getBoundingClientRect().top < 0) box.scrollIntoView({ block: "start", behavior: SMOOTH });
}
function plainPara(para, pi) {
  const box = el("div", "para");
  const p = el("p", para.length === 1 && para[0].sub ? "sub" : "");
  p.append(el("span", "pno", "[" + (pi + 1) + "]"), document.createTextNode(paraText(para)));
  box.append(p);
  return box;
}
function zHidden(a, s, para, pi, zs) {
  const box = el("div", "zhide"); box._para = para; box._pi = pi; box._zs = zs;
  const nums = zs.map(z => circ(a.z.indexOf(z) + 1)).join("");
  box.append(el("span", "pno", "[" + (pi + 1) + "]"), el("span", "", "这段先收起：它会露出主旨题 " + nums + " 的答案，做完再看。"));
  const b = el("button", "linkish", "现在就看"); b.type = "button";
  b.addEventListener("click", () => box.replaceWith(plainPara(para, pi)));
  box.append(b);
  return box;
}
function titleBox(a, s) {
  const h = el("h1"); h.id = "atitle";
  if (!titleHidden(a)) { h.textContent = a.title; return h; }
  h.className = "tmask";
  const nums = a.z.map((z, i) => z.htitle && s.zans[z.id] == null ? circ(i + 1) : "").join("");
  h.append(el("span", "", "标题先遮住"), el("span", "tnote", "它会露出主旨题 " + nums + " 的答案，做完再看。"));
  const b = el("button", "linkish", "现在就看"); b.type = "button";
  b.addEventListener("click", () => { s.tshow = true; save(); h.replaceWith(titleBox(a, s)); updateMbar(); renderNavLite(); });
  h.append(b);
  return h;
}
// 做完一题，把只为它收起的段落和标题展开；上方展开的段落会把题卡往下推，这里把页面滚回原位
function unhideZ(s, anchor) {
  const before = anchor.getBoundingClientRect().top;
  for (const h of document.querySelectorAll(".zhide")) if (h._zs.every(z => s.zans[z.id] != null)) h.replaceWith(plainPara(h._para, h._pi));
  const t = document.getElementById("atitle"), a = byId[current];
  if (t && a && t.classList.contains("tmask") && !titleHidden(a)) t.replaceWith(titleBox(a, s));
  const d = anchor.getBoundingClientRect().top - before;
  if (d) { if (isPhone()) window.scrollBy(0, d); else document.getElementById("main").scrollTop += d; }
}

// ---------- 广东式政治理论 / 常识 ----------
function renderItems(a, s, art) {
  const jb = el("section", "block");
  jb.append(el("h2", "", "政治理论 · 常识（按广东卷考法）"));
  jb.append(el("div", "hint", "题型照广东卷，有判断、单选、多选。答完看解析和依据；依据标了类型，“搜索佐证”表示只核到搜索结果、没打开原页面，记的时候留个心。"));
  a.items.forEach((it, ii) => jb.append(itemBox(a, s, it, ii)));
  art.append(jb);
  if (a.judgments && a.judgments.length) {
    const d = el("details", "old");
    d.append(el("summary", "", "旧版判断题（对照用，" + a.judgments.length + " 道）"));
    d.append(oldJudgments(a, s, null));
    art.append(d);
  }
}
const KIND_TAG = { "原文": "原文", "已核原话": "已核原话", "搜索佐证": "搜索佐证" };
function itemBox(a, s, it, ii) {
  const box = el("div", "judg");
  const stem = el("div", "stem");
  stem.append(el("span", "kind", "（" + it.type + "题 · " + it.area + "）"), document.createTextNode((ii + 1) + ". " + it.stem));
  box.append(stem);
  const res = el("div", "res2");
  const done = s.iqa[it.id] != null;
  const show = () => {
    const v = s.iqa[it.id];
    res.replaceChildren();
    const right = it.type === "多选" ? JSON.stringify(v) === JSON.stringify(it.answer) : v === it.answer;
    const ans = it.type === "判断" ? (it.answer ? "正确" : "错误") : it.type === "多选" ? it.answer.map(i => LETTERS[i]).join("") : LETTERS[it.answer];
    res.append(el("span", right ? "ok" : "bad", (right ? "答对了。" : "答错了。") + "正确答案：" + ans + "。"));
    res.append(document.createTextNode(it.explain));
    if ((it.sources || []).length) {
      const weakN = it.sources.filter(x => x.kind === "搜索佐证").length;
      const det = el("details", "srcs-d");
      det.append(el("summary", "", "依据 " + it.sources.length + " 条" + (weakN ? "（其中搜索佐证 " + weakN + " 条）" : "")));
      const ss = el("div", "srcs");
      for (const x of it.sources) {
        const line = el("div", "s");
        line.append(el("span", "tag" + (x.kind === "搜索佐证" ? " weak" : ""), KIND_TAG[x.kind] || x.kind));
        if (x.quote) line.append(document.createTextNode(x.kind === "搜索佐证" ? "搜索摘要：" + x.quote.replace(/^【[^】]*】/, "") + " " : "“" + x.quote + "” "));
        if (x.url) { const l = el("a", "", x.url); l.href = x.url; l.target = "_blank"; l.rel = "noopener"; line.append(l); }
        ss.append(line);
      }
      det.append(ss);
      res.append(det);
    }
  };
  if (it.type === "判断") {
    const row = el("div", "row");
    for (const [v, name] of [[true, "正确"], [false, "错误"]]) {
      const b = el("button", "", name); b.type = "button";
      if (done) { b.disabled = true; b.setAttribute("aria-pressed", s.iqa[it.id] === v ? "true" : "false"); }
      b.addEventListener("click", () => { s.iqa[it.id] = v; save(); box.replaceWith(itemBox(a, s, it, ii)); });
      row.append(b);
    }
    box.append(row);
  } else {
    const multi = it.type === "多选";
    const opts = el("div", "opts long");
    const picked = new Set(done && multi ? s.iqa[it.id] : []);
    it.options.forEach((o, i) => {
      const b = el("button"); b.type = "button";
      b.append(el("span", "k", LETTERS[i]), el("span", "t", o));
      if (done) {
        b.disabled = true;
        const isAns = multi ? it.answer.includes(i) : it.answer === i;
        const isPick = multi ? s.iqa[it.id].includes(i) : s.iqa[it.id] === i;
        if (isAns) b.classList.add("right");
        else if (isPick) b.classList.add("wrong");
        if (isPick) b.setAttribute("aria-pressed", "true");
      } else if (multi) {
        b.setAttribute("aria-pressed", "false");
        b.addEventListener("click", () => { if (picked.has(i)) picked.delete(i); else picked.add(i); b.setAttribute("aria-pressed", picked.has(i) ? "true" : "false"); });
      } else {
        b.addEventListener("click", () => { s.iqa[it.id] = i; save(); box.replaceWith(itemBox(a, s, it, ii)); });
      }
      opts.append(b);
    });
    box.append(opts);
    if (multi && !done) {
      const row = el("div", "row");
      const sub = el("button", "submit", "提交"); sub.type = "button";
      sub.addEventListener("click", () => { if (!picked.size) return; s.iqa[it.id] = [...picked].sort(); save(); box.replaceWith(itemBox(a, s, it, ii)); });
      row.append(sub);
      box.append(row);
    }
  }
  box.append(res);
  if (done) show();
  return box;
}

function oldJudgments(a, s, title) {
  const jb = el("section", title ? "block" : "");
  if (title) jb.append(el("h2", "", title));
  a.judgments.forEach((j, ji) => {
    const box = el("div", "judg");
    box.append(el("div", "stem", (ji + 1) + ". （判断题）" + j.statement));
    const row = el("div", "row");
    const res = el("div", "res");
    const show = (pick) => {
      res.replaceChildren();
      const right = pick === j.answer;
      res.append(el("span", right ? "ok" : "bad", (right ? "答对了。" : "答错了。") + "正确答案：" + (j.answer ? "正确" : "错误") + "。"));
      res.append(document.createTextNode(j.explain));
      const q = el("div", "quote", "原话：" + j.source_quote);
      const l = el("a", "", j.source_url); l.href = j.source_url; l.target = "_blank"; l.rel = "noopener";
      const srcLine = el("div", ""); srcLine.append(document.createTextNode("出处："), l);
      res.append(q, srcLine);
    };
    for (const [v, name] of [[true, "正确"], [false, "错误"]]) {
      const b = el("button", "", name); b.type = "button";
      b.addEventListener("click", () => { s.judg[ji] = v; save(); show(v); });
      row.append(b);
    }
    if (s.judg[ji] != null) show(s.judg[ji]);
    box.append(row, res);
    jb.append(box);
  });
  return jb;
}

// ---------- 旧版遮词（未做新版的文章，以及新版文章里的对照） ----------
function renderWordPara(a, s, para, pi, p, checks) {
  const full = paraText(para);
  const ws = (a.w || []).filter(w => w.p === pi + 1).sort((x, y) => x.b - y.b);
  let pos = 0;
  for (const w of ws) {
    if (w.b > pos) p.append(document.createTextNode(full.slice(pos, w.b)));
    const word = full.slice(w.b, w.e);
    const slot = el("span"); p.append(slot);
    const reveal = () => slot.replaceChildren(el("mark", "wrev", word));
    const blank = () => {
      const wordLength = Array.from(word).length;
      const b = el("button", "blank", "＿".repeat(wordLength)); b.type = "button"; b.dataset.word = w.id;
      b.setAttribute("aria-label", "第" + (pi + 1) + "段被遮住的词句，" + wordLength + "个字");
      b.addEventListener("click", () => {
        const pk = el("span", "pick");
        for (const [k, name] of [["sure", "有把握"], ["unsure", "没把握"]]) {
          const c = el("button", "", name); c.type = "button";
          c.addEventListener("click", () => { s.wopen[w.id] = 1; s.wconf[w.id] = k; save(); reveal(); checks.append(wordRow(a, w, word, pi)); updateProg(a); });
          pk.append(c);
        }
        slot.replaceChildren(pk); pk.firstChild.focus();
      });
      slot.replaceChildren(b);
    };
    if (s.wopen[w.id]) { reveal(); checks.append(wordRow(a, w, word, pi)); } else blank();
    pos = w.e;
  }
  if (pos < full.length) p.append(document.createTextNode(full.slice(pos)));
}
function wordRow(a, w, word, pi) {
  const s = st(a.id);
  const row = el("div", "check");
  row.append(el("span", "which", "第" + (pi + 1) + "段「" + word + "」（揭开前" + (s.wconf[w.id] === "sure" ? "有把握" : "没把握") + "）：和我的措辞比——"));
  const chips = el("div", "chips"); chips.setAttribute("role", "group");
  for (const [v, name] of [[true, "对上了"], [false, "没对上"]]) {
    const b = el("button", "", name); b.type = "button";
    b.setAttribute("aria-pressed", s.whit[w.id] === v ? "true" : "false");
    b.addEventListener("click", () => {
      if (s.whit[w.id] === v) delete s.whit[w.id]; else s.whit[w.id] = v;
      for (const c of chips.children) c.setAttribute("aria-pressed", c === b && s.whit[w.id] === v ? "true" : "false");
      save(); updateProg(a);
    });
    chips.append(b);
  }
  row.append(chips);
  if (w.note) row.append(el("span", "note", w.note));
  return row;
}
function wordContext(a, w) {
  const full = paraText(a.paras[w.p - 1]);
  let b = w.b, e = w.e;
  while (b > 0 && !"。！？；".includes(full[b - 1])) b--;
  while (e < full.length && !"。！？；".includes(full[e - 1] || "")) e++;
  return [full.slice(b, w.b), full.slice(w.b, w.e), full.slice(w.e, e)];
}
// 一道新版题所在的句子，空处标出原文
function qContext(a, q) {
  const full = paraText(a.paras[q.p - 1]);
  let b = q.blanks[0].b, e = q.blanks[q.blanks.length - 1].e;
  while (b > 0 && !"。！？".includes(full[b - 1])) b--;
  while (e < full.length && !"。！？".includes(full[e - 1] || "")) e++;
  const out = []; let pos = b;
  for (const x of q.blanks) { out.push([full.slice(pos, x.b), false], [full.slice(x.b, x.e), true]); pos = x.e; }
  out.push([full.slice(pos, e), false]);
  return out;
}
let navTimer; function renderNavLite() { clearTimeout(navTimer); navTimer = setTimeout(renderNav, 150); }

function renderStats() {
  view = "stats"; renderNav(); updateMbar();
  const wrap = el("div", "wrap");
  let jr = 0, jt = 0, cr = 0, ct = 0, done = 0;
  let qn = 0, qr = 0, ir = 0, itn = 0, zn = 0, zr = 0, cn = 0, crr = 0;
  const words = [], qmiss = [], zmiss = [];
  for (const a of DATA) {
    const s = store[a.id]; if (!s) continue;
    for (const z of a.z || []) {
      const v = s.zans && s.zans[z.id]; if (v == null || v === -1) continue;
      zn++; if (v === z.answer) zr++; else zmiss.push([a, z, v]);
      if (z.contested) { cn++; if (v === z.answer) crr++; }
    }
    if (!(a.items || []).length) (a.judgments || []).forEach((j, i) => { if (s.judg && s.judg[i] != null) { if (a.kind === "cs") { ct++; if (s.judg[i] === j.answer) cr++; } else { jt++; if (s.judg[i] === j.answer) jr++; } } });
    for (const it of a.items || []) { const v = s.iqa && s.iqa[it.id]; if (v == null) continue; itn++; if (it.type === "多选" ? JSON.stringify(v) === JSON.stringify(it.answer) : v === it.answer) ir++; }
    for (const q of a.q || []) { const v = s.qans && s.qans[q.id]; if (v == null || v === -1) continue; qn++; if (v === q.answer) qr++; else qmiss.push([a, q, v]); }
    if (statusOf(a) === "done") done++;
    if (s.words && s.words.trim()) words.push("【" + titleOf(a) + "】" + s.words.trim());
  }
  wrap.append(el("h1", "", "我的记录"));
  const grid = el("div", "stats");
  const card = (n, l, pct) => { const d = el("div", "stat"); const nn = el("div", "n", String(n)); if (pct) nn.append(el("span", "pct", pct)); d.append(nn, el("div", "l", l)); return d; };
  grid.append(card(done + " / " + DATA.length, "读完的篇数"), card(zn ? zr + " / " + zn : "0", "主旨题答对"));
  if (DATA.some(a => (a.z || []).some(z => z.contested))) grid.append(card(cn ? crr + " / " + cn : "0", "其中争议题答对"));
  grid.append(card(qn ? qr + " / " + qn : "0", "词句题答对"), card(itn ? ir + " / " + itn : "0", "广东式政治常识题答对"));
  grid.append(card(jt ? jr + " / " + jt : "0", "旧版政治理论判断题答对"), card(ct ? cr + " / " + ct : "0", "旧版常识判断题答对"));
  let wn = 0, wh = 0; const miss = [];
  for (const a of DATA) {
    const s = store[a.id]; if (!s || !s.whit) continue;
    for (const w of a.w || []) {
      const hit = s.whit[w.id]; if (hit == null) continue;
      wn++; if (hit) wh++; else if (s.wconf && s.wconf[w.id] === "sure") miss.push([a, w]);
    }
  }
  grid.append(card(wn ? wh + " / " + wn : "0", "旧版词语对上了"), card(miss.length, "旧版有把握却没对上的词"));
  wrap.append(grid);
  if (zmiss.length) {
    const rsec = el("section", "block");
    rsec.append(el("h2", "", "选错的主旨题（重点复习）"), el("div", "hint", "看看当时被哪个选项带走了，再回原文对照命题人删了哪句。"));
    const list = el("div", "review");
    for (const [a, z, v] of zmiss) {
      const it = el("div", "it");
      it.append(el("div", "ctx", (z.contested ? "【争议题】" : "") + z.stem), el("div", "", "你选了 " + LETTERS[v] + "．" + z.options[v] + "；答案 " + LETTERS[z.answer] + "．" + z.options[z.answer]), el("div", "", z.note));
      const src = el("a", "src", "【" + titleOf(a) + "】" + zRange(z).replace(/ /g, "")); src.href = "#" + a.id;
      src.addEventListener("click", e => { e.preventDefault(); mode = "zz"; saveUi(); openArticle(a.id); });
      it.append(src);
      list.append(it);
    }
    rsec.append(list);
    wrap.append(rsec);
  }
  if (qmiss.length) {
    const rsec = el("section", "block");
    rsec.append(el("h2", "", "选错的词句题（重点复习）"), el("div", "hint", "原文用词标了出来。看看当时被哪个选项带走了，再读一遍说明。"));
    const list = el("div", "review");
    for (const [a, q, v] of qmiss) {
      const it = el("div", "it");
      const ctx = el("div", "ctx");
      for (const [t, hl] of qContext(a, q)) ctx.append(hl ? el("mark", "wrev", t) : document.createTextNode(t));
      it.append(ctx, el("div", "", "你选了 " + LETTERS[v] + "．" + q.options[v] + "；原文 " + LETTERS[q.answer] + "．" + q.options[q.answer]), el("div", "", q.note));
      const src = el("a", "src", "【" + titleOf(a) + "】第" + q.p + "段"); src.href = "#" + a.id;
      src.addEventListener("click", e => { e.preventDefault(); mode = "word"; saveUi(); openArticle(a.id); });
      it.append(src);
      list.append(it);
    }
    rsec.append(list);
    wrap.append(rsec);
  }
  if (miss.length) {
    const rsec = el("section", "block");
    rsec.append(el("h2", "", "旧版：有把握却没对上的词"), el("div", "hint", "这些是你以为稳了、结果原文用了别的词的地方，最值得回看。"));
    const list = el("div", "review");
    for (const [a, w] of miss) {
      const [l, m, r] = wordContext(a, w);
      const it = el("div", "it");
      const ctx = el("div", "ctx"); ctx.append(document.createTextNode(l), el("mark", "wrev", m), document.createTextNode(r));
      const src = el("a", "src", "【" + titleOf(a) + "】第" + w.p + "段"); src.href = "#" + a.id;
      src.addEventListener("click", e => { e.preventDefault(); mode = hasQ(a) ? "wold" : "word"; saveUi(); openArticle(a.id); });
      it.append(ctx);
      if (w.note) it.append(el("div", "", w.note));
      it.append(src);
      list.append(it);
    }
    rsec.append(list);
    wrap.append(rsec);
  }
  const wsec = el("section", "block");
  wsec.append(el("h2", "", "攒下的措辞（可整段复制给 DeepSeek）"));
  const pre = el("div", "words-all", words.length ? words.join("\n") : "还没有记录。");
  const copy = el("button", "", "复制全部"); copy.type = "button";
  copy.addEventListener("click", async () => { try { await navigator.clipboard.writeText(words.join("\n")); copy.textContent = "已复制"; } catch (e) { const r = document.createRange(); r.selectNodeContents(pre); const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); copy.textContent = "已选中，请手动复制"; } });
  wsec.append(pre, copy);
  wrap.append(wsec);
  const bsec = el("section", "block");
  bsec.append(el("h2", "", "备份与恢复"), el("div", "hint", "记录保存在这台设备的浏览器里，换个浏览器或换台设备就看不到了。换设备或清理浏览器数据前，先导出备份。"));
  const tools = el("div", "tools");
  const ex = el("button", "", "导出备份"); ex.type = "button";
  ex.addEventListener("click", () => { const blob = new Blob([JSON.stringify(store)], { type: "application/json" }); const u = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = u; a.download = "盖句精读-记录.json"; document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(u), 1000); });
  const imLabel = el("label", "", "导入备份："); const im = el("input"); im.type = "file"; im.accept = "application/json"; imLabel.append(im);
  im.addEventListener("change", async () => { const f = im.files[0]; if (!f) return; try { const v = JSON.parse(await f.text()); if (v && typeof v === "object") { store = v; save(); renderStats(); } } catch (e) { imLabel.append(el("span", "", " 文件读不了，请选导出的那份。")); } });
  tools.append(ex, imLabel);
  bsec.append(tools);
  wrap.append(bsec);
  document.getElementById("main").replaceChildren(wrap);
}

function render1310() {
  view = "ref"; renderNav(); updateMbar();
  const wrap = el("div", "wrap");
  wrap.append(el("h1", "", "广东省委“1310”具体部署"));
  wrap.append(el("div", "how", REF.intro));
  const t = el("table", "ref");
  const tb = el("tbody");
  REF.items.forEach((x, i) => { const tr = el("tr"); tr.append(el("td", "", String(i + 1)), el("td", "", x)); tb.append(tr); });
  t.append(tb); wrap.append(t);
  for (const n of REF.notes) wrap.append(el("div", "hint", n));
  const l = el("a", "", "原文：广东省人民政府网（需联网）"); l.href = REF.url; l.target = "_blank"; l.rel = "noopener";
  wrap.append(l);
  document.getElementById("main").replaceChildren(wrap);
}

// 来源筛选里加一个"新版"按钮
(function addPilotFilter() {
  if (!DATA.some(a => a.pilot)) return;
  const seg = document.querySelector('[aria-label="来源筛选"]');
  // 全部文章都做了新版遮词句以后，"新版"筛选就等于"全部"，换成只列做了主旨题的
  const allNew = DATA.every(a => a.pilot);
  if (allNew && !DATA.some(hasZ)) { if (srcFilter === "试点") srcFilter = "all"; }
  else {
    const b = document.createElement("button"); b.type = "button";
    b.dataset.src = allNew ? "主旨" : "试点"; b.textContent = allNew ? "主旨" : "新版"; b.setAttribute("aria-pressed", "false");
    seg.prepend(b);
    if (allNew && srcFilter === "试点") srcFilter = "all";
  }
  const head = document.querySelector(".nav-head");
  const note = el("div", "pilot-note", META.note || "");
  if (META.note) head.append(note);
})();

document.querySelectorAll("[data-order]").forEach(b => b.addEventListener("click", () => { order = b.dataset.order; saveUi(); renderNav(); }));
document.querySelectorAll("[data-src]").forEach(b => b.addEventListener("click", () => { srcFilter = b.dataset.src; saveUi(); renderNav(); }));
document.getElementById("q").addEventListener("input", e => { query = e.target.value; renderNav(); });
for (const [bid, fn] of [["go-stats", renderStats], ["go-1310", render1310]]) {
  document.getElementById(bid).addEventListener("click", () => { closeNav(); closeSheet(); fn(); document.getElementById("main").scrollTop = 0; window.scrollTo(0, 0); });
}
// 手机抽屉里的“收起”
(function addNavClose() {
  const b = el("button", "nav-close", "收起"); b.type = "button";
  b.addEventListener("click", () => closeNav());
  document.querySelector(".brand").append(b);
})();
// 屏幕在手机和电脑宽度之间切换时（平板转屏），收起抽屉和面板，按新宽度重画
(PHONE.addEventListener ? PHONE.addEventListener.bind(PHONE, "change") : PHONE.addListener.bind(PHONE))(() => {
  closeNav(); closeSheet();
  if (view === "article" && byId[current]) renderArticle(byId[current]);
});
document.addEventListener("keydown", e => {
  if (view !== "article" || e.target.matches("textarea, input")) return;
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const list = ordered(); const i = list.findIndex(x => x.id === current);
  if (activeQ && !activeQ.ctl.card.hidden && activeQ.s.qans[activeQ.ctl.q.id] == null) {
    const k = e.key.toUpperCase();
    const idx = "ABCD".indexOf(k) >= 0 ? "ABCD".indexOf(k) : "1234".indexOf(e.key);
    if (idx >= 0 && e.key.length === 1) { const { a, s, ctl } = activeQ; answerQ(a, s, ctl, idx); e.preventDefault(); return; }
  }
  if (activeZ && activeZ.box.isConnected && activeZ.s.zans[activeZ.z.id] == null) {
    const k = e.key.toUpperCase();
    const idx = "ABCD".indexOf(k) >= 0 ? "ABCD".indexOf(k) : "1234".indexOf(e.key);
    if (idx >= 0 && e.key.length === 1) { answerZ(activeZ, idx); e.preventDefault(); return; }
  }
  if (e.key === "ArrowRight" && i >= 0 && i < list.length - 1) { openArticle(list[i + 1].id); e.preventDefault(); }
  else if (e.key === "ArrowLeft" && i > 0) { openArticle(list[i - 1].id); e.preventDefault(); }
  else if (e.key === " ") {
    if (e.target.closest && e.target.closest(".pick")) return;
    if (nextTarget()) { goNext(); e.preventDefault(); }
  }
  else if (e.key === "Escape") { closeSheet(); closeNav(); }
});

const visibleNow = ordered();
let start = (location.hash && byId[location.hash.slice(1)]) ? location.hash.slice(1) : (current && byId[current] ? current : null);
if (resumeZ && !location.hash) {
  const full = sorted(DATA.slice()), p = start ? full.findIndex(a => a.id === start) : -1;
  const nx = p >= 0 ? full.slice(p).find(zLeft) : visibleNow.find(zLeft);
  if (nx) start = nx.id;
}
openArticle(start || (visibleNow[0] || DATA[0]).id);
