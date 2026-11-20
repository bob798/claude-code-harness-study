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
