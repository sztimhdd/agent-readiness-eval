# Pipeline｜管理员准备与检查

原题与已测公开初态，Python3.12。原目标tests/test_pipeline.py不在公开包内。

源码中的/testbed映射到本题workspace。改动限本仓库，交付Python源码。

将TASK.md、EXECUTION.md与workspace交给受测agent。RUN.md及顶层管理文档留在隔离外。每题1800秒。

管理员在任务执行前建立本题独立venv：

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cd workspace
PYTHONPATH=. ../.venv/bin/python -m pytest tests/test_type_adapter.py tests/test_json_schema.py -q -o addopts=""
```

初态故意挖空，运行前测试失败是预期，不是完整安装通过证明。受测修复后使用同一命令。真实库缺失需准备阶段解决，不得以恒真/空桩替代。隐藏F2P未包含；公开测试不能保证原64/47判分复现。
