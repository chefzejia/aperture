# Agentic Work Infra

企业人机协同工作的基础设施。

## 核心命题

**Agent App的能力已经趋同，真正的差异在于给AI的业务操作手册（Skill）和可复用的企业知识。**

## 项目内容

### Skill

- [知识库Skill](tracks/knowledge-base/SKILL.md) - 教AI建库、用库、整理库
- [Skill设计最佳实践](docs/skill-design.md) - 如何设计和迭代Skill

### 治理方法

- [Agent治理规范](docs/governance/agent-governance.md) - AGENTS.md怎么写、Correct Simplicity原则
- [Agent调试与E2E](docs/governance/debugging-standard.md) - 自主调试、三证据面、根因定位

### 培训材料

- [知识库培训](docs/training/知识库培训.html) - 面向业务人员
- [Skill培训](docs/training/Skill培训.html) - 面向AI协调员

### 解决方案

- [知识库到投标业务打通](docs/solutions/打通方案-知识库到投标.md) - 两层结构+投标Skill

## 项目结构

```
agentic-work-infra/
├── docs/
│   ├── skill-design.md          # Skill设计最佳实践
│   ├── governance/              # 治理方法
│   ├── training/                # 培训材料
│   └── solutions/               # 解决方案
└── tracks/
    └── knowledge-base/
        └── SKILL.md
```

## 许可证

[Apache License 2.0](LICENSE)
