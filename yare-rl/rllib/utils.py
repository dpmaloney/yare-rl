import yaml
import functools

from ..envs.multiAgentEnv import MultiAgentEnv


def select_policy(policies, agent_id):
    raise NotImplementedError("TODO")


def env_creater(mpe_args):
    return MultiAgentEnv(**mpe_args)


def load_config(path):
    with open(path) as f:
        # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
        config = yaml.load(f, Loader=yaml.SafeLoader)
    return config


def config_multiagent(
        config,
        obs_space,
        act_space,
        policies,
        policies_to_train,
        num_learners,
        framework="tf"):
    learned_policies_config = (None, obs_space, act_space, {"framework": framework})
    config["multiagent"] = {
        "policies_to_train": policies_to_train,
        "policy_mapping_fn": functools.partial(select_policy, policies)
    }
    config["multiagent"]["policies"].update(
        {f"policy-{i}": learned_policies_config for i in range(0, num_learners)})
    return config