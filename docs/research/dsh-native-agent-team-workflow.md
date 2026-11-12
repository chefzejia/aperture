# 多 Agent 协同工作流设计：基于 `TASKS.md + Git Hook + 多 Worktree 流水线` 的双环四重身份闭环

> **事实核查时间**：2026-11-06（基于本地常驻会话 JSONL 运行日志、SQLite 账单审计，以及 DeepSeek `dsh-superagent-prototype`、yetone `magpie`、Orca、Herdr 横向对比）

---

## 一、 核心命题：当算力无限而人的注意力锁死在 3~5 个会话，普通开发者如何破局？

在 Agent 时代，模型的编码与工具执行算力几乎可以无限横向扩展，但**人类的注意力带宽存在硬物理上限（同时跟进超过 3~5 个活跃 Session 即迅速衰减）**。当前社区出现了三种典型解法：

| 模式 | 代表项目 | 核心机制 | 适用场景与普通开发者的边界 |
| :--- | :--- | :--- | :--- |
| **1. 专用运行时路由派** | DeepSeek `dsh-superagent-prototype` | 独立 Runtime + SQLite 事件流 + 常驻 Router 与隔离 Worker（消融实验证明单 Session + Subagent 在中性提示下 5 次均退化为不调子代理硬干，p95 达 29.5m；双层拆分后降至 15.7m） | 偏理论原型与 IM 群聊/GitHub 多事件并发入口；个人开发本地项目时无需维护重型运行时。 |
| **2. 社区维护三 Loop 派** | yetone `magpie`（[推文实证](https://x.com/yetone/status/2109855710444237018)） | 3 个常驻 `claude --dangerously-skip-permissions` 循环（`dev-app-loop` / `release-magpie` / `agents-status`）+ 严苛 CI + `LESSONS.md`（每晚人工复盘提取规则） | 适合**架构已定型、每日有大量社区 Issue/PR 涌入的成熟开源项目（维护态）**；个人从 0 到 1 做新产品时若无高密度 Issue 喂入，死循环易空转或过度设计。 |
| **3. 双环四重身份 + Git Hook 事件派（本仓方案 ⭐）** | `aperture` | **思考环（人 $\leftrightarrow$ 宏观 Brain）** + **`.git/hooks/post-commit` 监听 `TASKS.md (Status: pending)` 秒级事件唤醒** + **执行环（无人值守 Router 管理 `.tmp/worktrees/` 调度常驻 Worker 与独立 Tester，收口改回 `Status: verified`）** | 专为**独立开发者/小团队从 0 到 1 推进项目及多任务并发演进**设计：零外部编排器依赖、平时 0 Token 空转、需要时秒级多轨闭环。 |

---

## 二、 核心机制与底层原理解析

1. **为什么不用 15 分钟定时轮询（Heartbeat），而用 Git `post-commit` 事件驱动？**
   - 定时轮询存在三大固有缺陷：
     - **触发延迟与早退空等**：提交任务后需等待下一个轮询周期；若总控调 `wait_agent` 超时设置过短（如 10 秒）提前退出回合，即使 Worker 2 分钟后已完成，也会白白干等下一个 15 分钟周期；
     - **夜间空转缓存税**：无新任务时，定时轮询仍会每 15 分钟唤醒会话重发十余万 Token 上下文检查 `git log`；
     - **动态改写定时任务 Prompt 易腐败**：将已处理 Commit SHA 写进宿主私有的定时任务配置里，既脆弱又强绑定特定客户端。
   - **Git Hook 事件驱动原语**：利用 Git 原生 `.git/hooks/post-commit`，仅在检测到 `docs/TASKS.md` 包含 `Status: pending` 提交时，通过本地队列与静默唤醒深链（如 `codex queue` + `open -g "codex://threads/wake/<UUID>"` 或对应 CLI 命令）在 **2 秒内**直接拍醒后台常驻会话；平时无提交则 **0 唤醒、0 Token 消耗**。

2. **实测数据**
   - **常驻热节点复用**：下游 Router、Worker 与 Tester 作为常驻热会话（Warm Sessions）跨波次持续复用上下文前缀，实测常驻 Router 缓存命中率达 `98.62%`，常驻 Worker 缓存命中率达 `97.75%`。
   - **订阅直通**：同一项目连续波次的后续任务直接发给已驻留的具名会话，记录中省下约 37% 的读缓存 Token。

> 本文早期记录的四重身份分工、`in_progress` 状态与调度板细则已不再使用；角色职责、调度板规则与排空循环的现行版本见 [multi-agent-collab](../../skills/multi-agent-collab/SKILL.md)。
