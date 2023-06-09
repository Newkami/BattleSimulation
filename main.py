from environment.enemy import Jammer, Radar, MissileVehicle
from environment.arguments import get_env_common_args

if __name__ == '__main__':
    args = get_env_common_args()
    mv = MissileVehicle(args, 1, 2, 3)
    mv.hp_to_strike_ability()
    # print(args)
