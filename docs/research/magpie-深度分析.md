# 对 magpie 人机协同研究的深度分析

> 事实核查：2026-10-13。文中数字已与 GitHub API 实测对齐；标注"研究时记录"的为 2026-10-12 快照。

## 问题 1：我们项目本身的问题和可优化点

### 现有问题

#### 1.1 缺少失败反馈机制

**问题**：没有类似 LESSONS.md 的机制来记录 Agent 重复失败的模式。

- **现状**：AGENTS.md 和 agent-governance.md 写的是"应该怎么做"的规则
- **缺失**：没有记录"实际做错了什么"和"为什么错"
- **后果**：Agent 可能重复犯同样的错误，因为没有显式的失败历史可查

**magpie 的做法**：
- 每晚 review 当天所有 commits
- 提取"修复了两次以上"的问题 → LESSONS.md
- 出现 3 次 → 晋升到 code-standards.md

#### 1.2 验收标准不可执行

**问题**：agent-governance.md 说"代码即事实，运行结果是最终判断标准"，但没有具体的检查列表。

- **现状**：原则层面正确，但 Agent 不知道具体要运行什么
- **对比 magpie**：有 6 条明确的验收标准，每条都可以执行：
  1. 测试能在旧代码上失败
  2. 测试在沙盒中运行
  3. gofmt + go vet + go test
  4. GUI 双引擎测试
  5. 真实验证
  6. UI 规则

**我们缺少**：
- 知识库 Skill 的"验收清单"只有 9 个 checkbox，但没说怎么验证
- 没有自动化检查（CI）
- 没有"真实验证"的具体标准（什么算真实？）

#### 1.3 规则过早固化

**问题**：所有原则都直接写在 agentic-work-model.md 和 agent-governance.md 中。

- **现状**：架构约束"不可违反"，开发约束"不允许 mock"等绝对原则
- **风险**：可能是过早泛化，基于假设而非真实失败案例
- **magpie 的做法**：有"暂存区"（LESSONS），出现 3 次才固化

**我们需要**：
- 区分"稳定原则"和"待验证规则"
- 有临时规则的存放位置
- 有规则晋升机制

#### 1.4 文档维护负担不明确

**问题**：要求每个项目都有 AGENTS.md、HANDOFF.md、architecture/、product/、research/。

- **现状**：对小项目可能过度设计
- **缺失**：没有说明"什么规模的项目需要什么文档"
- **magpie 的做法**：
  - AGENTS.md 5004B（实测，2026-10-13）
  - LESSONS.md 约 26KB（2026-10-13 实测；研究中记录为 479 行/25KB，持续增长中）
  - code-standards.md 14238B（实测，2026-10-13）
  - 12 个 subsystems 文档（总计约 455KB，实测 2026-10-13）
  - **单日峰值 220 commits（2026-10-05，见 LESSONS.md 原文）**

#### 1.5 人的角色不够具体

**问题**：说"人确认长期结论、裁定冲突"，但没说**何时确认、如何确认、确认什么**。

- **现状**：原则正确，但操作性不强
- **magpie 的做法**：
  - **每晚 review**（明确频率）
  - **PR 验收**（pull、merge、运行检查、记录）
  - **产品决策**（scroll guard 等具体例子）
  - **规则晋升**（3 次后从 LESSONS 到 code-standards）

#### 1.6 缺少 CI 作为共同真相

**问题**：没有自动化检查作为"人和 Agent 的共同判断基准"。

- **现状**：依赖人的 review，但没有机器可验证的门禁
- **magpie 的做法**：
  - main 的 CI run 不取消（保证有绿色基线）
  - release 必须等 CI 绿色
  - PR 合并前必须有绿色 run

### 可优化点

#### 1. 建立 LESSONS 机制

**立即可做**：
```
docs/LESSONS.md  # 或 tracks/knowledge-base/LESSONS.md
```

**内容结构**：
```markdown
<!-- reviewed-through: <commit-hash> (<date>) -->

## [问题类别]

**规则**：应该怎么做
- 证据1：<commit> + <issue> + 说明
- 证据2：...
- Seen N× (<dates>)
```

**运作**：
- 定期 review（可以是每周，不必每晚）
- 记录"Agent 修复了两次以上"的问题
- 出现 3 次 → 晋升到 code-standards.md（AGENTS.md 保持入口角色不收规则——这是渐进披露的关键：入口不随规则积累膨胀）

#### 2. 明确验收标准

**为 knowledge-base Skill 补充**：

```markdown
## 验收检查

执行前说明将运行哪些检查，执行后说明结果。

1. **笔记可读性**：
   - 运行：在 Obsidian/VS Code 中打开 notes/
   - 检查：frontmatter 解析、wiki 链接可点击、图片显示
   
2. **来源可回溯**：
   - 运行：随机抽取 3 篇笔记
   - 检查：能否根据来源字段找到原始材料
   
3. **无重复污染**：
   - 运行：重复执行同一任务
   - 检查：notes/ 中是否产生重复笔记
   
4. **真实使用**：
   - 运行：让另一个 Agent 查询知识库完成任务
   - 检查：能否找到正确答案、是否误用候选内容
```

#### 3. 引入规则暂存区

**在 AGENTS.md 中区分**：

```markdown
## 架构约束（稳定，不可违反）

[现有的 5 条]

## 实验性规则（tracks/*/LESSONS.md）

以下规则在特定 track 中试行，出现 3 次验证有效后晋升：
- [规则A] - 见 tracks/knowledge-base/LESSONS.md
- [规则B] - 见 tracks/bidding/LESSONS.md
```

#### 4. 明确人的操作频率和方式

**补充到 agent-governance.md**：

```markdown
## 定期 Review

### 频率
- 日常开发：每周一次
- 关键阶段：每日一次（如新 track 启动期）

### Review 内容
1. 检查 `git log --since="1 week ago"`
2. 识别"修复了前一天/前一周问题"的 commits
3. 提取模式 → 写入 LESSONS.md
4. 评估规则晋升（出现 3 次的规则）

### PR 验收
1. `git pull origin pr/<number>`
2. `git merge main`（解决冲突）
3. 运行验收检查（见 Skill 的验收清单）
4. 在 PR 上记录：
   - 运行了什么检查
   - 在哪个 commit
   - 哪些通过、哪些未验证
5. `gh pr merge --match-head-commit <sha>`
```

#### 5. 引入 CI（可选，依项目需要）

**如果需要高频迭代**：
- 知识库：可能不需要 CI
- 投标系统：可能需要模板验证、链接检查等

**最小 CI**：
```yaml
# .github/workflows/check.yml
name: Check
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check markdown links
        run: |
          # 检查 wiki 链接、文档引用
      - name: Validate frontmatter
        run: |
          # 检查 notes/ 中的 frontmatter 格式
```

#### 6. 文档分级

**补充到 agent-governance.md**：

```markdown
## 项目规模与文档要求

### 小型（单 track，单人）
- 必需：AGENTS.md、README.md
- 可选：HANDOFF.md（无交接时可省略）
- track SKILL.md

### 中型（多 track，小团队）
- 必需：AGENTS.md、README.md、HANDOFF.md
- 推荐：LESSONS.md
- track SKILL.md + references/

### 大型（多 track，多人协作）
- 必需：全套文档
- 必需：LESSONS.md
- 推荐：CI 检查
```

---

## 问题 2：LESSONS 是否会无限膨胀

### magpie 的实际情况

**LESSONS.md 当前状态**：
- 479 行（约 25KB）
- 8 个主分类
- reviewed-through: c98160c0 (2026-10-10 13:51)

**防膨胀机制**：

#### 机制 1：规则晋升（主要机制）

```
LESSONS.md（暂存） --3次--> code-standards.md（固化）
```

**实际案例**（2026-10-07）：
- "一个修复覆盖所有兄弟情况" → 移到 code-standards.md
- "main 上红色测试是当前 bug" → 移到 code-standards.md
- "测试启动的任何东西在测试结束时终止" → 移到 code-standards.md

**效果**：规则稳定后从 LESSONS.md 删除，只保留引用。

#### 机制 2：reviewed-through 标记

```markdown
<!-- reviewed-through: c98160c0 (2026-10-10 13:51 +0800) -->
```

**含义**：
- 这个 commit 之前的问题已经 review 过
- 更早的历史可以归档
- 不需要无限保留所有历史

#### 机制 3：分类固定（8 个）

```
1. Reading the report
2. Fix the class, not the sample
3. The user's own files and settings
4. Verification
5. Concurrency and tests
6. Red tests and releases
7. Merging and closing
8. Moved to the code standards
```

**效果**：
- 不是每个问题都建新分类
- 类似问题合并到同一分类下
- 第 8 类专门存放"已晋升"的记录

#### 机制 4：证据可删除

**LESSONS.md 中的条目**：
```markdown
- 878a8489 "proved" the Trae case with an invented sample.
- 3f76105b's test used a short reason. The real one was ellipsized.
- Seen 1× (2026-10-05).
```

**特点**：
- commit hash + issue + 一句话说明
- 不保留完整代码或长篇分析
- 规则晋升后，详细证据可以归档

### 防膨胀的设计原则

1. **LESSONS 是暂存区，不是历史档案**
   - 目的：让 Agent 看到"最近反复出现"的问题
   - 不是：保存所有历史错误

2. **有出口（晋升机制）**
   - 3 次后 → code-standards.md
   - 成为规则后，LESSONS 可以删除详细证据

3. **有入口控制（只记录重复失败）**
   - 不是所有 bug 都进 LESSONS
   - 只记录"修复了两次以上"的问题

4. **有 GC（reviewed-through）**
   - 老的 commits 可以归档
   - 保留"最近几周/几个月"的即可

### 我们可以采用的防膨胀策略

```markdown
## LESSONS.md 维护规则

### 何时写入
- Agent 修复了前一周/两周内出现过的问题
- 记录规则 + 最新证据（commit + issue）

### 何时晋升
- 规则被看到 3 次 → 移到 STANDARDS.md（AGENTS.md 保持入口角色不收规则）
- 在 LESSONS.md 保留引用：
  ```
  - [规则名] → 已晋升到 standards（STANDARDS.md）
  ```

### 何时归档
- 每月/每季度更新 reviewed-through 标记
- 超过 3 个月未再出现的规则 → 移到 docs/archive/lessons-YYYY-QN.md
- LESSONS.md 只保留"最近 3 个月"的活跃规则

### 大小上限
- 目标：不超过 500 行
- 超过时：优先晋升高频规则，其次归档老规则
```

---

## 问题 3：问题如何出现、commits 是什么、Agent 如何迭代

### magpie 的实际工作流程（推测 + 证据）

#### 3.1 问题来源

**从 LESSONS.md 的证据看**：

1. **用户报告 issue**
   - #834、#792、#743 等
   - 用户描述：某功能不工作、报错、显示错误

2. **Agent 提交修复**
   - commit 4788cf2b：修复 Cursor list error
   - 但只修复了 GUI，用户用的是 TUI
   - 用户回报还是不行

3. **人工 review 发现模式**
   - 每晚 review 当天的 commits
   - 发现：同一问题修复了多次
   - 提取规则："在报告者的确切环境测试"

**问题出现 ≠ Agent 自动检索 issues**，而是：
- 用户手动提 issue
- Agent 读 issue 并修复
- 修复后用户可能回报"还是不行"
- 或者 CI 红了
- 或者另一个 Agent session 又遇到同样问题

#### 3.2 Commits 的产生过程

**从 git log 和 LESSONS.md 推测**：

```
2026-10-05: 220 commits, ~170 releases
```

**可能的工作方式**：

1. **多个 Agent sessions 并行**
   - LESSONS.md 记录："两个 sessions 同时修复一个 flake"
   - 证据：4caae1c8 和 3f4287e6 在同一分钟修复同一个测试

2. **每个 issue 一个 Agent task**
   - 用户报 #834 → Agent 修复 → commit 878a8489
   - 用户说还不行 → Agent 再修复 → commit c353f7bd
   - 最终可能修复 4 次（v0.1.920 → .925 → .931 → .938）

3. **每个修复可能包含**：
   - 代码修改
   - 新增测试
   - 验收检查
   - release（打 tag）

4. **高频 release**：
   - 每个修复都打 tag（v0.1.xxx）
   - 单日 170 releases 意味着平均每 8 分钟一个 release

#### 3.3 Agent 如何开启写代码和迭代

**推测的触发方式**：

**方式 1：Issue triage**
```
用户提 issue → 
  (可能) Agent 自动 triage 并分配 →
  Agent 读 issue + AGENTS.md + LESSONS.md →
  Agent 写代码 + 测试 →
  Agent 运行验收检查 →
  提交 PR 或直接 commit →
  (可能) 自动或人工 merge →
  打 tag → CI → release
```

**方式 2：CI 失败**
```
某个 commit 让 CI 红了 →
  Agent 被触发修复 →
  读 CI 日志 + AGENTS.md + LESSONS.md →
  修复 + 测试 →
  commit → CI 绿色
```

**方式 3：定期任务**
```
每天定时：
  review 当天 commits →
  提取重复失败模式 →
  更新 LESSONS.md
```

#### 3.4 Agent 如何发现问题

**从 LESSONS.md 看，发现问题的方式**：

1. **用户报告**
   - #823: 用户截图显示解析失败
   - Agent 第一次修复用了错误的 fixture
   - 用户回报还不行
   - Agent 才用真实的 bytes

2. **CI 红了**
   - TestCursor 在 Windows 红了 3 天
   - 但被标记为"和 main 一样"而未修复
   - 直到 #1248 才修复

3. **人工 review 发现**
   - 每晚 review 发现：同一问题修复了多次
   - 或者：多个 sessions 修复了同一个问题
   - 或者：修复后引入了新问题

4. **验收检查失败**
   - Agent 运行 `go test` 失败
   - Agent 运行 GUI 测试失败
   - Agent 在真实 vendor 测试失败

### 完整工作流推测

```
┌─────────────────────────────────────────────┐
│ 白天（7×24h Agent 运行）                      │
├─────────────────────────────────────────────┤
│                                             │
│ Issues (用户报告/CI 失败) →                   │
│   Agent 读 AGENTS.md + LESSONS.md →         │
│   Agent 写代码 + 测试 →                       │
│   Agent 运行验收 (gofmt/vet/test/真实验证) → │
│   Commit + PR (或直接 commit) →             │
│   Merge (人工或自动) →                        │
│   Tag →                                     │
│   CI run →                                  │
│   Release (如果 CI 绿)                       │
│                                             │
│ 并行：多个 Agent sessions 处理不同 issues     │
│                                             │
└─────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│ 晚上（人工 review）                           │
├─────────────────────────────────────────────┤
│                                             │
│ git log --since="1 day ago" →               │
│ 识别：重复修复、修复后回退、同时修复 →          │
│ 提取规则 →                                   │
│ 写入 LESSONS.md (附 commit + issue) →       │
│ 评估晋升（Seen 3×? → code-standards.md）    │
│                                             │
└─────────────────────────────────────────────┘
```

### 关键证据

**LESSONS.md 开头**：
> magpie's code is written, reviewed, merged and released **by agents**. Each night the day's commits are **reviewed** for what had to be fixed again, what shouldn't have merged and what was verified too thinly.

**说明**：
- 代码由 agents（复数）写
- 每晚人工 review
- review 的对象是"当天的 commits"

**LESSONS.md 中的例子**：
```
- #834 came back 4 times (v0.1.920 → .925 → .931 → .938). 
  Each round fixed only the agent in the screenshot.
```

**说明**：
- 一个 issue 修复了 4 次
- 每次都发了 release
- 最终才修对

---

## 问题 4：magpie 工程设计的优秀点和不足

### 优秀的工程设计

#### 4.1 Subsystems 设计文档体系

**创新点**：不是代码文档，而是**系统行为文档**。

**docs/subsystems/README.md**：
```
一个 subsystem 可以跨多个包或仓库。
它的 reference 描述这些部分共同提供的行为；
不需要列出每个函数。
```

**特点**：

1. **行为导向，不是实现导向**
   - 不写"有哪些类和方法"
   - 写"有哪些职责、状态转换、失败行为"

2. **链接到源码，不复制代码**
   - 引用具体的文件和符号
   - 而不是把实现细节抄到文档里

3. **PR 必须更新对应 reference**
   - 如果修改了"职责、接口、状态转换、失败行为"
   - 必须同步更新 subsystem reference

4. **Review 依赖 reference**
   ```
   1. 识别影响的 subsystem
   2. 对比 claimed behavior 和实际实现
   3. 检查 reference 是否更新
   4. 检查测试是否覆盖 claimed behavior
   ```

**启发**：
- 我们的 tracks/ 可以借鉴
- tracks/knowledge-base/references/framework.md 已经在往这个方向走
- 但需要更明确："修改 Skill 行为 → 必须更新 reference"

#### 4.2 --match-head-commit 防护

**创新点**：防止"review 期间代码变了"而静默合并。

```bash
gh pr merge --match-head-commit <reviewed sha>
```

**效果**：
- 如果 review 期间有新 push
- merge 会失败
- 必须重新 review 新的 head

**magpie 的教训**：
> #974 was merged without that. A head pushed after the review is reviewed again.

**启发**：
- 我们目前没有 PR 流程
- 但如果建立 PR 流程，这个机制很重要

#### 4.3 测试沙盒设计

**创新点**：完全隔离真实 agent 配置。

```bash
HOME=$(mktemp -d)
export GOPATH=$(go env GOPATH)
export GOMODCACHE=$(go env GOMODCACHE)
export GOCACHE=$(go env GOCACHE)

# 测试结束后
chmod -R u+w "$HOME"
rm -rf "$HOME"
```

**效果**：
- 测试不污染 ~/.claude、~/.codex 等
- 但仍然复用 Go 的 module cache（否则每次下载 1-2 GB）

**启发**：
- 知识库 Skill 测试也需要沙盒
- inbox/、notes/、archive/ 应该在 temp dir 中测试
- 而不是污染真实知识库

#### 4.4 CI 并发控制的智慧

```yaml
concurrency:
  group: test-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
```

**设计思想**：
- PR：快速迭代，新 push 取消旧 run
- main：保证基线，不取消 run（release 需要等绿色）

**教训来源**（LESSONS.md）：
> 曾因取消 main run，导致 release 无绿色 run 可等

**启发**：
- 如果我们建 CI，需要这个区分

#### 4.5 "真实验证"文化

**写进 code-standards.md**：
> A change to a provider, subscription or agent is also checked against the real thing: a real account or key, the agent's real config format, the vendor's real reply.

**强制要求**：
- PR description 必须说明"哪些真实验证过，哪些没有"
- "What wasn't tried with the real thing isn't built on and isn't told to users as working."

**LESSONS.md 强化**：
- 多次记录"因未真实验证而返工"
- 例如：84554e57 没在真实 Claude Desktop 测试，导致页面挂了 2 天

**启发**：
- 知识库 Skill 需要"真实知识库验证"
- 不能只在 mock 数据上测试

#### 4.6 规则有证据链

**LESSONS.md 的格式**：
```markdown
**规则**：应该怎么做
- 证据1：<commit hash> + <issue> + 说明
- 证据2：...
- Seen N× (<dates>)
```

**效果**：
- 每条规则都可以回溯到真实案例
- 可以验证"这条规则是否真的有用"
- 可以看到"这条规则出现了几次"

**启发**：
- 我们的 AGENTS.md 写的是抽象原则
- 缺少"这条原则从哪个真实问题来"
- 应该建立证据链

### 做得不够好的地方

#### 4.1 过度依赖人工 review

**问题**：每晚人工 review 220 commits 是巨大的工作量。

**风险**：
- 作者不可替代（单点故障）
- 无法 scale（如果团队扩大）
- 可能漏掉模式

**可能的改进**：
- 自动化提取"修复了两次的 issue"
- 自动化识别"同一文件的多次修改"
- 辅助工具：commit message 分析、issue 链接分析

#### 4.2 返工率 18% 被接受

**问题**：220 commits 中约 40 个是返工。

**分析**：
- 这是"快速失败"的代价
- 但 18% 仍然很高

**可能的改进**：
- 更严格的 PR review（在 merge 前发现问题）
- 更好的 Agent 引导（减少常见错误）
- 更多的自动化检查（CI 提前发现）

**magpie 的选择**：
- 接受返工率
- 用 LESSONS 机制从返工中学习
- 不追求一次正确

**这是权衡**：快速迭代 vs. 低返工率

#### 4.3 LESSONS.md 仍然需要人工维护

**问题**：规则晋升、分类、归档都是人工的。

**风险**：
- 人的判断可能不一致
- "Seen 3×"是手工计数
- 晋升决策没有明确标准（除了"3 次"）

**可能的改进**：
- 自动统计规则出现次数
- 自动建议"可以晋升的规则"
- 版本化 LESSONS（git blame 可以看演化）

#### 4.4 文档量大

**问题**：
- AGENTS.md 5004B（实测，2026-10-13）
- LESSONS.md 26442B（实测，2026-10-13）
- code-standards.md 14238B（实测，2026-10-13）
- subsystems/ 约 455KB（12 个文件，实测 2026-10-13）
- **总计约 500KB 文档（按 2026-10-13 实测数字重算）**

**对 Agent 的认知负担**：
- 需要读 400KB 才能开始工作
- 可能遗漏重要规则

**可能的改进**：
- 分层引导（AGENTS.md → 相关 subsystem → 相关 LESSONS）
- 根据任务类型只读相关文档
- 文档索引或摘要

#### 4.5 高频 release 的必要性存疑

**问题**：单日 170 releases 是否必要？

**分析**：
- magpie 是 Gateway，用户需要最新修复
- 但某些修复可以 batch（比如文档、测试）

**风险**：
- CI 负担
- 用户的更新疲劳
- release notes 的意义降低

**可能的改进**：
- 区分 hotfix 和 regular release
- 每天只 release 一次（把当天修复 batch）
- 只有"用户可见的修复"才 release

#### 4.6 多 Agent sessions 的协调不足

**问题**（从 LESSONS.md）：
- 两个 sessions 同时修复同一个问题
- 两个 sessions 的文件被 commit 到错误的 subject

**说明**：
- 缺少 Agent 之间的协调机制
- 没有"任务锁"或"我正在处理这个 issue"的机制

**可能的改进**：
- Agent 开始任务前检查"是否有其他 Agent 在处理"
- 在 issue 上留 comment："I'm working on this"
- 或者：只允许一个 Agent session，减少并发

### 对我们的启发总结

**应该学习的**：

1. **LESSONS 机制** - 最重要的创新
2. **Subsystems reference** - 行为导向的文档
3. **真实验证文化** - 写进标准，反复强调
4. **规则证据链** - 每条规则回溯到真实案例
5. **测试沙盒** - 完全隔离真实环境
6. **CI 并发控制** - main 不取消，PR 快速迭代

**不应该照搬的**：

1. **高频 release** - 依场景而定
2. **每晚 review** - 可以是每周，依迭代频率
3. **18% 返工率** - 可以通过更好的 PR review 降低
4. **多 Agent 并发** - 可能需要协调机制

**我们的改进路径**：

1. **立即**：建立 docs/LESSONS.md
2. **短期**：为 knowledge-base Skill 补充验收清单
3. **短期**：在 AGENTS.md 区分稳定原则和实验规则
4. **中期**：建立 CI（markdown 检查、frontmatter 验证）
5. **中期**：明确人的 review 频率和方式
6. **长期**：规则自动化（自动统计、自动建议晋升）
