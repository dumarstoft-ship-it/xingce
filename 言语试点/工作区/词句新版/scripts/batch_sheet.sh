#!/bin/bash
# 用法：batch_sheet.sh B01 [文章id ...]   校验 M_B01.json，组卷到 full/sheets/卷_B01.md（只含给出的文章；不给就是整批），答案存 keys/
SP=/tmp/claude-0/-home-user-xingce/c27c4f14-7f89-5a62-8e0a-9c6994ddaec0/scratchpad
B=$1; shift
python3 -I $SP/tools/check_masks.py $SP/full/out/M_$B.json $SP/full/in | tail -2 || exit 1
TAG=$B
if [ $# -gt 0 ]; then
  TAG=${B}_r$(date +%H%M%S)
  python3 -I - "$SP/full/out/M_$B.json" "$SP/keys/sub_$TAG.json" "$@" <<'PY'
import json, sys
src, out, ids = sys.argv[1], sys.argv[2], set(sys.argv[3:])
r = json.load(open(src))
json.dump({'articles': [a for a in r['articles'] if a['id'] in ids]}, open(out, 'w'), ensure_ascii=False)
PY
  SRC=$SP/keys/sub_$TAG.json
else
  SRC=$SP/full/out/M_$B.json
fi
python3 -I $SP/tools/make_solver_input.py $SP/full/in $SP/full/sheets/卷_$TAG.md $SRC >/dev/null && mv $SP/full/sheets/卷_$TAG.md.key.json $SP/keys/卷_$TAG.key.json && echo "卷：$SP/full/sheets/卷_$TAG.md（$(python3 -c "import json;print(len(json.load(open('$SP/keys/卷_$TAG.key.json'))))") 题）"
