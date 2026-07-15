# tasks 模块

## 概述

**位置:** `src/tasks/`

## 文件统计

- TypeScript 文件: 10
- TypeScript React 文件: 4
- 总计: 14

## 文件详情

---


### `src/tasks/DreamTask/DreamTask.ts`

**信息:**
- 行数: 157
- 大小: 4988 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Background task entry for auto-dream (memory consolidation subagent).
// Makes the otherwise-invisible forked agent visible in the footer pill and
// Shift+Down dialog. The dream agent itself is unchanged — this is pure UI
// surfacing via the existing task registry.

import { rollbackConsolidationLock } from '../../services/autoDream/consolidationLock.js'
import type { SetAppState, Task, TaskStateBase } from '../../Task.js'
import { createTaskStateBase, generateTaskId } from '../../Task.js'
import { registerTask, updateTaskState } from '../../utils/task/framework.js'

// Keep only the N most recent turns for live display.
const MAX_TURNS = 30

// A single assistant turn from the dream agent, tool uses collapsed to a count.
export type DreamTurn = {
  text: string
  toolUseCount: number
}

// No phase detection — the dream prompt has a 4-stage structure
// (orient/gather/consolidate/prune) but we don't parse it. Just flip from
// 'starting' to 'updating' when the first Edit/Write tool_use lands.
export type DreamPhase = 'starting' | 'updating'

export type DreamTaskState = TaskStateBase & {
  type: 'dream'
  phase: DreamPhase
  sessionsReviewing: number
  /**
   * Paths observed in Edit/Write tool_use blocks via onMessage. This is an
   * INCOMPLETE reflection of what the dream agent actually changed — it misses
   * any bash-mediated writes and only captures the tool calls we pattern-match.
   * Treat as "at least these were touched", not "only these were touched".
   */
  filesTouched: string[]
  /** Assistant text responses, tool uses collapsed. Prompt is NOT included. */
  turns: DreamTurn[]
  abortController?: AbortController
  /** Stashed so kill can rewind the lock mtime (same path as fork-failure). */
  priorMtime: number
}

export function isDreamTask(task: unknown): task is DreamTaskState {
  return (
    typeof task === 'object' &&
    task !== null &&
    'type' in task &&
    task.type === 'dream'
  )
}

```

---


### `src/tasks/InProcessTeammateTask/InProcessTeammateTask.tsx`

**信息:**
- 行数: 126
- 大小: 16381 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
/**
 * InProcessTeammateTask - Manages in-process teammate lifecycle
 *
 * This component implements the Task interface for in-process teammates.
 * Unlike LocalAgentTask (background agents), in-process teammates:
 * 1. Run in the same Node.js process using AsyncLocalStorage for isolation
 * 2. Have team-aware identity (agentName@teamName)
 * 3. Support plan mode approval flow
 * 4. Can be idle (waiting for work) or active (processing)
 */

import { isTerminalTaskStatus, type SetAppState, type Task, type TaskStateBase } from '../../Task.js';
import type { Message } from '../../types/message.js';
import { logForDebugging } from '../../utils/debug.js';
import { createUserMessage } from '../../utils/messages.js';
import { killInProcessTeammate } from '../../utils/swarm/spawnInProcess.js';
import { updateTaskState } from '../../utils/task/framework.js';
import type { InProcessTeammateTaskState } from './types.js';
import { appendCappedMessage, isInProcessTeammateTask } from './types.js';

/**
 * InProcessTeammateTask - Handles in-process teammate execution.
 */
export const InProcessTeammateTask: Task = {
  name: 'InProcessTeammateTask',
  type: 'in_process_teammate',
  async kill(taskId, setAppState) {
    killInProcessTeammate(taskId, setAppState);
  }
};

/**
 * Request shutdown for a teammate.
 */
export function requestTeammateShutdown(taskId: string, setAppState: SetAppState): void {
  updateTaskState<InProcessTeammateTaskState>(taskId, setAppState, task => {
    if (task.status !== 'running' || task.shutdownRequested) {
      return task;
    }
    return {
      ...task,
      shutdownRequested: true
    };
  });
}

/**
 * Append a message to a teammate's conversation history.
 * Used for zoomed view to show the teammate's conversation.
 */

```

---


### `src/tasks/InProcessTeammateTask/types.ts`

**信息:**
- 行数: 121
- 大小: 4322 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { TaskStateBase } from '../../Task.js'
import type { AgentToolResult } from '../../tools/AgentTool/agentToolUtils.js'
import type { AgentDefinition } from '../../tools/AgentTool/loadAgentsDir.js'
import type { Message } from '../../types/message.js'
import type { PermissionMode } from '../../utils/permissions/PermissionMode.js'
import type { AgentProgress } from '../LocalAgentTask/LocalAgentTask.js'

/**
 * Teammate identity stored in task state.
 * Same shape as TeammateContext (runtime) but stored as plain data.
 * TeammateContext is for AsyncLocalStorage; this is for AppState persistence.
 */
export type TeammateIdentity = {
  agentId: string // e.g., "researcher@my-team"
  agentName: string // e.g., "researcher"
  teamName: string
  color?: string
  planModeRequired: boolean
  parentSessionId: string // Leader's session ID
}

export type InProcessTeammateTaskState = TaskStateBase & {
  type: 'in_process_teammate'

  // Identity as sub-object (matches TeammateContext shape for consistency)
  // Stored as plain data in AppState, NOT a reference to AsyncLocalStorage
  identity: TeammateIdentity

  // Execution
  prompt: string
  // Optional model override for this teammate
  model?: string
  // Optional: Only set if teammate uses a specific agent definition
  // Many teammates run as general-purpose agents without a predefined definition
  selectedAgent?: AgentDefinition
  abortController?: AbortController // Runtime only, not serialized to disk - kills WHOLE teammate
  currentWorkAbortController?: AbortController // Runtime only - aborts current turn without killing teammate
  unregisterCleanup?: () => void // Runtime only

  // Plan mode approval tracking (planModeRequired is in identity)
  awaitingPlanApproval: boolean

  // Permission mode for this teammate (cycled independently via Shift+Tab when viewing)
  permissionMode: PermissionMode

  // State
  error?: string
  result?: AgentToolResult // Reuse existing type since teammates run via runAgent()
  progress?: AgentProgress


```

---


### `src/tasks/LocalAgentTask/LocalAgentTask.tsx`

**信息:**
- 行数: 683
- 大小: 82910 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { getSdkAgentProgressSummariesEnabled } from '../../bootstrap/state.js';
import { OUTPUT_FILE_TAG, STATUS_TAG, SUMMARY_TAG, TASK_ID_TAG, TASK_NOTIFICATION_TAG, TOOL_USE_ID_TAG, WORKTREE_BRANCH_TAG, WORKTREE_PATH_TAG, WORKTREE_TAG } from '../../constants/xml.js';
import { abortSpeculation } from '../../services/PromptSuggestion/speculation.js';
import type { AppState } from '../../state/AppState.js';
import type { SetAppState, Task, TaskStateBase } from '../../Task.js';
import { createTaskStateBase } from '../../Task.js';
import type { Tools } from '../../Tool.js';
import { findToolByName } from '../../Tool.js';
import type { AgentToolResult } from '../../tools/AgentTool/agentToolUtils.js';
import type { AgentDefinition } from '../../tools/AgentTool/loadAgentsDir.js';
import { SYNTHETIC_OUTPUT_TOOL_NAME } from '../../tools/SyntheticOutputTool/SyntheticOutputTool.js';
import { asAgentId } from '../../types/ids.js';
import type { Message } from '../../types/message.js';
import { createAbortController, createChildAbortController } from '../../utils/abortController.js';
import { registerCleanup } from '../../utils/cleanupRegistry.js';
import { getToolSearchOrReadInfo } from '../../utils/collapseReadSearch.js';
import { enqueuePendingNotification } from '../../utils/messageQueueManager.js';
import { getAgentTranscriptPath } from '../../utils/sessionStorage.js';
import { evictTaskOutput, getTaskOutputPath, initTaskOutputAsSymlink } from '../../utils/task/diskOutput.js';
import { PANEL_GRACE_MS, registerTask, updateTaskState } from '../../utils/task/framework.js';
import { emitTaskProgress } from '../../utils/task/sdkProgress.js';
import type { TaskState } from '../types.js';
export type ToolActivity = {
  toolName: string;
  input: Record<string, unknown>;
  /** Pre-computed activity description from the tool, e.g. "Reading src/foo.ts" */
  activityDescription?: string;
  /** Pre-computed: true if this is a search operation (Grep, Glob, etc.) */
  isSearch?: boolean;
  /** Pre-computed: true if this is a read operation (Read, cat, etc.) */
  isRead?: boolean;
};
export type AgentProgress = {
  toolUseCount: number;
  tokenCount: number;
  lastActivity?: ToolActivity;
  recentActivities?: ToolActivity[];
  summary?: string;
};
const MAX_RECENT_ACTIVITIES = 5;
export type ProgressTracker = {
  toolUseCount: number;
  // Track input and output separately to avoid double-counting.
  // input_tokens in Claude API is cumulative per turn (includes all previous context),
  // so we keep the latest value. output_tokens is per-turn, so we sum those.
  latestInputTokens: number;
  cumulativeOutputTokens: number;
  recentActivities: ToolActivity[];
};
export function createProgressTracker(): ProgressTracker {

```

---


### `src/tasks/LocalMainSessionTask.ts`

**信息:**
- 行数: 479
- 大小: 15136 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * LocalMainSessionTask - Handles backgrounding the main session query.
 *
 * When user presses Ctrl+B twice during a query, the session is "backgrounded":
 * - The query continues running in the background
 * - The UI clears to a fresh prompt
 * - A notification is sent when the query completes
 *
 * This reuses the LocalAgentTask state structure since the behavior is similar.
 */

import type { UUID } from 'crypto'
import { randomBytes } from 'crypto'
import {
  OUTPUT_FILE_TAG,
  STATUS_TAG,
  SUMMARY_TAG,
  TASK_ID_TAG,
  TASK_NOTIFICATION_TAG,
  TOOL_USE_ID_TAG,
} from '../constants/xml.js'
import { type QueryParams, query } from '../query.js'
import { roughTokenCountEstimation } from '../services/tokenEstimation.js'
import type { SetAppState } from '../Task.js'
import { createTaskStateBase } from '../Task.js'
import type {
  AgentDefinition,
  CustomAgentDefinition,
} from '../tools/AgentTool/loadAgentsDir.js'
import { asAgentId } from '../types/ids.js'
import type { Message } from '../types/message.js'
import { createAbortController } from '../utils/abortController.js'
import {
  runWithAgentContext,
  type SubagentContext,
} from '../utils/agentContext.js'
import { registerCleanup } from '../utils/cleanupRegistry.js'
import { logForDebugging } from '../utils/debug.js'
import { logError } from '../utils/log.js'
import { enqueuePendingNotification } from '../utils/messageQueueManager.js'
import { emitTaskTerminatedSdk } from '../utils/sdkEventQueue.js'
import {
  getAgentTranscriptPath,
  recordSidechainTranscript,
} from '../utils/sessionStorage.js'
import {
  evictTaskOutput,
  getTaskOutputPath,
  initTaskOutputAsSymlink,
} from '../utils/task/diskOutput.js'

```

---


### `src/tasks/LocalShellTask/LocalShellTask.tsx`

**信息:**
- 行数: 523
- 大小: 66306 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import { stat } from 'fs/promises';
import { OUTPUT_FILE_TAG, STATUS_TAG, SUMMARY_TAG, TASK_ID_TAG, TASK_NOTIFICATION_TAG, TOOL_USE_ID_TAG } from '../../constants/xml.js';
import { abortSpeculation } from '../../services/PromptSuggestion/speculation.js';
import type { AppState } from '../../state/AppState.js';
import type { LocalShellSpawnInput, SetAppState, Task, TaskContext, TaskHandle } from '../../Task.js';
import { createTaskStateBase } from '../../Task.js';
import type { AgentId } from '../../types/ids.js';
import { registerCleanup } from '../../utils/cleanupRegistry.js';
import { tailFile } from '../../utils/fsOperations.js';
import { logError } from '../../utils/log.js';
import { enqueuePendingNotification } from '../../utils/messageQueueManager.js';
import type { ShellCommand } from '../../utils/ShellCommand.js';
import { evictTaskOutput, getTaskOutputPath } from '../../utils/task/diskOutput.js';
import { registerTask, updateTaskState } from '../../utils/task/framework.js';
import { escapeXml } from '../../utils/xml.js';
import { backgroundAgentTask, isLocalAgentTask } from '../LocalAgentTask/LocalAgentTask.js';
import { isMainSessionTask } from '../LocalMainSessionTask.js';
import { type BashTaskKind, isLocalShellTask, type LocalShellTaskState } from './guards.js';
import { killTask } from './killShellTasks.js';

/** Prefix that identifies a LocalShellTask summary to the UI collapse transform. */
export const BACKGROUND_BASH_SUMMARY_PREFIX = 'Background command ';
const STALL_CHECK_INTERVAL_MS = 5_000;
const STALL_THRESHOLD_MS = 45_000;
const STALL_TAIL_BYTES = 1024;

// Last-line patterns that suggest a command is blocked waiting for keyboard
// input. Used to gate the stall notification — we stay silent on commands that
// are merely slow (git log -S, long builds) and only notify when the tail
// looks like an interactive prompt the model can act on. See CC-1175.
const PROMPT_PATTERNS = [/\(y\/n\)/i,
// (Y/n), (y/N)
/\[y\/n\]/i,
// [Y/n], [y/N]
/\(yes\/no\)/i, /\b(?:Do you|Would you|Shall I|Are you sure|Ready to)\b.*\? *$/i,
// directed questions
/Press (any key|Enter)/i, /Continue\?/i, /Overwrite\?/i];
export function looksLikePrompt(tail: string): boolean {
  const lastLine = tail.trimEnd().split('\n').pop() ?? '';
  return PROMPT_PATTERNS.some(p => p.test(lastLine));
}

// Output-side analog of peekForStdinData (utils/process.ts): fire a one-shot
// notification if output stops growing and the tail looks like a prompt.
function startStallWatchdog(taskId: string, description: string, kind: BashTaskKind | undefined, toolUseId?: string, agentId?: AgentId): () => void {
  if (kind === 'monitor') return () => {};
  const outputPath = getTaskOutputPath(taskId);
  let lastSize = 0;
  let lastGrowth = Date.now();

```

---


### `src/tasks/LocalShellTask/guards.ts`

**信息:**
- 行数: 41
- 大小: 1552 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Pure type + type guard for LocalShellTask state.
// Extracted from LocalShellTask.tsx so non-React consumers (stopTask.ts via
// print.ts) don't pull React/ink into the module graph.

import type { TaskStateBase } from '../../Task.js'
import type { AgentId } from '../../types/ids.js'
import type { ShellCommand } from '../../utils/ShellCommand.js'

export type BashTaskKind = 'bash' | 'monitor'

export type LocalShellTaskState = TaskStateBase & {
  type: 'local_bash' // Keep as 'local_bash' for backward compatibility with persisted session state
  command: string
  result?: {
    code: number
    interrupted: boolean
  }
  completionStatusSentInAttachment: boolean
  shellCommand: ShellCommand | null
  unregisterCleanup?: () => void
  cleanupTimeoutId?: NodeJS.Timeout
  // Track what we last reported for computing deltas (total lines from TaskOutput)
  lastReportedTotalLines: number
  // Whether the task has been backgrounded (false = foreground running, true = backgrounded)
  isBackgrounded: boolean
  // Agent that spawned this task. Used to kill orphaned bash tasks when the
  // agent exits (see killShellTasksForAgent). Undefined = main thread.
  agentId?: AgentId
  // UI display variant. 'monitor' → shows description instead of command,
  // 'Monitor details' dialog title, distinct status bar pill.
  kind?: BashTaskKind
}

export function isLocalShellTask(task: unknown): task is LocalShellTaskState {
  return (
    typeof task === 'object' &&
    task !== null &&
    'type' in task &&
    task.type === 'local_bash'
  )
}

```

---


### `src/tasks/LocalShellTask/killShellTasks.ts`

**信息:**
- 行数: 76
- 大小: 2565 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Pure (non-React) kill helpers for LocalShellTask.
// Extracted so runAgent.ts can kill agent-scoped bash tasks without pulling
// React/Ink into its module graph (same rationale as guards.ts).

import type { AppState } from '../../state/AppState.js'
import type { AgentId } from '../../types/ids.js'
import { logForDebugging } from '../../utils/debug.js'
import { logError } from '../../utils/log.js'
import { dequeueAllMatching } from '../../utils/messageQueueManager.js'
import { evictTaskOutput } from '../../utils/task/diskOutput.js'
import { updateTaskState } from '../../utils/task/framework.js'
import { isLocalShellTask } from './guards.js'

type SetAppStateFn = (updater: (prev: AppState) => AppState) => void

export function killTask(taskId: string, setAppState: SetAppStateFn): void {
  updateTaskState(taskId, setAppState, task => {
    if (task.status !== 'running' || !isLocalShellTask(task)) {
      return task
    }

    try {
      logForDebugging(`LocalShellTask ${taskId} kill requested`)
      task.shellCommand?.kill()
      task.shellCommand?.cleanup()
    } catch (error) {
      logError(error)
    }

    task.unregisterCleanup?.()
    if (task.cleanupTimeoutId) {
      clearTimeout(task.cleanupTimeoutId)
    }

    return {
      ...task,
      status: 'killed',
      notified: true,
      shellCommand: null,
      unregisterCleanup: undefined,
      cleanupTimeoutId: undefined,
      endTime: Date.now(),
    }
  })
  void evictTaskOutput(taskId)
}

/**
 * Kill all running bash tasks spawned by a given agent.
 * Called from runAgent.ts finally block so background processes don't outlive

```

---


### `src/tasks/LocalWorkflowTask/LocalWorkflowTask.ts`

**信息:**
- 行数: 5
- 大小: 143 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type LocalWorkflowTaskState = Record<string, unknown>

export function isLocalWorkflowTask(_value: unknown): boolean {
  return false
}

```

---


### `src/tasks/MonitorMcpTask/MonitorMcpTask.ts`

**信息:**
- 行数: 5
- 大小: 137 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type MonitorMcpTaskState = Record<string, unknown>

export function isMonitorMcpTask(_value: unknown): boolean {
  return false
}

```

---


### `src/tasks/RemoteAgentTask/RemoteAgentTask.tsx`

**信息:**
- 行数: 856
- 大小: 126389 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { ToolUseBlock } from '@anthropic-ai/sdk/resources';
import { getRemoteSessionUrl } from '../../constants/product.js';
import { OUTPUT_FILE_TAG, REMOTE_REVIEW_PROGRESS_TAG, REMOTE_REVIEW_TAG, STATUS_TAG, SUMMARY_TAG, TASK_ID_TAG, TASK_NOTIFICATION_TAG, TASK_TYPE_TAG, TOOL_USE_ID_TAG, ULTRAPLAN_TAG } from '../../constants/xml.js';
import type { SDKAssistantMessage, SDKMessage } from '../../entrypoints/agentSdkTypes.js';
import type { SetAppState, Task, TaskContext, TaskStateBase } from '../../Task.js';
import { createTaskStateBase, generateTaskId } from '../../Task.js';
import { TodoWriteTool } from '../../tools/TodoWriteTool/TodoWriteTool.js';
import { type BackgroundRemoteSessionPrecondition, checkBackgroundRemoteSessionEligibility } from '../../utils/background/remote/remoteSession.js';
import { logForDebugging } from '../../utils/debug.js';
import { logError } from '../../utils/log.js';
import { enqueuePendingNotification } from '../../utils/messageQueueManager.js';
import { extractTag, extractTextContent } from '../../utils/messages.js';
import { emitTaskTerminatedSdk } from '../../utils/sdkEventQueue.js';
import { deleteRemoteAgentMetadata, listRemoteAgentMetadata, type RemoteAgentMetadata, writeRemoteAgentMetadata } from '../../utils/sessionStorage.js';
import { jsonStringify } from '../../utils/slowOperations.js';
import { appendTaskOutput, evictTaskOutput, getTaskOutputPath, initTaskOutput } from '../../utils/task/diskOutput.js';
import { registerTask, updateTaskState } from '../../utils/task/framework.js';
import { fetchSession } from '../../utils/teleport/api.js';
import { archiveRemoteSession, pollRemoteSessionEvents } from '../../utils/teleport.js';
import type { TodoList } from '../../utils/todo/types.js';
import type { UltraplanPhase } from '../../utils/ultraplan/ccrSession.js';
export type RemoteAgentTaskState = TaskStateBase & {
  type: 'remote_agent';
  remoteTaskType: RemoteTaskType;
  /** Task-specific metadata (PR number, repo, etc.). */
  remoteTaskMetadata?: RemoteTaskMetadata;
  sessionId: string; // Original session ID for API calls
  command: string;
  title: string;
  todoList: TodoList;
  log: SDKMessage[];
  /**
   * Long-running agent that will not be marked as complete after the first `result`.
   */
  isLongRunning?: boolean;
  /**
   * When the local poller started watching this task (at spawn or on restore).
   * Review timeout clocks from here so a restore doesn't immediately time out
   * a task spawned >30min ago.
   */
  pollStartedAt: number;
  /** True when this task was created by a teleported /ultrareview command. */
  isRemoteReview?: boolean;
  /** Parsed from the orchestrator's <remote-review-progress> heartbeat echoes. */
  reviewProgress?: {
    stage?: 'finding' | 'verifying' | 'synthesizing';
    bugsFound: number;
    bugsVerified: number;
    bugsRefuted: number;
  };

```

---


### `src/tasks/pillLabel.ts`

**信息:**
- 行数: 82
- 大小: 2898 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { DIAMOND_FILLED, DIAMOND_OPEN } from '../constants/figures.js'
import { count } from '../utils/array.js'
import type { BackgroundTaskState } from './types.js'

/**
 * Produces the compact footer-pill label for a set of background tasks.
 * Used by both the footer pill and the turn-duration transcript line so the
 * two surfaces agree on terminology.
 */
export function getPillLabel(tasks: BackgroundTaskState[]): string {
  const n = tasks.length
  const allSameType = tasks.every(t => t.type === tasks[0]!.type)

  if (allSameType) {
    switch (tasks[0]!.type) {
      case 'local_bash': {
        const monitors = count(
          tasks,
          t => t.type === 'local_bash' && t.kind === 'monitor',
        )
        const shells = n - monitors
        const parts: string[] = []
        if (shells > 0)
          parts.push(shells === 1 ? '1 shell' : `${shells} shells`)
        if (monitors > 0)
          parts.push(monitors === 1 ? '1 monitor' : `${monitors} monitors`)
        return parts.join(', ')
      }
      case 'in_process_teammate': {
        const teamCount = new Set(
          tasks.map(t =>
            t.type === 'in_process_teammate' ? t.identity.teamName : '',
          ),
        ).size
        return teamCount === 1 ? '1 team' : `${teamCount} teams`
      }
      case 'local_agent':
        return n === 1 ? '1 local agent' : `${n} local agents`
      case 'remote_agent': {
        const first = tasks[0]!
        // Per design mockup: ◇ open diamond while running/needs-input,
        // ◆ filled once ExitPlanMode is awaiting approval.
        if (n === 1 && first.type === 'remote_agent' && first.isUltraplan) {
          switch (first.ultraplanPhase) {
            case 'plan_ready':
              return `${DIAMOND_FILLED} ultraplan ready`
            case 'needs_input':
              return `${DIAMOND_OPEN} ultraplan needs your input`
            default:
              return `${DIAMOND_OPEN} ultraplan`

```

---


### `src/tasks/stopTask.ts`

**信息:**
- 行数: 100
- 大小: 2894 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Shared logic for stopping a running task.
// Used by TaskStopTool (LLM-invoked) and SDK stop_task control request.

import type { AppState } from '../state/AppState.js'
import type { TaskStateBase } from '../Task.js'
import { getTaskByType } from '../tasks.js'
import { emitTaskTerminatedSdk } from '../utils/sdkEventQueue.js'
import { isLocalShellTask } from './LocalShellTask/guards.js'

export class StopTaskError extends Error {
  constructor(
    message: string,
    public readonly code: 'not_found' | 'not_running' | 'unsupported_type',
  ) {
    super(message)
    this.name = 'StopTaskError'
  }
}

type StopTaskContext = {
  getAppState: () => AppState
  setAppState: (f: (prev: AppState) => AppState) => void
}

type StopTaskResult = {
  taskId: string
  taskType: string
  command: string | undefined
}

/**
 * Look up a task by ID, validate it is running, kill it, and mark it as notified.
 *
 * Throws {@link StopTaskError} when the task cannot be stopped (not found,
 * not running, or unsupported type). Callers can inspect `error.code` to
 * distinguish the failure reason.
 */
export async function stopTask(
  taskId: string,
  context: StopTaskContext,
): Promise<StopTaskResult> {
  const { getAppState, setAppState } = context
  const appState = getAppState()
  const task = appState.tasks?.[taskId] as TaskStateBase | undefined

  if (!task) {
    throw new StopTaskError(`No task found with ID: ${taskId}`, 'not_found')
  }

  if (task.status !== 'running') {

```

---


### `src/tasks/types.ts`

**信息:**
- 行数: 46
- 大小: 1691 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Union of all concrete task state types
// Use this for components that need to work with any task type

import type { DreamTaskState } from './DreamTask/DreamTask.js'
import type { InProcessTeammateTaskState } from './InProcessTeammateTask/types.js'
import type { LocalAgentTaskState } from './LocalAgentTask/LocalAgentTask.js'
import type { LocalShellTaskState } from './LocalShellTask/guards.js'
import type { LocalWorkflowTaskState } from './LocalWorkflowTask/LocalWorkflowTask.js'
import type { MonitorMcpTaskState } from './MonitorMcpTask/MonitorMcpTask.js'
import type { RemoteAgentTaskState } from './RemoteAgentTask/RemoteAgentTask.js'

export type TaskState =
  | LocalShellTaskState
  | LocalAgentTaskState
  | RemoteAgentTaskState
  | InProcessTeammateTaskState
  | LocalWorkflowTaskState
  | MonitorMcpTaskState
  | DreamTaskState

// Task types that can appear in the background tasks indicator
export type BackgroundTaskState =
  | LocalShellTaskState
  | LocalAgentTaskState
  | RemoteAgentTaskState
  | InProcessTeammateTaskState
  | LocalWorkflowTaskState
  | MonitorMcpTaskState
  | DreamTaskState

/**
 * Check if a task should be shown in the background tasks indicator.
 * A task is considered a background task if:
 * 1. It is running or pending
 * 2. It has been explicitly backgrounded (not a foreground task)
 */
export function isBackgroundTask(task: TaskState): task is BackgroundTaskState {
  if (task.status !== 'running' && task.status !== 'pending') {
    return false
  }
  // Foreground tasks (isBackgrounded === false) are not yet "background tasks"
  if ('isBackgrounded' in task && task.isBackgrounded === false) {
    return false
  }
  return true
}

```

---

