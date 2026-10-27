# v02: only-one count
A,B,C=38,34,28; AB,AC,BC=17,12,8; t=5
only=(A-AB-AC+t)+(B-AB-BC+t)+(C-AC-BC+t)
print('v02 only-one', only, ' exactly-two', AB+AC+BC-3*t)
# v03: identity d = mb + n holds in every filling; what do the slips give?
N=140; n=N*15//100; m=20; t3=5
print('v03 correct', (m-t3)+n, '| plug 20 as MB-only:', m+n, '| forget none:', m-t3, '| both slips:', m,
      '| answer+triple:', (m-t3)+n+t3, '| reviewer 26 = n+t3:', n+t3)
# v04: ignore "half"
print('v04 ignore half', 14+10+16)
# v05: parity of exactly-one, and 126-57
vals=sorted({88+79-2*b for b in range(41,58)})
print('v05 feasible exactly-one values', vals[:3],'...',vals[-1], 'all odd:', all(v%2 for v in vals), '| 126-57 =', 126-57)
# v07: union - sum(pairs)
print('v07 union-sumpairs', 15-(2+3+2), '| correct', 15-(7-2*1))
