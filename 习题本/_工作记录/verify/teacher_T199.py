# T199 9个空瓶换2瓶汽水，一共喝了263瓶（含空瓶换来的），至少要买多少瓶（不借瓶）。
DRUNK, EX_IN, EX_OUT = 263, 9, 2
OPTS = {'A': 259, 'B': 243, 'C': 221, 'D': 205}


def total_drunk(bought):
    drunk, empty = bought, bought
    while empty >= EX_IN:
        new = (empty // EX_IN) * EX_OUT
        drunk += new
        empty = empty % EX_IN + new
    return drunk


ans = next(n for n in range(1, DRUNK + 1) if total_drunk(n) >= DRUNK)
assert total_drunk(ans) == DRUNK
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('min bought =', ans)
print(hits[0])
