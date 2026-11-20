# Antigravity（AGY）落地复刻指南

**事实核查时间**：2026-11-20（对应 Antigravity Customization System：全局配置根 `~/.gemini/config/`、工作区级 `.agents/`、原生 `invoke_subagent` / `swarm` / `browser` subagent）

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
  "version": "1.6.2",
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

## 三、第 2 步：配置全局动态模型路由（不写死版本号）

AGY 的两条原生多 Agent 通道模型机制不同，且存在一个容易踩中的实测坑：
- **`invoke_subagent`**（轻量子代理）：`Model` 参数只接受抽象档位（`inherit`、`flash`、`flash_lite`、`pro`）。**注意**：在 AGY 双模型编排（Orchestrator）模式下，`Model: "inherit"` 会继承执行层的轻量 Flash Worker，而非旗舰或编码次旗舰；
- **`swarm`**（原生编排器，**普通会话即可直接调用，不必每次敲 `/teamwork`**）：支持先调用 `swarm(action="models")` 读取当前账号实时可用模型与配额，再为每个 Worker / Tester 显式传入具体模型名。

因此全局规则必须**明确派发器优先级**（编码 Worker 与独立终端 Tester 优先走 `swarm`；`invoke_subagent` 收窄给 `research`/`browser` 与显式 `Model: "pro"` 兜底），并显式覆写内置 `swarm` Skill 在轻型里程碑里强制拉起 `monitor`/`narrator` 的条款，同时写死 `swarm` 成员**全局唯一命名**（`kill` 后名字不可复用）与**先合入再 `kill`** 两条红线。

在插件内新建 **`~/.gemini/config/plugins/aperture/rules/AGENTS.md`**（纯 Markdown，**不加 YAML frontmatter**；只要 `aperture` 插件开启，该规则会注入 `<user_rules>` 对本机所有 AGY 会话与项目默认生效，且不污染任何业务仓库）：

```markdown
# Aperture 本机多 Agent 模型路由偏好（Antigravity 全局）

以下为本机在 Antigravity 中协作时的默认模型分层与派发策略；若用户在当前对话中显式指定其他模型或编排方式，以用户指定为准。

1. **主会话（Brain）与 Fast Path**：
   - 使用用户在 AGY 界面当前选中的旗舰模型，负责架构定界、任务切分、契约冻结与最终把关。
   - ≤5 步或局部单点小改动直接由主会话完成，不启动多 Agent 编排。
2. **编码 Worker 与独立终端 Tester：默认优先走 `swarm`（普通会话直接调用，不限于 `/teamwork`）**：
   - **动态选型（不写死版本号）**：派生前先调用 `swarm(action="models")` 读取当前账号实时可用模型与配额，优先显式传入最新一代 `<你偏好的次旗舰编码系列>` 的 `high` 档；若换代或配额耗尽，顺延实时列表中同梯队具体模型名，**禁止省略 `model` 参数**（防止隐式落入双模型执行层）。
   - **精简编排（显式覆写内置 `swarm` Skill）**：1–2 个常规成员的串行或轻型里程碑，**不额外拉起 `monitor` 与 `narrator`**；仅在 ≥3 个长时并行 Worker 或用户显式启用 `/teamwork` 时才按需启用。
   - **生命周期铁律**：成员名必须带里程碑/切片前缀且全局唯一（如 `m72-s1`、`m72-tester`，因 `kill` 后名字永久不可复用）；串行单切片用 `workspace: "inherit"`，物理正交并行用 `workspace: "share"`；**`share`/`branch` 成员必须先确认提交已合入主工作树，再 `swarm(action="kill")` 回收**，里程碑结案即清理。
3. **`invoke_subagent` 收窄适用范围与兜底红线**：
   - 仅用于三类场景：`research` 只读代码库探索/大范围检索（`Model: "flash"`）、`browser` 纯网页 UI 交互验收（`Model: "flash"`），以及 `swarm` 不可用时的兜底。
   - 若被迫回退到 `invoke_subagent` 执行编码或重推理任务，**禁止传 `Model: "inherit"`**（双模型 Orchestrator 编排下会降级至 Flash 执行层），必须显式传 `Model: "pro"`。
4. **异源交叉审计（`Auditor`）**：
   - 在重大架构定稿前与合并/发版前，优先调用与主力异源的旗舰只读模型做实证审计（外部只读 CLI 或 `swarm` 内为只读 `auditor` 显式指定异源旗舰均可）；具体模型由主控按任务决定，不硬编码型号，默认高推理深度（`high`）。
5. **反假死看门狗纪律（禁止双层无限静默等待）**：
   - **Brain 派发看门狗**：派生编码 Worker 或独立 Tester 后，顺手调用 `schedule(DurationSeconds=600~900, TimerCondition="any")` 挂一个一次性看门狗闹钟（Worker 正常回报会自动取消、零额外开销）；超时未归即刻查 `swarm(action="status")` 与后台日志介入。
   - **长命令看门狗与硬超时**：主会话或 Worker 的构建/测试进入后台任务（`RUNNING`）时，挂一个 `schedule(DurationSeconds=300~600, TimerCondition="<taskId或any>")`；超时无进展立即查日志并 `kill` 僵死进程，同时要求项目测试脚本配置显式硬超时、避免嵌套抢同一构建锁。
```

> **为什么需要第 5 条看门狗**：AGY 的后台 `run_command` 默认没有硬超时，且消息机制要求 Agent 结束回合等待自动唤醒。一旦 Worker 跑的测试脚本发生自死锁或浏览器句柄挂死，就会出现“Worker 无限等后台任务、Brain 无限等 Worker”的双层静默假死；用 AGY 原生 `schedule(..., TimerCondition=...)` 挂条件取消闹钟，正常完工零开销，卡死时能自动破冰。

**同时确保各业务仓库自身不与全局规则打架**：不要在项目仓的 `AGENTS.md` 或 `docs/ROLES.md` 中写死 `invoke_subagent`、`inherit`、固定子代理名或特定宿主派发器；业务仓只需声明“按宿主全局模型路由规则派生独立 Worker 与全新 Tester”，换代或换宿主时只改上面这一处全局文件即可全机生效。

---

## 四、第 3 步：对接只读异源审计（可选）

- **纯 AGY 内部方案**：使用 `swarm` 时，将只读 `auditor` / `verifier` 成员指定为账号下与主会话异源的旗舰模型即可；
- **接入外部只读 CLI（如本机 Codex CLI / Claude Code）**：在 `~/.gemini/config/plugins/aperture/skills/` 下新增一个本机私有 Skill，按 [异源交叉审计参考实现](../../skills/multi-agent-collab/references/cross-model-audit.md) 封装：
  - 强制只读沙盒 + 一次性无痕会话 + 非交互模式 + 内联 `<= 80KB` unified diff 降轮数；
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
