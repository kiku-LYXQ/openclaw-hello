"""逻辑层单元测试。"""
import unittest

from snake_game.logic import Direction, GameConfig, SnakeGame


class SnakeLogicTest(unittest.TestCase):
    def test_initial_snake_state(self):
        config = GameConfig(width=12, height=12, initial_length=3)
        game = SnakeGame(config)
        snapshot = game.get_snapshot()
        self.assertEqual(len(snapshot.snake), config.initial_length)
        self.assertEqual(snapshot.score, 0)
        self.assertFalse(snapshot.game_over)

    def test_food_consumption_grows_snake(self):
        config = GameConfig(width=16, height=10, initial_length=3)
        game = SnakeGame(config)
        head = game.get_snapshot().snake[0]
        food_pos = (head[0] + 1, head[1])
        game.food = food_pos
        snapshot = game.step(Direction.RIGHT)
        self.assertEqual(snapshot.score, 1)
        self.assertGreater(len(snapshot.snake), config.initial_length)
        self.assertFalse(snapshot.game_over)

    def test_collision_marks_game_over(self):
        config = GameConfig(width=6, height=6, initial_length=3)
        game = SnakeGame(config)
        snapshot = None
        for _ in range(config.width):
            snapshot = game.step(Direction.LEFT)
            if snapshot.game_over:
                break
        self.assertIsNotNone(snapshot)
        self.assertTrue(snapshot.game_over)


if __name__ == "__main__":
    unittest.main()
