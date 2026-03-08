"""贪吃蛇游戏入口脚本。"""
import curses
from .ui import TerminalUI


def main() -> None:
    curses.wrapper(lambda stdscr: TerminalUI(stdscr).run())


if __name__ == "__main__":
    main()
