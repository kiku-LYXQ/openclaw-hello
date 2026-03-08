# Hello App Repository

本仓库的实际应用都放在 `hello-app/` 目录内：所有游戏逻辑、界面、测试和高分记录都在这个子项目里。

---
## 快速入口
1. 先安装好 Python 3.9+（可选虚拟环境），并在 Windows 上安装 `windows-curses`。
2. 运行（或测试/静态扫描）常用命令（请始终在仓库根执行 `make` 命令，内部会自动 `cd hello-app`）：
   ```bash
   make run   # 启动终端蛇游戏（内部会 cd hello-app）
   make test  # 运行 hello-app 下的单元测试
   make lint  # 用 py_compile 快速检查语法
   ```
   `make` 命令引用的 target 等价于：
   - `make run` -> `cd hello-app && python -m snake_game`
   - `make test` -> `cd hello-app && python -m unittest snake_game.tests.test_logic`
   - `make lint` -> `cd hello-app && python -m py_compile snake_game/*.py snake_game/tests/*.py`
> ⚠️ 这些 `make` 命令必须在仓库根运行（它们会负责进入 `hello-app`）；如果你在 `hello-app` 目录里直接执行 `make` 会收到 "No rule to make target ..." 之类错误。
3. 想要了解更详尽的依赖、控制、测试与高分机制，请阅读 `hello-app/README.md`（本文件仅补充关键亮点）。

---
## 关键运行要点
- **curses 依赖**：Linux/macOS 自带；Windows 需 `pip install windows-curses`。
- **非 TTY 会报错**：在 CI 或后台执行时常会看到 `curses.cbreak()/nocbreak() returned ERR`，属于预期（curses 无法绑定 TTY），可忽略，真实终端运行才有完全体验。
- **可调地图/帧率**：设置环境变量 `SNAKE_GRID_WIDTH`、`SNAKE_GRID_HEIGHT`（最小 5）、`SNAKE_TICK_INTERVAL`（秒/帧）就能改变地图尺寸与速度，`config.py` 会自动校验合法性。
- **高分记录**：游戏会读写 `hello-app/highscore.txt`，启动时会显示 `High Score: X`，游戏结束后自动更新文件。
- **新快捷键**：`P/p` 暂停或继续、`H/h` 打开帮助叠加（列出所有键位与提示），帮助面板按任意键即可关闭；`High Score` 会在头部/底部实时同步。
- **Makefile 便捷**：只需 `make run/test/lint` 就能按推荐流程执行，所有命令都会自动切换到 `hello-app`，保持一致的工作目录。

---
## 路径提醒
- 代码和文档：`hello-app/`。
- 高分：`hello-app/highscore.txt`。
- 入口：`hello-app/snakes_game` 中的 shim 会把包暴露给 `python -m snake_game`。

## 其他文档
更多说明（依赖、命令、操作、常见问题、测试）请查看：
- `hello-app/README.md`（一步步指导）
- `DESIGN_SUMMARY.md`（架构/协作记录）

如果你是第一次打开本仓库，请从 `make run` 开始，或按照 `hello-app/README.md` 提示逐步操作。