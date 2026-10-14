# Research 目录

**最小有效结构原则**：只保留有独特价值的文档，删除重复和过时内容。

**事实核查**：2026-10-13 对全部文档做过一轮 GitHub API / 官网复核。无法核实的用户体验转述已标注为未验证；数字类声明已按实测更新。后续新增调研文档应注明来源和核查方式。

---

## 📖 核心文档（必读）

### 1. [多Agent协同与ComputerUse-总结.md](./多Agent协同与ComputerUse-总结.md)
**入口文档** - 从这里开始

**内容**：
- 多 Agent 管理工具（Herdr、LangGraph、CrewAI）
- Computer Use 技术对比
- Claude Code ↔ Codex 协同方案
- 调研局限和改进建议

**何时读**：现在立即读

---

### 2. [herdr-调研.md](./herdr-调研.md)
**深度技术文档**

**内容**：
- Herdr 的核心定位（运行时 vs 编排框架）
- 与 LangGraph/CrewAI 的本质区别
- Claude Code 调用 Codex 的具体实现方案
- 技术架构和配置指南

**何时读**：需要理解 Herdr 或实现 Agent 协同时

---

### 3. [我的agents清单.md](./我的agents清单.md)
**工具清单**

**内容**：
- 已安装的所有 Agent 工具
- 快速参考

**何时读**：想查看有哪些工具时

---

## 📚 magpie 系列（参考）

### 4. [magpie-完整配置总结.md](./magpie-完整配置总结.md)
**配置指南**

**内容**：
- magpie 的完整配置步骤
- 实际使用案例

**何时读**：需要配置 magpie 时

---

### 5. [magpie-深度分析.md](./magpie-深度分析.md)
**架构文档**

**内容**：
- magpie 的架构设计和实现原理
- 技术深度分析

**何时读**：想深入理解 magpie 原理时

---

### 6. [magpie-人机协同研究.md](./magpie-人机协同研究.md)
**理念结合**

**内容**：
- magpie 与本项目人机协同理念的结合
- 设计思考

**何时读**：研究人机协同模型时

---

### 7. [magpie-九个深度问题.md](./magpie-九个深度问题.md)
**高级参考**

**内容**：
- magpie 的高级问题和解答
- 疑难场景处理

**何时读**：遇到高级配置问题时

---

## 🎯 阅读路径

### 快速了解（15分钟）
1. [多Agent协同与ComputerUse-总结.md](./多Agent协同与ComputerUse-总结.md) - 完整阅读
2. [我的agents清单.md](./我的agents清单.md) - 快速浏览

### 实现 Agent 协同（1小时）
1. [多Agent协同与ComputerUse-总结.md](./多Agent协同与ComputerUse-总结.md) - 理解方案
2. [herdr-调研.md](./herdr-调研.md) - 深入技术细节
3. 开始实践

### magpie 专题（1小时）
1. [magpie-完整配置总结.md](./magpie-完整配置总结.md) - 配置
2. [magpie-深度分析.md](./magpie-深度分析.md) - 原理
3. [magpie-九个深度问题.md](./magpie-九个深度问题.md) - 按需查阅

---

## 📊 文档统计

- **总文档数**：7个
- **核心文档**：3个
- **magpie 系列**：4个
- **总大小**：约 100KB

---

## 🧹 清理记录

**已删除的重复/过时文档**：
- 调研总结-多Agent协同与ComputerUse.md（被新总结覆盖）
- 跨Agent协同方案研究.md（整合到新总结）
- 多Agent管理工具调研.md（整合到新总结）
- Computer-Use技术对比.md（整合到新总结）
- computer-use-实际体验对比.md（整合到新总结）
- README.md（旧版索引）
- archive/（过时文档归档）

**清理原则**：
- 多个文档讲同一主题 → 合并为一个
- 早期版本被新版本覆盖 → 删除旧版本
- 临时记录和过程文件 → 删除
- 保留有独特价值的深度文档

---

## 🔗 相关文档

- [人机协同模型](../core/agentic-work-model.md)
- [Agent 项目协同规范](../governance/agent-governance.md)
