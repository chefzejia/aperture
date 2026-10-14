<!-- reviewed-through: <commit-hash> (YYYY-MM-DD) -->
# Lessons from Work

记录重复出现的失败模式。出现 3 次后晋升到 `docs/STANDARDS.md`（AGENTS.md 保持入口角色，不收规则）。

## 使用说明

**何时记录**：
- Agent 修复了前一周/两周内出现过的同一问题
- 同一类型错误出现多次

**记录格式**：
```markdown
### [具体规则名称]

**规则**：[一句话说应该怎么做]
- 证据1：<commit/任务标识> + 简要说明
- 证据2：...
- Seen N× (YYYY-MM-DD, YYYY-MM-DD, ...)
- 做对示例：<commit/任务标识>（这条规则被正确执行的一次，可模仿）
```

"做对示例"让规则可模仿而不只是可回避；没有时可省略此行。

**晋升标准**：
- 出现 ≥3 次 → 移到 `docs/STANDARDS.md` 的对应小节
- 在此保留引用（规则名 + 指向 STANDARDS 的位置）

---

## [分类1：如"需求理解"]

### [规则占位符 - 删除此示例]

**规则**：[应该怎么做]
- 证据1：commit abc123 + 修复了边界判断错误
- 证据2：commit def456 + 又一次边界错误
- Seen 2× (2024-01-15, 2024-01-20)

---

## 已晋升规范

以下规则已晋升到 STANDARDS.md，此处保留引用：

- [规则名称] → 见 docs/STANDARDS.md 对应小节
