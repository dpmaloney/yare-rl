from typing import Union, Callable
from ctypes import c_uint

import gym

from bindings.yare import YareBindings, TICKFN

NUM_PLAYERS = 2

class YareEnv(gym.Env):
    def __init__(self, shape_0: int = 0, shape_1: int = 0, 
                 bot_fn_1: Callable[[int], None] = (lambda x: None), 
                 bot_fn_2: Callable[[int], None] = (lambda x: None)) -> None:
        """
        Args:
            shape_0: shape of player 1's spirits (0, 1 or 2)
            shape_1: similar to shape_0 for player 2
            bot_fn_1: function that runs player 1's bot at each tick
            bot_fn_2: similar to bot_fn_1 for player 2
        """
        self.action_spaces: gym.Space = [gym.spaces.Discrete(10) for _ in range(NUM_PLAYERS)]
        self.observation_spaces: gym.Space = [gym.spaces.Discrete(10) for _ in range(NUM_PLAYERS)]
        self.shape_0 = shape_0
        self.shape_1 = shape_1
        self.bot_fn_1 = bot_fn_1
        self.bot_fn_2 = bot_fn_2

    def step(self, actions: dict) -> Union[dict, float, bool, dict]:
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
        self._process_actions(actions)
        self.env.headless_gather_commands(self.yare_ptr, c_uint(0))
        self.env.headless_gather_commands(self.yare_ptr, c_uint(1))
        result: int = self.env.headless_process_commands(self.yare_ptr).result


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
        print("Environment instantiated")

    def _process_actions(self, actions: dict) -> None:
        # self.env.spirit_goto(0, 500, 500)
        return None

    def _init_game(self) -> None:
        self.env: YareEnv = YareBindings().lib

        # TODO: allow custom bot functions
        # def partial_bot(bot_fn):
        #     def wrapper(tick):
        #         bot_fn(self.env, tick)
        #     return TICKFN(wrapper)

        def print_pos(_):
            print(self.env.spirit_position(0).x, self.env.spirit_position(0).y)
            return

        bot1 = TICKFN(print_pos)
        bot2 = TICKFN(print_pos)
        i = c_uint(0)
        self.yare_ptr = self.env.headless_init(bot1, i, bot2, i)
        print("ptr", self.yare_ptr)
