# magpie 项目人机协同研究

> 研究时间：2026-10-12；事实核查：2026-10-13（GitHub API 复核）
> 项目来源：https://github.com/yetone/magpie
> 本地路径：`thirdparty/magpie/`（2026-10-14 已恢复：经 codeload 下载主分支快照，目录已加入 .gitignore。历史注记：曾被误提交为 gitlink、后在 feb057c 删除，本地目录也随之丢失）

## 研究目的

magpie 作者已经打造了一套 7×24h 持续迭代的 Agent workflow。本研究旨在理解：
1. 作者如何做人机协同
2. 如何达到平衡状态
3. 如何同时把控项目质量和工程质量

## 项目背景

**magpie 是什么**：一个 API Gateway，聚合多个 AI 提供商（Claude、ChatGPT、Gemini 等），为 Codex、Claude Desktop 等 AI 编辑器提供统一接口。

**规模**：
- 2026-10-05 单日：220 commits，约 170 个 release
- 2026-10-08 单日：192 commits，18 个 release
- 每个 release 都等待 CI 绿色后才打 tag
- Go 语言项目，有 GUI（WebKit/Chromium）和 CLI

## magpie 的人机协同模型

### 1. 明确的协同边界

**AGENTS.md（5004 字节）**：
- 简洁定位："Notes for coding agents"
- 列出必读文档：subsystem design、code standards、contributors、LESSONS.md
- 明确内建订阅的迁移规则和代码位置
- 区分"已迁移"和"未迁移"用户的代码路径

**CLAUDE.md（23 字节）**：
```
@AGENTS.md
@LESSONS.md
```

极简引用设计，Agent 被引导到两个核心文档。

### 2. 核心协同文档：LESSONS.md

**这是人机协同的关键创新**。LESSONS.md 记录：
- **每晚 review 当天所有 commits**
- **提取当天修复过两次以上的问题**
- **转化为规则，附带证据和 issue 编号**
- **规则被看到 3 次以上，晋升到 code-standards.md**

示例结构：
```markdown
## 标题（问题类别）

**规则**：一句话说应该怎么做
- 证据1：commit hash + issue + 说明
- 证据2：...
- Seen 2×（2026-10-06, 2026-10-10）
```

**关键观察**：
- 2026-10-05：220 commits，约 40 个修复当天或前一天的 bug
- 大部分修复不需要第二次尝试
- 需要第二次的，落入 LESSONS.md 的模式

### 3. 严格的验证标准（code-standards.md）

**PR 合并前必须满足**：
1. **有测试能在旧代码上失败**（真正的 FAIL，不是编译错误）
2. **测试在沙盒中运行**（临时 HOME + pinned Go caches）
3. **完整构建和测试套件**：gofmt、go vet（跨平台）、go test
4. **GUI 测试双引擎**：Chromium + WebKit，中英日德繁多语言
5. **真实验证**：在真实账号/真实 vendor 上测试
6. **UI 规则**：所有字符串通过 t() 翻译、不用原生 select、点击不滚动

**PR review 后才能合并**：
```bash
gh pr merge --match-head-commit <reviewed sha>
```
如果 review 期间有新 push，阻止合并，必须重新 review。

### 4. 高频发布机制

**release.yml workflow**：
- 推送 `v*` tag 触发
- 交给独立仓库 `yetone/magpie-releases` 构建、签名、公证
- 等待 16 个 assets 全部上传完成
- 镜像回主仓库

**release 标准**：
- CI Test run 在 tagged commit 上绿色
- tag 在 main 分支上
- 16 个 assets 全部存在
- 标记为 Latest

### 5. test.yml 的并发控制

**关键设计**：
```yaml
concurrency:
  group: test-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
```

**含义**：
- PR 的新 push 取消旧 run（快速迭代）
- **main 的 run 不取消**（保证 release 有绿色基线）
- LESSONS.md 记录：曾因取消 main run，导致 release 无绿色 run 可等

### 6. 多平台验证

**测试矩阵**：
- ubuntu-latest、macos-latest、windows-latest
- Linux 运行完整测试套件
- macOS 运行完整测试套件
- **Windows 只编译全部测试**，运行隔离的原生检查

**原因**（来自 LESSONS.md）：
- Windows CI 只编译测试，跨平台构建不编译 `_test.go`
- 所以加了 `go vet` 对 Linux 和 Windows

### 7. 迭代反馈循环

```
当天 commits → 当晚 review →
  提取重复失败 → 写入 LESSONS.md →
  被看到 3 次 → 晋升到 code-standards.md →
  PR reviewer 检查 code-standards
```

**2026-10-07 晋升的规则**：
- "一个修复覆盖所有兄弟情况"
- "一个修改重新推导基于它构建的所有东西"
- "main 上红色测试是当前 bug"
- "合并记录在 reviewed head 运行了什么"

**2026-10-08 晋升的规则**：
- "在基础之上构建之前先真实使用"
- "GUI 测试在两个引擎和每种语言中运行"

**2026-10-11 晋升的规则**：
- "测试启动的任何东西在测试结束时终止"
- "时间测试在两侧留有余地"

## 人机协同的平衡点

### 人的角色

1. **每晚 review**：人工 review 当天所有提交，提取模式
2. **规则晋升决策**：哪些规则从 LESSONS 晋升到 code-standards
3. **产品决策**：scroll guard、button cursor 等产品决策是 maintainer 的
4. **PR 最终把关**：
   - pull、merge 到 main、运行验收检查
   - 在 PR 上记录运行了什么、在哪个 commit
   - 用 `--match-head-commit` 合并，防止静默合并未 review 的代码

### Agent 的角色

1. **写代码**：大部分代码由 Agent 编写
2. **写测试**：每个修复都有测试
3. **执行验收**：运行 gofmt、go vet、go test、GUI 测试
4. **遵守规则**：AGENTS.md 引导 Agent 读 LESSONS.md 和 code-standards.md

### 平衡机制

**反馈速度**：
- 单日 220 commits 意味着平均每 7 分钟一个 commit
- 约 40 个修复当天 bug 意味着 18% 的返工率
- **这个返工率被接受**，因为有机制从中学习

**规则累积**：
- LESSONS.md 作为"暂存区"
- 被看到 3 次才固化为 code-standards
- 避免过早泛化

**真实验证强制**：
- 要求在真实 vendor、真实账号上测试
- GUI 测试要求两个引擎、多语言
- 防止 mock 和假设

## 质量把控机制

### 项目质量

1. **subsystems 设计文档**：
   - 12 个子系统文档（2026-10-13 实测，总计约 455KB；研究时为 14 个/350KB，仓库持续演化中）
   - agent-wiring、gateway-routing、provider-plugins 等
   - 修改子系统前必须读设计文档

2. **reference.md**：API 参考文档（研究中记录为 139KB，未在核查中确认当前大小）

3. **contributors.md**：什么情况下关闭 PR、哪些作者的 PR 直接关闭

### 工程质量

1. **自动化门禁**：
   - gofmt -l（输出为空才通过）
   - go vet 跨平台
   - go test 全套件
   - GUI 测试双引擎

2. **真实场景验证**：
   - "在真实账号上测试"被反复强调
   - LESSONS.md 记录多次因未在真实环境验证而返工

3. **并发和竞态检测**：
   - `go test -race` 专门运行
   - gateway 套件拆分到多个进程并行（无法用 t.Parallel）
   - 账号使用测试单独跑 race 检测

4. **测试沙盒**：
   - 临时 HOME + pinned GOPATH/GOMODCACHE/GOCACHE
   - 防止测试污染真实 agent 配置
   - 测试结束后 `chmod -R u+w "$h"; rm -rf "$h"`

## 与本项目的对比

### 相似之处

| 维度 | magpie | agentic-work-infra |
|------|--------|-------------------|
| 核心原则 | AGENTS.md + LESSONS.md + code-standards.md | 人机协同模型 + Agent 治理规范 |
| 文档分层 | subsystems/ + AGENTS.md + LESSONS.md | docs/core/ + docs/governance/ + tracks/ |
| 共同可观测 | 代码 + 文档 + LESSONS.md（显式问题） | 工作状态 + Markdown + 显式不确定 |
| 迭代反馈 | 每晚 review → LESSONS → code-standards | 真实任务 → Skill 迭代 |

### 关键差异

| 维度 | magpie | agentic-work-infra |
|------|--------|-------------------|
| **应用场景** | 软件开发（高频 commit/release） | 知识整理、投标等真实工作 |
| **反馈周期** | 每日（220 commits/day） | 未明确，依赖任务频率 |
| **质量验证** | CI + 真实 vendor 验证 + GUI 双引擎 | "代码即事实，运行结果是最终判断" |
| **Agent 边界** | AGENTS.md 引导，LESSONS.md 约束 | AGENTS.md + 授权边界 + 停止规则 |
| **失败处理** | LESSONS.md 记录 + 规则晋升 | Skill 的失败安全 + 停止规则 |
| **长期积累** | LESSONS → code-standards（3 次后晋升） | 原则稳定，Skill 从真实任务迭代 |
| **人的介入** | 每晚 review + PR 验收 + 产品决策 | 确认长期结论 + 裁定冲突 + 高风险批准 |

### 核心洞察

**magpie 的创新在于 LESSONS.md**：
- 它是**可观测的失败历史**
- 它是**Agent 和人之间的共同学习日志**
- 它有**明确的晋升机制**（3 次 → code-standards）
- 它**附带证据**（commit hash + issue number）

**这解决了 Agent 协同的核心问题**：
1. **如何让 Agent 从错误中学习**：LESSONS.md 作为显式记忆
2. **如何避免过早泛化**：暂存在 LESSONS，3 次后才固化
3. **如何保持规则可验证**：每条规则附带真实案例
4. **如何让规则不腐化**：定期 review（每晚）+ 证据链

## magpie 的人机协同为什么有效

### 1. 高频迭代 + 快速失败

- 220 commits/day，18% 返工率
- **不追求一次正确**，而是快速暴露问题
- CI 保证每个 release 都是绿色的

### 2. 显式的失败记录

- LESSONS.md 不是"bug tracker"，而是"失败模式库"
- 每条规则有：描述 + 证据 + 出现次数
- Agent 每次修改前读 LESSONS.md

### 3. 规则的生命周期

```
发现问题 → LESSONS.md（暂存） →
  被看到 3 次 → code-standards.md（固化） →
  PR reviewer 检查 → Agent 遵守
```

**关键**：有"暂存区"，避免一次失败就立规矩

### 4. 真实验证强制

- "在真实 vendor 上测试"被写进 code-standards
- LESSONS.md 记录多次因未真实验证而返工
- **Agent 被训练为"必须说明哪些真实验证过，哪些没有"**

### 5. 人在关键节点把关

- **每晚 review**：人提取模式
- **PR 合并**：人运行验收、记录、用 --match-head-commit 合并
- **产品决策**：scroll guard 等由 maintainer 决定

### 6. CI 作为共同真相

- main 的 CI run 不取消（保证有绿色基线）
- release 必须等 CI 绿色
- 跨平台验证（Linux、macOS、Windows）

## 可借鉴的实践

### 对本项目的启发

1. **建立 LESSONS 机制**：
   - 创建 `docs/LESSONS.md` 或 `tracks/*/LESSONS.md`
   - 记录 Agent 重复失败的模式
   - 附带证据（commit、issue、时间）
   - 出现 3 次后晋升到 code-standards.md（我们的对应物：STANDARDS.md；AGENTS.md 保持入口角色不收规则）

2. **明确验收标准**：
   - code-standards.md 的 6 条验收标准可以借鉴
   - "代码即事实"需要具体化为可执行的检查

3. **规则晋升机制**：
   - 不是所有原则都一开始就固化
   - 有"暂存区"（LESSONS）
   - 有"晋升条件"（3 次）

4. **Agent 引导设计**：
   - CLAUDE.md 只有两行引用
   - AGENTS.md 简洁但完整
   - 分层文档（AGENTS → LESSONS → code-standards → subsystems）

5. **真实验证文化**：
   - "在真实环境测试"写进标准
   - PR description 说明"哪些真实验证过，哪些没有"
   - LESSONS.md 强化这个习惯

### 不适合直接照搬的

1. **高频发布**：magpie 是 API Gateway，每日 170 release 合理；知识库项目可能不需要
2. **GUI 双引擎测试**：特定于有 GUI 的项目
3. **跨平台编译**：Go 项目特有

## 总结

magpie 作者通过以下方式达到人机协同平衡：

**机制设计**：
- LESSONS.md 作为共同学习日志
- 规则晋升机制（3 次后固化）
- 严格的验收标准（6 条）
- CI 作为共同真相源

**人的角色**：
- 每晚 review 提取模式
- PR 验收和记录
- 产品决策
- 规则晋升决策

**Agent 的角色**：
- 写代码和测试
- 遵守 LESSONS 和 code-standards
- 执行验收检查
- 在 PR 中说明验证情况

**质量把控**：
- 项目质量：subsystems 设计文档
- 工程质量：CI + 真实验证 + 沙盒测试
- 接受 18% 返工率，但从中学习

**核心洞察**：
> LESSONS.md 是 magpie 人机协同的关键创新。它是可观测的失败历史，是 Agent 和人之间的共同学习日志，有明确的晋升机制和证据链。

这套机制让 Agent 能够 7×24h 迭代，同时保持项目和工程质量。
