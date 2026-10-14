# Handoff

更新时间：2026-10-14（二轮 review 后）

## 当前状态

治理架构重整完成并经全仓 review 修正：agent-governance.md 为纯文档工程指南，templates/standards.md 是可复制标准真源，本仓自身以指向式 docs/STANDARDS.md 承接（真源仓库形态，不复制避免双写）。review 修复：验收清单重复段、readme 模板完整配置缺 STANDARDS、agents 模板失效路径引用、governance 与 standards 核心原则逐字重复、LESSONS 未入小型推荐列。

## 下一步

- 在下一个真实项目中走完整流程：读指南 → 复制三件套（agents/standards/readme）→ 验证新项目的 agent 能凭文档开工
- 归因收尾：Claude Code 的 Chrome/computer-use 能力取决于 claude.ai Pro/Max 认证（当前会话走第三方 provider）——是否配双账号由人决定

## 关键文件

- `AGENTS.md` — 项目入口、架构约束、工具选择梯度、浏览器使用规范
- `docs/governance/agent-governance.md` — 文档工程指南 + 真源/投影架构
- `docs/governance/templates/standards.md` — 通用工作标准真源；`docs/STANDARDS.md` — 本仓指向式承接
- `docs/LESSONS.md` — 失败记录和规则演化（晋升出口：standards 真源）
- `docs/governance/templates/` — 10 个模板
- `docs/research/` — 研究文档；`thirdparty/magpie/` — magpie 源码快照（gitignore）
- `tracks/knowledge-base/SKILL.md` — 知识库 Skill；`~/.claude/skills/knowledge-base/` 是它的安装副本，改完需重新复制
