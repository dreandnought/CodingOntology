# query 模块

## 概述

**位置:** `src/query/`

## 文件统计

- TypeScript 文件: 5
- TypeScript React 文件: 0
- 总计: 5

## 文件详情

---


### `src/query/config.ts`

**信息:**
- 行数: 46
- 大小: 1808 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getSessionId } from '../bootstrap/state.js'
import { checkStatsigFeatureGate_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js'
import type { SessionId } from '../types/ids.js'
import { isEnvTruthy } from '../utils/envUtils.js'

// -- config

// Immutable values snapshotted once at query() entry. Separating these from
// the per-iteration State struct and the mutable ToolUseContext makes future
// step() extraction tractable — a pure reducer can take (state, event, config)
// where config is plain data.
//
// Intentionally excludes feature() gates — those are tree-shaking boundaries
// and must stay inline at the guarded blocks for dead-code elimination.
export type QueryConfig = {
  sessionId: SessionId

  // Runtime gates (env/statsig). NOT feature() gates — see above.
  gates: {
    // Statsig — CACHED_MAY_BE_STALE already admits staleness, so snapshotting
    // once per query() call stays within the existing contract.
    streamingToolExecution: boolean
    emitToolUseSummaries: boolean
    isAnt: boolean
    fastModeEnabled: boolean
  }
}

export function buildQueryConfig(): QueryConfig {
  return {
    sessionId: getSessionId(),
    gates: {
      streamingToolExecution: checkStatsigFeatureGate_CACHED_MAY_BE_STALE(
        'tengu_streaming_tool_execution2',
      ),
      emitToolUseSummaries: isEnvTruthy(
        process.env.CLAUDE_CODE_EMIT_TOOL_USE_SUMMARIES,
      ),
      isAnt: process.env.USER_TYPE === 'ant',
      // Inlined from fastMode.ts to avoid pulling its heavy module graph
      // (axios, settings, auth, model, oauth, config) into test shards that
      // didn't previously load it — changes init order and breaks unrelated tests.
      fastModeEnabled: !isEnvTruthy(process.env.CLAUDE_CODE_DISABLE_FAST_MODE),
    },
  }
}

```

---


### `src/query/deps.ts`

**信息:**
- 行数: 40
- 大小: 1445 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { randomUUID } from 'crypto'
import { queryModelWithStreaming } from '../services/api/claude.js'
import { autoCompactIfNeeded } from '../services/compact/autoCompact.js'
import { microcompactMessages } from '../services/compact/microCompact.js'

// -- deps

// I/O dependencies for query(). Passing a `deps` override into QueryParams
// lets tests inject fakes directly instead of spyOn-per-module — the most
// common mocks (callModel, autocompact) are each spied in 6-8 test files
// today with module-import-and-spy boilerplate.
//
// Using `typeof fn` keeps signatures in sync with the real implementations
// automatically. This file imports the real functions for both typing and
// the production factory — tests that import this file for typing are
// already importing query.ts (which imports everything), so there's no
// new module-graph cost.
//
// Scope is intentionally narrow (4 deps) to prove the pattern. Followup
// PRs can add runTools, handleStopHooks, logEvent, queue ops, etc.
export type QueryDeps = {
  // -- model
  callModel: typeof queryModelWithStreaming

  // -- compaction
  microcompact: typeof microcompactMessages
  autocompact: typeof autoCompactIfNeeded

  // -- platform
  uuid: () => string
}

export function productionDeps(): QueryDeps {
  return {
    callModel: queryModelWithStreaming,
    microcompact: microcompactMessages,
    autocompact: autoCompactIfNeeded,
    uuid: randomUUID,
  }
}

```

---


### `src/query/stopHooks.ts`

**信息:**
- 行数: 473
- 大小: 17290 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { getShortcutDisplay } from '../keybindings/shortcutFormat.js'
import { isExtractModeActive } from '../memdir/paths.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import type { ToolUseContext } from '../Tool.js'
import type { HookProgress } from '../types/hooks.js'
import type {
  AssistantMessage,
  Message,
  RequestStartEvent,
  StopHookInfo,
  StreamEvent,
  TombstoneMessage,
  ToolUseSummaryMessage,
} from '../types/message.js'
import { createAttachmentMessage } from '../utils/attachments.js'
import { logForDebugging } from '../utils/debug.js'
import { errorMessage } from '../utils/errors.js'
import type { REPLHookContext } from '../utils/hooks/postSamplingHooks.js'
import {
  executeStopHooks,
  executeTaskCompletedHooks,
  executeTeammateIdleHooks,
  getStopHookMessage,
  getTaskCompletedHookMessage,
  getTeammateIdleHookMessage,
} from '../utils/hooks.js'
import {
  createStopHookSummaryMessage,
  createSystemMessage,
  createUserInterruptionMessage,
  createUserMessage,
} from '../utils/messages.js'
import type { SystemPrompt } from '../utils/systemPromptType.js'
import { getTaskListId, listTasks } from '../utils/tasks.js'
import { getAgentName, getTeamName, isTeammate } from '../utils/teammate.js'

/* eslint-disable @typescript-eslint/no-require-imports */
const extractMemoriesModule = feature('EXTRACT_MEMORIES')
  ? (require('../services/extractMemories/extractMemories.js') as typeof import('../services/extractMemories/extractMemories.js'))
  : null
const jobClassifierModule = feature('TEMPLATES')
  ? (require('../jobs/classifier.js') as typeof import('../jobs/classifier.js'))
  : null

/* eslint-enable @typescript-eslint/no-require-imports */


```

---


### `src/query/tokenBudget.ts`

**信息:**
- 行数: 93
- 大小: 2320 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getBudgetContinuationMessage } from '../utils/tokenBudget.js'

const COMPLETION_THRESHOLD = 0.9
const DIMINISHING_THRESHOLD = 500

export type BudgetTracker = {
  continuationCount: number
  lastDeltaTokens: number
  lastGlobalTurnTokens: number
  startedAt: number
}

export function createBudgetTracker(): BudgetTracker {
  return {
    continuationCount: 0,
    lastDeltaTokens: 0,
    lastGlobalTurnTokens: 0,
    startedAt: Date.now(),
  }
}

type ContinueDecision = {
  action: 'continue'
  nudgeMessage: string
  continuationCount: number
  pct: number
  turnTokens: number
  budget: number
}

type StopDecision = {
  action: 'stop'
  completionEvent: {
    continuationCount: number
    pct: number
    turnTokens: number
    budget: number
    diminishingReturns: boolean
    durationMs: number
  } | null
}

export type TokenBudgetDecision = ContinueDecision | StopDecision

export function checkTokenBudget(
  tracker: BudgetTracker,
  agentId: string | undefined,
  budget: number | null,
  globalTurnTokens: number,
): TokenBudgetDecision {

```

---


### `src/query/transitions.ts`

**信息:**
- 行数: 3
- 大小: 72 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function transitionQueryState<T>(value: T): T {
  return value
}

```

---

