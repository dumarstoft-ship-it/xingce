# Reverse-engineer which typical wrong method lands on each distractor (blind, before key).
from fractions import Fraction as F
from math import comb

def show(tag, val):
    print(f"   {tag:<60s} = {val}  ({float(val):.4f})")

print("v01 options 1/7, 4/7*, 13/21, 2/3")
show("forgot x2x2: C(5,1)C(4,2)/C(10,4)", F(5 * comb(4, 2), comb(10, 4)))
show("correct: C(5,1)C(4,2)*4/C(10,4)", F(5 * comb(4, 2) * 4, comb(10, 4)))
show("'at least one pair' 1-C(5,4)*16/210", 1 - F(comb(5, 4) * 16, 210))
show("overcount C(5,1)C(8,2)/210", F(5 * comb(8, 2), 210))

print("v02 options 58.2%, 60%, 64%, 70%*")
show("day-by-day independent 1-(1-(2/5)^2)^5", 1 - (1 - F(2, 5) ** 2) ** 5)
show("exactly one common day 2*3/10", F(6, 10))
show("Liu's two picks w/ replacement 1-(3/5)^2", 1 - F(3, 5) ** 2)
show("correct 1-C(3,2)/C(5,2)", 1 - F(3, 10))

print("v03 options 27%, 33%, 39%*, 76%")
A = {0: F(4, 25), 1: F(12, 25), 2: F(9, 25)}
B = {0: F(1, 4), 1: F(1, 2), 2: F(1, 4)}
show("only A=2 case", A[2] * (B[0] + B[1]))
A_bad = {0: F(4, 25), 1: F(6, 25), 2: F(9, 25)}  # forgot C(2,1)
show("forgot C(2,1) for A=1", A_bad[1] * B[0] + A_bad[2] * (B[0] + B[1]))
show("correct", A[1] * B[0] + A[2] * (B[0] + B[1]))
show("used >= instead of >", sum(A[a] * B[b] for a in A for b in B if a >= b))

print("v04 options 17.28%*, 28.80%, 34.56%, 82.08%")
p, q = F(3, 5), F(2, 5)
show("correct C(3,1)p q^2 * p", 3 * p * q * q * p)
show("forgot final p: C(3,1) p q^2  (== P(N=3) too)", 3 * p * q * q)
show("P(N=3) = C(2,1)pq*p", 2 * p * q * p)
show("no 'last must succeed': C(4,2)p^2q^2", comb(4, 2) * p * p * q * q)
show("P(N<=4)", 1 - q ** 4 - 4 * p * q ** 3)

print("v05 options 9/50, 9/29*, 3/7, 9/20")
show("unconditional P(re-path & final)", F(6, 10) * F(3, 10))
show("correct .18/(.4+.18)", F(18, 100) / (F(40, 100) + F(18, 100)))
show("forgot x0.6: .3/(.4+.3)", F(3, 10) / (F(4, 10) + F(3, 10)))
show("ratio re/init .18/.4", F(18, 100) / F(40, 100))

print("v06 options 2/3, 20/27, 4/5*, 8/9")
p, q = F(2, 3), F(1, 3)
show("best-of-3 p^3+3p^2q", p ** 3 + 3 * p * p * q)
show("p^2 + 2pq*p (one more point after split)", p * p + 2 * p * q * p)
show("correct p^2/(p^2+q^2)", p * p / (p * p + q * q))
show("1-q^2", 1 - q * q)
show("truncated after 4 points", p * p + 2 * p * q * p * p)

print("v07 options 85%, 86%, 87.5%, 89%*")
show("by buildings (32+19)/60", F(32 + 19, 60))
show("weights swapped", (F(4, 5) * 1440 + F(19, 20) * 960) / 2400)
show("simple mean", (F(4, 5) + F(19, 20)) / 2)
show("correct by households", (F(4, 5) * 960 + F(19, 20) * 1440) / 2400)

print("v08 options 2/5, 18/35*, 4/7, 3/5")
show("ignore transfer", F(2, 5))
show("assume both moved are science", F(4, 7))
show("P(two science moved)", F(comb(4, 2), comb(5, 2)))
show("pool both boxes (6/10)", F(6, 10))
show("correct (2+8/5)/7", (2 + F(8, 5)) / 7)

print("v09 options 1/3, 4/9, 5/9*, 2/3")
show("unconditional P(A)", F(5, 15))
show("A only | cond", F(4, 9))
show("correct", F(5, 9))
show("double-count both: 6/9", F(6, 9))
show("P(A)+P(B) as P(cond)", F(1, 3) + F(1, 3))
show("intuitive symmetry 1/2 (NOT offered)", F(1, 2))
show("P(both | at least one)", F(1, 9))
show("P(B | A chosen)", F(1, 5))

print("v10 options 96*, 100, 120, 152")
show("correct 0.8*max(100, 0.3*400)", F(4, 5) * max(100, F(3, 10) * 400))
show("conditional after Q1 continue", F(3, 10) * 400)
show("ignores 'clear to 0' : 0.8*(100+0.3*300)", F(4, 5) * (100 + F(3, 10) * 300))
show("stop strategy overall 0.8*100", F(4, 5) * 100)
