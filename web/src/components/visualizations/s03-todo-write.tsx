"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useSteppedVisualization } from "@/hooks/useSteppedVisualization";
import { StepControls } from "@/components/visualizations/shared/step-controls";

// -- 任务定义 --

type TaskStatus = "pending" | "in_progress" | "done";

interface Task {
  id: number;
  label: string;
  status: TaskStatus;
}

// 每一步 4 个任务的快照
const TASK_STATES: Task[][] = [
  // 第 0 步：全部待处理
  [
    { id: 1, label: "Write auth tests", status: "pending" },
    { id: 2, label: "Fix mobile layout", status: "pending" },
    { id: 3, label: "Add error handling", status: "pending" },
    { id: 4, label: "Update config loader", status: "pending" },
  ],
  // 第 1 步：仍全部待处理（空闲轮次 1）
  [
    { id: 1, label: "Write auth tests", status: "pending" },
    { id: 2, label: "Fix mobile layout", status: "pending" },
    { id: 3, label: "Add error handling", status: "pending" },
    { id: 4, label: "Update config loader", status: "pending" },
  ],
  // 第 2 步：仍全部待处理（空闲轮次 2）
  [
    { id: 1, label: "Write auth tests", status: "pending" },
    { id: 2, label: "Fix mobile layout", status: "pending" },
    { id: 3, label: "Add error handling", status: "pending" },
    { id: 4, label: "Update config loader", status: "pending" },
  ],
  // 第 3 步：NAG 触发，任务 1 进入进行中
  [
    { id: 1, label: "Write auth tests", status: "in_progress" },
    { id: 2, label: "Fix mobile layout", status: "pending" },
    { id: 3, label: "Add error handling", status: "pending" },
    { id: 4, label: "Update config loader", status: "pending" },
  ],
  // 第 4 步：任务 1 完成
  [
    { id: 1, label: "Write auth tests", status: "done" },
    { id: 2, label: "Fix mobile layout", status: "pending" },
    { id: 3, label: "Add error handling", status: "pending" },
    { id: 4, label: "Update config loader", status: "pending" },
  ],
  // 第 5 步：任务 2 自主进入进行中
  [
    { id: 1, label: "Write auth tests", status: "done" },
    { id: 2, label: "Fix mobile layout", status: "in_progress" },
    { id: 3, label: "Add error handling", status: "pending" },
    { id: 4, label: "Update config loader", status: "pending" },
  ],
  // 第 6 步：任务 2、3 完成，任务 4 进行中
  [
    { id: 1, label: "Write auth tests", status: "done" },
    { id: 2, label: "Fix mobile layout", status: "done" },
    { id: 3, label: "Add error handling", status: "done" },
    { id: 4, label: "Update config loader", status: "in_progress" },
  ],
];

// 每一步的 Nag 计时值（总计 3）
const NAG_TIMER_PER_STEP = [0, 1, 2, 3, 0, 0, 0];
const NAG_THRESHOLD = 3;

// 该步是否触发 nag
const NAG_FIRES_PER_STEP = [false, false, false, true, false, false, false];

// 步骤注释
const STEP_INFO = [
  { title: "The Plan", desc: "TodoWrite gives the model a visible plan. All tasks start as pending." },
  { title: "Round 1 -- Idle", desc: "The model does work but doesn't touch its todos. The nag counter increments." },
  { title: "Round 2 -- Still Idle", desc: "Two rounds without progress. Pressure builds." },
  { title: "NAG!", desc: "Threshold reached! System message injected: 'You have pending tasks. Pick one up now!'" },
  { title: "Task Complete", desc: "The model completes the task. Timer stays at 0 -- working on todos resets the counter." },
  { title: "Self-Directed", desc: "Once the model learns the pattern, it picks up tasks voluntarily." },
  { title: "Mission Accomplished", desc: "Visible plan + nag pressure = reliable task completion." },
];

// -- 列组件 --

function KanbanColumn({
  title,
  tasks,
  accentClass,
  headerBg,
}: {
  title: string;
  tasks: Task[];
  accentClass: string;
  headerBg: string;
}) {
  return (
    <div className="flex min-h-[280px] flex-1 flex-col rounded-lg border border-zinc-200 bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-900">
      <div
        className={`rounded-t-lg px-3 py-2 text-center text-xs font-bold uppercase tracking-wider ${headerBg}`}
      >
        {title}
        <span className={`ml-1.5 inline-flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold ${accentClass}`}>
          {tasks.length}
        </span>
      </div>
      <div className="flex flex-1 flex-col gap-2 p-2">
        <AnimatePresence mode="popLayout">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))}
        </AnimatePresence>
        {tasks.length === 0 && (
          <div className="flex flex-1 items-center justify-center text-xs text-zinc-400 dark:text-zinc-600">
            --
          </div>
        )}
      </div>
    </div>
  );
}

// -- 任务卡片 --

function TaskCard({ task }: { task: Task }) {
  const statusStyles: Record<TaskStatus, string> = {
    pending: "bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400",
    in_progress: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
    done: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
  };

  const borderStyles: Record<TaskStatus, string> = {
    pending: "border-zinc-200 bg-white dark:border-zinc-700 dark:bg-zinc-800",
    in_progress: "border-amber-300 bg-amber-50 dark:border-amber-700 dark:bg-amber-950/30",
    done: "border-emerald-300 bg-emerald-50 dark:border-emerald-700 dark:bg-emerald-950/30",
  };

  return (
    <motion.div
      layout
      layoutId={`task-${task.id}`}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      transition={{ type: "spring", stiffness: 400, damping: 30 }}
      className={`rounded-md border p-2.5 ${borderStyles[task.status]}`}
    >
      <div className="mb-1.5 flex items-center justify-between">
        <span className="font-mono text-[10px] text-zinc-400 dark:text-zinc-500">
          #{task.id}
        </span>
        <span
          className={`rounded-full px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wide ${statusStyles[task.status]}`}
        >
          {task.status.replace("_", " ")}
        </span>
      </div>
      <div className="text-xs font-medium text-zinc-700 dark:text-zinc-300">
        {task.label}
      </div>
    </motion.div>
  );
}

// -- Nag 仪表盘 --

function NagGauge({ value, max, firing }: { value: number; max: number; firing: boolean }) {
  const pct = Math.min((value / max) * 100, 100);

  const barColor =
    value === 0
      ? "bg-zinc-300 dark:bg-zinc-600"
      : value === 1
        ? "bg-green-400 dark:bg-green-500"
        : value === 2
          ? "bg-yellow-400 dark:bg-yellow-500"
          : "bg-red-500 dark:bg-red-500";

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-zinc-600 dark:text-zinc-300">
          Nag Timer
        </span>
        <span className="font-mono text-xs text-zinc-500 dark:text-zinc-400">
          {value}/{max}
        </span>
      </div>
      <div className="relative h-4 w-full overflow-hidden rounded-full bg-zinc-200 dark:bg-zinc-700">
        <motion.div
          className={`absolute inset-y-0 left-0 rounded-full ${barColor}`}
          initial={{ width: "0%" }}
          animate={{
            width: `${pct}%`,
            ...(firing ? { scale: [1, 1.05, 1] } : {}),
          }}
          transition={{
            width: { duration: 0.5, ease: "easeOut" },
            scale: { duration: 0.3, repeat: 2 },
          }}
        />
        {firing && (
          <motion.div
            className="absolute inset-0 rounded-full border-2 border-red-500"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0, 1, 0] }}
            transition={{ duration: 1 }}
          />
        )}
      </div>
    </div>
  );
}

// -- 主组件 --

export default function TodoWrite({ title }: { title?: string }) {
  const {
    currentStep,
    totalSteps,
    next,
    prev,
    reset,
    isPlaying,
    toggleAutoPlay,
  } = useSteppedVisualization({ totalSteps: 7, autoPlayInterval: 2500 });

  const tasks = TASK_STATES[currentStep];
  const nagValue = NAG_TIMER_PER_STEP[currentStep];
  const nagFires = NAG_FIRES_PER_STEP[currentStep];
  const stepInfo = STEP_INFO[currentStep];

  const pendingTasks = tasks.filter((t) => t.status === "pending");
  const inProgressTasks = tasks.filter((t) => t.status === "in_progress");
  const doneTasks = tasks.filter((t) => t.status === "done");

  return (
    <section className="min-h-[500px] space-y-4">
      <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-100">
        {title || "TodoWrite Nag System"}
      </h2>

      <div className="rounded-lg border border-zinc-200 bg-white p-4 dark:border-zinc-700 dark:bg-zinc-900">
        {/* Nag 仪表盘 + Nag 消息 */}
        <div className="mb-4 space-y-2">
          <NagGauge value={nagValue} max={NAG_THRESHOLD} firing={nagFires} />

          <AnimatePresence>
            {nagFires && (
              <motion.div
                initial={{ opacity: 0, y: -8, height: 0 }}
                animate={{ opacity: 1, y: 0, height: "auto" }}
                exit={{ opacity: 0, y: -8, height: 0 }}
                className="rounded-md border border-red-300 bg-red-50 px-3 py-2 text-center text-xs font-bold text-red-700 dark:border-red-700 dark:bg-red-950/30 dark:text-red-300"
              >
                SYSTEM: "You have pending tasks. Pick one up now!"
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* 看板 */}
        <div className="flex gap-3">
          <KanbanColumn
            title="Pending"
            tasks={pendingTasks}
            accentClass="bg-zinc-200 text-zinc-600 dark:bg-zinc-700 dark:text-zinc-300"
            headerBg="bg-zinc-200 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300"
          />
          <KanbanColumn
            title="In Progress"
            tasks={inProgressTasks}
            accentClass="bg-amber-200 text-amber-700 dark:bg-amber-800 dark:text-amber-200"
            headerBg="bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300"
          />
          <KanbanColumn
            title="Done"
            tasks={doneTasks}
            accentClass="bg-emerald-200 text-emerald-700 dark:bg-emerald-800 dark:text-emerald-200"
            headerBg="bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300"
          />
        </div>

        {/* 进度摘要 */}
        <div className="mt-3 flex items-center justify-between rounded-md bg-zinc-100 px-3 py-2 dark:bg-zinc-800">
          <span className="font-mono text-[11px] text-zinc-500 dark:text-zinc-400">
            Progress: {doneTasks.length}/{tasks.length} complete
          </span>
          <div className="flex gap-0.5">
            {tasks.map((t) => (
              <div
                key={t.id}
                className={`h-2 w-6 rounded-sm ${
                  t.status === "done"
                    ? "bg-emerald-500"
                    : t.status === "in_progress"
                      ? "bg-amber-400"
                      : "bg-zinc-300 dark:bg-zinc-600"
                }`}
              />
            ))}
          </div>
        </div>
      </div>

      <StepControls
        currentStep={currentStep}
        totalSteps={totalSteps}
        onPrev={prev}
        onNext={next}
        onReset={reset}
        isPlaying={isPlaying}
        onToggleAutoPlay={toggleAutoPlay}
        stepTitle={stepInfo.title}
        stepDescription={stepInfo.desc}
      />
    </section>
  );
}
