# 通用工作标准（本仓形态：指向真源）

本仓库是标准的**真源仓库**，不复制 `templates/standards.md`（避免真源与副本双写漂移）。本仓一切任务的执行标准 = [templates/standards.md](governance/templates/standards.md) 全文，复制到其他项目时该文件即为 `docs/STANDARDS.md`。

**本仓特有裁决**（真源仓库的项目级约束）：

- 标准正文只改 `templates/standards.md` 一处；AGENTS.md 只保留入口级摘要和路由，不复制标准条文
- 本仓的 LESSONS（`docs/LESSONS.md`）晋升出口 = `templates/standards.md`（即真源本身，见 LESSONS 使用说明）
- 文档级验证命令（替代代码项目的测试套件）：

```bash
git status --short --branch -uall
git diff --check
# 链接检查：全仓 Markdown 相对链接目标存在
```
