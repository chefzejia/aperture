# 模板使用指南

这些模板帮助项目保持结构一致，降低 Agent 理解成本。

## 核心模板

### README.md
**必需** | 每个项目都要有

**内容**：
- 项目是什么
- 如何运行、测试
- 目录结构
- 常用命令

**参考**：`readme.md`

---

### AGENTS.md
**必需** | 每个项目都要有

**内容**：
- 项目定位和边界
- 架构约束（不可违反）
- 验证命令
- 文档路由

**参考**：`agents.md`

---

### HANDOFF.md
**推荐** | 有交接需求时使用

**内容**：
- 当前状态
- 下一步要做什么
- 已知问题

**何时创建**：
- 项目有多人/Agent 协作
- 需要跨会话工作
- 需要明确"下一步"

**参考**：`handoff.md`

---

## 架构文档

### ARCHITECTURE.md
**可选** | 中等复杂度项目

**何时需要**：
- 项目有 3-5 个子系统
- 有重要的架构决策需要记录
- 有复杂的数据流或状态转换

**何时不需要**：
- 简单项目（结构一目了然）
- README 已经足够

**何时升级到目录结构**：
- 子系统 > 5 个
- 架构决策 > 10 个
- 需要频繁更新架构
- 团队规模 > 5 人

**升级方式**：
```
docs/architecture/
  ├── overview.md         # 架构概览
  ├── subsystems/         # 各子系统设计
  │   ├── auth.md
  │   └── storage.md
  ├── data-flow.md        # 数据流
  ├── deployment.md       # 部署架构
  └── adr/                # 架构决策记录
      ├── 0001-use-sqlite.md
      └── 0002-event-sourcing.md
```

**参考**：`architecture.md`

---

### ADR (Architecture Decision Record)
**可选** | 需要记录重要决策时使用

**何时写 ADR**：
- 决策影响多个子系统
- 决策有显著的技术或业务代价
- 在几个方案间难以选择
- 需要向未来的自己解释"为什么这样做"

**何时不写**：
- 显而易见的选择
- 局部实现细节
- 临时解决方案

**存放位置**：
- 简单项目：放在 `ARCHITECTURE.md` 的"关键决策"部分
- 复杂项目：`docs/architecture/adr/NNNN-title.md`

**命名规则**：
- `0001-use-sqlite.md`
- `0002-event-sourcing.md`
- 用 4 位数字编号，按时间顺序递增

**参考**：`adr.md`

---

## 设计文档

### DESIGN.md
**可选** | 有视觉输出的项目

**何时需要**：
- 项目有视觉界面（网站、产品、文档、演示）
- 需要让 AI 记住品牌色、字体、气质
- 有明确的设计约束或禁用风格

**何时不需要**：
- 纯后端项目，无视觉界面
- 完全依赖现成 UI 库
- 设计系统已在 Figma 等工具中完整定义

**内容**：
- 项目气质
- 颜色、字体、排版
- 组件规范
- 布局原则
- 禁用风格

**注意**：这是给 AI 读的设计规范，不是架构文档

**参考**：`design.md` | [gateway.com/docs/agent-memory/remember-design](https://gateway.com/docs/agent-memory/remember-design)

---

## 其他模板

### LESSONS.md
**可选** | 记录教训和改进

**内容**：
- 遇到的问题
- 解决方案
- 学到的经验
- 下次如何避免

**参考**：`lessons.md`

---

## 模板使用建议

### 最小配置（所有项目）
```
project/
  ├── README.md           # 项目说明
  └── AGENTS.md           # Agent 协同规范
```

### 标准配置（中等项目）
```
project/
  ├── README.md
  ├── AGENTS.md
  ├── HANDOFF.md          # 当前状态和下一步
  └── ARCHITECTURE.md     # 架构概览
```

### 完整配置（复杂项目）
```
project/
  ├── README.md
  ├── AGENTS.md
  ├── HANDOFF.md
  ├── DESIGN.md           # 如果有视觉输出
  └── docs/
      ├── architecture/
      │   ├── overview.md
      │   ├── subsystems/
      │   └── adr/
      └── research/
```

---

## 文档维护原则

1. **README 优先**：最基础的信息先写在 README
2. **按需创建**：只在需要时创建额外文档
3. **避免重复**：同一信息不要写在多个地方
4. **保持同步**：改了代码要同步更新文档
5. **可删除**：过时的文档要及时删除或归档

---

## 文档职责对比

| 文档 | 职责 | 更新频率 | 必需性 |
|------|------|---------|-------|
| **README** | 项目说明、如何运行 | 低 | 必需 |
| **AGENTS** | 架构约束、验证命令 | 低 | 必需 |
| **HANDOFF** | 当前状态、下一步 | 高 | 推荐 |
| **ARCHITECTURE** | 架构组成、关键决策 | 中 | 可选 |
| **ADR** | 单个架构决策记录 | 低 | 可选 |
| **DESIGN** | 视觉设计规范 | 低 | 可选 |
| **LESSONS** | 经验教训 | 低 | 可选 |

---

## 进一步阅读

- [Agent 项目协同规范](../agent-governance.md)
- [人机协同模型](../../core/agentic-work-model.md)
