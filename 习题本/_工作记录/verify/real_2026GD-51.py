# real 2026GD-51  集约高效 → 资源消耗减少；减少速度非常缓慢 → 不会对经济造成负面影响。可以推出哪项？
from itertools import product

SPEEDS = ['very_slow', 'moderate', 'fast']   # 只在"减少"时有意义

def worlds():
    for J, R, N in product([True, False], repeat=3):
        for sp in (SPEEDS if R else [None]):
            # J 集约高效, R 消耗量减少, sp 减少速度, N 对经济有负面影响
            if J and not R:
                continue                        # 集约高效 → 减少
            if sp == 'very_slow' and N:
                continue                        # 减少得非常缓慢 → 不会有负面影响
            yield J, R, sp, N

W = list(worlds())
assert W
OPTS = {
    'A': lambda J, R, sp, N: R or not J,                    # 没减少 → 没采用集约高效
    'B': lambda J, R, sp, N: J or not R,                    # 没采用集约高效 → 没减少
    'C': lambda J, R, sp, N: (not R) or J,                  # 减少 → 采用了集约高效
    'D': lambda J, R, sp, N: not (R and sp == 'fast') or N, # 减少很快 → 有负面影响
}
valid = [k for k, f in OPTS.items() if all(f(*w) for w in W)]
for k, f in OPTS.items():
    cex = next((w for w in W if not f(*w)), None)
    print(k, '必然成立' if cex is None else f'反例 {cex}')
assert len(valid) == 1, valid
print(valid[0])
