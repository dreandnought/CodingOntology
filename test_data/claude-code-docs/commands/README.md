# commands 模块

## 概述

**位置:** `src/commands/`

## 文件统计

- TypeScript 文件: 116
- TypeScript React 文件: 79
- 总计: 195

## 文件详情

---


### `src/commands/add-dir/add-dir.tsx`

**信息:**
- 行数: 126
- 大小: 18017 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import figures from 'figures';
import React, { useEffect } from 'react';
import { getAdditionalDirectoriesForClaudeMd, setAdditionalDirectoriesForClaudeMd } from '../../bootstrap/state.js';
import type { LocalJSXCommandContext } from '../../commands.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { AddWorkspaceDirectory } from '../../components/permissions/rules/AddWorkspaceDirectory.js';
import { Box, Text } from '../../ink.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { applyPermissionUpdate, persistPermissionUpdate } from '../../utils/permissions/PermissionUpdate.js';
import type { PermissionUpdateDestination } from '../../utils/permissions/PermissionUpdateSchema.js';
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js';
import { addDirHelpMessage, validateDirectoryForWorkspace } from './validation.js';
function AddDirError(t0) {
  const $ = _c(10);
  const {
    message,
    args,
    onDone
  } = t0;
  let t1;
  let t2;
  if ($[0] !== onDone) {
    t1 = () => {
      const timer = setTimeout(onDone, 0);
      return () => clearTimeout(timer);
    };
    t2 = [onDone];
    $[0] = onDone;
    $[1] = t1;
    $[2] = t2;
  } else {
    t1 = $[1];
    t2 = $[2];
  }
  useEffect(t1, t2);
  let t3;
  if ($[3] !== args) {
    t3 = <Text dimColor={true}>{figures.pointer} /add-dir {args}</Text>;
    $[3] = args;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  let t4;
  if ($[5] !== message) {
    t4 = <MessageResponse><Text>{message}</Text></MessageResponse>;
    $[5] = message;
    $[6] = t4;

```

---


### `src/commands/add-dir/index.ts`

**信息:**
- 行数: 11
- 大小: 260 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const addDir = {
  type: 'local-jsx',
  name: 'add-dir',
  description: 'Add a new working directory',
  argumentHint: '<path>',
  load: () => import('./add-dir.js'),
} satisfies Command

export default addDir

```

---


### `src/commands/add-dir/validation.ts`

**信息:**
- 行数: 110
- 大小: 3207 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import chalk from 'chalk'
import { stat } from 'fs/promises'
import { dirname, resolve } from 'path'
import type { ToolPermissionContext } from '../../Tool.js'
import { getErrnoCode } from '../../utils/errors.js'
import { expandPath } from '../../utils/path.js'
import {
  allWorkingDirectories,
  pathInWorkingPath,
} from '../../utils/permissions/filesystem.js'

export type AddDirectoryResult =
  | {
      resultType: 'success'
      absolutePath: string
    }
  | {
      resultType: 'emptyPath'
    }
  | {
      resultType: 'pathNotFound' | 'notADirectory'
      directoryPath: string
      absolutePath: string
    }
  | {
      resultType: 'alreadyInWorkingDirectory'
      directoryPath: string
      workingDir: string
    }

export async function validateDirectoryForWorkspace(
  directoryPath: string,
  permissionContext: ToolPermissionContext,
): Promise<AddDirectoryResult> {
  if (!directoryPath) {
    return {
      resultType: 'emptyPath',
    }
  }

  // resolve() strips the trailing slash expandPath can leave on absolute
  // inputs, so /foo and /foo/ map to the same storage key (CC-33).
  const absolutePath = resolve(expandPath(directoryPath))

  // Check if path exists and is a directory (single syscall)
  try {
    const stats = await stat(absolutePath)
    if (!stats.isDirectory()) {
      return {
        resultType: 'notADirectory',

```

---


### `src/commands/advisor.ts`

**信息:**
- 行数: 109
- 大小: 3182 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../commands.js'
import type { LocalCommandCall } from '../types/command.js'
import {
  canUserConfigureAdvisor,
  isValidAdvisorModel,
  modelSupportsAdvisor,
} from '../utils/advisor.js'
import {
  getDefaultMainLoopModelSetting,
  normalizeModelStringForAPI,
  parseUserSpecifiedModel,
} from '../utils/model/model.js'
import { validateModel } from '../utils/model/validateModel.js'
import { updateSettingsForSource } from '../utils/settings/settings.js'

const call: LocalCommandCall = async (args, context) => {
  const arg = args.trim().toLowerCase()
  const baseModel = parseUserSpecifiedModel(
    context.getAppState().mainLoopModel ?? getDefaultMainLoopModelSetting(),
  )

  if (!arg) {
    const current = context.getAppState().advisorModel
    if (!current) {
      return {
        type: 'text',
        value:
          'Advisor: not set\nUse "/advisor <model>" to enable (e.g. "/advisor opus").',
      }
    }
    if (!modelSupportsAdvisor(baseModel)) {
      return {
        type: 'text',
        value: `Advisor: ${current} (inactive)\nThe current model (${baseModel}) does not support advisors.`,
      }
    }
    return {
      type: 'text',
      value: `Advisor: ${current}\nUse "/advisor unset" to disable or "/advisor <model>" to change.`,
    }
  }

  if (arg === 'unset' || arg === 'off') {
    const prev = context.getAppState().advisorModel
    context.setAppState(s => {
      if (s.advisorModel === undefined) return s
      return { ...s, advisorModel: undefined }
    })
    updateSettingsForSource('userSettings', { advisorModel: undefined })
    return {

```

---


### `src/commands/agents/agents.tsx`

**信息:**
- 行数: 12
- 大小: 2500 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { AgentsMenu } from '../../components/agents/AgentsMenu.js';
import type { ToolUseContext } from '../../Tool.js';
import { getTools } from '../../tools.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
export async function call(onDone: LocalJSXCommandOnDone, context: ToolUseContext): Promise<React.ReactNode> {
  const appState = context.getAppState();
  const permissionContext = appState.toolPermissionContext;
  const tools = getTools(permissionContext);
  return <AgentsMenu tools={tools} onExit={onDone} />;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkFnZW50c01lbnUiLCJUb29sVXNlQ29udGV4dCIsImdldFRvb2xzIiwiTG9jYWxKU1hDb21tYW5kT25Eb25lIiwiY2FsbCIsIm9uRG9uZSIsImNvbnRleHQiLCJQcm9taXNlIiwiUmVhY3ROb2RlIiwiYXBwU3RhdGUiLCJnZXRBcHBTdGF0ZSIsInBlcm1pc3Npb25Db250ZXh0IiwidG9vbFBlcm1pc3Npb25Db250ZXh0IiwidG9vbHMiXSwic291cmNlcyI6WyJhZ2VudHMudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgQWdlbnRzTWVudSB9IGZyb20gJy4uLy4uL2NvbXBvbmVudHMvYWdlbnRzL0FnZW50c01lbnUuanMnXG5pbXBvcnQgdHlwZSB7IFRvb2xVc2VDb250ZXh0IH0gZnJvbSAnLi4vLi4vVG9vbC5qcydcbmltcG9ydCB7IGdldFRvb2xzIH0gZnJvbSAnLi4vLi4vdG9vbHMuanMnXG5pbXBvcnQgdHlwZSB7IExvY2FsSlNYQ29tbWFuZE9uRG9uZSB9IGZyb20gJy4uLy4uL3R5cGVzL2NvbW1hbmQuanMnXG5cbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBjYWxsKFxuICBvbkRvbmU6IExvY2FsSlNYQ29tbWFuZE9uRG9uZSxcbiAgY29udGV4dDogVG9vbFVzZUNvbnRleHQsXG4pOiBQcm9taXNlPFJlYWN0LlJlYWN0Tm9kZT4ge1xuICBjb25zdCBhcHBTdGF0ZSA9IGNvbnRleHQuZ2V0QXBwU3RhdGUoKVxuICBjb25zdCBwZXJtaXNzaW9uQ29udGV4dCA9IGFwcFN0YXRlLnRvb2xQZXJtaXNzaW9uQ29udGV4dFxuICBjb25zdCB0b29scyA9IGdldFRvb2xzKHBlcm1pc3Npb25Db250ZXh0KVxuXG4gIHJldHVybiA8QWdlbnRzTWVudSB0b29scz17dG9vbHN9IG9uRXhpdD17b25Eb25lfSAvPlxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLFVBQVUsUUFBUSx1Q0FBdUM7QUFDbEUsY0FBY0MsY0FBYyxRQUFRLGVBQWU7QUFDbkQsU0FBU0MsUUFBUSxRQUFRLGdCQUFnQjtBQUN6QyxjQUFjQyxxQkFBcUIsUUFBUSx3QkFBd0I7QUFFbkUsT0FBTyxlQUFlQyxJQUFJQSxDQUN4QkMsTUFBTSxFQUFFRixxQkFBcUIsRUFDN0JHLE9BQU8sRUFBRUwsY0FBYyxDQUN4QixFQUFFTSxPQUFPLENBQUNSLEtBQUssQ0FBQ1MsU0FBUyxDQUFDLENBQUM7RUFDMUIsTUFBTUMsUUFBUSxHQUFHSCxPQUFPLENBQUNJLFdBQVcsQ0FBQyxDQUFDO0VBQ3RDLE1BQU1DLGlCQUFpQixHQUFHRixRQUFRLENBQUNHLHFCQUFxQjtFQUN4RCxNQUFNQyxLQUFLLEdBQUdYLFFBQVEsQ0FBQ1MsaUJBQWlCLENBQUM7RUFFekMsT0FBTyxDQUFDLFVBQVUsQ0FBQyxLQUFLLENBQUMsQ0FBQ0UsS0FBSyxDQUFDLENBQUMsTUFBTSxDQUFDLENBQUNSLE1BQU0sQ0FBQyxHQUFHO0FBQ3JEIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/agents/index.ts`

**信息:**
- 行数: 10
- 大小: 232 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const agents = {
  type: 'local-jsx',
  name: 'agents',
  description: 'Manage agent configurations',
  load: () => import('./agents.js'),
} satisfies Command

export default agents

```

---


### `src/commands/agents-platform/index.ts`

**信息:**
- 行数: 21
- 大小: 686 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
const agentsPlatform = {
  name: 'agents-platform',
  type: 'local',
  description:
    'Reserved internal command. This restored build keeps the command visible but does not include the original agents platform backend.',
  supportsNonInteractive: true,
  load: async () => ({
    async call() {
      return {
        type: 'text' as const,
        value:
          'agents-platform is not included in this restored workspace.\n\n' +
          'The command shell is present so callers fail cleanly, but the ' +
          'internal backend that powers platform-managed agents was not ' +
          'recoverable from source maps.',
      }
    },
  }),
}

export default agentsPlatform

```

---


### `src/commands/branch/branch.ts`

**信息:**
- 行数: 296
- 大小: 9580 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { randomUUID, type UUID } from 'crypto'
import { mkdir, readFile, writeFile } from 'fs/promises'
import { getOriginalCwd, getSessionId } from '../../bootstrap/state.js'
import type { LocalJSXCommandContext } from '../../commands.js'
import { logEvent } from '../../services/analytics/index.js'
import type { LocalJSXCommandOnDone } from '../../types/command.js'
import type {
  ContentReplacementEntry,
  Entry,
  LogOption,
  SerializedMessage,
  TranscriptMessage,
} from '../../types/logs.js'
import { parseJSONL } from '../../utils/json.js'
import {
  getProjectDir,
  getTranscriptPath,
  getTranscriptPathForSession,
  isTranscriptMessage,
  saveCustomTitle,
  searchSessionsByCustomTitle,
} from '../../utils/sessionStorage.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { escapeRegExp } from '../../utils/stringUtils.js'

type TranscriptEntry = TranscriptMessage & {
  forkedFrom?: {
    sessionId: string
    messageUuid: UUID
  }
}

/**
 * Derive a single-line title base from the first user message.
 * Collapses whitespace — multiline first messages (pasted stacks, code)
 * otherwise flow into the saved title and break the resume hint.
 */
export function deriveFirstPrompt(
  firstUserMessage: Extract<SerializedMessage, { type: 'user' }> | undefined,
): string {
  const content = firstUserMessage?.message?.content
  if (!content) return 'Branched conversation'
  const raw =
    typeof content === 'string'
      ? content
      : content.find(
          (block): block is { type: 'text'; text: string } =>
            block.type === 'text',
        )?.text
  if (!raw) return 'Branched conversation'

```

---


### `src/commands/branch/index.ts`

**信息:**
- 行数: 14
- 大小: 445 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { Command } from '../../commands.js'

const branch = {
  type: 'local-jsx',
  name: 'branch',
  // 'fork' alias only when /fork doesn't exist as its own command
  aliases: feature('FORK_SUBAGENT') ? [] : ['fork'],
  description: 'Create a branch of the current conversation at this point',
  argumentHint: '[name]',
  load: () => import('./branch.js'),
} satisfies Command

export default branch

```

---


### `src/commands/bridge/bridge.tsx`

**信息:**
- 行数: 509
- 大小: 46907 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import { toString as qrToString } from 'qrcode';
import * as React from 'react';
import { useEffect, useState } from 'react';
import { getBridgeAccessToken } from '../../bridge/bridgeConfig.js';
import { checkBridgeMinVersion, getBridgeDisabledReason, isEnvLessBridgeEnabled } from '../../bridge/bridgeEnabled.js';
import { checkEnvLessBridgeMinVersion } from '../../bridge/envLessBridgeConfig.js';
import { BRIDGE_LOGIN_INSTRUCTION, REMOTE_CONTROL_DISCONNECTED_MSG } from '../../bridge/types.js';
import { Dialog } from '../../components/design-system/Dialog.js';
import { ListItem } from '../../components/design-system/ListItem.js';
import { shouldShowRemoteCallout } from '../../components/RemoteCallout.js';
import { useRegisterOverlay } from '../../context/overlayContext.js';
import { Box, Text } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../services/analytics/index.js';
import { useAppState, useSetAppState } from '../../state/AppState.js';
import type { ToolUseContext } from '../../Tool.js';
import type { LocalJSXCommandContext, LocalJSXCommandOnDone } from '../../types/command.js';
import { logForDebugging } from '../../utils/debug.js';
type Props = {
  onDone: LocalJSXCommandOnDone;
  name?: string;
};

/**
 * /remote-control command — manages the bidirectional bridge connection.
 *
 * When enabled, sets replBridgeEnabled in AppState, which triggers
 * useReplBridge in REPL.tsx to initialize the bridge connection.
 * The bridge registers an environment, creates a session with the current
 * conversation, polls for work, and connects an ingress WebSocket for
 * bidirectional messaging between the CLI and claude.ai.
 *
 * Running /remote-control when already connected shows a dialog with the session
 * URL and options to disconnect or continue.
 */
function BridgeToggle(t0) {
  const $ = _c(10);
  const {
    onDone,
    name
  } = t0;
  const setAppState = useSetAppState();
  const replBridgeConnected = useAppState(_temp);
  const replBridgeEnabled = useAppState(_temp2);
  const replBridgeOutboundOnly = useAppState(_temp3);
  const [showDisconnectDialog, setShowDisconnectDialog] = useState(false);
  let t1;
  if ($[0] !== name || $[1] !== onDone || $[2] !== replBridgeConnected || $[3] !== replBridgeEnabled || $[4] !== replBridgeOutboundOnly || $[5] !== setAppState) {

```

---


### `src/commands/bridge/index.ts`

**信息:**
- 行数: 26
- 大小: 604 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { isBridgeEnabled } from '../../bridge/bridgeEnabled.js'
import type { Command } from '../../commands.js'

function isEnabled(): boolean {
  if (!feature('BRIDGE_MODE')) {
    return false
  }
  return isBridgeEnabled()
}

const bridge = {
  type: 'local-jsx',
  name: 'remote-control',
  aliases: ['rc'],
  description: 'Connect this terminal for remote-control sessions',
  argumentHint: '[name]',
  isEnabled,
  get isHidden() {
    return !isEnabled()
  },
  immediate: true,
  load: () => import('./bridge.js'),
} satisfies Command

export default bridge

```

---


### `src/commands/bridge-kick.ts`

**信息:**
- 行数: 200
- 大小: 6703 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getBridgeDebugHandle } from '../bridge/bridgeDebug.js'
import type { Command } from '../commands.js'
import type { LocalCommandCall } from '../types/command.js'

/**
 * Ant-only: inject bridge failure states to manually test recovery paths.
 *
 *   /bridge-kick close 1002            — fire ws_closed with code 1002
 *   /bridge-kick close 1006            — fire ws_closed with code 1006
 *   /bridge-kick poll 404              — next poll throws 404/not_found_error
 *   /bridge-kick poll 404 <type>       — next poll throws 404 with error_type
 *   /bridge-kick poll 401              — next poll throws 401 (auth)
 *   /bridge-kick poll transient        — next poll throws axios-style rejection
 *   /bridge-kick register fail         — next register (inside doReconnect) transient-fails
 *   /bridge-kick register fail 3       — next 3 registers transient-fail
 *   /bridge-kick register fatal        — next register 403s (terminal)
 *   /bridge-kick reconnect-session fail — POST /bridge/reconnect fails (→ Strategy 2)
 *   /bridge-kick heartbeat 401         — next heartbeat 401s (JWT expired)
 *   /bridge-kick reconnect             — call doReconnect directly (= SIGUSR2)
 *   /bridge-kick status                — print current bridge state
 *
 * Workflow: connect Remote Control, run a subcommand, `tail -f debug.log`
 * and watch [bridge:repl] / [bridge:debug] lines for the recovery reaction.
 *
 * Composite sequences — the failure modes in the BQ data are chains, not
 * single events. Queue faults then fire the trigger:
 *
 *   # #22148 residual: ws_closed → register transient-blips → teardown?
 *   /bridge-kick register fail 2
 *   /bridge-kick close 1002
 *   → expect: doReconnect tries register, fails, returns false → teardown
 *     (demonstrates the retry gap that needs fixing)
 *
 *   # Dead gate: poll 404/not_found_error → does onEnvironmentLost fire?
 *   /bridge-kick poll 404
 *   → expect: tengu_bridge_repl_fatal_error (gate is dead — 147K/wk)
 *     after fix: tengu_bridge_repl_env_lost → doReconnect
 */

const USAGE = `/bridge-kick <subcommand>
  close <code>              fire ws_closed with the given code (e.g. 1002)
  poll <status> [type]      next poll throws BridgeFatalError(status, type)
  poll transient            next poll throws axios-style rejection (5xx/net)
  register fail [N]         next N registers transient-fail (default 1)
  register fatal            next register 403s (terminal)
  reconnect-session fail    next POST /bridge/reconnect fails
  heartbeat <status>        next heartbeat throws BridgeFatalError(status)
  reconnect                 call reconnectEnvironmentWithSession directly
  status                    print bridge state`


```

---


### `src/commands/brief.ts`

**信息:**
- 行数: 130
- 大小: 5173 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { z } from 'zod/v4'
import { getKairosActive, setUserMsgOptIn } from '../bootstrap/state.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import type { ToolUseContext } from '../Tool.js'
import { isBriefEntitled } from '../tools/BriefTool/BriefTool.js'
import { BRIEF_TOOL_NAME } from '../tools/BriefTool/prompt.js'
import type {
  Command,
  LocalJSXCommandContext,
  LocalJSXCommandOnDone,
} from '../types/command.js'
import { lazySchema } from '../utils/lazySchema.js'

// Zod guards against fat-fingered GB pushes (same pattern as pollConfig.ts /
// cronScheduler.ts). A malformed config falls back to DEFAULT_BRIEF_CONFIG
// entirely rather than being partially trusted.
const briefConfigSchema = lazySchema(() =>
  z.object({
    enable_slash_command: z.boolean(),
  }),
)
type BriefConfig = z.infer<ReturnType<typeof briefConfigSchema>>

const DEFAULT_BRIEF_CONFIG: BriefConfig = {
  enable_slash_command: false,
}

// No TTL — this gate controls slash-command *visibility*, not a kill switch.
// CACHED_MAY_BE_STALE still has one background-update flip (first call kicks
// off fetch; second call sees fresh value), but no additional flips after that.
// The tool-availability gate (tengu_kairos_brief in isBriefEnabled) keeps its
// 5-min TTL because that one IS a kill switch.
function getBriefConfig(): BriefConfig {
  const raw = getFeatureValue_CACHED_MAY_BE_STALE<unknown>(
    'tengu_kairos_brief_config',
    DEFAULT_BRIEF_CONFIG,
  )
  const parsed = briefConfigSchema().safeParse(raw)
  return parsed.success ? parsed.data : DEFAULT_BRIEF_CONFIG
}

const brief = {
  type: 'local-jsx',
  name: 'brief',
  description: 'Toggle brief-only mode',

```

---


### `src/commands/btw/btw.tsx`

**信息:**
- 行数: 243
- 大小: 30250 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { useInterval } from 'usehooks-ts';
import type { CommandResultDisplay } from '../../commands.js';
import { Markdown } from '../../components/Markdown.js';
import { SpinnerGlyph } from '../../components/Spinner/SpinnerGlyph.js';
import { DOWN_ARROW, UP_ARROW } from '../../constants/figures.js';
import { getSystemPrompt } from '../../constants/prompts.js';
import { useModalOrTerminalSize } from '../../context/modalContext.js';
import { getSystemContext, getUserContext } from '../../context.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import ScrollBox, { type ScrollBoxHandle } from '../../ink/components/ScrollBox.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text } from '../../ink.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import type { Message } from '../../types/message.js';
import { createAbortController } from '../../utils/abortController.js';
import { saveGlobalConfig } from '../../utils/config.js';
import { errorMessage } from '../../utils/errors.js';
import { type CacheSafeParams, getLastCacheSafeParams } from '../../utils/forkedAgent.js';
import { getMessagesAfterCompactBoundary } from '../../utils/messages.js';
import type { ProcessUserInputContext } from '../../utils/processUserInput/processUserInput.js';
import { runSideQuestion } from '../../utils/sideQuestion.js';
import { asSystemPrompt } from '../../utils/systemPromptType.js';
type BtwComponentProps = {
  question: string;
  context: ProcessUserInputContext;
  onDone: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
const CHROME_ROWS = 5;
const OUTER_CHROME_ROWS = 6;
const SCROLL_LINES = 3;
function BtwSideQuestion(t0) {
  const $ = _c(25);
  const {
    question,
    context,
    onDone
  } = t0;
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [frame, setFrame] = useState(0);
  const scrollRef = useRef(null);
  const {
    rows
  } = useModalOrTerminalSize(useTerminalSize());
  let t1;

```

---


### `src/commands/btw/index.ts`

**信息:**
- 行数: 13
- 大小: 314 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const btw = {
  type: 'local-jsx',
  name: 'btw',
  description:
    'Ask a quick side question without interrupting the main conversation',
  immediate: true,
  argumentHint: '<question>',
  load: () => import('./btw.js'),
} satisfies Command

export default btw

```

---


### `src/commands/chrome/chrome.tsx`

**信息:**
- 行数: 285
- 大小: 31974 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useState } from 'react';
import { type OptionWithDescription, Select } from '../../components/CustomSelect/select.js';
import { Dialog } from '../../components/design-system/Dialog.js';
import { Box, Text } from '../../ink.js';
import { useAppState } from '../../state/AppState.js';
import { isClaudeAISubscriber } from '../../utils/auth.js';
import { openBrowser } from '../../utils/browser.js';
import { CLAUDE_IN_CHROME_MCP_SERVER_NAME, openInChrome } from '../../utils/claudeInChrome/common.js';
import { isChromeExtensionInstalled } from '../../utils/claudeInChrome/setup.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { env } from '../../utils/env.js';
import { isRunningOnHomespace } from '../../utils/envUtils.js';
const CHROME_EXTENSION_URL = 'https://claude.ai/chrome';
const CHROME_PERMISSIONS_URL = 'https://clau.de/chrome/permissions';
const CHROME_RECONNECT_URL = 'https://clau.de/chrome/reconnect';
type MenuAction = 'install-extension' | 'reconnect' | 'manage-permissions' | 'toggle-default';
type Props = {
  onDone: (result?: string) => void;
  isExtensionInstalled: boolean;
  configEnabled: boolean | undefined;
  isClaudeAISubscriber: boolean;
  isWSL: boolean;
};
function ClaudeInChromeMenu(t0) {
  const $ = _c(41);
  const {
    onDone,
    isExtensionInstalled: installed,
    configEnabled,
    isClaudeAISubscriber,
    isWSL
  } = t0;
  const mcpClients = useAppState(_temp);
  const [selectKey, setSelectKey] = useState(0);
  const [enabledByDefault, setEnabledByDefault] = useState(configEnabled ?? false);
  const [showInstallHint, setShowInstallHint] = useState(false);
  const [isExtensionInstalled, setIsExtensionInstalled] = useState(installed);
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = false && isRunningOnHomespace();
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const isHomespace = t1;
  let t2;
  if ($[1] !== mcpClients) {
    t2 = mcpClients.find(_temp2);
    $[1] = mcpClients;

```

---


### `src/commands/chrome/index.ts`

**信息:**
- 行数: 13
- 大小: 381 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getIsNonInteractiveSession } from '../../bootstrap/state.js'
import type { Command } from '../../commands.js'

const command: Command = {
  name: 'chrome',
  description: 'Claude in Chrome (Beta) settings',
  availability: ['claude-ai'],
  isEnabled: () => !getIsNonInteractiveSession(),
  type: 'local-jsx',
  load: () => import('./chrome.js'),
}

export default command

```

---


### `src/commands/clear/caches.ts`

**信息:**
- 行数: 144
- 大小: 6370 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Session cache clearing utilities.
 * This module is imported at startup by main.tsx, so keep imports minimal.
 */
import { feature } from 'bun:bundle'
import {
  clearInvokedSkills,
  setLastEmittedDate,
} from '../../bootstrap/state.js'
import { clearCommandsCache } from '../../commands.js'
import { getSessionStartDate } from '../../constants/common.js'
import {
  getGitStatus,
  getSystemContext,
  getUserContext,
  setSystemPromptInjection,
} from '../../context.js'
import { clearFileSuggestionCaches } from '../../hooks/fileSuggestions.js'
import { clearAllPendingCallbacks } from '../../hooks/useSwarmPermissionPoller.js'
import { clearAllDumpState } from '../../services/api/dumpPrompts.js'
import { resetPromptCacheBreakDetection } from '../../services/api/promptCacheBreakDetection.js'
import { clearAllSessions } from '../../services/api/sessionIngress.js'
import { runPostCompactCleanup } from '../../services/compact/postCompactCleanup.js'
import { resetAllLSPDiagnosticState } from '../../services/lsp/LSPDiagnosticRegistry.js'
import { clearTrackedMagicDocs } from '../../services/MagicDocs/magicDocs.js'
import { clearDynamicSkills } from '../../skills/loadSkillsDir.js'
import { resetSentSkillNames } from '../../utils/attachments.js'
import { clearCommandPrefixCaches } from '../../utils/bash/commands.js'
import { resetGetMemoryFilesCache } from '../../utils/claudemd.js'
import { clearRepositoryCaches } from '../../utils/detectRepository.js'
import { clearResolveGitDirCache } from '../../utils/git/gitFilesystem.js'
import { clearStoredImagePaths } from '../../utils/imageStore.js'
import { clearSessionEnvVars } from '../../utils/sessionEnvVars.js'

/**
 * Clear all session-related caches.
 * Call this when resuming a session to ensure fresh file/skill discovery.
 * This is a subset of what clearConversation does - it only clears caches
 * without affecting messages, session ID, or triggering hooks.
 *
 * @param preservedAgentIds - Agent IDs whose per-agent state should survive
 *   the clear (e.g., background tasks preserved across /clear). When non-empty,
 *   agentId-keyed state (invoked skills) is selectively cleared and requestId-keyed
 *   state (pending permission callbacks, dump state, cache-break tracking) is left
 *   intact since it cannot be safely scoped to the main session.
 */
export function clearSessionCaches(
  preservedAgentIds: ReadonlySet<string> = new Set(),
): void {
  const hasPreserved = preservedAgentIds.size > 0

```

---


### `src/commands/clear/clear/caches.ts`

**信息:**
- 行数: 1
- 大小: 18 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export default {}

```

---


### `src/commands/clear/clear/conversation.ts`

**信息:**
- 行数: 1
- 大小: 18 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export default {}

```

---


### `src/commands/clear/clear.ts`

**信息:**
- 行数: 7
- 大小: 254 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { LocalCommandCall } from '../../types/command.js'
import { clearConversation } from './conversation.js'

export const call: LocalCommandCall = async (_, context) => {
  await clearConversation(context)
  return { type: 'text', value: '' }
}

```

---


### `src/commands/clear/conversation.ts`

**信息:**
- 行数: 251
- 大小: 9325 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Conversation clearing utility.
 * This module has heavier dependencies and should be lazy-loaded when possible.
 */
import { feature } from 'bun:bundle'
import { randomUUID, type UUID } from 'crypto'
import {
  getLastMainRequestId,
  getOriginalCwd,
  getSessionId,
  regenerateSessionId,
} from '../../bootstrap/state.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import type { AppState } from '../../state/AppState.js'
import { isInProcessTeammateTask } from '../../tasks/InProcessTeammateTask/types.js'
import {
  isLocalAgentTask,
  type LocalAgentTaskState,
} from '../../tasks/LocalAgentTask/LocalAgentTask.js'
import { isLocalShellTask } from '../../tasks/LocalShellTask/guards.js'
import { asAgentId } from '../../types/ids.js'
import type { Message } from '../../types/message.js'
import { createEmptyAttributionState } from '../../utils/commitAttribution.js'
import type { FileStateCache } from '../../utils/fileStateCache.js'
import {
  executeSessionEndHooks,
  getSessionEndHookTimeoutMs,
} from '../../utils/hooks.js'
import { logError } from '../../utils/log.js'
import { clearAllPlanSlugs } from '../../utils/plans.js'
import { setCwd } from '../../utils/Shell.js'
import { processSessionStartHooks } from '../../utils/sessionStart.js'
import {
  clearSessionMetadata,
  getAgentTranscriptPath,
  resetSessionFilePointer,
  saveWorktreeState,
} from '../../utils/sessionStorage.js'
import {
  evictTaskOutput,
  initTaskOutputAsSymlink,
} from '../../utils/task/diskOutput.js'
import { getCurrentWorktreeSession } from '../../utils/worktree.js'
import { clearSessionCaches } from './caches.js'

export async function clearConversation({
  setMessages,

```

---


### `src/commands/clear/index.ts`

**信息:**
- 行数: 19
- 大小: 603 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Clear command - minimal metadata only.
 * Implementation is lazy-loaded from clear.ts to reduce startup time.
 * Utility functions:
 * - clearSessionCaches: import from './clear/caches.js'
 * - clearConversation: import from './clear/conversation.js'
 */
import type { Command } from '../../commands.js'

const clear = {
  type: 'local',
  name: 'clear',
  description: 'Clear conversation history and free up context',
  aliases: ['reset', 'new'],
  supportsNonInteractive: false, // Should just create a new session
  load: () => import('./clear.js'),
} satisfies Command

export default clear

```

---


### `src/commands/color/color.ts`

**信息:**
- 行数: 93
- 大小: 2712 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { UUID } from 'crypto'
import { getSessionId } from '../../bootstrap/state.js'
import type { ToolUseContext } from '../../Tool.js'
import {
  AGENT_COLORS,
  type AgentColorName,
} from '../../tools/AgentTool/agentColorManager.js'
import type {
  LocalJSXCommandContext,
  LocalJSXCommandOnDone,
} from '../../types/command.js'
import {
  getTranscriptPath,
  saveAgentColor,
} from '../../utils/sessionStorage.js'
import { isTeammate } from '../../utils/teammate.js'

const RESET_ALIASES = ['default', 'reset', 'none', 'gray', 'grey'] as const

export async function call(
  onDone: LocalJSXCommandOnDone,
  context: ToolUseContext & LocalJSXCommandContext,
  args: string,
): Promise<null> {
  // Teammates cannot set their own color
  if (isTeammate()) {
    onDone(
      'Cannot set color: This session is a swarm teammate. Teammate colors are assigned by the team leader.',
      { display: 'system' },
    )
    return null
  }

  if (!args || args.trim() === '') {
    const colorList = AGENT_COLORS.join(', ')
    onDone(`Please provide a color. Available colors: ${colorList}, default`, {
      display: 'system',
    })
    return null
  }

  const colorArg = args.trim().toLowerCase()

  // Handle reset to default (gray)
  if (RESET_ALIASES.includes(colorArg as (typeof RESET_ALIASES)[number])) {
    const sessionId = getSessionId() as UUID
    const fullPath = getTranscriptPath()

    // Use "default" sentinel (not empty string) so truthiness guards
    // in sessionStorage.ts persist the reset across session restarts

```

---


### `src/commands/color/index.ts`

**信息:**
- 行数: 16
- 大小: 417 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Color command - minimal metadata only.
 * Implementation is lazy-loaded from color.ts to reduce startup time.
 */
import type { Command } from '../../commands.js'

const color = {
  type: 'local-jsx',
  name: 'color',
  description: 'Set the prompt bar color for this session',
  immediate: true,
  argumentHint: '<color|default>',
  load: () => import('./color.js'),
} satisfies Command

export default color

```

---


### `src/commands/commit-push-pr.ts`

**信息:**
- 行数: 158
- 大小: 6309 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../commands.js'
import {
  getAttributionTexts,
  getEnhancedPRAttribution,
} from '../utils/attribution.js'
import { getDefaultBranch } from '../utils/git.js'
import { executeShellCommandsInPrompt } from '../utils/promptShellExecution.js'
import { getUndercoverInstructions, isUndercover } from '../utils/undercover.js'

const ALLOWED_TOOLS = [
  'Bash(git checkout --branch:*)',
  'Bash(git checkout -b:*)',
  'Bash(git add:*)',
  'Bash(git status:*)',
  'Bash(git push:*)',
  'Bash(git commit:*)',
  'Bash(gh pr create:*)',
  'Bash(gh pr edit:*)',
  'Bash(gh pr view:*)',
  'Bash(gh pr merge:*)',
  'ToolSearch',
  'mcp__slack__send_message',
  'mcp__claude_ai_Slack__slack_send_message',
]

function getPromptContent(
  defaultBranch: string,
  prAttribution?: string,
): string {
  const { commit: commitAttribution, pr: defaultPrAttribution } =
    getAttributionTexts()
  // Use provided PR attribution or fall back to default
  const effectivePrAttribution = prAttribution ?? defaultPrAttribution
  const safeUser = process.env.SAFEUSER || ''
  const username = process.env.USER || ''

  let prefix = ''
  let reviewerArg = ' and `--reviewer anthropics/claude-code`'
  let addReviewerArg = ' (and add `--add-reviewer anthropics/claude-code`)'
  let changelogSection = `

## Changelog
<!-- CHANGELOG:START -->
[If this PR contains user-facing changes, add a changelog entry here. Otherwise, remove this section.]
<!-- CHANGELOG:END -->`
  let slackStep = `

5. After creating/updating the PR, check if the user's CLAUDE.md mentions posting to Slack channels. If it does, use ToolSearch to search for "slack send message" tools. If ToolSearch finds a Slack tool, ask the user if they'd like you to post the PR URL to the relevant Slack channel. Only post if the user confirms. If ToolSearch returns no results or errors, skip this step silently—do not mention the failure, do not attempt workarounds, and do not try alternative approaches.`
  if (process.env.USER_TYPE === 'ant' && isUndercover()) {
    prefix = getUndercoverInstructions() + '\n'

```

---


### `src/commands/commit.ts`

**信息:**
- 行数: 92
- 大小: 3492 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../commands.js'
import { getAttributionTexts } from '../utils/attribution.js'
import { executeShellCommandsInPrompt } from '../utils/promptShellExecution.js'
import { getUndercoverInstructions, isUndercover } from '../utils/undercover.js'

const ALLOWED_TOOLS = [
  'Bash(git add:*)',
  'Bash(git status:*)',
  'Bash(git commit:*)',
]

function getPromptContent(): string {
  const { commit: commitAttribution } = getAttributionTexts()

  let prefix = ''
  if (process.env.USER_TYPE === 'ant' && isUndercover()) {
    prefix = getUndercoverInstructions() + '\n'
  }

  return `${prefix}## Context

- Current git status: !\`git status\`
- Current git diff (staged and unstaged changes): !\`git diff HEAD\`
- Current branch: !\`git branch --show-current\`
- Recent commits: !\`git log --oneline -10\`

## Git Safety Protocol

- NEVER update the git config
- NEVER skip hooks (--no-verify, --no-gpg-sign, etc) unless the user explicitly requests it
- CRITICAL: ALWAYS create NEW commits. NEVER use git commit --amend, unless the user explicitly requests it
- Do not commit files that likely contain secrets (.env, credentials.json, etc). Warn the user if they specifically request to commit those files
- If there are no changes to commit (i.e., no untracked files and no modifications), do not create an empty commit
- Never use git commands with the -i flag (like git rebase -i or git add -i) since they require interactive input which is not supported

## Your task

Based on the above changes, create a single git commit:

1. Analyze all staged changes and draft a commit message:
   - Look at the recent commits above to follow this repository's commit message style
   - Summarize the nature of the changes (new feature, enhancement, bug fix, refactoring, test, docs, etc.)
   - Ensure the message accurately reflects the changes and their purpose (i.e. "add" means a wholly new feature, "update" means an enhancement to an existing feature, "fix" means a bug fix, etc.)
   - Draft a concise (1-2 sentences) commit message that focuses on the "why" rather than the "what"

2. Stage relevant files and create the commit using HEREDOC syntax:
\`\`\`
git commit -m "$(cat <<'EOF'
Commit message here.${commitAttribution ? `\n\n${commitAttribution}` : ''}
EOF

```

---


### `src/commands/compact/compact.ts`

**信息:**
- 行数: 287
- 大小: 10079 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import chalk from 'chalk'
import { markPostCompaction } from 'src/bootstrap/state.js'
import { getSystemPrompt } from '../../constants/prompts.js'
import { getSystemContext, getUserContext } from '../../context.js'
import { getShortcutDisplay } from '../../keybindings/shortcutFormat.js'
import { notifyCompaction } from '../../services/api/promptCacheBreakDetection.js'
import {
  type CompactionResult,
  compactConversation,
  ERROR_MESSAGE_INCOMPLETE_RESPONSE,
  ERROR_MESSAGE_NOT_ENOUGH_MESSAGES,
  ERROR_MESSAGE_USER_ABORT,
  mergeHookInstructions,
} from '../../services/compact/compact.js'
import { suppressCompactWarning } from '../../services/compact/compactWarningState.js'
import { microcompactMessages } from '../../services/compact/microCompact.js'
import { runPostCompactCleanup } from '../../services/compact/postCompactCleanup.js'
import { trySessionMemoryCompaction } from '../../services/compact/sessionMemoryCompact.js'
import { setLastSummarizedMessageId } from '../../services/SessionMemory/sessionMemoryUtils.js'
import type { ToolUseContext } from '../../Tool.js'
import type { LocalCommandCall } from '../../types/command.js'
import type { Message } from '../../types/message.js'
import { hasExactErrorMessage } from '../../utils/errors.js'
import { executePreCompactHooks } from '../../utils/hooks.js'
import { logError } from '../../utils/log.js'
import { getMessagesAfterCompactBoundary } from '../../utils/messages.js'
import { getUpgradeMessage } from '../../utils/model/contextWindowUpgradeCheck.js'
import {
  buildEffectiveSystemPrompt,
  type SystemPrompt,
} from '../../utils/systemPrompt.js'

/* eslint-disable @typescript-eslint/no-require-imports */
const reactiveCompact = feature('REACTIVE_COMPACT')
  ? (require('../../services/compact/reactiveCompact.js') as typeof import('../../services/compact/reactiveCompact.js'))
  : null
/* eslint-enable @typescript-eslint/no-require-imports */

export const call: LocalCommandCall = async (args, context) => {
  const { abortController } = context
  let { messages } = context

  // REPL keeps snipped messages for UI scrollback — project so the compact
  // model doesn't summarize content that was intentionally removed.
  messages = getMessagesAfterCompactBoundary(messages)

  if (messages.length === 0) {
    throw new Error('No messages to compact')
  }

```

---


### `src/commands/compact/index.ts`

**信息:**
- 行数: 15
- 大小: 530 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { isEnvTruthy } from '../../utils/envUtils.js'

const compact = {
  type: 'local',
  name: 'compact',
  description:
    'Clear conversation history but keep a summary in context. Optional: /compact [instructions for summarization]',
  isEnabled: () => !isEnvTruthy(process.env.DISABLE_COMPACT),
  supportsNonInteractive: true,
  argumentHint: '<optional custom summarization instructions>',
  load: () => import('./compact.js'),
} satisfies Command

export default compact

```

---


### `src/commands/config/config.tsx`

**信息:**
- 行数: 7
- 大小: 1408 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { Settings } from '../../components/Settings/Settings.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
export const call: LocalJSXCommandCall = async (onDone, context) => {
  return <Settings onClose={onDone} context={context} defaultTab="Config" />;
};
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlNldHRpbmdzIiwiTG9jYWxKU1hDb21tYW5kQ2FsbCIsImNhbGwiLCJvbkRvbmUiLCJjb250ZXh0Il0sInNvdXJjZXMiOlsiY29uZmlnLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IFNldHRpbmdzIH0gZnJvbSAnLi4vLi4vY29tcG9uZW50cy9TZXR0aW5ncy9TZXR0aW5ncy5qcydcbmltcG9ydCB0eXBlIHsgTG9jYWxKU1hDb21tYW5kQ2FsbCB9IGZyb20gJy4uLy4uL3R5cGVzL2NvbW1hbmQuanMnXG5cbmV4cG9ydCBjb25zdCBjYWxsOiBMb2NhbEpTWENvbW1hbmRDYWxsID0gYXN5bmMgKG9uRG9uZSwgY29udGV4dCkgPT4ge1xuICByZXR1cm4gPFNldHRpbmdzIG9uQ2xvc2U9e29uRG9uZX0gY29udGV4dD17Y29udGV4dH0gZGVmYXVsdFRhYj1cIkNvbmZpZ1wiIC8+XG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsUUFBUSxRQUFRLHVDQUF1QztBQUNoRSxjQUFjQyxtQkFBbUIsUUFBUSx3QkFBd0I7QUFFakUsT0FBTyxNQUFNQyxJQUFJLEVBQUVELG1CQUFtQixHQUFHLE1BQUFDLENBQU9DLE1BQU0sRUFBRUMsT0FBTyxLQUFLO0VBQ2xFLE9BQU8sQ0FBQyxRQUFRLENBQUMsT0FBTyxDQUFDLENBQUNELE1BQU0sQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDQyxPQUFPLENBQUMsQ0FBQyxVQUFVLENBQUMsUUFBUSxHQUFHO0FBQzVFLENBQUMiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/commands/config/index.ts`

**信息:**
- 行数: 11
- 大小: 247 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const config = {
  aliases: ['settings'],
  type: 'local-jsx',
  name: 'config',
  description: 'Open config panel',
  load: () => import('./config.js'),
} satisfies Command

export default config

```

---


### `src/commands/context/context-noninteractive.ts`

**信息:**
- 行数: 325
- 大小: 10781 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { microcompactMessages } from '../../services/compact/microCompact.js'
import type { AppState } from '../../state/AppStateStore.js'
import type { Tools, ToolUseContext } from '../../Tool.js'
import type { AgentDefinitionsResult } from '../../tools/AgentTool/loadAgentsDir.js'
import type { Message } from '../../types/message.js'
import {
  analyzeContextUsage,
  type ContextData,
} from '../../utils/analyzeContext.js'
import { formatTokens } from '../../utils/format.js'
import { getMessagesAfterCompactBoundary } from '../../utils/messages.js'
import { getSourceDisplayName } from '../../utils/settings/constants.js'
import { plural } from '../../utils/stringUtils.js'

/**
 * Shared data-collection path for `/context` (slash command) and the SDK
 * `get_context_usage` control request. Mirrors query.ts's pre-API transforms
 * (compact boundary, projectView, microcompact) so the token count reflects
 * what the model actually sees.
 */
type CollectContextDataInput = {
  messages: Message[]
  getAppState: () => AppState
  options: {
    mainLoopModel: string
    tools: Tools
    agentDefinitions: AgentDefinitionsResult
    customSystemPrompt?: string
    appendSystemPrompt?: string
  }
}

export async function collectContextData(
  context: CollectContextDataInput,
): Promise<ContextData> {
  const {
    messages,
    getAppState,
    options: {
      mainLoopModel,
      tools,
      agentDefinitions,
      customSystemPrompt,
      appendSystemPrompt,
    },
  } = context

  let apiView = getMessagesAfterCompactBoundary(messages)
  if (feature('CONTEXT_COLLAPSE')) {

```

---


### `src/commands/context/context.tsx`

**信息:**
- 行数: 64
- 大小: 9099 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import * as React from 'react';
import type { LocalJSXCommandContext } from '../../commands.js';
import { ContextVisualization } from '../../components/ContextVisualization.js';
import { microcompactMessages } from '../../services/compact/microCompact.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import type { Message } from '../../types/message.js';
import { analyzeContextUsage } from '../../utils/analyzeContext.js';
import { getMessagesAfterCompactBoundary } from '../../utils/messages.js';
import { renderToAnsiString } from '../../utils/staticRender.js';

/**
 * Apply the same context transforms query.ts does before the API call, so
 * /context shows what the model actually sees rather than the REPL's raw
 * history. Without projectView the token count overcounts by however much
 * was collapsed — user sees "180k, 3 spans collapsed" when the API sees 120k.
 */
function toApiView(messages: Message[]): Message[] {
  let view = getMessagesAfterCompactBoundary(messages);
  if (feature('CONTEXT_COLLAPSE')) {
    /* eslint-disable @typescript-eslint/no-require-imports */
    const {
      projectView
    } = require('../../services/contextCollapse/operations.js') as typeof import('../../services/contextCollapse/operations.js');
    /* eslint-enable @typescript-eslint/no-require-imports */
    view = projectView(view);
  }
  return view;
}
export async function call(onDone: LocalJSXCommandOnDone, context: LocalJSXCommandContext): Promise<React.ReactNode> {
  const {
    messages,
    getAppState,
    options: {
      mainLoopModel,
      tools
    }
  } = context;
  const apiView = toApiView(messages);

  // Apply microcompact to get accurate representation of messages sent to API
  const {
    messages: compactedMessages
  } = await microcompactMessages(apiView);

  // Get terminal width for responsive sizing
  const terminalWidth = process.stdout.columns || 80;
  const appState = getAppState();

  // Analyze context with compacted messages

```

---


### `src/commands/context/index.ts`

**信息:**
- 行数: 24
- 大小: 695 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getIsNonInteractiveSession } from '../../bootstrap/state.js'
import type { Command } from '../../commands.js'

export const context: Command = {
  name: 'context',
  description: 'Visualize current context usage as a colored grid',
  isEnabled: () => !getIsNonInteractiveSession(),
  type: 'local-jsx',
  load: () => import('./context.js'),
}

export const contextNonInteractive: Command = {
  type: 'local',
  name: 'context',
  supportsNonInteractive: true,
  description: 'Show current context usage',
  get isHidden() {
    return !getIsNonInteractiveSession()
  },
  isEnabled() {
    return getIsNonInteractiveSession()
  },
  load: () => import('./context-noninteractive.js'),
}

```

---


### `src/commands/copy/copy.tsx`

**信息:**
- 行数: 371
- 大小: 42252 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { mkdir, writeFile } from 'fs/promises';
import { marked, type Tokens } from 'marked';
import { tmpdir } from 'os';
import { join } from 'path';
import React, { useRef } from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import type { OptionWithDescription } from '../../components/CustomSelect/select.js';
import { Select } from '../../components/CustomSelect/select.js';
import { Byline } from '../../components/design-system/Byline.js';
import { KeyboardShortcutHint } from '../../components/design-system/KeyboardShortcutHint.js';
import { Pane } from '../../components/design-system/Pane.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { setClipboard } from '../../ink/termio/osc.js';
import { Box, Text } from '../../ink.js';
import { logEvent } from '../../services/analytics/index.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
import type { AssistantMessage, Message } from '../../types/message.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { extractTextContent, stripPromptXMLTags } from '../../utils/messages.js';
import { countCharInString } from '../../utils/stringUtils.js';
const COPY_DIR = join(tmpdir(), 'claude');
const RESPONSE_FILENAME = 'response.md';
const MAX_LOOKBACK = 20;
type CodeBlock = {
  code: string;
  lang: string | undefined;
};
function extractCodeBlocks(markdown: string): CodeBlock[] {
  const tokens = marked.lexer(stripPromptXMLTags(markdown));
  const blocks: CodeBlock[] = [];
  for (const token of tokens) {
    if (token.type === 'code') {
      const codeToken = token as Tokens.Code;
      blocks.push({
        code: codeToken.text,
        lang: codeToken.lang
      });
    }
  }
  return blocks;
}

/**
 * Walk messages newest-first, returning text from assistant messages that
 * actually said something (skips tool-use-only turns and API errors).
 * Index 0 = latest, 1 = second-to-latest, etc. Caps at MAX_LOOKBACK.
 */
export function collectRecentAssistantTexts(messages: Message[]): string[] {

```

---


### `src/commands/copy/index.ts`

**信息:**
- 行数: 15
- 大小: 393 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Copy command - minimal metadata only.
 * Implementation is lazy-loaded from copy.tsx to reduce startup time.
 */
import type { Command } from '../../commands.js'

const copy = {
  type: 'local-jsx',
  name: 'copy',
  description:
    "Copy Claude's last response to clipboard (or /copy N for the Nth-latest)",
  load: () => import('./copy.js'),
} satisfies Command

export default copy

```

---


### `src/commands/cost/cost.ts`

**信息:**
- 行数: 24
- 大小: 909 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { formatTotalCost } from '../../cost-tracker.js'
import { currentLimits } from '../../services/claudeAiLimits.js'
import type { LocalCommandCall } from '../../types/command.js'
import { isClaudeAISubscriber } from '../../utils/auth.js'

export const call: LocalCommandCall = async () => {
  if (isClaudeAISubscriber()) {
    let value: string

    if (currentLimits.isUsingOverage) {
      value =
        'You are currently using your overages to power your Claude Code usage. We will automatically switch you back to your subscription rate limits when they reset'
    } else {
      value =
        'You are currently using your subscription to power your Claude Code usage'
    }

    if (process.env.USER_TYPE === 'ant') {
      value += `\n\n[ANT-ONLY] Showing cost anyway:\n ${formatTotalCost()}`
    }
    return { type: 'text', value }
  }
  return { type: 'text', value: formatTotalCost() }
}

```

---


### `src/commands/cost/index.ts`

**信息:**
- 行数: 23
- 大小: 668 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Cost command - minimal metadata only.
 * Implementation is lazy-loaded from cost.ts to reduce startup time.
 */
import type { Command } from '../../commands.js'
import { isClaudeAISubscriber } from '../../utils/auth.js'

const cost = {
  type: 'local',
  name: 'cost',
  description: 'Show the total cost and duration of the current session',
  get isHidden() {
    // Keep visible for Ants even if they're subscribers (they see cost breakdowns)
    if (process.env.USER_TYPE === 'ant') {
      return false
    }
    return isClaudeAISubscriber()
  },
  supportsNonInteractive: true,
  load: () => import('./cost.js'),
} satisfies Command

export default cost

```

---


### `src/commands/createMovedToPluginCommand.ts`

**信息:**
- 行数: 65
- 大小: 1789 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/messages.js'
import type { Command } from '../commands.js'
import type { ToolUseContext } from '../Tool.js'

type Options = {
  name: string
  description: string
  progressMessage: string
  pluginName: string
  pluginCommand: string
  /**
   * The prompt to use while the marketplace is private.
   * External users will get this prompt. Once the marketplace is public,
   * this parameter and the fallback logic can be removed.
   */
  getPromptWhileMarketplaceIsPrivate: (
    args: string,
    context: ToolUseContext,
  ) => Promise<ContentBlockParam[]>
}

export function createMovedToPluginCommand({
  name,
  description,
  progressMessage,
  pluginName,
  pluginCommand,
  getPromptWhileMarketplaceIsPrivate,
}: Options): Command {
  return {
    type: 'prompt',
    name,
    description,
    progressMessage,
    contentLength: 0, // Dynamic content
    userFacingName() {
      return name
    },
    source: 'builtin',
    async getPromptForCommand(
      args: string,
      context: ToolUseContext,
    ): Promise<ContentBlockParam[]> {
      if (process.env.USER_TYPE === 'ant') {
        return [
          {
            type: 'text',
            text: `This command has been moved to a plugin. Tell the user:

1. To install the plugin, run:

```

---


### `src/commands/desktop/desktop.tsx`

**信息:**
- 行数: 9
- 大小: 1645 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { DesktopHandoff } from '../../components/DesktopHandoff.js';
export async function call(onDone: (result?: string, options?: {
  display?: CommandResultDisplay;
}) => void): Promise<React.ReactNode> {
  return <DesktopHandoff onDone={onDone} />;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkNvbW1hbmRSZXN1bHREaXNwbGF5IiwiRGVza3RvcEhhbmRvZmYiLCJjYWxsIiwib25Eb25lIiwicmVzdWx0Iiwib3B0aW9ucyIsImRpc3BsYXkiLCJQcm9taXNlIiwiUmVhY3ROb2RlIl0sInNvdXJjZXMiOlsiZGVza3RvcC50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHR5cGUgeyBDb21tYW5kUmVzdWx0RGlzcGxheSB9IGZyb20gJy4uLy4uL2NvbW1hbmRzLmpzJ1xuaW1wb3J0IHsgRGVza3RvcEhhbmRvZmYgfSBmcm9tICcuLi8uLi9jb21wb25lbnRzL0Rlc2t0b3BIYW5kb2ZmLmpzJ1xuXG5leHBvcnQgYXN5bmMgZnVuY3Rpb24gY2FsbChcbiAgb25Eb25lOiAoXG4gICAgcmVzdWx0Pzogc3RyaW5nLFxuICAgIG9wdGlvbnM/OiB7IGRpc3BsYXk/OiBDb21tYW5kUmVzdWx0RGlzcGxheSB9LFxuICApID0+IHZvaWQsXG4pOiBQcm9taXNlPFJlYWN0LlJlYWN0Tm9kZT4ge1xuICByZXR1cm4gPERlc2t0b3BIYW5kb2ZmIG9uRG9uZT17b25Eb25lfSAvPlxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPQSxLQUFLLE1BQU0sT0FBTztBQUN6QixjQUFjQyxvQkFBb0IsUUFBUSxtQkFBbUI7QUFDN0QsU0FBU0MsY0FBYyxRQUFRLG9DQUFvQztBQUVuRSxPQUFPLGVBQWVDLElBQUlBLENBQ3hCQyxNQUFNLEVBQUUsQ0FDTkMsTUFBZSxDQUFSLEVBQUUsTUFBTSxFQUNmQyxPQUE0QyxDQUFwQyxFQUFFO0VBQUVDLE9BQU8sQ0FBQyxFQUFFTixvQkFBb0I7QUFBQyxDQUFDLEVBQzVDLEdBQUcsSUFBSSxDQUNWLEVBQUVPLE9BQU8sQ0FBQ1IsS0FBSyxDQUFDUyxTQUFTLENBQUMsQ0FBQztFQUMxQixPQUFPLENBQUMsY0FBYyxDQUFDLE1BQU0sQ0FBQyxDQUFDTCxNQUFNLENBQUMsR0FBRztBQUMzQyIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/commands/desktop/index.ts`

**信息:**
- 行数: 26
- 大小: 601 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

function isSupportedPlatform(): boolean {
  if (process.platform === 'darwin') {
    return true
  }
  if (process.platform === 'win32' && process.arch === 'x64') {
    return true
  }
  return false
}

const desktop = {
  type: 'local-jsx',
  name: 'desktop',
  aliases: ['app'],
  description: 'Continue the current session in Claude Desktop',
  availability: ['claude-ai'],
  isEnabled: isSupportedPlatform,
  get isHidden() {
    return !isSupportedPlatform()
  },
  load: () => import('./desktop.js'),
} satisfies Command

export default desktop

```

---


### `src/commands/diff/diff.tsx`

**信息:**
- 行数: 9
- 大小: 1461 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import type { LocalJSXCommandCall } from '../../types/command.js';
export const call: LocalJSXCommandCall = async (onDone, context) => {
  const {
    DiffDialog
  } = await import('../../components/diff/DiffDialog.js');
  return <DiffDialog messages={context.messages} onDone={onDone} />;
};
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkxvY2FsSlNYQ29tbWFuZENhbGwiLCJjYWxsIiwib25Eb25lIiwiY29udGV4dCIsIkRpZmZEaWFsb2ciLCJtZXNzYWdlcyJdLCJzb3VyY2VzIjpbImRpZmYudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHR5cGUgeyBMb2NhbEpTWENvbW1hbmRDYWxsIH0gZnJvbSAnLi4vLi4vdHlwZXMvY29tbWFuZC5qcydcblxuZXhwb3J0IGNvbnN0IGNhbGw6IExvY2FsSlNYQ29tbWFuZENhbGwgPSBhc3luYyAob25Eb25lLCBjb250ZXh0KSA9PiB7XG4gIGNvbnN0IHsgRGlmZkRpYWxvZyB9ID0gYXdhaXQgaW1wb3J0KCcuLi8uLi9jb21wb25lbnRzL2RpZmYvRGlmZkRpYWxvZy5qcycpXG4gIHJldHVybiA8RGlmZkRpYWxvZyBtZXNzYWdlcz17Y29udGV4dC5tZXNzYWdlc30gb25Eb25lPXtvbkRvbmV9IC8+XG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsY0FBY0MsbUJBQW1CLFFBQVEsd0JBQXdCO0FBRWpFLE9BQU8sTUFBTUMsSUFBSSxFQUFFRCxtQkFBbUIsR0FBRyxNQUFBQyxDQUFPQyxNQUFNLEVBQUVDLE9BQU8sS0FBSztFQUNsRSxNQUFNO0lBQUVDO0VBQVcsQ0FBQyxHQUFHLE1BQU0sTUFBTSxDQUFDLHFDQUFxQyxDQUFDO0VBQzFFLE9BQU8sQ0FBQyxVQUFVLENBQUMsUUFBUSxDQUFDLENBQUNELE9BQU8sQ0FBQ0UsUUFBUSxDQUFDLENBQUMsTUFBTSxDQUFDLENBQUNILE1BQU0sQ0FBQyxHQUFHO0FBQ25FLENBQUMiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/commands/diff/index.ts`

**信息:**
- 行数: 8
- 大小: 221 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

export default {
  type: 'local-jsx',
  name: 'diff',
  description: 'View uncommitted changes and per-turn diffs',
  load: () => import('./diff.js'),
} satisfies Command

```

---


### `src/commands/doctor/doctor.tsx`

**信息:**
- 行数: 7
- 大小: 1309 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { Doctor } from '../../screens/Doctor.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
export const call: LocalJSXCommandCall = (onDone, _context, _args) => {
  return Promise.resolve(<Doctor onDone={onDone} />);
};
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkRvY3RvciIsIkxvY2FsSlNYQ29tbWFuZENhbGwiLCJjYWxsIiwib25Eb25lIiwiX2NvbnRleHQiLCJfYXJncyIsIlByb21pc2UiLCJyZXNvbHZlIl0sInNvdXJjZXMiOlsiZG9jdG9yLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBEb2N0b3IgfSBmcm9tICcuLi8uLi9zY3JlZW5zL0RvY3Rvci5qcydcbmltcG9ydCB0eXBlIHsgTG9jYWxKU1hDb21tYW5kQ2FsbCB9IGZyb20gJy4uLy4uL3R5cGVzL2NvbW1hbmQuanMnXG5cbmV4cG9ydCBjb25zdCBjYWxsOiBMb2NhbEpTWENvbW1hbmRDYWxsID0gKG9uRG9uZSwgX2NvbnRleHQsIF9hcmdzKSA9PiB7XG4gIHJldHVybiBQcm9taXNlLnJlc29sdmUoPERvY3RvciBvbkRvbmU9e29uRG9uZX0gLz4pXG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU9BLEtBQUssTUFBTSxPQUFPO0FBQ3pCLFNBQVNDLE1BQU0sUUFBUSx5QkFBeUI7QUFDaEQsY0FBY0MsbUJBQW1CLFFBQVEsd0JBQXdCO0FBRWpFLE9BQU8sTUFBTUMsSUFBSSxFQUFFRCxtQkFBbUIsR0FBR0MsQ0FBQ0MsTUFBTSxFQUFFQyxRQUFRLEVBQUVDLEtBQUssS0FBSztFQUNwRSxPQUFPQyxPQUFPLENBQUNDLE9BQU8sQ0FBQyxDQUFDLE1BQU0sQ0FBQyxNQUFNLENBQUMsQ0FBQ0osTUFBTSxDQUFDLEdBQUcsQ0FBQztBQUNwRCxDQUFDIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/doctor/index.ts`

**信息:**
- 行数: 12
- 大小: 381 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { isEnvTruthy } from '../../utils/envUtils.js'

const doctor: Command = {
  name: 'doctor',
  description: 'Diagnose and verify your Claude Code installation and settings',
  isEnabled: () => !isEnvTruthy(process.env.DISABLE_DOCTOR_COMMAND),
  type: 'local-jsx',
  load: () => import('./doctor.js'),
}

export default doctor

```

---


### `src/commands/effort/effort.tsx`

**信息:**
- 行数: 183
- 大小: 22128 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useMainLoopModel } from '../../hooks/useMainLoopModel.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../services/analytics/index.js';
import { useAppState, useSetAppState } from '../../state/AppState.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { type EffortValue, getDisplayedEffortLevel, getEffortEnvOverride, getEffortValueDescription, isEffortLevel, toPersistableEffort } from '../../utils/effort.js';
import { updateSettingsForSource } from '../../utils/settings/settings.js';
const COMMON_HELP_ARGS = ['help', '-h', '--help'];
type EffortCommandResult = {
  message: string;
  effortUpdate?: {
    value: EffortValue | undefined;
  };
};
function setEffortValue(effortValue: EffortValue): EffortCommandResult {
  const persistable = toPersistableEffort(effortValue);
  if (persistable !== undefined) {
    const result = updateSettingsForSource('userSettings', {
      effortLevel: persistable
    });
    if (result.error) {
      return {
        message: `Failed to set effort level: ${result.error.message}`
      };
    }
  }
  logEvent('tengu_effort_command', {
    effort: effortValue as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS
  });

  // Env var wins at resolveAppliedEffort time. Only flag it when it actually
  // conflicts — if env matches what the user just asked for, the outcome is
  // the same, so "Set effort to X" is true and the note is noise.
  const envOverride = getEffortEnvOverride();
  if (envOverride !== undefined && envOverride !== effortValue) {
    const envRaw = process.env.CLAUDE_CODE_EFFORT_LEVEL;
    if (persistable === undefined) {
      return {
        message: `Not applied: CLAUDE_CODE_EFFORT_LEVEL=${envRaw} overrides effort this session, and ${effortValue} is session-only (nothing saved)`,
        effortUpdate: {
          value: effortValue
        }
      };
    }
    return {
      message: `CLAUDE_CODE_EFFORT_LEVEL=${envRaw} overrides this session — clear it and ${effortValue} takes over`,
      effortUpdate: {
        value: effortValue
      }

```

---


### `src/commands/effort/index.ts`

**信息:**
- 行数: 13
- 大小: 428 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { shouldInferenceConfigCommandBeImmediate } from '../../utils/immediateCommand.js'

export default {
  type: 'local-jsx',
  name: 'effort',
  description: 'Set effort level for model usage',
  argumentHint: '[low|medium|high|max|auto]',
  get immediate() {
    return shouldInferenceConfigCommandBeImmediate()
  },
  load: () => import('./effort.js'),
} satisfies Command

```

---


### `src/commands/exit/exit.tsx`

**信息:**
- 行数: 33
- 大小: 5272 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import { spawnSync } from 'child_process';
import sample from 'lodash-es/sample.js';
import * as React from 'react';
import { ExitFlow } from '../../components/ExitFlow.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { isBgSession } from '../../utils/concurrentSessions.js';
import { gracefulShutdown } from '../../utils/gracefulShutdown.js';
import { getCurrentWorktreeSession } from '../../utils/worktree.js';
const GOODBYE_MESSAGES = ['Goodbye!', 'See ya!', 'Bye!', 'Catch you later!'];
function getRandomGoodbyeMessage(): string {
  return sample(GOODBYE_MESSAGES) ?? 'Goodbye!';
}
export async function call(onDone: LocalJSXCommandOnDone): Promise<React.ReactNode> {
  // Inside a `claude --bg` tmux session: detach instead of kill. The REPL
  // keeps running; `claude attach` can reconnect. Covers /exit, /quit,
  // ctrl+c, ctrl+d — all funnel through here via REPL's handleExit.
  if (feature('BG_SESSIONS') && isBgSession()) {
    onDone();
    spawnSync('tmux', ['detach-client'], {
      stdio: 'ignore'
    });
    return null;
  }
  const showWorktree = getCurrentWorktreeSession() !== null;
  if (showWorktree) {
    return <ExitFlow showWorktree={showWorktree} onDone={onDone} onCancel={() => onDone()} />;
  }
  onDone(getRandomGoodbyeMessage());
  await gracefulShutdown(0, 'prompt_input_exit');
  return null;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJmZWF0dXJlIiwic3Bhd25TeW5jIiwic2FtcGxlIiwiUmVhY3QiLCJFeGl0RmxvdyIsIkxvY2FsSlNYQ29tbWFuZE9uRG9uZSIsImlzQmdTZXNzaW9uIiwiZ3JhY2VmdWxTaHV0ZG93biIsImdldEN1cnJlbnRXb3JrdHJlZVNlc3Npb24iLCJHT09EQllFX01FU1NBR0VTIiwiZ2V0UmFuZG9tR29vZGJ5ZU1lc3NhZ2UiLCJjYWxsIiwib25Eb25lIiwiUHJvbWlzZSIsIlJlYWN0Tm9kZSIsInN0ZGlvIiwic2hvd1dvcmt0cmVlIl0sInNvdXJjZXMiOlsiZXhpdC50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgZmVhdHVyZSB9IGZyb20gJ2J1bjpidW5kbGUnXG5pbXBvcnQgeyBzcGF3blN5bmMgfSBmcm9tICdjaGlsZF9wcm9jZXNzJ1xuaW1wb3J0IHNhbXBsZSBmcm9tICdsb2Rhc2gtZXMvc2FtcGxlLmpzJ1xuaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBFeGl0RmxvdyB9IGZyb20gJy4uLy4uL2NvbXBvbmVudHMvRXhpdEZsb3cuanMnXG5pbXBvcnQgdHlwZSB7IExvY2FsSlNYQ29tbWFuZE9uRG9uZSB9IGZyb20gJy4uLy4uL3R5cGVzL2NvbW1hbmQuanMnXG5pbXBvcnQgeyBpc0JnU2Vzc2lvbiB9IGZyb20gJy4uLy4uL3V0aWxzL2NvbmN1cnJlbnRTZXNzaW9ucy5qcydcbmltcG9ydCB7IGdyYWNlZnVsU2h1dGRvd24gfSBmcm9tICcuLi8uLi91dGlscy9ncmFjZWZ1bFNodXRkb3duLmpzJ1xuaW1wb3J0IHsgZ2V0Q3VycmVudFdvcmt0cmVlU2Vzc2lvbiB9IGZyb20gJy4uLy4uL3V0aWxzL3dvcmt0cmVlLmpzJ1xuXG5jb25zdCBHT09EQllFX01FU1NBR0VTID0gWydHb29kYnllIScsICdTZWUgeWEhJywgJ0J5ZSEnLCAnQ2F0Y2ggeW91IGxhdGVyISddXG5cbmZ1bmN0aW9uIGdldFJhbmRvbUdvb2RieWVNZXNzYWdlKCk6IHN0cmluZyB7XG4gIHJldHVybiBzYW1wbGUoR09PREJZRV9NRVNTQUdFUykgPz8gJ0dvb2RieWUhJ1xufVxuXG5leHBvcnQgYXN5bmMgZnVuY3Rpb24gY2FsbChcbiAgb25Eb25lOiBMb2NhbEpTWENvbW1hbmRPbkRvbmUsXG4pOiBQcm9taXNlPFJlYWN0LlJlYWN0Tm9kZT4ge1xuICAvLyBJbnNpZGUgYSBgY2xhdWRlIC0tYmdgIHRtdXggc2Vzc2lvbjogZGV0YWNoIGluc3RlYWQgb2Yga2lsbC4gVGhlIFJFUExcbiAgLy8ga2VlcHMgcnVubmluZzsgYGNsYXVkZSBhdHRhY2hgIGNhbiByZWNvbm5lY3QuIENvdmVycyAvZXhpdCwgL3F1aXQsXG4gIC8vIGN0cmwrYywgY3RybCtkIOKAlCBhbGwgZnVubmVsIHRocm91Z2ggaGVyZSB2aWEgUkVQTCdzIGhhbmRsZUV4aXQuXG4gIGlmIChmZWF0dXJlKCdCR19TRVNTSU9OUycpICYmIGlzQmdTZXNzaW9uKCkpIHtcbiAgICBvbkRvbmUoKVxuICAgIHNwYXduU3luYygndG11eCcsIFsnZGV0YWNoLWNsaWVudCddLCB7IHN0ZGlvOiAnaWdub3JlJyB9KVxuICAgIHJldHVybiBudWxsXG4gIH1cblxuICBjb25zdCBzaG93V29ya3RyZWUgPSBnZXRDdXJyZW50V29ya3RyZWVTZXNzaW9uKCkgIT09IG51bGxcblxuICBpZiAoc2hvd1dvcmt0cmVlKSB7XG4gICAgcmV0dXJuIChcbiAgICAgIDxFeGl0Rmxvd1xuICAgICAgICBzaG93V29ya3RyZWU9e3Nob3dXb3JrdHJlZX1cbiAgICAgICAgb25Eb25lPXtvbkRvbmV9XG4gICAgICAgIG9uQ2FuY2VsPXsoKSA9PiBvbkRvbmUoKX1cbiAgICAgIC8+XG4gICAgKVxuICB9XG5cbiAgb25Eb25lKGdldFJhbmRvbUdvb2RieWVNZXNzYWdlKCkpXG4gIGF3YWl0IGdyYWNlZnVsU2h1dGRvd24oMCwgJ3Byb21wdF9pbnB1dF9leGl0JylcbiAgcmV0dXJuIG51bGxcbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsU0FBU0EsT0FBTyxRQUFRLFlBQVk7QUFDcEMsU0FBU0MsU0FBUyxRQUFRLGVBQWU7QUFDekMsT0FBT0MsTUFBTSxNQUFNLHFCQUFxQjtBQUN4QyxPQUFPLEtBQUtDLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLFFBQVEsUUFBUSw4QkFBOEI7QUFDdkQsY0FBY0MscUJBQXFCLFFBQVEsd0JBQXdCO0FBQ25FLFNBQVNDLFdBQVcsUUFBUSxtQ0FBbUM7QUFDL0QsU0FBU0MsZ0JBQWdCLFFBQVEsaUNBQWlDO0FBQ2xFLFNBQVNDLHlCQUF5QixRQUFRLHlCQUF5QjtBQUVuRSxNQUFNQyxnQkFBZ0IsR0FBRyxDQUFDLFVBQVUsRUFBRSxTQUFTLEVBQUUsTUFBTSxFQUFFLGtCQUFrQixDQUFDO0FBRTVFLFNBQVNDLHVCQUF1QkEsQ0FBQSxDQUFFLEVBQUUsTUFBTSxDQUFDO0VBQ3pDLE9BQU9SLE1BQU0sQ0FBQ08sZ0JBQWdCLENBQUMsSUFBSSxVQUFVO0FBQy9DO0FBRUEsT0FBTyxlQUFlRSxJQUFJQSxDQUN4QkMsTUFBTSxFQUFFUCxxQkFBcUIsQ0FDOUIsRUFBRVEsT0FBTyxDQUFDVixLQUFLLENBQUNXLFNBQVMsQ0FBQyxDQUFDO0VBQzFCO0VBQ0E7RUFDQTtFQUNBLElBQUlkLE9BQU8sQ0FBQyxhQUFhLENBQUMsSUFBSU0sV0FBVyxDQUFDLENBQUMsRUFBRTtJQUMzQ00sTUFBTSxDQUFDLENBQUM7SUFDUlgsU0FBUyxDQUFDLE1BQU0sRUFBRSxDQUFDLGVBQWUsQ0FBQyxFQUFFO01BQUVjLEtBQUssRUFBRTtJQUFTLENBQUMsQ0FBQztJQUN6RCxPQUFPLElBQUk7RUFDYjtFQUVBLE1BQU1DLFlBQVksR0FBR1IseUJBQXlCLENBQUMsQ0FBQyxLQUFLLElBQUk7RUFFekQsSUFBSVEsWUFBWSxFQUFFO0lBQ2hCLE9BQ0UsQ0FBQyxRQUFRLENBQ1AsWUFBWSxDQUFDLENBQUNBLFlBQVksQ0FBQyxDQUMzQixNQUFNLENBQUMsQ0FBQ0osTUFBTSxDQUFDLENBQ2YsUUFBUSxDQUFDLENBQUMsTUFBTUEsTUFBTSxDQUFDLENBQUMsQ0FBQyxHQUN6QjtFQUVOO0VBRUFBLE1BQU0sQ0FBQ0YsdUJBQXVCLENBQUMsQ0FBQyxDQUFDO0VBQ2pDLE1BQU1ILGdCQUFnQixDQUFDLENBQUMsRUFBRSxtQkFBbUIsQ0FBQztFQUM5QyxPQUFPLElBQUk7QUFDYiIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/commands/exit/index.ts`

**信息:**
- 行数: 12
- 大小: 250 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const exit = {
  type: 'local-jsx',
  name: 'exit',
  aliases: ['quit'],
  description: 'Exit the REPL',
  immediate: true,
  load: () => import('./exit.js'),
} satisfies Command

export default exit

```

---


### `src/commands/export/export.tsx`

**信息:**
- 行数: 91
- 大小: 15104 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { join } from 'path';
import React from 'react';
import { ExportDialog } from '../../components/ExportDialog.js';
import type { ToolUseContext } from '../../Tool.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import type { Message } from '../../types/message.js';
import { getCwd } from '../../utils/cwd.js';
import { renderMessagesToPlainText } from '../../utils/exportRenderer.js';
import { writeFileSync_DEPRECATED } from '../../utils/slowOperations.js';
function formatTimestamp(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day}-${hours}${minutes}${seconds}`;
}
export function extractFirstPrompt(messages: Message[]): string {
  const firstUserMessage = messages.find(msg => msg.type === 'user');
  if (!firstUserMessage || firstUserMessage.type !== 'user') {
    return '';
  }
  const content = firstUserMessage.message?.content;
  let result = '';
  if (typeof content === 'string') {
    result = content.trim();
  } else if (Array.isArray(content)) {
    const textContent = content.find(item => item.type === 'text');
    if (textContent && 'text' in textContent) {
      result = textContent.text.trim();
    }
  }

  // Take first line only and limit length
  result = result.split('\n')[0] || '';
  if (result.length > 50) {
    result = result.substring(0, 49) + '…';
  }
  return result;
}
export function sanitizeFilename(text: string): string {
  // Replace special characters with hyphens
  return text.toLowerCase().replace(/[^a-z0-9\s-]/g, '') // Remove special chars
  .replace(/\s+/g, '-') // Replace spaces with hyphens
  .replace(/-+/g, '-') // Replace multiple hyphens with single
  .replace(/^-|-$/g, ''); // Remove leading/trailing hyphens
}
async function exportWithReactRenderer(context: ToolUseContext): Promise<string> {
  const tools = context.options.tools || [];

```

---


### `src/commands/export/index.ts`

**信息:**
- 行数: 11
- 大小: 303 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const exportCommand = {
  type: 'local-jsx',
  name: 'export',
  description: 'Export the current conversation to a file or clipboard',
  argumentHint: '[filename]',
  load: () => import('./export.js'),
} satisfies Command

export default exportCommand

```

---


### `src/commands/extra-usage/extra-usage-core.ts`

**信息:**
- 行数: 118
- 大小: 4000 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  checkAdminRequestEligibility,
  createAdminRequest,
  getMyAdminRequests,
} from '../../services/api/adminRequests.js'
import { invalidateOverageCreditGrantCache } from '../../services/api/overageCreditGrant.js'
import { type ExtraUsage, fetchUtilization } from '../../services/api/usage.js'
import { getSubscriptionType } from '../../utils/auth.js'
import { hasClaudeAiBillingAccess } from '../../utils/billing.js'
import { openBrowser } from '../../utils/browser.js'
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js'
import { logError } from '../../utils/log.js'

type ExtraUsageResult =
  | { type: 'message'; value: string }
  | { type: 'browser-opened'; url: string; opened: boolean }

export async function runExtraUsage(): Promise<ExtraUsageResult> {
  if (!getGlobalConfig().hasVisitedExtraUsage) {
    saveGlobalConfig(prev => ({ ...prev, hasVisitedExtraUsage: true }))
  }
  // Invalidate only the current org's entry so a follow-up read refetches
  // the granted state. Separate from the visited flag since users may run
  // /extra-usage more than once while iterating on the claim flow.
  invalidateOverageCreditGrantCache()

  const subscriptionType = getSubscriptionType()
  const isTeamOrEnterprise =
    subscriptionType === 'team' || subscriptionType === 'enterprise'
  const hasBillingAccess = hasClaudeAiBillingAccess()

  if (!hasBillingAccess && isTeamOrEnterprise) {
    // Mirror apps/claude-ai useHasUnlimitedOverage(): if overage is enabled
    // with no monthly cap, there is nothing to request. On fetch error, fall
    // through and let the user ask (matching web's "err toward show" behavior).
    let extraUsage: ExtraUsage | null | undefined
    try {
      const utilization = await fetchUtilization()
      extraUsage = utilization?.extra_usage
    } catch (error) {
      logError(error as Error)
    }

    if (extraUsage?.is_enabled && extraUsage.monthly_limit === null) {
      return {
        type: 'message',
        value:
          'Your organization already has unlimited extra usage. No request needed.',
      }
    }

```

---


### `src/commands/extra-usage/extra-usage-noninteractive.ts`

**信息:**
- 行数: 16
- 大小: 466 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { runExtraUsage } from './extra-usage-core.js'

export async function call(): Promise<{ type: 'text'; value: string }> {
  const result = await runExtraUsage()

  if (result.type === 'message') {
    return { type: 'text', value: result.value }
  }

  return {
    type: 'text',
    value: result.opened
      ? `Browser opened to manage extra usage. If it didn't open, visit: ${result.url}`
      : `Please visit ${result.url} to manage extra usage.`,
  }
}

```

---


### `src/commands/extra-usage/extra-usage.tsx`

**信息:**
- 行数: 17
- 大小: 3134 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import type { LocalJSXCommandContext } from '../../commands.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { Login } from '../login/login.js';
import { runExtraUsage } from './extra-usage-core.js';
export async function call(onDone: LocalJSXCommandOnDone, context: LocalJSXCommandContext): Promise<React.ReactNode | null> {
  const result = await runExtraUsage();
  if (result.type === 'message') {
    onDone(result.value);
    return null;
  }
  return <Login startingMessage={'Starting new login following /extra-usage. Exit with Ctrl-C to use existing account.'} onDone={success => {
    context.onChangeAPIKey();
    onDone(success ? 'Login successful' : 'Login interrupted');
  }} />;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkxvY2FsSlNYQ29tbWFuZENvbnRleHQiLCJMb2NhbEpTWENvbW1hbmRPbkRvbmUiLCJMb2dpbiIsInJ1bkV4dHJhVXNhZ2UiLCJjYWxsIiwib25Eb25lIiwiY29udGV4dCIsIlByb21pc2UiLCJSZWFjdE5vZGUiLCJyZXN1bHQiLCJ0eXBlIiwidmFsdWUiLCJzdWNjZXNzIiwib25DaGFuZ2VBUElLZXkiXSwic291cmNlcyI6WyJleHRyYS11c2FnZS50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHR5cGUgeyBMb2NhbEpTWENvbW1hbmRDb250ZXh0IH0gZnJvbSAnLi4vLi4vY29tbWFuZHMuanMnXG5pbXBvcnQgdHlwZSB7IExvY2FsSlNYQ29tbWFuZE9uRG9uZSB9IGZyb20gJy4uLy4uL3R5cGVzL2NvbW1hbmQuanMnXG5pbXBvcnQgeyBMb2dpbiB9IGZyb20gJy4uL2xvZ2luL2xvZ2luLmpzJ1xuaW1wb3J0IHsgcnVuRXh0cmFVc2FnZSB9IGZyb20gJy4vZXh0cmEtdXNhZ2UtY29yZS5qcydcblxuZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGNhbGwoXG4gIG9uRG9uZTogTG9jYWxKU1hDb21tYW5kT25Eb25lLFxuICBjb250ZXh0OiBMb2NhbEpTWENvbW1hbmRDb250ZXh0LFxuKTogUHJvbWlzZTxSZWFjdC5SZWFjdE5vZGUgfCBudWxsPiB7XG4gIGNvbnN0IHJlc3VsdCA9IGF3YWl0IHJ1bkV4dHJhVXNhZ2UoKVxuXG4gIGlmIChyZXN1bHQudHlwZSA9PT0gJ21lc3NhZ2UnKSB7XG4gICAgb25Eb25lKHJlc3VsdC52YWx1ZSlcbiAgICByZXR1cm4gbnVsbFxuICB9XG5cbiAgcmV0dXJuIChcbiAgICA8TG9naW5cbiAgICAgIHN0YXJ0aW5nTWVzc2FnZT17XG4gICAgICAgICdTdGFydGluZyBuZXcgbG9naW4gZm9sbG93aW5nIC9leHRyYS11c2FnZS4gRXhpdCB3aXRoIEN0cmwtQyB0byB1c2UgZXhpc3RpbmcgYWNjb3VudC4nXG4gICAgICB9XG4gICAgICBvbkRvbmU9e3N1Y2Nlc3MgPT4ge1xuICAgICAgICBjb250ZXh0Lm9uQ2hhbmdlQVBJS2V5KClcbiAgICAgICAgb25Eb25lKHN1Y2Nlc3MgPyAnTG9naW4gc3VjY2Vzc2Z1bCcgOiAnTG9naW4gaW50ZXJydXB0ZWQnKVxuICAgICAgfX1cbiAgICAvPlxuICApXG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU9BLEtBQUssTUFBTSxPQUFPO0FBQ3pCLGNBQWNDLHNCQUFzQixRQUFRLG1CQUFtQjtBQUMvRCxjQUFjQyxxQkFBcUIsUUFBUSx3QkFBd0I7QUFDbkUsU0FBU0MsS0FBSyxRQUFRLG1CQUFtQjtBQUN6QyxTQUFTQyxhQUFhLFFBQVEsdUJBQXVCO0FBRXJELE9BQU8sZUFBZUMsSUFBSUEsQ0FDeEJDLE1BQU0sRUFBRUoscUJBQXFCLEVBQzdCSyxPQUFPLEVBQUVOLHNCQUFzQixDQUNoQyxFQUFFTyxPQUFPLENBQUNSLEtBQUssQ0FBQ1MsU0FBUyxHQUFHLElBQUksQ0FBQyxDQUFDO0VBQ2pDLE1BQU1DLE1BQU0sR0FBRyxNQUFNTixhQUFhLENBQUMsQ0FBQztFQUVwQyxJQUFJTSxNQUFNLENBQUNDLElBQUksS0FBSyxTQUFTLEVBQUU7SUFDN0JMLE1BQU0sQ0FBQ0ksTUFBTSxDQUFDRSxLQUFLLENBQUM7SUFDcEIsT0FBTyxJQUFJO0VBQ2I7RUFFQSxPQUNFLENBQUMsS0FBSyxDQUNKLGVBQWUsQ0FBQyxDQUNkLHNGQUNGLENBQUMsQ0FDRCxNQUFNLENBQUMsQ0FBQ0MsT0FBTyxJQUFJO0lBQ2pCTixPQUFPLENBQUNPLGNBQWMsQ0FBQyxDQUFDO0lBQ3hCUixNQUFNLENBQUNPLE9BQU8sR0FBRyxrQkFBa0IsR0FBRyxtQkFBbUIsQ0FBQztFQUM1RCxDQUFDLENBQUMsR0FDRjtBQUVOIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/extra-usage/index.ts`

**信息:**
- 行数: 31
- 大小: 1101 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getIsNonInteractiveSession } from '../../bootstrap/state.js'
import type { Command } from '../../commands.js'
import { isOverageProvisioningAllowed } from '../../utils/auth.js'
import { isEnvTruthy } from '../../utils/envUtils.js'

function isExtraUsageAllowed(): boolean {
  if (isEnvTruthy(process.env.DISABLE_EXTRA_USAGE_COMMAND)) {
    return false
  }
  return isOverageProvisioningAllowed()
}

export const extraUsage = {
  type: 'local-jsx',
  name: 'extra-usage',
  description: 'Configure extra usage to keep working when limits are hit',
  isEnabled: () => isExtraUsageAllowed() && !getIsNonInteractiveSession(),
  load: () => import('./extra-usage.js'),
} satisfies Command

export const extraUsageNonInteractive = {
  type: 'local',
  name: 'extra-usage',
  supportsNonInteractive: true,
  description: 'Configure extra usage to keep working when limits are hit',
  isEnabled: () => isExtraUsageAllowed() && getIsNonInteractiveSession(),
  get isHidden() {
    return !getIsNonInteractiveSession()
  },
  load: () => import('./extra-usage-noninteractive.js'),
} satisfies Command

```

---


### `src/commands/fast/fast.tsx`

**信息:**
- 行数: 269
- 大小: 33931 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useState } from 'react';
import type { CommandResultDisplay, LocalJSXCommandContext } from '../../commands.js';
import { Dialog } from '../../components/design-system/Dialog.js';
import { FastIcon, getFastIconString } from '../../components/FastIcon.js';
import { Box, Link, Text } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../services/analytics/index.js';
import { type AppState, useAppState, useSetAppState } from '../../state/AppState.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { clearFastModeCooldown, FAST_MODE_MODEL_DISPLAY, getFastModeModel, getFastModeRuntimeState, getFastModeUnavailableReason, isFastModeEnabled, isFastModeSupportedByModel, prefetchFastModeStatus } from '../../utils/fastMode.js';
import { formatDuration } from '../../utils/format.js';
import { formatModelPricing, getOpus46CostTier } from '../../utils/modelCost.js';
import { updateSettingsForSource } from '../../utils/settings/settings.js';
function applyFastMode(enable: boolean, setAppState: (f: (prev: AppState) => AppState) => void): void {
  clearFastModeCooldown();
  updateSettingsForSource('userSettings', {
    fastMode: enable ? true : undefined
  });
  if (enable) {
    setAppState(prev => {
      // Only switch model if current model doesn't support fast mode
      const needsModelSwitch = !isFastModeSupportedByModel(prev.mainLoopModel);
      return {
        ...prev,
        ...(needsModelSwitch ? {
          mainLoopModel: getFastModeModel(),
          mainLoopModelForSession: null
        } : {}),
        fastMode: true
      };
    });
  } else {
    setAppState(prev => ({
      ...prev,
      fastMode: false
    }));
  }
}
export function FastModePicker(t0) {
  const $ = _c(30);
  const {
    onDone,
    unavailableReason
  } = t0;
  const model = useAppState(_temp);
  const initialFastMode = useAppState(_temp2);
  const setAppState = useSetAppState();
  const [enableFastMode, setEnableFastMode] = useState(initialFastMode ?? false);

```

---


### `src/commands/fast/index.ts`

**信息:**
- 行数: 26
- 大小: 693 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import {
  FAST_MODE_MODEL_DISPLAY,
  isFastModeEnabled,
} from '../../utils/fastMode.js'
import { shouldInferenceConfigCommandBeImmediate } from '../../utils/immediateCommand.js'

const fast = {
  type: 'local-jsx',
  name: 'fast',
  get description() {
    return `Toggle fast mode (${FAST_MODE_MODEL_DISPLAY} only)`
  },
  availability: ['claude-ai', 'console'],
  isEnabled: () => isFastModeEnabled(),
  get isHidden() {
    return !isFastModeEnabled()
  },
  argumentHint: '[on|off]',
  get immediate() {
    return shouldInferenceConfigCommandBeImmediate()
  },
  load: () => import('./fast.js'),
} satisfies Command

export default fast

```

---


### `src/commands/feedback/feedback.tsx`

**信息:**
- 行数: 25
- 大小: 5095 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import type { CommandResultDisplay, LocalJSXCommandContext } from '../../commands.js';
import { Feedback } from '../../components/Feedback.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import type { Message } from '../../types/message.js';

// Shared function to render the Feedback component
export function renderFeedbackComponent(onDone: (result?: string, options?: {
  display?: CommandResultDisplay;
}) => void, abortSignal: AbortSignal, messages: Message[], initialDescription: string = '', backgroundTasks: {
  [taskId: string]: {
    type: string;
    identity?: {
      agentId: string;
    };
    messages?: Message[];
  };
} = {}): React.ReactNode {
  return <Feedback abortSignal={abortSignal} messages={messages} initialDescription={initialDescription} onDone={onDone} backgroundTasks={backgroundTasks} />;
}
export async function call(onDone: LocalJSXCommandOnDone, context: LocalJSXCommandContext, args?: string): Promise<React.ReactNode> {
  const initialDescription = args || '';
  return renderFeedbackComponent(onDone, context.abortController.signal, context.messages, initialDescription);
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkNvbW1hbmRSZXN1bHREaXNwbGF5IiwiTG9jYWxKU1hDb21tYW5kQ29udGV4dCIsIkZlZWRiYWNrIiwiTG9jYWxKU1hDb21tYW5kT25Eb25lIiwiTWVzc2FnZSIsInJlbmRlckZlZWRiYWNrQ29tcG9uZW50Iiwib25Eb25lIiwicmVzdWx0Iiwib3B0aW9ucyIsImRpc3BsYXkiLCJhYm9ydFNpZ25hbCIsIkFib3J0U2lnbmFsIiwibWVzc2FnZXMiLCJpbml0aWFsRGVzY3JpcHRpb24iLCJiYWNrZ3JvdW5kVGFza3MiLCJ0YXNrSWQiLCJ0eXBlIiwiaWRlbnRpdHkiLCJhZ2VudElkIiwiUmVhY3ROb2RlIiwiY2FsbCIsImNvbnRleHQiLCJhcmdzIiwiUHJvbWlzZSIsImFib3J0Q29udHJvbGxlciIsInNpZ25hbCJdLCJzb3VyY2VzIjpbImZlZWRiYWNrLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB0eXBlIHtcbiAgQ29tbWFuZFJlc3VsdERpc3BsYXksXG4gIExvY2FsSlNYQ29tbWFuZENvbnRleHQsXG59IGZyb20gJy4uLy4uL2NvbW1hbmRzLmpzJ1xuaW1wb3J0IHsgRmVlZGJhY2sgfSBmcm9tICcuLi8uLi9jb21wb25lbnRzL0ZlZWRiYWNrLmpzJ1xuaW1wb3J0IHR5cGUgeyBMb2NhbEpTWENvbW1hbmRPbkRvbmUgfSBmcm9tICcuLi8uLi90eXBlcy9jb21tYW5kLmpzJ1xuaW1wb3J0IHR5cGUgeyBNZXNzYWdlIH0gZnJvbSAnLi4vLi4vdHlwZXMvbWVzc2FnZS5qcydcblxuLy8gU2hhcmVkIGZ1bmN0aW9uIHRvIHJlbmRlciB0aGUgRmVlZGJhY2sgY29tcG9uZW50XG5leHBvcnQgZnVuY3Rpb24gcmVuZGVyRmVlZGJhY2tDb21wb25lbnQoXG4gIG9uRG9uZTogKFxuICAgIHJlc3VsdD86IHN0cmluZyxcbiAgICBvcHRpb25zPzogeyBkaXNwbGF5PzogQ29tbWFuZFJlc3VsdERpc3BsYXkgfSxcbiAgKSA9PiB2b2lkLFxuICBhYm9ydFNpZ25hbDogQWJvcnRTaWduYWwsXG4gIG1lc3NhZ2VzOiBNZXNzYWdlW10sXG4gIGluaXRpYWxEZXNjcmlwdGlvbjogc3RyaW5nID0gJycsXG4gIGJhY2tncm91bmRUYXNrczoge1xuICAgIFt0YXNrSWQ6IHN0cmluZ106IHtcbiAgICAgIHR5cGU6IHN0cmluZ1xuICAgICAgaWRlbnRpdHk/OiB7IGFnZW50SWQ6IHN0cmluZyB9XG4gICAgICBtZXNzYWdlcz86IE1lc3NhZ2VbXVxuICAgIH1cbiAgfSA9IHt9LFxuKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgcmV0dXJuIChcbiAgICA8RmVlZGJhY2tcbiAgICAgIGFib3J0U2lnbmFsPXthYm9ydFNpZ25hbH1cbiAgICAgIG1lc3NhZ2VzPXttZXNzYWdlc31cbiAgICAgIGluaXRpYWxEZXNjcmlwdGlvbj17aW5pdGlhbERlc2NyaXB0aW9ufVxuICAgICAgb25Eb25lPXtvbkRvbmV9XG4gICAgICBiYWNrZ3JvdW5kVGFza3M9e2JhY2tncm91bmRUYXNrc31cbiAgICAvPlxuICApXG59XG5cbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBjYWxsKFxuICBvbkRvbmU6IExvY2FsSlNYQ29tbWFuZE9uRG9uZSxcbiAgY29udGV4dDogTG9jYWxKU1hDb21tYW5kQ29udGV4dCxcbiAgYXJncz86IHN0cmluZyxcbik6IFByb21pc2U8UmVhY3QuUmVhY3ROb2RlPiB7XG4gIGNvbnN0IGluaXRpYWxEZXNjcmlwdGlvbiA9IGFyZ3MgfHwgJydcbiAgcmV0dXJuIHJlbmRlckZlZWRiYWNrQ29tcG9uZW50KFxuICAgIG9uRG9uZSxcbiAgICBjb250ZXh0LmFib3J0Q29udHJvbGxlci5zaWduYWwsXG4gICAgY29udGV4dC5tZXNzYWdlcyxcbiAgICBpbml0aWFsRGVzY3JpcHRpb24sXG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixjQUNFQyxvQkFBb0IsRUFDcEJDLHNCQUFzQixRQUNqQixtQkFBbUI7QUFDMUIsU0FBU0MsUUFBUSxRQUFRLDhCQUE4QjtBQUN2RCxjQUFjQyxxQkFBcUIsUUFBUSx3QkFBd0I7QUFDbkUsY0FBY0MsT0FBTyxRQUFRLHdCQUF3Qjs7QUFFckQ7QUFDQSxPQUFPLFNBQVNDLHVCQUF1QkEsQ0FDckNDLE1BQU0sRUFBRSxDQUNOQyxNQUFlLENBQVIsRUFBRSxNQUFNLEVBQ2ZDLE9BQTRDLENBQXBDLEVBQUU7RUFBRUMsT0FBTyxDQUFDLEVBQUVULG9CQUFvQjtBQUFDLENBQUMsRUFDNUMsR0FBRyxJQUFJLEVBQ1RVLFdBQVcsRUFBRUMsV0FBVyxFQUN4QkMsUUFBUSxFQUFFUixPQUFPLEVBQUUsRUFDbkJTLGtCQUFrQixFQUFFLE1BQU0sR0FBRyxFQUFFLEVBQy9CQyxlQUFlLEVBQUU7RUFDZixDQUFDQyxNQUFNLEVBQUUsTUFBTSxDQUFDLEVBQUU7SUFDaEJDLElBQUksRUFBRSxNQUFNO0lBQ1pDLFFBQVEsQ0FBQyxFQUFFO01BQUVDLE9BQU8sRUFBRSxNQUFNO0lBQUMsQ0FBQztJQUM5Qk4sUUFBUSxDQUFDLEVBQUVSLE9BQU8sRUFBRTtFQUN0QixDQUFDO0FBQ0gsQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUNQLEVBQUVMLEtBQUssQ0FBQ29CLFNBQVMsQ0FBQztFQUNqQixPQUNFLENBQUMsUUFBUSxDQUNQLFdBQVcsQ0FBQyxDQUFDVCxXQUFXLENBQUMsQ0FDekIsUUFBUSxDQUFDLENBQUNFLFFBQVEsQ0FBQyxDQUNuQixrQkFBa0IsQ0FBQyxDQUFDQyxrQkFBa0IsQ0FBQyxDQUN2QyxNQUFNLENBQUMsQ0FBQ1AsTUFBTSxDQUFDLENBQ2YsZUFBZSxDQUFDLENBQUNRLGVBQWUsQ0FBQyxHQUNqQztBQUVOO0FBRUEsT0FBTyxlQUFlTSxJQUFJQSxDQUN4QmQsTUFBTSxFQUFFSCxxQkFBcUIsRUFDN0JrQixPQUFPLEVBQUVwQixzQkFBc0IsRUFDL0JxQixJQUFhLENBQVIsRUFBRSxNQUFNLENBQ2QsRUFBRUMsT0FBTyxDQUFDeEIsS0FBSyxDQUFDb0IsU0FBUyxDQUFDLENBQUM7RUFDMUIsTUFBTU4sa0JBQWtCLEdBQUdTLElBQUksSUFBSSxFQUFFO0VBQ3JDLE9BQU9qQix1QkFBdUIsQ0FDNUJDLE1BQU0sRUFDTmUsT0FBTyxDQUFDRyxlQUFlLENBQUNDLE1BQU0sRUFDOUJKLE9BQU8sQ0FBQ1QsUUFBUSxFQUNoQkMsa0JBQ0YsQ0FBQztBQUNIIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/feedback/index.ts`

**信息:**
- 行数: 26
- 大小: 931 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { isPolicyAllowed } from '../../services/policyLimits/index.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { isEssentialTrafficOnly } from '../../utils/privacyLevel.js'

const feedback = {
  aliases: ['bug'],
  type: 'local-jsx',
  name: 'feedback',
  description: `Submit feedback about Claude Code`,
  argumentHint: '[report]',
  isEnabled: () =>
    !(
      isEnvTruthy(process.env.CLAUDE_CODE_USE_BEDROCK) ||
      isEnvTruthy(process.env.CLAUDE_CODE_USE_VERTEX) ||
      isEnvTruthy(process.env.CLAUDE_CODE_USE_FOUNDRY) ||
      isEnvTruthy(process.env.DISABLE_FEEDBACK_COMMAND) ||
      isEnvTruthy(process.env.DISABLE_BUG_COMMAND) ||
      isEssentialTrafficOnly() ||
      process.env.USER_TYPE === 'ant' ||
      !isPolicyAllowed('allow_product_feedback')
    ),
  load: () => import('./feedback.js'),
} satisfies Command

export default feedback

```

---


### `src/commands/files/files.ts`

**信息:**
- 行数: 19
- 大小: 688 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { relative } from 'path'
import type { ToolUseContext } from '../../Tool.js'
import type { LocalCommandResult } from '../../types/command.js'
import { getCwd } from '../../utils/cwd.js'
import { cacheKeys } from '../../utils/fileStateCache.js'

export async function call(
  _args: string,
  context: ToolUseContext,
): Promise<LocalCommandResult> {
  const files = context.readFileState ? cacheKeys(context.readFileState) : []

  if (files.length === 0) {
    return { type: 'text' as const, value: 'No files in context' }
  }

  const fileList = files.map(file => relative(getCwd(), file)).join('\n')
  return { type: 'text' as const, value: `Files in context:\n${fileList}` }
}

```

---


### `src/commands/files/index.ts`

**信息:**
- 行数: 12
- 大小: 316 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const files = {
  type: 'local',
  name: 'files',
  description: 'List all files currently in context',
  isEnabled: () => process.env.USER_TYPE === 'ant',
  supportsNonInteractive: true,
  load: () => import('./files.js'),
} satisfies Command

export default files

```

---


### `src/commands/heapdump/heapdump.ts`

**信息:**
- 行数: 17
- 大小: 398 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { performHeapDump } from '../../utils/heapDumpService.js'

export async function call(): Promise<{ type: 'text'; value: string }> {
  const result = await performHeapDump()

  if (!result.success) {
    return {
      type: 'text',
      value: `Failed to create heap dump: ${result.error}`,
    }
  }

  return {
    type: 'text',
    value: `${result.heapPath}\n${result.diagPath}`,
  }
}

```

---


### `src/commands/heapdump/index.ts`

**信息:**
- 行数: 12
- 大小: 288 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const heapDump = {
  type: 'local',
  name: 'heapdump',
  description: 'Dump the JS heap to ~/Desktop',
  isHidden: true,
  supportsNonInteractive: true,
  load: () => import('./heapdump.js'),
} satisfies Command

export default heapDump

```

---


### `src/commands/help/help.tsx`

**信息:**
- 行数: 11
- 大小: 1432 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { HelpV2 } from '../../components/HelpV2/HelpV2.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
export const call: LocalJSXCommandCall = async (onDone, {
  options: {
    commands
  }
}) => {
  return <HelpV2 commands={commands} onClose={onDone} />;
};
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkhlbHBWMiIsIkxvY2FsSlNYQ29tbWFuZENhbGwiLCJjYWxsIiwib25Eb25lIiwib3B0aW9ucyIsImNvbW1hbmRzIl0sInNvdXJjZXMiOlsiaGVscC50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBIZWxwVjIgfSBmcm9tICcuLi8uLi9jb21wb25lbnRzL0hlbHBWMi9IZWxwVjIuanMnXG5pbXBvcnQgdHlwZSB7IExvY2FsSlNYQ29tbWFuZENhbGwgfSBmcm9tICcuLi8uLi90eXBlcy9jb21tYW5kLmpzJ1xuXG5leHBvcnQgY29uc3QgY2FsbDogTG9jYWxKU1hDb21tYW5kQ2FsbCA9IGFzeW5jIChcbiAgb25Eb25lLFxuICB7IG9wdGlvbnM6IHsgY29tbWFuZHMgfSB9LFxuKSA9PiB7XG4gIHJldHVybiA8SGVscFYyIGNvbW1hbmRzPXtjb21tYW5kc30gb25DbG9zZT17b25Eb25lfSAvPlxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLE1BQU0sUUFBUSxtQ0FBbUM7QUFDMUQsY0FBY0MsbUJBQW1CLFFBQVEsd0JBQXdCO0FBRWpFLE9BQU8sTUFBTUMsSUFBSSxFQUFFRCxtQkFBbUIsR0FBRyxNQUFBQyxDQUN2Q0MsTUFBTSxFQUNOO0VBQUVDLE9BQU8sRUFBRTtJQUFFQztFQUFTO0FBQUUsQ0FBQyxLQUN0QjtFQUNILE9BQU8sQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLENBQUNBLFFBQVEsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDRixNQUFNLENBQUMsR0FBRztBQUN4RCxDQUFDIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/help/index.ts`

**信息:**
- 行数: 10
- 大小: 229 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const help = {
  type: 'local-jsx',
  name: 'help',
  description: 'Show help and available commands',
  load: () => import('./help.js'),
} satisfies Command

export default help

```

---


### `src/commands/hooks/hooks.tsx`

**信息:**
- 行数: 13
- 大小: 2679 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { HooksConfigMenu } from '../../components/hooks/HooksConfigMenu.js';
import { logEvent } from '../../services/analytics/index.js';
import { getTools } from '../../tools.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
export const call: LocalJSXCommandCall = async (onDone, context) => {
  logEvent('tengu_hooks_command', {});
  const appState = context.getAppState();
  const permissionContext = appState.toolPermissionContext;
  const toolNames = getTools(permissionContext).map(tool => tool.name);
  return <HooksConfigMenu toolNames={toolNames} onExit={onDone} />;
};
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkhvb2tzQ29uZmlnTWVudSIsImxvZ0V2ZW50IiwiZ2V0VG9vbHMiLCJMb2NhbEpTWENvbW1hbmRDYWxsIiwiY2FsbCIsIm9uRG9uZSIsImNvbnRleHQiLCJhcHBTdGF0ZSIsImdldEFwcFN0YXRlIiwicGVybWlzc2lvbkNvbnRleHQiLCJ0b29sUGVybWlzc2lvbkNvbnRleHQiLCJ0b29sTmFtZXMiLCJtYXAiLCJ0b29sIiwibmFtZSJdLCJzb3VyY2VzIjpbImhvb2tzLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IEhvb2tzQ29uZmlnTWVudSB9IGZyb20gJy4uLy4uL2NvbXBvbmVudHMvaG9va3MvSG9va3NDb25maWdNZW51LmpzJ1xuaW1wb3J0IHsgbG9nRXZlbnQgfSBmcm9tICcuLi8uLi9zZXJ2aWNlcy9hbmFseXRpY3MvaW5kZXguanMnXG5pbXBvcnQgeyBnZXRUb29scyB9IGZyb20gJy4uLy4uL3Rvb2xzLmpzJ1xuaW1wb3J0IHR5cGUgeyBMb2NhbEpTWENvbW1hbmRDYWxsIH0gZnJvbSAnLi4vLi4vdHlwZXMvY29tbWFuZC5qcydcblxuZXhwb3J0IGNvbnN0IGNhbGw6IExvY2FsSlNYQ29tbWFuZENhbGwgPSBhc3luYyAob25Eb25lLCBjb250ZXh0KSA9PiB7XG4gIGxvZ0V2ZW50KCd0ZW5ndV9ob29rc19jb21tYW5kJywge30pXG4gIGNvbnN0IGFwcFN0YXRlID0gY29udGV4dC5nZXRBcHBTdGF0ZSgpXG4gIGNvbnN0IHBlcm1pc3Npb25Db250ZXh0ID0gYXBwU3RhdGUudG9vbFBlcm1pc3Npb25Db250ZXh0XG4gIGNvbnN0IHRvb2xOYW1lcyA9IGdldFRvb2xzKHBlcm1pc3Npb25Db250ZXh0KS5tYXAodG9vbCA9PiB0b29sLm5hbWUpXG4gIHJldHVybiA8SG9va3NDb25maWdNZW51IHRvb2xOYW1lcz17dG9vbE5hbWVzfSBvbkV4aXQ9e29uRG9uZX0gLz5cbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixTQUFTQyxlQUFlLFFBQVEsMkNBQTJDO0FBQzNFLFNBQVNDLFFBQVEsUUFBUSxtQ0FBbUM7QUFDNUQsU0FBU0MsUUFBUSxRQUFRLGdCQUFnQjtBQUN6QyxjQUFjQyxtQkFBbUIsUUFBUSx3QkFBd0I7QUFFakUsT0FBTyxNQUFNQyxJQUFJLEVBQUVELG1CQUFtQixHQUFHLE1BQUFDLENBQU9DLE1BQU0sRUFBRUMsT0FBTyxLQUFLO0VBQ2xFTCxRQUFRLENBQUMscUJBQXFCLEVBQUUsQ0FBQyxDQUFDLENBQUM7RUFDbkMsTUFBTU0sUUFBUSxHQUFHRCxPQUFPLENBQUNFLFdBQVcsQ0FBQyxDQUFDO0VBQ3RDLE1BQU1DLGlCQUFpQixHQUFHRixRQUFRLENBQUNHLHFCQUFxQjtFQUN4RCxNQUFNQyxTQUFTLEdBQUdULFFBQVEsQ0FBQ08saUJBQWlCLENBQUMsQ0FBQ0csR0FBRyxDQUFDQyxJQUFJLElBQUlBLElBQUksQ0FBQ0MsSUFBSSxDQUFDO0VBQ3BFLE9BQU8sQ0FBQyxlQUFlLENBQUMsU0FBUyxDQUFDLENBQUNILFNBQVMsQ0FBQyxDQUFDLE1BQU0sQ0FBQyxDQUFDTixNQUFNLENBQUMsR0FBRztBQUNsRSxDQUFDIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/hooks/index.ts`

**信息:**
- 行数: 11
- 大小: 260 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const hooks = {
  type: 'local-jsx',
  name: 'hooks',
  description: 'View hook configurations for tool events',
  immediate: true,
  load: () => import('./hooks.js'),
} satisfies Command

export default hooks

```

---


### `src/commands/ide/ide.tsx`

**信息:**
- 行数: 646
- 大小: 77066 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import * as path from 'path';
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { logEvent } from 'src/services/analytics/index.js';
import type { CommandResultDisplay, LocalJSXCommandContext } from '../../commands.js';
import { Select } from '../../components/CustomSelect/index.js';
import { Dialog } from '../../components/design-system/Dialog.js';
import { IdeAutoConnectDialog, IdeDisableAutoConnectDialog, shouldShowAutoConnectDialog, shouldShowDisableAutoConnectDialog } from '../../components/IdeAutoConnectDialog.js';
import { Box, Text } from '../../ink.js';
import { clearServerCache } from '../../services/mcp/client.js';
import type { ScopedMcpServerConfig } from '../../services/mcp/types.js';
import { useAppState, useSetAppState } from '../../state/AppState.js';
import { getCwd } from '../../utils/cwd.js';
import { execFileNoThrow } from '../../utils/execFileNoThrow.js';
import { type DetectedIDEInfo, detectIDEs, detectRunningIDEs, type IdeType, isJetBrainsIde, isSupportedJetBrainsTerminal, isSupportedTerminal, toIDEDisplayName } from '../../utils/ide.js';
import { getCurrentWorktreeSession } from '../../utils/worktree.js';
type IDEScreenProps = {
  availableIDEs: DetectedIDEInfo[];
  unavailableIDEs: DetectedIDEInfo[];
  selectedIDE?: DetectedIDEInfo | null;
  onClose: () => void;
  onSelect: (ide?: DetectedIDEInfo) => void;
};
function IDEScreen(t0) {
  const $ = _c(39);
  const {
    availableIDEs,
    unavailableIDEs,
    selectedIDE,
    onClose,
    onSelect
  } = t0;
  let t1;
  if ($[0] !== selectedIDE?.port) {
    t1 = selectedIDE?.port?.toString() ?? "None";
    $[0] = selectedIDE?.port;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const [selectedValue, setSelectedValue] = useState(t1);
  const [showAutoConnectDialog, setShowAutoConnectDialog] = useState(false);
  const [showDisableAutoConnectDialog, setShowDisableAutoConnectDialog] = useState(false);
  let t2;
  if ($[2] !== availableIDEs || $[3] !== onSelect) {
    t2 = value => {
      if (value !== "None" && shouldShowAutoConnectDialog()) {
        setShowAutoConnectDialog(true);
      } else {

```

---


### `src/commands/ide/index.ts`

**信息:**
- 行数: 11
- 大小: 258 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const ide = {
  type: 'local-jsx',
  name: 'ide',
  description: 'Manage IDE integrations and show status',
  argumentHint: '[open]',
  load: () => import('./ide.js'),
} satisfies Command

export default ide

```

---


### `src/commands/init-verifiers.ts`

**信息:**
- 行数: 262
- 大小: 10315 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../commands.js'

const command = {
  type: 'prompt',
  name: 'init-verifiers',
  description:
    'Create verifier skill(s) for automated verification of code changes',
  contentLength: 0, // Dynamic content
  progressMessage: 'analyzing your project and creating verifier skills',
  source: 'builtin',
  async getPromptForCommand() {
    return [
      {
        type: 'text',
        text: `Use the TodoWrite tool to track your progress through this multi-step task.

## Goal

Create one or more verifier skills that can be used by the Verify agent to automatically verify code changes in this project or folder. You may create multiple verifiers if the project has different verification needs (e.g., both web UI and API endpoints).

**Do NOT create verifiers for unit tests or typechecking.** Those are already handled by the standard build/test workflow and don't need dedicated verifier skills. Focus on functional verification: web UI (Playwright), CLI (Tmux), and API (HTTP) verifiers.

## Phase 1: Auto-Detection

Analyze the project to detect what's in different subdirectories. The project may contain multiple sub-projects or areas that need different verification approaches (e.g., a web frontend, an API backend, and shared libraries all in one repo).

1. **Scan top-level directories** to identify distinct project areas:
   - Look for separate package.json, Cargo.toml, pyproject.toml, go.mod in subdirectories
   - Identify distinct application types in different folders

2. **For each area, detect:**

   a. **Project type and stack**
      - Primary language(s) and frameworks
      - Package managers (npm, yarn, pnpm, pip, cargo, etc.)

   b. **Application type**
      - Web app (React, Next.js, Vue, etc.) → suggest Playwright-based verifier
      - CLI tool → suggest Tmux-based verifier
      - API service (Express, FastAPI, etc.) → suggest HTTP-based verifier

   c. **Existing verification tools**
      - Test frameworks (Jest, Vitest, pytest, etc.)
      - E2E tools (Playwright, Cypress, etc.)
      - Dev server scripts in package.json

   d. **Dev server configuration**
      - How to start the dev server
      - What URL it runs on
      - What text indicates it's ready

```

---


### `src/commands/init.ts`

**信息:**
- 行数: 256
- 大小: 20961 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { Command } from '../commands.js'
import { maybeMarkProjectOnboardingComplete } from '../projectOnboardingState.js'
import { isEnvTruthy } from '../utils/envUtils.js'

const OLD_INIT_PROMPT = `Please analyze this codebase and create a CLAUDE.md file, which will be given to future instances of Claude Code to operate in this repository.

What to add:
1. Commands that will be commonly used, such as how to build, lint, and run tests. Include the necessary commands to develop in this codebase, such as how to run a single test.
2. High-level code architecture and structure so that future instances can be productive more quickly. Focus on the "big picture" architecture that requires reading multiple files to understand.

Usage notes:
- If there's already a CLAUDE.md, suggest improvements to it.
- When you make the initial CLAUDE.md, do not repeat yourself and do not include obvious instructions like "Provide helpful error messages to users", "Write unit tests for all new utilities", "Never include sensitive information (API keys, tokens) in code or commits".
- Avoid listing every component or file structure that can be easily discovered.
- Don't include generic development practices.
- If there are Cursor rules (in .cursor/rules/ or .cursorrules) or Copilot rules (in .github/copilot-instructions.md), make sure to include the important parts.
- If there is a README.md, make sure to include the important parts.
- Do not make up information such as "Common Development Tasks", "Tips for Development", "Support and Documentation" unless this is expressly included in other files that you read.
- Be sure to prefix the file with the following text:

\`\`\`
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
\`\`\``

const NEW_INIT_PROMPT = `Set up a minimal CLAUDE.md (and optionally skills and hooks) for this repo. CLAUDE.md is loaded into every Claude Code session, so it must be concise — only include what Claude would get wrong without it.

## Phase 1: Ask what to set up

Use AskUserQuestion to find out what the user wants:

- "Which CLAUDE.md files should /init set up?"
  Options: "Project CLAUDE.md" | "Personal CLAUDE.local.md" | "Both project + personal"
  Description for project: "Team-shared instructions checked into source control — architecture, coding standards, common workflows."
  Description for personal: "Your private preferences for this project (gitignored, not shared) — your role, sandbox URLs, preferred test data, workflow quirks."

- "Also set up skills and hooks?"
  Options: "Skills + hooks" | "Skills only" | "Hooks only" | "Neither, just CLAUDE.md"
  Description for skills: "On-demand capabilities you or Claude invoke with \`/skill-name\` — good for repeatable workflows and reference knowledge."
  Description for hooks: "Deterministic shell commands that run on tool events (e.g., format after every edit). Claude can't skip them."

## Phase 2: Explore the codebase

Launch a subagent to survey the codebase, and ask it to read key files to understand the project: manifest files (package.json, Cargo.toml, pyproject.toml, go.mod, pom.xml, etc.), README, Makefile/build configs, CI config, existing CLAUDE.md, .claude/rules/, AGENTS.md, .cursor/rules or .cursorrules, .github/copilot-instructions.md, .windsurfrules, .clinerules, .mcp.json.

Detect:
- Build, test, and lint commands (especially non-standard ones)
- Languages, frameworks, and package manager

```

---


### `src/commands/insights.ts`

**信息:**
- 行数: 3200
- 大小: 115949 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { execFileSync } from 'child_process'
import { diffLines } from 'diff'
import { constants as fsConstants } from 'fs'
import {
  copyFile,
  mkdir,
  mkdtemp,
  readdir,
  readFile,
  rm,
  unlink,
  writeFile,
} from 'fs/promises'
import { tmpdir } from 'os'
import { extname, join } from 'path'
import type { Command } from '../commands.js'
import { queryWithModel } from '../services/api/claude.js'
import {
  AGENT_TOOL_NAME,
  LEGACY_AGENT_TOOL_NAME,
} from '../tools/AgentTool/constants.js'
import type { LogOption } from '../types/logs.js'
import { getClaudeConfigHomeDir } from '../utils/envUtils.js'
import { toError } from '../utils/errors.js'
import { execFileNoThrow } from '../utils/execFileNoThrow.js'
import { logError } from '../utils/log.js'
import { extractTextContent } from '../utils/messages.js'
import { getDefaultOpusModel } from '../utils/model/model.js'
import {
  getProjectsDir,
  getSessionFilesWithMtime,
  getSessionIdFromLog,
  loadAllLogsFromSessionFile,
} from '../utils/sessionStorage.js'
import { jsonParse, jsonStringify } from '../utils/slowOperations.js'
import { countCharInString } from '../utils/stringUtils.js'
import { asSystemPrompt } from '../utils/systemPromptType.js'
import { escapeXmlAttr as escapeHtml } from '../utils/xml.js'

// Model for facet extraction and summarization (Opus - best quality)
function getAnalysisModel(): string {
  return getDefaultOpusModel()
}

// Model for narrative insights (Opus - best quality)
function getInsightsModel(): string {
  return getDefaultOpusModel()
}

// ============================================================================

```

---


### `src/commands/install-github-app/ApiKeyStep.tsx`

**信息:**
- 行数: 231
- 大小: 23518 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useState } from 'react';
import TextInput from '../../components/TextInput.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { Box, color, Text, useTheme } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
interface ApiKeyStepProps {
  existingApiKey: string | null;
  useExistingKey: boolean;
  apiKeyOrOAuthToken: string;
  onApiKeyChange: (value: string) => void;
  onToggleUseExistingKey: (useExisting: boolean) => void;
  onSubmit: () => void;
  onCreateOAuthToken?: () => void;
  selectedOption?: 'existing' | 'new' | 'oauth';
  onSelectOption?: (option: 'existing' | 'new' | 'oauth') => void;
}
export function ApiKeyStep(t0) {
  const $ = _c(55);
  const {
    existingApiKey,
    apiKeyOrOAuthToken,
    onApiKeyChange,
    onSubmit,
    onToggleUseExistingKey,
    onCreateOAuthToken,
    selectedOption: t1,
    onSelectOption
  } = t0;
  const selectedOption = t1 === undefined ? existingApiKey ? "existing" : onCreateOAuthToken ? "oauth" : "new" : t1;
  const [cursorOffset, setCursorOffset] = useState(0);
  const terminalSize = useTerminalSize();
  const [theme] = useTheme();
  let t2;
  if ($[0] !== existingApiKey || $[1] !== onCreateOAuthToken || $[2] !== onSelectOption || $[3] !== onToggleUseExistingKey || $[4] !== selectedOption) {
    t2 = () => {
      if (selectedOption === "new" && onCreateOAuthToken) {
        onSelectOption?.("oauth");
      } else {
        if (selectedOption === "oauth" && existingApiKey) {
          onSelectOption?.("existing");
          onToggleUseExistingKey(true);
        }
      }
    };
    $[0] = existingApiKey;
    $[1] = onCreateOAuthToken;
    $[2] = onSelectOption;
    $[3] = onToggleUseExistingKey;
    $[4] = selectedOption;

```

---


### `src/commands/install-github-app/CheckExistingSecretStep.tsx`

**信息:**
- 行数: 190
- 大小: 18135 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useState } from 'react';
import TextInput from '../../components/TextInput.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { Box, color, Text, useTheme } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
interface CheckExistingSecretStepProps {
  useExistingSecret: boolean;
  secretName: string;
  onToggleUseExistingSecret: (useExisting: boolean) => void;
  onSecretNameChange: (value: string) => void;
  onSubmit: () => void;
}
export function CheckExistingSecretStep(t0) {
  const $ = _c(42);
  const {
    useExistingSecret,
    secretName,
    onToggleUseExistingSecret,
    onSecretNameChange,
    onSubmit
  } = t0;
  const [cursorOffset, setCursorOffset] = useState(0);
  const terminalSize = useTerminalSize();
  const [theme] = useTheme();
  let t1;
  if ($[0] !== onToggleUseExistingSecret) {
    t1 = () => onToggleUseExistingSecret(true);
    $[0] = onToggleUseExistingSecret;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const handlePrevious = t1;
  let t2;
  if ($[2] !== onToggleUseExistingSecret) {
    t2 = () => onToggleUseExistingSecret(false);
    $[2] = onToggleUseExistingSecret;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  const handleNext = t2;
  let t3;
  if ($[4] !== handleNext || $[5] !== handlePrevious || $[6] !== onSubmit) {
    t3 = {
      "confirm:previous": handlePrevious,
      "confirm:next": handleNext,
      "confirm:yes": onSubmit
    };

```

---


### `src/commands/install-github-app/CheckGitHubStep.tsx`

**信息:**
- 行数: 15
- 大小: 1248 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Text } from '../../ink.js';
export function CheckGitHubStep() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <Text>Checking GitHub CLI installation…</Text>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlRleHQiLCJDaGVja0dpdEh1YlN0ZXAiLCIkIiwiX2MiLCJ0MCIsIlN5bWJvbCIsImZvciJdLCJzb3VyY2VzIjpbIkNoZWNrR2l0SHViU3RlcC50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgVGV4dCB9IGZyb20gJy4uLy4uL2luay5qcydcblxuZXhwb3J0IGZ1bmN0aW9uIENoZWNrR2l0SHViU3RlcCgpIHtcbiAgcmV0dXJuIDxUZXh0PkNoZWNraW5nIEdpdEh1YiBDTEkgaW5zdGFsbGF0aW9u4oCmPC9UZXh0PlxufVxuIl0sIm1hcHBpbmdzIjoiO0FBQUEsT0FBT0EsS0FBSyxNQUFNLE9BQU87QUFDekIsU0FBU0MsSUFBSSxRQUFRLGNBQWM7QUFFbkMsT0FBTyxTQUFBQyxnQkFBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUFBLElBQUFDLEVBQUE7RUFBQSxJQUFBRixDQUFBLFFBQUFHLE1BQUEsQ0FBQUMsR0FBQTtJQUNFRixFQUFBLElBQUMsSUFBSSxDQUFDLGlDQUFpQyxFQUF0QyxJQUFJLENBQXlDO0lBQUFGLENBQUEsTUFBQUUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUYsQ0FBQTtFQUFBO0VBQUEsT0FBOUNFLEVBQThDO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/commands/install-github-app/ChooseRepoStep.tsx`

**信息:**
- 行数: 211
- 大小: 21279 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useState } from 'react';
import TextInput from '../../components/TextInput.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { Box, Text } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
interface ChooseRepoStepProps {
  currentRepo: string | null;
  useCurrentRepo: boolean;
  repoUrl: string;
  onRepoUrlChange: (value: string) => void;
  onToggleUseCurrentRepo: (useCurrentRepo: boolean) => void;
  onSubmit: () => void;
}
export function ChooseRepoStep(t0) {
  const $ = _c(49);
  const {
    currentRepo,
    useCurrentRepo,
    repoUrl,
    onRepoUrlChange,
    onSubmit,
    onToggleUseCurrentRepo
  } = t0;
  const [cursorOffset, setCursorOffset] = useState(0);
  const [showEmptyError, setShowEmptyError] = useState(false);
  const terminalSize = useTerminalSize();
  const textInputColumns = terminalSize.columns;
  let t1;
  if ($[0] !== currentRepo || $[1] !== onSubmit || $[2] !== repoUrl || $[3] !== useCurrentRepo) {
    t1 = () => {
      const repoName = useCurrentRepo ? currentRepo : repoUrl;
      if (!repoName?.trim()) {
        setShowEmptyError(true);
        return;
      }
      onSubmit();
    };
    $[0] = currentRepo;
    $[1] = onSubmit;
    $[2] = repoUrl;
    $[3] = useCurrentRepo;
    $[4] = t1;
  } else {
    t1 = $[4];
  }
  const handleSubmit = t1;
  const isTextInputVisible = !useCurrentRepo || !currentRepo;
  let t2;
  if ($[5] !== onToggleUseCurrentRepo) {

```

---


### `src/commands/install-github-app/CreatingStep.tsx`

**信息:**
- 行数: 65
- 大小: 9266 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../../ink.js';
import type { Workflow } from './types.js';
interface CreatingStepProps {
  currentWorkflowInstallStep: number;
  secretExists: boolean;
  useExistingSecret: boolean;
  secretName: string;
  skipWorkflow?: boolean;
  selectedWorkflows: Workflow[];
}
export function CreatingStep(t0) {
  const $ = _c(10);
  const {
    currentWorkflowInstallStep,
    secretExists,
    useExistingSecret,
    secretName,
    skipWorkflow: t1,
    selectedWorkflows
  } = t0;
  const skipWorkflow = t1 === undefined ? false : t1;
  let t2;
  if ($[0] !== secretExists || $[1] !== secretName || $[2] !== selectedWorkflows || $[3] !== skipWorkflow || $[4] !== useExistingSecret) {
    t2 = skipWorkflow ? ["Getting repository information", secretExists && useExistingSecret ? "Using existing API key secret" : `Setting up ${secretName} secret`] : ["Getting repository information", "Creating branch", selectedWorkflows.length > 1 ? "Creating workflow files" : "Creating workflow file", secretExists && useExistingSecret ? "Using existing API key secret" : `Setting up ${secretName} secret`, "Opening pull request page"];
    $[0] = secretExists;
    $[1] = secretName;
    $[2] = selectedWorkflows;
    $[3] = skipWorkflow;
    $[4] = useExistingSecret;
    $[5] = t2;
  } else {
    t2 = $[5];
  }
  const progressSteps = t2;
  let t3;
  if ($[6] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = <Box flexDirection="column" marginBottom={1}><Text bold={true}>Install GitHub App</Text><Text dimColor={true}>Create GitHub Actions workflow</Text></Box>;
    $[6] = t3;
  } else {
    t3 = $[6];
  }
  let t4;
  if ($[7] !== currentWorkflowInstallStep || $[8] !== progressSteps) {
    t4 = <><Box flexDirection="column" borderStyle="round" paddingX={1}>{t3}{progressSteps.map((stepText, index) => {
          let status = "pending";
          if (index < currentWorkflowInstallStep) {
            status = "completed";
          } else {

```

---


### `src/commands/install-github-app/ErrorStep.tsx`

**信息:**
- 行数: 85
- 大小: 8602 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { GITHUB_ACTION_SETUP_DOCS_URL } from '../../constants/github-app.js';
import { Box, Text } from '../../ink.js';
interface ErrorStepProps {
  error: string | undefined;
  errorReason?: string;
  errorInstructions?: string[];
}
export function ErrorStep(t0) {
  const $ = _c(15);
  const {
    error,
    errorReason,
    errorInstructions
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Box flexDirection="column" marginBottom={1}><Text bold={true}>Install GitHub App</Text></Box>;
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  let t2;
  if ($[1] !== error) {
    t2 = <Text color="error">Error: {error}</Text>;
    $[1] = error;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  let t3;
  if ($[3] !== errorReason) {
    t3 = errorReason && <Box marginTop={1}><Text dimColor={true}>Reason: {errorReason}</Text></Box>;
    $[3] = errorReason;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  let t4;
  if ($[5] !== errorInstructions) {
    t4 = errorInstructions && errorInstructions.length > 0 && <Box flexDirection="column" marginTop={1}><Text dimColor={true}>How to fix:</Text>{errorInstructions.map(_temp)}</Box>;
    $[5] = errorInstructions;
    $[6] = t4;
  } else {
    t4 = $[6];
  }
  let t5;
  if ($[7] === Symbol.for("react.memo_cache_sentinel")) {
    t5 = <Box marginTop={1}><Text dimColor={true}>For manual setup instructions, see:{" "}<Text color="claude">{GITHUB_ACTION_SETUP_DOCS_URL}</Text></Text></Box>;

```

---


### `src/commands/install-github-app/ExistingWorkflowStep.tsx`

**信息:**
- 行数: 103
- 大小: 9833 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Select } from 'src/components/CustomSelect/index.js';
import { Box, Text } from '../../ink.js';
interface ExistingWorkflowStepProps {
  repoName: string;
  onSelectAction: (action: 'update' | 'skip' | 'exit') => void;
}
export function ExistingWorkflowStep(t0) {
  const $ = _c(16);
  const {
    repoName,
    onSelectAction
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = [{
      label: "Update workflow file with latest version",
      value: "update"
    }, {
      label: "Skip workflow update (configure secrets only)",
      value: "skip"
    }, {
      label: "Exit without making changes",
      value: "exit"
    }];
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const options = t1;
  let t2;
  if ($[1] !== onSelectAction) {
    t2 = value => {
      onSelectAction(value as 'update' | 'skip' | 'exit');
    };
    $[1] = onSelectAction;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  const handleSelect = t2;
  let t3;
  if ($[3] !== onSelectAction) {
    t3 = () => {
      onSelectAction("exit");
    };
    $[3] = onSelectAction;
    $[4] = t3;
  } else {

```

---


### `src/commands/install-github-app/InstallAppStep.tsx`

**信息:**
- 行数: 94
- 大小: 9601 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React from 'react';
import { GITHUB_ACTION_SETUP_DOCS_URL } from '../../constants/github-app.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
interface InstallAppStepProps {
  repoUrl: string;
  onSubmit: () => void;
}
export function InstallAppStep(t0) {
  const $ = _c(12);
  const {
    repoUrl,
    onSubmit
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = {
      context: "Confirmation"
    };
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  useKeybinding("confirm:yes", onSubmit, t1);
  let t2;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Box flexDirection="column" marginBottom={1}><Text bold={true}>Install the Claude GitHub App</Text></Box>;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  let t3;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = <Box marginBottom={1}><Text>Opening browser to install the Claude GitHub App…</Text></Box>;
    $[2] = t3;
  } else {
    t3 = $[2];
  }
  let t4;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
    t4 = <Box marginBottom={1}><Text>If your browser doesn't open automatically, visit:</Text></Box>;
    $[3] = t4;
  } else {
    t4 = $[3];
  }
  let t5;
  if ($[4] === Symbol.for("react.memo_cache_sentinel")) {
    t5 = <Box marginBottom={1}><Text underline={true}>https://github.com/apps/claude</Text></Box>;

```

---


### `src/commands/install-github-app/OAuthFlowStep.tsx`

**信息:**
- 行数: 276
- 大小: 39935 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { KeyboardShortcutHint } from '../../components/design-system/KeyboardShortcutHint.js';
import { Spinner } from '../../components/Spinner.js';
import TextInput from '../../components/TextInput.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { setClipboard } from '../../ink/termio/osc.js';
import { Box, Link, Text } from '../../ink.js';
import { OAuthService } from '../../services/oauth/index.js';
import { saveOAuthTokensIfNeeded } from '../../utils/auth.js';
import { logError } from '../../utils/log.js';
interface OAuthFlowStepProps {
  onSuccess: (token: string) => void;
  onCancel: () => void;
}
type OAuthStatus = {
  state: 'starting';
} | {
  state: 'waiting_for_login';
  url: string;
} | {
  state: 'processing';
} | {
  state: 'success';
  token: string;
} | {
  state: 'error';
  message: string;
  toRetry?: OAuthStatus;
} | {
  state: 'about_to_retry';
  nextState: OAuthStatus;
};
const PASTE_HERE_MSG = 'Paste code here if prompted > ';
export function OAuthFlowStep({
  onSuccess,
  onCancel
}: OAuthFlowStepProps): React.ReactNode {
  const [oauthStatus, setOAuthStatus] = useState<OAuthStatus>({
    state: 'starting'
  });
  const [oauthService] = useState(() => new OAuthService());
  const [pastedCode, setPastedCode] = useState('');
  const [cursorOffset, setCursorOffset] = useState(0);
  const [showPastePrompt, setShowPastePrompt] = useState(false);
  const [urlCopied, setUrlCopied] = useState(false);
  const timersRef = useRef<Set<NodeJS.Timeout>>(new Set());
  // Separate ref so startOAuth's timer clear doesn't cancel the urlCopied reset
  const urlCopiedTimerRef = useRef<NodeJS.Timeout | undefined>(undefined);

```

---


### `src/commands/install-github-app/SuccessStep.tsx`

**信息:**
- 行数: 96
- 大小: 10170 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../../ink.js';
type SuccessStepProps = {
  secretExists: boolean;
  useExistingSecret: boolean;
  secretName: string;
  skipWorkflow?: boolean;
};
export function SuccessStep(t0) {
  const $ = _c(21);
  const {
    secretExists,
    useExistingSecret,
    secretName,
    skipWorkflow: t1
  } = t0;
  const skipWorkflow = t1 === undefined ? false : t1;
  let t2;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Box flexDirection="column" marginBottom={1}><Text bold={true}>Install GitHub App</Text><Text dimColor={true}>Success</Text></Box>;
    $[0] = t2;
  } else {
    t2 = $[0];
  }
  let t3;
  if ($[1] !== skipWorkflow) {
    t3 = !skipWorkflow && <Text color="success">✓ GitHub Actions workflow created!</Text>;
    $[1] = skipWorkflow;
    $[2] = t3;
  } else {
    t3 = $[2];
  }
  let t4;
  if ($[3] !== secretExists || $[4] !== useExistingSecret) {
    t4 = secretExists && useExistingSecret && <Box marginTop={1}><Text color="success">✓ Using existing ANTHROPIC_API_KEY secret</Text></Box>;
    $[3] = secretExists;
    $[4] = useExistingSecret;
    $[5] = t4;
  } else {
    t4 = $[5];
  }
  let t5;
  if ($[6] !== secretExists || $[7] !== secretName || $[8] !== useExistingSecret) {
    t5 = (!secretExists || !useExistingSecret) && <Box marginTop={1}><Text color="success">✓ API key saved as {secretName} secret</Text></Box>;
    $[6] = secretExists;
    $[7] = secretName;
    $[8] = useExistingSecret;
    $[9] = t5;
  } else {

```

---


### `src/commands/install-github-app/WarningsStep.tsx`

**信息:**
- 行数: 73
- 大小: 9132 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React from 'react';
import { GITHUB_ACTION_SETUP_DOCS_URL } from '../../constants/github-app.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import type { Warning } from './types.js';
interface WarningsStepProps {
  warnings: Warning[];
  onContinue: () => void;
}
export function WarningsStep(t0) {
  const $ = _c(8);
  const {
    warnings,
    onContinue
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = {
      context: "Confirmation"
    };
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  useKeybinding("confirm:yes", onContinue, t1);
  let t2;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Box flexDirection="column" marginBottom={1}><Text bold={true}>{figures.warning} Setup Warnings</Text><Text dimColor={true}>We found some potential issues, but you can continue anyway</Text></Box>;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  let t3;
  if ($[2] !== warnings) {
    t3 = warnings.map(_temp2);
    $[2] = warnings;
    $[3] = t3;
  } else {
    t3 = $[3];
  }
  let t4;
  if ($[4] === Symbol.for("react.memo_cache_sentinel")) {
    t4 = <Box marginTop={1}><Text bold={true} color="permission">Press Enter to continue anyway, or Ctrl+C to exit and fix issues</Text></Box>;
    $[4] = t4;
  } else {
    t4 = $[4];
  }
  let t5;

```

---


### `src/commands/install-github-app/index.ts`

**信息:**
- 行数: 13
- 大小: 471 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { isEnvTruthy } from '../../utils/envUtils.js'

const installGitHubApp = {
  type: 'local-jsx',
  name: 'install-github-app',
  description: 'Set up Claude GitHub Actions for a repository',
  availability: ['claude-ai', 'console'],
  isEnabled: () => !isEnvTruthy(process.env.DISABLE_INSTALL_GITHUB_APP_COMMAND),
  load: () => import('./install-github-app.js'),
} satisfies Command

export default installGitHubApp

```

---


### `src/commands/install-github-app/install-github-app.tsx`

**信息:**
- 行数: 587
- 大小: 87155 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { execa } from 'execa';
import React, { useCallback, useState } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { WorkflowMultiselectDialog } from '../../components/WorkflowMultiselectDialog.js';
import { GITHUB_ACTION_SETUP_DOCS_URL } from '../../constants/github-app.js';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box } from '../../ink.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { getAnthropicApiKey, isAnthropicAuthEnabled } from '../../utils/auth.js';
import { openBrowser } from '../../utils/browser.js';
import { execFileNoThrow } from '../../utils/execFileNoThrow.js';
import { getGithubRepo } from '../../utils/git.js';
import { plural } from '../../utils/stringUtils.js';
import { ApiKeyStep } from './ApiKeyStep.js';
import { CheckExistingSecretStep } from './CheckExistingSecretStep.js';
import { CheckGitHubStep } from './CheckGitHubStep.js';
import { ChooseRepoStep } from './ChooseRepoStep.js';
import { CreatingStep } from './CreatingStep.js';
import { ErrorStep } from './ErrorStep.js';
import { ExistingWorkflowStep } from './ExistingWorkflowStep.js';
import { InstallAppStep } from './InstallAppStep.js';
import { OAuthFlowStep } from './OAuthFlowStep.js';
import { SuccessStep } from './SuccessStep.js';
import { setupGitHubActions } from './setupGitHubActions.js';
import type { State, Warning, Workflow } from './types.js';
import { WarningsStep } from './WarningsStep.js';
const INITIAL_STATE: State = {
  step: 'check-gh',
  selectedRepoName: '',
  currentRepo: '',
  useCurrentRepo: false,
  // Default to false, will be set to true if repo detected
  apiKeyOrOAuthToken: '',
  useExistingKey: true,
  currentWorkflowInstallStep: 0,
  warnings: [],
  secretExists: false,
  secretName: 'ANTHROPIC_API_KEY',
  useExistingSecret: true,
  workflowExists: false,
  selectedWorkflows: ['claude', 'claude-review'] as Workflow[],
  selectedApiKeyOption: 'new' as 'existing' | 'new' | 'oauth',
  authType: 'api_key'
};
function InstallGitHubApp(props: {
  onDone: (message: string) => void;
}): React.ReactNode {
  const [existingApiKey] = useState(() => getAnthropicApiKey());
  const [state, setState] = useState({

```

---


### `src/commands/install-github-app/setupGitHubActions.ts`

**信息:**
- 行数: 325
- 大小: 10168 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from 'src/services/analytics/index.js'
import { saveGlobalConfig } from 'src/utils/config.js'
import {
  CODE_REVIEW_PLUGIN_WORKFLOW_CONTENT,
  PR_BODY,
  PR_TITLE,
  WORKFLOW_CONTENT,
} from '../../constants/github-app.js'
import { openBrowser } from '../../utils/browser.js'
import { execFileNoThrow } from '../../utils/execFileNoThrow.js'
import { logError } from '../../utils/log.js'
import type { Workflow } from './types.js'

async function createWorkflowFile(
  repoName: string,
  branchName: string,
  workflowPath: string,
  workflowContent: string,
  secretName: string,
  message: string,
  context?: {
    useCurrentRepo?: boolean
    workflowExists?: boolean
    secretExists?: boolean
  },
): Promise<void> {
  // Check if workflow file already exists
  const checkFileResult = await execFileNoThrow('gh', [
    'api',
    `repos/${repoName}/contents/${workflowPath}`,
    '--jq',
    '.sha',
  ])

  let fileSha: string | null = null
  if (checkFileResult.code === 0) {
    fileSha = checkFileResult.stdout.trim()
  }

  let content = workflowContent
  if (secretName === 'CLAUDE_CODE_OAUTH_TOKEN') {
    // For OAuth tokens, use the claude_code_oauth_token parameter
    content = workflowContent.replace(
      /anthropic_api_key: \$\{\{ secrets\.ANTHROPIC_API_KEY \}\}/g,
      `claude_code_oauth_token: \${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}`,
    )
  } else if (secretName !== 'ANTHROPIC_API_KEY') {

```

---


### `src/commands/install-github-app/types.ts`

**信息:**
- 行数: 3
- 大小: 137 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type Workflow = Record<string, unknown>
export type Warning = Record<string, unknown>
export type State = Record<string, unknown>

```

---


### `src/commands/install-slack-app/index.ts`

**信息:**
- 行数: 12
- 大小: 333 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const installSlackApp = {
  type: 'local',
  name: 'install-slack-app',
  description: 'Install the Claude Slack app',
  availability: ['claude-ai'],
  supportsNonInteractive: false,
  load: () => import('./install-slack-app.js'),
} satisfies Command

export default installSlackApp

```

---


### `src/commands/install-slack-app/install-slack-app.ts`

**信息:**
- 行数: 30
- 大小: 877 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { LocalCommandResult } from '../../commands.js'
import { logEvent } from '../../services/analytics/index.js'
import { openBrowser } from '../../utils/browser.js'
import { saveGlobalConfig } from '../../utils/config.js'

const SLACK_APP_URL = 'https://slack.com/marketplace/A08SF47R6P4-claude'

export async function call(): Promise<LocalCommandResult> {
  logEvent('tengu_install_slack_app_clicked', {})

  // Track that user has clicked to install
  saveGlobalConfig(current => ({
    ...current,
    slackAppInstallCount: (current.slackAppInstallCount ?? 0) + 1,
  }))

  const success = await openBrowser(SLACK_APP_URL)

  if (success) {
    return {
      type: 'text',
      value: 'Opening Slack app installation page in browser…',
    }
  } else {
    return {
      type: 'text',
      value: `Couldn't open browser. Visit: ${SLACK_APP_URL}`,
    }
  }
}

```

---


### `src/commands/install.tsx`

**信息:**
- 行数: 300
- 大小: 39068 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { homedir } from 'node:os';
import { join } from 'node:path';
import React, { useEffect, useState } from 'react';
import type { CommandResultDisplay } from 'src/commands.js';
import { logEvent } from 'src/services/analytics/index.js';
import { StatusIcon } from '../components/design-system/StatusIcon.js';
import { Box, render, Text } from '../ink.js';
import { logForDebugging } from '../utils/debug.js';
import { env } from '../utils/env.js';
import { errorMessage } from '../utils/errors.js';
import { checkInstall, cleanupNpmInstallations, cleanupShellAliases, installLatest } from '../utils/nativeInstaller/index.js';
import { getInitialSettings, updateSettingsForSource } from '../utils/settings/settings.js';
interface InstallProps {
  onDone: (result: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  force?: boolean;
  target?: string; // 'latest', 'stable', or version like '1.0.34'
}
type InstallState = {
  type: 'checking';
} | {
  type: 'cleaning-npm';
} | {
  type: 'installing';
  version: string;
} | {
  type: 'setting-up';
} | {
  type: 'set-up';
  messages: string[];
} | {
  type: 'success';
  version: string;
  setupMessages?: string[];
} | {
  type: 'error';
  message: string;
  warnings?: string[];
};
function getInstallationPath(): string {
  const isWindows = env.platform === 'win32';
  const homeDir = homedir();
  if (isWindows) {
    // Convert to Windows-style path
    const windowsPath = join(homeDir, '.local', 'bin', 'claude.exe');
    // Replace forward slashes with backslashes for Windows display
    return windowsPath.replace(/\//g, '\\');
  }

```

---


### `src/commands/keybindings/index.ts`

**信息:**
- 行数: 13
- 大小: 448 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { isKeybindingCustomizationEnabled } from '../../keybindings/loadUserBindings.js'

const keybindings = {
  name: 'keybindings',
  description: 'Open or create your keybindings configuration file',
  isEnabled: () => isKeybindingCustomizationEnabled(),
  supportsNonInteractive: false,
  type: 'local',
  load: () => import('./keybindings.js'),
} satisfies Command

export default keybindings

```

---


### `src/commands/keybindings/keybindings.ts`

**信息:**
- 行数: 53
- 大小: 1645 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { mkdir, writeFile } from 'fs/promises'
import { dirname } from 'path'
import {
  getKeybindingsPath,
  isKeybindingCustomizationEnabled,
} from '../../keybindings/loadUserBindings.js'
import { generateKeybindingsTemplate } from '../../keybindings/template.js'
import { getErrnoCode } from '../../utils/errors.js'
import { editFileInEditor } from '../../utils/promptEditor.js'

export async function call(): Promise<{ type: 'text'; value: string }> {
  if (!isKeybindingCustomizationEnabled()) {
    return {
      type: 'text',
      value:
        'Keybinding customization is not enabled. This feature is currently in preview.',
    }
  }

  const keybindingsPath = getKeybindingsPath()

  // Write template with 'wx' flag (exclusive create) — fails with EEXIST if
  // the file already exists. Avoids a stat pre-check (TOCTOU race + extra syscall).
  let fileExists = false
  await mkdir(dirname(keybindingsPath), { recursive: true })
  try {
    await writeFile(keybindingsPath, generateKeybindingsTemplate(), {
      encoding: 'utf-8',
      flag: 'wx',
    })
  } catch (e: unknown) {
    if (getErrnoCode(e) === 'EEXIST') {
      fileExists = true
    } else {
      throw e
    }
  }

  // Open in editor
  const result = await editFileInEditor(keybindingsPath)
  if (result.error) {
    return {
      type: 'text',
      value: `${fileExists ? 'Opened' : 'Created'} ${keybindingsPath}. Could not open in editor: ${result.error}`,
    }
  }
  return {
    type: 'text',
    value: fileExists
      ? `Opened ${keybindingsPath} in your editor.`

```

---


### `src/commands/login/index.ts`

**信息:**
- 行数: 14
- 大小: 489 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { hasAnthropicApiKeyAuth } from '../../utils/auth.js'
import { isEnvTruthy } from '../../utils/envUtils.js'

export default () =>
  ({
    type: 'local-jsx',
    name: 'login',
    description: hasAnthropicApiKeyAuth()
      ? 'Switch Anthropic accounts'
      : 'Sign in with your Anthropic account',
    isEnabled: () => !isEnvTruthy(process.env.DISABLE_LOGIN_COMMAND),
    load: () => import('./login.js'),
  }) satisfies Command

```

---


### `src/commands/login/login.tsx`

**信息:**
- 行数: 104
- 大小: 16109 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import * as React from 'react';
import { resetCostState } from '../../bootstrap/state.js';
import { clearTrustedDeviceToken, enrollTrustedDevice } from '../../bridge/trustedDevice.js';
import type { LocalJSXCommandContext } from '../../commands.js';
import { ConfigurableShortcutHint } from '../../components/ConfigurableShortcutHint.js';
import { ConsoleOAuthFlow } from '../../components/ConsoleOAuthFlow.js';
import { Dialog } from '../../components/design-system/Dialog.js';
import { useMainLoopModel } from '../../hooks/useMainLoopModel.js';
import { Text } from '../../ink.js';
import { refreshGrowthBookAfterAuthChange } from '../../services/analytics/growthbook.js';
import { refreshPolicyLimits } from '../../services/policyLimits/index.js';
import { refreshRemoteManagedSettings } from '../../services/remoteManagedSettings/index.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { stripSignatureBlocks } from '../../utils/messages.js';
import { checkAndDisableAutoModeIfNeeded, checkAndDisableBypassPermissionsIfNeeded, resetAutoModeGateCheck, resetBypassPermissionsCheck } from '../../utils/permissions/bypassPermissionsKillswitch.js';
import { resetUserCache } from '../../utils/user.js';
export async function call(onDone: LocalJSXCommandOnDone, context: LocalJSXCommandContext): Promise<React.ReactNode> {
  return <Login onDone={async success => {
    context.onChangeAPIKey();
    // Signature-bearing blocks (thinking, connector_text) are bound to the API key —
    // strip them so the new key doesn't reject stale signatures.
    context.setMessages(stripSignatureBlocks);
    if (success) {
      // Post-login refresh logic. Keep in sync with onboarding in src/interactiveHelpers.tsx
      // Reset cost state when switching accounts
      resetCostState();
      // Refresh remotely managed settings after login (non-blocking)
      void refreshRemoteManagedSettings();
      // Refresh policy limits after login (non-blocking)
      void refreshPolicyLimits();
      // Clear user data cache BEFORE GrowthBook refresh so it picks up fresh credentials
      resetUserCache();
      // Refresh GrowthBook after login to get updated feature flags (e.g., for claude.ai MCPs)
      refreshGrowthBookAfterAuthChange();
      // Clear any stale trusted device token from a previous account before
      // re-enrolling — prevents sending the old token on bridge calls while
      // the async enrollTrustedDevice() is in-flight.
      clearTrustedDeviceToken();
      // Enroll as a trusted device for Remote Control (10-min fresh-session window)
      void enrollTrustedDevice();
      // Reset killswitch gate checks and re-run with new org
      resetBypassPermissionsCheck();
      const appState = context.getAppState();
      void checkAndDisableBypassPermissionsIfNeeded(appState.toolPermissionContext, context.setAppState);
      if (feature('TRANSCRIPT_CLASSIFIER')) {
        resetAutoModeGateCheck();
        void checkAndDisableAutoModeIfNeeded(appState.toolPermissionContext, context.setAppState, appState.fastMode);
      }

```

---


### `src/commands/logout/index.ts`

**信息:**
- 行数: 10
- 大小: 341 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { isEnvTruthy } from '../../utils/envUtils.js'

export default {
  type: 'local-jsx',
  name: 'logout',
  description: 'Sign out from your Anthropic account',
  isEnabled: () => !isEnvTruthy(process.env.DISABLE_LOGOUT_COMMAND),
  load: () => import('./logout.js'),
} satisfies Command

```

---


### `src/commands/logout/logout.tsx`

**信息:**
- 行数: 82
- 大小: 10732 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { clearTrustedDeviceTokenCache } from '../../bridge/trustedDevice.js';
import { Text } from '../../ink.js';
import { refreshGrowthBookAfterAuthChange } from '../../services/analytics/growthbook.js';
import { getGroveNoticeConfig, getGroveSettings } from '../../services/api/grove.js';
import { clearPolicyLimitsCache } from '../../services/policyLimits/index.js';
// flushTelemetry is loaded lazily to avoid pulling in ~1.1MB of OpenTelemetry at startup
import { clearRemoteManagedSettingsCache } from '../../services/remoteManagedSettings/index.js';
import { getClaudeAIOAuthTokens, removeApiKey } from '../../utils/auth.js';
import { clearBetasCaches } from '../../utils/betas.js';
import { saveGlobalConfig } from '../../utils/config.js';
import { gracefulShutdownSync } from '../../utils/gracefulShutdown.js';
import { getSecureStorage } from '../../utils/secureStorage/index.js';
import { clearToolSchemaCache } from '../../utils/toolSchemaCache.js';
import { resetUserCache } from '../../utils/user.js';
export async function performLogout({
  clearOnboarding = false
}): Promise<void> {
  // Flush telemetry BEFORE clearing credentials to prevent org data leakage
  const {
    flushTelemetry
  } = await import('../../utils/telemetry/instrumentation.js');
  await flushTelemetry();
  await removeApiKey();

  // Wipe all secure storage data on logout
  const secureStorage = getSecureStorage();
  secureStorage.delete();
  await clearAuthRelatedCaches();
  saveGlobalConfig(current => {
    const updated = {
      ...current
    };
    if (clearOnboarding) {
      updated.hasCompletedOnboarding = false;
      updated.subscriptionNoticeCount = 0;
      updated.hasAvailableSubscription = false;
      if (updated.customApiKeyResponses?.approved) {
        updated.customApiKeyResponses = {
          ...updated.customApiKeyResponses,
          approved: []
        };
      }
    }
    updated.oauthAccount = undefined;
    return updated;
  });
}

// clearing anything memoized that must be invalidated when user/session/auth changes

```

---


### `src/commands/mcp/addCommand.ts`

**信息:**
- 行数: 280
- 大小: 9848 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * MCP add CLI subcommand
 *
 * Extracted from main.tsx to enable direct testing.
 */
import { type Command, Option } from '@commander-js/extra-typings'
import { cliError, cliOk } from '../../cli/exit.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import {
  readClientSecret,
  saveMcpClientSecret,
} from '../../services/mcp/auth.js'
import { addMcpConfig } from '../../services/mcp/config.js'
import {
  describeMcpConfigFilePath,
  ensureConfigScope,
  ensureTransport,
  parseHeaders,
} from '../../services/mcp/utils.js'
import {
  getXaaIdpSettings,
  isXaaEnabled,
} from '../../services/mcp/xaaIdpLogin.js'
import { parseEnvVars } from '../../utils/envUtils.js'
import { jsonStringify } from '../../utils/slowOperations.js'

/**
 * Registers the `mcp add` subcommand on the given Commander command.
 */
export function registerMcpAddCommand(mcp: Command): void {
  mcp
    .command('add <name> <commandOrUrl> [args...]')
    .description(
      'Add an MCP server to Claude Code.\n\n' +
        'Examples:\n' +
        '  # Add HTTP server:\n' +
        '  claude mcp add --transport http sentry https://mcp.sentry.dev/mcp\n\n' +
        '  # Add HTTP server with headers:\n' +
        '  claude mcp add --transport http corridor https://app.corridor.dev/api/mcp --header "Authorization: Bearer ..."\n\n' +
        '  # Add stdio server with environment variables:\n' +
        '  claude mcp add -e API_KEY=xxx my-server -- npx my-mcp-server\n\n' +
        '  # Add stdio server with subprocess flags:\n' +
        '  claude mcp add my-server -- my-command --some-flag arg1',
    )
    .option(
      '-s, --scope <scope>',
      'Configuration scope (local, user, or project)',

```

---


### `src/commands/mcp/index.ts`

**信息:**
- 行数: 12
- 大小: 280 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const mcp = {
  type: 'local-jsx',
  name: 'mcp',
  description: 'Manage MCP servers',
  immediate: true,
  argumentHint: '[enable|disable [server-name]]',
  load: () => import('./mcp.js'),
} satisfies Command

export default mcp

```

---


### `src/commands/mcp/mcp.tsx`

**信息:**
- 行数: 85
- 大小: 12126 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useEffect, useRef } from 'react';
import { MCPSettings } from '../../components/mcp/index.js';
import { MCPReconnect } from '../../components/mcp/MCPReconnect.js';
import { useMcpToggleEnabled } from '../../services/mcp/MCPConnectionManager.js';
import { useAppState } from '../../state/AppState.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { PluginSettings } from '../plugin/PluginSettings.js';

// TODO: This is a hack to get the context value from toggleMcpServer (useContext only works in a component)
// Ideally, all MCP state and functions would be in global state.
function MCPToggle(t0) {
  const $ = _c(7);
  const {
    action,
    target,
    onComplete
  } = t0;
  const mcpClients = useAppState(_temp);
  const toggleMcpServer = useMcpToggleEnabled();
  const didRun = useRef(false);
  let t1;
  let t2;
  if ($[0] !== action || $[1] !== mcpClients || $[2] !== onComplete || $[3] !== target || $[4] !== toggleMcpServer) {
    t1 = () => {
      if (didRun.current) {
        return;
      }
      didRun.current = true;
      const isEnabling = action === "enable";
      const clients = mcpClients.filter(_temp2);
      const toToggle = target === "all" ? clients.filter(c_0 => isEnabling ? c_0.type === "disabled" : c_0.type !== "disabled") : clients.filter(c_1 => c_1.name === target);
      if (toToggle.length === 0) {
        onComplete(target === "all" ? `All MCP servers are already ${isEnabling ? "enabled" : "disabled"}` : `MCP server "${target}" not found`);
        return;
      }
      for (const s_0 of toToggle) {
        toggleMcpServer(s_0.name);
      }
      onComplete(target === "all" ? `${isEnabling ? "Enabled" : "Disabled"} ${toToggle.length} MCP server(s)` : `MCP server "${target}" ${isEnabling ? "enabled" : "disabled"}`);
    };
    t2 = [action, target, mcpClients, toggleMcpServer, onComplete];
    $[0] = action;
    $[1] = mcpClients;
    $[2] = onComplete;
    $[3] = target;
    $[4] = toggleMcpServer;
    $[5] = t1;
    $[6] = t2;
  } else {

```

---


### `src/commands/mcp/xaaIdpCommand.ts`

**信息:**
- 行数: 266
- 大小: 10290 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * `claude mcp xaa` — manage the XAA (SEP-990) IdP connection.
 *
 * The IdP connection is user-level: configure once, all XAA-enabled MCP
 * servers reuse it. Lives in settings.xaaIdp (non-secret) + a keychain slot
 * keyed by issuer (secret). Separate trust domain from per-server AS secrets.
 */
import type { Command } from '@commander-js/extra-typings'
import { cliError, cliOk } from '../../cli/exit.js'
import {
  acquireIdpIdToken,
  clearIdpClientSecret,
  clearIdpIdToken,
  getCachedIdpIdToken,
  getIdpClientSecret,
  getXaaIdpSettings,
  issuerKey,
  saveIdpClientSecret,
  saveIdpIdTokenFromJwt,
} from '../../services/mcp/xaaIdpLogin.js'
import { errorMessage } from '../../utils/errors.js'
import { updateSettingsForSource } from '../../utils/settings/settings.js'

export function registerMcpXaaIdpCommand(mcp: Command): void {
  const xaaIdp = mcp
    .command('xaa')
    .description('Manage the XAA (SEP-990) IdP connection')

  xaaIdp
    .command('setup')
    .description(
      'Configure the IdP connection (one-time setup for all XAA-enabled servers)',
    )
    .requiredOption('--issuer <url>', 'IdP issuer URL (OIDC discovery)')
    .requiredOption('--client-id <id>', "Claude Code's client_id at the IdP")
    .option(
      '--client-secret',
      'Read IdP client secret from MCP_XAA_IDP_CLIENT_SECRET env var',
    )
    .option(
      '--callback-port <port>',
      'Fixed loopback callback port (only if IdP does not honor RFC 8252 port-any matching)',
    )
    .action(options => {
      // Validate everything BEFORE any writes. An exit(1) mid-write leaves
      // settings configured but keychain missing — confusing state.
      // updateSettingsForSource doesn't schema-check on write; a non-URL
      // issuer lands on disk and then poisons the whole userSettings source
      // on next launch (SettingsSchema .url() fails → parseSettingsFile
      // returns { settings: null }, dropping everything, not just xaaIdp).

```

---


### `src/commands/memory/index.ts`

**信息:**
- 行数: 10
- 大小: 220 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const memory: Command = {
  type: 'local-jsx',
  name: 'memory',
  description: 'Edit Claude memory files',
  load: () => import('./memory.js'),
}

export default memory

```

---


### `src/commands/memory/memory.tsx`

**信息:**
- 行数: 90
- 大小: 12608 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { mkdir, writeFile } from 'fs/promises';
import * as React from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { Dialog } from '../../components/design-system/Dialog.js';
import { MemoryFileSelector } from '../../components/memory/MemoryFileSelector.js';
import { getRelativeMemoryPath } from '../../components/memory/MemoryUpdateNotification.js';
import { Box, Link, Text } from '../../ink.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
import { clearMemoryFileCaches, getMemoryFiles } from '../../utils/claudemd.js';
import { getClaudeConfigHomeDir } from '../../utils/envUtils.js';
import { getErrnoCode } from '../../utils/errors.js';
import { logError } from '../../utils/log.js';
import { editFileInEditor } from '../../utils/promptEditor.js';
function MemoryCommand({
  onDone
}: {
  onDone: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
}): React.ReactNode {
  const handleSelectMemoryFile = async (memoryPath: string) => {
    try {
      // Create claude directory if it doesn't exist (idempotent with recursive)
      if (memoryPath.includes(getClaudeConfigHomeDir())) {
        await mkdir(getClaudeConfigHomeDir(), {
          recursive: true
        });
      }

      // Create file if it doesn't exist (wx flag fails if file exists,
      // which we catch to preserve existing content)
      try {
        await writeFile(memoryPath, '', {
          encoding: 'utf8',
          flag: 'wx'
        });
      } catch (e: unknown) {
        if (getErrnoCode(e) !== 'EEXIST') {
          throw e;
        }
      }
      await editFileInEditor(memoryPath);

      // Determine which environment variable controls the editor
      let editorSource = 'default';
      let editorValue = '';
      if (process.env.VISUAL) {
        editorSource = '$VISUAL';
        editorValue = process.env.VISUAL;
      } else if (process.env.EDITOR) {

```

---


### `src/commands/mobile/index.ts`

**信息:**
- 行数: 11
- 大小: 282 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const mobile = {
  type: 'local-jsx',
  name: 'mobile',
  aliases: ['ios', 'android'],
  description: 'Show QR code to download the Claude mobile app',
  load: () => import('./mobile.js'),
} satisfies Command

export default mobile

```

---


### `src/commands/mobile/mobile.tsx`

**信息:**
- 行数: 274
- 大小: 21797 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { toString as qrToString } from 'qrcode';
import * as React from 'react';
import { useCallback, useEffect, useState } from 'react';
import { Pane } from '../../components/design-system/Pane.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
type Platform = 'ios' | 'android';
type Props = {
  onDone: () => void;
};
const PLATFORMS: Record<Platform, {
  url: string;
}> = {
  ios: {
    url: 'https://apps.apple.com/app/claude-by-anthropic/id6473753684'
  },
  android: {
    url: 'https://play.google.com/store/apps/details?id=com.anthropic.claude'
  }
};
function MobileQRCode(t0) {
  const $ = _c(52);
  const {
    onDone
  } = t0;
  const [platform, setPlatform] = useState("ios");
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = {
      ios: "",
      android: ""
    };
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const [qrCodes, setQrCodes] = useState(t1);
  const {
    url
  } = PLATFORMS[platform];
  const qrCode = qrCodes[platform];
  let t2;
  let t3;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = () => {
      const generateQRCodes = async function generateQRCodes() {
        const [ios, android] = await Promise.all([qrToString(PLATFORMS.ios.url, {

```

---


### `src/commands/model/index.ts`

**信息:**
- 行数: 16
- 大小: 559 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { shouldInferenceConfigCommandBeImmediate } from '../../utils/immediateCommand.js'
import { getMainLoopModel, renderModelName } from '../../utils/model/model.js'

export default {
  type: 'local-jsx',
  name: 'model',
  get description() {
    return `Set the AI model for Claude Code (currently ${renderModelName(getMainLoopModel())})`
  },
  argumentHint: '[model]',
  get immediate() {
    return shouldInferenceConfigCommandBeImmediate()
  },
  load: () => import('./model.js'),
} satisfies Command

```

---


### `src/commands/model/model.tsx`

**信息:**
- 行数: 297
- 大小: 37569 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import * as React from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { ModelPicker } from '../../components/ModelPicker.js';
import { COMMON_HELP_ARGS, COMMON_INFO_ARGS } from '../../constants/xml.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../services/analytics/index.js';
import { useAppState, useSetAppState } from '../../state/AppState.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
import type { EffortLevel } from '../../utils/effort.js';
import { isBilledAsExtraUsage } from '../../utils/extraUsage.js';
import { clearFastModeCooldown, isFastModeAvailable, isFastModeEnabled, isFastModeSupportedByModel } from '../../utils/fastMode.js';
import { MODEL_ALIASES } from '../../utils/model/aliases.js';
import { checkOpus1mAccess, checkSonnet1mAccess } from '../../utils/model/check1mAccess.js';
import { getDefaultMainLoopModelSetting, isOpus1mMergeEnabled, renderDefaultModelSetting } from '../../utils/model/model.js';
import { isModelAllowed } from '../../utils/model/modelAllowlist.js';
import { validateModel } from '../../utils/model/validateModel.js';
function ModelPickerWrapper(t0) {
  const $ = _c(17);
  const {
    onDone
  } = t0;
  const mainLoopModel = useAppState(_temp);
  const mainLoopModelForSession = useAppState(_temp2);
  const isFastMode = useAppState(_temp3);
  const setAppState = useSetAppState();
  let t1;
  if ($[0] !== mainLoopModel || $[1] !== onDone) {
    t1 = function handleCancel() {
      logEvent("tengu_model_command_menu", {
        action: "cancel" as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS
      });
      const displayModel = renderModelLabel(mainLoopModel);
      onDone(`Kept model as ${chalk.bold(displayModel)}`, {
        display: "system"
      });
    };
    $[0] = mainLoopModel;
    $[1] = onDone;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  const handleCancel = t1;
  let t2;
  if ($[3] !== isFastMode || $[4] !== mainLoopModel || $[5] !== onDone || $[6] !== setAppState) {
    t2 = function handleSelect(model, effort) {
      logEvent("tengu_model_command_menu", {
        action: model as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
        from_model: mainLoopModel as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,

```

---


### `src/commands/output-style/index.ts`

**信息:**
- 行数: 11
- 大小: 291 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const outputStyle = {
  type: 'local-jsx',
  name: 'output-style',
  description: 'Deprecated: use /config to change output style',
  isHidden: true,
  load: () => import('./output-style.js'),
} satisfies Command

export default outputStyle

```

---


### `src/commands/output-style/output-style.tsx`

**信息:**
- 行数: 7
- 大小: 1343 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { LocalJSXCommandOnDone } from '../../types/command.js';
export async function call(onDone: LocalJSXCommandOnDone): Promise<undefined> {
  onDone('/output-style has been deprecated. Use /config to change your output style, or set it in your settings file. Changes take effect on the next session.', {
    display: 'system'
  });
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJMb2NhbEpTWENvbW1hbmRPbkRvbmUiLCJjYWxsIiwib25Eb25lIiwiUHJvbWlzZSIsImRpc3BsYXkiXSwic291cmNlcyI6WyJvdXRwdXQtc3R5bGUudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB0eXBlIHsgTG9jYWxKU1hDb21tYW5kT25Eb25lIH0gZnJvbSAnLi4vLi4vdHlwZXMvY29tbWFuZC5qcydcblxuZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGNhbGwob25Eb25lOiBMb2NhbEpTWENvbW1hbmRPbkRvbmUpOiBQcm9taXNlPHVuZGVmaW5lZD4ge1xuICBvbkRvbmUoXG4gICAgJy9vdXRwdXQtc3R5bGUgaGFzIGJlZW4gZGVwcmVjYXRlZC4gVXNlIC9jb25maWcgdG8gY2hhbmdlIHlvdXIgb3V0cHV0IHN0eWxlLCBvciBzZXQgaXQgaW4geW91ciBzZXR0aW5ncyBmaWxlLiBDaGFuZ2VzIHRha2UgZWZmZWN0IG9uIHRoZSBuZXh0IHNlc3Npb24uJyxcbiAgICB7IGRpc3BsYXk6ICdzeXN0ZW0nIH0sXG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsY0FBY0EscUJBQXFCLFFBQVEsd0JBQXdCO0FBRW5FLE9BQU8sZUFBZUMsSUFBSUEsQ0FBQ0MsTUFBTSxFQUFFRixxQkFBcUIsQ0FBQyxFQUFFRyxPQUFPLENBQUMsU0FBUyxDQUFDLENBQUM7RUFDNUVELE1BQU0sQ0FDSix1SkFBdUosRUFDdko7SUFBRUUsT0FBTyxFQUFFO0VBQVMsQ0FDdEIsQ0FBQztBQUNIIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/passes/index.ts`

**信息:**
- 行数: 22
- 大小: 632 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import {
  checkCachedPassesEligibility,
  getCachedReferrerReward,
} from '../../services/api/referral.js'

export default {
  type: 'local-jsx',
  name: 'passes',
  get description() {
    const reward = getCachedReferrerReward()
    if (reward) {
      return 'Share a free week of Claude Code with friends and earn extra usage'
    }
    return 'Share a free week of Claude Code with friends'
  },
  get isHidden() {
    const { eligible, hasCache } = checkCachedPassesEligibility()
    return !eligible || !hasCache
  },
  load: () => import('./passes.js'),
} satisfies Command

```

---


### `src/commands/passes/passes.tsx`

**信息:**
- 行数: 24
- 大小: 3783 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { Passes } from '../../components/Passes/Passes.js';
import { logEvent } from '../../services/analytics/index.js';
import { getCachedRemainingPasses } from '../../services/api/referral.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
export async function call(onDone: LocalJSXCommandOnDone): Promise<React.ReactNode> {
  // Mark that user has visited /passes so we stop showing the upsell
  const config = getGlobalConfig();
  const isFirstVisit = !config.hasVisitedPasses;
  if (isFirstVisit) {
    const remaining = getCachedRemainingPasses();
    saveGlobalConfig(current => ({
      ...current,
      hasVisitedPasses: true,
      passesLastSeenRemaining: remaining ?? current.passesLastSeenRemaining
    }));
  }
  logEvent('tengu_guest_passes_visited', {
    is_first_visit: isFirstVisit
  });
  return <Passes onDone={onDone} />;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlBhc3NlcyIsImxvZ0V2ZW50IiwiZ2V0Q2FjaGVkUmVtYWluaW5nUGFzc2VzIiwiTG9jYWxKU1hDb21tYW5kT25Eb25lIiwiZ2V0R2xvYmFsQ29uZmlnIiwic2F2ZUdsb2JhbENvbmZpZyIsImNhbGwiLCJvbkRvbmUiLCJQcm9taXNlIiwiUmVhY3ROb2RlIiwiY29uZmlnIiwiaXNGaXJzdFZpc2l0IiwiaGFzVmlzaXRlZFBhc3NlcyIsInJlbWFpbmluZyIsImN1cnJlbnQiLCJwYXNzZXNMYXN0U2VlblJlbWFpbmluZyIsImlzX2ZpcnN0X3Zpc2l0Il0sInNvdXJjZXMiOlsicGFzc2VzLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IFBhc3NlcyB9IGZyb20gJy4uLy4uL2NvbXBvbmVudHMvUGFzc2VzL1Bhc3Nlcy5qcydcbmltcG9ydCB7IGxvZ0V2ZW50IH0gZnJvbSAnLi4vLi4vc2VydmljZXMvYW5hbHl0aWNzL2luZGV4LmpzJ1xuaW1wb3J0IHsgZ2V0Q2FjaGVkUmVtYWluaW5nUGFzc2VzIH0gZnJvbSAnLi4vLi4vc2VydmljZXMvYXBpL3JlZmVycmFsLmpzJ1xuaW1wb3J0IHR5cGUgeyBMb2NhbEpTWENvbW1hbmRPbkRvbmUgfSBmcm9tICcuLi8uLi90eXBlcy9jb21tYW5kLmpzJ1xuaW1wb3J0IHsgZ2V0R2xvYmFsQ29uZmlnLCBzYXZlR2xvYmFsQ29uZmlnIH0gZnJvbSAnLi4vLi4vdXRpbHMvY29uZmlnLmpzJ1xuXG5leHBvcnQgYXN5bmMgZnVuY3Rpb24gY2FsbChcbiAgb25Eb25lOiBMb2NhbEpTWENvbW1hbmRPbkRvbmUsXG4pOiBQcm9taXNlPFJlYWN0LlJlYWN0Tm9kZT4ge1xuICAvLyBNYXJrIHRoYXQgdXNlciBoYXMgdmlzaXRlZCAvcGFzc2VzIHNvIHdlIHN0b3Agc2hvd2luZyB0aGUgdXBzZWxsXG4gIGNvbnN0IGNvbmZpZyA9IGdldEdsb2JhbENvbmZpZygpXG4gIGNvbnN0IGlzRmlyc3RWaXNpdCA9ICFjb25maWcuaGFzVmlzaXRlZFBhc3Nlc1xuICBpZiAoaXNGaXJzdFZpc2l0KSB7XG4gICAgY29uc3QgcmVtYWluaW5nID0gZ2V0Q2FjaGVkUmVtYWluaW5nUGFzc2VzKClcbiAgICBzYXZlR2xvYmFsQ29uZmlnKGN1cnJlbnQgPT4gKHtcbiAgICAgIC4uLmN1cnJlbnQsXG4gICAgICBoYXNWaXNpdGVkUGFzc2VzOiB0cnVlLFxuICAgICAgcGFzc2VzTGFzdFNlZW5SZW1haW5pbmc6IHJlbWFpbmluZyA/PyBjdXJyZW50LnBhc3Nlc0xhc3RTZWVuUmVtYWluaW5nLFxuICAgIH0pKVxuICB9XG4gIGxvZ0V2ZW50KCd0ZW5ndV9ndWVzdF9wYXNzZXNfdmlzaXRlZCcsIHsgaXNfZmlyc3RfdmlzaXQ6IGlzRmlyc3RWaXNpdCB9KVxuICByZXR1cm4gPFBhc3NlcyBvbkRvbmU9e29uRG9uZX0gLz5cbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixTQUFTQyxNQUFNLFFBQVEsbUNBQW1DO0FBQzFELFNBQVNDLFFBQVEsUUFBUSxtQ0FBbUM7QUFDNUQsU0FBU0Msd0JBQXdCLFFBQVEsZ0NBQWdDO0FBQ3pFLGNBQWNDLHFCQUFxQixRQUFRLHdCQUF3QjtBQUNuRSxTQUFTQyxlQUFlLEVBQUVDLGdCQUFnQixRQUFRLHVCQUF1QjtBQUV6RSxPQUFPLGVBQWVDLElBQUlBLENBQ3hCQyxNQUFNLEVBQUVKLHFCQUFxQixDQUM5QixFQUFFSyxPQUFPLENBQUNULEtBQUssQ0FBQ1UsU0FBUyxDQUFDLENBQUM7RUFDMUI7RUFDQSxNQUFNQyxNQUFNLEdBQUdOLGVBQWUsQ0FBQyxDQUFDO0VBQ2hDLE1BQU1PLFlBQVksR0FBRyxDQUFDRCxNQUFNLENBQUNFLGdCQUFnQjtFQUM3QyxJQUFJRCxZQUFZLEVBQUU7SUFDaEIsTUFBTUUsU0FBUyxHQUFHWCx3QkFBd0IsQ0FBQyxDQUFDO0lBQzVDRyxnQkFBZ0IsQ0FBQ1MsT0FBTyxLQUFLO01BQzNCLEdBQUdBLE9BQU87TUFDVkYsZ0JBQWdCLEVBQUUsSUFBSTtNQUN0QkcsdUJBQXVCLEVBQUVGLFNBQVMsSUFBSUMsT0FBTyxDQUFDQztJQUNoRCxDQUFDLENBQUMsQ0FBQztFQUNMO0VBQ0FkLFFBQVEsQ0FBQyw0QkFBNEIsRUFBRTtJQUFFZSxjQUFjLEVBQUVMO0VBQWEsQ0FBQyxDQUFDO0VBQ3hFLE9BQU8sQ0FBQyxNQUFNLENBQUMsTUFBTSxDQUFDLENBQUNKLE1BQU0sQ0FBQyxHQUFHO0FBQ25DIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/permissions/index.ts`

**信息:**
- 行数: 11
- 大小: 296 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const permissions = {
  type: 'local-jsx',
  name: 'permissions',
  aliases: ['allowed-tools'],
  description: 'Manage allow & deny tool permission rules',
  load: () => import('./permissions.js'),
} satisfies Command

export default permissions

```

---


### `src/commands/permissions/permissions.tsx`

**信息:**
- 行数: 10
- 大小: 2223 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { PermissionRuleList } from '../../components/permissions/rules/PermissionRuleList.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
import { createPermissionRetryMessage } from '../../utils/messages.js';
export const call: LocalJSXCommandCall = async (onDone, context) => {
  return <PermissionRuleList onExit={onDone} onRetryDenials={commands => {
    context.setMessages(prev => [...prev, createPermissionRetryMessage(commands)]);
  }} />;
};
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlBlcm1pc3Npb25SdWxlTGlzdCIsIkxvY2FsSlNYQ29tbWFuZENhbGwiLCJjcmVhdGVQZXJtaXNzaW9uUmV0cnlNZXNzYWdlIiwiY2FsbCIsIm9uRG9uZSIsImNvbnRleHQiLCJjb21tYW5kcyIsInNldE1lc3NhZ2VzIiwicHJldiJdLCJzb3VyY2VzIjpbInBlcm1pc3Npb25zLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IFBlcm1pc3Npb25SdWxlTGlzdCB9IGZyb20gJy4uLy4uL2NvbXBvbmVudHMvcGVybWlzc2lvbnMvcnVsZXMvUGVybWlzc2lvblJ1bGVMaXN0LmpzJ1xuaW1wb3J0IHR5cGUgeyBMb2NhbEpTWENvbW1hbmRDYWxsIH0gZnJvbSAnLi4vLi4vdHlwZXMvY29tbWFuZC5qcydcbmltcG9ydCB7IGNyZWF0ZVBlcm1pc3Npb25SZXRyeU1lc3NhZ2UgfSBmcm9tICcuLi8uLi91dGlscy9tZXNzYWdlcy5qcydcblxuZXhwb3J0IGNvbnN0IGNhbGw6IExvY2FsSlNYQ29tbWFuZENhbGwgPSBhc3luYyAob25Eb25lLCBjb250ZXh0KSA9PiB7XG4gIHJldHVybiAoXG4gICAgPFBlcm1pc3Npb25SdWxlTGlzdFxuICAgICAgb25FeGl0PXtvbkRvbmV9XG4gICAgICBvblJldHJ5RGVuaWFscz17Y29tbWFuZHMgPT4ge1xuICAgICAgICBjb250ZXh0LnNldE1lc3NhZ2VzKHByZXYgPT4gW1xuICAgICAgICAgIC4uLnByZXYsXG4gICAgICAgICAgY3JlYXRlUGVybWlzc2lvblJldHJ5TWVzc2FnZShjb21tYW5kcyksXG4gICAgICAgIF0pXG4gICAgICB9fVxuICAgIC8+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixTQUFTQyxrQkFBa0IsUUFBUSwwREFBMEQ7QUFDN0YsY0FBY0MsbUJBQW1CLFFBQVEsd0JBQXdCO0FBQ2pFLFNBQVNDLDRCQUE0QixRQUFRLHlCQUF5QjtBQUV0RSxPQUFPLE1BQU1DLElBQUksRUFBRUYsbUJBQW1CLEdBQUcsTUFBQUUsQ0FBT0MsTUFBTSxFQUFFQyxPQUFPLEtBQUs7RUFDbEUsT0FDRSxDQUFDLGtCQUFrQixDQUNqQixNQUFNLENBQUMsQ0FBQ0QsTUFBTSxDQUFDLENBQ2YsY0FBYyxDQUFDLENBQUNFLFFBQVEsSUFBSTtJQUMxQkQsT0FBTyxDQUFDRSxXQUFXLENBQUNDLElBQUksSUFBSSxDQUMxQixHQUFHQSxJQUFJLEVBQ1BOLDRCQUE0QixDQUFDSSxRQUFRLENBQUMsQ0FDdkMsQ0FBQztFQUNKLENBQUMsQ0FBQyxHQUNGO0FBRU4sQ0FBQyIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/commands/plan/index.ts`

**信息:**
- 行数: 11
- 大小: 286 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const plan = {
  type: 'local-jsx',
  name: 'plan',
  description: 'Enable plan mode or view the current session plan',
  argumentHint: '[open|<description>]',
  load: () => import('./plan.js'),
} satisfies Command

export default plan

```

---


### `src/commands/plan/plan.tsx`

**信息:**
- 行数: 122
- 大小: 13904 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { handlePlanModeTransition } from '../../bootstrap/state.js';
import type { LocalJSXCommandContext } from '../../commands.js';
import { Box, Text } from '../../ink.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { getExternalEditor } from '../../utils/editor.js';
import { toIDEDisplayName } from '../../utils/ide.js';
import { applyPermissionUpdate } from '../../utils/permissions/PermissionUpdate.js';
import { prepareContextForPlanMode } from '../../utils/permissions/permissionSetup.js';
import { getPlan, getPlanFilePath } from '../../utils/plans.js';
import { editFileInEditor } from '../../utils/promptEditor.js';
import { renderToString } from '../../utils/staticRender.js';
function PlanDisplay(t0) {
  const $ = _c(11);
  const {
    planContent,
    planPath,
    editorName
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Text bold={true}>Current Plan</Text>;
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  let t2;
  if ($[1] !== planPath) {
    t2 = <Text dimColor={true}>{planPath}</Text>;
    $[1] = planPath;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  let t3;
  if ($[3] !== planContent) {
    t3 = <Box marginTop={1}><Text>{planContent}</Text></Box>;
    $[3] = planContent;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  let t4;
  if ($[5] !== editorName) {
    t4 = editorName && <Box marginTop={1}><Text dimColor={true}>"/plan open"</Text><Text dimColor={true}> to edit this plan in </Text><Text bold={true} dimColor={true}>{editorName}</Text></Box>;
    $[5] = editorName;
    $[6] = t4;
  } else {
    t4 = $[6];

```

---


### `src/commands/plugin/AddMarketplace.tsx`

**信息:**
- 行数: 162
- 大小: 21821 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { ConfigurableShortcutHint } from '../../components/ConfigurableShortcutHint.js';
import { Byline } from '../../components/design-system/Byline.js';
import { KeyboardShortcutHint } from '../../components/design-system/KeyboardShortcutHint.js';
import { Spinner } from '../../components/Spinner.js';
import TextInput from '../../components/TextInput.js';
import { Box, Text } from '../../ink.js';
import { toError } from '../../utils/errors.js';
import { logError } from '../../utils/log.js';
import { clearAllCaches } from '../../utils/plugins/cacheUtils.js';
import { addMarketplaceSource, saveMarketplaceToSettings } from '../../utils/plugins/marketplaceManager.js';
import { parseMarketplaceInput } from '../../utils/plugins/parseMarketplaceInput.js';
import type { ViewState } from './types.js';
type Props = {
  inputValue: string;
  setInputValue: (value: string) => void;
  cursorOffset: number;
  setCursorOffset: (offset: number) => void;
  error: string | null;
  setError: (error: string | null) => void;
  result: string | null;
  setResult: (result: string | null) => void;
  setViewState: (state: ViewState) => void;
  onAddComplete?: () => void | Promise<void>;
  cliMode?: boolean;
};
export function AddMarketplace({
  inputValue,
  setInputValue,
  cursorOffset,
  setCursorOffset,
  error,
  setError,
  result,
  setResult,
  setViewState,
  onAddComplete,
  cliMode = false
}: Props): React.ReactNode {
  const hasAttemptedAutoAdd = useRef(false);
  const [isLoading, setLoading] = useState(false);
  const [progressMessage, setProgressMessage] = useState<string>('');
  const handleAdd = async () => {
    const input = inputValue.trim();
    if (!input) {
      setError('Please enter a marketplace source');
      return;
    }

```

---


### `src/commands/plugin/BrowseMarketplace.tsx`

**信息:**
- 行数: 802
- 大小: 119562 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import figures from 'figures';
import * as React from 'react';
import { useEffect, useState } from 'react';
import { ConfigurableShortcutHint } from '../../components/ConfigurableShortcutHint.js';
import { Byline } from '../../components/design-system/Byline.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding, useKeybindings } from '../../keybindings/useKeybinding.js';
import type { LoadedPlugin } from '../../types/plugin.js';
import { count } from '../../utils/array.js';
import { openBrowser } from '../../utils/browser.js';
import { logForDebugging } from '../../utils/debug.js';
import { errorMessage } from '../../utils/errors.js';
import { clearAllCaches } from '../../utils/plugins/cacheUtils.js';
import { formatInstallCount, getInstallCounts } from '../../utils/plugins/installCounts.js';
import { isPluginGloballyInstalled, isPluginInstalled } from '../../utils/plugins/installedPluginsManager.js';
import { createPluginId, formatFailureDetails, formatMarketplaceLoadingErrors, getMarketplaceSourceDisplay, loadMarketplacesWithGracefulDegradation } from '../../utils/plugins/marketplaceHelpers.js';
import { getMarketplace, loadKnownMarketplacesConfig } from '../../utils/plugins/marketplaceManager.js';
import { OFFICIAL_MARKETPLACE_NAME } from '../../utils/plugins/officialMarketplace.js';
import { installPluginFromMarketplace } from '../../utils/plugins/pluginInstallationHelpers.js';
import { isPluginBlockedByPolicy } from '../../utils/plugins/pluginPolicy.js';
import { plural } from '../../utils/stringUtils.js';
import { truncateToWidth } from '../../utils/truncate.js';
import { findPluginOptionsTarget, PluginOptionsFlow } from './PluginOptionsFlow.js';
import { PluginTrustWarning } from './PluginTrustWarning.js';
import { buildPluginDetailsMenuOptions, extractGitHubRepo, type InstallablePlugin, PluginSelectionKeyHint } from './pluginDetailsHelpers.js';
import type { ViewState as ParentViewState } from './types.js';
import { usePagination } from './usePagination.js';
type Props = {
  error: string | null;
  setError: (error: string | null) => void;
  result: string | null;
  setResult: (result: string | null) => void;
  setViewState: (state: ParentViewState) => void;
  onInstallComplete?: () => void | Promise<void>;
  targetMarketplace?: string;
  targetPlugin?: string;
};
type ViewState = 'marketplace-list' | 'plugin-list' | 'plugin-details' | {
  type: 'plugin-options';
  plugin: LoadedPlugin;
  pluginId: string;
};
type MarketplaceInfo = {
  name: string;
  totalPlugins: number;
  installedCount: number;
  source?: string;
};
export function BrowseMarketplace({
  error,

```

---


### `src/commands/plugin/DiscoverPlugins.tsx`

**信息:**
- 行数: 781
- 大小: 106666 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { ConfigurableShortcutHint } from '../../components/ConfigurableShortcutHint.js';
import { Byline } from '../../components/design-system/Byline.js';
import { SearchBox } from '../../components/SearchBox.js';
import { useSearchInput } from '../../hooks/useSearchInput.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- useInput needed for raw search mode text input
import { Box, Text, useInput, useTerminalFocus } from '../../ink.js';
import { useKeybinding, useKeybindings } from '../../keybindings/useKeybinding.js';
import type { LoadedPlugin } from '../../types/plugin.js';
import { count } from '../../utils/array.js';
import { openBrowser } from '../../utils/browser.js';
import { logForDebugging } from '../../utils/debug.js';
import { errorMessage } from '../../utils/errors.js';
import { clearAllCaches } from '../../utils/plugins/cacheUtils.js';
import { formatInstallCount, getInstallCounts } from '../../utils/plugins/installCounts.js';
import { isPluginGloballyInstalled } from '../../utils/plugins/installedPluginsManager.js';
import { createPluginId, detectEmptyMarketplaceReason, type EmptyMarketplaceReason, formatFailureDetails, formatMarketplaceLoadingErrors, loadMarketplacesWithGracefulDegradation } from '../../utils/plugins/marketplaceHelpers.js';
import { loadKnownMarketplacesConfig } from '../../utils/plugins/marketplaceManager.js';
import { OFFICIAL_MARKETPLACE_NAME } from '../../utils/plugins/officialMarketplace.js';
import { installPluginFromMarketplace } from '../../utils/plugins/pluginInstallationHelpers.js';
import { isPluginBlockedByPolicy } from '../../utils/plugins/pluginPolicy.js';
import { plural } from '../../utils/stringUtils.js';
import { truncateToWidth } from '../../utils/truncate.js';
import { findPluginOptionsTarget, PluginOptionsFlow } from './PluginOptionsFlow.js';
import { PluginTrustWarning } from './PluginTrustWarning.js';
import { buildPluginDetailsMenuOptions, extractGitHubRepo, type InstallablePlugin } from './pluginDetailsHelpers.js';
import type { ViewState as ParentViewState } from './types.js';
import { usePagination } from './usePagination.js';
type Props = {
  error: string | null;
  setError: (error: string | null) => void;
  result: string | null;
  setResult: (result: string | null) => void;
  setViewState: (state: ParentViewState) => void;
  onInstallComplete?: () => void | Promise<void>;
  onSearchModeChange?: (isActive: boolean) => void;
  targetPlugin?: string;
};
type ViewState = 'plugin-list' | 'plugin-details' | {
  type: 'plugin-options';
  plugin: LoadedPlugin;
  pluginId: string;
};
export function DiscoverPlugins({
  error,
  setError,

```

---


### `src/commands/plugin/ManageMarketplaces.tsx`

**信息:**
- 行数: 838
- 大小: 118912 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { ConfigurableShortcutHint } from '../../components/ConfigurableShortcutHint.js';
import { Byline } from '../../components/design-system/Byline.js';
import { KeyboardShortcutHint } from '../../components/design-system/KeyboardShortcutHint.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- useInput needed for marketplace-specific u/r shortcuts and y/n confirmation not in keybinding schema
import { Box, Text, useInput } from '../../ink.js';
import { useKeybinding, useKeybindings } from '../../keybindings/useKeybinding.js';
import type { LoadedPlugin } from '../../types/plugin.js';
import { count } from '../../utils/array.js';
import { shouldSkipPluginAutoupdate } from '../../utils/config.js';
import { errorMessage } from '../../utils/errors.js';
import { clearAllCaches } from '../../utils/plugins/cacheUtils.js';
import { createPluginId, formatMarketplaceLoadingErrors, getMarketplaceSourceDisplay, loadMarketplacesWithGracefulDegradation } from '../../utils/plugins/marketplaceHelpers.js';
import { loadKnownMarketplacesConfig, refreshMarketplace, removeMarketplaceSource, setMarketplaceAutoUpdate } from '../../utils/plugins/marketplaceManager.js';
import { updatePluginsForMarketplaces } from '../../utils/plugins/pluginAutoupdate.js';
import { loadAllPlugins } from '../../utils/plugins/pluginLoader.js';
import { isMarketplaceAutoUpdate } from '../../utils/plugins/schemas.js';
import { getSettingsForSource, updateSettingsForSource } from '../../utils/settings/settings.js';
import { plural } from '../../utils/stringUtils.js';
import type { ViewState } from './types.js';
type Props = {
  setViewState: (state: ViewState) => void;
  error?: string | null;
  setError?: (error: string | null) => void;
  setResult: (result: string | null) => void;
  exitState: {
    pending: boolean;
    keyName: 'Ctrl-C' | 'Ctrl-D' | null;
  };
  onManageComplete?: () => void | Promise<void>;
  targetMarketplace?: string;
  action?: 'update' | 'remove';
};
type MarketplaceState = {
  name: string;
  source: string;
  lastUpdated?: string;
  pluginCount?: number;
  installedPlugins?: LoadedPlugin[];
  pendingUpdate?: boolean;
  pendingRemove?: boolean;
  autoUpdate?: boolean;
};
type InternalViewState = 'list' | 'details' | 'confirm-remove';
export function ManageMarketplaces({
  setViewState,

```

---


### `src/commands/plugin/ManagePlugins.tsx`

**信息:**
- 行数: 2215
- 大小: 321775 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import figures from 'figures';
import type { Dirent } from 'fs';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as React from 'react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ConfigurableShortcutHint } from '../../components/ConfigurableShortcutHint.js';
import { Byline } from '../../components/design-system/Byline.js';
import { MCPRemoteServerMenu } from '../../components/mcp/MCPRemoteServerMenu.js';
import { MCPStdioServerMenu } from '../../components/mcp/MCPStdioServerMenu.js';
import { MCPToolDetailView } from '../../components/mcp/MCPToolDetailView.js';
import { MCPToolListView } from '../../components/mcp/MCPToolListView.js';
import type { ClaudeAIServerInfo, HTTPServerInfo, SSEServerInfo, StdioServerInfo } from '../../components/mcp/types.js';
import { SearchBox } from '../../components/SearchBox.js';
import { useSearchInput } from '../../hooks/useSearchInput.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- useInput needed for raw search mode text input
import { Box, Text, useInput, useTerminalFocus } from '../../ink.js';
import { useKeybinding, useKeybindings } from '../../keybindings/useKeybinding.js';
import { getBuiltinPluginDefinition } from '../../plugins/builtinPlugins.js';
import { useMcpToggleEnabled } from '../../services/mcp/MCPConnectionManager.js';
import type { MCPServerConnection, McpClaudeAIProxyServerConfig, McpHTTPServerConfig, McpSSEServerConfig, McpStdioServerConfig } from '../../services/mcp/types.js';
import { filterToolsByServer } from '../../services/mcp/utils.js';
import { disablePluginOp, enablePluginOp, getPluginInstallationFromV2, isInstallableScope, isPluginEnabledAtProjectScope, uninstallPluginOp, updatePluginOp } from '../../services/plugins/pluginOperations.js';
import { useAppState } from '../../state/AppState.js';
import type { Tool } from '../../Tool.js';
import type { LoadedPlugin, PluginError } from '../../types/plugin.js';
import { count } from '../../utils/array.js';
import { openBrowser } from '../../utils/browser.js';
import { logForDebugging } from '../../utils/debug.js';
import { errorMessage, toError } from '../../utils/errors.js';
import { logError } from '../../utils/log.js';
import { clearAllCaches } from '../../utils/plugins/cacheUtils.js';
import { loadInstalledPluginsV2 } from '../../utils/plugins/installedPluginsManager.js';
import { getMarketplace } from '../../utils/plugins/marketplaceManager.js';
import { isMcpbSource, loadMcpbFile, type McpbNeedsConfigResult, type UserConfigValues } from '../../utils/plugins/mcpbHandler.js';
import { getPluginDataDirSize, pluginDataDirPath } from '../../utils/plugins/pluginDirectories.js';
import { getFlaggedPlugins, markFlaggedPluginsSeen, removeFlaggedPlugin } from '../../utils/plugins/pluginFlagging.js';
import { type PersistablePluginScope, parsePluginIdentifier } from '../../utils/plugins/pluginIdentifier.js';
import { loadAllPlugins } from '../../utils/plugins/pluginLoader.js';
import { loadPluginOptions, type PluginOptionSchema, savePluginOptions } from '../../utils/plugins/pluginOptionsStorage.js';
import { isPluginBlockedByPolicy } from '../../utils/plugins/pluginPolicy.js';
import { getPluginEditableScopes } from '../../utils/plugins/pluginStartupCheck.js';
import { getSettings_DEPRECATED, getSettingsForSource, updateSettingsForSource } from '../../utils/settings/settings.js';
import { jsonParse } from '../../utils/slowOperations.js';
import { plural } from '../../utils/stringUtils.js';
import { formatErrorMessage, getErrorGuidance } from './PluginErrors.js';
import { PluginOptionsDialog } from './PluginOptionsDialog.js';
import { PluginOptionsFlow } from './PluginOptionsFlow.js';
import type { ViewState as ParentViewState } from './types.js';

```

---


### `src/commands/plugin/PluginErrors.tsx`

**信息:**
- 行数: 124
- 大小: 23316 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { getPluginErrorMessage, type PluginError } from '../../types/plugin.js';
export function formatErrorMessage(error: PluginError): string {
  switch (error.type) {
    case 'path-not-found':
      return `${error.component} path not found: ${error.path}`;
    case 'git-auth-failed':
      return `Git ${error.authType.toUpperCase()} authentication failed for ${error.gitUrl}`;
    case 'git-timeout':
      return `Git ${error.operation} timed out for ${error.gitUrl}`;
    case 'network-error':
      return `Network error accessing ${error.url}${error.details ? `: ${error.details}` : ''}`;
    case 'manifest-parse-error':
      return `Failed to parse manifest at ${error.manifestPath}: ${error.parseError}`;
    case 'manifest-validation-error':
      return `Invalid manifest at ${error.manifestPath}: ${error.validationErrors.join(', ')}`;
    case 'plugin-not-found':
      return `Plugin "${error.pluginId}" not found in marketplace "${error.marketplace}"`;
    case 'marketplace-not-found':
      return `Marketplace "${error.marketplace}" not found`;
    case 'marketplace-load-failed':
      return `Failed to load marketplace "${error.marketplace}": ${error.reason}`;
    case 'mcp-config-invalid':
      return `Invalid MCP server config for "${error.serverName}": ${error.validationError}`;
    case 'mcp-server-suppressed-duplicate':
      {
        const dup = error.duplicateOf.startsWith('plugin:') ? `server provided by plugin "${error.duplicateOf.split(':')[1] ?? '?'}"` : `already-configured "${error.duplicateOf}"`;
        return `MCP server "${error.serverName}" skipped — same command/URL as ${dup}`;
      }
    case 'hook-load-failed':
      return `Failed to load hooks from ${error.hookPath}: ${error.reason}`;
    case 'component-load-failed':
      return `Failed to load ${error.component} from ${error.path}: ${error.reason}`;
    case 'mcpb-download-failed':
      return `Failed to download MCPB from ${error.url}: ${error.reason}`;
    case 'mcpb-extract-failed':
      return `Failed to extract MCPB ${error.mcpbPath}: ${error.reason}`;
    case 'mcpb-invalid-manifest':
      return `MCPB manifest invalid at ${error.mcpbPath}: ${error.validationError}`;
    case 'marketplace-blocked-by-policy':
      return error.blockedByBlocklist ? `Marketplace "${error.marketplace}" is blocked by enterprise policy` : `Marketplace "${error.marketplace}" is not in the allowed marketplace list`;
    case 'dependency-unsatisfied':
      return error.reason === 'not-enabled' ? `Dependency "${error.dependency}" is disabled` : `Dependency "${error.dependency}" is not installed`;
    case 'lsp-config-invalid':
      return `Invalid LSP server config for "${error.serverName}": ${error.validationError}`;
    case 'lsp-server-start-failed':
      return `LSP server "${error.serverName}" failed to start: ${error.reason}`;
    case 'lsp-server-crashed':
      return error.signal ? `LSP server "${error.serverName}" crashed with signal ${error.signal}` : `LSP server "${error.serverName}" crashed with exit code ${error.exitCode ?? 'unknown'}`;
    case 'lsp-request-timeout':
      return `LSP server "${error.serverName}" timed out on ${error.method} after ${error.timeoutMs}ms`;

```

---


### `src/commands/plugin/PluginOptionsDialog.tsx`

**信息:**
- 行数: 357
- 大小: 34537 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { useCallback, useState } from 'react';
import { Dialog } from '../../components/design-system/Dialog.js';
import { stringWidth } from '../../ink/stringWidth.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- raw text input for config dialog
import { Box, Text, useInput } from '../../ink.js';
import { useKeybinding, useKeybindings } from '../../keybindings/useKeybinding.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import type { PluginOptionSchema, PluginOptionValues } from '../../utils/plugins/pluginOptionsStorage.js';

/**
 * Build the onSave payload from collected string inputs.
 *
 * Sensitive fields are never prepopulated in the text buffer (security), so
 * by the time the user reaches the last field every sensitive field they
 * stepped through contains '' in collected. To avoid silently wiping saved
 * secrets on reconfigure: if a sensitive field is '' AND initialValues has
 * a value for it, OMIT the key entirely. savePluginOptions only writes keys
 * it receives, so omitting = keep existing.
 *
 * Exported for unit testing.
 */
export function buildFinalValues(fields: string[], collected: Record<string, string>, configSchema: PluginOptionSchema, initialValues: PluginOptionValues | undefined): PluginOptionValues {
  const finalValues: PluginOptionValues = {};
  for (const fieldKey of fields) {
    const schema = configSchema[fieldKey];
    const value = collected[fieldKey] ?? '';
    if (schema?.sensitive === true && value === '' && initialValues?.[fieldKey] !== undefined) {
      continue;
    }
    if (schema?.type === 'number') {
      // Number('') returns 0, not NaN — omit blank number inputs so
      // validateUserConfig's required check actually catches them.
      if (value.trim() === '') continue;
      const num = Number(value);
      finalValues[fieldKey] = Number.isNaN(num) ? value : num;
    } else if (schema?.type === 'boolean') {
      finalValues[fieldKey] = isEnvTruthy(value);
    } else {
      finalValues[fieldKey] = value;
    }
  }
  return finalValues;
}
type Props = {
  title: string;
  subtitle: string;
  configSchema: PluginOptionSchema;
  /** Pre-fill fields when reconfiguring. Sensitive fields are not prepopulated. */

```

---


### `src/commands/plugin/PluginOptionsFlow.tsx`

**信息:**
- 行数: 135
- 大小: 18702 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
/**
 * Post-install/post-enable config prompt.
 *
 * Given a LoadedPlugin, checks both the top-level manifest.userConfig and the
 * channel-specific userConfig. Walks PluginOptionsDialog through each
 * unconfigured item, saving via the appropriate storage function. Calls
 * onDone('skipped') immediately if nothing needs filling.
 */

import * as React from 'react';
import type { LoadedPlugin } from '../../types/plugin.js';
import { errorMessage } from '../../utils/errors.js';
import { loadMcpServerUserConfig, saveMcpServerUserConfig } from '../../utils/plugins/mcpbHandler.js';
import { getUnconfiguredChannels, type UnconfiguredChannel } from '../../utils/plugins/mcpPluginIntegration.js';
import { loadAllPlugins } from '../../utils/plugins/pluginLoader.js';
import { getUnconfiguredOptions, loadPluginOptions, type PluginOptionSchema, type PluginOptionValues, savePluginOptions } from '../../utils/plugins/pluginOptionsStorage.js';
import { PluginOptionsDialog } from './PluginOptionsDialog.js';

/**
 * Post-install lookup: return the LoadedPlugin for the just-installed
 * pluginId so the caller can divert to PluginOptionsFlow. Returns undefined
 * if the plugin somehow didn't make it into the fresh load — callers treat
 * undefined as "carry on closing."
 *
 * Install should have cleared caches already; loadAllPlugins reads fresh.
 */
export async function findPluginOptionsTarget(pluginId: string): Promise<LoadedPlugin | undefined> {
  const {
    enabled,
    disabled
  } = await loadAllPlugins();
  return [...enabled, ...disabled].find(p => p.repository === pluginId || p.source === pluginId);
}

/**
 * A single dialog step in the walk. Top-level options and channels both
 * collapse to this shape — the only difference is which save function runs.
 */
type ConfigStep = {
  key: string;
  title: string;
  subtitle: string;
  schema: PluginOptionSchema;
  /** Returns any already-saved values so PluginOptionsDialog can pre-fill and
   *  skip unchanged sensitive fields on reconfigure. */
  load: () => PluginOptionValues | undefined;
  save: (values: PluginOptionValues) => void;
};
type Props = {
  plugin: LoadedPlugin;

```

---


### `src/commands/plugin/PluginSettings.tsx`

**信息:**
- 行数: 1072
- 大小: 128668 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useCallback, useEffect, useState } from 'react';
import { ConfigurableShortcutHint } from '../../components/ConfigurableShortcutHint.js';
import { Byline } from '../../components/design-system/Byline.js';
import { Pane } from '../../components/design-system/Pane.js';
import { Tab, Tabs } from '../../components/design-system/Tabs.js';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding, useKeybindings } from '../../keybindings/useKeybinding.js';
import { useAppState, useSetAppState } from '../../state/AppState.js';
import type { PluginError } from '../../types/plugin.js';
import { errorMessage } from '../../utils/errors.js';
import { clearAllCaches } from '../../utils/plugins/cacheUtils.js';
import { loadMarketplacesWithGracefulDegradation } from '../../utils/plugins/marketplaceHelpers.js';
import { loadKnownMarketplacesConfig, removeMarketplaceSource } from '../../utils/plugins/marketplaceManager.js';
import { getPluginEditableScopes } from '../../utils/plugins/pluginStartupCheck.js';
import type { EditableSettingSource } from '../../utils/settings/constants.js';
import { getSettingsForSource, updateSettingsForSource } from '../../utils/settings/settings.js';
import { AddMarketplace } from './AddMarketplace.js';
import { BrowseMarketplace } from './BrowseMarketplace.js';
import { DiscoverPlugins } from './DiscoverPlugins.js';
import { ManageMarketplaces } from './ManageMarketplaces.js';
import { ManagePlugins } from './ManagePlugins.js';
import { formatErrorMessage, getErrorGuidance } from './PluginErrors.js';
import { type ParsedCommand, parsePluginArgs } from './parseArgs.js';
import type { PluginSettingsProps, ViewState } from './types.js';
import { ValidatePlugin } from './ValidatePlugin.js';
type TabId = 'discover' | 'installed' | 'marketplaces' | 'errors';
function MarketplaceList(t0) {
  const $ = _c(4);
  const {
    onComplete
  } = t0;
  let t1;
  let t2;
  if ($[0] !== onComplete) {
    t1 = () => {
      const loadList = async function loadList() {
        ;
        try {
          const config = await loadKnownMarketplacesConfig();
          const names = Object.keys(config);
          if (names.length === 0) {
            onComplete("No marketplaces configured");
          } else {
            onComplete(`Configured marketplaces:\n${names.map(_temp).join("\n")}`);
          }
        } catch (t3) {

```

---


### `src/commands/plugin/PluginTrustWarning.tsx`

**信息:**
- 行数: 32
- 大小: 3919 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { getPluginTrustMessage } from '../../utils/plugins/marketplaceHelpers.js';
export function PluginTrustWarning() {
  const $ = _c(3);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = getPluginTrustMessage();
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  const customMessage = t0;
  let t1;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Text color="claude">{figures.warning} </Text>;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Box marginBottom={1}>{t1}<Text dimColor={true} italic={true}>Make sure you trust a plugin before installing, updating, or using it. Anthropic does not control what MCP servers, files, or other software are included in plugins and cannot verify that they will work as intended or that they won't change. See each plugin's homepage for more information.{customMessage ? ` ${customMessage}` : ""}</Text></Box>;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  return t2;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJmaWd1cmVzIiwiUmVhY3QiLCJCb3giLCJUZXh0IiwiZ2V0UGx1Z2luVHJ1c3RNZXNzYWdlIiwiUGx1Z2luVHJ1c3RXYXJuaW5nIiwiJCIsIl9jIiwidDAiLCJTeW1ib2wiLCJmb3IiLCJjdXN0b21NZXNzYWdlIiwidDEiLCJ3YXJuaW5nIiwidDIiXSwic291cmNlcyI6WyJQbHVnaW5UcnVzdFdhcm5pbmcudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCBmaWd1cmVzIGZyb20gJ2ZpZ3VyZXMnXG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IEJveCwgVGV4dCB9IGZyb20gJy4uLy4uL2luay5qcydcbmltcG9ydCB7IGdldFBsdWdpblRydXN0TWVzc2FnZSB9IGZyb20gJy4uLy4uL3V0aWxzL3BsdWdpbnMvbWFya2V0cGxhY2VIZWxwZXJzLmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gUGx1Z2luVHJ1c3RXYXJuaW5nKCk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIGNvbnN0IGN1c3RvbU1lc3NhZ2UgPSBnZXRQbHVnaW5UcnVzdE1lc3NhZ2UoKVxuICByZXR1cm4gKFxuICAgIDxCb3ggbWFyZ2luQm90dG9tPXsxfT5cbiAgICAgIDxUZXh0IGNvbG9yPVwiY2xhdWRlXCI+e2ZpZ3VyZXMud2FybmluZ30gPC9UZXh0PlxuICAgICAgPFRleHQgZGltQ29sb3IgaXRhbGljPlxuICAgICAgICBNYWtlIHN1cmUgeW91IHRydXN0IGEgcGx1Z2luIGJlZm9yZSBpbnN0YWxsaW5nLCB1cGRhdGluZywgb3IgdXNpbmcgaXQuXG4gICAgICAgIEFudGhyb3BpYyBkb2VzIG5vdCBjb250cm9sIHdoYXQgTUNQIHNlcnZlcnMsIGZpbGVzLCBvciBvdGhlciBzb2Z0d2FyZVxuICAgICAgICBhcmUgaW5jbHVkZWQgaW4gcGx1Z2lucyBhbmQgY2Fubm90IHZlcmlmeSB0aGF0IHRoZXkgd2lsbCB3b3JrIGFzXG4gICAgICAgIGludGVuZGVkIG9yIHRoYXQgdGhleSB3b24mYXBvczt0IGNoYW5nZS4gU2VlIGVhY2ggcGx1Z2luJmFwb3M7cyBob21lcGFnZVxuICAgICAgICBmb3IgbW9yZSBpbmZvcm1hdGlvbi57Y3VzdG9tTWVzc2FnZSA/IGAgJHtjdXN0b21NZXNzYWdlfWAgOiAnJ31cbiAgICAgIDwvVGV4dD5cbiAgICA8L0JveD5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiO0FBQUEsT0FBT0EsT0FBTyxNQUFNLFNBQVM7QUFDN0IsT0FBTyxLQUFLQyxLQUFLLE1BQU0sT0FBTztBQUM5QixTQUFTQyxHQUFHLEVBQUVDLElBQUksUUFBUSxjQUFjO0FBQ3hDLFNBQVNDLHFCQUFxQixRQUFRLDJDQUEyQztBQUVqRixPQUFPLFNBQUFDLG1CQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQUEsSUFBQUMsRUFBQTtFQUFBLElBQUFGLENBQUEsUUFBQUcsTUFBQSxDQUFBQyxHQUFBO0lBQ2lCRixFQUFBLEdBQUFKLHFCQUFxQixDQUFDLENBQUM7SUFBQUUsQ0FBQSxNQUFBRSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBRixDQUFBO0VBQUE7RUFBN0MsTUFBQUssYUFBQSxHQUFzQkgsRUFBdUI7RUFBQSxJQUFBSSxFQUFBO0VBQUEsSUFBQU4sQ0FBQSxRQUFBRyxNQUFBLENBQUFDLEdBQUE7SUFHekNFLEVBQUEsSUFBQyxJQUFJLENBQU8sS0FBUSxDQUFSLFFBQVEsQ0FBRSxDQUFBWixPQUFPLENBQUFhLE9BQU8sQ0FBRSxDQUFDLEVBQXRDLElBQUksQ0FBeUM7SUFBQVAsQ0FBQSxNQUFBTSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBTixDQUFBO0VBQUE7RUFBQSxJQUFBUSxFQUFBO0VBQUEsSUFBQVIsQ0FBQSxRQUFBRyxNQUFBLENBQUFDLEdBQUE7SUFEaERJLEVBQUEsSUFBQyxHQUFHLENBQWUsWUFBQyxDQUFELEdBQUMsQ0FDbEIsQ0FBQUYsRUFBNkMsQ0FDN0MsQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFSLEtBQU8sQ0FBQyxDQUFDLE1BQU0sQ0FBTixLQUFLLENBQUMsQ0FBQyxrU0FLRSxDQUFBRCxhQUFhLEdBQWIsSUFBb0JBLGFBQWEsRUFBTyxHQUF4QyxFQUF1QyxDQUMvRCxFQU5DLElBQUksQ0FPUCxFQVRDLEdBQUcsQ0FTRTtJQUFBTCxDQUFBLE1BQUFRLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFSLENBQUE7RUFBQTtFQUFBLE9BVE5RLEVBU007QUFBQSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/commands/plugin/UnifiedInstalledCell.tsx`

**信息:**
- 行数: 565
- 大小: 44441 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { Box, color, Text, useTheme } from '../../ink.js';
import { plural } from '../../utils/stringUtils.js';
import type { UnifiedInstalledItem } from './unifiedTypes.js';
type Props = {
  item: UnifiedInstalledItem;
  isSelected: boolean;
};
export function UnifiedInstalledCell(t0) {
  const $ = _c(142);
  const {
    item,
    isSelected
  } = t0;
  const [theme] = useTheme();
  if (item.type === "plugin") {
    let statusIcon;
    let statusText;
    if (item.pendingToggle) {
      let t1;
      if ($[0] !== theme) {
        t1 = color("suggestion", theme)(figures.arrowRight);
        $[0] = theme;
        $[1] = t1;
      } else {
        t1 = $[1];
      }
      statusIcon = t1;
      statusText = item.pendingToggle === "will-enable" ? "will enable" : "will disable";
    } else {
      if (item.errorCount > 0) {
        let t1;
        if ($[2] !== theme) {
          t1 = color("error", theme)(figures.cross);
          $[2] = theme;
          $[3] = t1;
        } else {
          t1 = $[3];
        }
        statusIcon = t1;
        const t2 = item.errorCount;
        let t3;
        if ($[4] !== item.errorCount) {
          t3 = plural(item.errorCount, "error");
          $[4] = item.errorCount;
          $[5] = t3;
        } else {
          t3 = $[5];

```

---


### `src/commands/plugin/ValidatePlugin.tsx`

**信息:**
- 行数: 98
- 大小: 12369 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useEffect } from 'react';
import { Box, Text } from '../../ink.js';
import { errorMessage } from '../../utils/errors.js';
import { logError } from '../../utils/log.js';
import { validateManifest } from '../../utils/plugins/validatePlugin.js';
import { plural } from '../../utils/stringUtils.js';
type Props = {
  onComplete: (result?: string) => void;
  path?: string;
};
export function ValidatePlugin(t0) {
  const $ = _c(5);
  const {
    onComplete,
    path
  } = t0;
  let t1;
  let t2;
  if ($[0] !== onComplete || $[1] !== path) {
    t1 = () => {
      const runValidation = async function runValidation() {
        if (!path) {
          onComplete("Usage: /plugin validate <path>\n\nValidate a plugin or marketplace manifest file or directory.\n\nExamples:\n  /plugin validate .claude-plugin/plugin.json\n  /plugin validate /path/to/plugin-directory\n  /plugin validate .\n\nWhen given a directory, automatically validates .claude-plugin/marketplace.json\nor .claude-plugin/plugin.json (prefers marketplace if both exist).\n\nOr from the command line:\n  claude plugin validate <path>");
          return;
        }
        ;
        try {
          const result = await validateManifest(path);
          let output = "";
          output = output + `Validating ${result.fileType} manifest: ${result.filePath}\n\n`;
          output;
          if (result.errors.length > 0) {
            output = output + `${figures.cross} Found ${result.errors.length} ${plural(result.errors.length, "error")}:\n\n`;
            output;
            result.errors.forEach(error_0 => {
              output = output + `  ${figures.pointer} ${error_0.path}: ${error_0.message}\n`;
              output;
            });
            output = output + "\n";
            output;
          }
          if (result.warnings.length > 0) {
            output = output + `${figures.warning} Found ${result.warnings.length} ${plural(result.warnings.length, "warning")}:\n\n`;
            output;
            result.warnings.forEach(warning => {
              output = output + `  ${figures.pointer} ${warning.path}: ${warning.message}\n`;
              output;

```

---


### `src/commands/plugin/index.tsx`

**信息:**
- 行数: 11
- 大小: 1337 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js';
const plugin = {
  type: 'local-jsx',
  name: 'plugin',
  aliases: ['plugins', 'marketplace'],
  description: 'Manage Claude Code plugins',
  immediate: true,
  load: () => import('./plugin.js')
} satisfies Command;
export default plugin;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJDb21tYW5kIiwicGx1Z2luIiwidHlwZSIsIm5hbWUiLCJhbGlhc2VzIiwiZGVzY3JpcHRpb24iLCJpbW1lZGlhdGUiLCJsb2FkIl0sInNvdXJjZXMiOlsiaW5kZXgudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB0eXBlIHsgQ29tbWFuZCB9IGZyb20gJy4uLy4uL2NvbW1hbmRzLmpzJ1xuXG5jb25zdCBwbHVnaW4gPSB7XG4gIHR5cGU6ICdsb2NhbC1qc3gnLFxuICBuYW1lOiAncGx1Z2luJyxcbiAgYWxpYXNlczogWydwbHVnaW5zJywgJ21hcmtldHBsYWNlJ10sXG4gIGRlc2NyaXB0aW9uOiAnTWFuYWdlIENsYXVkZSBDb2RlIHBsdWdpbnMnLFxuICBpbW1lZGlhdGU6IHRydWUsXG4gIGxvYWQ6ICgpID0+IGltcG9ydCgnLi9wbHVnaW4uanMnKSxcbn0gc2F0aXNmaWVzIENvbW1hbmRcblxuZXhwb3J0IGRlZmF1bHQgcGx1Z2luXG4iXSwibWFwcGluZ3MiOiJBQUFBLGNBQWNBLE9BQU8sUUFBUSxtQkFBbUI7QUFFaEQsTUFBTUMsTUFBTSxHQUFHO0VBQ2JDLElBQUksRUFBRSxXQUFXO0VBQ2pCQyxJQUFJLEVBQUUsUUFBUTtFQUNkQyxPQUFPLEVBQUUsQ0FBQyxTQUFTLEVBQUUsYUFBYSxDQUFDO0VBQ25DQyxXQUFXLEVBQUUsNEJBQTRCO0VBQ3pDQyxTQUFTLEVBQUUsSUFBSTtFQUNmQyxJQUFJLEVBQUVBLENBQUEsS0FBTSxNQUFNLENBQUMsYUFBYTtBQUNsQyxDQUFDLFdBQVdQLE9BQU87QUFFbkIsZUFBZUMsTUFBTSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/commands/plugin/parseArgs.ts`

**信息:**
- 行数: 103
- 大小: 2818 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Parse plugin subcommand arguments into structured commands
export type ParsedCommand =
  | { type: 'menu' }
  | { type: 'help' }
  | { type: 'install'; marketplace?: string; plugin?: string }
  | { type: 'manage' }
  | { type: 'uninstall'; plugin?: string }
  | { type: 'enable'; plugin?: string }
  | { type: 'disable'; plugin?: string }
  | { type: 'validate'; path?: string }
  | {
      type: 'marketplace'
      action?: 'add' | 'remove' | 'update' | 'list'
      target?: string
    }

export function parsePluginArgs(args?: string): ParsedCommand {
  if (!args) {
    return { type: 'menu' }
  }

  const parts = args.trim().split(/\s+/)
  const command = parts[0]?.toLowerCase()

  switch (command) {
    case 'help':
    case '--help':
    case '-h':
      return { type: 'help' }

    case 'install':
    case 'i': {
      const target = parts[1]
      if (!target) {
        return { type: 'install' }
      }

      // Check if it's in format plugin@marketplace
      if (target.includes('@')) {
        const [plugin, marketplace] = target.split('@')
        return { type: 'install', plugin, marketplace }
      }

      // Check if the target looks like a marketplace (URL or path)
      const isMarketplace =
        target.startsWith('http://') ||
        target.startsWith('https://') ||
        target.startsWith('file://') ||
        target.includes('/') ||
        target.includes('\\')

```

---


### `src/commands/plugin/plugin.tsx`

**信息:**
- 行数: 7
- 大小: 1590 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { PluginSettings } from './PluginSettings.js';
export async function call(onDone: LocalJSXCommandOnDone, _context: unknown, args?: string): Promise<React.ReactNode> {
  return <PluginSettings onComplete={onDone} args={args} />;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkxvY2FsSlNYQ29tbWFuZE9uRG9uZSIsIlBsdWdpblNldHRpbmdzIiwiY2FsbCIsIm9uRG9uZSIsIl9jb250ZXh0IiwiYXJncyIsIlByb21pc2UiLCJSZWFjdE5vZGUiXSwic291cmNlcyI6WyJwbHVnaW4udHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHR5cGUgeyBMb2NhbEpTWENvbW1hbmRPbkRvbmUgfSBmcm9tICcuLi8uLi90eXBlcy9jb21tYW5kLmpzJ1xuaW1wb3J0IHsgUGx1Z2luU2V0dGluZ3MgfSBmcm9tICcuL1BsdWdpblNldHRpbmdzLmpzJ1xuXG5leHBvcnQgYXN5bmMgZnVuY3Rpb24gY2FsbChcbiAgb25Eb25lOiBMb2NhbEpTWENvbW1hbmRPbkRvbmUsXG4gIF9jb250ZXh0OiB1bmtub3duLFxuICBhcmdzPzogc3RyaW5nLFxuKTogUHJvbWlzZTxSZWFjdC5SZWFjdE5vZGU+IHtcbiAgcmV0dXJuIDxQbHVnaW5TZXR0aW5ncyBvbkNvbXBsZXRlPXtvbkRvbmV9IGFyZ3M9e2FyZ3N9IC8+XG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsY0FBY0MscUJBQXFCLFFBQVEsd0JBQXdCO0FBQ25FLFNBQVNDLGNBQWMsUUFBUSxxQkFBcUI7QUFFcEQsT0FBTyxlQUFlQyxJQUFJQSxDQUN4QkMsTUFBTSxFQUFFSCxxQkFBcUIsRUFDN0JJLFFBQVEsRUFBRSxPQUFPLEVBQ2pCQyxJQUFhLENBQVIsRUFBRSxNQUFNLENBQ2QsRUFBRUMsT0FBTyxDQUFDUCxLQUFLLENBQUNRLFNBQVMsQ0FBQyxDQUFDO0VBQzFCLE9BQU8sQ0FBQyxjQUFjLENBQUMsVUFBVSxDQUFDLENBQUNKLE1BQU0sQ0FBQyxDQUFDLElBQUksQ0FBQyxDQUFDRSxJQUFJLENBQUMsR0FBRztBQUMzRCIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/commands/plugin/pluginDetailsHelpers.tsx`

**信息:**
- 行数: 117
- 大小: 12424 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * Shared helper functions and types for plugin details views
 *
 * Used by both DiscoverPlugins and BrowseMarketplace components.
 */

import * as React from 'react';
import { ConfigurableShortcutHint } from '../../components/ConfigurableShortcutHint.js';
import { Byline } from '../../components/design-system/Byline.js';
import { Box, Text } from '../../ink.js';
import type { PluginMarketplaceEntry } from '../../utils/plugins/schemas.js';

/**
 * Represents a plugin available for installation from a marketplace
 */
export type InstallablePlugin = {
  entry: PluginMarketplaceEntry;
  marketplaceName: string;
  pluginId: string;
  isInstalled: boolean;
};

/**
 * Menu option for plugin details view
 */
export type PluginDetailsMenuOption = {
  label: string;
  action: string;
};

/**
 * Extract GitHub repo info from a plugin's source
 */
export function extractGitHubRepo(plugin: InstallablePlugin): string | null {
  const isGitHub = plugin.entry.source && typeof plugin.entry.source === 'object' && 'source' in plugin.entry.source && plugin.entry.source.source === 'github';
  if (isGitHub && typeof plugin.entry.source === 'object' && 'repo' in plugin.entry.source) {
    return plugin.entry.source.repo;
  }
  return null;
}

/**
 * Build menu options for plugin details view with scoped installation options
 */
export function buildPluginDetailsMenuOptions(hasHomepage: string | undefined, githubRepo: string | null): PluginDetailsMenuOption[] {
  const options: PluginDetailsMenuOption[] = [{
    label: 'Install for you (user scope)',
    action: 'install-user'
  }, {

```

---


### `src/commands/plugin/types.ts`

**信息:**
- 行数: 2
- 大小: 89 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type ViewState = string
export type PluginSettingsProps = Record<string, unknown>

```

---


### `src/commands/plugin/unifiedTypes.ts`

**信息:**
- 行数: 2
- 大小: 122 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type UnifiedMarketplaceItem = Record<string, unknown>
export type UnifiedInstalledPlugin = Record<string, unknown>

```

---


### `src/commands/plugin/usePagination.ts`

**信息:**
- 行数: 171
- 大小: 4990 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useMemo, useRef } from 'react'

const DEFAULT_MAX_VISIBLE = 5

type UsePaginationOptions = {
  totalItems: number
  maxVisible?: number
  selectedIndex?: number
}

type UsePaginationResult<T> = {
  // For backwards compatibility with page-based terminology
  currentPage: number
  totalPages: number
  startIndex: number
  endIndex: number
  needsPagination: boolean
  pageSize: number
  // Get visible slice of items
  getVisibleItems: (items: T[]) => T[]
  // Convert visible index to actual index
  toActualIndex: (visibleIndex: number) => number
  // Check if actual index is visible
  isOnCurrentPage: (actualIndex: number) => boolean
  // Navigation (kept for API compatibility)
  goToPage: (page: number) => void
  nextPage: () => void
  prevPage: () => void
  // Handle selection - just updates the index, scrolling is automatic
  handleSelectionChange: (
    newIndex: number,
    setSelectedIndex: (index: number) => void,
  ) => void
  // Page navigation - returns false for continuous scrolling (not needed)
  handlePageNavigation: (
    direction: 'left' | 'right',
    setSelectedIndex: (index: number) => void,
  ) => boolean
  // Scroll position info for UI display
  scrollPosition: {
    current: number
    total: number
    canScrollUp: boolean
    canScrollDown: boolean
  }
}

export function usePagination<T>({
  totalItems,
  maxVisible = DEFAULT_MAX_VISIBLE,

```

---


### `src/commands/pr_comments/index.ts`

**信息:**
- 行数: 50
- 大小: 1848 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { createMovedToPluginCommand } from '../createMovedToPluginCommand.js'

export default createMovedToPluginCommand({
  name: 'pr-comments',
  description: 'Get comments from a GitHub pull request',
  progressMessage: 'fetching PR comments',
  pluginName: 'pr-comments',
  pluginCommand: 'pr-comments',
  async getPromptWhileMarketplaceIsPrivate(args) {
    return [
      {
        type: 'text',
        text: `You are an AI assistant integrated into a git-based version control system. Your task is to fetch and display comments from a GitHub pull request.

Follow these steps:

1. Use \`gh pr view --json number,headRepository\` to get the PR number and repository info
2. Use \`gh api /repos/{owner}/{repo}/issues/{number}/comments\` to get PR-level comments
3. Use \`gh api /repos/{owner}/{repo}/pulls/{number}/comments\` to get review comments. Pay particular attention to the following fields: \`body\`, \`diff_hunk\`, \`path\`, \`line\`, etc. If the comment references some code, consider fetching it using eg \`gh api /repos/{owner}/{repo}/contents/{path}?ref={branch} | jq .content -r | base64 -d\`
4. Parse and format all comments in a readable way
5. Return ONLY the formatted comments, with no additional text

Format the comments as:

## Comments

[For each comment thread:]
- @author file.ts#line:
  \`\`\`diff
  [diff_hunk from the API response]
  \`\`\`
  > quoted comment text

  [any replies indented]

If there are no comments, return "No comments found."

Remember:
1. Only show the actual comments, no explanatory text
2. Include both PR-level and code review comments
3. Preserve the threading/nesting of comment replies
4. Show the file and line number context for code review comments
5. Use jq to parse the JSON responses from the GitHub API

${args ? 'Additional user input: ' + args : ''}
`,
      },
    ]
  },
})

```

---


### `src/commands/privacy-settings/index.ts`

**信息:**
- 行数: 14
- 大小: 399 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { isConsumerSubscriber } from '../../utils/auth.js'

const privacySettings = {
  type: 'local-jsx',
  name: 'privacy-settings',
  description: 'View and update your privacy settings',
  isEnabled: () => {
    return isConsumerSubscriber()
  },
  load: () => import('./privacy-settings.js'),
} satisfies Command

export default privacySettings

```

---


### `src/commands/privacy-settings/privacy-settings.tsx`

**信息:**
- 行数: 58
- 大小: 10043 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { type GroveDecision, GroveDialog, PrivacySettingsDialog } from '../../components/grove/Grove.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../services/analytics/index.js';
import { getGroveNoticeConfig, getGroveSettings, isQualifiedForGrove } from '../../services/api/grove.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
const FALLBACK_MESSAGE = 'Review and manage your privacy settings at https://claude.ai/settings/data-privacy-controls';
export async function call(onDone: LocalJSXCommandOnDone): Promise<React.ReactNode | null> {
  const qualified = await isQualifiedForGrove();
  if (!qualified) {
    onDone(FALLBACK_MESSAGE);
    return null;
  }
  const [settingsResult, configResult] = await Promise.all([getGroveSettings(), getGroveNoticeConfig()]);
  // Hide dialog on API failure (after retry)
  if (!settingsResult.success) {
    onDone(FALLBACK_MESSAGE);
    return null;
  }
  const settings = settingsResult.data;
  const config = configResult.success ? configResult.data : null;
  async function onDoneWithDecision(decision: GroveDecision) {
    if (decision === 'escape' || decision === 'defer') {
      onDone('Privacy settings dialog dismissed', {
        display: 'system'
      });
      return;
    }
    await onDoneWithSettingsCheck();
  }
  async function onDoneWithSettingsCheck() {
    const updatedSettingsResult = await getGroveSettings();
    if (!updatedSettingsResult.success) {
      onDone('Unable to retrieve updated privacy settings', {
        display: 'system'
      });
      return;
    }
    const updatedSettings = updatedSettingsResult.data;
    const groveStatus = updatedSettings.grove_enabled ? 'true' : 'false';
    onDone(`"Help improve Claude" set to ${groveStatus}.`);
    if (settings.grove_enabled !== null && settings.grove_enabled !== updatedSettings.grove_enabled) {
      logEvent('tengu_grove_policy_toggled', {
        state: updatedSettings.grove_enabled as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
        location: 'settings' as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS
      });
    }
  }

  // Show privacy settings directly if the user has already accepted the
  // terms.

```

---


### `src/commands/rate-limit-options/index.ts`

**信息:**
- 行数: 19
- 大小: 511 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { isClaudeAISubscriber } from '../../utils/auth.js'

const rateLimitOptions = {
  type: 'local-jsx',
  name: 'rate-limit-options',
  description: 'Show options when rate limit is reached',
  isEnabled: () => {
    if (!isClaudeAISubscriber()) {
      return false
    }

    return true
  },
  isHidden: true, // Hidden from help - only used internally
  load: () => import('./rate-limit-options.js'),
} satisfies Command

export default rateLimitOptions

```

---


### `src/commands/rate-limit-options/rate-limit-options.tsx`

**信息:**
- 行数: 210
- 大小: 23749 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useMemo, useState } from 'react';
import type { CommandResultDisplay, LocalJSXCommandContext } from '../../commands.js';
import { type OptionWithDescription, Select } from '../../components/CustomSelect/select.js';
import { Dialog } from '../../components/design-system/Dialog.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js';
import { logEvent } from '../../services/analytics/index.js';
import { useClaudeAiLimits } from '../../services/claudeAiLimitsHook.js';
import type { ToolUseContext } from '../../Tool.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { getOauthAccountInfo, getRateLimitTier, getSubscriptionType } from '../../utils/auth.js';
import { hasClaudeAiBillingAccess } from '../../utils/billing.js';
import { call as extraUsageCall } from '../extra-usage/extra-usage.js';
import { extraUsage } from '../extra-usage/index.js';
import upgrade from '../upgrade/index.js';
import { call as upgradeCall } from '../upgrade/upgrade.js';
type RateLimitOptionsMenuOptionType = 'upgrade' | 'extra-usage' | 'cancel';
type RateLimitOptionsMenuProps = {
  onDone: (result?: string, options?: {
    display?: CommandResultDisplay | undefined;
  } | undefined) => void;
  context: ToolUseContext & LocalJSXCommandContext;
};
function RateLimitOptionsMenu(t0) {
  const $ = _c(25);
  const {
    onDone,
    context
  } = t0;
  const [subCommandJSX, setSubCommandJSX] = useState(null);
  const claudeAiLimits = useClaudeAiLimits();
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = getSubscriptionType();
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const subscriptionType = t1;
  let t2;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = getRateLimitTier();
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  const rateLimitTier = t2;
  const hasExtraUsageEnabled = getOauthAccountInfo()?.hasExtraUsageEnabled === true;
  const isMax = subscriptionType === "max";
  const isMax20x = isMax && rateLimitTier === "default_claude_max_20x";

```

---


### `src/commands/release-notes/index.ts`

**信息:**
- 行数: 11
- 大小: 268 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const releaseNotes: Command = {
  description: 'View release notes',
  name: 'release-notes',
  type: 'local',
  supportsNonInteractive: true,
  load: () => import('./release-notes.js'),
}

export default releaseNotes

```

---


### `src/commands/release-notes/release-notes.ts`

**信息:**
- 行数: 50
- 大小: 1524 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { LocalCommandResult } from '../../types/command.js'
import {
  CHANGELOG_URL,
  fetchAndStoreChangelog,
  getAllReleaseNotes,
  getStoredChangelog,
} from '../../utils/releaseNotes.js'

function formatReleaseNotes(notes: Array<[string, string[]]>): string {
  return notes
    .map(([version, notes]) => {
      const header = `Version ${version}:`
      const bulletPoints = notes.map(note => `· ${note}`).join('\n')
      return `${header}\n${bulletPoints}`
    })
    .join('\n\n')
}

export async function call(): Promise<LocalCommandResult> {
  // Try to fetch the latest changelog with a 500ms timeout
  let freshNotes: Array<[string, string[]]> = []

  try {
    const timeoutPromise = new Promise<void>((_, reject) => {
      setTimeout(rej => rej(new Error('Timeout')), 500, reject)
    })

    await Promise.race([fetchAndStoreChangelog(), timeoutPromise])
    freshNotes = getAllReleaseNotes(await getStoredChangelog())
  } catch {
    // Either fetch failed or timed out - just use cached notes
  }

  // If we have fresh notes from the quick fetch, use those
  if (freshNotes.length > 0) {
    return { type: 'text', value: formatReleaseNotes(freshNotes) }
  }

  // Otherwise check cached notes
  const cachedNotes = getAllReleaseNotes(await getStoredChangelog())
  if (cachedNotes.length > 0) {
    return { type: 'text', value: formatReleaseNotes(cachedNotes) }
  }

  // Nothing available, show link
  return {
    type: 'text',
    value: `See the full changelog at: ${CHANGELOG_URL}`,
  }
}

```

---


### `src/commands/reload-plugins/index.ts`

**信息:**
- 行数: 18
- 大小: 653 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * /reload-plugins — Layer-3 refresh. Applies pending plugin changes to the
 * running session. Implementation lazy-loaded.
 */
import type { Command } from '../../commands.js'

const reloadPlugins = {
  type: 'local',
  name: 'reload-plugins',
  description: 'Activate pending plugin changes in the current session',
  // SDK callers use query.reloadPlugins() (control request) instead of
  // sending this as a text prompt — that returns structured data
  // (commands, agents, plugins, mcpServers) for UI updates.
  supportsNonInteractive: false,
  load: () => import('./reload-plugins.js'),
} satisfies Command

export default reloadPlugins

```

---


### `src/commands/reload-plugins/reload-plugins.ts`

**信息:**
- 行数: 61
- 大小: 2598 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { getIsRemoteMode } from '../../bootstrap/state.js'
import { redownloadUserSettings } from '../../services/settingsSync/index.js'
import type { LocalCommandCall } from '../../types/command.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { refreshActivePlugins } from '../../utils/plugins/refresh.js'
import { settingsChangeDetector } from '../../utils/settings/changeDetector.js'
import { plural } from '../../utils/stringUtils.js'

export const call: LocalCommandCall = async (_args, context) => {
  // CCR: re-pull user settings before the cache sweep so enabledPlugins /
  // extraKnownMarketplaces pushed from the user's local CLI (settingsSync)
  // take effect. Non-CCR headless (e.g. vscode SDK subprocess) shares disk
  // with whoever writes settings — the file watcher delivers changes, no
  // re-pull needed there.
  //
  // Managed settings intentionally NOT re-fetched: it already polls hourly
  // (POLLING_INTERVAL_MS), and policy enforcement is eventually-consistent
  // by design (stale-cache fallback on fetch failure). Interactive
  // /reload-plugins has never re-fetched it either.
  //
  // No retries: user-initiated command, one attempt + fail-open. The user
  // can re-run /reload-plugins to retry. Startup path keeps its retries.
  if (
    feature('DOWNLOAD_USER_SETTINGS') &&
    (isEnvTruthy(process.env.CLAUDE_CODE_REMOTE) || getIsRemoteMode())
  ) {
    const applied = await redownloadUserSettings()
    // applyRemoteEntriesToLocal uses markInternalWrite to suppress the
    // file watcher (correct for startup, nothing listening yet); fire
    // notifyChange here so mid-session applySettingsChange runs.
    if (applied) {
      settingsChangeDetector.notifyChange('userSettings')
    }
  }

  const r = await refreshActivePlugins(context.setAppState)

  const parts = [
    n(r.enabled_count, 'plugin'),
    n(r.command_count, 'skill'),
    n(r.agent_count, 'agent'),
    n(r.hook_count, 'hook'),
    // "plugin MCP/LSP" disambiguates from user-config/built-in servers,
    // which /reload-plugins doesn't touch. Commands/hooks are plugin-only;
    // agent_count is total agents (incl. built-ins). (gh-31321)
    n(r.mcp_count, 'plugin MCP server'),
    n(r.lsp_count, 'plugin LSP server'),
  ]
  let msg = `Reloaded: ${parts.join(' · ')}`

```

---


### `src/commands/remote-env/index.ts`

**信息:**
- 行数: 15
- 大小: 577 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { isPolicyAllowed } from '../../services/policyLimits/index.js'
import { isClaudeAISubscriber } from '../../utils/auth.js'

export default {
  type: 'local-jsx',
  name: 'remote-env',
  description: 'Configure the default remote environment for teleport sessions',
  isEnabled: () =>
    isClaudeAISubscriber() && isPolicyAllowed('allow_remote_sessions'),
  get isHidden() {
    return !isClaudeAISubscriber() || !isPolicyAllowed('allow_remote_sessions')
  },
  load: () => import('./remote-env.js'),
} satisfies Command

```

---


### `src/commands/remote-env/remote-env.tsx`

**信息:**
- 行数: 7
- 大小: 1454 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { RemoteEnvironmentDialog } from '../../components/RemoteEnvironmentDialog.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
export async function call(onDone: LocalJSXCommandOnDone): Promise<React.ReactNode> {
  return <RemoteEnvironmentDialog onDone={onDone} />;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlJlbW90ZUVudmlyb25tZW50RGlhbG9nIiwiTG9jYWxKU1hDb21tYW5kT25Eb25lIiwiY2FsbCIsIm9uRG9uZSIsIlByb21pc2UiLCJSZWFjdE5vZGUiXSwic291cmNlcyI6WyJyZW1vdGUtZW52LnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IFJlbW90ZUVudmlyb25tZW50RGlhbG9nIH0gZnJvbSAnLi4vLi4vY29tcG9uZW50cy9SZW1vdGVFbnZpcm9ubWVudERpYWxvZy5qcydcbmltcG9ydCB0eXBlIHsgTG9jYWxKU1hDb21tYW5kT25Eb25lIH0gZnJvbSAnLi4vLi4vdHlwZXMvY29tbWFuZC5qcydcblxuZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGNhbGwoXG4gIG9uRG9uZTogTG9jYWxKU1hDb21tYW5kT25Eb25lLFxuKTogUHJvbWlzZTxSZWFjdC5SZWFjdE5vZGU+IHtcbiAgcmV0dXJuIDxSZW1vdGVFbnZpcm9ubWVudERpYWxvZyBvbkRvbmU9e29uRG9uZX0gLz5cbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixTQUFTQyx1QkFBdUIsUUFBUSw2Q0FBNkM7QUFDckYsY0FBY0MscUJBQXFCLFFBQVEsd0JBQXdCO0FBRW5FLE9BQU8sZUFBZUMsSUFBSUEsQ0FDeEJDLE1BQU0sRUFBRUYscUJBQXFCLENBQzlCLEVBQUVHLE9BQU8sQ0FBQ0wsS0FBSyxDQUFDTSxTQUFTLENBQUMsQ0FBQztFQUMxQixPQUFPLENBQUMsdUJBQXVCLENBQUMsTUFBTSxDQUFDLENBQUNGLE1BQU0sQ0FBQyxHQUFHO0FBQ3BEIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/remote-setup/api.ts`

**信息:**
- 行数: 182
- 大小: 5519 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { getOauthConfig } from '../../constants/oauth.js'
import { logForDebugging } from '../../utils/debug.js'
import { getOAuthHeaders, prepareApiRequest } from '../../utils/teleport/api.js'
import { fetchEnvironments } from '../../utils/teleport/environments.js'

const CCR_BYOC_BETA_HEADER = 'ccr-byoc-2025-07-29'

/**
 * Wraps a raw GitHub token so that its string representation is redacted.
 * `String(token)`, template literals, `JSON.stringify(token)`, and any
 * attached error messages will show `[REDACTED:gh-token]` instead of the
 * token value. Call `.reveal()` only at the single point where the raw
 * value is placed into an HTTP body.
 */
export class RedactedGithubToken {
  readonly #value: string
  constructor(raw: string) {
    this.#value = raw
  }
  reveal(): string {
    return this.#value
  }
  toString(): string {
    return '[REDACTED:gh-token]'
  }
  toJSON(): string {
    return '[REDACTED:gh-token]'
  }
  [Symbol.for('nodejs.util.inspect.custom')](): string {
    return '[REDACTED:gh-token]'
  }
}

export type ImportTokenResult = {
  github_username: string
}

export type ImportTokenError =
  | { kind: 'not_signed_in' }
  | { kind: 'invalid_token' }
  | { kind: 'server'; status: number }
  | { kind: 'network' }

/**
 * POSTs a GitHub token to the CCR backend, which validates it against
 * GitHub's /user endpoint and stores it Fernet-encrypted in sync_user_tokens.
 * The stored token satisfies the same read paths as an OAuth token, so
 * clone/push in claude.ai/code works immediately after this succeeds.
 */

```

---


### `src/commands/remote-setup/index.ts`

**信息:**
- 行数: 20
- 大小: 693 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import { isPolicyAllowed } from '../../services/policyLimits/index.js'

const web = {
  type: 'local-jsx',
  name: 'web-setup',
  description:
    'Setup Claude Code on the web (requires connecting your GitHub account)',
  availability: ['claude-ai'],
  isEnabled: () =>
    getFeatureValue_CACHED_MAY_BE_STALE('tengu_cobalt_lantern', false) &&
    isPolicyAllowed('allow_remote_sessions'),
  get isHidden() {
    return !isPolicyAllowed('allow_remote_sessions')
  },
  load: () => import('./remote-setup.js'),
} satisfies Command

export default web

```

---


### `src/commands/remote-setup/remote-setup.tsx`

**信息:**
- 行数: 187
- 大小: 21786 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { execa } from 'execa';
import * as React from 'react';
import { useEffect, useState } from 'react';
import { Select } from '../../components/CustomSelect/index.js';
import { Dialog } from '../../components/design-system/Dialog.js';
import { LoadingState } from '../../components/design-system/LoadingState.js';
import { Box, Text } from '../../ink.js';
import { logEvent, type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS as SafeString } from '../../services/analytics/index.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { openBrowser } from '../../utils/browser.js';
import { getGhAuthStatus } from '../../utils/github/ghAuthStatus.js';
import { createDefaultEnvironment, getCodeWebUrl, type ImportTokenError, importGithubToken, isSignedIn, RedactedGithubToken } from './api.js';
type CheckResult = {
  status: 'not_signed_in';
} | {
  status: 'has_gh_token';
  token: RedactedGithubToken;
} | {
  status: 'gh_not_installed';
} | {
  status: 'gh_not_authenticated';
};
async function checkLoginState(): Promise<CheckResult> {
  if (!(await isSignedIn())) {
    return {
      status: 'not_signed_in'
    };
  }
  const ghStatus = await getGhAuthStatus();
  if (ghStatus === 'not_installed') {
    return {
      status: 'gh_not_installed'
    };
  }
  if (ghStatus === 'not_authenticated') {
    return {
      status: 'gh_not_authenticated'
    };
  }

  // ghStatus === 'authenticated'. getGhAuthStatus spawns with stdout:'ignore'
  // (telemetry-safe); spawn once more with stdout:'pipe' to read the token.
  const {
    stdout
  } = await execa('gh', ['auth', 'token'], {
    stdout: 'pipe',
    stderr: 'ignore',
    timeout: 5000,
    reject: false
  });

```

---


### `src/commands/rename/generateSessionName.ts`

**信息:**
- 行数: 67
- 大小: 2297 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { queryHaiku } from '../../services/api/claude.js'
import type { Message } from '../../types/message.js'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { safeParseJSON } from '../../utils/json.js'
import { extractTextContent } from '../../utils/messages.js'
import { extractConversationText } from '../../utils/sessionTitle.js'
import { asSystemPrompt } from '../../utils/systemPromptType.js'

export async function generateSessionName(
  messages: Message[],
  signal: AbortSignal,
): Promise<string | null> {
  const conversationText = extractConversationText(messages)
  if (!conversationText) {
    return null
  }

  try {
    const result = await queryHaiku({
      systemPrompt: asSystemPrompt([
        'Generate a short kebab-case name (2-4 words) that captures the main topic of this conversation. Use lowercase words separated by hyphens. Examples: "fix-login-bug", "add-auth-feature", "refactor-api-client", "debug-test-failures". Return JSON with a "name" field.',
      ]),
      userPrompt: conversationText,
      outputFormat: {
        type: 'json_schema',
        schema: {
          type: 'object',
          properties: {
            name: { type: 'string' },
          },
          required: ['name'],
          additionalProperties: false,
        },
      },
      signal,
      options: {
        querySource: 'rename_generate_name',
        agents: [],
        isNonInteractiveSession: false,
        hasAppendSystemPrompt: false,
        mcpTools: [],
      },
    })

    const content = extractTextContent(result.message.content)

    const response = safeParseJSON(content)
    if (
      response &&

```

---


### `src/commands/rename/index.ts`

**信息:**
- 行数: 12
- 大小: 281 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const rename = {
  type: 'local-jsx',
  name: 'rename',
  description: 'Rename the current conversation',
  immediate: true,
  argumentHint: '[name]',
  load: () => import('./rename.js'),
} satisfies Command

export default rename

```

---


### `src/commands/rename/rename.ts`

**信息:**
- 行数: 87
- 大小: 2759 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { UUID } from 'crypto'
import { getSessionId } from '../../bootstrap/state.js'
import {
  getBridgeBaseUrlOverride,
  getBridgeTokenOverride,
} from '../../bridge/bridgeConfig.js'
import type { ToolUseContext } from '../../Tool.js'
import type {
  LocalJSXCommandContext,
  LocalJSXCommandOnDone,
} from '../../types/command.js'
import { getMessagesAfterCompactBoundary } from '../../utils/messages.js'
import {
  getTranscriptPath,
  saveAgentName,
  saveCustomTitle,
} from '../../utils/sessionStorage.js'
import { isTeammate } from '../../utils/teammate.js'
import { generateSessionName } from './generateSessionName.js'

export async function call(
  onDone: LocalJSXCommandOnDone,
  context: ToolUseContext & LocalJSXCommandContext,
  args: string,
): Promise<null> {
  // Prevent teammates from renaming - their names are set by team leader
  if (isTeammate()) {
    onDone(
      'Cannot rename: This session is a swarm teammate. Teammate names are set by the team leader.',
      { display: 'system' },
    )
    return null
  }

  let newName: string
  if (!args || args.trim() === '') {
    const generated = await generateSessionName(
      getMessagesAfterCompactBoundary(context.messages),
      context.abortController.signal,
    )
    if (!generated) {
      onDone(
        'Could not generate a name: no conversation context yet. Usage: /rename <name>',
        { display: 'system' },
      )
      return null
    }
    newName = generated
  } else {
    newName = args.trim()

```

---


### `src/commands/resume/index.ts`

**信息:**
- 行数: 12
- 大小: 303 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const resume: Command = {
  type: 'local-jsx',
  name: 'resume',
  description: 'Resume a previous conversation',
  aliases: ['continue'],
  argumentHint: '[conversation id or search term]',
  load: () => import('./resume.js'),
}

export default resume

```

---


### `src/commands/resume/resume.tsx`

**信息:**
- 行数: 275
- 大小: 37026 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import type { UUID } from 'crypto';
import figures from 'figures';
import * as React from 'react';
import { getOriginalCwd, getSessionId } from '../../bootstrap/state.js';
import type { CommandResultDisplay, ResumeEntrypoint } from '../../commands.js';
import { LogSelector } from '../../components/LogSelector.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { Spinner } from '../../components/Spinner.js';
import { useIsInsideModal } from '../../context/modalContext.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { setClipboard } from '../../ink/termio/osc.js';
import { Box, Text } from '../../ink.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
import type { LogOption } from '../../types/logs.js';
import { agenticSessionSearch } from '../../utils/agenticSessionSearch.js';
import { checkCrossProjectResume } from '../../utils/crossProjectResume.js';
import { getWorktreePaths } from '../../utils/getWorktreePaths.js';
import { logError } from '../../utils/log.js';
import { getLastSessionLog, getSessionIdFromLog, isCustomTitleEnabled, isLiteLog, loadAllProjectsMessageLogs, loadFullLog, loadSameRepoMessageLogs, searchSessionsByCustomTitle } from '../../utils/sessionStorage.js';
import { validateUuid } from '../../utils/uuid.js';
type ResumeResult = {
  resultType: 'sessionNotFound';
  arg: string;
} | {
  resultType: 'multipleMatches';
  arg: string;
  count: number;
};
function resumeHelpMessage(result: ResumeResult): string {
  switch (result.resultType) {
    case 'sessionNotFound':
      return `Session ${chalk.bold(result.arg)} was not found.`;
    case 'multipleMatches':
      return `Found ${result.count} sessions matching ${chalk.bold(result.arg)}. Please use /resume to pick a specific session.`;
  }
}
function ResumeError(t0) {
  const $ = _c(10);
  const {
    message,
    args,
    onDone
  } = t0;
  let t1;
  let t2;
  if ($[0] !== onDone) {
    t1 = () => {
      const timer = setTimeout(onDone, 0);

```

---


### `src/commands/review/UltrareviewOverageDialog.tsx`

**信息:**
- 行数: 96
- 大小: 9655 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useRef, useState } from 'react';
import { Select } from '../../components/CustomSelect/select.js';
import { Dialog } from '../../components/design-system/Dialog.js';
import { Box, Text } from '../../ink.js';
type Props = {
  onProceed: (signal: AbortSignal) => Promise<void>;
  onCancel: () => void;
};
export function UltrareviewOverageDialog(t0) {
  const $ = _c(15);
  const {
    onProceed,
    onCancel
  } = t0;
  const [isLaunching, setIsLaunching] = useState(false);
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = new AbortController();
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const abortControllerRef = useRef(t1);
  let t2;
  if ($[1] !== onCancel || $[2] !== onProceed) {
    t2 = value => {
      if (value === "proceed") {
        setIsLaunching(true);
        onProceed(abortControllerRef.current.signal).catch(() => setIsLaunching(false));
      } else {
        onCancel();
      }
    };
    $[1] = onCancel;
    $[2] = onProceed;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  const handleSelect = t2;
  let t3;
  if ($[4] !== onCancel) {
    t3 = () => {
      abortControllerRef.current.abort();
      onCancel();
    };
    $[4] = onCancel;
    $[5] = t3;
  } else {

```

---


### `src/commands/review/reviewRemote.ts`

**信息:**
- 行数: 316
- 大小: 11926 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Teleported /ultrareview execution. Creates a CCR session with the current repo,
 * sends the review prompt as the initial message, and registers a
 * RemoteAgentTask so the polling loop pipes results back into the local
 * session via task-notification. Mirrors the /ultraplan → CCR flow.
 *
 * TODO(#22051): pass useBundleMode once landed so local-only / uncommitted
 * repo state is captured. The GitHub-clone path (current) only works for
 * pushed branches on repos with the Claude GitHub app installed.
 */

import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/messages.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import { fetchUltrareviewQuota } from '../../services/api/ultrareviewQuota.js'
import { fetchUtilization } from '../../services/api/usage.js'
import type { ToolUseContext } from '../../Tool.js'
import {
  checkRemoteAgentEligibility,
  formatPreconditionError,
  getRemoteTaskSessionUrl,
  registerRemoteAgentTask,
} from '../../tasks/RemoteAgentTask/RemoteAgentTask.js'
import { isEnterpriseSubscriber, isTeamSubscriber } from '../../utils/auth.js'
import { detectCurrentRepositoryWithHost } from '../../utils/detectRepository.js'
import { execFileNoThrow } from '../../utils/execFileNoThrow.js'
import { getDefaultBranch, gitExe } from '../../utils/git.js'
import { teleportToRemote } from '../../utils/teleport.js'

// One-time session flag: once the user confirms overage billing via the
// dialog, all subsequent /ultrareview invocations in this session proceed
// without re-prompting.
let sessionOverageConfirmed = false

export function confirmOverage(): void {
  sessionOverageConfirmed = true
}

export type OverageGate =
  | { kind: 'proceed'; billingNote: string }
  | { kind: 'not-enabled' }
  | { kind: 'low-balance'; available: number }
  | { kind: 'needs-confirm' }

/**
 * Determine whether the user can launch an ultrareview and under what
 * billing terms. Fetches quota and utilization in parallel.

```

---


### `src/commands/review/ultrareviewCommand.tsx`

**信息:**
- 行数: 58
- 大小: 9855 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/messages.js';
import React from 'react';
import type { LocalJSXCommandCall, LocalJSXCommandOnDone } from '../../types/command.js';
import { checkOverageGate, confirmOverage, launchRemoteReview } from './reviewRemote.js';
import { UltrareviewOverageDialog } from './UltrareviewOverageDialog.js';
function contentBlocksToString(blocks: ContentBlockParam[]): string {
  return blocks.map(b => b.type === 'text' ? b.text : '').filter(Boolean).join('\n');
}
async function launchAndDone(args: string, context: Parameters<LocalJSXCommandCall>[1], onDone: LocalJSXCommandOnDone, billingNote: string, signal?: AbortSignal): Promise<void> {
  const result = await launchRemoteReview(args, context, billingNote);
  // User hit Escape during the ~5s launch — the dialog already showed
  // "cancelled" and unmounted, so skip onDone (would write to a dead
  // transcript slot) and let the caller skip confirmOverage.
  if (signal?.aborted) return;
  if (result) {
    onDone(contentBlocksToString(result), {
      shouldQuery: true
    });
  } else {
    // Precondition failures now return specific ContentBlockParam[] above.
    // null only reaches here on teleport failure (PR mode) or non-github
    // repo — both are CCR/repo connectivity issues.
    onDone('Ultrareview failed to launch the remote session. Check that this is a GitHub repo and try again.', {
      display: 'system'
    });
  }
}
export const call: LocalJSXCommandCall = async (onDone, context, args) => {
  const gate = await checkOverageGate();
  if (gate.kind === 'not-enabled') {
    onDone('Free ultrareviews used. Enable Extra Usage at https://claude.ai/settings/billing to continue.', {
      display: 'system'
    });
    return null;
  }
  if (gate.kind === 'low-balance') {
    onDone(`Balance too low to launch ultrareview ($${gate.available.toFixed(2)} available, $10 minimum). Top up at https://claude.ai/settings/billing`, {
      display: 'system'
    });
    return null;
  }
  if (gate.kind === 'needs-confirm') {
    return <UltrareviewOverageDialog onProceed={async signal => {
      await launchAndDone(args, context, onDone, ' This review bills as Extra Usage.', signal);
      // Only persist the confirmation flag after a non-aborted launch —
      // otherwise Escape-during-launch would leave the flag set and
      // skip this dialog on the next attempt.
      if (!signal.aborted) confirmOverage();
    }} onCancel={() => onDone('Ultrareview cancelled.', {
      display: 'system'

```

---


### `src/commands/review/ultrareviewEnabled.ts`

**信息:**
- 行数: 14
- 大小: 526 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'

/**
 * Runtime gate for /ultrareview. GB config's `enabled` field controls
 * visibility — isEnabled() on the command filters it from getCommands()
 * when false, so ungated users don't see the command at all.
 */
export function isUltrareviewEnabled(): boolean {
  const cfg = getFeatureValue_CACHED_MAY_BE_STALE<Record<
    string,
    unknown
  > | null>('tengu_review_bughunter_config', null)
  return cfg?.enabled === true
}

```

---


### `src/commands/review.ts`

**信息:**
- 行数: 57
- 大小: 2188 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/messages.js'
import type { Command } from '../commands.js'
import { isUltrareviewEnabled } from './review/ultrareviewEnabled.js'

// Legal wants the explicit surface name plus a docs link visible before the
// user triggers, so the description carries "Claude Code on the web" + URL.
const CCR_TERMS_URL = 'https://code.claude.com/docs/en/claude-code-on-the-web'

const LOCAL_REVIEW_PROMPT = (args: string) => `
      You are an expert code reviewer. Follow these steps:

      1. If no PR number is provided in the args, run \`gh pr list\` to show open PRs
      2. If a PR number is provided, run \`gh pr view <number>\` to get PR details
      3. Run \`gh pr diff <number>\` to get the diff
      4. Analyze the changes and provide a thorough code review that includes:
         - Overview of what the PR does
         - Analysis of code quality and style
         - Specific suggestions for improvements
         - Any potential issues or risks

      Keep your review concise but thorough. Focus on:
      - Code correctness
      - Following project conventions
      - Performance implications
      - Test coverage
      - Security considerations

      Format your review with clear sections and bullet points.

      PR number: ${args}
    `

const review: Command = {
  type: 'prompt',
  name: 'review',
  description: 'Review a pull request',
  progressMessage: 'reviewing pull request',
  contentLength: 0,
  source: 'builtin',
  async getPromptForCommand(args): Promise<ContentBlockParam[]> {
    return [{ type: 'text', text: LOCAL_REVIEW_PROMPT(args) }]
  },
}

// /ultrareview is the ONLY entry point to the remote bughunter path —
// /review stays purely local. local-jsx type renders the overage permission
// dialog when free reviews are exhausted.
const ultrareview: Command = {
  type: 'local-jsx',
  name: 'ultrareview',

```

---


### `src/commands/rewind/index.ts`

**信息:**
- 行数: 13
- 大小: 337 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const rewind = {
  description: `Restore the code and/or conversation to a previous point`,
  name: 'rewind',
  aliases: ['checkpoint'],
  argumentHint: '',
  type: 'local',
  supportsNonInteractive: false,
  load: () => import('./rewind.js'),
} satisfies Command

export default rewind

```

---


### `src/commands/rewind/rewind.ts`

**信息:**
- 行数: 13
- 大小: 376 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { LocalCommandResult } from '../../commands.js'
import type { ToolUseContext } from '../../Tool.js'

export async function call(
  _args: string,
  context: ToolUseContext,
): Promise<LocalCommandResult> {
  if (context.openMessageSelector) {
    context.openMessageSelector()
  }
  // Return a skip message to not append any messages.
  return { type: 'skip' }
}

```

---


### `src/commands/sandbox-toggle/index.ts`

**信息:**
- 行数: 50
- 大小: 1520 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import figures from 'figures'
import type { Command } from '../../commands.js'
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js'

const command = {
  name: 'sandbox',
  get description() {
    const currentlyEnabled = SandboxManager.isSandboxingEnabled()
    const autoAllow = SandboxManager.isAutoAllowBashIfSandboxedEnabled()
    const allowUnsandboxed = SandboxManager.areUnsandboxedCommandsAllowed()
    const isLocked = SandboxManager.areSandboxSettingsLockedByPolicy()
    const hasDeps = SandboxManager.checkDependencies().errors.length === 0

    // Show warning icon if dependencies missing, otherwise enabled/disabled status
    let icon: string
    if (!hasDeps) {
      icon = figures.warning
    } else {
      icon = currentlyEnabled ? figures.tick : figures.circle
    }

    let statusText = 'sandbox disabled'
    if (currentlyEnabled) {
      statusText = autoAllow
        ? 'sandbox enabled (auto-allow)'
        : 'sandbox enabled'

      // Add unsandboxed fallback status
      statusText += allowUnsandboxed ? ', fallback allowed' : ''
    }

    if (isLocked) {
      statusText += ' (managed)'
    }

    return `${icon} ${statusText} (⏎ to configure)`
  },
  argumentHint: 'exclude "command pattern"',
  get isHidden() {
    return (
      !SandboxManager.isSupportedPlatform() ||
      !SandboxManager.isPlatformInEnabledList()
    )
  },
  immediate: true,
  type: 'local-jsx',
  load: () => import('./sandbox-toggle.js'),
} satisfies Command

export default command

```

---


### `src/commands/sandbox-toggle/sandbox-toggle.tsx`

**信息:**
- 行数: 83
- 大小: 13157 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { relative } from 'path';
import React from 'react';
import { getCwdState } from '../../bootstrap/state.js';
import { SandboxSettings } from '../../components/sandbox/SandboxSettings.js';
import { color } from '../../ink.js';
import { getPlatform } from '../../utils/platform.js';
import { addToExcludedCommands, SandboxManager } from '../../utils/sandbox/sandbox-adapter.js';
import { getSettings_DEPRECATED, getSettingsFilePathForSource } from '../../utils/settings/settings.js';
import type { ThemeName } from '../../utils/theme.js';
export async function call(onDone: (result?: string) => void, _context: unknown, args?: string): Promise<React.ReactNode | null> {
  const settings = getSettings_DEPRECATED();
  const themeName: ThemeName = settings.theme as ThemeName || 'light';
  const platform = getPlatform();
  if (!SandboxManager.isSupportedPlatform()) {
    // WSL1 users will see this since isSupportedPlatform returns false for WSL1
    const errorMessage = platform === 'wsl' ? 'Error: Sandboxing requires WSL2. WSL1 is not supported.' : 'Error: Sandboxing is currently only supported on macOS, Linux, and WSL2.';
    const message = color('error', themeName)(errorMessage);
    onDone(message);
    return null;
  }

  // Check dependencies - get structured result with errors/warnings
  const depCheck = SandboxManager.checkDependencies();

  // Check if platform is in enabledPlatforms list (undocumented enterprise setting)
  if (!SandboxManager.isPlatformInEnabledList()) {
    const message = color('error', themeName)(`Error: Sandboxing is disabled for this platform (${platform}) via the enabledPlatforms setting.`);
    onDone(message);
    return null;
  }

  // Check if sandbox settings are locked by higher-priority settings
  if (SandboxManager.areSandboxSettingsLockedByPolicy()) {
    const message = color('error', themeName)('Error: Sandbox settings are overridden by a higher-priority configuration and cannot be changed locally.');
    onDone(message);
    return null;
  }

  // Parse the arguments
  const trimmedArgs = args?.trim() || '';

  // If no args, show the interactive menu
  if (!trimmedArgs) {
    return <SandboxSettings onComplete={onDone} depCheck={depCheck} />;
  }

  // Handle subcommands
  if (trimmedArgs) {
    const parts = trimmedArgs.split(' ');
    const subcommand = parts[0];

```

---


### `src/commands/security-review.ts`

**信息:**
- 行数: 243
- 大小: 12531 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { parseFrontmatter } from '../utils/frontmatterParser.js'
import { parseSlashCommandToolsFromFrontmatter } from '../utils/markdownConfigLoader.js'
import { executeShellCommandsInPrompt } from '../utils/promptShellExecution.js'
import { createMovedToPluginCommand } from './createMovedToPluginCommand.js'

const SECURITY_REVIEW_MARKDOWN = `---
allowed-tools: Bash(git diff:*), Bash(git status:*), Bash(git log:*), Bash(git show:*), Bash(git remote show:*), Read, Glob, Grep, LS, Task
description: Complete a security review of the pending changes on the current branch
---

You are a senior security engineer conducting a focused security review of the changes on this branch.

GIT STATUS:

\`\`\`
!\`git status\`
\`\`\`

FILES MODIFIED:

\`\`\`
!\`git diff --name-only origin/HEAD...\`
\`\`\`

COMMITS:

\`\`\`
!\`git log --no-decorate origin/HEAD...\`
\`\`\`

DIFF CONTENT:

\`\`\`
!\`git diff origin/HEAD...\`
\`\`\`

Review the complete diff above. This contains all code changes in the PR.


OBJECTIVE:
Perform a security-focused code review to identify HIGH-CONFIDENCE security vulnerabilities that could have real exploitation potential. This is not a general code review - focus ONLY on security implications newly added by this PR. Do not comment on existing security concerns.

CRITICAL INSTRUCTIONS:
1. MINIMIZE FALSE POSITIVES: Only flag issues where you're >80% confident of actual exploitability
2. AVOID NOISE: Skip theoretical issues, style concerns, or low-impact findings
3. FOCUS ON IMPACT: Prioritize vulnerabilities that could lead to unauthorized access, data breaches, or system compromise
4. EXCLUSIONS: Do NOT report the following issue types:
   - Denial of Service (DOS) vulnerabilities, even if they allow service disruption
   - Secrets or sensitive data stored on disk (these are handled by other processes)
   - Rate limiting or resource exhaustion issues

```

---


### `src/commands/session/index.ts`

**信息:**
- 行数: 16
- 大小: 418 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getIsRemoteMode } from '../../bootstrap/state.js'
import type { Command } from '../../commands.js'

const session = {
  type: 'local-jsx',
  name: 'session',
  aliases: ['remote'],
  description: 'Show remote session URL and QR code',
  isEnabled: () => getIsRemoteMode(),
  get isHidden() {
    return !getIsRemoteMode()
  },
  load: () => import('./session.js'),
} satisfies Command

export default session

```

---


### `src/commands/session/session.tsx`

**信息:**
- 行数: 140
- 大小: 13009 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { toString as qrToString } from 'qrcode';
import * as React from 'react';
import { useEffect, useState } from 'react';
import { Pane } from '../../components/design-system/Pane.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { useAppState } from '../../state/AppState.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
import { logForDebugging } from '../../utils/debug.js';
type Props = {
  onDone: () => void;
};
function SessionInfo(t0) {
  const $ = _c(19);
  const {
    onDone
  } = t0;
  const remoteSessionUrl = useAppState(_temp);
  const [qrCode, setQrCode] = useState("");
  let t1;
  let t2;
  if ($[0] !== remoteSessionUrl) {
    t1 = () => {
      if (!remoteSessionUrl) {
        return;
      }
      const url = remoteSessionUrl;
      const generateQRCode = async function generateQRCode() {
        const qr = await qrToString(url, {
          type: "utf8",
          errorCorrectionLevel: "L"
        });
        setQrCode(qr);
      };
      generateQRCode().catch(_temp2);
    };
    t2 = [remoteSessionUrl];
    $[0] = remoteSessionUrl;
    $[1] = t1;
    $[2] = t2;
  } else {
    t1 = $[1];
    t2 = $[2];
  }
  useEffect(t1, t2);
  let t3;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = {
      context: "Confirmation"

```

---


### `src/commands/skills/index.ts`

**信息:**
- 行数: 10
- 大小: 226 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const skills = {
  type: 'local-jsx',
  name: 'skills',
  description: 'List available skills',
  load: () => import('./skills.js'),
} satisfies Command

export default skills

```

---


### `src/commands/skills/skills.tsx`

**信息:**
- 行数: 8
- 大小: 1888 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import type { LocalJSXCommandContext } from '../../commands.js';
import { SkillsMenu } from '../../components/skills/SkillsMenu.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
export async function call(onDone: LocalJSXCommandOnDone, context: LocalJSXCommandContext): Promise<React.ReactNode> {
  return <SkillsMenu onExit={onDone} commands={context.options.commands} />;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkxvY2FsSlNYQ29tbWFuZENvbnRleHQiLCJTa2lsbHNNZW51IiwiTG9jYWxKU1hDb21tYW5kT25Eb25lIiwiY2FsbCIsIm9uRG9uZSIsImNvbnRleHQiLCJQcm9taXNlIiwiUmVhY3ROb2RlIiwib3B0aW9ucyIsImNvbW1hbmRzIl0sInNvdXJjZXMiOlsic2tpbGxzLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB0eXBlIHsgTG9jYWxKU1hDb21tYW5kQ29udGV4dCB9IGZyb20gJy4uLy4uL2NvbW1hbmRzLmpzJ1xuaW1wb3J0IHsgU2tpbGxzTWVudSB9IGZyb20gJy4uLy4uL2NvbXBvbmVudHMvc2tpbGxzL1NraWxsc01lbnUuanMnXG5pbXBvcnQgdHlwZSB7IExvY2FsSlNYQ29tbWFuZE9uRG9uZSB9IGZyb20gJy4uLy4uL3R5cGVzL2NvbW1hbmQuanMnXG5cbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBjYWxsKFxuICBvbkRvbmU6IExvY2FsSlNYQ29tbWFuZE9uRG9uZSxcbiAgY29udGV4dDogTG9jYWxKU1hDb21tYW5kQ29udGV4dCxcbik6IFByb21pc2U8UmVhY3QuUmVhY3ROb2RlPiB7XG4gIHJldHVybiA8U2tpbGxzTWVudSBvbkV4aXQ9e29uRG9uZX0gY29tbWFuZHM9e2NvbnRleHQub3B0aW9ucy5jb21tYW5kc30gLz5cbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixjQUFjQyxzQkFBc0IsUUFBUSxtQkFBbUI7QUFDL0QsU0FBU0MsVUFBVSxRQUFRLHVDQUF1QztBQUNsRSxjQUFjQyxxQkFBcUIsUUFBUSx3QkFBd0I7QUFFbkUsT0FBTyxlQUFlQyxJQUFJQSxDQUN4QkMsTUFBTSxFQUFFRixxQkFBcUIsRUFDN0JHLE9BQU8sRUFBRUwsc0JBQXNCLENBQ2hDLEVBQUVNLE9BQU8sQ0FBQ1AsS0FBSyxDQUFDUSxTQUFTLENBQUMsQ0FBQztFQUMxQixPQUFPLENBQUMsVUFBVSxDQUFDLE1BQU0sQ0FBQyxDQUFDSCxNQUFNLENBQUMsQ0FBQyxRQUFRLENBQUMsQ0FBQ0MsT0FBTyxDQUFDRyxPQUFPLENBQUNDLFFBQVEsQ0FBQyxHQUFHO0FBQzNFIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/stats/index.ts`

**信息:**
- 行数: 10
- 大小: 252 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const stats = {
  type: 'local-jsx',
  name: 'stats',
  description: 'Show your Claude Code usage statistics and activity',
  load: () => import('./stats.js'),
} satisfies Command

export default stats

```

---


### `src/commands/stats/stats.tsx`

**信息:**
- 行数: 7
- 大小: 1141 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { Stats } from '../../components/Stats.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
export const call: LocalJSXCommandCall = async onDone => {
  return <Stats onClose={onDone} />;
};
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlN0YXRzIiwiTG9jYWxKU1hDb21tYW5kQ2FsbCIsImNhbGwiLCJvbkRvbmUiXSwic291cmNlcyI6WyJzdGF0cy50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBTdGF0cyB9IGZyb20gJy4uLy4uL2NvbXBvbmVudHMvU3RhdHMuanMnXG5pbXBvcnQgdHlwZSB7IExvY2FsSlNYQ29tbWFuZENhbGwgfSBmcm9tICcuLi8uLi90eXBlcy9jb21tYW5kLmpzJ1xuXG5leHBvcnQgY29uc3QgY2FsbDogTG9jYWxKU1hDb21tYW5kQ2FsbCA9IGFzeW5jIG9uRG9uZSA9PiB7XG4gIHJldHVybiA8U3RhdHMgb25DbG9zZT17b25Eb25lfSAvPlxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLEtBQUssUUFBUSwyQkFBMkI7QUFDakQsY0FBY0MsbUJBQW1CLFFBQVEsd0JBQXdCO0FBRWpFLE9BQU8sTUFBTUMsSUFBSSxFQUFFRCxtQkFBbUIsR0FBRyxNQUFNRSxNQUFNLElBQUk7RUFDdkQsT0FBTyxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsQ0FBQ0EsTUFBTSxDQUFDLEdBQUc7QUFDbkMsQ0FBQyIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/commands/status/index.ts`

**信息:**
- 行数: 12
- 大小: 322 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const status = {
  type: 'local-jsx',
  name: 'status',
  description:
    'Show Claude Code status including version, model, account, API connectivity, and tool statuses',
  immediate: true,
  load: () => import('./status.js'),
} satisfies Command

export default status

```

---


### `src/commands/status/status.tsx`

**信息:**
- 行数: 8
- 大小: 1855 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import type { LocalJSXCommandContext } from '../../commands.js';
import { Settings } from '../../components/Settings/Settings.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
export async function call(onDone: LocalJSXCommandOnDone, context: LocalJSXCommandContext): Promise<React.ReactNode> {
  return <Settings onClose={onDone} context={context} defaultTab="Status" />;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkxvY2FsSlNYQ29tbWFuZENvbnRleHQiLCJTZXR0aW5ncyIsIkxvY2FsSlNYQ29tbWFuZE9uRG9uZSIsImNhbGwiLCJvbkRvbmUiLCJjb250ZXh0IiwiUHJvbWlzZSIsIlJlYWN0Tm9kZSJdLCJzb3VyY2VzIjpbInN0YXR1cy50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgdHlwZSB7IExvY2FsSlNYQ29tbWFuZENvbnRleHQgfSBmcm9tICcuLi8uLi9jb21tYW5kcy5qcydcbmltcG9ydCB7IFNldHRpbmdzIH0gZnJvbSAnLi4vLi4vY29tcG9uZW50cy9TZXR0aW5ncy9TZXR0aW5ncy5qcydcbmltcG9ydCB0eXBlIHsgTG9jYWxKU1hDb21tYW5kT25Eb25lIH0gZnJvbSAnLi4vLi4vdHlwZXMvY29tbWFuZC5qcydcblxuZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGNhbGwoXG4gIG9uRG9uZTogTG9jYWxKU1hDb21tYW5kT25Eb25lLFxuICBjb250ZXh0OiBMb2NhbEpTWENvbW1hbmRDb250ZXh0LFxuKTogUHJvbWlzZTxSZWFjdC5SZWFjdE5vZGU+IHtcbiAgcmV0dXJuIDxTZXR0aW5ncyBvbkNsb3NlPXtvbkRvbmV9IGNvbnRleHQ9e2NvbnRleHR9IGRlZmF1bHRUYWI9XCJTdGF0dXNcIiAvPlxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLGNBQWNDLHNCQUFzQixRQUFRLG1CQUFtQjtBQUMvRCxTQUFTQyxRQUFRLFFBQVEsdUNBQXVDO0FBQ2hFLGNBQWNDLHFCQUFxQixRQUFRLHdCQUF3QjtBQUVuRSxPQUFPLGVBQWVDLElBQUlBLENBQ3hCQyxNQUFNLEVBQUVGLHFCQUFxQixFQUM3QkcsT0FBTyxFQUFFTCxzQkFBc0IsQ0FDaEMsRUFBRU0sT0FBTyxDQUFDUCxLQUFLLENBQUNRLFNBQVMsQ0FBQyxDQUFDO0VBQzFCLE9BQU8sQ0FBQyxRQUFRLENBQUMsT0FBTyxDQUFDLENBQUNILE1BQU0sQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDQyxPQUFPLENBQUMsQ0FBQyxVQUFVLENBQUMsUUFBUSxHQUFHO0FBQzVFIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/statusline.tsx`

**信息:**
- 行数: 24
- 大小: 3568 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import type { Command } from '../commands.js';
import { AGENT_TOOL_NAME } from '../tools/AgentTool/constants.js';
const statusline = {
  type: 'prompt',
  description: "Set up Claude Code's status line UI",
  contentLength: 0,
  // Dynamic content
  aliases: [],
  name: 'statusline',
  progressMessage: 'setting up statusLine',
  allowedTools: [AGENT_TOOL_NAME, 'Read(~/**)', 'Edit(~/.claude/settings.json)'],
  source: 'builtin',
  disableNonInteractive: true,
  async getPromptForCommand(args): Promise<ContentBlockParam[]> {
    const prompt = args.trim() || 'Configure my statusLine from my shell PS1 configuration';
    return [{
      type: 'text',
      text: `Create an ${AGENT_TOOL_NAME} with subagent_type "statusline-setup" and the prompt "${prompt}"`
    }];
  }
} satisfies Command;
export default statusline;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJDb250ZW50QmxvY2tQYXJhbSIsIkNvbW1hbmQiLCJBR0VOVF9UT09MX05BTUUiLCJzdGF0dXNsaW5lIiwidHlwZSIsImRlc2NyaXB0aW9uIiwiY29udGVudExlbmd0aCIsImFsaWFzZXMiLCJuYW1lIiwicHJvZ3Jlc3NNZXNzYWdlIiwiYWxsb3dlZFRvb2xzIiwic291cmNlIiwiZGlzYWJsZU5vbkludGVyYWN0aXZlIiwiZ2V0UHJvbXB0Rm9yQ29tbWFuZCIsImFyZ3MiLCJQcm9taXNlIiwicHJvbXB0IiwidHJpbSIsInRleHQiXSwic291cmNlcyI6WyJzdGF0dXNsaW5lLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgdHlwZSB7IENvbnRlbnRCbG9ja1BhcmFtIH0gZnJvbSAnQGFudGhyb3BpYy1haS9zZGsvcmVzb3VyY2VzL2luZGV4Lm1qcydcbmltcG9ydCB0eXBlIHsgQ29tbWFuZCB9IGZyb20gJy4uL2NvbW1hbmRzLmpzJ1xuaW1wb3J0IHsgQUdFTlRfVE9PTF9OQU1FIH0gZnJvbSAnLi4vdG9vbHMvQWdlbnRUb29sL2NvbnN0YW50cy5qcydcblxuY29uc3Qgc3RhdHVzbGluZSA9IHtcbiAgdHlwZTogJ3Byb21wdCcsXG4gIGRlc2NyaXB0aW9uOiBcIlNldCB1cCBDbGF1ZGUgQ29kZSdzIHN0YXR1cyBsaW5lIFVJXCIsXG4gIGNvbnRlbnRMZW5ndGg6IDAsIC8vIER5bmFtaWMgY29udGVudFxuICBhbGlhc2VzOiBbXSxcbiAgbmFtZTogJ3N0YXR1c2xpbmUnLFxuICBwcm9ncmVzc01lc3NhZ2U6ICdzZXR0aW5nIHVwIHN0YXR1c0xpbmUnLFxuICBhbGxvd2VkVG9vbHM6IFtcbiAgICBBR0VOVF9UT09MX05BTUUsXG4gICAgJ1JlYWQofi8qKiknLFxuICAgICdFZGl0KH4vLmNsYXVkZS9zZXR0aW5ncy5qc29uKScsXG4gIF0sXG4gIHNvdXJjZTogJ2J1aWx0aW4nLFxuICBkaXNhYmxlTm9uSW50ZXJhY3RpdmU6IHRydWUsXG4gIGFzeW5jIGdldFByb21wdEZvckNvbW1hbmQoYXJncyk6IFByb21pc2U8Q29udGVudEJsb2NrUGFyYW1bXT4ge1xuICAgIGNvbnN0IHByb21wdCA9XG4gICAgICBhcmdzLnRyaW0oKSB8fCAnQ29uZmlndXJlIG15IHN0YXR1c0xpbmUgZnJvbSBteSBzaGVsbCBQUzEgY29uZmlndXJhdGlvbidcbiAgICByZXR1cm4gW1xuICAgICAge1xuICAgICAgICB0eXBlOiAndGV4dCcsXG4gICAgICAgIHRleHQ6IGBDcmVhdGUgYW4gJHtBR0VOVF9UT09MX05BTUV9IHdpdGggc3ViYWdlbnRfdHlwZSBcInN0YXR1c2xpbmUtc2V0dXBcIiBhbmQgdGhlIHByb21wdCBcIiR7cHJvbXB0fVwiYCxcbiAgICAgIH0sXG4gICAgXVxuICB9LFxufSBzYXRpc2ZpZXMgQ29tbWFuZFxuXG5leHBvcnQgZGVmYXVsdCBzdGF0dXNsaW5lXG4iXSwibWFwcGluZ3MiOiJBQUFBLGNBQWNBLGlCQUFpQixRQUFRLHVDQUF1QztBQUM5RSxjQUFjQyxPQUFPLFFBQVEsZ0JBQWdCO0FBQzdDLFNBQVNDLGVBQWUsUUFBUSxpQ0FBaUM7QUFFakUsTUFBTUMsVUFBVSxHQUFHO0VBQ2pCQyxJQUFJLEVBQUUsUUFBUTtFQUNkQyxXQUFXLEVBQUUscUNBQXFDO0VBQ2xEQyxhQUFhLEVBQUUsQ0FBQztFQUFFO0VBQ2xCQyxPQUFPLEVBQUUsRUFBRTtFQUNYQyxJQUFJLEVBQUUsWUFBWTtFQUNsQkMsZUFBZSxFQUFFLHVCQUF1QjtFQUN4Q0MsWUFBWSxFQUFFLENBQ1pSLGVBQWUsRUFDZixZQUFZLEVBQ1osK0JBQStCLENBQ2hDO0VBQ0RTLE1BQU0sRUFBRSxTQUFTO0VBQ2pCQyxxQkFBcUIsRUFBRSxJQUFJO0VBQzNCLE1BQU1DLG1CQUFtQkEsQ0FBQ0MsSUFBSSxDQUFDLEVBQUVDLE9BQU8sQ0FBQ2YsaUJBQWlCLEVBQUUsQ0FBQyxDQUFDO0lBQzVELE1BQU1nQixNQUFNLEdBQ1ZGLElBQUksQ0FBQ0csSUFBSSxDQUFDLENBQUMsSUFBSSx5REFBeUQ7SUFDMUUsT0FBTyxDQUNMO01BQ0ViLElBQUksRUFBRSxNQUFNO01BQ1pjLElBQUksRUFBRSxhQUFhaEIsZUFBZSwwREFBMERjLE1BQU07SUFDcEcsQ0FBQyxDQUNGO0VBQ0g7QUFDRixDQUFDLFdBQVdmLE9BQU87QUFFbkIsZUFBZUUsVUFBVSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/commands/stickers/index.ts`

**信息:**
- 行数: 11
- 大小: 268 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const stickers = {
  type: 'local',
  name: 'stickers',
  description: 'Order Claude Code stickers',
  supportsNonInteractive: false,
  load: () => import('./stickers.js'),
} satisfies Command

export default stickers

```

---


### `src/commands/stickers/stickers.ts`

**信息:**
- 行数: 16
- 大小: 476 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { LocalCommandResult } from '../../types/command.js'
import { openBrowser } from '../../utils/browser.js'

export async function call(): Promise<LocalCommandResult> {
  const url = 'https://www.stickermule.com/claudecode'
  const success = await openBrowser(url)

  if (success) {
    return { type: 'text', value: 'Opening sticker page in browser…' }
  } else {
    return {
      type: 'text',
      value: `Failed to open browser. Visit: ${url}`,
    }
  }
}

```

---


### `src/commands/tag/index.ts`

**信息:**
- 行数: 12
- 大小: 321 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const tag = {
  type: 'local-jsx',
  name: 'tag',
  description: 'Toggle a searchable tag on the current session',
  isEnabled: () => process.env.USER_TYPE === 'ant',
  argumentHint: '<tag-name>',
  load: () => import('./tag.js'),
} satisfies Command

export default tag

```

---


### `src/commands/tag/tag.tsx`

**信息:**
- 行数: 215
- 大小: 20999 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import type { UUID } from 'crypto';
import * as React from 'react';
import { getSessionId } from '../../bootstrap/state.js';
import type { CommandResultDisplay } from '../../commands.js';
import { Select } from '../../components/CustomSelect/select.js';
import { Dialog } from '../../components/design-system/Dialog.js';
import { COMMON_HELP_ARGS, COMMON_INFO_ARGS } from '../../constants/xml.js';
import { Box, Text } from '../../ink.js';
import { logEvent } from '../../services/analytics/index.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { recursivelySanitizeUnicode } from '../../utils/sanitization.js';
import { getCurrentSessionTag, getTranscriptPath, saveTag } from '../../utils/sessionStorage.js';
function ConfirmRemoveTag(t0) {
  const $ = _c(11);
  const {
    tagName,
    onConfirm,
    onCancel
  } = t0;
  const t1 = `Current tag: #${tagName}`;
  let t2;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Text>This will remove the tag from the current session.</Text>;
    $[0] = t2;
  } else {
    t2 = $[0];
  }
  let t3;
  if ($[1] !== onCancel || $[2] !== onConfirm) {
    t3 = value => value === "yes" ? onConfirm() : onCancel();
    $[1] = onCancel;
    $[2] = onConfirm;
    $[3] = t3;
  } else {
    t3 = $[3];
  }
  let t4;
  if ($[4] === Symbol.for("react.memo_cache_sentinel")) {
    t4 = [{
      label: "Yes, remove tag",
      value: "yes"
    }, {
      label: "No, keep tag",
      value: "no"
    }];
    $[4] = t4;
  } else {
    t4 = $[4];

```

---


### `src/commands/tasks/index.ts`

**信息:**
- 行数: 11
- 大小: 256 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const tasks = {
  type: 'local-jsx',
  name: 'tasks',
  aliases: ['bashes'],
  description: 'List and manage background tasks',
  load: () => import('./tasks.js'),
} satisfies Command

export default tasks

```

---


### `src/commands/tasks/tasks.tsx`

**信息:**
- 行数: 8
- 大小: 1901 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import type { LocalJSXCommandContext } from '../../commands.js';
import { BackgroundTasksDialog } from '../../components/tasks/BackgroundTasksDialog.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
export async function call(onDone: LocalJSXCommandOnDone, context: LocalJSXCommandContext): Promise<React.ReactNode> {
  return <BackgroundTasksDialog toolUseContext={context} onDone={onDone} />;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkxvY2FsSlNYQ29tbWFuZENvbnRleHQiLCJCYWNrZ3JvdW5kVGFza3NEaWFsb2ciLCJMb2NhbEpTWENvbW1hbmRPbkRvbmUiLCJjYWxsIiwib25Eb25lIiwiY29udGV4dCIsIlByb21pc2UiLCJSZWFjdE5vZGUiXSwic291cmNlcyI6WyJ0YXNrcy50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgdHlwZSB7IExvY2FsSlNYQ29tbWFuZENvbnRleHQgfSBmcm9tICcuLi8uLi9jb21tYW5kcy5qcydcbmltcG9ydCB7IEJhY2tncm91bmRUYXNrc0RpYWxvZyB9IGZyb20gJy4uLy4uL2NvbXBvbmVudHMvdGFza3MvQmFja2dyb3VuZFRhc2tzRGlhbG9nLmpzJ1xuaW1wb3J0IHR5cGUgeyBMb2NhbEpTWENvbW1hbmRPbkRvbmUgfSBmcm9tICcuLi8uLi90eXBlcy9jb21tYW5kLmpzJ1xuXG5leHBvcnQgYXN5bmMgZnVuY3Rpb24gY2FsbChcbiAgb25Eb25lOiBMb2NhbEpTWENvbW1hbmRPbkRvbmUsXG4gIGNvbnRleHQ6IExvY2FsSlNYQ29tbWFuZENvbnRleHQsXG4pOiBQcm9taXNlPFJlYWN0LlJlYWN0Tm9kZT4ge1xuICByZXR1cm4gPEJhY2tncm91bmRUYXNrc0RpYWxvZyB0b29sVXNlQ29udGV4dD17Y29udGV4dH0gb25Eb25lPXtvbkRvbmV9IC8+XG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsY0FBY0Msc0JBQXNCLFFBQVEsbUJBQW1CO0FBQy9ELFNBQVNDLHFCQUFxQixRQUFRLGlEQUFpRDtBQUN2RixjQUFjQyxxQkFBcUIsUUFBUSx3QkFBd0I7QUFFbkUsT0FBTyxlQUFlQyxJQUFJQSxDQUN4QkMsTUFBTSxFQUFFRixxQkFBcUIsRUFDN0JHLE9BQU8sRUFBRUwsc0JBQXNCLENBQ2hDLEVBQUVNLE9BQU8sQ0FBQ1AsS0FBSyxDQUFDUSxTQUFTLENBQUMsQ0FBQztFQUMxQixPQUFPLENBQUMscUJBQXFCLENBQUMsY0FBYyxDQUFDLENBQUNGLE9BQU8sQ0FBQyxDQUFDLE1BQU0sQ0FBQyxDQUFDRCxNQUFNLENBQUMsR0FBRztBQUMzRSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/commands/terminalSetup/index.ts`

**信息:**
- 行数: 23
- 大小: 725 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { env } from '../../utils/env.js'

// Terminals that natively support CSI u / Kitty keyboard protocol
const NATIVE_CSIU_TERMINALS: Record<string, string> = {
  ghostty: 'Ghostty',
  kitty: 'Kitty',
  'iTerm.app': 'iTerm2',
  WezTerm: 'WezTerm',
}

const terminalSetup = {
  type: 'local-jsx',
  name: 'terminal-setup',
  description:
    env.terminal === 'Apple_Terminal'
      ? 'Enable Option+Enter key binding for newlines and visual bell'
      : 'Install Shift+Enter key binding for newlines',
  isHidden: env.terminal !== null && env.terminal in NATIVE_CSIU_TERMINALS,
  load: () => import('./terminalSetup.js'),
} satisfies Command

export default terminalSetup

```

---


### `src/commands/terminalSetup/terminalSetup.tsx`

**信息:**
- 行数: 531
- 大小: 77528 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import chalk from 'chalk';
import { randomBytes } from 'crypto';
import { copyFile, mkdir, readFile, writeFile } from 'fs/promises';
import { homedir, platform } from 'os';
import { dirname, join } from 'path';
import type { ThemeName } from 'src/utils/theme.js';
import { pathToFileURL } from 'url';
import { supportsHyperlinks } from '../../ink/supports-hyperlinks.js';
import { color } from '../../ink.js';
import { maybeMarkProjectOnboardingComplete } from '../../projectOnboardingState.js';
import type { ToolUseContext } from '../../Tool.js';
import type { LocalJSXCommandContext, LocalJSXCommandOnDone } from '../../types/command.js';
import { backupTerminalPreferences, checkAndRestoreTerminalBackup, getTerminalPlistPath, markTerminalSetupComplete } from '../../utils/appleTerminalBackup.js';
import { setupShellCompletion } from '../../utils/completionCache.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { env } from '../../utils/env.js';
import { isFsInaccessible } from '../../utils/errors.js';
import { execFileNoThrow } from '../../utils/execFileNoThrow.js';
import { addItemToJSONCArray, safeParseJSONC } from '../../utils/json.js';
import { logError } from '../../utils/log.js';
import { getPlatform } from '../../utils/platform.js';
import { jsonParse, jsonStringify } from '../../utils/slowOperations.js';
const EOL = '\n';

// Terminals that natively support CSI u / Kitty keyboard protocol
const NATIVE_CSIU_TERMINALS: Record<string, string> = {
  ghostty: 'Ghostty',
  kitty: 'Kitty',
  'iTerm.app': 'iTerm2',
  WezTerm: 'WezTerm',
  WarpTerminal: 'Warp'
};

/**
 * Detect if we're running in a VSCode Remote SSH session.
 * In this case, keybindings need to be installed on the LOCAL machine,
 * not the remote server where Claude is running.
 */
function isVSCodeRemoteSSH(): boolean {
  const askpassMain = process.env.VSCODE_GIT_ASKPASS_MAIN ?? '';
  const path = process.env.PATH ?? '';

  // Check both env vars - VSCODE_GIT_ASKPASS_MAIN is more reliable when git extension
  // is active, and PATH is a fallback. Omit path separator for Windows compatibility.
  return askpassMain.includes('.vscode-server') || askpassMain.includes('.cursor-server') || askpassMain.includes('.windsurf-server') || path.includes('.vscode-server') || path.includes('.cursor-server') || path.includes('.windsurf-server');
}
export function getNativeCSIuTerminalDisplayName(): string | null {
  if (!env.terminal || !(env.terminal in NATIVE_CSIU_TERMINALS)) {
    return null;
  }

```

---


### `src/commands/theme/index.ts`

**信息:**
- 行数: 10
- 大小: 217 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const theme = {
  type: 'local-jsx',
  name: 'theme',
  description: 'Change the theme',
  load: () => import('./theme.js'),
} satisfies Command

export default theme

```

---


### `src/commands/theme/theme.tsx`

**信息:**
- 行数: 57
- 大小: 5180 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { Pane } from '../../components/design-system/Pane.js';
import { ThemePicker } from '../../components/ThemePicker.js';
import { useTheme } from '../../ink.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
type Props = {
  onDone: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
function ThemePickerCommand(t0) {
  const $ = _c(8);
  const {
    onDone
  } = t0;
  const [, setTheme] = useTheme();
  let t1;
  if ($[0] !== onDone || $[1] !== setTheme) {
    t1 = setting => {
      setTheme(setting);
      onDone(`Theme set to ${setting}`);
    };
    $[0] = onDone;
    $[1] = setTheme;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  let t2;
  if ($[3] !== onDone) {
    t2 = () => {
      onDone("Theme picker dismissed", {
        display: "system"
      });
    };
    $[3] = onDone;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  let t3;
  if ($[5] !== t1 || $[6] !== t2) {
    t3 = <Pane color="permission"><ThemePicker onThemeSelect={t1} onCancel={t2} skipExitHandling={true} /></Pane>;
    $[5] = t1;
    $[6] = t2;
    $[7] = t3;
  } else {
    t3 = $[7];

```

---


### `src/commands/thinkback/index.ts`

**信息:**
- 行数: 13
- 大小: 442 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { checkStatsigFeatureGate_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'

const thinkback = {
  type: 'local-jsx',
  name: 'think-back',
  description: 'Your 2025 Claude Code Year in Review',
  isEnabled: () =>
    checkStatsigFeatureGate_CACHED_MAY_BE_STALE('tengu_thinkback'),
  load: () => import('./thinkback.js'),
} satisfies Command

export default thinkback

```

---


### `src/commands/thinkback/thinkback.tsx`

**信息:**
- 行数: 554
- 大小: 61993 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { execa } from 'execa';
import { readFile } from 'fs/promises';
import { join } from 'path';
import * as React from 'react';
import { useCallback, useEffect, useState } from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { Select } from '../../components/CustomSelect/select.js';
import { Dialog } from '../../components/design-system/Dialog.js';
import { Spinner } from '../../components/Spinner.js';
import instances from '../../ink/instances.js';
import { Box, Text } from '../../ink.js';
import { enablePluginOp } from '../../services/plugins/pluginOperations.js';
import { logForDebugging } from '../../utils/debug.js';
import { isENOENT, toError } from '../../utils/errors.js';
import { execFileNoThrow } from '../../utils/execFileNoThrow.js';
import { pathExists } from '../../utils/file.js';
import { logError } from '../../utils/log.js';
import { getPlatform } from '../../utils/platform.js';
import { clearAllCaches } from '../../utils/plugins/cacheUtils.js';
import { isPluginInstalled } from '../../utils/plugins/installedPluginsManager.js';
import { addMarketplaceSource, clearMarketplacesCache, loadKnownMarketplacesConfig, refreshMarketplace } from '../../utils/plugins/marketplaceManager.js';
import { OFFICIAL_MARKETPLACE_NAME } from '../../utils/plugins/officialMarketplace.js';
import { loadAllPlugins } from '../../utils/plugins/pluginLoader.js';
import { installSelectedPlugins } from '../../utils/plugins/pluginStartupCheck.js';

// Marketplace and plugin identifiers - varies by user type
const INTERNAL_MARKETPLACE_NAME = 'claude-code-marketplace';
const INTERNAL_MARKETPLACE_REPO = 'anthropics/claude-code-marketplace';
const OFFICIAL_MARKETPLACE_REPO = 'anthropics/claude-plugins-official';
function getMarketplaceName(): string {
  return "external" === 'ant' ? INTERNAL_MARKETPLACE_NAME : OFFICIAL_MARKETPLACE_NAME;
}
function getMarketplaceRepo(): string {
  return "external" === 'ant' ? INTERNAL_MARKETPLACE_REPO : OFFICIAL_MARKETPLACE_REPO;
}
function getPluginId(): string {
  return `thinkback@${getMarketplaceName()}`;
}
const SKILL_NAME = 'thinkback';

/**
 * Get the thinkback skill directory from the installed plugin's cache path
 */
async function getThinkbackSkillDir(): Promise<string | null> {
  const {
    enabled
  } = await loadAllPlugins();
  const thinkbackPlugin = enabled.find(p => p.name === 'thinkback' || p.source && p.source.includes(getPluginId()));
  if (!thinkbackPlugin) {

```

---


### `src/commands/thinkback-play/index.ts`

**信息:**
- 行数: 17
- 大小: 608 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { checkStatsigFeatureGate_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'

// Hidden command that just plays the animation
// Called by the thinkback skill after generation is complete
const thinkbackPlay = {
  type: 'local',
  name: 'thinkback-play',
  description: 'Play the thinkback animation',
  isEnabled: () =>
    checkStatsigFeatureGate_CACHED_MAY_BE_STALE('tengu_thinkback'),
  isHidden: true,
  supportsNonInteractive: false,
  load: () => import('./thinkback-play.js'),
} satisfies Command

export default thinkbackPlay

```

---


### `src/commands/thinkback-play/thinkback-play.ts`

**信息:**
- 行数: 43
- 大小: 1430 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { join } from 'path'
import type { LocalCommandResult } from '../../commands.js'
import { loadInstalledPluginsV2 } from '../../utils/plugins/installedPluginsManager.js'
import { OFFICIAL_MARKETPLACE_NAME } from '../../utils/plugins/officialMarketplace.js'
import { playAnimation } from '../thinkback/thinkback.js'

const INTERNAL_MARKETPLACE_NAME = 'claude-code-marketplace'
const SKILL_NAME = 'thinkback'

function getPluginId(): string {
  const marketplaceName =
    process.env.USER_TYPE === 'ant'
      ? INTERNAL_MARKETPLACE_NAME
      : OFFICIAL_MARKETPLACE_NAME
  return `thinkback@${marketplaceName}`
}

export async function call(): Promise<LocalCommandResult> {
  // Get skill directory from installed plugins config
  const v2Data = loadInstalledPluginsV2()
  const pluginId = getPluginId()
  const installations = v2Data.plugins[pluginId]

  if (!installations || installations.length === 0) {
    return {
      type: 'text' as const,
      value:
        'Thinkback plugin not installed. Run /think-back first to install it.',
    }
  }

  const firstInstall = installations[0]
  if (!firstInstall?.installPath) {
    return {
      type: 'text' as const,
      value: 'Thinkback plugin installation path not found.',
    }
  }

  const skillDir = join(firstInstall.installPath, 'skills', SKILL_NAME)
  const result = await playAnimation(skillDir)
  return { type: 'text' as const, value: result.message }
}

```

---


### `src/commands/ultraplan.tsx`

**信息:**
- 行数: 471
- 大小: 66629 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { readFileSync } from 'fs';
import { REMOTE_CONTROL_DISCONNECTED_MSG } from '../bridge/types.js';
import type { Command } from '../commands.js';
import { DIAMOND_OPEN } from '../constants/figures.js';
import { getRemoteSessionUrl } from '../constants/product.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../services/analytics/index.js';
import type { AppState } from '../state/AppStateStore.js';
import { checkRemoteAgentEligibility, formatPreconditionError, RemoteAgentTask, type RemoteAgentTaskState, registerRemoteAgentTask } from '../tasks/RemoteAgentTask/RemoteAgentTask.js';
import type { LocalJSXCommandCall } from '../types/command.js';
import { logForDebugging } from '../utils/debug.js';
import { errorMessage } from '../utils/errors.js';
import { logError } from '../utils/log.js';
import { enqueuePendingNotification } from '../utils/messageQueueManager.js';
import { ALL_MODEL_CONFIGS } from '../utils/model/configs.js';
import { updateTaskState } from '../utils/task/framework.js';
import { archiveRemoteSession, teleportToRemote } from '../utils/teleport.js';
import { pollForApprovedExitPlanMode, UltraplanPollError } from '../utils/ultraplan/ccrSession.js';

// TODO(prod-hardening): OAuth token may go stale over the 30min poll;
// consider refresh.

// Multi-agent exploration is slow; 30min timeout.
const ULTRAPLAN_TIMEOUT_MS = 30 * 60 * 1000;
export const CCR_TERMS_URL = 'https://code.claude.com/docs/en/claude-code-on-the-web';

// CCR runs against the first-party API — use the canonical ID, not the
// provider-specific string getModelStrings() would return (which may be a
// Bedrock ARN or Vertex ID on the local CLI). Read at call time, not module
// load: the GrowthBook cache is empty at import and `/config` Gates can flip
// it between invocations.
function getUltraplanModel(): string {
  return getFeatureValue_CACHED_MAY_BE_STALE('tengu_ultraplan_model', ALL_MODEL_CONFIGS.opus46.firstParty);
}

// prompt.txt is wrapped in <system-reminder> so the CCR browser hides
// scaffolding (CLI_BLOCK_TAGS dropped by stripSystemNotifications)
// while the model still sees full text.
// Phrasing deliberately avoids the feature name because
// the remote CCR CLI runs keyword detection on raw input before
// any tag stripping, and a bare "ultraplan" in the prompt would self-trigger as
// /ultraplan, which is filtered out of headless mode as "Unknown skill"
//
// Bundler inlines .txt as a string; the test runner wraps it as {default}.
/* eslint-disable @typescript-eslint/no-require-imports */
const _rawPrompt = require('../utils/ultraplan/prompt.txt');
/* eslint-enable @typescript-eslint/no-require-imports */
const DEFAULT_INSTRUCTIONS: string = (typeof _rawPrompt === 'string' ? _rawPrompt : _rawPrompt.default).trimEnd();

// Dev-only prompt override resolved eagerly at module load.

```

---


### `src/commands/upgrade/index.ts`

**信息:**
- 行数: 16
- 大小: 523 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import { getSubscriptionType } from '../../utils/auth.js'
import { isEnvTruthy } from '../../utils/envUtils.js'

const upgrade = {
  type: 'local-jsx',
  name: 'upgrade',
  description: 'Upgrade to Max for higher rate limits and more Opus',
  availability: ['claude-ai'],
  isEnabled: () =>
    !isEnvTruthy(process.env.DISABLE_UPGRADE_COMMAND) &&
    getSubscriptionType() !== 'enterprise',
  load: () => import('./upgrade.js'),
} satisfies Command

export default upgrade

```

---


### `src/commands/upgrade/upgrade.tsx`

**信息:**
- 行数: 38
- 大小: 7438 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import type { LocalJSXCommandContext } from '../../commands.js';
import { getOauthProfileFromOauthToken } from '../../services/oauth/getOauthProfile.js';
import type { LocalJSXCommandOnDone } from '../../types/command.js';
import { getClaudeAIOAuthTokens, isClaudeAISubscriber } from '../../utils/auth.js';
import { openBrowser } from '../../utils/browser.js';
import { logError } from '../../utils/log.js';
import { Login } from '../login/login.js';
export async function call(onDone: LocalJSXCommandOnDone, context: LocalJSXCommandContext): Promise<React.ReactNode | null> {
  try {
    // Check if user is already on the highest Max plan (20x)
    if (isClaudeAISubscriber()) {
      const tokens = getClaudeAIOAuthTokens();
      let isMax20x = false;
      if (tokens?.subscriptionType && tokens?.rateLimitTier) {
        isMax20x = tokens.subscriptionType === 'max' && tokens.rateLimitTier === 'default_claude_max_20x';
      } else if (tokens?.accessToken) {
        const profile = await getOauthProfileFromOauthToken(tokens.accessToken);
        isMax20x = profile?.organization?.organization_type === 'claude_max' && profile?.organization?.rate_limit_tier === 'default_claude_max_20x';
      }
      if (isMax20x) {
        setTimeout(onDone, 0, 'You are already on the highest Max subscription plan. For additional usage, run /login to switch to an API usage-billed account.');
        return null;
      }
    }
    const url = 'https://claude.ai/upgrade/max';
    await openBrowser(url);
    return <Login startingMessage={'Starting new login following /upgrade. Exit with Ctrl-C to use existing account.'} onDone={success => {
      context.onChangeAPIKey();
      onDone(success ? 'Login successful' : 'Login interrupted');
    }} />;
  } catch (error) {
    logError(error as Error);
    setTimeout(onDone, 0, 'Failed to open browser. Please visit https://claude.ai/upgrade/max to upgrade.');
  }
  return null;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkxvY2FsSlNYQ29tbWFuZENvbnRleHQiLCJnZXRPYXV0aFByb2ZpbGVGcm9tT2F1dGhUb2tlbiIsIkxvY2FsSlNYQ29tbWFuZE9uRG9uZSIsImdldENsYXVkZUFJT0F1dGhUb2tlbnMiLCJpc0NsYXVkZUFJU3Vic2NyaWJlciIsIm9wZW5Ccm93c2VyIiwibG9nRXJyb3IiLCJMb2dpbiIsImNhbGwiLCJvbkRvbmUiLCJjb250ZXh0IiwiUHJvbWlzZSIsIlJlYWN0Tm9kZSIsInRva2VucyIsImlzTWF4MjB4Iiwic3Vic2NyaXB0aW9uVHlwZSIsInJhdGVMaW1pdFRpZXIiLCJhY2Nlc3NUb2tlbiIsInByb2ZpbGUiLCJvcmdhbml6YXRpb24iLCJvcmdhbml6YXRpb25fdHlwZSIsInJhdGVfbGltaXRfdGllciIsInNldFRpbWVvdXQiLCJ1cmwiLCJzdWNjZXNzIiwib25DaGFuZ2VBUElLZXkiLCJlcnJvciIsIkVycm9yIl0sInNvdXJjZXMiOlsidXBncmFkZS50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgdHlwZSB7IExvY2FsSlNYQ29tbWFuZENvbnRleHQgfSBmcm9tICcuLi8uLi9jb21tYW5kcy5qcydcbmltcG9ydCB7IGdldE9hdXRoUHJvZmlsZUZyb21PYXV0aFRva2VuIH0gZnJvbSAnLi4vLi4vc2VydmljZXMvb2F1dGgvZ2V0T2F1dGhQcm9maWxlLmpzJ1xuaW1wb3J0IHR5cGUgeyBMb2NhbEpTWENvbW1hbmRPbkRvbmUgfSBmcm9tICcuLi8uLi90eXBlcy9jb21tYW5kLmpzJ1xuaW1wb3J0IHtcbiAgZ2V0Q2xhdWRlQUlPQXV0aFRva2VucyxcbiAgaXNDbGF1ZGVBSVN1YnNjcmliZXIsXG59IGZyb20gJy4uLy4uL3V0aWxzL2F1dGguanMnXG5pbXBvcnQgeyBvcGVuQnJvd3NlciB9IGZyb20gJy4uLy4uL3V0aWxzL2Jyb3dzZXIuanMnXG5pbXBvcnQgeyBsb2dFcnJvciB9IGZyb20gJy4uLy4uL3V0aWxzL2xvZy5qcydcbmltcG9ydCB7IExvZ2luIH0gZnJvbSAnLi4vbG9naW4vbG9naW4uanMnXG5cbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBjYWxsKFxuICBvbkRvbmU6IExvY2FsSlNYQ29tbWFuZE9uRG9uZSxcbiAgY29udGV4dDogTG9jYWxKU1hDb21tYW5kQ29udGV4dCxcbik6IFByb21pc2U8UmVhY3QuUmVhY3ROb2RlIHwgbnVsbD4ge1xuICB0cnkge1xuICAgIC8vIENoZWNrIGlmIHVzZXIgaXMgYWxyZWFkeSBvbiB0aGUgaGlnaGVzdCBNYXggcGxhbiAoMjB4KVxuICAgIGlmIChpc0NsYXVkZUFJU3Vic2NyaWJlcigpKSB7XG4gICAgICBjb25zdCB0b2tlbnMgPSBnZXRDbGF1ZGVBSU9BdXRoVG9rZW5zKClcbiAgICAgIGxldCBpc01heDIweCA9IGZhbHNlXG5cbiAgICAgIGlmICh0b2tlbnM/LnN1YnNjcmlwdGlvblR5cGUgJiYgdG9rZW5zPy5yYXRlTGltaXRUaWVyKSB7XG4gICAgICAgIGlzTWF4MjB4ID1cbiAgICAgICAgICB0b2tlbnMuc3Vic2NyaXB0aW9uVHlwZSA9PT0gJ21heCcgJiZcbiAgICAgICAgICB0b2tlbnMucmF0ZUxpbWl0VGllciA9PT0gJ2RlZmF1bHRfY2xhdWRlX21heF8yMHgnXG4gICAgICB9IGVsc2UgaWYgKHRva2Vucz8uYWNjZXNzVG9rZW4pIHtcbiAgICAgICAgY29uc3QgcHJvZmlsZSA9IGF3YWl0IGdldE9hdXRoUHJvZmlsZUZyb21PYXV0aFRva2VuKHRva2Vucy5hY2Nlc3NUb2tlbilcbiAgICAgICAgaXNNYXgyMHggPVxuICAgICAgICAgIHByb2ZpbGU/Lm9yZ2FuaXphdGlvbj8ub3JnYW5pemF0aW9uX3R5cGUgPT09ICdjbGF1ZGVfbWF4JyAmJlxuICAgICAgICAgIHByb2ZpbGU/Lm9yZ2FuaXphdGlvbj8ucmF0ZV9saW1pdF90aWVyID09PSAnZGVmYXVsdF9jbGF1ZGVfbWF4XzIweCdcbiAgICAgIH1cblxuICAgICAgaWYgKGlzTWF4MjB4KSB7XG4gICAgICAgIHNldFRpbWVvdXQoXG4gICAgICAgICAgb25Eb25lLFxuICAgICAgICAgIDAsXG4gICAgICAgICAgJ1lvdSBhcmUgYWxyZWFkeSBvbiB0aGUgaGlnaGVzdCBNYXggc3Vic2NyaXB0aW9uIHBsYW4uIEZvciBhZGRpdGlvbmFsIHVzYWdlLCBydW4gL2xvZ2luIHRvIHN3aXRjaCB0byBhbiBBUEkgdXNhZ2UtYmlsbGVkIGFjY291bnQuJyxcbiAgICAgICAgKVxuICAgICAgICByZXR1cm4gbnVsbFxuICAgICAgfVxuICAgIH1cblxuICAgIGNvbnN0IHVybCA9ICdodHRwczovL2NsYXVkZS5haS91cGdyYWRlL21heCdcbiAgICBhd2FpdCBvcGVuQnJvd3Nlcih1cmwpXG5cbiAgICByZXR1cm4gKFxuICAgICAgPExvZ2luXG4gICAgICAgIHN0YXJ0aW5nTWVzc2FnZT17XG4gICAgICAgICAgJ1N0YXJ0aW5nIG5ldyBsb2dpbiBmb2xsb3dpbmcgL3VwZ3JhZGUuIEV4aXQgd2l0aCBDdHJsLUMgdG8gdXNlIGV4aXN0aW5nIGFjY291bnQuJ1xuICAgICAgICB9XG4gICAgICAgIG9uRG9uZT17c3VjY2VzcyA9PiB7XG4gICAgICAgICAgY29udGV4dC5vbkNoYW5nZUFQSUtleSgpXG4gICAgICAgICAgb25Eb25lKHN1Y2Nlc3MgPyAnTG9naW4gc3VjY2Vzc2Z1bCcgOiAnTG9naW4gaW50ZXJydXB0ZWQnKVxuICAgICAgICB9fVxuICAgICAgLz5cbiAgICApXG4gIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgbG9nRXJyb3IoZXJyb3IgYXMgRXJyb3IpXG4gICAgc2V0VGltZW91dChcbiAgICAgIG9uRG9uZSxcbiAgICAgIDAsXG4gICAgICAnRmFpbGVkIHRvIG9wZW4gYnJvd3Nlci4gUGxlYXNlIHZpc2l0IGh0dHBzOi8vY2xhdWRlLmFpL3VwZ3JhZGUvbWF4IHRvIHVwZ3JhZGUuJyxcbiAgICApXG4gIH1cbiAgcmV0dXJuIG51bGxcbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixjQUFjQyxzQkFBc0IsUUFBUSxtQkFBbUI7QUFDL0QsU0FBU0MsNkJBQTZCLFFBQVEseUNBQXlDO0FBQ3ZGLGNBQWNDLHFCQUFxQixRQUFRLHdCQUF3QjtBQUNuRSxTQUNFQyxzQkFBc0IsRUFDdEJDLG9CQUFvQixRQUNmLHFCQUFxQjtBQUM1QixTQUFTQyxXQUFXLFFBQVEsd0JBQXdCO0FBQ3BELFNBQVNDLFFBQVEsUUFBUSxvQkFBb0I7QUFDN0MsU0FBU0MsS0FBSyxRQUFRLG1CQUFtQjtBQUV6QyxPQUFPLGVBQWVDLElBQUlBLENBQ3hCQyxNQUFNLEVBQUVQLHFCQUFxQixFQUM3QlEsT0FBTyxFQUFFVixzQkFBc0IsQ0FDaEMsRUFBRVcsT0FBTyxDQUFDWixLQUFLLENBQUNhLFNBQVMsR0FBRyxJQUFJLENBQUMsQ0FBQztFQUNqQyxJQUFJO0lBQ0Y7SUFDQSxJQUFJUixvQkFBb0IsQ0FBQyxDQUFDLEVBQUU7TUFDMUIsTUFBTVMsTUFBTSxHQUFHVixzQkFBc0IsQ0FBQyxDQUFDO01BQ3ZDLElBQUlXLFFBQVEsR0FBRyxLQUFLO01BRXBCLElBQUlELE1BQU0sRUFBRUUsZ0JBQWdCLElBQUlGLE1BQU0sRUFBRUcsYUFBYSxFQUFFO1FBQ3JERixRQUFRLEdBQ05ELE1BQU0sQ0FBQ0UsZ0JBQWdCLEtBQUssS0FBSyxJQUNqQ0YsTUFBTSxDQUFDRyxhQUFhLEtBQUssd0JBQXdCO01BQ3JELENBQUMsTUFBTSxJQUFJSCxNQUFNLEVBQUVJLFdBQVcsRUFBRTtRQUM5QixNQUFNQyxPQUFPLEdBQUcsTUFBTWpCLDZCQUE2QixDQUFDWSxNQUFNLENBQUNJLFdBQVcsQ0FBQztRQUN2RUgsUUFBUSxHQUNOSSxPQUFPLEVBQUVDLFlBQVksRUFBRUMsaUJBQWlCLEtBQUssWUFBWSxJQUN6REYsT0FBTyxFQUFFQyxZQUFZLEVBQUVFLGVBQWUsS0FBSyx3QkFBd0I7TUFDdkU7TUFFQSxJQUFJUCxRQUFRLEVBQUU7UUFDWlEsVUFBVSxDQUNSYixNQUFNLEVBQ04sQ0FBQyxFQUNELGtJQUNGLENBQUM7UUFDRCxPQUFPLElBQUk7TUFDYjtJQUNGO0lBRUEsTUFBTWMsR0FBRyxHQUFHLCtCQUErQjtJQUMzQyxNQUFNbEIsV0FBVyxDQUFDa0IsR0FBRyxDQUFDO0lBRXRCLE9BQ0UsQ0FBQyxLQUFLLENBQ0osZUFBZSxDQUFDLENBQ2Qsa0ZBQ0YsQ0FBQyxDQUNELE1BQU0sQ0FBQyxDQUFDQyxPQUFPLElBQUk7TUFDakJkLE9BQU8sQ0FBQ2UsY0FBYyxDQUFDLENBQUM7TUFDeEJoQixNQUFNLENBQUNlLE9BQU8sR0FBRyxrQkFBa0IsR0FBRyxtQkFBbUIsQ0FBQztJQUM1RCxDQUFDLENBQUMsR0FDRjtFQUVOLENBQUMsQ0FBQyxPQUFPRSxLQUFLLEVBQUU7SUFDZHBCLFFBQVEsQ0FBQ29CLEtBQUssSUFBSUMsS0FBSyxDQUFDO0lBQ3hCTCxVQUFVLENBQ1JiLE1BQU0sRUFDTixDQUFDLEVBQ0QsZ0ZBQ0YsQ0FBQztFQUNIO0VBQ0EsT0FBTyxJQUFJO0FBQ2IiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/commands/usage/index.ts`

**信息:**
- 行数: 9
- 大小: 233 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

export default {
  type: 'local-jsx',
  name: 'usage',
  description: 'Show plan usage limits',
  availability: ['claude-ai'],
  load: () => import('./usage.js'),
} satisfies Command

```

---


### `src/commands/usage/usage.tsx`

**信息:**
- 行数: 7
- 大小: 1403 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { Settings } from '../../components/Settings/Settings.js';
import type { LocalJSXCommandCall } from '../../types/command.js';
export const call: LocalJSXCommandCall = async (onDone, context) => {
  return <Settings onClose={onDone} context={context} defaultTab="Usage" />;
};
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlNldHRpbmdzIiwiTG9jYWxKU1hDb21tYW5kQ2FsbCIsImNhbGwiLCJvbkRvbmUiLCJjb250ZXh0Il0sInNvdXJjZXMiOlsidXNhZ2UudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgU2V0dGluZ3MgfSBmcm9tICcuLi8uLi9jb21wb25lbnRzL1NldHRpbmdzL1NldHRpbmdzLmpzJ1xuaW1wb3J0IHR5cGUgeyBMb2NhbEpTWENvbW1hbmRDYWxsIH0gZnJvbSAnLi4vLi4vdHlwZXMvY29tbWFuZC5qcydcblxuZXhwb3J0IGNvbnN0IGNhbGw6IExvY2FsSlNYQ29tbWFuZENhbGwgPSBhc3luYyAob25Eb25lLCBjb250ZXh0KSA9PiB7XG4gIHJldHVybiA8U2V0dGluZ3Mgb25DbG9zZT17b25Eb25lfSBjb250ZXh0PXtjb250ZXh0fSBkZWZhdWx0VGFiPVwiVXNhZ2VcIiAvPlxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLFFBQVEsUUFBUSx1Q0FBdUM7QUFDaEUsY0FBY0MsbUJBQW1CLFFBQVEsd0JBQXdCO0FBRWpFLE9BQU8sTUFBTUMsSUFBSSxFQUFFRCxtQkFBbUIsR0FBRyxNQUFBQyxDQUFPQyxNQUFNLEVBQUVDLE9BQU8sS0FBSztFQUNsRSxPQUFPLENBQUMsUUFBUSxDQUFDLE9BQU8sQ0FBQyxDQUFDRCxNQUFNLENBQUMsQ0FBQyxPQUFPLENBQUMsQ0FBQ0MsT0FBTyxDQUFDLENBQUMsVUFBVSxDQUFDLE9BQU8sR0FBRztBQUMzRSxDQUFDIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/commands/version.ts`

**信息:**
- 行数: 22
- 大小: 577 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command, LocalCommandCall } from '../types/command.js'

const call: LocalCommandCall = async () => {
  return {
    type: 'text',
    value: MACRO.BUILD_TIME
      ? `${MACRO.VERSION} (built ${MACRO.BUILD_TIME})`
      : MACRO.VERSION,
  }
}

const version = {
  type: 'local',
  name: 'version',
  description:
    'Print the version this session is running (not what autoupdate downloaded)',
  isEnabled: () => process.env.USER_TYPE === 'ant',
  supportsNonInteractive: true,
  load: () => Promise.resolve({ call }),
} satisfies Command

export default version

```

---


### `src/commands/vim/index.ts`

**信息:**
- 行数: 11
- 大小: 273 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'

const command = {
  name: 'vim',
  description: 'Toggle between Vim and Normal editing modes',
  supportsNonInteractive: false,
  type: 'local',
  load: () => import('./vim.js'),
} satisfies Command

export default command

```

---


### `src/commands/vim/vim.ts`

**信息:**
- 行数: 38
- 大小: 1139 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import type { LocalCommandCall } from '../../types/command.js'
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js'

export const call: LocalCommandCall = async () => {
  const config = getGlobalConfig()
  let currentMode = config.editorMode || 'normal'

  // Handle backward compatibility - treat 'emacs' as 'normal'
  if (currentMode === 'emacs') {
    currentMode = 'normal'
  }

  const newMode = currentMode === 'normal' ? 'vim' : 'normal'

  saveGlobalConfig(current => ({
    ...current,
    editorMode: newMode,
  }))

  logEvent('tengu_editor_mode_changed', {
    mode: newMode as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
    source:
      'command' as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  })

  return {
    type: 'text',
    value: `Editor mode set to ${newMode}. ${
      newMode === 'vim'
        ? 'Use Escape key to toggle between INSERT and NORMAL modes.'
        : 'Using standard (readline) keyboard bindings.'
    }`,
  }
}

```

---


### `src/commands/voice/index.ts`

**信息:**
- 行数: 20
- 大小: 482 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../commands.js'
import {
  isVoiceGrowthBookEnabled,
  isVoiceModeEnabled,
} from '../../voice/voiceModeEnabled.js'

const voice = {
  type: 'local',
  name: 'voice',
  description: 'Toggle voice mode',
  availability: ['claude-ai'],
  isEnabled: () => isVoiceGrowthBookEnabled(),
  get isHidden() {
    return !isVoiceModeEnabled()
  },
  supportsNonInteractive: false,
  load: () => import('./voice.js'),
} satisfies Command

export default voice

```

---


### `src/commands/voice/voice.ts`

**信息:**
- 行数: 150
- 大小: 5264 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { normalizeLanguageForSTT } from '../../hooks/useVoice.js'
import { getShortcutDisplay } from '../../keybindings/shortcutFormat.js'
import { logEvent } from '../../services/analytics/index.js'
import type { LocalCommandCall } from '../../types/command.js'
import { isAnthropicAuthEnabled } from '../../utils/auth.js'
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js'
import { settingsChangeDetector } from '../../utils/settings/changeDetector.js'
import {
  getInitialSettings,
  updateSettingsForSource,
} from '../../utils/settings/settings.js'
import { isVoiceModeEnabled } from '../../voice/voiceModeEnabled.js'

const LANG_HINT_MAX_SHOWS = 2

export const call: LocalCommandCall = async () => {
  // Check auth and kill-switch before allowing voice mode
  if (!isVoiceModeEnabled()) {
    // Differentiate: OAuth-less users get an auth hint, everyone else
    // gets nothing (command shouldn't be reachable when the kill-switch is on).
    if (!isAnthropicAuthEnabled()) {
      return {
        type: 'text' as const,
        value:
          'Voice mode requires a Claude.ai account. Please run /login to sign in.',
      }
    }
    return {
      type: 'text' as const,
      value: 'Voice mode is not available.',
    }
  }

  const currentSettings = getInitialSettings()
  const isCurrentlyEnabled = currentSettings.voiceEnabled === true

  // Toggle OFF — no checks needed
  if (isCurrentlyEnabled) {
    const result = updateSettingsForSource('userSettings', {
      voiceEnabled: false,
    })
    if (result.error) {
      return {
        type: 'text' as const,
        value:
          'Failed to update settings. Check your settings file for syntax errors.',
      }
    }
    settingsChangeDetector.notifyChange('userSettings')
    logEvent('tengu_voice_toggled', { enabled: false })

```

---

