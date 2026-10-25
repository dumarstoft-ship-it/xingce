# D04-math-2-v09 网约车两条路线费用比较
from fractions import Fraction as F
def fare(km, kmh, toll):
    minutes = F(km, kmh) * 60
    return 10 + 2 * max(0, km - 3) + F(1, 2) * minutes + toll
hw = fare(30, 60, 10)
city = fare(24, 24, 0)
if city < hw:
    ans = ('市区', hw - city)
else:
    ans = ('高速', city - hw)
print('highway =', hw, 'city =', city, ans)
options = {'A': ('市区', 7), 'B': ('市区', 12), 'C': ('市区', 22), 'D': ('高速', 3)}
hits = [k for k, v in options.items() if v[0] == ans[0] and v[1] == ans[1]]
assert len(hits) == 1, hits
print(hits[0])
