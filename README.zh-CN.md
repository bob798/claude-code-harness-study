# Claude Code Harness Study

围绕 Claude Code 的公开资料开展**证据驱动的架构研究**，独立实现 Agent Harness 机制，并用可复现实验检验工程取舍。

本仓库不是 Claude Code 源码镜像、官方项目或功能替代品，不传播泄露或专有源码。

**[研究规则（L1–L6）](RESEARCH_RULES.md)** · **[调研资料与引用目录](references/README.md)**

## 研究规则：六级能力、六问法与学术出处

[**RESEARCH_RULES.md**](RESEARCH_RULES.md) 明确 L1 概念理解到 L6 业务落地的最低证据要求，并规定每项机制必须回答“问题、基线、不足、替代、取舍、验证”六个问题。实验必须满足本文件内的 [研究流程与证据分级](RESEARCH_RULES.md#10-研究工作流8-个执行动作) 及 [G0/G1/G2 准入门槛](RESEARCH_RULES.md#14-g0g1g2-研究准入门槛)，不得把 Mock 测试、第三方源码解读或模型自称完成当作真实效果验证。

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

## A0-02 · 真实 Claude Code 行为观察

[研究报告](research/A0-01-agent-loop-path/A0-02-REPORT.md) · [安全采集步骤](research/A0-01-agent-loop-path/a0_02/RUNBOOK.md)

官方 CLI 支持 `stream-json` 工具调用与结果事件。但当前研究环境缺少 `claude` 可执行文件和认证信息，因此**没有执行任何真实 Claude Code 任务**；本轮完成事件摘要工具及 4 个合成数据单元测试。下一步需在具备 Claude Code 的独立环境采集匿名化真实轨迹。

## A0-02b · 公开真实会话数据路线

[公开样本核查报告](research/A0-01-agent-loop-path/A0-02B-REPORT.md) · [数据来源](research/A0-01-agent-loop-path/a0_02/DATA_SOURCES.md) · [Session JSONL 解析器](research/A0-01-agent-loop-path/a0_02/session_analyzer.py)

已检查 Trace Commons 上的 Claude Code v2.1.177 公开会话展示，能看到工具调用与中断标记。当前环境无法下载完整原始文件，因此**未宣称完成真实会话全量指标统计**。新增适配器与 5 项合成数据测试均已完成；下一步需要固定数据集版本并取得可复算的摘要。

## A0-03 · Claude Code v2.1.88 源码证据核验

[源码分析报告](research/A0-03-source-control-flow/REPORT.md) · [证据与函数登记](research/A0-03-source-control-flow/SOURCE_CLAIMS.md)

已核验 v2.1.88 意外发布 Source Map 的历史事件，并读取固定版本的两份第三方架构分析。目前并**未**独立取得、校验和检查原始 Source Map，因此暂时没有任何函数级事实升级为“经源码核验（S）”；所有内部函数对应关系仍标为第三方分析（T）。允许将经验证源码作为强证据，但不意味着可以再分发专有源码。

## A0-03b：复用社区结论并比较替代设计

[现有研究清单](research/A0-03-source-control-flow/COMMUNITY_REUSE.md) · [七种 Loop 架构及取舍](research/A0-03-source-control-flow/ALTERNATIVE_DESIGNS.md) · [可证伪对照实验计划](research/A0-03-source-control-flow/EVALUATION_PLAN.md)

已有社区对 Claude Code v2.1.88 进行系统性分析；OpenHands、Goose、LangGraph 提供不同的单步事件、可重入状态机及显式图/函数式持久化实现。现有阅读证据**不能证明** Claude Code 的 while Loop 因其结构而具有更高成功率或更低成本。后续只做严格控制变量的最小比较，不重复构造大型框架。

## A0-04：轻量 Loop 与可重入单步的首次公平对照

[实验报告](research/A0-04-loop-comparison/REPORT.md) · [代码](experiments/a0_04_loop_comparison/experiment.py) · [结果](results/a0-04-pilot.json)

本地 4 项测试通过，真实子进程在第二轮完成持久化后被 SIGKILL 终止，再由新进程从保存状态恢复。两种控制方式都正确完成（5 次脚本决策、4 个模拟工具效果）；**同等 Checkpoint 条件下，不能把恢复能力归功于可重入结构本身。** 未调用任何 LLM 或真实 Goose/Claude Code。另核实 Goose 可重入 GDK 已正式实现并发布，不再只是设计提案。

## A0-04-03 公开基准适配与架构文章审计

[基准适配研究报告](research/A0-04-loop-comparison/A0-04-03-REPORT.md) · [Vikash Rungta 架构文章核查](research/A0-03-source-control-flow/RUNGTA_ARTICLE_AUDIT.md)

本地 11 项测试通过；两种独立模拟控制器分别通过 21 个 AgentBench **衍生输入向量**和 10 个本地扩展审批边界场景。这不是上游官方基准得分，也未调用真实 Claude Code/Goose。发现独立快照下取消与审批竞争可导致过期执行的构造反例。Rungta 2026-02-17 的文章适合研究模型自主性与 Harness 强制约束；不能作为 v2.1.88 泄露源码的直接证据。**模型决策权和 Loop 可重入性是两个独立架构维度。**

## A0-05：扩展 Claude Code Harness 研究资料（2026-11-21）

[12 份优先参考资料（独立 Markdown）](references/TOP_12_REFERENCES.md) · [31 项参考资料与证据审计](research/A0-05-literature-expansion/SEARCH_REPORT.md) · [优先阅读路径及下一步实验](research/A0-05-literature-expansion/PRIORITY_PATH.md)

本轮新增官方 Loop 触发/停止类型、Managed Agents 事件会话设计、Auto Mode 权限拒绝反馈、上下文重置与独立评估器，并梳理同模型受控 Harness 研究。Loop 触发/停止、模型决策权、运行时可重入、状态/上下文、权限与独立任务验收应拆成独立实验维度。目前没有证据证明 `while` 控制语法本身必然优于可重入 `step`。建议优先进行“模型宣称完成 vs 独立验收”的对照实验；可重入性继续独立测控制权交接与开销。
