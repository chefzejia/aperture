# Git 总线参考实现：`docs/TASKS.md` + `post-commit` 唤醒

本文件是 [SKILL.md](../SKILL.md) 中双环协议的一种宿主无关落地方式。角色职责、状态值、升级规则以 SKILL.md 为准，这里只描述基于 Git 的派单、唤醒与审计机制。

## 派单与唤醒

- **一个项目一个常驻 Router**：每个项目在执行环宿主中有一个归属于该项目根目录的常驻 Router 顶层会话（不是 Brain 的子代理），不跨项目复用。唤醒命令与会话标识写进该项目的 `.git/hooks/post-commit`。
- **Brain 单向异步派单**：Brain 派单或标废时只提交 `docs/TASKS.md`（`git commit --only docs/TASKS.md`），更新其他契约或台账文档时同样用 `--only` 显式列出目标文件并及时提交，提交后立即回到人类对话，不阻塞等待执行环。
- **主工作树限定与边沿触发**：Git 的 `.git/hooks/post-commit` 被主工作树和所有 `.tmp/worktrees/*` 共享；钩子首先检查是否位于主工作树，跳过 linked worktree 中的提交（避免 Worker 合并 `main` 时误触发，同时避免 Worktree 内 `.git` 为文件导致日志路径报错）。在主工作树中满足其一才唤醒：本次提交的 diff 新增了 `Status: pending` 行；或者有里程碑新变为 `pending`。第二条是兜底：整块挪动或改写区块时，diff 可能把 `pending` 行当成上下文，所以钩子再比较前后两个版本里 `pending` 里程碑的编号。钩子不检查文件里是否还残留 `pending`；Router 的结案提交只把 `pending` 改成别的状态，两条都不满足，不会把自己再次唤醒。
- **唤醒消息只指路**：消息只要求重读 `docs/ROLES.md`，再按它执行前置已满足的 `pending` 里程碑，不复述协议细节。协议改动只改 `docs/ROLES.md`，不用动钩子；Router 每次取单前也会重读它。
- **钩子只做唤醒**：不在钩子里启动其他后台进程或加锁脚本，审计等工作由 Router 在自己的回合内完成。

## 睡前审计（Auditor）

Router 执行完所有前置已满足的 `pending` 里程碑、准备休眠前：

1. 用 `git log --oneline <reviewed-through>..HEAD -- docs/TASKS.md` 查看 `docs/LESSONS.md` 首行 `reviewed-through` 之后的调度提交（若 `docs/LESSONS.md` 尚未建立，则自首个里程碑提交起算，并在本轮审计后创建该文件），数出已结案（`verified`）的里程碑数，并确认其间是否有验收栏写“无”、跳过了 Tester 的里程碑；
2. 若已结案不少于 2 个里程碑（项目可在 `docs/ROLES.md` 中调整），或有里程碑跳过了 Tester，用宿主的子代理能力派生一个全新的、不复用 Worker 与 Tester 上下文的 Auditor，按 SKILL.md 的三类实证审查该区间；
3. 有实证问题时，在当前回合派生新的 Worker 清理，并按 SKILL.md 的验收规则决定是否派 Tester 复验；最后把 `reviewed-through` 更新为最新 `HEAD` 并提交（只含 `docs/LESSONS.md`），提交后再重读一次 `docs/TASKS.md`，确认审计期间没有新进且前置已满足的 `pending` 里程碑后才休眠。

## 钩子模板

把 `<wake-project-router-command>` 换成执行环宿主的唤醒命令，`<project>` 换成项目名；如需补充 `PATH`，按本机安装位置填写。

```bash
#!/usr/bin/env bash
# 仅在主工作树触发（linked worktree 共享 hooks 目录，避免在 Worktree 内合并 main 时误唤醒）：
GIT_DIR="$(git rev-parse --git-dir 2>/dev/null)" || exit 0
COMMON_DIR="$(git rev-parse --git-common-dir 2>/dev/null)" || exit 0
if [ "$(cd "$GIT_DIR" && pwd -P)" != "$(cd "$COMMON_DIR" && pwd -P)" ]; then
  exit 0
fi

# 满足其一即唤醒本项目的常驻 Router：
# 1. 本次提交在 docs/TASKS.md 的 diff 中新增了 Status: pending 行；
# 2. 有里程碑新变为 pending（整块挪动或改写时，diff 可能把 pending 行当成上下文）。
# Router 的结案提交只把 pending 改成别的状态，两条都不满足，不会自激。
pending_ids() {
  git show "$1:docs/TASKS.md" 2>/dev/null \
    | awk '/^## \[Milestone #/{id=$0; sub(/^## \[Milestone #/, "", id); sub(/\].*/, "", id)} /^(- \*\*Status\*\*|Status): pending([[:space:]]|$)/{if (id != "") print id}' \
    | LC_ALL=C sort -u
}
NEW_PENDING="$(LC_ALL=C comm -13 <(pending_ids HEAD~1) <(pending_ids HEAD))"

if git diff-tree --no-commit-id -p HEAD --root -- docs/TASKS.md 2>/dev/null | grep -qE "^\+(- \*\*Status\*\*|Status): pending([[:space:]]|$)" || [ -n "$NEW_PENDING" ]; then
  <wake-project-router-command> "[AUTO-WAKEUP] 你是 <project> 的无人值守 Router，对面没有人在看，不要停下提问或等待回复。先重读 docs/ROLES.md，以文件里的协议为准，不沿用会话里记住的旧规则；再按它执行 docs/TASKS.md 中前置已满足的 pending 里程碑，排空后才休眠。" 2>>"$COMMON_DIR/router-wakeup.err" || echo "[post-commit] wake-router failed, see $COMMON_DIR/router-wakeup.err" >&2
fi
```
