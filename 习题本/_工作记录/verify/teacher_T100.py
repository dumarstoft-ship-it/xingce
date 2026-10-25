# T100 2014北京：48人至少参观1个景点；只参观1个=至少参观2个=4×参观3个，求门票数
TOTAL = 48
OPTS = {'A': 48, 'B': 72, 'C': 78, 'D': 84}

sols = []
for three in range(0, TOTAL + 1):
    for two in range(0, TOTAL + 1):          # 恰好参观两个
        one = TOTAL - two - three
        if one < 0:
            continue
        if one == two + three and one == 4 * three:
            sols.append((one, two, three, one + 2 * two + 3 * three))
assert len(sols) == 1, sols
one, two, three, tickets = sols[0]
hits = [k for k, v in OPTS.items() if v == tickets]
assert len(hits) == 1
assert one + 2 * (two + three) == OPTS['B']   # 干扰项："至少两处"都按2张票
print('one/two/three =', one, two, three, 'tickets =', tickets)
print(hits[0])
