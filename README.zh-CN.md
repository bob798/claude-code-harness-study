# Claude Code Harness Study

围绕 Claude Code 的公开资料开展**证据驱动的架构研究**，独立实现 Agent Harness 机制，并用可复现实验检验工程取舍。

本仓库不是 Claude Code 源码镜像、官方项目或功能替代品，不传播泄露或专有源码。

## 从哪里开始

1. 阅读 [Agent Loop 分析](docs/01-agent-loop/analysis.md)。
2. 对照 [证据登记](docs/01-agent-loop/evidence.md)，区分官方事实、第三方分析、假设与实验结果。
3. 运行 `python -m unittest discover -s experiments/loop_recovery -v`。
4. 查看 [PLAN.md](PLAN.md) 中的下一轮问题。

**第一轮实验**：工具已经发生副作用，但结果返回丢失。比较无条件重试和带稳定幂等键的重试。注意：这是独立 Mock 实验，不能据此声称 Claude Code 具有相同行为。

研究节奏：一个问题、一份分析、一组对照实验、一个小 PR。

## R1 第二轮：类型化状态不等于执行安全

[实验报告](research/02-agent-loop/R1-ITERATION-02.md) · [研究方向调整记录](research/02-agent-loop/DECISION_LOG.md)

将三种实现对比：局部变量、类型化 State、类型化 State + 转换校验。258 条短事件序列中，前两者均有 249 条接受了不允许的事件；加入规则校验后为 0 条。此结果只针对人为定义的事件模型，并非 Claude Code 实测。推荐使用“执行安全约束”，首次说明其形式化概念为 *Invariant*。

## R1-03：崩溃与取消恢复

[实验报告](research/02-agent-loop/R1-ITERATION-03.md) · [模型和源码依据说明](research/02-agent-loop/MODEL_AND_SOURCE_PROVENANCE.md) · [研究决策日志](research/02-agent-loop/DECISION_LOG.md)

本轮**不调用任何 LLM**。五个脚本化事件场景显示：同等策略下，类型化 State 与普通局部状态表现一致；Checkpoint 保存取消状态后，重启不再发起新的已取消工具操作，但外部操作已提交、回执丢失时仍需幂等与核对。不是 Claude Code 运行实测。
