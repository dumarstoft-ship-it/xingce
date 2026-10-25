# 验算 T072：合作 3 小时后小李离开、小张一直工作，小李回来后再合作 1 小时完成；小张比小李多干几小时
import sys
from sympy import symbols, Eq, solve, Rational
a = symbols('a', nonnegative=True)   # 小李离开的时长
li, zhang = Rational(1, 8), Rational(1, 10)
li_time = 3 + 1
zhang_time = 3 + a + 1
sol = solve(Eq(li * li_time + zhang * zhang_time, 1), a)
assert len(sol) == 1
diff = zhang_time.subs(a, sol[0]) - li_time
options = {'A': 1, 'B': Rational(3, 2), 'C': 2, 'D': Rational(5, 2)}
ans = [k for k, v in options.items() if v == diff]
assert len(ans) == 1
print(f'小李离开{sol[0]}小时，多干{diff}小时', file=sys.stderr)
print(ans[0])
