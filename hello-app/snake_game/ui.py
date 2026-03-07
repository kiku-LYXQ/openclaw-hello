"""基于 curses 的终端界面。"""
from __future__ import annotations

import curses
import time
from typing import Dict

from .config import DIRECTION_HINT, GRID_HEIGHT, GRID_WIDTH, TICK_INTERVAL
from .logic import Direction, GameConfig, GameSnapshot, SnakeGame


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

    HEADER_LINES = 3
    FOOTER_LINES = 2
    WINDOW_MARGIN = 2

    def __init__(self, stdscr: "curses._CursesWindow") -> None:
        self.stdscr = stdscr
        self.config = GameConfig(width=GRID_WIDTH, height=GRID_HEIGHT)
        self.game = SnakeGame(config=self.config)
        self.board_height = self.config.height
        self.board_width = self.config.width
        self.board_top = self.HEADER_LINES + self.WINDOW_MARGIN
        self.board_left = self.WINDOW_MARGIN
        self.head_attr = curses.A_NORMAL
        self.body_attr = curses.A_NORMAL
        self.food_attr = curses.A_NORMAL

    def run(self) -> None:
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        self._update_layout()
        self._init_colors()
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

    def _init_colors(self) -> None:
        if not curses.has_colors():
            return
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_CYAN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        self.head_attr = curses.color_pair(1) | curses.A_BOLD
        self.body_attr = curses.color_pair(2)
        self.food_attr = curses.color_pair(3) | curses.A_BOLD

    def _loop(self) -> None:
        snapshot = self.game.get_snapshot()
        self._render(snapshot)
        while True:
            frame_start = time.monotonic()
            key = self.stdscr.getch()
            if key == curses.KEY_RESIZE:
                curses.resize_term(0, 0)
                self._update_layout()
                if not self._fits_screen():
                    self._draw_too_small_message()
                    self.stdscr.getch()
                    break
                self._render(snapshot)
                continue
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

    def _render(self, snapshot: GameSnapshot) -> None:
        self.stdscr.erase()
        if not self._fits_screen():
            self._draw_too_small_message()
            self.stdscr.refresh()
            return
        self._draw_header(snapshot)
        self._draw_board_border(snapshot)
        self._draw_board(snapshot)
        self._draw_footer(snapshot)
        self.stdscr.refresh()

    def _draw_header(self, snapshot: GameSnapshot) -> None:
        title = f"终端贪吃蛇 | 地图 {snapshot.width}x{snapshot.height}"
        score = f"分数: {snapshot.score}  步数: {snapshot.steps}"
        hints = f"{DIRECTION_HINT}  按 Q 退出，游戏结束后按 R 重新开始。"
        self._safe_addstr(0, 0, title, curses.A_BOLD)
        self._safe_addstr(1, 0, score)
        self._safe_addstr(2, 0, hints)

    def _draw_board_border(self, snapshot: GameSnapshot) -> None:
        top = self.board_top - 1
        left = self.board_left - 1
        bottom = self.board_top + snapshot.height
        right = self.board_left + snapshot.width
        self.stdscr.addch(top, left, curses.ACS_ULCORNER)
        self.stdscr.addch(top, right, curses.ACS_URCORNER)
        self.stdscr.addch(bottom, left, curses.ACS_LLCORNER)
        self.stdscr.addch(bottom, right, curses.ACS_LRCORNER)
        self.stdscr.hline(top, left + 1, curses.ACS_HLINE, snapshot.width)
        self.stdscr.hline(bottom, left + 1, curses.ACS_HLINE, snapshot.width)
        self.stdscr.vline(top + 1, left, curses.ACS_VLINE, snapshot.height)
        self.stdscr.vline(top + 1, right, curses.ACS_VLINE, snapshot.height)

    def _draw_board(self, snapshot: GameSnapshot) -> None:
        head = snapshot.snake[0]
        body = set(snapshot.snake[1:])
        for row in range(snapshot.height):
            for col in range(snapshot.width):
                coord = (col, row)
                if coord == snapshot.food:
                    char = "*"
                    attr = self.food_attr
                elif coord == head:
                    char = "@"
                    attr = self.head_attr
                elif coord in body:
                    char = "O"
                    attr = self.body_attr
                else:
                    char = "."
                    attr = curses.A_DIM
                try:
                    self.stdscr.addch(self.board_top + row, self.board_left + col, char, attr)
                except curses.error:
                    # 有可能在窗口收缩时越界，忽略异常
                    pass

    def _draw_footer(self, snapshot: GameSnapshot) -> None:
        if snapshot.game_over:
            footer = "游戏暂停，按 R 重玩，Q 退出。"
        else:
            footer = "按 Q/ESC 退出；游戏结束后可按 R 重玩。"
        self._safe_addstr(self.board_top + snapshot.height + 1, self.board_left, footer)

    def _handle_game_over(self, snapshot: GameSnapshot) -> str:
        prompt_y = self.board_top + snapshot.height + 3
        prompt = "游戏结束！按 R 重玩，Q 退出。"
        self._safe_addstr(prompt_y, self.board_left, prompt, curses.A_BOLD)
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        try:
            while True:
                key = self.stdscr.getch()
                if key in RESTART_KEYS:
                    return "restart"
                if key in EXIT_KEYS:
                    return "quit"
                if key == curses.KEY_RESIZE:
                    curses.resize_term(0, 0)
                    self._update_layout()
                    if not self._fits_screen():
                        self._draw_too_small_message()
                        self.stdscr.getch()
                        return "quit"
                    self._render(snapshot)
        finally:
            self.stdscr.nodelay(True)

    def _draw_too_small_message(self) -> None:
        self.stdscr.erase()
        msg = (
            "终端窗口太小，最少需要 {} 行 x {} 列。"
            "请调整终端大小后重试。".format(
                self._required_rows(), self._required_cols()
            )
        )
        self._safe_addstr(0, 0, msg)
        self._safe_addstr(2, 0, "按任意键退出。")
        self.stdscr.refresh()

    def _update_layout(self) -> None:
        self.board_left = max(
            self.WINDOW_MARGIN, (curses.COLS - self.board_width) // 2
        )
        self.board_top = self.HEADER_LINES + self.WINDOW_MARGIN

    def _fits_screen(self) -> bool:
        return curses.LINES >= self._required_rows() and curses.COLS >= self._required_cols()

    def _required_rows(self) -> int:
        return self.board_top + self.board_height + self.FOOTER_LINES + self.WINDOW_MARGIN

    def _required_cols(self) -> int:
        return max(self.board_width + self.WINDOW_MARGIN * 2, len(DIRECTION_HINT) + 10)

    def _safe_addstr(self, y: int, x: int, text: str, attr: int = 0) -> None:
        if y < 0 or y >= curses.LINES:
            return
        available = curses.COLS - x
        if available <= 0:
            return
        self.stdscr.addnstr(y, x, text, available, attr)
