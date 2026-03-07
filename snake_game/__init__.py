"""Package shim that forwards imports to hello-app/snake_game."""
from __future__ import annotations

from pathlib import Path

__all__: list[str] = []

_this_dir = Path(__file__).resolve().parent
_hello_app_snake = _this_dir.parent / "hello-app" / "snake_game"
_hello_app_snake_path = str(_hello_app_snake.resolve())
if _hello_app_snake_path not in __path__:
    __path__.append(_hello_app_snake_path)
