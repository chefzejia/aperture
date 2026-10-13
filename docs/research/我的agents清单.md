# 我的 Agents 清单

> 更新时间：2026-10-13  
> 清理后状态

## 保留的 Agents

### 核心编程工具

1. **Claude Code** (`claude`)
   - 路径：`~/.claude/settings.json`
   - 当前模型：`claude-opus-5-5`
   - Effort：max
   - 用途：主力编程 agent

2. **Claude Desktop**
   - 路径：`~/Library/Application Support/Claude/claude_desktop_config.json`
   - 当前模型：provider —
   - 用途：桌面对话

3. **Codex** (`codex`)
   - 路径：`~/.codex/config.toml`
   - 当前模型：`gpt-6.1-sol`
   - Effort：xhigh
   - 用途：另一个编程 agent

4. **Pi** (`pi`)
   - 路径：`~/.pi/agent/settings.json`
   - 当前模型：`gateway/gpt-6.1-sol`
   - Thinking：xhigh
   - 用途：当前使用的 agent（你）

### 开发工具

5. **DeepSeek Harness** (`dsh`)
   - 路径：`~/.dsh/profiles/web/cordis.patch.yml`
   - 当前模型：`deepseek-v4-pro`
   - Thinking：—
   - 用途：DeepSeek 专用 harness

6. **Zed**
   - 路径：`~/.config/zed/settings.json`
   - 当前模型：—
   - 用途：编辑器集成

7. **Grok Build**
   - 路径：`~/.grok/config.toml`
   - 当前模型：`grok-4.6`
   - Effort：—
   - 用途：Grok 构建工具

8. **WorkBuddy**
   - 路径：`~/.workbuddy/models.json`
   - 当前模型：provider —
   - 用途：工作协作工具

9. **Kimi Code**
   - 路径：`~/.kimi-code/config.toml`
   - 当前模型：`gateway/kimi`
   - 用途：Kimi 编程 agent

### 其他工具

10. **Orca.app**
    - 路径：`/Applications/Orca.app`
    - 用途：菜单栏快速 AI 对话工具
    - 说明：不会被 magpie 替代，各司其职

## 已卸载的 Agents

✅ 已完全清理（2026-10-13）

1. ~~Gemini CLI~~ - `npm uninstall -g @google/gemini-cli` + 删除 `~/.gemini`
2. ~~Qwen Code~~ - 删除 `~/.qwen` + 删除命令链接
3. ~~OpenCode~~ - 删除 `~/.config/opencode`
4. ~~CodeBuddy Code~~ - 删除 `~/.codebuddy`
5. ~~Hermes Agent~~ - 删除 `~/.hermes`

## 使用 magpie 管理

### 核心命令

```bash
# 查看所有 agents 状态
magpie agents

# 切换某个 agent 的模型
magpie claude deepseek/deepseek-v4-pro
magpie codex moonshot/kimi-k2.5
magpie pi openai/gpt-6.1-sol

# 创建和切换 profile
magpie save work
magpie save experiment
magpie use work

# 查看配额
magpie quota

# 查看可用模型
magpie models
```

### 推荐配置思路

**场景一：工作模式（高质量）**
- Claude Code → claude-opus-5-5
- Codex → gpt-6.1-sol
- Pi → claude-opus-5-5

**场景二：实验模式（快速迭代）**
- Claude Code → deepseek/deepseek-v4-pro
- Codex → moonshot/kimi-k2.5
- Pi → deepseek/deepseek-v4-pro

**场景三：混合模式（按需）**
- Claude Code → claude-opus-5-5（精细工作）
- Codex → deepseek/deepseek-v4-pro（快速原型）
- Pi → routing group（自动切换）

## 下一步计划

- [ ] 添加常用的 API providers
- [ ] 配置 Claude Code 和 Codex 的模型
- [ ] 创建 2-3 个 profiles
- [ ] 设置 routing groups（如果有多账号）
- [ ] 测试配置是否生效
