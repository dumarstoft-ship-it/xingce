from fractions import Fraction as F
import itertools

def inter(c1, c2):
    (a1, b1, r1), (a2, b2, r2) = c1, c2
    det = a1*b2 - a2*b1
    if det == 0: return None
    x = F(r1*b2 - r2*b1, det); y = F(a1*r2 - a2*r1, det)
    return (x, y)

def feas(p, cons):
    x, y = p
    return x >= 0 and y >= 0 and all(a*x + b*y <= r for a, b, r in cons)

out = []
for S in range(40, 130, 10):
    for (a1, b1) in [(2,1),(3,1),(3,2)]:
        for (a2, b2) in [(1,2),(1,3),(2,3)]:
            for W in range(S, 4*S, 10):
                for L in range(S, 4*S, 10):
                    area = (1, 1, S); wat = (a1, b1, W); lab = (a2, b2, L)
                    cons = [area, wat, lab]
                    P_wl = inter(wat, lab); P_aw = inter(area, wat); P_al = inter(area, lab)
                    if None in (P_wl, P_aw, P_al): continue
                    if any(v.denominator != 1 or v < 0 for P in (P_wl, P_aw, P_al) for v in P): continue
                    if feas(P_wl, cons): continue           # water∩labor must be infeasible
                    if not (P_wl[0] + P_wl[1] > S): continue
                    if not feas(P_aw, cons) or not feas(P_al, cons): continue
                    # y-axis endpoint
                    ymax = min(F(S), F(W, b1), F(L, b2)); xmax = min(F(S), F(W, a1), F(L, a2))
                    if ymax.denominator != 1 or xmax.denominator != 1: continue
                    if not (ymax == F(L, b2)): continue    # labor limits only-y
                    for p1 in range(2, 10):
                        for p2 in range(p1+1, 2*p1+3):
                            f = lambda P: p1*P[0] + p2*P[1]
                            verts = [(F(0),F(0)), (xmax, F(0)), P_aw, P_al, (F(0), ymax)]
                            vals = [f(v) for v in verts]
                            best = max(vals)
                            if vals.count(best) != 1 or f(P_al) != best: continue
                            if not (f(P_wl) > best): continue
                            # water∩labor is the largest among all pair intersections incl. axes
                            dis = [f(P_wl), f(P_aw), f((F(0), ymax))]
                            all_y = p2 * S
                            vals_opts = [best] + dis
                            if len(set(vals_opts)) < 4: continue
                            if all_y in vals_opts: continue
                            out.append((S, (a1,b1,W), (a2,b2,L), (p1,p2), P_al, best, P_wl, f(P_wl), P_aw, f(P_aw), ymax, f((F(0),ymax)), all_y))

print(len(out))
for o in out[:400:7]:
    S, w, l, p, Pal, best, Pwl, fwl, Paw, faw, ym, fy, ally = o
    print('S', S, 'water', w, 'labor', l, 'p', p, 'opt', tuple(map(int,Pal)), int(best), '| WL', tuple(map(int,Pwl)), int(fwl), '| AW', tuple(map(int,Paw)), int(faw), '| y-only', int(ym), int(fy), '| all-y', ally)
