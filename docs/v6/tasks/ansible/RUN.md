# Ansible mount_facts｜管理员准备与检查

公开app来自已测pristine teacher。taskBase40ade1与实际appHead9ab63986分别保留，未宣称原上游Git树等同。

题面/app映射到workspace。新增模块lib/ansible/modules/mount_facts.py，保留公开文件。

将TASK.md、EXECUTION.md与workspace交给受测agent。RUN.md及顶层管理文档留在隔离外。每题1800秒。

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cd workspace
PYTHONPATH=lib ../.venv/bin/python -c "import ansible; print(ansible.__file__)"
```

题目完成后可检查语法：

```sh
../.venv/bin/python -m py_compile lib/ansible/modules/mount_facts.py
```

这不等于原48用例通过。原判器需管理员从固定来源在受测隔离外独立准备。公开仓库文件对应已测pristine appHead9ab63986，任务标识base40ade1，不宣称locked官方协议复现。
