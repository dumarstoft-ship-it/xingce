# real 2026ZJA-98  6人获奖：一等1人、二等2人、三等3人，满足(1)(2)(3)，哪项一定为真？
from itertools import permutations

PEOPLE = ['琪琪', '依依', '冰冰', '鑫鑫', '磊磊', '静静']
sols = []
for prizes in set(permutations([1, 2, 2, 3, 3, 3])):
    g = dict(zip(PEOPLE, prizes))
    # (1) 除非琪琪二等奖，否则冰冰一等奖：琪琪≠2 → 冰冰=1
    if g['琪琪'] != 2 and g['冰冰'] != 1:
        continue
    # (2) 琪琪或依依有人二等奖 → 鑫鑫三等奖且静静二等奖
    if (g['琪琪'] == 2 or g['依依'] == 2) and not (g['鑫鑫'] == 3 and g['静静'] == 2):
        continue
    # (3) 鑫鑫三等奖 → 冰冰二等奖且依依不是三等奖
    if g['鑫鑫'] == 3 and not (g['冰冰'] == 2 and g['依依'] != 3):
        continue
    sols.append(g)

for g in sols:
    print(g)
assert sols
OPTS = {
    'A': lambda g: g['冰冰'] != 1,
    'B': lambda g: g['琪琪'] == 2,
    'C': lambda g: g['鑫鑫'] != 1,
    'D': lambda g: g['磊磊'] == 3,
}
hits = [k for k, f in OPTS.items() if all(f(g) for g in sols)]
assert len(hits) == 1, hits
print(hits[0])
