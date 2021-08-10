from typing import List

import gym


class RandomPolicy:
    def __init__(self, action_spaces: List[gym.Space]) -> None:
        self.action_spaces = action_spaces

    def get_action(self, observations: dict, agent: str) -> dict:
        return self.action_spaces[agent].sample()
