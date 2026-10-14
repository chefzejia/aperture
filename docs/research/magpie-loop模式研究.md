# magpie 的 loop 模式与人的真实占比

> 来源：作者推文 https://x.com/yetone/status/2109855710444237018（2026-10，经 fxtwitter API 取全文与 3 张终端截图）  
> 事实核查：2026-10-14。推文原文、截图内容均已直接读取，非转述。

## 作者自述的工作流

> "其实我就是用 Claude Code，然后用官方的 Opus 5.5 模型执行 loop 就可以了。我会并行执行图里的 3 个 loop，然后每晚抽一点时间铲铲屎（主要是 UI/UX 的问题），然后就没活儿了。"

三个并行 loop（截图实证，均为 `claude --dangerously-skip-permissions` 起的常驻会话）：

1. **dev-app-loop**：开发主循环，agent 在仓库自主写代码修 bug
2. **release-magpie**：发布循环，等 CI 绿、打 tag、走 16-assets 发布流程
3. **agents-status**：状态监控循环，盯各 agent 状态

人的全部工作：每晚 review 当天 commits（"铲屎"），主要是 UI/UX 判断，并把重复失败提取成 LESSONS 规则。

## 核心认知：放权成立的前提是自动治理三件套

`--dangerously-skip-permissions`（权限全开）之所以在 magpie 成立，不是因为"敢放权"本身，而是**事前人审被三件套置换**：

1. **CI 门禁**：机器裁判。红色不许发布；`--match-head-commit` 保证合并的就是 review 过的 commit
2. **沉淀规则**：agent 每次改码前读 AGENTS.md(5KB)→LESSONS.md(26KB)→code-standards(14KB)→subsystems(455KB)，自我约束
3. **人事后介入**：每晚一次、低频高杠杆——不是逐行审 200 个 commit，而是把当天重复出现的失败提取成一条规则。人花的时间恒定，但规则产出随历史累积，系统越跑越稳

人的占比极小（~每 30 分钟一个 release，人每天只出现一次），但**规则产出是整个系统收敛的来源**——LESSONS 里每条规则都带着真实事故的 commit hash。

## 渐进披露是自治的控制平面

不同 loop 会话/不同任务深度读不同层的文档，越深越少读：

```text
AGENTS.md（5KB，入口，每个会话必读）
  → LESSONS.md（26KB，改代码前读：最近的失败模式）
  → code-standards.md（14KB，写和 review 时对照：已晋升的硬规则）
  → subsystems/（455KB，改特定子系统前读那一份）
```

并行 loop 的稳定不靠编排框架，靠：各有各的职责边界（对应 LESSONS 里"两个 session 不共享同一 checkout"的教训）+ 各自只读自己需要的文档层。

## 任务式 vs 常驻式：人机介入时机的两种模式

| | 任务式 agent | 常驻式 agent（magpie loop） |
|---|---|---|
| 生命周期 | 一次任务、交付即结束 | 7×24 循环、持续迭代 |
| 人机边界 | 高风险修改**事前**批准 | **事后**低频高杠杆介入 |
| 安全机制 | 权限收紧 + 逐项确认 | CI 门禁 + 沉淀规则 + 事后批量 review |
| 人的角色 | 验收者、决策者 | 模式提取者、价值判断者（UI/UX 等机器弱项） |
| 放权程度 | 受权限层约束 | skip-permissions，约束全在文档层 |

两模式不混用。放权的前提：三件套齐备；缺 CI 门禁的常驻 loop 是灾难，缺文档沉淀的 skip-permissions 同样是。

## 对 agentic-work-infra 的修正（已落地）

1. STANDARDS.md 新增"任务式与常驻式"一节：明确两种介入时机，常驻式的放权条件写清
2. 渐进披露写入 standards（入口→失败规则→标准→子系统参考的读取分层）
3. 补吸收 code-standards 的"变更纪律"7 条（fix 覆盖精确范围、到达所有同类位置、重推导依赖、读失败即未知 fail-closed、预览无副作用、错误分类窄化、外部系统值从其本源取）——此前只吸收了 6 条 acceptance 里的部分
4. 标注验收清单和失败测试约束的项目适用性：文档项目裁掉测试相关项，保留文档级验证（链接检查、引用一致性）
5. 复制裁剪指导进模板头部：标准重量匹配项目节奏，轻项目不全量继承

## 未吸收的（记录原因）

- `--match-head-commit` 具体命令写进标准：属于 GitHub 工作流细节，留在 standards 的合并规则一句里已够，命令级细节由项目自定
- 30 分钟发布节奏本身：是 magpie 产品形态（API gateway + CLI 工具）决定的，不是普适目标
