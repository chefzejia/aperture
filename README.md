# Agentic Work Infra

本项目研究一个共同问题：**人和 Agent 如何通过同一套可观察的知识理解同一件事，并在明确的工作规则下完成可检查、可继续使用、失败后可以接管的任务。**

项目的共性主线只有一条：

```text
Markdown 知识文件
  ├── 正文：人和 Agent 共同理解的内容
  ├── Frontmatter：这篇笔记的属性
  ├── Wiki 链接：知识之间可观察的关系
  └── 图片/附件引用：证据和补充材料的位置
        ↓
Skill 与用户确认的长期工作规则
        ↓
当前任务工作区与项目变量
        ↓
全文搜索、属性过滤、向量检索和 RAG 等可重建辅助能力
```

这里的分工是固定的：

- **知识笔记**记录事情本身。Markdown 正文是共同理解的语义，Frontmatter 跟随笔记记录属性，Wiki 链接表达关系，图片和附件通过可观察引用保留证据位置。
- **Skill 和长期工作规则**记录 Agent 应该如何工作。它们不能代替知识笔记，也不能把一次任务的推断写成企业事实。
- **当前任务工作区**记录这一次的客户、金额、工期、临时要求、草稿和交付物。它可以引用长期知识，但不能自动反写长期知识。
- **检索层**只负责更快找到和使用 Markdown 知识。全文索引、向量索引和 RAG 都可以删除、替换和重建，不能成为第二套知识真相。

原始 Word、PDF、Excel、图片和聊天记录可以很乱，作为证据原样保留。业务处理过程中也可以保留盘点、候选、草稿和失败现场，用于回溯和恢复；它们是工作产物，不是与 Markdown 知识并列的另一套长期架构。

企业知识库、个人知识库、投标和其他业务都是场景。场景可以增加自己的目录、字段、权限和工作规则，但不能改变共同知识表达，也不能把场景做法提升为全局要求。

## 先读

- [Agentic Work 的共同模型](docs/core/agentic-work-model.md)
- [知识库的共同底层框架](docs/core/knowledge-base-framework.md)
- [知识库 Skill](tracks/knowledge-base/SKILL.md)
- [Skill 设计最佳实践](docs/core/skill-design.md)

## 场景材料

- [知识库场景对照](docs/scenarios/知识库场景对照.md)
- [企业知识库场景](docs/scenarios/企业知识库.md)
- [投标工作流场景](docs/scenarios/投标工作流.md)
- [知识库培训](docs/training/知识库培训.html)
- [Skill 培训](docs/training/Skill培训.html)

场景材料用于验证共同模型，不与核心文档形成第二条主线。

## 方法

- [项目 Agent 入口](AGENTS.md)
- [Agent 治理规范](docs/governance/agent-governance.md)
- [Agent 调试与真实 E2E](docs/governance/debugging-standard.md)

## 目录

```text
agentic-work-infra/
├── AGENTS.md
├── docs/
│   ├── core/                 # 唯一的共性模型和方法
│   ├── governance/           # 治理与验证方法
│   ├── scenarios/            # 企业、个人、投标等场景材料
│   └── training/             # 面向人的培训材料
└── tracks/
    └── knowledge-base/       # 可执行的知识库 Skill
```

[Apache License 2.0](LICENSE)
