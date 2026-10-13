# magpie 配置记录

> 配置时间：2026-10-13  
> Provider：gateway  
> 目的：统一管理所有 agents 的模型

## ✅ 已完成配置

### 1. 添加 gateway provider

```bash
magpie provider add "Gateway" \
  url=https://api.gateway.example/v1 \
  key=REDACTED-SCRUBBED
```

**配置详情**：
- Provider ID: `gateway`
- Base URL: `https://api.gateway.example/v1`
- API Key: `sk-eb88...b436` (Claude Code 的 key)
- 已被使用：Pi、Kimi Code

### 2. 添加支持的模型（10 个）

```bash
magpie provider models gateway \
  claude-opus-5-5 \
  claude-sonnet-5-5 \
  claude-sonnet-4-6 \
  claude-haiku-4-5-20251001 \
  gpt-6.1-sol \
  gpt-5.1 \
  deepseek-v4-pro \
  kimi \
  k3 \
  kimi-for-coding
```

**模型列表**：
| 模型 ID | 全名 | Reasoning Efforts |
|---------|------|-------------------|
| `gateway/claude-opus-5-5` | Claude Opus 5.5 | low/medium/high/xhigh/max |
| `gateway/claude-sonnet-5-5` | Claude Sonnet 5.5 | - |
| `gateway/claude-sonnet-4-6` | Claude Sonnet 4.6 | low/medium/high/max |
| `gateway/claude-haiku-4-5-20251001` | Claude Haiku 4.5 | low/medium/high/xhigh/max |
| `gateway/gpt-6.1-sol` | GPT-6.1 Sol | none/low/medium/high/xhigh/max/ultra |
| `gateway/gpt-5.1` | GPT-5.1 | none/low/medium/high |
| `gateway/deepseek-v4-pro` | DeepSeek V4 Pro | high/max |
| `gateway/kimi` | Kimi | - |
| `gateway/k3` | Kimi K3 | low/high/max |
| `gateway/kimi-for-coding` | Kimi K2.7 Code | - |

### 3. 配置核心 agents

```bash
# 保存基线
magpie save baseline

# 配置 Claude Code
magpie claude gateway/claude-opus-5-5

# 配置 Codex
magpie codex gateway/gpt-6.1-sol

# 配置 Pi
magpie pi gateway/gpt-6.1-sol
```

**当前状态**：
```
Claude Code: claude-opus-5-5 · effort max
Codex:       gpt-6.1-sol · effort xhigh
Pi:          gateway/gpt-6.1-sol · thinking xhigh
```

**注意**：Codex 需要重启才能看到新模型：
```bash
codex app-server daemon restart
# 然后重启 Codex app
```

## 配置文件位置

### magpie 配置
- 配置文件：`~/.config/magpie/` (推测)
- Provider 信息：已添加到 magpie 数据库

### Agents 原始配置（已被 magpie 接管）

**Claude Code**：
```json
~/.claude/settings.json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.gateway.example",
    "ANTHROPIC_API_KEY": "sk-eb88...b436"
  }
}
```

**Codex**：
```toml
~/.codex/config.toml
model_provider = "gateway"
model = "gpt-6.1-sol"

[model_providers.gateway]
base_url = "https://api.gateway.example/v1"
wire_api = "responses"
```

**Kimi Code**：
```toml
~/.kimi-code/config.toml
[providers.gateway-kimi]
base_url = "https://gateway.com/v1"
api_key = "sk-eb20...c912"
```

## 使用方式

### 查看配置

```bash
# 查看所有 providers
magpie providers

# 查看 gateway 的详细信息
magpie provider gateway

# 查看所有 agents 状态
magpie agents

# 查看所有可用模型
magpie models
```

### 切换模型

```bash
# 单个 agent 切换
magpie claude gateway/deepseek-v4-pro
magpie codex gateway/gpt-5.1
magpie pi gateway/claude-opus-5-5

# 切换 reasoning effort
magpie claude effort max
magpie codex effort high
```

### Profile 管理

```bash
# 保存当前配置为 profile
magpie save work

# 创建实验配置
magpie claude gateway/deepseek-v4-pro
magpie codex gateway/gpt-5.1
magpie save experiment

# 切换 profile
magpie use work
magpie use experiment
magpie use baseline  # 恢复初始状态

# 查看所有 profiles
magpie profiles
```

## 推荐的使用场景

### 场景一：工作模式（高质量）

```bash
magpie claude gateway/claude-opus-5-5 effort max
magpie codex gateway/gpt-6.1-sol effort xhigh
magpie pi gateway/claude-opus-5-5 thinking xhigh
magpie save work
```

**用途**：生产代码、关键功能、需要高质量输出

### 场景二：快速模式（省钱）

```bash
magpie claude gateway/deepseek-v4-pro effort high
magpie codex gateway/gpt-5.1 effort medium
magpie pi gateway/deepseek-v4-pro thinking medium
magpie save fast
```

**用途**：快速原型、简单修改、测试想法

### 场景三：实验模式（测试新模型）

```bash
magpie claude gateway/claude-sonnet-4-6 effort high
magpie codex gateway/k3 effort max
magpie pi gateway/kimi-for-coding thinking high
magpie save experiment
```

**用途**：测试不同模型的表现、对比效果

## 下一步建议

### 1. 创建常用 profiles

```bash
# 创建 3 个场景
magpie use baseline
magpie save work      # 当前配置（opus + gpt-6.1）

# 切换到快速模式
magpie claude gateway/deepseek-v4-pro
magpie codex gateway/gpt-5.1
magpie pi gateway/deepseek-v4-pro
magpie save fast

# 恢复工作模式
magpie use work
```

### 2. 添加其他 API keys（如果有）

```bash
# 如果你有多个 gateway 账号
magpie provider add "Gateway 2" \
  url=https://api.gateway.example/v1 \
  key=sk-另一个key

# 添加模型
magpie provider models gateway-2 claude-opus-5-5 gpt-6.1-sol
```

### 3. 配置 routing group（多账号自动切换）

```bash
# 创建路由组
magpie group add "Opus anywhere" \
  models=gateway/claude-opus-5-5,gateway-2/claude-opus-5-5 \
  routing=smart

# 使用路由组
magpie claude group/opus-anywhere
```

当第一个账号配额用完，自动切换到第二个。

### 4. 测试配置

```bash
# 重启 Codex（让它识别新模型）
codex app-server daemon restart

# 打开 magpie GUI 查看
open -a magpie

# 或用 TUI
magpie tui
```

## 验证配置是否生效

### 方法一：查看 agents 状态

```bash
magpie agents | grep -E "Claude Code|Codex|Pi"
```

应该看到：
```
Claude Code: gateway/claude-opus-5-5 · effort max
Codex:       gateway/gpt-6.1-sol · effort xhigh
Pi:          gateway/gpt-6.1-sol · thinking xhigh
```

### 方法二：实际使用

- 打开 Claude Code，开始一个新对话，看网关是否正常工作
- 打开 Codex，检查模型列表是否包含 gateway 的模型
- 用 Pi 执行一个任务，看是否正常响应

### 方法三：查看 magpie 日志

```bash
# magpie 会记录所有请求
# 可以在 GUI 或 TUI 中查看实时日志
magpie tui
```

## 故障排查

### 问题 1：Codex 看不到新模型

**原因**：Codex 在启动时加载模型列表

**解决**：
```bash
codex app-server daemon restart
# 然后重启 Codex app
```

### 问题 2：API 调用失败

**检查**：
```bash
# 查看 provider 状态
magpie provider gateway

# 测试 API key 是否有效
curl https://api.gateway.example/v1/models \
  -H "Authorization: Bearer sk-eb88...b436"
```

### 问题 3：magpie 网关没有启动

**检查**：
```bash
# 查看网关是否在运行
lsof -i :3425

# 启动 magpie
open -a magpie
# 或
magpie tui
```

### 问题 4：想恢复原始配置

**方法一**：使用 baseline profile
```bash
magpie use baseline
```

**方法二**：手动恢复
- 关闭 magpie
- 直接编辑 `~/.claude/settings.json`、`~/.codex/config.toml` 等

## 总结

✅ **已完成**：
1. 添加 gateway provider
2. 配置 10 个常用模型
3. 为 Claude Code、Codex、Pi 配置模型
4. 保存 baseline profile

✅ **现在可以**：
- 一个命令切换所有 agent 的模型
- 创建和切换不同场景的 profiles
- 查看所有 agent 的配置状态
- 统一管理 gateway 的所有模型

🎯 **下一步**：
- 测试配置是否正常工作
- 创建 work/fast/experiment 三个 profiles
- 如果有多账号，配置 routing groups
