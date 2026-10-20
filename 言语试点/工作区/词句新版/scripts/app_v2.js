"use strict";
const DATA = JSON.parse(document.getElementById("data").textContent);
const REF = JSON.parse(document.getElementById("ref1310").textContent);
const META = JSON.parse(document.getElementById("meta").textContent);
const TAGS = [["hit", "猜中"], ["narrow", "太窄"], ["level", "层次不对"], ["tail", "被尾句带走"]];
const KEY = "gaiju-v1";
let store = {};
try { store = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { store = {}; }
function save() { try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) {} }
function st(id) {
  const s = store[id] || (store[id] = { open: {}, tags: {}, words: "", judg: {} });
  s.wopen = s.wopen || {}; s.wconf = s.wconf || {}; s.whit = s.whit || {};
  s.qans = s.qans || {}; s.iqa = s.iqa || {};
  return s;
}

let order = "theme", srcFilter = "all", query = "", current = null, view = "article", mode = "word";
try {
  const u = JSON.parse(localStorage.getItem(KEY + ":ui") || "{}");
  order = u.order || order; srcFilter = u.src || srcFilter; current = u.cur || null;
  if (u.mode === "word" || u.mode === "sent" || u.mode === "wold") mode = u.mode;
  if (u.ver !== META.ver && DATA.some(a => a.pilot)) { srcFilter = "试点"; mode = "word"; current = null; }
} catch (e) {}
function saveUi() { try { localStorage.setItem(KEY + ":ui", JSON.stringify({ order, src: srcFilter, cur: current, mode, ver: META.ver })); } catch (e) {} }

const byId = Object.fromEntries(DATA.map(a => [a.id, a]));
const LETTERS = "ABCD";
function circ(n) { return n >= 1 && n <= 20 ? String.fromCharCode(0x2460 + n - 1) : "(" + n + ")"; }
function masksOf(a) { return a.paras.flat().filter(x => x.m); }
function hasQ(a) { return (a.q || []).length > 0; }
function statusOf(a) {
  const s = store[a.id]; if (!s) return "";
  if (hasQ(a)) {
    const n = a.q.length, t = a.q.filter(q => s.qans && s.qans[q.id] != null).length;
    if (t >= n) return "done";
    return (t || Object.keys(s.tags || {}).length || Object.keys(s.open || {}).length) ? "part" : "";
  }
  const n = masksOf(a).length, t = Object.keys(s.tags || {}).length;
  if (n && t >= n) return "done";
  return (t || Object.keys(s.open || {}).length) ? "part" : "";
}
function visible() {
  const q = query.trim();
  return DATA.filter(a => {
    if (srcFilter === "试点") { if (!a.pilot) return false; }
    else if (srcFilter === "常识") { if (a.kind !== "cs") return false; }
    else if (srcFilter !== "all") { if (a.kind === "cs" || a.src !== srcFilter) return false; }
    return !q || (a.title + a.group + a.col).includes(q);
  });
}
function rank(a) { return a.kind === "cs" ? 2 : a.src === "南方日报" ? 1 : 0; }
function ordered() {
  const list = visible().slice();
  if (order === "date") list.sort((x, y) => x.date.localeCompare(y.date) || x.id.localeCompare(y.id));
  else list.sort((x, y) => rank(x) - rank(y) || x.gidx - y.gidx || x.date.localeCompare(y.date));
  return list;
}

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
    const t = document.createElement("div"); t.className = "t"; t.textContent = a.title;
    if (a.pilot) t.append(el("span", "badge", "新版"));
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
  current = id; view = "article"; saveUi();
  renderArticle(byId[id]); renderNav();
  document.getElementById("main").scrollTop = 0;
  const cur = document.querySelector('.item[aria-current="true"]'); if (cur) cur.scrollIntoView({ block: "nearest" });
}

function el(tag, cls, text) { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

// 当前文章实际用哪种遮法：sent 点题句；q 新版遮词句；w 旧版遮词
function effMode(a) {
  if (mode === "sent") return "sent";
  if (mode === "wold") return (a.w || []).length ? "w" : hasQ(a) ? "q" : "sent";
  return hasQ(a) ? "q" : (a.w || []).length ? "w" : "sent";
}

let activeQ = null;

function renderArticle(a) {
  const s = st(a.id);
  const em = effMode(a);
  activeQ = null;
  const main = document.getElementById("main");
  const wrap = el("div", "wrap");
  const how = el("div", "how");
  const legend = el("div", "legend");
  if (em === "q") {
    how.innerHTML = "读到空格，先<b>自己想原文用了什么词、什么句</b>，再点空格看选项、选一个。选完揭开原文和说明。空格前的 ①② 是题号，题号相同的几个空是同一道题，依次填入。";
    const nw = a.q.filter(q => q.kind === "选词填空").length, ns = a.q.length - nw;
    legend.innerHTML = `<span>本篇：选词填空 <b>${nw}</b> 题、语句填空 <b>${ns}</b> 题</span><span>选错的题会收进“我的记录”</span>`;
  } else if (em === "w") {
    how.innerHTML = "读到遮住的词句，先<b>想想自己会怎样接</b>，再选“有把握”或“没把握”揭开。对照原文的措辞和语气，点“对上了”或“没对上”；不必一字不差。";
    legend.innerHTML = "<span><b>有把握却没对上</b>的词会收进“我的记录”，留着重点复习</span>";
  } else {
    how.innerHTML = "每段先读灰条以外的部分，<b>心里用一句话说出这段在讲什么</b>，再点灰条看原句，选一个对照结果。灰条遮住的是这一段的点题句，命题人出片段阅读时常删的就是它。";
    legend.innerHTML = "<span><b>猜中</b>：意思对上了</span><span><b>太窄</b>：把例子或局部当成观点</span><span><b>层次不对</b>：抽象得太高或太低</span><span><b>被尾句带走</b>：抓了段尾，但它不是中心</span>";
  }
  const art = el("article");
  const meta = el("div", "meta");
  const src = el("span", "src" + (a.src === "南方日报" ? " nf" : ""), a.src);
  meta.append(src, el("span", "", a.col), el("span", "", a.date), el("span", "", a.page || ""));
  const h = el("h1", "", a.title);
  const by = el("div", "byline");
  if (a.author) by.append(el("span", "", a.author));
  const link = el("a", "", "原文链接（需联网）"); link.href = a.url; link.target = "_blank"; link.rel = "noopener";
  const prog = el("span", "progress"); prog.id = "prog";
  by.append(link, prog);
  const grp = el("div", "group", (a.kind === "cs" ? "考点：" : a.src === "南方日报" ? "覆盖：" : "主题：") + a.group);
  art.append(meta, h, by, grp);
  if (hasQ(a) || (a.w || []).length) {
    const mb = el("div", "modebar");
    const seg = el("div", "seg"); seg.setAttribute("role", "group"); seg.setAttribute("aria-label", "遮挡方式");
    const modes = [["sent", "遮点题句（" + masksOf(a).length + "）"]];
    if (hasQ(a)) modes.push(["word", "遮词句 · 新版（" + a.q.length + " 题）"]);
    else modes.push(["word", "遮词句（" + a.w.length + "）"]);
    if (hasQ(a) && (a.w || []).length) modes.push(["wold", "旧版遮词（对照）"]);
    const cur = em === "sent" ? "sent" : em === "q" ? "word" : hasQ(a) ? "wold" : "word";
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

  a.paras.forEach((para, pi) => {
    const box = el("div", "para");
    const p = el("p", para.length === 1 && para[0].sub ? "sub" : "");
    p.append(el("span", "pno", "[" + (pi + 1) + "]"));
    const checks = el("div", "checks");
    if (em === "q") { renderQPara(a, s, para, pi, p, checks, qn); box.append(p, checks); art.append(box); return; }
    if (em === "w") { renderWordPara(a, s, para, pi, p, checks); box.append(p, checks); art.append(box); return; }
    for (const part of para) {
      if (part.t != null) { p.append(document.createTextNode(part.t)); continue; }
      const slot = el("span");
      p.append(slot);
      const reveal = () => { const mk = el("mark", "rev", part.m); slot.replaceChildren(mk); };
      const mask = () => {
        const b = el("button", "tape", (part.label ? part.label + " · " : "") + "点题句，点开");
        b.type = "button"; b.dataset.mask = part.id;
        b.setAttribute("aria-label", "揭开第" + (pi + 1) + "段被遮住的句子");
        b.addEventListener("click", () => { s.open[part.id] = 1; save(); reveal(); checks.append(checkRow(a, part, pi)); updateProg(a); renderNavLite(); });
        slot.replaceChildren(b);
      };
      if (s.open[part.id]) { reveal(); checks.append(checkRow(a, part, pi)); } else mask();
    }
    box.append(p, checks);
    art.append(box);
  });

  const w = el("section", "block");
  w.append(el("h2", "", "意外的措辞"), el("div", "hint", "读到“换我会写别的”的地方就记下来，攒一批再回看。"));
  const ta = el("textarea"); ta.id = "words"; ta.placeholder = "例：充斥着较量；固守过去的经验"; ta.value = s.words || "";
  let tmr; ta.addEventListener("input", () => { clearTimeout(tmr); tmr = setTimeout(() => { s.words = ta.value; save(); }, 500); });
  w.append(ta);
  art.append(w);

  if ((a.items || []).length) renderItems(a, s, art);
  else if (a.judgments && a.judgments.length) art.append(oldJudgments(a, s, (a.kind === "cs" ? "常识" : "政治理论") + " · 判断题"));

  const tools = el("div", "tools");
  const again = el("button", "", "重新遮住，再读一遍"); again.type = "button";
  again.addEventListener("click", () => {
    if (em === "q") s.qans = {}; else if (em === "w") s.wopen = {}; else s.open = {};
    save(); renderArticle(a); renderNavLite();
  });
  tools.append(again, el("span", "kbd", em === "q" ? "快捷键：空格 打开下一处 · A–D 或 1–4 选项 · ← → 上一篇 / 下一篇" : "快捷键：空格 揭开下一处 · ← → 上一篇 / 下一篇"));
  art.append(tools);

  const list = ordered(); const i = list.findIndex(x => x.id === a.id);
  const pager = el("div", "pager");
  const prev = el("button", "", "← 上一篇"); prev.type = "button"; prev.disabled = i <= 0;
  const next = el("button", "", "下一篇 →"); next.type = "button"; next.disabled = i < 0 || i >= list.length - 1;
  prev.addEventListener("click", () => openArticle(list[i - 1].id));
  next.addEventListener("click", () => openArticle(list[i + 1].id));
  pager.append(prev, next);

  wrap.append(how, legend, art, pager);
  main.replaceChildren(wrap);
  updateProg(a);
}

function checkRow(a, part, pi) {
  const s = st(a.id);
  const row = el("div", "check");
  row.append(el("span", "which", "第" + (pi + 1) + "段" + (part.label ? "（" + part.label + "）" : "") + "：我的一句话和原句比——"));
  const chips = el("div", "chips"); chips.setAttribute("role", "group");
  for (const [k, name] of TAGS) {
    const b = el("button", "", name); b.type = "button";
    b.setAttribute("aria-pressed", s.tags[part.id] === k ? "true" : "false");
    b.addEventListener("click", () => {
      if (s.tags[part.id] === k) delete s.tags[part.id]; else s.tags[part.id] = k;
      for (const c of chips.children) c.setAttribute("aria-pressed", c === b && s.tags[part.id] ? "true" : "false");
      save(); updateProg(a); renderNavLite();
    });
    chips.append(b);
  }
  row.append(chips);
  return row;
}
function updateProg(a) {
  const s = st(a.id); const p = document.getElementById("prog"); if (!p) return;
  const em = effMode(a);
  if (em === "q") {
    const done = a.q.filter(q => s.qans[q.id] != null);
    const ok = done.filter(q => s.qans[q.id] === q.answer).length;
    p.textContent = "词句题已答 " + done.length + " / " + a.q.length + (done.length ? " · 答对 " + ok : "");
    return;
  }
  if (em === "w") { const t = a.w.filter(w => s.whit[w.id] != null).length; p.textContent = "词句已对照 " + t + " / " + a.w.length; return; }
  const n = masksOf(a).length; const t = masksOf(a).filter(m => s.tags[m.id]).length;
  p.textContent = "已对照 " + t + " / " + n;
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
  ctl.card.hidden = false; fillCard(a, s, ctl, false);
  activeQ = { a, s, ctl };
  const first = ctl.card.querySelector(".opts button"); if (first) first.focus({ preventScroll: true });
  ctl.card.scrollIntoView({ block: "nearest" });
}
function answerQ(a, s, ctl, i) {
  s.qans[ctl.q.id] = i; save(); activeQ = null;
  paintQ(a, s, ctl); updateProg(a); renderNavLite();
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
  view = "stats"; renderNav();
  const wrap = el("div", "wrap");
  const c = { hit: 0, narrow: 0, level: 0, tail: 0 }; let jr = 0, jt = 0, cr = 0, ct = 0, done = 0;
  let qn = 0, qr = 0, ir = 0, itn = 0;
  const words = [], qmiss = [];
  for (const a of DATA) {
    const s = store[a.id]; if (!s) continue;
    for (const k of Object.values(s.tags || {})) c[k] = (c[k] || 0) + 1;
    if (!(a.items || []).length) (a.judgments || []).forEach((j, i) => { if (s.judg && s.judg[i] != null) { if (a.kind === "cs") { ct++; if (s.judg[i] === j.answer) cr++; } else { jt++; if (s.judg[i] === j.answer) jr++; } } });
    for (const it of a.items || []) { const v = s.iqa && s.iqa[it.id]; if (v == null) continue; itn++; if (it.type === "多选" ? JSON.stringify(v) === JSON.stringify(it.answer) : v === it.answer) ir++; }
    for (const q of a.q || []) { const v = s.qans && s.qans[q.id]; if (v == null || v === -1) continue; qn++; if (v === q.answer) qr++; else qmiss.push([a, q, v]); }
    if (statusOf(a) === "done") done++;
    if (s.words && s.words.trim()) words.push("【" + a.title + "】" + s.words.trim());
  }
  const total = c.hit + c.narrow + c.level + c.tail;
  wrap.append(el("h1", "", "我的记录"));
  const grid = el("div", "stats");
  const card = (n, l, pct) => { const d = el("div", "stat"); const nn = el("div", "n", String(n)); if (pct) nn.append(el("span", "pct", pct)); d.append(nn, el("div", "l", l)); return d; };
  grid.append(card(done + " / " + DATA.length, "读完的篇数"), card(total, "对照过的点题句"));
  for (const [k, name] of TAGS) grid.append(card(c[k], name, total ? Math.round(c[k] * 100 / total) + "%" : ""));
  grid.append(card(qn ? qr + " / " + qn : "0", "新版词句题答对"), card(itn ? ir + " / " + itn : "0", "广东式政治常识题答对"));
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
  if (qmiss.length) {
    const rsec = el("section", "block");
    rsec.append(el("h2", "", "选错的词句题（重点复习）"), el("div", "hint", "原文用词标了出来。看看当时被哪个选项带走了，再读一遍说明。"));
    const list = el("div", "review");
    for (const [a, q, v] of qmiss) {
      const it = el("div", "it");
      const ctx = el("div", "ctx");
      for (const [t, hl] of qContext(a, q)) ctx.append(hl ? el("mark", "wrev", t) : document.createTextNode(t));
      it.append(ctx, el("div", "", "你选了 " + LETTERS[v] + "．" + q.options[v] + "；原文 " + LETTERS[q.answer] + "．" + q.options[q.answer]), el("div", "", q.note));
      const src = el("a", "src", "【" + a.title + "】第" + q.p + "段"); src.href = "#" + a.id;
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
      const src = el("a", "src", "【" + a.title + "】第" + w.p + "段"); src.href = "#" + a.id;
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
  copy.addEventListener("click", async () => { try { await navigator.clipboard.writeText(words.join("\n")); copy.textContent = "已复制"; } catch (e) { const r = document.createRange(); r.selectNodeContents(pre); const sel = getSelection(); sel.removeAllRanges(); sel.addRange(r); copy.textContent = "已选中，按 Ctrl+C 复制"; } });
  wsec.append(pre, copy);
  wrap.append(wsec);
  const bsec = el("section", "block");
  bsec.append(el("h2", "", "备份与恢复"), el("div", "hint", "记录保存在这台电脑的浏览器里。换电脑或清理浏览器数据前，先导出备份。"));
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
  view = "ref"; renderNav();
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
  const b = document.createElement("button"); b.type = "button"; b.dataset.src = "试点"; b.textContent = "新版"; b.setAttribute("aria-pressed", "false");
  seg.prepend(b);
  const head = document.querySelector(".nav-head");
  const note = el("div", "pilot-note", META.note || "");
  if (META.note) head.append(note);
})();

document.querySelectorAll("[data-order]").forEach(b => b.addEventListener("click", () => { order = b.dataset.order; saveUi(); renderNav(); }));
document.querySelectorAll("[data-src]").forEach(b => b.addEventListener("click", () => { srcFilter = b.dataset.src; saveUi(); renderNav(); }));
document.getElementById("q").addEventListener("input", e => { query = e.target.value; renderNav(); });
document.getElementById("go-stats").addEventListener("click", renderStats);
document.getElementById("go-1310").addEventListener("click", render1310);
document.addEventListener("keydown", e => {
  if (view !== "article" || e.target.matches("textarea, input")) return;
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  const list = ordered(); const i = list.findIndex(x => x.id === current);
  if (activeQ && !activeQ.ctl.card.hidden && activeQ.s.qans[activeQ.ctl.q.id] == null) {
    const k = e.key.toUpperCase();
    const idx = "ABCD".indexOf(k) >= 0 ? "ABCD".indexOf(k) : "1234".indexOf(e.key);
    if (idx >= 0 && e.key.length === 1) { const { a, s, ctl } = activeQ; answerQ(a, s, ctl, idx); e.preventDefault(); return; }
  }
  if (e.key === "ArrowRight" && i >= 0 && i < list.length - 1) { openArticle(list[i + 1].id); e.preventDefault(); }
  else if (e.key === "ArrowLeft" && i > 0) { openArticle(list[i - 1].id); e.preventDefault(); }
  else if (e.key === " ") {
    if (e.target.closest && e.target.closest(".pick")) return;
    const a = byId[current]; const em = a ? effMode(a) : "sent";
    const b = document.querySelector(em === "sent" ? "button.tape" : "button.blank");
    if (b) { b.click(); e.preventDefault(); }
  }
});

const visibleNow = ordered();
const start = (location.hash && byId[location.hash.slice(1)]) ? location.hash.slice(1) : (current && byId[current] ? current : (visibleNow[0] || DATA[0]).id);
openArticle(start);
