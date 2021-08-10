import argparse

import gym
from pettingzoo.butterfly import knights_archers_zombies_v7

from env import YareEnv
from policies import RandomPolicy


def random_baseline(env: gym.Env) -> None:
    policy = RandomPolicy(env.action_spaces)
    while True:
        observations = env.reset()
        max_steps: int = 1000
        for _ in range(max_steps):
            actions = {
                agent: policy.get_action(
                    observations[agent],
                    agent) for agent in env.agents}
            observations, rewards, dones, infos = env.step(actions)
            env.render()
            if all(dones):
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--env',
        default="yare",
        choices=[
            "yare",
            "butterfly"],
        help='Environment to train in.')
    args = parser.parse_args()

    if args.env == "yare":
        env = YareEnv()
    elif args.env == "butterfly":
        env = knights_archers_zombies_v7.parallel_env()
    else:
        raise NotImplementedError

    random_baseline(env)
