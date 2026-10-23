# 库存408｜管理员准备与检查

Python标准库业务。原可见unittest保留。

题面/app与/root映射到workspace，按FEATURE.md实现，交付修改后的完整源码。

将TASK.md、EXECUTION.md与workspace交给受测agent。RUN.md及顶层管理文档留在隔离外。每题1800秒。

```sh
cd workspace
python3 -m unittest discover -s tests
```

Python3.12或兼容版本，业务只需标准库。保留原公开测试，不修改它们来求通过。公开回归不等于完整新增功能验收，新增功能按FEATURE.md检查。
