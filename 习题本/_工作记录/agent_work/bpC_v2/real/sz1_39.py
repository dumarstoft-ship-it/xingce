# 2020SZ1-39 课程表：上午4节(AM1-4)，下午3节(PM1-3)，中午休息
from itertools import product
C=['语','英','数','历','地','物','化','生','道','体']
allowed=['语','英','数','物','化','体']   # 条件(5)
def check(sched, adj_mode):
    am,pm=sched[:4],sched[4:]
    # (1) 只有一门课程安排了两节，上、下午各一节；其余至多一节
    cnt={c:sched.count(c) for c in set(sched)}
    twos=[c for c,k in cnt.items() if k==2]
    if any(k>2 for k in cnt.values()) or len(twos)!=1: return False
    t=twos[0]
    if not (t in am and t in pm): return False
    # (2) 语文紧挨数学（同一半天内相邻）
    def adjacent_pairs(half):
        return [(half[i],half[i+1]) for i in range(len(half)-1)]
    pairs=adjacent_pairs(am)+adjacent_pairs(pm)
    yu_pos=[i for i,c in enumerate(sched) if c=='语']
    if not yu_pos or '数' not in sched: return False
    def adj_to_shu(i):
        half=(range(0,4) if i<4 else range(4,len(sched)))
        return any(j in half and abs(j-i)==1 and sched[j]=='数' for j in range(len(sched)))
    if adj_mode=='每节语文都紧挨数学':
        if not all(adj_to_shu(i) for i in yu_pos): return False
    else:
        if not any(adj_to_shu(i) for i in yu_pos): return False
    # (3) 上了体育
    if '体' not in sched: return False
    # (4) 物理、化学都上了，且都在下午
    for c in ('物','化'):
        if c not in sched: return False
        if c in am: return False
    return True
for npm in (3,2):
    for mode in ('每节语文都紧挨数学','至少一节语文紧挨数学'):
        S=[s for s in product(allowed,repeat=4+npm) if check(list(s),mode)]
        A=all(len(set(s))==5 for s in S)
        B=all('体' in s[:4] for s in S)
        Cc=any(s[4]=='语' for s in S)
        D=any(s.count('化')==2 for s in S)
        print(f'下午{npm}节 | {mode} | 解数{len(S)} | A上了5门(必然?){A} B上午体育(必然?){B} C下午第一节语文(可能?){Cc} D两节化学(可能?){D}')
