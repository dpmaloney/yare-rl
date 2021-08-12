from typing import Union, Callable, List

import gym

from baseEnv import BaseEnv

class MultiAgentEnv(BaseEnv):
    def __init__(self, replay_path: str, shapes: List[int] = [0, 0], 
                 bot_fns: List[Callable[[int], None]] = [(lambda _: None), (lambda _: None)]):
        super().__init__(replay_path, shapes, bot_fns)

    def process_actions(self, player: int, actions: dict) -> None:
        raise NotImplementedError("TODO")

    def build_observation(self) -> dict:
        raise NotImplementedError("TODO")

    def build_rewards(self) -> dict:
        raise NotImplementedError("TODO")

    def build_dones(self, result: int) -> dict:
        raise NotImplementedError("TODO")

    def build_info(self) -> dict:
        raise NotImplementedError("TODO")

    @property
    def action_spaces(self) -> List[gym.Space]:
        raise NotImplementedError("TODO")

    @property
    def observation_spaces(self) -> List[gym.Space]:
        raise NotImplementedError("TODO")
