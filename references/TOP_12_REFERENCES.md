# Claude Code Harness 研究：12 份优先参考资料

> **整理日期**：2026-11-22  
> **项目**：[claude-code-harness-study](https://github.com/bob798/claude-code-harness-study)  
> **目的**：复用高质量源码分析与工程研究，围绕 Agent Loop、工具执行、运行时控制、Context 和任务验收，提出可证伪的架构对照实验。  
> **范围说明**：以下是**精选阅读清单**，不是 12 个独立验证结论，也不是我们已经执行过的基准测试。

## 一、快速索引

优先级针对**本项目当前阶段**：**P0** = 直接影响当前研究假设或实验；**P1** = 后续专项研究重要补充。

| 编号 | 资料 | 来源类型 | 优先级 | 最值得提取的内容 |
| --- | --- | --- | --- | --- |
| S01 | [Claude Code from Source](https://github.com/alejandrobalderas/claude-code-from-source) | 第三方源码研究 | P0 | Loop、工具流水线、并发调度的实现设计 |
| S02 | [Claude Code 源码分析（liuup）](https://github.com/liuup/claude-code-analysis) | 第三方源码研究 | P0 | StreamingToolExecutor、runTools、权限与工具结果回注 |
| S03 | [《马书》：驾驭工程](https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding) | 第三方工程技术书 | P1 | Prompt、Context、缓存、安全及生产实践的设计取舍 |
| S04 | [Dive into Claude Code（VILA-Lab）](https://arxiv.org/abs/2604.14228) / [GitHub](https://github.com/VILA-Lab/Dive-into-Claude-Code) | 学术论文 + 源码分析 | P0 | v2.1.88 架构基线、queryLoop、权限和 Context |
| O01 | [Scaling Managed Agents](https://www.anthropic.com/research/managed-agents) | Anthropic 官方研究 | P0 | 持久化事件会话、无状态执行 Harness、故障恢复 |
| O02 | [How We Built Claude Code Auto Mode](https://www.anthropic.com/research/claude-code-auto-mode) | Anthropic 官方工程文章 | P0 | 两阶段操作检查、拒绝反馈、审批与终止边界 |
| O03 | [Harness Design for Long-running Apps](https://www.anthropic.com/research/harness-design-long-running-apps) | Anthropic 官方研究 | P0 | Context 重置、规划/生成/评估分工、独立验收 |
| O04 | [Infrastructure Noise in Agentic Evals](https://www.anthropic.com/research/infrastructure-noise) | Anthropic 官方评测研究 | P0 | 资源环境、超时与运行条件造成的评测混杂 |
| E01 | [Harness or Model?](https://arxiv.org/abs/2609.11987) | 同模型受控对照研究 | P0 | Harness 之间的成对比较、任务分层与置信区间 |
| E02 | [Same Model, Different Harness](https://arxiv.org/abs/2608.26218) | Harness 消融实验 | P0 | Context 压力下的任务完成率与部分进度 |
| E03 | [An Empirical Study of Harness Design for Coding Agents](https://arxiv.org/abs/2609.20804) | 多配置受控实验 | P0 | Planning / Action Space / Context 的条件性收益 |
| E04 | [When Does Restricting a Coding Agent to execute_code Help?](https://arxiv.org/abs/2607.10569) / [代码](https://github.com/hyang0129/onlycodes) | 工具集合消融实验 | P0 | 默认工具、Bash-only、Code-only 的能力/成本取舍 |

**证据判定原则**：源码分析说明“某版本可能如何实现”；官方研究说明“特定团队或产品如何设计”；受控实验说明“在其测试条件下什么机制产生何种效果”。三者不能相互代替。

## 二、Claude Code 的源码与架构分析（4 份）

### S01 — Claude Code from Source

- **地址**：https://github.com/alejandrobalderas/claude-code-from-source
- **建议阅读**：
  - [Chapter 5: Agent Loop](https://github.com/alejandrobalderas/claude-code-from-source/blob/main/book/ch05-agent-loop.md)
  - [Chapter 6: Tools](https://github.com/alejandrobalderas/claude-code-from-source/blob/main/book/ch06-tools.md)
  - [Chapter 7: Concurrent Tool Execution](https://github.com/alejandrobalderas/claude-code-from-source/blob/main/book/ch07-concurrency.md)
- **研究用途**：建立模型响应、工具识别、权限判定、并发分组、结果反馈与停止条件的模块级概念图；与 Goose / OpenHands 的运行时调度作对照。
- **可提取问题**：为什么存在 Streaming Tool Executor 与常规执行路径？并发安全由什么条件决定？工具失败如何反馈到下一轮？
- **限制**：是第三方从源码提炼的技术书，原创示意伪代码不等于已独立核验的 Claude Code 原始源码。

### S02 — Claude Code 源码分析（liuup）

- **地址**：https://github.com/liuup/claude-code-analysis
- **重点章节**：[Tool Call 机制实现细节](https://github.com/liuup/claude-code-analysis/blob/main/analysis/04b-tool-call-implementation.md)
- **研究用途**：查明 `StreamingToolExecutor`、`runTools`、`isConcurrencySafe`、PreToolUse Hooks、Permission 与 `tool_result` 的衔接。
- **可提取问题**：流式提前执行是否缩短首个工具启动延迟？它如何处理不可并发工具及取消？预先检查能否覆盖实际执行参数？
- **限制**：项目展示了泄露源码相关内容；**不要复制、提交或再分发其专有源码文件/压缩包**。其文字性分析仍属于第三方来源。

### S03 — 《马书》：驾驭工程

- **地址**：https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding
- **阅读重点**：架构、上下文管理、Prompt Cache、权限模式、Harness 设计模式与生产实践。
- **研究用途**：从“代码如何组织”过渡到“为什么在生产环境这样组织”，尤其适合归纳 Context 经济性、权限治理和模型/运行时责任边界。
- **可提取问题**：哪些机制属于模型提示，哪些必须由程序强制？缓存优化的效果应如何区分于模型性能？
- **限制**：仍基于 v2.1.88 的材料及作者解释；工程经验不等同于可量化的性能验证。

### S04 — Dive into Claude Code（VILA-Lab）

- **论文**：https://arxiv.org/abs/2604.14228
- **仓库**：https://github.com/VILA-Lab/Dive-into-Claude-Code
- **建议阅读**：[架构深度分析](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/architecture.md) 与 [设计空间指南](https://github.com/VILA-Lab/Dive-into-Claude-Code/blob/main/docs/build-your-own-agent.md)；比较时固定论文版本，例如 [v3](https://arxiv.org/abs/2604.14228v3)。
- **研究用途**：作为 **Claude Code v2.1.88 的主要二级证据基线**，建立核心 `queryLoop` 与 Context、Tool、Permission、Session 的边界。
- **可提取问题**：核心 Loop 的简单性与外围 Harness 的复杂性如何分工？如何把不同组件的设计影响拆开测量？
- **限制**：报告所称代码占比和各模块数量依赖其分类方法；不能仅凭相同源码的多篇转述提升可信等级。

## 三、Anthropic 官方工程与评测研究（4 份）

### O01 — Scaling Managed Agents

- **地址**：https://www.anthropic.com/research/managed-agents
- **研究用途**：借鉴**持久化事件会话与可替换执行进程**的职责分离。
- **对应实验**：A0-04 的宿主控制权交接、中断后重入、恢复状态规模及延迟。
- **关键边界**：这是 **Managed Agents 平台**的架构经验，不能直接推定 Claude Code CLI 使用完全相同的实现。

### O02 — How We Built Claude Code Auto Mode

- **地址**：https://www.anthropic.com/research/claude-code-auto-mode
- **研究用途**：理解操作审批、模型决策与执行约束的边界，特别是权限拒绝如何返回给模型，以及反复拒绝如何受限。
- **对应实验**：审批对象/执行动作一致性、拒绝后安全继续、误拒绝率、终止和升级策略。
- **关键边界**：针对特定运行模式；某模式下的工程设计不应无条件推广到其他模式/版本。

### O03 — Harness Design for Long-running Apps

- **地址**：https://www.anthropic.com/research/harness-design-long-running-apps
- **研究用途**：比较 Context 重置、压缩、结构化进度交接，以及 Generator / Evaluator 分离。
- **对应实验**：模型自行宣布完成 vs 外部验收器；长任务中的约束保真、错误完成率与 Token 成本。
- **关键边界**：具体研究中的多 Agent 分工不等于 Claude Code 默认 Loop 的全部行为。

### O04 — Infrastructure Noise in Agentic Evals

- **地址**：https://www.anthropic.com/research/infrastructure-noise
- **研究用途**：为结果可信度制定控制变量，避免将 CPU、内存、并发、超时等差异误判为 Harness 架构优势。
- **对应实验**：任务配对、同一执行镜像、同样时间/工具预算、重复运行、置信区间。
- **关键边界**：基础设施带来的结果差异需要按文章的测试任务与配置解释，不能直接迁移为本项目实测数字。

## 四、独立受控实验研究（4 份）

### E01 — Harness or Model?

- **地址**：https://arxiv.org/abs/2609.11987
- **研究用途**：学习**同一模型、不同 Harness**的配对设计，以及如何报告不显著结果与任务条件差异。
- **应复用**：同模型/同任务/同预算、任务分层、效果大小、置信区间、费用口径。
- **警惕**：比较两个完整 Harness 得到的差异，**不等于 Loop 写法本身的因果影响**。

### E02 — Same Model, Different Harness

- **地址**：https://arxiv.org/abs/2608.26218
- **研究用途**：研究紧张 Context 预算下，管理旧工具输出与停滞响应策略的作用。
- **应复用**：除了最终任务是否完成，还评价部分进度、失败阶段、成本与上下文压力。
- **警惕**：多个机制的组合干预，不能把全部收益分配给单一压缩算法或 Loop 形式。

### E03 — An Empirical Study of Harness Design for Coding Agents

- **地址**：https://arxiv.org/abs/2609.20804
- **研究用途**：系统分析 Planning、Action Space、Context Management 与模型/任务条件的交互。
- **应复用**：受控消融、跨任务族比较、预算约束及可重复性报告。
- **警惕**：实验所固定的 Loop 无法证明 `while` 优于显式 FSM 或 Graph。

### E04 — When Does Restricting a Coding Agent to execute_code Help?

- **论文**：https://arxiv.org/abs/2607.10569
- **代码**：https://github.com/hyang0129/onlycodes
- **研究用途**：对照工具集合（默认工具 / Bash-only / Code-only）在任务正确性、成本与调用模式上的取舍。
- **应复用**：工具能力受控的三组消融，以及跨模型、跨任务条件的分析方式。
- **警惕**：工具集合的选择与 Loop 调度是两个实验变量，不能混淆。

## 五、与本仓库研究任务的对应关系

| 本仓库研究任务 | 最推荐使用的参考资料 | 应形成的交付物 |
| --- | --- | --- |
| **A0-03：源码架构与执行路径** | S01、S02、S04 | 版本化函数级证据矩阵；源代码事实与第三方推断分开 |
| **A0-04：Loop vs 可重入 Step** | S01、S04、O01、O04 | 控制权交接与恢复的公平对照；开销、状态规模和错误路径 |
| **A0-04：审批与动作边界** | S02、O02 | 批准动作与实际副作用的一致性、撤销和迟到批准实验 |
| **下一阶段：完成条件与验收** | O03、E01、E03 | 模型声明完成 vs 独立验收器；错误完成率和增量成本 |
| **下一阶段：Context Engineering** | S03、O03、E02、E03 | 约束保留率、有效任务进展、压缩成本 |
| **下一阶段：工具设计取舍** | S02、E03、E04 | 原语工具 vs 专用工具，固定任务覆盖与权限约束 |

## 六、推荐阅读顺序（节省时间）

**第一批（先读，决定研究问题）**：O01 → O02 → O03 → E01 → E02。  
**第二批（明确具体实现边界）**：S04 → S01（第 5–7 章）→ S02（Tool Call 章）。  
**第三批（设计消融和控制混杂因素）**：E03 → E04 → O04 → S03。

建议每读完一篇，只提取五项：**(1) 可定位证据；(2) 工程设计决策；(3) 替代方案；(4) 已公开的效果证据；(5) 未验证的问题**。避免重复编写宽泛的 Claude Code 架构百科。

## 七、引用与复用边界

1. **源码材料**：多份资料依赖同一 Claude Code v2.1.88 Source Map；不同文章不是完全独立的源码验证。不要转载专有源代码、压缩包或大段实现。
2. **官方材料**：第一方工程文章能说明某团队为何这么设计，但应区分 Claude Code CLI、Claude Agent SDK 和 Managed Agents 等具体对象。
3. **学术实验**：研究结果只在其模型、任务、预算和评测环境下成立；引用时保留实验条件和负面结果。
4. **自身贡献**：未经我们执行的论文结果仍标为外部研究，不写成仓库原创的实测结论。

---

## 相关仓库研究文档

- [A0-05：扩大检索范围的完整证据清单](../research/A0-05-literature-expansion/SEARCH_REPORT.md)
- [A0-05：阅读优先级与原创实验建议](../research/A0-05-literature-expansion/PRIORITY_PATH.md)
- [A0-03：源码主张核查](../research/A0-03-source-control-flow/REPORT.md)
- [A0-04：Loop 对照实验](../research/A0-04-loop-comparison/REPORT.md)
- [研究决策日志](../research/02-agent-loop/DECISION_LOG.md)

**研究方向结论**：应从“复述 Claude Code 的架构”转向“在严格控制变量的前提下，测量 Harness 机制在不同任务条件下的价值与代价”。
