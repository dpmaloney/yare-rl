import argparse

import gym

from env import YareEnv
from policies import RandomPolicy


def random_baseline(env: gym.Env) -> None:
    policy = RandomPolicy(env.action_spaces)
    while True:
        observations = env.reset()
        max_steps: int = 10000
        for _ in range(max_steps):
            actions = {} # {agent: policy.get_action(observations[agent], agent) for agent in env.agents}
            observations, rewards, done, infos = env.step(actions)
            if done:
                break


def bot1_fn(env, tick):
    print(tick, env.spirit_position(0).x, env.spirit_position(0).y)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--shape_0', default=0, type=int, choices=[0, 1, 2],
                        help="Shape of player 1's spirits")
    parser.add_argument('--shape_1', default=0, type=int, choices=[0, 1, 2],
                        help="Shape of player 2's spirits")
    args = parser.parse_args()

    env = YareEnv(args.shape_0, args.shape_1, bot1_fn)

    random_baseline(env)
