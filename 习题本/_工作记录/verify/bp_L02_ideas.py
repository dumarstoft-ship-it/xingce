"""L02 blueprint -- planning-stage verification of every truth/lie variant design (87) and of the numbers in the
quantitative induction variants. Each design id (Dxx-g-k) is quoted at the end of the matching `idea` in
blueprints/L02.json as 〔验算 Dxx-g-k〕. Writers must still write an independent solver per finished item.
Run: python3 -I verify/bp_L02_ideas.py"""
import itertools, sys
from fractions import Fraction as F
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_L02_work')
from tfengine import check, identity, fixed_points, solve

D = {}
ALL4 = '甲 and 乙 and 丙 and 丁'
ANY4 = '甲 or 乙 or 丙 or 丁'
# ======================= DAY 7 =======================
# 考法一  显性矛盾 + 只有一真/一假
D['D07-1-1'] = dict(dom=('bool', ['污', '路', '场']),            # 污水管网 / 村道硬化 / 文化广场 开工
    stmts=[('甲', '污 or 路'), ('乙', 'not 污 and not 路'), ('丙', '(not 路) or 场'), ('丁', 'not 场')],
    count=('false', '==', 1), ask='must_true',
    opts={'A': '污', 'B': '路', 'C': 'not 路 and not 场', 'D': 'not 污 and not 路 and not 场'}, ans='C')
D['D07-1-2'] = dict(dom=('one', ['A', 'B', 'C', 'D']),            # 评上的街道
    stmts=[('赵', "x=='A'"), ('钱', "x!='A'"), ('孙', "x in ('B','C')"), ('李', "x!='D'")],
    count=('true', '==', 1), ask='must_true',
    opts={'A': "T[1] and x=='B'", 'B': "T[1] and x=='D'", 'C': "T[3] and x=='A'", 'D': "T[0] and x=='A'"}, ans='B')
D['D07-1-3'] = dict(dom=('bool', ['甲', '乙']),                    # 被推荐
    stmts=[('1', '甲 and 乙'), ('2', 'not 甲 or not 乙'), ('3', '乙 or not 甲')],   # (3) 如果乙没被推荐，那么甲也没被推荐
    count=('false', '==', 2), ask='must_false',
    opts={'A': '甲', 'B': 'not 乙', 'C': 'T[1]', 'D': '乙'}, ans='D')
D['D07-1-4'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 镇入选
    stmts=[('1', '甲 and 乙'), ('2', 'not 甲 or not 乙'), ('3', '甲 or not 乙'), ('4', '(not 丙) or (not 乙)'), ('5', 'not 丙')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '甲 and 乙', 'B': 'not 甲 and 乙 and 丙', 'C': '甲 and 丙 and not 乙', 'D': '甲 and 乙 and 丙'}, ans='B')
D['D07-1-5'] = dict(dom=('bool', ['体', '饭', '托']),              # 体育公园 / 长者饭堂 / 托育中心
    stmts=[('甲', '体 or 饭'), ('乙', 'not 体 and not 饭'), ('丙', '(not 托) or 饭')],
    count=('true', '==', 1), ask='undetermined',
    opts={'A': '托', 'B': '饭', 'C': 'T[2]', 'D': '体'}, ans='D')
D['D07-1-6'] = dict(dom=('bool', ['甲', '乙', '丙', '丁']),        # 通过考核
    stmts=[('1', ALL4), ('2', 'not (' + ALL4 + ')'), ('3', '甲'), ('4', '(not 乙) or 丙'), ('5', 'not 丁')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '甲+乙+丙+丁==1', 'B': '甲+乙+丙+丁==2', 'C': '甲+乙+丙+丁==3', 'D': '甲+乙+丙+丁==4'}, ans='B')
# 考法三  矛盾 + 多真多假
D['D07-2-1'] = dict(dom=('bool', ['甲', '乙', '丙', '丁']),        # 被通报
    stmts=[('1', 'not (' + ANY4 + ')'), ('2', 'not 乙'), ('3', 'not 乙 or not 丙'), ('4', ANY4)],
    count=('true', '==', 2), ask='must_true',
    opts={'A': 'T[0] and T[1]', 'B': 'T[1] and T[2]', 'C': 'T[2] and T[3]', 'D': 'T[0] and T[2]'}, ans='C')
D['D07-2-2'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 报名
    stmts=[('1', '甲 and 乙 and 丙'), ('2', 'not (甲 and 乙 and 丙)'), ('3', '甲'), ('4', '(not 乙) or (not 丙)')],
    count=('false', '==', 1), ask='must_true',
    opts={'A': '甲 and not 乙', 'B': '甲 and not (乙 and 丙)', 'C': 'not 丙', 'D': '甲 and 乙 and 丙'}, ans='B')
D['D07-2-3'] = dict(dom=('bool', ['A', 'B', 'C']),                 # 课题立项
    stmts=[('1', 'A'), ('2', 'not A'), ('3', '(not B) or C'), ('4', 'B and not C'), ('5', 'C')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': 'A', 'B': 'B', 'C': 'not C', 'D': 'B and C'}, ans='C')
D['D07-2-4'] = dict(dom=('bool', ['甲', '乙', '丙', '丁']),        # 报名
    stmts=[('1', ALL4), ('2', 'not (' + ALL4 + ')'), ('3', '甲'), ('4', '甲 or 乙')],
    count=('true', '==', 2), ask='may_true',
    opts={'A': '甲', 'B': 'not 乙', 'C': ALL4, 'D': 'not 丙 and not 丁'}, ans='D')
D['D07-2-5'] = dict(dom=('bool', ['甲', '乙']),                    # 公园通过复检
    stmts=[('黄', '甲'), ('李', 'not 乙'), ('陈', '乙'), ('何', '甲 and 乙')],    # 小陈："小李说的不对"
    count=('true', '==', 2), ask='must_true',
    opts={'A': '甲 and 乙', 'B': '甲 and not 乙', 'C': 'not 甲 and 乙', 'D': 'not 甲 and not 乙'}, ans='B')
# 考法四  反对 / 下反对
reg = {'老林': '东湖', '小吴': '东湖', '小陈': '西岭', '小郑': '南江'}
D['D07-3-1'] = dict(dom=('custom', [{'x': k, 'r': v} for k, v in reg.items()]),
    stmts=[('甲', "r=='东湖'"), ('乙', "x=='老林'"), ('丙', "r=='南江'"), ('丁', "x!='小陈'")],
    count=('false', '==', 1), ask='must_true',
    opts={'A': 'not T[0]', 'B': 'not T[1]', 'C': 'not T[2]', 'D': 'not T[3]'}, ans='C')
D['D07-3-2'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 完成适老化改造
    stmts=[('1', '甲 or 乙 or 丙'), ('2', 'not (甲 and 乙 and 丙)'), ('3', 'not 甲')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '甲 and 乙 and 丙', 'B': 'not (甲 or 乙 or 丙)', 'C': '甲 and not 乙', 'D': '甲 and not 乙 and not 丙'}, ans='A')
D['D07-3-3'] = dict(dom=('bool', ['广', '潮', '醒']),              # 广绣 / 潮绣 / 醒狮 获奖
    stmts=[('1', '广+潮+醒>=2'), ('2', '广 and not 潮 and not 醒'), ('3', 'not 潮'), ('4', '醒')],
    count=('false', '<=', 1), ask='must_true',
    opts={'A': '广 and not 潮 and not 醒', 'B': '广 and 醒 and not 潮', 'C': '广 and 潮 and 醒', 'D': '醒 and not 广 and not 潮'}, ans='B')
D['D07-3-4'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 去参加论坛
    stmts=[('1', '甲 or 乙'), ('2', 'not 甲 or not 乙'), ('3', '甲 and not 丙'), ('4', '丙')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': 'not (甲 or 乙 or 丙)', 'B': '甲 and not 乙 and not 丙', 'C': '乙 and not 甲 and not 丙', 'D': '甲 and 乙'}, ans='A')
D['D07-3-5'] = dict(dom=('bool', ['A', 'B', 'C']),                 # 社区达标
    stmts=[('1', 'A or B or C'), ('2', 'not A'), ('3', 'B'), ('4', 'A and B and C')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': 'not B', 'B': 'A', 'C': 'not (A or B or C)', 'D': 'C'}, ans='A')
# 考法五  推出关系与代入
D['D07-4-1'] = dict(dom=('one', ['甲', '乙', '丙']),               # 被聘用
    stmts=[('一', "x=='甲'"), ('二', "x!='乙'"), ('三', "x!='丙'")],
    count=('true', '==', 1), ask='must_true',
    opts={'A': "x=='乙'", 'B': "x=='丙'", 'C': "x!='甲'", 'D': 'T[2]'}, ans='C')
D['D07-4-2'] = dict(dom=('k', ['甲', '乙', '丙', '丁'], 2),        # 选派2人
    stmts=[('1', "'甲' in S"), ('2', "'甲' in S or '乙' in S"), ('3', "'丙' not in S and '丁' not in S"), ('4', "('丁' not in S) or ('甲' in S)")],
    count=('true', '==', 1), ask='must_true',
    opts={'A': "S==frozenset('甲丁')", 'B': "S==frozenset('乙丙')", 'C': "S==frozenset('乙丁')", 'D': "S==frozenset('丙丁')"}, ans='C')
D['D07-4-3'] = dict(dom=('one', ['甲', '乙', '丙', '丁']),         # 试点社区
    stmts=[('王', "x!='甲'"), ('李', "x=='乙'"), ('张', "x in ('乙','丙')"), ('赵', "x!='丁'")],
    count=('true', '==', 1), ask='must_false',
    opts={'A': 'T[0]', 'B': 'T[3]', 'C': "x=='甲'", 'D': 'T[2]'}, ans='D')
D['D07-4-4'] = dict(dom=('bool', ['骑', '醒', '侨']),              # 骑楼 / 醒狮 / 侨批 获奖
    stmts=[('1', '骑 and 醒 and 侨'), ('2', '骑+醒+侨==1'), ('3', 'not 骑'), ('4', '醒')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '骑', 'B': 'not 醒', 'C': 'not 侨', 'D': '骑+醒+侨==1'}, ans='C')
# ======================= DAY 14 =======================
D['D14-1-1'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 专精特新获批
    stmts=[('1', '甲 and 乙'), ('2', 'not (甲 and 乙)'), ('3', 'not 甲 and 乙'), ('4', '(not 乙) or 丙'), ('5', '丙')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': 'T[0]', 'B': 'T[1]', 'C': 'T[3]', 'D': 'T[4]'}, ans='A')
D['D14-1-2'] = dict(dom=('perm', ['甲', '乙', '丙', '丁', '戊'], ['一', '二', '三']),
    stmts=[('周', "at['一']=='丙'"), ('吴', "at['一'] in ('甲','乙','丁','戊')"), ('郑', "pos['甲'] is None"),
           ('钱', "at['二']=='戊'"), ('王', "at['一']!='乙'")],
    count=('true', '==', 1), ask='must_true',
    opts={'A': "at['一']=='乙'", 'B': "at['二']=='甲'", 'C': "pos['戊'] is None", 'D': "at['三']=='丙'"}, ans='A')
D['D14-2-1'] = dict(dom=('bool', ['研', '宿', '展']),              # 研学基地 / 民宿 / 展销馆 开工
    stmts=[('甲', '(not 研) or 宿'), ('乙', '研 and not 宿'), ('丙', 'not 宿'), ('丁', '展')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '研 and 宿', 'B': '宿 and not 展', 'C': '研 and not 宿', 'D': 'not 研 and not 宿 and not 展'}, ans='B')
D['D14-2-2'] = dict(dom=('bool', ['海', '龙']),                    # 海丝文化节 / 龙舟邀请赛
    stmts=[('1', '(not 龙) or 海'), ('2', '龙 and not 海'), ('3', '海 and 龙'), ('4', 'not 海')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '海 and not 龙', 'B': '龙 and not 海', 'C': '海 and 龙', 'D': 'not 海 and not 龙'}, ans='A')
D['D14-2-3'] = dict(dom=('bool', ['选', '扶']),                    # 选调生 / 三支一扶
    stmts=[('1', '选 != 扶'), ('2', '选 == 扶'), ('3', '选'), ('4', '(not 选) or 扶'), ('5', 'not 扶')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': '选 and 扶', 'B': '选 and not 扶', 'C': 'not 选 and 扶', 'D': 'not 选 and not 扶'}, ans='C')
D['D14-2-4'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 获奖
    stmts=[('1', '甲+乙+丙>=2'), ('2', '甲+乙+丙<=1'), ('3', '甲'), ('4', '(not 乙) or 丙'), ('5', 'not 乙')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '乙 and not 甲 and not 丙', 'B': '乙 and 丙 and not 甲', 'C': '甲 and 乙 and not 丙', 'D': 'not (甲 or 乙 or 丙)'}, ans='A')
D['D14-2-5'] = dict(dom=('bool', ['A', 'B', 'C', 'D', 'E']),       # 五个镇评上
    stmts=[('甲', 'not (A and B and C and D and E)'), ('乙', 'A and B and C and D and E'), ('丙', 'A or B or C or D or E'), ('丁', 'not A')],
    count=('false', '==', 1), ask='must_true',
    opts={'A': 'A and B and C and D and E', 'B': 'not A and (B or C or D or E)', 'C': 'not (A or B or C or D or E)', 'D': 'not A and B and C and D and E'}, ans='B')
D['D14-3-1'] = dict(dom=('bool', ['张', '王']),                    # 去送教下乡
    stmts=[('吴', '(not 王) or 张'), ('陈', '张 and 王'), ('郑', '王'), ('刘', '王 and not 张')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': 'T[0] and T[1]', 'B': 'T[2] and T[3]', 'C': 'T[1] and T[2]', 'D': 'T[0] and T[2]'}, ans='B')
D['D14-3-2'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 捐赠
    stmts=[('1', 'not (甲 or 乙 or 丙)'), ('2', 'not 丙'), ('3', 'not 乙 or not 丙'), ('4', '甲 or 乙 or 丙')],
    count=('true', '==', 2), ask='undetermined',
    opts={'A': '丙', 'B': '乙', 'C': '甲', 'D': 'not T[0]'}, ans='C')
D['D14-3-3'] = dict(dom=('bool', ['甲', '乙', '丙', '丁', '戊']),  # 完成专题学习
    stmts=[('甲', '乙'), ('乙', 'not 丙'), ('丙', '丙'), ('丁', '甲 and 丙'), ('戊', 'not 甲')],
    count=('false', '==', 2), ask='must_true',
    opts={'A': '乙', 'B': '丙', 'C': 'not 甲', 'D': '甲 and 丙'}, ans='A')
D['D14-3-4'] = dict(dom=('one', ['A', 'B', 'C', 'D']),             # 入选案例
    stmts=[('甲', "x=='A'"), ('乙', "x!='A'"), ('丙', "x=='B'"), ('丁', "x in ('B','C')")],
    count=('true', '==', 2), ask='must_true',
    opts={'A': "x=='A'", 'B': "x=='B'", 'C': "x=='C'", 'D': "x=='D'"}, ans='C')
D['D14-4-1'] = dict(dom=('bool', ['林', '周', '吴']),              # 入选
    stmts=[('1', '林 and 周'), ('2', 'not 林 and not 周'), ('3', '周'), ('4', '(not 周) or 吴')],
    count=('false', '==', 1), ask='must_true',
    opts={'A': '林 and 周 and 吴', 'B': '林 and 周 and not 吴', 'C': 'not 林', 'D': 'not 吴'}, ans='A')
D['D14-4-2'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 园区达标
    stmts=[('1', '甲+乙+丙>=2'), ('2', '甲+乙+丙<=2'), ('3', 'not 甲'), ('4', '乙')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '甲 and not 乙 and not 丙', 'B': '甲 and 丙 and not 乙', 'C': '甲 and 乙 and 丙', 'D': '甲 and 乙 and not 丙'}, ans='A')
D['D14-4-3'] = dict(dom=('one', ['甲', '乙', '丙', '丁', '戊']),   # 示范基地所在县
    stmts=[('1', "x=='甲'"), ('2', "x=='乙'"), ('3', "x!='丙'"), ('4', "x in ('甲','丁')"), ('5', "x!='戊'")],
    count=('false', '<=', 1), ask='must_true',
    opts={'A': "x=='甲'", 'B': "x=='乙'", 'C': "x=='丙'", 'D': "x=='丁'"}, ans='A')
D['D14-5-1'] = dict(dom=('bool', ['渔', '茶']),                    # 《渔歌》《茶韵》获奖
    stmts=[('1', '渔 and 茶'), ('2', '渔 != 茶'), ('3', 'not 渔'), ('4', '茶')],
    count=('false', '==', 1), ask='must_true',
    opts={'A': '渔 and 茶', 'B': '渔 and not 茶', 'C': '茶 and not 渔', 'D': 'not 渔 and not 茶'}, ans='C')
D['D14-5-2'] = dict(dom=('one', ['甲', '乙', '丙', '丁']),         # 链主企业
    stmts=[('一', "x=='甲'"), ('二', "x in ('甲','乙')"), ('三', "x=='丙'"), ('四', "x=='丁'")],
    count=('true', '==', 1), ask='may_true',
    opts={'A': "x=='甲'", 'B': 'T[0] and T[1]', 'C': 'not T[1] and not T[2]', 'D': 'T[2] and T[3]'}, ans='C')
D['D14-5-3'] = dict(dom=('bool', ['A', 'B', 'C']),                 # 项目获资助
    stmts=[('1', 'not C'), ('2', '(not A) or B'), ('3', '(not C) or B'), ('4', 'A and B')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': 'C and not A and not B', 'B': 'A and not B and not C', 'C': 'A and B and not C', 'D': 'A and B and C'}, ans='A')
D['D14-6-1'] = dict(dom=('one', [1, 2, 3]),                        # 奖品所在箱；3号箱的话为假
    stmts=[('3号', '((x==1) + (x!=2)) == 1')],
    count=('true', '==', 0), ask='must_true',
    opts={'A': 'x==1', 'B': 'x==2', 'C': 'x!=3', 'D': 'x==3'}, ans='C')
# ======================= DAY 27 =======================
D['D27-1-1'] = dict(dom=('bool', ['甲', '乙', '丙', '丁']),        # True = 线下参加, False = 线上参加
    stmts=[('1', '丁'), ('2', '(not 甲) or (not 乙)'), ('3', '(not 丁) or (not 丙)'), ('4', '甲 and 乙')],
    count=('false', '==', 1), ask='must_true',
    opts={'A': 'not 丙 and 丁', 'B': 'not 甲', 'C': '乙', 'D': '甲 and 乙'}, ans='A')
D['D27-1-2'] = dict(dom=('one', ['A', 'B', 'C']),                  # 选定方案
    stmts=[('甲', "x=='A'"), ('乙', "x in ('B','C')"), ('丙', "x!='B'"), ('丁', "x=='C'")],
    count=('true', '==', 1), ask='must_true',
    opts={'A': "x=='A'", 'B': "x=='B'", 'C': "x=='C'", 'D': 'T[2]'}, ans='B')
D['D27-1-3'] = dict(dom=('bool', ['夜', '券', '志']),              # 夜间经济节 / 文旅消费券 / 志愿服务季
    stmts=[('1', '(not 夜) or 券'), ('2', '夜 and not 券'), ('3', '(not 志) or 夜'), ('4', '志'), ('5', 'not 券')],
    count=('false', '==', 1), ask='must_true',
    opts={'A': '夜 and 志 and not 券', 'B': '夜 and 券 and 志', 'C': '志 and not 夜 and not 券', 'D': '券 and not 夜'}, ans='A')
D['D27-1-4'] = dict(dom=('bool', ['甲广', '乙深']),                # 甲去广州(否则深圳) / 乙去深圳(否则广州)
    stmts=[('1', '甲广 or 乙深'), ('2', 'not 甲广 and not 乙深'), ('3', '甲广'), ('4', '乙深')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': '甲广', 'B': '乙深', 'C': '甲广 == (not 乙深)', 'D': '甲广 == 乙深'}, ans='C')
D['D27-2-1'] = dict(dom=('bool', ['王', '郑', '林']),              # 考核通过（参考人员为三人）
    stmts=[('1', '王 and 郑 and 林'), ('2', '王'), ('3', 'not (王 and 郑 and 林)'), ('4', '郑 or 王')],
    count=('false', '==', 1), ask='must_true',
    opts={'A': '王', 'B': '郑', 'C': '王 and 郑 and 林', 'D': 'not (王 and 郑 and 林)'}, ans='A')
D['D27-2-2'] = dict(dom=('bool', ['甲', '乙']),                    # 进决赛
    stmts=[('赵', '(not 甲) or 乙'), ('钱', '甲'), ('孙', '甲 and not 乙'), ('李', '甲 or 乙')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': 'T[0] and T[1]', 'B': 'T[0] and T[3]', 'C': 'T[1] and T[2]', 'D': 'T[2] and T[3]'}, ans='B')
D['D27-2-3'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 去调研
    stmts=[('1', 'not (甲 and 乙)'), ('2', '甲 and not 丙'), ('3', '甲 and 乙'), ('4', '(not 甲) or 丙'), ('5', 'not 乙')],
    count=('true', '==', 3), ask='must_true',
    opts={'A': '甲', 'B': 'not 乙', 'C': '丙', 'D': '甲 and not 丙'}, ans='B')
D['D27-2-4'] = dict(dom=('bool', ['甲', '乙', '丙', '丁', '戊', '己']),
    stmts=[('甲', 'not 乙'), ('乙', '乙'), ('丙', '丁'), ('丁', '丙 and 丁'), ('戊', '乙'), ('己', 'not 丁')],   # 乙："甲说的是假话"
    count=('false', '==', 2), ask='must_true',
    opts={'A': '乙 and 丙 and 丁', 'B': '甲', 'C': 'not 丁', 'D': 'not T[0] and not T[4]'}, ans='A')
D['D27-2-5'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 获奖
    stmts=[('1', '甲'), ('2', 'not 甲'), ('3', '乙 and 丙'), ('4', 'not 乙 or not 丙'), ('5', '乙'), ('6', '甲 or 乙')],
    count=('true', '==', 3), ask='must_true',
    opts={'A': '甲 and not 乙', 'B': '丙', 'C': '乙', 'D': 'not 甲 and not 乙'}, ans='A')
D['D27-3-1'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 能在8级风中作业
    stmts=[('1', 'not 甲'), ('2', '甲 or 乙 or 丙'), ('3', 'not (甲 and 乙 and 丙)')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': 'T[0]', 'B': 'T[1]', 'C': 'T[2]', 'D': 'not (甲 or 乙 or 丙)'}, ans='B')
D['D27-3-2'] = dict(dom=('bool', ['A', 'B', 'C']),                 # 窗口实现"一网通办"
    stmts=[('1', 'A and B and C'), ('2', 'not (A or B or C)'), ('3', 'A'), ('4', 'B')],
    count=('false', '<=', 1), ask='must_true',
    opts={'A': 'A and B and C', 'B': 'A and B and not C', 'C': 'not C', 'D': 'not T[0]'}, ans='A')
D['D27-3-3'] = dict(dom=('bool', ['甲', '乙', '丙']),              # 达标
    stmts=[('1', '甲 and 乙'), ('2', 'not 甲 and not 乙'), ('3', '甲 or 丙'), ('4', 'not 甲 or not 丙')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '甲', 'B': '乙', 'C': '乙 != 丙', 'D': '甲 and 乙 and 丙'}, ans='C')
D['D27-3-4'] = dict(dom=('one', ['甲', '乙', '丙', '丁', '戊']),   # 入选
    stmts=[('1', "x=='甲'"), ('2', "x=='乙'"), ('3', "x in ('甲','丙')"), ('4', "x!='丙'"), ('5', "x in ('乙','戊')")],
    count=('true', '==', 2), ask='must_true',
    opts={'A': "x=='甲'", 'B': "x=='丙'", 'C': "x=='丁'", 'D': "x=='戊'"}, ans='D')
D['D27-4-1'] = dict(dom=('k', ['甲', '乙', '丙', '丁'], 2),
    stmts=[('1', "'甲' in S"), ('2', "'甲' in S or '乙' in S"), ('3', "'甲' not in S and '丙' not in S"), ('4', "('乙' not in S) or ('甲' in S)")],
    count=('true', '==', 2), ask='must_true',
    opts={'A': "S==frozenset('甲乙')", 'B': "S==frozenset('乙丙')", 'C': "S==frozenset('乙丁')", 'D': "S==frozenset('丙丁')"}, ans='C')
D['D27-4-2'] = dict(dom=('bool', ['广彩', '潮绣', '陶塑']),        # 广彩 / 潮绣 / 石湾陶塑 获奖
    stmts=[('1', '广彩 and 潮绣 and 陶塑'), ('2', '广彩+潮绣+陶塑==1'), ('3', 'not 广彩'), ('4', '潮绣')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': '广彩', 'B': 'not 潮绣', 'C': '陶塑', 'D': '广彩 and 潮绣 and 陶塑'}, ans='C')
D['D27-4-3'] = dict(dom=('bool', ['A', 'B', 'C']),
    stmts=[('1', 'A'), ('2', '(not C) or A'), ('3', 'A and B'), ('4', 'A or B')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': 'B and not A and not C', 'B': 'A and not B and not C', 'C': 'A and B and not C', 'D': 'B and C and not A'}, ans='A')
D['D27-5-1'] = dict(dom=('one', [1, 2, 3, 4]),                     # 4号门的话为真
    stmts=[('4号', '((x==1) + (x!=1) + (x!=3)) == 1')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': 'x==1', 'B': 'x==2', 'C': 'x==3', 'D': 'x==4'}, ans='C')
# ======================= DAY 36 =======================
D['D36-1-1'] = dict(dom=('bool', ['甲', '乙', '丙', '丁', '戊']),  # 通过学法考试
    stmts=[('甲', 'not 丙'), ('乙', '丙'), ('丙', '丁 and 戊'), ('丁', '甲 and not 乙'), ('戊', 'not 丙 or not 丁')],
    count=('false', '==', 1), ask='must_true',
    opts={'A': 'not T[1] and 甲+乙+丙+丁+戊==3', 'B': 'not T[0] and 甲+乙+丙+丁+戊==3', 'C': 'not T[1] and 甲+乙+丙+丁+戊==4', 'D': 'not T[2] and 甲+乙+丙+丁+戊==2'}, ans='A')
D['D36-1-2'] = dict(dom=('bool', ['甲', '乙', '丙', '丁', '戊', '己']),
    stmts=[('甲', '甲 != 乙'), ('乙', 'not (甲 or 乙 or 丙 or 丁 or 戊 or 己)'), ('丙', '乙 != 丙'),
           ('丁', 'not (not 甲 or not 丙)'), ('戊', 'not 甲 or not 丙'), ('己', '甲')],          # 丁："戊说的是假话"
    count=('false', '==', 2), ask='must_true',
    opts={'A': 'not T[1] and not T[4]', 'B': 'not T[3] and not T[5]', 'C': 'not T[1] and not T[3]', 'D': 'not T[0] and not T[4]'}, ans='A')
D['D36-1-3'] = dict(dom=('bool', ['甲', '乙', '丙', '丁']),
    stmts=[('1', '丙'), ('2', 'not 丙'), ('3', '甲 or 丙'), ('4', 'not 甲 and not 丙'), ('5', 'not 甲 or not 丁'), ('6', '(not 乙) or 丁'), ('7', '(not 丙) or 乙')],
    count=('true', '==', 3), ask='must_true',
    opts={'A': '甲 and 丙 and 丁 and not 乙', 'B': ALL4, 'C': '乙 and 丙 and 丁 and not 甲', 'D': '甲 and 丙 and not 乙 and not 丁'}, ans='A')
D['D36-1-4'] = dict(dom=('bool', ['甲', '乙', '丙', '丁']),
    stmts=[('1', '甲 or 丙'), ('2', 'not 甲 and not 丙'), ('3', '甲 and 丙'), ('4', '乙 and 丁'), ('5', 'not 乙 and not 丙')],
    count=('true', '>=', 3), ask='must_true',
    opts={'A': ALL4, 'B': '甲 and 丙 and not 乙 and not 丁', 'C': 'not 乙 and not 丙', 'D': '乙 and 丁 and not 甲 and not 丙'}, ans='A')
D['D36-2-1'] = dict(dom=('bool', ['甲', '乙', '丙', '丁']),
    stmts=[('1', '(not 甲) or 乙'), ('2', '甲 and not 乙'), ('3', ALL4), ('4', 'not (' + ALL4 + ')'), ('5', '丙'), ('6', 'not 丁')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': '甲', 'B': 'not 乙', 'C': 'not 丙 and 丁', 'D': ALL4}, ans='C')
D['D36-2-2'] = dict(dom=('bool', ['A', 'B', 'C']),                 # 考察组是否去了A、B、C三个镇
    stmts=[('1', 'A != B'), ('2', 'A == B'), ('3', 'C'), ('4', '(not B) or C')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': 'not B and not C', 'B': 'A', 'C': 'B', 'D': 'A and B and C'}, ans='A')
D['D36-2-3'] = dict(dom=('bool', ['甲', '乙', '丙', '丁', '戊']),
    stmts=[('1', '甲+乙+丙+丁+戊==2'), ('2', '甲+乙+丙+丁+戊!=2'), ('3', '甲 and 乙'), ('4', 'not 丙 and not 丁 and not 戊')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': '甲+乙+丙+丁+戊==2', 'B': '甲', 'C': '甲+乙+丙+丁+戊!=2', 'D': '丙'}, ans='C')
D['D36-3-1'] = dict(dom=('bool', ['甲', '乙', '丙']),
    stmts=[('1', '甲 and 乙'), ('2', 'not 甲 and not 乙'), ('3', '乙 or 丙'), ('4', 'not 乙 or not 丙'), ('5', '(not 甲) or 丙')],
    count=('true', '==', 2), ask='must_true',
    opts={'A': '乙 and 丙 and not 甲', 'B': '甲 and not 乙 and not 丙', 'C': '甲 and 乙 and 丙', 'D': '甲 and 乙 and not 丙'}, ans='A')
D['D36-3-2'] = dict(dom=('bool', ['A', 'B', 'C']),
    stmts=[('1', 'A or B or C'), ('2', 'not (A and B and C)'), ('3', 'not A'), ('4', 'not C')],
    count=('true', '<=', 1), ask='must_true',
    opts={'A': 'A and B and C', 'B': 'not (A or B or C)', 'C': 'A and C and not B', 'D': 'not B'}, ans='A')
D['D36-4-1'] = dict(dom=('bool', ['A', 'B', 'C']),
    stmts=[('1', 'A and B'), ('2', '(not C) or A'), ('3', 'not B'), ('4', 'A or C')],
    count=('true', '==', 3), ask='must_false',
    opts={'A': 'A and not B and not C', 'B': 'C and not A and not B', 'C': 'A and C and not B', 'D': 'A and B and C'}, ans='B')
D['D36-12-1'] = dict(dom=('bool', ['甲', '乙', '丙', '丁', '戊']),
    stmts=[('1', '甲+乙+丙+丁+戊>=3'), ('2', '甲+乙+丙+丁+戊<=2'), ('3', '甲 and 乙'), ('4', 'not 丙 and not 丁 and not 戊'), ('5', '(not 甲) or 丙')],
    count=('true', '==', 1), ask='must_true',
    opts={'A': '甲 and 乙', 'B': '甲 and not 乙 and not 丙', 'C': '丁 and 戊', 'D': '甲+乙+丙+丁+戊==2'}, ans='B')
D['D36-12-2'] = dict(dom=('bool', ['甲', '乙', '丙']),
    stmts=[('1', '甲+乙+丙==1'), ('2', '甲+乙+丙==2'), ('3', '甲'), ('4', 'not 乙 or not 丙'), ('5', '乙')],
    count=('false', '<=', 1), ask='must_true',
    opts={'A': '甲 and 乙 and not 丙', 'B': '甲 and not 乙 and not 丙', 'C': '甲 and 乙 and 丙', 'D': '甲 and 丙'}, ans='A')
D['D36-12-3'] = dict(dom=('k', ['甲', '乙', '丙', '丁'], 2),
    stmts=[('1', "'甲' in S"), ('2', "'乙' in S"), ('3', "'丙' not in S"), ('4', "('丁' not in S) or ('甲' in S)")],
    count=('false', '==', 1), ask='must_true',
    opts={'A': "S==frozenset('甲乙')", 'B': "S==frozenset('甲丁')", 'C': "S==frozenset('乙丙')", 'D': "S==frozenset('丙丁')"}, ans='B')

ok = True
for k in sorted(D):
    ok &= check(k, D[k])

def flag(name, cond, info=''):
    global ok
    ok &= bool(cond)
    print(('OK ' if cond else 'BAD'), name, info)

# ---- one-person-two-sentences (每人两句恰一真) ----
def half_true(cands, speakers):
    return [w for w in cands if all((a(w) + b(w)) == 1 for a, b in speakers)]
C5 = ['甲', '乙', '丙', '丁', '戊']
s = half_true(C5, [(lambda w: w == '甲', lambda w: w != '乙'), (lambda w: w == '甲', lambda w: w != '丙'), (lambda w: w != '甲', lambda w: w == '丁')])
flag('D14-7-1 一人两句半真半假 -> 戊', s == ['戊'], s)
s = half_true(C5, [(lambda w: w == '甲', lambda w: w != '乙'), (lambda w: w == '乙', lambda w: w in ('丙', '戊')), (lambda w: w == '丁', lambda w: w in ('乙', '戊'))])
flag('D27-6-1 一人两句(含"或") -> 戊', s == ['戊'], s)
spk = {'赵': (lambda w: w == '甲', lambda w: w != '乙'), '钱': (lambda w: w == '甲', lambda w: w != '丁'), '孙': (lambda w: w == '乙', lambda w: w != '丙')}
s = [(w, {k: a(w) + b(w) for k, (a, b) in spk.items()}) for w in C5 if sorted(a(w) + b(w) for a, b in spk.values()) == [0, 1, 2]]
flag('D36-6-2 一人全对/一人全错/一人半对 -> 乙', len(s) == 1 and s[0][0] == '乙', s)

# ---- identity (诚实者 H / 说谎者 L / 随机者 R) ----
HL2 = list(itertools.product('HL', repeat=2)); HL3 = list(itertools.product('HL', repeat=3))
s = identity(['甲', '乙'], HL2, {'甲': lambda a: a['乙'] == 'L', '乙': lambda a: a['甲'] == a['乙']})
flag('D14-7-2 身份型2人 -> 甲H 乙L', s == [{'甲': 'H', '乙': 'L'}], s)
s = identity(['甲', '乙', '丙'], HL3, {'甲': lambda a: 'L' in a.values(), '乙': lambda a: a['丙'] == 'H', '丙': lambda a: a['甲'] == 'L'})
flag('D14-7-3 身份型3人 -> 甲H 乙L 丙L', s == [{'甲': 'H', '乙': 'L', '丙': 'L'}], s)
sols = []
for t in HL2:
    for ex in ('左', '右'):
        a = {'甲': t[0], '乙': t[1]}
        v1 = a['甲'] == 'L' or a['乙'] == 'L'; v2 = ex == '左'
        if (v1 == (a['甲'] == 'H')) and (v2 == (a['乙'] == 'H')):
            sols.append((a, ex))
flag('D27-6-2 身份+内容 -> 甲H 乙L 出口在右', sols == [({'甲': 'H', '乙': 'L'}, '右')], sols)
s = identity(['甲', '乙', '丙'], list(itertools.permutations('HLR')), {'甲': lambda a: a['乙'] == 'H', '乙': lambda a: a['甲'] == 'H', '丙': lambda a: a['甲'] == 'L'})
flag('D27-6-3 诚实/说谎/随机各一 -> 甲L 乙R 丙H', s == [{'甲': 'L', '乙': 'R', '丙': 'H'}], s)
s = identity(['甲', '乙', '丙'], list(itertools.permutations('HLR')), {'甲': lambda a: a['乙'] != 'H', '乙': lambda a: a['甲'] == 'H', '丙': lambda a: a['甲'] == 'L'})
flag('D36-6-3 诚实/说谎/随机各一 -> 随机者是乙', s == [{'甲': 'H', '乙': 'R', '丙': 'L'}], s)
s = identity(['甲', '乙', '丙'], HL3, {'甲': lambda a: a['甲'] == 'L' and a['乙'] == 'L', '乙': lambda a: a['甲'] == 'L' or a['丙'] == 'L', '丙': lambda a: a['乙'] == 'L'})
flag('D36-12-4 身份型3人(含自指) -> 甲L 乙H 丙L', s == [{'甲': 'L', '乙': 'H', '丙': 'L'}], s)
lines = {'A 我是说谎者': lambda a, me, o: a[me] == 'L', 'B 我是诚实者': lambda a, me, o: a[me] == 'H',
         'C 我的同伴是说谎者': lambda a, me, o: a[o] == 'L', 'D 我们两人都是说谎者': lambda a, me, o: a[me] == 'L' and a[o] == 'L'}
poss = {k: any(f({'甲': x, '乙': y}, '甲', '乙') == (x == 'H') for x in 'HL' for y in 'HL') for k, f in lines.items()}
flag('D36-6-1 任何人都不可能说出的话 -> A', [k for k, p in poss.items() if not p] == ['A 我是说谎者'], poss)

# ---- self-reference / accusation chains ----
fp = fixed_points(3, lambda t, w: [not t[1], not t[2], (not t[0]) and (not t[1])])
flag('D14-6-2 链式指控3人 -> 只有乙说真话', fp == [((False, True, False), None)], fp)
fp = fixed_points(3, lambda t, w: [sum(t) == 1, sum(t) == 2, sum(t) == 0])
flag('D14-6-3 自我指涉计数3句 -> 只有①真', fp == [((True, False, False), None)], fp)
fp = fixed_points(4, lambda t, w: [not t[1], not t[2], not t[3], (not t[0]) and (not t[1])])
flag('D27-5-2 链式指控4人 -> 甲、丙说真话', fp == [((True, False, True, False), None)], fp)
fp = fixed_points(3, lambda t, w: [t[1] != t[2], t[0] and (w == 'A'), sum(t) <= 1], extra=('A', 'B'))
flag('D27-5-3 自我指涉+内容 -> ①②真③假，奖品在A箱', fp == [((True, True, False), 'A')], fp)
fp = fixed_points(4, lambda t, w: [sum(t) == 1, sum(t) == 2, sum(t) == 3, sum(t) == 0])
flag('D36-5-1 自我指涉计数4句 -> 只有①真', fp == [((True, False, False, False), None)], fp)

# ---- meta-information (2020SZS-80 type) ----
P3 = ['甲', '乙', '丙']
ws = [{'X': X, '甲': a, '乙': b, '丙': c} for X in P3 for a in ('乙', '丙') for b in ('甲', '丙') for c in ('甲', '乙')]
tr = lambda w, p: w[p] == w['X']
base = [w for w in ws if tr(w, '甲')]
ded = {st: {w['X'] for w in base if tr(w, '丙') == st} for st in (True, False)}
told = [st for st in ded if len(ded[st]) > 1]          # 老赵 was told 丙's status but still could NOT identify
final = [w for w in base if tr(w, '丙') in told]
o = {'A 乙是真凶': lambda w: w['X'] == '乙', 'B 丙说了假话': lambda w: not tr(w, '丙'), 'C 丙是真凶': lambda w: w['X'] == '丙', 'D 乙说了真话': lambda w: tr(w, '乙')}
res = [k for k, f in o.items() if final and all(f(w) for w in final)]
flag('D36-5-2 元信息(知道丙真假仍无法确定) -> B 丙说了假话', res == ['B 丙说了假话'], (ded, res))
boxes = ['红', '黄', '蓝']
red = lambda p: p == '黄'                                # 红盒："奖品在黄盒里"
ded = {st: [p for p in boxes if red(p) == st] for st in (True, False)}
known = [st for st in ded if len(ded[st]) == 1]
flag('D36-5-3 元信息(盒子) -> 奖品在黄盒', known == [True] and ded[True] == ['黄'], ded)

# ---- D36-4-2 补充一句 / D36-4-3 真话最多几句 ----
Wb = [dict(zip(['甲', '乙', '丙'], v)) for v in itertools.product([False, True], repeat=3)]
baseS = [lambda w: w['甲'] and w['乙'], lambda w: not w['甲'], lambda w: (not w['乙']) or w['丙']]
cands = {'A 乙没有入选': lambda w: not w['乙'], 'B 丙没有入选': lambda w: not w['丙'], 'C 甲入选了': lambda w: w['甲'], 'D 乙和丙都入选了': lambda w: w['乙'] and w['丙']}
good = []
for k, f in cands.items():
    val = [w for w in Wb if sum(g(w) for g in baseS + [f]) == 1]
    if val and all(w['丙'] for w in val):
        good.append((k, len(val)))
flag('D36-4-2 补充哪句后(四句只有一句真)可确定丙入选 -> B', [g[0] for g in good] == ['B 丙没有入选'], good)
cnt = {x: sum([x == '乙', x in ('丙', '丁'), x != '丁', x != '甲']) for x in ['甲', '乙', '丙', '丁']}
flag('D36-4-3 四句话最多几句为真 -> 3', max(cnt.values()) == 3, cnt)

# =================== quantitative induction variants (numbers) ===================
r = F(108, 100) * F(97, 100)
flag(f'D07-7-2 人均+8%、人口-3% -> 总额为原来的 {float(r):.4f} 倍（上升，且不是+11%）', r > 1 and r != F(111, 100))
nev0, nev1 = F(40, 100), F(50, 100) * F(90, 100)
oil = (1 - F(50, 100)) * F(90, 100) / F(60, 100)
flag(f'D07-7-3 新能源占比40%->50%、总量-10% -> 新能源为原来的 {float(nev1 / nev0):.3f} 倍、燃油 {float(oil):.3f} 倍', nev1 > nev0 and nev1 / nev0 != F(125, 100) and oil == F(3, 4))
avg = F(82 * 1 + 78 * 2, 3)
flag(f'D07-7-4 两校加权平均 = {float(avg):.2f} < 80', avg < 80)
flag('D14-11-1 门票80->40、人次+50% -> 门票收入 40x1.5=60 < 80', 40 * F(3, 2) < 80)
avg = F(92 * 100 + 86 * 300, 400)
flag(f'D14-11-2 加权平均 = {float(avg)} < 89', avg < 89 and avg != 89)
S5 = [c for c in itertools.combinations_with_replacement(range(60, 96), 4) if sum(c) + 95 == 400]
opt = {'A 有3人低于80': lambda c: sum(x < 80 for x in c) >= 3, 'B 只有1人在90分以上(含90)': lambda c: sum(x >= 90 for x in c) == 0,
       'C 最低分恰为60': lambda c: min(c) == 60, 'D 有4人不低于90': lambda c: sum(x >= 90 for x in c) >= 3}
pos = {k: any(f(c) for c in S5) for k, f in opt.items()}
flag('D14-11-3 唯一不可能为真 -> D', [k for k, p in pos.items() if not p] == ['D 有4人不低于90'], pos)
ow0, ow1 = F(30, 100), F(40, 100) * F(120, 100); no0, no1 = F(70, 100), F(60, 100) * F(120, 100)
flag(f'D14-9-3 海外仓 {float(ow0):.2f}->{float(ow1):.2f}（+60%）；非海外仓 {float(no0):.2f}->{float(no1):.2f} 也上升（故C错）', ow1 > ow0 and no1 > no0)
flag('D27-9-1 停车6->8元/时、收入持平 -> 计费总时长为原来的3/4', F(6, 8) == F(3, 4))
d24, d25 = F(30, 100), F(35, 100) * F(90, 100); n24, n25 = F(70, 100), F(65, 100) * F(90, 100)
flag(f'D27-9-2 数字岗位 {float(d24):.3f}->{float(d25):.3f} 增加；非数字 {float(n24):.3f}->{float(n25):.3f}（降{float(1 - n25 / n24) * 100:.1f}%，故B错）', d25 > d24 and n25 < n24 and 1 - n25 / n24 > F(10, 100))
comb = [c for c in itertools.combinations_with_replacement(range(3, 9), 8) if sum(c) == 40 and max(c) == 8]
opt = {'A 有一个社区只有3名': lambda c: 3 in c, 'B 有3个社区各8名': lambda c: c.count(8) >= 3, 'C 每个社区都不少于5名': lambda c: min(c) >= 5, 'D 有5个社区各4名': lambda c: c.count(4) >= 5}
pos = {k: any(f(c) for c in comb) for k, f in opt.items()}
flag('D27-9-3 唯一不可能为真 -> C', [k for k, p in pos.items() if not p] == ['C 每个社区都不少于5名'], pos)
# 会粤语60%、会英语55%：两样都会的比例范围；"都不会"的范围
both = [F(x, 100) for x in range(0, 101) if F(60, 100) + F(55, 100) - F(x, 100) <= 1 and x <= 55]
neither = [1 - (F(60, 100) + F(55, 100) - b) for b in both]
flag(f'D27-9-4 两样都会的最少为 {float(min(both)):.0%}；"都不会"可低至 {float(min(neither)):.0%}；英语者中会粤语最少 {float(min(both) / F(55, 100)):.0%}', min(both) == F(15, 100) and min(neither) == 0 and min(both) / F(55, 100) < F(1, 2))
flag('D27-10-1 抽检2/50=4%<=5% 不召回；再抽50仍2件 -> 4/100=4% 仍不召回', F(2, 50) <= F(5, 100) and F(4, 100) <= F(5, 100))
bmi = F(60) / (F(16, 10) ** 2)
flag(f'D27-10-2 身高1.6米、体重60千克 BMI={float(bmi):.2f}（正常，不是超重）', F(185, 10) <= bmi <= F(239, 10))
art = [(a, b, c) for a in range(1, 13) for b in range(1, 13) for c in range(1, 13) if a + b + c == 12 and a > b > c]
opt = {'A 竹编6人': lambda t: t[0] == 6, 'B 木雕5人': lambda t: t[1] == 5, 'C 陶艺4人': lambda t: t[2] == 4, 'D 木雕2人': lambda t: t[1] == 2}
pos = {k: any(f(t) for t in art) for k, f in opt.items()}
flag('D27-11-3 乡村工匠 唯一不可能为真 -> C', [k for k, p in pos.items() if not p] == ['C 陶艺4人'], pos)
flag('D36-7-3 105/150=70%，45/150=30%，比例为2倍多', F(105, 150) / F(45, 150) > 2 and F(105, 150) == F(7, 10))
tot24 = F(1) / F(108, 100); wm24 = F(60, 100) / F(112, 100); nm24 = tot24 - wm24; nm25 = F(40, 100)
g_nm = nm25 / nm24 - 1
inc_ratio = (F(60, 100) - wm24) / (nm25 - nm24)
flag(f'D36-9-1 港口：内贸增速={float(g_nm) * 100:.2f}%（0~8%之间）；2024外贸占比={float(wm24 / tot24) * 100:.2f}%<60%；外贸/内贸增量比={float(inc_ratio):.2f}', 0 < g_nm < F(8, 100) and wm24 / tot24 < F(60, 100) and inc_ratio != F(3, 2))
S = [c for c in itertools.combinations(range(0, 95), 4) if sum(c) == 305]
opt = {'A 最低分为60': lambda c: min(c) == 60, 'B 有2人低于60': lambda c: sum(x < 60 for x in c) >= 2, 'C 第二名94分': lambda c: max(c) == 94, 'D 有3人在80分以上': lambda c: sum(x > 80 for x in c) + 1 >= 3}
pos = {k: any(f(c) for c in S) for k, f in opt.items()}
flag('D36-9-2 唯一不可能为真 -> B', [k for k, p in pos.items() if not p] == ['B 有2人低于60'], pos)
# 辛普森：若两院都是"重症成功率<轻症成功率"，甲院两层都更高而总体更低，则甲院重症占比一定更高（网格穷举找反例）
grid = [F(k, 10) for k in range(1, 10)]
counter = 0
for Al in grid:
    for Ah in grid:
        for Bl in grid:
            for Bh in grid:
                if not (Al > Bl and Ah > Bh and Bh < Bl and Ah < Al):
                    continue
                for a in grid:
                    for b in grid:
                        if a * Ah + (1 - a) * Al < b * Bh + (1 - b) * Bl and not a > b:
                            counter += 1
ex = (F(3, 10) * 98 + F(7, 10) * 80, F(9, 10) * 96 + F(1, 10) * 75)
flag(f'D36-9-3 辛普森：网格穷举反例数={counter}；示例 甲院总体{float(ex[0]):.1f}%<乙院{float(ex[1]):.1f}%（甲院重症占70%>乙院10%）', counter == 0 and ex[0] < ex[1])
fee = lambda t: 3 * min(t, 15) + 5 * max(t - 15, 0)
flag(f'D36-10-1 阶梯水价：甲20吨={fee(20)}元，乙10吨={fee(10)}元（>2倍）；甲均价{fee(20) / 20}元；乙15吨={fee(15)}元', fee(20) > 2 * fee(10) and fee(20) / 20 != 4 and fee(15) <= 50)
z = lambda x: F(x - 70, 10)
flag('D36-10-2 标准分：70分->0；90分->2；相差10分->标准分差1', z(70) == 0 and z(90) == 2 and z(80) - z(70) == 1 and z(72) != 2)
flag('D36-12-6 夜校：去年100期；每期平均人次为去年的1.25倍', F(120) / F(12, 10) == 100 and F(15, 10) / F(12, 10) == F(5, 4))
print('ALL IDEAS OK' if ok else 'SOME IDEAS BAD')
