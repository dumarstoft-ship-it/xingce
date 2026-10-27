# w2_r1 blind answers (recorded BEFORE opening w2_r1_key.json)

| vid | my answer | one-line reason |
|---|---|---|
| D09-math-w2-v01 | C 45 | worst case = one variety fully taken (甲30) + others capped at min(stock,4): 4+4+4+2 -> 44, +1 = 45 |
| D10-math-w2-v01 | C 16 | vertices: land&labor (20,40)=16万 optimal; water&labor (40,30)=17万 violates land (70>60); land&water (45,15)=13.5万; all-乙 50亩=15万 |
| D10-math-w2-v02 | B 16 | per-unit cost 甲2.5 > 乙2 (万/unit, W=24); cost=48+0.5a<=52 -> 甲 does <=8 units; time=max(a/2,24-a) -> 16 |
| D10-math-w2-v03 | B 88 | Smith rule p/w ascending: 丁1, 丙1.5, 乙2, 甲2.5 -> C=3,9,11,16 -> 9+36+11+32 = 88 (brute force over 24 orders confirms unique) |
| D10-math-w2-v04 | A 458 | tree median: at C the E-F branch holds 22 > 21 = half -> move to E; at E sides 14 / 20 both <=21 -> E; 229 t·km x2 = 458 |
| D12-math-w2-v01 | A 第一 | remove 甲 (400@40): 乙丙丁 avg = 80000/1600 = 50 > 49 > 46 -> 丁 > 50, rank 1; "丁 most orders" is a lure, not needed |

Guessability notes (to check against key):
- Q1: 20/44/45/47 - the only "x, x+1" pair is 44/45 and 20 is an outlier -> both test-taking heuristics point to 45.
- Q4: 43/88/95/101 min question - 43 < sum(p*w)=45 lower bound, quick to exclude; then correct = smallest of the cluster.
- Q5: 458/478/542/654 min question - correct is the smallest of all four (exact pattern the brief warns about). Candidate replacement below 458: 428 (forgot C's own 3 t when moving C->E, or omitted C in the sum).
- Q2, Q3: trap value sits on the "greedy" side (17 for max, 8 for min) -> not guessable.
- Q6: natural option set.
