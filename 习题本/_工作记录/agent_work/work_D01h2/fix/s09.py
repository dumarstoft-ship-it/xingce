from fractions import Fraction as F
def pct(x):
    v=x*100
    return int(v) if v.denominator==1 else None
out=[]
for E1 in range(-40,-4):          # 2025 Sep vs Aug (%)
  for E3 in range(-40,-4):        # 2024 Sep vs Aug (%)
    if E1==E3: continue
    for Gp in range(5,81):        # combined YoY (%)
      e1,e3,G=F(E1,100),F(E3,100),F(Gp,100)
      a24=F(100); s24=a24*(1+e3); T=(a24+s24)*(1+G)
      a25=T/(2+e1); s25=a25*(1+e1)
      g9=s25/s24-1; g8=a25/a24-1
      if pct(g9) is None or pct(g8) is None: continue
      vals={'g9':pct(g9),'g8':pct(g8),'G':Gp}
      add=G+(e1-e3); vals['add']=pct(add)
      sb=T/(2-e1); vals['base']=pct(sb/s24-1)          # Aug = Sep*(1-e1)
      ss=T/(2+e1); vals['swap']=pct(ss/s24-1)          # larger share to Sep
      # simple-average error: (g8'+g9')/2=G, (1+g9')=(1+g8')(1+e1)/(1+e3)
      r=(1+e1)/(1+e3); x=(2*(1+G))/(1+r); vals['simp']=pct(x*r-1)
      clean={k:v for k,v in vals.items() if v is not None}
      if vals['add']==vals['g9']: continue
      if vals['G']==vals['g9']: continue
      # need >=3 distinct clean distractors besides g9
      ds={v for k,v in clean.items() if k!='g9' and v!=vals['g9']}
      if len(ds)<3: continue
      nice=sum(1 for e in (E1,E3,Gp) if e%5==0)
      out.append((nice,E1,E3,Gp,clean))
out.sort(key=lambda o:(-o[0],o[1]))
for o in out[:60]: print(o)
print(len(out))
