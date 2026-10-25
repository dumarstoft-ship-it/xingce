# 核对各题干扰项确实来自所述错误路径
from math import comb as C, factorial as F, perm as A
from itertools import product
chk = {}
# v01 定序
chk['v01'] = dict(right=F(6)//F(3), only_C63=C(6,3), div3=F(6)//3, none=F(6))
# v02 插入
chk['v02'] = dict(right=6*7, gaps_fixed=6*6, not_adjacent=A(6,2), choose_only=C(7,2))
# v03 旗
tot = F(6)//(F(3)*F(2)); top=F(5)//(F(2)*F(2)); both=F(4)//F(2)
chk['v03'] = dict(right=3*4, ie=tot-top-top+both, yellow_distinct=A(3,2)*4, miss_YY=2*4, total=tot, top=top, both=both)
# v04 路径
chk['v04'] = dict(right=C(7,3)-C(3,1)*C(4,2), through=C(3,1)*C(4,2), add=C(7,3)-(C(3,1)+C(4,2)), total=C(7,3))
# v05
g = C(6,1)*C(5,2)*C(3,3)
s411 = C(6,4)*C(2,1)//2*6; s222 = F(6)//(F(2)**3)
chk['v05'] = dict(right=g*6, fixed=g, times3=g*3, all_surj=s411+g*6+s222, ie=3**6-3*2**6+3)
# v06
chk['v06'] = dict(right=3*C(4,2), group_only=C(4,2)//2, extra_div=3*C(4,2)//2, miss_step1=C(4,2))
# v07
a = C(5,3)*6; b = C(5,2)*C(3,2)//2*6
chk['v07'] = dict(right=a+b, s311=a, s221=b, no_div=C(5,3)*C(2,1)*6 + C(5,2)*C(3,2)*6, first_each=A(5,3)*9, ie=3**5-3*2**5+3)
# v08
tot = 7*5*3; meet = 5*3
chk['v08'] = dict(right=6*15, ie=tot-meet, meet_nodiv=tot-C(6,2)*C(4,2)*C(2,2), double=tot-2*meet, total=tot,
                  hard=C(8,2)*C(6,2)*C(4,2)*C(2,2)//F(4))
# v09
parts = {tuple(sorted(t)) for t in product(range(13), repeat=3) if sum(t)==12 and min(t)>=2}
chk['v09'] = dict(right=C(8,2), atleast1=C(11,2), pre2_then1=C(5,2), unordered=len(parts))
# v10
even = sum(s-1 for s in (8,6,4,2)); odd = sum(s-1 for s in (9,7,5,3))
chk['v10'] = dict(right=even, odd=odd, total=C(9,2), half=C(9,2)//2, s_ways=sum((8,6,4,2)))
# v11
base = C(9,3); over = 4*C(5,3)
wrong_upper = 4*C(1+3,3)   # 误把预分后的上限当 4（超限=再多拿≥5个）
chk['v11'] = dict(right=base-over, no_upper=base, over_once=base-C(5,3), upper_not_reduced=base-wrong_upper, over=over)
for k, v in chk.items(): print(k, v)
