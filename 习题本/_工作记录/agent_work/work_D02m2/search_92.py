# 2-9-2: 甲乙合作N天可完成; 合作a天后乙退出, 甲单独若干天(s), 乙回来再合作J天完工; 总工期推迟d天. 求甲单独T.
from fractions import Fraction as F
for N in range(12,37):
    for a in range(2,9):
        for J in range(3,16):
            for d in range(1,7):
                s = N + d - a - J          # 乙缺席天数
                if s<=0: continue
                left = 1 - F(a+J, N)       # 甲单独 s 天完成的份额
                if left<=0: continue
                T = s/left                 # 甲单独天数
                if T.denominator!=1: continue
                T=int(T)
                if T<=N: continue
                rB = F(1,N)-F(1,T)
                if rB<=0 or rB.numerator!=1: continue
                TB = rB.denominator
                # error paths
                e_delay_as_absence = d/left            # 把推迟d天当缺席天数
                e_forget_a = s/(1-F(J,N))              # 合作只算后J天
                errs = {'absence=d':e_delay_as_absence,'forget_a':e_forget_a,'T乙':TB}
                good = [k for k,v in errs.items() if v>N and v!=T and F(v).denominator==1]
                print(N,a,J,d,'s=',s,'T甲=',T,'T乙=',TB, {k:str(v) for k,v in errs.items()}, good)
