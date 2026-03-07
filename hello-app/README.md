# 终端贪吃蛇

一个为“小白”准备的 Python 终端游戏示例：逻辑与界面分离、地图固定为 20×20，使用 `curses` 渲染，保持依赖简单，适合在类 Unix 终端或装了 `windows-curses` 的 Windows 终端运行。

> ⚠️ **所有命令必须在 `hello-app` 目录下执行**，始终从这个目录开始操作（先 `ls` 或 `pwd` 确认位置）。

---
## 1. 环境准备（一步步来）
1. 检查 Python 版本（需 3.9 及以上）：
   ```bash
   python --version
   ```
   如果版本过低，请先安装最新 Python。
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
  > 如果遇到 `ModuleNotFoundError: No module named 'curses'`，请确认在虚拟环境中运行，并已安装 `windows-curses`。

---
## 3. 运行游戏
确保仍在 `hello-app` 目录内，再运行：
```bash
python -m snake_game
```
或者直接使用启动脚本：
```bash
python snake_game/main.py
```
- 每次启动请保持终端最大化或让窗口至少 80×24 行列以避免界面布局错乱。
- 若提示 `terminal too small`，请扩大终端然后重新运行。

---
## 4. 控制说明
| 操作 | 说明 |
| --- | --- |
| 方向键 / WASD | 控制蛇移动方向 |
| `R` | 游戏结束后重玩（即“再次开始”） |
| `Q` 或 `Esc` | 立即退出游戏 |
| `Ctrl+C` | 强制终止（仅在程序无响应时使用） |

吃到地图中的 `*` 会增长并得分；触碰边界或身体自己时游戏结束并自动暂停，屏幕上会提示按 `R` 重玩。

---
## 5. 常见问题小贴士
- **我按 `python -m snake_game` 它报错：`ModuleNotFoundError`**
  - 确认当前目录是 `hello-app`。
  - 激活虚拟环境后再执行 `python -m pip install windows-curses`。
- **游戏界面黑屏或乱码**
  - 只支持 UTF-8 终端，Windows 可使用 PowerShell 或 Windows Terminal，避免老旧 cmd。
- **终端提示窗口太小**
  - 把终端拉大或切换到全屏；Linux 可用 `resize` 指令。
- **键位无响应**
  - 先确保终端窗口在前台，尝试左右方向键或 WASD 组合，`curses` 读取按键需要焦点。

---
## 6. 测试说明（可选，但推荐）
在 `hello-app` 目录下运行：
```bash
python -m unittest snake_game.tests.test_logic
```
- 这个测试检查游戏逻辑的基本行为（初始化、吃食、碰撞）；通过即代表核心模块可用。
- 如果跑不过，请先确认在同一个虚拟环境中且没有修改逻辑层（架构目前不允许更动）。

---
## 7. 目录结构速览
```
snake_game/          # 游戏源代码
  config.py          # 地图与常量配置
  logic.py           # 纯逻辑状态机
  ui.py              # curses 控制与渲染
  main.py            # 启动脚本入口
  __main__.py        # 支持 python -m snake_game
snake_game/tests/    # 轻量逻辑单元测试
  test_logic.py      # 核心逻辑用例
```

---
## 8. 期待的体验
跟着 README 操作，确保：
1. 在 `hello-app` 目录下安装依赖并运行 `python -m snake_game`。
2. 使用方向键 / WASD 控制蛇，能正常吃到 `*`。
3. 撞到边界或自身后屏幕提示 `按 R 重玩`。
4. 可按 `Q` 或 `Esc` 退出游戏。

如遇无法复现的问题，请截图终端错误信息并反馈给维护人员。