# Agent Readiness Eval V6.0.0

本包提供五道固定任务，供 CTO 下载、查阅和按需运行。每题限时 1800 秒。

V6.0.0 是五题选集，不代表六槽能力全集，也不构成六槽正式榜单。各题采用原有任务内容和本版统一时限。不同任务的环境、交付物和可验证范围不同，结果不能直接解释为官方榜单成绩。

## 五题

| 任务 | 主要工作 | 交付边界 |
|---|---|---|
| Pipeline | 在公开的 Pydantic 仓库中完成代码任务 | workspace 是公开上游仓库的挖空初态，含公开测试和 `pydantic-core` 源码；它不是已提交答案 |
| Ansible | 完成 `mount_facts` 模块任务 | workspace 是 teacher 提供的 pristine 公开 app，含公开上游测试；不含 gold patch 或私有 verifier |
| Inventory408 | 处理库存任务 | 使用原公开初态文件 |
| Purchase409 | 处理采购任务 | 使用原公开初态文件；交付物为 CSV |
| Finance | 处理财务任务 | 13 个 CSV 位于 `workspace/inputs/`，并预建 `workspace/output/` |

## 下载与校验

从 [固定 Release](https://github.com/sztimhdd/agent-readiness-eval/releases/tag/v6.0.0) 下载 ZIP 与校验和，再解压 `agent-readiness-eval-v6.0.0/`。发布包包含：

```text
agent-readiness-eval-v6.0.0/
├── README.md
├── RUNBOOK.md
├── SCORING.md
├── manifest.json
├── SHA256SUMS
├── licenses/
└── tasks/
    ├── pipeline/{TASK.md,RUN.md,workspace/}
    ├── ansible/{TASK.md,RUN.md,workspace/}
    ├── inventory408/{TASK.md,RUN.md,workspace/}
    ├── purchase409/{TASK.md,RUN.md,workspace/}
    └── finance/{TASK.md,RUN.md,workspace/}
```

在解压目录执行以下命令，检查文件哈希：

```sh
sha256sum -c SHA256SUMS
```

macOS 若没有 `sha256sum`，可用系统 `shasum` 逐项核对 SHA-256。校验通过只表示文件与清单一致，不表示任务结果正确。

## 准备、执行与验收

1. 管理员先阅读 [RUNBOOK.md](RUNBOOK.md)，并在隔离的一次性环境中准备任务 workspace 和依赖。
2. 管理员只向受测 agent 提供对应任务的 `TASK.md`、`EXECUTION.md` 与 `workspace/`。
3. 受测 agent 按任务文件完成工作，并将结果留在指定 workspace 或任务要求的位置。
4. 管理员按 [SCORING.md](SCORING.md) 检查结果。公开测试或格式检查不能代替业务判定。

不要把本包的 `RUNBOOK.md`、`SCORING.md`、历史成绩、其他任务答案或上游 solution 提供给受测 agent。隐藏 F2P 和原 verifier 不在下载包中。管理员只能按固定来源链接，在受测隔离环境之外单独准备它们。公开包不能保证复现历史分数。

## 许可

各任务的许可材料位于 `licenses/`。请按对应材料查看任务和上游项目的许可信息。本 README 不作额外法律结论。
