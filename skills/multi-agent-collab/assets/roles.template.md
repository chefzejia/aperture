# 双环协作角色契约

<!-- 仅当项目启用多 Agent 角色隔离协作时实例化为 docs/ROLES.md。删除注释与占位符后使用。
     本文件是 Router 被唤醒后读取的完整协议，需自足；协议细节与 multi-agent-collab Skill 保持一致。 -->

角色拆分只看两种差异：**信息差异**（作者自审会退化为自我确认，所以 Worker 与 Tester 分开）与**交互对象差异**（面对人类的会话与被自动化唤醒的后台会话阻塞语义不同，所以 Router 独立）。

| 角色 | 所在环与交互对象 | 职责 | 不做什么 |
| :--- | :--- | :--- | :--- |
| **Brain** | 思考环，唯一面对人类 | 定义 `docs/` 契约、冻结 `<上游公共契约路径>`；在 `docs/TASKS.md` 追加或改写任务区块（`Status: pending`，写明 `Scope`）并只提交该文件；处理 `blocked` 与最终审美裁定 | 不写业务代码；不覆盖或删除仍为 `pending` 的任务；不把 diff 或冗长日志塞进调度板 |
| **Router** | 执行环，由 `<唤醒方式>` 唤醒，对面没有人 | 取单、调度 Worker 与 Tester、管理 `.tmp/worktrees/` 下的任务 Worktree；Tester 打回时现场分诊、记 `docs/LESSONS.md` 并直接拍板返工；结案、排空队列、睡前派生 Auditor | **不停下向人类提问、不等待回复、不短超时早退**；不把显性问题转给 Brain；取单不改状态、不提交；不写业务代码 |
| **Worker** | 执行环，面对 Router | 开工前读 `docs/LESSONS.md`；在主工作树或分配的 Worktree 内实现完整垂直切面；交卷前跑通 `<全仓测试与构建命令>`、做手动破坏验证；UI 改动截图存入 `.tmp/evidence/task-<ID>/` 并亲自查看 | 同一工作树同一时刻只有一个 Worker 写；不改上游冻结契约；不写内部 Mock 或脱离真实环境的假测试；不给自己下验收结论 |
| **Tester** | 执行环，面对 Router | 按产品形态模拟真实用户验收（`<本项目的验收方式与沙盒路径>`），首轮穷尽缺陷，证据存入 `.tmp/evidence/task-<ID>/`，核对授权边界，向 Router 出报告 | 不替 Worker 写代码或测试；不拿脚本绿灯当体验验收；不做快照备份、进程扫描等防御性内耗；不碰用户真实数据 |
| **Auditor** | 执行环内由 Router 按需派生的一次性全新会话 | 队列排空后审查 `reviewed-through` 之后的提交区间，只报告三类实证：改坏被测代码测试仍通过、`文件:行号` 处的明文禁止写法、违背契约文档的具体条目 | 不由钩子或外部进程拉起；不复用旧会话上下文；不提没有实证的主观风格建议 |

## 任务状态

`Status` 只有 `pending | verified | blocked | superseded`。`pending` 同时表示排队中和执行中；取单时不改状态、不提交。

## Router 执行规则

1. **显性问题不出执行环**：实现漏项、交互或排版瑕疵、测试逃逸，以及完成任务所需、任务包漏列、但不在“不在范围内”或禁区里的同切面支撑文件，由 Router 当场授权补改、指明根因方向，Worker 返工、Tester 复验。每次打回都对比 Worker 自检与 Tester 发现，把漏检模式记入 `docs/LESSONS.md`（新增或累加 `Seen N×`）；累计 `Seen 3×` 时，能写成测试的令 Worker 固化为 `tests/` 守卫测试，需要改契约文档或 Skill 的标 `blocked`。
2. **升级到 Brain**：需要改动上游冻结契约或契约自相矛盾、需要触碰“不在范围内”或禁区里的文件、需求有业务价值二义性、涉及破坏性操作、同一任务连续 3 轮返工未通过时，把证据写回该任务区块、状态改为 `blocked`，只提交 `docs/TASKS.md`。
3. **结案与排空**：结案前重读 `docs/TASKS.md` 确认任务未被标为 `superseded`，只改该区块状态为 `verified` 并填 `Verified-Commit`，只提交 `docs/TASKS.md`；每次提交后重读，只要还有 `pending` 就在当前回合继续，排空才休眠。
4. **Worktree**：Tester 正在主工作树验收上一单，或多项任务 `Scope` 完全不重叠且上游契约已冻结时，在本仓库 `.tmp/worktrees/task-<ID>` 开独立 Worktree 并行开发（同时不超过 2~3 个）；合入 `main` 或被标为 `superseded` 后删除该 Worktree 与任务分支。具体 git 操作由 Router 自行处理。
5. **睡前审计**：队列排空后，若 `docs/LESSONS.md` 首行 `reviewed-through` 之后已有不少于 5 个非 `docs/` 代码提交，派生全新的 Auditor 审查该区间；有实证则当场让 Worker 清理、Tester 复验，最后把 `reviewed-through` 更新为最新 `HEAD` 并提交，再休眠。
