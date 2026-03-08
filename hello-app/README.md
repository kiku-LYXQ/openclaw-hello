# 终端贪吃蛇

这是面向“小白”的 Python 终端游戏：逻辑/界面分离、地图默认 20×20、用 `curses` 渲染，适合在类 Unix 终端或安装过 `windows-curses` 的 Windows 终端运行。游戏会在启动过程中自动读取 `hello-app/highscore.txt` 并在头部/底部显示“历史最高分”；按 `P` 暂停/继续、`H` 打开帮助叠加提示，`High Score` 会在 UI 和帮助页中显示。

> ⚠️ 所有命令都应在 `hello-app` 目录下执行（或者在仓库根直接运行 `make run/test/lint`，Makefile 会自动进入该目录）。始终先 `ls`/`pwd` 确认当前目录再动手。

---
## 1. 环境准备
1. 检查 Python 版本（需 3.9 及以上）：
   ```bash
   python --version
   ```
2. 建议创建虚拟环境并激活（可隔离依赖）：
   ```bash
   python -m venv .venv
   ```
   - macOS / Linux：
     ```bash
     source .venv/bin/activate
     ```
   - Windows（PowerShell）：
     ```bash
     .venv\Scripts\Activate.ps1
     ```
   - Windows（命令提示符）：
     ```bash
     .venv\Scripts\activate.bat
     ```

---
## 2. 安装依赖
- macOS / Linux：`curses` 已内置，无需额外依赖。
- Windows：`curses` 不自带，安装兼容包：
  ```bash
  pip install windows-curses
  ```
  > 遇到 `ModuleNotFoundError: No module named 'curses'`，请确认在虚拟环境中运行并已安装 `windows-curses`。

---
## 3. 运行游戏
- 保持当前目录在 `hello-app` 内，运行：
  ```bash
  python -m snake_game
  ```
- 如果你在仓库根，推荐使用 Makefile：
  ```bash
  make run
  ```
  该命令会自动 `cd hello-app` 后再执行 `python -m snake_game`。
- 也可以直接运行启动脚本：
  ```bash
  python snake_game/main.py
  ```
- 每次启动请保持终端至少 80×24，以免窗口太小（程序会提示并让你按任意键退出）。
- 非交互式终端（如 CI / 后台 shell）会报 `curses.cbreak()/nocbreak() returned ERR`，这是因为 `curses` 找不到 TTY，可以放心忽略；在真实终端中不会出现。
- 高分会被写入 `hello-app/highscore.txt`，文件会自动创建，不需要手动写入；如果想复位可以删除该文件再启动。

---
## 4. 控制说明
| 操作 | 说明 |
| --- | --- |
| 方向键 / WASD | 控制蛇移动方向 |
| `P` / `p` | 切换暂停状态（暂停时不会自动移动，继续再按一次） |
| `H` / `h` | 显示帮助叠加面板，面板里提示按任意键返回 |
| `R` | 游戏结束后重玩 |
| `Q` / `Esc` | 立即退出 |
| `Ctrl+C` | 强制终止（仅在程序无响应时使用） |

屏幕顶部会同步显示 `High Score: X`；底部也会额外列出本轮得分与状态。帮助面板会列出所有快捷键与提示，退出叠加层后返回游戏画面。

---
## 5. 帮助与暂停提示
- 按 `H` / `h` 会弹出帮助 overlay，包括快捷键列表与当前 `High Score`，按任意键即可返回游戏。
- `P` / `p` 只在游戏进行中有效，暂停状态下提示 `已暂停，按 P 继续`，不会消耗帧；若游戏已结束请先按 `R` 重来。
- 退出时会检测当前得分并更新 `hello-app/highscore.txt`，当高分增加时文件会自动改写。

---
## 6. 可配置的环境变量
- `SNAKE_GRID_WIDTH`：地图宽度（默认 20）。
- `SNAKE_GRID_HEIGHT`：地图高度（默认 20）。
- `SNAKE_TICK_INTERVAL`：每帧间隔（秒 / 帧，默认 0.18）。

这些环境变量在游戏启动前读取，必须是正数；地图宽高最小 5，初始蛇身长度会自动推导为合法值。设置示例：
```bash
SNAKE_GRID_WIDTH=24 SNAKE_GRID_HEIGHT=16 SNAKE_TICK_INTERVAL=0.12 python -m snake_game
```
或 `make run` 之前再导出变量。

---
## 7. Makefile 与常用命令
- 项目根目录提供 `Makefile`，封装了常用流程，在仓库根执行：
  ```bash
  make run   # 启动游戏（相当于 cd hello-app && python -m snake_game）
  make test  # 运行逻辑单元测试
  make lint  # 检查 Python 语法（py_compile）
  ```
- `make test` 等价于：
  ```bash
  cd hello-app && python -m unittest snake_game.tests.test_logic
  ```
- `make lint` 通过 `py_compile` 编译主程序与测试，确保语法能通过解析。

---
## 8. 测试说明
在 `hello-app` 目录下运行：
```bash
python -m unittest snake_game.tests.test_logic
```
- `make test` 会在仓库根自动切换目录再执行相同命令。
- 测试覆盖初始化、吃食、碰撞等核心逻辑；跑不过时请确认你在相同虚拟环境且未修改逻辑层。

---
## 9. 常见问题与提示
- **运行时报 `ModuleNotFoundError: No module named 'curses'`**：需在虚拟环境中安装 `windows-curses` 或在类 Unix 终端使用内置 curses。
- **非交互式 shell 报 `curses.cbreak()/nocbreak() returned ERR`**：这是因为 curses 需要 TTY，真实终端运行即可；CI 或后台任务可以忽略该错误。
- **窗口提示太小 / 图形错位**：请把终端拉到至少 80×24，Linux 可用 `resize` 调整；若还是报错，重新启动并确认 `curses.COLS/COLS` 足够大。
- **高分未更新**：`hello-app/highscore.txt` 会在游戏结束时写入，确保启动者对该目录有写权限。
- **希望自定义地图/速度**：设置 `SNAKE_GRID_WIDTH`, `SNAKE_GRID_HEIGHT`, `SNAKE_TICK_INTERVAL` 再启动即可。

---
## 10. 目录结构速览
```
snake_game/          # 游戏源（config/logic/ui/main + __main__）
  config.py          # 网格/帧率常量与环境变量解析
  logic.py           # 纯逻辑状态机（SnakeGame）
  ui.py              # curses 交互、暂停、帮助、最高分
  main.py            # wrapper
  __main__.py        # 支持 python -m snake_game
snake_game/tests/    # 单元测试
  test_logic.py      # 核心行为用例
highscore.txt       # 运行时生成（记录历史最高分）
```

---
## 11. 期待的体验
1. 在 `hello-app` 目录（或仓库根 `make run`）中启动游戏，确认终端支持 curses，遇到 `curses.cbreak()/nocbreak()` 报错时在真实终端重试。
2. 使用方向键/WASD 控制蛇，按 `P` 暂停/继续，按 `H` 查看帮助并确认高分提示。
3. 吃到 `*` 会加分并刷新高分，游戏结束后按 `R` 重玩，`Q/Esc` 退出。
4. 若要验证逻辑，运行 `make test` 或 `python -m unittest snake_game.tests.test_logic`。

如果无法复现某些行为，请把具体终端错误截图发送给维护人员。