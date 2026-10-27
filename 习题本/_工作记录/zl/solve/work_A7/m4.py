# MK2739X-M2 forex market, cumulative values (亿元) at end of Q1..Q4
T = {
 'spot':        [251553,530709,815697,1090835],
 'spot_c':      [73111,151373,237755,324793],
 'spot_c_buy':  [38822,77406,118495,158951],
 'spot_c_sell': [34289,73967,119260,165843],
 'spot_i':      [178442,379335,577942,766042],
 'fwd':         [11572,24737,38980,52755],
 'fwd_c':       [7717,16827,27182,38516],
 'fwd_i':       [3855,7910,11797,14239],
 'swap':        [409246,870550,1320144,1743899],
 'swap_c':      [16219,31964,43886,55784],
 'swap_i':      [393027,838586,1276258,1688115],
 'opt':         [39967,82667,126201,158238],
 'opt_c':       [11846,21534,34967,44339],
 'opt_i':       [28121,61133,91235,113899],
 'total':       [712339,1508663,2301021,3045727],
}
def q(k): c=T[k]; return [c[0]]+[c[i]-c[i-1] for i in range(1,4)]
# sanity
for i in range(4):
    print("chk col",i, T['spot_c'][i]+T['spot_i'][i]-T['spot'][i], T['fwd_c'][i]+T['fwd_i'][i]-T['fwd'][i],
          T['swap_c'][i]+T['swap_i'][i]-T['swap'][i], T['opt_c'][i]+T['opt_i'][i]-T['opt'][i],
          T['spot'][i]+T['fwd'][i]+T['swap'][i]+T['opt'][i]-T['total'][i], T['spot_c_buy'][i]+T['spot_c_sell'][i]-T['spot_c'][i])
print("Q1 H1 spot share of year", T['spot'][1]/T['spot'][3], " alt: spot H1/total year", T['spot'][1]/T['total'][3])
q4c = sum(q(k)[3] for k in ['spot_c','fwd_c','swap_c','opt_c'])
print("Q2 Q4 bank-customer", [q(k)[3] for k in ['spot_c','fwd_c','swap_c','opt_c']], q4c, "万亿", q4c/1e4)
print("   (wrong: cumulative year bank-customer)", sum(T[k][3] for k in ['spot_c','fwd_c','swap_c','opt_c'])/1e4)
qt=q('total'); print("Q3 quarterly totals", qt, "Q2 qoq", qt[1]/qt[0]-1, " wrong cumulative:", T['total'][1]/T['total'][0]-1)
for k in ['spot_i','fwd_i','swap_i','opt_i']:
    qq=q(k); print("Q4",k, qq, "avg", T[k][3]/4, "Q4>avg?", qq[3]>T[k][3]/4)
b=q('spot_c_buy'); s=q('spot_c_sell'); c=q('spot_c')
print("Q5-1 Q2 buy",b[1],"sell",s[1],"total",c[1],"sell share",s[1]/c[1])
print("Q5-2 opt i/c", T['opt_i'][3]/T['opt_c'][3], "多", T['opt_i'][3]/T['opt_c'][3]-1)
print("Q5-3 fwd_c quarterly", q('fwd_c'))
