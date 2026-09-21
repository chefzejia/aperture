# Agentic Work Infra

> **Agent 时代的知识库，首先要构建一个人类和 Agent 都能同时观测、操作、修正、演化的共同知识对象，让知识在使用中持续积累。**

## 这个项目研究什么

本项目研究的不是“怎样给 Agent 建一个更快的搜索系统”，也不是先选一个数据库或知识图谱。我们研究的是：

> **如何让人和 Agent 面对同一个知识状态，共同理解一件事，并在真实工作中持续把它修正、复用和积累下来。**

这就是项目的第一性原理。个人知识库、企业知识库、投标、研发和客服只是不同的验证场景。

## 从原则到当前实现

共同知识对象需要同时满足四件事：

- 人能看见和理解；
- Agent 能读取和操作；
- 任何结论都能回到来源并接受修正；
- 每次使用产生的确认、纠正和新内容能够回到同一个对象中。

当前项目选择用本地 Markdown 文件承载这个对象：

```text
Markdown 文件
  ├── 正文：人和 Agent 共同理解的语义
  ├── Frontmatter：跟随笔记保存的属性
  ├── Wiki 链接：人和 Agent 都能看到的关系
  └── 图片/附件引用：证据和补充材料的位置
        ↓
Skill 与用户确认的长期工作规则
        ↓
当前任务工作区与项目变量
        ↓
全文搜索、属性过滤、向量检索和 RAG 等可重建辅助能力
```

这段图描述的是当前实现，不是第一性原理。Markdown 可以替换，底层原则不能被替换成“只让 Agent 查得快”。

## 三类内容的边界

- **共同知识对象**记录事情本身。正文写语义，Frontmatter 写这篇笔记的属性，Wiki 链接写关系，附件引用保留证据位置。
- **Skill 和长期工作规则**记录 Agent 应该如何工作。它们可以操作知识对象，但不能把一次任务的推断写成企业事实。
- **当前任务工作区**记录这一次的客户、金额、工期、临时要求、草稿和交付物。它可以引用长期知识，但不能自动反写长期知识。

原始 Word、PDF、Excel、图片和聊天记录可以很乱，先作为输入和证据保留。业务处理过程中也可以保留盘点、候选、草稿和失败现场用于回溯；这些是工作产物，不是另一套长期知识架构。

## 检索和工具的位置

目录、标题、全文搜索和属性过滤是最先使用的查找方式。向量索引、混合检索和 RAG 只有在真实查询中暴露出需要时才增加：

- 向量索引帮助按含义寻找；
- RAG 负责先取资料，再基于资料回答；
- 二者都可以删除、替换和重建；
- 二者都不能成为人看不到、无法核对和无法维护的第二套知识。

Obsidian 是观察和维护 Markdown 文件的一种界面，不是知识本身。换工具时，共同知识对象仍然应该能被人和 Agent 继续使用。

## 先读

- [Agentic Work 的共同模型](docs/core/agentic-work-model.md)
- [知识库共同底层框架](docs/core/knowledge-base-framework.md)
- [知识库 Skill](tracks/knowledge-base/SKILL.md)
- [Skill 设计最佳实践](docs/core/skill-design.md)

## 场景材料

- [知识库场景对照](docs/scenarios/知识库场景对照.md)
- [企业知识库场景](docs/scenarios/企业知识库.md)
- [投标工作流场景](docs/scenarios/投标工作流.md)
- [知识库培训](docs/training/知识库培训.html)
- [Skill 培训](docs/training/Skill培训.html)

场景和培训材料用于验证、解释和教会这条主线，不与核心文档形成第二条主线。

## 方法

- [项目 Agent 入口](AGENTS.md)
- [Agent 治理规范](docs/governance/agent-governance.md)
- [Agent 调试与真实 E2E](docs/governance/debugging-standard.md)

## 目录

```text
agentic-work-infra/
├── AGENTS.md
├── docs/
│   ├── core/                 # 共性原则和当前实现
│   ├── governance/           # 治理与验证方法
│   ├── scenarios/            # 企业、个人、投标等场景材料
│   └── training/             # 面向人的培训材料
└── tracks/
    └── knowledge-base/       # 可执行的知识库 Skill
```

[Apache License 2.0](LICENSE)
