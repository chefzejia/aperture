# Handoff

更新时间：2026-10-13

## 当前状态

文档体系优化已完成：建立了 LESSONS 机制，补充了 4 个新模板（readme、lessons、design、adr），更新了 agent-governance.md 的文档分级策略。深度研究了 magpie 的人机协同模式。项目可以接受新任务。

## 下一步

按新的文档分级策略验证：在实际项目中使用新模板，收集使用中的问题到 LESSONS.md。

## 关键文件

- `AGENTS.md` — 项目入口和架构约束
- `docs/governance/agent-governance.md` — 协同原则、文档分级策略、开发约束
- `docs/LESSONS.md` — 失败记录和规则演化（新增）
- `docs/governance/templates/` — 8 个模板：agents、readme、handoff、lessons、design、adr、dev-project-agents、task-contract
- `docs/governance/文档体系优化方案.md` — 优化过程和决策记录
- `docs/research/magpie-*.md` — magpie 人机协同研究（3 份）
- `tracks/knowledge-base/SKILL.md` — 知识库 Skill；`~/.claude/skills/knowledge-base/` 是它的安装副本，改完需重新复制
