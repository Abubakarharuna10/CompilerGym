# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Tests for the example CompilerGym service."""
import gym
import numpy as np
import pytest
from gym.spaces import Box

import examples.example_compiler_gym_service  # Register environments.
from compiler_gym.envs import CompilerEnv
from compiler_gym.spaces import NamedDiscrete, Sequence
from tests.test_main import main


@pytest.fixture(scope="function")
def env() -> CompilerEnv:
    env = gym.make("example-v0")
    try:
        yield env
    finally:
        env.close()


def test_action_space(env: CompilerEnv):
    assert env.action_spaces == [
        NamedDiscrete(
            name="default",
            items=["a", "b", "c"],
        )
    ]


def test_observation_space_list(env: CompilerEnv):
    env.reset()
    env.observation.spaces = {
        "ir": Sequence(size_range=(0, None)),
        "features": Box(shape=(3,), low=-100, high=100),
    }


def test_reward_space_list(env: CompilerEnv):
    env.reset()
    env.reward.ranges = {
        "codesize": (None, 0),
    }


def test_takeAction_before_startEpisode(env: CompilerEnv):
    with pytest.raises(Exception):
        env.step(0)


def test_observation_before_startEpisode(env: CompilerEnv):
    with pytest.raises(TypeError) as ctx:
        _ = env.observation["ir"]
    assert str(ctx.value) == "No episode"


def test_reward_before_reset(env: CompilerEnv):
    with pytest.raises(TypeError) as ctx:
        _ = env.reward["codesize"]
    assert str(ctx.value) == "No episode"


def test_reset_invalid_benchmark(env: CompilerEnv):
    with pytest.raises(ValueError) as ctx:
        env.reset(benchmark="foobar")
    assert str(ctx.value) == "Unknown program name"


def test_invalid_eager_observation_space(
    env: CompilerEnv,
):
    with pytest.raises(LookupError):
        env.eager_observation_space = 100


def test_invalid_eager_reward_space(
    env: CompilerEnv,
):
    with pytest.raises(LookupError):
        env.eager_reward_space = 100


def test_double_reset(env: CompilerEnv):
    env.reset()
    env.reset()


def test_takeAction_out_of_range(env: CompilerEnv):
    env.reset()
    with pytest.raises(ValueError) as ctx:
        env.step(100)
    assert str(ctx.value) == "Out-of-range"


def test_eager_ir_observation(env: CompilerEnv):
    env.eager_observation_space = "ir"
    observation = env.reset()
    assert observation == "Hello, world!"

    observation, reward, done, info = env.step(0)
    assert observation == "Hello, world!"
    assert reward is None
    assert not done


def test_eager_features_observation(
    env: CompilerEnv,
):
    env.eager_observation_space = "features"
    observation = env.reset()
    assert isinstance(observation, np.ndarray)
    assert observation.shape == (3,)
    assert observation.dtype == np.int64
    assert observation.tolist() == [0, 0, 0]


def test_eager_reward(env: CompilerEnv):
    env.eager_reward_space = "codesize"
    env.reset()
    observation, reward, done, info = env.step(0)
    assert observation is None
    assert reward == 0
    assert not done


def test_getObservation_ir(env: CompilerEnv):
    env.reset()
    assert env.observation["ir"] == "Hello, world!"


def test_getReward(env: CompilerEnv):
    env.reset()
    assert env.reward["codesize"] == 0


def test_benchmarks(env: CompilerEnv):
    assert env.benchmarks == ["foo", "bar"]


if __name__ == "__main__":
    main()
