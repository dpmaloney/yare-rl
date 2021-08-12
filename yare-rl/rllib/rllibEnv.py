from typing import List, Callable

from ray import rllib

from ..envs.multiAgentEnv import MultiAgentEnv


class rllibMultiAgentWrapper(rllib.MultiAgentEnv):
    def __init__(self, replay_path: str, shapes: List[int] = [0, 0], 
                 bot_fns: List[Callable[[int], None]] = [(lambda _: None), (lambda _: None)]):
        self.env = MultiAgentEnv(replay_path, shapes, bot_fns)
        self.observation_space = self.env.observation_space
        self.action_space = self.env.action_space

    def step(self, actions):
        observations, rewards, dones, info = self.env.step(actions)
        dones["__all__"] = all(dones)
        return observations, rewards, dones, info

    def reset(self):
        return self.env.reset()
