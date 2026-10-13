# magpie 实操分析

> 分析时间：2026-10-13  
> magpie 版本：0.1.1222  
> 目的：评估 magpie 能替代什么工具，如何优化现有 workflow

## 当前环境检测

### 已安装的 Agents

```
✓ Claude Code (claude-opus-5-5, effort max)
✓ Claude Desktop (provider —)
✓ Codex (gpt-6.1-sol, effort xhigh)
✓ Gemini CLI (auth google)
✓ OpenCode (—, small —)
✓ Pi (gateway/gpt-6.1-sol, thinking xhigh)
✓ Zed (—)
✓ DeepSeek Harness (deepseek-v4-pro, thinking —)
✓ Hermes Agent (—, effort —)
✓ Kimi Code (gateway/kimi)
✓ Qwen Code (coder-model)
✓ Grok Build (grok-4.6, effort —)
✓ WorkBuddy (provider —)
✓ CodeBuddy Code (—)
```

### 已安装的工具

```
✓ Orca.app - /Applications/Orca.app
✓ pi - /opt/homebrew/bin/pi
✓ codex - /opt/homebrew/bin/codex
✓ claude - /opt/homebrew/bin/claude
```

## magpie 核心能力

### 1. 统一模型网关（这是核心价值）

**magpie 做什么**：
- 在 `127.0.0.1:<port>` 运行一个本地网关
- 支持 OpenAI Chat、Anthropic Messages、Gemini 三种协议
- 协议之间自动转换（streaming、tool calls、reasoning 都支持）
- 所有 agent 通过这一个网关访问所有模型

**示意图**：
```
你的 agents                    magpie 网关                    模型提供商
┌─────────────┐               ┌──────────────┐              ┌──────────────┐
│ Claude Code │──────┐        │              │──────────────│ DeepSeek API │
│ Codex       │──────┼───────▶│ 127.0.0.1    │──────────────│ Kimi API     │
│ Pi          │──────┤        │    :3425     │──────────────│ ChatGPT 订阅 │
│ Gemini CLI  │──────┘        │              │──────────────│ Claude 订阅  │
└─────────────┘               └──────────────┘              └──────────────┘
```

### 2. 统一模型选择

**一个地方管理所有 agent 的模型**：
```bash
magpie claude deepseek/deepseek-v4-pro      # Claude Code 用 DeepSeek
magpie codex moonshot/kimi-k2.5             # Codex 用 Kimi
magpie pi group/opus-anywhere               # Pi 用路由组（自动切换账号）
```

### 3. 配额自动切换（Routing Groups）

**核心场景**：你有多个账号，一个用完自动切换下一个
```bash
magpie group add "Opus anywhere" \
  models=claude/claude-opus-5-5,copilot/claude-opus-5.5 \
  routing=smart

magpie claude group/opus-anywhere
```

当第一个账号配额用完，自动切换到第二个，agent 无感知。

### 4. 多账号管理

magpie 自动发现你已登录的订阅：
- Claude Code 的登录文件
- Codex 的登录文件
- Keychain 里的凭证

## magpie 能替代什么？

### ❌ magpie **不能**替代 Orca

**Orca 是什么**：
- Orca 是一个 **macOS 菜单栏工具**
- 提供快速访问 AI 对话的界面
- 类似 Raycast AI 或 ChatGPT menubar app

**为什么不能替代**：
- magpie 是 **网关/路由器**，不是对话界面
- magpie 服务于 **编程 agents**（Claude Code、Codex 等）
- Orca 是给 **人用的快速对话工具**

**结论**：两者不冲突，各司其职。

### ✅ magpie 能优化什么？

#### 1. 统一模型配置管理

**现状痛点**：
- Claude Code 有自己的 `~/.claude/settings.json`
- Codex 有自己的 `~/.codex/config.toml`
- Pi 有自己的 `~/.pi/agent/settings.json`
- 每个 agent 分别配置，很难统一管理

**magpie 改进**：
```bash
# 一个命令看所有 agent 用什么模型
magpie agents

# 一个命令切换某个 agent 的模型
magpie pi deepseek/deepseek-v4-pro

# 一个命令设置所有 agent 的 reasoning 等级
magpie claude effort high
magpie codex effort high
magpie pi thinking high
```

#### 2. Profile 管理（场景切换）

**核心场景**：不同场景用不同模型组合

```bash
# 工作场景：用付费的高质量模型
magpie save work
magpie claude claude-opus-5-5
magpie codex gpt-6.1-sol
magpie pi claude-opus-5-5

# 实验场景：用便宜的开源模型
magpie save experiment
magpie claude deepseek/deepseek-v4-pro
magpie codex moonshot/kimi-k2.5
magpie pi qwen/qwen-max

# 快速切换
magpie use work
magpie use experiment
```

#### 3. 配额监控和自动切换

**核心价值**：你有多个 API key 或订阅账号，magpie 自动管理

```bash
# 查看所有账号剩余配额
magpie quota

# 设置自动切换
magpie group add "DeepSeek cluster" \
  models=deepseek/deepseek-v4-pro,deepseek-2/deepseek-v4-pro \
  routing=smart

magpie claude group/deepseek-cluster
```

当第一个 key 用完，自动切换到第二个。

#### 4. 新模型快速验证

**场景**：你想测试新模型，不用改每个 agent 的配置

```bash
# 给所有 agent 临时切换到新模型
magpie claude deepseek/deepseek-v4-pro
magpie codex deepseek/deepseek-v4-pro
magpie pi deepseek/deepseek-v4-pro

# 测试完，一键恢复
magpie claude default
magpie codex default
magpie pi default
```

## 推荐的实操步骤

### 第一步：添加你的 Provider

```bash
# 添加 DeepSeek
magpie provider add deepseek sk-YOUR-KEY

# 添加 Moonshot (Kimi)
magpie provider add moonshot sk-YOUR-KEY

# 添加 OpenAI
magpie provider add openai sk-YOUR-KEY

# 查看已添加的 providers
magpie providers
```

### 第二步：配置核心 agents

```bash
# 保存当前配置为 baseline
magpie save baseline

# 配置 Claude Code（你的主力编程工具）
magpie claude deepseek/deepseek-v4-pro

# 配置 Codex
magpie codex moonshot/kimi-k2.5

# 配置 Pi（你现在正在用的）
magpie pi deepseek/deepseek-v4-pro
```

### 第三步：创建 routing group（可选，高级用法）

```bash
# 如果你有多个 DeepSeek key
magpie group add "DeepSeek cluster" \
  models=deepseek/deepseek-v4-pro,deepseek-2/deepseek-v4-pro \
  routing=smart

magpie claude group/deepseek-cluster
```

### 第四步：验证配置

```bash
# 查看所有 agent 当前配置
magpie agents

# 查看可用的所有模型
magpie models

# 查看配额情况
magpie quota
```

## magpie 的局限性

### 1. 不是对话界面
- magpie 不能替代 Orca、ChatGPT Desktop 等对话工具
- 它只是一个"交换机"，连接 agents 和模型

### 2. 只服务于支持的 agents
- 必须是 magpie 支持的 agent（见 `magpie agents` 列表）
- 自己写的脚本需要手动设置 `OPENAI_BASE_URL`

### 3. 网关模式有性能开销
- 多了一层转发
- 对于本地模型可能不如直连快

## 是否值得使用？

### ✅ 强烈推荐的场景

1. **你有多个 agents**（Claude Code、Codex、Pi 等）
2. **你有多个 API keys 或订阅账号**
3. **你经常测试不同模型**
4. **你需要统一管理配置**

### ⚠️ 可以不用的场景

1. **你只用一个 agent + 一个订阅**
2. **你不关心统一配置**
3. **你的 workflow 很简单**

## 对你的建议

根据你当前的情况：
- ✓ 你有多个 agents（Claude、Codex、Pi、Gemini CLI 等）
- ✓ 你在研究 Agent workflow 优化
- ✓ 你关心工程质量和工具链

**建议**：
1. **先用 magpie 管理 Claude Code 和 Codex**
   - 这是你最常用的编程工具
   - 通过 magpie 统一切换模型
   
2. **保留 Orca**
   - Orca 是快速对话工具，和 magpie 不冲突
   
3. **Pi 可以通过 magpie 管理，也可以不管**
   - Pi 本身就有很好的模型管理
   - 如果你想统一配置，可以用 magpie

4. **创建 2-3 个 profiles**
   - `work`: 高质量模型（Claude Opus、GPT-6.1）
   - `fast`: 快速廉价模型（DeepSeek、Kimi）
   - `experiment`: 测试新模型

## 下一步行动

```bash
# 1. 打开 magpie app（看看 GUI）
open -a magpie

# 2. 或者用 TUI（终端界面）
magpie tui

# 3. 查看当前状态
magpie agents
magpie providers
```

你想先做什么？
1. 添加你的 API keys
2. 配置几个常用 agents
3. 创建 profiles
4. 先用 TUI 看看界面
