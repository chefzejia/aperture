# Agent 文档工程指南

适用范围：Agent 参与项目文档的创建、改造和优化工作。本指南教方法；执行任务时绑定的工作标准在 `templates/standards.md`（复制进目标项目后生效）。

## 如何使用本指南

**Agent 改造或新建项目文档的标准流程**：

1. 读完本指南的"文档分级策略"和"模板使用"，知道目标项目该有哪些文档
2. 从 `templates/` 复制所需模板到目标项目（见"使用 templates"）
3. 用本指南的"文档写作原则"和"文档路由规则"填充内容
4. 按 `templates/standards.md` 复制通用工作标准到 `docs/STANDARDS.md`
5. 验证：目标项目的 agent 读完 `AGENTS.md` + `STANDARDS.md`，能开始第一个任务

**新建项目骨架**：

1. 从 `templates/agents.md` 创建 `AGENTS.md`，填写项目定位和特有约束
2. 从 `templates/readme.md` 创建 `README.md`，填写快速开始
3. 从 `templates/standards.md` 复制 `docs/STANDARDS.md`（通用工作标准，开箱即用）
4. 根据项目规模，选择性添加其他文档（见下方"文档分级策略"）
5. 运行 `git status` 确认没有多余的未跟踪文件

**判断标准**：Agent 读完目标项目的 `AGENTS.md` 和 `README.md`，能开始第一个任务；读完 `STANDARDS.md`，知道干活时受什么约束。

**遇到问题**：返回本指南的对应原则，不要打补丁。

---

## 本指南与标准的关系（真源与投影）

```text
本仓库（agentic-work-infra）
├── docs/governance/agent-governance.md   ← 本文件：教 Agent 如何做文档工程（读一次，用完即走）
├── docs/governance/templates/standards.md ← 通用工作标准的真源
└── 目标项目（复制后自治）
    ├── AGENTS.md        ← 从 templates/agents.md 复制并实例化
    ├── docs/STANDARDS.md ← 从 templates/standards.md 复制（复制后项目自治，经 LESSONS 演化，不回写真源）
    └── docs/LESSONS.md  ← 从 templates/lessons.md 复制（失败记录驱动标准演化）
```

关键规则：

- **标准随项目走**：agent 读完本指南去目标项目干活时，绑定的标准来自目标项目自己的 `STANDARDS.md`，不是本仓库
- **复制后自治**：目标项目通过自己的 LESSONS.md 演化标准（3 次晋升机制），不回写本仓库的真源
- **真源更新只影响未来**：本仓库更新 `templates/standards.md`，已复制的项目不自动同步——各项目按需自查

---

## 核心原则（文档工程层面）

**代码即事实，运行结果是最终判断标准。** 不接受 Agent 声称完成、日志看起来正常、文件存在等表象作为验收依据。任何工作结果必须能被人独立检查。

**共同可观测，不分裂成两套状态。** Agent 的代码、判断和整理结果必须对人直接可见。不接受 Agent 在不透明的索引、缓存或生成结果中维护一套人无法核对的状态。

**先从目标出发，不打补丁。** 遇到问题先找根本原因，再决定如何修改。连续两次对同一问题打局部补丁，说明根因没找到，需要重新分析。

---

## AGENTS.md 的职责

每个项目的 `AGENTS.md` 是 Agent 进入项目时的唯一入口，负责：

- **项目定位**：这是什么项目，不是什么
- **架构约束**：不可违反的边界，5条以内，每条一句话
- **修改和验证**：运行什么命令验证修改
- **文档路由**：任务需要的核心文件在哪里

`AGENTS.md` 不放：历史记录、benchmark 结果、详细架构说明、一次性任务记录、Handoff 内容。

**长度指导**：50行以内覆盖大部分项目；复杂项目上限100行。超过时先检查是否有内容该移到专门文档。

---

## 文档分级策略

### 必需文档（所有项目）

**AGENTS.md** - Agent 的唯一入口
- 项目定位（是什么、不是什么）
- 架构约束（不可违反，5条以内）
- 修改和验证（必须运行的命令）
- 文档路由（其他文档在哪里）
- 长度：50-100 行

**README.md** - 人类入口
- 一句话介绍
- 快速开始
- 常用命令
- 项目结构（如果复杂）

**docs/STANDARDS.md** - 通用工作标准
- 从 `templates/standards.md` 复制，开箱即用
- 内容：核心工作原则、工具选择梯度、工作方式、人机边界、开发约束、验证与验收清单、调试、架构选择
- 长度：约 200 行（复制后不动，靠 LESSONS 演化）

**判断标准**：Agent 读完这三个文件，能开始第一个任务。

### 推荐文档（按需要）

**docs/HANDOFF.md** - 当前状态和下一步
- 何时需要：多人协作、长期项目、有交接需求
- 内容：当前在哪里、下一步做什么、关键文件
- 更新频率：每周或每次重要变更

**docs/LESSONS.md** - 失败记录和规则演化
- 何时需要：开始用 Agent 后，有重复失败案例
- 内容：规则 + 证据 + 出现次数 + 做对示例
- 更新频率：每周 review 或发现重复失败时
- 晋升：出现 3 次 → 移到 AGENTS.md 或 STANDARDS.md

**DEPLOYMENT.md** - 部署流程（有部署动作的项目）
- 何时需要：产物需要部署到别处才生效（构建后复制、打包上架、推送服务器），或部署由 Agent/脚本执行
- 内容：部署目标、标准流程（构建→部署→启用）、验证清单、回滚、常见问题
- 模板：`templates/deployment.md`
- 判断：没有它，Agent 或人会部署错文件、部署后不验证、出问题不会回滚吗？是则加

**docs/operations/<名称>.md** - 一次性危险操作协议
- 何时需要：操作不可逆或影响大量文件（迁移、重命名、批量清理、目录重组、数据搬移），由 Agent 执行
- 内容：目标、前置检查、预览（无副作用）→ 人确认 → 执行、备份与恢复、明确不支持
- 模板：`templates/operation.md`
- 判断：操作失败或做错，能无损退回吗？不能则先写协议

### 可选文档（按复杂度）

**DESIGN.md** - 架构概览（中型项目）
- 何时需要：有多个子系统、有重要架构决策
- 内容：系统组成、职责边界、关键决策理由
- 替代方案：docs/architecture/overview.md

**docs/architecture/** - 架构详细（大型项目）
- 何时需要：有多个架构决策需要分别记录
- 内容：每个子系统一个文件（见 `templates/architecture.md`：源码锚点、失败行为、验证命令、状态文件清单）、ADR 记录（见 `templates/adr.md`）
- 替代：DESIGN.md（中型项目）

**docs/product/** - 产品决策
- 何时需要：有产品判断需要记录
- 内容：PRD、交互决策、商业模式

**docs/research/** - 调研和验收
- 何时需要：有调研任务、需要验收矩阵
- 内容：调研报告、benchmark、验收清单

### 规模参考

| 规模 | 代码量 | 必需 | 推荐 | 可选 |
|------|--------|------|------|------|
| 小型 | < 5K 行 | AGENTS.md<br>README.md<br>STANDARDS.md | HANDOFF.md* | - |
| 中型 | 5K-50K | 同上 | HANDOFF.md<br>LESSONS.md | DESIGN.md<br>或 architecture/<br>DEPLOYMENT.md |
| 大型 | > 50K | 同上 | 同上<br>architecture/ | product/<br>research/ |

*小型项目的 HANDOFF.md：如果是单人且持续工作，可以省略；如果有间隔或需要交接，建议加上。

### 使用 templates

**新建项目**：
1. 从 `templates/agents.md` 创建 `AGENTS.md`
2. 从 `templates/readme.md` 创建 `README.md`
3. 从 `templates/standards.md` 复制 `docs/STANDARDS.md`
4. 根据规模，选择性添加：
   - `templates/handoff.md` → `docs/HANDOFF.md`
   - `templates/lessons.md` → `docs/LESSONS.md`
   - `templates/design.md` → `DESIGN.md`
   - `templates/deployment.md` → `DEPLOYMENT.md`（有部署动作时）
   - `templates/operation.md` → `docs/operations/<名称>.md`（执行不可逆或大范围操作前）
   - `templates/adr.md` → `docs/architecture/ADR-001-xxx.md`
5. **不建空目录**，有内容再建

**改造现有项目**：诊断现有文档（缺什么、什么过时）→ 按分级策略补齐/精简 → STANDARDS.md 直接复制即可，不与现有内容合并。

**判断是否需要某文档**：
1. 没有它，Agent 或人会做错决策吗？
2. 它会持续更新吗？
3. 它的内容能合并到其他文档吗？

如果 1=是、2=是、3=否 → 需要独立文档
否则 → 不需要或可以合并

### 文档路由规则

每次修改 `AGENTS.md` 前先问：**这条内容三个月后还应该存在吗？** 否定则不进 `AGENTS.md`。

判断规则：
- 稳定原则 → `AGENTS.md`（项目级）或 `STANDARDS.md`（通用工作标准）
- 当前状态 → `docs/HANDOFF.md`
- 失败记录 → `docs/LESSONS.md`
- 架构概览 → `DESIGN.md` 或 `docs/architecture/overview.md`
- 部署流程 → `DEPLOYMENT.md`
- 一次性危险操作（迁移、批量清理、目录重组）→ `docs/operations/<名称>.md`（见 `templates/operation.md`），预览-确认-备份-可恢复
- 架构决策 → `docs/architecture/ADR-NNN-xxx.md`
- 产品判断 → `docs/product/`
- 证据实验 → `docs/research/`
- 运行命令 → 最近的 `README.md`

### 文档写作原则

文档是工作状态的投影，不是工作过程的记录。

**写之前先问**：有人（或 Agent）三个月后需要这个信息才能做决策吗？否则不写。

**每份文档只回答一个问题**。写完后问：删掉这份文档，什么决策会变差？答案是"没有"则删掉。

**更新优先于新建**。能加进现有文档的内容，不单独建文件。能加一行的不写一节。

**不留占位符**。不创建内容为"待补充"的文件，不建没有文件的空目录。

**结论和理由，不是过程**。ADR 写"做了什么决策、为什么、代价是什么"，不写讨论过程。调研写"结论和支撑证据"，不写流水账。

**验收即交付**。文档工程任务的验收是：目标项目的 agent 能凭这套文档开始干活（读 AGENTS.md 知道边界，读 STANDARDS.md 知道约束，读 HANDOFF.md 知道现状），而不是"文件已创建"。
