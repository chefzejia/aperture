# 研究文档

本目录保存调研当时的记录，正文保留当时的文件名与术语（如 `HANDOFF.md`、`STANDARDS.md`、`agent-governance.md`、`tracks/`、“三角色”“四重身份”），不随规范更新。当前规范以 [`docs/core/`](../core/agentic-work-model.md) 与 [`skills/`](../../AGENTS.md) 为准。

| 文档 | 事实核查 | 内容 | 状态 |
| --- | --- | --- | --- |
| [dsh-native-agent-team-workflow.md](dsh-native-agent-team-workflow.md) | 2026-11-06 | 双环协作 + Git 钩子唤醒方案与 dsh-superagent-prototype、magpie 三 loop 的对比；常驻会话提示缓存命中率 97.75%~98.62% 的实测 | 协议已并入 multi-agent-collab Skill，本文保留对比与实测数据 |
| [worker-benchmark-2026-10-28.md](worker-benchmark-2026-10-28.md) | 2026-10-28~29 | 本机候选 Worker 宿主与模型的实测：耗时、轮数、成本、范围纪律，以及 RTK、Magpie 插件等混杂变量 | 仅适用于当时本机的模型与宿主 |
| [三角色协作设计.md](三角色协作设计.md) | 2026-10-15 | Brain / Worker / Tester 三角色设计与基于 Orca CLI 的协调脚本 | 已被 multi-agent-collab Skill 的双环协作取代 |
| [orca-配置指南.md](orca-配置指南.md) | 2026-10-15 | Orca v1.4.224 的监督式编排与完全移交、worktree、模型参数 | CLI 结论对应当时版本 |
| [herdr-调研.md](herdr-调研.md) | 2026-10-13 | Herdr 作为编码 Agent 运行时的定位，与 LangGraph、CrewAI 的分层对比 | 调研快照 |
| [magpie-九个深度问题.md](magpie-九个深度问题.md) | 2026-10-13 | magpie 的 LESSONS 机制、规则晋升、人机边界与 CI 门禁 | LESSONS 漏斗已并入 project-governance Skill |
| [magpie-loop模式研究.md](magpie-loop模式研究.md) | 2026-10-14 | 作者的三个常驻 loop、任务式与常驻式两种人机介入时机 | 调研快照 |

## 多 Agent 工具定位

| 工具 | 定位 | 适用场景 |
| --- | --- | --- |
| Orca | 桌面 ADE，并行 worktrees | GUI 工作流，可视化管理多个 Agent |
| Herdr | 终端运行时 | 后台持久化，CLI 工作流 |
| LangGraph | 编排框架（低层） | 复杂状态流转，需要精细控制 |
| CrewAI | 编排框架（高层） | 角色明确的多 Agent 团队 |
| Claude Code Workflow | 内置编排 | 官方原生，`agent()` / `parallel()` / `pipeline()` |

## 收录原则

- 个人配置不是研究成果，不收录；
- 已沉淀进 Skill 的结论以 Skill 为准，原文作为快照保留；
- 中间产物被最终报告吸收后删除，只保留有独立价值的调研报告。
