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
  "version": "1.6.1",
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

AGY 的两条原生多 Agent 通道模型机制不同，需要分别理解：
- **`invoke_subagent`**（单子代理）：`Model` 参数只接受抽象档位（`inherit`、`flash`、`flash_lite`、`pro`），由 AGY 平台自动映射到当下最新版本，无需维护具体版本号；
- **`swarm`**（`/teamwork` 多 Worker 协同）：支持先调用 `swarm(action="models")` 读取当前账号实时可用模型与配额，再为每个 Worker 动态指定模型。

在插件内新建 **`~/.gemini/config/plugins/aperture/rules/AGENTS.md`**（纯 Markdown，**不加 YAML frontmatter**；只要 `aperture` 插件开启，该规则对本机所有 AGY 会话与项目默认生效，且不污染任何业务仓库）：

```markdown
# Aperture 本机多 Agent 模型路由偏好（Antigravity 全局）

以下为本机在 Antigravity 中协作时的默认模型分层策略；若用户在当前对话中显式指定其他模型，以用户指定为准。

1. **主会话（Brain）**：使用用户在 AGY 界面当前选中的旗舰模型，负责架构定界、任务切分与最终把关。
2. **`swarm`（`/teamwork`）编码 Worker 动态选型（不写死版本号）**：
   - 派生编码 Worker 前，先调用 `swarm(action="models")` 读取当前账号实时可用模型与配额；
   - 默认优先动态匹配最新一代 `<你偏好的次旗舰编码系列>` 的 `high` 档作为编码 Worker；若未来模型更名换代或配额耗尽，按实时列表选用同梯队次旗舰或回退为继承主会话模型。
3. **`invoke_subagent` 档位分工**：
   - 编码实现、重构与需要完整推理的任务保持默认 `Model: "inherit"`；
   - 纯只读代码库探索（`research`）或大范围信息检索优先使用 `Model: "flash"` 以提速并节省旗舰配额。
4. **异源交叉审计（`Auditor`）**：
   - 在重大架构定稿前与合并/发版前，优先调用与主力异源的旗舰只读模型做实证审计（外部只读 CLI 或 `swarm` 内指定异源旗舰均可）；具体模型由主控按任务决定，不硬编码型号，默认高推理深度（`high`）。
```

当未来模型快速迭代或更名换代时，只需改这一处文件的第 2 条关键词即可全机生效，零仓库维护成本。

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
