import os

import ray
from ray.tune.registry import register_env
from ray.rllib.agents.registry import get_agent_class
from ray.tune import run

from utils import load_config, env_creater, config_multiagent
from rllibEnv import rllibMultiAgentWrapper


def add_parse_args(parser):
    parser.add_argument("--checkpoint", type=str, help="Checkpoint from which to train.")
    parser.add_argument("--checkpoint_freq", type=int, default=10, help="Number of episodes between checkpoints.")
    parser.add_argument("--config",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml"),
        help="Configuration file used to train the checkpoint.")
    parser.add_argument("--algorithm", default="PPO", help="Algorithm used for training.") # TODO: allow for QMIX (https://docs.ray.io/en/master/rllib-algorithms.html#qmix-monotonic-value-factorisation-qmix-vdn-iqn)
    parser.add_argument("--results_dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"),
        help="Directory where training results are saved.")
    return parser.parse_args()

def train():
    args = add_parse_args()

    config = load_config(args.config)
    config["env_config"] = {
        "replay_path": "replay.json",
        "shapes": [0, 0],
    }
    register_env(env_creater)

    ray.init()

    dummy_env = rllibMultiAgentWrapper(**config["env_config"])
    config_multiagent(
        config,
        dummy_env.observation_space,
        dummy_env.action_space,
        args.policies,
        policies_to_train=args.policies_to_train,
        num_learners=args.num_learned_policies)

    cls = get_agent_class(args.algorithm)

    results = run(
        cls,
        config=config,
        checkpoint_freq=args.checkpoint_freq,
        local_dir=args.results_dir,
        restore=args.checkpoint)

if __name__ == '__main__':
    train()
