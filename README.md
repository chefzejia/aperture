# Agentic Work Infra

研究人和 Agent 如何在真实任务中共享材料、工作规则和当前上下文，完成可检查、可继续使用、失败后可以接管的结果。

本项目维护两类共性能力：

- **知识库**：材料如何进入、整理、复用、检索和更新；
- **Skill**：一类工作应该怎样做、怎样检查和何时停下。

企业知识库、个人知识库、投标和其他业务都是场景。场景可以选择不同目录、字段、权限、载体和 Agent，但不能改变共同边界。

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

场景材料用于验证共同模型，不反过来定义项目的全局结构。

## 方法

- [项目 Agent 入口](AGENTS.md)
- [Agent 治理规范](docs/governance/agent-governance.md)
- [Agent 调试与真实 E2E](docs/governance/debugging-standard.md)

## 目录

```text
agentic-work-infra/
├── AGENTS.md
├── docs/
│   ├── core/                 # 共性模型和共性方法
│   ├── governance/           # 项目治理与验证方法
│   ├── scenarios/            # 企业、个人、投标等场景材料
│   └── training/             # 面向人的培训材料
└── tracks/
    └── knowledge-base/       # 可执行的知识库 Skill
```

[Apache License 2.0](LICENSE)
