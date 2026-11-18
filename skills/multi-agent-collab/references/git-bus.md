# Git 总线参考实现：`docs/TASKS.md` + `post-commit` 唤醒

本文件是 [SKILL.md](../SKILL.md) 中双环协议的一种宿主无关落地方式。角色职责、状态值、升级规则以 SKILL.md 为准，这里只描述基于 Git 的派单、唤醒与审计机制。

## 派单与唤醒

- **一个项目一个常驻 Router**：每个项目在执行环宿主中有一个归属于该项目根目录的常驻 Router 顶层会话（不是 Brain 的子代理），不跨项目复用。唤醒命令与会话标识写进该项目的 `.git/hooks/post-commit`。
- **Brain 单向异步派单**：Brain 只通过写 `docs/TASKS.md` 并执行 `git commit --only docs/TASKS.md` 派单，提交后立即回到人类对话，不阻塞等待执行环。
- **边沿触发**：满足其一才唤醒：本次提交的 diff 新增了 `Status: pending` 行；或者有里程碑新变为 `pending`。第二条是兜底：整块挪动或改写区块时，diff 可能把 `pending` 行当成上下文，所以钩子再比较前后两个版本里 `pending` 里程碑的编号。钩子不检查文件里是否还残留 `pending`；Router 的结案提交只把 `pending` 改成别的状态，两条都不满足，不会把自己再次唤醒。
- **唤醒消息只指路**：消息只要求重读 `docs/ROLES.md`，再按它执行前置已满足的 `pending` 里程碑，不复述协议细节。协议改动只改 `docs/ROLES.md`，不用动钩子；Router 每次取单前也会重读它。
- **钩子只做唤醒**：不在钩子里启动其他后台进程或加锁脚本，审计等工作由 Router 在自己的回合内完成。

## 睡前审计（Auditor）

Router 执行完所有前置已满足的 `pending` 里程碑、准备休眠前：

1. 用 `git log --oneline <reviewed-through>..HEAD -- docs/TASKS.md` 查看 `docs/LESSONS.md` 首行 `reviewed-through` 之后的调度提交，数出已结案（`verified`）的里程碑数，并确认其间是否有验收栏写“无”、跳过了 Tester 的里程碑；
2. 若已结案不少于 2 个里程碑（项目可在 `docs/ROLES.md` 中调整），或有里程碑跳过了 Tester，用宿主的子代理能力派生一个全新的、不复用 Worker 与 Tester 上下文的 Auditor，按 SKILL.md 的三类实证审查该区间；
3. 有实证问题时，在当前回合派生新的 Worker 清理，并按 SKILL.md 的验收规则决定是否派 Tester 复验；最后把 `reviewed-through` 更新为最新 `HEAD` 并提交，再休眠。

## 钩子模板

把 `<wake-project-router-command>` 换成执行环宿主的唤醒命令，`<project>` 换成项目名；如需补充 `PATH`，按本机安装位置填写。

```bash
#!/usr/bin/env bash
# 满足其一即唤醒本项目的常驻 Router：
# 1. 本次提交在 docs/TASKS.md 的 diff 中新增了 Status: pending 行；
# 2. 有里程碑新变为 pending（整块挪动或改写时，diff 可能把 pending 行当成上下文）。
# Router 的结案提交只把 pending 改成别的状态，两条都不满足，不会自激。
pending_ids() {
  git show "$1:docs/TASKS.md" 2>/dev/null | awk '/^## \[Milestone #/{id=$0; sub(/^## \[Milestone #/, "", id); sub(/\].*/, "", id)} /^- \*\*Status\*\*: pending/{print id}' | sort -u
}
NEW_PENDING=$(comm -13 <(pending_ids HEAD~1) <(pending_ids HEAD))

if git diff-tree --no-commit-id -p HEAD --root -- docs/TASKS.md 2>/dev/null | grep -qE "^\+(- \*\*Status\*\*|Status): pending(\s|$)" || [ -n "$NEW_PENDING" ]; then
  <wake-project-router-command> "[AUTO-WAKEUP] 你是 <project> 的无人值守 Router，对面没有人在看，不要停下提问或等待回复。先重读 docs/ROLES.md，以文件里的协议为准，不沿用会话里记住的旧规则；再按它执行 docs/TASKS.md 中前置已满足的 pending 里程碑，排空后才休眠。" 2>>.git/router-wakeup.err || echo "[post-commit] wake-router failed, see .git/router-wakeup.err" >&2
fi
```
