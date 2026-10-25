# T205（2021上海B）买24套设备，总价为五位数☆579△元（首位、末位模糊），单价为整数元，☆可能是几。
QTY = 24
OPTS = {'A': 3, 'B': 5, 'C': 7, 'D': 9}
cands = {s for s in range(1, 10) for t in range(10) if (s * 10000 + 5790 + t) % QTY == 0}
hits = [k for k, v in OPTS.items() if v in cands]
assert len(hits) == 1, (cands, hits)
print('possible first digits =', sorted(cands))
print(hits[0])
