import pickle, sys
out = pickle.load(open(sys.argv[1], 'rb'))
N = 1440
for label, (cx, cy, R, prof) in out.items():
    # print boundary candidates: angles where dark fraction > 0.8 (radial lines) 
    cls = []
    for d, m, w in prof:
        if d > 0.85: c = 'LINE/BLACK'
        elif m > 0.7: c = 'gray'
        elif w > 0.97: c = 'white'
        elif d > 0.3: c = 'hatch'
        elif d > 0.1: c = 'grid'
        else: c = 'dots'
        cls.append(c)
    # run-length encode
    runs = []
    start = 0
    for k in range(1, N+1):
        if k == N or cls[k] != cls[start]:
            runs.append((cls[start], start*360/N, k*360/N)); start = k
    print(label)
    for c, s, e in runs:
        if e - s >= 0.5:
            print(f'   {c:12s} {s:7.2f} -> {e:7.2f}  width {e-s:6.2f} deg = {(e-s)/3.6:5.2f}%')
