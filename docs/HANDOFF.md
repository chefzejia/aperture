# Handoff

更新时间：2026-10-14

## 当前状态

文档体系修复、research 事实核查、magpie 源码恢复（thirdparty/，已 gitignore）均已完成。本机浏览器环境已清理：删除孤儿浏览器缓存（chromium-1228/1234，约 1.1GB），保留 1.57.0 引用的 chromium-1200，双通道实测通过。新增浏览器使用规范（AGENTS.md + 治理模板 agents.md）和部署文档模板（templates/deployment.md，源自 sample-ts-repo/DEPLOYMENT.md 的实践）。

## 下一步

- 归因收尾：Claude Code 的 Chrome/computer-use 能力取决于 claude.ai Pro/Max 认证（当前会话走第三方 provider，官方文档明确此路径不可用）——是否配双账号由人决定
- 按新的文档分级策略验证：在实际项目中使用新模板，收集使用中的问题到 LESSONS.md

## 关键文件

- `AGENTS.md` — 项目入口、架构约束、浏览器使用规范
- `docs/governance/agent-governance.md` — 协同原则、文档分级策略（含 DEPLOYMENT.md）、开发约束
- `docs/LESSONS.md` — 失败记录和规则演化（含 2026-10-13 两起新案例）
- `docs/governance/templates/` — 8 个模板：agents、readme、handoff、lessons、design、deployment、adr、architecture
- `docs/research/` — 研究文档（见 `docs/research/README.md`）；`thirdparty/magpie/` — magpie 源码快照（gitignore，可随时重下）
- `tracks/knowledge-base/SKILL.md` — 知识库 Skill；`~/.claude/skills/knowledge-base/` 是它的安装副本，改完需重新复制
