# screens 模块

## 概述

**位置:** `src/screens/`

## 文件统计

- TypeScript 文件: 0
- TypeScript React 文件: 3
- 总计: 3

## 文件详情

---


### `src/screens/Doctor.tsx`

**信息:**
- 行数: 575
- 大小: 73277 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import { join } from 'path';
import React, { Suspense, use, useCallback, useEffect, useMemo, useState } from 'react';
import { KeybindingWarnings } from 'src/components/KeybindingWarnings.js';
import { McpParsingWarnings } from 'src/components/mcp/McpParsingWarnings.js';
import { getModelMaxOutputTokens } from 'src/utils/context.js';
import { getClaudeConfigHomeDir } from 'src/utils/envUtils.js';
import type { SettingSource } from 'src/utils/settings/constants.js';
import { getOriginalCwd } from '../bootstrap/state.js';
import type { CommandResultDisplay } from '../commands.js';
import { Pane } from '../components/design-system/Pane.js';
import { PressEnterToContinue } from '../components/PressEnterToContinue.js';
import { SandboxDoctorSection } from '../components/sandbox/SandboxDoctorSection.js';
import { ValidationErrorsList } from '../components/ValidationErrorsList.js';
import { useSettingsErrors } from '../hooks/notifs/useSettingsErrors.js';
import { useExitOnCtrlCDWithKeybindings } from '../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Text } from '../ink.js';
import { useKeybindings } from '../keybindings/useKeybinding.js';
import { useAppState } from '../state/AppState.js';
import { getPluginErrorMessage } from '../types/plugin.js';
import { getGcsDistTags, getNpmDistTags, type NpmDistTags } from '../utils/autoUpdater.js';
import { type ContextWarnings, checkContextWarnings } from '../utils/doctorContextWarnings.js';
import { type DiagnosticInfo, getDoctorDiagnostic } from '../utils/doctorDiagnostic.js';
import { validateBoundedIntEnvVar } from '../utils/envValidation.js';
import { pathExists } from '../utils/file.js';
import { cleanupStaleLocks, getAllLockInfo, isPidBasedLockingEnabled, type LockInfo } from '../utils/nativeInstaller/pidLock.js';
import { getInitialSettings } from '../utils/settings/settings.js';
import { BASH_MAX_OUTPUT_DEFAULT, BASH_MAX_OUTPUT_UPPER_LIMIT } from '../utils/shell/outputLimits.js';
import { TASK_MAX_OUTPUT_DEFAULT, TASK_MAX_OUTPUT_UPPER_LIMIT } from '../utils/task/outputFormatting.js';
import { getXDGStateHome } from '../utils/xdg.js';
type Props = {
  onDone: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
type AgentInfo = {
  activeAgents: Array<{
    agentType: string;
    source: SettingSource | 'built-in' | 'plugin';
  }>;
  userAgentsDir: string;
  projectAgentsDir: string;
  userDirExists: boolean;
  projectDirExists: boolean;
  failedFiles?: Array<{
    path: string;
    error: string;
  }>;
};

```

---


### `src/screens/REPL.tsx`

**信息:**
- 行数: 5061
- 大小: 897875 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
import { feature } from 'bun:bundle';
import { spawnSync } from 'child_process';
import { snapshotOutputTokensForTurn, getCurrentTurnTokenBudget, getTurnOutputTokens, getBudgetContinuationCount, getTotalInputTokens } from '../bootstrap/state.js';
import { parseTokenBudget } from '../utils/tokenBudget.js';
import { count } from '../utils/array.js';
import { dirname, join } from 'path';
import { tmpdir } from 'os';
import figures from 'figures';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- / n N Esc [ v are bare letters in transcript modal context, same class as g/G/j/k in ScrollKeybindingHandler
import { useInput } from '../ink.js';
import { useSearchInput } from '../hooks/useSearchInput.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { useSearchHighlight } from '../ink/hooks/use-search-highlight.js';
import type { JumpHandle } from '../components/VirtualMessageList.js';
import { renderMessagesToPlainText } from '../utils/exportRenderer.js';
import { openFileInExternalEditor } from '../utils/editor.js';
import { writeFile } from 'fs/promises';
import { Box, Text, useStdin, useTheme, useTerminalFocus, useTerminalTitle, useTabStatus } from '../ink.js';
import type { TabStatusKind } from '../ink/hooks/use-tab-status.js';
import { CostThresholdDialog } from '../components/CostThresholdDialog.js';
import { IdleReturnDialog } from '../components/IdleReturnDialog.js';
import * as React from 'react';
import { useEffect, useMemo, useRef, useState, useCallback, useDeferredValue, useLayoutEffect, type RefObject } from 'react';
import { useNotifications } from '../context/notifications.js';
import { sendNotification } from '../services/notifier.js';
import { startPreventSleep, stopPreventSleep } from '../services/preventSleep.js';
import { useTerminalNotification } from '../ink/useTerminalNotification.js';
import { hasCursorUpViewportYankBug } from '../ink/terminal.js';
import { createFileStateCacheWithSizeLimit, mergeFileStateCaches, READ_FILE_STATE_CACHE_SIZE } from '../utils/fileStateCache.js';
import { updateLastInteractionTime, getLastInteractionTime, getOriginalCwd, getProjectRoot, getSessionId, switchSession, setCostStateForRestore, getTurnHookDurationMs, getTurnHookCount, resetTurnHookDuration, getTurnToolDurationMs, getTurnToolCount, resetTurnToolDuration, getTurnClassifierDurationMs, getTurnClassifierCount, resetTurnClassifierDuration } from '../bootstrap/state.js';
import { asSessionId, asAgentId } from '../types/ids.js';
import { logForDebugging } from '../utils/debug.js';
import { QueryGuard } from '../utils/QueryGuard.js';
import { isEnvTruthy } from '../utils/envUtils.js';
import { formatTokens, truncateToWidth } from '../utils/format.js';
import { consumeEarlyInput } from '../utils/earlyInput.js';
import { setMemberActive } from '../utils/swarm/teamHelpers.js';
import { isSwarmWorker, generateSandboxRequestId, sendSandboxPermissionRequestViaMailbox, sendSandboxPermissionResponseViaMailbox } from '../utils/swarm/permissionSync.js';
import { registerSandboxPermissionCallback } from '../hooks/useSwarmPermissionPoller.js';
import { getTeamName, getAgentName } from '../utils/teammate.js';
import { WorkerPendingPermission } from '../components/permissions/WorkerPendingPermission.js';
import { injectUserMessageToTeammate, getAllInProcessTeammateTasks } from '../tasks/InProcessTeammateTask/InProcessTeammateTask.js';
import { isLocalAgentTask, queuePendingMessage, appendMessageToLocalAgent, type LocalAgentTaskState } from '../tasks/LocalAgentTask/LocalAgentTask.js';
import { registerLeaderToolUseConfirmQueue, unregisterLeaderToolUseConfirmQueue, registerLeaderSetToolPermissionContext, unregisterLeaderSetToolPermissionContext } from '../utils/swarm/leaderPermissionBridge.js';
import { endInteractionSpan } from '../utils/telemetry/sessionTracing.js';
import { useLogMessages } from '../hooks/useLogMessages.js';
import { useReplBridge } from '../hooks/useReplBridge.js';
import { type Command, type CommandResultDisplay, type ResumeEntrypoint, getCommandName, isCommandEnabled } from '../commands.js';

```

---


### `src/screens/ResumeConversation.tsx`

**信息:**
- 行数: 399
- 大小: 59682 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import { dirname } from 'path';
import React from 'react';
import { useTerminalSize } from 'src/hooks/useTerminalSize.js';
import { getOriginalCwd, switchSession } from '../bootstrap/state.js';
import type { Command } from '../commands.js';
import { LogSelector } from '../components/LogSelector.js';
import { Spinner } from '../components/Spinner.js';
import { restoreCostStateForSession } from '../cost-tracker.js';
import { setClipboard } from '../ink/termio/osc.js';
import { Box, Text } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../services/analytics/index.js';
import type { MCPServerConnection, ScopedMcpServerConfig } from '../services/mcp/types.js';
import { useAppState, useSetAppState } from '../state/AppState.js';
import type { Tool } from '../Tool.js';
import type { AgentColorName } from '../tools/AgentTool/agentColorManager.js';
import type { AgentDefinition } from '../tools/AgentTool/loadAgentsDir.js';
import { asSessionId } from '../types/ids.js';
import type { LogOption } from '../types/logs.js';
import type { Message } from '../types/message.js';
import { agenticSessionSearch } from '../utils/agenticSessionSearch.js';
import { renameRecordingForSession } from '../utils/asciicast.js';
import { updateSessionName } from '../utils/concurrentSessions.js';
import { loadConversationForResume } from '../utils/conversationRecovery.js';
import { checkCrossProjectResume } from '../utils/crossProjectResume.js';
import type { FileHistorySnapshot } from '../utils/fileHistory.js';
import { logError } from '../utils/log.js';
import { createSystemMessage } from '../utils/messages.js';
import { computeStandaloneAgentContext, restoreAgentFromSession, restoreWorktreeForResume } from '../utils/sessionRestore.js';
import { adoptResumedSessionFile, enrichLogs, isCustomTitleEnabled, loadAllProjectsMessageLogsProgressive, loadSameRepoMessageLogsProgressive, recordContentReplacement, resetSessionFilePointer, restoreSessionMetadata, type SessionLogResult } from '../utils/sessionStorage.js';
import type { ThinkingConfig } from '../utils/thinking.js';
import type { ContentReplacementRecord } from '../utils/toolResultStorage.js';
import { REPL } from './REPL.js';
function parsePrIdentifier(value: string): number | null {
  const directNumber = parseInt(value, 10);
  if (!isNaN(directNumber) && directNumber > 0) {
    return directNumber;
  }
  const urlMatch = value.match(/github\.com\/[^/]+\/[^/]+\/pull\/(\d+)/);
  if (urlMatch?.[1]) {
    return parseInt(urlMatch[1], 10);
  }
  return null;
}
type Props = {
  commands: Command[];
  worktreePaths: string[];
  initialTools: Tool[];

```

---

