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

## 工具选择梯度（固定策略）

一切任务按"最轻够用一级优先"选择，跳级必须说明理由；computer use 只用于无 API 的表面，不是更重的浏览器工具。完整定义见 [Agent 项目协同规范](docs/governance/agent-governance.md) 的"工具选择梯度"。宿主缺某级时显式报告缺口，不假装完成；断言"不具备某能力"前先实测。

## 浏览器使用规范（本机实测 2026-10-14）

浏览器任务在本机的具体入口（上一节梯度的实例化）：

1. **检索/读静态页面**：curl/WebFetch（无 JS 渲染需求时首选，最轻）
2. **需要渲染或交互**：playwright，**只用 poetry venv 的 python**：
   `"~/Library/Application Support/pypoetry/venv/bin/python"`
   （默认 `python3` 没装 playwright，用错解释器会误报"未安装"）
3. **访问系统 Chrome 登录态**：`chromium.launch(channel="chrome")`
4. **无 API 的原生 App / 模拟器 / 纯 GUI 表面**：computer use（注意：这是另一类表面，不是浏览器的升级版；浏览器内任务不应落到这级）
5. **用不了某一级时**：明确报告缺口，按需升级或停下，不静默跳级、不假装完成

浏览器缓存只保留在装版本引用的 build（当前 chromium-1200）。声称"本机不具备某能力"前必须先实测。

外部源码引用统一放 `thirdparty/`（已 gitignore，快照可重下，不进主仓库）。

## 文档路由

### 理解原则
- [人机协同模型](docs/core/agentic-work-model.md) — 第一性原则、协同边界、Track 定义
- [Agent 项目协同规范](docs/governance/agent-governance.md) — 日常协同、验证、调试和架构选择
- [Skill 设计最佳实践](docs/core/skill-design.md) — 如何写好 Skill

### Tracks
- [知识库](tracks/knowledge-base/SKILL.md) — 人机协同整理和使用知识
