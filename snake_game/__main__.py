"""Entrypoint shim that delegates to hello-app/snake_game.main."""
from __future__ import annotations


def main() -> None:
    from snake_game import main as snake_main  # type: ignore[import]

    snake_main.main()


if __name__ == "__main__":
    main()
