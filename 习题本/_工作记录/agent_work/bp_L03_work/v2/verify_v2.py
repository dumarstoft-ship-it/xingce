# -*- coding: utf-8 -*-
"""Independent checks for the L03 blueprint (v2).
1) Formal-bridging items: model each argument from its stem, add each option as an extra premise and
   test (by exhaustive truth-table / finite-model enumeration) whether the conclusion becomes valid.
   Exactly the intended option must work, and the bare argument must be invalid.
   "大多/大都/多数" statements are modelled as imposing no constraint on the named individual.
2) Numeric items: recompute every number quoted in a data-type idea from the stem data.
run(): returns a list of (name, detail, ok)."""
import itertools

imp = lambda a, b: (not a) or b


def valid_individual(vars_, premises, option, conclusion):
    for vals in itertools.product([False, True], repeat=len(vars_)):
        env = dict(zip(vars_, vals))
        if all(p(env) for p in premises) and option(env) and not conclusion(env):
            return False
    return True


def formal(name, vars_, premises, options, conclusion, expect):
    res = [k for k, f in options.items() if valid_individual(vars_, premises, f, conclusion)]
    bare = valid_individual(vars_, premises, lambda e: True, conclusion)
    ok = (res == [expect]) and not bare
    return (name, '能使论证有效的选项：%s；不加选项时论证%s' % ('、'.join(res) or '无', '有效（错误）' if bare else '无效'), ok)


def run():
    out = []
    # real 2024SZ-38: X=想从事, Z=想取得证书, R=报名考试, Q=已取得证书, S=有资格从事
    out.append(formal('真题 2024SZ-38（官方 B）', ['X', 'Z', 'R', 'Q', 'S'],
                      [lambda e: imp(e['X'], e['Z']), lambda e: e['Z']],
                      {'A 不想取得→不报名': lambda e: imp(not e['Z'], not e['R']),
                       'B 只有想从事才想取得': lambda e: imp(e['Z'], e['X']),
                       'C 只有取得才有资格': lambda e: imp(e['S'], e['Q']),
                       'D 大都持证（对个体无约束）': lambda e: True},
                      lambda e: e['X'], 'B 只有想从事才想取得'))
    # 10-1-2 人才公寓: C=符合条件, S=社保满3年, M=硕士
    out.append(formal('〔10-1-2〕人才公寓（双条件）', ['C', 'S', 'M'],
                      [lambda e: imp(e['C'], e['S']), lambda e: e['S'], lambda e: e['M']],
                      {'正确：社保满3年且硕士→符合': lambda e: imp(e['S'] and e['M'], e['C']),
                       '只有硕士才符合（符合→硕士）': lambda e: imp(e['C'], e['M']),
                       '没缴满3年的都不符合（前提逆否）': lambda e: imp(not e['S'], not e['C']),
                       '多数硕士符合（无约束）': lambda e: True},
                      lambda e: e['C'], '正确：社保满3年且硕士→符合'))
    # 10-9-1 示范店: X=示范店, Z=承诺退货, P=张贴承诺书
    out.append(formal('〔10-9-1〕示范店（肯定后件修复）', ['X', 'Z', 'P'],
                      [lambda e: imp(e['X'], e['Z']), lambda e: e['Z']],
                      {'正确：只有示范店才承诺（Z→X）': lambda e: imp(e['Z'], e['X']),
                       '示范店都张贴承诺书（X→P）': lambda e: imp(e['X'], e['P']),
                       '承诺者大多是示范店（无约束）': lambda e: True,
                       '未承诺的都不是示范店（前提逆否）': lambda e: imp(not e['Z'], not e['X'])},
                      lambda e: e['X'], '正确：只有示范店才承诺（Z→X）'))
    # 23-5-1 网格员: Y=优秀, T=消防培训, D=应急演练; premise Y->T, fact not Y, concl not T
    out.append(formal('〔23-5-1〕网格员（否定前件修复）', ['Y', 'T', 'D'],
                      [lambda e: imp(e['Y'], e['T']), lambda e: not e['Y']],
                      {'正确：只有优秀才培训（T→Y）': lambda e: imp(e['T'], e['Y']),
                       '培训者大多优秀（无约束）': lambda e: True,
                       '未培训的都不优秀（前提逆否）': lambda e: imp(not e['T'], not e['Y']),
                       '优秀者都参加演练（Y→D）': lambda e: imp(e['Y'], e['D'])},
                      lambda e: not e['T'], '正确：只有优秀才培训（T→Y）'))
    # 37-11-6 优秀社区: Y=优秀, W=无违建, Q=清理; Y->W, W->Q, Q; concl Y
    out.append(formal('〔37-11-6〕优秀社区（两步链）', ['Y', 'W', 'Q', 'F'],
                      [lambda e: imp(e['Y'], e['W']), lambda e: imp(e['W'], e['Q']), lambda e: e['Q']],
                      {'正确：只有优秀才清理（Q→Y）': lambda e: imp(e['Q'], e['Y']),
                       '无违建都入选优秀（W→Y）': lambda e: imp(e['W'], e['Y']),
                       '只有无违建才清理（Q→W）': lambda e: imp(e['Q'], e['W']),
                       '清理的都通过消防检查（Q→F）': lambda e: imp(e['Q'], e['F'])},
                      lambda e: e['Y'], '正确：只有优秀才清理（Q→Y）'))
    # 30-11-3 绿色社区（一元谓词，有限模型枚举）: G=绿色, J=积分制, E=交换站
    types = list(itertools.product([False, True], repeat=3))

    def models():
        for mask in range(1, 2 ** len(types)):
            yield [t for i, t in enumerate(types) if mask >> i & 1]
    all_ = lambda m, f: all(f(*t) for t in m)
    some = lambda m, f: any(f(*t) for t in m)
    prem = [lambda m: all_(m, lambda G, J, E: imp(G, J)), lambda m: some(m, lambda G, J, E: J and E)]
    concl = lambda m: some(m, lambda G, J, E: E and G)
    opts = {'正确：积分制社区都是绿色社区（J→G）': lambda m: all_(m, lambda G, J, E: imp(J, G)),
            '有些绿色社区没开交换站': lambda m: some(m, lambda G, J, E: G and not E),
            '开交换站的都实行积分制（E→J）': lambda m: all_(m, lambda G, J, E: imp(E, J)),
            '有些绿色社区实行积分制': lambda m: some(m, lambda G, J, E: G and J)}
    bare = all(concl(m) for m in models() if all(p(m) for p in prem))
    res = [k for k, f in opts.items() if all(concl(m) for m in models() if all(p(m) for p in prem) and f(m))]
    out.append(('〔30-11-3〕绿色社区（特称结论）', '能使论证有效的选项：%s；不加选项时论证%s' % ('、'.join(res), '有效（错误）' if bare else '无效'),
                res == ['正确：积分制社区都是绿色社区（J→G）'] and not bare))

    # ---- numeric ----
    def num(name, detail, ok):
        out.append((name, detail, bool(ok)))
    num('〔2-4-1〕新能源增量贡献', '9÷10＝%.0f%%（占比三成≠拉动增长）' % (9 / 10 * 100), abs(9 / 10 - 0.9) < 1e-9)
    r1 = 260 / 200; r2 = 260 / 1.4 / 200
    num('〔10-5-1〕高温与骑手事故', '订单持平时 7 月/4 月事故率＝260÷200＝%.2f（高约三成）；若订单增四成，比值＝%.2f（反而略降）' % (r1, r2), abs(r1 - 1.3) < 1e-9 and r2 < 1)
    rr = (0.8 / 0.2) / (0.2 / 0.8)
    num('〔10-5-2〕头盔与死亡风险', '未戴头盔者相对风险＝(0.8÷0.2)÷(0.2÷0.8)＝%.0f 倍' % rr, abs(rr - 16) < 1e-9)
    a30, a50 = 1 - 1 / 30, 1 - 1 / 50
    num('〔10-7-2〕SPF30 vs SPF50', '阻挡率 %.1f%% vs %.1f%%，差 %.1f 个百分点（约 1 个百分点）' % (a30 * 100, a50 * 100, (a50 - a30) * 100), 1.0 <= (a50 - a30) * 100 <= 1.5)
    num('〔17-2-5〕培训与再就业', '1360÷2000＝%.0f%%，3600÷8000＝%.0f%%；绝对数 3600÷1360≈%.2f 倍' % (1360 / 2000 * 100, 3600 / 8000 * 100, 3600 / 1360), 1360 / 2000 > 3600 / 8000 and 3600 / 1360 > 2)
    wh, need = 0.01 * 300 * 8, 5 * 3.85
    num('〔30-2-2〕柔性太阳能薄膜', '0.01×300×8＝%.0f 瓦时 ＞ 5000 毫安时×3.85 伏≈%.1f 瓦时' % (wh, need), wh > need)
    hk0, fo0 = 2760 / 1.15, 320 / 1.6
    dhk, dfo = 2760 - hk0, 320 - fo0
    num('〔30-2-3〕港澳 vs 外国游客', '港澳去年 %.0f 万、增量 %.0f 万；外国去年 %.0f 万、增量 %.0f 万；港澳占增量 %.0f%%；增速比 60÷15＝%.0f' % (hk0, dhk, fo0, dfo, dhk / (dhk + dfo) * 100, 60 / 15),
        abs(hk0 - 2400) < 1e-6 and abs(fo0 - 200) < 1e-6 and abs(dhk / (dhk + dfo) - 0.75) < 1e-9)
    save = 20000 * 0.30 * 15000 / 1e4
    num('〔37-5-3〕肺炎疫苗算账', '2 万人次×30%%×1.5 万元＝%.0f 万元 ＞ 接种费 6000 万元' % save, save > 6000)
    num('〔37-10-2〕新业态净增', '4500÷6000＝%.0f%%；传统业态新登记 12000−4800＝7200 户、净增 6000−4500＝1500 户' % (4500 / 6000 * 100), abs(4500 / 6000 - 0.75) < 1e-9 and 12000 - 4800 == 7200)
    v0, v1 = 0.60, 0.60 - 0.40
    num('〔37-11-5〕就业见习', '见习组签约率 60%%，比未见习组高 40 个百分点→未见习组 %.0f%%（数字自洽）' % (v1 * 100), abs(v1 - 0.20) < 1e-9)
    return out


if __name__ == '__main__':
    for name, detail, ok in run():
        print('OK ' if ok else 'BAD', name, '|', detail)
