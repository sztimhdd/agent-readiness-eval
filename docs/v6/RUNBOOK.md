# V6.0.0 管理员运行手册

本手册供管理员使用。每题运行上限为 1800 秒。请在隔离的一次性 workspace 中运行任务。

## 运行前

1. 校验下载包的 `SHA256SUMS`。
2. 为每次运行复制一份干净的对应 `workspace/`。不要让不同受测者共用可写目录。
3. 按任务 `RUN.md` 准备环境和依赖。先完成准备，再启动计时。
4. 只把对应任务的 `TASK.md`、`EXECUTION.md` 和 `workspace/` 交给受测 agent。
5. 不要提供本手册、`SCORING.md`、历史成绩、其他答案或上游 solution。

本包不含 runner 或 grader。由各 harness 使用原生方式执行。管理员负责隔离、计时、保存交付物和记录环境信息。

## 各题准备与公开检查

### Pipeline

使用 Python 3.12。依赖版本固定为 `pydantic-core==2.41.5`、`annotated-types==0.8.0`、`typing-extensions==4.16.0`。这些版本对应本版任务环境。

公开 pytest 检查必须使用真实依赖库。不要用 mock 或 no-op stub 替代库行为。公开测试结果只能说明公开测试的覆盖范围，不能代替独立源判器。

### Ansible

建议使用 Python 3.12，并按原仓库的 `requirements.txt` 或相关 requirements 文件安装依赖。

可运行以下命令检查目标文件语法：

```sh
python -m compileall -q lib/ansible/modules/mount_facts.py
```

语法检查不代表业务通过。原 48 项用例需要独立源判器。teacher 基线 `HEAD 9ab63986` 与任务 base `40ade1` 是不同标识，不要将二者描述为同一提交。

### Inventory408

在任务 workspace 中运行公开测试：

```sh
python3 -m unittest discover -s tests
```

### Purchase409

本题交付物为 CSV。管理员可以手工检查文件和 CSV 格式。格式有效不代表采购选择正确。

### Finance

输入文件位于 `workspace/inputs/`，输出目录为 `workspace/output/`。可用 `openpyxl` 检查工作簿公式和缓存值。该检查不代表财务业务结果正确。

本版财务题冻结为本次已有成绩所用的原交付合同。三项增强交付检查仅供未来改版讨论，不属于 V6.0.0 默认要求。

## 隔离判分材料

隐藏 F2P 和原 verifier 不在受测 agent 下载包内。管理员如需使用，必须按固定来源链接，在受测隔离环境之外单独准备。不得把这些材料放入提供给受测 agent 的目录。

本发布包不保证复现历史分数。公开测试、语法检查、CSV 格式检查、公式检查和缓存值检查都不能单独证明业务正确。

## 运行记录

管理员应为每次运行记录任务名、harness、模型、依赖版本、开始与结束时间、时限结果，以及实际保留的交付物位置。只记录 harness 能直接观察的值。无法观察的值标为 `UNAVAILABLE`，不要估算。
