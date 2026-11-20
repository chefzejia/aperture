<!-- reviewed-through: <commit-sha> (<YYYY-MM-DD HH:mm +0800>) -->
# Lessons from Merged Work

<!-- 实例化为 docs/LESSONS.md。顶部注释是周期性逆熵审计（Auditor）的提交水位线；记账、审计与 Seen 3× 晋升的分工见 multi-agent-collab Skill。
     每条记录按缺陷背后的「机制」（隐含模型或假设失效）合并计数，顺序固定为：一句话可执行规则（粗体）→ 失效机制与输入维度 → 已观测症状与真实翻车证据（Commit/Issue）→ Seen N× (<日期列表>)。
     晋升后从正文移除，移入底部已晋升列表并保留机制名（已晋升机制复发时直接扩充原守卫测试维度，不重复建 Seen 1×）。实例化时删除本注释与占位符。 -->

## Active Lessons

**<一句话可执行规则，直接写主语与必须满足的动作/禁止项>**
- **失效机制**：<哪个隐含的模型或假设失效；需要覆盖哪些输入维度>
- **症状与翻车证据**：<`<commit-sha>` / `#<issue>` 出现了什么症状，为什么逃过自检，最后在 `<fix-sha>` 如何修复>
- Seen 1× (<YYYY-MM-DD>).

## Moved to Guard Tests / Standards

- **[<机制名>] <已晋升的一句话规则>** → 已固化为守卫测试 `<test_file>:<test_name>`（或 `<目标文档#章节>`）。
