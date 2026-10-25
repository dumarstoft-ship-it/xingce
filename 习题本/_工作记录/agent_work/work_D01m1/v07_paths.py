# Explore error paths for the rewritten v07: first = T/3 - 20; rest = T - first; second = 3/5*rest + 6; second = T/2
from fractions import Fraction as F
def solve(second_of_T):
    # second_of_T(T) - T/2 is linear in T; solve exactly
    f0 = second_of_T(F(0)) - 0; f1 = second_of_T(F(1)) - F(1, 2)
    a = f1 - f0
    if a == 0: return None
    T = -f0 / a
    return T
paths = {
 'correct':                 lambda T: F(3,5)*(T - (T/3 - 20)) + 6,
 '20 not x3/5 (260?)':      lambda T: F(3,5)*(2*T/3) + 20 + 6,
 'forgot +6 (120?)':        lambda T: F(3,5)*(T - (T/3 - 20)),
 'forgot 20 in rest (60?)': lambda T: F(3,5)*(2*T/3) + 6,
 'sign 多6 as 少6':          lambda T: F(3,5)*(T - (T/3 - 20)) - 6,
 '6 also x3/5':             lambda T: F(3,5)*(T - (T/3 - 20) + 6),
 'rest sign (2T/3-20)':     lambda T: F(3,5)*(2*T/3 - 20) + 6,
 '3/5 of total':            lambda T: F(3,5)*T + 6,
 'rest = T/3+20 (paid/remain swap)': lambda T: F(3,5)*(T/3 + 20) + 6,
}
for name, fn in paths.items():
    T = solve(fn)
    first = T/3 - 20 if T is not None else None
    print(f'{name:36s} T={T}  first={first}')
# 'set second = x, total = 2x, forget to double' -> answer x
x = solve(paths['correct']) / 2
print('second payment (forgot to double) =', x)
