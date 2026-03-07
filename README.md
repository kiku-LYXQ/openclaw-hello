# Hello App Repository

此仓库的实际项目内容位于 `hello-app/` 目录中。安装、运行、调试都请在该目录内进行；最新的兼容 shim 也在 `hello-app/snakes_game` 里面，所以 reviewer 只需同步 `hello-app` 即可完整访问 `snake_game` 模块。

```bash
cd hello-app
python -m snake_game
```

如果必须在仓库根直接执行（例如 CI 流水线），请手动把 `hello-app` 加入 `PYTHONPATH`：

```bash
PYTHONPATH=hello-app python -m snake_game
```
