# Handoff

更新时间：2026-09-25

## 当前状态

治理框架主线已稳定，knowledge-base track 已重构为标准 Skill 并安装到 `~/.claude/skills/`。有一个待提交的 commit（见下方进行中任务）。

## 下一步

在 `docs/` 下为当前活跃的研究方向建立第一份 ADR 或产品文档：人机协同模型的 Track 设计边界（知识库之外，下一个 track 如何判断要不要建）。

## 进行中的任务

**待提交 commit**：knowledge-base 重构 + scenario docs 删除 + AGENTS.md 链接修复，所有改动已在暂存区，等待手动提交：

```
git add AGENTS.md tracks/knowledge-base/ docs/scenarios/ && git commit -m "refactor: skill-ify knowledge-base track, clean up AGENTS.md

- Move tracks/knowledge-base/framework.md → references/framework.md
- Trim SKILL.md 143→102 lines: move design rationale to references/,
  merge retrieval list into step 6, drop duplicate long-term-separation rule
- Delete docs/scenarios/{企业知识库,投标工作流,知识库场景对照}.md
- Remove stale scenario links from AGENTS.md doc routing

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

**~/.claude/skills/ 清理**：以下目录是无效 skill，待手动删除：

```
rm -rf ~/.claude/skills/vercel-react-best-practices \
       ~/.claude/skills/hyperframes \
       ~/.claude/skills/hyperframes-animation \
       ~/.claude/skills/hyperframes-audio \
       ~/.claude/skills/hyperframes-cli \
       ~/.claude/skills/hyperframes-core \
       ~/.claude/skills/hyperframes-creative \
       ~/.claude/skills/hyperframes-keyframes \
       ~/.claude/skills/hyperframes-registry \
       ~/.claude/skills/general-video \
       ~/.claude/skills/media-use
```

## 已知问题

`docs/core/skill-design.md` 在 AGENTS.md 文档路由里有引用，但该文件尚未创建。下次需要时再建，不建空文件。

## 关键文件

- `AGENTS.md` — 项目入口和架构约束
- `docs/governance/agent-governance.md` — 协同原则、开发约束、调试和架构选择的完整版
- `docs/governance/templates/` — agents-md、dev-project-agents-md、task-contract、handoff 四个模板
- `tracks/knowledge-base/SKILL.md` — 知识库 Skill 操作指南
- `tracks/knowledge-base/references/framework.md` — 知识库设计原理深度参考
