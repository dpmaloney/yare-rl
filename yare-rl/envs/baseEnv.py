from typing import Union, Callable, List
from ctypes import CDLL, c_uint, c_char_p

import gym

from bindings.yare import YareBindings, TICKFN

class BaseEnv(gym.Env):
    def __init__(self, replay_path: str, shapes: List[int] = [0, 0], 
                 bot_fns: List[Callable[[int], None]] = [(lambda _: None), (lambda _: None)]):
        """
        Args:
            replay_path: where to save json replay
            shape_0: shape of player 1's spirits (0, 1 or 2)
            shape_1: similar to shape_0 for player 2
            bot_fn_1: function that runs player 1's bot at each tick
            bot_fn_2: similar to bot_fn_1 for player 2
        """
        self.replay_path = replay_path
        self.shapes = shapes
        self.bot_fns = [self._bot_wrapper(bot_fn) for bot_fn in bot_fns]

    def step(self, actions: dict) -> Union[dict, dict, dict, dict]:
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Args:
            actions (object): an action provided by the agent

        Returns:
            observation (object): agent's observation of the current environment
            reward (float): amount of reward returned after previous action
            done (bool): whether the episode has ended, in which case further step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for debugging, and sometimes learning)
        """
        self.env.headless_update_env(self.yare_ptr)
        self.process_actions(0, actions)
        self.env.headless_gather_commands(self.yare_ptr, c_uint(0))
        self.process_actions(1, actions)
        self.env.headless_gather_commands(self.yare_ptr, c_uint(1))
        result: int = self.env.headless_process_commands(self.yare_ptr).result
        observations: dict = self.build_observations()
        rewards: dict = self.build_rewards()
        dones: dict = self.build_dones(result)
        info: dict = self.build_info()
        return observations, rewards, dones, info


    def reset(self) -> dict:
        """Resets the environment to an initial state and returns an initial
        observation.

        Note that this function should not reset the environment's random
        number generator(s); random variables in the environment's state should
        be sampled independently between multiple calls to `reset()`. In other
        words, each call of `reset()` should yield an environment suitable for
        a new episode, independent of previous episodes.

        Returns:
            observation (object): the initial observation.
        """
        self._init_game()

    def _init_game(self) -> None:
        self.env: CDLL = YareBindings().lib
        self.yare_ptr = self.env.headless_init(self.bot_fns[0], c_uint(self.shapes[0]), 
                                               self.bot_fns[1], c_uint(self.shapes[1]),
                                               c_char_p(str.encode(self.replay_path)))

    def _bot_wrapper(self, bot) -> Callable:
        def bot_fn(tick):
            return bot(self.env, tick)
        return TICKFN(bot_fn)

    def process_actions(self, player: int, actions: dict) -> None:
        """Method must be implemented by subclass."""
        pass

    def build_observations(self) -> dict:
        """Method must be implemented by subclass."""
        return {}

    def build_rewards(self) -> dict:
        """Method must be implemented by subclass."""
        return {}

    def build_dones(self, result: int) -> dict:
        """Method must be implemented by subclass."""
        return {"__all__": result >= 0}

    def build_info(self) -> dict:
        """Method must be implemented by subclass."""
        return {}

    @property
    def action_spaces(self) -> List[gym.Space]:
        raise NotImplementedError("Method must be implemented by subclass.")

    @property
    def observation_spaces(self) -> List[gym.Space]:
        raise NotImplementedError("Method must be implemented by subclass.")
