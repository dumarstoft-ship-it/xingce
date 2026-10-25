# D06-math-2-v10: 20 tickets: 1 x 200, 3 x 50, 6 x 10, rest 0. Expected prize of one random ticket.
from fractions import Fraction as F

tickets = [200] * 1 + [50] * 3 + [10] * 6
tickets += [0] * (20 - len(tickets))
assert len(tickets) == 20
E = F(sum(tickets), len(tickets))

opts = {'A': F(205, 10), 'B': F(410, 10), 'C': F(650, 10), 'D': F(867, 10)}
hit = [k for k, v in opts.items() if v == E]
assert len(hit) == 1, (E, hit)
print('E =', float(E))
print(hit[0])
