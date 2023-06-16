from runner import Runner
from environment.battle_simulation import BattleEnv
from environment.arguments import get_env_common_args
from common.arguments import get_rl_common_args, get_coma_args, get_mixer_args, get_centralv_args, get_reinforce_args, \
    get_commnet_args, get_g2anet_args

if __name__ == '__main__':
    for i in range(4):
        env_args = get_env_common_args()
        rl_args = get_rl_common_args()
        if rl_args.alg.find('coma') > -1:
            args = get_coma_args(rl_args)
        elif rl_args.alg.find('central_v') > -1:
            args = get_centralv_args(rl_args)
        elif rl_args.alg.find('reinforce') > -1:
            rl_args = get_reinforce_args(rl_args)
        else:
            rl_args = get_mixer_args(rl_args)
        if rl_args.alg.find('commnet') > -1:
            rl_args = get_commnet_args(rl_args)
        if rl_args.alg.find('g2anet') > -1:
            rl_args = get_g2anet_args(rl_args)
        env = BattleEnv(env_args, rl_args)
        env_info = env.get_env_info()
        rl_args.n_actions = env_info["n_actions"]
        rl_args.n_agents = env_info["n_agents"]
        rl_args.state_shape = env_info["state_shape"]
        rl_args.obs_shape = env_info["obs_shape"]
        rl_args.episode_limit = env_info["episode_limit"]
        rl_args.map = env_info["map"]
        runner = Runner(env, rl_args)
        if not rl_args.evaluate:
            runner.run(i)
        else:
            win_rate, _ = runner.evaluate()
            print('The win rate of {} is  {}'.format(rl_args.alg, win_rate))
            break
        env.close()
