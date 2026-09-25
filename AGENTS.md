# Agentic Work Infra

适用范围：整个 `agentic-work-infra` 仓库。

## 项目定位

本项目研究 Agent 时代人和 Agent 如何协同完成真实工作。知识库、投标和其他业务是研究课题（track），不是项目的边界。

原则、推导和实现方式在 [人机协同模型](docs/core/agentic-work-model.md)。

## 架构约束（不可违反）

1. **共同可观测**：人和 Agent 面对同一个工作状态，不分别维护两套。
2. **授权边界**：Agent 只修改明确授权的范围，不能静默覆盖原始材料。
3. **显式不确定**：未知、冲突和待确认必须保持显式，不能伪装成确定。
4. **当前与长期分离**：当前任务可以引用长期知识和规则，但不能把任务变量自动写回长期层。
5. **单一主线**：架构不分叉；辅助工具（索引、缓存、生成结果）可以删除后重建，不能成为第二套工作状态。

## 修改和验证

```bash
git status --short --branch -uall
git diff --check
```

检查：文档链接目标是否存在；核心文档是否仍只有一条主线；未跟踪文件是否形成重复版本或隐藏主线。

## 文档路由

### 理解原则
- [人机协同模型](docs/core/agentic-work-model.md) — 第一性原则、协同边界、Track 定义
- [Agent 项目协同规范](docs/governance/agent-governance.md) — 日常协同、验证、调试和架构选择
- [Skill 设计最佳实践](docs/core/skill-design.md) — 如何写好 Skill

### Tracks
- [知识库](tracks/knowledge-base/SKILL.md) — 人机协同整理和使用知识
