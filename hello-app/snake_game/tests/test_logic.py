"""逻辑层单元测试，覆盖 SnakeGame API 的关键场景。"""
import unittest

from snake_game.config import GRID_HEIGHT, GRID_WIDTH, INITIAL_SNAKE_LENGTH
from snake_game.logic import Direction, GameConfig, SnakeGame


class SnakeLogicTest(unittest.TestCase):
    def test_initial_snake_state_uses_default_grid(self):
        """默认配置应生成固定 20×20 网格和初始蛇身。"""
        game = SnakeGame(random_seed=0)
        snapshot = game.get_snapshot()
        self.assertEqual(snapshot.width, GRID_WIDTH)
        self.assertEqual(snapshot.height, GRID_HEIGHT)
        self.assertEqual(len(snapshot.snake), INITIAL_SNAKE_LENGTH)
        self.assertEqual(snapshot.score, 0)
        self.assertEqual(snapshot.steps, 0)
        self.assertFalse(snapshot.game_over)

    def test_reset_reinitializes_state(self):
        game = SnakeGame(random_seed=1)
        game.step(Direction.DOWN)
        snapshot = game.reset()
        self.assertEqual(snapshot.steps, 0)
        self.assertEqual(snapshot.score, 0)
        self.assertFalse(snapshot.game_over)
        self.assertEqual(snapshot.direction, Direction.RIGHT)
        self.assertEqual(len(snapshot.snake), INITIAL_SNAKE_LENGTH)

    def test_step_updates_direction_and_steps(self):
        game = SnakeGame(random_seed=2)
        snapshot = game.step(Direction.DOWN)
        self.assertEqual(snapshot.direction, Direction.DOWN)
        self.assertEqual(snapshot.steps, 1)
        self.assertFalse(snapshot.game_over)

    def test_reverse_direction_ignored(self):
        game = SnakeGame(random_seed=3)
        snapshot = game.step(Direction.LEFT)
        self.assertEqual(snapshot.direction, Direction.RIGHT)
        self.assertEqual(snapshot.steps, 1)

    def test_food_consumption_grows_snake(self):
        game = SnakeGame(random_seed=4)
        head = game.get_snapshot().snake[0]
        game.food = (head[0] + 1, head[1])
        snapshot = game.step(Direction.RIGHT)
        self.assertEqual(snapshot.score, 1)
        self.assertGreater(len(snapshot.snake), INITIAL_SNAKE_LENGTH)
        self.assertFalse(snapshot.game_over)
        self.assertNotIn(snapshot.food, snapshot.snake)
        x, y = snapshot.food
        self.assertTrue(0 <= x < GRID_WIDTH)
        self.assertTrue(0 <= y < GRID_HEIGHT)

    def test_collision_marks_game_over(self):
        config = GameConfig(width=6, height=6, initial_length=3)
        game = SnakeGame(config, random_seed=5)
        snapshot = None
        for _ in range(config.width):
            snapshot = game.step(Direction.RIGHT)
            if snapshot.game_over:
                break
        self.assertIsNotNone(snapshot)
        self.assertTrue(snapshot.game_over)


if __name__ == "__main__":
    unittest.main()
