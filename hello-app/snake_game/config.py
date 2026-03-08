"""游戏常量配置，逻辑层可直接引用。"""

from __future__ import annotations

import os
from typing import Final


# 默认常量
_DEFAULT_GRID_WIDTH: Final = 20
"""默认网格宽度（列数）。"""

_DEFAULT_GRID_HEIGHT: Final = 20
"""默认网格高度（行数）。"""

_DEFAULT_TICK_INTERVAL: Final = 0.18  # 秒 / 帧
"""游戏更新帧率间隔，界面可据此设置定时器。"""

MIN_GRID_DIMENSION: Final = 5
"""允许的最小地图维度，避免太小导致行为异常。"""

_MIN_SNAKE_LENGTH: Final = 2
"""允许的最小初始蛇长。"""

_MAX_SNAKE_LENGTH: Final = 4
"""默认初始长度的上限，保持与现有地图兼容。"""


def _read_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"环境变量 {name} 必须是整数: {value!r}") from exc
    if parsed <= 0:
        raise ValueError(f"环境变量 {name} 必须是正整数: {parsed}")
    return parsed


def _read_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValueError(f"环境变量 {name} 必须是数字: {value!r}") from exc
    if parsed <= 0:
        raise ValueError(f"环境变量 {name} 必须是大于 0 的数: {parsed}")
    return parsed


def _derive_initial_length(width: int, height: int) -> int:
    """根据地图尺寸推导默认初始蛇长，保持与现有逻辑兼容。"""
    safe_max = min(_MAX_SNAKE_LENGTH, width - 1, height - 1)
    return max(_MIN_SNAKE_LENGTH, safe_max)


GRID_WIDTH: Final = _read_int("SNAKE_GRID_WIDTH", _DEFAULT_GRID_WIDTH)
"""网格宽度（列数）。可通过环境变量 SNAKE_GRID_WIDTH 调整。"""

GRID_HEIGHT: Final = _read_int("SNAKE_GRID_HEIGHT", _DEFAULT_GRID_HEIGHT)
"""网格高度（行数）。可通过环境变量 SNAKE_GRID_HEIGHT 调整。"""

INITIAL_SNAKE_LENGTH: Final = _derive_initial_length(GRID_WIDTH, GRID_HEIGHT)
"""游戏开始时蛇身的初始长度，依赖 GRID_WIDTH/GRID_HEIGHT 保持合法。"""

TICK_INTERVAL: Final = _read_float("SNAKE_TICK_INTERVAL", _DEFAULT_TICK_INTERVAL)
"""游戏更新帧率间隔，界面可据此设置定时器，可通过环境变量调整。"""

DIRECTION_HINT = "方向键↑↓←→ 或 WASD 控制移动。"
"""用于向用户提示操控方式。"""
