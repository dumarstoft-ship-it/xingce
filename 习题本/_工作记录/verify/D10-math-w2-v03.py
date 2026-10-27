# D10-math-w2-v03: one repairer fixes 4 machines that broke down at the same moment, one after another
# (no switching in the middle of a repair).  Repair hours and loss per idle hour (10^4 yuan):
#   甲 5 h, 2;  乙 2 h, 1;  丙 6 h, 4;  丁 3 h, 3
# Each machine loses money from the breakdown until it is repaired (its own repair time included).
# Question: the minimum total loss.
# Method: enumerate all 24 repair orders, take the minimum, check it is unique; then match the options.
import itertools

T = {'甲': 5, '乙': 2, '丙': 6, '丁': 3}
W = {'甲': 2, '乙': 1, '丙': 4, '丁': 3}


def loss(order, own=True):
    clock, total = 0, 0
    for m in order:
        start = clock
        clock += T[m]
        total += W[m] * (clock if own else start)
    return total


orders = list(itertools.permutations(T))
vals = {o: loss(o) for o in orders}
best = min(vals.values())
best_orders = [o for o in orders if vals[o] == best]
assert len(best_orders) == 1, best_orders
opt = best_orders[0]

opts = {'A': 43, 'B': 88, 'C': 95, 'D': 101}
hit = [k for k, v in opts.items() if v == best]
assert len(hit) == 1, (best, hit)

# where the distractors come from (documentation only)
spt = tuple(sorted(T, key=lambda m: T[m]))           # shortest repair first
heavy = tuple(sorted(T, key=lambda m: -W[m]))        # largest hourly loss first
wait_only = min(loss(o, own=False) for o in orders)  # forgetting the loss during a machine's own repair
assert spt != opt and heavy != opt
assert [loss(spt), loss(heavy), wait_only] == [opts['D'], opts['C'], opts['A']]
# the optimal order is exactly "repair time / hourly loss" from small to large (adjacent-exchange rule)
assert opt == tuple(sorted(T, key=lambda m: T[m] / W[m]))

print('optimal order', ''.join(opt), 'loss', best, '| SPT', ''.join(spt), loss(spt), '| heavy-first', ''.join(heavy), loss(heavy))
print(hit[0])
