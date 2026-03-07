# 终端贪吃蛇

一个纯终端运行、地图固定的贪吃蛇游戏示例。逻辑层独立于界面，方便扩展并支持简单的自动化测试；终端界面使用 `curses` 呈现，适用于类 Unix 终端。地图默认固定为 20×20，额外功能只保留必要交互，目标是让“小白”也能读懂 README 并运行。

---
## 快速上手
1. 确保使用 Python 3.9 及以上：
   ```bash
   python --version
   ```
2. （可选）创建虚拟环境并激活：
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate     # Windows（PowerShell 用 `./.venv/Scripts/Activate.ps1`）
   ```
3. 安装依赖：
   - macOS / Linux：无需额外库，`curses` 已内置。
   - Windows：安装 `windows-curses` 提供兼容层：
     ```bash
     pip install windows-curses
     ```
4. 运行游戏：
   ```bash
   python -m snake_game
   ```
   或直接：
   ```bash
   python snake_game/main.py
   ```
5. 控制说明：
   - 方向键 / WASD 控制蛇移动。
   - 吃到 `*` 会增长并获得一分。
   - 遇到边界或自身后游戏结束，自动暂停并提示按 `R` 重玩。
   - 游戏中按 `Q` 或 `Esc` 立即退出。

---
## 地图与配置
- 默认地图大小 20×20（由 `snake_game/config.py` 中的 `GRID_WIDTH` 与 `GRID_HEIGHT` 决定）。
- 初始蛇身长度为 `INITIAL_SNAKE_LENGTH = 4`，可在配置文件中调整。
- 通过 `TICK_INTERVAL` 控制帧率（秒 / 帧），值越小节奏越快。
- 如需修改地图大小或初始方向，直接编辑 `snake_game/config.py`，无需改界面层代码。

---
## 目录结构
```
snake_game/          # 游戏源代码
  config.py          # 固定地图常量
  logic.py           # 纯逻辑（状态机 + 快照）
  ui.py              # curses 交互与渲染
  main.py            # 启动脚本
  __main__.py        # 支持 python -m snake_game
snake_game/tests/    # 轻量级单元测试
  test_logic.py      # 验证初始化、吃食与碰撞逻辑
```

---
## 开发与测试
- 运行逻辑测试：
  ```bash
  python -m unittest snake_game.tests.test_logic
  ```
- `SnakeGame` 可拆分给其他前端（Web、AI 代理）复用。
- 如果终端窗口太小，curses 会提示最小行/列，请调整后再运行。

---
继续迭代建议：
1. 增加设置文件或命令行参数控制速度、地图大小等。
2. 将界面替换为 `rich`、`blessed` 或 `textual`，提升视觉表现。
3. 实现自动回放脚本，用测试驱动序列验证行为。
