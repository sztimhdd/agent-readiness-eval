# Task 002 调研：主流 Agent Benchmark 题型分析

## 调研范围

GAIA、Terminal-Bench、SWE-bench、τ-bench / ToolSandbox。

目标：从每个 benchmark 提取一条最值得借鉴的设计思路，并识别其不适合本项目的部分，为 Task 002 命题提供直接启发。

---

## GAIA

**论文**: GAIA: a General AI Assistant Benchmark (Mialon et al., 2023)

### 最值得借鉴的一点

**无需评分模型的确切匹配打分**。GAIA 证明可以设计多步推理 + 信息检索的复杂任务，但最终答案用简单字符串正规化即可自动评分。不需要 LLM-as-judge，不需要复杂 rubric，不依赖评分模型。对跨 Harness 场景，这意味着每个 Harness 只需产出标准格式答案，评分可比性天然存在。

### 借鉴方式

Task 002 的输出 JSON 字段应设计得足够结构化，使人工评分能够快速判断字段值是否正确（类似 GAIA 的 `FINAL ANSWER: [...]` 模式），而不是让 reviewer 阅读长篇自由文本再主观打分。

### 不适合本项目的部分

GAIA 大量依赖实时网络访问（Wikipedia、arXiv、ScienceDirect）。URL 会过期，内容会变化，部分站点会屏蔽 bot。纯文件包无法复现这种"去真实世界找信息"的设计。另外 GAIA Level 2/3 任务需要多步工具链和代码执行，超出了本 question-pack 的范围。

---

## Terminal-Bench

**论文**: Terminal-Bench: A Benchmark for Evaluating AI Agents on Terminal-Based Tasks (Mao et al., 2025)

### 最值得借鉴的一点

**基于状态的验证**，而非过程跟踪。Terminal-Bench 的测试只检查最终容器状态（文件是否存在、数据库记录是否正确），不检查 agent 执行了哪些命令、按什么顺序执行。不同 agent 可以用完全不同的路径达成同一结果。这种"只看结果不问过程"的评估哲学非常适合跨 Harness benchmark。

### 借鉴方式

Task 002 的评分应聚焦于最终产出内容（JSON 字段值、Markdown 中的关键断言），不关心 agent 先读了哪个文件、读了几次。只要最终答案正确且证据链完整，就是满分。

### 不适合本项目的部分

Terminal-Bench 的整个评估模型依赖 Docker 容器执行——agent 需要交互式 shell、可变的文件系统、隔离的运行环境。纯文件 question-pack 无法提供这些。我们只能评估答案质量，不能评估 agent 在真实终端中的操作能力。

---

## SWE-bench

**论文**: SWE-bench: Can Language Models Resolve Real-World GitHub Issues? (Jimenez et al., 2024)

### 最值得借鉴的一点

**执行门控任务验证**（execution-gated task validation）。SWE-bench 在收录每道题之前，先应用 gold patch 并验证 FAIL_TO_PASS 测试确实翻转。这筛掉了约 68% 的候选题目（SWE-bench Verified 数据），原因是题面描述模糊或测试过于严格。这个原则完全可以泛化到非代码任务：**每道题上线前，应该让一个"理想 agent"完整走一遍，确认题目是唯一可解的、评分不会产生歧义**。

### 借鉴方式

Task 002 设计完成后，由人类 reviewer（或我自己）以"已知正确答案"身份走一遍完整流程，确认：
- 所有关键结论都能从提供的文件中推导出来
- 不存在两种同等合理的解释导致不同的"正确答案"
- 干扰文件是真的干扰（不是故意误导）
- 评分表能覆盖所有合理答题路径

### 不适合本项目的部分

SWE-bench 的核心挑战是大代码库定位（438K 行代码中找到 1-3 个需要改的文件），这本质上是一个检索问题。纯文件 question-pack 无法复制这种规模。如果不涉及编码，SWE-bench 的评估范式（生成 patch → Docker 中跑测试）完全不适用。

---

## τ-bench / ToolSandbox

**论文**: τ-bench: A Benchmark for Tool-Agent-User Interaction (Yao et al., 2024) / ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool-Use Capabilities (Lu et al., 2024)

### 最值得借鉴的一点

**Milestone DAG 评估**。ToolSandbox 不要求 agent 按固定顺序执行步骤，而是定义一组关键里程碑（milestones），它们之间的依赖关系构成有向无环图（DAG）。agent 可以走不同的路径，只要最终触发了所有必要里程碑且未触发"雷区"（minefields）就算成功。这与 Terminal-Bench 的"只看结果"理念一致，但增加了对推理链质量的约束。

### 借鉴方式

Task 002 的评分可以不要求 agent 按特定顺序发现信息，但应检查最终答案中是否包含了所有关键事实、是否排除了干扰、是否正确处理了信息冲突。评分表的分值分配应反映这种"里程碑完整性"的评估思路。

### 不适合本项目的部分

τ-bench 依赖 LLM 模拟用户与 agent 对话（动态信息提供），ToolSandbox 依赖可变世界状态（工具 A 的结果影响工具 B 的可用性）。这些都要求交互式运行时环境。纯文件 question-pack 是静态的——agent 读取文件然后提交答卷，没有中间对话和状态变化。

---

## 对 Task 002 的直接启发

| 来源 | 启发 | Task 002 中的应用 |
|------|------|------------------|
| GAIA | 确切匹配打分 | JSON 字段值设计成可直接比对，减少主观判断 |
| Terminal-Bench | 只看结果不问过程 | 评分只检查最终答案，不关心文件读取顺序 |
| SWE-bench | 执行门控验证 | 设计完成后由 reviewer 走通一遍验证可解性 |
| ToolSandbox | Milestone DAG | 多文件信息整合允许多种路径，评分聚焦里程碑完整性 |

**核心命题思路**: 设计一个任务，其中 agent 必须主动发现并读取多个文件、跨文件核对信息、识别冲突和干扰、做出有证据支持的判断。评分聚焦于最终产物的信息完整性和推理正确性，不关心 agent 按什么顺序读了哪些文件。题目本身是静态的（无外部 API、无代码执行、无对话模拟），但 agent 需要的信息分布在多个文件中，必须主动探索才能完整获取——这正是从 Task 001 的"单一输入处理"到 Task 002 的"多源信息整合"的关键跃迁。
