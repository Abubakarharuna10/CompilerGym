"""Generate enum declarations for LLVM capabilities.

Usage: make_specs.py <output_path>.
"""
# TODO: As we add support for more compilers we could generalize this script
# to work with other compiler services rather than hardcoding to LLVM.
import sys

from compiler_gym.envs.llvm.llvm_env import LlvmEnv
from compiler_gym.util.runfiles_path import runfiles_path


def main(argv):
    assert len(argv) == 2, "Usage: make_specs.py <output_path>"
    env = LlvmEnv(
        runfiles_path("compiler_gym/envs/llvm/service/compiler_gym-llvm-service")
    )
    try:
        with open(argv[1], "w") as f:
            print("from enum import Enum", file=f)
            print(file=f)
            print("class observation_spaces(Enum):", file=f)
            for name in env.observation.spaces:
                print(f'    {name} = "{name}"', file=f)
            print(file=f)
            print("class reward_spaces(Enum):", file=f)
            for name in env.reward.spaces:
                print(f'    {name} = "{name}"', file=f)
    finally:
        env.close()


if __name__ == "__main__":
    main(sys.argv)
