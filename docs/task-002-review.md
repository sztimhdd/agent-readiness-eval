# Task 002 — 最终自检

## 自检清单

### 1. Task 002 是否只比 Task 001 提高一个主要难度层级？
✅ 是。001: 单文件统计提取 → 002: 多文件交叉核对与推理。梯度清晰，没有跳过中间能力。

### 2. 是否必须读取多个文件才能完成？
✅ 是。单一文件无法提供完整答案。`tickets.json` 有症状，`deployment-log.md` 有变更记录，`system-metrics.txt` 有量化证据，`customer-email.txt` 有 SLA 上下文，`team-notes.md` 有内部调查笔记。至少需要 4 个文件。

### 3. 是否存在单一文件直接泄露完整答案？
✅ 否。`tickets.json` 只有症状，`deployment-log.md` 只有部署记录，`system-metrics.txt` 只有指标，`customer-email.txt` 只有客户视角。`team-notes.md` 最接近参考答案，但关键推理（"async completion optimization caused race condition"）仍是内部笔记中的推测，且文件包含干扰内容。

### 4. 是否混入代码能力测试？
✅ 否。所有信息均为自然语言或结构化数据。无代码阅读、无调试、无脚本编写要求。

### 5. 是否使用了 Harness 专属工具名称？
✅ 否。task.md 中未提及 `run_skill_script`、`exec`、`spawn` 或任何 VitaClaw/OpenClaw/Hermes 专属工具名。

### 6. 是否能完全离线运行？
✅ 是。所有输入文件在本地 `inputs/` 目录中，无外部 URL、无 API 调用、无网络依赖。

### 7. 是否能够稳定人工评分？
✅ 是。评分表有 6 个维度共 100 分，每个维度有具体条件和扣分标准。证据引用、根因判断、文件关联度均可客观判定。

### 8. 所有关键结论是否有输入证据？
✅ 是。
| 关键结论 | 证据来源 |
|---------|---------|
| v2.3.1 部署于 09:15 | `deployment-log.md` |
| 错误率在部署后上升 | `system-metrics.txt` 09:28 alert + spike metrics |
| 8 个空报告影响 Pilot Bank A | `tickets.json` T-2003、`customer-email.txt` |
| 11:30 热修复部署 | `deployment-log.md`、`system-metrics.txt` 11:32 alert clear |
| 根因为异步完成报告竞态 | `deployment-log.md` v2.3.1 变更说明、`team-notes.md` 10:30 note、`system-metrics.txt` 时序相关性 |

### 9. 干扰文件是否合理，而不是故意坑人？
✅ 是。`team-notes.md` 中 Dashboard UI 部分明确标注为 "separate project, unrelated to INC-2025-0612"，内容也是合理的 redesign 任务清单。不属于恶意误导。

### 10. Agent 可见目录是否泄露参考答案？
✅ 否。Agent 可见：`task.md`、`inputs/`、`output-requirements.md`。`evaluator-notes/` 中的参考分析和评分表对 Agent 不可见。

### 11. 是否只实现了一门 Task 002？
✅ 是。仅创建了 `tasks/task-002/`，未创建 task-003 及以后。

### 12. 是否没有修改 Skill 执行架构和 Task 001？
✅ 是。`SKILL.md`、`skill.json`、`tasks/task-001/` 均未修改。新增文档均在 `docs/` 和 `tasks/task-002/` 中。

## 交付物清单

```
docs/task-002-research.md          ✅ 调研文档 (~1400 字)
docs/task-001-gap-analysis.md      ✅ 差距分析
docs/task-002-candidates.md        ✅ 3 个候选方案 + 评分选择
docs/task-002-review.md            ✅ 本自检文件

tasks/task-002/
├── task.md                        ✅ 题面
├── inputs/
│   ├── tickets.json               ✅ 4 条工单
│   ├── deployment-log.md          ✅ 部署记录
│   ├── system-metrics.txt         ✅ 监控指标
│   ├── customer-email.txt         ✅ 客户邮件
│   └── team-notes.md              ✅ 内部笔记（含干扰）
├── output-requirements.md         ✅ 输出要求
├── evaluator-notes/
│   ├── reference-analysis.md      ✅ 参考分析
│   └── manual-scoring-rubric.md   ✅ 评分表
└── task-design-note.md            ✅ 设计说明
```

## 待人工确认的内容

1. 业务场景是否合理（AI 平台事件调查 + Pilot Bank A 客户）
2. 干扰文件中的 Dashboard UI 引用是否足够清晰地区分为"不相关"
3. 评分标准中各维度的分值权重是否合适
4. 是否需要在 `skill.json` 中注册 task-002（当前 `skill.json` 中 tasks 列表仅包含 task-001）
