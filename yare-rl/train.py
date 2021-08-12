import argparse

import gym

from envs.baseEnv import BaseEnv
from policies import RandomPolicy


def random_baseline(env: gym.Env) -> None:
    # policy = RandomPolicy(env.action_spaces) TODO: implement observation space
    # training loop
    while True: 
        observations = env.reset()
         # episode loop
        while True:
            actions = {} # TODO: policy is not valid yet to pass {agent: policy.get_action(observations[agent], agent) for agent in env.agents}
            observations, rewards, done, infos = env.step(actions)
            if done["__all__"]:
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--shape_0', default=0, type=int, choices=[0, 1, 2],
                        help="Shape of player 1's spirits")
    parser.add_argument('--shape_1', default=0, type=int, choices=[0, 1, 2],
                        help="Shape of player 2's spirits")
    args = parser.parse_args()


    def print_pos(env, tick):
        print(tick, env.spirit_position(0).x, env.spirit_position(0).y)
        return

    env = BaseEnv("replay.json", [args.shape_0, args.shape_1], [print_pos, print_pos])

    random_baseline(env)
