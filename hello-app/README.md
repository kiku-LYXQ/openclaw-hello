# 终端贪吃蛇

这是一个面向“小白”的 Python 终端游戏；逻辑与界面分离、地图默认 20×20，使用 `curses` 渲染，适用于类 Unix 终端或安装了 `windows-curses` 的 Windows 终端运行。所有游戏源码、配置、文档与高分记录都在本仓库根目录中。

## 快速开始
1. 安装 Python 3.9+，并可选激活虚拟环境：
   ```bash
   python --version
   python -m venv .venv
   source .venv/bin/activate     # Linux/macOS
   .venv\Scripts\Activate.ps1   # Windows PowerShell
   .venv\Scripts\activate.bat   # Windows CMD
   ```
2. 安装依赖（主要是 curses）
   ```bash
   pip install windows-curses   # Windows
   ```
   Linux/macOS 自带，无需额外操作。
3. 使用 Makefile 运行/测试/扫描（在仓库根）
   ```bash
   make run   # 启动游戏，等价于 python -m snake_game
   make test  # 运行 snake_game/tests/test_logic.py
   make lint  # py_compile 检查 snake_game/*.py snake_game/tests/*.py
   ```
   这些命令默认在根目录运行，不需要额外 cd。若想直接跑 Python 命令，也可按下一节所述。

## 运行游戏
- 直接执行：
  ```bash
  python -m snake_game
  ```
- 或者启动入口脚本：
  ```bash
  python snake_game/main.py
  ```
- 终端需要支持 curses；非交互式环境（CI、后台）会抛出 `curses.cbreak()/nocbreak() returned ERR`，这是因为 curses 找不到 TTY，真实终端运行即可忽略。
- 终端窗口建议至少 80×24 行，程序会在过小时提示并退出。
- 高分记录在 `highscore.txt` 中自动创建，游戏结束时会更新；若要重置可删除该文件。

## 控制说明
| 操作 | 说明 |
| --- | --- |
| 方向键 / WASD | 控制蛇移动 |
| `P` / `p` | 暂停/继续 |
| `H` / `h` | 显示帮助叠层（按任意键关闭） |
| `R` | 游戏结束后重玩 |
| `Q` / `Esc` | 退出 |
| `Ctrl+C` | 强制终止 |

顶部/底部实时显示当前得分与历史最高分，帮助叠层也会列出高分与快捷键。暂停/帮助期间仍可捕捉窗口 resize 与退出按键。

## 自定义地图与速度
- 可通过环境变量修改参数：
  ```bash
  SNAKE_GRID_WIDTH=24 SNAKE_GRID_HEIGHT=16 SNAKE_TICK_INTERVAL=0.12 python -m snake_game
  ```
- `config.py` 会读取变量、确保宽高 >=5、帧率为正，并在减小地图时动态推导初始蛇身长度，始终保持 < 宽高。

## Makefile 说明
- `Makefile`（在仓库根）提供：
  - `make run` → `python -m snake_game`
  - `make test` → `python -m unittest snake_game.tests.test_logic`
  - `make lint` → `python -m py_compile snake_game/*.py snake_game/tests/*.py`
- 这些命令仅在当前目录有效，请不要在其他子目录运行 `make`，否则会提示 “No rule to make target ...”。

## 测试与验证
- `make test`/`python -m unittest snake_game.tests.test_logic` 确认逻辑核心行为；CI 可复用该命令。
- `make lint` 通过 `py_compile` 检查语法完整性。

## 常见问题
- `ModuleNotFoundError: No module named 'curses'`：Windows 需要 `pip install windows-curses`。
- `curses.cbreak()/nocbreak()` ERR：非 TTY 环境预期出现，真实终端即可正常。
- 终端显示乱码：请使用 UTF-8 终端（推荐 Windows Terminal、PowerShell，避免老旧 cmd）。
- 高分没更新：确保 `highscore.txt` 可写，程序会在游戏结束后刷新。

## 目录结构
```
snake_game/           # 游戏源码（config/logic/ui/main + __main__）
snake_game/tests/     # 逻辑测试
highscore.txt        # 每轮记录历史最高分
DESIGN_SUMMARY.md     # 需求→架构→实现→验证流程记录
Makefile              # 方便的 run/test/lint 命令
README.md             # 当前说明
```

## 期待的体验
1. 安装依赖，运行 `make run` 或 `python -m snake_game`，在支持 curses 的终端里看到界面。 
2. 使用方向键/WASD 控制，按 `P` 暂停、`H` 打开帮助、吃到 `*` 增加得分、撞到边界/自身后提示 `Press R to restart`。 
3. `make test` 验证逻辑稳定，`make lint` 检查语法。 
4. 如遇问题，抓取终端错误并反馈给维护人员。
