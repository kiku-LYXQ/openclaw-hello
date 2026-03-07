# 贪吃蛇项目开发总结

## 1. 需求回顾
- 用户要求：在提供的仓库中实现终端版固定 20×20 地图的贪吃蛇游戏，支持方向/WASD、吃食增长、碰撞退出、重玩，文档要面向“小白”。
- 额外限制：所有代码必须放在 `hello-app/`（后续想只同步该目录），1）runner 必须能在仓库根执行 `python -m snake_game`，2）文档须说明终端依赖，3） reviewer 给出“通过/不通过 + 建议”的反馈。

## 2. 架构与接口设计
- 采用三层架构：
  1. `snake_game.logic`：纯状态机（`SnakeGame`, `GameSnapshot`, `GameConfig`）负责位置、碰撞、食物、方向保护，返回快照供 UI 消费。
  2. `snake_game.ui`：基于 `curses` 渲染，按键/帧率/resize/边框/提示层分离，调用逻辑层的快照接口。
  3. 文档/启动：`snake_game/main.py` + `__main__.py` 作为入口，`hello-app/README.md` 指导运行流程。
- shim：root 移动到 `hello-app/snakes_game`，通过 `__path__` 修改使 `python -m snake_game` 能直接加载 `hello-app/snake_game`；`__main__` 调用主入口。
- 各模块接口：
  * `SnakeGame.step(direction)` 返回 `GameSnapshot`。
  * `TerminalUI.run()` 读取快照、渲染板块、处理输入，遇到游戏结束弹出提示。
  * README 中提供命令、依赖提示和测试步骤，强调非 TTY 下 `cbreak()/nocbreak()` ERR 属预期。

## 3. 开发过程摘要
1. 创建 `hello-app/snake_game` 逻辑/UI/tests，保证 `cd hello-app && python -m unittest snake_game.tests.test_logic` pass。
2. 编写 curses UI，增加边框、彩色渲染、`KEY_RESIZE` 处理、边界提示、重玩/退出，依赖 readonly of `SnakeGame`。
3. 写文档，说明 Windows 需 `windows-curses`、运行方法、操作说明、常见问题、测试命令并强调在 `hello-app` 目录执行。
4. 添加 reviewer 指令/记忆：确保 reviewer 多次拉新 master，使用真实终端运行 `python -m snake_game` 并提交正式结论。
5. 添加 shim：先在 root 目录添加 `snake_game` package，将 `hello-app/snake_game` 加入 `__path__` 并通过 `__main__` 调用 game 入口，后续重构将 shim 移至 `hello-app/snakes_game`。
6. reviewer 验证：在新 clone 的 `hello-app` 里运行命令，通过只在非 TTY 看到 curses 的 `cbreak()/nocbreak()` 错误。文档后续统一指出终端依赖。

## 4. 模块/接口清单
| 模块 | 说明 | 主要接口 |
| --- | --- | --- |
| `snake_game.logic` | 控制游戏状态、快照、方向保护 | `GameConfig`, `SnakeGame.step`, `SnakeGame.reset`, `GameSnapshot` |
| `snake_game.ui` | curses 渲染、输入、边框、提示 | `TerminalUI.run`, `TerminalUI._render`, `TerminalUI._handle_game_over` |
| `snake_game.main` | 入口 | `curses.wrapper` 调用 `TerminalUI` |
| `hello-app/snakes_game/__init__.py` | shim，将 `hello-app/snake_game` 加入 `__path__` | 额外 `__all__` 以同步逻辑导出 |
| `hello-app/snakes_game/__main__.py` | CLI | `snake_game.main.main()` 调用 |

## 5. Reviewer/验证记录
- reviewer 在全新 clone 的 `hello-app` 目录中运行 `python -m snake_game`，确认 shim 生效并能导入 `hello-app/snake_game/main.py`。
- 所有测试指令：`cd hello-app && python -m unittest snake_game.tests.test_logic`。
- reviewer 建议在 README 里明确指出：命令需在支持 curses 的真实终端运行，非 TTY 环境会报 `cbreak()/nocbreak()` ERR但属于预期。

## 6. 后续建议
- 若未来还需要扩展更多 UI/模式或增加自动回放，可在 `snake_game.logic` 中添加接口，UI 层无感知；只要保持 shim 的路径指向即可。
- 按照 review 模板继续提醒 reviewer：背景、动作、输出严格分三段，确保环境/命令一致。

*编写者：Architect（协调 coder1/2/3 与 reviewer），2026-03-08* 
