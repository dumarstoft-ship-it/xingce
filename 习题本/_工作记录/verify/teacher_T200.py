# T200（2019山东选调）新窗户90元/扇，每7扇换下的旧窗户可兑换1扇新窗户；共花16560元，最后剩4扇旧窗户未兑换。
# 求写字楼窗户总数。模拟：装上新窗即换下一扇旧窗，旧窗凑满7扇就兑换。
PRICE, COST, EX, LEFT = 90, 16560, 7, 4
OPTS = {'A': 214, 'B': 218, 'C': 184, 'D': 188}
assert COST % PRICE == 0
new, old, installed = COST // PRICE, 0, 0
while new:
    installed += new
    old += new
    new, old = old // EX, old % EX
assert old == LEFT                      # 与题干"剩余4个旧窗户"吻合
hits = [k for k, v in OPTS.items() if v == installed]
assert len(hits) == 1, (installed, hits)
print('bought =', COST // PRICE, 'total windows =', installed)
print(hits[0])
