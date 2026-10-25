# Pending items (main agent notes)

## New real questions not yet in blueprints (cls/out_new_batch.jsonl, 119 items)
- Papers: 2021HB, 2021SC0327, 2022SZ, 2026GZ (3.14联考, answers are 机构估分 — GZ-50/51/53/60 keys look wrong), 2026HB (no answers → self-solve), 2026JS (answers read from gray highlights → answer_fixes).
- Integrate into later days of each module (replace variant slots in round 2/3 days), not pilot days.
- Missing questions visible in crops but not in DB: 2021SC0327-77, 2021HB-105, 2022SZ-37/38, 2022SZ-53, 2026JS-63.

## Blueprint issue lists to act on
- M03: 2020SZS-29 stem says 15天 but official solution uses 10天 → exclude (use 备1) on day 30; 2022SC1-46 missing fraction → exclude (备2) day 30.
- M07: issues list (20 items) — crops fixed by re-crop; re-check 2023HB-75 figure, 2026CQ-63 crop contains 【答案】 line.
- L04: 2021GK-107 crop fixed via override; 2022SC1-78 crop bottom has next question half-line (check after re-crop).
- Check every blueprint's "issues" before assembling the corresponding day.

## Rendering
- Option fractions → \dfrac (done). Group titles not shown on question pages (done); kaofa/technique/source shown in 解析.
- Duplicate 参考用时 guarded (done).

## Answer leaks in question crops (found 2026-10-25 after resume)
- 2026CQ / 2026GZ printed "【答案】X" under each question → cut via scripts/fix_answer_leaks.py (73 crops re-made; overrides.json has cut_before_re; build_db.apply_overrides handles it).
- 2026JS marks the correct option with a gray highlight. scripts/fix_js_highlight.py removes most of it, but faint traces remain → when 2026JS questions are scheduled, retype them in db/real_overrides.json (stem + options) instead of using the crop. Original crops backed up in crops/js_backup/.
- 2026CQ stems contain "****" masks (网友回忆版). Retype with completed stems in db/real_overrides.json when scheduled (done: CQ-61, CQ-62). Scheduled later: CQ-56 (M01 d15), CQ-57 (M01 d39), CQ-63 (M07 d20), CQ-65/66 (M08 d42).
- Original question numbers are whited out in crops/real2_nonum/ (scripts/mask_qnum.py); render uses those when present.

## User decision 2026-10-25: NO variants for 逻辑判断 and 综合推理
- "逻辑判断和综合推理不要自编了" → logic and 综合推理 use real questions only. Math keeps verified variants.
- Stopped: logic/C blueprint agents (L01 L02 L05 L06 L07 C), D02 logic generation, D03 logic review. gen/D03_logic_*.json (19 variants) are NOT to be used (moved to gen_unused/).
- Pool now: 逻辑 435, 综合推理 75 (54 papers; ~8 logic and ~1.4 综合 per paper after dedupe).
- Asked the user to pick daily volume / whether to upload more papers (recommendation: 逻辑 20/day + 综合推理 3/day; needs ~50 more papers for logic, ~15 江苏/深圳 papers for 综合).

## From M01 blueprint (2026-10-25)
- real_overrides added: 2021GK-67 (crop has C/D swapped vs official key → typed stem in original order), 2026CQ-56/57 (masked stems + self-written 解析), 2020HB-75 (fraction cut in crop → typed), 2021GK-64 / 2022ZJA-60 (extra notes).
- j crops to re-crop (top half-line cut, bottom shows next question's answer): 2022ZJA-60, 2022ZJA-63 (day 15), 2024ZJA-64 (day 29); 2023GK-74 j crop right side cut (day 29); 2021ZJA-61 q crop fraction top clipped (day 15).
- 2026HB-71 duplicates 2026CQ-56 (keep one).

## Teacher bank (忧郁牛牛 26数量关系笔记, uploaded 2026-10-25)
- teacher/examples.json (267 parsed examples; scripts/teacher_parse.py, teacher_match.py, teacher_crops.py) → teacher/bank_B1..B6.json + bank_B6x.json (16 extra geometry examples found inside long crops). 272 usable, all answers verified (verify/teacher_*.py). Teacher's errors found: T025 answer (44 not 42), T012 stem contradiction (fixed), many solution typos (in issues).
- Possible missed examples: sections 三/五/八/九/十二/十四 have 1–3 more white boxes than parsed examples — check later.
- Teacher items that match DB questions (db_match) should be used via the DB crop + official 解析 (+ teacher method as note).

## Week-1 math 去水 (2026-10-25): conflicts to clear when building days 8–42
- Every real added to week 1 via db/math_harden.json add_real was pulled from a later day's plan → when assembling days 8–42, skip any real already used in days 1–7 (build a global used-set from the delivered week-1 item lists) and refill those slots.
- D01 pulled seeds from days 15/29/39 → re-plan 〔15-2-2〕〔15-9-1〕〔15-10-2〕〔15-14-1〕〔29-4-2〕〔29-7-2〕〔29-15-2〕〔39-6-1〕〔39-9-2〕〔39-12-2〕〔39-15-2〕.
- D04 new variants borrowed M05 skeletons of days 18/32 (报童、三套餐、分段变动成本、两级补贴、订货批量、差量反推分界) → change those two days.
- D07 used 2024SD-60 (teacher T261; DB module M04) → mark as used in M04 later rounds.
- New-variant overlaps found by the blind reviews (revh_A, revh_B):
  - D02-h-v01 was the 2026ZJA-56 template (day 16 real; 〔30-5-2〕 same seed) → v01 being rewritten; re-check day 16/30 anyway.
  - D02-h-v03 ↔ 〔30-7-1〕 (中途减牛/减泵); day 16 has 中途增开窗口.
  - D03-h-v01 ↔ 〔17-5-3〕; D03-h-v04 ↔ 〔17-15-1〕; D03-h-v02 ↔ 〔31-6-2〕; D03-h-v03 ↔ 〔40-12-2〕.
  - D07-h-v01 ↔ 〔42-5-1〕; D07-h-v02 ↔ day-42 real 2026CQ-65, 〔42-4-1〕, 〔21-4-5〕.
  - D06-h-v08 box data (3+2 / 2+3) = 〔34-11-1〕 → change day 34's data/direction.
- Teacher figures: SVG redraws in teacher/bank_B6x.json; T255x1 had the teacher's added sector edge (dashed r to the intersection) → removed. Check every teacher figure against the original exam figure before use (teacher crops carry handwritten auxiliary lines).
