"""Entrypoint shim that routes to the snake_game launcher."""
from __future__ import annotations


def main() -> None:
    from snake_game import main as snake_main  # type: ignore[import]

    snake_main.main()


if __name__ == "__main__":
    main()
