# state 模块

## 概述

**位置:** `src/state/`

## 文件统计

- TypeScript 文件: 5
- TypeScript React 文件: 1
- 总计: 6

## 文件详情

---


### `src/state/AppState.tsx`

**信息:**
- 行数: 200
- 大小: 23480 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import React, { useContext, useEffect, useEffectEvent, useState, useSyncExternalStore } from 'react';
import { MailboxProvider } from '../context/mailbox.js';
import { useSettingsChange } from '../hooks/useSettingsChange.js';
import { logForDebugging } from '../utils/debug.js';
import { createDisabledBypassPermissionsContext, isBypassPermissionsModeDisabled } from '../utils/permissions/permissionSetup.js';
import { applySettingsChange } from '../utils/settings/applySettingsChange.js';
import type { SettingSource } from '../utils/settings/constants.js';
import { createStore } from './store.js';

// DCE: voice context is ant-only. External builds get a passthrough.
/* eslint-disable @typescript-eslint/no-require-imports */
const VoiceProvider: (props: {
  children: React.ReactNode;
}) => React.ReactNode = feature('VOICE_MODE') ? require('../context/voice.js').VoiceProvider : ({
  children
}) => children;

/* eslint-enable @typescript-eslint/no-require-imports */
import { type AppState, type AppStateStore, getDefaultAppState } from './AppStateStore.js';

// TODO: Remove these re-exports once all callers import directly from
// ./AppStateStore.js. Kept for back-compat during migration so .ts callers
// can incrementally move off the .tsx import and stop pulling React.
export { type AppState, type AppStateStore, type CompletionBoundary, getDefaultAppState, IDLE_SPECULATION_STATE, type SpeculationResult, type SpeculationState } from './AppStateStore.js';
export const AppStoreContext = React.createContext<AppStateStore | null>(null);
type Props = {
  children: React.ReactNode;
  initialState?: AppState;
  onChangeAppState?: (args: {
    newState: AppState;
    oldState: AppState;
  }) => void;
};
const HasAppStateContext = React.createContext<boolean>(false);
export function AppStateProvider(t0) {
  const $ = _c(13);
  const {
    children,
    initialState,
    onChangeAppState
  } = t0;
  const hasAppStateContext = useContext(HasAppStateContext);
  if (hasAppStateContext) {
    throw new Error("AppStateProvider can not be nested within another AppStateProvider");
  }
  let t1;
  if ($[0] !== initialState || $[1] !== onChangeAppState) {
    t1 = () => createStore(initialState ?? getDefaultAppState(), onChangeAppState);

```

---


### `src/state/AppStateStore.ts`

**信息:**
- 行数: 569
- 大小: 21847 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Notification } from 'src/context/notifications.js'
import type { TodoList } from 'src/utils/todo/types.js'
import type { BridgePermissionCallbacks } from '../bridge/bridgePermissionCallbacks.js'
import type { Command } from '../commands.js'
import type { ChannelPermissionCallbacks } from '../services/mcp/channelPermissions.js'
import type { ElicitationRequestEvent } from '../services/mcp/elicitationHandler.js'
import type {
  MCPServerConnection,
  ServerResource,
} from '../services/mcp/types.js'
import { shouldEnablePromptSuggestion } from '../services/PromptSuggestion/promptSuggestion.js'
import {
  getEmptyToolPermissionContext,
  type Tool,
  type ToolPermissionContext,
} from '../Tool.js'
import type { TaskState } from '../tasks/types.js'
import type { AgentColorName } from '../tools/AgentTool/agentColorManager.js'
import type { AgentDefinitionsResult } from '../tools/AgentTool/loadAgentsDir.js'
import type { AllowedPrompt } from '../tools/ExitPlanModeTool/ExitPlanModeV2Tool.js'
import type { AgentId } from '../types/ids.js'
import type { Message, UserMessage } from '../types/message.js'
import type { LoadedPlugin, PluginError } from '../types/plugin.js'
import type { DeepImmutable } from '../types/utils.js'
import {
  type AttributionState,
  createEmptyAttributionState,
} from '../utils/commitAttribution.js'
import type { EffortValue } from '../utils/effort.js'
import type { FileHistoryState } from '../utils/fileHistory.js'
import type { REPLHookContext } from '../utils/hooks/postSamplingHooks.js'
import type { SessionHooksState } from '../utils/hooks/sessionHooks.js'
import type { ModelSetting } from '../utils/model/model.js'
import type { DenialTrackingState } from '../utils/permissions/denialTracking.js'
import type { PermissionMode } from '../utils/permissions/PermissionMode.js'
import { getInitialSettings } from '../utils/settings/settings.js'
import type { SettingsJson } from '../utils/settings/types.js'
import { shouldEnableThinkingByDefault } from '../utils/thinking.js'
import type { Store } from './store.js'

export type CompletionBoundary =
  | { type: 'complete'; completedAt: number; outputTokens: number }
  | { type: 'bash'; command: string; completedAt: number }
  | { type: 'edit'; toolName: string; filePath: string; completedAt: number }
  | {
      type: 'denied_tool'
      toolName: string
      detail: string
      completedAt: number
    }

```

---


### `src/state/onChangeAppState.ts`

**信息:**
- 行数: 171
- 大小: 6197 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { setMainLoopModelOverride } from '../bootstrap/state.js'
import {
  clearApiKeyHelperCache,
  clearAwsCredentialsCache,
  clearGcpCredentialsCache,
} from '../utils/auth.js'
import { getGlobalConfig, saveGlobalConfig } from '../utils/config.js'
import { toError } from '../utils/errors.js'
import { logError } from '../utils/log.js'
import { applyConfigEnvironmentVariables } from '../utils/managedEnv.js'
import {
  permissionModeFromString,
  toExternalPermissionMode,
} from '../utils/permissions/PermissionMode.js'
import {
  notifyPermissionModeChanged,
  notifySessionMetadataChanged,
  type SessionExternalMetadata,
} from '../utils/sessionState.js'
import { updateSettingsForSource } from '../utils/settings/settings.js'
import type { AppState } from './AppStateStore.js'

// Inverse of the push below — restore on worker restart.
export function externalMetadataToAppState(
  metadata: SessionExternalMetadata,
): (prev: AppState) => AppState {
  return prev => ({
    ...prev,
    ...(typeof metadata.permission_mode === 'string'
      ? {
          toolPermissionContext: {
            ...prev.toolPermissionContext,
            mode: permissionModeFromString(metadata.permission_mode),
          },
        }
      : {}),
    ...(typeof metadata.is_ultraplan_mode === 'boolean'
      ? { isUltraplanMode: metadata.is_ultraplan_mode }
      : {}),
  })
}

export function onChangeAppState({
  newState,
  oldState,
}: {
  newState: AppState
  oldState: AppState
}) {
  // toolPermissionContext.mode — single choke point for CCR/SDK mode sync.

```

---


### `src/state/selectors.ts`

**信息:**
- 行数: 76
- 大小: 2240 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Selectors for deriving computed state from AppState.
 * Keep selectors pure and simple - just data extraction, no side effects.
 */

import type { InProcessTeammateTaskState } from '../tasks/InProcessTeammateTask/types.js'
import { isInProcessTeammateTask } from '../tasks/InProcessTeammateTask/types.js'
import type { LocalAgentTaskState } from '../tasks/LocalAgentTask/LocalAgentTask.js'
import type { AppState } from './AppStateStore.js'

/**
 * Get the currently viewed teammate task, if any.
 * Returns undefined if:
 * - No teammate is being viewed (viewingAgentTaskId is undefined)
 * - The task ID doesn't exist in tasks
 * - The task is not an in-process teammate task
 */
export function getViewedTeammateTask(
  appState: Pick<AppState, 'viewingAgentTaskId' | 'tasks'>,
): InProcessTeammateTaskState | undefined {
  const { viewingAgentTaskId, tasks } = appState

  // Not viewing any teammate
  if (!viewingAgentTaskId) {
    return undefined
  }

  // Look up the task
  const task = tasks[viewingAgentTaskId]
  if (!task) {
    return undefined
  }

  // Verify it's an in-process teammate task
  if (!isInProcessTeammateTask(task)) {
    return undefined
  }

  return task
}

/**
 * Return type for getActiveAgentForInput selector.
 * Discriminated union for type-safe input routing.
 */
export type ActiveAgentForInput =
  | { type: 'leader' }
  | { type: 'viewed'; task: InProcessTeammateTaskState }
  | { type: 'named_agent'; task: LocalAgentTaskState }


```

---


### `src/state/store.ts`

**信息:**
- 行数: 34
- 大小: 836 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
type Listener = () => void
type OnChange<T> = (args: { newState: T; oldState: T }) => void

export type Store<T> = {
  getState: () => T
  setState: (updater: (prev: T) => T) => void
  subscribe: (listener: Listener) => () => void
}

export function createStore<T>(
  initialState: T,
  onChange?: OnChange<T>,
): Store<T> {
  let state = initialState
  const listeners = new Set<Listener>()

  return {
    getState: () => state,

    setState: (updater: (prev: T) => T) => {
      const prev = state
      const next = updater(prev)
      if (Object.is(next, prev)) return
      state = next
      onChange?.({ newState: next, oldState: prev })
      for (const listener of listeners) listener()
    },

    subscribe: (listener: Listener) => {
      listeners.add(listener)
      return () => listeners.delete(listener)
    },
  }
}

```

---


### `src/state/teammateViewHelpers.ts`

**信息:**
- 行数: 141
- 大小: 4399 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { logEvent } from '../services/analytics/index.js'
import { isTerminalTaskStatus } from '../Task.js'
import type { LocalAgentTaskState } from '../tasks/LocalAgentTask/LocalAgentTask.js'

// Inlined from framework.ts — importing creates a cycle through
// BackgroundTasksDialog. Keep in sync with PANEL_GRACE_MS there.
const PANEL_GRACE_MS = 30_000

import type { AppState } from './AppState.js'

// Inline type check instead of importing isLocalAgentTask — breaks the
// teammateViewHelpers → LocalAgentTask runtime edge that creates a cycle
// through BackgroundTasksDialog.
function isLocalAgent(task: unknown): task is LocalAgentTaskState {
  return (
    typeof task === 'object' &&
    task !== null &&
    'type' in task &&
    task.type === 'local_agent'
  )
}

/**
 * Return the task released back to stub form: retain dropped, messages
 * cleared, evictAfter set if terminal. Shared by exitTeammateView and
 * the switch-away path in enterTeammateView.
 */
function release(task: LocalAgentTaskState): LocalAgentTaskState {
  return {
    ...task,
    retain: false,
    messages: undefined,
    diskLoaded: false,
    evictAfter: isTerminalTaskStatus(task.status)
      ? Date.now() + PANEL_GRACE_MS
      : undefined,
  }
}

/**
 * Transitions the UI to view a teammate's transcript.
 * Sets viewingAgentTaskId and, for local_agent, retain: true (blocks eviction,
 * enables stream-append, triggers disk bootstrap) and clears evictAfter.
 * If switching from another agent, releases the previous one back to stub.
 */
export function enterTeammateView(
  taskId: string,
  setAppState: (updater: (prev: AppState) => AppState) => void,
): void {
  logEvent('tengu_transcript_view_enter', {})

```

---

