# real 2026GD-54  科技馆K、文化馆W、博物馆B、美术馆M；补充哪项可得出"一定去科技馆"？
from itertools import product

def base(K, W, B, M):
    return (not (K and W and B and M)      # 4个场馆不能都去
            and not (W and B)              # (1) 不既去文化馆又去博物馆
            and (M or W)                   # (2) 美术馆、文化馆至少去一个
            and not M)                     # (3) 今年不去美术馆

OPTS = {
    'A': lambda K, W, B, M: K or B,              # 如果不去科技馆，就去博物馆：¬K→B
    'B': lambda K, W, B, M: (not B) or (not K),  # 只有不去科技馆，才去博物馆：B→¬K
    'C': lambda K, W, B, M: K or (not B),        # 只有不去博物馆，才不去科技馆：¬K→¬B
    'D': lambda K, W, B, M: (not B) or (not K),  # 如果去博物馆，就不去科技馆：B→¬K
}

hits = []
for k, f in OPTS.items():
    W_ = [v for v in product([True, False], repeat=4) if base(*v) and f(*v)]
    forced = bool(W_) and all(v[0] for v in W_)
    print(k, '可行方案', [''.join(n for n, x in zip('KWBM', v) if x) for v in W_], '→ 必去科技馆' if forced else '')
    if forced:
        hits.append(k)
assert len(hits) == 1, hits
print(hits[0])
