# T198（2019山东选调）6个空瓶换1瓶啤酒，买了109瓶，不断用空瓶换酒，一共喝了多少瓶（不借瓶）。
BOUGHT, EX = 109, 6
OPTS = {'A': 127, 'B': 128, 'C': 129, 'D': 130}
drunk, empty = BOUGHT, BOUGHT
while empty >= EX:
    new = empty // EX
    drunk += new
    empty = empty % EX + new
hits = [k for k, v in OPTS.items() if v == drunk]
assert len(hits) == 1, (drunk, hits)
print('total drunk =', drunk, 'empties left =', empty)
print(hits[0])
