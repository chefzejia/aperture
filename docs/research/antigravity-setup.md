# Antigravity（AGY）落地复刻指南

**事实核查时间**：2026-11-27（对应 Antigravity Customization System：全局配置根 `~/.gemini/config/`、工作区级 `.agents/`、原生 **Orchestrator Settings** 双模型配置、`invoke_subagent` / `browser` subagent 与显式 `/swarm`、`/teamwork`）

本指南面向以 **Antigravity（AGY）** 为主力宿主的开发者，说明如何将本仓的 5 个通用 Skill、动态模型路由偏好与只读异源审计器无痛接入 AGY，同时保持业务仓库和公开 Skill 100% 宿主与模型无关。

---

## 一、先避开一个常见目录坑：`.agents/` 不是 AGY 的全局目录

在 Antigravity 中：
- **`.agents/`（或 `.agent/`）是工作区 / 项目级发现目录**：AGY 从当前目录一路向上扫描到 `.git` 仓库根即停止，**不会**扫描家目录下的 `~/.agents/skills/`；
- **`~/.gemini/config/` 才是机器级全局配置根目录**，官方推荐把一组相关能力封装为全局 **Plugin**（`~/.gemini/config/plugins/<name>/`），可在 Customizations 页面一键启停且实时生效。

---

## 二、第 1 步：用软链挂载全局 `aperture` 插件（零副本同步）

将 `<path-to-aperture>` 替换为你本机克隆 `aperture` 仓库的绝对路径：

```bash
APERTURE_DIR="<path-to-aperture>"
PLUGIN_DIR="$HOME/.gemini/config/plugins/aperture"

mkdir -p "$PLUGIN_DIR/skills" "$PLUGIN_DIR/assets" "$PLUGIN_DIR/rules"

# 1. 软链全部 5 个核心 Skill 与 Logo（单一事实来源，拉取仓库更新自动生效）
for s in engineering-discipline project-governance multi-agent-collab knowledge-base web-research-with-assets; do
  ln -sfn "$APERTURE_DIR/skills/$s" "$PLUGIN_DIR/skills/$s"
done
ln -sfn "$APERTURE_DIR/assets/logo.svg" "$PLUGIN_DIR/assets/logo.svg"

# 2. 写入插件清单 plugin.json
cat > "$PLUGIN_DIR/plugin.json" <<'EOF'
{
  "name": "aperture",
  "displayName": "Aperture",
  "version": "1.6.4",
  "logo": "assets/logo.svg",
  "description": "AI-Native engineering discipline, minimal anti-rot project governance, unified multi-agent collaboration, shared knowledge-base management, and offline web research packages.",
  "repository": "https://github.com/chefzejia/aperture",
  "suggestedPrompts": [
    "按 project-governance 梳理并初始化本仓库的极简 AGENTS.md 与治理文档",
    "按 engineering-discipline 的反 Slop 单测与破壁验证纪律审查并加固当前改动",
    "按 multi-agent-collab 单宿主原生编排模式拆分并实现当前里程碑"
  ]
}
EOF
```

---

## 三、第 2 步：启用 AGY 原生编排双模型 + 极简全局规则

AGY 的 **Settings → Models & Usage → Orchestrator Settings** 现已支持分别配置 **Orchestrator Model**（规划、架构决策、结果审查，选旗舰模型）与 **Executor Model**（搜索、编辑、构建、测试，选高速高性价比次旗舰编码模型）。

因此不再需要为了“让执行层用上指定编码模型”而在普通会话里绕路私调 `swarm`；三条通道按本质各司其职：
- **Orchestrator 编排模式（日常与单切片首选）**：直接承担「旗舰大脑 + 次旗舰执行层」的算力分层，零编排摩擦；
- **`invoke_subagent`（信息隔离与轻型并行）**：用于需要独立冷上下文的只读 `research`、真实网页 `browser` 验收（`Tester`），以及 1–2 个独立终端 `Tester` 或 `Workspace: "share"` 正交切片；
- **`/swarm` / `/teamwork`（重型并行团队）**：遵守 AGY 官方约束，**仅在用户显式触发时启用**（适合 ≥3 个正交长时并行切片与共享看板协作）。

在插件内新建 **`~/.gemini/config/plugins/aperture/rules/AGENTS.md`**（纯 Markdown，**不加 YAML frontmatter**；只要 `aperture` 插件开启，该规则会注入 `<user_rules>` 对本机所有 AGY 会话与项目默认生效，且不污染任何业务仓库）：

```markdown
# Aperture 本机多 Agent 协作偏好（Antigravity 全局）

以下为本机在 Antigravity 中协作时的默认分层与派发策略；若用户在当前对话中显式指定其他模型或编排方式，以用户指定为准。

1. **日常与单切片开发（默认走 AGY 原生 Orchestrator 双模型）**：
   - 在 AGY `Models & Usage → Orchestrator Settings` 中直接配置 `Orchestrator Model`（旗舰）与 `Executor Model`（次旗舰编码档）；
   - ≤5 步 Fast Path、契约冻结以及常规单切片里程碑直接在主会话/编排模式内自然完成，不为了切换模型而额外套壳拉起多 Agent 团队。
2. **上下文隔离与轻型并行（优先原生 `invoke_subagent`）**：
   - **`research`（只读代码库大范围探索）与 `browser`（网页/GUI 独立验收 `Tester`）**：使用 `Model: "flash"`，保持冷上下文独立视角；
   - **独立终端 `Tester` 或 1–2 个正交并行切片**：使用 `invoke_subagent`（物理正交并行写必传 `Workspace: "share"`），需重推理时显式指定 `Model: "pro"`；验收通过后按最小语义单元 Squash 线性合入 `main` 并清理工作树。
3. **重型多 Agent 团队（仅在用户显式触发 `/swarm` 或 `/teamwork` 时启用）**：
   - 遵守宿主约束，普通对话不私自调用 `swarm`；进入显式团队模式后（如 ≥3 个正交长任务），成员名带里程碑/切片前缀且全局唯一，物理正交并行用 `workspace: "share"`，**先确认按最小语义单元 Squash 线性合入 `main`，再 `swarm(action="kill")` 回收**。
4. **异源交叉审计（`Auditor`）**：
   - 在重大架构定稿前与合并/发版前，优先调用与主力异源的旗舰只读模型做实证审计（推荐外部只读 CLI，独立配额不受宿主内第三方模型额度限制；具体模型由主控按任务决定，不硬编码型号，默认高推理深度 `high`）。
5. **反假死看门狗纪律（活性驱动，禁止双层静默等待与盲杀）**：
   - **派发看门狗**：派生编码/验收子代理后，顺手调用 `schedule(DurationSeconds=600~900, TimerCondition="any")` 挂一次性看门狗闹钟（正常回报自动取消、零额外开销）；超时未归即刻检查子代理/团队状态与后台日志介入。
   - **长命令看门狗、活性续期与硬超时**：构建/测试/外部审计进入后台任务（`RUNNING`）时，挂 `schedule(DurationSeconds=300~600, TimerCondition="<taskId或any>")`；超时唤醒后检查 `manage_task(Action="status")` 与日志末尾实时心跳——**若确认仍在持续推进（如外部审计心跳显示工具调用递增、思考未超空闲阈值），续挂一个看门狗周期而不盲杀**；仅在长时间静默超阈值、进程僵死或活锁时 `kill` 并排查根因。本地测试脚本仍配显式硬超时且避免嵌套抢同一构建锁。
6. **人机极简 Issue 协作响应协议（跨仓库全局默认）**：
   - 人类通过 GitHub Issue 提单时，按标题前缀或标签开关直接分流：`[直接修]` / `fix` 直接定位修复验证并交付；`[先讨论]` / `discuss` 严禁直接写代码，先读代码给 2–3 个带取舍选项对齐后再动工；`[先记着]` 记入待办池不打断主线；未走模板的口语化 Issue 先用 3 行规整要点与开关。
7. **Git 主干线性收口、分支清理与公开仓卫生（跨仓库全局默认）**：
   - **草稿态与主干账本分离**：`main` 只收经过验收的线性原子提交，严禁 `wip:` 半成品与菱形 `merge commit` 落入 `main`；完整里程碑/切片在本地短命分支或隔离 Worktree（`.tmp/worktrees/` 或宿主原生 `share`）中开发与返工，验收（及按需审计）通过后按最小可独立回滚语义单元（单切片 = 1 条；多正交切片 = 每切片 1 条）**Squash 线性合入 `main`**，在 Commit Body 写明验证证据并立即删除本地分支与工作树；≤5 步 Fast Path 微调与上游契约冻结仍可直接单次干净提交到 `main`；绝不改写或强推已落入 `main` 的历史。
   - **远端零僵尸分支与跨人 PR**：本地探索与切片分支不推远端；跨人/开源 PR 采用短命分支 + 落后时 `git fetch && git rebase origin/main` + `git push --force-with-lease`（高并发仓库优先 Merge Queue）+ `Squash & Merge` + 自动删除远端分支；分支落后过久或与新冻结契约硬冲突时弃旧分支基于最新 `main` 重放意图与守卫测试，不硬解腐烂冲突。
   - **公开仓库隐私卫生**：向公开仓库提交前检查 `user.email`，优先使用 GitHub noreply 隐私邮箱；发现历史已含个人邮箱时未经用户确认不擅自改写已有主干历史。
```

> **为什么需要第 5 条看门狗**：AGY 的后台 `run_command` 默认没有硬超时，且消息机制要求 Agent 结束回合等待自动唤醒。一旦子代理跑的测试脚本发生自死锁或浏览器句柄挂死，就会出现“子代理无限等后台任务、主控无限等子代理”的双层静默假死；用 AGY 原生 `schedule(..., TimerCondition=...)` 挂条件取消闹钟，正常完工零开销，卡死时能自动破冰，仍在健康推进时看心跳续期即可。

**同时确保各业务仓库自身不与全局规则打架**：不要在项目仓的 `AGENTS.md` 或 `docs/ROLES.md` 中写死 `invoke_subagent`、`swarm`、具体模型名或特定宿主派发器；业务仓只需声明“按宿主全局规则执行独立验收与异源审计”，换代或换宿主时只改上面这一处全局文件即可全机生效。

---

## 四、第 3 步：对接只读异源审计（可选）

- **纯 AGY 内部方案**：使用 `swarm` 时，将只读 `auditor` / `verifier` 成员指定为账号下与主会话异源的旗舰模型即可；
- **接入外部只读 CLI（如本机 Codex CLI / Claude Code）**：在 `~/.gemini/config/plugins/aperture/skills/` 下新增一个本机私有 Skill，按 [异源交叉审计参考实现](../../skills/multi-agent-collab/references/cross-model-audit.md) 封装：
  - 强制只读沙盒 + 一次性无痕会话 + 非交互模式 + 内联 `<= 80KB` unified diff（超大改动按正交模块分片并行审）；
  - 启用 JSONL 事件流实时心跳 + **分态空闲超时**（思考态按 `--effort` 自适应、本地只读命令紧收 `120s`）+ **活锁熔断与 Fail-Fast** + 进程组清理，替代单一机械 10 分钟总超时；
  - 模型解析严格遵循 `Brain 显式参数 > 环境变量 > 外部 CLI 本机默认配置`，不在脚本里写死型号；
  - 日常 GUI / Web 体验验收留在 AGY 原生 `browser` subagent，不下放给无头 CLI。

---

## 五、第 4 步：单项目专属 Skill 与权限边界

1. **单项目重型业务 Skill 不要挂全局**：在对应业务仓库根目录建 `.agents/skills.json`，只在打开该仓库时自动加载：
   ```json
   {
     "entries": [
       { "path": "skills" }
     ]
   }
   ```
2. **审陌生开源仓库时收紧项目级权限**：若全局开启了激进自动执行模式或关闭终端沙盒，在打开外部陌生仓库审查 PR 前，务必在 AGY 的 **Project-Level Settings** 中单独开启终端沙盒并切回审批模式。
