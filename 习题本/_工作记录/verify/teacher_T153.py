# teacher T153（2022广东县级）管材每层比上层多1根，搬走99根后少了3层且剩余每层少3根，剩10层，求剩余根数
OPTS = {'A': 245, 'B': 265, 'C': 305, 'D': 325}
REMOVED, LOST, CUT, LEFT = 99, 3, 3, 10
sols = []
for top in range(1, 1000):                      # 原最上层根数
    layers = [top + i for i in range(LOST + LEFT)]
    if sum(layers[:LOST]) + CUT * LEFT == REMOVED:
        sols.append((top, sum(x - CUT for x in layers[LOST:])))
print('(原顶层, 剩余) =', sols)
assert len(sols) == 1
hits = [k for k, v in OPTS.items() if v == sols[0][1]]
assert len(hits) == 1, hits
print(hits[0])
