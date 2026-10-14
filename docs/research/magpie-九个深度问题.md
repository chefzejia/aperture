# magpie 九个深度问题的回答

> 事实核查：2026-10-13（GitHub API）。文中 LESSONS.md 尺寸等数字已按实测更新。


## 问题 1：LESSONS 是第一个要吸收的机制

**完全同意**。LESSONS 是 magpie 人机协同的核心创新，也是最值得我们立即实施的。

### 为什么 LESSONS 在 AI 化时代不可或缺

1. **Agent 需要显式记忆**
   - LLM 本身无状态，每次对话都是新开始
   - LESSONS.md 提供了"项目级别的错误记忆"
   - Agent 每次开始任务前读 LESSONS，避免重复错误

2. **人的认知有限**
   - 人无法记住所有历史错误
   - LESSONS 作为外部记忆，弥补人的遗忘
   - 规则有证据链（commit + issue），可验证

3. **规则需要演化**
   - 不是所有规则都一开始就对
   - LESSONS 是"暂存区"，验证 3 次后才固化
   - 避免过早泛化

### 我们的实施方案

**立即创建** `docs/LESSONS.md`：

```markdown
<!-- reviewed-through: <commit-hash> (YYYY-MM-DD) -->
# Lessons from Agent Work

本文档记录 Agent 在实际工作中重复出现的失败模式。
每条规则附带证据（commit + issue/任务记录），出现 3 次后晋升到 agent-governance.md。

## 知识整理

### [规则占位符]

**规则**：[应该怎么做]
- 证据1：[commit/任务] + 说明
- 证据2：...
- Seen N× (YYYY-MM-DD, ...)

## Skill 实现

[待补充]

## 文档维护

[待补充]

## 已晋升到治理规范

以下规则已被看到 3 次以上，移入 agent-governance.md：
- [规则名] → 见 agent-governance.md#xxx
```

**运作流程**：

1. **记录失败**（人或 Agent）
   - Agent 修复了前一周/两周内的问题
   - 写入 LESSONS.md：规则 + 最新证据

2. **定期 review**（建议每周）
   - 人工 review 本周的工作
   - 识别重复失败模式
   - 更新 LESSONS.md

3. **规则晋升**（3 次后）
   - 移到 agent-governance.md
   - 在 LESSONS.md 保留引用

4. **定期归档**（每季度）
   - 更新 reviewed-through 标记
   - 超过 3 个月未再出现的规则 → 归档到 docs/archive/

---

## 问题 2：验收标准应该从底层思考，适配具体项目

**非常对**。验收标准不应该是"一刀切"，而应该是**可定义的第一性原理 + 项目适配层**。

### magpie 的验收标准设计

magpie 的 6 条验收标准看起来是具体的，但实际上是**两层结构**：

**第一层：通用原则**（适用所有项目）
1. **可证伪性**："测试能在旧代码上失败"
2. **隔离性**："测试在沙盒中运行"
3. **自动化**："构建和测试套件"
4. **真实性**："在真实环境验证"

**第二层：项目实现**（Go + GUI 项目的具体化）
1. gofmt + go vet + go test
2. GUI 测试双引擎（Chromium + WebKit）
3. 跨平台（Linux、macOS、Windows）
4. 在真实 vendor 账号测试

### 我们的设计原则

**定义通用的验收原则**（写入 agent-governance.md）：

```markdown
## 验收原则（第一性）

任何工作结果必须满足：

1. **可证伪性**：有明确的"失败方式"，能被检查证伪
2. **可重现性**：他人或 Agent 能独立重现结果
3. **可观测性**：过程和结果对人直接可见、可理解
4. **真实性**：在真实环境/数据/工具中验证
5. **边界性**：只修改授权范围，不污染其他部分
6. **可回滚性**：失败时能恢复到之前状态

## 项目验收标准（适配层）

每个 track 根据自己的工作类型，把验收原则具体化为可执行的检查。
```

**为 knowledge-base 制定具体标准**：

```markdown
## knowledge-base Skill 验收标准

基于验收原则的具体实现：

### 1. 可证伪性
- [ ] 笔记有明确的 frontmatter（状态、来源、有效期）
- [ ] 冲突和未知显式标记，不伪装成确定
- 检查方法：`grep -r "状态: 待确认\|conflicted\|unknown" notes/`

### 2. 可重现性
- [ ] 来源可回溯（页码、章节、URL、时间戳）
- [ ] 重复执行不产生新的重复笔记
- 检查方法：运行两次，`diff -r notes/` 无变化

### 3. 可观测性
- [ ] 在 Obsidian/VS Code 中打开 notes/，frontmatter 解析正确
- [ ] Wiki 链接可点击，图片显示
- [ ] 人能直接编辑 Markdown 继续工作

### 4. 真实性
- [ ] 在真实知识库上测试（不是 mock 数据）
- [ ] 让另一个 Agent 查询知识库完成任务
- [ ] 检查是否找到正确答案、是否误用候选内容

### 5. 边界性
- [ ] 只写入 notes/（经确认的）
- [ ] 候选和草稿留在 inbox/
- [ ] 未触碰授权范围外的文件

### 6. 可回滚性
- [ ] 原始材料保留在 inbox/
- [ ] 失败现场可查看
- [ ] 可删除 notes/ 重新运行
```

### 关键洞察

验收标准的设计应该是：

```
第一性原则（6条，跨项目）
    ↓
验收原则（agent-governance.md）
    ↓
项目验收标准（tracks/*/SKILL.md）
    ↓
可执行的检查（命令、步骤、工具）
```

这样：
- 不同项目可以有不同的检查方式
- 但都基于相同的第一性原则
- 新 track 可以参考知识库的标准，适配自己的场景

---

## 问题 3：强制规范的区分和标准

**你的思考非常对**。不是所有规则都应该"强制"，需要区分**稳定原则**和**待验证规则**。

### magpie 的处理方式

magpie 实际上有三层规则：

1. **不可违反的规则**（code-standards.md）
   - 经过 3 次以上验证
   - 每次违反都导致问题
   - 例如："测试能在旧代码上失败"

2. **待验证的规则**（LESSONS.md）
   - 出现 1-2 次
   - 可能是真实模式，也可能是偶然
   - 例如："GUI 测试在两个引擎"（出现 2 次后才固化）

3. **原则性指导**（AGENTS.md）
   - 简洁、稳定
   - 不是具体规则，而是方向性指导
   - 例如："Before changing code, read LESSONS.md"

### 我们的改进方案

**在 agent-governance.md 中区分三个层次**：

```markdown
## 架构约束（不可违反）

以下约束从第一性原理推出，违反会破坏人机协同的基础：

1. 共同可观测
2. 授权边界
3. 显式不确定
4. 当前与长期分离
5. 单一主线

**判断标准**：如果违反这条，会导致"人和 Agent 失去共同真相"。

## 开发规范（经过验证）

以下规范来自真实失败案例，已被验证 3 次以上：

[从 LESSONS.md 晋升的规则]

**判断标准**：在 LESSONS.md 中出现 3 次，每次违反都导致返工。

## 实验性规则（LESSONS.md）

以下规则正在验证中，出现 1-2 次：

[见 docs/LESSONS.md]

**判断标准**：出现次数未达到 3 次，但有明确证据。

## 场景化规则（tracks/*/SKILL.md）

每个 track 可以有自己的规则，但不能与架构约束冲突：

- knowledge-base: [见 tracks/knowledge-base/SKILL.md]
- [未来的其他 tracks]
```

### 规则晋升的判断标准

**什么时候一条规则可以从"待验证"晋升为"强制"？**

必须同时满足：
1. **出现 ≥3 次**（数量标准）
2. **每次违反都导致返工**（影响标准）
3. **有明确的检查方式**（可执行标准）
4. **不同场景下都成立**（普遍性标准）

例如：
- ✅ "测试能在旧代码上失败" - 满足所有条件
- ❌ "GUI 测试双引擎" - 只在有 GUI 的项目成立
- ❌ "不允许 mock" - 太绝对，有例外场景

---

## 问题 4：magpie 的文档是否完整暴露？

**非常犀利的问题**。你说得对，**magpie 的文档可能并未完全暴露工作流**。

### 证据分析

**已暴露的文档**（34 个 .md 文件）：
- AGENTS.md (5KB)
- LESSONS.md (约 26KB, 2026-10-13 实测)
- code-standards.md (14KB)
- subsystems/ (350KB)
- contributors.md

**但关键工作流细节缺失**：

1. **如何触发 Agent 工作？**
   - 没有找到 "issue watcher"、"webhook handler" 等代码
   - 没有文档说明 "Agent 如何知道有新 issue"

2. **如何协调多个 Agent？**
   - LESSONS.md 提到"两个 sessions 同时修复同一问题"
   - 但没有文档说明如何避免冲突

3. **人的 review 流程？**
   - 说"每晚 review"，但没说：
     - 用什么工具？
     - 怎么提取模式？
     - 如何决定规则晋升？

4. **commit 的产生过程？**
   - Git log 显示 2458 commits by yetone
   - 但没说这些 commits 是：
     - Agent 直接 commit？
     - 人 review 后 commit？
     - Agent 提 PR，人 merge？

### 推测的隐藏细节

**基于 Git 分析**：

```bash
# Git 作者分析
2458 commits by yetone (94%)
  36 commits by TryWorld
  29 commits by forever
  27 commits by Charan Rathore
```

**说明**：
- yetone（作者）占 94% 的 commits
- 可能的模式：
  - Agent 在本地工作
  - 人 review 后以人的名义 commit
  - 或者：Agent 使用人的 git config

**基于 LESSONS.md 的线索**：

> magpie's code is written, reviewed, merged and released **by agents**. Each night the day's commits are **reviewed** for what had to be fixed again.

**说明**：
- 代码由 agents（复数）写
- 每晚人工 review
- 但没说中间的流程

### 我们的文档可能也有类似问题

**检查我们的文档**：

当前我们有：
- AGENTS.md ✓
- agentic-work-model.md ✓
- agent-governance.md ✓
- knowledge-base/SKILL.md ✓

**但缺少**：
- ❌ 如何启动一个任务？
- ❌ Agent 如何读取任务？
- ❌ 人如何 review Agent 的工作？
- ❌ 如何确认结论进入长期知识？
- ❌ 实际的工作流脚本/工具

### 改进方案

**补充到 AGENTS.md**：

```markdown
## 如何使用本项目

### Agent 开始工作

1. 读取当前状态：`docs/HANDOFF.md`
2. 读取协同规范：`docs/governance/agent-governance.md`
3. 读取失败历史：`docs/LESSONS.md`（如果存在）
4. 确认任务边界（授权范围、输入、输出）
5. 执行工作
6. 运行验收检查
7. 报告结果

### 人的介入时机

- 确认长期结论（knowledge-base 的 notes/）
- 裁定冲突（多个来源不一致时）
- 批准高风险修改（删除、重构）
- Review 并晋升规则（LESSONS → agent-governance）

### 实际操作

[这里应该有具体的命令、脚本或工具]
```

**需要补充的实际工具**：
- review.sh - 辅助人 review 本周工作
- promote.sh - 辅助规则晋升
- verify.sh - 运行验收检查

---

## 问题 5：如何固化人的参与，引入人类参与

**magpie 人类参与的程度确实极少**（作者占 94% commits），但**人的参与是关键节点**。

### magpie 的人类参与点

**从 LESSONS.md 和 code-standards.md 反推**：

1. **每晚 review**（最重要）
   - 人工看当天所有 commits
   - 提取重复失败模式
   - 写入 LESSONS.md

2. **PR 验收**
   - pull、merge、运行检查、记录
   - 使用 `--match-head-commit` 防护

3. **规则晋升决策**
   - 哪些规则从 LESSONS → code-standards
   - 这是**人的判断**，不是自动的

4. **产品决策**
   - scroll guard、button cursor 等
   - 明确说"是 maintainer 的决策"

5. **风险决策**
   - contributors.md：哪些 PR 需要人先看
   - 哪些作者进 block list

### 我们的人类参与设计

**在 agent-governance.md 补充**：

```markdown
## 人的参与节点

### 1. 定期 Review（每周/每两周）

**时间**：建议周五下午或周日晚

**步骤**：
1. 检查本周的工作记录
   ```bash
   git log --since="1 week ago" --oneline
   ```

2. 识别重复失败
   - 看哪些文件/问题被修改了多次
   - 看 commit message 中的"fix"、"修复"

3. 更新 LESSONS.md
   - 提取规则
   - 附加证据（commit hash + 说明）
   - 标记 Seen N×

4. 评估规则晋升
   - 检查 LESSONS.md 中 Seen ≥3× 的规则
   - 决定是否晋升到 agent-governance.md

**工具辅助**：
```bash
# 辅助脚本（未来实现）
./scripts/review-helper.sh
```

### 2. 任务启动（每次）

**人决定**：
- 这个任务是否启动？
- 授权范围是什么？
- 边界条件是什么？

**Agent 执行**：
- 在授权范围内工作
- 遇到边界停下来询问

### 3. 结论确认（每次）

**人确认**：
- 这个结论是否足够稳定？
- 可以进入长期知识吗？
- 还是只是当前任务的临时结论？

**标准**：
- 有明确来源
- 无冲突
- 适用范围清楚
- 有效期明确（如果有）

### 4. 冲突裁定（按需）

**什么时候**：
- 多个来源说法不一致
- 新信息与旧知识矛盾
- 规则之间有冲突

**人决定**：
- 哪个来源更可信
- 如何合并不同版本
- 是否需要更多证据

### 5. 高风险批准（按需）

**需要批准的操作**：
- 删除多个文件
- 重构架构
- 修改授权边界
- 影响生产的修改

**Agent 做**：
- 说明影响
- 列出风险
- 提供可逆方案（如果有）

**人决定**：批准/拒绝/修改方案

## 人的参与频率

| 角色 | 频率 | 耗时估计 |
|------|------|---------|
| 定期 review | 每周 | 30-60 分钟 |
| 任务启动 | 每个任务 | 5-10 分钟 |
| 结论确认 | 每个长期结论 | 5-15 分钟 |
| 冲突裁定 | 按需 | 10-30 分钟 |
| 高风险批准 | 按需 | 15-30 分钟 |
```

### 工具支持（未来实现）

```bash
# scripts/review-helper.sh
# 辅助人 review 本周工作

# 1. 列出本周修改最多的文件
git log --since="1 week ago" --name-only --format="" | sort | uniq -c | sort -rn | head -20

# 2. 列出包含"fix"的 commits
git log --since="1 week ago" --oneline --grep="fix\|修复\|修正"

# 3. 列出 LESSONS.md 中可能晋升的规则
grep "Seen [3-9]" docs/LESSONS.md
```

---

## 问题 6：CI 的替代方案和性价比

**非常实际的问题**。GitHub Actions 有免费额度，但如果超了确实需要考虑替代方案。

### GitHub Actions 的免费额度

**Public repos**：
- 无限制（免费）

**Private repos**：
- Free plan: 2000 分钟/月
- Pro plan: 3000 分钟/月

**我们的情况**：
- agentic-work-infra 是 public repo？
- 如果是，完全免费

### 本地 CI 方案

**方案 1：Git Hooks**

```bash
# .git/hooks/pre-commit
#!/bin/bash

# 检查 markdown 链接
./scripts/check-links.sh

# 检查 frontmatter 格式
./scripts/check-frontmatter.sh

# 检查没有未跟踪的重要文件
git status --short | grep "^??" && echo "有未跟踪文件" && exit 1

exit 0
```

**优点**：
- 完全本地
- 立即反馈
- 零成本

**缺点**：
- 只在本地运行
- 容易被 skip（`git commit --no-verify`）
- 不能跨平台测试

**方案 2：本地 CI 工具**

**选项 A：act（模拟 GitHub Actions）**

```bash
# 安装
brew install act

# 运行 .github/workflows/check.yml
act -j check
```

**优点**：
- 复用 GitHub Actions 配置
- 本地预览 CI 结果

**缺点**：
- 需要 Docker
- 慢

**选项 B：pre-commit framework**

```bash
# 安装
pip install pre-commit

# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-markdown-links
        name: Check markdown links
        entry: scripts/check-links.sh
        language: script
      - id: check-frontmatter
        name: Check frontmatter
        entry: scripts/check-frontmatter.sh
        language: script
```

**优点**：
- 标准化
- 易于扩展
- 有社区 hooks

**缺点**：
- 依赖 Python
- 学习成本

**方案 3：Makefile**

```makefile
# Makefile

.PHONY: check
check: check-links check-frontmatter check-untracked

check-links:
	@echo "Checking markdown links..."
	@./scripts/check-links.sh

check-frontmatter:
	@echo "Checking frontmatter..."
	@./scripts/check-frontmatter.sh

check-untracked:
	@echo "Checking untracked files..."
	@git status --short | grep "^??" && echo "有未跟踪文件" && exit 1 || true

.PHONY: review
review:
	@echo "Review helper..."
	@./scripts/review-helper.sh
```

**使用**：
```bash
make check  # 运行所有检查
make review # 辅助 review
```

**优点**：
- 简单
- 无依赖（Make 内置）
- 易于理解

**缺点**：
- 功能有限
- 不如专业 CI 工具

### 推荐方案

**对我们项目**：

```
阶段 1（当前）：Makefile + 简单脚本
  ↓
阶段 2（有需要时）：GitHub Actions（public repo 免费）
  ↓
阶段 3（复杂后）：本地 pre-commit + 远程 GitHub Actions
```

**立即实施**：

```bash
# 创建 Makefile
# 创建 scripts/check-links.sh
# 创建 scripts/check-frontmatter.sh
# 创建 scripts/review-helper.sh
```

**GitHub Actions（如果需要）**：

```yaml
# .github/workflows/check.yml
name: Check
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check links
        run: make check-links
      - name: Check frontmatter
        run: make check-frontmatter
```

### 性价比最高的方案

**对大多数项目**：
1. **Makefile + Git hooks**（本地，立即反馈）
2. **GitHub Actions**（远程，public repo 免费）
3. 两者结合：本地快速检查 + 远程完整验证

**成本**：
- 开发时间：1-2 小时建立脚本
- 运行成本：$0（public repo）

---

## 问题 7：Agent 如何感知 issue？工作流细节

**这是最关键的问题**，magpie 的文档确实没有完全暴露这部分。

### 从证据推测工作流

**证据 1：Git log 分析**

```
2458 commits by yetone (94%)
单日 220 commits（2026-10-05）
```

**说明**：
- 绝大多数 commits 由作者提交
- 不是每个 Agent 用自己的 git config
- **可能模式**：Agent 工作 → 人 review → 人以自己名义 commit

**证据 2：LESSONS.md 的表述**

> Two sessions committing from one checkout shipped each other's files under the wrong subjects.

**说明**：
- 有"两个 sessions"概念
- 它们共享一个 git checkout
- **可能**：多个 Agent sessions 并行，但共享一个工作目录

**证据 3：contributors.md**

> magpie merges community PRs through agents. An agent only proposes. It writes the evidence (PR numbers, dates, what was wrong) to the maintainer; **the maintainer decides**.

**说明**：
- Agent 处理 community PRs
- Agent 只"提议"（propose），不直接决策
- 人最终决定

### 推测的工作流

**模式 A：Issue → Agent → 人 review → commit**

```
用户提 issue #123 →
  (可能手动) 分配给 Agent →
  Agent 在本地分支工作 →
  Agent 运行测试 →
  Agent 报告"完成，通过测试" →
  人 review 代码和测试 →
  人以自己名义 commit →
  人 push →
  CI 运行 →
  (如果绿) 人打 tag release
```

**模式 B：Agent 监控 issues**

```
脚本/服务监控 GitHub issues →
  新 issue 触发 Agent →
  Agent 读 issue + AGENTS.md + LESSONS.md →
  Agent 在独立分支工作 →
  Agent 提交本地 commits →
  Agent 报告完成 →
  人 review →
  人 cherry-pick 到 main（以人的名义）→
  人 push 和 release
```

**模式 C：多个 Agent，人协调**

```
人看 issues，分配任务 →
  Agent A 处理 #123 →
  Agent B 处理 #124 →
  并行工作（不同 worktrees？）→
  各自报告完成 →
  人 review 所有工作 →
  人合并、解决冲突 →
  人 commit 和 push →
  人 release
```

### 关键问题的答案

**Q: Agent 是如何感知 issue 的？**

**推测**：
- **不是自动**的（没找到 webhook/watcher 代码）
- **可能是人工分配**：人看到 issue，告诉 Agent "处理 #123"
- **或者是定时轮询**：脚本定期检查新 issues（但代码里没找到）

**Q: 什么叫"同一问题修复了多次"？**

**案例**（LESSONS.md）：
> #834 came back 4 times (v0.1.920 → .925 → .931 → .938). Each round fixed only the agent in the screenshot.

**说明**：
- 用户报 #834
- Agent 修复 → release v0.1.920
- 用户说还不行
- Agent 再修复 → release v0.1.925
- 用户又说还不行
- Agent 再修复 → release v0.1.931
- 最终修对 → release v0.1.938

**不是"不同 Agent 在不同分支"**，而是**同一 issue，多次迭代修复**。

**Q: 是否有主 Agent 和人一起 review？**

**推测**：
- **人是主 reviewer**
- **Agent 可能辅助**（比如运行测试、检查格式）
- **但最终决策是人的**

**证据**：
- contributors.md："An agent only proposes... the maintainer decides"
- code-standards.md："A PR is merged only after a maintainer has pulled it, merged it onto current main and run the checks"

### 我们可以借鉴的

**简化版工作流**（适合我们）：

```
1. 人创建任务（在 issues、或本地文档）
   ↓
2. 人告诉 Agent："处理这个任务"
   ↓
3. Agent 读 AGENTS.md + LESSONS.md + 任务描述
   ↓
4. Agent 工作（在授权范围内）
   ↓
5. Agent 报告完成 + 运行了哪些检查 + 结果
   ↓
6. 人 review
   ↓
7. 人确认 → commit
   或人拒绝 → Agent 修改
```

**不需要**：
- 自动监控 issues
- 多个 Agent 并发
- 复杂的协调机制

**足够的**：
- 人手动分配任务
- 单个 Agent 顺序执行
- 人最终把关

---

## 问题 8：维护工作流 vs. 开发工作流

**非常敏锐的观察**。你说得对，我们看到的可能是**维护阶段**的工作流，不是**开发阶段**。

### 证据分析

**项目特征**：
- 代码量：258,297 行 Go（不含测试）
- 测试：1,752 个测试文件
- 提交：2458 by yetone，36 by TryWorld...
- 文档：LESSONS.md reviewed-through 2026-10-10

**说明**：
- 这是一个**成熟项目**
- 已经建立了完整的规范体系
- 现在处于**高频维护 + 功能迭代**阶段

### 开发阶段 vs. 维护阶段

**开发阶段**（推测 magpie 早期）：
- 作者手写核心架构
- 建立 subsystems 设计文档
- 制定 code-standards.md
- 训练 Agent 理解项目

**维护阶段**（现在）：
- Agent 处理 issues 和 PRs
- 人 review 和提取 LESSONS
- 规则不断优化
- 高频 release

### 可能缺失的文档

**早期决策文档**：
- 为什么选 Go？
- 为什么用 Gateway 架构？
- 为什么用 plugin 系统？
- 这些可能只在作者脑子里

**架构演化**：
- 哪些设计是重构的？
- 哪些是一开始就对的？
- 踩过哪些坑？
- 可能在 git history，但没文档

**工程品味**：
- 什么是"好代码"？
- 什么是"过度设计"？
- 什么时候应该抽象？
- 这些在 code-standards.md 有部分体现

### 我们可以学到什么

**阶段 1：建立基础**（我们现在）
- 定义核心原则（agentic-work-model.md ✓）
- 建立治理规范（agent-governance.md ✓）
- 实现第一个 track（knowledge-base ✓）
- **关键**：人写核心设计，Agent 实现细节

**阶段 2：迭代验证**（接下来）
- 在真实任务中使用
- 记录失败（LESSONS.md）
- 优化规则
- Agent 参与度逐渐提高

**阶段 3：稳定运行**（未来）
- Agent 处理大部分任务
- 人定期 review
- 规则自动化
- 类似 magpie 现在的状态

**关键洞察**：
> magpie 的文档体系是**演化出来的**，不是一开始就设计好的。
>
> 我们也应该：
> 1. 先有核心原则
> 2. 在实践中验证
> 3. 用 LESSONS 记录失败
> 4. 逐步固化规则

---

## 问题 9：如何防止 Agent 过度设计和堆屎山

**这是最深刻的问题**，也是人机协同的核心挑战。

### magpie 是如何做到的？

**证据 1：code-standards.md 的设计原则**

虽然没有单独章节讲"防止过度设计"，但有暗含的原则：

```markdown
| A change does only what its goal needs. |
| Every change in behavior has a reason. |
| Unrelated refactors, extra features and policy changes go in a PR of their own. |
```

**说明**：
- 每个修改只做需要的事
- 无关的重构单独做
- 功能和策略分离

**证据 2：LESSONS.md 的例子**

> 653cb8ee bundled ZCode sign-in with WSL session deletion.
> 5464a362 capped six pages at 1200px when #860 asked for a speed display.
>
> Seen 2× (2026-10-05, 2026-10-06).

**说明**：
- 捆绑不相关的修改被记录为失败模式
- 这种"顺手做"被明确反对

**证据 3：架构选择章节**

虽然 agent-governance.md 有，但 magpie 的 code-standards.md **没有**专门讲"何时抽象"、"何时不抽象"。

**可能的原因**：
- 这些是作者脑子里的
- 通过 PR review 传递
- **没有完全文档化**

### magpie 防止过度设计的机制（推测）

**机制 1：人的 PR review**

```markdown
A PR is merged only after a maintainer has pulled it,
merged it onto current main and run the checks above on the result.
```

**说明**：
- 人最终把关
- 人可以拒绝"过度设计"的 PR
- **这是最重要的防线**

**机制 2：规则约束**

```markdown
A change does only what its goal needs.
```

**说明**：
- 限制 Agent 的修改范围
- 不允许"顺手做其他事"

**机制 3：LESSONS 反馈**

- 发现"bundled"修改 → 记录到 LESSONS
- 下次 Agent 读 LESSONS，避免重复

**机制 4：真实验证**

- 要求在真实环境测试
- 过度设计往往在真实环境暴露问题
- 例如：不必要的抽象导致性能问题

### magpie 可能缺失的

**代码量控制**：
- 没有看到"删除代码"的奖励机制
- 258K 行代码，是否有不必要的部分？

**架构审查**：
- 没有看到定期"架构 review"
- 是否有技术债累积？

**重构标准**：
- 什么时候应该重构？
- 什么时候不应该？
- 文档里没有

### 我们如何防止过度设计

**在 agent-governance.md 补充章节**：

```markdown
## 防止过度设计

### 判断标准

**什么时候加复杂度？**

必须同时满足：
1. **解决真实问题**：有具体的用户需求或技术问题
2. **成本可控**：维护、认知、运行成本不超过收益
3. **未来可变**：让某个已知的未来变化更便宜
4. **不加会坏**：选更小的方案，某个质量/安全边界会被破坏

**什么时候不加？**

- 为假想需求设计
- "可能以后会用"
- "更工程化"、"别人都这么做"
- Agent 写起来更顺手

### 单一职责

**一个 PR/commit 只做一件事**：
- 修复 bug
- 或添加功能
- 或重构
- **不混合**

**证据**（LESSONS.md）：
- 653cb8ee bundled ZCode sign-in with WSL session deletion
- 这种做法被明确反对

### 抽象的时机

**原则**：
- **单一场景直接实现**
- **抽象延迟到第二个真实用例**

**例子**：
- ✅ 第一次：直接写 knowledge-base 的笔记处理
- ✅ 第二次：有新 track 需要类似功能，才抽象共同部分
- ❌ 第一次就设计"通用内容管理框架"

### 删除优于兼容

**内部重构**：
- 直接删除过时代码
- 不增加兼容层
- 不双写

**对外接口**：
- API、数据格式的兼容另论
- 需要单独评估

### 人的审查职责

**每次 review 时检查**：
1. 这个修改是否只做了它应该做的？
2. 是否有"顺手做"的其他事？
3. 是否引入了不必要的抽象？
4. 是否有更简单的实现？
5. 删除了什么代码吗？（删除是好事）

### LESSONS 记录

**出现过度设计时**：
- 记录到 LESSONS.md
- 说明为什么是过度的
- 附加证据（commit + 问题）

**例子格式**：
```markdown
## 过度设计

**不要为假想需求设计系统**

- 证据1: commit xxx 为"可能的未来多语言"建立了复杂的 i18n 框架，
  但项目只用中文，增加了维护负担
- Seen 1× (YYYY-MM-DD)
```
```

### 核心洞察

**magpie 能防止过度设计，主要靠**：
1. **人的最终把关**（94% commits by 作者）
2. **规则约束**（一次只做一件事）
3. **真实验证**（过度设计在真实环境暴露）
4. **LESSONS 反馈**（记录失败，避免重复）

**但 magpie 可能也有过度设计**：
- 258K 行代码
- 是否有不必要的部分？
- 文档里没有"删除代码"的案例

**我们的优势**：
- 从一开始就意识到这个问题
- 可以设计"防过度设计"的机制
- 用 LESSONS 显式记录

**关键**：
> **人的审美和判断力是最后防线**
>
> Agent 可以写代码，但"什么是好设计"仍然需要人判断。
>
> 所以：
> 1. 人必须定期 review
> 2. 人必须有权拒绝"过度设计"
> 3. 人的判断要记录到 LESSONS，让 Agent 学习

---

## 总结：九个问题的核心启示

1. **LESSONS 是核心机制** - 立即实施
2. **验收标准分层** - 第一性原则 + 项目适配
3. **规则分三层** - 架构约束 / 经过验证 / 实验性
4. **文档可能不完整** - 补充实际工作流和工具
5. **人的参与是关键** - 定期 review、规则晋升、风险决策
6. **CI 可以简化** - Makefile + Git hooks 足够
7. **工作流是人分配的** - 不需要自动监控，人手动分配任务
8. **维护 vs 开发** - 我们处于建立阶段，需要人写核心设计
9. **防止过度设计** - 人的审美是最后防线，用 LESSONS 记录

**最重要的三点**：

1. **建立 LESSONS.md** - 记录失败，让 Agent 从错误中学习
2. **人的定期 review** - 每周 review，提取模式，晋升规则
3. **防过度设计机制** - 一次一件事、延迟抽象、人有权拒绝
