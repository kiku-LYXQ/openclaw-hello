"""Shim that exposes the packed snake_game implementation under hello-app."""
from __future__ import annotations

from pathlib import Path

__all__: list[str] = []

_this_dir = Path(__file__).resolve().parent
_snake_impl = _this_dir.parent / "snake_game"
_snake_impl_path = str(_snake_impl.resolve())
if _snake_impl_path not in __path__:
    __path__.append(_snake_impl_path)
