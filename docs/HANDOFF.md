# Handoff

更新时间：2026-10-14

## 当前状态

完成治理架构重整：agent-governance.md 瘦身为纯文档工程指南（教 agent 如何创建/改造项目文档），新增 templates/standards.md 作为通用工作标准的可复制真源（工具梯度、验收清单、开发约束、调试、人机边界），新项目复制为 docs/STANDARDS.md 后自治演化。标准从此随项目走，不再只在中央指南里。此前已完成：magpie 全文档体系吸收（8 项）、research 事实核查、magpie 源码恢复、浏览器环境清理。

## 下一步

- 在下一个真实项目中走完整流程：读指南 → 复制模板三件套（agents/standards/readme）→ 验证新项目的 agent 能凭文档开工
- 归因收尾：Claude Code 的 Chrome/computer-use 能力取决于 claude.ai Pro/Max 认证（当前会话走第三方 provider）——是否配双账号由人决定

## 关键文件

- `AGENTS.md` — 项目入口、架构约束、工具选择梯度、浏览器使用规范
- `docs/governance/agent-governance.md` — 文档工程指南 + 真源/投影架构说明
- `docs/governance/templates/standards.md` — 通用工作标准真源（复制即用的固定策略）
- `docs/LESSONS.md` — 失败记录和规则演化（含做对示例格式）
- `docs/governance/templates/` — 10 个模板：agents、readme、standards、handoff、lessons、design、deployment、operation、adr、architecture
- `docs/research/` — 研究文档；`thirdparty/magpie/` — magpie 源码快照（gitignore）
- `tracks/knowledge-base/SKILL.md` — 知识库 Skill；`~/.claude/skills/knowledge-base/` 是它的安装副本，改完需重新复制
