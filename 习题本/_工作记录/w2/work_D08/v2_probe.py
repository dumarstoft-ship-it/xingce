# Probe the scheme-count skeleton: 45x + 75y = 3000, x,y >= 1, optional x >= y
sols = [(x, y) for x in range(1, 100) for y in range(1, 100) if 45 * x + 75 * y == 3000]
print('all positive solutions:', len(sols), sols[:3], '...', sols[-2:])
print('with x >= y:', len([s for s in sols if s[0] >= s[1]]))
print('allowing zeros:', len([(x, y) for x in range(0, 100) for y in range(0, 100) if 45 * x + 75 * y == 3000]))
