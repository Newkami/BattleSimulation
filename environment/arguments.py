import argparse


# 环境参数
def get_env_common_args():
    parser = argparse.ArgumentParser(description="the necessrary params of environments")

    parser.add_argument('--difficulty', type=int, default=2, help='任务难度')  # 0 Easy 1 Medium 2 Difficulty
    parser.add_argument('--n_jammer', type=int, default=2, help='干扰机数量')
    parser.add_argument('--n_missilevehicle', type=int, default=2, help='导弹车数量')
    parser.add_argument('--n_radar', type=int, default=3, help='雷达数量')
    parser.add_argument('--n_antiAirturrent', type=int, default=2, help='防空炮数量')
    parser.add_argument('--n_commandpost', type=int, default=1, help='指挥所数量')

    parser.add_argument('--mapX', type=int, default=50, help='the X of map size')
    parser.add_argument('--mapY', type=int, default=50, help='the Y of map size')

    parser.add_argument('--jammer_strike_ability', type=int, default=3, help='干扰机打击能力')
    parser.add_argument('--jm_maxHP', type=int, default=100, help='干扰机最大耐久')
    parser.add_argument('--attack_range', type=int, default=10, help='干扰机攻击范围')
    parser.add_argument('--repair_coef', type=float, default=0.2, help='干扰机修复系数')
    parser.add_argument('--min_takeoff_hp', type=int, default=50, help='干扰机最小起飞耐久')

    parser.add_argument('--mv_maxHP', type=int, default=100, help='导弹车最大耐久')
    parser.add_argument('--mv_strike_ability', type=int, default=3, help='导弹车打击能力')  # 5 4 3 fixme:这个值在目前的场景中基本触发不到
    parser.add_argument('--mv_attack_range', type=float, default=3, help='导弹车打击范围')  # 5 4 3 fixme:这个值在目前的场景中基本触发不到

    parser.add_argument('--rd_maxHP', type=int, default=100, help='雷达最大耐久')
    parser.add_argument('--detect_radius', type=float, default=15, help='雷达探测半径')  # 5 4 3 fixme:这个值在目前的场景中基本触发不到

    parser.add_argument('--aat_maxHP', type=int, default=100, help='防空炮最大耐久')
    parser.add_argument('--defend_radius', type=float, default=15, help='防空炮防卫半径')  # 8 6 5
    parser.add_argument('--defend_coef', type=float, default=0.3, help='防空炮防卫系数')  # 0.6 0.4 0.3

    parser.add_argument('--cp_maxHP', type=int, default=100, help='防空炮最大耐久')

    parser.add_argument('--plot', type=bool, default=True)

    parser.add_argument('--damage_to_jammer', type=int, default=30, help='无人机对干扰机的百分比伤害')
    parser.add_argument('--damage_to_mv', type=int, default=40, help='无人机对导弹车的百分比伤害')
    parser.add_argument('--damage_to_rd', type=int, default=50, help='无人机对雷达的百分比伤害')
    parser.add_argument('--damage_to_aat', type=int, default=60, help='无人机对防空炮的百分比伤害')
    parser.add_argument('--damage_to_cp', type=int, default=70, help='无人机对指挥所的百分比伤害')

    args = parser.parse_args()
    return args


# 无人机参数

def get_multirotor_args():
    parser = argparse.ArgumentParser(description="the necessrary params of Multirotor")
    parser.add_argument('--x_cord', type=int, default=-1, help='无人机初始x坐标')
    parser.add_argument('--y_cord', type=int, default=-1, help='无人机初始y坐标')
    parser.add_argument('--steps', type=int, default=3, help='无人机的移动步数')
    parser.add_argument('--attack_range', type=int, default=3, help='无人机攻击范围')
    parser.add_argument('--detect_range', type=int, default=5, help='无人机探测范围')
    args = parser.parse_args()
    return args
