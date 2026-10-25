# T217（2019辽宁）礼物卡1~100：2的倍数领2枝，3的倍数领3枝，既是2又是3的倍数可重复领，其他领1枝。共需多少枝。
CARDS = range(1, 101)
OPTS = {'A': 215, 'B': 232, 'C': 312, 'D': 416}
total = 0
for n in CARDS:
    got = 0
    if n % 2 == 0:
        got += 2
    if n % 3 == 0:
        got += 3
    total += got if got else 1
hits = [k for k, v in OPTS.items() if v == total]
assert len(hits) == 1, (total, hits)
print('roses =', total)
print(hits[0])
