# hooks 模块

## 概述

**位置:** `src/hooks/`

## 文件统计

- TypeScript 文件: 77
- TypeScript React 文件: 28
- 总计: 105

## 文件详情

---


### `src/hooks/fileSuggestions.ts`

**信息:**
- 行数: 811
- 大小: 27152 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { statSync } from 'fs'
import ignore from 'ignore'
import * as path from 'path'
import {
  CLAUDE_CONFIG_DIRECTORIES,
  loadMarkdownFilesForSubdir,
} from 'src/utils/markdownConfigLoader.js'
import type { SuggestionItem } from '../components/PromptInput/PromptInputFooterSuggestions.js'
import {
  CHUNK_MS,
  FileIndex,
  yieldToEventLoop,
} from '../native-ts/file-index/index.js'
import { logEvent } from '../services/analytics/index.js'
import type { FileSuggestionCommandInput } from '../types/fileSuggestion.js'
import { getGlobalConfig } from '../utils/config.js'
import { getCwd } from '../utils/cwd.js'
import { logForDebugging } from '../utils/debug.js'
import { errorMessage } from '../utils/errors.js'
import { execFileNoThrowWithCwd } from '../utils/execFileNoThrow.js'
import { getFsImplementation } from '../utils/fsOperations.js'
import { findGitRoot, gitExe } from '../utils/git.js'
import {
  createBaseHookInput,
  executeFileSuggestionCommand,
} from '../utils/hooks.js'
import { logError } from '../utils/log.js'
import { expandPath } from '../utils/path.js'
import { ripGrep } from '../utils/ripgrep.js'
import { getInitialSettings } from '../utils/settings/settings.js'
import { createSignal } from '../utils/signal.js'

// Lazily constructed singleton
let fileIndex: FileIndex | null = null

function getFileIndex(): FileIndex {
  if (!fileIndex) {
    fileIndex = new FileIndex()
  }
  return fileIndex
}

let fileListRefreshPromise: Promise<FileIndex> | null = null
// Signal fired when an in-progress index build completes. Lets the
// typeahead UI re-run its last search so partial results upgrade to full.
const indexBuildComplete = createSignal()
export const onIndexBuildComplete = indexBuildComplete.subscribe
let cacheGeneration = 0

// Background fetch for untracked files

```

---


### `src/hooks/notifs/useAntOrgWarningNotification.ts`

**信息:**
- 行数: 1
- 大小: 56 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function useAntOrgWarningNotification(): void {}

```

---


### `src/hooks/notifs/useAutoModeUnavailableNotification.ts`

**信息:**
- 行数: 56
- 大小: 1965 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { useEffect, useRef } from 'react'
import { useNotifications } from 'src/context/notifications.js'
import { getIsRemoteMode } from '../../bootstrap/state.js'
import { useAppState } from '../../state/AppState.js'
import type { PermissionMode } from '../../utils/permissions/PermissionMode.js'
import {
  getAutoModeUnavailableNotification,
  getAutoModeUnavailableReason,
} from '../../utils/permissions/permissionSetup.js'
import { hasAutoModeOptIn } from '../../utils/settings/settings.js'

/**
 * Shows a one-shot notification when the shift-tab carousel wraps past where
 * auto mode would have been. Covers all reasons (settings, circuit-breaker,
 * org-allowlist). The startup case (defaultMode: auto silently downgraded) is
 * handled by verifyAutoModeGateAccess → checkAndDisableAutoModeIfNeeded.
 */
export function useAutoModeUnavailableNotification(): void {
  const { addNotification } = useNotifications()
  const mode = useAppState(s => s.toolPermissionContext.mode)
  const isAutoModeAvailable = useAppState(
    s => s.toolPermissionContext.isAutoModeAvailable,
  )
  const shownRef = useRef(false)
  const prevModeRef = useRef<PermissionMode>(mode)

  useEffect(() => {
    const prevMode = prevModeRef.current
    prevModeRef.current = mode

    if (!feature('TRANSCRIPT_CLASSIFIER')) return
    if (getIsRemoteMode()) return
    if (shownRef.current) return

    const wrappedPastAutoSlot =
      mode === 'default' &&
      prevMode !== 'default' &&
      prevMode !== 'auto' &&
      !isAutoModeAvailable &&
      hasAutoModeOptIn()

    if (!wrappedPastAutoSlot) return

    const reason = getAutoModeUnavailableReason()
    if (!reason) return

    shownRef.current = true
    addNotification({
      key: 'auto-mode-unavailable',

```

---


### `src/hooks/notifs/useCanSwitchToExistingSubscription.tsx`

**信息:**
- 行数: 60
- 大小: 7274 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { getOauthProfileFromApiKey } from 'src/services/oauth/getOauthProfile.js';
import { isClaudeAISubscriber } from 'src/utils/auth.js';
import { Text } from '../../ink.js';
import { logEvent } from '../../services/analytics/index.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { useStartupNotification } from './useStartupNotification.js';
const MAX_SHOW_COUNT = 3;

/**
 * Hook to check if the user has a subscription on Console but isn't logged into it.
 */
export function useCanSwitchToExistingSubscription() {
  useStartupNotification(_temp2);
}

/**
 * Checks if the user has a subscription but is not currently logged into it.
 * This helps inform users they should run /login to access their subscription.
 */
async function _temp2() {
  if ((getGlobalConfig().subscriptionNoticeCount ?? 0) >= MAX_SHOW_COUNT) {
    return null;
  }
  const subscriptionType = await getExistingClaudeSubscription();
  if (subscriptionType === null) {
    return null;
  }
  saveGlobalConfig(_temp);
  logEvent("tengu_switch_to_subscription_notice_shown", {});
  return {
    key: "switch-to-subscription",
    jsx: <Text color="suggestion">Use your existing Claude {subscriptionType} plan with Claude Code<Text color="text" dimColor={true}>{" "}· /login to activate</Text></Text>,
    priority: "low"
  };
}
function _temp(current) {
  return {
    ...current,
    subscriptionNoticeCount: (current.subscriptionNoticeCount ?? 0) + 1
  };
}
async function getExistingClaudeSubscription(): Promise<'Max' | 'Pro' | null> {
  // If already using subscription auth, there is nothing to switch to
  if (isClaudeAISubscriber()) {
    return null;
  }
  const profile = await getOauthProfileFromApiKey();
  if (!profile) {
    return null;

```

---


### `src/hooks/notifs/useDeprecationWarningNotification.tsx`

**信息:**
- 行数: 44
- 大小: 4605 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { useEffect, useRef } from 'react';
import { useNotifications } from 'src/context/notifications.js';
import { getModelDeprecationWarning } from 'src/utils/model/deprecation.js';
import { getIsRemoteMode } from '../../bootstrap/state.js';
export function useDeprecationWarningNotification(model) {
  const $ = _c(4);
  const {
    addNotification
  } = useNotifications();
  const lastWarningRef = useRef(null);
  let t0;
  let t1;
  if ($[0] !== addNotification || $[1] !== model) {
    t0 = () => {
      if (getIsRemoteMode()) {
        return;
      }
      const deprecationWarning = getModelDeprecationWarning(model);
      if (deprecationWarning && deprecationWarning !== lastWarningRef.current) {
        lastWarningRef.current = deprecationWarning;
        addNotification({
          key: "model-deprecation-warning",
          text: deprecationWarning,
          color: "warning",
          priority: "high"
        });
      }
      if (!deprecationWarning) {
        lastWarningRef.current = null;
      }
    };
    t1 = [model, addNotification];
    $[0] = addNotification;
    $[1] = model;
    $[2] = t0;
    $[3] = t1;
  } else {
    t0 = $[2];
    t1 = $[3];
  }
  useEffect(t0, t1);
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJ1c2VFZmZlY3QiLCJ1c2VSZWYiLCJ1c2VOb3RpZmljYXRpb25zIiwiZ2V0TW9kZWxEZXByZWNhdGlvbldhcm5pbmciLCJnZXRJc1JlbW90ZU1vZGUiLCJ1c2VEZXByZWNhdGlvbldhcm5pbmdOb3RpZmljYXRpb24iLCJtb2RlbCIsIiQiLCJfYyIsImFkZE5vdGlmaWNhdGlvbiIsImxhc3RXYXJuaW5nUmVmIiwidDAiLCJ0MSIsImRlcHJlY2F0aW9uV2FybmluZyIsImN1cnJlbnQiLCJrZXkiLCJ0ZXh0IiwiY29sb3IiLCJwcmlvcml0eSJdLCJzb3VyY2VzIjpbInVzZURlcHJlY2F0aW9uV2FybmluZ05vdGlmaWNhdGlvbi50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgdXNlRWZmZWN0LCB1c2VSZWYgfSBmcm9tICdyZWFjdCdcbmltcG9ydCB7IHVzZU5vdGlmaWNhdGlvbnMgfSBmcm9tICdzcmMvY29udGV4dC9ub3RpZmljYXRpb25zLmpzJ1xuaW1wb3J0IHsgZ2V0TW9kZWxEZXByZWNhdGlvbldhcm5pbmcgfSBmcm9tICdzcmMvdXRpbHMvbW9kZWwvZGVwcmVjYXRpb24uanMnXG5pbXBvcnQgeyBnZXRJc1JlbW90ZU1vZGUgfSBmcm9tICcuLi8uLi9ib290c3RyYXAvc3RhdGUuanMnXG5cbmV4cG9ydCBmdW5jdGlvbiB1c2VEZXByZWNhdGlvbldhcm5pbmdOb3RpZmljYXRpb24obW9kZWw6IHN0cmluZyk6IHZvaWQge1xuICBjb25zdCB7IGFkZE5vdGlmaWNhdGlvbiB9ID0gdXNlTm90aWZpY2F0aW9ucygpXG4gIGNvbnN0IGxhc3RXYXJuaW5nUmVmID0gdXNlUmVmPHN0cmluZyB8IG51bGw+KG51bGwpXG5cbiAgdXNlRWZmZWN0KCgpID0+IHtcbiAgICBpZiAoZ2V0SXNSZW1vdGVNb2RlKCkpIHJldHVyblxuICAgIGNvbnN0IGRlcHJlY2F0aW9uV2FybmluZyA9IGdldE1vZGVsRGVwcmVjYXRpb25XYXJuaW5nKG1vZGVsKVxuXG4gICAgLy8gU2hvdyB3YXJuaW5nIGlmIG1vZGVsIGlzIGRlcHJlY2F0ZWQgYW5kIHdlIGhhdmVuJ3Qgc2hvd24gdGhpcyBleGFjdCB3YXJuaW5nIHlldFxuICAgIGlmIChkZXByZWNhdGlvbldhcm5pbmcgJiYgZGVwcmVjYXRpb25XYXJuaW5nICE9PSBsYXN0V2FybmluZ1JlZi5jdXJyZW50KSB7XG4gICAgICBsYXN0V2FybmluZ1JlZi5jdXJyZW50ID0gZGVwcmVjYXRpb25XYXJuaW5nXG4gICAgICBhZGROb3RpZmljYXRpb24oe1xuICAgICAgICBrZXk6ICdtb2RlbC1kZXByZWNhdGlvbi13YXJuaW5nJyxcbiAgICAgICAgdGV4dDogZGVwcmVjYXRpb25XYXJuaW5nLFxuICAgICAgICBjb2xvcjogJ3dhcm5pbmcnLFxuICAgICAgICBwcmlvcml0eTogJ2hpZ2gnLFxuICAgICAgfSlcbiAgICB9XG5cbiAgICAvLyBSZXNldCB0cmFja2luZyBpZiBtb2RlbCBjaGFuZ2VzIHRvIG5vbi1kZXByZWNhdGVkXG4gICAgaWYgKCFkZXByZWNhdGlvbldhcm5pbmcpIHtcbiAgICAgIGxhc3RXYXJuaW5nUmVmLmN1cnJlbnQgPSBudWxsXG4gICAgfVxuICB9LCBbbW9kZWwsIGFkZE5vdGlmaWNhdGlvbl0pXG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxTQUFTQSxTQUFTLEVBQUVDLE1BQU0sUUFBUSxPQUFPO0FBQ3pDLFNBQVNDLGdCQUFnQixRQUFRLDhCQUE4QjtBQUMvRCxTQUFTQywwQkFBMEIsUUFBUSxnQ0FBZ0M7QUFDM0UsU0FBU0MsZUFBZSxRQUFRLDBCQUEwQjtBQUUxRCxPQUFPLFNBQUFDLGtDQUFBQyxLQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQ0w7SUFBQUM7RUFBQSxJQUE0QlAsZ0JBQWdCLENBQUMsQ0FBQztFQUM5QyxNQUFBUSxjQUFBLEdBQXVCVCxNQUFNLENBQWdCLElBQUksQ0FBQztFQUFBLElBQUFVLEVBQUE7RUFBQSxJQUFBQyxFQUFBO0VBQUEsSUFBQUwsQ0FBQSxRQUFBRSxlQUFBLElBQUFGLENBQUEsUUFBQUQsS0FBQTtJQUV4Q0ssRUFBQSxHQUFBQSxDQUFBO01BQ1IsSUFBSVAsZUFBZSxDQUFDLENBQUM7UUFBQTtNQUFBO01BQ3JCLE1BQUFTLGtCQUFBLEdBQTJCViwwQkFBMEIsQ0FBQ0csS0FBSyxDQUFDO01BRzVELElBQUlPLGtCQUFtRSxJQUE3Q0Esa0JBQWtCLEtBQUtILGNBQWMsQ0FBQUksT0FBUTtRQUNyRUosY0FBYyxDQUFBSSxPQUFBLEdBQVdELGtCQUFIO1FBQ3RCSixlQUFlLENBQUM7VUFBQU0sR0FBQSxFQUNULDJCQUEyQjtVQUFBQyxJQUFBLEVBQzFCSCxrQkFBa0I7VUFBQUksS0FBQSxFQUNqQixTQUFTO1VBQUFDLFFBQUEsRUFDTjtRQUNaLENBQUMsQ0FBQztNQUFBO01BSUosSUFBSSxDQUFDTCxrQkFBa0I7UUFDckJILGNBQWMsQ0FBQUksT0FBQSxHQUFXLElBQUg7TUFBQTtJQUN2QixDQUNGO0lBQUVGLEVBQUEsSUFBQ04sS0FBSyxFQUFFRyxlQUFlLENBQUM7SUFBQUYsQ0FBQSxNQUFBRSxlQUFBO0lBQUFGLENBQUEsTUFBQUQsS0FBQTtJQUFBQyxDQUFBLE1BQUFJLEVBQUE7SUFBQUosQ0FBQSxNQUFBSyxFQUFBO0VBQUE7SUFBQUQsRUFBQSxHQUFBSixDQUFBO0lBQUFLLEVBQUEsR0FBQUwsQ0FBQTtFQUFBO0VBbkIzQlAsU0FBUyxDQUFDVyxFQW1CVCxFQUFFQyxFQUF3QixDQUFDO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/hooks/notifs/useFastModeNotification.tsx`

**信息:**
- 行数: 162
- 大小: 14961 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { useEffect } from 'react';
import { useNotifications } from 'src/context/notifications.js';
import { useAppState, useSetAppState } from 'src/state/AppState.js';
import { type CooldownReason, isFastModeEnabled, onCooldownExpired, onCooldownTriggered, onFastModeOverageRejection, onOrgFastModeChanged } from 'src/utils/fastMode.js';
import { formatDuration } from 'src/utils/format.js';
import { getIsRemoteMode } from '../../bootstrap/state.js';
const COOLDOWN_STARTED_KEY = 'fast-mode-cooldown-started';
const COOLDOWN_EXPIRED_KEY = 'fast-mode-cooldown-expired';
const ORG_CHANGED_KEY = 'fast-mode-org-changed';
const OVERAGE_REJECTED_KEY = 'fast-mode-overage-rejected';
export function useFastModeNotification() {
  const $ = _c(13);
  const {
    addNotification
  } = useNotifications();
  const isFastMode = useAppState(_temp);
  const setAppState = useSetAppState();
  let t0;
  let t1;
  if ($[0] !== addNotification || $[1] !== isFastMode || $[2] !== setAppState) {
    t0 = () => {
      if (getIsRemoteMode()) {
        return;
      }
      if (!isFastModeEnabled()) {
        return;
      }
      return onOrgFastModeChanged(orgEnabled => {
        if (orgEnabled) {
          addNotification({
            key: ORG_CHANGED_KEY,
            color: "fastMode",
            priority: "immediate",
            text: "Fast mode is now available \xB7 /fast to turn on"
          });
        } else {
          if (isFastMode) {
            setAppState(_temp2);
            addNotification({
              key: ORG_CHANGED_KEY,
              color: "warning",
              priority: "immediate",
              text: "Fast mode has been disabled by your organization"
            });
          }
        }
      });
    };
    t1 = [addNotification, isFastMode, setAppState];

```

---


### `src/hooks/notifs/useIDEStatusIndicator.tsx`

**信息:**
- 行数: 186
- 大小: 20764 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useEffect, useRef } from 'react';
import { useNotifications } from 'src/context/notifications.js';
import { Text } from 'src/ink.js';
import type { MCPServerConnection } from 'src/services/mcp/types.js';
import { getGlobalConfig, saveGlobalConfig } from 'src/utils/config.js';
import { detectIDEs, type IDEExtensionInstallationStatus, isJetBrainsIde, isSupportedTerminal } from 'src/utils/ide.js';
import { getIsRemoteMode } from '../../bootstrap/state.js';
import { useIdeConnectionStatus } from '../useIdeConnectionStatus.js';
import type { IDESelection } from '../useIdeSelection.js';
const MAX_IDE_HINT_SHOW_COUNT = 5;
type Props = {
  ideInstallationStatus: IDEExtensionInstallationStatus | null;
  ideSelection: IDESelection | undefined;
  mcpClients: MCPServerConnection[];
};
export function useIDEStatusIndicator(t0) {
  const $ = _c(26);
  const {
    ideSelection,
    mcpClients,
    ideInstallationStatus
  } = t0;
  const {
    addNotification,
    removeNotification
  } = useNotifications();
  const {
    status: ideStatus,
    ideName
  } = useIdeConnectionStatus(mcpClients);
  const hasShownHintRef = useRef(false);
  let t1;
  if ($[0] !== ideInstallationStatus) {
    t1 = ideInstallationStatus ? isJetBrainsIde(ideInstallationStatus?.ideType) : false;
    $[0] = ideInstallationStatus;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const isJetBrains = t1;
  const showIDEInstallErrorOrJetBrainsInfo = ideInstallationStatus?.error || isJetBrains;
  const shouldShowIdeSelection = ideStatus === "connected" && (ideSelection?.filePath || ideSelection?.text && ideSelection.lineCount > 0);
  const shouldShowConnected = ideStatus === "connected" && !shouldShowIdeSelection;
  const showIDEInstallError = showIDEInstallErrorOrJetBrainsInfo && !isJetBrains && !shouldShowConnected && !shouldShowIdeSelection;
  const showJetBrainsInfo = showIDEInstallErrorOrJetBrainsInfo && isJetBrains && !shouldShowConnected && !shouldShowIdeSelection;
  let t2;
  let t3;
  if ($[2] !== addNotification || $[3] !== ideStatus || $[4] !== removeNotification || $[5] !== showJetBrainsInfo) {
    t2 = () => {

```

---


### `src/hooks/notifs/useInstallMessages.tsx`

**信息:**
- 行数: 26
- 大小: 3180 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { checkInstall } from 'src/utils/nativeInstaller/index.js';
import { useStartupNotification } from './useStartupNotification.js';
export function useInstallMessages() {
  useStartupNotification(_temp2);
}
async function _temp2() {
  const messages = await checkInstall();
  return messages.map(_temp);
}
function _temp(message, index) {
  let priority = "low";
  if (message.type === "error" || message.userActionRequired) {
    priority = "high";
  } else {
    if (message.type === "path" || message.type === "alias") {
      priority = "medium";
    }
  }
  return {
    key: `install-message-${index}-${message.type}`,
    text: message.message,
    priority,
    color: message.type === "error" ? "error" : "warning"
  };
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJjaGVja0luc3RhbGwiLCJ1c2VTdGFydHVwTm90aWZpY2F0aW9uIiwidXNlSW5zdGFsbE1lc3NhZ2VzIiwiX3RlbXAyIiwibWVzc2FnZXMiLCJtYXAiLCJfdGVtcCIsIm1lc3NhZ2UiLCJpbmRleCIsInByaW9yaXR5IiwidHlwZSIsInVzZXJBY3Rpb25SZXF1aXJlZCIsImtleSIsInRleHQiLCJjb2xvciJdLCJzb3VyY2VzIjpbInVzZUluc3RhbGxNZXNzYWdlcy50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgY2hlY2tJbnN0YWxsIH0gZnJvbSAnc3JjL3V0aWxzL25hdGl2ZUluc3RhbGxlci9pbmRleC5qcydcbmltcG9ydCB7IHVzZVN0YXJ0dXBOb3RpZmljYXRpb24gfSBmcm9tICcuL3VzZVN0YXJ0dXBOb3RpZmljYXRpb24uanMnXG5cbmV4cG9ydCBmdW5jdGlvbiB1c2VJbnN0YWxsTWVzc2FnZXMoKTogdm9pZCB7XG4gIHVzZVN0YXJ0dXBOb3RpZmljYXRpb24oYXN5bmMgKCkgPT4ge1xuICAgIGNvbnN0IG1lc3NhZ2VzID0gYXdhaXQgY2hlY2tJbnN0YWxsKClcbiAgICByZXR1cm4gbWVzc2FnZXMubWFwKChtZXNzYWdlLCBpbmRleCkgPT4ge1xuICAgICAgbGV0IHByaW9yaXR5OiAnbG93JyB8ICdtZWRpdW0nIHwgJ2hpZ2gnIHwgJ2ltbWVkaWF0ZScgPSAnbG93J1xuICAgICAgaWYgKG1lc3NhZ2UudHlwZSA9PT0gJ2Vycm9yJyB8fCBtZXNzYWdlLnVzZXJBY3Rpb25SZXF1aXJlZCkge1xuICAgICAgICBwcmlvcml0eSA9ICdoaWdoJ1xuICAgICAgfSBlbHNlIGlmIChtZXNzYWdlLnR5cGUgPT09ICdwYXRoJyB8fCBtZXNzYWdlLnR5cGUgPT09ICdhbGlhcycpIHtcbiAgICAgICAgcHJpb3JpdHkgPSAnbWVkaXVtJ1xuICAgICAgfVxuICAgICAgcmV0dXJuIHtcbiAgICAgICAga2V5OiBgaW5zdGFsbC1tZXNzYWdlLSR7aW5kZXh9LSR7bWVzc2FnZS50eXBlfWAsXG4gICAgICAgIHRleHQ6IG1lc3NhZ2UubWVzc2FnZSxcbiAgICAgICAgcHJpb3JpdHksXG4gICAgICAgIGNvbG9yOiBtZXNzYWdlLnR5cGUgPT09ICdlcnJvcicgPyAnZXJyb3InIDogJ3dhcm5pbmcnLFxuICAgICAgfVxuICAgIH0pXG4gIH0pXG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLFNBQVNBLFlBQVksUUFBUSxvQ0FBb0M7QUFDakUsU0FBU0Msc0JBQXNCLFFBQVEsNkJBQTZCO0FBRXBFLE9BQU8sU0FBQUMsbUJBQUE7RUFDTEQsc0JBQXNCLENBQUNFLE1BZ0J0QixDQUFDO0FBQUE7QUFqQkcsZUFBQUEsT0FBQTtFQUVILE1BQUFDLFFBQUEsR0FBaUIsTUFBTUosWUFBWSxDQUFDLENBQUM7RUFBQSxPQUM5QkksUUFBUSxDQUFBQyxHQUFJLENBQUNDLEtBYW5CLENBQUM7QUFBQTtBQWhCQyxTQUFBQSxNQUFBQyxPQUFBLEVBQUFDLEtBQUE7RUFJRCxJQUFBQyxRQUFBLEdBQXdELEtBQUs7RUFDN0QsSUFBSUYsT0FBTyxDQUFBRyxJQUFLLEtBQUssT0FBcUMsSUFBMUJILE9BQU8sQ0FBQUksa0JBQW1CO0lBQ3hERixRQUFBLENBQUFBLENBQUEsQ0FBV0EsTUFBTTtFQUFUO0lBQ0gsSUFBSUYsT0FBTyxDQUFBRyxJQUFLLEtBQUssTUFBa0MsSUFBeEJILE9BQU8sQ0FBQUcsSUFBSyxLQUFLLE9BQU87TUFDNURELFFBQUEsQ0FBQUEsQ0FBQSxDQUFXQSxRQUFRO0lBQVg7RUFDVDtFQUFBLE9BQ007SUFBQUcsR0FBQSxFQUNBLG1CQUFtQkosS0FBSyxJQUFJRCxPQUFPLENBQUFHLElBQUssRUFBRTtJQUFBRyxJQUFBLEVBQ3pDTixPQUFPLENBQUFBLE9BQVE7SUFBQUUsUUFBQTtJQUFBSyxLQUFBLEVBRWRQLE9BQU8sQ0FBQUcsSUFBSyxLQUFLLE9BQTZCLEdBQTlDLE9BQThDLEdBQTlDO0VBQ1QsQ0FBQztBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/hooks/notifs/useLspInitializationNotification.tsx`

**信息:**
- 行数: 143
- 大小: 16569 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useInterval } from 'usehooks-ts';
import { getIsRemoteMode, getIsScrollDraining } from '../../bootstrap/state.js';
import { useNotifications } from '../../context/notifications.js';
import { Text } from '../../ink.js';
import { getInitializationStatus, getLspServerManager } from '../../services/lsp/manager.js';
import { useSetAppState } from '../../state/AppState.js';
import { logForDebugging } from '../../utils/debug.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
const LSP_POLL_INTERVAL_MS = 5000;

/**
 * Hook that polls LSP status and shows a notification when:
 * 1. Manager initialization fails
 * 2. Any LSP server enters an error state
 *
 * Also adds errors to appState.plugins.errors for /doctor display.
 *
 * Only active when ENABLE_LSP_TOOL is set.
 */
export function useLspInitializationNotification() {
  const $ = _c(10);
  const {
    addNotification
  } = useNotifications();
  const setAppState = useSetAppState();
  const [shouldPoll, setShouldPoll] = React.useState(_temp);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = new Set();
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  const notifiedErrorsRef = React.useRef(t0);
  let t1;
  if ($[1] !== addNotification || $[2] !== setAppState) {
    t1 = (source, errorMessage) => {
      const errorKey = `${source}:${errorMessage}`;
      if (notifiedErrorsRef.current.has(errorKey)) {
        return;
      }
      notifiedErrorsRef.current.add(errorKey);
      logForDebugging(`LSP error: ${source} - ${errorMessage}`);
      setAppState(prev => {
        const existingKeys = new Set(prev.plugins.errors.map(_temp2));
        const stateErrorKey = `generic-error:${source}:${errorMessage}`;
        if (existingKeys.has(stateErrorKey)) {
          return prev;

```

---


### `src/hooks/notifs/useMcpConnectivityStatus.tsx`

**信息:**
- 行数: 88
- 大小: 14710 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useEffect } from 'react';
import { useNotifications } from 'src/context/notifications.js';
import { getIsRemoteMode } from '../../bootstrap/state.js';
import { Text } from '../../ink.js';
import { hasClaudeAiMcpEverConnected } from '../../services/mcp/claudeai.js';
import type { MCPServerConnection } from '../../services/mcp/types.js';
type Props = {
  mcpClients?: MCPServerConnection[];
};
const EMPTY_MCP_CLIENTS: MCPServerConnection[] = [];
export function useMcpConnectivityStatus(t0) {
  const $ = _c(4);
  const {
    mcpClients: t1
  } = t0;
  const mcpClients = t1 === undefined ? EMPTY_MCP_CLIENTS : t1;
  const {
    addNotification
  } = useNotifications();
  let t2;
  let t3;
  if ($[0] !== addNotification || $[1] !== mcpClients) {
    t2 = () => {
      if (getIsRemoteMode()) {
        return;
      }
      const failedLocalClients = mcpClients.filter(_temp);
      const failedClaudeAiClients = mcpClients.filter(_temp2);
      const needsAuthLocalServers = mcpClients.filter(_temp3);
      const needsAuthClaudeAiServers = mcpClients.filter(_temp4);
      if (failedLocalClients.length === 0 && failedClaudeAiClients.length === 0 && needsAuthLocalServers.length === 0 && needsAuthClaudeAiServers.length === 0) {
        return;
      }
      if (failedLocalClients.length > 0) {
        addNotification({
          key: "mcp-failed",
          jsx: <><Text color="error">{failedLocalClients.length} MCP{" "}{failedLocalClients.length === 1 ? "server" : "servers"} failed</Text><Text dimColor={true}> · /mcp</Text></>,
          priority: "medium"
        });
      }
      if (failedClaudeAiClients.length > 0) {
        addNotification({
          key: "mcp-claudeai-failed",
          jsx: <><Text color="error">{failedClaudeAiClients.length} claude.ai{" "}{failedClaudeAiClients.length === 1 ? "connector" : "connectors"}{" "}unavailable</Text><Text dimColor={true}> · /mcp</Text></>,
          priority: "medium"
        });
      }
      if (needsAuthLocalServers.length > 0) {

```

---


### `src/hooks/notifs/useModelMigrationNotifications.tsx`

**信息:**
- 行数: 52
- 大小: 6988 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { Notification } from 'src/context/notifications.js';
import { type GlobalConfig, getGlobalConfig } from 'src/utils/config.js';
import { useStartupNotification } from './useStartupNotification.js';

// Shows a one-time notification right after a model migration writes its
// timestamp to config. Each entry reads its own timestamp field(s) and emits
// a notification if the write happened within the last 3s (i.e. this launch).
// Future model migrations: add an entry to MIGRATIONS below.
const MIGRATIONS: ((c: GlobalConfig) => Notification | undefined)[] = [
// Sonnet 4.5 → 4.6 (pro/max/team premium)
c => {
  if (!recent(c.sonnet45To46MigrationTimestamp)) return;
  return {
    key: 'sonnet-46-update',
    text: 'Model updated to Sonnet 4.6',
    color: 'suggestion',
    priority: 'high',
    timeoutMs: 3000
  };
},
// Opus Pro → default, or pinned 4.0/4.1 → opus alias. Both land on the
// current Opus default (4.6 for 1P).
c => {
  const isLegacyRemap = Boolean(c.legacyOpusMigrationTimestamp);
  const ts = c.legacyOpusMigrationTimestamp ?? c.opusProMigrationTimestamp;
  if (!recent(ts)) return;
  return {
    key: 'opus-pro-update',
    text: isLegacyRemap ? 'Model updated to Opus 4.6 · Set CLAUDE_CODE_DISABLE_LEGACY_MODEL_REMAP=1 to opt out' : 'Model updated to Opus 4.6',
    color: 'suggestion',
    priority: 'high',
    timeoutMs: isLegacyRemap ? 8000 : 3000
  };
}];
export function useModelMigrationNotifications() {
  useStartupNotification(_temp);
}
function _temp() {
  const config = getGlobalConfig();
  const notifs = [];
  for (const migration of MIGRATIONS) {
    const notif = migration(config);
    if (notif) {
      notifs.push(notif);
    }
  }
  return notifs.length > 0 ? notifs : null;
}
function recent(ts: number | undefined): boolean {
  return ts !== undefined && Date.now() - ts < 3000;

```

---


### `src/hooks/notifs/useNpmDeprecationNotification.tsx`

**信息:**
- 行数: 25
- 大小: 3602 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { isInBundledMode } from 'src/utils/bundledMode.js';
import { getCurrentInstallationType } from 'src/utils/doctorDiagnostic.js';
import { isEnvTruthy } from 'src/utils/envUtils.js';
import { useStartupNotification } from './useStartupNotification.js';
const NPM_DEPRECATION_MESSAGE = 'Claude Code has switched from npm to native installer. Run `claude install` or see https://docs.anthropic.com/en/docs/claude-code/getting-started for more options.';
export function useNpmDeprecationNotification() {
  useStartupNotification(_temp);
}
async function _temp() {
  if (isInBundledMode() || isEnvTruthy(process.env.DISABLE_INSTALLATION_CHECKS)) {
    return null;
  }
  const installationType = await getCurrentInstallationType();
  if (installationType === "development") {
    return null;
  }
  return {
    timeoutMs: 15000,
    key: "npm-deprecation-warning",
    text: NPM_DEPRECATION_MESSAGE,
    color: "warning",
    priority: "high"
  };
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJpc0luQnVuZGxlZE1vZGUiLCJnZXRDdXJyZW50SW5zdGFsbGF0aW9uVHlwZSIsImlzRW52VHJ1dGh5IiwidXNlU3RhcnR1cE5vdGlmaWNhdGlvbiIsIk5QTV9ERVBSRUNBVElPTl9NRVNTQUdFIiwidXNlTnBtRGVwcmVjYXRpb25Ob3RpZmljYXRpb24iLCJfdGVtcCIsInByb2Nlc3MiLCJlbnYiLCJESVNBQkxFX0lOU1RBTExBVElPTl9DSEVDS1MiLCJpbnN0YWxsYXRpb25UeXBlIiwidGltZW91dE1zIiwia2V5IiwidGV4dCIsImNvbG9yIiwicHJpb3JpdHkiXSwic291cmNlcyI6WyJ1c2VOcG1EZXByZWNhdGlvbk5vdGlmaWNhdGlvbi50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgaXNJbkJ1bmRsZWRNb2RlIH0gZnJvbSAnc3JjL3V0aWxzL2J1bmRsZWRNb2RlLmpzJ1xuaW1wb3J0IHsgZ2V0Q3VycmVudEluc3RhbGxhdGlvblR5cGUgfSBmcm9tICdzcmMvdXRpbHMvZG9jdG9yRGlhZ25vc3RpYy5qcydcbmltcG9ydCB7IGlzRW52VHJ1dGh5IH0gZnJvbSAnc3JjL3V0aWxzL2VudlV0aWxzLmpzJ1xuaW1wb3J0IHsgdXNlU3RhcnR1cE5vdGlmaWNhdGlvbiB9IGZyb20gJy4vdXNlU3RhcnR1cE5vdGlmaWNhdGlvbi5qcydcblxuY29uc3QgTlBNX0RFUFJFQ0FUSU9OX01FU1NBR0UgPVxuICAnQ2xhdWRlIENvZGUgaGFzIHN3aXRjaGVkIGZyb20gbnBtIHRvIG5hdGl2ZSBpbnN0YWxsZXIuIFJ1biBgY2xhdWRlIGluc3RhbGxgIG9yIHNlZSBodHRwczovL2RvY3MuYW50aHJvcGljLmNvbS9lbi9kb2NzL2NsYXVkZS1jb2RlL2dldHRpbmctc3RhcnRlZCBmb3IgbW9yZSBvcHRpb25zLidcblxuZXhwb3J0IGZ1bmN0aW9uIHVzZU5wbURlcHJlY2F0aW9uTm90aWZpY2F0aW9uKCk6IHZvaWQge1xuICB1c2VTdGFydHVwTm90aWZpY2F0aW9uKGFzeW5jICgpID0+IHtcbiAgICBpZiAoXG4gICAgICBpc0luQnVuZGxlZE1vZGUoKSB8fFxuICAgICAgaXNFbnZUcnV0aHkocHJvY2Vzcy5lbnYuRElTQUJMRV9JTlNUQUxMQVRJT05fQ0hFQ0tTKVxuICAgICkge1xuICAgICAgcmV0dXJuIG51bGxcbiAgICB9XG4gICAgY29uc3QgaW5zdGFsbGF0aW9uVHlwZSA9IGF3YWl0IGdldEN1cnJlbnRJbnN0YWxsYXRpb25UeXBlKClcbiAgICBpZiAoaW5zdGFsbGF0aW9uVHlwZSA9PT0gJ2RldmVsb3BtZW50JykgcmV0dXJuIG51bGxcbiAgICByZXR1cm4ge1xuICAgICAgdGltZW91dE1zOiAxNTAwMCxcbiAgICAgIGtleTogJ25wbS1kZXByZWNhdGlvbi13YXJuaW5nJyxcbiAgICAgIHRleHQ6IE5QTV9ERVBSRUNBVElPTl9NRVNTQUdFLFxuICAgICAgY29sb3I6ICd3YXJuaW5nJyxcbiAgICAgIHByaW9yaXR5OiAnaGlnaCcsXG4gICAgfVxuICB9KVxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxTQUFTQSxlQUFlLFFBQVEsMEJBQTBCO0FBQzFELFNBQVNDLDBCQUEwQixRQUFRLCtCQUErQjtBQUMxRSxTQUFTQyxXQUFXLFFBQVEsdUJBQXVCO0FBQ25ELFNBQVNDLHNCQUFzQixRQUFRLDZCQUE2QjtBQUVwRSxNQUFNQyx1QkFBdUIsR0FDM0IscUtBQXFLO0FBRXZLLE9BQU8sU0FBQUMsOEJBQUE7RUFDTEYsc0JBQXNCLENBQUNHLEtBZ0J0QixDQUFDO0FBQUE7QUFqQkcsZUFBQUEsTUFBQTtFQUVILElBQ0VOLGVBQWUsQ0FDb0MsQ0FBQyxJQUFwREUsV0FBVyxDQUFDSyxPQUFPLENBQUFDLEdBQUksQ0FBQUMsMkJBQTRCLENBQUM7SUFBQSxPQUU3QyxJQUFJO0VBQUE7RUFFYixNQUFBQyxnQkFBQSxHQUF5QixNQUFNVCwwQkFBMEIsQ0FBQyxDQUFDO0VBQzNELElBQUlTLGdCQUFnQixLQUFLLGFBQWE7SUFBQSxPQUFTLElBQUk7RUFBQTtFQUFBLE9BQzVDO0lBQUFDLFNBQUEsRUFDTSxLQUFLO0lBQUFDLEdBQUEsRUFDWCx5QkFBeUI7SUFBQUMsSUFBQSxFQUN4QlQsdUJBQXVCO0lBQUFVLEtBQUEsRUFDdEIsU0FBUztJQUFBQyxRQUFBLEVBQ047RUFDWixDQUFDO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/hooks/notifs/usePluginAutoupdateNotification.tsx`

**信息:**
- 行数: 83
- 大小: 9015 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useEffect, useState } from 'react';
import { getIsRemoteMode } from '../../bootstrap/state.js';
import { useNotifications } from '../../context/notifications.js';
import { Text } from '../../ink.js';
import { logForDebugging } from '../../utils/debug.js';
import { onPluginsAutoUpdated } from '../../utils/plugins/pluginAutoupdate.js';

/**
 * Hook that displays a notification when plugins have been auto-updated.
 * The notification tells the user to run /reload-plugins to apply the updates.
 */
export function usePluginAutoupdateNotification() {
  const $ = _c(7);
  const {
    addNotification
  } = useNotifications();
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = [];
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  const [updatedPlugins, setUpdatedPlugins] = useState(t0);
  let t1;
  let t2;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = () => {
      if (getIsRemoteMode()) {
        return;
      }
      const unsubscribe = onPluginsAutoUpdated(plugins => {
        logForDebugging(`Plugin autoupdate notification: ${plugins.length} plugin(s) updated`);
        setUpdatedPlugins(plugins);
      });
      return unsubscribe;
    };
    t2 = [];
    $[1] = t1;
    $[2] = t2;
  } else {
    t1 = $[1];
    t2 = $[2];
  }
  useEffect(t1, t2);
  let t3;
  let t4;
  if ($[3] !== addNotification || $[4] !== updatedPlugins) {

```

---


### `src/hooks/notifs/usePluginInstallationStatus.tsx`

**信息:**
- 行数: 128
- 大小: 12012 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useEffect, useMemo } from 'react';
import { getIsRemoteMode } from '../../bootstrap/state.js';
import { useNotifications } from '../../context/notifications.js';
import { Text } from '../../ink.js';
import { useAppState } from '../../state/AppState.js';
import { logForDebugging } from '../../utils/debug.js';
import { plural } from '../../utils/stringUtils.js';
export function usePluginInstallationStatus() {
  const $ = _c(20);
  const {
    addNotification
  } = useNotifications();
  const installationStatus = useAppState(_temp);
  let t0;
  bb0: {
    if (!installationStatus) {
      let t1;
      if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
        t1 = {
          totalFailed: 0,
          failedMarketplacesCount: 0,
          failedPluginsCount: 0
        };
        $[0] = t1;
      } else {
        t1 = $[0];
      }
      t0 = t1;
      break bb0;
    }
    let t1;
    if ($[1] !== installationStatus.marketplaces) {
      t1 = installationStatus.marketplaces.filter(_temp2);
      $[1] = installationStatus.marketplaces;
      $[2] = t1;
    } else {
      t1 = $[2];
    }
    const failedMarketplaces = t1;
    let t2;
    if ($[3] !== installationStatus.plugins) {
      t2 = installationStatus.plugins.filter(_temp3);
      $[3] = installationStatus.plugins;
      $[4] = t2;
    } else {
      t2 = $[4];
    }
    const failedPlugins = t2;

```

---


### `src/hooks/notifs/useRateLimitWarningNotification.tsx`

**信息:**
- 行数: 114
- 大小: 12250 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useEffect, useMemo, useRef, useState } from 'react';
import { useNotifications } from 'src/context/notifications.js';
import { Text } from 'src/ink.js';
import { getRateLimitWarning, getUsingOverageText } from 'src/services/claudeAiLimits.js';
import { useClaudeAiLimits } from 'src/services/claudeAiLimitsHook.js';
import { getSubscriptionType } from 'src/utils/auth.js';
import { hasClaudeAiBillingAccess } from 'src/utils/billing.js';
import { getIsRemoteMode } from '../../bootstrap/state.js';
export function useRateLimitWarningNotification(model) {
  const $ = _c(17);
  const {
    addNotification
  } = useNotifications();
  const claudeAiLimits = useClaudeAiLimits();
  let t0;
  if ($[0] !== claudeAiLimits || $[1] !== model) {
    t0 = getRateLimitWarning(claudeAiLimits, model);
    $[0] = claudeAiLimits;
    $[1] = model;
    $[2] = t0;
  } else {
    t0 = $[2];
  }
  const rateLimitWarning = t0;
  let t1;
  if ($[3] !== claudeAiLimits) {
    t1 = getUsingOverageText(claudeAiLimits);
    $[3] = claudeAiLimits;
    $[4] = t1;
  } else {
    t1 = $[4];
  }
  const usingOverageText = t1;
  const shownWarningRef = useRef(null);
  let t2;
  if ($[5] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = getSubscriptionType();
    $[5] = t2;
  } else {
    t2 = $[5];
  }
  const subscriptionType = t2;
  let t3;
  if ($[6] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = hasClaudeAiBillingAccess();
    $[6] = t3;
  } else {
    t3 = $[6];

```

---


### `src/hooks/notifs/useSettingsErrors.tsx`

**信息:**
- 行数: 69
- 大小: 6756 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { useCallback, useEffect, useState } from 'react';
import { useNotifications } from 'src/context/notifications.js';
import { getIsRemoteMode } from '../../bootstrap/state.js';
import { getSettingsWithAllErrors } from '../../utils/settings/allErrors.js';
import type { ValidationError } from '../../utils/settings/validation.js';
import { useSettingsChange } from '../useSettingsChange.js';
const SETTINGS_ERRORS_NOTIFICATION_KEY = 'settings-errors';
export function useSettingsErrors() {
  const $ = _c(6);
  const {
    addNotification,
    removeNotification
  } = useNotifications();
  const [errors_0, setErrors] = useState(_temp);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = () => {
      const {
        errors: errors_1
      } = getSettingsWithAllErrors();
      setErrors(errors_1);
    };
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  const handleSettingsChange = t0;
  useSettingsChange(handleSettingsChange);
  let t1;
  let t2;
  if ($[1] !== addNotification || $[2] !== errors_0 || $[3] !== removeNotification) {
    t1 = () => {
      if (getIsRemoteMode()) {
        return;
      }
      if (errors_0.length > 0) {
        const message = `Found ${errors_0.length} settings ${errors_0.length === 1 ? "issue" : "issues"} · /doctor for details`;
        addNotification({
          key: SETTINGS_ERRORS_NOTIFICATION_KEY,
          text: message,
          color: "warning",
          priority: "high",
          timeoutMs: 60000
        });
      } else {
        removeNotification(SETTINGS_ERRORS_NOTIFICATION_KEY);
      }
    };
    t2 = [errors_0, addNotification, removeNotification];

```

---


### `src/hooks/notifs/useStartupNotification.ts`

**信息:**
- 行数: 41
- 大小: 1278 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef } from 'react'
import { getIsRemoteMode } from '../../bootstrap/state.js'
import {
  type Notification,
  useNotifications,
} from '../../context/notifications.js'
import { logError } from '../../utils/log.js'

type Result = Notification | Notification[] | null

/**
 * Fires notification(s) once on mount. Encapsulates the remote-mode gate and
 * once-per-session ref guard that was hand-rolled across 10+ notifs/ hooks.
 *
 * The compute fn runs exactly once on first effect. Return null to skip,
 * a Notification to fire one, or an array to fire several. Sync or async.
 * Rejections are routed to logError.
 */
export function useStartupNotification(
  compute: () => Result | Promise<Result>,
): void {
  const { addNotification } = useNotifications()
  const hasRunRef = useRef(false)
  const computeRef = useRef(compute)
  computeRef.current = compute

  useEffect(() => {
    if (getIsRemoteMode() || hasRunRef.current) return
    hasRunRef.current = true

    void Promise.resolve()
      .then(() => computeRef.current())
      .then(result => {
        if (!result) return
        for (const n of Array.isArray(result) ? result : [result]) {
          addNotification(n)
        }
      })
      .catch(logError)
  }, [addNotification])
}

```

---


### `src/hooks/notifs/useTeammateShutdownNotification.ts`

**信息:**
- 行数: 78
- 大小: 2296 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef } from 'react'
import { getIsRemoteMode } from '../../bootstrap/state.js'
import {
  type Notification,
  useNotifications,
} from '../../context/notifications.js'
import { useAppState } from '../../state/AppState.js'
import { isInProcessTeammateTask } from '../../tasks/InProcessTeammateTask/types.js'

function parseCount(notif: Notification): number {
  if (!('text' in notif)) {
    return 1
  }
  const match = notif.text.match(/^(\d+)/)
  return match?.[1] ? parseInt(match[1], 10) : 1
}

function foldSpawn(acc: Notification, _incoming: Notification): Notification {
  return makeSpawnNotif(parseCount(acc) + 1)
}

function makeSpawnNotif(count: number): Notification {
  return {
    key: 'teammate-spawn',
    text: count === 1 ? '1 agent spawned' : `${count} agents spawned`,
    priority: 'low',
    timeoutMs: 5000,
    fold: foldSpawn,
  }
}

function foldShutdown(
  acc: Notification,
  _incoming: Notification,
): Notification {
  return makeShutdownNotif(parseCount(acc) + 1)
}

function makeShutdownNotif(count: number): Notification {
  return {
    key: 'teammate-shutdown',
    text: count === 1 ? '1 agent shut down' : `${count} agents shut down`,
    priority: 'low',
    timeoutMs: 5000,
    fold: foldShutdown,
  }
}

/**
 * Fires batched notifications when in-process teammates spawn or shut down.

```

---


### `src/hooks/renderPlaceholder.ts`

**信息:**
- 行数: 51
- 大小: 1280 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import chalk from 'chalk'

type PlaceholderRendererProps = {
  placeholder?: string
  value: string
  showCursor?: boolean
  focus?: boolean
  terminalFocus: boolean
  invert?: (text: string) => string
  hidePlaceholderText?: boolean
}

export function renderPlaceholder({
  placeholder,
  value,
  showCursor,
  focus,
  terminalFocus = true,
  invert = chalk.inverse,
  hidePlaceholderText = false,
}: PlaceholderRendererProps): {
  renderedPlaceholder: string | undefined
  showPlaceholder: boolean
} {
  let renderedPlaceholder: string | undefined = undefined

  if (placeholder) {
    if (hidePlaceholderText) {
      // Voice recording: show only the cursor, no placeholder text
      renderedPlaceholder =
        showCursor && focus && terminalFocus ? invert(' ') : ''
    } else {
      renderedPlaceholder = chalk.dim(placeholder)

      // Show inverse cursor only when both input and terminal are focused
      if (showCursor && focus && terminalFocus) {
        renderedPlaceholder =
          placeholder.length > 0
            ? invert(placeholder[0]!) + chalk.dim(placeholder.slice(1))
            : invert(' ')
      }
    }
  }

  const showPlaceholder = value.length === 0 && Boolean(placeholder)

  return {
    renderedPlaceholder,
    showPlaceholder,
  }

```

---


### `src/hooks/toolPermission/PermissionContext.ts`

**信息:**
- 行数: 388
- 大小: 12768 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/messages.mjs'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from 'src/services/analytics/index.js'
import { sanitizeToolNameForAnalytics } from 'src/services/analytics/metadata.js'
import type { ToolUseConfirm } from '../../components/permissions/PermissionRequest.js'
import type {
  ToolPermissionContext,
  Tool as ToolType,
  ToolUseContext,
} from '../../Tool.js'
import { awaitClassifierAutoApproval } from '../../tools/BashTool/bashPermissions.js'
import { BASH_TOOL_NAME } from '../../tools/BashTool/toolName.js'
import type { AssistantMessage } from '../../types/message.js'
import type {
  PendingClassifierCheck,
  PermissionAllowDecision,
  PermissionDecisionReason,
  PermissionDenyDecision,
} from '../../types/permissions.js'
import { setClassifierApproval } from '../../utils/classifierApprovals.js'
import { logForDebugging } from '../../utils/debug.js'
import { executePermissionRequestHooks } from '../../utils/hooks.js'
import {
  REJECT_MESSAGE,
  REJECT_MESSAGE_WITH_REASON_PREFIX,
  SUBAGENT_REJECT_MESSAGE,
  SUBAGENT_REJECT_MESSAGE_WITH_REASON_PREFIX,
  withMemoryCorrectionHint,
} from '../../utils/messages.js'
import type { PermissionDecision } from '../../utils/permissions/PermissionResult.js'
import {
  applyPermissionUpdates,
  persistPermissionUpdates,
  supportsPersistence,
} from '../../utils/permissions/PermissionUpdate.js'
import type { PermissionUpdate } from '../../utils/permissions/PermissionUpdateSchema.js'
import {
  logPermissionDecision,
  type PermissionDecisionArgs,
} from './permissionLogging.js'

type PermissionApprovalSource =
  | { type: 'hook'; permanent?: boolean }
  | { type: 'user'; permanent: boolean }
  | { type: 'classifier' }

type PermissionRejectionSource =

```

---


### `src/hooks/toolPermission/handlers/coordinatorHandler.ts`

**信息:**
- 行数: 65
- 大小: 2374 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { PendingClassifierCheck } from '../../../types/permissions.js'
import { logError } from '../../../utils/log.js'
import type { PermissionDecision } from '../../../utils/permissions/PermissionResult.js'
import type { PermissionUpdate } from '../../../utils/permissions/PermissionUpdateSchema.js'
import type { PermissionContext } from '../PermissionContext.js'

type CoordinatorPermissionParams = {
  ctx: PermissionContext
  pendingClassifierCheck?: PendingClassifierCheck | undefined
  updatedInput: Record<string, unknown> | undefined
  suggestions: PermissionUpdate[] | undefined
  permissionMode: string | undefined
}

/**
 * Handles the coordinator worker permission flow.
 *
 * For coordinator workers, automated checks (hooks and classifier) are
 * awaited sequentially before falling through to the interactive dialog.
 *
 * Returns a PermissionDecision if the automated checks resolved the
 * permission, or null if the caller should fall through to the
 * interactive dialog.
 */
async function handleCoordinatorPermission(
  params: CoordinatorPermissionParams,
): Promise<PermissionDecision | null> {
  const { ctx, updatedInput, suggestions, permissionMode } = params

  try {
    // 1. Try permission hooks first (fast, local)
    const hookResult = await ctx.runHooks(
      permissionMode,
      suggestions,
      updatedInput,
    )
    if (hookResult) return hookResult

    // 2. Try classifier (slow, inference -- bash only)
    const classifierResult = feature('BASH_CLASSIFIER')
      ? await ctx.tryClassifier?.(params.pendingClassifierCheck, updatedInput)
      : null
    if (classifierResult) {
      return classifierResult
    }
  } catch (error) {
    // If automated checks fail unexpectedly, fall through to show the dialog
    // so the user can decide manually. Non-Error throws get a context prefix
    // so the log is traceable — intentionally NOT toError(), which would drop

```

---


### `src/hooks/toolPermission/handlers/interactiveHandler.ts`

**信息:**
- 行数: 536
- 大小: 20194 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/messages.mjs'
import { randomUUID } from 'crypto'
import { logForDebugging } from 'src/utils/debug.js'
import { getAllowedChannels } from '../../../bootstrap/state.js'
import type { BridgePermissionCallbacks } from '../../../bridge/bridgePermissionCallbacks.js'
import { getTerminalFocused } from '../../../ink/terminal-focus-state.js'
import {
  CHANNEL_PERMISSION_REQUEST_METHOD,
  type ChannelPermissionRequestParams,
  findChannelEntry,
} from '../../../services/mcp/channelNotification.js'
import type { ChannelPermissionCallbacks } from '../../../services/mcp/channelPermissions.js'
import {
  filterPermissionRelayClients,
  shortRequestId,
  truncateForPreview,
} from '../../../services/mcp/channelPermissions.js'
import { executeAsyncClassifierCheck } from '../../../tools/BashTool/bashPermissions.js'
import { BASH_TOOL_NAME } from '../../../tools/BashTool/toolName.js'
import {
  clearClassifierChecking,
  setClassifierApproval,
  setClassifierChecking,
  setYoloClassifierApproval,
} from '../../../utils/classifierApprovals.js'
import { errorMessage } from '../../../utils/errors.js'
import type { PermissionDecision } from '../../../utils/permissions/PermissionResult.js'
import type { PermissionUpdate } from '../../../utils/permissions/PermissionUpdateSchema.js'
import { hasPermissionsToUseTool } from '../../../utils/permissions/permissions.js'
import type { PermissionContext } from '../PermissionContext.js'
import { createResolveOnce } from '../PermissionContext.js'

type InteractivePermissionParams = {
  ctx: PermissionContext
  description: string
  result: PermissionDecision & { behavior: 'ask' }
  awaitAutomatedChecksBeforeDialog: boolean | undefined
  bridgeCallbacks?: BridgePermissionCallbacks
  channelCallbacks?: ChannelPermissionCallbacks
}

/**
 * Handles the interactive (main-agent) permission flow.
 *
 * Pushes a ToolUseConfirm entry to the confirm queue with callbacks:
 * onAbort, onAllow, onReject, recheckPermission, onUserInteraction.
 *
 * Runs permission hooks and bash classifier checks asynchronously in the
 * background, racing them against user interaction. Uses a resolve-once

```

---


### `src/hooks/toolPermission/handlers/swarmWorkerHandler.ts`

**信息:**
- 行数: 159
- 大小: 5537 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/messages.mjs'
import type { PendingClassifierCheck } from '../../../types/permissions.js'
import { isAgentSwarmsEnabled } from '../../../utils/agentSwarmsEnabled.js'
import { toError } from '../../../utils/errors.js'
import { logError } from '../../../utils/log.js'
import type { PermissionDecision } from '../../../utils/permissions/PermissionResult.js'
import type { PermissionUpdate } from '../../../utils/permissions/PermissionUpdateSchema.js'
import {
  createPermissionRequest,
  isSwarmWorker,
  sendPermissionRequestViaMailbox,
} from '../../../utils/swarm/permissionSync.js'
import { registerPermissionCallback } from '../../useSwarmPermissionPoller.js'
import type { PermissionContext } from '../PermissionContext.js'
import { createResolveOnce } from '../PermissionContext.js'

type SwarmWorkerPermissionParams = {
  ctx: PermissionContext
  description: string
  pendingClassifierCheck?: PendingClassifierCheck | undefined
  updatedInput: Record<string, unknown> | undefined
  suggestions: PermissionUpdate[] | undefined
}

/**
 * Handles the swarm worker permission flow.
 *
 * When running as a swarm worker:
 * 1. Tries classifier auto-approval for bash commands
 * 2. Forwards the permission request to the leader via mailbox
 * 3. Registers callbacks for when the leader responds
 * 4. Sets the pending indicator while waiting
 *
 * Returns a PermissionDecision if the classifier auto-approves,
 * or a Promise that resolves when the leader responds.
 * Returns null if swarms are not enabled or this is not a swarm worker,
 * so the caller can fall through to interactive handling.
 */
async function handleSwarmWorkerPermission(
  params: SwarmWorkerPermissionParams,
): Promise<PermissionDecision | null> {
  if (!isAgentSwarmsEnabled() || !isSwarmWorker()) {
    return null
  }

  const { ctx, description, updatedInput, suggestions } = params

  // For bash commands, try classifier auto-approval before forwarding to
  // the leader. Agents await the classifier result (rather than racing it

```

---


### `src/hooks/toolPermission/permissionLogging.ts`

**信息:**
- 行数: 238
- 大小: 7286 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Centralized analytics/telemetry logging for tool permission decisions.
// All permission approve/reject events flow through logPermissionDecision(),
// which fans out to Statsig analytics, OTel telemetry, and code-edit metrics.
import { feature } from 'bun:bundle'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from 'src/services/analytics/index.js'
import { sanitizeToolNameForAnalytics } from 'src/services/analytics/metadata.js'
import { getCodeEditToolDecisionCounter } from '../../bootstrap/state.js'
import type { Tool as ToolType, ToolUseContext } from '../../Tool.js'
import { getLanguageName } from '../../utils/cliHighlight.js'
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js'
import { logOTelEvent } from '../../utils/telemetry/events.js'
import type {
  PermissionApprovalSource,
  PermissionRejectionSource,
} from './PermissionContext.js'

type PermissionLogContext = {
  tool: ToolType
  input: unknown
  toolUseContext: ToolUseContext
  messageId: string
  toolUseID: string
}

// Discriminated union: 'accept' pairs with approval sources, 'reject' with rejection sources
type PermissionDecisionArgs =
  | { decision: 'accept'; source: PermissionApprovalSource | 'config' }
  | { decision: 'reject'; source: PermissionRejectionSource | 'config' }

const CODE_EDITING_TOOLS = ['Edit', 'Write', 'NotebookEdit']

function isCodeEditingTool(toolName: string): boolean {
  return CODE_EDITING_TOOLS.includes(toolName)
}

// Builds OTel counter attributes for code editing tools, enriching with
// language when the tool's target file path can be extracted from input
async function buildCodeEditToolAttributes(
  tool: ToolType,
  input: unknown,
  decision: 'accept' | 'reject',
  source: string,
): Promise<Record<string, string>> {
  // Derive language from file path if the tool exposes one (e.g., Edit, Write)
  let language: string | undefined
  if (tool.getPath && input) {
    const parseResult = tool.inputSchema.safeParse(input)

```

---


### `src/hooks/unifiedSuggestions.ts`

**信息:**
- 行数: 202
- 大小: 5837 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import Fuse from 'fuse.js'
import { basename } from 'path'
import type { SuggestionItem } from 'src/components/PromptInput/PromptInputFooterSuggestions.js'
import { generateFileSuggestions } from 'src/hooks/fileSuggestions.js'
import type { ServerResource } from 'src/services/mcp/types.js'
import { getAgentColor } from 'src/tools/AgentTool/agentColorManager.js'
import type { AgentDefinition } from 'src/tools/AgentTool/loadAgentsDir.js'
import { truncateToWidth } from 'src/utils/format.js'
import { logError } from 'src/utils/log.js'
import type { Theme } from 'src/utils/theme.js'

type FileSuggestionSource = {
  type: 'file'
  displayText: string
  description?: string
  path: string
  filename: string
  score?: number
}

type McpResourceSuggestionSource = {
  type: 'mcp_resource'
  displayText: string
  description: string
  server: string
  uri: string
  name: string
}

type AgentSuggestionSource = {
  type: 'agent'
  displayText: string
  description: string
  agentType: string
  color?: keyof Theme
}

type SuggestionSource =
  | FileSuggestionSource
  | McpResourceSuggestionSource
  | AgentSuggestionSource

/**
 * Creates a unified suggestion item from a source
 */
function createSuggestionFromSource(source: SuggestionSource): SuggestionItem {
  switch (source.type) {
    case 'file':
      return {
        id: `file-${source.path}`,

```

---


### `src/hooks/useAfterFirstRender.ts`

**信息:**
- 行数: 17
- 大小: 485 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect } from 'react'
import { isEnvTruthy } from '../utils/envUtils.js'

export function useAfterFirstRender(): void {
  useEffect(() => {
    if (
      process.env.USER_TYPE === 'ant' &&
      isEnvTruthy(process.env.CLAUDE_CODE_EXIT_AFTER_FIRST_RENDER)
    ) {
      process.stderr.write(
        `\nStartup time: ${Math.round(process.uptime() * 1000)}ms\n`,
      )
      // eslint-disable-next-line custom-rules/no-process-exit
      process.exit(0)
    }
  }, [])
}

```

---


### `src/hooks/useApiKeyVerification.ts`

**信息:**
- 行数: 84
- 大小: 2678 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useState } from 'react'
import { getIsNonInteractiveSession } from '../bootstrap/state.js'
import { verifyApiKey } from '../services/api/claude.js'
import {
  getAnthropicApiKeyWithSource,
  getApiKeyFromApiKeyHelper,
  isAnthropicAuthEnabled,
  isClaudeAISubscriber,
} from '../utils/auth.js'

export type VerificationStatus =
  | 'loading'
  | 'valid'
  | 'invalid'
  | 'missing'
  | 'error'

export type ApiKeyVerificationResult = {
  status: VerificationStatus
  reverify: () => Promise<void>
  error: Error | null
}

export function useApiKeyVerification(): ApiKeyVerificationResult {
  const [status, setStatus] = useState<VerificationStatus>(() => {
    if (!isAnthropicAuthEnabled() || isClaudeAISubscriber()) {
      return 'valid'
    }
    // Use skipRetrievingKeyFromApiKeyHelper to avoid executing apiKeyHelper
    // before trust dialog is shown (security: prevents RCE via settings.json)
    const { key, source } = getAnthropicApiKeyWithSource({
      skipRetrievingKeyFromApiKeyHelper: true,
    })
    // If apiKeyHelper is configured, we have a key source even though we
    // haven't executed it yet - return 'loading' to indicate we'll verify later
    if (key || source === 'apiKeyHelper') {
      return 'loading'
    }
    return 'missing'
  })
  const [error, setError] = useState<Error | null>(null)

  const verify = useCallback(async (): Promise<void> => {
    if (!isAnthropicAuthEnabled() || isClaudeAISubscriber()) {
      setStatus('valid')
      return
    }
    // Warm the apiKeyHelper cache (no-op if not configured), then read from
    // all sources. getAnthropicApiKeyWithSource() reads the now-warm cache.
    await getApiKeyFromApiKeyHelper(getIsNonInteractiveSession())

```

---


### `src/hooks/useArrowKeyHistory.tsx`

**信息:**
- 行数: 229
- 大小: 34135 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React, { useCallback, useRef, useState } from 'react';
import { getModeFromInput } from 'src/components/PromptInput/inputModes.js';
import { useNotifications } from 'src/context/notifications.js';
import { ConfigurableShortcutHint } from '../components/ConfigurableShortcutHint.js';
import { FOOTER_TEMPORARY_STATUS_TIMEOUT } from '../components/PromptInput/Notifications.js';
import { getHistory } from '../history.js';
import { Text } from '../ink.js';
import type { PromptInputMode } from '../types/textInputTypes.js';
import type { HistoryEntry, PastedContent } from '../utils/config.js';
export type HistoryMode = PromptInputMode;

// Load history entries in chunks to reduce disk reads on rapid keypresses
const HISTORY_CHUNK_SIZE = 10;

// Shared state for batching concurrent load requests into a single disk read
// Mode filter is included to ensure we don't mix filtered and unfiltered caches
let pendingLoad: Promise<HistoryEntry[]> | null = null;
let pendingLoadTarget = 0;
let pendingLoadModeFilter: HistoryMode | undefined = undefined;
async function loadHistoryEntries(minCount: number, modeFilter?: HistoryMode): Promise<HistoryEntry[]> {
  // Round up to next chunk to avoid repeated small reads
  const target = Math.ceil(minCount / HISTORY_CHUNK_SIZE) * HISTORY_CHUNK_SIZE;

  // If a load is already pending with the same mode filter and will satisfy our needs, wait for it
  if (pendingLoad && pendingLoadTarget >= target && pendingLoadModeFilter === modeFilter) {
    return pendingLoad;
  }

  // If a load is pending but won't satisfy our needs or has different filter, we need to wait for it
  // to complete first, then start a new one (can't interrupt an ongoing read)
  if (pendingLoad) {
    await pendingLoad;
  }

  // Start a new load
  pendingLoadTarget = target;
  pendingLoadModeFilter = modeFilter;
  pendingLoad = (async () => {
    const entries: HistoryEntry[] = [];
    let loaded = 0;
    for await (const entry of getHistory()) {
      // If mode filter is specified, only include entries that match the mode
      if (modeFilter) {
        const entryMode = getModeFromInput(entry.display);
        if (entryMode !== modeFilter) {
          continue;
        }
      }
      entries.push(entry);
      loaded++;

```

---


### `src/hooks/useAssistantHistory.ts`

**信息:**
- 行数: 250
- 大小: 9228 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { randomUUID } from 'crypto'
import {
  type RefObject,
  useCallback,
  useEffect,
  useLayoutEffect,
  useRef,
} from 'react'
import {
  createHistoryAuthCtx,
  fetchLatestEvents,
  fetchOlderEvents,
  type HistoryAuthCtx,
  type HistoryPage,
} from '../assistant/sessionHistory.js'
import type { ScrollBoxHandle } from '../ink/components/ScrollBox.js'
import type { RemoteSessionConfig } from '../remote/RemoteSessionManager.js'
import { convertSDKMessage } from '../remote/sdkMessageAdapter.js'
import type { Message, SystemInformationalMessage } from '../types/message.js'
import { logForDebugging } from '../utils/debug.js'

type Props = {
  /** Gated on viewerOnly — non-viewer sessions have no remote history to page. */
  config: RemoteSessionConfig | undefined
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>
  scrollRef: RefObject<ScrollBoxHandle | null>
  /** Called after prepend from the layout effect with message count + height
   *  delta. Lets useUnseenDivider shift dividerIndex + dividerYRef. */
  onPrepend?: (indexDelta: number, heightDelta: number) => void
}

type Result = {
  /** Trigger for ScrollKeybindingHandler's onScroll composition. */
  maybeLoadOlder: (handle: ScrollBoxHandle) => void
}

/** Fire loadOlder when scrolled within this many rows of the top. */
const PREFETCH_THRESHOLD_ROWS = 40

/** Max chained page loads to fill the viewport on mount. Bounds the loop if
 *  events convert to zero visible messages (everything filtered). */
const MAX_FILL_PAGES = 10

const SENTINEL_LOADING = 'loading older messages…'
const SENTINEL_LOADING_FAILED =
  'failed to load older messages — scroll up to retry'
const SENTINEL_START = 'start of session'

/** Convert a HistoryPage to REPL Message[] using the same opts as viewer mode. */
function pageToMessages(page: HistoryPage): Message[] {

```

---


### `src/hooks/useAwaySummary.ts`

**信息:**
- 行数: 125
- 大小: 3835 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { useEffect, useRef } from 'react'
import {
  getTerminalFocusState,
  subscribeTerminalFocus,
} from '../ink/terminal-focus-state.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js'
import { generateAwaySummary } from '../services/awaySummary.js'
import type { Message } from '../types/message.js'
import { createAwaySummaryMessage } from '../utils/messages.js'

const BLUR_DELAY_MS = 5 * 60_000

type SetMessages = (updater: (prev: Message[]) => Message[]) => void

function hasSummarySinceLastUserTurn(messages: readonly Message[]): boolean {
  for (let i = messages.length - 1; i >= 0; i--) {
    const m = messages[i]!
    if (m.type === 'user' && !m.isMeta && !m.isCompactSummary) return false
    if (m.type === 'system' && m.subtype === 'away_summary') return true
  }
  return false
}

/**
 * Appends a "while you were away" summary message after the terminal has been
 * blurred for 5 minutes. Fires only when (a) 5min since blur, (b) no turn in
 * progress, and (c) no existing away_summary since the last user message.
 *
 * Focus state 'unknown' (terminal doesn't support DECSET 1004) is a no-op.
 */
export function useAwaySummary(
  messages: readonly Message[],
  setMessages: SetMessages,
  isLoading: boolean,
): void {
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const abortRef = useRef<AbortController | null>(null)
  const messagesRef = useRef(messages)
  const isLoadingRef = useRef(isLoading)
  const pendingRef = useRef(false)
  const generateRef = useRef<(() => Promise<void>) | null>(null)

  messagesRef.current = messages
  isLoadingRef.current = isLoading

  // 3P default: false
  const gbEnabled = getFeatureValue_CACHED_MAY_BE_STALE(
    'tengu_sedge_lantern',
    false,

```

---


### `src/hooks/useBackgroundTaskNavigation.ts`

**信息:**
- 行数: 251
- 大小: 8553 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef } from 'react'
import { KeyboardEvent } from '../ink/events/keyboard-event.js'
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- backward-compat bridge until REPL wires handleKeyDown to <Box onKeyDown>
import { useInput } from '../ink.js'
import {
  type AppState,
  useAppState,
  useSetAppState,
} from '../state/AppState.js'
import {
  enterTeammateView,
  exitTeammateView,
} from '../state/teammateViewHelpers.js'
import {
  getRunningTeammatesSorted,
  InProcessTeammateTask,
} from '../tasks/InProcessTeammateTask/InProcessTeammateTask.js'
import {
  type InProcessTeammateTaskState,
  isInProcessTeammateTask,
} from '../tasks/InProcessTeammateTask/types.js'
import { isBackgroundTask } from '../tasks/types.js'

// Step teammate selection by delta, wrapping across leader(-1)..teammates(0..n-1)..hide(n).
// First step from a collapsed tree expands it and parks on leader.
function stepTeammateSelection(
  delta: 1 | -1,
  setAppState: (updater: (prev: AppState) => AppState) => void,
): void {
  setAppState(prev => {
    const currentCount = getRunningTeammatesSorted(prev.tasks).length
    if (currentCount === 0) return prev

    if (prev.expandedView !== 'teammates') {
      return {
        ...prev,
        expandedView: 'teammates' as const,
        viewSelectionMode: 'selecting-agent',
        selectedIPAgentIndex: -1,
      }
    }

    const maxIdx = currentCount // hide row
    const cur = prev.selectedIPAgentIndex
    const next =
      delta === 1
        ? cur >= maxIdx
          ? -1
          : cur + 1
        : cur <= -1

```

---


### `src/hooks/useBlink.ts`

**信息:**
- 行数: 34
- 大小: 1279 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { type DOMElement, useAnimationFrame, useTerminalFocus } from '../ink.js'

const BLINK_INTERVAL_MS = 600

/**
 * Hook for synchronized blinking animations that pause when offscreen.
 *
 * Returns a ref to attach to the animated element and the current blink state.
 * All instances blink together because they derive state from the same
 * animation clock. The clock only runs when at least one subscriber is visible.
 * Pauses when the terminal is blurred.
 *
 * @param enabled - Whether blinking is active
 * @returns [ref, isVisible] - Ref to attach to element, true when visible in blink cycle
 *
 * @example
 * function BlinkingDot({ shouldAnimate }) {
 *   const [ref, isVisible] = useBlink(shouldAnimate)
 *   return <Box ref={ref}>{isVisible ? '●' : ' '}</Box>
 * }
 */
export function useBlink(
  enabled: boolean,
  intervalMs: number = BLINK_INTERVAL_MS,
): [ref: (element: DOMElement | null) => void, isVisible: boolean] {
  const focused = useTerminalFocus()
  const [ref, time] = useAnimationFrame(enabled && focused ? intervalMs : null)

  if (!enabled || !focused) return [ref, true]

  // Derive blink state from time - all instances see the same time so they sync
  const isVisible = Math.floor(time / intervalMs) % 2 === 0
  return [ref, isVisible]
}

```

---


### `src/hooks/useCanUseTool.tsx`

**信息:**
- 行数: 204
- 大小: 40206 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import { APIUserAbortError } from '@anthropic-ai/sdk';
import * as React from 'react';
import { useCallback } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { sanitizeToolNameForAnalytics } from 'src/services/analytics/metadata.js';
import type { ToolUseConfirm } from '../components/permissions/PermissionRequest.js';
import { Text } from '../ink.js';
import type { ToolPermissionContext, Tool as ToolType, ToolUseContext } from '../Tool.js';
import { consumeSpeculativeClassifierCheck, peekSpeculativeClassifierCheck } from '../tools/BashTool/bashPermissions.js';
import { BASH_TOOL_NAME } from '../tools/BashTool/toolName.js';
import type { AssistantMessage } from '../types/message.js';
import { recordAutoModeDenial } from '../utils/autoModeDenials.js';
import { clearClassifierChecking, setClassifierApproval, setYoloClassifierApproval } from '../utils/classifierApprovals.js';
import { logForDebugging } from '../utils/debug.js';
import { AbortError } from '../utils/errors.js';
import { logError } from '../utils/log.js';
import type { PermissionDecision } from '../utils/permissions/PermissionResult.js';
import { hasPermissionsToUseTool } from '../utils/permissions/permissions.js';
import { jsonStringify } from '../utils/slowOperations.js';
import { handleCoordinatorPermission } from './toolPermission/handlers/coordinatorHandler.js';
import { handleInteractivePermission } from './toolPermission/handlers/interactiveHandler.js';
import { handleSwarmWorkerPermission } from './toolPermission/handlers/swarmWorkerHandler.js';
import { createPermissionContext, createPermissionQueueOps } from './toolPermission/PermissionContext.js';
import { logPermissionDecision } from './toolPermission/permissionLogging.js';
export type CanUseToolFn<Input extends Record<string, unknown> = Record<string, unknown>> = (tool: ToolType, input: Input, toolUseContext: ToolUseContext, assistantMessage: AssistantMessage, toolUseID: string, forceDecision?: PermissionDecision<Input>) => Promise<PermissionDecision<Input>>;
function useCanUseTool(setToolUseConfirmQueue, setToolPermissionContext) {
  const $ = _c(3);
  let t0;
  if ($[0] !== setToolPermissionContext || $[1] !== setToolUseConfirmQueue) {
    t0 = async (tool, input, toolUseContext, assistantMessage, toolUseID, forceDecision) => new Promise(resolve => {
      const ctx = createPermissionContext(tool, input, toolUseContext, assistantMessage, toolUseID, setToolPermissionContext, createPermissionQueueOps(setToolUseConfirmQueue));
      if (ctx.resolveIfAborted(resolve)) {
        return;
      }
      const decisionPromise = forceDecision !== undefined ? Promise.resolve(forceDecision) : hasPermissionsToUseTool(tool, input, toolUseContext, assistantMessage, toolUseID);
      return decisionPromise.then(async result => {
        if (result.behavior === "allow") {
          if (ctx.resolveIfAborted(resolve)) {
            return;
          }
          if (feature("TRANSCRIPT_CLASSIFIER") && result.decisionReason?.type === "classifier" && result.decisionReason.classifier === "auto-mode") {
            setYoloClassifierApproval(toolUseID, result.decisionReason.reason);
          }
          ctx.logDecision({
            decision: "accept",
            source: "config"
          });
          resolve(ctx.buildAllow(result.updatedInput ?? input, {

```

---


### `src/hooks/useCancelRequest.ts`

**信息:**
- 行数: 276
- 大小: 10127 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * CancelRequestHandler component for handling cancel/escape keybinding.
 *
 * Must be rendered inside KeybindingSetup to have access to the keybinding context.
 * This component renders nothing - it just registers the cancel keybinding handler.
 */
import { useCallback, useRef } from 'react'
import { logEvent } from 'src/services/analytics/index.js'
import type { AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS } from 'src/services/analytics/metadata.js'
import {
  useAppState,
  useAppStateStore,
  useSetAppState,
} from 'src/state/AppState.js'
import { isVimModeEnabled } from '../components/PromptInput/utils.js'
import type { ToolUseConfirm } from '../components/permissions/PermissionRequest.js'
import type { SpinnerMode } from '../components/Spinner/types.js'
import { useNotifications } from '../context/notifications.js'
import { useIsOverlayActive } from '../context/overlayContext.js'
import { useCommandQueue } from '../hooks/useCommandQueue.js'
import { getShortcutDisplay } from '../keybindings/shortcutFormat.js'
import { useKeybinding } from '../keybindings/useKeybinding.js'
import type { Screen } from '../screens/REPL.js'
import { exitTeammateView } from '../state/teammateViewHelpers.js'
import {
  killAllRunningAgentTasks,
  markAgentsNotified,
} from '../tasks/LocalAgentTask/LocalAgentTask.js'
import type { PromptInputMode, VimMode } from '../types/textInputTypes.js'
import {
  clearCommandQueue,
  enqueuePendingNotification,
  hasCommandsInQueue,
} from '../utils/messageQueueManager.js'
import { emitTaskTerminatedSdk } from '../utils/sdkEventQueue.js'

/** Time window in ms during which a second press kills all background agents. */
const KILL_AGENTS_CONFIRM_WINDOW_MS = 3000

type CancelRequestHandlerProps = {
  setToolUseConfirmQueue: (
    f: (toolUseConfirmQueue: ToolUseConfirm[]) => ToolUseConfirm[],
  ) => void
  onCancel: () => void
  onAgentsKilled: () => void
  isMessageSelectorVisible: boolean
  screen: Screen
  abortSignal?: AbortSignal
  popCommandFromQueue?: () => void
  vimMode?: VimMode

```

---


### `src/hooks/useChromeExtensionNotification.tsx`

**信息:**
- 行数: 50
- 大小: 6779 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { Text } from '../ink.js';
import { isClaudeAISubscriber } from '../utils/auth.js';
import { isChromeExtensionInstalled, shouldEnableClaudeInChrome } from '../utils/claudeInChrome/setup.js';
import { isRunningOnHomespace } from '../utils/envUtils.js';
import { useStartupNotification } from './notifs/useStartupNotification.js';
function getChromeFlag(): boolean | undefined {
  if (process.argv.includes('--chrome')) {
    return true;
  }
  if (process.argv.includes('--no-chrome')) {
    return false;
  }
  return undefined;
}
export function useChromeExtensionNotification() {
  useStartupNotification(_temp);
}
async function _temp() {
  const chromeFlag = getChromeFlag();
  if (!shouldEnableClaudeInChrome(chromeFlag)) {
    return null;
  }
  if (true && !isClaudeAISubscriber()) {
    return {
      key: "chrome-requires-subscription",
      jsx: <Text color="error">Claude in Chrome requires a claude.ai subscription</Text>,
      priority: "immediate",
      timeoutMs: 5000
    };
  }
  const installed = await isChromeExtensionInstalled();
  if (!installed && !isRunningOnHomespace()) {
    return {
      key: "chrome-extension-not-detected",
      jsx: <Text color="warning">Chrome extension not detected · https://claude.ai/chrome to install</Text>,
      priority: "immediate",
      timeoutMs: 3000
    };
  }
  if (chromeFlag === undefined) {
    return {
      key: "claude-in-chrome-default-enabled",
      text: "Claude in Chrome enabled \xB7 /chrome",
      priority: "low"
    };
  }
  return null;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlRleHQiLCJpc0NsYXVkZUFJU3Vic2NyaWJlciIsImlzQ2hyb21lRXh0ZW5zaW9uSW5zdGFsbGVkIiwic2hvdWxkRW5hYmxlQ2xhdWRlSW5DaHJvbWUiLCJpc1J1bm5pbmdPbkhvbWVzcGFjZSIsInVzZVN0YXJ0dXBOb3RpZmljYXRpb24iLCJnZXRDaHJvbWVGbGFnIiwicHJvY2VzcyIsImFyZ3YiLCJpbmNsdWRlcyIsInVuZGVmaW5lZCIsInVzZUNocm9tZUV4dGVuc2lvbk5vdGlmaWNhdGlvbiIsIl90ZW1wIiwiY2hyb21lRmxhZyIsImtleSIsImpzeCIsInByaW9yaXR5IiwidGltZW91dE1zIiwiaW5zdGFsbGVkIiwidGV4dCJdLCJzb3VyY2VzIjpbInVzZUNocm9tZUV4dGVuc2lvbk5vdGlmaWNhdGlvbi50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBUZXh0IH0gZnJvbSAnLi4vaW5rLmpzJ1xuaW1wb3J0IHsgaXNDbGF1ZGVBSVN1YnNjcmliZXIgfSBmcm9tICcuLi91dGlscy9hdXRoLmpzJ1xuaW1wb3J0IHtcbiAgaXNDaHJvbWVFeHRlbnNpb25JbnN0YWxsZWQsXG4gIHNob3VsZEVuYWJsZUNsYXVkZUluQ2hyb21lLFxufSBmcm9tICcuLi91dGlscy9jbGF1ZGVJbkNocm9tZS9zZXR1cC5qcydcbmltcG9ydCB7IGlzUnVubmluZ09uSG9tZXNwYWNlIH0gZnJvbSAnLi4vdXRpbHMvZW52VXRpbHMuanMnXG5pbXBvcnQgeyB1c2VTdGFydHVwTm90aWZpY2F0aW9uIH0gZnJvbSAnLi9ub3RpZnMvdXNlU3RhcnR1cE5vdGlmaWNhdGlvbi5qcydcblxuZnVuY3Rpb24gZ2V0Q2hyb21lRmxhZygpOiBib29sZWFuIHwgdW5kZWZpbmVkIHtcbiAgaWYgKHByb2Nlc3MuYXJndi5pbmNsdWRlcygnLS1jaHJvbWUnKSkge1xuICAgIHJldHVybiB0cnVlXG4gIH1cbiAgaWYgKHByb2Nlc3MuYXJndi5pbmNsdWRlcygnLS1uby1jaHJvbWUnKSkge1xuICAgIHJldHVybiBmYWxzZVxuICB9XG4gIHJldHVybiB1bmRlZmluZWRcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHVzZUNocm9tZUV4dGVuc2lvbk5vdGlmaWNhdGlvbigpOiB2b2lkIHtcbiAgdXNlU3RhcnR1cE5vdGlmaWNhdGlvbihhc3luYyAoKSA9PiB7XG4gICAgY29uc3QgY2hyb21lRmxhZyA9IGdldENocm9tZUZsYWcoKVxuICAgIGlmICghc2hvdWxkRW5hYmxlQ2xhdWRlSW5DaHJvbWUoY2hyb21lRmxhZykpIHJldHVybiBudWxsXG5cbiAgICAvLyBDbGF1ZGUgaW4gQ2hyb21lIGlzIG9ubHkgc3VwcG9ydGVkIGZvciBjbGF1ZGUuYWkgc3Vic2NyaWJlcnMgKHVubGVzcyB1c2VyIGlzIGFudClcbiAgICBpZiAoXCJleHRlcm5hbFwiICE9PSAnYW50JyAmJiAhaXNDbGF1ZGVBSVN1YnNjcmliZXIoKSkge1xuICAgICAgcmV0dXJuIHtcbiAgICAgICAga2V5OiAnY2hyb21lLXJlcXVpcmVzLXN1YnNjcmlwdGlvbicsXG4gICAgICAgIGpzeDogKFxuICAgICAgICAgIDxUZXh0IGNvbG9yPVwiZXJyb3JcIj5cbiAgICAgICAgICAgIENsYXVkZSBpbiBDaHJvbWUgcmVxdWlyZXMgYSBjbGF1ZGUuYWkgc3Vic2NyaXB0aW9uXG4gICAgICAgICAgPC9UZXh0PlxuICAgICAgICApLFxuICAgICAgICBwcmlvcml0eTogJ2ltbWVkaWF0ZScsXG4gICAgICAgIHRpbWVvdXRNczogNTAwMCxcbiAgICAgIH1cbiAgICB9XG5cbiAgICBjb25zdCBpbnN0YWxsZWQgPSBhd2FpdCBpc0Nocm9tZUV4dGVuc2lvbkluc3RhbGxlZCgpXG4gICAgaWYgKCFpbnN0YWxsZWQgJiYgIWlzUnVubmluZ09uSG9tZXNwYWNlKCkpIHtcbiAgICAgIC8vIFNraXAgbm90aWZpY2F0aW9uIG9uIEhvbWVzcGFjZSBzaW5jZSBDaHJvbWUgc2V0dXAgcmVxdWlyZXMgZGlmZmVyZW50IHN0ZXBzIChzZWUgZ28vaHNwcm94eSlcbiAgICAgIHJldHVybiB7XG4gICAgICAgIGtleTogJ2Nocm9tZS1leHRlbnNpb24tbm90LWRldGVjdGVkJyxcbiAgICAgICAganN4OiAoXG4gICAgICAgICAgPFRleHQgY29sb3I9XCJ3YXJuaW5nXCI+XG4gICAgICAgICAgICBDaHJvbWUgZXh0ZW5zaW9uIG5vdCBkZXRlY3RlZCDCtyBodHRwczovL2NsYXVkZS5haS9jaHJvbWUgdG8gaW5zdGFsbFxuICAgICAgICAgIDwvVGV4dD5cbiAgICAgICAgKSxcbiAgICAgICAgLy8gVE9ETyhoYWNreW9uKTogTG93ZXIgdGhlIHByaW9yaXR5IGlmIHRoZSBjbGF1ZGUtaW4tY2hyb21lIGludGVncmF0aW9uIGlzIG5vIGxvbmdlciBvcHQtaW5cbiAgICAgICAgcHJpb3JpdHk6ICdpbW1lZGlhdGUnLFxuICAgICAgICB0aW1lb3V0TXM6IDMwMDAsXG4gICAgICB9XG4gICAgfVxuICAgIGlmIChjaHJvbWVGbGFnID09PSB1bmRlZmluZWQpIHtcbiAgICAgIC8vIFNob3cgbG93IHByaW9yaXR5IG5vdGlmaWNhdGlvbiBvbmx5IHdoZW4gQ2hyb21lIGlzIGVuYWJsZWQgYnkgZGVmYXVsdFxuICAgICAgLy8gKG5vdCBleHBsaWNpdGx5IGVuYWJsZWQgd2l0aCAtLWNocm9tZSBvciBkaXNhYmxlZCB3aXRoIC0tbm8tY2hyb21lKVxuICAgICAgcmV0dXJuIHtcbiAgICAgICAga2V5OiAnY2xhdWRlLWluLWNocm9tZS1kZWZhdWx0LWVuYWJsZWQnLFxuICAgICAgICB0ZXh0OiBgQ2xhdWRlIGluIENocm9tZSBlbmFibGVkIMK3IC9jaHJvbWVgLFxuICAgICAgICBwcmlvcml0eTogJ2xvdycsXG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBudWxsXG4gIH0pXG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsSUFBSSxRQUFRLFdBQVc7QUFDaEMsU0FBU0Msb0JBQW9CLFFBQVEsa0JBQWtCO0FBQ3ZELFNBQ0VDLDBCQUEwQixFQUMxQkMsMEJBQTBCLFFBQ3JCLGtDQUFrQztBQUN6QyxTQUFTQyxvQkFBb0IsUUFBUSxzQkFBc0I7QUFDM0QsU0FBU0Msc0JBQXNCLFFBQVEsb0NBQW9DO0FBRTNFLFNBQVNDLGFBQWFBLENBQUEsQ0FBRSxFQUFFLE9BQU8sR0FBRyxTQUFTLENBQUM7RUFDNUMsSUFBSUMsT0FBTyxDQUFDQyxJQUFJLENBQUNDLFFBQVEsQ0FBQyxVQUFVLENBQUMsRUFBRTtJQUNyQyxPQUFPLElBQUk7RUFDYjtFQUNBLElBQUlGLE9BQU8sQ0FBQ0MsSUFBSSxDQUFDQyxRQUFRLENBQUMsYUFBYSxDQUFDLEVBQUU7SUFDeEMsT0FBTyxLQUFLO0VBQ2Q7RUFDQSxPQUFPQyxTQUFTO0FBQ2xCO0FBRUEsT0FBTyxTQUFBQywrQkFBQTtFQUNMTixzQkFBc0IsQ0FBQ08sS0EyQ3RCLENBQUM7QUFBQTtBQTVDRyxlQUFBQSxNQUFBO0VBRUgsTUFBQUMsVUFBQSxHQUFtQlAsYUFBYSxDQUFDLENBQUM7RUFDbEMsSUFBSSxDQUFDSCwwQkFBMEIsQ0FBQ1UsVUFBVSxDQUFDO0lBQUEsT0FBUyxJQUFJO0VBQUE7RUFHeEQsSUFBSSxJQUErQyxJQUEvQyxDQUF5Qlosb0JBQW9CLENBQUMsQ0FBQztJQUFBLE9BQzFDO01BQUFhLEdBQUEsRUFDQSw4QkFBOEI7TUFBQUMsR0FBQSxFQUVqQyxDQUFDLElBQUksQ0FBTyxLQUFPLENBQVAsT0FBTyxDQUFDLGtEQUVwQixFQUZDLElBQUksQ0FFRTtNQUFBQyxRQUFBLEVBRUMsV0FBVztNQUFBQyxTQUFBLEVBQ1Y7SUFDYixDQUFDO0VBQUE7RUFHSCxNQUFBQyxTQUFBLEdBQWtCLE1BQU1oQiwwQkFBMEIsQ0FBQyxDQUFDO0VBQ3BELElBQUksQ0FBQ2dCLFNBQW9DLElBQXJDLENBQWVkLG9CQUFvQixDQUFDLENBQUM7SUFBQSxPQUVoQztNQUFBVSxHQUFBLEVBQ0EsK0JBQStCO01BQUFDLEdBQUEsRUFFbEMsQ0FBQyxJQUFJLENBQU8sS0FBUyxDQUFULFNBQVMsQ0FBQyxtRUFFdEIsRUFGQyxJQUFJLENBRUU7TUFBQUMsUUFBQSxFQUdDLFdBQVc7TUFBQUMsU0FBQSxFQUNWO0lBQ2IsQ0FBQztFQUFBO0VBRUgsSUFBSUosVUFBVSxLQUFLSCxTQUFTO0lBQUEsT0FHbkI7TUFBQUksR0FBQSxFQUNBLGtDQUFrQztNQUFBSyxJQUFBLEVBQ2pDLHVDQUFvQztNQUFBSCxRQUFBLEVBQ2hDO0lBQ1osQ0FBQztFQUFBO0VBQ0YsT0FDTSxJQUFJO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/hooks/useClaudeCodeHintRecommendation.tsx`

**信息:**
- 行数: 129
- 大小: 15388 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * Surfaces plugin-install prompts driven by `<claude-code-hint />` tags
 * that CLIs/SDKs emit to stderr. See docs/claude-code-hints.md.
 *
 * Show-once semantics: each plugin is prompted for at most once ever,
 * recorded in config regardless of yes/no. The pre-store gate in
 * maybeRecordPluginHint already dropped installed/shown/capped hints, so
 * anything that reaches this hook is worth resolving.
 */

import * as React from 'react';
import { useNotifications } from '../context/notifications.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, type AnalyticsMetadata_I_VERIFIED_THIS_IS_PII_TAGGED, logEvent } from '../services/analytics/index.js';
import { clearPendingHint, getPendingHintSnapshot, markShownThisSession, subscribeToPendingHint } from '../utils/claudeCodeHints.js';
import { logForDebugging } from '../utils/debug.js';
import { disableHintRecommendations, markHintPluginShown, type PluginHintRecommendation, resolvePluginHint } from '../utils/plugins/hintRecommendation.js';
import { installPluginFromMarketplace } from '../utils/plugins/pluginInstallationHelpers.js';
import { installPluginAndNotify, usePluginRecommendationBase } from './usePluginRecommendationBase.js';
type UseClaudeCodeHintRecommendationResult = {
  recommendation: PluginHintRecommendation | null;
  handleResponse: (response: 'yes' | 'no' | 'disable') => void;
};
export function useClaudeCodeHintRecommendation() {
  const $ = _c(11);
  const pendingHint = React.useSyncExternalStore(subscribeToPendingHint, getPendingHintSnapshot);
  const {
    addNotification
  } = useNotifications();
  const {
    recommendation,
    clearRecommendation,
    tryResolve
  } = usePluginRecommendationBase();
  let t0;
  let t1;
  if ($[0] !== pendingHint || $[1] !== tryResolve) {
    t0 = () => {
      if (!pendingHint) {
        return;
      }
      tryResolve(async () => {
        const resolved = await resolvePluginHint(pendingHint);
        if (resolved) {
          logForDebugging(`[useClaudeCodeHintRecommendation] surfacing ${resolved.pluginId} from ${resolved.sourceCommand}`);
          markShownThisSession();
        }
        if (getPendingHintSnapshot() === pendingHint) {
          clearPendingHint();
        }

```

---


### `src/hooks/useClipboardImageHint.ts`

**信息:**
- 行数: 77
- 大小: 2458 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef } from 'react'
import { useNotifications } from '../context/notifications.js'
import { getShortcutDisplay } from '../keybindings/shortcutFormat.js'
import { hasImageInClipboard } from '../utils/imagePaste.js'

const NOTIFICATION_KEY = 'clipboard-image-hint'
// Small debounce to batch rapid focus changes
const FOCUS_CHECK_DEBOUNCE_MS = 1000
// Don't show the hint more than once per this interval
const HINT_COOLDOWN_MS = 30000

/**
 * Hook that shows a notification when the terminal regains focus
 * and the clipboard contains an image.
 *
 * @param isFocused - Whether the terminal is currently focused
 * @param enabled - Whether image paste is enabled (onImagePaste is defined)
 */
export function useClipboardImageHint(
  isFocused: boolean,
  enabled: boolean,
): void {
  const { addNotification } = useNotifications()
  const lastFocusedRef = useRef(isFocused)
  const lastHintTimeRef = useRef(0)
  const checkTimeoutRef = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    // Only trigger on focus regain (was unfocused, now focused)
    const wasFocused = lastFocusedRef.current
    lastFocusedRef.current = isFocused

    if (!enabled || !isFocused || wasFocused) {
      return
    }

    // Clear any pending check
    if (checkTimeoutRef.current) {
      clearTimeout(checkTimeoutRef.current)
    }

    // Small debounce to batch rapid focus changes
    checkTimeoutRef.current = setTimeout(
      async (checkTimeoutRef, lastHintTimeRef, addNotification) => {
        checkTimeoutRef.current = null

        // Check cooldown to avoid spamming the user
        const now = Date.now()
        if (now - lastHintTimeRef.current < HINT_COOLDOWN_MS) {
          return

```

---


### `src/hooks/useCommandKeybindings.tsx`

**信息:**
- 行数: 108
- 大小: 11023 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * Component that registers keybinding handlers for command bindings.
 *
 * Must be rendered inside KeybindingSetup to have access to the keybinding context.
 * Reads "command:*" actions from the current keybinding configuration and registers
 * handlers that invoke the corresponding slash command via onSubmit.
 *
 * Commands triggered via keybinding are treated as "immediate" - they execute right
 * away and preserve the user's existing input text (the prompt is not cleared).
 */
import { useMemo } from 'react';
import { useIsModalOverlayActive } from '../context/overlayContext.js';
import { useOptionalKeybindingContext } from '../keybindings/KeybindingContext.js';
import { useKeybindings } from '../keybindings/useKeybinding.js';
import type { PromptInputHelpers } from '../utils/handlePromptSubmit.js';
type Props = {
  // onSubmit accepts additional parameters beyond what we pass here,
  // so we use a rest parameter to allow any additional args
  onSubmit: (input: string, helpers: PromptInputHelpers, ...rest: [speculationAccept?: undefined, options?: {
    fromKeybinding?: boolean;
  }]) => void;
  /** Set to false to disable command keybindings (e.g., when a dialog is open) */
  isActive?: boolean;
};
const NOOP_HELPERS: PromptInputHelpers = {
  setCursorOffset: () => {},
  clearBuffer: () => {},
  resetHistory: () => {}
};

/**
 * Registers keybinding handlers for all "command:*" actions found in the
 * user's keybinding configuration. When triggered, each handler submits
 * the corresponding slash command (e.g., "command:commit" submits "/commit").
 */
export function CommandKeybindingHandlers(t0) {
  const $ = _c(8);
  const {
    onSubmit,
    isActive: t1
  } = t0;
  const isActive = t1 === undefined ? true : t1;
  const keybindingContext = useOptionalKeybindingContext();
  const isModalOverlayActive = useIsModalOverlayActive();
  let t2;
  bb0: {
    if (!keybindingContext) {
      let t3;
      if ($[0] === Symbol.for("react.memo_cache_sentinel")) {

```

---


### `src/hooks/useCommandQueue.ts`

**信息:**
- 行数: 15
- 大小: 543 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useSyncExternalStore } from 'react'
import type { QueuedCommand } from '../types/textInputTypes.js'
import {
  getCommandQueueSnapshot,
  subscribeToCommandQueue,
} from '../utils/messageQueueManager.js'

/**
 * React hook to subscribe to the unified command queue.
 * Returns a frozen array that only changes reference on mutation.
 * Components re-render only when the queue changes.
 */
export function useCommandQueue(): readonly QueuedCommand[] {
  return useSyncExternalStore(subscribeToCommandQueue, getCommandQueueSnapshot)
}

```

---


### `src/hooks/useCopyOnSelect.ts`

**信息:**
- 行数: 98
- 大小: 4287 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef } from 'react'
import { useTheme } from '../components/design-system/ThemeProvider.js'
import type { useSelection } from '../ink/hooks/use-selection.js'
import { getGlobalConfig } from '../utils/config.js'
import { getTheme } from '../utils/theme.js'

type Selection = ReturnType<typeof useSelection>

/**
 * Auto-copy the selection to the clipboard when the user finishes dragging
 * (mouse-up with a non-empty selection) or multi-clicks to select a word/line.
 * Mirrors iTerm2's "Copy to pasteboard on selection" — the highlight is left
 * intact so the user can see what was copied. Only fires in alt-screen mode
 * (selection state is ink-instance-owned; outside alt-screen, the native
 * terminal handles selection and this hook is a no-op via the ink stub).
 *
 * selection.subscribe fires on every mutation (start/update/finish/clear/
 * multiclick). Both char drags and multi-clicks set isDragging=true while
 * pressed, so a selection appearing with isDragging=false is always a
 * drag-finish. copiedRef guards against double-firing on spurious notifies.
 *
 * onCopied is optional — when omitted, copy is silent (clipboard is written
 * but no toast/notification fires). FleetView uses this silent mode; the
 * fullscreen REPL passes showCopiedToast for user feedback.
 */
export function useCopyOnSelect(
  selection: Selection,
  isActive: boolean,
  onCopied?: (text: string) => void,
): void {
  // Tracks whether the *previous* notification had a visible selection with
  // isDragging=false (i.e., we already auto-copied it). Without this, the
  // finish→clear transition would look like a fresh selection-gone-idle
  // event and we'd toast twice for a single drag.
  const copiedRef = useRef(false)
  // onCopied is a fresh closure each render; read through a ref so the
  // effect doesn't re-subscribe (which would reset copiedRef via unmount).
  const onCopiedRef = useRef(onCopied)
  onCopiedRef.current = onCopied

  useEffect(() => {
    if (!isActive) return

    const unsubscribe = selection.subscribe(() => {
      const sel = selection.getState()
      const has = selection.hasSelection()
      // Drag in progress — wait for finish. Reset copied flag so a new drag
      // that ends on the same range still triggers a fresh copy.
      if (sel?.isDragging) {
        copiedRef.current = false

```

---


### `src/hooks/useDeferredHookMessages.ts`

**信息:**
- 行数: 46
- 大小: 1499 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useEffect, useRef } from 'react'
import type { HookResultMessage, Message } from '../types/message.js'

/**
 * Manages deferred SessionStart hook messages so the REPL can render
 * immediately instead of blocking on hook execution (~500ms).
 *
 * Hook messages are injected asynchronously when the promise resolves.
 * Returns a callback that onSubmit should call before the first API
 * request to ensure the model always sees hook context.
 */
export function useDeferredHookMessages(
  pendingHookMessages: Promise<HookResultMessage[]> | undefined,
  setMessages: (action: React.SetStateAction<Message[]>) => void,
): () => Promise<void> {
  const pendingRef = useRef(pendingHookMessages ?? null)
  const resolvedRef = useRef(!pendingHookMessages)

  useEffect(() => {
    const promise = pendingRef.current
    if (!promise) return
    let cancelled = false
    promise.then(msgs => {
      if (cancelled) return
      resolvedRef.current = true
      pendingRef.current = null
      if (msgs.length > 0) {
        setMessages(prev => [...msgs, ...prev])
      }
    })
    return () => {
      cancelled = true
    }
  }, [setMessages])

  return useCallback(async () => {
    if (resolvedRef.current || !pendingRef.current) return
    const msgs = await pendingRef.current
    if (resolvedRef.current) return
    resolvedRef.current = true
    pendingRef.current = null
    if (msgs.length > 0) {
      setMessages(prev => [...msgs, ...prev])
    }
  }, [setMessages])
}

```

---


### `src/hooks/useDiffData.ts`

**信息:**
- 行数: 110
- 大小: 2839 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { StructuredPatchHunk } from 'diff'
import { useEffect, useMemo, useState } from 'react'
import {
  fetchGitDiff,
  fetchGitDiffHunks,
  type GitDiffResult,
  type GitDiffStats,
} from '../utils/gitDiff.js'

const MAX_LINES_PER_FILE = 400

export type DiffFile = {
  path: string
  linesAdded: number
  linesRemoved: number
  isBinary: boolean
  isLargeFile: boolean
  isTruncated: boolean
  isNewFile?: boolean
  isUntracked?: boolean
}

export type DiffData = {
  stats: GitDiffStats | null
  files: DiffFile[]
  hunks: Map<string, StructuredPatchHunk[]>
  loading: boolean
}

/**
 * Hook to fetch current git diff data on demand.
 * Fetches both stats and hunks when component mounts.
 */
export function useDiffData(): DiffData {
  const [diffResult, setDiffResult] = useState<GitDiffResult | null>(null)
  const [hunks, setHunks] = useState<Map<string, StructuredPatchHunk[]>>(
    new Map(),
  )
  const [loading, setLoading] = useState(true)

  // Fetch diff data on mount
  useEffect(() => {
    let cancelled = false

    async function loadDiffData() {
      try {
        // Fetch both stats and hunks
        const [statsResult, hunksResult] = await Promise.all([
          fetchGitDiff(),
          fetchGitDiffHunks(),

```

---


### `src/hooks/useDiffInIDE.ts`

**信息:**
- 行数: 379
- 大小: 9867 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { randomUUID } from 'crypto'
import { basename } from 'path'
import { useEffect, useMemo, useRef, useState } from 'react'
import { logEvent } from 'src/services/analytics/index.js'
import { readFileSync } from 'src/utils/fileRead.js'
import { expandPath } from 'src/utils/path.js'
import type { PermissionOption } from '../components/permissions/FilePermissionDialog/permissionOptions.js'
import type {
  MCPServerConnection,
  McpSSEIDEServerConfig,
  McpWebSocketIDEServerConfig,
} from '../services/mcp/types.js'
import type { ToolUseContext } from '../Tool.js'
import type { FileEdit } from '../tools/FileEditTool/types.js'
import {
  getEditsForPatch,
  getPatchForEdits,
} from '../tools/FileEditTool/utils.js'
import { getGlobalConfig } from '../utils/config.js'
import { getPatchFromContents } from '../utils/diff.js'
import { isENOENT } from '../utils/errors.js'
import {
  callIdeRpc,
  getConnectedIdeClient,
  getConnectedIdeName,
  hasAccessToIDEExtensionDiffFeature,
} from '../utils/ide.js'
import { WindowsToWSLConverter } from '../utils/idePathConversion.js'
import { logError } from '../utils/log.js'
import { getPlatform } from '../utils/platform.js'

type Props = {
  onChange(
    option: PermissionOption,
    input: {
      file_path: string
      edits: FileEdit[]
    },
  ): void
  toolUseContext: ToolUseContext
  filePath: string
  edits: FileEdit[]
  editMode: 'single' | 'multiple'
}

export function useDiffInIDE({
  onChange,
  toolUseContext,
  filePath,
  edits,

```

---


### `src/hooks/useDirectConnect.ts`

**信息:**
- 行数: 229
- 大小: 7504 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useEffect, useMemo, useRef } from 'react'
import type { ToolUseConfirm } from '../components/permissions/PermissionRequest.js'
import type { RemotePermissionResponse } from '../remote/RemoteSessionManager.js'
import {
  createSyntheticAssistantMessage,
  createToolStub,
} from '../remote/remotePermissionBridge.js'
import {
  convertSDKMessage,
  isSessionEndMessage,
} from '../remote/sdkMessageAdapter.js'
import {
  type DirectConnectConfig,
  DirectConnectSessionManager,
} from '../server/directConnectManager.js'
import type { Tool } from '../Tool.js'
import { findToolByName } from '../Tool.js'
import type { Message as MessageType } from '../types/message.js'
import type { PermissionAskDecision } from '../types/permissions.js'
import { logForDebugging } from '../utils/debug.js'
import { gracefulShutdown } from '../utils/gracefulShutdown.js'
import type { RemoteMessageContent } from '../utils/teleport/api.js'

type UseDirectConnectResult = {
  isRemoteMode: boolean
  sendMessage: (content: RemoteMessageContent) => Promise<boolean>
  cancelRequest: () => void
  disconnect: () => void
}

type UseDirectConnectProps = {
  config: DirectConnectConfig | undefined
  setMessages: React.Dispatch<React.SetStateAction<MessageType[]>>
  setIsLoading: (loading: boolean) => void
  setToolUseConfirmQueue: React.Dispatch<React.SetStateAction<ToolUseConfirm[]>>
  tools: Tool[]
}

export function useDirectConnect({
  config,
  setMessages,
  setIsLoading,
  setToolUseConfirmQueue,
  tools,
}: UseDirectConnectProps): UseDirectConnectResult {
  const isRemoteMode = !!config

  const managerRef = useRef<DirectConnectSessionManager | null>(null)
  const hasReceivedInitRef = useRef(false)
  const isConnectedRef = useRef(false)

```

---


### `src/hooks/useDoublePress.ts`

**信息:**
- 行数: 62
- 大小: 1651 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Creates a function that calls one function on the first call and another
// function on the second call within a certain timeout

import { useCallback, useEffect, useRef } from 'react'

export const DOUBLE_PRESS_TIMEOUT_MS = 800

export function useDoublePress(
  setPending: (pending: boolean) => void,
  onDoublePress: () => void,
  onFirstPress?: () => void,
): () => void {
  const lastPressRef = useRef<number>(0)
  const timeoutRef = useRef<NodeJS.Timeout | undefined>(undefined)

  const clearTimeoutSafe = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
      timeoutRef.current = undefined
    }
  }, [])

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      clearTimeoutSafe()
    }
  }, [clearTimeoutSafe])

  return useCallback(() => {
    const now = Date.now()
    const timeSinceLastPress = now - lastPressRef.current
    const isDoublePress =
      timeSinceLastPress <= DOUBLE_PRESS_TIMEOUT_MS &&
      timeoutRef.current !== undefined

    if (isDoublePress) {
      // Double press detected
      clearTimeoutSafe()
      setPending(false)
      onDoublePress()
    } else {
      // First press
      onFirstPress?.()
      setPending(true)

      // Clear any existing timeout and set new one
      clearTimeoutSafe()
      timeoutRef.current = setTimeout(
        (setPending, timeoutRef) => {

```

---


### `src/hooks/useDynamicConfig.ts`

**信息:**
- 行数: 22
- 大小: 703 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import React from 'react'
import { getDynamicConfig_BLOCKS_ON_INIT } from '../services/analytics/growthbook.js'

/**
 * React hook for dynamic config values.
 * Returns the default value initially, then updates when the config is fetched.
 */
export function useDynamicConfig<T>(configName: string, defaultValue: T): T {
  const [configValue, setConfigValue] = React.useState<T>(defaultValue)

  React.useEffect(() => {
    if (process.env.NODE_ENV === 'test') {
      // Prevents a test hang when using this hook in tests
      return
    }
    void getDynamicConfig_BLOCKS_ON_INIT<T>(configName, defaultValue).then(
      setConfigValue,
    )
  }, [configName, defaultValue])

  return configValue
}

```

---


### `src/hooks/useElapsedTime.ts`

**信息:**
- 行数: 37
- 大小: 1226 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useSyncExternalStore } from 'react'
import { formatDuration } from '../utils/format.js'

/**
 * Hook that returns formatted elapsed time since startTime.
 * Uses useSyncExternalStore with interval-based updates for efficiency.
 *
 * @param startTime - Unix timestamp in ms
 * @param isRunning - Whether to actively update the timer
 * @param ms - How often should we trigger updates?
 * @param pausedMs - Total paused duration to subtract
 * @param endTime - If set, freezes the duration at this timestamp (for
 *   terminal tasks). Without this, viewing a 2-min task 30 min after
 *   completion would show "32m".
 * @returns Formatted duration string (e.g., "1m 23s")
 */
export function useElapsedTime(
  startTime: number,
  isRunning: boolean,
  ms: number = 1000,
  pausedMs: number = 0,
  endTime?: number,
): string {
  const get = () =>
    formatDuration(Math.max(0, (endTime ?? Date.now()) - startTime - pausedMs))

  const subscribe = useCallback(
    (notify: () => void) => {
      if (!isRunning) return () => {}
      const interval = setInterval(notify, ms)
      return () => clearInterval(interval)
    },
    [isRunning, ms],
  )

  return useSyncExternalStore(subscribe, get, get)
}

```

---


### `src/hooks/useExitOnCtrlCD.ts`

**信息:**
- 行数: 95
- 大小: 3226 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useMemo, useState } from 'react'
import useApp from '../ink/hooks/use-app.js'
import type { KeybindingContextName } from '../keybindings/types.js'
import { useDoublePress } from './useDoublePress.js'

export type ExitState = {
  pending: boolean
  keyName: 'Ctrl-C' | 'Ctrl-D' | null
}

type KeybindingOptions = {
  context?: KeybindingContextName
  isActive?: boolean
}

type UseKeybindingsHook = (
  handlers: Record<string, () => void>,
  options?: KeybindingOptions,
) => void

/**
 * Handle ctrl+c and ctrl+d for exiting the application.
 *
 * Uses a time-based double-press mechanism:
 * - First press: Shows "Press X again to exit" message
 * - Second press within timeout: Exits the application
 *
 * Note: We use time-based double-press rather than the chord system because
 * we want the first ctrl+c to also trigger interrupt (handled elsewhere).
 * The chord system would prevent the first press from firing any action.
 *
 * These keys are hardcoded and cannot be rebound via keybindings.json.
 *
 * @param useKeybindingsHook - The useKeybindings hook to use for registering handlers
 *                            (dependency injection to avoid import cycles)
 * @param onInterrupt - Optional callback for features to handle interrupt (ctrl+c).
 *                      Return true if handled, false to fall through to double-press exit.
 * @param onExit - Optional custom exit handler
 * @param isActive - Whether the keybinding is active (default true). Set false
 *                   while an embedded TextInput is focused — TextInput's own
 *                   ctrl+c/d handlers will manage cancel/exit, and Dialog's
 *                   handler would otherwise double-fire (child useInput runs
 *                   before parent useKeybindings, so both see every keypress).
 */
export function useExitOnCtrlCD(
  useKeybindingsHook: UseKeybindingsHook,
  onInterrupt?: () => boolean,
  onExit?: () => void,
  isActive = true,
): ExitState {

```

---


### `src/hooks/useExitOnCtrlCDWithKeybindings.ts`

**信息:**
- 行数: 24
- 大小: 948 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useKeybindings } from '../keybindings/useKeybinding.js'
import { type ExitState, useExitOnCtrlCD } from './useExitOnCtrlCD.js'

export type { ExitState }

/**
 * Convenience hook that wires up useExitOnCtrlCD with useKeybindings.
 *
 * This is the standard way to use useExitOnCtrlCD in components.
 * The separation exists to avoid import cycles - useExitOnCtrlCD.ts
 * doesn't import from the keybindings module directly.
 *
 * @param onExit - Optional custom exit handler
 * @param onInterrupt - Optional callback for features to handle interrupt (ctrl+c).
 *                      Return true if handled, false to fall through to double-press exit.
 * @param isActive - Whether the keybinding is active (default true).
 */
export function useExitOnCtrlCDWithKeybindings(
  onExit?: () => void,
  onInterrupt?: () => boolean,
  isActive?: boolean,
): ExitState {
  return useExitOnCtrlCD(useKeybindings, onInterrupt, onExit, isActive)
}

```

---


### `src/hooks/useFileHistorySnapshotInit.ts`

**信息:**
- 行数: 25
- 大小: 767 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef } from 'react'
import {
  type FileHistorySnapshot,
  type FileHistoryState,
  fileHistoryEnabled,
  fileHistoryRestoreStateFromLog,
} from '../utils/fileHistory.js'

export function useFileHistorySnapshotInit(
  initialFileHistorySnapshots: FileHistorySnapshot[] | undefined,
  fileHistoryState: FileHistoryState,
  onUpdateState: (newState: FileHistoryState) => void,
): void {
  const initialized = useRef(false)

  useEffect(() => {
    if (!fileHistoryEnabled() || initialized.current) {
      return
    }
    initialized.current = true
    if (initialFileHistorySnapshots) {
      fileHistoryRestoreStateFromLog(initialFileHistorySnapshots, onUpdateState)
    }
  }, [fileHistoryState, initialFileHistorySnapshots, onUpdateState])
}

```

---


### `src/hooks/useGlobalKeybindings.tsx`

**信息:**
- 行数: 249
- 大小: 31213 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
/**
 * Component that registers global keybinding handlers.
 *
 * Must be rendered inside KeybindingSetup to have access to the keybinding context.
 * This component renders nothing - it just registers the keybinding handlers.
 */
import { feature } from 'bun:bundle';
import { useCallback } from 'react';
import instances from '../ink/instances.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import type { Screen } from '../screens/REPL.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../services/analytics/index.js';
import { useAppState, useSetAppState } from '../state/AppState.js';
import { count } from '../utils/array.js';
import { getTerminalPanel } from '../utils/terminalPanel.js';
type Props = {
  screen: Screen;
  setScreen: React.Dispatch<React.SetStateAction<Screen>>;
  showAllInTranscript: boolean;
  setShowAllInTranscript: React.Dispatch<React.SetStateAction<boolean>>;
  messageCount: number;
  onEnterTranscript?: () => void;
  onExitTranscript?: () => void;
  virtualScrollActive?: boolean;
  searchBarOpen?: boolean;
};

/**
 * Registers global keybinding handlers for:
 * - ctrl+t: Toggle todo list
 * - ctrl+o: Toggle transcript mode
 * - ctrl+e: Toggle showing all messages in transcript
 * - ctrl+c/escape: Exit transcript mode
 */
export function GlobalKeybindingHandlers({
  screen,
  setScreen,
  showAllInTranscript,
  setShowAllInTranscript,
  messageCount,
  onEnterTranscript,
  onExitTranscript,
  virtualScrollActive,
  searchBarOpen = false
}: Props): null {
  const expandedView = useAppState(s => s.expandedView);
  const setAppState = useSetAppState();

  // Toggle todo list (ctrl+t) - cycles through views

```

---


### `src/hooks/useHistorySearch.ts`

**信息:**
- 行数: 303
- 大小: 9488 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import {
  getModeFromInput,
  getValueFromInput,
} from '../components/PromptInput/inputModes.js'
import { makeHistoryReader } from '../history.js'
import { KeyboardEvent } from '../ink/events/keyboard-event.js'
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- backward-compat bridge until consumers wire handleKeyDown to <Box onKeyDown>
import { useInput } from '../ink.js'
import { useKeybinding, useKeybindings } from '../keybindings/useKeybinding.js'
import type { PromptInputMode } from '../types/textInputTypes.js'
import type { HistoryEntry } from '../utils/config.js'

export function useHistorySearch(
  onAcceptHistory: (entry: HistoryEntry) => void,
  currentInput: string,
  onInputChange: (input: string) => void,
  onCursorChange: (cursorOffset: number) => void,
  currentCursorOffset: number,
  onModeChange: (mode: PromptInputMode) => void,
  currentMode: PromptInputMode,
  isSearching: boolean,
  setIsSearching: (isSearching: boolean) => void,
  setPastedContents: (pastedContents: HistoryEntry['pastedContents']) => void,
  currentPastedContents: HistoryEntry['pastedContents'],
): {
  historyQuery: string
  setHistoryQuery: (query: string) => void
  historyMatch: HistoryEntry | undefined
  historyFailedMatch: boolean
  handleKeyDown: (e: KeyboardEvent) => void
} {
  const [historyQuery, setHistoryQuery] = useState('')
  const [historyFailedMatch, setHistoryFailedMatch] = useState(false)
  const [originalInput, setOriginalInput] = useState('')
  const [originalCursorOffset, setOriginalCursorOffset] = useState(0)
  const [originalMode, setOriginalMode] = useState<PromptInputMode>('prompt')
  const [originalPastedContents, setOriginalPastedContents] = useState<
    HistoryEntry['pastedContents']
  >({})
  const [historyMatch, setHistoryMatch] = useState<HistoryEntry | undefined>(
    undefined,
  )
  const historyReader = useRef<AsyncGenerator<HistoryEntry> | undefined>(
    undefined,
  )
  const seenPrompts = useRef<Set<string>>(new Set())
  const searchAbortController = useRef<AbortController | null>(null)


```

---


### `src/hooks/useIDEIntegration.tsx`

**信息:**
- 行数: 70
- 大小: 10517 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { useEffect } from 'react';
import type { ScopedMcpServerConfig } from '../services/mcp/types.js';
import { getGlobalConfig } from '../utils/config.js';
import { isEnvDefinedFalsy, isEnvTruthy } from '../utils/envUtils.js';
import type { DetectedIDEInfo } from '../utils/ide.js';
import { type IDEExtensionInstallationStatus, type IdeType, initializeIdeIntegration, isSupportedTerminal } from '../utils/ide.js';
type UseIDEIntegrationProps = {
  autoConnectIdeFlag?: boolean;
  ideToInstallExtension: IdeType | null;
  setDynamicMcpConfig: React.Dispatch<React.SetStateAction<Record<string, ScopedMcpServerConfig> | undefined>>;
  setShowIdeOnboarding: React.Dispatch<React.SetStateAction<boolean>>;
  setIDEInstallationState: React.Dispatch<React.SetStateAction<IDEExtensionInstallationStatus | null>>;
};
export function useIDEIntegration(t0) {
  const $ = _c(7);
  const {
    autoConnectIdeFlag,
    ideToInstallExtension,
    setDynamicMcpConfig,
    setShowIdeOnboarding,
    setIDEInstallationState
  } = t0;
  let t1;
  let t2;
  if ($[0] !== autoConnectIdeFlag || $[1] !== ideToInstallExtension || $[2] !== setDynamicMcpConfig || $[3] !== setIDEInstallationState || $[4] !== setShowIdeOnboarding) {
    t1 = () => {
      const addIde = function addIde(ide) {
        if (!ide) {
          return;
        }
        const globalConfig = getGlobalConfig();
        const autoConnectEnabled = (globalConfig.autoConnectIde || autoConnectIdeFlag || isSupportedTerminal() || process.env.CLAUDE_CODE_SSE_PORT || ideToInstallExtension || isEnvTruthy(process.env.CLAUDE_CODE_AUTO_CONNECT_IDE)) && !isEnvDefinedFalsy(process.env.CLAUDE_CODE_AUTO_CONNECT_IDE);
        if (!autoConnectEnabled) {
          return;
        }
        setDynamicMcpConfig(prev => {
          if (prev?.ide) {
            return prev;
          }
          return {
            ...prev,
            ide: {
              type: ide.url.startsWith("ws:") ? "ws-ide" : "sse-ide",
              url: ide.url,
              ideName: ide.name,
              authToken: ide.authToken,
              ideRunningInWindows: ide.ideRunningInWindows,
              scope: "dynamic" as const
            }

```

---


### `src/hooks/useIdeAtMentioned.ts`

**信息:**
- 行数: 76
- 大小: 2217 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef } from 'react'
import { logError } from 'src/utils/log.js'
import { z } from 'zod/v4'
import type {
  ConnectedMCPServer,
  MCPServerConnection,
} from '../services/mcp/types.js'
import { getConnectedIdeClient } from '../utils/ide.js'
import { lazySchema } from '../utils/lazySchema.js'
export type IDEAtMentioned = {
  filePath: string
  lineStart?: number
  lineEnd?: number
}

const NOTIFICATION_METHOD = 'at_mentioned'

const AtMentionedSchema = lazySchema(() =>
  z.object({
    method: z.literal(NOTIFICATION_METHOD),
    params: z.object({
      filePath: z.string(),
      lineStart: z.number().optional(),
      lineEnd: z.number().optional(),
    }),
  }),
)

/**
 * A hook that tracks IDE at-mention notifications by directly registering
 * with MCP client notification handlers,
 */
export function useIdeAtMentioned(
  mcpClients: MCPServerConnection[],
  onAtMentioned: (atMentioned: IDEAtMentioned) => void,
): void {
  const ideClientRef = useRef<ConnectedMCPServer | undefined>(undefined)

  useEffect(() => {
    // Find the IDE client from the MCP clients list
    const ideClient = getConnectedIdeClient(mcpClients)

    if (ideClientRef.current !== ideClient) {
      ideClientRef.current = ideClient
    }

    // If we found a connected IDE client, register our handler
    if (ideClient) {
      ideClient.client.setNotificationHandler(
        AtMentionedSchema(),

```

---


### `src/hooks/useIdeConnectionStatus.ts`

**信息:**
- 行数: 33
- 大小: 981 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useMemo } from 'react'
import type { MCPServerConnection } from '../services/mcp/types.js'

export type IdeStatus = 'connected' | 'disconnected' | 'pending' | null

type IdeConnectionResult = {
  status: IdeStatus
  ideName: string | null
}

export function useIdeConnectionStatus(
  mcpClients?: MCPServerConnection[],
): IdeConnectionResult {
  return useMemo(() => {
    const ideClient = mcpClients?.find(client => client.name === 'ide')
    if (!ideClient) {
      return { status: null, ideName: null }
    }
    // Extract IDE name from config if available
    const config = ideClient.config
    const ideName =
      config.type === 'sse-ide' || config.type === 'ws-ide'
        ? config.ideName
        : null
    if (ideClient.type === 'connected') {
      return { status: 'connected', ideName }
    }
    if (ideClient.type === 'pending') {
      return { status: 'pending', ideName }
    }
    return { status: 'disconnected', ideName }
  }, [mcpClients])
}

```

---


### `src/hooks/useIdeLogging.ts`

**信息:**
- 行数: 41
- 大小: 1201 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect } from 'react'
import { logEvent } from 'src/services/analytics/index.js'
import { z } from 'zod/v4'
import type { MCPServerConnection } from '../services/mcp/types.js'
import { getConnectedIdeClient } from '../utils/ide.js'
import { lazySchema } from '../utils/lazySchema.js'

const LogEventSchema = lazySchema(() =>
  z.object({
    method: z.literal('log_event'),
    params: z.object({
      eventName: z.string(),
      eventData: z.object({}).passthrough(),
    }),
  }),
)

export function useIdeLogging(mcpClients: MCPServerConnection[]): void {
  useEffect(() => {
    // Skip if there are no clients
    if (!mcpClients.length) {
      return
    }

    // Find the IDE client from the MCP clients list
    const ideClient = getConnectedIdeClient(mcpClients)
    if (ideClient) {
      // Register the log event handler
      ideClient.client.setNotificationHandler(
        LogEventSchema(),
        notification => {
          const { eventName, eventData } = notification.params
          logEvent(
            `tengu_ide_${eventName}`,
            eventData as { [key: string]: boolean | number | undefined },
          )
        },
      )
    }
  }, [mcpClients])
}

```

---


### `src/hooks/useIdeSelection.ts`

**信息:**
- 行数: 150
- 大小: 4349 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef } from 'react'
import { logError } from 'src/utils/log.js'
import { z } from 'zod/v4'
import type {
  ConnectedMCPServer,
  MCPServerConnection,
} from '../services/mcp/types.js'
import { getConnectedIdeClient } from '../utils/ide.js'
import { lazySchema } from '../utils/lazySchema.js'
export type SelectionPoint = {
  line: number
  character: number
}

export type SelectionData = {
  selection: {
    start: SelectionPoint
    end: SelectionPoint
  } | null
  text?: string
  filePath?: string
}

export type IDESelection = {
  lineCount: number
  lineStart?: number
  text?: string
  filePath?: string
}

// Define the selection changed notification schema
const SelectionChangedSchema = lazySchema(() =>
  z.object({
    method: z.literal('selection_changed'),
    params: z.object({
      selection: z
        .object({
          start: z.object({
            line: z.number(),
            character: z.number(),
          }),
          end: z.object({
            line: z.number(),
            character: z.number(),
          }),
        })
        .nullable()
        .optional(),
      text: z.string().optional(),
      filePath: z.string().optional(),

```

---


### `src/hooks/useInboxPoller.ts`

**信息:**
- 行数: 969
- 大小: 34375 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { randomUUID } from 'crypto'
import { useCallback, useEffect, useRef } from 'react'
import { useInterval } from 'usehooks-ts'
import type { ToolUseConfirm } from '../components/permissions/PermissionRequest.js'
import { TEAMMATE_MESSAGE_TAG } from '../constants/xml.js'
import { useTerminalNotification } from '../ink/useTerminalNotification.js'
import { sendNotification } from '../services/notifier.js'
import {
  type AppState,
  useAppState,
  useAppStateStore,
  useSetAppState,
} from '../state/AppState.js'
import { findToolByName } from '../Tool.js'
import { isInProcessTeammateTask } from '../tasks/InProcessTeammateTask/types.js'
import { getAllBaseTools } from '../tools.js'
import type { PermissionUpdate } from '../types/permissions.js'
import { logForDebugging } from '../utils/debug.js'
import {
  findInProcessTeammateTaskId,
  handlePlanApprovalResponse,
} from '../utils/inProcessTeammateHelpers.js'
import { createAssistantMessage } from '../utils/messages.js'
import {
  permissionModeFromString,
  toExternalPermissionMode,
} from '../utils/permissions/PermissionMode.js'
import { applyPermissionUpdate } from '../utils/permissions/PermissionUpdate.js'
import { jsonStringify } from '../utils/slowOperations.js'
import { isInsideTmux } from '../utils/swarm/backends/detection.js'
import {
  ensureBackendsRegistered,
  getBackendByType,
} from '../utils/swarm/backends/registry.js'
import type { PaneBackendType } from '../utils/swarm/backends/types.js'
import { TEAM_LEAD_NAME } from '../utils/swarm/constants.js'
import { getLeaderToolUseConfirmQueue } from '../utils/swarm/leaderPermissionBridge.js'
import { sendPermissionResponseViaMailbox } from '../utils/swarm/permissionSync.js'
import {
  removeTeammateFromTeamFile,
  setMemberMode,
} from '../utils/swarm/teamHelpers.js'
import { unassignTeammateTasks } from '../utils/tasks.js'
import {
  getAgentName,
  isPlanModeRequired,
  isTeamLead,
  isTeammate,
} from '../utils/teammate.js'
import { isInProcessTeammate } from '../utils/teammateContext.js'

```

---


### `src/hooks/useInputBuffer.ts`

**信息:**
- 行数: 132
- 大小: 3386 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useRef, useState } from 'react'
import type { PastedContent } from '../utils/config.js'

export type BufferEntry = {
  text: string
  cursorOffset: number
  pastedContents: Record<number, PastedContent>
  timestamp: number
}

export type UseInputBufferProps = {
  maxBufferSize: number
  debounceMs: number
}

export type UseInputBufferResult = {
  pushToBuffer: (
    text: string,
    cursorOffset: number,
    pastedContents?: Record<number, PastedContent>,
  ) => void
  undo: () => BufferEntry | undefined
  canUndo: boolean
  clearBuffer: () => void
}

export function useInputBuffer({
  maxBufferSize,
  debounceMs,
}: UseInputBufferProps): UseInputBufferResult {
  const [buffer, setBuffer] = useState<BufferEntry[]>([])
  const [currentIndex, setCurrentIndex] = useState(-1)
  const lastPushTime = useRef<number>(0)
  const pendingPush = useRef<ReturnType<typeof setTimeout> | null>(null)

  const pushToBuffer = useCallback(
    (
      text: string,
      cursorOffset: number,
      pastedContents: Record<number, PastedContent> = {},
    ) => {
      const now = Date.now()

      // Clear any pending push
      if (pendingPush.current) {
        clearTimeout(pendingPush.current)
        pendingPush.current = null
      }

      // Debounce rapid changes

```

---


### `src/hooks/useIssueFlagBanner.ts`

**信息:**
- 行数: 133
- 大小: 3828 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useMemo, useRef } from 'react'
import { BASH_TOOL_NAME } from '../tools/BashTool/toolName.js'
import type { Message } from '../types/message.js'
import { getUserMessageText } from '../utils/messages.js'

const EXTERNAL_COMMAND_PATTERNS = [
  /\bcurl\b/,
  /\bwget\b/,
  /\bssh\b/,
  /\bkubectl\b/,
  /\bsrun\b/,
  /\bdocker\b/,
  /\bbq\b/,
  /\bgsutil\b/,
  /\bgcloud\b/,
  /\baws\b/,
  /\bgit\s+push\b/,
  /\bgit\s+pull\b/,
  /\bgit\s+fetch\b/,
  /\bgh\s+(pr|issue)\b/,
  /\bnc\b/,
  /\bncat\b/,
  /\btelnet\b/,
  /\bftp\b/,
]

const FRICTION_PATTERNS = [
  // "No," or "No!" at start — comma/exclamation implies correction tone
  // (avoids "No problem", "No thanks", "No I think we should...")
  /^no[,!]\s/i,
  // Direct corrections about Claude's output
  /\bthat'?s (wrong|incorrect|not (what|right|correct))\b/i,
  /\bnot what I (asked|wanted|meant|said)\b/i,
  // Referencing prior instructions Claude missed
  /\bI (said|asked|wanted|told you|already said)\b/i,
  // Questioning Claude's actions
  /\bwhy did you\b/i,
  /\byou should(n'?t| not)? have\b/i,
  /\byou were supposed to\b/i,
  // Explicit retry/revert of Claude's work
  /\btry again\b/i,
  /\b(undo|revert) (that|this|it|what you)\b/i,
]

export function isSessionContainerCompatible(messages: Message[]): boolean {
  for (const msg of messages) {
    if (msg.type !== 'assistant') {
      continue
    }
    const content = msg.message.content

```

---


### `src/hooks/useLogMessages.ts`

**信息:**
- 行数: 119
- 大小: 5710 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { UUID } from 'crypto'
import { useEffect, useRef } from 'react'
import { useAppState } from '../state/AppState.js'
import type { Message } from '../types/message.js'
import { isAgentSwarmsEnabled } from '../utils/agentSwarmsEnabled.js'
import {
  cleanMessagesForLogging,
  isChainParticipant,
  recordTranscript,
} from '../utils/sessionStorage.js'

/**
 * Hook that logs messages to the transcript
 * conversation ID that only changes when a new conversation is started.
 *
 * @param messages The current conversation messages
 * @param ignore When true, messages will not be recorded to the transcript
 */
export function useLogMessages(messages: Message[], ignore: boolean = false) {
  const teamContext = useAppState(s => s.teamContext)

  // messages is append-only between compactions, so track where we left off
  // and only pass the new tail to recordTranscript. Avoids O(n) filter+scan
  // on every setMessages (~20x/turn, so n=3000 was ~120k wasted iterations).
  const lastRecordedLengthRef = useRef(0)
  const lastParentUuidRef = useRef<UUID | undefined>(undefined)
  // First-uuid change = compaction or /clear rebuilt the array; length alone
  // can't detect this since post-compact [CB,summary,...keep,new] may be longer.
  const firstMessageUuidRef = useRef<UUID | undefined>(undefined)
  // Guard against stale async .then() overwriting a fresher sync update when
  // an incremental render fires before the compaction .then() resolves.
  const callSeqRef = useRef(0)

  useEffect(() => {
    if (ignore) return

    const currentFirstUuid = messages[0]?.uuid as UUID | undefined
    const prevLength = lastRecordedLengthRef.current

    // First-render: firstMessageUuidRef is undefined. Compaction: first uuid changes.
    // Both are !isIncremental, but first-render sync-walk is safe (no messagesToKeep).
    const wasFirstRender = firstMessageUuidRef.current === undefined
    const isIncremental =
      currentFirstUuid !== undefined &&
      !wasFirstRender &&
      currentFirstUuid === firstMessageUuidRef.current &&
      prevLength <= messages.length
    // Same-head shrink: tombstone filter, rewind, snip, partial-compact.
    // Distinguished from compaction (first uuid changes) because the tail
    // is either an existing on-disk message or a fresh message that this

```

---


### `src/hooks/useLspPluginRecommendation.tsx`

**信息:**
- 行数: 194
- 大小: 21588 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * Hook for LSP plugin recommendations
 *
 * Detects file edits and recommends LSP plugins when:
 * - File extension matches an LSP plugin
 * - LSP binary is already installed on the system
 * - Plugin is not already installed
 * - User hasn't disabled recommendations
 *
 * Only shows one recommendation per session.
 */

import { extname, join } from 'path';
import * as React from 'react';
import { hasShownLspRecommendationThisSession, setLspRecommendationShownThisSession } from '../bootstrap/state.js';
import { useNotifications } from '../context/notifications.js';
import { useAppState } from '../state/AppState.js';
import { saveGlobalConfig } from '../utils/config.js';
import { logForDebugging } from '../utils/debug.js';
import { logError } from '../utils/log.js';
import { addToNeverSuggest, getMatchingLspPlugins, incrementIgnoredCount } from '../utils/plugins/lspRecommendation.js';
import { cacheAndRegisterPlugin } from '../utils/plugins/pluginInstallationHelpers.js';
import { getSettingsForSource, updateSettingsForSource } from '../utils/settings/settings.js';
import { installPluginAndNotify, usePluginRecommendationBase } from './usePluginRecommendationBase.js';

// Threshold for detecting timeout vs explicit dismiss (ms)
// Menu auto-dismisses at 30s, so anything over 28s is likely timeout
const TIMEOUT_THRESHOLD_MS = 28_000;
export type LspRecommendationState = {
  pluginId: string;
  pluginName: string;
  pluginDescription?: string;
  fileExtension: string;
  shownAt: number; // Timestamp for timeout detection
} | null;
type UseLspPluginRecommendationResult = {
  recommendation: LspRecommendationState;
  handleResponse: (response: 'yes' | 'no' | 'never' | 'disable') => void;
};
export function useLspPluginRecommendation() {
  const $ = _c(12);
  const trackedFiles = useAppState(_temp);
  const {
    addNotification
  } = useNotifications();
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = new Set();
    $[0] = t0;

```

---


### `src/hooks/useMailboxBridge.ts`

**信息:**
- 行数: 21
- 大小: 716 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useEffect, useMemo, useSyncExternalStore } from 'react'
import { useMailbox } from '../context/mailbox.js'

type Props = {
  isLoading: boolean
  onSubmitMessage: (content: string) => boolean
}

export function useMailboxBridge({ isLoading, onSubmitMessage }: Props): void {
  const mailbox = useMailbox()

  const subscribe = useMemo(() => mailbox.subscribe.bind(mailbox), [mailbox])
  const getSnapshot = useCallback(() => mailbox.revision, [mailbox])
  const revision = useSyncExternalStore(subscribe, getSnapshot)

  useEffect(() => {
    if (isLoading) return
    const msg = mailbox.poll()
    if (msg) onSubmitMessage(msg.content)
  }, [isLoading, revision, mailbox, onSubmitMessage])
}

```

---


### `src/hooks/useMainLoopModel.ts`

**信息:**
- 行数: 34
- 大小: 1509 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useReducer } from 'react'
import { onGrowthBookRefresh } from '../services/analytics/growthbook.js'
import { useAppState } from '../state/AppState.js'
import {
  getDefaultMainLoopModelSetting,
  type ModelName,
  parseUserSpecifiedModel,
} from '../utils/model/model.js'

// The value of the selector is a full model name that can be used directly in
// API calls. Use this over getMainLoopModel() when the component needs to
// update upon a model config change.
export function useMainLoopModel(): ModelName {
  const mainLoopModel = useAppState(s => s.mainLoopModel)
  const mainLoopModelForSession = useAppState(s => s.mainLoopModelForSession)

  // parseUserSpecifiedModel reads tengu_ant_model_override via
  // _CACHED_MAY_BE_STALE (in resolveAntModel). Until GB init completes,
  // that's the stale disk cache; after, it's the in-memory remoteEval map.
  // AppState doesn't change when GB init finishes, so we subscribe to the
  // refresh signal and force a re-render to re-resolve with fresh values.
  // Without this, the alias resolution is frozen until something else
  // happens to re-render the component — the API would sample one model
  // while /model (which also re-resolves) displays another.
  const [, forceRerender] = useReducer(x => x + 1, 0)
  useEffect(() => onGrowthBookRefresh(forceRerender), [])

  const model = parseUserSpecifiedModel(
    mainLoopModelForSession ??
      mainLoopModel ??
      getDefaultMainLoopModelSetting(),
  )
  return model
}

```

---


### `src/hooks/useManagePlugins.ts`

**信息:**
- 行数: 304
- 大小: 11888 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useEffect } from 'react'
import type { Command } from '../commands.js'
import { useNotifications } from '../context/notifications.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import { reinitializeLspServerManager } from '../services/lsp/manager.js'
import { useAppState, useSetAppState } from '../state/AppState.js'
import type { AgentDefinition } from '../tools/AgentTool/loadAgentsDir.js'
import { count } from '../utils/array.js'
import { logForDebugging } from '../utils/debug.js'
import { logForDiagnosticsNoPII } from '../utils/diagLogs.js'
import { toError } from '../utils/errors.js'
import { logError } from '../utils/log.js'
import { loadPluginAgents } from '../utils/plugins/loadPluginAgents.js'
import { getPluginCommands } from '../utils/plugins/loadPluginCommands.js'
import { loadPluginHooks } from '../utils/plugins/loadPluginHooks.js'
import { loadPluginLspServers } from '../utils/plugins/lspPluginIntegration.js'
import { loadPluginMcpServers } from '../utils/plugins/mcpPluginIntegration.js'
import { detectAndUninstallDelistedPlugins } from '../utils/plugins/pluginBlocklist.js'
import { getFlaggedPlugins } from '../utils/plugins/pluginFlagging.js'
import { loadAllPlugins } from '../utils/plugins/pluginLoader.js'

/**
 * Hook to manage plugin state and synchronize with AppState.
 *
 * On mount: loads all plugins, runs delisting enforcement, surfaces flagged-
 * plugin notifications, populates AppState.plugins. This is the initial
 * Layer-3 load — subsequent refresh goes through /reload-plugins.
 *
 * On needsRefresh: shows a notification directing the user to /reload-plugins.
 * Does NOT auto-refresh. All Layer-3 swap (commands, agents, hooks, MCP)
 * goes through refreshActivePlugins() via /reload-plugins for one consistent
 * mental model. See Outline: declarative-settings-hXHBMDIf4b PR 5c.
 */
export function useManagePlugins({
  enabled = true,
}: {
  enabled?: boolean
} = {}) {
  const setAppState = useSetAppState()
  const needsRefresh = useAppState(s => s.plugins.needsRefresh)
  const { addNotification } = useNotifications()

  // Initial plugin load. Runs once on mount. NOT used for refresh — all
  // post-mount refresh goes through /reload-plugins → refreshActivePlugins().
  // Unlike refreshActivePlugins, this also runs delisting enforcement and
  // flagged-plugin notifications (session-start concerns), and does NOT bump
  // mcp.pluginReconnectKey (MCP effects fire on their own mount).

```

---


### `src/hooks/useMemoryUsage.ts`

**信息:**
- 行数: 39
- 大小: 1293 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useState } from 'react'
import { useInterval } from 'usehooks-ts'

export type MemoryUsageStatus = 'normal' | 'high' | 'critical'

export type MemoryUsageInfo = {
  heapUsed: number
  status: MemoryUsageStatus
}

const HIGH_MEMORY_THRESHOLD = 1.5 * 1024 * 1024 * 1024 // 1.5GB in bytes
const CRITICAL_MEMORY_THRESHOLD = 2.5 * 1024 * 1024 * 1024 // 2.5GB in bytes

/**
 * Hook to monitor Node.js process memory usage.
 * Polls every 10 seconds; returns null while status is 'normal'.
 */
export function useMemoryUsage(): MemoryUsageInfo | null {
  const [memoryUsage, setMemoryUsage] = useState<MemoryUsageInfo | null>(null)

  useInterval(() => {
    const heapUsed = process.memoryUsage().heapUsed
    const status: MemoryUsageStatus =
      heapUsed >= CRITICAL_MEMORY_THRESHOLD
        ? 'critical'
        : heapUsed >= HIGH_MEMORY_THRESHOLD
          ? 'high'
          : 'normal'
    setMemoryUsage(prev => {
      // Bail when status is 'normal' — nothing is shown, so heapUsed is
      // irrelevant and we avoid re-rendering the whole Notifications subtree
      // every 10 seconds for the 99%+ of users who never reach 1.5GB.
      if (status === 'normal') return prev === null ? prev : null
      return { heapUsed, status }
    })
  }, 10_000)

  return memoryUsage
}

```

---


### `src/hooks/useMergedClients.ts`

**信息:**
- 行数: 23
- 大小: 745 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import uniqBy from 'lodash-es/uniqBy.js'
import { useMemo } from 'react'
import type { MCPServerConnection } from '../services/mcp/types.js'

export function mergeClients(
  initialClients: MCPServerConnection[] | undefined,
  mcpClients: readonly MCPServerConnection[] | undefined,
): MCPServerConnection[] {
  if (initialClients && mcpClients && mcpClients.length > 0) {
    return uniqBy([...initialClients, ...mcpClients], 'name')
  }
  return initialClients || []
}

export function useMergedClients(
  initialClients: MCPServerConnection[] | undefined,
  mcpClients: MCPServerConnection[] | undefined,
): MCPServerConnection[] {
  return useMemo(
    () => mergeClients(initialClients, mcpClients),
    [initialClients, mcpClients],
  )
}

```

---


### `src/hooks/useMergedCommands.ts`

**信息:**
- 行数: 15
- 大小: 423 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import uniqBy from 'lodash-es/uniqBy.js'
import { useMemo } from 'react'
import type { Command } from '../commands.js'

export function useMergedCommands(
  initialCommands: Command[],
  mcpCommands: Command[],
): Command[] {
  return useMemo(() => {
    if (mcpCommands.length > 0) {
      return uniqBy([...initialCommands, ...mcpCommands], 'name')
    }
    return initialCommands
  }, [initialCommands, mcpCommands])
}

```

---


### `src/hooks/useMergedTools.ts`

**信息:**
- 行数: 44
- 大小: 1645 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
import { useMemo } from 'react'
import type { Tools, ToolPermissionContext } from '../Tool.js'
import { assembleToolPool } from '../tools.js'
import { useAppState } from '../state/AppState.js'
import { mergeAndFilterTools } from '../utils/toolPool.js'

/**
 * React hook that assembles the full tool pool for the REPL.
 *
 * Uses assembleToolPool() (the shared pure function used by both REPL and runAgent)
 * to combine built-in tools with MCP tools, applying deny rules and deduplication.
 * Any extra initialTools are merged on top.
 *
 * @param initialTools - Extra tools to include (built-in + startup MCP from props).
 *   These are merged with the assembled pool and take precedence in deduplication.
 * @param mcpTools - MCP tools discovered dynamically (from mcp state)
 * @param toolPermissionContext - Permission context for filtering
 */
export function useMergedTools(
  initialTools: Tools,
  mcpTools: Tools,
  toolPermissionContext: ToolPermissionContext,
): Tools {
  let replBridgeEnabled = false
  let replBridgeOutboundOnly = false
  return useMemo(() => {
    // assembleToolPool is the shared function that both REPL and runAgent use.
    // It handles: getTools() + MCP deny-rule filtering + dedup + MCP CLI exclusion.
    const assembled = assembleToolPool(toolPermissionContext, mcpTools)

    return mergeAndFilterTools(
      initialTools,
      assembled,
      toolPermissionContext.mode,
    )
  }, [
    initialTools,
    mcpTools,
    toolPermissionContext,
    replBridgeEnabled,
    replBridgeOutboundOnly,
  ])
}

```

---


### `src/hooks/useMinDisplayTime.ts`

**信息:**
- 行数: 35
- 大小: 1010 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef, useState } from 'react'

/**
 * Throttles a value so each distinct value stays visible for at least `minMs`.
 * Prevents fast-cycling progress text from flickering past before it's readable.
 *
 * Unlike debounce (wait for quiet) or throttle (limit rate), this guarantees
 * each value gets its minimum screen time before being replaced.
 */
export function useMinDisplayTime<T>(value: T, minMs: number): T {
  const [displayed, setDisplayed] = useState(value)
  const lastShownAtRef = useRef(0)

  useEffect(() => {
    const elapsed = Date.now() - lastShownAtRef.current
    if (elapsed >= minMs) {
      lastShownAtRef.current = Date.now()
      setDisplayed(value)
      return
    }
    const timer = setTimeout(
      (shownAtRef, setFn, v) => {
        shownAtRef.current = Date.now()
        setFn(v)
      },
      minMs - elapsed,
      lastShownAtRef,
      setDisplayed,
      value,
    )
    return () => clearTimeout(timer)
  }, [value, minMs])

  return displayed
}

```

---


### `src/hooks/useNotifyAfterTimeout.ts`

**信息:**
- 行数: 65
- 大小: 2471 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect } from 'react'
import {
  getLastInteractionTime,
  updateLastInteractionTime,
} from '../bootstrap/state.js'
import { useTerminalNotification } from '../ink/useTerminalNotification.js'
import { sendNotification } from '../services/notifier.js'
// The time threshold in milliseconds for considering an interaction "recent" (6 seconds)
export const DEFAULT_INTERACTION_THRESHOLD_MS = 6000

function getTimeSinceLastInteraction(): number {
  return Date.now() - getLastInteractionTime()
}

function hasRecentInteraction(threshold: number): boolean {
  return getTimeSinceLastInteraction() < threshold
}

function shouldNotify(threshold: number): boolean {
  return process.env.NODE_ENV !== 'test' && !hasRecentInteraction(threshold)
}

// NOTE: User interaction tracking is now done in App.tsx's processKeysInBatch
// function, which calls updateLastInteractionTime() when any input is received.
// This avoids having a separate stdin 'data' listener that would compete with
// the main 'readable' listener and cause dropped input characters.

/**
 * Hook that manages desktop notifications after a timeout period.
 *
 * Shows a notification in two cases:
 * 1. Immediately if the app has been idle for longer than the threshold
 * 2. After the specified timeout if the user doesn't interact within that time
 *
 * @param message - The notification message to display
 * @param timeout - The timeout in milliseconds (defaults to 6000ms)
 */
export function useNotifyAfterTimeout(
  message: string,
  notificationType: string,
): void {
  const terminal = useTerminalNotification()

  // Reset interaction time when hook is called to make sure that requests
  // that took a long time to complete don't pop up a notification right away.
  // Must be immediate because useEffect runs after Ink's render cycle has
  // already flushed; without it the timestamp stays stale and a premature
  // notification fires if the user is idle (no subsequent renders to flush).
  useEffect(() => {
    updateLastInteractionTime(true)

```

---


### `src/hooks/useOfficialMarketplaceNotification.tsx`

**信息:**
- 行数: 48
- 大小: 7299 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import type { Notification } from '../context/notifications.js';
import { Text } from '../ink.js';
import { logForDebugging } from '../utils/debug.js';
import { checkAndInstallOfficialMarketplace } from '../utils/plugins/officialMarketplaceStartupCheck.js';
import { useStartupNotification } from './notifs/useStartupNotification.js';

/**
 * Hook that handles official marketplace auto-installation and shows
 * notifications for success/failure in the bottom right of the REPL.
 */
export function useOfficialMarketplaceNotification() {
  useStartupNotification(_temp);
}
async function _temp() {
  const result = await checkAndInstallOfficialMarketplace();
  const notifs = [];
  if (result.configSaveFailed) {
    logForDebugging("Showing marketplace config save failure notification");
    notifs.push({
      key: "marketplace-config-save-failed",
      jsx: <Text color="error">Failed to save marketplace retry info · Check ~/.claude.json permissions</Text>,
      priority: "immediate",
      timeoutMs: 10000
    });
  }
  if (result.installed) {
    logForDebugging("Showing marketplace installation success notification");
    notifs.push({
      key: "marketplace-installed",
      jsx: <Text color="success">✓ Anthropic marketplace installed · /plugin to see available plugins</Text>,
      priority: "immediate",
      timeoutMs: 7000
    });
  } else {
    if (result.skipped && result.reason === "unknown") {
      logForDebugging("Showing marketplace installation failure notification");
      notifs.push({
        key: "marketplace-install-failed",
        jsx: <Text color="warning">Failed to install Anthropic marketplace · Will retry on next startup</Text>,
        priority: "immediate",
        timeoutMs: 8000
      });
    }
  }
  return notifs;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIk5vdGlmaWNhdGlvbiIsIlRleHQiLCJsb2dGb3JEZWJ1Z2dpbmciLCJjaGVja0FuZEluc3RhbGxPZmZpY2lhbE1hcmtldHBsYWNlIiwidXNlU3RhcnR1cE5vdGlmaWNhdGlvbiIsInVzZU9mZmljaWFsTWFya2V0cGxhY2VOb3RpZmljYXRpb24iLCJfdGVtcCIsInJlc3VsdCIsIm5vdGlmcyIsImNvbmZpZ1NhdmVGYWlsZWQiLCJwdXNoIiwia2V5IiwianN4IiwicHJpb3JpdHkiLCJ0aW1lb3V0TXMiLCJpbnN0YWxsZWQiLCJza2lwcGVkIiwicmVhc29uIl0sInNvdXJjZXMiOlsidXNlT2ZmaWNpYWxNYXJrZXRwbGFjZU5vdGlmaWNhdGlvbi50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgdHlwZSB7IE5vdGlmaWNhdGlvbiB9IGZyb20gJy4uL2NvbnRleHQvbm90aWZpY2F0aW9ucy5qcydcbmltcG9ydCB7IFRleHQgfSBmcm9tICcuLi9pbmsuanMnXG5pbXBvcnQgeyBsb2dGb3JEZWJ1Z2dpbmcgfSBmcm9tICcuLi91dGlscy9kZWJ1Zy5qcydcbmltcG9ydCB7IGNoZWNrQW5kSW5zdGFsbE9mZmljaWFsTWFya2V0cGxhY2UgfSBmcm9tICcuLi91dGlscy9wbHVnaW5zL29mZmljaWFsTWFya2V0cGxhY2VTdGFydHVwQ2hlY2suanMnXG5pbXBvcnQgeyB1c2VTdGFydHVwTm90aWZpY2F0aW9uIH0gZnJvbSAnLi9ub3RpZnMvdXNlU3RhcnR1cE5vdGlmaWNhdGlvbi5qcydcblxuLyoqXG4gKiBIb29rIHRoYXQgaGFuZGxlcyBvZmZpY2lhbCBtYXJrZXRwbGFjZSBhdXRvLWluc3RhbGxhdGlvbiBhbmQgc2hvd3NcbiAqIG5vdGlmaWNhdGlvbnMgZm9yIHN1Y2Nlc3MvZmFpbHVyZSBpbiB0aGUgYm90dG9tIHJpZ2h0IG9mIHRoZSBSRVBMLlxuICovXG5leHBvcnQgZnVuY3Rpb24gdXNlT2ZmaWNpYWxNYXJrZXRwbGFjZU5vdGlmaWNhdGlvbigpOiB2b2lkIHtcbiAgdXNlU3RhcnR1cE5vdGlmaWNhdGlvbihhc3luYyAoKSA9PiB7XG4gICAgY29uc3QgcmVzdWx0ID0gYXdhaXQgY2hlY2tBbmRJbnN0YWxsT2ZmaWNpYWxNYXJrZXRwbGFjZSgpXG4gICAgY29uc3Qgbm90aWZzOiBOb3RpZmljYXRpb25bXSA9IFtdXG5cbiAgICAvLyBDaGVjayBmb3IgY29uZmlnIHNhdmUgZmFpbHVyZSBmaXJzdCAtIHRoaXMgaXMgY3JpdGljYWxcbiAgICBpZiAocmVzdWx0LmNvbmZpZ1NhdmVGYWlsZWQpIHtcbiAgICAgIGxvZ0ZvckRlYnVnZ2luZygnU2hvd2luZyBtYXJrZXRwbGFjZSBjb25maWcgc2F2ZSBmYWlsdXJlIG5vdGlmaWNhdGlvbicpXG4gICAgICBub3RpZnMucHVzaCh7XG4gICAgICAgIGtleTogJ21hcmtldHBsYWNlLWNvbmZpZy1zYXZlLWZhaWxlZCcsXG4gICAgICAgIGpzeDogKFxuICAgICAgICAgIDxUZXh0IGNvbG9yPVwiZXJyb3JcIj5cbiAgICAgICAgICAgIEZhaWxlZCB0byBzYXZlIG1hcmtldHBsYWNlIHJldHJ5IGluZm8gwrcgQ2hlY2sgfi8uY2xhdWRlLmpzb25cbiAgICAgICAgICAgIHBlcm1pc3Npb25zXG4gICAgICAgICAgPC9UZXh0PlxuICAgICAgICApLFxuICAgICAgICBwcmlvcml0eTogJ2ltbWVkaWF0ZScsXG4gICAgICAgIHRpbWVvdXRNczogMTAwMDAsXG4gICAgICB9KVxuICAgIH1cblxuICAgIGlmIChyZXN1bHQuaW5zdGFsbGVkKSB7XG4gICAgICBsb2dGb3JEZWJ1Z2dpbmcoJ1Nob3dpbmcgbWFya2V0cGxhY2UgaW5zdGFsbGF0aW9uIHN1Y2Nlc3Mgbm90aWZpY2F0aW9uJylcbiAgICAgIG5vdGlmcy5wdXNoKHtcbiAgICAgICAga2V5OiAnbWFya2V0cGxhY2UtaW5zdGFsbGVkJyxcbiAgICAgICAganN4OiAoXG4gICAgICAgICAgPFRleHQgY29sb3I9XCJzdWNjZXNzXCI+XG4gICAgICAgICAgICDinJMgQW50aHJvcGljIG1hcmtldHBsYWNlIGluc3RhbGxlZCDCtyAvcGx1Z2luIHRvIHNlZSBhdmFpbGFibGUgcGx1Z2luc1xuICAgICAgICAgIDwvVGV4dD5cbiAgICAgICAgKSxcbiAgICAgICAgcHJpb3JpdHk6ICdpbW1lZGlhdGUnLFxuICAgICAgICB0aW1lb3V0TXM6IDcwMDAsXG4gICAgICB9KVxuICAgIH0gZWxzZSBpZiAocmVzdWx0LnNraXBwZWQgJiYgcmVzdWx0LnJlYXNvbiA9PT0gJ3Vua25vd24nKSB7XG4gICAgICBsb2dGb3JEZWJ1Z2dpbmcoJ1Nob3dpbmcgbWFya2V0cGxhY2UgaW5zdGFsbGF0aW9uIGZhaWx1cmUgbm90aWZpY2F0aW9uJylcbiAgICAgIG5vdGlmcy5wdXNoKHtcbiAgICAgICAga2V5OiAnbWFya2V0cGxhY2UtaW5zdGFsbC1mYWlsZWQnLFxuICAgICAgICBqc3g6IChcbiAgICAgICAgICA8VGV4dCBjb2xvcj1cIndhcm5pbmdcIj5cbiAgICAgICAgICAgIEZhaWxlZCB0byBpbnN0YWxsIEFudGhyb3BpYyBtYXJrZXRwbGFjZSDCtyBXaWxsIHJldHJ5IG9uIG5leHQgc3RhcnR1cFxuICAgICAgICAgIDwvVGV4dD5cbiAgICAgICAgKSxcbiAgICAgICAgcHJpb3JpdHk6ICdpbW1lZGlhdGUnLFxuICAgICAgICB0aW1lb3V0TXM6IDgwMDAsXG4gICAgICB9KVxuICAgIH1cbiAgICAvLyBEb24ndCBzaG93IG5vdGlmaWNhdGlvbnMgZm9yOlxuICAgIC8vIC0gYWxyZWFkeV9pbnN0YWxsZWQgKHVzZXIgYWxyZWFkeSBoYXMgaXQpXG4gICAgLy8gLSBwb2xpY3lfYmxvY2tlZCAoZW50ZXJwcmlzZSBwb2xpY3ksIGRvbid0IG5hZylcbiAgICAvLyAtIGFscmVhZHlfYXR0ZW1wdGVkIChoYW5kbGVkIGJ5IHJldHJ5IGxvZ2ljIG5vdylcbiAgICAvLyAtIGdpdF91bmF2YWlsYWJsZSAobWFya2V0cGxhY2UgaXMgYSBuaWNlLXRvLWhhdmU7IGlmIGdpdCBpcyBtaXNzaW5nXG4gICAgLy8gICBvciBpcyBhIG5vbi1mdW5jdGlvbmFsIG1hY09TIHhjcnVuIHNoaW0sIHJldHJ5IHNpbGVudGx5IG9uIGJhY2tvZmZcbiAgICAvLyAgIHJhdGhlciB0aGFuIG5hZ2dpbmcg4oCUIHRoZSB1c2VyIHdpbGwgc29ydCBnaXQgb3V0IGZvciBvdGhlciByZWFzb25zKVxuICAgIHJldHVybiBub3RpZnNcbiAgfSlcbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixjQUFjQyxZQUFZLFFBQVEsNkJBQTZCO0FBQy9ELFNBQVNDLElBQUksUUFBUSxXQUFXO0FBQ2hDLFNBQVNDLGVBQWUsUUFBUSxtQkFBbUI7QUFDbkQsU0FBU0Msa0NBQWtDLFFBQVEscURBQXFEO0FBQ3hHLFNBQVNDLHNCQUFzQixRQUFRLG9DQUFvQzs7QUFFM0U7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPLFNBQUFDLG1DQUFBO0VBQ0xELHNCQUFzQixDQUFDRSxLQXFEdEIsQ0FBQztBQUFBO0FBdERHLGVBQUFBLE1BQUE7RUFFSCxNQUFBQyxNQUFBLEdBQWUsTUFBTUosa0NBQWtDLENBQUMsQ0FBQztFQUN6RCxNQUFBSyxNQUFBLEdBQStCLEVBQUU7RUFHakMsSUFBSUQsTUFBTSxDQUFBRSxnQkFBaUI7SUFDekJQLGVBQWUsQ0FBQyxzREFBc0QsQ0FBQztJQUN2RU0sTUFBTSxDQUFBRSxJQUFLLENBQUM7TUFBQUMsR0FBQSxFQUNMLGdDQUFnQztNQUFBQyxHQUFBLEVBRW5DLENBQUMsSUFBSSxDQUFPLEtBQU8sQ0FBUCxPQUFPLENBQUMsd0VBR3BCLEVBSEMsSUFBSSxDQUdFO01BQUFDLFFBQUEsRUFFQyxXQUFXO01BQUFDLFNBQUEsRUFDVjtJQUNiLENBQUMsQ0FBQztFQUFBO0VBR0osSUFBSVAsTUFBTSxDQUFBUSxTQUFVO0lBQ2xCYixlQUFlLENBQUMsdURBQXVELENBQUM7SUFDeEVNLE1BQU0sQ0FBQUUsSUFBSyxDQUFDO01BQUFDLEdBQUEsRUFDTCx1QkFBdUI7TUFBQUMsR0FBQSxFQUUxQixDQUFDLElBQUksQ0FBTyxLQUFTLENBQVQsU0FBUyxDQUFDLG9FQUV0QixFQUZDLElBQUksQ0FFRTtNQUFBQyxRQUFBLEVBRUMsV0FBVztNQUFBQyxTQUFBLEVBQ1Y7SUFDYixDQUFDLENBQUM7RUFBQTtJQUNHLElBQUlQLE1BQU0sQ0FBQVMsT0FBdUMsSUFBM0JULE1BQU0sQ0FBQVUsTUFBTyxLQUFLLFNBQVM7TUFDdERmLGVBQWUsQ0FBQyx1REFBdUQsQ0FBQztNQUN4RU0sTUFBTSxDQUFBRSxJQUFLLENBQUM7UUFBQUMsR0FBQSxFQUNMLDRCQUE0QjtRQUFBQyxHQUFBLEVBRS9CLENBQUMsSUFBSSxDQUFPLEtBQVMsQ0FBVCxTQUFTLENBQUMsb0VBRXRCLEVBRkMsSUFBSSxDQUVFO1FBQUFDLFFBQUEsRUFFQyxXQUFXO1FBQUFDLFNBQUEsRUFDVjtNQUNiLENBQUMsQ0FBQztJQUFBO0VBQ0g7RUFBQSxPQVFNTixNQUFNO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/hooks/usePasteHandler.ts`

**信息:**
- 行数: 285
- 大小: 10146 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { basename } from 'path'
import React from 'react'
import { logError } from 'src/utils/log.js'
import { useDebounceCallback } from 'usehooks-ts'
import type { InputEvent, Key } from '../ink.js'
import {
  getImageFromClipboard,
  isImageFilePath,
  PASTE_THRESHOLD,
  tryReadImageFromPath,
} from '../utils/imagePaste.js'
import type { ImageDimensions } from '../utils/imageResizer.js'
import { getPlatform } from '../utils/platform.js'

const CLIPBOARD_CHECK_DEBOUNCE_MS = 50
const PASTE_COMPLETION_TIMEOUT_MS = 100

type PasteHandlerProps = {
  onPaste?: (text: string) => void
  onInput: (input: string, key: Key) => void
  onImagePaste?: (
    base64Image: string,
    mediaType?: string,
    filename?: string,
    dimensions?: ImageDimensions,
    sourcePath?: string,
  ) => void
}

export function usePasteHandler({
  onPaste,
  onInput,
  onImagePaste,
}: PasteHandlerProps): {
  wrappedOnInput: (input: string, key: Key, event: InputEvent) => void
  pasteState: {
    chunks: string[]
    timeoutId: ReturnType<typeof setTimeout> | null
  }
  isPasting: boolean
} {
  const [pasteState, setPasteState] = React.useState<{
    chunks: string[]
    timeoutId: ReturnType<typeof setTimeout> | null
  }>({ chunks: [], timeoutId: null })
  const [isPasting, setIsPasting] = React.useState(false)
  const isMountedRef = React.useRef(true)
  // Mirrors pasteState.timeoutId but updated synchronously. When paste + a
  // keystroke arrive in the same stdin chunk, both wrappedOnInput calls run
  // in the same discreteUpdates batch before React commits — the second call

```

---


### `src/hooks/usePluginRecommendationBase.tsx`

**信息:**
- 行数: 105
- 大小: 11418 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * Shared state machine + install helper for plugin-recommendation hooks
 * (LSP, claude-code-hint). Centralizes the gate chain, async-guard,
 * and success/failure notification JSX so new sources stay small.
 */

import figures from 'figures';
import * as React from 'react';
import { getIsRemoteMode } from '../bootstrap/state.js';
import type { useNotifications } from '../context/notifications.js';
import { Text } from '../ink.js';
import { logError } from '../utils/log.js';
import { getPluginById } from '../utils/plugins/marketplaceManager.js';
type AddNotification = ReturnType<typeof useNotifications>['addNotification'];
type PluginData = NonNullable<Awaited<ReturnType<typeof getPluginById>>>;

/**
 * Call tryResolve inside a useEffect; it applies standard gates (remote
 * mode, already-showing, in-flight) then runs resolve(). Non-null return
 * becomes the recommendation. Include tryResolve in effect deps — its
 * identity tracks recommendation, so clearing re-triggers resolution.
 */
export function usePluginRecommendationBase() {
  const $ = _c(6);
  const [recommendation, setRecommendation] = React.useState(null);
  const isCheckingRef = React.useRef(false);
  let t0;
  if ($[0] !== recommendation) {
    t0 = resolve => {
      if (getIsRemoteMode()) {
        return;
      }
      if (recommendation) {
        return;
      }
      if (isCheckingRef.current) {
        return;
      }
      isCheckingRef.current = true;
      resolve().then(rec => {
        if (rec) {
          setRecommendation(rec);
        }
      }).catch(logError).finally(() => {
        isCheckingRef.current = false;
      });
    };
    $[0] = recommendation;
    $[1] = t0;

```

---


### `src/hooks/usePrStatus.ts`

**信息:**
- 行数: 106
- 大小: 3202 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef, useState } from 'react'
import { getLastInteractionTime } from '../bootstrap/state.js'
import { fetchPrStatus, type PrReviewState } from '../utils/ghPrStatus.js'

const POLL_INTERVAL_MS = 60_000
const SLOW_GH_THRESHOLD_MS = 4_000
const IDLE_STOP_MS = 60 * 60_000 // stop polling after 60 min idle

export type PrStatusState = {
  number: number | null
  url: string | null
  reviewState: PrReviewState | null
  lastUpdated: number
}

const INITIAL_STATE: PrStatusState = {
  number: null,
  url: null,
  reviewState: null,
  lastUpdated: 0,
}

/**
 * Polls PR review status every 60s while the session is active.
 * When no interaction is detected for 60 minutes, the loop stops — no
 * timers remain. React re-runs the effect when isLoading changes
 * (turn starts/ends), restarting the loop. Effect setup schedules
 * the next poll relative to the last fetch time so turn boundaries
 * don't spawn `gh` more than once per interval. Disables permanently
 * if a fetch exceeds 4s.
 *
 * Pass `enabled: false` to skip polling entirely (hook still must be
 * called unconditionally to satisfy the rules of hooks).
 */
export function usePrStatus(isLoading: boolean, enabled = true): PrStatusState {
  const [prStatus, setPrStatus] = useState<PrStatusState>(INITIAL_STATE)
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const disabledRef = useRef(false)
  const lastFetchRef = useRef(0)

  useEffect(() => {
    if (!enabled) return
    if (disabledRef.current) return

    let cancelled = false
    let lastSeenInteractionTime = -1
    let lastActivityTimestamp = Date.now()

    async function poll() {
      if (cancelled) return

```

---


### `src/hooks/usePromptSuggestion.ts`

**信息:**
- 行数: 177
- 大小: 5315 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useRef } from 'react'
import { useTerminalFocus } from '../ink/hooks/use-terminal-focus.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import { abortSpeculation } from '../services/PromptSuggestion/speculation.js'
import { useAppState, useSetAppState } from '../state/AppState.js'

type Props = {
  inputValue: string
  isAssistantResponding: boolean
}

export function usePromptSuggestion({
  inputValue,
  isAssistantResponding,
}: Props): {
  suggestion: string | null
  markAccepted: () => void
  markShown: () => void
  logOutcomeAtSubmission: (
    finalInput: string,
    opts?: { skipReset: boolean },
  ) => void
} {
  const promptSuggestion = useAppState(s => s.promptSuggestion)
  const setAppState = useSetAppState()
  const isTerminalFocused = useTerminalFocus()
  const {
    text: suggestionText,
    promptId,
    shownAt,
    acceptedAt,
    generationRequestId,
  } = promptSuggestion

  const suggestion =
    isAssistantResponding || inputValue.length > 0 ? null : suggestionText

  const isValidSuggestion = suggestionText && shownAt > 0

  // Track engagement depth for telemetry
  const firstKeystrokeAt = useRef<number>(0)
  const wasFocusedWhenShown = useRef<boolean>(true)
  const prevShownAt = useRef<number>(0)

  // Capture focus state when a new suggestion appears (shownAt changes)
  if (shownAt > 0 && shownAt !== prevShownAt.current) {
    prevShownAt.current = shownAt

```

---


### `src/hooks/usePromptsFromClaudeInChrome.tsx`

**信息:**
- 行数: 71
- 大小: 11623 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/messages.mjs';
import { useEffect, useRef } from 'react';
import { logError } from 'src/utils/log.js';
import { z } from 'zod/v4';
import { callIdeRpc } from '../services/mcp/client.js';
import type { ConnectedMCPServer, MCPServerConnection } from '../services/mcp/types.js';
import type { PermissionMode } from '../types/permissions.js';
import { CLAUDE_IN_CHROME_MCP_SERVER_NAME, isTrackedClaudeInChromeTabId } from '../utils/claudeInChrome/common.js';
import { lazySchema } from '../utils/lazySchema.js';
import { enqueuePendingNotification } from '../utils/messageQueueManager.js';

// Schema for the prompt notification from Chrome extension (JSON-RPC 2.0 format)
const ClaudeInChromePromptNotificationSchema = lazySchema(() => z.object({
  method: z.literal('notifications/message'),
  params: z.object({
    prompt: z.string(),
    image: z.object({
      type: z.literal('base64'),
      media_type: z.enum(['image/jpeg', 'image/png', 'image/gif', 'image/webp']),
      data: z.string()
    }).optional(),
    tabId: z.number().optional()
  })
}));

/**
 * A hook that listens for prompt notifications from the Claude for Chrome extension,
 * enqueues them as user prompts, and syncs permission mode changes to the extension.
 */
export function usePromptsFromClaudeInChrome(mcpClients, toolPermissionMode) {
  const $ = _c(6);
  useRef(undefined);
  let t0;
  if ($[0] !== mcpClients) {
    t0 = [mcpClients];
    $[0] = mcpClients;
    $[1] = t0;
  } else {
    t0 = $[1];
  }
  useEffect(_temp, t0);
  let t1;
  let t2;
  if ($[2] !== mcpClients || $[3] !== toolPermissionMode) {
    t1 = () => {
      const chromeClient = findChromeClient(mcpClients);
      if (!chromeClient) {
        return;
      }

```

---


### `src/hooks/useQueueProcessor.ts`

**信息:**
- 行数: 68
- 大小: 2547 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useSyncExternalStore } from 'react'
import type { QueuedCommand } from '../types/textInputTypes.js'
import {
  getCommandQueueSnapshot,
  subscribeToCommandQueue,
} from '../utils/messageQueueManager.js'
import type { QueryGuard } from '../utils/QueryGuard.js'
import { processQueueIfReady } from '../utils/queueProcessor.js'

type UseQueueProcessorParams = {
  executeQueuedInput: (commands: QueuedCommand[]) => Promise<void>
  hasActiveLocalJsxUI: boolean
  queryGuard: QueryGuard
}

/**
 * Hook that processes queued commands when conditions are met.
 *
 * Uses a single unified command queue (module-level store). Priority determines
 * processing order: 'now' > 'next' (user input) > 'later' (task notifications).
 * The dequeue() function handles priority ordering automatically.
 *
 * Processing triggers when:
 * - No query active (queryGuard — reactive via useSyncExternalStore)
 * - Queue has items
 * - No active local JSX UI blocking input
 */
export function useQueueProcessor({
  executeQueuedInput,
  hasActiveLocalJsxUI,
  queryGuard,
}: UseQueueProcessorParams): void {
  // Subscribe to the query guard. Re-renders when a query starts or ends
  // (or when reserve/cancelReservation transitions dispatching state).
  const isQueryActive = useSyncExternalStore(
    queryGuard.subscribe,
    queryGuard.getSnapshot,
  )

  // Subscribe to the unified command queue via useSyncExternalStore.
  // This guarantees re-render when the store changes, bypassing
  // React context propagation delays that cause missed notifications in Ink.
  const queueSnapshot = useSyncExternalStore(
    subscribeToCommandQueue,
    getCommandQueueSnapshot,
  )

  useEffect(() => {
    if (isQueryActive) return
    if (hasActiveLocalJsxUI) return

```

---


### `src/hooks/useRemoteSession.ts`

**信息:**
- 行数: 605
- 大小: 23010 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useEffect, useMemo, useRef } from 'react'
import { BoundedUUIDSet } from '../bridge/bridgeMessaging.js'
import type { ToolUseConfirm } from '../components/permissions/PermissionRequest.js'
import type { SpinnerMode } from '../components/Spinner/types.js'
import {
  type RemotePermissionResponse,
  type RemoteSessionConfig,
  RemoteSessionManager,
} from '../remote/RemoteSessionManager.js'
import {
  createSyntheticAssistantMessage,
  createToolStub,
} from '../remote/remotePermissionBridge.js'
import {
  convertSDKMessage,
  isSessionEndMessage,
} from '../remote/sdkMessageAdapter.js'
import { useSetAppState } from '../state/AppState.js'
import type { AppState } from '../state/AppStateStore.js'
import type { Tool } from '../Tool.js'
import { findToolByName } from '../Tool.js'
import type { Message as MessageType } from '../types/message.js'
import type { PermissionAskDecision } from '../types/permissions.js'
import { logForDebugging } from '../utils/debug.js'
import { truncateToWidth } from '../utils/format.js'
import {
  createSystemMessage,
  extractTextContent,
  handleMessageFromStream,
  type StreamingToolUse,
} from '../utils/messages.js'
import { generateSessionTitle } from '../utils/sessionTitle.js'
import type { RemoteMessageContent } from '../utils/teleport/api.js'
import { updateSessionTitle } from '../utils/teleport/api.js'

// How long to wait for a response before showing a warning
const RESPONSE_TIMEOUT_MS = 60000 // 60 seconds
// Extended timeout during compaction — compact API calls take 5-30s and
// block other SDK messages, so the normal 60s timeout isn't enough when
// compaction itself runs close to the edge.
const COMPACTION_TIMEOUT_MS = 180000 // 3 minutes

type UseRemoteSessionProps = {
  config: RemoteSessionConfig | undefined
  setMessages: React.Dispatch<React.SetStateAction<MessageType[]>>
  setIsLoading: (loading: boolean) => void
  onInit?: (slashCommands: string[]) => void
  setToolUseConfirmQueue: React.Dispatch<React.SetStateAction<ToolUseConfirm[]>>
  tools: Tool[]
  setStreamingToolUses?: React.Dispatch<

```

---


### `src/hooks/useReplBridge.tsx`

**信息:**
- 行数: 723
- 大小: 115652 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import React, { useCallback, useEffect, useRef } from 'react';
import { setMainLoopModelOverride } from '../bootstrap/state.js';
import { type BridgePermissionCallbacks, type BridgePermissionResponse, isBridgePermissionResponse } from '../bridge/bridgePermissionCallbacks.js';
import { buildBridgeConnectUrl } from '../bridge/bridgeStatusUtil.js';
import { extractInboundMessageFields } from '../bridge/inboundMessages.js';
import type { BridgeState, ReplBridgeHandle } from '../bridge/replBridge.js';
import { setReplBridgeHandle } from '../bridge/replBridgeHandle.js';
import type { Command } from '../commands.js';
import { getSlashCommandToolSkills, isBridgeSafeCommand } from '../commands.js';
import { getRemoteSessionUrl } from '../constants/product.js';
import { useNotifications } from '../context/notifications.js';
import type { PermissionMode, SDKMessage } from '../entrypoints/agentSdkTypes.js';
import type { SDKControlResponse } from '../entrypoints/sdk/controlTypes.js';
import { Text } from '../ink.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js';
import { useAppState, useAppStateStore, useSetAppState } from '../state/AppState.js';
import type { Message } from '../types/message.js';
import { getCwd } from '../utils/cwd.js';
import { logForDebugging } from '../utils/debug.js';
import { errorMessage } from '../utils/errors.js';
import { enqueue } from '../utils/messageQueueManager.js';
import { buildSystemInitMessage } from '../utils/messages/systemInit.js';
import { createBridgeStatusMessage, createSystemMessage } from '../utils/messages.js';
import { getAutoModeUnavailableNotification, getAutoModeUnavailableReason, isAutoModeGateEnabled, isBypassPermissionsModeDisabled, transitionPermissionMode } from '../utils/permissions/permissionSetup.js';
import { getLeaderToolUseConfirmQueue } from '../utils/swarm/leaderPermissionBridge.js';

/** How long after a failure before replBridgeEnabled is auto-cleared (stops retries). */
export const BRIDGE_FAILURE_DISMISS_MS = 10_000;

/**
 * Max consecutive initReplBridge failures before the hook stops re-attempting
 * for the session lifetime. Guards against paths that flip replBridgeEnabled
 * back on after auto-disable (settings sync, /remote-control, config tool)
 * when the underlying OAuth is unrecoverable — each re-attempt is another
 * guaranteed 401 against POST /v1/environments/bridge. Datadog 2026-03-08:
 * top stuck client generated 2,879 × 401/day alone (17% of all 401s on the
 * route).
 */
const MAX_CONSECUTIVE_INIT_FAILURES = 3;

/**
 * Hook that initializes an always-on bridge connection in the background
 * and writes new user/assistant messages to the bridge session.
 *
 * Silently skips if bridge is not enabled or user is not OAuth-authenticated.
 *
 * Watches AppState.replBridgeEnabled — when toggled off (via /config or footer),
 * the bridge is torn down. When toggled back on, it re-initializes.
 *

```

---


### `src/hooks/useSSHSession.ts`

**信息:**
- 行数: 241
- 大小: 8316 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * REPL integration hook for `claude ssh` sessions.
 *
 * Sibling to useDirectConnect — same shape (isRemoteMode/sendMessage/
 * cancelRequest/disconnect), same REPL wiring, but drives an SSH child
 * process instead of a WebSocket. Kept separate rather than generalizing
 * useDirectConnect because the lifecycle differs: the ssh process and auth
 * proxy are created BEFORE this hook runs (during startup, in main.tsx) and
 * handed in; useDirectConnect creates its WebSocket inside the effect.
 */

import { randomUUID } from 'crypto'
import { useCallback, useEffect, useMemo, useRef } from 'react'
import type { ToolUseConfirm } from '../components/permissions/PermissionRequest.js'
import {
  createSyntheticAssistantMessage,
  createToolStub,
} from '../remote/remotePermissionBridge.js'
import {
  convertSDKMessage,
  isSessionEndMessage,
} from '../remote/sdkMessageAdapter.js'
import type { SSHSession } from '../ssh/createSSHSession.js'
import type { SSHSessionManager } from '../ssh/SSHSessionManager.js'
import type { Tool } from '../Tool.js'
import { findToolByName } from '../Tool.js'
import type { Message as MessageType } from '../types/message.js'
import type { PermissionAskDecision } from '../types/permissions.js'
import { logForDebugging } from '../utils/debug.js'
import { gracefulShutdown } from '../utils/gracefulShutdown.js'
import type { RemoteMessageContent } from '../utils/teleport/api.js'

type UseSSHSessionResult = {
  isRemoteMode: boolean
  sendMessage: (content: RemoteMessageContent) => Promise<boolean>
  cancelRequest: () => void
  disconnect: () => void
}

type UseSSHSessionProps = {
  session: SSHSession | undefined
  setMessages: React.Dispatch<React.SetStateAction<MessageType[]>>
  setIsLoading: (loading: boolean) => void
  setToolUseConfirmQueue: React.Dispatch<React.SetStateAction<ToolUseConfirm[]>>
  tools: Tool[]
}

export function useSSHSession({
  session,
  setMessages,

```

---


### `src/hooks/useScheduledTasks.ts`

**信息:**
- 行数: 139
- 大小: 5975 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef } from 'react'
import { useAppStateStore, useSetAppState } from '../state/AppState.js'
import { isTerminalTaskStatus } from '../Task.js'
import {
  findTeammateTaskByAgentId,
  injectUserMessageToTeammate,
} from '../tasks/InProcessTeammateTask/InProcessTeammateTask.js'
import { isKairosCronEnabled } from '../tools/ScheduleCronTool/prompt.js'
import type { Message } from '../types/message.js'
import { getCronJitterConfig } from '../utils/cronJitterConfig.js'
import { createCronScheduler } from '../utils/cronScheduler.js'
import { removeCronTasks } from '../utils/cronTasks.js'
import { logForDebugging } from '../utils/debug.js'
import { enqueuePendingNotification } from '../utils/messageQueueManager.js'
import { createScheduledTaskFireMessage } from '../utils/messages.js'
import { WORKLOAD_CRON } from '../utils/workloadContext.js'

type Props = {
  isLoading: boolean
  /**
   * When true, bypasses the isLoading gate so tasks can enqueue while a
   * query is streaming rather than deferring to the next 1s check tick
   * after the turn ends. Assistant mode no longer forces --proactive
   * (#20425) so isLoading drops between turns like a normal REPL — this
   * bypass is now a latency nicety, not a starvation fix. The prompt is
   * enqueued at 'later' priority either way and drains between turns.
   */
  assistantMode?: boolean
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>
}

/**
 * REPL wrapper for the cron scheduler. Mounts the scheduler once and tears
 * it down on unmount. Fired prompts go into the command queue as 'later'
 * priority, which the REPL drains via useCommandQueue between turns.
 *
 * Scheduler core (timer, file watcher, fire logic) lives in cronScheduler.ts
 * so SDK/-p mode can share it — see print.ts for the headless wiring.
 */
export function useScheduledTasks({
  isLoading,
  assistantMode = false,
  setMessages,
}: Props): void {
  // Latest-value ref so the scheduler's isLoading() getter doesn't capture
  // a stale closure. The effect mounts once; isLoading changes every turn.
  const isLoadingRef = useRef(isLoading)
  isLoadingRef.current = isLoading

  const store = useAppStateStore()

```

---


### `src/hooks/useSearchInput.ts`

**信息:**
- 行数: 364
- 大小: 10327 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useState } from 'react'
import { KeyboardEvent } from '../ink/events/keyboard-event.js'
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- backward-compat bridge until consumers wire handleKeyDown to <Box onKeyDown>
import { useInput } from '../ink.js'
import {
  Cursor,
  getLastKill,
  pushToKillRing,
  recordYank,
  resetKillAccumulation,
  resetYankState,
  updateYankLength,
  yankPop,
} from '../utils/Cursor.js'
import { useTerminalSize } from './useTerminalSize.js'

type UseSearchInputOptions = {
  isActive: boolean
  onExit: () => void
  /** Esc + Ctrl+C abandon (distinct from onExit = Enter commit). When
   *  provided: single-Esc calls this directly (no clear-first-then-exit
   *  two-press). When absent: current behavior — Esc clears non-empty
   *  query, exits on empty; Ctrl+C silently swallowed (no switch case). */
  onCancel?: () => void
  onExitUp?: () => void
  columns?: number
  passthroughCtrlKeys?: string[]
  initialQuery?: string
  /** Backspace (and ctrl+h) on empty query calls onCancel ?? onExit — the
   *  less/vim "delete past the /" convention. Dialogs that want Esc-only
   *  cancel set this false so a held backspace doesn't eject the user. */
  backspaceExitsOnEmpty?: boolean
}

type UseSearchInputReturn = {
  query: string
  setQuery: (q: string) => void
  cursorOffset: number
  handleKeyDown: (e: KeyboardEvent) => void
}

function isKillKey(e: KeyboardEvent): boolean {
  if (e.ctrl && (e.key === 'k' || e.key === 'u' || e.key === 'w')) {
    return true
  }
  if (e.meta && e.key === 'backspace') {
    return true
  }
  return false
}

```

---


### `src/hooks/useSessionBackgrounding.ts`

**信息:**
- 行数: 158
- 大小: 4944 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Hook for managing session backgrounding (Ctrl+B to background/foreground sessions).
 *
 * Handles:
 * - Calling onBackgroundQuery to spawn a background task for the current query
 * - Re-backgrounding foregrounded tasks
 * - Syncing foregrounded task messages/state to main view
 */

import { useCallback, useEffect, useRef } from 'react'
import { useAppState, useSetAppState } from '../state/AppState.js'
import type { Message } from '../types/message.js'

type UseSessionBackgroundingProps = {
  setMessages: (messages: Message[] | ((prev: Message[]) => Message[])) => void
  setIsLoading: (loading: boolean) => void
  resetLoadingState: () => void
  setAbortController: (controller: AbortController | null) => void
  onBackgroundQuery: () => void
}

type UseSessionBackgroundingResult = {
  /** Call when user wants to background (Ctrl+B) */
  handleBackgroundSession: () => void
}

export function useSessionBackgrounding({
  setMessages,
  setIsLoading,
  resetLoadingState,
  setAbortController,
  onBackgroundQuery,
}: UseSessionBackgroundingProps): UseSessionBackgroundingResult {
  const foregroundedTaskId = useAppState(s => s.foregroundedTaskId)
  const foregroundedTask = useAppState(s =>
    s.foregroundedTaskId ? s.tasks[s.foregroundedTaskId] : undefined,
  )
  const setAppState = useSetAppState()
  const lastSyncedMessagesLengthRef = useRef<number>(0)

  const handleBackgroundSession = useCallback(() => {
    if (foregroundedTaskId) {
      // Re-background the foregrounded task
      setAppState(prev => {
        const taskId = prev.foregroundedTaskId
        if (!taskId) return prev
        const task = prev.tasks[taskId]
        if (!task) {
          return { ...prev, foregroundedTaskId: undefined }
        }

```

---


### `src/hooks/useSettings.ts`

**信息:**
- 行数: 17
- 大小: 618 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { type AppState, useAppState } from '../state/AppState.js'

/**
 * Settings type as stored in AppState (DeepImmutable wrapped).
 * Use this type when you need to annotate variables that hold settings from useSettings().
 */
export type ReadonlySettings = AppState['settings']

/**
 * React hook to access current settings from AppState.
 * Settings automatically update when files change on disk via settingsChangeDetector.
 *
 * Use this instead of getSettings_DEPRECATED() in React components for reactive updates.
 */
export function useSettings(): ReadonlySettings {
  return useAppState(s => s.settings)
}

```

---


### `src/hooks/useSettingsChange.ts`

**信息:**
- 行数: 25
- 大小: 946 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useEffect } from 'react'
import { settingsChangeDetector } from '../utils/settings/changeDetector.js'
import type { SettingSource } from '../utils/settings/constants.js'
import { getSettings_DEPRECATED } from '../utils/settings/settings.js'
import type { SettingsJson } from '../utils/settings/types.js'

export function useSettingsChange(
  onChange: (source: SettingSource, settings: SettingsJson) => void,
): void {
  const handleChange = useCallback(
    (source: SettingSource) => {
      // Cache is already reset by the notifier (changeDetector.fanOut) —
      // resetting here caused N-way thrashing with N subscribers: each
      // cleared the cache, re-read from disk, then the next cleared again.
      const newSettings = getSettings_DEPRECATED()
      onChange(source, newSettings)
    },
    [onChange],
  )

  useEffect(
    () => settingsChangeDetector.subscribe(handleChange),
    [handleChange],
  )
}

```

---


### `src/hooks/useSkillImprovementSurvey.ts`

**信息:**
- 行数: 105
- 大小: 3528 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useRef, useState } from 'react'
import type { FeedbackSurveyResponse } from '../components/FeedbackSurvey/utils.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_PII_TAGGED,
  logEvent,
} from '../services/analytics/index.js'
import { useAppState, useSetAppState } from '../state/AppState.js'
import type { Message } from '../types/message.js'
import type { SkillUpdate } from '../utils/hooks/skillImprovement.js'
import { applySkillImprovement } from '../utils/hooks/skillImprovement.js'
import { createSystemMessage } from '../utils/messages.js'

type SkillImprovementSuggestion = {
  skillName: string
  updates: SkillUpdate[]
}

type SetMessages = (fn: (prev: Message[]) => Message[]) => void

export function useSkillImprovementSurvey(setMessages: SetMessages): {
  isOpen: boolean
  suggestion: SkillImprovementSuggestion | null
  handleSelect: (selected: FeedbackSurveyResponse) => void
} {
  const suggestion = useAppState(s => s.skillImprovement.suggestion)
  const setAppState = useSetAppState()
  const [isOpen, setIsOpen] = useState(false)
  const lastSuggestionRef = useRef(suggestion)
  const loggedAppearanceRef = useRef(false)

  // Track the suggestion for display even after clearing AppState
  if (suggestion) {
    lastSuggestionRef.current = suggestion
  }

  // Open when a new suggestion arrives
  if (suggestion && !isOpen) {
    setIsOpen(true)
    if (!loggedAppearanceRef.current) {
      loggedAppearanceRef.current = true
      logEvent('tengu_skill_improvement_survey', {
        event_type:
          'appeared' as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
        // _PROTO_skill_name routes to the privileged skill_name BQ column.
        // Unredacted names don't go in additional_metadata.
        _PROTO_skill_name: (suggestion.skillName ??
          'unknown') as AnalyticsMetadata_I_VERIFIED_THIS_IS_PII_TAGGED,
      })
    }

```

---


### `src/hooks/useSkillsChange.ts`

**信息:**
- 行数: 62
- 大小: 2084 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useEffect } from 'react'
import type { Command } from '../commands.js'
import {
  clearCommandMemoizationCaches,
  clearCommandsCache,
  getCommands,
} from '../commands.js'
import { onGrowthBookRefresh } from '../services/analytics/growthbook.js'
import { logError } from '../utils/log.js'
import { skillChangeDetector } from '../utils/skills/skillChangeDetector.js'

/**
 * Keep the commands list fresh across two triggers:
 *
 * 1. Skill file changes (watcher) — full cache clear + disk re-scan, since
 *    skill content changed on disk.
 * 2. GrowthBook init/refresh — memo-only clear, since only `isEnabled()`
 *    predicates may have changed. Handles commands like /btw whose gate
 *    reads a flag that isn't in the disk cache yet on first session after
 *    a flag rename: getCommands() runs before GB init (main.tsx:2855 vs
 *    showSetupScreens at :3106), so the memoized list is baked with the
 *    default. Once init populates remoteEvalFeatureValues, re-filter.
 */
export function useSkillsChange(
  cwd: string | undefined,
  onCommandsChange: (commands: Command[]) => void,
): void {
  const handleChange = useCallback(async () => {
    if (!cwd) return
    try {
      // Clear all command caches to ensure fresh load
      clearCommandsCache()
      const commands = await getCommands(cwd)
      onCommandsChange(commands)
    } catch (error) {
      // Errors during reload are non-fatal - log and continue
      if (error instanceof Error) {
        logError(error)
      }
    }
  }, [cwd, onCommandsChange])

  useEffect(() => skillChangeDetector.subscribe(handleChange), [handleChange])

  const handleGrowthBookRefresh = useCallback(async () => {
    if (!cwd) return
    try {
      clearCommandMemoizationCaches()
      const commands = await getCommands(cwd)
      onCommandsChange(commands)

```

---


### `src/hooks/useSwarmInitialization.ts`

**信息:**
- 行数: 81
- 大小: 3151 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Swarm Initialization Hook
 *
 * Initializes swarm features: teammate hooks and context.
 * Handles both fresh spawns and resumed teammate sessions.
 *
 * This hook is conditionally loaded to allow dead code elimination when swarms are disabled.
 */

import { useEffect } from 'react'
import { getSessionId } from '../bootstrap/state.js'
import type { AppState } from '../state/AppState.js'
import type { Message } from '../types/message.js'
import { isAgentSwarmsEnabled } from '../utils/agentSwarmsEnabled.js'
import { initializeTeammateContextFromSession } from '../utils/swarm/reconnection.js'
import { readTeamFile } from '../utils/swarm/teamHelpers.js'
import { initializeTeammateHooks } from '../utils/swarm/teammateInit.js'
import { getDynamicTeamContext } from '../utils/teammate.js'

type SetAppState = (f: (prevState: AppState) => AppState) => void

/**
 * Hook that initializes swarm features when ENABLE_AGENT_SWARMS is true.
 *
 * Handles both:
 * - Resumed teammate sessions (from --resume or /resume) where teamName/agentName
 *   are stored in transcript messages
 * - Fresh spawns where context is read from environment variables
 */
export function useSwarmInitialization(
  setAppState: SetAppState,
  initialMessages: Message[] | undefined,
  { enabled = true }: { enabled?: boolean } = {},
): void {
  useEffect(() => {
    if (!enabled) return
    if (isAgentSwarmsEnabled()) {
      // Check if this is a resumed agent session (from --resume or /resume)
      // Resumed sessions have teamName/agentName stored in transcript messages
      const firstMessage = initialMessages?.[0]
      const teamName =
        firstMessage && 'teamName' in firstMessage
          ? (firstMessage.teamName as string | undefined)
          : undefined
      const agentName =
        firstMessage && 'agentName' in firstMessage
          ? (firstMessage.agentName as string | undefined)
          : undefined

      if (teamName && agentName) {

```

---


### `src/hooks/useSwarmPermissionPoller.ts`

**信息:**
- 行数: 330
- 大小: 9617 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Swarm Permission Poller Hook
 *
 * This hook polls for permission responses from the team leader when running
 * as a worker agent in a swarm. When a response is received, it calls the
 * appropriate callback (onAllow/onReject) to continue execution.
 *
 * This hook should be used in conjunction with the worker-side integration
 * in useCanUseTool.ts, which creates pending requests that this hook monitors.
 */

import { useCallback, useEffect, useRef } from 'react'
import { useInterval } from 'usehooks-ts'
import { logForDebugging } from '../utils/debug.js'
import { errorMessage } from '../utils/errors.js'
import {
  type PermissionUpdate,
  permissionUpdateSchema,
} from '../utils/permissions/PermissionUpdateSchema.js'
import {
  isSwarmWorker,
  type PermissionResponse,
  pollForResponse,
  removeWorkerResponse,
} from '../utils/swarm/permissionSync.js'
import { getAgentName, getTeamName } from '../utils/teammate.js'

const POLL_INTERVAL_MS = 500

/**
 * Validate permissionUpdates from external sources (mailbox IPC, disk polling).
 * Malformed entries from buggy/old teammate processes are filtered out rather
 * than propagated unchecked into callback.onAllow().
 */
function parsePermissionUpdates(raw: unknown): PermissionUpdate[] {
  if (!Array.isArray(raw)) {
    return []
  }
  const schema = permissionUpdateSchema()
  const valid: PermissionUpdate[] = []
  for (const entry of raw) {
    const result = schema.safeParse(entry)
    if (result.success) {
      valid.push(result.data)
    } else {
      logForDebugging(
        `[SwarmPermissionPoller] Dropping malformed permissionUpdate entry: ${result.error.message}`,
        { level: 'warn' },
      )
    }

```

---


### `src/hooks/useTaskListWatcher.ts`

**信息:**
- 行数: 221
- 大小: 6822 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { type FSWatcher, watch } from 'fs'
import { useEffect, useRef } from 'react'
import { logForDebugging } from '../utils/debug.js'
import {
  claimTask,
  DEFAULT_TASKS_MODE_TASK_LIST_ID,
  ensureTasksDir,
  getTasksDir,
  listTasks,
  type Task,
  updateTask,
} from '../utils/tasks.js'

const DEBOUNCE_MS = 1000

type Props = {
  /** When undefined, the hook does nothing. The task list id is also used as the agent ID. */
  taskListId?: string
  isLoading: boolean
  /**
   * Called when a task is ready to be worked on.
   * Returns true if submission succeeded, false if rejected.
   */
  onSubmitTask: (prompt: string) => boolean
}

/**
 * Hook that watches a task list directory and automatically picks up
 * open, unowned tasks to work on.
 *
 * This enables "tasks mode" where Claude watches for externally-created
 * tasks and processes them one at a time.
 */
export function useTaskListWatcher({
  taskListId,
  isLoading,
  onSubmitTask,
}: Props): void {
  const currentTaskRef = useRef<string | null>(null)
  const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  // Stabilize unstable props via refs so the watcher effect doesn't depend on
  // them. isLoading flips every turn, and onSubmitTask's identity changes
  // whenever onQuery's deps change. Without this, the watcher effect re-runs
  // on every turn, calling watcher.close() + watch() each time — which is a
  // trigger for Bun's PathWatcherManager deadlock (oven-sh/bun#27469).
  const isLoadingRef = useRef(isLoading)
  isLoadingRef.current = isLoading
  const onSubmitTaskRef = useRef(onSubmitTask)
  onSubmitTaskRef.current = onSubmitTask

```

---


### `src/hooks/useTasksV2.ts`

**信息:**
- 行数: 250
- 大小: 8808 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { type FSWatcher, watch } from 'fs'
import { useEffect, useSyncExternalStore } from 'react'
import { useAppState, useSetAppState } from '../state/AppState.js'
import { createSignal } from '../utils/signal.js'
import type { Task } from '../utils/tasks.js'
import {
  getTaskListId,
  getTasksDir,
  isTodoV2Enabled,
  listTasks,
  onTasksUpdated,
  resetTaskList,
} from '../utils/tasks.js'
import { isTeamLead } from '../utils/teammate.js'

const HIDE_DELAY_MS = 5000
const DEBOUNCE_MS = 50
const FALLBACK_POLL_MS = 5000 // Fallback in case fs.watch misses events

/**
 * Singleton store for the TodoV2 task list. Owns the file watcher, timers,
 * and cached task list. Multiple hook instances (REPL, Spinner,
 * PromptInputFooterLeftSide) subscribe to one shared store instead of each
 * setting up their own fs.watch on the same directory. The Spinner mounts/
 * unmounts every turn — per-hook watchers caused constant watch/unwatch churn.
 *
 * Implements the useSyncExternalStore contract: subscribe/getSnapshot.
 */
class TasksV2Store {
  /** Stable array reference; replaced only on fetch. undefined until started. */
  #tasks: Task[] | undefined = undefined
  /**
   * Set when the hide timer has elapsed (all tasks completed for >5s), or
   * when the task list is empty. Starts false so the first fetch runs the
   * "all completed → schedule 5s hide" path (matches original behavior:
   * resuming a session with completed tasks shows them briefly).
   */
  #hidden = false
  #watcher: FSWatcher | null = null
  #watchedDir: string | null = null
  #hideTimer: ReturnType<typeof setTimeout> | null = null
  #debounceTimer: ReturnType<typeof setTimeout> | null = null
  #pollTimer: ReturnType<typeof setTimeout> | null = null
  #unsubscribeTasksUpdated: (() => void) | null = null
  #changed = createSignal()
  #subscriberCount = 0
  #started = false

  /**
   * useSyncExternalStore snapshot. Returns the same Task[] reference between

```

---


### `src/hooks/useTeammateViewAutoExit.ts`

**信息:**
- 行数: 63
- 大小: 2189 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect } from 'react'
import { useAppState, useSetAppState } from '../state/AppState.js'
import { exitTeammateView } from '../state/teammateViewHelpers.js'
import { isInProcessTeammateTask } from '../tasks/InProcessTeammateTask/types.js'

/**
 * Auto-exits teammate viewing mode when the viewed teammate
 * is killed or encounters an error. Users stay viewing completed
 * teammates so they can review the full transcript.
 */
export function useTeammateViewAutoExit(): void {
  const setAppState = useSetAppState()
  const viewingAgentTaskId = useAppState(s => s.viewingAgentTaskId)
  // Select only the viewed task, not the full tasks map — otherwise every
  // streaming update from any teammate re-renders this hook.
  const task = useAppState(s =>
    s.viewingAgentTaskId ? s.tasks[s.viewingAgentTaskId] : undefined,
  )

  const viewedTask = task && isInProcessTeammateTask(task) ? task : undefined
  const viewedStatus = viewedTask?.status
  const viewedError = viewedTask?.error
  const taskExists = task !== undefined

  useEffect(() => {
    // Not viewing any teammate
    if (!viewingAgentTaskId) {
      return
    }

    // Task no longer exists in the map — evicted out from under us.
    // Check raw `task` not teammate-narrowed `viewedTask`; local_agent
    // tasks exist but narrow to undefined, which would eject immediately.
    if (!taskExists) {
      exitTeammateView(setAppState)
      return
    }
    // Status checks below are teammate-only (viewedTask is teammate-narrowed).
    // For local_agent, viewedStatus is undefined → all checks falsy → no eject.
    if (!viewedTask) return

    // Auto-exit if teammate is killed, stopped, has error, or is no longer running
    // This handles shutdown scenarios where teammate becomes inactive
    if (
      viewedStatus === 'killed' ||
      viewedStatus === 'failed' ||
      viewedError ||
      (viewedStatus !== 'running' &&
        viewedStatus !== 'completed' &&
        viewedStatus !== 'pending')

```

---


### `src/hooks/useTeleportResume.tsx`

**信息:**
- 行数: 85
- 大小: 9840 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { useCallback, useState } from 'react';
import { setTeleportedSessionInfo } from 'src/bootstrap/state.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import type { TeleportRemoteResponse } from 'src/utils/conversationRecovery.js';
import type { CodeSession } from 'src/utils/teleport/api.js';
import { errorMessage, TeleportOperationError } from '../utils/errors.js';
import { teleportResumeCodeSession } from '../utils/teleport.js';
export type TeleportResumeError = {
  message: string;
  formattedMessage?: string;
  isOperationError: boolean;
};
export type TeleportSource = 'cliArg' | 'localCommand';
export function useTeleportResume(source) {
  const $ = _c(8);
  const [isResuming, setIsResuming] = useState(false);
  const [error, setError] = useState(null);
  const [selectedSession, setSelectedSession] = useState(null);
  let t0;
  if ($[0] !== source) {
    t0 = async session => {
      setIsResuming(true);
      setError(null);
      setSelectedSession(session);
      logEvent("tengu_teleport_resume_session", {
        source: source as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
        session_id: session.id as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS
      });
      ;
      try {
        const result = await teleportResumeCodeSession(session.id);
        setTeleportedSessionInfo({
          sessionId: session.id
        });
        setIsResuming(false);
        return result;
      } catch (t1) {
        const err = t1;
        const teleportError = {
          message: err instanceof TeleportOperationError ? err.message : errorMessage(err),
          formattedMessage: err instanceof TeleportOperationError ? err.formattedMessage : undefined,
          isOperationError: err instanceof TeleportOperationError
        };
        setError(teleportError);
        setIsResuming(false);
        return null;
      }
    };
    $[0] = source;

```

---


### `src/hooks/useTerminalSize.ts`

**信息:**
- 行数: 15
- 大小: 354 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useContext } from 'react'
import {
  type TerminalSize,
  TerminalSizeContext,
} from 'src/ink/components/TerminalSizeContext.js'

export function useTerminalSize(): TerminalSize {
  const size = useContext(TerminalSizeContext)

  if (!size) {
    throw new Error('useTerminalSize must be used within an Ink App component')
  }

  return size
}

```

---


### `src/hooks/useTextInput.ts`

**信息:**
- 行数: 529
- 大小: 17027 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { isInputModeCharacter } from 'src/components/PromptInput/inputModes.js'
import { useNotifications } from 'src/context/notifications.js'
import stripAnsi from 'strip-ansi'
import { markBackslashReturnUsed } from '../commands/terminalSetup/terminalSetup.js'
import { addToHistory } from '../history.js'
import type { Key } from '../ink.js'
import type {
  InlineGhostText,
  TextInputState,
} from '../types/textInputTypes.js'
import {
  Cursor,
  getLastKill,
  pushToKillRing,
  recordYank,
  resetKillAccumulation,
  resetYankState,
  updateYankLength,
  yankPop,
} from '../utils/Cursor.js'
import { env } from '../utils/env.js'
import { isFullscreenEnvEnabled } from '../utils/fullscreen.js'
import type { ImageDimensions } from '../utils/imageResizer.js'
import { isModifierPressed, prewarmModifiers } from '../utils/modifiers.js'
import { useDoublePress } from './useDoublePress.js'

type MaybeCursor = void | Cursor
type InputHandler = (input: string) => MaybeCursor
type InputMapper = (input: string) => MaybeCursor
const NOOP_HANDLER: InputHandler = () => {}
function mapInput(input_map: Array<[string, InputHandler]>): InputMapper {
  const map = new Map(input_map)
  return function (input: string): MaybeCursor {
    return (map.get(input) ?? NOOP_HANDLER)(input)
  }
}

export type UseTextInputProps = {
  value: string
  onChange: (value: string) => void
  onSubmit?: (value: string) => void
  onExit?: () => void
  onExitMessage?: (show: boolean, key?: string) => void
  onHistoryUp?: () => void
  onHistoryDown?: () => void
  onHistoryReset?: () => void
  onClearInput?: () => void
  focus?: boolean
  mask?: string
  multiline?: boolean

```

---


### `src/hooks/useTimeout.ts`

**信息:**
- 行数: 14
- 大小: 362 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useState } from 'react'

export function useTimeout(delay: number, resetTrigger?: number): boolean {
  const [isElapsed, setIsElapsed] = useState(false)

  useEffect(() => {
    setIsElapsed(false)
    const timer = setTimeout(setIsElapsed, delay, true)

    return () => clearTimeout(timer)
  }, [delay, resetTrigger])

  return isElapsed
}

```

---


### `src/hooks/useTurnDiffs.ts`

**信息:**
- 行数: 213
- 大小: 6686 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { StructuredPatchHunk } from 'diff'
import { useMemo, useRef } from 'react'
import type { FileEditOutput } from '../tools/FileEditTool/types.js'
import type { Output as FileWriteOutput } from '../tools/FileWriteTool/FileWriteTool.js'
import type { Message } from '../types/message.js'

export type TurnFileDiff = {
  filePath: string
  hunks: StructuredPatchHunk[]
  isNewFile: boolean
  linesAdded: number
  linesRemoved: number
}

export type TurnDiff = {
  turnIndex: number
  userPromptPreview: string
  timestamp: string
  files: Map<string, TurnFileDiff>
  stats: {
    filesChanged: number
    linesAdded: number
    linesRemoved: number
  }
}

type FileEditResult = FileEditOutput | FileWriteOutput

type TurnDiffCache = {
  completedTurns: TurnDiff[]
  currentTurn: TurnDiff | null
  lastProcessedIndex: number
  lastTurnIndex: number
}

function isFileEditResult(result: unknown): result is FileEditResult {
  if (!result || typeof result !== 'object') return false
  const r = result as Record<string, unknown>
  // FileEditTool: has structuredPatch with content
  // FileWriteTool (update): has structuredPatch with content
  // FileWriteTool (create): has type='create' and content (structuredPatch is empty)
  const hasFilePath = typeof r.filePath === 'string'
  const hasStructuredPatch =
    Array.isArray(r.structuredPatch) && r.structuredPatch.length > 0
  const isNewFile = r.type === 'create' && typeof r.content === 'string'
  return hasFilePath && (hasStructuredPatch || isNewFile)
}

function isFileWriteOutput(result: FileEditResult): result is FileWriteOutput {
  return (

```

---


### `src/hooks/useTypeahead.tsx`

**信息:**
- 行数: 1385
- 大小: 212610 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useNotifications } from 'src/context/notifications.js';
import { Text } from 'src/ink.js';
import { logEvent } from 'src/services/analytics/index.js';
import { useDebounceCallback } from 'usehooks-ts';
import { type Command, getCommandName } from '../commands.js';
import { getModeFromInput, getValueFromInput } from '../components/PromptInput/inputModes.js';
import type { SuggestionItem, SuggestionType } from '../components/PromptInput/PromptInputFooterSuggestions.js';
import { useIsModalOverlayActive, useRegisterOverlay } from '../context/overlayContext.js';
import { KeyboardEvent } from '../ink/events/keyboard-event.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- backward-compat bridge until consumers wire handleKeyDown to <Box onKeyDown>
import { useInput } from '../ink.js';
import { useOptionalKeybindingContext, useRegisterKeybindingContext } from '../keybindings/KeybindingContext.js';
import { useKeybindings } from '../keybindings/useKeybinding.js';
import { useShortcutDisplay } from '../keybindings/useShortcutDisplay.js';
import { useAppState, useAppStateStore } from '../state/AppState.js';
import type { AgentDefinition } from '../tools/AgentTool/loadAgentsDir.js';
import type { InlineGhostText, PromptInputMode } from '../types/textInputTypes.js';
import { isAgentSwarmsEnabled } from '../utils/agentSwarmsEnabled.js';
import { generateProgressiveArgumentHint, parseArguments } from '../utils/argumentSubstitution.js';
import { getShellCompletions, type ShellCompletionType } from '../utils/bash/shellCompletion.js';
import { formatLogMetadata } from '../utils/format.js';
import { getSessionIdFromLog, searchSessionsByCustomTitle } from '../utils/sessionStorage.js';
import { applyCommandSuggestion, findMidInputSlashCommand, generateCommandSuggestions, getBestCommandMatch, isCommandInput } from '../utils/suggestions/commandSuggestions.js';
import { getDirectoryCompletions, getPathCompletions, isPathLikeToken } from '../utils/suggestions/directoryCompletion.js';
import { getShellHistoryCompletion } from '../utils/suggestions/shellHistoryCompletion.js';
import { getSlackChannelSuggestions, hasSlackMcpServer } from '../utils/suggestions/slackChannelSuggestions.js';
import { TEAM_LEAD_NAME } from '../utils/swarm/constants.js';
import { applyFileSuggestion, findLongestCommonPrefix, onIndexBuildComplete, startBackgroundCacheRefresh } from './fileSuggestions.js';
import { generateUnifiedSuggestions } from './unifiedSuggestions.js';

// Unicode-aware character class for file path tokens:
// \p{L} = letters (CJK, Latin, Cyrillic, etc.)
// \p{N} = numbers (incl. fullwidth)
// \p{M} = combining marks (macOS NFD accents, Devanagari vowel signs)
const AT_TOKEN_HEAD_RE = /^@[\p{L}\p{N}\p{M}_\-./\\()[\]~:]*/u;
const PATH_CHAR_HEAD_RE = /^[\p{L}\p{N}\p{M}_\-./\\()[\]~:]+/u;
const TOKEN_WITH_AT_RE = /(@[\p{L}\p{N}\p{M}_\-./\\()[\]~:]*|[\p{L}\p{N}\p{M}_\-./\\()[\]~:]+)$/u;
const TOKEN_WITHOUT_AT_RE = /[\p{L}\p{N}\p{M}_\-./\\()[\]~:]+$/u;
const HAS_AT_SYMBOL_RE = /(^|\s)@([\p{L}\p{N}\p{M}_\-./\\()[\]~:]*|"[^"]*"?)$/u;
const HASH_CHANNEL_RE = /(^|\s)#([a-z0-9][a-z0-9_-]*)$/;

// Type guard for path completion metadata
function isPathMetadata(metadata: unknown): metadata is {
  type: 'directory' | 'file';
} {
  return typeof metadata === 'object' && metadata !== null && 'type' in metadata && (metadata.type === 'directory' || metadata.type === 'file');
}


```

---


### `src/hooks/useUpdateNotification.ts`

**信息:**
- 行数: 34
- 大小: 982 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useState } from 'react'
import { major, minor, patch } from 'semver'

export function getSemverPart(version: string): string {
  return `${major(version, { loose: true })}.${minor(version, { loose: true })}.${patch(version, { loose: true })}`
}

export function shouldShowUpdateNotification(
  updatedVersion: string,
  lastNotifiedSemver: string | null,
): boolean {
  const updatedSemver = getSemverPart(updatedVersion)
  return updatedSemver !== lastNotifiedSemver
}

export function useUpdateNotification(
  updatedVersion: string | null | undefined,
  initialVersion: string = MACRO.VERSION,
): string | null {
  const [lastNotifiedSemver, setLastNotifiedSemver] = useState<string | null>(
    () => getSemverPart(initialVersion),
  )

  if (!updatedVersion) {
    return null
  }

  const updatedSemver = getSemverPart(updatedVersion)
  if (updatedSemver !== lastNotifiedSemver) {
    setLastNotifiedSemver(updatedSemver)
    return updatedSemver
  }
  return null
}

```

---


### `src/hooks/useVimInput.ts`

**信息:**
- 行数: 316
- 大小: 9741 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import React, { useCallback, useState } from 'react'
import type { Key } from '../ink.js'
import type { VimInputState, VimMode } from '../types/textInputTypes.js'
import { Cursor } from '../utils/Cursor.js'
import { lastGrapheme } from '../utils/intl.js'
import {
  executeIndent,
  executeJoin,
  executeOpenLine,
  executeOperatorFind,
  executeOperatorMotion,
  executeOperatorTextObj,
  executeReplace,
  executeToggleCase,
  executeX,
  type OperatorContext,
} from '../vim/operators.js'
import { type TransitionContext, transition } from '../vim/transitions.js'
import {
  createInitialPersistentState,
  createInitialVimState,
  type PersistentState,
  type RecordedChange,
  type VimState,
} from '../vim/types.js'
import { type UseTextInputProps, useTextInput } from './useTextInput.js'

type UseVimInputProps = Omit<UseTextInputProps, 'inputFilter'> & {
  onModeChange?: (mode: VimMode) => void
  onUndo?: () => void
  inputFilter?: UseTextInputProps['inputFilter']
}

export function useVimInput(props: UseVimInputProps): VimInputState {
  const vimStateRef = React.useRef<VimState>(createInitialVimState())
  const [mode, setMode] = useState<VimMode>('INSERT')

  const persistentRef = React.useRef<PersistentState>(
    createInitialPersistentState(),
  )

  // inputFilter is applied once at the top of handleVimInput (not here) so
  // vim-handled paths that return without calling textInput.onInput still
  // run the filter — otherwise a stateful filter (e.g. lazy-space-after-
  // pill) stays armed across an Escape → NORMAL → INSERT round-trip.
  const textInput = useTextInput({ ...props, inputFilter: undefined })
  const { onModeChange, inputFilter } = props

  const switchToInsertMode = useCallback(
    (offset?: number): void => {

```

---


### `src/hooks/useVirtualScroll.ts`

**信息:**
- 行数: 721
- 大小: 35122 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { RefObject } from 'react'
import {
  useCallback,
  useDeferredValue,
  useLayoutEffect,
  useMemo,
  useRef,
  useSyncExternalStore,
} from 'react'
import type { ScrollBoxHandle } from '../ink/components/ScrollBox.js'
import type { DOMElement } from '../ink/dom.js'

/**
 * Estimated height (rows) for items not yet measured. Intentionally LOW:
 * overestimating causes blank space (we stop mounting too early and the
 * viewport bottom shows empty spacer), while underestimating just mounts
 * a few extra items into overscan. The asymmetry means we'd rather err low.
 */
const DEFAULT_ESTIMATE = 3
/**
 * Extra rows rendered above and below the viewport. Generous because real
 * heights can be 10x the estimate for long tool results.
 */
const OVERSCAN_ROWS = 80
/** Items rendered before the ScrollBox has laid out (viewportHeight=0). */
const COLD_START_COUNT = 30
/**
 * scrollTop quantization for the useSyncExternalStore snapshot. Without
 * this, every wheel tick (3-5 per notch) triggers a full React commit +
 * Yoga calculateLayout() + Ink diff cycle — the CPU spike. Visual scroll
 * stays smooth regardless: ScrollBox.forceRender fires on every scrollBy
 * and Ink reads the REAL scrollTop from the DOM node, independent of what
 * React thinks. React only needs to re-render when the mounted range must
 * shift; half of OVERSCAN_ROWS is the tightest safe bin (guarantees ≥40
 * rows of overscan remain before the new range is needed).
 */
const SCROLL_QUANTUM = OVERSCAN_ROWS >> 1
/**
 * Worst-case height assumed for unmeasured items when computing coverage.
 * A MessageRow can be as small as 1 row (single-line tool call). Using 1
 * here guarantees the mounted span physically reaches the viewport bottom
 * regardless of how small items actually are — at the cost of over-mounting
 * when items are larger (which is fine, overscan absorbs it).
 */
const PESSIMISTIC_HEIGHT = 1
/** Cap on mounted items to bound fiber allocation even in degenerate cases. */
const MAX_MOUNTED_ITEMS = 300
/**
 * Max NEW items to mount in a single commit. Scrolling into a fresh range
 * with PESSIMISTIC_HEIGHT=1 would mount 194 items at once (OVERSCAN_ROWS*2+

```

---


### `src/hooks/useVoice.ts`

**信息:**
- 行数: 1144
- 大小: 45802 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// React hook for hold-to-talk voice input using Anthropic voice_stream STT.
//
// Hold the keybinding to record; release to stop and submit.  Auto-repeat
// key events reset an internal timer — when no keypress arrives within
// RELEASE_TIMEOUT_MS the recording stops automatically.  Uses the native
// audio module (macOS) or SoX for recording, and Anthropic's voice_stream
// endpoint (conversation_engine) for STT.

import { useCallback, useEffect, useRef, useState } from 'react'
import { useSetVoiceState } from '../context/voice.js'
import { useTerminalFocus } from '../ink/hooks/use-terminal-focus.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import { getVoiceKeyterms } from '../services/voiceKeyterms.js'
import {
  connectVoiceStream,
  type FinalizeSource,
  isVoiceStreamAvailable,
  type VoiceStreamConnection,
} from '../services/voiceStreamSTT.js'
import { logForDebugging } from '../utils/debug.js'
import { toError } from '../utils/errors.js'
import { getSystemLocaleLanguage } from '../utils/intl.js'
import { logError } from '../utils/log.js'
import { getInitialSettings } from '../utils/settings/settings.js'
import { sleep } from '../utils/sleep.js'

// ─── Language normalization ─────────────────────────────────────────────

const DEFAULT_STT_LANGUAGE = 'en'

// Maps language names (English and native) to BCP-47 codes supported by
// the voice_stream Deepgram backend.  Keys must be lowercase.
//
// This list must be a SUBSET of the server-side supported_language_codes
// allowlist (GrowthBook: speech_to_text_voice_stream_config).
// If the CLI sends a code the server rejects, the WebSocket closes with
// 1008 "Unsupported language" and voice breaks.  Unsupported languages
// fall back to DEFAULT_STT_LANGUAGE so recording still works.
const LANGUAGE_NAME_TO_CODE: Record<string, string> = {
  english: 'en',
  spanish: 'es',
  español: 'es',
  espanol: 'es',
  french: 'fr',
  français: 'fr',
  francais: 'fr',
  japanese: 'ja',

```

---


### `src/hooks/useVoiceEnabled.ts`

**信息:**
- 行数: 25
- 大小: 1134 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useMemo } from 'react'
import { useAppState } from '../state/AppState.js'
import {
  hasVoiceAuth,
  isVoiceGrowthBookEnabled,
} from '../voice/voiceModeEnabled.js'

/**
 * Combines user intent (settings.voiceEnabled) with auth + GB kill-switch.
 * Only the auth half is memoized on authVersion — it's the expensive one
 * (cold getClaudeAIOAuthTokens memoize → sync `security` spawn, ~60ms/call,
 * ~180ms total in profile v5 when token refresh cleared the cache mid-session).
 * GB is a cheap cached-map lookup and stays outside the memo so a mid-session
 * kill-switch flip still takes effect on the next render.
 *
 * authVersion bumps on /login only. Background token refresh leaves it alone
 * (user is still authed), so the auth memo stays correct without re-eval.
 */
export function useVoiceEnabled(): boolean {
  const userIntent = useAppState(s => s.settings.voiceEnabled === true)
  const authVersion = useAppState(s => s.authVersion)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const authed = useMemo(hasVoiceAuth, [authVersion])
  return userIntent && authed && isVoiceGrowthBookEnabled()
}

```

---


### `src/hooks/useVoiceIntegration.tsx`

**信息:**
- 行数: 677
- 大小: 99464 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import * as React from 'react';
import { useCallback, useEffect, useMemo, useRef } from 'react';
import { useNotifications } from '../context/notifications.js';
import { useIsModalOverlayActive } from '../context/overlayContext.js';
import { useGetVoiceState, useSetVoiceState, useVoiceState } from '../context/voice.js';
import { KeyboardEvent } from '../ink/events/keyboard-event.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- backward-compat bridge until REPL wires handleKeyDown to <Box onKeyDown>
import { useInput } from '../ink.js';
import { useOptionalKeybindingContext } from '../keybindings/KeybindingContext.js';
import { keystrokesEqual } from '../keybindings/resolver.js';
import type { ParsedKeystroke } from '../keybindings/types.js';
import { normalizeFullWidthSpace } from '../utils/stringUtils.js';
import { useVoiceEnabled } from './useVoiceEnabled.js';

// Dead code elimination: conditional import for voice input hook.
/* eslint-disable @typescript-eslint/no-require-imports */
// Capture the module namespace, not the function: spyOn() mutates the module
// object, so `voiceNs.useVoice(...)` resolves to the spy even if this module
// was loaded before the spy was installed (test ordering independence).
const voiceNs: {
  useVoice: typeof import('./useVoice.js').useVoice;
} = feature('VOICE_MODE') ? require('./useVoice.js') : {
  useVoice: ({
    enabled: _e
  }: {
    onTranscript: (t: string) => void;
    enabled: boolean;
  }) => ({
    state: 'idle' as const,
    handleKeyEvent: (_fallbackMs?: number) => {}
  })
};
/* eslint-enable @typescript-eslint/no-require-imports */

// Maximum gap (ms) between key presses to count as held (auto-repeat).
// Terminal auto-repeat fires every 30-80ms; 120ms covers jitter while
// excluding normal typing speed (100-300ms between keystrokes).
const RAPID_KEY_GAP_MS = 120;

// Fallback (ms) for modifier-combo first-press activation. Must match
// FIRST_PRESS_FALLBACK_MS in useVoice.ts. Covers the max OS initial
// key-repeat delay (~2s on macOS with slider at "Long") so holding a
// modifier combo doesn't fragment into two sessions when the first
// auto-repeat arrives after the default 600ms REPEAT_FALLBACK_MS.
const MODIFIER_FIRST_PRESS_FALLBACK_MS = 2000;

// Number of rapid consecutive key events required to activate voice.
// Only applies to bare-char bindings (space, v, etc.) where a single press
// could be normal typing. Modifier combos activate on the first press.

```

---

