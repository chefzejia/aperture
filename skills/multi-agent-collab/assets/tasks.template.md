# Tasks Queue

<!-- 实例化为 docs/TASKS.md：双环协作的调度板，状态值、提交方式与滑动窗口规则见 multi-agent-collab Skill。默认的工程门禁与验收方式写在 docs/ROLES.md，里程碑里只写偏离默认的项。实例化时删除本注释与占位符。 -->

## [Milestone #<N>] <用户能做到什么>

- **Status**: <pending | verified | blocked | superseded>
- **Verified-Commit**: <sha-or-none>
- **用户可观测目标**：<这个里程碑完成后，用户能端到端做到什么>
- **Tester 验收**：<一条真实用户路径与检查点，一轮跑完；没有外部可观测变化时写“无”>
- **不在范围内**：<冻结的核心契约、用户真实数据目录、本轮不做的功能>

### 切片

1. **S1** `Scope: <路径前缀>`：<行为契约；完成本切片所需的同切面支撑文件 Router 可直接授权补改>
2. **S2** `Scope: <路径前缀>`：<行为契约；与 S1 的 Scope 正交才单独成片>
3. **S3**（依赖 S1）`Scope: <路径前缀>`：<行为契约；有串行依赖或 Scope 重叠的并入同一切片>
