# T104 2019甘肃：60人，徒步40、羽毛球38、乒乓球31，三项都报18，问最多多少人都没报
TOTAL, G1, G2, G3, ALL3 = 60, 40, 38, 31, 18
OPTS = {'A': 14, 'B': 15, 'C': 16, 'D': 18}

best, witness = -1, None
for p in range(0, 61):          # 仅徒步+羽毛球
    for q in range(0, 61):      # 仅徒步+乒乓球
        for r in range(0, 61):  # 仅羽毛球+乒乓球
            o1, o2, o3 = G1 - ALL3 - p - q, G2 - ALL3 - p - r, G3 - ALL3 - q - r
            if min(o1, o2, o3) < 0:
                continue
            none = TOTAL - (o1 + o2 + o3 + p + q + r + ALL3)
            if none >= 0 and none > best:
                best, witness = none, (p, q, r, o1, o2, o3)
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1
print('max none =', best, 'witness (p,q,r,o1,o2,o3) =', witness)
print(hits[0])
