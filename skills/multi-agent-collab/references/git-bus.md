# Git 总线参考实现：`docs/TASKS.md` + `post-commit` 唤醒

本文件是 [SKILL.md](../SKILL.md) 中双环协议的一种宿主无关落地方式。角色职责、状态值、升级规则以 SKILL.md 为准，这里只描述基于 Git 的派单、唤醒与审计机制。

## 派单与唤醒

- **一个项目一个常驻 Router**：每个项目在执行环宿主中有一个归属于该项目根目录的常驻 Router 顶层会话（不是 Brain 的子代理），不跨项目复用。唤醒命令与会话标识写进该项目的 `.git/hooks/post-commit`。
- **Brain 单向异步派单**：Brain 只通过写 `docs/TASKS.md` 并执行 `git commit --only docs/TASKS.md` 派单，提交后立即回到人类对话，不阻塞等待执行环。
- **边沿触发**：钩子只检查本次提交的 diff 是否新增了 `Status: pending` 行，而不是检查文件里是否还残留 `pending`。Router 结案提交（`pending` 改为 `verified` 或 `blocked`）不会新增 `pending` 行，因此不会把自己再次唤醒。
- **钩子只做唤醒**：不在钩子里启动其他后台进程或加锁脚本，审计等工作由 Router 在自己的回合内完成。

## 睡前审计（Auditor）

Router 排空全部 `pending` 任务、准备休眠前：

1. 用 `git rev-list --count <reviewed-through>..HEAD -- . ":!docs/"` 计算 `docs/LESSONS.md` 首行 `reviewed-through` 之后的非文档代码提交数；
2. 若不少于 5 个，用宿主的子代理能力派生一个全新的、不复用 Worker 与 Tester 上下文的 Auditor，按 SKILL.md 的三类实证审查该区间；
3. 有实证问题时，在当前回合调度 Worker 清理、Tester 复验；最后把 `reviewed-through` 更新为最新 `HEAD` 并提交，再休眠。

## 钩子模板

把 `<wake-project-router-command>` 换成执行环宿主的唤醒命令；如需补充 `PATH`，按本机安装位置填写。

```bash
#!/usr/bin/env bash
# 仅当本次提交在 docs/TASKS.md 的 diff 中新增了 Status: pending 行时，唤醒本项目的常驻 Router
if git diff-tree --no-commit-id -p HEAD --root -- docs/TASKS.md 2>/dev/null | grep -qE "^\+(- \*\*Status\*\*|Status): pending(\s|$)"; then
  <wake-project-router-command> "[AUTO-WAKEUP] 你是本项目的无人值守 Router，对面没有人在看，不要停下提问。请先读 docs/ROLES.md，再按其中的协议执行 docs/TASKS.md 中所有 Status: pending 的任务。" 2>>.git/router-wakeup.err || echo "[post-commit] wake-router failed, see .git/router-wakeup.err" >&2
fi
```
