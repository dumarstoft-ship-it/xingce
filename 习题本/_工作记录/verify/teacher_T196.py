# T196（2013江苏A）89吨货物，大卡车载7吨耗油14升/次，小卡车载4吨耗油9升/次，运完的最小耗油量。
GOODS, (BIG_CAP, BIG_OIL), (SMALL_CAP, SMALL_OIL) = 89, (7, 14), (4, 9)
OPTS = {'A': 141, 'B': 162, 'C': 181, 'D': 193}
best = min(BIG_OIL * b + SMALL_OIL * s
           for b in range(GOODS // BIG_CAP + 2)
           for s in range(GOODS // SMALL_CAP + 2)
           if BIG_CAP * b + SMALL_CAP * s >= GOODS)
hits = [k for k, v in OPTS.items() if v == best]
assert len(hits) == 1, (best, hits)
print('min oil =', best)
print(hits[0])
