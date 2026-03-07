"""终端界面层，基于 curses。"""
from __future__ import annotations

import curses
import time
from typing import Dict

from .config import DIRECTION_HINT, GRID_HEIGHT, GRID_WIDTH, TICK_INTERVAL
from .logic import Direction, GameConfig, SnakeGame

KEY_DIRECTION: Dict[int, Direction] = {
    curses.KEY_UP: Direction.UP,
    curses.KEY_DOWN: Direction.DOWN,
    curses.KEY_LEFT: Direction.LEFT,
    curses.KEY_RIGHT: Direction.RIGHT,
    ord("w"): Direction.UP,
    ord("W"): Direction.UP,
    ord("s"): Direction.DOWN,
    ord("S"): Direction.DOWN,
    ord("a"): Direction.LEFT,
    ord("A"): Direction.LEFT,
    ord("d"): Direction.RIGHT,
    ord("D"): Direction.RIGHT,
}

EXIT_KEYS = {ord("q"), ord("Q"), 27}
RESTART_KEYS = {ord("r"), ord("R")}


class TerminalUI:
    """封装 curses 的游戏渲染与交互。"""

    def __init__(self, stdscr: "curses._CursesWindow") -> None:
        config = GameConfig(width=GRID_WIDTH, height=GRID_HEIGHT)
        self.stdscr = stdscr
        self.game = SnakeGame(config=config)
        self.board_top = 4
        self.board_left = 4

    def run(self) -> None:
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        try:
            if not self._fits_screen():
                self._draw_too_small_message()
                self.stdscr.getch()
                return
            self._loop()
        finally:
            curses.curs_set(1)
            curses.nocbreak()
            self.stdscr.keypad(False)
            curses.echo()

    def _fits_screen(self) -> bool:
        required_rows = self.board_top + GRID_HEIGHT + 3
        required_cols = self.board_left + GRID_WIDTH + 2
        return curses.LINES >= required_rows and curses.COLS >= required_cols

    def _draw_too_small_message(self) -> None:
        self.stdscr.clear()
        msg = (
            "终端窗口太小，最少需要 {} 行 x {} 列。"
            "请调整终端大小后重试。".format(
                self.board_top + GRID_HEIGHT + 3, self.board_left + GRID_WIDTH + 2
            )
        )
        self.stdscr.addstr(0, 0, msg)
        self.stdscr.addstr(2, 0, "按任意键退出。")
        self.stdscr.refresh()

    def _loop(self) -> None:
        snapshot = self.game.get_snapshot()
        self._render(snapshot)
        while True:
            frame_start = time.monotonic()
            key = self.stdscr.getch()
            if key in EXIT_KEYS:
                break
            direction = KEY_DIRECTION.get(key)
            snapshot = self.game.step(direction)
            self._render(snapshot)
            if snapshot.game_over:
                decision = self._handle_game_over(snapshot)
                if decision == "restart":
                    snapshot = self.game.reset()
                    self._render(snapshot)
                    continue
                break
            self._wait_frame(frame_start)

    def _wait_frame(self, start: float) -> None:
        elapsed = time.monotonic() - start
        delay = max(0.0, TICK_INTERVAL - elapsed)
        if delay:
            time.sleep(delay)

    def _render(self, snapshot) -> None:
        self.stdscr.erase()
        self._draw_header(snapshot)
        self._draw_board(snapshot)
        self._draw_footer(snapshot)
        self.stdscr.refresh()

    def _draw_header(self, snapshot) -> None:
        title = f"终端贪吃蛇 | 地图 {snapshot.width}x{snapshot.height}"
        score = f"分数: {snapshot.score}  步数: {snapshot.steps}"
        hints = f"{DIRECTION_HINT}  按 Q 退出，游戏结束后按 R 重新开始。"
        self.stdscr.addstr(0, 0, title)
        self.stdscr.addstr(1, 0, score)
        self.stdscr.addstr(2, 0, hints)

    def _draw_board(self, snapshot) -> None:
        head = snapshot.snake[0]
        body = set(snapshot.snake[1:])
        for row in range(snapshot.height):
            for col in range(snapshot.width):
                cell = " "
                if (col, row) == snapshot.food:
                    cell = "*"
                elif (col, row) == head:
                    cell = "@"
                elif (col, row) in body:
                    cell = "O"
                else:
                    cell = "."
                self.stdscr.addch(self.board_top + row, self.board_left + col, cell)

    def _draw_footer(self, snapshot) -> None:
        footer = "按 Q 立即退出；游戏结束自动暂停，按 R 重玩。"
        self.stdscr.addstr(self.board_top + snapshot.height + 1, 0, footer)

    def _handle_game_over(self, snapshot) -> str:
        msg = "游戏结束！按 R 重玩，Q 退出。"
        self.stdscr.addstr(self.board_top + snapshot.height + 3, 0, msg)
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        try:
            while True:
                key = self.stdscr.getch()
                if key in RESTART_KEYS:
                    return "restart"
                if key in EXIT_KEYS:
                    return "quit"
        finally:
            self.stdscr.nodelay(True)
