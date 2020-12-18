# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
"""Unit tests for //compiler_gym/util:timer."""
from compiler_gym.util import timer
from tests.test_main import main


def test_humanize_duration_seconds():
    assert timer.humanize_duration(5) == "5.000s"
    assert timer.humanize_duration(500.111111) == "500.1s"


def test_humanize_duration_ms():
    assert timer.humanize_duration(0.0055) == "5.5ms"
    assert timer.humanize_duration(0.5) == "500.0ms"
    assert timer.humanize_duration(0.51) == "510.0ms"
    assert timer.humanize_duration(0.9999) == "999.9ms"


def test_humanize_duration_us():
    assert timer.humanize_duration(0.0005) == "500.0us"
    assert timer.humanize_duration(0.0000119) == "11.9us"


def test_humanize_duration_ns():
    assert timer.humanize_duration(0.0000005) == "500.0ns"
    assert timer.humanize_duration(0.0000000019) == "1.9ns"


def test_humanize_duration_negative_seconds():
    assert timer.humanize_duration(-1.5) == "-1.500s"


if __name__ == "__main__":
    main()
