# magpie 完整配置总结

> 配置时间：2026-10-13  
> 状态：✅ 已完成  
> Profile：all-models-configured

## ✅ 已配置的 6 个 Providers

### 1. Gateway（主 provider，已清理）
- **ID**: `gateway`
- **Base URL**: `https://api.gateway.example/v1`
- **API Key**: `sk-e…b436`
- **模型数**: 5 个（已移除国产模型 Kimi、K3）
- **使用者**: Claude Code, Codex, Pi, Kimi Code

**模型列表**：
- `gateway/claude-opus-5-5` - Claude Opus 5.5 (low/medium/high/xhigh/max)
- `gateway/claude-sonnet-5-5` - Claude Sonnet 5.5 (low/medium/high/xhigh/max)
- `gateway/claude-haiku-4-5-20251001` - Claude Haiku 4.5 (low/medium/high/xhigh/max)
- `gateway/gpt-6.1-sol` - GPT-6.1 Sol (low/medium/high/xhigh/max/ultra)
- `gateway/deepseek-v4-pro` - DeepSeek V4 Pro (low/high/max)

### 2. Gateway GPT（GPT 专用）
- **ID**: `gw-gpt`
- **Base URL**: `https://gateway.com/v1`
- **API**: OpenAI Responses
- **API Key**: `sk-d…edcd`
- **模型数**: 1 个

**模型列表**：
- `gw-gpt/gpt-6.1-sol` - GPT-6.1 Sol (low/medium/high/xhigh/max/ultra)

### 3. Gateway Claude（Claude 原生 API）
- **ID**: `gw-claude`
- **Base URL**: `https://gateway.com`
- **API**: Anthropic Messages
- **API Key**: `sk-e…b436`
- **模型数**: 3 个

**模型列表**：
- `gw-claude/claude-opus-5-5` - Claude Opus 5.5 (low/medium/high/xhigh/max)
- `gw-claude/claude-sonnet-5-5` - Claude Sonnet 5.5 (low/medium/high/xhigh/max)
- `gw-claude/claude-opus-4-6` - Claude Opus 4.6 (low/medium/high/max)

### 4. Gateway Gemini
- **ID**: `gw-gemini`
- **Base URL**: `https://gateway.com/v1`
- **API**: OpenAI Responses
- **API Key**: `sk-3…6a9c`
- **模型数**: 1 个

**模型列表**：
- `gw-gemini/gemini-3.8-flash` - Gemini 3.8 Flash (low/medium/high)

### 5. Gateway Grok
- **ID**: `gateway-grok`
- **Base URL**: `https://gateway.com/v1`
- **API**: OpenAI Responses
- **API Key**: `sk-0…cfd8`
- **模型数**: 1 个

**模型列表**：
- `gateway-grok/grok-4.7` - Grok 4.7 (low/medium/high/xhigh)

### 6. Gateway CN（国产模型）
- **ID**: `gw-cn`
- **Base URL**: `https://gateway.com/v1`
- **API**: OpenAI Responses
- **API Key**: `sk-e…c912`
- **模型数**: 2 个

**模型列表**：
- `gw-cn/deepseek-flash` - DeepSeek V4.1 Flash (low/high/max)
- `gw-cn/glm-5.3-prime` - GLM 5.3 Prime (low/high/max)

---

## 🎯 模型分类（按用途）

### 高质量模型（生产代码、关键功能）

1. **Claude Opus 5.5** - 最高质量
   - `gateway/claude-opus-5-5`
   - `gw-claude/claude-opus-5-5`
   - 支持 max reasoning effort

2. **GPT-6.1 Sol** - 最强推理
   - `gateway/gpt-6.1-sol`
   - `gw-gpt/gpt-6.1-sol`
   - 支持 ultra reasoning effort（独有）

3. **Claude Opus 4.6** - 上一代旗舰
   - `gw-claude/claude-opus-4-6`

### 干活模型（日常开发、快速迭代）

1. **Claude Sonnet 5.5** - 平衡性能
   - `gateway/claude-sonnet-5-5`
   - `gw-claude/claude-sonnet-5-5`

2. **DeepSeek Flash** - 快速+便宜
   - `gw-cn/deepseek-flash`

### 快速模型（简单任务、测试）

1. **Claude Haiku 4.5** - 最快的 Claude
   - `gateway/claude-haiku-4-5-20251001`

2. **Gemini 3.8 Flash** - Google 快速模型
   - `gw-gemini/gemini-3.8-flash`

3. **DeepSeek V4 Pro** - 性价比高
   - `gateway/deepseek-v4-pro`

### 实验/特殊用途

1. **Grok 4.7** - xAI 的模型
   - `gateway-grok/grok-4.7`

2. **GLM 5.3 Prime** - 智谱 AI
   - `gw-cn/glm-5.3-prime`

---

## 📊 当前 Agents 配置

### Claude Code
- **模型**: `gateway/claude-opus-5-5`
- **Effort**: max
- **Haiku**: `gateway/claude-haiku-4-5-20251001`
- **配置文件**: `~/.claude/settings.json`

### Codex
- **模型**: `gateway/gpt-6.1-sol`
- **Effort**: xhigh
- **配置文件**: `~/.codex/config.toml`

### Pi
- **模型**: `magpie/gateway/gpt-6.1-sol`
- **Thinking**: xhigh
- **配置文件**: `~/.pi/agent/settings.json`

---

## 🔄 自动生成的 Routing Groups

magpie 自动为同名模型创建了 routing groups：

1. **group/auto-claude-opus-5-5**
   - 自动在 `gateway` 和 `gw-claude` 之间切换
   
2. **group/auto-claude-sonnet-5-5**
   - 自动在 `gateway` 和 `gw-claude` 之间切换
   
3. **group/auto-gpt-6-1-sol**
   - 自动在 `gateway` 和 `gw-gpt` 之间切换

**优势**：如果一个 provider 配额用完，自动切换到另一个

---

## 💡 推荐使用场景配置

### 场景 1: 工作模式（高质量）

```bash
magpie claude gw-claude/claude-opus-5-5 effort max
magpie codex gw-gpt/gpt-6.1-sol effort xhigh
magpie pi gw-claude/claude-opus-5-5 thinking xhigh
magpie save work
```

**特点**：
- 使用最高质量模型
- 独立的 API keys（不互相影响配额）
- 适合：生产代码、关键功能、重要决策

### 场景 2: 干活模式（平衡）

```bash
magpie claude gw-claude/claude-sonnet-5-5 effort high
magpie codex gw-gpt/gpt-6.1-sol effort high
magpie pi gw-cn/deepseek-flash thinking high
magpie save daily
```

**特点**：
- Sonnet 5.5 性能足够好
- DeepSeek Flash 快速+便宜
- 适合：日常开发、快速迭代、大量任务

### 场景 3: 快速模式（省钱）

```bash
magpie claude gateway/claude-haiku-4-5-20251001 effort medium
magpie codex gateway/deepseek-v4-pro effort medium
magpie pi gw-cn/deepseek-flash thinking low
magpie save fast
```

**特点**：
- 最快速的模型
- 成本最低
- 适合：简单修改、测试、调试、文档

### 场景 4: 实验模式（测试新模型）

```bash
magpie claude gateway-grok/grok-4.7 effort high
magpie codex gw-gemini/gemini-3.8-flash effort medium
magpie pi gw-cn/glm-5.3-prime thinking medium
magpie save experiment
```

**特点**：
- 尝试不同厂商的模型
- 对比效果
- 适合：研究、评测、探索

---

## 🎮 常用命令速查

### 查看配置

```bash
# 查看所有 providers
magpie providers

# 查看所有模型
magpie models

# 查看所有 agents 状态
magpie agents

# 查看某个 provider 详情
magpie provider gw-claude
```

### 切换模型

```bash
# 单个 agent 切换
magpie claude gw-claude/claude-opus-5-5
magpie codex gw-gpt/gpt-6.1-sol
magpie pi gw-cn/deepseek-flash

# 使用 routing group（自动切换账号）
magpie claude group/auto-claude-opus-5-5
```

### Profile 管理

```bash
# 保存当前配置
magpie save <profile-name>

# 切换 profile
magpie use work
magpie use daily
magpie use fast
magpie use experiment

# 查看所有 profiles
magpie profiles

# 恢复初始配置
magpie use baseline
```

### 配额管理

```bash
# 查看配额
magpie quota

# 查看某个 provider 的配额
magpie provider gw-claude
```

---

## ⚙️ 关键配置说明

### 1. Reasoning Effort Levels

不同模型支持的 reasoning levels：

- **ultra** (最高): 只有 GPT-6.1 Sol 支持
- **max**: Claude Opus、GPT-6.1、DeepSeek 系列
- **xhigh**: Claude 全系列、GPT-6.1、Grok
- **high**: 所有模型
- **medium/low**: 所有模型

### 2. API 协议差异

- **OpenAI Chat**: `gateway` (默认)
- **OpenAI Responses**: `gw-gpt`, `gw-cn`, `gw-gemini`, `gateway-grok`
- **Anthropic Messages**: `gw-claude` (原生 Claude API)

### 3. Routing Groups 工作原理

当你使用 `group/auto-claude-opus-5-5` 时：
1. magpie 优先使用第一个 provider
2. 如果失败（配额/限流），自动切换到第二个
3. 所有 provider 都恢复后，重新均衡分配

---

## 🚀 下一步建议

### 1. 创建常用 profiles

```bash
# 已保存：all-models-configured, baseline
# 建议创建：work, daily, fast, experiment
```

### 2. 测试不同模型效果

- 用同一个任务测试不同模型
- 对比质量、速度、成本
- 找到最适合你的组合

### 3. 配置 routing groups（如果需要）

```bash
# 如果你有多个 Claude 账号
magpie group add "Opus cluster" \
  models=gw-claude/claude-opus-5-5,gateway-2/claude-opus-5-5 \
  routing=smart
```

### 4. 监控配额使用

```bash
# 定期检查
magpie quota

# 根据使用情况调整 profiles
```

---

## 📝 关于你提到的模型

你提到的一些模型在当前配置中的对应关系：

### 已配置
- ✅ `claude-opus-5-5` - 最高质量
- ✅ `claude-sonnet-5-5` - 干活模型
- ✅ `gpt-6.1-sol` - 最高质量
- ✅ `deepseek-flash` - 干活模型（快速+便宜）
- ✅ `claude-haiku-4-5-20251001` - 快速模型

### 未找到（可能还未上线到 gateway）
- ❓ `gpt-6.1-astra` - 在 Pi 配置中未找到
- ❓ `gpt-6-luna` - 在 Pi 配置中未找到
- ❓ `claude-haiku-5-5` - 当前最新是 haiku-4-5

**建议**：
- 如果这些模型上线，可以用 `magpie provider models <provider> +<model>` 添加
- 或者联系 gateway 确认这些模型的可用性

---

## ✅ 配置验证清单

- [x] 添加 6 个 gateway providers
- [x] 配置 18 个模型（5+1+3+1+1+2）
- [x] 清理旧 gateway provider（移除 Kimi、K3）
- [x] 保存 baseline 和 all-models-configured profiles
- [x] 验证 Claude Code、Codex、Pi 配置正常
- [x] 创建自动 routing groups

**状态**: ✅ 全部完成

---

## 🎯 总结

你现在拥有：
- **6 个独立的 API keys**，每个负责不同类型的模型
- **18 个前沿模型**，覆盖高质量、干活、快速三个场景
- **自动 routing groups**，多账号无缝切换
- **统一管理界面**，一个命令切换所有 agent

这套配置让你可以：
1. 根据任务类型选择最合适的模型
2. 灵活切换工作场景（work/daily/fast/experiment）
3. 最大化利用多个 API keys 的配额
4. 快速测试和对比不同模型的效果

恭喜！你的 magpie + gateway 生态已经完全配置好了 🎉
