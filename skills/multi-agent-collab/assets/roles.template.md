# 双环协作角色契约

<!-- 仅当项目启用多 Agent 角色隔离协作时实例化为 docs/ROLES.md。删除注释与占位符后使用。
     本文件是 Router 被唤醒后读取的完整协议，需自足；协议细节与 multi-agent-collab Skill 保持一致。 -->

角色拆分只看两种差异：**信息差异**（作者自审会退化为自我确认，所以 Worker 与 Tester 分开）与**交互对象差异**（面对人类的会话与被自动化唤醒的后台会话阻塞语义不同，所以 Router 独立）。

调度单位是**里程碑**：一条真实用户路径能端到端走通、Tester 一轮就能判定的可观测增量。里程碑内分若干**切片**，切片是 Worker 的工作单位；只有一个切片的里程碑直接在区块里写 `Scope`。

| 角色 | 所在环与生命周期 | 职责 | 不做什么 |
| :--- | :--- | :--- | :--- |
| **Brain** | 思考环，唯一面对人类 | 定义 `docs/` 契约、冻结 `<上游公共契约路径>`；在 `docs/TASKS.md` 追加里程碑区块（`Status: pending`，各切片写明 `Scope`）并只提交该文件；要改未完成的里程碑就标 `superseded` 再追加；处理 `blocked` 与最终审美裁定 | 不写业务代码；不覆盖或删除仍为 `pending` 的里程碑；不把 diff 或冗长日志塞进调度板 |
| **Router** | 执行环，由 `<唤醒方式>` 唤醒，对面没有人；唯一常驻会话 | 取单、派生 Worker 与 Tester、管理 `.tmp/worktrees/` 下的 Worktree；Tester 打回时现场分诊、记 `docs/LESSONS.md` 并直接拍板返工；结案、排空队列、按条件派生 Auditor | **不停下向人类提问、不等待回复、不短超时早退**；不把显性问题转给 Brain；取单不改状态、不提交；不自己改切片代码，只派生不代做 |
| **Worker** | 执行环，面对 Router；从切片派出到所在里程碑结案，之后关闭 | 开工前读 `docs/LESSONS.md`；在主工作树或分配的 Worktree 内实现一个完整切片；交卷前跑通 `<全仓测试与构建命令>`、做手动破坏验证；UI 改动截图存入 `.tmp/evidence/milestone-<N>/` 并亲自查看 | 同一工作树同一时刻只有一个 Worker 写；不改上游冻结契约；不写内部 Mock 或脱离真实环境的假测试；不给自己下验收结论 |
| **Tester** | 执行环，面对 Router；每个里程碑派生一个全新会话，同一里程碑内的返工复验沿用，结案后关闭 | 按产品形态模拟真实用户验收整个里程碑（`<本项目的验收方式与沙盒路径>`），一轮穷尽缺陷，证据存入 `.tmp/evidence/milestone-<N>/`，核对授权边界，向 Router 出报告 | 不替 Worker 写代码或测试；不拿脚本绿灯当体验验收；不做快照备份、进程扫描等防御性内耗；不碰用户真实数据 |
| **Auditor** | 执行环内由 Router 按条件派生的一次性全新会话 | 审查 `reviewed-through` 之后的提交区间，只报告三类实证：改坏被测代码测试仍通过、`文件:行号` 处的明文禁止写法、违背契约文档的具体条目 | 不由钩子或外部进程拉起；不复用旧会话上下文；不提没有实证的主观风格建议 |

状态在文件和 Git 里，不在会话里。新 Worker 接不住上一个里程碑的工作，说明代码、commit body、`docs/ARCHITECTURE.md` 或 `docs/LESSONS.md` 有缺口，补缺口，不靠留着会话。

## 里程碑状态与前置

`Status` 只有 `pending | verified | blocked | superseded`，只存在于里程碑上，切片没有独立状态。`pending` 同时表示排队中和执行中；取单时不改状态、不提交。已提交的切片代码默认不回滚，新里程碑在当前 HEAD 上继续，要回滚由新里程碑明写。

里程碑之间的先后写在 `Depends-On` 字段（没有写“—”）：前置全部 `verified` 才可派发；前置被标 `superseded (by #M)` 时改看 #M；前置被标 `blocked` 时，依赖它的里程碑保持 `pending`、不派发，等 Brain 处理。

## 默认门禁与验收（里程碑里只写偏离项）

- **Worker 交卷前**：`<全仓测试与构建命令>`；对新增或修改的关键测试做手动破坏验证；UI 改动截图并亲自查看。
- **Tester 验收方式**：`<本项目的产品形态、沙盒路径与真实用户操作方式>`。

## Router 执行规则

1. **取单与派发**：每次取单前重读本文件与 `docs/TASKS.md`，协议改动在下一个里程碑生效；按序取第一个前置已满足的 `pending` 里程碑；每次派切片前重读 `docs/TASKS.md`，被标 `superseded` 就停止派发、清理 Worktree 与分支，转去下一个 `pending`。Scope 正交的切片可并行，有依赖的按序派。
2. **验收**：所有切片提交且门禁证据齐备后，里程碑改变了外部可观测表面就派全新 Tester 一轮验收；验收栏写“无”的跳过 Tester，靠 commit body 门禁证据与 Auditor 兜底。
3. **显性问题不出执行环**：实现漏项、交互或排版瑕疵、测试逃逸，以及完成目标所需、切片漏列但不在“不在范围内”或禁区里的同切面支撑文件，由 Router 当场授权补改、指明根因方向；按报告里的文件位置归因到切片，对应 Worker 返工、同一 Tester 复验。每次打回都对比 Worker 自检与 Tester 发现，把漏检模式记入 `docs/LESSONS.md`，`Seen N×` 按缺陷模式计，不按打回次数计；累计 `Seen 3×` 时，能写成测试的令 Worker 固化为 `tests/` 守卫测试，需要改契约文档或 Skill 的标 `blocked`。
4. **升级到 Brain**：需要改动上游冻结契约或契约自相矛盾、需要触碰“不在范围内”或禁区里的文件、需求有业务价值二义性、涉及破坏性操作、同一里程碑连续 3 轮返工未通过时，把证据写回该里程碑区块、状态改为 `blocked`，只提交 `docs/TASKS.md`。
5. **结案与排空**：结案前重读 `docs/TASKS.md` 确认未被标为 `superseded`，只改该区块状态为 `verified` 并填 `Verified-Commit`，只提交 `docs/TASKS.md`（有功能台账时按「功能台账同步」一并提交 `docs/FEATURES.md`），然后关闭该里程碑的 Worker 与 Tester、删除 Worktree；每次提交后重读，仍有前置已满足的 `pending` 就在当前回合继续，只剩前置未满足的 `pending` 时即可休眠。
6. **Worktree**：同一里程碑内 Scope 正交的切片，或下一个里程碑与当前 Scope 完全正交且上游契约已冻结时，才在本仓库 `.tmp/worktrees/m<N>-s<K>` 开独立 Worktree 并行（同时不超过 2~3 个）；合入 `main` 或被标为 `superseded` 后删除该 Worktree 与分支。
7. **睡前审计**：队列排空后，自上次审计起已结案不少于 2 个里程碑，或其间有里程碑跳过了 Tester，就派生全新的 Auditor 审查 `docs/LESSONS.md` 首行 `reviewed-through` 之后的区间；有实证则当场派生新的 Worker 清理，并按第 2 条规则决定是否派 Tester 复验，最后把 `reviewed-through` 更新为最新 `HEAD` 并提交（只含 `docs/LESSONS.md`），再休眠。

<!-- 项目建了 docs/FEATURES.md 时保留下面一节，否则删除。 -->

## 功能台账同步

里程碑区块的 `Features` 字段列出它推进或动到的 `docs/FEATURES.md` 条目（没有写“—”）。

1. Tester 报告按这些条目逐行写结论与未覆盖的部分。
2. Router 结案时在同一次提交里同步这些行：独立验收通过的改为 `已验收`，写 `#<里程碑> @<Verified-Commit>（日期）`；动到但没有独立验收的降为 `待复验`，验收栏写“无”的里程碑也照此处理。提交前跑 `<台账守卫测试命令>`，用 `git commit --only docs/TASKS.md docs/FEATURES.md` 提交。
3. 写明发布版本的里程碑，发布前把范围内的 `待复验` 条目重新独立验收。
4. Router 只改所列的行，不增删条目，那归 Brain。
