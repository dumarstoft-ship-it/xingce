# 词句新版（试点中）

把"盖句精读"网页的"遮词句"模式重做：

- 遮词改成选词填空的样子，一题 1–3 个空，配 A–D 四个选项，正确项是原文用词；遮句改成语句填空，正确项是原句。
- 每题附说明：原文为什么最好，陷阱在哪。
- 文末的政治理论、常识题改按广东卷的考法出，有判断、单选、多选三种，每题列出依据并标明依据类型。

先做 11 篇试点，考生看过、确认方向后再铺开到 151 篇。"遮点题句"模式不动。

## 目录

- `试点/`：副 agent 交回的试点结果。`M*.json` 是遮词句，`P*.json` 是政治常识题。只存挖空位置、选项、说明和依据，不存文章全文。
- `scripts/`：
  - `extract_base.py`：从现有的盖句精读网页拆出文章数据（含全文，不要提交）、`ref1310.json` 和网页外壳。
  - `build_v2.py`：把试点结果并进去，生成新网页。
  - `app_v2.js`、`extra.css`、`head.html`：新网页的脚本、样式和外壳（外壳来自考生上传的那版网页，不含文章）。
  - `check_masks.py`、`check_items.py`：检查挖空能否在原文里逐字定位，依据原话能否在原文或已核原话里找到。
  - `make_solver_input.py`：生成不带答案的作答卷，交给没见过答案的 agent 独立作答，用来查答案是否唯一。
  - `test_v2.js`：浏览器实测。
  - `clean_paper.py`：把真题 PDF 的政治理论、常识、言语部分转成文本，空处标成＿＿＿＿。

## 构建

```
python3 -I scripts/extract_base.py 盖句精读旧版.html 底稿目录
python3 -I scripts/build_v2.py --base 底稿目录/data.json --ref 底稿目录/ref1310.json --head 底稿目录/head.html \
    --css scripts/extra.css --js scripts/app_v2.js --masks 试点/M*.json --items 试点/P*.json \
    --out 盖句精读.html --ver <版本号> --note "<目录栏上的说明>"
node scripts/test_v2.js <网页绝对路径> <截图目录>
```

网页里有文章全文，只单独发给考生，不放进仓库。
