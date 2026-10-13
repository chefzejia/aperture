# 多 Agent 协同与 Computer Use 调研

最后更新：2025-01-13

---

## 核心发现总结

### 1. 多 Agent 管理工具

**Orca 和 Herdr 的真相**：
- ❌ **Orca**：是 Spinnaker 的 CI/CD 编排引擎，与 AI Agent 管理无关
- ✅ **Herdr**（https://herdr.dev/）：是编码 Agent 的**运行时**，专门解决 Agent 后台持久化运行的问题

**主流多 Agent 框架**：
- **LangGraph**：低层级编排框架，混合确定性和 Agent 步骤，适合需要精细控制的复杂工作流
- **CrewAI**：高层抽象的多 Agent 框架，基于角色的团队协作，与 Claude Code 深度集成
- **Herdr**：运行时基础设施，让 Agent 能后台运行、断开重连、跨机器访问

**关键区别**：
- **Herdr** 解决"Agent 在哪里运行、如何持久化"
- **LangGraph/CrewAI** 解决"Agent 如何协作、状态如何管理"
- 两者不冲突，Herdr 可作为 LangGraph/CrewAI 的底层运行时

### 2. Computer Use 实际体验

**调研局限**：
- ❌ 无法访问 X/Twitter、Reddit、YouTube、Hacker News
- ❌ OpenAI 官方文档被墙（HTTP 403）
- ✅ 仅能访问 Anthropic 官方文档和 GitHub

**Claude Computer Use（已验证）**：
- 2024年10月公开 Beta
- 官方承认"实验性、缓慢、容易出错"
- OSWorld 基准：14.9%（最佳成绩）
- 不支持拖拽、缩放等基本操作

**GPT Computer Use（用户报告"断档领先"）**：
- ⚠️ 无法通过公开渠道验证
- ⚠️ 未找到官方 API 文档或技术规格
- ⚠️ 用户体验数据无法获取（社交媒体被墙）

**结论**：
- 用户的实际体验（"GPT 丝滑，Claude 触发困难"）无法通过当前调研工具验证
- 建议在 Codex（能访问 X/Reddit）中重新调研用户体验对比

### 3. Herdr 的独特价值

**核心定位**：终端运行时 + Agent 感知层

**关键特性**：
- 后台持久化：关闭窗口、断网后 Agent 继续工作
- Agent 生命周期管理：working、blocked、idle、done
- 跨机器访问：一个 Herdr 管理多台机器的 Agent
- 多客户端连接：TUI、CLI、SSH 可随时连接/断开

**适用场景**：
- ✅ 让 Claude Code 调用 Codex 并后台运行
- ✅ 管理多个编码 Agent 的持久化会话
- ✅ 跨机器的 Agent 协同

**与 LangGraph/CrewAI 的关系**：
- 不冲突，可以组合使用
- Herdr 提供运行时，LangGraph/CrewAI 提供编排逻辑

---

## 技术方案分析

### 方案 1：Codex + magpie 换模型

**目标**：保留 Codex 的基础设施，使用 Claude Opus 5.5 模型

**可行性**：需要验证
- Codex 是否支持 Anthropic API 格式？
- magpie 的 API 转换是否完整？
- Computer Use 是否依赖 GPT 特性？

**验证步骤**：
```bash
magpie codex gateway/claude-opus-5-5
codex app-server daemon restart
# 测试 Computer Use、浏览器调试、推理质量
```

### 方案 2：Claude Code 调用 Codex（通过 Herdr）

**Herdr 是唯一专门为此设计的工具**

**架构**：
```
用户 → Claude Code (架构师)
         ↓
      Herdr 管理
         ↓
       Codex (工程师，后台运行)
         ↓
       Computer Use / 浏览器调试
         ↓
      返回结果给 Claude Code
```

**优势**：
- ✅ Herdr 专门支持编码 Agent 间协同
- ✅ 后台持久化，不依赖窗口
- ✅ Agent 状态可观测（working/blocked/idle）
- ✅ 断开重连不影响工作

**挑战**：
- 需要配置 Herdr 环境
- 需要定义 Agent 间的通信协议
- 需要处理上下文传递

### 方案 3：通过 MCP 集成

**Claude Code + MCP Server**

可以开发 Codex MCP Server 封装 Codex 能力，但：
- Codex 的非交互式调用能力未知
- 上下文传递和结果获取的技术方案需要验证
- MCP 不提供持久化和后台运行

**CrewAI 集成**：
- CrewAI 提供官方 Claude Code 插件
- 可用于多 Agent 编排
- 但不解决 Computer Use 基础设施问题

---

## 调研局限与改进建议

### 当前调研工具的局限

**Pi 中的调研能力**：
- ✅ 可以访问官方文档和 GitHub
- ✅ 可以分析技术架构和 API
- ❌ 无法访问社交媒体（X、Reddit）
- ❌ 无法访问被墙的网站（OpenAI 官网）
- ❌ 无法获取真实用户体验

**Codex 中的调研能力**（用户报告）：
- ✅ 可以访问 X/Twitter 帖子
- ✅ 可以访问 Reddit 讨论
- ✅ 可以检索社区反馈
- ✅ 可以获取更全面的信息

### 改进建议

1. **工具分工**：
   - Pi：官方文档、技术架构、代码分析
   - Codex：社交媒体、社区反馈、用户体验

2. **调研充分性标准**：
   - Tier 1（必须）：官网、GitHub、官方文档
   - Tier 2（重要）：X/Twitter、Reddit、HN
   - Tier 3（补充）：技术博客、第三方评测

3. **文档管理原则**：
   - ✅ 保留最新综合总结（单一入口）
   - ✅ 保留深度调研（有独特价值）
   - ❌ 删除重复和过时内容
   - ❌ 避免无限新增

---

## 下一步行动

### 立即验证（本周）

1. **测试方案 1**：
   ```bash
   magpie codex gateway/claude-opus-5-5
   codex app-server daemon restart
   # 验证兼容性和性能
   ```

2. **体验 Herdr**：
   - 安装 Herdr
   - 配置 Codex 在 Herdr 中运行
   - 测试后台持久化和断开重连

3. **在 Codex 中调研 Computer Use 用户体验**：
   - 搜索 X: "chatgpt computer use vs claude"
   - 搜索 Reddit: r/ChatGPT, r/ClaudeAI
   - 找实际用户的对比体验

### 中期探索（2-4周）

1. **研究 Herdr + LangGraph/CrewAI 组合**：
   - Herdr 作为运行时
   - LangGraph 或 CrewAI 作为编排层
   - 验证技术可行性

2. **设计 Claude Code ↔ Codex 协同模式**：
   - 定义角色分工
   - 设计通信协议
   - 建立验收标准

### 长期规划（2-3个月）

1. **建立统一的调试基础设施**：
   - 标准化浏览器调试接口
   - 让所有 Agent 都能使用
   - 降低 Agent 间切换成本

2. **优化 Agent 协同模式**：
   - 清晰的角色分工
   - 稳定的通信机制
   - 低成本的工具调用

---

## 关键问题需要澄清

1. **GPT Computer Use 的准确信息**：
   - 正式名称？（Operator？）
   - 访问方式？（ChatGPT App？API？）
   - 具体的触发方式和使用场景？

2. **Codex 的 browser_local**：
   - 具体是什么？MCP 服务器？内置工具？
   - 配置文件在哪里？
   - 如何调用？

3. **核心需求优先级**：
   - 更快的模型 + Codex 基础设施？
   - 多个 Agent 协同工作？
   - 稳定的浏览器调试？

---

## 参考资料

### 官方文档
- **Herdr**：https://herdr.dev/
- **Herdr GitHub**：https://github.com/herdrdev/herdr
- **LangGraph**：https://python.langchain.com/docs/langgraph
- **CrewAI**：https://docs.crewai.com
- **Claude Computer Use**：https://docs.anthropic.com/en/docs/build-with-claude/computer-use
- **Anthropic Quickstarts**：https://github.com/anthropics/anthropic-quickstarts

### 调研局限
- ❌ X/Twitter、Reddit、YouTube、Hacker News 无法访问
- ❌ OpenAI 官方文档无法访问
- ⚠️ 用户体验数据缺失，需要在 Codex 中补充调研
