# Tasks Queue

<!-- 实例化为 docs/TASKS.md：多 Agent 双环协作的调度板，状态值、提交方式与滑动窗口规则见 multi-agent-collab Skill。实例化时删除本注释与占位符。 -->

## [Task #<N>] <任务名称>

- **Status**: <pending | verified | blocked | superseded>
- **Scope**: `<允许修改的文件/模块前缀，供 Router 判断能否并行>`
- **Verified-Commit**: <sha-or-none>
- **Updated**: <YYYY-MM-DD>

### 1. 目标与边界
- **授权修改范围**：<允许 Worker 修改的文件/模块列表；完成本任务所需的同切面支撑文件 Router 可直接授权补改>
- **不在范围内**：<不在本轮范围内的冻结核心契约或用户真实数据目录>

### 2. 任务包明细
1. **<具体改动项 1>**：`<filepath>` — <明确行为契约>
2. **<具体改动项 2>**：`<filepath>` — <明确行为契约>

### 3. 验收门禁
- **Worker 交卷前置条件**：<必须跑通的全仓测试、守卫测试、手动破坏验证与构建命令；涉及 UI 时，截 1~3 张真实渲染图存入 .tmp/evidence/task-<N>/ 并亲自查看>
- **Tester 真实用户验收要求**：<Tester 如何在专用沙盒中像真实用户一样操作产品、要检查哪些排版、交互位置与文案；首轮列全问题，截图归档至 .tmp/evidence/task-<N>/；不以脚本退出码代替体验验收>
