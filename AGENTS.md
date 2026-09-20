# Agentic Work Infra Agent Guide

适用范围：整个 `agentic-work-infra` 仓库。

## 先读

1. `README.md`：项目入口；
2. `docs/core/agentic-work-model.md`：项目共同模型；
3. `docs/core/knowledge-base-framework.md`：知识库共同框架；
4. `tracks/knowledge-base/SKILL.md`：知识库的可执行规则；
5. 任务涉及具体业务时，再读取对应的 `docs/scenarios/` 或 `docs/training/` 文件。

## 项目边界

- 本仓库研究共性模型、可执行 Skill、场景材料和验证方法，不保存客户原件、凭证、未脱敏业务资料或真实项目输出；
- 知识库、Skill、Agent 和任务工作区是不同角色，不把其中一个场景写成全局结构；
- 原始材料、整理结果、当前任务内容和最终结果要能区分；
- 不确定、冲突或过期内容不能被写成确定答案；
- 自动处理必须可观察、可恢复，不能静默覆盖原始材料；
- Agent 只修改明确授权的范围；
- 不因为某个场景暂时需要，就把固定目录、字段、载体、模型或高级检索技术提升为全局要求；
- 场景方案必须经过至少一个不同场景的对照，才能进入共同模型。

## 修改和验证

修改前先查看：

```bash
git status --short --branch -uall
```

文档修改完成后至少运行：

```bash
git diff --check
```

还要检查：

- 文档链接目标是否存在；
- 示例路径是否被误写成全局要求；
- 核心文档是否能在不读取企业或投标材料的情况下独立理解；
- 同一条共同原则是否在多个文件中产生互相冲突的说法；
- 场景文件是否明确自己的适用范围。
