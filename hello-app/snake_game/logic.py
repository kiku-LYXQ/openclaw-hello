"""贪吃蛇核心逻辑模块。"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
import random
from typing import Deque, Iterable, List, Optional, Tuple

Point = Tuple[int, int]


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def vector(self) -> Point:
        return self.value

    def opposite(self) -> "Direction":
        dx, dy = self.value
        return Direction((-dx, -dy))


@dataclass
class GameConfig:
    width: int = 20
    height: int = 20
    initial_length: int = 4

    def __post_init__(self) -> None:
        if self.width < 5 or self.height < 5:
            raise ValueError("地图太小，宽高至少 5")
        if self.initial_length < 2:
            raise ValueError("初始蛇身长度至少 2")
        if self.initial_length >= self.width:
            raise ValueError("初始蛇身过长，须小于地图宽度")


@dataclass(frozen=True)
class GameSnapshot:
    snake: Tuple[Point, ...]
    food: Point
    score: int
    width: int
    height: int
    game_over: bool
    direction: Direction
    steps: int


class SnakeGame:
    """贪吃蛇状态机，独立于界面。"""

    def __init__(self, config: Optional[GameConfig] = None, *, random_seed: Optional[int] = None):
        self.config = config or GameConfig()
        self._random = random.Random(random_seed)
        self.reset()

    def reset(self) -> GameSnapshot:
        """重置游戏返回初始快照。"""
        self.direction = Direction.RIGHT
        center_x = self.config.width // 2
        center_y = self.config.height // 2
        self.snake: Deque[Point] = deque()
        for offset in range(self.config.initial_length):
            self.snake.append((center_x - offset, center_y))
        self.score = 0
        self.game_over = False
        self.steps = 0
        self.food = self._place_food()
        self._snapshot = self._build_snapshot()
        return self._snapshot

    def step(self, direction: Optional[Direction] = None) -> GameSnapshot:
        """前进一步，返回新的快照。"""
        if self.game_over:
            return self._snapshot
        if direction is not None:
            self._try_change_direction(direction)
        next_head = self._next_head_position()
        if self._is_collision(next_head):
            self.snake.appendleft(next_head)
            self.game_over = True
            self._snapshot = self._build_snapshot()
            return self._snapshot
        self.snake.appendleft(next_head)
        if next_head == self.food:
            self.score += 1
            self.food = self._place_food()
        else:
            self.snake.pop()
        self.steps += 1
        self._snapshot = self._build_snapshot()
        return self._snapshot

    def _try_change_direction(self, candidate: Direction) -> None:
        if candidate == self.direction.opposite():
            return
        self.direction = candidate

    def _next_head_position(self) -> Point:
        dx, dy = self.direction.vector
        head_x, head_y = self.snake[0]
        return head_x + dx, head_y + dy

    def _is_collision(self, candidate: Point) -> bool:
        x, y = candidate
        if not (0 <= x < self.config.width and 0 <= y < self.config.height):
            return True
        if candidate in self.snake:
            if candidate == self.snake[-1]:
                return False
            return True
        return False

    def _place_food(self) -> Point:
        occupied = set(self.snake)
        all_cells = [
            (x, y)
            for y in range(self.config.height)
            for x in range(self.config.width)
            if (x, y) not in occupied
        ]
        if not all_cells:
            self.game_over = True
            return self.snake[0]
        return self._random.choice(all_cells)

    def _build_snapshot(self) -> GameSnapshot:
        return GameSnapshot(
            snake=tuple(self.snake),
            food=self.food,
            score=self.score,
            width=self.config.width,
            height=self.config.height,
            game_over=self.game_over,
            direction=self.direction,
            steps=self.steps,
        )

    def get_snapshot(self) -> GameSnapshot:
        """获取当前快照。"""
        return self._snapshot
