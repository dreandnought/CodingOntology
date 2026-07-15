# components 模块

## 概述

**位置:** `src/components/`

## 文件统计

- TypeScript 文件: 49
- TypeScript React 文件: 357
- 总计: 406

## 文件详情

---


### `src/components/AgentProgressLine.tsx`

**信息:**
- 行数: 136
- 大小: 14238 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../ink.js';
import { formatNumber } from '../utils/format.js';
import type { Theme } from '../utils/theme.js';
type Props = {
  agentType: string;
  description?: string;
  name?: string;
  descriptionColor?: keyof Theme;
  taskDescription?: string;
  toolUseCount: number;
  tokens: number | null;
  color?: keyof Theme;
  isLast: boolean;
  isResolved: boolean;
  isError: boolean;
  isAsync?: boolean;
  shouldAnimate: boolean;
  lastToolInfo?: string | null;
  hideType?: boolean;
};
export function AgentProgressLine(t0) {
  const $ = _c(32);
  const {
    agentType,
    description,
    name,
    descriptionColor,
    taskDescription,
    toolUseCount,
    tokens,
    color,
    isLast,
    isResolved,
    isAsync: t1,
    lastToolInfo,
    hideType: t2
  } = t0;
  const isAsync = t1 === undefined ? false : t1;
  const hideType = t2 === undefined ? false : t2;
  const treeChar = isLast ? "\u2514\u2500" : "\u251C\u2500";
  const isBackgrounded = isAsync && isResolved;
  let t3;
  if ($[0] !== isBackgrounded || $[1] !== isResolved || $[2] !== lastToolInfo || $[3] !== taskDescription) {
    t3 = () => {
      if (!isResolved) {
        return lastToolInfo || "Initializing\u2026";
      }
      if (isBackgrounded) {

```

---


### `src/components/AntModelSwitchCallout.tsx`

**信息:**
- 行数: 3
- 大小: 58 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function AntModelSwitchCallout() {
  return null
}

```

---


### `src/components/App.tsx`

**信息:**
- 行数: 96
- 大小: 6279 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../ink.js';
import { FpsMetricsProvider } from '../context/fpsMetrics.js';
import { StatsProvider, type StatsStore } from '../context/stats.js';
import { type AppState, AppStateProvider } from '../state/AppState.js';
import { onChangeAppState } from '../state/onChangeAppState.js';
import type { FpsMetrics } from '../utils/fpsTracker.js';
type Props = {
  getFpsMetrics: () => FpsMetrics | undefined;
  stats?: StatsStore;
  initialState: AppState;
  children: React.ReactNode;
};

type BootstrapBoundaryState = {
  error: Error | null;
};

class BootstrapBoundary extends React.Component<{
  children: React.ReactNode;
}, BootstrapBoundaryState> {
  override state: BootstrapBoundaryState = {
    error: null
  };
  static override getDerivedStateFromError(error: Error): BootstrapBoundaryState {
    return {
      error
    };
  }
  override componentDidCatch(error: Error): void {
    const message = error?.stack ?? error?.message ?? String(error);
    console.error(`[restored-app-bootstrap] ${message}`);
  }
  override render(): React.ReactNode {
    if (!this.state.error) {
      return this.props.children;
    }
    return <Box flexDirection="column" paddingX={1}>
      <Text color="red">Failed to initialize restored app bootstrap.</Text>
      <Text dimColor>{this.state.error.message || String(this.state.error)}</Text>
    </Box>;
  }
}

/**
 * Top-level wrapper for interactive sessions.
 * Provides FPS metrics, stats context, and app state to the component tree.
 */
export function App(t0) {

```

---


### `src/components/ApproveApiKey.tsx`

**信息:**
- 行数: 123
- 大小: 10621 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Text } from '../ink.js';
import { saveGlobalConfig } from '../utils/config.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
type Props = {
  customApiKeyTruncated: string;
  onDone(approved: boolean): void;
};
export function ApproveApiKey(t0) {
  const $ = _c(17);
  const {
    customApiKeyTruncated,
    onDone
  } = t0;
  let t1;
  if ($[0] !== customApiKeyTruncated || $[1] !== onDone) {
    t1 = function onChange(value) {
      bb2: switch (value) {
        case "yes":
          {
            saveGlobalConfig(current_0 => ({
              ...current_0,
              customApiKeyResponses: {
                ...current_0.customApiKeyResponses,
                approved: [...(current_0.customApiKeyResponses?.approved ?? []), customApiKeyTruncated]
              }
            }));
            onDone(true);
            break bb2;
          }
        case "no":
          {
            saveGlobalConfig(current => ({
              ...current,
              customApiKeyResponses: {
                ...current.customApiKeyResponses,
                rejected: [...(current.customApiKeyResponses?.rejected ?? []), customApiKeyTruncated]
              }
            }));
            onDone(false);
          }
      }
    };
    $[0] = customApiKeyTruncated;
    $[1] = onDone;
    $[2] = t1;
  } else {
    t1 = $[2];

```

---


### `src/components/AutoModeOptInDialog.tsx`

**信息:**
- 行数: 142
- 大小: 13302 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { logEvent } from 'src/services/analytics/index.js';
import { Box, Link, Text } from '../ink.js';
import { updateSettingsForSource } from '../utils/settings/settings.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';

// NOTE: This copy is legally reviewed — do not modify without Legal team approval.
export const AUTO_MODE_DESCRIPTION = "Auto mode lets Claude handle permission prompts automatically — Claude checks each tool call for risky actions and prompt injection before executing. Actions Claude identifies as safe are executed, while actions Claude identifies as risky are blocked and Claude may try a different approach. Ideal for long-running tasks. Sessions are slightly more expensive. Claude can make mistakes that allow harmful commands to run, it's recommended to only use in isolated environments. Shift+Tab to change mode.";
type Props = {
  onAccept(): void;
  onDecline(): void;
  // Startup gate: decline exits the process, so relabel accordingly.
  declineExits?: boolean;
};
export function AutoModeOptInDialog(t0) {
  const $ = _c(18);
  const {
    onAccept,
    onDecline,
    declineExits
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = [];
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  React.useEffect(_temp, t1);
  let t2;
  if ($[1] !== onAccept || $[2] !== onDecline) {
    t2 = function onChange(value) {
      bb3: switch (value) {
        case "accept":
          {
            logEvent("tengu_auto_mode_opt_in_dialog_accept", {});
            updateSettingsForSource("userSettings", {
              skipAutoPermissionPrompt: true
            });
            onAccept();
            break bb3;
          }
        case "accept-default":
          {
            logEvent("tengu_auto_mode_opt_in_dialog_accept_default", {});
            updateSettingsForSource("userSettings", {
              skipAutoPermissionPrompt: true,
              permissions: {

```

---


### `src/components/AutoUpdater.tsx`

**信息:**
- 行数: 198
- 大小: 30788 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { useInterval } from 'usehooks-ts';
import { useUpdateNotification } from '../hooks/useUpdateNotification.js';
import { Box, Text } from '../ink.js';
import { type AutoUpdaterResult, getLatestVersion, getMaxVersion, type InstallStatus, installGlobalPackage, shouldSkipVersion } from '../utils/autoUpdater.js';
import { getGlobalConfig, isAutoUpdaterDisabled } from '../utils/config.js';
import { logForDebugging } from '../utils/debug.js';
import { getCurrentInstallationType } from '../utils/doctorDiagnostic.js';
import { installOrUpdateClaudePackage, localInstallationExists } from '../utils/localInstaller.js';
import { removeInstalledSymlink } from '../utils/nativeInstaller/index.js';
import { gt, gte } from '../utils/semver.js';
import { getInitialSettings } from '../utils/settings/settings.js';
type Props = {
  isUpdating: boolean;
  onChangeIsUpdating: (isUpdating: boolean) => void;
  onAutoUpdaterResult: (autoUpdaterResult: AutoUpdaterResult) => void;
  autoUpdaterResult: AutoUpdaterResult | null;
  showSuccessMessage: boolean;
  verbose: boolean;
};
export function AutoUpdater({
  isUpdating,
  onChangeIsUpdating,
  onAutoUpdaterResult,
  autoUpdaterResult,
  showSuccessMessage,
  verbose
}: Props): React.ReactNode {
  const [versions, setVersions] = useState<{
    global?: string | null;
    latest?: string | null;
  }>({});
  const [hasLocalInstall, setHasLocalInstall] = useState(false);
  const updateSemver = useUpdateNotification(autoUpdaterResult?.version);
  useEffect(() => {
    void localInstallationExists().then(setHasLocalInstall);
  }, []);

  // Track latest isUpdating value in a ref so the memoized checkForUpdates
  // callback always sees the current value. Without this, the 30-minute
  // interval fires with a stale closure where isUpdating is false, allowing
  // a concurrent installGlobalPackage() to run while one is already in
  // progress.
  const isUpdatingRef = useRef(isUpdating);
  isUpdatingRef.current = isUpdating;
  const checkForUpdates = React.useCallback(async () => {
    if (isUpdatingRef.current) {
      return;

```

---


### `src/components/AutoUpdaterWrapper.tsx`

**信息:**
- 行数: 91
- 大小: 11972 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import * as React from 'react';
import type { AutoUpdaterResult } from '../utils/autoUpdater.js';
import { isAutoUpdaterDisabled } from '../utils/config.js';
import { logForDebugging } from '../utils/debug.js';
import { getCurrentInstallationType } from '../utils/doctorDiagnostic.js';
import { AutoUpdater } from './AutoUpdater.js';
import { NativeAutoUpdater } from './NativeAutoUpdater.js';
import { PackageManagerAutoUpdater } from './PackageManagerAutoUpdater.js';
type Props = {
  isUpdating: boolean;
  onChangeIsUpdating: (isUpdating: boolean) => void;
  onAutoUpdaterResult: (autoUpdaterResult: AutoUpdaterResult) => void;
  autoUpdaterResult: AutoUpdaterResult | null;
  showSuccessMessage: boolean;
  verbose: boolean;
};
export function AutoUpdaterWrapper(t0) {
  const $ = _c(17);
  const {
    isUpdating,
    onChangeIsUpdating,
    onAutoUpdaterResult,
    autoUpdaterResult,
    showSuccessMessage,
    verbose
  } = t0;
  const [useNativeInstaller, setUseNativeInstaller] = React.useState(null);
  const [isPackageManager, setIsPackageManager] = React.useState(null);
  let t1;
  let t2;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = () => {
      const checkInstallation = async function checkInstallation() {
        if (feature("SKIP_DETECTION_WHEN_AUTOUPDATES_DISABLED") && isAutoUpdaterDisabled()) {
          logForDebugging("AutoUpdaterWrapper: Skipping detection, auto-updates disabled");
          return;
        }
        const installationType = await getCurrentInstallationType();
        logForDebugging(`AutoUpdaterWrapper: Installation type: ${installationType}`);
        setUseNativeInstaller(installationType === "native");
        setIsPackageManager(installationType === "package-manager");
      };
      checkInstallation();
    };
    t2 = [];
    $[0] = t1;
    $[1] = t2;
  } else {

```

---


### `src/components/AwsAuthStatusBox.tsx`

**信息:**
- 行数: 82
- 大小: 9707 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useEffect, useState } from 'react';
import { Box, Link, Text } from '../ink.js';
import { type AwsAuthStatus, AwsAuthStatusManager } from '../utils/awsAuthStatusManager.js';
const URL_RE = /https?:\/\/\S+/;
export function AwsAuthStatusBox() {
  const $ = _c(11);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = AwsAuthStatusManager.getInstance().getStatus();
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  const [status, setStatus] = useState(t0);
  let t1;
  let t2;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = () => {
      const unsubscribe = AwsAuthStatusManager.getInstance().subscribe(setStatus);
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
  if (!status.isAuthenticating && !status.error && status.output.length === 0) {
    return null;
  }
  if (!status.isAuthenticating && !status.error) {
    return null;
  }
  let t3;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = <Text bold={true} color="permission">Cloud Authentication</Text>;
    $[3] = t3;
  } else {
    t3 = $[3];
  }
  let t4;
  if ($[4] !== status.output) {
    t4 = status.output.length > 0 && <Box flexDirection="column" marginTop={1}>{status.output.slice(-5).map(_temp)}</Box>;
    $[4] = status.output;
    $[5] = t4;
  } else {
    t4 = $[5];

```

---


### `src/components/BaseTextInput.tsx`

**信息:**
- 行数: 136
- 大小: 19313 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { renderPlaceholder } from '../hooks/renderPlaceholder.js';
import { usePasteHandler } from '../hooks/usePasteHandler.js';
import { useDeclaredCursor } from '../ink/hooks/use-declared-cursor.js';
import { Ansi, Box, Text, useInput } from '../ink.js';
import type { BaseInputState, BaseTextInputProps } from '../types/textInputTypes.js';
import type { TextHighlight } from '../utils/textHighlighting.js';
import { HighlightedInput } from './PromptInput/ShimmeredInput.js';
type BaseTextInputComponentProps = BaseTextInputProps & {
  inputState: BaseInputState;
  children?: React.ReactNode;
  terminalFocus: boolean;
  highlights?: TextHighlight[];
  invert?: (text: string) => string;
  hidePlaceholderText?: boolean;
};

/**
 * A base component for text inputs that handles rendering and basic input
 */
export function BaseTextInput(t0) {
  const $ = _c(14);
  const {
    inputState,
    children,
    terminalFocus,
    invert,
    hidePlaceholderText,
    ...props
  } = t0;
  const {
    onInput,
    renderedValue,
    cursorLine,
    cursorColumn
  } = inputState;
  const t1 = Boolean(props.focus && props.showCursor && terminalFocus);
  let t2;
  if ($[0] !== cursorColumn || $[1] !== cursorLine || $[2] !== t1) {
    t2 = {
      line: cursorLine,
      column: cursorColumn,
      active: t1
    };
    $[0] = cursorColumn;
    $[1] = cursorLine;
    $[2] = t1;
    $[3] = t2;
  } else {

```

---


### `src/components/BashModeProgress.tsx`

**信息:**
- 行数: 56
- 大小: 5675 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box } from '../ink.js';
import { BashTool } from '../tools/BashTool/BashTool.js';
import type { ShellProgress } from '../types/tools.js';
import { UserBashInputMessage } from './messages/UserBashInputMessage.js';
import { ShellProgressMessage } from './shell/ShellProgressMessage.js';
type Props = {
  input: string;
  progress: ShellProgress | null;
  verbose: boolean;
};
export function BashModeProgress(t0) {
  const $ = _c(8);
  const {
    input,
    progress,
    verbose
  } = t0;
  const t1 = `<bash-input>${input}</bash-input>`;
  let t2;
  if ($[0] !== t1) {
    t2 = <UserBashInputMessage addMargin={false} param={{
      text: t1,
      type: "text"
    }} />;
    $[0] = t1;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  let t3;
  if ($[2] !== progress || $[3] !== verbose) {
    t3 = progress ? <ShellProgressMessage fullOutput={progress.fullOutput} output={progress.output} elapsedTimeSeconds={progress.elapsedTimeSeconds} totalLines={progress.totalLines} verbose={verbose} /> : BashTool.renderToolUseProgressMessage?.([], {
      verbose,
      tools: [],
      terminalSize: undefined
    });
    $[2] = progress;
    $[3] = verbose;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  let t4;
  if ($[5] !== t2 || $[6] !== t3) {
    t4 = <Box flexDirection="column" marginTop={1}>{t2}{t3}</Box>;
    $[5] = t2;
    $[6] = t3;
    $[7] = t4;

```

---


### `src/components/BridgeDialog.tsx`

**信息:**
- 行数: 401
- 大小: 34418 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { basename } from 'path';
import { toString as qrToString } from 'qrcode';
import * as React from 'react';
import { useEffect, useState } from 'react';
import { getOriginalCwd } from '../bootstrap/state.js';
import { buildActiveFooterText, buildIdleFooterText, FAILED_FOOTER_TEXT, getBridgeStatus } from '../bridge/bridgeStatusUtil.js';
import { BRIDGE_FAILED_INDICATOR, BRIDGE_READY_INDICATOR } from '../constants/figures.js';
import { useRegisterOverlay } from '../context/overlayContext.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- raw 'd' key for disconnect, not a configurable keybinding action
import { Box, Text, useInput } from '../ink.js';
import { useKeybindings } from '../keybindings/useKeybinding.js';
import { useAppState, useSetAppState } from '../state/AppState.js';
import { saveGlobalConfig } from '../utils/config.js';
import { getBranch } from '../utils/git.js';
import { Dialog } from './design-system/Dialog.js';
type Props = {
  onDone: () => void;
};
export function BridgeDialog(t0) {
  const $ = _c(87);
  const {
    onDone
  } = t0;
  useRegisterOverlay("bridge-dialog");
  const connected = useAppState(_temp);
  const sessionActive = useAppState(_temp2);
  const reconnecting = useAppState(_temp3);
  const connectUrl = useAppState(_temp4);
  const sessionUrl = useAppState(_temp5);
  const error = useAppState(_temp6);
  const explicit = useAppState(_temp7);
  const environmentId = useAppState(_temp8);
  const sessionId = useAppState(_temp9);
  const verbose = useAppState(_temp0);
  const setAppState = useSetAppState();
  const [showQR, setShowQR] = useState(false);
  const [qrText, setQrText] = useState("");
  const [branchName, setBranchName] = useState("");
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = basename(getOriginalCwd());
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const repoName = t1;
  let t2;
  let t3;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {

```

---


### `src/components/BypassPermissionsModeDialog.tsx`

**信息:**
- 行数: 87
- 大小: 9136 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback } from 'react';
import { logEvent } from 'src/services/analytics/index.js';
import { Box, Link, Newline, Text } from '../ink.js';
import { gracefulShutdownSync } from '../utils/gracefulShutdown.js';
import { updateSettingsForSource } from '../utils/settings/settings.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
type Props = {
  onAccept(): void;
};
export function BypassPermissionsModeDialog(t0) {
  const $ = _c(7);
  const {
    onAccept
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = [];
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  React.useEffect(_temp, t1);
  let t2;
  if ($[1] !== onAccept) {
    t2 = function onChange(value) {
      bb3: switch (value) {
        case "accept":
          {
            logEvent("tengu_bypass_permissions_mode_dialog_accept", {});
            updateSettingsForSource("userSettings", {
              skipDangerousModePermissionPrompt: true
            });
            onAccept();
            break bb3;
          }
        case "decline":
          {
            gracefulShutdownSync(1);
          }
      }
    };
    $[1] = onAccept;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  const onChange = t2;
  const handleEscape = _temp2;

```

---


### `src/components/ChannelDowngradeDialog.tsx`

**信息:**
- 行数: 102
- 大小: 8253 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Text } from '../ink.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
export type ChannelDowngradeChoice = 'downgrade' | 'stay' | 'cancel';
type Props = {
  currentVersion: string;
  onChoice: (choice: ChannelDowngradeChoice) => void;
};

/**
 * Dialog shown when switching from latest to stable channel.
 * Allows user to choose whether to downgrade or stay on current version.
 */
export function ChannelDowngradeDialog(t0) {
  const $ = _c(17);
  const {
    currentVersion,
    onChoice
  } = t0;
  let t1;
  if ($[0] !== onChoice) {
    t1 = function handleSelect(value) {
      onChoice(value);
    };
    $[0] = onChoice;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const handleSelect = t1;
  let t2;
  if ($[2] !== onChoice) {
    t2 = function handleCancel() {
      onChoice("cancel");
    };
    $[2] = onChoice;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  const handleCancel = t2;
  let t3;
  if ($[4] !== currentVersion) {
    t3 = <Text>The stable channel may have an older version than what you're currently running ({currentVersion}).</Text>;
    $[4] = currentVersion;
    $[5] = t3;
  } else {
    t3 = $[5];

```

---


### `src/components/ClaudeCodeHint/PluginHintMenu.tsx`

**信息:**
- 行数: 78
- 大小: 9341 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { Select } from '../CustomSelect/select.js';
import { PermissionDialog } from '../permissions/PermissionDialog.js';
type Props = {
  pluginName: string;
  pluginDescription?: string;
  marketplaceName: string;
  sourceCommand: string;
  onResponse: (response: 'yes' | 'no' | 'disable') => void;
};
const AUTO_DISMISS_MS = 30_000;
export function PluginHintMenu({
  pluginName,
  pluginDescription,
  marketplaceName,
  sourceCommand,
  onResponse
}: Props): React.ReactNode {
  const onResponseRef = React.useRef(onResponse);
  onResponseRef.current = onResponse;
  React.useEffect(() => {
    const timeoutId = setTimeout(ref => ref.current('no'), AUTO_DISMISS_MS, onResponseRef);
    return () => clearTimeout(timeoutId);
  }, []);
  function onSelect(value: string): void {
    switch (value) {
      case 'yes':
        onResponse('yes');
        break;
      case 'disable':
        onResponse('disable');
        break;
      default:
        onResponse('no');
    }
  }
  const options = [{
    label: <Text>
          Yes, install <Text bold>{pluginName}</Text>
        </Text>,
    value: 'yes'
  }, {
    label: 'No',
    value: 'no'
  }, {
    label: "No, and don't show plugin installation hints again",
    value: 'disable'
  }];
  return <PermissionDialog title="Plugin Recommendation">

```

---


### `src/components/ClaudeInChromeOnboarding.tsx`

**信息:**
- 行数: 121
- 大小: 12151 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { logEvent } from 'src/services/analytics/index.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- enter to continue
import { Box, Link, Newline, Text, useInput } from '../ink.js';
import { isChromeExtensionInstalled } from '../utils/claudeInChrome/setup.js';
import { saveGlobalConfig } from '../utils/config.js';
import { Dialog } from './design-system/Dialog.js';
const CHROME_EXTENSION_URL = 'https://claude.ai/chrome';
const CHROME_PERMISSIONS_URL = 'https://clau.de/chrome/permissions';
type Props = {
  onDone(): void;
};
export function ClaudeInChromeOnboarding(t0) {
  const $ = _c(20);
  const {
    onDone
  } = t0;
  const [isExtensionInstalled, setIsExtensionInstalled] = React.useState(false);
  let t1;
  let t2;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = () => {
      logEvent("tengu_claude_in_chrome_onboarding_shown", {});
      isChromeExtensionInstalled().then(setIsExtensionInstalled);
      saveGlobalConfig(_temp);
    };
    t2 = [];
    $[0] = t1;
    $[1] = t2;
  } else {
    t1 = $[0];
    t2 = $[1];
  }
  React.useEffect(t1, t2);
  let t3;
  if ($[2] !== onDone) {
    t3 = (_input, key) => {
      if (key.return) {
        onDone();
      }
    };
    $[2] = onDone;
    $[3] = t3;
  } else {
    t3 = $[3];
  }
  useInput(t3);
  let t4;
  if ($[4] !== isExtensionInstalled) {

```

---


### `src/components/ClaudeMdExternalIncludesDialog.tsx`

**信息:**
- 行数: 137
- 大小: 13532 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback } from 'react';
import { logEvent } from 'src/services/analytics/index.js';
import { Box, Link, Text } from '../ink.js';
import type { ExternalClaudeMdInclude } from '../utils/claudemd.js';
import { saveCurrentProjectConfig } from '../utils/config.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
type Props = {
  onDone(): void;
  isStandaloneDialog?: boolean;
  externalIncludes?: ExternalClaudeMdInclude[];
};
export function ClaudeMdExternalIncludesDialog(t0) {
  const $ = _c(18);
  const {
    onDone,
    isStandaloneDialog,
    externalIncludes
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = [];
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  React.useEffect(_temp, t1);
  let t2;
  if ($[1] !== onDone) {
    t2 = value => {
      if (value === "no") {
        logEvent("tengu_claude_md_external_includes_dialog_declined", {});
        saveCurrentProjectConfig(_temp2);
      } else {
        logEvent("tengu_claude_md_external_includes_dialog_accepted", {});
        saveCurrentProjectConfig(_temp3);
      }
      onDone();
    };
    $[1] = onDone;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  const handleSelection = t2;
  let t3;
  if ($[3] !== handleSelection) {
    t3 = () => {
      handleSelection("no");

```

---


### `src/components/ClickableImageRef.tsx`

**信息:**
- 行数: 73
- 大小: 7495 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { pathToFileURL } from 'url';
import Link from '../ink/components/Link.js';
import { supportsHyperlinks } from '../ink/supports-hyperlinks.js';
import { Text } from '../ink.js';
import { getStoredImagePath } from '../utils/imageStore.js';
import type { Theme } from '../utils/theme.js';
type Props = {
  imageId: number;
  backgroundColor?: keyof Theme;
  isSelected?: boolean;
};

/**
 * Renders an image reference like [Image #1] as a clickable link.
 * When clicked, opens the stored image file in the default viewer.
 *
 * Falls back to styled text if:
 * - Terminal doesn't support hyperlinks
 * - Image file is not found in the store
 */
export function ClickableImageRef(t0) {
  const $ = _c(13);
  const {
    imageId,
    backgroundColor,
    isSelected: t1
  } = t0;
  const isSelected = t1 === undefined ? false : t1;
  const imagePath = getStoredImagePath(imageId);
  const displayText = `[Image #${imageId}]`;
  if (imagePath && supportsHyperlinks()) {
    const fileUrl = pathToFileURL(imagePath).href;
    let t2;
    let t3;
    if ($[0] !== backgroundColor || $[1] !== displayText || $[2] !== isSelected) {
      t2 = <Text backgroundColor={backgroundColor} inverse={isSelected}>{displayText}</Text>;
      t3 = <Text backgroundColor={backgroundColor} inverse={isSelected} bold={isSelected}>{displayText}</Text>;
      $[0] = backgroundColor;
      $[1] = displayText;
      $[2] = isSelected;
      $[3] = t2;
      $[4] = t3;
    } else {
      t2 = $[3];
      t3 = $[4];
    }
    let t4;
    if ($[5] !== fileUrl || $[6] !== t2 || $[7] !== t3) {

```

---


### `src/components/CompactSummary.tsx`

**信息:**
- 行数: 118
- 大小: 14437 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { BLACK_CIRCLE } from '../constants/figures.js';
import { Box, Text } from '../ink.js';
import type { Screen } from '../screens/REPL.js';
import type { NormalizedUserMessage } from '../types/message.js';
import { getUserMessageText } from '../utils/messages.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { MessageResponse } from './MessageResponse.js';
type Props = {
  message: NormalizedUserMessage;
  screen: Screen;
};
export function CompactSummary(t0) {
  const $ = _c(24);
  const {
    message,
    screen
  } = t0;
  const isTranscriptMode = screen === "transcript";
  let t1;
  if ($[0] !== message) {
    t1 = getUserMessageText(message) || "";
    $[0] = message;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const textContent = t1;
  const metadata = message.summarizeMetadata;
  if (metadata) {
    let t2;
    if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
      t2 = <Box minWidth={2}><Text color="text">{BLACK_CIRCLE}</Text></Box>;
      $[2] = t2;
    } else {
      t2 = $[2];
    }
    let t3;
    if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
      t3 = <Text bold={true}>Summarized conversation</Text>;
      $[3] = t3;
    } else {
      t3 = $[3];
    }
    let t4;
    if ($[4] !== isTranscriptMode || $[5] !== metadata) {
      t4 = !isTranscriptMode && <MessageResponse><Box flexDirection="column"><Text dimColor={true}>Summarized {metadata.messagesSummarized} messages{" "}{metadata.direction === "up_to" ? "up to this point" : "from this point"}</Text>{metadata.userContext && <Text dimColor={true}>Context: {"\u201C"}{metadata.userContext}{"\u201D"}</Text>}<Text dimColor={true}><ConfigurableShortcutHint action="app:toggleTranscript" context="Global" fallback="ctrl+o" description="expand history" parens={true} /></Text></Box></MessageResponse>;
      $[4] = isTranscriptMode;
      $[5] = metadata;

```

---


### `src/components/ConfigurableShortcutHint.tsx`

**信息:**
- 行数: 57
- 大小: 5436 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import type { KeybindingAction, KeybindingContextName } from '../keybindings/types.js';
import { useShortcutDisplay } from '../keybindings/useShortcutDisplay.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
type Props = {
  /** The keybinding action (e.g., 'app:toggleTranscript') */
  action: KeybindingAction;
  /** The keybinding context (e.g., 'Global') */
  context: KeybindingContextName;
  /** Default shortcut if keybinding not configured */
  fallback: string;
  /** The action description text (e.g., 'expand') */
  description: string;
  /** Whether to wrap in parentheses */
  parens?: boolean;
  /** Whether to show in bold */
  bold?: boolean;
};

/**
 * KeyboardShortcutHint that displays the user-configured shortcut.
 * Falls back to default if keybinding context is not available.
 *
 * @example
 * <ConfigurableShortcutHint
 *   action="app:toggleTranscript"
 *   context="Global"
 *   fallback="ctrl+o"
 *   description="expand"
 * />
 */
export function ConfigurableShortcutHint(t0) {
  const $ = _c(5);
  const {
    action,
    context,
    fallback,
    description,
    parens,
    bold
  } = t0;
  const shortcut = useShortcutDisplay(action, context, fallback);
  let t1;
  if ($[0] !== bold || $[1] !== description || $[2] !== parens || $[3] !== shortcut) {
    t1 = <KeyboardShortcutHint shortcut={shortcut} action={description} parens={parens} bold={bold} />;
    $[0] = bold;
    $[1] = description;
    $[2] = parens;
    $[3] = shortcut;

```

---


### `src/components/ConsoleOAuthFlow.tsx`

**信息:**
- 行数: 631
- 大小: 79968 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { installOAuthTokens } from '../cli/handlers/auth.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { setClipboard } from '../ink/termio/osc.js';
import { useTerminalNotification } from '../ink/useTerminalNotification.js';
import { Box, Link, Text } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { getSSLErrorHint } from '../services/api/errorUtils.js';
import { sendNotification } from '../services/notifier.js';
import { OAuthService } from '../services/oauth/index.js';
import { getOauthAccountInfo, validateForceLoginOrg } from '../utils/auth.js';
import { logError } from '../utils/log.js';
import { getSettings_DEPRECATED } from '../utils/settings/settings.js';
import { Select } from './CustomSelect/select.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import { Spinner } from './Spinner.js';
import TextInput from './TextInput.js';
type Props = {
  onDone(): void;
  startingMessage?: string;
  mode?: 'login' | 'setup-token';
  forceLoginMethod?: 'claudeai' | 'console';
};
type OAuthStatus = {
  state: 'idle';
} // Initial state, waiting to select login method
| {
  state: 'platform_setup';
} // Show platform setup info (Bedrock/Vertex/Foundry)
| {
  state: 'ready_to_start';
} // Flow started, waiting for browser to open
| {
  state: 'waiting_for_login';
  url: string;
} // Browser opened, waiting for user to login
| {
  state: 'creating_api_key';
} // Got access token, creating API key
| {
  state: 'about_to_retry';
  nextState: OAuthStatus;
} | {
  state: 'success';
  token?: string;
} | {
  state: 'error';
  message: string;

```

---


### `src/components/ContextSuggestions.tsx`

**信息:**
- 行数: 47
- 大小: 5952 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { Box, Text } from '../ink.js';
import type { ContextSuggestion } from '../utils/contextSuggestions.js';
import { formatTokens } from '../utils/format.js';
import { StatusIcon } from './design-system/StatusIcon.js';
type Props = {
  suggestions: ContextSuggestion[];
};
export function ContextSuggestions(t0) {
  const $ = _c(5);
  const {
    suggestions
  } = t0;
  if (suggestions.length === 0) {
    return null;
  }
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Text bold={true}>Suggestions</Text>;
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  let t2;
  if ($[1] !== suggestions) {
    t2 = suggestions.map(_temp);
    $[1] = suggestions;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  let t3;
  if ($[3] !== t2) {
    t3 = <Box flexDirection="column" marginTop={1}>{t1}{t2}</Box>;
    $[3] = t2;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  return t3;
}
function _temp(suggestion, i) {
  return <Box key={i} flexDirection="column" marginTop={i === 0 ? 0 : 1}><Box><StatusIcon status={suggestion.severity} withSpace={true} /><Text bold={true}>{suggestion.title}</Text>{suggestion.savingsTokens ? <Text dimColor={true}>{" "}{figures.arrowRight} save ~{formatTokens(suggestion.savingsTokens)}</Text> : null}</Box><Box marginLeft={2}><Text dimColor={true}>{suggestion.detail}</Text></Box></Box>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJmaWd1cmVzIiwiUmVhY3QiLCJCb3giLCJUZXh0IiwiQ29udGV4dFN1Z2dlc3Rpb24iLCJmb3JtYXRUb2tlbnMiLCJTdGF0dXNJY29uIiwiUHJvcHMiLCJzdWdnZXN0aW9ucyIsIkNvbnRleHRTdWdnZXN0aW9ucyIsInQwIiwiJCIsIl9jIiwibGVuZ3RoIiwidDEiLCJTeW1ib2wiLCJmb3IiLCJ0MiIsIm1hcCIsIl90ZW1wIiwidDMiLCJzdWdnZXN0aW9uIiwiaSIsInNldmVyaXR5IiwidGl0bGUiLCJzYXZpbmdzVG9rZW5zIiwiYXJyb3dSaWdodCIsImRldGFpbCJdLCJzb3VyY2VzIjpbIkNvbnRleHRTdWdnZXN0aW9ucy50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IGZpZ3VyZXMgZnJvbSAnZmlndXJlcydcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgQm94LCBUZXh0IH0gZnJvbSAnLi4vaW5rLmpzJ1xuaW1wb3J0IHR5cGUgeyBDb250ZXh0U3VnZ2VzdGlvbiB9IGZyb20gJy4uL3V0aWxzL2NvbnRleHRTdWdnZXN0aW9ucy5qcydcbmltcG9ydCB7IGZvcm1hdFRva2VucyB9IGZyb20gJy4uL3V0aWxzL2Zvcm1hdC5qcydcbmltcG9ydCB7IFN0YXR1c0ljb24gfSBmcm9tICcuL2Rlc2lnbi1zeXN0ZW0vU3RhdHVzSWNvbi5qcydcblxudHlwZSBQcm9wcyA9IHtcbiAgc3VnZ2VzdGlvbnM6IENvbnRleHRTdWdnZXN0aW9uW11cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIENvbnRleHRTdWdnZXN0aW9ucyh7IHN1Z2dlc3Rpb25zIH06IFByb3BzKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgaWYgKHN1Z2dlc3Rpb25zLmxlbmd0aCA9PT0gMCkgcmV0dXJuIG51bGxcblxuICByZXR1cm4gKFxuICAgIDxCb3ggZmxleERpcmVjdGlvbj1cImNvbHVtblwiIG1hcmdpblRvcD17MX0+XG4gICAgICA8VGV4dCBib2xkPlN1Z2dlc3Rpb25zPC9UZXh0PlxuICAgICAge3N1Z2dlc3Rpb25zLm1hcCgoc3VnZ2VzdGlvbiwgaSkgPT4gKFxuICAgICAgICA8Qm94IGtleT17aX0gZmxleERpcmVjdGlvbj1cImNvbHVtblwiIG1hcmdpblRvcD17aSA9PT0gMCA/IDAgOiAxfT5cbiAgICAgICAgICA8Qm94PlxuICAgICAgICAgICAgPFN0YXR1c0ljb24gc3RhdHVzPXtzdWdnZXN0aW9uLnNldmVyaXR5fSB3aXRoU3BhY2UgLz5cbiAgICAgICAgICAgIDxUZXh0IGJvbGQ+e3N1Z2dlc3Rpb24udGl0bGV9PC9UZXh0PlxuICAgICAgICAgICAge3N1Z2dlc3Rpb24uc2F2aW5nc1Rva2VucyA/IChcbiAgICAgICAgICAgICAgPFRleHQgZGltQ29sb3I+XG4gICAgICAgICAgICAgICAgeycgJ31cbiAgICAgICAgICAgICAgICB7ZmlndXJlcy5hcnJvd1JpZ2h0fSBzYXZlIH5cbiAgICAgICAgICAgICAgICB7Zm9ybWF0VG9rZW5zKHN1Z2dlc3Rpb24uc2F2aW5nc1Rva2Vucyl9XG4gICAgICAgICAgICAgIDwvVGV4dD5cbiAgICAgICAgICAgICkgOiBudWxsfVxuICAgICAgICAgIDwvQm94PlxuICAgICAgICAgIDxCb3ggbWFyZ2luTGVmdD17Mn0+XG4gICAgICAgICAgICA8VGV4dCBkaW1Db2xvcj57c3VnZ2VzdGlvbi5kZXRhaWx9PC9UZXh0PlxuICAgICAgICAgIDwvQm94PlxuICAgICAgICA8L0JveD5cbiAgICAgICkpfVxuICAgIDwvQm94PlxuICApXG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxPQUFPQSxPQUFPLE1BQU0sU0FBUztBQUM3QixPQUFPLEtBQUtDLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxRQUFRLFdBQVc7QUFDckMsY0FBY0MsaUJBQWlCLFFBQVEsZ0NBQWdDO0FBQ3ZFLFNBQVNDLFlBQVksUUFBUSxvQkFBb0I7QUFDakQsU0FBU0MsVUFBVSxRQUFRLCtCQUErQjtBQUUxRCxLQUFLQyxLQUFLLEdBQUc7RUFDWEMsV0FBVyxFQUFFSixpQkFBaUIsRUFBRTtBQUNsQyxDQUFDO0FBRUQsT0FBTyxTQUFBSyxtQkFBQUMsRUFBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUE0QjtJQUFBSjtFQUFBLElBQUFFLEVBQXNCO0VBQ3ZELElBQUlGLFdBQVcsQ0FBQUssTUFBTyxLQUFLLENBQUM7SUFBQSxPQUFTLElBQUk7RUFBQTtFQUFBLElBQUFDLEVBQUE7RUFBQSxJQUFBSCxDQUFBLFFBQUFJLE1BQUEsQ0FBQUMsR0FBQTtJQUlyQ0YsRUFBQSxJQUFDLElBQUksQ0FBQyxJQUFJLENBQUosS0FBRyxDQUFDLENBQUMsV0FBVyxFQUFyQixJQUFJLENBQXdCO0lBQUFILENBQUEsTUFBQUcsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUgsQ0FBQTtFQUFBO0VBQUEsSUFBQU0sRUFBQTtFQUFBLElBQUFOLENBQUEsUUFBQUgsV0FBQTtJQUM1QlMsRUFBQSxHQUFBVCxXQUFXLENBQUFVLEdBQUksQ0FBQ0MsS0FpQmhCLENBQUM7SUFBQVIsQ0FBQSxNQUFBSCxXQUFBO0lBQUFHLENBQUEsTUFBQU0sRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQU4sQ0FBQTtFQUFBO0VBQUEsSUFBQVMsRUFBQTtFQUFBLElBQUFULENBQUEsUUFBQU0sRUFBQTtJQW5CSkcsRUFBQSxJQUFDLEdBQUcsQ0FBZSxhQUFRLENBQVIsUUFBUSxDQUFZLFNBQUMsQ0FBRCxHQUFDLENBQ3RDLENBQUFOLEVBQTRCLENBQzNCLENBQUFHLEVBaUJBLENBQ0gsRUFwQkMsR0FBRyxDQW9CRTtJQUFBTixDQUFBLE1BQUFNLEVBQUE7SUFBQU4sQ0FBQSxNQUFBUyxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBVCxDQUFBO0VBQUE7RUFBQSxPQXBCTlMsRUFvQk07QUFBQTtBQXhCSCxTQUFBRCxNQUFBRSxVQUFBLEVBQUFDLENBQUE7RUFBQSxPQU9DLENBQUMsR0FBRyxDQUFNQSxHQUFDLENBQURBLEVBQUEsQ0FBQyxDQUFnQixhQUFRLENBQVIsUUFBUSxDQUFZLFNBQWUsQ0FBZixDQUFBQSxDQUFDLEtBQUssQ0FBUyxHQUFmLENBQWUsR0FBZixDQUFjLENBQUMsQ0FDNUQsQ0FBQyxHQUFHLENBQ0YsQ0FBQyxVQUFVLENBQVMsTUFBbUIsQ0FBbkIsQ0FBQUQsVUFBVSxDQUFBRSxRQUFRLENBQUMsQ0FBRSxTQUFTLENBQVQsS0FBUSxDQUFDLEdBQ2xELENBQUMsSUFBSSxDQUFDLElBQUksQ0FBSixLQUFHLENBQUMsQ0FBRSxDQUFBRixVQUFVLENBQUFHLEtBQUssQ0FBRSxFQUE1QixJQUFJLENBQ0osQ0FBQUgsVUFBVSxDQUFBSSxhQU1ILEdBTE4sQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFSLEtBQU8sQ0FBQyxDQUNYLElBQUUsQ0FDRixDQUFBekIsT0FBTyxDQUFBMEIsVUFBVSxDQUFFLE9BQ25CLENBQUFyQixZQUFZLENBQUNnQixVQUFVLENBQUFJLGFBQWMsRUFDeEMsRUFKQyxJQUFJLENBS0MsR0FOUCxJQU1NLENBQ1QsRUFWQyxHQUFHLENBV0osQ0FBQyxHQUFHLENBQWEsVUFBQyxDQUFELEdBQUMsQ0FDaEIsQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFSLEtBQU8sQ0FBQyxDQUFFLENBQUFKLFVBQVUsQ0FBQU0sTUFBTSxDQUFFLEVBQWpDLElBQUksQ0FDUCxFQUZDLEdBQUcsQ0FHTixFQWZDLEdBQUcsQ0FlRTtBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/ContextVisualization.tsx`

**信息:**
- 行数: 489
- 大小: 76073 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import * as React from 'react';
import { Box, Text } from '../ink.js';
import type { ContextData } from '../utils/analyzeContext.js';
import { generateContextSuggestions } from '../utils/contextSuggestions.js';
import { getDisplayPath } from '../utils/file.js';
import { formatTokens } from '../utils/format.js';
import { getSourceDisplayName, type SettingSource } from '../utils/settings/constants.js';
import { plural } from '../utils/stringUtils.js';
import { ContextSuggestions } from './ContextSuggestions.js';
const RESERVED_CATEGORY_NAME = 'Autocompact buffer';

/**
 * One-liner for the legend header showing what context-collapse has done.
 * Returns null when nothing's summarized/staged so we don't add visual
 * noise in the common case. This is the one place a user can see that
 * their context was rewritten — the <collapsed> placeholders are isMeta
 * and don't appear in the conversation view.
 */
function CollapseStatus() {
  const $ = _c(2);
  if (feature("CONTEXT_COLLAPSE")) {
    let t0;
    let t1;
    if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
      t1 = Symbol.for("react.early_return_sentinel");
      bb0: {
        const {
          getStats,
          isContextCollapseEnabled
        } = require("../services/contextCollapse/index.js") as typeof import('../services/contextCollapse/index.js');
        if (!isContextCollapseEnabled()) {
          t1 = null;
          break bb0;
        }
        const s = getStats();
        const {
          health: h
        } = s;
        const parts = [];
        if (s.collapsedSpans > 0) {
          parts.push(`${s.collapsedSpans} ${plural(s.collapsedSpans, "span")} summarized (${s.collapsedMessages} msgs)`);
        }
        if (s.stagedSpans > 0) {
          parts.push(`${s.stagedSpans} staged`);
        }
        const summary = parts.length > 0 ? parts.join(", ") : h.totalSpawns > 0 ? `${h.totalSpawns} ${plural(h.totalSpawns, "spawn")}, nothing staged yet` : "waiting for first trigger";
        let line2 = null;
        if (h.totalErrors > 0) {

```

---


### `src/components/CoordinatorAgentStatus.tsx`

**信息:**
- 行数: 273
- 大小: 36038 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * CoordinatorTaskPanel — Steerable list of background agents.
 *
 * Renders below the prompt input footer whenever local_agent tasks exist.
 * Visibility is driven by evictAfter: undefined (running/retained) shows
 * always; a timestamp shows until passed. Enter to view/steer, x to dismiss.
 */

import figures from 'figures';
import * as React from 'react';
import { BLACK_CIRCLE, PAUSE_ICON, PLAY_ICON } from '../constants/figures.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { stringWidth } from '../ink/stringWidth.js';
import { Box, Text, wrapText } from '../ink.js';
import { type AppState, useAppState, useSetAppState } from '../state/AppState.js';
import { enterTeammateView, exitTeammateView } from '../state/teammateViewHelpers.js';
import { isPanelAgentTask, type LocalAgentTaskState } from '../tasks/LocalAgentTask/LocalAgentTask.js';
import { formatDuration, formatNumber } from '../utils/format.js';
import { evictTerminalTask } from '../utils/task/framework.js';
import { isTerminalStatus } from './tasks/taskStatusUtils.js';

/**
 * Which panel-managed tasks currently have a visible row.
 * Presence in AppState.tasks IS visibility — the 1s tick in
 * CoordinatorTaskPanel evicts tasks past their evictAfter deadline. The
 * evictAfter !== 0 check handles immediate dismiss (x key) without making
 * the filter time-dependent. Shared by panel render, useCoordinatorTaskCount,
 * and index resolvers so the math can't drift.
 */
export function getVisibleAgentTasks(tasks: AppState['tasks']): LocalAgentTaskState[] {
  return Object.values(tasks).filter((t): t is LocalAgentTaskState => isPanelAgentTask(t) && t.evictAfter !== 0).sort((a, b) => a.startTime - b.startTime);
}
export function CoordinatorTaskPanel(): React.ReactNode {
  const tasks = useAppState(s => s.tasks);
  const viewingAgentTaskId = useAppState(s_0 => s_0.viewingAgentTaskId);
  const agentNameRegistry = useAppState(s_1 => s_1.agentNameRegistry);
  const coordinatorTaskIndex = useAppState(s_2 => s_2.coordinatorTaskIndex);
  const tasksSelected = useAppState(s_3 => s_3.footerSelection === 'tasks');
  const selectedIndex = tasksSelected ? coordinatorTaskIndex : undefined;
  const setAppState = useSetAppState();
  const visibleTasks = getVisibleAgentTasks(tasks);
  const hasTasks = Object.values(tasks).some(isPanelAgentTask);

  // 1s tick: re-render for elapsed time + evict tasks past their deadline.
  // The eviction deletes from prev.tasks, which makes useCoordinatorTaskCount
  // (and other consumers) see the updated count without their own tick.
  const tasksRef = React.useRef(tasks);
  tasksRef.current = tasks;
  const [, setTick] = React.useState(0);

```

---


### `src/components/CostThresholdDialog.tsx`

**信息:**
- 行数: 50
- 大小: 4336 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Link, Text } from '../ink.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
type Props = {
  onDone: () => void;
};
export function CostThresholdDialog(t0) {
  const $ = _c(7);
  const {
    onDone
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Box flexDirection="column"><Text>Learn more about how to monitor your spending:</Text><Link url="https://code.claude.com/docs/en/costs" /></Box>;
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  let t2;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = [{
      value: "ok",
      label: "Got it, thanks!"
    }];
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  let t3;
  if ($[2] !== onDone) {
    t3 = <Select options={t2} onChange={onDone} />;
    $[2] = onDone;
    $[3] = t3;
  } else {
    t3 = $[3];
  }
  let t4;
  if ($[4] !== onDone || $[5] !== t3) {
    t4 = <Dialog title="You've spent $5 on the Anthropic API this session." onCancel={onDone}>{t1}{t3}</Dialog>;
    $[4] = onDone;
    $[5] = t3;
    $[6] = t4;
  } else {
    t4 = $[6];
  }
  return t4;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJveCIsIkxpbmsiLCJUZXh0IiwiU2VsZWN0IiwiRGlhbG9nIiwiUHJvcHMiLCJvbkRvbmUiLCJDb3N0VGhyZXNob2xkRGlhbG9nIiwidDAiLCIkIiwiX2MiLCJ0MSIsIlN5bWJvbCIsImZvciIsInQyIiwidmFsdWUiLCJsYWJlbCIsInQzIiwidDQiXSwic291cmNlcyI6WyJDb3N0VGhyZXNob2xkRGlhbG9nLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBCb3gsIExpbmssIFRleHQgfSBmcm9tICcuLi9pbmsuanMnXG5pbXBvcnQgeyBTZWxlY3QgfSBmcm9tICcuL0N1c3RvbVNlbGVjdC9pbmRleC5qcydcbmltcG9ydCB7IERpYWxvZyB9IGZyb20gJy4vZGVzaWduLXN5c3RlbS9EaWFsb2cuanMnXG5cbnR5cGUgUHJvcHMgPSB7XG4gIG9uRG9uZTogKCkgPT4gdm9pZFxufVxuXG5leHBvcnQgZnVuY3Rpb24gQ29zdFRocmVzaG9sZERpYWxvZyh7IG9uRG9uZSB9OiBQcm9wcyk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIHJldHVybiAoXG4gICAgPERpYWxvZ1xuICAgICAgdGl0bGU9XCJZb3UndmUgc3BlbnQgJDUgb24gdGhlIEFudGhyb3BpYyBBUEkgdGhpcyBzZXNzaW9uLlwiXG4gICAgICBvbkNhbmNlbD17b25Eb25lfVxuICAgID5cbiAgICAgIDxCb3ggZmxleERpcmVjdGlvbj1cImNvbHVtblwiPlxuICAgICAgICA8VGV4dD5MZWFybiBtb3JlIGFib3V0IGhvdyB0byBtb25pdG9yIHlvdXIgc3BlbmRpbmc6PC9UZXh0PlxuICAgICAgICA8TGluayB1cmw9XCJodHRwczovL2NvZGUuY2xhdWRlLmNvbS9kb2NzL2VuL2Nvc3RzXCIgLz5cbiAgICAgIDwvQm94PlxuICAgICAgPFNlbGVjdFxuICAgICAgICBvcHRpb25zPXtbXG4gICAgICAgICAge1xuICAgICAgICAgICAgdmFsdWU6ICdvaycsXG4gICAgICAgICAgICBsYWJlbDogJ0dvdCBpdCwgdGhhbmtzIScsXG4gICAgICAgICAgfSxcbiAgICAgICAgXX1cbiAgICAgICAgb25DaGFuZ2U9e29uRG9uZX1cbiAgICAgIC8+XG4gICAgPC9EaWFsb2c+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU9BLEtBQUssTUFBTSxPQUFPO0FBQ3pCLFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxFQUFFQyxJQUFJLFFBQVEsV0FBVztBQUMzQyxTQUFTQyxNQUFNLFFBQVEseUJBQXlCO0FBQ2hELFNBQVNDLE1BQU0sUUFBUSwyQkFBMkI7QUFFbEQsS0FBS0MsS0FBSyxHQUFHO0VBQ1hDLE1BQU0sRUFBRSxHQUFHLEdBQUcsSUFBSTtBQUNwQixDQUFDO0FBRUQsT0FBTyxTQUFBQyxvQkFBQUMsRUFBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUE2QjtJQUFBSjtFQUFBLElBQUFFLEVBQWlCO0VBQUEsSUFBQUcsRUFBQTtFQUFBLElBQUFGLENBQUEsUUFBQUcsTUFBQSxDQUFBQyxHQUFBO0lBTS9DRixFQUFBLElBQUMsR0FBRyxDQUFlLGFBQVEsQ0FBUixRQUFRLENBQ3pCLENBQUMsSUFBSSxDQUFDLDhDQUE4QyxFQUFuRCxJQUFJLENBQ0wsQ0FBQyxJQUFJLENBQUssR0FBdUMsQ0FBdkMsdUNBQXVDLEdBQ25ELEVBSEMsR0FBRyxDQUdFO0lBQUFGLENBQUEsTUFBQUUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUYsQ0FBQTtFQUFBO0VBQUEsSUFBQUssRUFBQTtFQUFBLElBQUFMLENBQUEsUUFBQUcsTUFBQSxDQUFBQyxHQUFBO0lBRUtDLEVBQUEsSUFDUDtNQUFBQyxLQUFBLEVBQ1MsSUFBSTtNQUFBQyxLQUFBLEVBQ0o7SUFDVCxDQUFDLENBQ0Y7SUFBQVAsQ0FBQSxNQUFBSyxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBTCxDQUFBO0VBQUE7RUFBQSxJQUFBUSxFQUFBO0VBQUEsSUFBQVIsQ0FBQSxRQUFBSCxNQUFBO0lBTkhXLEVBQUEsSUFBQyxNQUFNLENBQ0ksT0FLUixDQUxRLENBQUFILEVBS1QsQ0FBQyxDQUNTUixRQUFNLENBQU5BLE9BQUssQ0FBQyxHQUNoQjtJQUFBRyxDQUFBLE1BQUFILE1BQUE7SUFBQUcsQ0FBQSxNQUFBUSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBUixDQUFBO0VBQUE7RUFBQSxJQUFBUyxFQUFBO0VBQUEsSUFBQVQsQ0FBQSxRQUFBSCxNQUFBLElBQUFHLENBQUEsUUFBQVEsRUFBQTtJQWhCSkMsRUFBQSxJQUFDLE1BQU0sQ0FDQyxLQUFvRCxDQUFwRCxvREFBb0QsQ0FDaERaLFFBQU0sQ0FBTkEsT0FBSyxDQUFDLENBRWhCLENBQUFLLEVBR0ssQ0FDTCxDQUFBTSxFQVFDLENBQ0gsRUFqQkMsTUFBTSxDQWlCRTtJQUFBUixDQUFBLE1BQUFILE1BQUE7SUFBQUcsQ0FBQSxNQUFBUSxFQUFBO0lBQUFSLENBQUEsTUFBQVMsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQVQsQ0FBQTtFQUFBO0VBQUEsT0FqQlRTLEVBaUJTO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/components/CtrlOToExpand.tsx`

**信息:**
- 行数: 51
- 大小: 6062 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import React, { useContext } from 'react';
import { Text } from '../ink.js';
import { getShortcutDisplay } from '../keybindings/shortcutFormat.js';
import { useShortcutDisplay } from '../keybindings/useShortcutDisplay.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import { InVirtualListContext } from './messageActions.js';

// Context to track if we're inside a sub agent
// Similar to MessageResponseContext, this helps us avoid showing
// too many "(ctrl+o to expand)" hints in sub agent output
const SubAgentContext = React.createContext(false);
export function SubAgentProvider(t0) {
  const $ = _c(2);
  const {
    children
  } = t0;
  let t1;
  if ($[0] !== children) {
    t1 = <SubAgentContext.Provider value={true}>{children}</SubAgentContext.Provider>;
    $[0] = children;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  return t1;
}
export function CtrlOToExpand() {
  const $ = _c(2);
  const isInSubAgent = useContext(SubAgentContext);
  const inVirtualList = useContext(InVirtualListContext);
  const expandShortcut = useShortcutDisplay("app:toggleTranscript", "Global", "ctrl+o");
  if (isInSubAgent || inVirtualList) {
    return null;
  }
  let t0;
  if ($[0] !== expandShortcut) {
    t0 = <Text dimColor={true}><KeyboardShortcutHint shortcut={expandShortcut} action="expand" parens={true} /></Text>;
    $[0] = expandShortcut;
    $[1] = t0;
  } else {
    t0 = $[1];
  }
  return t0;
}
export function ctrlOToExpand(): string {
  const shortcut = getShortcutDisplay('app:toggleTranscript', 'Global', 'ctrl+o');
  return chalk.dim(`(${shortcut} to expand)`);
}

```

---


### `src/components/CustomSelect/SelectMulti.tsx`

**信息:**
- 行数: 213
- 大小: 29884 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React from 'react';
import { Box, Text } from '../../ink.js';
import type { PastedContent } from '../../utils/config.js';
import type { ImageDimensions } from '../../utils/imageResizer.js';
import type { OptionWithDescription } from './select.js';
import { SelectInputOption } from './select-input-option.js';
import { SelectOption } from './select-option.js';
import { useMultiSelectState } from './use-multi-select-state.js';
export type SelectMultiProps<T> = {
  readonly isDisabled?: boolean;
  readonly visibleOptionCount?: number;
  readonly options: OptionWithDescription<T>[];
  readonly defaultValue?: T[];
  readonly onCancel: () => void;
  readonly onChange?: (values: T[]) => void;
  readonly onFocus?: (value: T) => void;
  readonly focusValue?: T;
  /**
   * Text for the submit button. When provided, a submit button is shown and
   * Enter toggles selection (submit only fires when the button is focused).
   * When omitted, Enter submits directly and Space toggles selection.
   */
  readonly submitButtonText?: string;
  /**
   * Callback when user submits. Receives the currently selected values.
   */
  readonly onSubmit?: (values: T[]) => void;
  /**
   * When true, hides the numeric indexes next to each option.
   */
  readonly hideIndexes?: boolean;
  /**
   * Callback when user presses down from the last item (submit button).
   * If provided, navigation will not wrap to the first item.
   */
  readonly onDownFromLastItem?: () => void;
  /**
   * Callback when user presses up from the first item.
   * If provided, navigation will not wrap to the last item.
   */
  readonly onUpFromFirstItem?: () => void;
  /**
   * Focus the last option initially instead of the first.
   */
  readonly initialFocusLast?: boolean;
  /**
   * Callback to open external editor for editing input option values.
   * When provided, ctrl+g will trigger this callback in input options

```

---


### `src/components/CustomSelect/index.ts`

**信息:**
- 行数: 3
- 大小: 118 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export * from './SelectMulti.js'
export type { OptionWithDescription } from './select.js'
export * from './select.js'

```

---


### `src/components/CustomSelect/option-map.ts`

**信息:**
- 行数: 50
- 大小: 1189 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ReactNode } from 'react'
import type { OptionWithDescription } from './select.js'

type OptionMapItem<T> = {
  label: ReactNode
  value: T
  description?: string
  previous: OptionMapItem<T> | undefined
  next: OptionMapItem<T> | undefined
  index: number
}

export default class OptionMap<T> extends Map<T, OptionMapItem<T>> {
  readonly first: OptionMapItem<T> | undefined
  readonly last: OptionMapItem<T> | undefined

  constructor(options: OptionWithDescription<T>[]) {
    const items: Array<[T, OptionMapItem<T>]> = []
    let firstItem: OptionMapItem<T> | undefined
    let lastItem: OptionMapItem<T> | undefined
    let previous: OptionMapItem<T> | undefined
    let index = 0

    for (const option of options) {
      const item = {
        label: option.label,
        value: option.value,
        description: option.description,
        previous,
        next: undefined,
        index,
      }

      if (previous) {
        previous.next = item
      }

      firstItem ||= item
      lastItem = item

      items.push([option.value, item])
      index++
      previous = item
    }

    super(items)
    this.first = firstItem
    this.last = lastItem
  }
}

```

---


### `src/components/CustomSelect/select-input-option.tsx`

**信息:**
- 行数: 488
- 大小: 58172 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode, useEffect, useRef, useState } from 'react';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- UP arrow exit not in Attachments bindings
import { Box, Text, useInput } from '../../ink.js';
import { useKeybinding, useKeybindings } from '../../keybindings/useKeybinding.js';
import type { PastedContent } from '../../utils/config.js';
import { getImageFromClipboard } from '../../utils/imagePaste.js';
import type { ImageDimensions } from '../../utils/imageResizer.js';
import { ClickableImageRef } from '../ClickableImageRef.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Byline } from '../design-system/Byline.js';
import TextInput from '../TextInput.js';
import type { OptionWithDescription } from './select.js';
import { SelectOption } from './select-option.js';
type Props<T> = {
  option: Extract<OptionWithDescription<T>, {
    type: 'input';
  }>;
  isFocused: boolean;
  isSelected: boolean;
  shouldShowDownArrow: boolean;
  shouldShowUpArrow: boolean;
  maxIndexWidth: number;
  index: number;
  inputValue: string;
  onInputChange: (value: string) => void;
  onSubmit: (value: string) => void;
  onExit?: () => void;
  layout: 'compact' | 'expanded';
  children?: ReactNode;
  /**
   * When true, shows the label before the input field.
   * When false (default), uses the label as the placeholder.
   */
  showLabel?: boolean;
  /**
   * Callback to open external editor for editing the input value.
   * When provided, ctrl+g will trigger this callback with the current value
   * and a setter function to update the internal state.
   */
  onOpenEditor?: (currentValue: string, setValue: (value: string) => void) => void;
  /**
   * When true, automatically reset cursor to end of line when:
   * - Option becomes focused
   * - Input value changes
   * This prevents cursor position bugs when the input value updates asynchronously.
   */
  resetCursorOnUpdate?: boolean;
  /**
   * Optional callback when an image is pasted into the input.

```

---


### `src/components/CustomSelect/select-option.tsx`

**信息:**
- 行数: 68
- 大小: 5793 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode } from 'react';
import { ListItem } from '../design-system/ListItem.js';
export type SelectOptionProps = {
  /**
   * Determines if option is focused.
   */
  readonly isFocused: boolean;

  /**
   * Determines if option is selected.
   */
  readonly isSelected: boolean;

  /**
   * Option label.
   */
  readonly children: ReactNode;

  /**
   * Optional description to display below the label.
   */
  readonly description?: string;

  /**
   * Determines if the down arrow should be shown.
   */
  readonly shouldShowDownArrow?: boolean;

  /**
   * Determines if the up arrow should be shown.
   */
  readonly shouldShowUpArrow?: boolean;

  /**
   * Whether ListItem should declare the terminal cursor position.
   * Set false when a child declares its own cursor (e.g. BaseTextInput).
   */
  readonly declareCursor?: boolean;
};
export function SelectOption(t0) {
  const $ = _c(8);
  const {
    isFocused,
    isSelected,
    children,
    description,
    shouldShowDownArrow,
    shouldShowUpArrow,
    declareCursor

```

---


### `src/components/CustomSelect/select.tsx`

**信息:**
- 行数: 690
- 大小: 115187 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { type ReactNode, useEffect, useRef, useState } from 'react';
import { useDeclaredCursor } from '../../ink/hooks/use-declared-cursor.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { Ansi, Box, Text } from '../../ink.js';
import { count } from '../../utils/array.js';
import type { PastedContent } from '../../utils/config.js';
import type { ImageDimensions } from '../../utils/imageResizer.js';
import { SelectInputOption } from './select-input-option.js';
import { SelectOption } from './select-option.js';
import { useSelectInput } from './use-select-input.js';
import { useSelectState } from './use-select-state.js';

// Extract text content from ReactNode for width calculation
function getTextContent(node: ReactNode): string {
  if (typeof node === 'string') return node;
  if (typeof node === 'number') return String(node);
  if (!node) return '';
  if (Array.isArray(node)) return node.map(getTextContent).join('');
  if (React.isValidElement<{
    children?: ReactNode;
  }>(node)) {
    return getTextContent(node.props.children);
  }
  return '';
}
type BaseOption<T> = {
  description?: string;
  dimDescription?: boolean;
  label: ReactNode;
  value: T;
  disabled?: boolean;
};
export type OptionWithDescription<T = string> = (BaseOption<T> & {
  type?: 'text';
}) | (BaseOption<T> & {
  type: 'input';
  onChange: (value: string) => void;
  placeholder?: string;
  initialValue?: string;
  /**
   * Controls behavior when submitting with empty input:
   * - true: calls onChange (treats empty as valid submission)
   * - false (default): calls onCancel (treats empty as cancellation)
   *
   * Also affects initial Enter press: when true, submits immediately;
   * when false, enters input mode first so user can type.
   */
  allowEmptySubmitToCancel?: boolean;

```

---


### `src/components/CustomSelect/use-multi-select-state.ts`

**信息:**
- 行数: 414
- 大小: 10952 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useState } from 'react'
import { isDeepStrictEqual } from 'util'
import { useRegisterOverlay } from '../../context/overlayContext.js'
import type { InputEvent } from '../../ink/events/input-event.js'
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- raw space/arrow multiselect input
import { useInput } from '../../ink.js'
import {
  normalizeFullWidthDigits,
  normalizeFullWidthSpace,
} from '../../utils/stringUtils.js'
import type { OptionWithDescription } from './select.js'
import { useSelectNavigation } from './use-select-navigation.js'

export type UseMultiSelectStateProps<T> = {
  /**
   * When disabled, user input is ignored.
   *
   * @default false
   */
  isDisabled?: boolean

  /**
   * Number of items to display.
   *
   * @default 5
   */
  visibleOptionCount?: number

  /**
   * Options.
   */
  options: OptionWithDescription<T>[]

  /**
   * Initially selected values.
   */
  defaultValue?: T[]

  /**
   * Callback when selection changes.
   */
  onChange?: (values: T[]) => void

  /**
   * Callback for canceling the select.
   */
  onCancel: () => void

  /**
   * Callback for focusing an option.

```

---


### `src/components/CustomSelect/use-select-input.ts`

**信息:**
- 行数: 287
- 大小: 8770 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useMemo } from 'react'
import { useRegisterOverlay } from '../../context/overlayContext.js'
import type { InputEvent } from '../../ink/events/input-event.js'
import { useInput } from '../../ink.js'
import { useKeybindings } from '../../keybindings/useKeybinding.js'
import {
  normalizeFullWidthDigits,
  normalizeFullWidthSpace,
} from '../../utils/stringUtils.js'
import type { OptionWithDescription } from './select.js'
import type { SelectState } from './use-select-state.js'

export type UseSelectProps<T> = {
  /**
   * When disabled, user input is ignored.
   *
   * @default false
   */
  isDisabled?: boolean

  /**
   * When true, prevents selection on Enter or number keys, but allows
   * scrolling.
   * When 'numeric', prevents selection on number keys, but allows Enter (and
   * scrolling).
   *
   * @default false
   */
  readonly disableSelection?: boolean | 'numeric'

  /**
   * Select state.
   */
  state: SelectState<T>

  /**
   * Options.
   */
  options: OptionWithDescription<T>[]

  /**
   * Whether this is a multi-select component.
   *
   * @default false
   */
  isMultiSelect?: boolean

  /**
   * Callback when user presses up from the first item.
   * If provided, navigation will not wrap to the last item.

```

---


### `src/components/CustomSelect/use-select-navigation.ts`

**信息:**
- 行数: 653
- 大小: 16388 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  useCallback,
  useEffect,
  useMemo,
  useReducer,
  useRef,
  useState,
} from 'react'
import { isDeepStrictEqual } from 'util'
import OptionMap from './option-map.js'
import type { OptionWithDescription } from './select.js'

type State<T> = {
  /**
   * Map where key is option's value and value is option's index.
   */
  optionMap: OptionMap<T>

  /**
   * Number of visible options.
   */
  visibleOptionCount: number

  /**
   * Value of the currently focused option.
   */
  focusedValue: T | undefined

  /**
   * Index of the first visible option.
   */
  visibleFromIndex: number

  /**
   * Index of the last visible option.
   */
  visibleToIndex: number
}

type Action<T> =
  | FocusNextOptionAction
  | FocusPreviousOptionAction
  | FocusNextPageAction
  | FocusPreviousPageAction
  | SetFocusAction<T>
  | ResetAction<T>

type SetFocusAction<T> = {
  type: 'set-focus'
  value: T

```

---


### `src/components/CustomSelect/use-select-state.ts`

**信息:**
- 行数: 157
- 大小: 2859 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useState } from 'react'
import type { OptionWithDescription } from './select.js'
import { useSelectNavigation } from './use-select-navigation.js'

export type UseSelectStateProps<T> = {
  /**
   * Number of items to display.
   *
   * @default 5
   */
  visibleOptionCount?: number

  /**
   * Options.
   */
  options: OptionWithDescription<T>[]

  /**
   * Initially selected option's value.
   */
  defaultValue?: T

  /**
   * Callback for selecting an option.
   */
  onChange?: (value: T) => void

  /**
   * Callback for canceling the select.
   */
  onCancel?: () => void

  /**
   * Callback for focusing an option.
   */
  onFocus?: (value: T) => void

  /**
   * Value to focus
   */
  focusValue?: T
}

export type SelectState<T> = {
  /**
   * Value of the currently focused option.
   */
  focusedValue: T | undefined

  /**

```

---


### `src/components/DesktopHandoff.tsx`

**信息:**
- 行数: 193
- 大小: 19335 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useEffect, useState } from 'react';
import type { CommandResultDisplay } from '../commands.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- raw input for "any key" dismiss and y/n prompt
import { Box, Text, useInput } from '../ink.js';
import { openBrowser } from '../utils/browser.js';
import { getDesktopInstallStatus, openCurrentSessionInDesktop } from '../utils/desktopDeepLink.js';
import { errorMessage } from '../utils/errors.js';
import { gracefulShutdown } from '../utils/gracefulShutdown.js';
import { flushSessionStorage } from '../utils/sessionStorage.js';
import { LoadingState } from './design-system/LoadingState.js';
const DESKTOP_DOCS_URL = 'https://clau.de/desktop';
export function getDownloadUrl(): string {
  switch (process.platform) {
    case 'win32':
      return 'https://claude.ai/api/desktop/win32/x64/exe/latest/redirect';
    default:
      return 'https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect';
  }
}
type DesktopHandoffState = 'checking' | 'prompt-download' | 'flushing' | 'opening' | 'success' | 'error';
type Props = {
  onDone: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
export function DesktopHandoff(t0) {
  const $ = _c(20);
  const {
    onDone
  } = t0;
  const [state, setState] = useState("checking");
  const [error, setError] = useState(null);
  const [downloadMessage, setDownloadMessage] = useState("");
  let t1;
  if ($[0] !== error || $[1] !== onDone || $[2] !== state) {
    t1 = input => {
      if (state === "error") {
        onDone(error ?? "Unknown error", {
          display: "system"
        });
        return;
      }
      if (state === "prompt-download") {
        if (input === "y" || input === "Y") {
          openBrowser(getDownloadUrl()).catch(_temp);
          onDone(`Starting download. Re-run /desktop once you\u2019ve installed the app.\nLearn more at ${DESKTOP_DOCS_URL}`, {
            display: "system"
          });
        } else {

```

---


### `src/components/DesktopUpsell/DesktopUpsellStartup.tsx`

**信息:**
- 行数: 171
- 大小: 15520 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useEffect, useState } from 'react';
import { Box, Text } from '../../ink.js';
import { getDynamicConfig_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js';
import { logEvent } from '../../services/analytics/index.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { Select } from '../CustomSelect/select.js';
import { DesktopHandoff } from '../DesktopHandoff.js';
import { PermissionDialog } from '../permissions/PermissionDialog.js';
type DesktopUpsellConfig = {
  enable_shortcut_tip: boolean;
  enable_startup_dialog: boolean;
};
const DESKTOP_UPSELL_DEFAULT: DesktopUpsellConfig = {
  enable_shortcut_tip: false,
  enable_startup_dialog: false
};
export function getDesktopUpsellConfig(): DesktopUpsellConfig {
  return getDynamicConfig_CACHED_MAY_BE_STALE('tengu_desktop_upsell', DESKTOP_UPSELL_DEFAULT);
}
function isSupportedPlatform(): boolean {
  return process.platform === 'darwin' || process.platform === 'win32' && process.arch === 'x64';
}
export function shouldShowDesktopUpsellStartup(): boolean {
  if (!isSupportedPlatform()) return false;
  if (!getDesktopUpsellConfig().enable_startup_dialog) return false;
  const config = getGlobalConfig();
  if (config.desktopUpsellDismissed) return false;
  if ((config.desktopUpsellSeenCount ?? 0) >= 3) return false;
  return true;
}
type DesktopUpsellSelection = 'try' | 'not-now' | 'never';
type Props = {
  onDone: () => void;
};
export function DesktopUpsellStartup(t0) {
  const $ = _c(14);
  const {
    onDone
  } = t0;
  const [showHandoff, setShowHandoff] = useState(false);
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = [];
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  useEffect(_temp, t1);

```

---


### `src/components/DevBar.tsx`

**信息:**
- 行数: 49
- 大小: 5040 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useState } from 'react';
import { getSlowOperations } from '../bootstrap/state.js';
import { Text, useInterval } from '../ink.js';

// Show DevBar for dev builds or all ants
function shouldShowDevBar(): boolean {
  return "production" === 'development' || "external" === 'ant';
}
export function DevBar() {
  const $ = _c(5);
  const [slowOps, setSlowOps] = useState(getSlowOperations);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = () => {
      setSlowOps(getSlowOperations());
    };
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  useInterval(t0, shouldShowDevBar() ? 500 : null);
  if (!shouldShowDevBar() || slowOps.length === 0) {
    return null;
  }
  let t1;
  if ($[1] !== slowOps) {
    t1 = slowOps.slice(-3).map(_temp).join(" \xB7 ");
    $[1] = slowOps;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  const recentOps = t1;
  let t2;
  if ($[3] !== recentOps) {
    t2 = <Text wrap="truncate-end" color="warning">[ANT-ONLY] slow sync: {recentOps}</Text>;
    $[3] = recentOps;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  return t2;
}
function _temp(op) {
  return `${op.operation} (${Math.round(op.durationMs)}ms)`;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsInVzZVN0YXRlIiwiZ2V0U2xvd09wZXJhdGlvbnMiLCJUZXh0IiwidXNlSW50ZXJ2YWwiLCJzaG91bGRTaG93RGV2QmFyIiwiRGV2QmFyIiwiJCIsIl9jIiwic2xvd09wcyIsInNldFNsb3dPcHMiLCJ0MCIsIlN5bWJvbCIsImZvciIsImxlbmd0aCIsInQxIiwic2xpY2UiLCJtYXAiLCJfdGVtcCIsImpvaW4iLCJyZWNlbnRPcHMiLCJ0MiIsIm9wIiwib3BlcmF0aW9uIiwiTWF0aCIsInJvdW5kIiwiZHVyYXRpb25NcyJdLCJzb3VyY2VzIjpbIkRldkJhci50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyB1c2VTdGF0ZSB9IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgZ2V0U2xvd09wZXJhdGlvbnMgfSBmcm9tICcuLi9ib290c3RyYXAvc3RhdGUuanMnXG5pbXBvcnQgeyBUZXh0LCB1c2VJbnRlcnZhbCB9IGZyb20gJy4uL2luay5qcydcblxuLy8gU2hvdyBEZXZCYXIgZm9yIGRldiBidWlsZHMgb3IgYWxsIGFudHNcbmZ1bmN0aW9uIHNob3VsZFNob3dEZXZCYXIoKTogYm9vbGVhbiB7XG4gIHJldHVybiAoXG4gICAgXCJwcm9kdWN0aW9uXCIgPT09ICdkZXZlbG9wbWVudCcgfHwgXCJleHRlcm5hbFwiID09PSAnYW50J1xuICApXG59XG5cbmV4cG9ydCBmdW5jdGlvbiBEZXZCYXIoKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgY29uc3QgW3Nsb3dPcHMsIHNldFNsb3dPcHNdID1cbiAgICB1c2VTdGF0ZTxcbiAgICAgIFJlYWRvbmx5QXJyYXk8e1xuICAgICAgICBvcGVyYXRpb246IHN0cmluZ1xuICAgICAgICBkdXJhdGlvbk1zOiBudW1iZXJcbiAgICAgICAgdGltZXN0YW1wOiBudW1iZXJcbiAgICAgIH0+XG4gICAgPihnZXRTbG93T3BlcmF0aW9ucylcblxuICB1c2VJbnRlcnZhbChcbiAgICAoKSA9PiB7XG4gICAgICBzZXRTbG93T3BzKGdldFNsb3dPcGVyYXRpb25zKCkpXG4gICAgfSxcbiAgICBzaG91bGRTaG93RGV2QmFyKCkgPyA1MDAgOiBudWxsLFxuICApXG5cbiAgLy8gT25seSBzaG93IHdoZW4gdGhlcmUncyBzb21ldGhpbmcgdG8gZGlzcGxheVxuICBpZiAoIXNob3VsZFNob3dEZXZCYXIoKSB8fCBzbG93T3BzLmxlbmd0aCA9PT0gMCkge1xuICAgIHJldHVybiBudWxsXG4gIH1cblxuICAvLyBTaW5nbGUtbGluZSBmb3JtYXQgc28gc2hvcnQgdGVybWluYWxzIGRvbid0IGxvc2Ugcm93cyB0byBkZXYgbm9pc2UuXG4gIGNvbnN0IHJlY2VudE9wcyA9IHNsb3dPcHNcbiAgICAuc2xpY2UoLTMpXG4gICAgLm1hcChvcCA9PiBgJHtvcC5vcGVyYXRpb259ICgke01hdGgucm91bmQob3AuZHVyYXRpb25Ncyl9bXMpYClcbiAgICAuam9pbignIMK3ICcpXG5cbiAgcmV0dXJuIChcbiAgICA8VGV4dCB3cmFwPVwidHJ1bmNhdGUtZW5kXCIgY29sb3I9XCJ3YXJuaW5nXCI+XG4gICAgICBbQU5ULU9OTFldIHNsb3cgc3luYzoge3JlY2VudE9wc31cbiAgICA8L1RleHQ+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsUUFBUSxRQUFRLE9BQU87QUFDaEMsU0FBU0MsaUJBQWlCLFFBQVEsdUJBQXVCO0FBQ3pELFNBQVNDLElBQUksRUFBRUMsV0FBVyxRQUFRLFdBQVc7O0FBRTdDO0FBQ0EsU0FBU0MsZ0JBQWdCQSxDQUFBLENBQUUsRUFBRSxPQUFPLENBQUM7RUFDbkMsT0FDRSxZQUFZLEtBQUssYUFBYSxJQUFJLFVBQVUsS0FBSyxLQUFLO0FBRTFEO0FBRUEsT0FBTyxTQUFBQyxPQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQ0wsT0FBQUMsT0FBQSxFQUFBQyxVQUFBLElBQ0VULFFBQVEsQ0FNTkMsaUJBQWlCLENBQUM7RUFBQSxJQUFBUyxFQUFBO0VBQUEsSUFBQUosQ0FBQSxRQUFBSyxNQUFBLENBQUFDLEdBQUE7SUFHcEJGLEVBQUEsR0FBQUEsQ0FBQTtNQUNFRCxVQUFVLENBQUNSLGlCQUFpQixDQUFDLENBQUMsQ0FBQztJQUFBLENBQ2hDO0lBQUFLLENBQUEsTUFBQUksRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUosQ0FBQTtFQUFBO0VBSEhILFdBQVcsQ0FDVE8sRUFFQyxFQUNETixnQkFBZ0IsQ0FBYyxDQUFDLEdBQS9CLEdBQStCLEdBQS9CLElBQ0YsQ0FBQztFQUdELElBQUksQ0FBQ0EsZ0JBQWdCLENBQUMsQ0FBeUIsSUFBcEJJLE9BQU8sQ0FBQUssTUFBTyxLQUFLLENBQUM7SUFBQSxPQUN0QyxJQUFJO0VBQUE7RUFDWixJQUFBQyxFQUFBO0VBQUEsSUFBQVIsQ0FBQSxRQUFBRSxPQUFBO0lBR2lCTSxFQUFBLEdBQUFOLE9BQU8sQ0FBQU8sS0FDakIsQ0FBQyxFQUFFLENBQUMsQ0FBQUMsR0FDTixDQUFDQyxLQUF3RCxDQUFDLENBQUFDLElBQ3pELENBQUMsUUFBSyxDQUFDO0lBQUFaLENBQUEsTUFBQUUsT0FBQTtJQUFBRixDQUFBLE1BQUFRLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFSLENBQUE7RUFBQTtFQUhkLE1BQUFhLFNBQUEsR0FBa0JMLEVBR0o7RUFBQSxJQUFBTSxFQUFBO0VBQUEsSUFBQWQsQ0FBQSxRQUFBYSxTQUFBO0lBR1pDLEVBQUEsSUFBQyxJQUFJLENBQU0sSUFBYyxDQUFkLGNBQWMsQ0FBTyxLQUFTLENBQVQsU0FBUyxDQUFDLHNCQUNqQkQsVUFBUSxDQUNqQyxFQUZDLElBQUksQ0FFRTtJQUFBYixDQUFBLE1BQUFhLFNBQUE7SUFBQWIsQ0FBQSxNQUFBYyxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBZCxDQUFBO0VBQUE7RUFBQSxPQUZQYyxFQUVPO0FBQUE7QUEvQkosU0FBQUgsTUFBQUksRUFBQTtFQUFBLE9BeUJRLEdBQUdBLEVBQUUsQ0FBQUMsU0FBVSxLQUFLQyxJQUFJLENBQUFDLEtBQU0sQ0FBQ0gsRUFBRSxDQUFBSSxVQUFXLENBQUMsS0FBSztBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/DevChannelsDialog.tsx`

**信息:**
- 行数: 105
- 大小: 9113 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback } from 'react';
import type { ChannelEntry } from '../bootstrap/state.js';
import { Box, Text } from '../ink.js';
import { gracefulShutdownSync } from '../utils/gracefulShutdown.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
type Props = {
  channels: ChannelEntry[];
  onAccept(): void;
};
export function DevChannelsDialog(t0) {
  const $ = _c(14);
  const {
    channels,
    onAccept
  } = t0;
  let t1;
  if ($[0] !== onAccept) {
    t1 = function onChange(value) {
      bb2: switch (value) {
        case "accept":
          {
            onAccept();
            break bb2;
          }
        case "exit":
          {
            gracefulShutdownSync(1);
          }
      }
    };
    $[0] = onAccept;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const onChange = t1;
  const handleEscape = _temp;
  let t2;
  let t3;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Text>--dangerously-load-development-channels is for local channel development only. Do not use this option to run channels you have downloaded off the internet.</Text>;
    t3 = <Text>Please use --channels to run a list of approved channels.</Text>;
    $[2] = t2;
    $[3] = t3;
  } else {
    t2 = $[2];
    t3 = $[3];
  }

```

---


### `src/components/DiagnosticsDisplay.tsx`

**信息:**
- 行数: 95
- 大小: 13220 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { relative } from 'path';
import React from 'react';
import { Box, Text } from '../ink.js';
import { DiagnosticTrackingService } from '../services/diagnosticTracking.js';
import type { Attachment } from '../utils/attachments.js';
import { getCwd } from '../utils/cwd.js';
import { CtrlOToExpand } from './CtrlOToExpand.js';
import { MessageResponse } from './MessageResponse.js';
type DiagnosticsAttachment = Extract<Attachment, {
  type: 'diagnostics';
}>;
type DiagnosticsDisplayProps = {
  attachment: DiagnosticsAttachment;
  verbose: boolean;
};
export function DiagnosticsDisplay(t0) {
  const $ = _c(14);
  const {
    attachment,
    verbose
  } = t0;
  if (attachment.files.length === 0) {
    return null;
  }
  let t1;
  if ($[0] !== attachment.files) {
    t1 = attachment.files.reduce(_temp, 0);
    $[0] = attachment.files;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const totalIssues = t1;
  const fileCount = attachment.files.length;
  if (verbose) {
    let t2;
    if ($[2] !== attachment.files) {
      t2 = attachment.files.map(_temp3);
      $[2] = attachment.files;
      $[3] = t2;
    } else {
      t2 = $[3];
    }
    let t3;
    if ($[4] !== t2) {
      t3 = <Box flexDirection="column">{t2}</Box>;
      $[4] = t2;
      $[5] = t3;
    } else {

```

---


### `src/components/EffortCallout.tsx`

**信息:**
- 行数: 265
- 大小: 24778 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useEffect, useRef } from 'react';
import { Box, Text } from '../ink.js';
import { isMaxSubscriber, isProSubscriber, isTeamSubscriber } from '../utils/auth.js';
import { getGlobalConfig, saveGlobalConfig } from '../utils/config.js';
import type { EffortLevel } from '../utils/effort.js';
import { convertEffortValueToLevel, getDefaultEffortForModel, getOpusDefaultEffortConfig, toPersistableEffort } from '../utils/effort.js';
import { parseUserSpecifiedModel } from '../utils/model/model.js';
import { updateSettingsForSource } from '../utils/settings/settings.js';
import type { OptionWithDescription } from './CustomSelect/select.js';
import { Select } from './CustomSelect/select.js';
import { effortLevelToSymbol } from './EffortIndicator.js';
import { PermissionDialog } from './permissions/PermissionDialog.js';
type EffortCalloutSelection = EffortLevel | undefined | 'dismiss';
type Props = {
  model: string;
  onDone: (selection: EffortCalloutSelection) => void;
};
const AUTO_DISMISS_MS = 30_000;
export function EffortCallout(t0) {
  const $ = _c(18);
  const {
    model,
    onDone
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = getOpusDefaultEffortConfig();
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const defaultEffortConfig = t1;
  const onDoneRef = useRef(onDone);
  let t2;
  if ($[1] !== onDone) {
    t2 = () => {
      onDoneRef.current = onDone;
    };
    $[1] = onDone;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  useEffect(t2);
  let t3;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = () => {
      onDoneRef.current("dismiss");
    };

```

---


### `src/components/EffortIndicator.ts`

**信息:**
- 行数: 42
- 大小: 1128 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  EFFORT_HIGH,
  EFFORT_LOW,
  EFFORT_MAX,
  EFFORT_MEDIUM,
} from '../constants/figures.js'
import {
  type EffortLevel,
  type EffortValue,
  getDisplayedEffortLevel,
  modelSupportsEffort,
} from '../utils/effort.js'

/**
 * Build the text for the effort-changed notification, e.g. "◐ medium · /effort".
 * Returns undefined if the model doesn't support effort.
 */
export function getEffortNotificationText(
  effortValue: EffortValue | undefined,
  model: string,
): string | undefined {
  if (!modelSupportsEffort(model)) return undefined
  const level = getDisplayedEffortLevel(model, effortValue)
  return `${effortLevelToSymbol(level)} ${level} · /effort`
}

export function effortLevelToSymbol(level: EffortLevel): string {
  switch (level) {
    case 'low':
      return EFFORT_LOW
    case 'medium':
      return EFFORT_MEDIUM
    case 'high':
      return EFFORT_HIGH
    case 'max':
      return EFFORT_MAX
    default:
      // Defensive: level can originate from remote config. If an unknown
      // value slips through, render the high symbol rather than undefined.
      return EFFORT_HIGH
  }
}

```

---


### `src/components/ExitFlow.tsx`

**信息:**
- 行数: 48
- 大小: 4364 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import sample from 'lodash-es/sample.js';
import React from 'react';
import { gracefulShutdown } from '../utils/gracefulShutdown.js';
import { WorktreeExitDialog } from './WorktreeExitDialog.js';
const GOODBYE_MESSAGES = ['Goodbye!', 'See ya!', 'Bye!', 'Catch you later!'];
function getRandomGoodbyeMessage(): string {
  return sample(GOODBYE_MESSAGES) ?? 'Goodbye!';
}
type Props = {
  onDone: (message?: string) => void;
  onCancel?: () => void;
  showWorktree: boolean;
};
export function ExitFlow(t0) {
  const $ = _c(5);
  const {
    showWorktree,
    onDone,
    onCancel
  } = t0;
  let t1;
  if ($[0] !== onDone) {
    t1 = async function onExit(resultMessage) {
      onDone(resultMessage ?? getRandomGoodbyeMessage());
      await gracefulShutdown(0, "prompt_input_exit");
    };
    $[0] = onDone;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const onExit = t1;
  if (showWorktree) {
    let t2;
    if ($[2] !== onCancel || $[3] !== onExit) {
      t2 = <WorktreeExitDialog onDone={onExit} onCancel={onCancel} />;
      $[2] = onCancel;
      $[3] = onExit;
      $[4] = t2;
    } else {
      t2 = $[4];
    }
    return t2;
  }
  return null;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJzYW1wbGUiLCJSZWFjdCIsImdyYWNlZnVsU2h1dGRvd24iLCJXb3JrdHJlZUV4aXREaWFsb2ciLCJHT09EQllFX01FU1NBR0VTIiwiZ2V0UmFuZG9tR29vZGJ5ZU1lc3NhZ2UiLCJQcm9wcyIsIm9uRG9uZSIsIm1lc3NhZ2UiLCJvbkNhbmNlbCIsInNob3dXb3JrdHJlZSIsIkV4aXRGbG93IiwidDAiLCIkIiwiX2MiLCJ0MSIsIm9uRXhpdCIsInJlc3VsdE1lc3NhZ2UiLCJ0MiJdLCJzb3VyY2VzIjpbIkV4aXRGbG93LnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgc2FtcGxlIGZyb20gJ2xvZGFzaC1lcy9zYW1wbGUuanMnXG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBncmFjZWZ1bFNodXRkb3duIH0gZnJvbSAnLi4vdXRpbHMvZ3JhY2VmdWxTaHV0ZG93bi5qcydcbmltcG9ydCB7IFdvcmt0cmVlRXhpdERpYWxvZyB9IGZyb20gJy4vV29ya3RyZWVFeGl0RGlhbG9nLmpzJ1xuXG5jb25zdCBHT09EQllFX01FU1NBR0VTID0gWydHb29kYnllIScsICdTZWUgeWEhJywgJ0J5ZSEnLCAnQ2F0Y2ggeW91IGxhdGVyISddXG5cbmZ1bmN0aW9uIGdldFJhbmRvbUdvb2RieWVNZXNzYWdlKCk6IHN0cmluZyB7XG4gIHJldHVybiBzYW1wbGUoR09PREJZRV9NRVNTQUdFUykgPz8gJ0dvb2RieWUhJ1xufVxuXG50eXBlIFByb3BzID0ge1xuICBvbkRvbmU6IChtZXNzYWdlPzogc3RyaW5nKSA9PiB2b2lkXG4gIG9uQ2FuY2VsPzogKCkgPT4gdm9pZFxuICBzaG93V29ya3RyZWU6IGJvb2xlYW5cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIEV4aXRGbG93KHtcbiAgc2hvd1dvcmt0cmVlLFxuICBvbkRvbmUsXG4gIG9uQ2FuY2VsLFxufTogUHJvcHMpOiBSZWFjdC5SZWFjdE5vZGUge1xuICBhc3luYyBmdW5jdGlvbiBvbkV4aXQocmVzdWx0TWVzc2FnZT86IHN0cmluZykge1xuICAgIG9uRG9uZShyZXN1bHRNZXNzYWdlID8/IGdldFJhbmRvbUdvb2RieWVNZXNzYWdlKCkpXG4gICAgYXdhaXQgZ3JhY2VmdWxTaHV0ZG93bigwLCAncHJvbXB0X2lucHV0X2V4aXQnKVxuICB9XG5cbiAgaWYgKHNob3dXb3JrdHJlZSkge1xuICAgIHJldHVybiA8V29ya3RyZWVFeGl0RGlhbG9nIG9uRG9uZT17b25FeGl0fSBvbkNhbmNlbD17b25DYW5jZWx9IC8+XG4gIH1cblxuICByZXR1cm4gbnVsbFxufVxuIl0sIm1hcHBpbmdzIjoiO0FBQUEsT0FBT0EsTUFBTSxNQUFNLHFCQUFxQjtBQUN4QyxPQUFPQyxLQUFLLE1BQU0sT0FBTztBQUN6QixTQUFTQyxnQkFBZ0IsUUFBUSw4QkFBOEI7QUFDL0QsU0FBU0Msa0JBQWtCLFFBQVEseUJBQXlCO0FBRTVELE1BQU1DLGdCQUFnQixHQUFHLENBQUMsVUFBVSxFQUFFLFNBQVMsRUFBRSxNQUFNLEVBQUUsa0JBQWtCLENBQUM7QUFFNUUsU0FBU0MsdUJBQXVCQSxDQUFBLENBQUUsRUFBRSxNQUFNLENBQUM7RUFDekMsT0FBT0wsTUFBTSxDQUFDSSxnQkFBZ0IsQ0FBQyxJQUFJLFVBQVU7QUFDL0M7QUFFQSxLQUFLRSxLQUFLLEdBQUc7RUFDWEMsTUFBTSxFQUFFLENBQUNDLE9BQWdCLENBQVIsRUFBRSxNQUFNLEVBQUUsR0FBRyxJQUFJO0VBQ2xDQyxRQUFRLENBQUMsRUFBRSxHQUFHLEdBQUcsSUFBSTtFQUNyQkMsWUFBWSxFQUFFLE9BQU87QUFDdkIsQ0FBQztBQUVELE9BQU8sU0FBQUMsU0FBQUMsRUFBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUFrQjtJQUFBSixZQUFBO0lBQUFILE1BQUE7SUFBQUU7RUFBQSxJQUFBRyxFQUlqQjtFQUFBLElBQUFHLEVBQUE7RUFBQSxJQUFBRixDQUFBLFFBQUFOLE1BQUE7SUFDTlEsRUFBQSxrQkFBQUMsT0FBQUMsYUFBQTtNQUNFVixNQUFNLENBQUNVLGFBQTBDLElBQXpCWix1QkFBdUIsQ0FBQyxDQUFDLENBQUM7TUFDbEQsTUFBTUgsZ0JBQWdCLENBQUMsQ0FBQyxFQUFFLG1CQUFtQixDQUFDO0lBQUEsQ0FDL0M7SUFBQVcsQ0FBQSxNQUFBTixNQUFBO0lBQUFNLENBQUEsTUFBQUUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUYsQ0FBQTtFQUFBO0VBSEQsTUFBQUcsTUFBQSxHQUFBRCxFQUdDO0VBRUQsSUFBSUwsWUFBWTtJQUFBLElBQUFRLEVBQUE7SUFBQSxJQUFBTCxDQUFBLFFBQUFKLFFBQUEsSUFBQUksQ0FBQSxRQUFBRyxNQUFBO01BQ1BFLEVBQUEsSUFBQyxrQkFBa0IsQ0FBU0YsTUFBTSxDQUFOQSxPQUFLLENBQUMsQ0FBWVAsUUFBUSxDQUFSQSxTQUFPLENBQUMsR0FBSTtNQUFBSSxDQUFBLE1BQUFKLFFBQUE7TUFBQUksQ0FBQSxNQUFBRyxNQUFBO01BQUFILENBQUEsTUFBQUssRUFBQTtJQUFBO01BQUFBLEVBQUEsR0FBQUwsQ0FBQTtJQUFBO0lBQUEsT0FBMURLLEVBQTBEO0VBQUE7RUFDbEUsT0FFTSxJQUFJO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/components/ExportDialog.tsx`

**信息:**
- 行数: 128
- 大小: 19333 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { join } from 'path';
import React, { useCallback, useState } from 'react';
import type { ExitState } from '../hooks/useExitOnCtrlCDWithKeybindings.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { setClipboard } from '../ink/termio/osc.js';
import { Box, Text } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { getCwd } from '../utils/cwd.js';
import { writeFileSync_DEPRECATED } from '../utils/slowOperations.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { Select } from './CustomSelect/select.js';
import { Byline } from './design-system/Byline.js';
import { Dialog } from './design-system/Dialog.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import TextInput from './TextInput.js';
type ExportDialogProps = {
  content: string;
  defaultFilename: string;
  onDone: (result: {
    success: boolean;
    message: string;
  }) => void;
};
type ExportOption = 'clipboard' | 'file';
export function ExportDialog({
  content,
  defaultFilename,
  onDone
}: ExportDialogProps): React.ReactNode {
  const [, setSelectedOption] = useState<ExportOption | null>(null);
  const [filename, setFilename] = useState<string>(defaultFilename);
  const [cursorOffset, setCursorOffset] = useState<number>(defaultFilename.length);
  const [showFilenameInput, setShowFilenameInput] = useState(false);
  const {
    columns
  } = useTerminalSize();

  // Handle going back from filename input to option selection
  const handleGoBack = useCallback(() => {
    setShowFilenameInput(false);
    setSelectedOption(null);
  }, []);
  const handleSelectOption = async (value: string): Promise<void> => {
    if (value === 'clipboard') {
      // Copy to clipboard immediately
      const raw = await setClipboard(content);
      if (raw) process.stdout.write(raw);
      onDone({
        success: true,
        message: 'Conversation copied to clipboard'

```

---


### `src/components/FallbackToolUseErrorMessage.tsx`

**信息:**
- 行数: 116
- 大小: 12623 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/messages/messages.mjs';
import * as React from 'react';
import { stripUnderlineAnsi } from 'src/components/shell/OutputLine.js';
import { extractTag } from 'src/utils/messages.js';
import { removeSandboxViolationTags } from 'src/utils/sandbox/sandbox-ui-utils.js';
import { Box, Text } from '../ink.js';
import { useShortcutDisplay } from '../keybindings/useShortcutDisplay.js';
import { countCharInString } from '../utils/stringUtils.js';
import { MessageResponse } from './MessageResponse.js';
const MAX_RENDERED_LINES = 10;
type Props = {
  result: ToolResultBlockParam['content'];
  verbose: boolean;
};
export function FallbackToolUseErrorMessage(t0) {
  const $ = _c(25);
  const {
    result,
    verbose
  } = t0;
  const transcriptShortcut = useShortcutDisplay("app:toggleTranscript", "Global", "ctrl+o");
  let T0;
  let T1;
  let T2;
  let plusLines;
  let t1;
  let t2;
  let t3;
  if ($[0] !== result || $[1] !== verbose) {
    let error;
    if (typeof result !== "string") {
      error = "Tool execution failed";
    } else {
      const extractedError = extractTag(result, "tool_use_error") ?? result;
      const withoutSandboxViolations = removeSandboxViolationTags(extractedError);
      const withoutErrorTags = withoutSandboxViolations.replace(/<\/?error>/g, "");
      const trimmed = withoutErrorTags.trim();
      if (!verbose && trimmed.includes("InputValidationError: ")) {
        error = "Invalid tool parameters";
      } else {
        if (trimmed.startsWith("Error: ") || trimmed.startsWith("Cancelled: ")) {
          error = trimmed;
        } else {
          error = `Error: ${trimmed}`;
        }
      }
    }
    plusLines = countCharInString(error, "\n") + 1 - MAX_RENDERED_LINES;
    T2 = MessageResponse;

```

---


### `src/components/FallbackToolUseRejectedMessage.tsx`

**信息:**
- 行数: 16
- 大小: 1754 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { InterruptedByUser } from './InterruptedByUser.js';
import { MessageResponse } from './MessageResponse.js';
export function FallbackToolUseRejectedMessage() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <MessageResponse height={1}><InterruptedByUser /></MessageResponse>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkludGVycnVwdGVkQnlVc2VyIiwiTWVzc2FnZVJlc3BvbnNlIiwiRmFsbGJhY2tUb29sVXNlUmVqZWN0ZWRNZXNzYWdlIiwiJCIsIl9jIiwidDAiLCJTeW1ib2wiLCJmb3IiXSwic291cmNlcyI6WyJGYWxsYmFja1Rvb2xVc2VSZWplY3RlZE1lc3NhZ2UudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgSW50ZXJydXB0ZWRCeVVzZXIgfSBmcm9tICcuL0ludGVycnVwdGVkQnlVc2VyLmpzJ1xuaW1wb3J0IHsgTWVzc2FnZVJlc3BvbnNlIH0gZnJvbSAnLi9NZXNzYWdlUmVzcG9uc2UuanMnXG5cbmV4cG9ydCBmdW5jdGlvbiBGYWxsYmFja1Rvb2xVc2VSZWplY3RlZE1lc3NhZ2UoKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgcmV0dXJuIChcbiAgICA8TWVzc2FnZVJlc3BvbnNlIGhlaWdodD17MX0+XG4gICAgICA8SW50ZXJydXB0ZWRCeVVzZXIgLz5cbiAgICA8L01lc3NhZ2VSZXNwb25zZT5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiO0FBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixTQUFTQyxpQkFBaUIsUUFBUSx3QkFBd0I7QUFDMUQsU0FBU0MsZUFBZSxRQUFRLHNCQUFzQjtBQUV0RCxPQUFPLFNBQUFDLCtCQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQUEsSUFBQUMsRUFBQTtFQUFBLElBQUFGLENBQUEsUUFBQUcsTUFBQSxDQUFBQyxHQUFBO0lBRUhGLEVBQUEsSUFBQyxlQUFlLENBQVMsTUFBQyxDQUFELEdBQUMsQ0FDeEIsQ0FBQyxpQkFBaUIsR0FDcEIsRUFGQyxlQUFlLENBRUU7SUFBQUYsQ0FBQSxNQUFBRSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBRixDQUFBO0VBQUE7RUFBQSxPQUZsQkUsRUFFa0I7QUFBQSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/components/FastIcon.tsx`

**信息:**
- 行数: 46
- 大小: 4627 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import * as React from 'react';
import { LIGHTNING_BOLT } from '../constants/figures.js';
import { Text } from '../ink.js';
import { getGlobalConfig } from '../utils/config.js';
import { resolveThemeSetting } from '../utils/systemTheme.js';
import { color } from './design-system/color.js';
type Props = {
  cooldown?: boolean;
};
export function FastIcon(t0) {
  const $ = _c(2);
  const {
    cooldown
  } = t0;
  if (cooldown) {
    let t1;
    if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
      t1 = <Text color="promptBorder" dimColor={true}>{LIGHTNING_BOLT}</Text>;
      $[0] = t1;
    } else {
      t1 = $[0];
    }
    return t1;
  }
  let t1;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Text color="fastMode">{LIGHTNING_BOLT}</Text>;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  return t1;
}
export function getFastIconString(applyColor = true, cooldown = false): string {
  if (!applyColor) {
    return LIGHTNING_BOLT;
  }
  const themeName = resolveThemeSetting(getGlobalConfig().theme);
  if (cooldown) {
    return chalk.dim(color('promptBorder', themeName)(LIGHTNING_BOLT));
  }
  return color('fastMode', themeName)(LIGHTNING_BOLT);
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJjaGFsayIsIlJlYWN0IiwiTElHSFROSU5HX0JPTFQiLCJUZXh0IiwiZ2V0R2xvYmFsQ29uZmlnIiwicmVzb2x2ZVRoZW1lU2V0dGluZyIsImNvbG9yIiwiUHJvcHMiLCJjb29sZG93biIsIkZhc3RJY29uIiwidDAiLCIkIiwiX2MiLCJ0MSIsIlN5bWJvbCIsImZvciIsImdldEZhc3RJY29uU3RyaW5nIiwiYXBwbHlDb2xvciIsInRoZW1lTmFtZSIsInRoZW1lIiwiZGltIl0sInNvdXJjZXMiOlsiRmFzdEljb24udHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCBjaGFsayBmcm9tICdjaGFsaydcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgTElHSFROSU5HX0JPTFQgfSBmcm9tICcuLi9jb25zdGFudHMvZmlndXJlcy5qcydcbmltcG9ydCB7IFRleHQgfSBmcm9tICcuLi9pbmsuanMnXG5pbXBvcnQgeyBnZXRHbG9iYWxDb25maWcgfSBmcm9tICcuLi91dGlscy9jb25maWcuanMnXG5pbXBvcnQgeyByZXNvbHZlVGhlbWVTZXR0aW5nIH0gZnJvbSAnLi4vdXRpbHMvc3lzdGVtVGhlbWUuanMnXG5pbXBvcnQgeyBjb2xvciB9IGZyb20gJy4vZGVzaWduLXN5c3RlbS9jb2xvci5qcydcblxudHlwZSBQcm9wcyA9IHtcbiAgY29vbGRvd24/OiBib29sZWFuXG59XG5cbmV4cG9ydCBmdW5jdGlvbiBGYXN0SWNvbih7IGNvb2xkb3duIH06IFByb3BzKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgaWYgKGNvb2xkb3duKSB7XG4gICAgcmV0dXJuIChcbiAgICAgIDxUZXh0IGNvbG9yPVwicHJvbXB0Qm9yZGVyXCIgZGltQ29sb3I+XG4gICAgICAgIHtMSUdIVE5JTkdfQk9MVH1cbiAgICAgIDwvVGV4dD5cbiAgICApXG4gIH1cbiAgcmV0dXJuIDxUZXh0IGNvbG9yPVwiZmFzdE1vZGVcIj57TElHSFROSU5HX0JPTFR9PC9UZXh0PlxufVxuXG5leHBvcnQgZnVuY3Rpb24gZ2V0RmFzdEljb25TdHJpbmcoYXBwbHlDb2xvciA9IHRydWUsIGNvb2xkb3duID0gZmFsc2UpOiBzdHJpbmcge1xuICBpZiAoIWFwcGx5Q29sb3IpIHtcbiAgICByZXR1cm4gTElHSFROSU5HX0JPTFRcbiAgfVxuICBjb25zdCB0aGVtZU5hbWUgPSByZXNvbHZlVGhlbWVTZXR0aW5nKGdldEdsb2JhbENvbmZpZygpLnRoZW1lKVxuICBpZiAoY29vbGRvd24pIHtcbiAgICByZXR1cm4gY2hhbGsuZGltKGNvbG9yKCdwcm9tcHRCb3JkZXInLCB0aGVtZU5hbWUpKExJR0hUTklOR19CT0xUKSlcbiAgfVxuICByZXR1cm4gY29sb3IoJ2Zhc3RNb2RlJywgdGhlbWVOYW1lKShMSUdIVE5JTkdfQk9MVClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU9BLEtBQUssTUFBTSxPQUFPO0FBQ3pCLE9BQU8sS0FBS0MsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsY0FBYyxRQUFRLHlCQUF5QjtBQUN4RCxTQUFTQyxJQUFJLFFBQVEsV0FBVztBQUNoQyxTQUFTQyxlQUFlLFFBQVEsb0JBQW9CO0FBQ3BELFNBQVNDLG1CQUFtQixRQUFRLHlCQUF5QjtBQUM3RCxTQUFTQyxLQUFLLFFBQVEsMEJBQTBCO0FBRWhELEtBQUtDLEtBQUssR0FBRztFQUNYQyxRQUFRLENBQUMsRUFBRSxPQUFPO0FBQ3BCLENBQUM7QUFFRCxPQUFPLFNBQUFDLFNBQUFDLEVBQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFBa0I7SUFBQUo7RUFBQSxJQUFBRSxFQUFtQjtFQUMxQyxJQUFJRixRQUFRO0lBQUEsSUFBQUssRUFBQTtJQUFBLElBQUFGLENBQUEsUUFBQUcsTUFBQSxDQUFBQyxHQUFBO01BRVJGLEVBQUEsSUFBQyxJQUFJLENBQU8sS0FBYyxDQUFkLGNBQWMsQ0FBQyxRQUFRLENBQVIsS0FBTyxDQUFDLENBQ2hDWCxlQUFhLENBQ2hCLEVBRkMsSUFBSSxDQUVFO01BQUFTLENBQUEsTUFBQUUsRUFBQTtJQUFBO01BQUFBLEVBQUEsR0FBQUYsQ0FBQTtJQUFBO0lBQUEsT0FGUEUsRUFFTztFQUFBO0VBRVYsSUFBQUEsRUFBQTtFQUFBLElBQUFGLENBQUEsUUFBQUcsTUFBQSxDQUFBQyxHQUFBO0lBQ01GLEVBQUEsSUFBQyxJQUFJLENBQU8sS0FBVSxDQUFWLFVBQVUsQ0FBRVgsZUFBYSxDQUFFLEVBQXRDLElBQUksQ0FBeUM7SUFBQVMsQ0FBQSxNQUFBRSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBRixDQUFBO0VBQUE7RUFBQSxPQUE5Q0UsRUFBOEM7QUFBQTtBQUd2RCxPQUFPLFNBQVNHLGlCQUFpQkEsQ0FBQ0MsVUFBVSxHQUFHLElBQUksRUFBRVQsUUFBUSxHQUFHLEtBQUssQ0FBQyxFQUFFLE1BQU0sQ0FBQztFQUM3RSxJQUFJLENBQUNTLFVBQVUsRUFBRTtJQUNmLE9BQU9mLGNBQWM7RUFDdkI7RUFDQSxNQUFNZ0IsU0FBUyxHQUFHYixtQkFBbUIsQ0FBQ0QsZUFBZSxDQUFDLENBQUMsQ0FBQ2UsS0FBSyxDQUFDO0VBQzlELElBQUlYLFFBQVEsRUFBRTtJQUNaLE9BQU9SLEtBQUssQ0FBQ29CLEdBQUcsQ0FBQ2QsS0FBSyxDQUFDLGNBQWMsRUFBRVksU0FBUyxDQUFDLENBQUNoQixjQUFjLENBQUMsQ0FBQztFQUNwRTtFQUNBLE9BQU9JLEtBQUssQ0FBQyxVQUFVLEVBQUVZLFNBQVMsQ0FBQyxDQUFDaEIsY0FBYyxDQUFDO0FBQ3JEIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/Feedback.tsx`

**信息:**
- 行数: 592
- 大小: 87696 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import axios from 'axios';
import { readFile, stat } from 'fs/promises';
import * as React from 'react';
import { useCallback, useEffect, useState } from 'react';
import { getLastAPIRequest } from 'src/bootstrap/state.js';
import { logEventTo1P } from 'src/services/analytics/firstPartyEventLogger.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { getLastAssistantMessage, normalizeMessagesForAPI } from 'src/utils/messages.js';
import type { CommandResultDisplay } from '../commands.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { Box, Text, useInput } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { queryHaiku } from '../services/api/claude.js';
import { startsWithApiErrorPrefix } from '../services/api/errors.js';
import type { Message } from '../types/message.js';
import { checkAndRefreshOAuthTokenIfNeeded } from '../utils/auth.js';
import { openBrowser } from '../utils/browser.js';
import { logForDebugging } from '../utils/debug.js';
import { env } from '../utils/env.js';
import { type GitRepoState, getGitState, getIsGit } from '../utils/git.js';
import { getAuthHeaders, getUserAgent } from '../utils/http.js';
import { getInMemoryErrors, logError } from '../utils/log.js';
import { isEssentialTrafficOnly } from '../utils/privacyLevel.js';
import { extractTeammateTranscriptsFromTasks, getTranscriptPath, loadAllSubagentTranscriptsFromDisk, MAX_TRANSCRIPT_READ_BYTES } from '../utils/sessionStorage.js';
import { jsonStringify } from '../utils/slowOperations.js';
import { asSystemPrompt } from '../utils/systemPromptType.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { Byline } from './design-system/Byline.js';
import { Dialog } from './design-system/Dialog.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import TextInput from './TextInput.js';

// This value was determined experimentally by testing the URL length limit
const GITHUB_URL_LIMIT = 7250;
const GITHUB_ISSUES_REPO_URL = "external" === 'ant' ? 'https://github.com/anthropics/claude-cli-internal/issues' : 'https://github.com/anthropics/claude-code/issues';
type Props = {
  abortSignal: AbortSignal;
  messages: Message[];
  initialDescription?: string;
  onDone(result: string, options?: {
    display?: CommandResultDisplay;
  }): void;
  backgroundTasks?: {
    [taskId: string]: {
      type: string;
      identity?: {
        agentId: string;
      };
      messages?: Message[];
    };

```

---


### `src/components/FeedbackSurvey/FeedbackSurvey.tsx`

**信息:**
- 行数: 174
- 大小: 19393 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { Box, Text } from '../../ink.js';
import { FeedbackSurveyView, isValidResponseInput } from './FeedbackSurveyView.js';
import type { TranscriptShareResponse } from './TranscriptSharePrompt.js';
import { TranscriptSharePrompt } from './TranscriptSharePrompt.js';
import { useDebouncedDigitInput } from './useDebouncedDigitInput.js';
import type { FeedbackSurveyResponse } from './utils.js';
type Props = {
  state: 'closed' | 'open' | 'thanks' | 'transcript_prompt' | 'submitting' | 'submitted';
  lastResponse: FeedbackSurveyResponse | null;
  handleSelect: (selected: FeedbackSurveyResponse) => void;
  handleTranscriptSelect?: (selected: TranscriptShareResponse) => void;
  inputValue: string;
  setInputValue: (value: string) => void;
  onRequestFeedback?: () => void;
  message?: string;
};
export function FeedbackSurvey(t0) {
  const $ = _c(16);
  const {
    state,
    lastResponse,
    handleSelect,
    handleTranscriptSelect,
    inputValue,
    setInputValue,
    onRequestFeedback,
    message
  } = t0;
  if (state === "closed") {
    return null;
  }
  if (state === "thanks") {
    let t1;
    if ($[0] !== inputValue || $[1] !== lastResponse || $[2] !== onRequestFeedback || $[3] !== setInputValue) {
      t1 = <FeedbackSurveyThanks lastResponse={lastResponse} inputValue={inputValue} setInputValue={setInputValue} onRequestFeedback={onRequestFeedback} />;
      $[0] = inputValue;
      $[1] = lastResponse;
      $[2] = onRequestFeedback;
      $[3] = setInputValue;
      $[4] = t1;
    } else {
      t1 = $[4];
    }
    return t1;
  }
  if (state === "submitted") {
    let t1;

```

---


### `src/components/FeedbackSurvey/FeedbackSurveyView.tsx`

**信息:**
- 行数: 108
- 大小: 10660 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../../ink.js';
import { useDebouncedDigitInput } from './useDebouncedDigitInput.js';
import type { FeedbackSurveyResponse } from './utils.js';
type Props = {
  onSelect: (option: FeedbackSurveyResponse) => void;
  inputValue: string;
  setInputValue: (value: string) => void;
  message?: string;
};
const RESPONSE_INPUTS = ['0', '1', '2', '3'] as const;
type ResponseInput = (typeof RESPONSE_INPUTS)[number];
const inputToResponse: Record<ResponseInput, FeedbackSurveyResponse> = {
  '0': 'dismissed',
  '1': 'bad',
  '2': 'fine',
  '3': 'good'
} as const;
export const isValidResponseInput = (input: string): input is ResponseInput => (RESPONSE_INPUTS as readonly string[]).includes(input);
const DEFAULT_MESSAGE = 'How is Claude doing this session? (optional)';
export function FeedbackSurveyView(t0) {
  const $ = _c(15);
  const {
    onSelect,
    inputValue,
    setInputValue,
    message: t1
  } = t0;
  const message = t1 === undefined ? DEFAULT_MESSAGE : t1;
  let t2;
  if ($[0] !== onSelect) {
    t2 = digit => onSelect(inputToResponse[digit]);
    $[0] = onSelect;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  let t3;
  if ($[2] !== inputValue || $[3] !== setInputValue || $[4] !== t2) {
    t3 = {
      inputValue,
      setInputValue,
      isValidDigit: isValidResponseInput,
      onDigit: t2
    };
    $[2] = inputValue;
    $[3] = setInputValue;
    $[4] = t2;
    $[5] = t3;

```

---


### `src/components/FeedbackSurvey/TranscriptSharePrompt.tsx`

**信息:**
- 行数: 88
- 大小: 9933 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { BLACK_CIRCLE } from '../../constants/figures.js';
import { Box, Text } from '../../ink.js';
import { useDebouncedDigitInput } from './useDebouncedDigitInput.js';
export type TranscriptShareResponse = 'yes' | 'no' | 'dont_ask_again';
type Props = {
  onSelect: (option: TranscriptShareResponse) => void;
  inputValue: string;
  setInputValue: (value: string) => void;
};
const RESPONSE_INPUTS = ['1', '2', '3'] as const;
type ResponseInput = (typeof RESPONSE_INPUTS)[number];
const inputToResponse: Record<ResponseInput, TranscriptShareResponse> = {
  '1': 'yes',
  '2': 'no',
  '3': 'dont_ask_again'
} as const;
const isValidResponseInput = (input: string): input is ResponseInput => (RESPONSE_INPUTS as readonly string[]).includes(input);
export function TranscriptSharePrompt(t0) {
  const $ = _c(11);
  const {
    onSelect,
    inputValue,
    setInputValue
  } = t0;
  let t1;
  if ($[0] !== onSelect) {
    t1 = digit => onSelect(inputToResponse[digit]);
    $[0] = onSelect;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] !== inputValue || $[3] !== setInputValue || $[4] !== t1) {
    t2 = {
      inputValue,
      setInputValue,
      isValidDigit: isValidResponseInput,
      onDigit: t1
    };
    $[2] = inputValue;
    $[3] = setInputValue;
    $[4] = t1;
    $[5] = t2;
  } else {
    t2 = $[5];
  }
  useDebouncedDigitInput(t2);

```

---


### `src/components/FeedbackSurvey/submitTranscriptShare.ts`

**信息:**
- 行数: 112
- 大小: 3251 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { readFile, stat } from 'fs/promises'
import type { Message } from '../../types/message.js'
import { checkAndRefreshOAuthTokenIfNeeded } from '../../utils/auth.js'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { getAuthHeaders, getUserAgent } from '../../utils/http.js'
import { normalizeMessagesForAPI } from '../../utils/messages.js'
import {
  extractAgentIdsFromMessages,
  getTranscriptPath,
  loadSubagentTranscripts,
  MAX_TRANSCRIPT_READ_BYTES,
} from '../../utils/sessionStorage.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { redactSensitiveInfo } from '../Feedback.js'

type TranscriptShareResult = {
  success: boolean
  transcriptId?: string
}

export type TranscriptShareTrigger =
  | 'bad_feedback_survey'
  | 'good_feedback_survey'
  | 'frustration'
  | 'memory_survey'

export async function submitTranscriptShare(
  messages: Message[],
  trigger: TranscriptShareTrigger,
  appearanceId: string,
): Promise<TranscriptShareResult> {
  try {
    logForDebugging('Collecting transcript for sharing', { level: 'info' })

    const transcript = normalizeMessagesForAPI(messages)

    // Collect subagent transcripts
    const agentIds = extractAgentIdsFromMessages(messages)
    const subagentTranscripts = await loadSubagentTranscripts(agentIds)

    // Read raw JSONL transcript (with size guard to prevent OOM)
    let rawTranscriptJsonl: string | undefined
    try {
      const transcriptPath = getTranscriptPath()
      const { size } = await stat(transcriptPath)
      if (size <= MAX_TRANSCRIPT_READ_BYTES) {
        rawTranscriptJsonl = await readFile(transcriptPath, 'utf-8')
      } else {

```

---


### `src/components/FeedbackSurvey/useDebouncedDigitInput.ts`

**信息:**
- 行数: 82
- 大小: 2722 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef } from 'react'
import { normalizeFullWidthDigits } from '../../utils/stringUtils.js'

// Delay before accepting a digit as a response, to prevent accidental
// submissions when users start messages with numbers (e.g., numbered lists).
// Short enough to feel instant for intentional presses, long enough to
// cancel when the user types more characters.
const DEFAULT_DEBOUNCE_MS = 400

/**
 * Detects when the user types a single valid digit into the prompt input,
 * debounces to avoid accidental submissions (e.g., "1. First item"),
 * trims the digit from the input, and fires a callback.
 *
 * Used by survey components that accept numeric responses typed directly
 * into the main prompt input.
 */
export function useDebouncedDigitInput<T extends string = string>({
  inputValue,
  setInputValue,
  isValidDigit,
  onDigit,
  enabled = true,
  once = false,
  debounceMs = DEFAULT_DEBOUNCE_MS,
}: {
  inputValue: string
  setInputValue: (value: string) => void
  isValidDigit: (char: string) => char is T
  onDigit: (digit: T) => void
  enabled?: boolean
  once?: boolean
  debounceMs?: number
}): void {
  const initialInputValue = useRef(inputValue)
  const hasTriggeredRef = useRef(false)
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  // Latest-ref pattern so callers can pass inline callbacks without causing
  // the effect to re-run (which would reset the debounce timer every render).
  const callbacksRef = useRef({ setInputValue, isValidDigit, onDigit })
  callbacksRef.current = { setInputValue, isValidDigit, onDigit }

  useEffect(() => {
    if (!enabled || (once && hasTriggeredRef.current)) {
      return
    }

    if (debounceRef.current !== null) {
      clearTimeout(debounceRef.current)

```

---


### `src/components/FeedbackSurvey/useFeedbackSurvey.tsx`

**信息:**
- 行数: 296
- 大小: 48187 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useDynamicConfig } from 'src/hooks/useDynamicConfig.js';
import { isFeedbackSurveyDisabled } from 'src/services/analytics/config.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { isPolicyAllowed } from '../../services/policyLimits/index.js';
import type { Message } from '../../types/message.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import { getLastAssistantMessage } from '../../utils/messages.js';
import { getMainLoopModel } from '../../utils/model/model.js';
import { getInitialSettings } from '../../utils/settings/settings.js';
import { logOTelEvent } from '../../utils/telemetry/events.js';
import { submitTranscriptShare, type TranscriptShareTrigger } from './submitTranscriptShare.js';
import type { TranscriptShareResponse } from './TranscriptSharePrompt.js';
import { useSurveyState } from './useSurveyState.js';
import type { FeedbackSurveyResponse, FeedbackSurveyType } from './utils.js';
type FeedbackSurveyConfig = {
  minTimeBeforeFeedbackMs: number;
  minTimeBetweenFeedbackMs: number;
  minTimeBetweenGlobalFeedbackMs: number;
  minUserTurnsBeforeFeedback: number;
  minUserTurnsBetweenFeedback: number;
  hideThanksAfterMs: number;
  onForModels: string[];
  probability: number;
};
type TranscriptAskConfig = {
  probability: number;
};
const DEFAULT_FEEDBACK_SURVEY_CONFIG: FeedbackSurveyConfig = {
  minTimeBeforeFeedbackMs: 600000,
  minTimeBetweenFeedbackMs: 3600000,
  minTimeBetweenGlobalFeedbackMs: 100000000,
  minUserTurnsBeforeFeedback: 5,
  minUserTurnsBetweenFeedback: 10,
  hideThanksAfterMs: 3000,
  onForModels: ['*'],
  probability: 0.005
};
const DEFAULT_TRANSCRIPT_ASK_CONFIG: TranscriptAskConfig = {
  probability: 0
};
export function useFeedbackSurvey(messages: Message[], isLoading: boolean, submitCount: number, surveyType: FeedbackSurveyType = 'session', hasActivePrompt: boolean = false): {
  state: 'closed' | 'open' | 'thanks' | 'transcript_prompt' | 'submitting' | 'submitted';
  lastResponse: FeedbackSurveyResponse | null;
  handleSelect: (selected: FeedbackSurveyResponse) => boolean;
  handleTranscriptSelect: (selected: TranscriptShareResponse) => void;
} {
  const lastAssistantMessageIdRef = useRef('unknown');
  lastAssistantMessageIdRef.current = getLastAssistantMessage(messages)?.message?.id || 'unknown';

```

---


### `src/components/FeedbackSurvey/useFrustrationDetection.ts`

**信息:**
- 行数: 3
- 大小: 70 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function useFrustrationDetection(): boolean {
  return false
}

```

---


### `src/components/FeedbackSurvey/useMemorySurvey.tsx`

**信息:**
- 行数: 213
- 大小: 30418 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { useCallback, useEffect, useMemo, useRef } from 'react';
import { isFeedbackSurveyDisabled } from 'src/services/analytics/config.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from 'src/services/analytics/growthbook.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { isAutoMemoryEnabled } from '../../memdir/paths.js';
import { isPolicyAllowed } from '../../services/policyLimits/index.js';
import { FILE_READ_TOOL_NAME } from '../../tools/FileReadTool/prompt.js';
import type { Message } from '../../types/message.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import { isAutoManagedMemoryFile } from '../../utils/memoryFileDetection.js';
import { extractTextContent, getLastAssistantMessage } from '../../utils/messages.js';
import { logOTelEvent } from '../../utils/telemetry/events.js';
import { submitTranscriptShare } from './submitTranscriptShare.js';
import type { TranscriptShareResponse } from './TranscriptSharePrompt.js';
import { useSurveyState } from './useSurveyState.js';
import type { FeedbackSurveyResponse } from './utils.js';
const HIDE_THANKS_AFTER_MS = 3000;
const MEMORY_SURVEY_GATE = 'tengu_dunwich_bell';
const MEMORY_SURVEY_EVENT = 'tengu_memory_survey_event';
const SURVEY_PROBABILITY = 0.2;
const TRANSCRIPT_SHARE_TRIGGER = 'memory_survey';
const MEMORY_WORD_RE = /\bmemor(?:y|ies)\b/i;
function hasMemoryFileRead(messages: Message[]): boolean {
  for (const message of messages) {
    if (message.type !== 'assistant') {
      continue;
    }
    const content = message.message.content;
    if (!Array.isArray(content)) {
      continue;
    }
    for (const block of content) {
      if (block.type !== 'tool_use' || block.name !== FILE_READ_TOOL_NAME) {
        continue;
      }
      const input = block.input as {
        file_path?: unknown;
      };
      if (typeof input.file_path === 'string' && isAutoManagedMemoryFile(input.file_path)) {
        return true;
      }
    }
  }
  return false;
}
export function useMemorySurvey(messages: Message[], isLoading: boolean, hasActivePrompt = false, {
  enabled = true
}: {
  enabled?: boolean;

```

---


### `src/components/FeedbackSurvey/usePostCompactSurvey.tsx`

**信息:**
- 行数: 206
- 大小: 24071 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { isFeedbackSurveyDisabled } from 'src/services/analytics/config.js';
import { checkStatsigFeatureGate_CACHED_MAY_BE_STALE } from 'src/services/analytics/growthbook.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { shouldUseSessionMemoryCompaction } from '../../services/compact/sessionMemoryCompact.js';
import type { Message } from '../../types/message.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import { isCompactBoundaryMessage } from '../../utils/messages.js';
import { logOTelEvent } from '../../utils/telemetry/events.js';
import { useSurveyState } from './useSurveyState.js';
import type { FeedbackSurveyResponse } from './utils.js';
const HIDE_THANKS_AFTER_MS = 3000;
const POST_COMPACT_SURVEY_GATE = 'tengu_post_compact_survey';
const SURVEY_PROBABILITY = 0.2; // Show survey 20% of the time after compaction

function hasMessageAfterBoundary(messages: Message[], boundaryUuid: string): boolean {
  const boundaryIndex = messages.findIndex(msg => msg.uuid === boundaryUuid);
  if (boundaryIndex === -1) {
    return false;
  }

  // Check if there's a user or assistant message after the boundary
  for (let i = boundaryIndex + 1; i < messages.length; i++) {
    const msg = messages[i];
    if (msg && (msg.type === 'user' || msg.type === 'assistant')) {
      return true;
    }
  }
  return false;
}
export function usePostCompactSurvey(messages, isLoading, t0, t1) {
  const $ = _c(23);
  const hasActivePrompt = t0 === undefined ? false : t0;
  let t2;
  if ($[0] !== t1) {
    t2 = t1 === undefined ? {} : t1;
    $[0] = t1;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  const {
    enabled: t3
  } = t2;
  const enabled = t3 === undefined ? true : t3;
  const [gateEnabled, setGateEnabled] = useState(null);
  let t4;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t4 = new Set();

```

---


### `src/components/FeedbackSurvey/useSurveyState.tsx`

**信息:**
- 行数: 100
- 大小: 14800 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { randomUUID } from 'crypto';
import { useCallback, useRef, useState } from 'react';
import type { TranscriptShareResponse } from './TranscriptSharePrompt.js';
import type { FeedbackSurveyResponse } from './utils.js';
type SurveyState = 'closed' | 'open' | 'thanks' | 'transcript_prompt' | 'submitting' | 'submitted';
type UseSurveyStateOptions = {
  hideThanksAfterMs: number;
  onOpen: (appearanceId: string) => void | Promise<void>;
  onSelect: (appearanceId: string, selected: FeedbackSurveyResponse) => void | Promise<void>;
  shouldShowTranscriptPrompt?: (selected: FeedbackSurveyResponse) => boolean;
  onTranscriptPromptShown?: (appearanceId: string, surveyResponse: FeedbackSurveyResponse) => void;
  onTranscriptSelect?: (appearanceId: string, selected: TranscriptShareResponse, surveyResponse: FeedbackSurveyResponse | null) => boolean | Promise<boolean>;
};
export function useSurveyState({
  hideThanksAfterMs,
  onOpen,
  onSelect,
  shouldShowTranscriptPrompt,
  onTranscriptPromptShown,
  onTranscriptSelect
}: UseSurveyStateOptions): {
  state: SurveyState;
  lastResponse: FeedbackSurveyResponse | null;
  open: () => void;
  handleSelect: (selected: FeedbackSurveyResponse) => boolean;
  handleTranscriptSelect: (selected: TranscriptShareResponse) => void;
} {
  const [state, setState] = useState<SurveyState>('closed');
  const [lastResponse, setLastResponse] = useState<FeedbackSurveyResponse | null>(null);
  const appearanceId = useRef(randomUUID());
  const lastResponseRef = useRef<FeedbackSurveyResponse | null>(null);
  const showThanksThenClose = useCallback(() => {
    setState('thanks');
    setTimeout((setState_0, setLastResponse_0) => {
      setState_0('closed');
      setLastResponse_0(null);
    }, hideThanksAfterMs, setState, setLastResponse);
  }, [hideThanksAfterMs]);
  const showSubmittedThenClose = useCallback(() => {
    setState('submitted');
    setTimeout(setState, hideThanksAfterMs, 'closed');
  }, [hideThanksAfterMs]);
  const open = useCallback(() => {
    if (state !== 'closed') {
      return;
    }
    setState('open');
    appearanceId.current = randomUUID();
    void onOpen(appearanceId.current);
  }, [state, onOpen]);

```

---


### `src/components/FeedbackSurvey/utils.ts`

**信息:**
- 行数: 8
- 大小: 140 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type FeedbackSurveyResponse =
  | 'good'
  | 'bad'
  | 'neutral'
  | 'dismissed'
  | string

export type FeedbackSurveyType = string

```

---


### `src/components/FileEditToolDiff.tsx`

**信息:**
- 行数: 181
- 大小: 21900 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { StructuredPatchHunk } from 'diff';
import * as React from 'react';
import { Suspense, use, useState } from 'react';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { Box, Text } from '../ink.js';
import type { FileEdit } from '../tools/FileEditTool/types.js';
import { findActualString, preserveQuoteStyle } from '../tools/FileEditTool/utils.js';
import { adjustHunkLineNumbers, CONTEXT_LINES, getPatchForDisplay } from '../utils/diff.js';
import { logError } from '../utils/log.js';
import { CHUNK_SIZE, openForScan, readCapped, scanForContext } from '../utils/readEditContext.js';
import { firstLineOf } from '../utils/stringUtils.js';
import { StructuredDiffList } from './StructuredDiffList.js';
type Props = {
  file_path: string;
  edits: FileEdit[];
};
type DiffData = {
  patch: StructuredPatchHunk[];
  firstLine: string | null;
  fileContent: string | undefined;
};
export function FileEditToolDiff(props) {
  const $ = _c(7);
  let t0;
  if ($[0] !== props.edits || $[1] !== props.file_path) {
    t0 = () => loadDiffData(props.file_path, props.edits);
    $[0] = props.edits;
    $[1] = props.file_path;
    $[2] = t0;
  } else {
    t0 = $[2];
  }
  const [dataPromise] = useState(t0);
  let t1;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <DiffFrame placeholder={true} />;
    $[3] = t1;
  } else {
    t1 = $[3];
  }
  let t2;
  if ($[4] !== dataPromise || $[5] !== props.file_path) {
    t2 = <Suspense fallback={t1}><DiffBody promise={dataPromise} file_path={props.file_path} /></Suspense>;
    $[4] = dataPromise;
    $[5] = props.file_path;
    $[6] = t2;
  } else {
    t2 = $[6];
  }

```

---


### `src/components/FileEditToolUpdatedMessage.tsx`

**信息:**
- 行数: 124
- 大小: 12097 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { StructuredPatchHunk } from 'diff';
import * as React from 'react';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { Box, Text } from '../ink.js';
import { count } from '../utils/array.js';
import { MessageResponse } from './MessageResponse.js';
import { StructuredDiffList } from './StructuredDiffList.js';
type Props = {
  filePath: string;
  structuredPatch: StructuredPatchHunk[];
  firstLine: string | null;
  fileContent?: string;
  style?: 'condensed';
  verbose: boolean;
  previewHint?: string;
};
export function FileEditToolUpdatedMessage(t0) {
  const $ = _c(22);
  const {
    filePath,
    structuredPatch,
    firstLine,
    fileContent,
    style,
    verbose,
    previewHint
  } = t0;
  const {
    columns
  } = useTerminalSize();
  const numAdditions = structuredPatch.reduce(_temp2, 0);
  const numRemovals = structuredPatch.reduce(_temp4, 0);
  let t1;
  if ($[0] !== numAdditions) {
    t1 = numAdditions > 0 ? <>Added <Text bold={true}>{numAdditions}</Text>{" "}{numAdditions > 1 ? "lines" : "line"}</> : null;
    $[0] = numAdditions;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const t2 = numAdditions > 0 && numRemovals > 0 ? ", " : null;
  let t3;
  if ($[2] !== numAdditions || $[3] !== numRemovals) {
    t3 = numRemovals > 0 ? <>{numAdditions === 0 ? "R" : "r"}emoved <Text bold={true}>{numRemovals}</Text>{" "}{numRemovals > 1 ? "lines" : "line"}</> : null;
    $[2] = numAdditions;
    $[3] = numRemovals;
    $[4] = t3;
  } else {
    t3 = $[4];

```

---


### `src/components/FileEditToolUseRejectedMessage.tsx`

**信息:**
- 行数: 170
- 大小: 15126 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { StructuredPatchHunk } from 'diff';
import { relative } from 'path';
import * as React from 'react';
import { useTerminalSize } from 'src/hooks/useTerminalSize.js';
import { getCwd } from 'src/utils/cwd.js';
import { Box, Text } from '../ink.js';
import { HighlightedCode } from './HighlightedCode.js';
import { MessageResponse } from './MessageResponse.js';
import { StructuredDiffList } from './StructuredDiffList.js';
const MAX_LINES_TO_RENDER = 10;
type Props = {
  file_path: string;
  operation: 'write' | 'update';
  // For updates - show diff
  patch?: StructuredPatchHunk[];
  firstLine: string | null;
  fileContent?: string;
  // For new file creation - show content preview
  content?: string;
  style?: 'condensed';
  verbose: boolean;
};
export function FileEditToolUseRejectedMessage(t0) {
  const $ = _c(38);
  const {
    file_path,
    operation,
    patch,
    firstLine,
    fileContent,
    content,
    style,
    verbose
  } = t0;
  const {
    columns
  } = useTerminalSize();
  let t1;
  if ($[0] !== operation) {
    t1 = <Text color="subtle">User rejected {operation} to </Text>;
    $[0] = operation;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] !== file_path || $[3] !== verbose) {
    t2 = verbose ? file_path : relative(getCwd(), file_path);
    $[2] = file_path;

```

---


### `src/components/FilePathLink.tsx`

**信息:**
- 行数: 43
- 大小: 3242 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { pathToFileURL } from 'url';
import Link from '../ink/components/Link.js';
type Props = {
  /** The absolute file path */
  filePath: string;
  /** Optional display text (defaults to filePath) */
  children?: React.ReactNode;
};

/**
 * Renders a file path as an OSC 8 hyperlink.
 * This helps terminals like iTerm correctly identify file paths
 * even when they appear inside parentheses or other text.
 */
export function FilePathLink(t0) {
  const $ = _c(5);
  const {
    filePath,
    children
  } = t0;
  let t1;
  if ($[0] !== filePath) {
    t1 = pathToFileURL(filePath);
    $[0] = filePath;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const t2 = children ?? filePath;
  let t3;
  if ($[2] !== t1.href || $[3] !== t2) {
    t3 = <Link url={t1.href}>{t2}</Link>;
    $[2] = t1.href;
    $[3] = t2;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  return t3;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsInBhdGhUb0ZpbGVVUkwiLCJMaW5rIiwiUHJvcHMiLCJmaWxlUGF0aCIsImNoaWxkcmVuIiwiUmVhY3ROb2RlIiwiRmlsZVBhdGhMaW5rIiwidDAiLCIkIiwiX2MiLCJ0MSIsInQyIiwidDMiLCJocmVmIl0sInNvdXJjZXMiOlsiRmlsZVBhdGhMaW5rLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBwYXRoVG9GaWxlVVJMIH0gZnJvbSAndXJsJ1xuaW1wb3J0IExpbmsgZnJvbSAnLi4vaW5rL2NvbXBvbmVudHMvTGluay5qcydcblxudHlwZSBQcm9wcyA9IHtcbiAgLyoqIFRoZSBhYnNvbHV0ZSBmaWxlIHBhdGggKi9cbiAgZmlsZVBhdGg6IHN0cmluZ1xuICAvKiogT3B0aW9uYWwgZGlzcGxheSB0ZXh0IChkZWZhdWx0cyB0byBmaWxlUGF0aCkgKi9cbiAgY2hpbGRyZW4/OiBSZWFjdC5SZWFjdE5vZGVcbn1cblxuLyoqXG4gKiBSZW5kZXJzIGEgZmlsZSBwYXRoIGFzIGFuIE9TQyA4IGh5cGVybGluay5cbiAqIFRoaXMgaGVscHMgdGVybWluYWxzIGxpa2UgaVRlcm0gY29ycmVjdGx5IGlkZW50aWZ5IGZpbGUgcGF0aHNcbiAqIGV2ZW4gd2hlbiB0aGV5IGFwcGVhciBpbnNpZGUgcGFyZW50aGVzZXMgb3Igb3RoZXIgdGV4dC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIEZpbGVQYXRoTGluayh7IGZpbGVQYXRoLCBjaGlsZHJlbiB9OiBQcm9wcyk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIHJldHVybiA8TGluayB1cmw9e3BhdGhUb0ZpbGVVUkwoZmlsZVBhdGgpLmhyZWZ9PntjaGlsZHJlbiA/PyBmaWxlUGF0aH08L0xpbms+XG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxPQUFPQSxLQUFLLE1BQU0sT0FBTztBQUN6QixTQUFTQyxhQUFhLFFBQVEsS0FBSztBQUNuQyxPQUFPQyxJQUFJLE1BQU0sMkJBQTJCO0FBRTVDLEtBQUtDLEtBQUssR0FBRztFQUNYO0VBQ0FDLFFBQVEsRUFBRSxNQUFNO0VBQ2hCO0VBQ0FDLFFBQVEsQ0FBQyxFQUFFTCxLQUFLLENBQUNNLFNBQVM7QUFDNUIsQ0FBQzs7QUFFRDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTyxTQUFBQyxhQUFBQyxFQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQXNCO0lBQUFOLFFBQUE7SUFBQUM7RUFBQSxJQUFBRyxFQUE2QjtFQUFBLElBQUFHLEVBQUE7RUFBQSxJQUFBRixDQUFBLFFBQUFMLFFBQUE7SUFDdENPLEVBQUEsR0FBQVYsYUFBYSxDQUFDRyxRQUFRLENBQUM7SUFBQUssQ0FBQSxNQUFBTCxRQUFBO0lBQUFLLENBQUEsTUFBQUUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUYsQ0FBQTtFQUFBO0VBQVEsTUFBQUcsRUFBQSxHQUFBUCxRQUFvQixJQUFwQkQsUUFBb0I7RUFBQSxJQUFBUyxFQUFBO0VBQUEsSUFBQUosQ0FBQSxRQUFBRSxFQUFBLENBQUFHLElBQUEsSUFBQUwsQ0FBQSxRQUFBRyxFQUFBO0lBQTlEQyxFQUFBLElBQUMsSUFBSSxDQUFNLEdBQTRCLENBQTVCLENBQUFGLEVBQXVCLENBQUFHLElBQUksQ0FBQyxDQUFHLENBQUFGLEVBQW1CLENBQUUsRUFBOUQsSUFBSSxDQUFpRTtJQUFBSCxDQUFBLE1BQUFFLEVBQUEsQ0FBQUcsSUFBQTtJQUFBTCxDQUFBLE1BQUFHLEVBQUE7SUFBQUgsQ0FBQSxNQUFBSSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBSixDQUFBO0VBQUE7RUFBQSxPQUF0RUksRUFBc0U7QUFBQSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/components/FullscreenLayout.tsx`

**信息:**
- 行数: 637
- 大小: 84913 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { createContext, type ReactNode, type RefObject, useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import { fileURLToPath } from 'url';
import { ModalContext } from '../context/modalContext.js';
import { PromptOverlayProvider, usePromptOverlay, usePromptOverlayDialog } from '../context/promptOverlayContext.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import ScrollBox, { type ScrollBoxHandle } from '../ink/components/ScrollBox.js';
import instances from '../ink/instances.js';
import { Box, Text } from '../ink.js';
import type { Message } from '../types/message.js';
import { openBrowser, openPath } from '../utils/browser.js';
import { isFullscreenEnvEnabled } from '../utils/fullscreen.js';
import { plural } from '../utils/stringUtils.js';
import { isNullRenderingAttachment } from './messages/nullRenderingAttachments.js';
import PromptInputFooterSuggestions from './PromptInput/PromptInputFooterSuggestions.js';
import type { StickyPrompt } from './VirtualMessageList.js';

/** Rows of transcript context kept visible above the modal pane's ▔ divider. */
const MODAL_TRANSCRIPT_PEEK = 2;

/** Context for scroll-derived chrome (sticky header, pill). StickyTracker
 *  in VirtualMessageList writes via this instead of threading a callback
 *  up through Messages → REPL → FullscreenLayout. The setter is stable so
 *  consuming this context never causes re-renders. */
export const ScrollChromeContext = createContext<{
  setStickyPrompt: (p: StickyPrompt | null) => void;
}>({
  setStickyPrompt: () => {}
});
type Props = {
  /** Content that scrolls (messages, tool output) */
  scrollable: ReactNode;
  /** Content pinned to the bottom (spinner, prompt, permissions) */
  bottom: ReactNode;
  /** Content rendered inside the ScrollBox after messages — user can scroll
   *  up to see context while it's showing (used by PermissionRequest). */
  overlay?: ReactNode;
  /** Absolute-positioned content anchored at the bottom-right of the
   *  ScrollBox area, floating over scrollback. Rendered inside the flexGrow
   *  region (not the bottom slot) so the overflowY:hidden cap doesn't clip
   *  it. Fullscreen only — used for the companion speech bubble. */
  bottomFloat?: ReactNode;
  /** Slash-command dialog content. Rendered in an absolute-positioned
   *  bottom-anchored pane (▔ divider, paddingX=2) that paints over the
   *  ScrollBox AND bottom slot. Provides ModalContext so Pane/Dialog inside
   *  skip their own frame. Fullscreen only; inline after overlay otherwise. */
  modal?: ReactNode;
  /** Ref passed via ModalContext so Tabs (or any scroll-owning descendant)
   *  can attach it to their own ScrollBox for tall content. */

```

---


### `src/components/GlobalSearchDialog.tsx`

**信息:**
- 行数: 343
- 大小: 43997 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { resolve as resolvePath } from 'path';
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { useRegisterOverlay } from '../context/overlayContext.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { Text } from '../ink.js';
import { logEvent } from '../services/analytics/index.js';
import { getCwd } from '../utils/cwd.js';
import { openFileInExternalEditor } from '../utils/editor.js';
import { truncatePathMiddle, truncateToWidth } from '../utils/format.js';
import { highlightMatch } from '../utils/highlightMatch.js';
import { relativePath } from '../utils/permissions/filesystem.js';
import { readFileInRange } from '../utils/readFileInRange.js';
import { ripGrepStream } from '../utils/ripgrep.js';
import { FuzzyPicker } from './design-system/FuzzyPicker.js';
import { LoadingState } from './design-system/LoadingState.js';
type Props = {
  onDone: () => void;
  onInsert: (text: string) => void;
};
type Match = {
  file: string;
  line: number;
  text: string;
};
const VISIBLE_RESULTS = 12;
const DEBOUNCE_MS = 100;
const PREVIEW_CONTEXT_LINES = 4;
// rg -m is per-file; we also cap the parsed array to keep memory bounded.
const MAX_MATCHES_PER_FILE = 10;
const MAX_TOTAL_MATCHES = 500;

/**
 * Global Search dialog (ctrl+shift+f / cmd+shift+f).
 * Debounced ripgrep search across the workspace.
 */
export function GlobalSearchDialog(t0) {
  const $ = _c(40);
  const {
    onDone,
    onInsert
  } = t0;
  useRegisterOverlay("global-search");
  const {
    columns,
    rows
  } = useTerminalSize();
  const previewOnRight = columns >= 140;
  const visibleResults = Math.min(VISIBLE_RESULTS, Math.max(4, rows - 14));

```

---


### `src/components/HelpV2/Commands.tsx`

**信息:**
- 行数: 82
- 大小: 9738 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useMemo } from 'react';
import { type Command, formatDescriptionWithSource } from '../../commands.js';
import { Box, Text } from '../../ink.js';
import { truncate } from '../../utils/format.js';
import { Select } from '../CustomSelect/select.js';
import { useTabHeaderFocus } from '../design-system/Tabs.js';
type Props = {
  commands: Command[];
  maxHeight: number;
  columns: number;
  title: string;
  onCancel: () => void;
  emptyMessage?: string;
};
export function Commands(t0) {
  const $ = _c(14);
  const {
    commands,
    maxHeight,
    columns,
    title,
    onCancel,
    emptyMessage
  } = t0;
  const {
    headerFocused,
    focusHeader
  } = useTabHeaderFocus();
  const maxWidth = Math.max(1, columns - 10);
  const visibleCount = Math.max(1, Math.floor((maxHeight - 10) / 2));
  let t1;
  if ($[0] !== commands || $[1] !== maxWidth) {
    const seen = new Set();
    let t2;
    if ($[3] !== maxWidth) {
      t2 = cmd_0 => ({
        label: `/${cmd_0.name}`,
        value: cmd_0.name,
        description: truncate(formatDescriptionWithSource(cmd_0), maxWidth, true)
      });
      $[3] = maxWidth;
      $[4] = t2;
    } else {
      t2 = $[4];
    }
    t1 = commands.filter(cmd => {
      if (seen.has(cmd.name)) {
        return false;

```

---


### `src/components/HelpV2/General.tsx`

**信息:**
- 行数: 23
- 大小: 3101 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { PromptInputHelpMenu } from '../PromptInput/PromptInputHelpMenu.js';
export function General() {
  const $ = _c(2);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <Box><Text>Claude understands your codebase, makes edits with your permission, and executes commands — right from your terminal.</Text></Box>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  let t1;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Box flexDirection="column" paddingY={1} gap={1}>{t0}<Box flexDirection="column"><Box><Text bold={true}>Shortcuts</Text></Box><PromptInputHelpMenu gap={2} fixedWidth={true} /></Box></Box>;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  return t1;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJveCIsIlRleHQiLCJQcm9tcHRJbnB1dEhlbHBNZW51IiwiR2VuZXJhbCIsIiQiLCJfYyIsInQwIiwiU3ltYm9sIiwiZm9yIiwidDEiXSwic291cmNlcyI6WyJHZW5lcmFsLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IEJveCwgVGV4dCB9IGZyb20gJy4uLy4uL2luay5qcydcbmltcG9ydCB7IFByb21wdElucHV0SGVscE1lbnUgfSBmcm9tICcuLi9Qcm9tcHRJbnB1dC9Qcm9tcHRJbnB1dEhlbHBNZW51LmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gR2VuZXJhbCgpOiBSZWFjdC5SZWFjdE5vZGUge1xuICByZXR1cm4gKFxuICAgIDxCb3ggZmxleERpcmVjdGlvbj1cImNvbHVtblwiIHBhZGRpbmdZPXsxfSBnYXA9ezF9PlxuICAgICAgPEJveD5cbiAgICAgICAgPFRleHQ+XG4gICAgICAgICAgQ2xhdWRlIHVuZGVyc3RhbmRzIHlvdXIgY29kZWJhc2UsIG1ha2VzIGVkaXRzIHdpdGggeW91ciBwZXJtaXNzaW9uLFxuICAgICAgICAgIGFuZCBleGVjdXRlcyBjb21tYW5kcyDigJQgcmlnaHQgZnJvbSB5b3VyIHRlcm1pbmFsLlxuICAgICAgICA8L1RleHQ+XG4gICAgICA8L0JveD5cbiAgICAgIDxCb3ggZmxleERpcmVjdGlvbj1cImNvbHVtblwiPlxuICAgICAgICA8Qm94PlxuICAgICAgICAgIDxUZXh0IGJvbGQ+U2hvcnRjdXRzPC9UZXh0PlxuICAgICAgICA8L0JveD5cbiAgICAgICAgPFByb21wdElucHV0SGVscE1lbnUgZ2FwPXsyfSBmaXhlZFdpZHRoPXt0cnVlfSAvPlxuICAgICAgPC9Cb3g+XG4gICAgPC9Cb3g+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsR0FBRyxFQUFFQyxJQUFJLFFBQVEsY0FBYztBQUN4QyxTQUFTQyxtQkFBbUIsUUFBUSx1Q0FBdUM7QUFFM0UsT0FBTyxTQUFBQyxRQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQUEsSUFBQUMsRUFBQTtFQUFBLElBQUFGLENBQUEsUUFBQUcsTUFBQSxDQUFBQyxHQUFBO0lBR0RGLEVBQUEsSUFBQyxHQUFHLENBQ0YsQ0FBQyxJQUFJLENBQUMscUhBR04sRUFIQyxJQUFJLENBSVAsRUFMQyxHQUFHLENBS0U7SUFBQUYsQ0FBQSxNQUFBRSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBRixDQUFBO0VBQUE7RUFBQSxJQUFBSyxFQUFBO0VBQUEsSUFBQUwsQ0FBQSxRQUFBRyxNQUFBLENBQUFDLEdBQUE7SUFOUkMsRUFBQSxJQUFDLEdBQUcsQ0FBZSxhQUFRLENBQVIsUUFBUSxDQUFXLFFBQUMsQ0FBRCxHQUFDLENBQU8sR0FBQyxDQUFELEdBQUMsQ0FDN0MsQ0FBQUgsRUFLSyxDQUNMLENBQUMsR0FBRyxDQUFlLGFBQVEsQ0FBUixRQUFRLENBQ3pCLENBQUMsR0FBRyxDQUNGLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBSixLQUFHLENBQUMsQ0FBQyxTQUFTLEVBQW5CLElBQUksQ0FDUCxFQUZDLEdBQUcsQ0FHSixDQUFDLG1CQUFtQixDQUFNLEdBQUMsQ0FBRCxHQUFDLENBQWMsVUFBSSxDQUFKLEtBQUcsQ0FBQyxHQUMvQyxFQUxDLEdBQUcsQ0FNTixFQWJDLEdBQUcsQ0FhRTtJQUFBRixDQUFBLE1BQUFLLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFMLENBQUE7RUFBQTtFQUFBLE9BYk5LLEVBYU07QUFBQSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/components/HelpV2/HelpV2.tsx`

**信息:**
- 行数: 184
- 大小: 20986 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useExitOnCtrlCDWithKeybindings } from 'src/hooks/useExitOnCtrlCDWithKeybindings.js';
import { useShortcutDisplay } from 'src/keybindings/useShortcutDisplay.js';
import { builtInCommandNames, type Command, type CommandResultDisplay, INTERNAL_ONLY_COMMANDS } from '../../commands.js';
import { useIsInsideModal } from '../../context/modalContext.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { Box, Link, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { Pane } from '../design-system/Pane.js';
import { Tab, Tabs } from '../design-system/Tabs.js';
import { Commands } from './Commands.js';
import { General } from './General.js';
type Props = {
  onClose: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  commands: Command[];
};
export function HelpV2(t0) {
  const $ = _c(44);
  const {
    onClose,
    commands
  } = t0;
  const {
    rows,
    columns
  } = useTerminalSize();
  const maxHeight = Math.floor(rows / 2);
  const insideModal = useIsInsideModal();
  let t1;
  if ($[0] !== onClose) {
    t1 = () => onClose("Help dialog dismissed", {
      display: "system"
    });
    $[0] = onClose;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const close = t1;
  let t2;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = {
      context: "Help"
    };
    $[2] = t2;
  } else {
    t2 = $[2];

```

---


### `src/components/HighlightedCode/Fallback.tsx`

**信息:**
- 行数: 193
- 大小: 16263 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { extname } from 'path';
import React, { Suspense, use, useMemo } from 'react';
import { Ansi, Text } from '../../ink.js';
import { getCliHighlightPromise } from '../../utils/cliHighlight.js';
import { logForDebugging } from '../../utils/debug.js';
import { convertLeadingTabsToSpaces } from '../../utils/file.js';
import { hashPair } from '../../utils/hash.js';
type Props = {
  code: string;
  filePath: string;
  dim?: boolean;
  skipColoring?: boolean;
};

// Module-level highlight cache — hl.highlight() is the hot cost on virtual-
// scroll remounts. useMemo doesn't survive unmount→remount. Keyed by hash
// of code+language to avoid retaining full source strings (#24180 RSS fix).
const HL_CACHE_MAX = 500;
const hlCache = new Map<string, string>();
function cachedHighlight(hl: NonNullable<Awaited<ReturnType<typeof getCliHighlightPromise>>>, code: string, language: string): string {
  const key = hashPair(language, code);
  const hit = hlCache.get(key);
  if (hit !== undefined) {
    hlCache.delete(key);
    hlCache.set(key, hit);
    return hit;
  }
  const out = hl.highlight(code, {
    language
  });
  if (hlCache.size >= HL_CACHE_MAX) {
    const first = hlCache.keys().next().value;
    if (first !== undefined) hlCache.delete(first);
  }
  hlCache.set(key, out);
  return out;
}
export function HighlightedCodeFallback(t0) {
  const $ = _c(20);
  const {
    code,
    filePath,
    dim: t1,
    skipColoring: t2
  } = t0;
  const dim = t1 === undefined ? false : t1;
  const skipColoring = t2 === undefined ? false : t2;
  let t3;
  if ($[0] !== code) {

```

---


### `src/components/HighlightedCode.tsx`

**信息:**
- 行数: 190
- 大小: 17579 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { memo, useEffect, useMemo, useRef, useState } from 'react';
import { useSettings } from '../hooks/useSettings.js';
import { Ansi, Box, type DOMElement, measureElement, NoSelect, Text, useTheme } from '../ink.js';
import { isFullscreenEnvEnabled } from '../utils/fullscreen.js';
import sliceAnsi from '../utils/sliceAnsi.js';
import { countCharInString } from '../utils/stringUtils.js';
import { HighlightedCodeFallback } from './HighlightedCode/Fallback.js';
import { expectColorFile } from './StructuredDiff/colorDiff.js';
type Props = {
  code: string;
  filePath: string;
  width?: number;
  dim?: boolean;
};
const DEFAULT_WIDTH = 80;
export const HighlightedCode = memo(function HighlightedCode(t0) {
  const $ = _c(21);
  const {
    code,
    filePath,
    width,
    dim: t1
  } = t0;
  const dim = t1 === undefined ? false : t1;
  const ref = useRef(null);
  const [measuredWidth, setMeasuredWidth] = useState(width || DEFAULT_WIDTH);
  const [theme] = useTheme();
  const settings = useSettings();
  const syntaxHighlightingDisabled = settings.syntaxHighlightingDisabled ?? false;
  let t2;
  bb0: {
    if (syntaxHighlightingDisabled) {
      t2 = null;
      break bb0;
    }
    let t3;
    if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
      t3 = expectColorFile();
      $[0] = t3;
    } else {
      t3 = $[0];
    }
    const ColorFile = t3;
    if (!ColorFile) {
      t2 = null;
      break bb0;
    }
    let t4;

```

---


### `src/components/HistorySearchDialog.tsx`

**信息:**
- 行数: 118
- 大小: 19923 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { useEffect, useMemo, useState } from 'react';
import { useRegisterOverlay } from '../context/overlayContext.js';
import { getTimestampedHistory, type TimestampedHistoryEntry } from '../history.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { stringWidth } from '../ink/stringWidth.js';
import { wrapAnsi } from '../ink/wrapAnsi.js';
import { Box, Text } from '../ink.js';
import { logEvent } from '../services/analytics/index.js';
import type { HistoryEntry } from '../utils/config.js';
import { formatRelativeTimeAgo, truncateToWidth } from '../utils/format.js';
import { FuzzyPicker } from './design-system/FuzzyPicker.js';
type Props = {
  initialQuery?: string;
  onSelect: (entry: HistoryEntry) => void;
  onCancel: () => void;
};
const PREVIEW_ROWS = 6;
const AGE_WIDTH = 8;
type Item = {
  entry: TimestampedHistoryEntry;
  display: string;
  lower: string;
  firstLine: string;
  age: string;
};
export function HistorySearchDialog({
  initialQuery,
  onSelect,
  onCancel
}: Props): React.ReactNode {
  useRegisterOverlay('history-search');
  const {
    columns
  } = useTerminalSize();
  const [items, setItems] = useState<Item[] | null>(null);
  const [query, setQuery] = useState(initialQuery ?? '');
  useEffect(() => {
    let cancelled = false;
    void (async () => {
      const reader = getTimestampedHistory();
      const loaded: Item[] = [];
      for await (const entry of reader) {
        if (cancelled) {
          void reader.return(undefined);
          return;
        }
        const display = entry.display;
        const nl = display.indexOf('\n');
        const age = formatRelativeTimeAgo(new Date(entry.timestamp));

```

---


### `src/components/IdeAutoConnectDialog.tsx`

**信息:**
- 行数: 154
- 大小: 13271 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback } from 'react';
import { Text } from '../ink.js';
import { getGlobalConfig, saveGlobalConfig } from '../utils/config.js';
import { isSupportedTerminal } from '../utils/ide.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
type IdeAutoConnectDialogProps = {
  onComplete: () => void;
};
export function IdeAutoConnectDialog(t0) {
  const $ = _c(9);
  const {
    onComplete
  } = t0;
  let t1;
  if ($[0] !== onComplete) {
    t1 = async value => {
      const autoConnect = value === "yes";
      saveGlobalConfig(current => ({
        ...current,
        autoConnectIde: autoConnect,
        hasIdeAutoConnectDialogBeenShown: true
      }));
      onComplete();
    };
    $[0] = onComplete;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const handleSelect = t1;
  let t2;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = [{
      label: "Yes",
      value: "yes"
    }, {
      label: "No",
      value: "no"
    }];
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  const options = t2;
  let t3;
  if ($[3] !== handleSelect) {
    t3 = <Select options={options} onChange={handleSelect} defaultValue="yes" />;
    $[3] = handleSelect;

```

---


### `src/components/IdeOnboardingDialog.tsx`

**信息:**
- 行数: 167
- 大小: 16399 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { envDynamic } from 'src/utils/envDynamic.js';
import { Box, Text } from '../ink.js';
import { useKeybindings } from '../keybindings/useKeybinding.js';
import { getGlobalConfig, saveGlobalConfig } from '../utils/config.js';
import { env } from '../utils/env.js';
import { getTerminalIdeType, type IDEExtensionInstallationStatus, isJetBrainsIde, toIDEDisplayName } from '../utils/ide.js';
import { Dialog } from './design-system/Dialog.js';
interface Props {
  onDone: () => void;
  installationStatus: IDEExtensionInstallationStatus | null;
}
export function IdeOnboardingDialog(t0) {
  const $ = _c(23);
  const {
    onDone,
    installationStatus
  } = t0;
  markDialogAsShown();
  let t1;
  if ($[0] !== onDone) {
    t1 = {
      "confirm:yes": onDone,
      "confirm:no": onDone
    };
    $[0] = onDone;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = {
      context: "Confirmation"
    };
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  useKeybindings(t1, t2);
  let t3;
  if ($[3] !== installationStatus?.ideType) {
    t3 = installationStatus?.ideType ?? getTerminalIdeType();
    $[3] = installationStatus?.ideType;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  const ideType = t3;

```

---


### `src/components/IdeStatusIndicator.tsx`

**信息:**
- 行数: 58
- 大小: 6430 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { basename } from 'path';
import * as React from 'react';
import { useIdeConnectionStatus } from '../hooks/useIdeConnectionStatus.js';
import type { IDESelection } from '../hooks/useIdeSelection.js';
import { Text } from '../ink.js';
import type { MCPServerConnection } from '../services/mcp/types.js';
type IdeStatusIndicatorProps = {
  ideSelection: IDESelection | undefined;
  mcpClients?: MCPServerConnection[];
};
export function IdeStatusIndicator(t0) {
  const $ = _c(7);
  const {
    ideSelection,
    mcpClients
  } = t0;
  const {
    status: ideStatus
  } = useIdeConnectionStatus(mcpClients);
  const shouldShowIdeSelection = ideStatus === "connected" && (ideSelection?.filePath || ideSelection?.text && ideSelection.lineCount > 0);
  if (ideStatus === null || !shouldShowIdeSelection || !ideSelection) {
    return null;
  }
  if (ideSelection.text && ideSelection.lineCount > 0) {
    const t1 = ideSelection.lineCount === 1 ? "line" : "lines";
    let t2;
    if ($[0] !== ideSelection.lineCount || $[1] !== t1) {
      t2 = <Text color="ide" key="selection-indicator" wrap="truncate">⧉ {ideSelection.lineCount}{" "}{t1} selected</Text>;
      $[0] = ideSelection.lineCount;
      $[1] = t1;
      $[2] = t2;
    } else {
      t2 = $[2];
    }
    return t2;
  }
  if (ideSelection.filePath) {
    let t1;
    if ($[3] !== ideSelection.filePath) {
      t1 = basename(ideSelection.filePath);
      $[3] = ideSelection.filePath;
      $[4] = t1;
    } else {
      t1 = $[4];
    }
    let t2;
    if ($[5] !== t1) {
      t2 = <Text color="ide" key="selection-indicator" wrap="truncate">⧉ In {t1}</Text>;
      $[5] = t1;

```

---


### `src/components/IdleReturnDialog.tsx`

**信息:**
- 行数: 118
- 大小: 9861 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../ink.js';
import { formatTokens } from '../utils/format.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
type IdleReturnAction = 'continue' | 'clear' | 'dismiss' | 'never';
type Props = {
  idleMinutes: number;
  totalInputTokens: number;
  onDone: (action: IdleReturnAction) => void;
};
export function IdleReturnDialog(t0) {
  const $ = _c(16);
  const {
    idleMinutes,
    totalInputTokens,
    onDone
  } = t0;
  let t1;
  if ($[0] !== idleMinutes) {
    t1 = formatIdleDuration(idleMinutes);
    $[0] = idleMinutes;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const formattedIdle = t1;
  let t2;
  if ($[2] !== totalInputTokens) {
    t2 = formatTokens(totalInputTokens);
    $[2] = totalInputTokens;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  const formattedTokens = t2;
  const t3 = `You've been away ${formattedIdle} and this conversation is ${formattedTokens} tokens.`;
  let t4;
  if ($[4] !== onDone) {
    t4 = () => onDone("dismiss");
    $[4] = onDone;
    $[5] = t4;
  } else {
    t4 = $[5];
  }
  let t5;
  if ($[6] === Symbol.for("react.memo_cache_sentinel")) {
    t5 = <Box flexDirection="column"><Text>If this is a new task, clearing context will save usage and be faster.</Text></Box>;
    $[6] = t5;

```

---


### `src/components/InterruptedByUser.tsx`

**信息:**
- 行数: 15
- 大小: 1962 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Text } from '../ink.js';
export function InterruptedByUser() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <><Text dimColor={true}>Interrupted </Text>{false ? <Text dimColor={true}>· [ANT-ONLY] /issue to report a model issue</Text> : <Text dimColor={true}>· What should Claude do instead?</Text>}</>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlRleHQiLCJJbnRlcnJ1cHRlZEJ5VXNlciIsIiQiLCJfYyIsInQwIiwiU3ltYm9sIiwiZm9yIl0sInNvdXJjZXMiOlsiSW50ZXJydXB0ZWRCeVVzZXIudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgVGV4dCB9IGZyb20gJy4uL2luay5qcydcblxuZXhwb3J0IGZ1bmN0aW9uIEludGVycnVwdGVkQnlVc2VyKCk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIHJldHVybiAoXG4gICAgPD5cbiAgICAgIDxUZXh0IGRpbUNvbG9yPkludGVycnVwdGVkIDwvVGV4dD5cbiAgICAgIHtcImV4dGVybmFsXCIgPT09ICdhbnQnID8gKFxuICAgICAgICA8VGV4dCBkaW1Db2xvcj7CtyBbQU5ULU9OTFldIC9pc3N1ZSB0byByZXBvcnQgYSBtb2RlbCBpc3N1ZTwvVGV4dD5cbiAgICAgICkgOiAoXG4gICAgICAgIDxUZXh0IGRpbUNvbG9yPsK3IFdoYXQgc2hvdWxkIENsYXVkZSBkbyBpbnN0ZWFkPzwvVGV4dD5cbiAgICAgICl9XG4gICAgPC8+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsSUFBSSxRQUFRLFdBQVc7QUFFaEMsT0FBTyxTQUFBQyxrQkFBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUFBLElBQUFDLEVBQUE7RUFBQSxJQUFBRixDQUFBLFFBQUFHLE1BQUEsQ0FBQUMsR0FBQTtJQUVIRixFQUFBLEtBQ0UsQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFSLEtBQU8sQ0FBQyxDQUFDLFlBQVksRUFBMUIsSUFBSSxDQUNKLE1BQW9CLEdBQ25CLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBUixLQUFPLENBQUMsQ0FBQywyQ0FBMkMsRUFBekQsSUFBSSxDQUdOLEdBREMsQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFSLEtBQU8sQ0FBQyxDQUFDLGdDQUFnQyxFQUE5QyxJQUFJLENBQ1AsQ0FBQyxHQUNBO0lBQUFGLENBQUEsTUFBQUUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUYsQ0FBQTtFQUFBO0VBQUEsT0FQSEUsRUFPRztBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/InvalidConfigDialog.tsx`

**信息:**
- 行数: 156
- 大小: 15252 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, render, Text } from '../ink.js';
import { KeybindingSetup } from '../keybindings/KeybindingProviderSetup.js';
import { AppStateProvider } from '../state/AppState.js';
import type { ConfigParseError } from '../utils/errors.js';
import { getBaseRenderOptions } from '../utils/renderOptions.js';
import { jsonStringify, writeFileSync_DEPRECATED } from '../utils/slowOperations.js';
import type { ThemeName } from '../utils/theme.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
interface InvalidConfigHandlerProps {
  error: ConfigParseError;
}
interface InvalidConfigDialogProps {
  filePath: string;
  errorDescription: string;
  onExit: () => void;
  onReset: () => void;
}

/**
 * Dialog shown when the Claude config file contains invalid JSON
 */
function InvalidConfigDialog(t0) {
  const $ = _c(19);
  const {
    filePath,
    errorDescription,
    onExit,
    onReset
  } = t0;
  let t1;
  if ($[0] !== onExit || $[1] !== onReset) {
    t1 = value => {
      if (value === "exit") {
        onExit();
      } else {
        onReset();
      }
    };
    $[0] = onExit;
    $[1] = onReset;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  const handleSelect = t1;
  let t2;
  if ($[3] !== filePath) {

```

---


### `src/components/InvalidSettingsDialog.tsx`

**信息:**
- 行数: 89
- 大小: 7063 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Text } from '../ink.js';
import type { ValidationError } from '../utils/settings/validation.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
import { ValidationErrorsList } from './ValidationErrorsList.js';
type Props = {
  settingsErrors: ValidationError[];
  onContinue: () => void;
  onExit: () => void;
};

/**
 * Dialog shown when settings files have validation errors.
 * User must choose to continue (skipping invalid files) or exit to fix them.
 */
export function InvalidSettingsDialog(t0) {
  const $ = _c(13);
  const {
    settingsErrors,
    onContinue,
    onExit
  } = t0;
  let t1;
  if ($[0] !== onContinue || $[1] !== onExit) {
    t1 = function handleSelect(value) {
      if (value === "exit") {
        onExit();
      } else {
        onContinue();
      }
    };
    $[0] = onContinue;
    $[1] = onExit;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  const handleSelect = t1;
  let t2;
  if ($[3] !== settingsErrors) {
    t2 = <ValidationErrorsList errors={settingsErrors} />;
    $[3] = settingsErrors;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  let t3;
  if ($[5] === Symbol.for("react.memo_cache_sentinel")) {

```

---


### `src/components/KeybindingWarnings.tsx`

**信息:**
- 行数: 55
- 大小: 9534 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../ink.js';
import { getCachedKeybindingWarnings, getKeybindingsPath, isKeybindingCustomizationEnabled } from '../keybindings/loadUserBindings.js';

/**
 * Displays keybinding validation warnings in the UI.
 * Similar to McpParsingWarnings, this provides persistent visibility
 * of configuration issues.
 *
 * Only shown when keybinding customization is enabled (ant users + feature gate).
 */
export function KeybindingWarnings() {
  const $ = _c(2);
  if (!isKeybindingCustomizationEnabled()) {
    return null;
  }
  let t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = Symbol.for("react.early_return_sentinel");
    bb0: {
      const warnings = getCachedKeybindingWarnings();
      if (warnings.length === 0) {
        t1 = null;
        break bb0;
      }
      const errors = warnings.filter(_temp);
      const warns = warnings.filter(_temp2);
      t0 = <Box flexDirection="column" marginTop={1} marginBottom={1}><Text bold={true} color={errors.length > 0 ? "error" : "warning"}>Keybinding Configuration Issues</Text><Box><Text dimColor={true}>Location: </Text><Text dimColor={true}>{getKeybindingsPath()}</Text></Box><Box marginLeft={1} flexDirection="column" marginTop={1}>{errors.map(_temp3)}{warns.map(_temp4)}</Box></Box>;
    }
    $[0] = t0;
    $[1] = t1;
  } else {
    t0 = $[0];
    t1 = $[1];
  }
  if (t1 !== Symbol.for("react.early_return_sentinel")) {
    return t1;
  }
  return t0;
}
function _temp4(warning, i_0) {
  return <Box key={`warning-${i_0}`} flexDirection="column"><Box><Text dimColor={true}>└ </Text><Text color="warning">[Warning]</Text><Text dimColor={true}> {warning.message}</Text></Box>{warning.suggestion && <Box marginLeft={3}><Text dimColor={true}>→ {warning.suggestion}</Text></Box>}</Box>;
}
function _temp3(error, i) {
  return <Box key={`error-${i}`} flexDirection="column"><Box><Text dimColor={true}>└ </Text><Text color="error">[Error]</Text><Text dimColor={true}> {error.message}</Text></Box>{error.suggestion && <Box marginLeft={3}><Text dimColor={true}>→ {error.suggestion}</Text></Box>}</Box>;
}
function _temp2(w_0) {
  return w_0.severity === "warning";

```

---


### `src/components/LanguagePicker.tsx`

**信息:**
- 行数: 86
- 大小: 8664 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { useState } from 'react';
import { Box, Text } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import TextInput from './TextInput.js';
type Props = {
  initialLanguage: string | undefined;
  onComplete: (language: string | undefined) => void;
  onCancel: () => void;
};
export function LanguagePicker(t0) {
  const $ = _c(13);
  const {
    initialLanguage,
    onComplete,
    onCancel
  } = t0;
  const [language, setLanguage] = useState(initialLanguage);
  const [cursorOffset, setCursorOffset] = useState((initialLanguage ?? "").length);
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = {
      context: "Settings"
    };
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  useKeybinding("confirm:no", onCancel, t1);
  let t2;
  if ($[1] !== language || $[2] !== onComplete) {
    t2 = function handleSubmit() {
      const trimmed = language?.trim();
      onComplete(trimmed || undefined);
    };
    $[1] = language;
    $[2] = onComplete;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  const handleSubmit = t2;
  let t3;
  if ($[4] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = <Text>Enter your preferred response and voice language:</Text>;
    $[4] = t3;
  } else {
    t3 = $[4];
  }

```

---


### `src/components/LogSelector.tsx`

**信息:**
- 行数: 1575
- 大小: 200487 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import figures from 'figures';
import Fuse from 'fuse.js';
import React from 'react';
import { getOriginalCwd, getSessionId } from '../bootstrap/state.js';
import { useExitOnCtrlCDWithKeybindings } from '../hooks/useExitOnCtrlCDWithKeybindings.js';
import { useSearchInput } from '../hooks/useSearchInput.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { applyColor } from '../ink/colorize.js';
import type { Color } from '../ink/styles.js';
import { Box, Text, useInput, useTerminalFocus, useTheme } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { logEvent } from '../services/analytics/index.js';
import type { LogOption, SerializedMessage } from '../types/logs.js';
import { formatLogMetadata, truncateToWidth } from '../utils/format.js';
import { getWorktreePaths } from '../utils/getWorktreePaths.js';
import { getBranch } from '../utils/git.js';
import { getLogDisplayTitle } from '../utils/log.js';
import { getFirstMeaningfulUserMessageTextContent, getSessionIdFromLog, isCustomTitleEnabled, saveCustomTitle } from '../utils/sessionStorage.js';
import { getTheme } from '../utils/theme.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { Select } from './CustomSelect/select.js';
import { Byline } from './design-system/Byline.js';
import { Divider } from './design-system/Divider.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import { SearchBox } from './SearchBox.js';
import { SessionPreview } from './SessionPreview.js';
import { Spinner } from './Spinner.js';
import { TagTabs } from './TagTabs.js';
import TextInput from './TextInput.js';
import { type TreeNode, TreeSelect } from './ui/TreeSelect.js';
type AgenticSearchState = {
  status: 'idle';
} | {
  status: 'searching';
} | {
  status: 'results';
  results: LogOption[];
  query: string;
} | {
  status: 'error';
  message: string;
};
export type LogSelectorProps = {
  logs: LogOption[];
  maxHeight?: number;
  forceWidth?: number;
  onCancel?: () => void;
  onSelect: (log: LogOption) => void;

```

---


### `src/components/LogoV2/AnimatedAsterisk.tsx`

**信息:**
- 行数: 50
- 大小: 7562 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { TEARDROP_ASTERISK } from '../../constants/figures.js';
import { Box, Text, useAnimationFrame } from '../../ink.js';
import { getInitialSettings } from '../../utils/settings/settings.js';
import { hueToRgb, toRGBColor } from '../Spinner/utils.js';
const SWEEP_DURATION_MS = 1500;
const SWEEP_COUNT = 2;
const TOTAL_ANIMATION_MS = SWEEP_DURATION_MS * SWEEP_COUNT;
const SETTLED_GREY = toRGBColor({
  r: 153,
  g: 153,
  b: 153
});
export function AnimatedAsterisk({
  char = TEARDROP_ASTERISK
}: {
  char?: string;
}): React.ReactNode {
  // Read prefersReducedMotion once at mount — no useSettings() subscription,
  // since that would re-render whenever settings change.
  const [reducedMotion] = useState(() => getInitialSettings().prefersReducedMotion ?? false);
  const [done, setDone] = useState(reducedMotion);
  // useAnimationFrame's clock is shared — capture our start offset so the
  // sweep always begins at hue 0 regardless of when we mount.
  const startTimeRef = useRef<number | null>(null);
  // Wire the ref so useAnimationFrame's viewport-pause kicks in: if the
  // user submits a message before the sweep finishes, the clock stops
  // automatically once this row enters scrollback (prevents flicker).
  const [ref, time] = useAnimationFrame(done ? null : 50);
  useEffect(() => {
    if (done) return;
    const t = setTimeout(setDone, TOTAL_ANIMATION_MS, true);
    return () => clearTimeout(t);
  }, [done]);
  if (done) {
    return <Box ref={ref}>
        <Text color={SETTLED_GREY}>{char}</Text>
      </Box>;
  }
  if (startTimeRef.current === null) {
    startTimeRef.current = time;
  }
  const elapsed = time - startTimeRef.current;
  const hue = elapsed / SWEEP_DURATION_MS * 360 % 360;
  return <Box ref={ref}>
      <Text color={toRGBColor(hueToRgb(hue))}>{char}</Text>
    </Box>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsInVzZUVmZmVjdCIsInVzZVJlZiIsInVzZVN0YXRlIiwiVEVBUkRST1BfQVNURVJJU0siLCJCb3giLCJUZXh0IiwidXNlQW5pbWF0aW9uRnJhbWUiLCJnZXRJbml0aWFsU2V0dGluZ3MiLCJodWVUb1JnYiIsInRvUkdCQ29sb3IiLCJTV0VFUF9EVVJBVElPTl9NUyIsIlNXRUVQX0NPVU5UIiwiVE9UQUxfQU5JTUFUSU9OX01TIiwiU0VUVExFRF9HUkVZIiwiciIsImciLCJiIiwiQW5pbWF0ZWRBc3RlcmlzayIsImNoYXIiLCJSZWFjdE5vZGUiLCJyZWR1Y2VkTW90aW9uIiwicHJlZmVyc1JlZHVjZWRNb3Rpb24iLCJkb25lIiwic2V0RG9uZSIsInN0YXJ0VGltZVJlZiIsInJlZiIsInRpbWUiLCJ0Iiwic2V0VGltZW91dCIsImNsZWFyVGltZW91dCIsImN1cnJlbnQiLCJlbGFwc2VkIiwiaHVlIl0sInNvdXJjZXMiOlsiQW5pbWF0ZWRBc3Rlcmlzay50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyB1c2VFZmZlY3QsIHVzZVJlZiwgdXNlU3RhdGUgfSBmcm9tICdyZWFjdCdcbmltcG9ydCB7IFRFQVJEUk9QX0FTVEVSSVNLIH0gZnJvbSAnLi4vLi4vY29uc3RhbnRzL2ZpZ3VyZXMuanMnXG5pbXBvcnQgeyBCb3gsIFRleHQsIHVzZUFuaW1hdGlvbkZyYW1lIH0gZnJvbSAnLi4vLi4vaW5rLmpzJ1xuaW1wb3J0IHsgZ2V0SW5pdGlhbFNldHRpbmdzIH0gZnJvbSAnLi4vLi4vdXRpbHMvc2V0dGluZ3Mvc2V0dGluZ3MuanMnXG5pbXBvcnQgeyBodWVUb1JnYiwgdG9SR0JDb2xvciB9IGZyb20gJy4uL1NwaW5uZXIvdXRpbHMuanMnXG5cbmNvbnN0IFNXRUVQX0RVUkFUSU9OX01TID0gMTUwMFxuY29uc3QgU1dFRVBfQ09VTlQgPSAyXG5jb25zdCBUT1RBTF9BTklNQVRJT05fTVMgPSBTV0VFUF9EVVJBVElPTl9NUyAqIFNXRUVQX0NPVU5UXG5jb25zdCBTRVRUTEVEX0dSRVkgPSB0b1JHQkNvbG9yKHsgcjogMTUzLCBnOiAxNTMsIGI6IDE1MyB9KVxuXG5leHBvcnQgZnVuY3Rpb24gQW5pbWF0ZWRBc3Rlcmlzayh7XG4gIGNoYXIgPSBURUFSRFJPUF9BU1RFUklTSyxcbn06IHtcbiAgY2hhcj86IHN0cmluZ1xufSk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIC8vIFJlYWQgcHJlZmVyc1JlZHVjZWRNb3Rpb24gb25jZSBhdCBtb3VudCDigJQgbm8gdXNlU2V0dGluZ3MoKSBzdWJzY3JpcHRpb24sXG4gIC8vIHNpbmNlIHRoYXQgd291bGQgcmUtcmVuZGVyIHdoZW5ldmVyIHNldHRpbmdzIGNoYW5nZS5cbiAgY29uc3QgW3JlZHVjZWRNb3Rpb25dID0gdXNlU3RhdGUoXG4gICAgKCkgPT4gZ2V0SW5pdGlhbFNldHRpbmdzKCkucHJlZmVyc1JlZHVjZWRNb3Rpb24gPz8gZmFsc2UsXG4gIClcbiAgY29uc3QgW2RvbmUsIHNldERvbmVdID0gdXNlU3RhdGUocmVkdWNlZE1vdGlvbilcbiAgLy8gdXNlQW5pbWF0aW9uRnJhbWUncyBjbG9jayBpcyBzaGFyZWQg4oCUIGNhcHR1cmUgb3VyIHN0YXJ0IG9mZnNldCBzbyB0aGVcbiAgLy8gc3dlZXAgYWx3YXlzIGJlZ2lucyBhdCBodWUgMCByZWdhcmRsZXNzIG9mIHdoZW4gd2UgbW91bnQuXG4gIGNvbnN0IHN0YXJ0VGltZVJlZiA9IHVzZVJlZjxudW1iZXIgfCBudWxsPihudWxsKVxuICAvLyBXaXJlIHRoZSByZWYgc28gdXNlQW5pbWF0aW9uRnJhbWUncyB2aWV3cG9ydC1wYXVzZSBraWNrcyBpbjogaWYgdGhlXG4gIC8vIHVzZXIgc3VibWl0cyBhIG1lc3NhZ2UgYmVmb3JlIHRoZSBzd2VlcCBmaW5pc2hlcywgdGhlIGNsb2NrIHN0b3BzXG4gIC8vIGF1dG9tYXRpY2FsbHkgb25jZSB0aGlzIHJvdyBlbnRlcnMgc2Nyb2xsYmFjayAocHJldmVudHMgZmxpY2tlcikuXG4gIGNvbnN0IFtyZWYsIHRpbWVdID0gdXNlQW5pbWF0aW9uRnJhbWUoZG9uZSA/IG51bGwgOiA1MClcblxuICB1c2VFZmZlY3QoKCkgPT4ge1xuICAgIGlmIChkb25lKSByZXR1cm5cbiAgICBjb25zdCB0ID0gc2V0VGltZW91dChzZXREb25lLCBUT1RBTF9BTklNQVRJT05fTVMsIHRydWUpXG4gICAgcmV0dXJuICgpID0+IGNsZWFyVGltZW91dCh0KVxuICB9LCBbZG9uZV0pXG5cbiAgaWYgKGRvbmUpIHtcbiAgICByZXR1cm4gKFxuICAgICAgPEJveCByZWY9e3JlZn0+XG4gICAgICAgIDxUZXh0IGNvbG9yPXtTRVRUTEVEX0dSRVl9PntjaGFyfTwvVGV4dD5cbiAgICAgIDwvQm94PlxuICAgIClcbiAgfVxuXG4gIGlmIChzdGFydFRpbWVSZWYuY3VycmVudCA9PT0gbnVsbCkge1xuICAgIHN0YXJ0VGltZVJlZi5jdXJyZW50ID0gdGltZVxuICB9XG4gIGNvbnN0IGVsYXBzZWQgPSB0aW1lIC0gc3RhcnRUaW1lUmVmLmN1cnJlbnRcbiAgY29uc3QgaHVlID0gKChlbGFwc2VkIC8gU1dFRVBfRFVSQVRJT05fTVMpICogMzYwKSAlIDM2MFxuXG4gIHJldHVybiAoXG4gICAgPEJveCByZWY9e3JlZn0+XG4gICAgICA8VGV4dCBjb2xvcj17dG9SR0JDb2xvcihodWVUb1JnYihodWUpKX0+e2NoYXJ9PC9UZXh0PlxuICAgIDwvQm94PlxuICApXG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsU0FBUyxFQUFFQyxNQUFNLEVBQUVDLFFBQVEsUUFBUSxPQUFPO0FBQ25ELFNBQVNDLGlCQUFpQixRQUFRLDRCQUE0QjtBQUM5RCxTQUFTQyxHQUFHLEVBQUVDLElBQUksRUFBRUMsaUJBQWlCLFFBQVEsY0FBYztBQUMzRCxTQUFTQyxrQkFBa0IsUUFBUSxrQ0FBa0M7QUFDckUsU0FBU0MsUUFBUSxFQUFFQyxVQUFVLFFBQVEscUJBQXFCO0FBRTFELE1BQU1DLGlCQUFpQixHQUFHLElBQUk7QUFDOUIsTUFBTUMsV0FBVyxHQUFHLENBQUM7QUFDckIsTUFBTUMsa0JBQWtCLEdBQUdGLGlCQUFpQixHQUFHQyxXQUFXO0FBQzFELE1BQU1FLFlBQVksR0FBR0osVUFBVSxDQUFDO0VBQUVLLENBQUMsRUFBRSxHQUFHO0VBQUVDLENBQUMsRUFBRSxHQUFHO0VBQUVDLENBQUMsRUFBRTtBQUFJLENBQUMsQ0FBQztBQUUzRCxPQUFPLFNBQVNDLGdCQUFnQkEsQ0FBQztFQUMvQkMsSUFBSSxHQUFHZjtBQUdULENBRkMsRUFBRTtFQUNEZSxJQUFJLENBQUMsRUFBRSxNQUFNO0FBQ2YsQ0FBQyxDQUFDLEVBQUVuQixLQUFLLENBQUNvQixTQUFTLENBQUM7RUFDbEI7RUFDQTtFQUNBLE1BQU0sQ0FBQ0MsYUFBYSxDQUFDLEdBQUdsQixRQUFRLENBQzlCLE1BQU1LLGtCQUFrQixDQUFDLENBQUMsQ0FBQ2Msb0JBQW9CLElBQUksS0FDckQsQ0FBQztFQUNELE1BQU0sQ0FBQ0MsSUFBSSxFQUFFQyxPQUFPLENBQUMsR0FBR3JCLFFBQVEsQ0FBQ2tCLGFBQWEsQ0FBQztFQUMvQztFQUNBO0VBQ0EsTUFBTUksWUFBWSxHQUFHdkIsTUFBTSxDQUFDLE1BQU0sR0FBRyxJQUFJLENBQUMsQ0FBQyxJQUFJLENBQUM7RUFDaEQ7RUFDQTtFQUNBO0VBQ0EsTUFBTSxDQUFDd0IsR0FBRyxFQUFFQyxJQUFJLENBQUMsR0FBR3BCLGlCQUFpQixDQUFDZ0IsSUFBSSxHQUFHLElBQUksR0FBRyxFQUFFLENBQUM7RUFFdkR0QixTQUFTLENBQUMsTUFBTTtJQUNkLElBQUlzQixJQUFJLEVBQUU7SUFDVixNQUFNSyxDQUFDLEdBQUdDLFVBQVUsQ0FBQ0wsT0FBTyxFQUFFWCxrQkFBa0IsRUFBRSxJQUFJLENBQUM7SUFDdkQsT0FBTyxNQUFNaUIsWUFBWSxDQUFDRixDQUFDLENBQUM7RUFDOUIsQ0FBQyxFQUFFLENBQUNMLElBQUksQ0FBQyxDQUFDO0VBRVYsSUFBSUEsSUFBSSxFQUFFO0lBQ1IsT0FDRSxDQUFDLEdBQUcsQ0FBQyxHQUFHLENBQUMsQ0FBQ0csR0FBRyxDQUFDO0FBQ3BCLFFBQVEsQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLENBQUNaLFlBQVksQ0FBQyxDQUFDLENBQUNLLElBQUksQ0FBQyxFQUFFLElBQUk7QUFDL0MsTUFBTSxFQUFFLEdBQUcsQ0FBQztFQUVWO0VBRUEsSUFBSU0sWUFBWSxDQUFDTSxPQUFPLEtBQUssSUFBSSxFQUFFO0lBQ2pDTixZQUFZLENBQUNNLE9BQU8sR0FBR0osSUFBSTtFQUM3QjtFQUNBLE1BQU1LLE9BQU8sR0FBR0wsSUFBSSxHQUFHRixZQUFZLENBQUNNLE9BQU87RUFDM0MsTUFBTUUsR0FBRyxHQUFLRCxPQUFPLEdBQUdyQixpQkFBaUIsR0FBSSxHQUFHLEdBQUksR0FBRztFQUV2RCxPQUNFLENBQUMsR0FBRyxDQUFDLEdBQUcsQ0FBQyxDQUFDZSxHQUFHLENBQUM7QUFDbEIsTUFBTSxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsQ0FBQ2hCLFVBQVUsQ0FBQ0QsUUFBUSxDQUFDd0IsR0FBRyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUNkLElBQUksQ0FBQyxFQUFFLElBQUk7QUFDMUQsSUFBSSxFQUFFLEdBQUcsQ0FBQztBQUVWIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/LogoV2/AnimatedClawd.tsx`

**信息:**
- 行数: 124
- 大小: 14054 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { Box } from '../../ink.js';
import { getInitialSettings } from '../../utils/settings/settings.js';
import { Clawd, type ClawdPose } from './Clawd.js';
type Frame = {
  pose: ClawdPose;
  offset: number;
};

/** Hold a pose for n frames (60ms each). */
function hold(pose: ClawdPose, offset: number, frames: number): Frame[] {
  return Array.from({
    length: frames
  }, () => ({
    pose,
    offset
  }));
}

// Offset semantics: marginTop in a fixed-height-3 container. 0 = normal,
// 1 = crouched. Container height stays 3 so the layout never shifts; during
// a crouch (offset=1) Clawd's feet row dips below the container and gets
// clipped — reads as "ducking below the frame" before springing back up.

// Click animation: crouch, then spring up with both arms raised. Twice.
const JUMP_WAVE: readonly Frame[] = [...hold('default', 1, 2),
// crouch
...hold('arms-up', 0, 3),
// spring!
...hold('default', 0, 1), ...hold('default', 1, 2),
// crouch again
...hold('arms-up', 0, 3),
// spring!
...hold('default', 0, 1)];

// Click animation: glance right, then left, then back.
const LOOK_AROUND: readonly Frame[] = [...hold('look-right', 0, 5), ...hold('look-left', 0, 5), ...hold('default', 0, 1)];
const CLICK_ANIMATIONS: readonly (readonly Frame[])[] = [JUMP_WAVE, LOOK_AROUND];
const IDLE: Frame = {
  pose: 'default',
  offset: 0
};
const FRAME_MS = 60;
const incrementFrame = (i: number) => i + 1;
const CLAWD_HEIGHT = 3;

/**
 * Clawd with click-triggered animations (crouch-jump with arms up, or

```

---


### `src/components/LogoV2/ChannelsNotice.tsx`

**信息:**
- 行数: 266
- 大小: 29503 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
// Conditionally require()'d in LogoV2.tsx behind feature('KAIROS') ||
// feature('KAIROS_CHANNELS'). No feature() guard here — the whole file
// tree-shakes via the require pattern when both flags are false (see
// docs/feature-gating.md). Do NOT import this module statically from
// unguarded code.

import * as React from 'react';
import { useState } from 'react';
import { type ChannelEntry, getAllowedChannels, getHasDevChannels } from '../../bootstrap/state.js';
import { Box, Text } from '../../ink.js';
import { isChannelsEnabled } from '../../services/mcp/channelAllowlist.js';
import { getEffectiveChannelAllowlist } from '../../services/mcp/channelNotification.js';
import { getMcpConfigsByScope } from '../../services/mcp/config.js';
import { getClaudeAIOAuthTokens, getSubscriptionType } from '../../utils/auth.js';
import { loadInstalledPluginsV2 } from '../../utils/plugins/installedPluginsManager.js';
import { getSettingsForSource } from '../../utils/settings/settings.js';
export function ChannelsNotice() {
  const $ = _c(32);
  const [t0] = useState(_temp);
  const {
    channels,
    disabled,
    noAuth,
    policyBlocked,
    list,
    unmatched
  } = t0;
  if (channels.length === 0) {
    return null;
  }
  const hasNonDev = channels.some(_temp2);
  const flag = getHasDevChannels() && hasNonDev ? "Channels" : getHasDevChannels() ? "--dangerously-load-development-channels" : "--channels";
  if (disabled) {
    let t1;
    if ($[0] !== flag || $[1] !== list) {
      t1 = <Text color="error">{flag} ignored ({list})</Text>;
      $[0] = flag;
      $[1] = list;
      $[2] = t1;
    } else {
      t1 = $[2];
    }
    let t2;
    if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
      t2 = <Text dimColor={true}>Channels are not currently available</Text>;
      $[3] = t2;
    } else {
      t2 = $[3];
    }

```

---


### `src/components/LogoV2/Clawd.tsx`

**信息:**
- 行数: 240
- 大小: 18574 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { env } from '../../utils/env.js';
export type ClawdPose = 'default' | 'arms-up' // both arms raised (used during jump)
| 'look-left' // both pupils shifted left
| 'look-right'; // both pupils shifted right

type Props = {
  pose?: ClawdPose;
};

// Standard-terminal pose fragments. Each row is split into segments so we can
// vary only the parts that change (eyes, arms) while keeping the body/bg spans
// stable. All poses end up 9 cols wide.
//
// arms-up: the row-2 arm shapes (▝▜ / ▛▘) move to row 1 as their
// bottom-heavy mirrors (▗▟ / ▙▖) — same silhouette, one row higher.
//
// look-* use top-quadrant eye chars (▙/▟) so both eyes change from the
// default (▛/▜, bottom pupils) — otherwise only one eye would appear to move.
type Segments = {
  /** row 1 left (no bg): optional raised arm + side */
  r1L: string;
  /** row 1 eyes (with bg): left-eye, forehead, right-eye */
  r1E: string;
  /** row 1 right (no bg): side + optional raised arm */
  r1R: string;
  /** row 2 left (no bg): arm + body curve */
  r2L: string;
  /** row 2 right (no bg): body curve + arm */
  r2R: string;
};
const POSES: Record<ClawdPose, Segments> = {
  default: {
    r1L: ' ▐',
    r1E: '▛███▜',
    r1R: '▌',
    r2L: '▝▜',
    r2R: '▛▘'
  },
  'look-left': {
    r1L: ' ▐',
    r1E: '▟███▟',
    r1R: '▌',
    r2L: '▝▜',
    r2R: '▛▘'
  },
  'look-right': {
    r1L: ' ▐',

```

---


### `src/components/LogoV2/CondensedLogo.tsx`

**信息:**
- 行数: 161
- 大小: 19395 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { type ReactNode, useEffect } from 'react';
import { useMainLoopModel } from '../../hooks/useMainLoopModel.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { Box, Text } from '../../ink.js';
import { useAppState } from '../../state/AppState.js';
import { getEffortSuffix } from '../../utils/effort.js';
import { truncate } from '../../utils/format.js';
import { isFullscreenEnvEnabled } from '../../utils/fullscreen.js';
import { formatModelAndBilling, getLogoDisplayData, truncatePath } from '../../utils/logoV2Utils.js';
import { renderModelSetting } from '../../utils/model/model.js';
import { OffscreenFreeze } from '../OffscreenFreeze.js';
import { AnimatedClawd } from './AnimatedClawd.js';
import { Clawd } from './Clawd.js';
import { GuestPassesUpsell, incrementGuestPassesSeenCount, useShowGuestPassesUpsell } from './GuestPassesUpsell.js';
import { incrementOverageCreditUpsellSeenCount, OverageCreditUpsell, useShowOverageCreditUpsell } from './OverageCreditUpsell.js';
export function CondensedLogo() {
  const $ = _c(29);
  const {
    columns
  } = useTerminalSize();
  const agent = useAppState(_temp);
  const effortValue = useAppState(_temp2);
  const model = useMainLoopModel();
  const modelDisplayName = renderModelSetting(model);
  const {
    version,
    cwd,
    billingType,
    agentName: agentNameFromSettings
  } = getLogoDisplayData();
  const agentName = agent ?? agentNameFromSettings;
  const showGuestPassesUpsell = useShowGuestPassesUpsell();
  const showOverageCreditUpsell = useShowOverageCreditUpsell();
  let t0;
  let t1;
  if ($[0] !== showGuestPassesUpsell) {
    t0 = () => {
      if (showGuestPassesUpsell) {
        incrementGuestPassesSeenCount();
      }
    };
    t1 = [showGuestPassesUpsell];
    $[0] = showGuestPassesUpsell;
    $[1] = t0;
    $[2] = t1;
  } else {
    t0 = $[1];

```

---


### `src/components/LogoV2/EmergencyTip.tsx`

**信息:**
- 行数: 58
- 大小: 6707 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { useEffect, useMemo } from 'react';
import { Box, Text } from 'src/ink.js';
import { getDynamicConfig_CACHED_MAY_BE_STALE } from 'src/services/analytics/growthbook.js';
import { getGlobalConfig, saveGlobalConfig } from 'src/utils/config.js';
const CONFIG_NAME = 'tengu-top-of-feed-tip';
export function EmergencyTip(): React.ReactNode {
  const tip = useMemo(getTipOfFeed, []);
  // Memoize to prevent re-reads after we save - we want the value at mount time
  const lastShownTip = useMemo(() => getGlobalConfig().lastShownEmergencyTip, []);

  // Only show if this is a new/different tip
  const shouldShow = tip.tip && tip.tip !== lastShownTip;

  // Save the tip we're showing so we don't show it again
  useEffect(() => {
    if (shouldShow) {
      saveGlobalConfig(current => {
        if (current.lastShownEmergencyTip === tip.tip) return current;
        return {
          ...current,
          lastShownEmergencyTip: tip.tip
        };
      });
    }
  }, [shouldShow, tip.tip]);
  if (!shouldShow) {
    return null;
  }
  return <Box paddingLeft={2} flexDirection="column">
      <Text {...tip.color === 'warning' ? {
      color: 'warning'
    } : tip.color === 'error' ? {
      color: 'error'
    } : {
      dimColor: true
    }}>
        {tip.tip}
      </Text>
    </Box>;
}
type TipOfFeed = {
  tip: string;
  color?: 'dim' | 'warning' | 'error';
};
const DEFAULT_TIP: TipOfFeed = {
  tip: '',
  color: 'dim'
};


```

---


### `src/components/LogoV2/Feed.tsx`

**信息:**
- 行数: 112
- 大小: 13804 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { stringWidth } from '../../ink/stringWidth.js';
import { Box, Text } from '../../ink.js';
import { truncate } from '../../utils/format.js';
export type FeedLine = {
  text: string;
  timestamp?: string;
};
export type FeedConfig = {
  title: string;
  lines: FeedLine[];
  footer?: string;
  emptyMessage?: string;
  customContent?: {
    content: React.ReactNode;
    width: number;
  };
};
type FeedProps = {
  config: FeedConfig;
  actualWidth: number;
};
export function calculateFeedWidth(config: FeedConfig): number {
  const {
    title,
    lines,
    footer,
    emptyMessage,
    customContent
  } = config;
  let maxWidth = stringWidth(title);
  if (customContent !== undefined) {
    maxWidth = Math.max(maxWidth, customContent.width);
  } else if (lines.length === 0 && emptyMessage) {
    maxWidth = Math.max(maxWidth, stringWidth(emptyMessage));
  } else {
    const gap = '  ';
    const maxTimestampWidth = Math.max(0, ...lines.map(line => line.timestamp ? stringWidth(line.timestamp) : 0));
    for (const line of lines) {
      const timestampWidth = maxTimestampWidth > 0 ? maxTimestampWidth : 0;
      const lineWidth = stringWidth(line.text) + (timestampWidth > 0 ? timestampWidth + gap.length : 0);
      maxWidth = Math.max(maxWidth, lineWidth);
    }
  }
  if (footer) {
    maxWidth = Math.max(maxWidth, stringWidth(footer));
  }
  return maxWidth;
}

```

---


### `src/components/LogoV2/FeedColumn.tsx`

**信息:**
- 行数: 59
- 大小: 5379 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box } from '../../ink.js';
import { Divider } from '../design-system/Divider.js';
import type { FeedConfig } from './Feed.js';
import { calculateFeedWidth, Feed } from './Feed.js';
type FeedColumnProps = {
  feeds: FeedConfig[];
  maxWidth: number;
};
export function FeedColumn(t0) {
  const $ = _c(10);
  const {
    feeds,
    maxWidth
  } = t0;
  let t1;
  if ($[0] !== feeds) {
    const feedWidths = feeds.map(_temp);
    t1 = Math.max(...feedWidths);
    $[0] = feeds;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const maxOfAllFeeds = t1;
  const actualWidth = Math.min(maxOfAllFeeds, maxWidth);
  let t2;
  if ($[2] !== actualWidth || $[3] !== feeds) {
    let t3;
    if ($[5] !== actualWidth || $[6] !== feeds.length) {
      t3 = (feed_0, index) => <React.Fragment key={index}><Feed config={feed_0} actualWidth={actualWidth} />{index < feeds.length - 1 && <Divider color="claude" width={actualWidth} />}</React.Fragment>;
      $[5] = actualWidth;
      $[6] = feeds.length;
      $[7] = t3;
    } else {
      t3 = $[7];
    }
    t2 = feeds.map(t3);
    $[2] = actualWidth;
    $[3] = feeds;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  let t3;
  if ($[8] !== t2) {
    t3 = <Box flexDirection="column">{t2}</Box>;
    $[8] = t2;
    $[9] = t3;

```

---


### `src/components/LogoV2/GuestPassesUpsell.tsx`

**信息:**
- 行数: 70
- 大小: 9122 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useState } from 'react';
import { Text } from '../../ink.js';
import { logEvent } from '../../services/analytics/index.js';
import { checkCachedPassesEligibility, formatCreditAmount, getCachedReferrerReward, getCachedRemainingPasses } from '../../services/api/referral.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
function resetIfPassesRefreshed(): void {
  const remaining = getCachedRemainingPasses();
  if (remaining == null || remaining <= 0) return;
  const config = getGlobalConfig();
  const lastSeen = config.passesLastSeenRemaining ?? 0;
  if (remaining > lastSeen) {
    saveGlobalConfig(prev => ({
      ...prev,
      passesUpsellSeenCount: 0,
      hasVisitedPasses: false,
      passesLastSeenRemaining: remaining
    }));
  }
}
function shouldShowGuestPassesUpsell(): boolean {
  const {
    eligible,
    hasCache
  } = checkCachedPassesEligibility();
  // Only show if eligible and cache exists (don't block on fetch)
  if (!eligible || !hasCache) return false;
  // Reset upsell counters if passes were refreshed (covers both campaign change and pass refresh)
  resetIfPassesRefreshed();
  const config = getGlobalConfig();
  if ((config.passesUpsellSeenCount ?? 0) >= 3) return false;
  if (config.hasVisitedPasses) return false;
  return true;
}
export function useShowGuestPassesUpsell() {
  const [show] = useState(_temp);
  return show;
}
function _temp() {
  return shouldShowGuestPassesUpsell();
}
export function incrementGuestPassesSeenCount(): void {
  let newCount = 0;
  saveGlobalConfig(prev => {
    newCount = (prev.passesUpsellSeenCount ?? 0) + 1;
    return {
      ...prev,
      passesUpsellSeenCount: newCount
    };

```

---


### `src/components/LogoV2/LogoV2.tsx`

**信息:**
- 行数: 543
- 大小: 75183 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
import * as React from 'react';
import { Box, Text, color } from '../../ink.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { getLayoutMode, calculateLayoutDimensions, calculateOptimalLeftWidth, formatWelcomeMessage, truncatePath, getRecentActivitySync, getRecentReleaseNotesSync, getLogoDisplayData } from '../../utils/logoV2Utils.js';
import { truncate } from '../../utils/format.js';
import { getDisplayPath } from '../../utils/file.js';
import { Clawd } from './Clawd.js';
import { FeedColumn } from './FeedColumn.js';
import { createRecentActivityFeed, createWhatsNewFeed, createProjectOnboardingFeed, createGuestPassesFeed } from './feedConfigs.js';
import { getGlobalConfig, saveGlobalConfig } from 'src/utils/config.js';
import { resolveThemeSetting } from 'src/utils/systemTheme.js';
import { getInitialSettings } from 'src/utils/settings/settings.js';
import { isDebugMode, isDebugToStdErr, getDebugLogPath } from 'src/utils/debug.js';
import { useEffect, useState } from 'react';
import { getSteps, shouldShowProjectOnboarding, incrementProjectOnboardingSeenCount } from '../../projectOnboardingState.js';
import { CondensedLogo } from './CondensedLogo.js';
import { OffscreenFreeze } from '../OffscreenFreeze.js';
import { checkForReleaseNotesSync } from '../../utils/releaseNotes.js';
import { getDumpPromptsPath } from 'src/services/api/dumpPrompts.js';
import { isEnvTruthy } from 'src/utils/envUtils.js';
import { getStartupPerfLogPath, isDetailedProfilingEnabled } from 'src/utils/startupProfiler.js';
import { EmergencyTip } from './EmergencyTip.js';
import { VoiceModeNotice } from './VoiceModeNotice.js';
import { Opus1mMergeNotice } from './Opus1mMergeNotice.js';
import { feature } from 'bun:bundle';

// Conditional require so ChannelsNotice.tsx tree-shakes when both flags are
// false. A module-scope helper component inside a feature() ternary does NOT
// tree-shake (docs/feature-gating.md); the require pattern eliminates the
// whole file. VoiceModeNotice uses the unsafe helper pattern but VOICE_MODE
// is external: true so it's moot there.
/* eslint-disable @typescript-eslint/no-require-imports */
const ChannelsNoticeModule = feature('KAIROS') || feature('KAIROS_CHANNELS') ? require('./ChannelsNotice.js') as typeof import('./ChannelsNotice.js') : null;
/* eslint-enable @typescript-eslint/no-require-imports */
import { SandboxManager } from 'src/utils/sandbox/sandbox-adapter.js';
import { useShowGuestPassesUpsell, incrementGuestPassesSeenCount } from './GuestPassesUpsell.js';
import { useShowOverageCreditUpsell, incrementOverageCreditUpsellSeenCount, createOverageCreditFeed } from './OverageCreditUpsell.js';
import { plural } from '../../utils/stringUtils.js';
import { useAppState } from '../../state/AppState.js';
import { getEffortSuffix } from '../../utils/effort.js';
import { useMainLoopModel } from '../../hooks/useMainLoopModel.js';
import { renderModelSetting } from '../../utils/model/model.js';
const LEFT_PANEL_MAX_WIDTH = 50;
export function LogoV2() {
  const $ = _c(94);
  const activities = getRecentActivitySync();
  const username = getGlobalConfig().oauthAccount?.displayName ?? "";

```

---


### `src/components/LogoV2/Opus1mMergeNotice.tsx`

**信息:**
- 行数: 55
- 大小: 5812 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useEffect, useState } from 'react';
import { UP_ARROW } from '../../constants/figures.js';
import { Box, Text } from '../../ink.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { isOpus1mMergeEnabled } from '../../utils/model/model.js';
import { AnimatedAsterisk } from './AnimatedAsterisk.js';
const MAX_SHOW_COUNT = 6;
export function shouldShowOpus1mMergeNotice(): boolean {
  return isOpus1mMergeEnabled() && (getGlobalConfig().opus1mMergeNoticeSeenCount ?? 0) < MAX_SHOW_COUNT;
}
export function Opus1mMergeNotice() {
  const $ = _c(4);
  const [show] = useState(shouldShowOpus1mMergeNotice);
  let t0;
  let t1;
  if ($[0] !== show) {
    t0 = () => {
      if (!show) {
        return;
      }
      const newCount = (getGlobalConfig().opus1mMergeNoticeSeenCount ?? 0) + 1;
      saveGlobalConfig(prev => {
        if ((prev.opus1mMergeNoticeSeenCount ?? 0) >= newCount) {
          return prev;
        }
        return {
          ...prev,
          opus1mMergeNoticeSeenCount: newCount
        };
      });
    };
    t1 = [show];
    $[0] = show;
    $[1] = t0;
    $[2] = t1;
  } else {
    t0 = $[1];
    t1 = $[2];
  }
  useEffect(t0, t1);
  if (!show) {
    return null;
  }
  let t2;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Box paddingLeft={2}><AnimatedAsterisk char={UP_ARROW} /><Text dimColor={true}>{" "}Opus now defaults to 1M context · 5x more room, same pricing</Text></Box>;
    $[3] = t2;
  } else {

```

---


### `src/components/LogoV2/OverageCreditUpsell.tsx`

**信息:**
- 行数: 166
- 大小: 18347 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useState } from 'react';
import { Text } from '../../ink.js';
import { logEvent } from '../../services/analytics/index.js';
import { formatGrantAmount, getCachedOverageCreditGrant, refreshOverageCreditGrantCache } from '../../services/api/overageCreditGrant.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { truncate } from '../../utils/format.js';
import type { FeedConfig } from './Feed.js';
const MAX_IMPRESSIONS = 3;

/**
 * Whether to show the overage credit upsell on any surface.
 *
 * Eligibility comes entirely from the backend GET /overage_credit_grant
 * response — the CLI doesn't replicate tier/threshold/role checks. The
 * backend returns available: false for Team members who aren't admins,
 * so they don't see an upsell they can't act on.
 *
 * isEligibleForOverageCreditGrant — just the backend eligibility. Use for
 *   persistent reference surfaces (/usage) where the info should show
 *   whenever eligible, no impression cap.
 * shouldShowOverageCreditUpsell — adds the 3-impression cap and
 *   hasVisitedExtraUsage dismiss. Use for promotional surfaces
 *   (welcome feed, tips).
 */
export function isEligibleForOverageCreditGrant(): boolean {
  const info = getCachedOverageCreditGrant();
  if (!info || !info.available || info.granted) return false;
  return formatGrantAmount(info) !== null;
}
export function shouldShowOverageCreditUpsell(): boolean {
  if (!isEligibleForOverageCreditGrant()) return false;
  const config = getGlobalConfig();
  if (config.hasVisitedExtraUsage) return false;
  if ((config.overageCreditUpsellSeenCount ?? 0) >= MAX_IMPRESSIONS) return false;
  return true;
}

/**
 * Kick off a background fetch if the cache is empty. Safe to call
 * unconditionally on mount — it no-ops if cache is fresh.
 */
export function maybeRefreshOverageCreditCache(): void {
  if (getCachedOverageCreditGrant() !== null) return;
  void refreshOverageCreditGrantCache();
}
export function useShowOverageCreditUpsell() {
  const [show] = useState(_temp);
  return show;

```

---


### `src/components/LogoV2/VoiceModeNotice.tsx`

**信息:**
- 行数: 68
- 大小: 7668 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import * as React from 'react';
import { useEffect, useState } from 'react';
import { Box, Text } from '../../ink.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { getInitialSettings } from '../../utils/settings/settings.js';
import { isVoiceModeEnabled } from '../../voice/voiceModeEnabled.js';
import { AnimatedAsterisk } from './AnimatedAsterisk.js';
import { shouldShowOpus1mMergeNotice } from './Opus1mMergeNotice.js';
const MAX_SHOW_COUNT = 3;
export function VoiceModeNotice() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = feature("VOICE_MODE") ? <VoiceModeNoticeInner /> : null;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}
function VoiceModeNoticeInner() {
  const $ = _c(4);
  const [show] = useState(_temp);
  let t0;
  let t1;
  if ($[0] !== show) {
    t0 = () => {
      if (!show) {
        return;
      }
      const newCount = (getGlobalConfig().voiceNoticeSeenCount ?? 0) + 1;
      saveGlobalConfig(prev => {
        if ((prev.voiceNoticeSeenCount ?? 0) >= newCount) {
          return prev;
        }
        return {
          ...prev,
          voiceNoticeSeenCount: newCount
        };
      });
    };
    t1 = [show];
    $[0] = show;
    $[1] = t0;
    $[2] = t1;
  } else {
    t0 = $[1];
    t1 = $[2];

```

---


### `src/components/LogoV2/WelcomeV2.tsx`

**信息:**
- 行数: 433
- 大小: 57864 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text, useTheme } from 'src/ink.js';
import { env } from '../../utils/env.js';
const WELCOME_V2_WIDTH = 58;
export function WelcomeV2() {
  const $ = _c(35);
  const [theme] = useTheme();
  if (env.terminal === "Apple_Terminal") {
    let t0;
    if ($[0] !== theme) {
      t0 = <AppleTerminalWelcomeV2 theme={theme} welcomeMessage="Welcome to Claude Code" />;
      $[0] = theme;
      $[1] = t0;
    } else {
      t0 = $[1];
    }
    return t0;
  }
  if (["light", "light-daltonized", "light-ansi"].includes(theme)) {
    let t0;
    let t1;
    let t2;
    let t3;
    let t4;
    let t5;
    let t6;
    let t7;
    let t8;
    if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
      t0 = <Text><Text color="claude">{"Welcome to Claude Code"} </Text><Text dimColor={true}>v{MACRO.VERSION} </Text></Text>;
      t1 = <Text>{"\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026\u2026"}</Text>;
      t2 = <Text>{"                                                          "}</Text>;
      t3 = <Text>{"                                                          "}</Text>;
      t4 = <Text>{"                                                          "}</Text>;
      t5 = <Text>{"            \u2591\u2591\u2591\u2591\u2591\u2591                                        "}</Text>;
      t6 = <Text>{"    \u2591\u2591\u2591   \u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591                                      "}</Text>;
      t7 = <Text>{"   \u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591\u2591                                    "}</Text>;
      t8 = <Text>{"                                                          "}</Text>;
      $[2] = t0;
      $[3] = t1;
      $[4] = t2;
      $[5] = t3;
      $[6] = t4;
      $[7] = t5;
      $[8] = t6;
      $[9] = t7;
      $[10] = t8;
    } else {
      t0 = $[2];

```

---


### `src/components/LogoV2/feedConfigs.tsx`

**信息:**
- 行数: 92
- 大小: 12205 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import figures from 'figures';
import { homedir } from 'os';
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import type { Step } from '../../projectOnboardingState.js';
import { formatCreditAmount, getCachedReferrerReward } from '../../services/api/referral.js';
import type { LogOption } from '../../types/logs.js';
import { getCwd } from '../../utils/cwd.js';
import { formatRelativeTimeAgo } from '../../utils/format.js';
import type { FeedConfig, FeedLine } from './Feed.js';
export function createRecentActivityFeed(activities: LogOption[]): FeedConfig {
  const lines: FeedLine[] = activities.map(log => {
    const time = formatRelativeTimeAgo(log.modified);
    const description = log.summary && log.summary !== 'No prompt' ? log.summary : log.firstPrompt;
    return {
      text: description || '',
      timestamp: time
    };
  });
  return {
    title: 'Recent activity',
    lines,
    footer: lines.length > 0 ? '/resume for more' : undefined,
    emptyMessage: 'No recent activity'
  };
}
export function createWhatsNewFeed(releaseNotes: string[]): FeedConfig {
  const lines: FeedLine[] = releaseNotes.map(note => {
    if ("external" === 'ant') {
      const match = note.match(/^(\d+\s+\w+\s+ago)\s+(.+)$/);
      if (match) {
        return {
          timestamp: match[1],
          text: match[2] || ''
        };
      }
    }
    return {
      text: note
    };
  });
  const emptyMessage = "external" === 'ant' ? 'Unable to fetch latest claude-cli-internal commits' : 'Check the Claude Code changelog for updates';
  return {
    title: "external" === 'ant' ? "What's new [ANT-ONLY: Latest CC commits]" : "What's new",
    lines,
    footer: lines.length > 0 ? '/release-notes for more' : undefined,
    emptyMessage
  };
}
export function createProjectOnboardingFeed(steps: Step[]): FeedConfig {

```

---


### `src/components/LspRecommendation/LspRecommendationMenu.tsx`

**信息:**
- 行数: 88
- 大小: 10247 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { Select } from '../CustomSelect/select.js';
import { PermissionDialog } from '../permissions/PermissionDialog.js';
type Props = {
  pluginName: string;
  pluginDescription?: string;
  fileExtension: string;
  onResponse: (response: 'yes' | 'no' | 'never' | 'disable') => void;
};
const AUTO_DISMISS_MS = 30_000;
export function LspRecommendationMenu({
  pluginName,
  pluginDescription,
  fileExtension,
  onResponse
}: Props): React.ReactNode {
  // Use ref to avoid timer reset when onResponse changes
  const onResponseRef = React.useRef(onResponse);
  onResponseRef.current = onResponse;

  // 30-second auto-dismiss timer - counts as ignored (no)
  React.useEffect(() => {
    const timeoutId = setTimeout(ref => ref.current('no'), AUTO_DISMISS_MS, onResponseRef);
    return () => clearTimeout(timeoutId);
  }, []);
  function onSelect(value: string): void {
    switch (value) {
      case 'yes':
        onResponse('yes');
        break;
      case 'no':
        onResponse('no');
        break;
      case 'never':
        onResponse('never');
        break;
      case 'disable':
        onResponse('disable');
        break;
    }
  }
  const options = [{
    label: <Text>
          Yes, install <Text bold>{pluginName}</Text>
        </Text>,
    value: 'yes'
  }, {
    label: 'No, not now',
    value: 'no'

```

---


### `src/components/MCPServerApprovalDialog.tsx`

**信息:**
- 行数: 115
- 大小: 11563 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { getSettings_DEPRECATED, updateSettingsForSource } from '../utils/settings/settings.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
import { MCPServerDialogCopy } from './MCPServerDialogCopy.js';
type Props = {
  serverName: string;
  onDone(): void;
};
export function MCPServerApprovalDialog(t0) {
  const $ = _c(13);
  const {
    serverName,
    onDone
  } = t0;
  let t1;
  if ($[0] !== onDone || $[1] !== serverName) {
    t1 = function onChange(value) {
      logEvent("tengu_mcp_dialog_choice", {
        choice: value as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS
      });
      bb2: switch (value) {
        case "yes":
        case "yes_all":
          {
            const currentSettings_0 = getSettings_DEPRECATED() || {};
            const enabledServers = currentSettings_0.enabledMcpjsonServers || [];
            if (!enabledServers.includes(serverName)) {
              updateSettingsForSource("localSettings", {
                enabledMcpjsonServers: [...enabledServers, serverName]
              });
            }
            if (value === "yes_all") {
              updateSettingsForSource("localSettings", {
                enableAllProjectMcpServers: true
              });
            }
            onDone();
            break bb2;
          }
        case "no":
          {
            const currentSettings = getSettings_DEPRECATED() || {};
            const disabledServers = currentSettings.disabledMcpjsonServers || [];
            if (!disabledServers.includes(serverName)) {
              updateSettingsForSource("localSettings", {
                disabledMcpjsonServers: [...disabledServers, serverName]
              });

```

---


### `src/components/MCPServerDesktopImportDialog.tsx`

**信息:**
- 行数: 203
- 大小: 21016 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useEffect, useState } from 'react';
import { gracefulShutdown } from 'src/utils/gracefulShutdown.js';
import { writeToStdout } from 'src/utils/process.js';
import { Box, color, Text, useTheme } from '../ink.js';
import { addMcpConfig, getAllMcpConfigs } from '../services/mcp/config.js';
import type { ConfigScope, McpServerConfig, ScopedMcpServerConfig } from '../services/mcp/types.js';
import { plural } from '../utils/stringUtils.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { SelectMulti } from './CustomSelect/SelectMulti.js';
import { Byline } from './design-system/Byline.js';
import { Dialog } from './design-system/Dialog.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
type Props = {
  servers: Record<string, McpServerConfig>;
  scope: ConfigScope;
  onDone(): void;
};
export function MCPServerDesktopImportDialog(t0) {
  const $ = _c(36);
  const {
    servers,
    scope,
    onDone
  } = t0;
  let t1;
  if ($[0] !== servers) {
    t1 = Object.keys(servers);
    $[0] = servers;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const serverNames = t1;
  let t2;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = {};
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  const [existingServers, setExistingServers] = useState(t2);
  let t3;
  let t4;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = () => {
      getAllMcpConfigs().then(t5 => {
        const {
          servers: servers_0
        } = t5;

```

---


### `src/components/MCPServerDialogCopy.tsx`

**信息:**
- 行数: 15
- 大小: 1829 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Link, Text } from '../ink.js';
export function MCPServerDialogCopy() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <Text>MCP servers may execute code or access system resources. All tool calls require approval. Learn more in the{" "}<Link url="https://code.claude.com/docs/en/mcp">MCP documentation</Link>.</Text>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkxpbmsiLCJUZXh0IiwiTUNQU2VydmVyRGlhbG9nQ29weSIsIiQiLCJfYyIsInQwIiwiU3ltYm9sIiwiZm9yIl0sInNvdXJjZXMiOlsiTUNQU2VydmVyRGlhbG9nQ29weS50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgTGluaywgVGV4dCB9IGZyb20gJy4uL2luay5qcydcblxuZXhwb3J0IGZ1bmN0aW9uIE1DUFNlcnZlckRpYWxvZ0NvcHkoKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgcmV0dXJuIChcbiAgICA8VGV4dD5cbiAgICAgIE1DUCBzZXJ2ZXJzIG1heSBleGVjdXRlIGNvZGUgb3IgYWNjZXNzIHN5c3RlbSByZXNvdXJjZXMuIEFsbCB0b29sIGNhbGxzXG4gICAgICByZXF1aXJlIGFwcHJvdmFsLiBMZWFybiBtb3JlIGluIHRoZXsnICd9XG4gICAgICA8TGluayB1cmw9XCJodHRwczovL2NvZGUuY2xhdWRlLmNvbS9kb2NzL2VuL21jcFwiPk1DUCBkb2N1bWVudGF0aW9uPC9MaW5rPi5cbiAgICA8L1RleHQ+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU9BLEtBQUssTUFBTSxPQUFPO0FBQ3pCLFNBQVNDLElBQUksRUFBRUMsSUFBSSxRQUFRLFdBQVc7QUFFdEMsT0FBTyxTQUFBQyxvQkFBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUFBLElBQUFDLEVBQUE7RUFBQSxJQUFBRixDQUFBLFFBQUFHLE1BQUEsQ0FBQUMsR0FBQTtJQUVIRixFQUFBLElBQUMsSUFBSSxDQUFDLDJHQUVnQyxJQUFFLENBQ3RDLENBQUMsSUFBSSxDQUFLLEdBQXFDLENBQXJDLHFDQUFxQyxDQUFDLGlCQUFpQixFQUFoRSxJQUFJLENBQW1FLENBQzFFLEVBSkMsSUFBSSxDQUlFO0lBQUFGLENBQUEsTUFBQUUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUYsQ0FBQTtFQUFBO0VBQUEsT0FKUEUsRUFJTztBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/MCPServerMultiselectDialog.tsx`

**信息:**
- 行数: 133
- 大小: 16029 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import partition from 'lodash-es/partition.js';
import React, { useCallback } from 'react';
import { logEvent } from 'src/services/analytics/index.js';
import { Box, Text } from '../ink.js';
import { getSettings_DEPRECATED, updateSettingsForSource } from '../utils/settings/settings.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { SelectMulti } from './CustomSelect/SelectMulti.js';
import { Byline } from './design-system/Byline.js';
import { Dialog } from './design-system/Dialog.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import { MCPServerDialogCopy } from './MCPServerDialogCopy.js';
type Props = {
  serverNames: string[];
  onDone(): void;
};
export function MCPServerMultiselectDialog(t0) {
  const $ = _c(21);
  const {
    serverNames,
    onDone
  } = t0;
  let t1;
  if ($[0] !== onDone || $[1] !== serverNames) {
    t1 = function onSubmit(selectedServers) {
      const currentSettings = getSettings_DEPRECATED() || {};
      const enabledServers = currentSettings.enabledMcpjsonServers || [];
      const disabledServers = currentSettings.disabledMcpjsonServers || [];
      const [approvedServers, rejectedServers] = partition(serverNames, server => selectedServers.includes(server));
      logEvent("tengu_mcp_multidialog_choice", {
        approved: approvedServers.length,
        rejected: rejectedServers.length
      });
      if (approvedServers.length > 0) {
        const newEnabledServers = [...new Set([...enabledServers, ...approvedServers])];
        updateSettingsForSource("localSettings", {
          enabledMcpjsonServers: newEnabledServers
        });
      }
      if (rejectedServers.length > 0) {
        const newDisabledServers = [...new Set([...disabledServers, ...rejectedServers])];
        updateSettingsForSource("localSettings", {
          disabledMcpjsonServers: newDisabledServers
        });
      }
      onDone();
    };
    $[0] = onDone;
    $[1] = serverNames;
    $[2] = t1;

```

---


### `src/components/ManagedSettingsSecurityDialog/ManagedSettingsSecurityDialog.tsx`

**信息:**
- 行数: 149
- 大小: 14484 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import type { SettingsJson } from '../../utils/settings/types.js';
import { Select } from '../CustomSelect/index.js';
import { PermissionDialog } from '../permissions/PermissionDialog.js';
import { extractDangerousSettings, formatDangerousSettingsList } from './utils.js';
type Props = {
  settings: SettingsJson;
  onAccept: () => void;
  onReject: () => void;
};
export function ManagedSettingsSecurityDialog(t0) {
  const $ = _c(26);
  const {
    settings,
    onAccept,
    onReject
  } = t0;
  const dangerous = extractDangerousSettings(settings);
  const settingsList = formatDangerousSettingsList(dangerous);
  const exitState = useExitOnCtrlCDWithKeybindings();
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = {
      context: "Confirmation"
    };
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  useKeybinding("confirm:no", onReject, t1);
  let t2;
  if ($[1] !== onAccept || $[2] !== onReject) {
    t2 = function onChange(value) {
      if (value === "exit") {
        onReject();
        return;
      }
      onAccept();
    };
    $[1] = onAccept;
    $[2] = onReject;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  const onChange = t2;

```

---


### `src/components/ManagedSettingsSecurityDialog/utils.ts`

**信息:**
- 行数: 144
- 大小: 3979 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  DANGEROUS_SHELL_SETTINGS,
  SAFE_ENV_VARS,
} from '../../utils/managedEnvConstants.js'
import type { SettingsJson } from '../../utils/settings/types.js'
import { jsonStringify } from '../../utils/slowOperations.js'

type DangerousShellSetting = (typeof DANGEROUS_SHELL_SETTINGS)[number]

export type DangerousSettings = {
  shellSettings: Partial<Record<DangerousShellSetting, string>>
  envVars: Record<string, string>
  hasHooks: boolean
  hooks?: unknown
}

/**
 * Extract dangerous settings from a settings object.
 *
 * Dangerous env vars are determined by checking against SAFE_ENV_VARS -
 * any env var NOT in SAFE_ENV_VARS is considered dangerous.
 * See managedEnv.ts for the authoritative list and threat categories.
 */
export function extractDangerousSettings(
  settings: SettingsJson | null | undefined,
): DangerousSettings {
  if (!settings) {
    return {
      shellSettings: {},
      envVars: {},
      hasHooks: false,
    }
  }

  // Extract dangerous shell settings
  const shellSettings: Partial<Record<DangerousShellSetting, string>> = {}
  for (const key of DANGEROUS_SHELL_SETTINGS) {
    const value = settings[key]
    if (typeof value === 'string' && value.length > 0) {
      shellSettings[key] = value
    }
  }

  // Extract dangerous env vars - any var NOT in SAFE_ENV_VARS is dangerous
  const envVars: Record<string, string> = {}
  if (settings.env && typeof settings.env === 'object') {
    for (const [key, value] of Object.entries(settings.env)) {
      if (typeof value === 'string' && value.length > 0) {
        // Check if this env var is NOT in the safe list
        if (!SAFE_ENV_VARS.has(key.toUpperCase())) {

```

---


### `src/components/Markdown.tsx`

**信息:**
- 行数: 236
- 大小: 28160 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { marked, type Token, type Tokens } from 'marked';
import React, { Suspense, use, useMemo, useRef } from 'react';
import { useSettings } from '../hooks/useSettings.js';
import { Ansi, Box, useTheme } from '../ink.js';
import { type CliHighlight, getCliHighlightPromise } from '../utils/cliHighlight.js';
import { hashContent } from '../utils/hash.js';
import { configureMarked, formatToken } from '../utils/markdown.js';
import { stripPromptXMLTags } from '../utils/messages.js';
import { MarkdownTable } from './MarkdownTable.js';
type Props = {
  children: string;
  /** When true, render all text content as dim */
  dimColor?: boolean;
};

// Module-level token cache — marked.lexer is the hot cost on virtual-scroll
// remounts (~3ms per message). useMemo doesn't survive unmount→remount, so
// scrolling back to a previously-visible message re-parses. Messages are
// immutable in history; same content → same tokens. Keyed by hash to avoid
// retaining full content strings (turn50→turn99 RSS regression, #24180).
const TOKEN_CACHE_MAX = 500;
const tokenCache = new Map<string, Token[]>();

// Characters that indicate markdown syntax. If none are present, skip the
// ~3ms marked.lexer call entirely — render as a single paragraph. Covers
// the majority of short assistant responses and user prompts that are
// plain sentences. Checked via indexOf (not regex) for speed.
// Single regex: matches any MD marker or ordered-list start (N. at line start).
// One pass instead of 10× includes scans.
const MD_SYNTAX_RE = /[#*`|[>\-_~]|\n\n|^\d+\. |\n\d+\. /;
function hasMarkdownSyntax(s: string): boolean {
  // Sample first 500 chars — if markdown exists it's usually early (headers,
  // code fence, list). Long tool outputs are mostly plain text tails.
  return MD_SYNTAX_RE.test(s.length > 500 ? s.slice(0, 500) : s);
}
function cachedLexer(content: string): Token[] {
  // Fast path: plain text with no markdown syntax → single paragraph token.
  // Skips marked.lexer's full GFM parse (~3ms on long content). Not cached —
  // reconstruction is a single object allocation, and caching would retain
  // 4× content in raw/text fields plus the hash key for zero benefit.
  if (!hasMarkdownSyntax(content)) {
    return [{
      type: 'paragraph',
      raw: content,
      text: content,
      tokens: [{
        type: 'text',
        raw: content,
        text: content

```

---


### `src/components/MarkdownTable.tsx`

**信息:**
- 行数: 322
- 大小: 47567 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { Token, Tokens } from 'marked';
import React from 'react';
import stripAnsi from 'strip-ansi';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { stringWidth } from '../ink/stringWidth.js';
import { wrapAnsi } from '../ink/wrapAnsi.js';
import { Ansi, useTheme } from '../ink.js';
import type { CliHighlight } from '../utils/cliHighlight.js';
import { formatToken, padAligned } from '../utils/markdown.js';

/** Accounts for parent indentation (e.g. message dot prefix) and terminal
 *  resize races. Without enough margin the table overflows its layout box
 *  and Ink's clip truncates differently on alternating frames, causing an
 *  infinite flicker loop in scrollback. */
const SAFETY_MARGIN = 4;

/** Minimum column width to prevent degenerate layouts */
const MIN_COLUMN_WIDTH = 3;

/**
 * Maximum number of lines per row before switching to vertical format.
 * When wrapping would make rows taller than this, vertical (key-value)
 * format provides better readability.
 */
const MAX_ROW_LINES = 4;

/** ANSI escape codes for text formatting */
const ANSI_BOLD_START = '\x1b[1m';
const ANSI_BOLD_END = '\x1b[22m';
type Props = {
  token: Tokens.Table;
  highlight: CliHighlight | null;
  /** Override terminal width (useful for testing) */
  forceWidth?: number;
};

/**
 * Wrap text to fit within a given width, returning array of lines.
 * ANSI-aware: preserves styling across line breaks.
 *
 * @param hard - If true, break words that exceed width (needed when columns
 *               are narrower than the longest word). Default false.
 */
function wrapText(text: string, width: number, options?: {
  hard?: boolean;
}): string[] {
  if (width <= 0) return [text];
  // Strip trailing whitespace/newlines before wrapping.
  // formatToken() adds EOL to paragraphs and other token types,
  // which would otherwise create extra blank lines in table cells.

```

---


### `src/components/MemoryUsageIndicator.tsx`

**信息:**
- 行数: 37
- 大小: 4377 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { useMemoryUsage } from '../hooks/useMemoryUsage.js';
import { Box, Text } from '../ink.js';
import { formatFileSize } from '../utils/format.js';
export function MemoryUsageIndicator(): React.ReactNode {
  // Ant-only: the /heapdump link is an internal debugging aid. Gating before
  // the hook means the 10s polling interval is never set up in external builds.
  // USER_TYPE is a build-time constant, so the hook call below is either always
  // reached or dead-code-eliminated — never conditional at runtime.
  if ("external" !== 'ant') {
    return null;
  }

  // eslint-disable-next-line react-hooks/rules-of-hooks
  // biome-ignore lint/correctness/useHookAtTopLevel: USER_TYPE is a build-time constant
  const memoryUsage = useMemoryUsage();
  if (!memoryUsage) {
    return null;
  }
  const {
    heapUsed,
    status
  } = memoryUsage;

  // Only show indicator when memory usage is high or critical
  if (status === 'normal') {
    return null;
  }
  const formattedSize = formatFileSize(heapUsed);
  const color = status === 'critical' ? 'error' : 'warning';
  return <Box>
      <Text color={color} wrap="truncate">
        High memory usage ({formattedSize}) · /heapdump
      </Text>
    </Box>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsInVzZU1lbW9yeVVzYWdlIiwiQm94IiwiVGV4dCIsImZvcm1hdEZpbGVTaXplIiwiTWVtb3J5VXNhZ2VJbmRpY2F0b3IiLCJSZWFjdE5vZGUiLCJtZW1vcnlVc2FnZSIsImhlYXBVc2VkIiwic3RhdHVzIiwiZm9ybWF0dGVkU2l6ZSIsImNvbG9yIl0sInNvdXJjZXMiOlsiTWVtb3J5VXNhZ2VJbmRpY2F0b3IudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgdXNlTWVtb3J5VXNhZ2UgfSBmcm9tICcuLi9ob29rcy91c2VNZW1vcnlVc2FnZS5qcydcbmltcG9ydCB7IEJveCwgVGV4dCB9IGZyb20gJy4uL2luay5qcydcbmltcG9ydCB7IGZvcm1hdEZpbGVTaXplIH0gZnJvbSAnLi4vdXRpbHMvZm9ybWF0LmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gTWVtb3J5VXNhZ2VJbmRpY2F0b3IoKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgLy8gQW50LW9ubHk6IHRoZSAvaGVhcGR1bXAgbGluayBpcyBhbiBpbnRlcm5hbCBkZWJ1Z2dpbmcgYWlkLiBHYXRpbmcgYmVmb3JlXG4gIC8vIHRoZSBob29rIG1lYW5zIHRoZSAxMHMgcG9sbGluZyBpbnRlcnZhbCBpcyBuZXZlciBzZXQgdXAgaW4gZXh0ZXJuYWwgYnVpbGRzLlxuICAvLyBVU0VSX1RZUEUgaXMgYSBidWlsZC10aW1lIGNvbnN0YW50LCBzbyB0aGUgaG9vayBjYWxsIGJlbG93IGlzIGVpdGhlciBhbHdheXNcbiAgLy8gcmVhY2hlZCBvciBkZWFkLWNvZGUtZWxpbWluYXRlZCDigJQgbmV2ZXIgY29uZGl0aW9uYWwgYXQgcnVudGltZS5cbiAgaWYgKFwiZXh0ZXJuYWxcIiAhPT0gJ2FudCcpIHtcbiAgICByZXR1cm4gbnVsbFxuICB9XG5cbiAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIHJlYWN0LWhvb2tzL3J1bGVzLW9mLWhvb2tzXG4gIC8vIGJpb21lLWlnbm9yZSBsaW50L2NvcnJlY3RuZXNzL3VzZUhvb2tBdFRvcExldmVsOiBVU0VSX1RZUEUgaXMgYSBidWlsZC10aW1lIGNvbnN0YW50XG4gIGNvbnN0IG1lbW9yeVVzYWdlID0gdXNlTWVtb3J5VXNhZ2UoKVxuXG4gIGlmICghbWVtb3J5VXNhZ2UpIHtcbiAgICByZXR1cm4gbnVsbFxuICB9XG5cbiAgY29uc3QgeyBoZWFwVXNlZCwgc3RhdHVzIH0gPSBtZW1vcnlVc2FnZVxuXG4gIC8vIE9ubHkgc2hvdyBpbmRpY2F0b3Igd2hlbiBtZW1vcnkgdXNhZ2UgaXMgaGlnaCBvciBjcml0aWNhbFxuICBpZiAoc3RhdHVzID09PSAnbm9ybWFsJykge1xuICAgIHJldHVybiBudWxsXG4gIH1cblxuICBjb25zdCBmb3JtYXR0ZWRTaXplID0gZm9ybWF0RmlsZVNpemUoaGVhcFVzZWQpXG4gIGNvbnN0IGNvbG9yID0gc3RhdHVzID09PSAnY3JpdGljYWwnID8gJ2Vycm9yJyA6ICd3YXJuaW5nJ1xuXG4gIHJldHVybiAoXG4gICAgPEJveD5cbiAgICAgIDxUZXh0IGNvbG9yPXtjb2xvcn0gd3JhcD1cInRydW5jYXRlXCI+XG4gICAgICAgIEhpZ2ggbWVtb3J5IHVzYWdlICh7Zm9ybWF0dGVkU2l6ZX0pIMK3IC9oZWFwZHVtcFxuICAgICAgPC9UZXh0PlxuICAgIDwvQm94PlxuICApXG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsY0FBYyxRQUFRLDRCQUE0QjtBQUMzRCxTQUFTQyxHQUFHLEVBQUVDLElBQUksUUFBUSxXQUFXO0FBQ3JDLFNBQVNDLGNBQWMsUUFBUSxvQkFBb0I7QUFFbkQsT0FBTyxTQUFTQyxvQkFBb0JBLENBQUEsQ0FBRSxFQUFFTCxLQUFLLENBQUNNLFNBQVMsQ0FBQztFQUN0RDtFQUNBO0VBQ0E7RUFDQTtFQUNBLElBQUksVUFBVSxLQUFLLEtBQUssRUFBRTtJQUN4QixPQUFPLElBQUk7RUFDYjs7RUFFQTtFQUNBO0VBQ0EsTUFBTUMsV0FBVyxHQUFHTixjQUFjLENBQUMsQ0FBQztFQUVwQyxJQUFJLENBQUNNLFdBQVcsRUFBRTtJQUNoQixPQUFPLElBQUk7RUFDYjtFQUVBLE1BQU07SUFBRUMsUUFBUTtJQUFFQztFQUFPLENBQUMsR0FBR0YsV0FBVzs7RUFFeEM7RUFDQSxJQUFJRSxNQUFNLEtBQUssUUFBUSxFQUFFO0lBQ3ZCLE9BQU8sSUFBSTtFQUNiO0VBRUEsTUFBTUMsYUFBYSxHQUFHTixjQUFjLENBQUNJLFFBQVEsQ0FBQztFQUM5QyxNQUFNRyxLQUFLLEdBQUdGLE1BQU0sS0FBSyxVQUFVLEdBQUcsT0FBTyxHQUFHLFNBQVM7RUFFekQsT0FDRSxDQUFDLEdBQUc7QUFDUixNQUFNLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxDQUFDRSxLQUFLLENBQUMsQ0FBQyxJQUFJLENBQUMsVUFBVTtBQUN6QywyQkFBMkIsQ0FBQ0QsYUFBYSxDQUFDO0FBQzFDLE1BQU0sRUFBRSxJQUFJO0FBQ1osSUFBSSxFQUFFLEdBQUcsQ0FBQztBQUVWIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/Message.tsx`

**信息:**
- 行数: 627
- 大小: 79113 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import type { BetaContentBlock } from '@anthropic-ai/sdk/resources/beta/messages/messages.mjs';
import type { ImageBlockParam, TextBlockParam, ThinkingBlockParam, ToolResultBlockParam, ToolUseBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import type { Command } from '../commands.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { Box } from '../ink.js';
import type { Tools } from '../Tool.js';
import { type ConnectorTextBlock, isConnectorTextBlock } from '../types/connectorText.js';
import type { AssistantMessage, AttachmentMessage as AttachmentMessageType, CollapsedReadSearchGroup as CollapsedReadSearchGroupType, GroupedToolUseMessage as GroupedToolUseMessageType, NormalizedUserMessage, ProgressMessage, SystemMessage } from '../types/message.js';
import { type AdvisorBlock, isAdvisorBlock } from '../utils/advisor.js';
import { isFullscreenEnvEnabled } from '../utils/fullscreen.js';
import { logError } from '../utils/log.js';
import type { buildMessageLookups } from '../utils/messages.js';
import { CompactSummary } from './CompactSummary.js';
import { AdvisorMessage } from './messages/AdvisorMessage.js';
import { AssistantRedactedThinkingMessage } from './messages/AssistantRedactedThinkingMessage.js';
import { AssistantTextMessage } from './messages/AssistantTextMessage.js';
import { AssistantThinkingMessage } from './messages/AssistantThinkingMessage.js';
import { AssistantToolUseMessage } from './messages/AssistantToolUseMessage.js';
import { AttachmentMessage } from './messages/AttachmentMessage.js';
import { CollapsedReadSearchContent } from './messages/CollapsedReadSearchContent.js';
import { CompactBoundaryMessage } from './messages/CompactBoundaryMessage.js';
import { GroupedToolUseContent } from './messages/GroupedToolUseContent.js';
import { SystemTextMessage } from './messages/SystemTextMessage.js';
import { UserImageMessage } from './messages/UserImageMessage.js';
import { UserTextMessage } from './messages/UserTextMessage.js';
import { UserToolResultMessage } from './messages/UserToolResultMessage/UserToolResultMessage.js';
import { OffscreenFreeze } from './OffscreenFreeze.js';
import { ExpandShellOutputProvider } from './shell/ExpandShellOutputContext.js';
export type Props = {
  message: NormalizedUserMessage | AssistantMessage | AttachmentMessageType | SystemMessage | GroupedToolUseMessageType | CollapsedReadSearchGroupType;
  lookups: ReturnType<typeof buildMessageLookups>;
  // TODO: Find a way to remove this, and leave spacing to the consumer
  /** Absolute width for the container Box. When provided, eliminates a wrapper Box in the caller. */
  containerWidth?: number;
  addMargin: boolean;
  tools: Tools;
  commands: Command[];
  verbose: boolean;
  inProgressToolUseIDs: Set<string>;
  progressMessagesForMessage: ProgressMessage[];
  shouldAnimate: boolean;
  shouldShowDot: boolean;
  style?: 'condensed';
  width?: number | string;
  isTranscriptMode: boolean;
  isStatic: boolean;
  onOpenRateLimitOptions?: () => void;

```

---


### `src/components/MessageModel.tsx`

**信息:**
- 行数: 43
- 大小: 4110 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { stringWidth } from '../ink/stringWidth.js';
import { Box, Text } from '../ink.js';
import type { NormalizedMessage } from '../types/message.js';
type Props = {
  message: NormalizedMessage;
  isTranscriptMode: boolean;
};
export function MessageModel(t0) {
  const $ = _c(5);
  const {
    message,
    isTranscriptMode
  } = t0;
  const shouldShowModel = isTranscriptMode && message.type === "assistant" && message.message.model && message.message.content.some(_temp);
  if (!shouldShowModel) {
    return null;
  }
  const t1 = stringWidth(message.message.model) + 8;
  let t2;
  if ($[0] !== message.message.model) {
    t2 = <Text dimColor={true}>{message.message.model}</Text>;
    $[0] = message.message.model;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  let t3;
  if ($[2] !== t1 || $[3] !== t2) {
    t3 = <Box minWidth={t1}>{t2}</Box>;
    $[2] = t1;
    $[3] = t2;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  return t3;
}
function _temp(c) {
  return c.type === "text";
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsInN0cmluZ1dpZHRoIiwiQm94IiwiVGV4dCIsIk5vcm1hbGl6ZWRNZXNzYWdlIiwiUHJvcHMiLCJtZXNzYWdlIiwiaXNUcmFuc2NyaXB0TW9kZSIsIk1lc3NhZ2VNb2RlbCIsInQwIiwiJCIsIl9jIiwic2hvdWxkU2hvd01vZGVsIiwidHlwZSIsIm1vZGVsIiwiY29udGVudCIsInNvbWUiLCJfdGVtcCIsInQxIiwidDIiLCJ0MyIsImMiXSwic291cmNlcyI6WyJNZXNzYWdlTW9kZWwudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IHN0cmluZ1dpZHRoIH0gZnJvbSAnLi4vaW5rL3N0cmluZ1dpZHRoLmpzJ1xuaW1wb3J0IHsgQm94LCBUZXh0IH0gZnJvbSAnLi4vaW5rLmpzJ1xuaW1wb3J0IHR5cGUgeyBOb3JtYWxpemVkTWVzc2FnZSB9IGZyb20gJy4uL3R5cGVzL21lc3NhZ2UuanMnXG5cbnR5cGUgUHJvcHMgPSB7XG4gIG1lc3NhZ2U6IE5vcm1hbGl6ZWRNZXNzYWdlXG4gIGlzVHJhbnNjcmlwdE1vZGU6IGJvb2xlYW5cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIE1lc3NhZ2VNb2RlbCh7XG4gIG1lc3NhZ2UsXG4gIGlzVHJhbnNjcmlwdE1vZGUsXG59OiBQcm9wcyk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIGNvbnN0IHNob3VsZFNob3dNb2RlbCA9XG4gICAgaXNUcmFuc2NyaXB0TW9kZSAmJlxuICAgIG1lc3NhZ2UudHlwZSA9PT0gJ2Fzc2lzdGFudCcgJiZcbiAgICBtZXNzYWdlLm1lc3NhZ2UubW9kZWwgJiZcbiAgICBtZXNzYWdlLm1lc3NhZ2UuY29udGVudC5zb21lKGMgPT4gYy50eXBlID09PSAndGV4dCcpXG5cbiAgaWYgKCFzaG91bGRTaG93TW9kZWwpIHtcbiAgICByZXR1cm4gbnVsbFxuICB9XG5cbiAgcmV0dXJuIChcbiAgICA8Qm94IG1pbldpZHRoPXtzdHJpbmdXaWR0aChtZXNzYWdlLm1lc3NhZ2UubW9kZWwpICsgOH0+XG4gICAgICA8VGV4dCBkaW1Db2xvcj57bWVzc2FnZS5tZXNzYWdlLm1vZGVsfTwvVGV4dD5cbiAgICA8L0JveD5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiO0FBQUEsT0FBT0EsS0FBSyxNQUFNLE9BQU87QUFDekIsU0FBU0MsV0FBVyxRQUFRLHVCQUF1QjtBQUNuRCxTQUFTQyxHQUFHLEVBQUVDLElBQUksUUFBUSxXQUFXO0FBQ3JDLGNBQWNDLGlCQUFpQixRQUFRLHFCQUFxQjtBQUU1RCxLQUFLQyxLQUFLLEdBQUc7RUFDWEMsT0FBTyxFQUFFRixpQkFBaUI7RUFDMUJHLGdCQUFnQixFQUFFLE9BQU87QUFDM0IsQ0FBQztBQUVELE9BQU8sU0FBQUMsYUFBQUMsRUFBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUFzQjtJQUFBTCxPQUFBO0lBQUFDO0VBQUEsSUFBQUUsRUFHckI7RUFDTixNQUFBRyxlQUFBLEdBQ0VMLGdCQUM0QixJQUE1QkQsT0FBTyxDQUFBTyxJQUFLLEtBQUssV0FDSSxJQUFyQlAsT0FBTyxDQUFBQSxPQUFRLENBQUFRLEtBQ3FDLElBQXBEUixPQUFPLENBQUFBLE9BQVEsQ0FBQVMsT0FBUSxDQUFBQyxJQUFLLENBQUNDLEtBQXNCLENBQUM7RUFFdEQsSUFBSSxDQUFDTCxlQUFlO0lBQUEsT0FDWCxJQUFJO0VBQUE7RUFJSSxNQUFBTSxFQUFBLEdBQUFqQixXQUFXLENBQUNLLE9BQU8sQ0FBQUEsT0FBUSxDQUFBUSxLQUFNLENBQUMsR0FBRyxDQUFDO0VBQUEsSUFBQUssRUFBQTtFQUFBLElBQUFULENBQUEsUUFBQUosT0FBQSxDQUFBQSxPQUFBLENBQUFRLEtBQUE7SUFDbkRLLEVBQUEsSUFBQyxJQUFJLENBQUMsUUFBUSxDQUFSLEtBQU8sQ0FBQyxDQUFFLENBQUFiLE9BQU8sQ0FBQUEsT0FBUSxDQUFBUSxLQUFLLENBQUUsRUFBckMsSUFBSSxDQUF3QztJQUFBSixDQUFBLE1BQUFKLE9BQUEsQ0FBQUEsT0FBQSxDQUFBUSxLQUFBO0lBQUFKLENBQUEsTUFBQVMsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQVQsQ0FBQTtFQUFBO0VBQUEsSUFBQVUsRUFBQTtFQUFBLElBQUFWLENBQUEsUUFBQVEsRUFBQSxJQUFBUixDQUFBLFFBQUFTLEVBQUE7SUFEL0NDLEVBQUEsSUFBQyxHQUFHLENBQVcsUUFBc0MsQ0FBdEMsQ0FBQUYsRUFBcUMsQ0FBQyxDQUNuRCxDQUFBQyxFQUE0QyxDQUM5QyxFQUZDLEdBQUcsQ0FFRTtJQUFBVCxDQUFBLE1BQUFRLEVBQUE7SUFBQVIsQ0FBQSxNQUFBUyxFQUFBO0lBQUFULENBQUEsTUFBQVUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQVYsQ0FBQTtFQUFBO0VBQUEsT0FGTlUsRUFFTTtBQUFBO0FBakJILFNBQUFILE1BQUFJLENBQUE7RUFBQSxPQVErQkEsQ0FBQyxDQUFBUixJQUFLLEtBQUssTUFBTTtBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/MessageResponse.tsx`

**信息:**
- 行数: 78
- 大小: 6933 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useContext } from 'react';
import { Box, NoSelect, Text } from '../ink.js';
import { Ratchet } from './design-system/Ratchet.js';
type Props = {
  children: React.ReactNode;
  height?: number;
};
export function MessageResponse(t0) {
  const $ = _c(8);
  const {
    children,
    height
  } = t0;
  const isMessageResponse = useContext(MessageResponseContext);
  if (isMessageResponse) {
    return children;
  }
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <NoSelect fromLeftEdge={true} flexShrink={0}><Text dimColor={true}>{"  "}⎿  </Text></NoSelect>;
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  let t2;
  if ($[1] !== children) {
    t2 = <Box flexShrink={1} flexGrow={1}>{children}</Box>;
    $[1] = children;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  let t3;
  if ($[3] !== height || $[4] !== t2) {
    t3 = <MessageResponseProvider><Box flexDirection="row" height={height} overflowY="hidden">{t1}{t2}</Box></MessageResponseProvider>;
    $[3] = height;
    $[4] = t2;
    $[5] = t3;
  } else {
    t3 = $[5];
  }
  const content = t3;
  if (height !== undefined) {
    return content;
  }
  let t4;
  if ($[6] !== content) {
    t4 = <Ratchet lock="offscreen">{content}</Ratchet>;

```

---


### `src/components/MessageRow.tsx`

**信息:**
- 行数: 383
- 大小: 48342 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import type { Command } from '../commands.js';
import { Box } from '../ink.js';
import type { Screen } from '../screens/REPL.js';
import type { Tools } from '../Tool.js';
import type { RenderableMessage } from '../types/message.js';
import { getDisplayMessageFromCollapsed, getToolSearchOrReadInfo, getToolUseIdsFromCollapsedGroup, hasAnyToolInProgress } from '../utils/collapseReadSearch.js';
import { type buildMessageLookups, EMPTY_STRING_SET, getProgressMessagesFromLookup, getSiblingToolUseIDsFromLookup, getToolUseID } from '../utils/messages.js';
import { hasThinkingContent, Message } from './Message.js';
import { MessageModel } from './MessageModel.js';
import { shouldRenderStatically } from './Messages.js';
import { MessageTimestamp } from './MessageTimestamp.js';
import { OffscreenFreeze } from './OffscreenFreeze.js';
export type Props = {
  message: RenderableMessage;
  /** Whether the previous message in renderableMessages is also a user message. */
  isUserContinuation: boolean;
  /**
   * Whether there is non-skippable content after this message in renderableMessages.
   * Only needs to be accurate for `collapsed_read_search` messages — used to decide
   * if the collapsed group spinner should stay active. Pass `false` otherwise.
   */
  hasContentAfter: boolean;
  tools: Tools;
  commands: Command[];
  verbose: boolean;
  inProgressToolUseIDs: Set<string>;
  streamingToolUseIDs: Set<string>;
  screen: Screen;
  canAnimate: boolean;
  onOpenRateLimitOptions?: () => void;
  lastThinkingBlockId: string | null;
  latestBashOutputUUID: string | null;
  columns: number;
  isLoading: boolean;
  lookups: ReturnType<typeof buildMessageLookups>;
};

/**
 * Scans forward from `index+1` to check if any "real" content follows. Used to
 * decide whether a collapsed read/search group should stay in its active
 * (grey dot, present-tense "Reading…") state while the query is still loading.
 *
 * Exported so Messages.tsx can compute this once per message and pass the
 * result as a boolean prop — avoids passing the full `renderableMessages` array
 * to each MessageRow (which React Compiler would pin in the fiber's memoCache,
 * accumulating every historical version of the array ≈ 1-2MB over a 7-turn session).
 */
export function hasContentAfterIndex(messages: RenderableMessage[], index: number, tools: Tools, streamingToolUseIDs: Set<string>): boolean {

```

---


### `src/components/MessageSelector.tsx`

**信息:**
- 行数: 831
- 大小: 115618 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ContentBlockParam, TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import { randomUUID, type UUID } from 'crypto';
import figures from 'figures';
import * as React from 'react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { useAppState } from 'src/state/AppState.js';
import { type DiffStats, fileHistoryCanRestore, fileHistoryEnabled, fileHistoryGetDiffStats } from 'src/utils/fileHistory.js';
import { logError } from 'src/utils/log.js';
import { useExitOnCtrlCDWithKeybindings } from '../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Text } from '../ink.js';
import { useKeybinding, useKeybindings } from '../keybindings/useKeybinding.js';
import type { Message, PartialCompactDirection, UserMessage } from '../types/message.js';
import { stripDisplayTags } from '../utils/displayTags.js';
import { createUserMessage, extractTag, isEmptyMessageText, isSyntheticMessage, isToolUseResultMessage } from '../utils/messages.js';
import { type OptionWithDescription, Select } from './CustomSelect/select.js';
import { Spinner } from './Spinner.js';
function isTextBlock(block: ContentBlockParam): block is TextBlockParam {
  return block.type === 'text';
}
import * as path from 'path';
import { useTerminalSize } from 'src/hooks/useTerminalSize.js';
import type { FileEditOutput } from 'src/tools/FileEditTool/types.js';
import type { Output as FileWriteToolOutput } from 'src/tools/FileWriteTool/FileWriteTool.js';
import { BASH_STDERR_TAG, BASH_STDOUT_TAG, COMMAND_MESSAGE_TAG, LOCAL_COMMAND_STDERR_TAG, LOCAL_COMMAND_STDOUT_TAG, TASK_NOTIFICATION_TAG, TEAMMATE_MESSAGE_TAG, TICK_TAG } from '../constants/xml.js';
import { count } from '../utils/array.js';
import { formatRelativeTimeAgo, truncate } from '../utils/format.js';
import type { Theme } from '../utils/theme.js';
import { Divider } from './design-system/Divider.js';
type RestoreOption = 'both' | 'conversation' | 'code' | 'summarize' | 'summarize_up_to' | 'nevermind';
function isSummarizeOption(option: RestoreOption | null): option is 'summarize' | 'summarize_up_to' {
  return option === 'summarize' || option === 'summarize_up_to';
}
type Props = {
  messages: Message[];
  onPreRestore: () => void;
  onRestoreMessage: (message: UserMessage) => Promise<void>;
  onRestoreCode: (message: UserMessage) => Promise<void>;
  onSummarize: (message: UserMessage, feedback?: string, direction?: PartialCompactDirection) => Promise<void>;
  onClose: () => void;
  /** Skip pick-list, land on confirm. Caller ran skip-check first. Esc closes fully (no back-to-list). */
  preselectedMessage?: UserMessage;
};
const MAX_VISIBLE_MESSAGES = 7;
export function MessageSelector({
  messages,
  onPreRestore,
  onRestoreMessage,
  onRestoreCode,

```

---


### `src/components/MessageTimestamp.tsx`

**信息:**
- 行数: 63
- 大小: 5448 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { stringWidth } from '../ink/stringWidth.js';
import { Box, Text } from '../ink.js';
import type { NormalizedMessage } from '../types/message.js';
type Props = {
  message: NormalizedMessage;
  isTranscriptMode: boolean;
};
export function MessageTimestamp(t0) {
  const $ = _c(10);
  const {
    message,
    isTranscriptMode
  } = t0;
  const shouldShowTimestamp = isTranscriptMode && message.timestamp && message.type === "assistant" && message.message.content.some(_temp);
  if (!shouldShowTimestamp) {
    return null;
  }
  let T0;
  let formattedTimestamp;
  let t1;
  if ($[0] !== message.timestamp) {
    formattedTimestamp = new Date(message.timestamp).toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true
    });
    T0 = Box;
    t1 = stringWidth(formattedTimestamp);
    $[0] = message.timestamp;
    $[1] = T0;
    $[2] = formattedTimestamp;
    $[3] = t1;
  } else {
    T0 = $[1];
    formattedTimestamp = $[2];
    t1 = $[3];
  }
  let t2;
  if ($[4] !== formattedTimestamp) {
    t2 = <Text dimColor={true}>{formattedTimestamp}</Text>;
    $[4] = formattedTimestamp;
    $[5] = t2;
  } else {
    t2 = $[5];
  }
  let t3;
  if ($[6] !== T0 || $[7] !== t1 || $[8] !== t2) {
    t3 = <T0 minWidth={t1}>{t2}</T0>;

```

---


### `src/components/Messages.tsx`

**信息:**
- 行数: 834
- 大小: 147457 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import chalk from 'chalk';
import type { UUID } from 'crypto';
import type { RefObject } from 'react';
import * as React from 'react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { every } from 'src/utils/set.js';
import { getIsRemoteMode } from '../bootstrap/state.js';
import type { Command } from '../commands.js';
import { BLACK_CIRCLE } from '../constants/figures.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import type { ScrollBoxHandle } from '../ink/components/ScrollBox.js';
import { useTerminalNotification } from '../ink/useTerminalNotification.js';
import { Box, Text } from '../ink.js';
import { useShortcutDisplay } from '../keybindings/useShortcutDisplay.js';
import type { Screen } from '../screens/REPL.js';
import type { Tools } from '../Tool.js';
import { findToolByName } from '../Tool.js';
import type { AgentDefinitionsResult } from '../tools/AgentTool/loadAgentsDir.js';
import type { Message as MessageType, NormalizedMessage, ProgressMessage as ProgressMessageType, RenderableMessage } from '../types/message.js';
import { type AdvisorBlock, isAdvisorBlock } from '../utils/advisor.js';
import { collapseBackgroundBashNotifications } from '../utils/collapseBackgroundBashNotifications.js';
import { collapseHookSummaries } from '../utils/collapseHookSummaries.js';
import { collapseReadSearchGroups } from '../utils/collapseReadSearch.js';
import { collapseTeammateShutdowns } from '../utils/collapseTeammateShutdowns.js';
import { getGlobalConfig } from '../utils/config.js';
import { isEnvTruthy } from '../utils/envUtils.js';
import { isFullscreenEnvEnabled } from '../utils/fullscreen.js';
import { applyGrouping } from '../utils/groupToolUses.js';
import { buildMessageLookups, createAssistantMessage, deriveUUID, getMessagesAfterCompactBoundary, getToolUseID, getToolUseIDs, hasUnresolvedHooksFromLookup, isNotEmptyMessage, normalizeMessages, reorderMessagesInUI, type StreamingThinking, type StreamingToolUse, shouldShowUserMessage } from '../utils/messages.js';
import { plural } from '../utils/stringUtils.js';
import { renderableSearchText } from '../utils/transcriptSearch.js';
import { Divider } from './design-system/Divider.js';
import type { UnseenDivider } from './FullscreenLayout.js';
import { LogoV2 } from './LogoV2/LogoV2.js';
import { StreamingMarkdown } from './Markdown.js';
import { hasContentAfterIndex, MessageRow } from './MessageRow.js';
import { InVirtualListContext, type MessageActionsNav, MessageActionsSelectedContext, type MessageActionsState } from './messageActions.js';
import { AssistantThinkingMessage } from './messages/AssistantThinkingMessage.js';
import { isNullRenderingAttachment } from './messages/nullRenderingAttachments.js';
import { OffscreenFreeze } from './OffscreenFreeze.js';
import type { ToolUseConfirm } from './permissions/PermissionRequest.js';
import { StatusNotices } from './StatusNotices.js';
import type { JumpHandle } from './VirtualMessageList.js';

// Memoed logo header: this box is the FIRST sibling before all MessageRows
// in main-screen mode. If it becomes dirty on every Messages re-render,
// renderChildren's seenDirtyChild cascade disables prevScreen (blit) for
// ALL subsequent siblings — every MessageRow re-writes from scratch instead

```

---


### `src/components/ModelPicker.tsx`

**信息:**
- 行数: 448
- 大小: 54246 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import capitalize from 'lodash-es/capitalize.js';
import * as React from 'react';
import { useCallback, useMemo, useState } from 'react';
import { useExitOnCtrlCDWithKeybindings } from 'src/hooks/useExitOnCtrlCDWithKeybindings.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { FAST_MODE_MODEL_DISPLAY, isFastModeAvailable, isFastModeCooldown, isFastModeEnabled } from 'src/utils/fastMode.js';
import { Box, Text } from '../ink.js';
import { useKeybindings } from '../keybindings/useKeybinding.js';
import { useAppState, useSetAppState } from '../state/AppState.js';
import { convertEffortValueToLevel, type EffortLevel, getDefaultEffortForModel, modelSupportsEffort, modelSupportsMaxEffort, resolvePickerEffortPersistence, toPersistableEffort } from '../utils/effort.js';
import { getDefaultMainLoopModel, type ModelSetting, modelDisplayString, parseUserSpecifiedModel } from '../utils/model/model.js';
import { getModelOptions } from '../utils/model/modelOptions.js';
import { getSettingsForSource, updateSettingsForSource } from '../utils/settings/settings.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { Select } from './CustomSelect/index.js';
import { Byline } from './design-system/Byline.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import { Pane } from './design-system/Pane.js';
import { effortLevelToSymbol } from './EffortIndicator.js';
export type Props = {
  initial: string | null;
  sessionModel?: ModelSetting;
  onSelect: (model: string | null, effort: EffortLevel | undefined) => void;
  onCancel?: () => void;
  isStandaloneCommand?: boolean;
  showFastModeNotice?: boolean;
  /** Overrides the dim header line below "Select model". */
  headerText?: string;
  /**
   * When true, skip writing effortLevel to userSettings on selection.
   * Used by the assistant installer wizard where the model choice is
   * project-scoped (written to the assistant's .claude/settings.json via
   * install.ts) and should not leak to the user's global ~/.claude/settings.
   */
  skipSettingsWrite?: boolean;
};
const NO_PREFERENCE = '__NO_PREFERENCE__';
export function ModelPicker(t0) {
  const $ = _c(82);
  const {
    initial,
    sessionModel,
    onSelect,
    onCancel,
    isStandaloneCommand,
    showFastModeNotice,
    headerText,
    skipSettingsWrite
  } = t0;

```

---


### `src/components/NativeAutoUpdater.tsx`

**信息:**
- 行数: 193
- 大小: 26514 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { logEvent } from 'src/services/analytics/index.js';
import { logForDebugging } from 'src/utils/debug.js';
import { logError } from 'src/utils/log.js';
import { useInterval } from 'usehooks-ts';
import { useUpdateNotification } from '../hooks/useUpdateNotification.js';
import { Box, Text } from '../ink.js';
import type { AutoUpdaterResult } from '../utils/autoUpdater.js';
import { getMaxVersion, getMaxVersionMessage } from '../utils/autoUpdater.js';
import { isAutoUpdaterDisabled } from '../utils/config.js';
import { installLatest } from '../utils/nativeInstaller/index.js';
import { gt } from '../utils/semver.js';
import { getInitialSettings } from '../utils/settings/settings.js';

/**
 * Categorize error messages for analytics
 */
function getErrorType(errorMessage: string): string {
  if (errorMessage.includes('timeout')) {
    return 'timeout';
  }
  if (errorMessage.includes('Checksum mismatch')) {
    return 'checksum_mismatch';
  }
  if (errorMessage.includes('ENOENT') || errorMessage.includes('not found')) {
    return 'not_found';
  }
  if (errorMessage.includes('EACCES') || errorMessage.includes('permission')) {
    return 'permission_denied';
  }
  if (errorMessage.includes('ENOSPC')) {
    return 'disk_full';
  }
  if (errorMessage.includes('npm')) {
    return 'npm_error';
  }
  if (errorMessage.includes('network') || errorMessage.includes('ECONNREFUSED') || errorMessage.includes('ENOTFOUND')) {
    return 'network_error';
  }
  return 'unknown';
}
type Props = {
  isUpdating: boolean;
  onChangeIsUpdating: (isUpdating: boolean) => void;
  onAutoUpdaterResult: (autoUpdaterResult: AutoUpdaterResult) => void;
  autoUpdaterResult: AutoUpdaterResult | null;
  showSuccessMessage: boolean;
  verbose: boolean;
};

```

---


### `src/components/NotebookEditToolUseRejectedMessage.tsx`

**信息:**
- 行数: 92
- 大小: 8447 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { relative } from 'path';
import * as React from 'react';
import { getCwd } from 'src/utils/cwd.js';
import { Box, Text } from '../ink.js';
import { HighlightedCode } from './HighlightedCode.js';
import { MessageResponse } from './MessageResponse.js';
type Props = {
  notebook_path: string;
  cell_id: string | undefined;
  new_source: string;
  cell_type?: 'code' | 'markdown';
  edit_mode?: 'replace' | 'insert' | 'delete';
  verbose: boolean;
};
export function NotebookEditToolUseRejectedMessage(t0) {
  const $ = _c(20);
  const {
    notebook_path,
    cell_id,
    new_source,
    cell_type,
    edit_mode: t1,
    verbose
  } = t0;
  const edit_mode = t1 === undefined ? "replace" : t1;
  const operation = edit_mode === "delete" ? "delete" : `${edit_mode} cell in`;
  let t2;
  if ($[0] !== operation) {
    t2 = <Text color="subtle">User rejected {operation} </Text>;
    $[0] = operation;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  let t3;
  if ($[2] !== notebook_path || $[3] !== verbose) {
    t3 = verbose ? notebook_path : relative(getCwd(), notebook_path);
    $[2] = notebook_path;
    $[3] = verbose;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  let t4;
  if ($[5] !== t3) {
    t4 = <Text bold={true} color="subtle">{t3}</Text>;
    $[5] = t3;
    $[6] = t4;
  } else {

```

---


### `src/components/OffscreenFreeze.tsx`

**信息:**
- 行数: 44
- 大小: 5664 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React, { useContext, useRef } from 'react';
import { useTerminalViewport } from '../ink/hooks/use-terminal-viewport.js';
import { Box } from '../ink.js';
import { InVirtualListContext } from './messageActions.js';
type Props = {
  children: React.ReactNode;
};

/**
 * Freezes children when they scroll above the terminal viewport (into scrollback).
 *
 * Any content change above the viewport forces log-update.ts into a full terminal
 * reset (it cannot partially update rows that have scrolled out). For content that
 * updates on a timer — spinners, elapsed counters — this produces a reset per tick.
 *
 * When offscreen, returns the same ReactElement reference that was cached during
 * the last visible render. React's reconciler bails on identical element refs, so
 * the subtree never re-renders, producing zero diff.
 *
 * The cache is one slot deep: the first re-render after scrolling back into view
 * picks up the live children. Content still updates normally while visible.
 */
export function OffscreenFreeze({
  children
}: Props): React.ReactNode {
  // React Compiler: reading cached.current in the return is the entire
  // freeze mechanism — memoizing this component would defeat it. Opt out.
  'use no memo';

  const inVirtualList = useContext(InVirtualListContext);
  const [ref, {
    isVisible
  }] = useTerminalViewport();
  const cached = useRef(children);
  // Virtual list has no terminal scrollback — the ScrollBox clips inside the
  // viewport, so there's nothing to freeze. Freezing there also blocks
  // click-to-expand since useTerminalViewport's visibility calc can disagree
  // with the ScrollBox's virtual scroll position.
  if (isVisible || inVirtualList) {
    cached.current = children;
  }
  return <Box ref={ref}>{cached.current}</Box>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsInVzZUNvbnRleHQiLCJ1c2VSZWYiLCJ1c2VUZXJtaW5hbFZpZXdwb3J0IiwiQm94IiwiSW5WaXJ0dWFsTGlzdENvbnRleHQiLCJQcm9wcyIsImNoaWxkcmVuIiwiUmVhY3ROb2RlIiwiT2Zmc2NyZWVuRnJlZXplIiwiaW5WaXJ0dWFsTGlzdCIsInJlZiIsImlzVmlzaWJsZSIsImNhY2hlZCIsImN1cnJlbnQiXSwic291cmNlcyI6WyJPZmZzY3JlZW5GcmVlemUudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCBSZWFjdCwgeyB1c2VDb250ZXh0LCB1c2VSZWYgfSBmcm9tICdyZWFjdCdcbmltcG9ydCB7IHVzZVRlcm1pbmFsVmlld3BvcnQgfSBmcm9tICcuLi9pbmsvaG9va3MvdXNlLXRlcm1pbmFsLXZpZXdwb3J0LmpzJ1xuaW1wb3J0IHsgQm94IH0gZnJvbSAnLi4vaW5rLmpzJ1xuaW1wb3J0IHsgSW5WaXJ0dWFsTGlzdENvbnRleHQgfSBmcm9tICcuL21lc3NhZ2VBY3Rpb25zLmpzJ1xuXG50eXBlIFByb3BzID0ge1xuICBjaGlsZHJlbjogUmVhY3QuUmVhY3ROb2RlXG59XG5cbi8qKlxuICogRnJlZXplcyBjaGlsZHJlbiB3aGVuIHRoZXkgc2Nyb2xsIGFib3ZlIHRoZSB0ZXJtaW5hbCB2aWV3cG9ydCAoaW50byBzY3JvbGxiYWNrKS5cbiAqXG4gKiBBbnkgY29udGVudCBjaGFuZ2UgYWJvdmUgdGhlIHZpZXdwb3J0IGZvcmNlcyBsb2ctdXBkYXRlLnRzIGludG8gYSBmdWxsIHRlcm1pbmFsXG4gKiByZXNldCAoaXQgY2Fubm90IHBhcnRpYWxseSB1cGRhdGUgcm93cyB0aGF0IGhhdmUgc2Nyb2xsZWQgb3V0KS4gRm9yIGNvbnRlbnQgdGhhdFxuICogdXBkYXRlcyBvbiBhIHRpbWVyIOKAlCBzcGlubmVycywgZWxhcHNlZCBjb3VudGVycyDigJQgdGhpcyBwcm9kdWNlcyBhIHJlc2V0IHBlciB0aWNrLlxuICpcbiAqIFdoZW4gb2Zmc2NyZWVuLCByZXR1cm5zIHRoZSBzYW1lIFJlYWN0RWxlbWVudCByZWZlcmVuY2UgdGhhdCB3YXMgY2FjaGVkIGR1cmluZ1xuICogdGhlIGxhc3QgdmlzaWJsZSByZW5kZXIuIFJlYWN0J3MgcmVjb25jaWxlciBiYWlscyBvbiBpZGVudGljYWwgZWxlbWVudCByZWZzLCBzb1xuICogdGhlIHN1YnRyZWUgbmV2ZXIgcmUtcmVuZGVycywgcHJvZHVjaW5nIHplcm8gZGlmZi5cbiAqXG4gKiBUaGUgY2FjaGUgaXMgb25lIHNsb3QgZGVlcDogdGhlIGZpcnN0IHJlLXJlbmRlciBhZnRlciBzY3JvbGxpbmcgYmFjayBpbnRvIHZpZXdcbiAqIHBpY2tzIHVwIHRoZSBsaXZlIGNoaWxkcmVuLiBDb250ZW50IHN0aWxsIHVwZGF0ZXMgbm9ybWFsbHkgd2hpbGUgdmlzaWJsZS5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIE9mZnNjcmVlbkZyZWV6ZSh7IGNoaWxkcmVuIH06IFByb3BzKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgLy8gUmVhY3QgQ29tcGlsZXI6IHJlYWRpbmcgY2FjaGVkLmN1cnJlbnQgaW4gdGhlIHJldHVybiBpcyB0aGUgZW50aXJlXG4gIC8vIGZyZWV6ZSBtZWNoYW5pc20g4oCUIG1lbW9pemluZyB0aGlzIGNvbXBvbmVudCB3b3VsZCBkZWZlYXQgaXQuIE9wdCBvdXQuXG4gICd1c2Ugbm8gbWVtbydcbiAgY29uc3QgaW5WaXJ0dWFsTGlzdCA9IHVzZUNvbnRleHQoSW5WaXJ0dWFsTGlzdENvbnRleHQpXG4gIGNvbnN0IFtyZWYsIHsgaXNWaXNpYmxlIH1dID0gdXNlVGVybWluYWxWaWV3cG9ydCgpXG4gIGNvbnN0IGNhY2hlZCA9IHVzZVJlZihjaGlsZHJlbilcbiAgLy8gVmlydHVhbCBsaXN0IGhhcyBubyB0ZXJtaW5hbCBzY3JvbGxiYWNrIOKAlCB0aGUgU2Nyb2xsQm94IGNsaXBzIGluc2lkZSB0aGVcbiAgLy8gdmlld3BvcnQsIHNvIHRoZXJlJ3Mgbm90aGluZyB0byBmcmVlemUuIEZyZWV6aW5nIHRoZXJlIGFsc28gYmxvY2tzXG4gIC8vIGNsaWNrLXRvLWV4cGFuZCBzaW5jZSB1c2VUZXJtaW5hbFZpZXdwb3J0J3MgdmlzaWJpbGl0eSBjYWxjIGNhbiBkaXNhZ3JlZVxuICAvLyB3aXRoIHRoZSBTY3JvbGxCb3gncyB2aXJ0dWFsIHNjcm9sbCBwb3NpdGlvbi5cbiAgaWYgKGlzVmlzaWJsZSB8fCBpblZpcnR1YWxMaXN0KSB7XG4gICAgY2FjaGVkLmN1cnJlbnQgPSBjaGlsZHJlblxuICB9XG4gIHJldHVybiA8Qm94IHJlZj17cmVmfT57Y2FjaGVkLmN1cnJlbnR9PC9Cb3g+XG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU9BLEtBQUssSUFBSUMsVUFBVSxFQUFFQyxNQUFNLFFBQVEsT0FBTztBQUNqRCxTQUFTQyxtQkFBbUIsUUFBUSx1Q0FBdUM7QUFDM0UsU0FBU0MsR0FBRyxRQUFRLFdBQVc7QUFDL0IsU0FBU0Msb0JBQW9CLFFBQVEscUJBQXFCO0FBRTFELEtBQUtDLEtBQUssR0FBRztFQUNYQyxRQUFRLEVBQUVQLEtBQUssQ0FBQ1EsU0FBUztBQUMzQixDQUFDOztBQUVEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPLFNBQVNDLGVBQWVBLENBQUM7RUFBRUY7QUFBZ0IsQ0FBTixFQUFFRCxLQUFLLENBQUMsRUFBRU4sS0FBSyxDQUFDUSxTQUFTLENBQUM7RUFDcEU7RUFDQTtFQUNBLGFBQWE7O0VBQ2IsTUFBTUUsYUFBYSxHQUFHVCxVQUFVLENBQUNJLG9CQUFvQixDQUFDO0VBQ3RELE1BQU0sQ0FBQ00sR0FBRyxFQUFFO0lBQUVDO0VBQVUsQ0FBQyxDQUFDLEdBQUdULG1CQUFtQixDQUFDLENBQUM7RUFDbEQsTUFBTVUsTUFBTSxHQUFHWCxNQUFNLENBQUNLLFFBQVEsQ0FBQztFQUMvQjtFQUNBO0VBQ0E7RUFDQTtFQUNBLElBQUlLLFNBQVMsSUFBSUYsYUFBYSxFQUFFO0lBQzlCRyxNQUFNLENBQUNDLE9BQU8sR0FBR1AsUUFBUTtFQUMzQjtFQUNBLE9BQU8sQ0FBQyxHQUFHLENBQUMsR0FBRyxDQUFDLENBQUNJLEdBQUcsQ0FBQyxDQUFDLENBQUNFLE1BQU0sQ0FBQ0MsT0FBTyxDQUFDLEVBQUUsR0FBRyxDQUFDO0FBQzlDIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/Onboarding.tsx`

**信息:**
- 行数: 244
- 大小: 31528 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { setupTerminal, shouldOfferTerminalSetup } from '../commands/terminalSetup/terminalSetup.js';
import { useExitOnCtrlCDWithKeybindings } from '../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Link, Newline, Text, useTheme } from '../ink.js';
import { useKeybindings } from '../keybindings/useKeybinding.js';
import { isAnthropicAuthEnabled } from '../utils/auth.js';
import { normalizeApiKeyForConfig } from '../utils/authPortable.js';
import { getCustomApiKeyStatus } from '../utils/config.js';
import { env } from '../utils/env.js';
import { isRunningOnHomespace } from '../utils/envUtils.js';
import { PreflightStep } from '../utils/preflightChecks.js';
import type { ThemeSetting } from '../utils/theme.js';
import { ApproveApiKey } from './ApproveApiKey.js';
import { ConsoleOAuthFlow } from './ConsoleOAuthFlow.js';
import { Select } from './CustomSelect/select.js';
import { WelcomeV2 } from './LogoV2/WelcomeV2.js';
import { PressEnterToContinue } from './PressEnterToContinue.js';
import { ThemePicker } from './ThemePicker.js';
import { OrderedList } from './ui/OrderedList.js';
type StepId = 'preflight' | 'theme' | 'oauth' | 'api-key' | 'security' | 'terminal-setup';
interface OnboardingStep {
  id: StepId;
  component: React.ReactNode;
}
type Props = {
  onDone(): void;
};
export function Onboarding({
  onDone
}: Props): React.ReactNode {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [skipOAuth, setSkipOAuth] = useState(false);
  const [oauthEnabled] = useState(() => isAnthropicAuthEnabled());
  const [theme, setTheme] = useTheme();
  useEffect(() => {
    logEvent('tengu_began_setup', {
      oauthEnabled
    });
  }, [oauthEnabled]);
  function goToNextStep() {
    if (currentStepIndex < steps.length - 1) {
      const nextIndex = currentStepIndex + 1;
      setCurrentStepIndex(nextIndex);
      logEvent('tengu_onboarding_step', {
        oauthEnabled,
        stepId: steps[nextIndex]?.id as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS
      });
    } else {

```

---


### `src/components/OutputStylePicker.tsx`

**信息:**
- 行数: 112
- 大小: 13233 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useCallback, useEffect, useState } from 'react';
import { getAllOutputStyles, OUTPUT_STYLE_CONFIG, type OutputStyleConfig } from '../constants/outputStyles.js';
import { Box, Text } from '../ink.js';
import type { OutputStyle } from '../utils/config.js';
import { getCwd } from '../utils/cwd.js';
import type { OptionWithDescription } from './CustomSelect/select.js';
import { Select } from './CustomSelect/select.js';
import { Dialog } from './design-system/Dialog.js';
const DEFAULT_OUTPUT_STYLE_LABEL = 'Default';
const DEFAULT_OUTPUT_STYLE_DESCRIPTION = 'Claude completes coding tasks efficiently and provides concise responses';
function mapConfigsToOptions(styles: {
  [styleName: string]: OutputStyleConfig | null;
}): OptionWithDescription[] {
  return Object.entries(styles).map(([style, config]) => ({
    label: config?.name ?? DEFAULT_OUTPUT_STYLE_LABEL,
    value: style,
    description: config?.description ?? DEFAULT_OUTPUT_STYLE_DESCRIPTION
  }));
}
export type OutputStylePickerProps = {
  initialStyle: OutputStyle;
  onComplete: (style: OutputStyle) => void;
  onCancel: () => void;
  isStandaloneCommand?: boolean;
};
export function OutputStylePicker(t0) {
  const $ = _c(16);
  const {
    initialStyle,
    onComplete,
    onCancel,
    isStandaloneCommand
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = [];
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const [styleOptions, setStyleOptions] = useState(t1);
  const [isLoading, setIsLoading] = useState(true);
  let t2;
  let t3;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = () => {
      getAllOutputStyles(getCwd()).then(allStyles => {
        const options = mapConfigsToOptions(allStyles);

```

---


### `src/components/PackageManagerAutoUpdater.tsx`

**信息:**
- 行数: 104
- 大小: 13907 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useState } from 'react';
import { useInterval } from 'usehooks-ts';
import { Text } from '../ink.js';
import { type AutoUpdaterResult, getLatestVersionFromGcs, getMaxVersion, shouldSkipVersion } from '../utils/autoUpdater.js';
import { isAutoUpdaterDisabled } from '../utils/config.js';
import { logForDebugging } from '../utils/debug.js';
import { getPackageManager, type PackageManager } from '../utils/nativeInstaller/packageManagers.js';
import { gt, gte } from '../utils/semver.js';
import { getInitialSettings } from '../utils/settings/settings.js';
type Props = {
  isUpdating: boolean;
  onChangeIsUpdating: (isUpdating: boolean) => void;
  onAutoUpdaterResult: (autoUpdaterResult: AutoUpdaterResult) => void;
  autoUpdaterResult: AutoUpdaterResult | null;
  showSuccessMessage: boolean;
  verbose: boolean;
};
export function PackageManagerAutoUpdater(t0) {
  const $ = _c(10);
  const {
    verbose
  } = t0;
  const [updateAvailable, setUpdateAvailable] = useState(false);
  const [packageManager, setPackageManager] = useState("unknown");
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = async () => {
      false || false;
      if (isAutoUpdaterDisabled()) {
        return;
      }
      const [channel, pm] = await Promise.all([Promise.resolve(getInitialSettings()?.autoUpdatesChannel ?? "latest"), getPackageManager()]);
      setPackageManager(pm);
      let latest = await getLatestVersionFromGcs(channel);
      const maxVersion = await getMaxVersion();
      if (maxVersion && latest && gt(latest, maxVersion)) {
        logForDebugging(`PackageManagerAutoUpdater: maxVersion ${maxVersion} is set, capping update from ${latest} to ${maxVersion}`);
        if (gte(MACRO.VERSION, maxVersion)) {
          logForDebugging(`PackageManagerAutoUpdater: current version ${MACRO.VERSION} is already at or above maxVersion ${maxVersion}, skipping update`);
          setUpdateAvailable(false);
          return;
        }
        latest = maxVersion;
      }
      const hasUpdate = latest && !gte(MACRO.VERSION, latest) && !shouldSkipVersion(latest);
      setUpdateAvailable(!!hasUpdate);
      if (hasUpdate) {
        logForDebugging(`PackageManagerAutoUpdater: Update available ${MACRO.VERSION} -> ${latest}`);

```

---


### `src/components/Passes/Passes.tsx`

**信息:**
- 行数: 184
- 大小: 27380 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { useCallback, useEffect, useState } from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { TEARDROP_ASTERISK } from '../../constants/figures.js';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { setClipboard } from '../../ink/termio/osc.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- enter to copy link
import { Box, Link, Text, useInput } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { logEvent } from '../../services/analytics/index.js';
import { fetchReferralRedemptions, formatCreditAmount, getCachedOrFetchPassesEligibility } from '../../services/api/referral.js';
import type { ReferralRedemptionsResponse, ReferrerRewardInfo } from '../../services/oauth/types.js';
import { count } from '../../utils/array.js';
import { logError } from '../../utils/log.js';
import { Pane } from '../design-system/Pane.js';
type PassStatus = {
  passNumber: number;
  isAvailable: boolean;
};
type Props = {
  onDone: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
export function Passes({
  onDone
}: Props): React.ReactNode {
  const [loading, setLoading] = useState(true);
  const [passStatuses, setPassStatuses] = useState<PassStatus[]>([]);
  const [isAvailable, setIsAvailable] = useState(false);
  const [referralLink, setReferralLink] = useState<string | null>(null);
  const [referrerReward, setReferrerReward] = useState<ReferrerRewardInfo | null | undefined>(undefined);
  const exitState = useExitOnCtrlCDWithKeybindings(() => onDone('Guest passes dialog dismissed', {
    display: 'system'
  }));
  const handleCancel = useCallback(() => {
    onDone('Guest passes dialog dismissed', {
      display: 'system'
    });
  }, [onDone]);
  useKeybinding('confirm:no', handleCancel, {
    context: 'Confirmation'
  });
  useInput((_input, key) => {
    if (key.return && referralLink) {
      void setClipboard(referralLink).then(raw => {
        if (raw) process.stdout.write(raw);
        logEvent('tengu_guest_passes_link_copied', {});
        onDone(`Referral link copied to clipboard!`);
      });

```

---


### `src/components/PrBadge.tsx`

**信息:**
- 行数: 97
- 大小: 7703 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Link, Text } from '../ink.js';
import type { PrReviewState } from '../utils/ghPrStatus.js';
type Props = {
  number: number;
  url: string;
  reviewState?: PrReviewState;
  bold?: boolean;
};
export function PrBadge(t0) {
  const $ = _c(21);
  const {
    number,
    url,
    reviewState,
    bold
  } = t0;
  let t1;
  if ($[0] !== reviewState) {
    t1 = getPrStatusColor(reviewState);
    $[0] = reviewState;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const statusColor = t1;
  const t2 = !statusColor && !bold;
  let t3;
  if ($[2] !== bold || $[3] !== number || $[4] !== statusColor || $[5] !== t2) {
    t3 = <Text color={statusColor} dimColor={t2} bold={bold}>#{number}</Text>;
    $[2] = bold;
    $[3] = number;
    $[4] = statusColor;
    $[5] = t2;
    $[6] = t3;
  } else {
    t3 = $[6];
  }
  const label = t3;
  const t4 = !bold;
  let t5;
  if ($[7] !== t4) {
    t5 = <Text dimColor={t4}>PR</Text>;
    $[7] = t4;
    $[8] = t5;
  } else {
    t5 = $[8];
  }
  const t6 = !statusColor && !bold;

```

---


### `src/components/PressEnterToContinue.tsx`

**信息:**
- 行数: 15
- 大小: 1526 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Text } from '../ink.js';
export function PressEnterToContinue() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <Text color="permission">Press <Text bold={true}>Enter</Text> to continue…</Text>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlRleHQiLCJQcmVzc0VudGVyVG9Db250aW51ZSIsIiQiLCJfYyIsInQwIiwiU3ltYm9sIiwiZm9yIl0sInNvdXJjZXMiOlsiUHJlc3NFbnRlclRvQ29udGludWUudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgVGV4dCB9IGZyb20gJy4uL2luay5qcydcblxuZXhwb3J0IGZ1bmN0aW9uIFByZXNzRW50ZXJUb0NvbnRpbnVlKCk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIHJldHVybiAoXG4gICAgPFRleHQgY29sb3I9XCJwZXJtaXNzaW9uXCI+XG4gICAgICBQcmVzcyA8VGV4dCBib2xkPkVudGVyPC9UZXh0PiB0byBjb250aW51ZeKAplxuICAgIDwvVGV4dD5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiO0FBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixTQUFTQyxJQUFJLFFBQVEsV0FBVztBQUVoQyxPQUFPLFNBQUFDLHFCQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQUEsSUFBQUMsRUFBQTtFQUFBLElBQUFGLENBQUEsUUFBQUcsTUFBQSxDQUFBQyxHQUFBO0lBRUhGLEVBQUEsSUFBQyxJQUFJLENBQU8sS0FBWSxDQUFaLFlBQVksQ0FBQyxNQUNqQixDQUFDLElBQUksQ0FBQyxJQUFJLENBQUosS0FBRyxDQUFDLENBQUMsS0FBSyxFQUFmLElBQUksQ0FBa0IsYUFDL0IsRUFGQyxJQUFJLENBRUU7SUFBQUYsQ0FBQSxNQUFBRSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBRixDQUFBO0VBQUE7RUFBQSxPQUZQRSxFQUVPO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/components/PromptInput/HistorySearchInput.tsx`

**信息:**
- 行数: 51
- 大小: 5005 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { stringWidth } from '../../ink/stringWidth.js';
import { Box, Text } from '../../ink.js';
import TextInput from '../TextInput.js';
type Props = {
  value: string;
  onChange: (value: string) => void;
  historyFailedMatch: boolean;
};
function HistorySearchInput(t0) {
  const $ = _c(9);
  const {
    value,
    onChange,
    historyFailedMatch
  } = t0;
  const t1 = historyFailedMatch ? "no matching prompt:" : "search prompts:";
  let t2;
  if ($[0] !== t1) {
    t2 = <Text dimColor={true}>{t1}</Text>;
    $[0] = t1;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  const t3 = stringWidth(value) + 1;
  let t4;
  if ($[2] !== onChange || $[3] !== t3 || $[4] !== value) {
    t4 = <TextInput value={value} onChange={onChange} cursorOffset={value.length} onChangeCursorOffset={_temp} columns={t3} focus={true} showCursor={true} multiline={false} dimColor={true} />;
    $[2] = onChange;
    $[3] = t3;
    $[4] = value;
    $[5] = t4;
  } else {
    t4 = $[5];
  }
  let t5;
  if ($[6] !== t2 || $[7] !== t4) {
    t5 = <Box gap={1}>{t2}{t4}</Box>;
    $[6] = t2;
    $[7] = t4;
    $[8] = t5;
  } else {
    t5 = $[8];
  }
  return t5;
}
function _temp() {}
export default HistorySearchInput;

```

---


### `src/components/PromptInput/IssueFlagBanner.tsx`

**信息:**
- 行数: 12
- 大小: 1914 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { FLAG_ICON } from '../../constants/figures.js';
import { Box, Text } from '../../ink.js';

/**
 * ANT-ONLY: Banner shown in the transcript that prompts users to report
 * issues via /issue. Appears when friction is detected in the conversation.
 */
export function IssueFlagBanner() {
  return null;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkZMQUdfSUNPTiIsIkJveCIsIlRleHQiLCJJc3N1ZUZsYWdCYW5uZXIiXSwic291cmNlcyI6WyJJc3N1ZUZsYWdCYW5uZXIudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgRkxBR19JQ09OIH0gZnJvbSAnLi4vLi4vY29uc3RhbnRzL2ZpZ3VyZXMuanMnXG5pbXBvcnQgeyBCb3gsIFRleHQgfSBmcm9tICcuLi8uLi9pbmsuanMnXG5cbi8qKlxuICogQU5ULU9OTFk6IEJhbm5lciBzaG93biBpbiB0aGUgdHJhbnNjcmlwdCB0aGF0IHByb21wdHMgdXNlcnMgdG8gcmVwb3J0XG4gKiBpc3N1ZXMgdmlhIC9pc3N1ZS4gQXBwZWFycyB3aGVuIGZyaWN0aW9uIGlzIGRldGVjdGVkIGluIHRoZSBjb252ZXJzYXRpb24uXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBJc3N1ZUZsYWdCYW5uZXIoKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgaWYgKFwiZXh0ZXJuYWxcIiAhPT0gJ2FudCcpIHtcbiAgICByZXR1cm4gbnVsbFxuICB9XG5cbiAgcmV0dXJuIChcbiAgICA8Qm94IGZsZXhEaXJlY3Rpb249XCJyb3dcIiBtYXJnaW5Ub3A9ezF9IHdpZHRoPVwiMTAwJVwiPlxuICAgICAgPEJveCBtaW5XaWR0aD17Mn0+XG4gICAgICAgIDxUZXh0IGNvbG9yPVwid2FybmluZ1wiPntGTEFHX0lDT059PC9UZXh0PlxuICAgICAgPC9Cb3g+XG4gICAgICA8VGV4dD5cbiAgICAgICAgPFRleHQgZGltQ29sb3I+W0FOVC1PTkxZXSA8L1RleHQ+XG4gICAgICAgIDxUZXh0IGNvbG9yPVwid2FybmluZ1wiIGJvbGQ+XG4gICAgICAgICAgU29tZXRoaW5nIG9mZiB3aXRoIENsYXVkZT9cbiAgICAgICAgPC9UZXh0PlxuICAgICAgICA8VGV4dCBkaW1Db2xvcj4gL2lzc3VlIHRvIHJlcG9ydCBpdDwvVGV4dD5cbiAgICAgIDwvVGV4dD5cbiAgICA8L0JveD5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLFNBQVMsUUFBUSw0QkFBNEI7QUFDdEQsU0FBU0MsR0FBRyxFQUFFQyxJQUFJLFFBQVEsY0FBYzs7QUFFeEM7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPLFNBQUFDLGdCQUFBO0VBQUEsT0FFSSxJQUFJO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/components/PromptInput/Notifications.tsx`

**信息:**
- 行数: 332
- 大小: 48104 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import * as React from 'react';
import { type ReactNode, useEffect, useMemo, useState } from 'react';
import { type Notification, useNotifications } from 'src/context/notifications.js';
import { logEvent } from 'src/services/analytics/index.js';
import { useAppState } from 'src/state/AppState.js';
import { useVoiceState } from '../../context/voice.js';
import type { VerificationStatus } from '../../hooks/useApiKeyVerification.js';
import { useIdeConnectionStatus } from '../../hooks/useIdeConnectionStatus.js';
import type { IDESelection } from '../../hooks/useIdeSelection.js';
import { useMainLoopModel } from '../../hooks/useMainLoopModel.js';
import { useVoiceEnabled } from '../../hooks/useVoiceEnabled.js';
import { Box, Text } from '../../ink.js';
import { useClaudeAiLimits } from '../../services/claudeAiLimitsHook.js';
import { calculateTokenWarningState } from '../../services/compact/autoCompact.js';
import type { MCPServerConnection } from '../../services/mcp/types.js';
import type { Message } from '../../types/message.js';
import { getApiKeyHelperElapsedMs, getConfiguredApiKeyHelper, getSubscriptionType } from '../../utils/auth.js';
import type { AutoUpdaterResult } from '../../utils/autoUpdater.js';
import { getExternalEditor } from '../../utils/editor.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import { formatDuration } from '../../utils/format.js';
import { setEnvHookNotifier } from '../../utils/hooks/fileChangedWatcher.js';
import { toIDEDisplayName } from '../../utils/ide.js';
import { getMessagesAfterCompactBoundary } from '../../utils/messages.js';
import { tokenCountFromLastAPIResponse } from '../../utils/tokens.js';
import { AutoUpdaterWrapper } from '../AutoUpdaterWrapper.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { IdeStatusIndicator } from '../IdeStatusIndicator.js';
import { MemoryUsageIndicator } from '../MemoryUsageIndicator.js';
import { SentryErrorBoundary } from '../SentryErrorBoundary.js';
import { TokenWarning } from '../TokenWarning.js';
import { SandboxPromptFooterHint } from './SandboxPromptFooterHint.js';

/* eslint-disable @typescript-eslint/no-require-imports */
const VoiceIndicator: typeof import('./VoiceIndicator.js').VoiceIndicator = feature('VOICE_MODE') ? require('./VoiceIndicator.js').VoiceIndicator : () => null;
/* eslint-enable @typescript-eslint/no-require-imports */

export const FOOTER_TEMPORARY_STATUS_TIMEOUT = 5000;
type Props = {
  apiKeyStatus: VerificationStatus;
  autoUpdaterResult: AutoUpdaterResult | null;
  isAutoUpdating: boolean;
  debug: boolean;
  verbose: boolean;
  messages: Message[];
  onAutoUpdaterResult: (result: AutoUpdaterResult) => void;
  onChangeIsUpdating: (isUpdating: boolean) => void;
  ideSelection: IDESelection | undefined;

```

---


### `src/components/PromptInput/PromptInput.tsx`

**信息:**
- 行数: 2339
- 大小: 355032 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import chalk from 'chalk';
import * as path from 'path';
import * as React from 'react';
import { useCallback, useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import { useNotifications } from 'src/context/notifications.js';
import { useCommandQueue } from 'src/hooks/useCommandQueue.js';
import { type IDEAtMentioned, useIdeAtMentioned } from 'src/hooks/useIdeAtMentioned.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { type AppState, useAppState, useAppStateStore, useSetAppState } from 'src/state/AppState.js';
import type { FooterItem } from 'src/state/AppStateStore.js';
import { getCwd } from 'src/utils/cwd.js';
import { isQueuedCommandEditable, popAllEditable } from 'src/utils/messageQueueManager.js';
import stripAnsi from 'strip-ansi';
import { companionReservedColumns } from '../../buddy/CompanionSprite.js';
import { findBuddyTriggerPositions, useBuddyNotification } from '../../buddy/useBuddyNotification.js';
import { FastModePicker } from '../../commands/fast/fast.js';
import { isUltrareviewEnabled } from '../../commands/review/ultrareviewEnabled.js';
import { getNativeCSIuTerminalDisplayName } from '../../commands/terminalSetup/terminalSetup.js';
import { type Command, hasCommand } from '../../commands.js';
import { useIsModalOverlayActive } from '../../context/overlayContext.js';
import { useSetPromptOverlayDialog } from '../../context/promptOverlayContext.js';
import { formatImageRef, formatPastedTextRef, getPastedTextRefNumLines, parseReferences } from '../../history.js';
import type { VerificationStatus } from '../../hooks/useApiKeyVerification.js';
import { type HistoryMode, useArrowKeyHistory } from '../../hooks/useArrowKeyHistory.js';
import { useDoublePress } from '../../hooks/useDoublePress.js';
import { useHistorySearch } from '../../hooks/useHistorySearch.js';
import type { IDESelection } from '../../hooks/useIdeSelection.js';
import { useInputBuffer } from '../../hooks/useInputBuffer.js';
import { useMainLoopModel } from '../../hooks/useMainLoopModel.js';
import { usePromptSuggestion } from '../../hooks/usePromptSuggestion.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { useTypeahead } from '../../hooks/useTypeahead.js';
import type { BorderTextOptions } from '../../ink/render-border.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { Box, type ClickEvent, type Key, Text, useInput } from '../../ink.js';
import { useOptionalKeybindingContext } from '../../keybindings/KeybindingContext.js';
import { getShortcutDisplay } from '../../keybindings/shortcutFormat.js';
import { useKeybinding, useKeybindings } from '../../keybindings/useKeybinding.js';
import type { MCPServerConnection } from '../../services/mcp/types.js';
import { abortPromptSuggestion, logSuggestionSuppressed } from '../../services/PromptSuggestion/promptSuggestion.js';
import { type ActiveSpeculationState, abortSpeculation } from '../../services/PromptSuggestion/speculation.js';
import { getActiveAgentForInput, getViewedTeammateTask } from '../../state/selectors.js';
import { enterTeammateView, exitTeammateView, stopOrDismissAgent } from '../../state/teammateViewHelpers.js';
import type { ToolPermissionContext } from '../../Tool.js';
import { getRunningTeammatesSorted } from '../../tasks/InProcessTeammateTask/InProcessTeammateTask.js';
import type { InProcessTeammateTaskState } from '../../tasks/InProcessTeammateTask/types.js';
import { isPanelAgentTask, type LocalAgentTaskState } from '../../tasks/LocalAgentTask/LocalAgentTask.js';
import { isBackgroundTask } from '../../tasks/types.js';
import { AGENT_COLOR_TO_THEME_COLOR, AGENT_COLORS, type AgentColorName } from '../../tools/AgentTool/agentColorManager.js';

```

---


### `src/components/PromptInput/PromptInputFooter.tsx`

**信息:**
- 行数: 191
- 大小: 33176 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import * as React from 'react';
import { memo, type ReactNode, useMemo, useRef } from 'react';
import { isBridgeEnabled } from '../../bridge/bridgeEnabled.js';
import { getBridgeStatus } from '../../bridge/bridgeStatusUtil.js';
import { useSetPromptOverlay } from '../../context/promptOverlayContext.js';
import type { VerificationStatus } from '../../hooks/useApiKeyVerification.js';
import type { IDESelection } from '../../hooks/useIdeSelection.js';
import { useSettings } from '../../hooks/useSettings.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { Box, Text } from '../../ink.js';
import type { MCPServerConnection } from '../../services/mcp/types.js';
import { useAppState } from '../../state/AppState.js';
import type { ToolPermissionContext } from '../../Tool.js';
import type { Message } from '../../types/message.js';
import type { PromptInputMode, VimMode } from '../../types/textInputTypes.js';
import type { AutoUpdaterResult } from '../../utils/autoUpdater.js';
import { isFullscreenEnvEnabled } from '../../utils/fullscreen.js';
import { isUndercover } from '../../utils/undercover.js';
import { CoordinatorTaskPanel, useCoordinatorTaskCount } from '../CoordinatorAgentStatus.js';
import { getLastAssistantMessageId, StatusLine, statusLineShouldDisplay } from '../StatusLine.js';
import { Notifications } from './Notifications.js';
import { PromptInputFooterLeftSide } from './PromptInputFooterLeftSide.js';
import { PromptInputFooterSuggestions, type SuggestionItem } from './PromptInputFooterSuggestions.js';
import { PromptInputHelpMenu } from './PromptInputHelpMenu.js';
type Props = {
  apiKeyStatus: VerificationStatus;
  debug: boolean;
  exitMessage: {
    show: boolean;
    key?: string;
  };
  vimMode: VimMode | undefined;
  mode: PromptInputMode;
  autoUpdaterResult: AutoUpdaterResult | null;
  isAutoUpdating: boolean;
  verbose: boolean;
  onAutoUpdaterResult: (result: AutoUpdaterResult) => void;
  onChangeIsUpdating: (isUpdating: boolean) => void;
  suggestions: SuggestionItem[];
  selectedSuggestion: number;
  maxColumnWidth?: number;
  toolPermissionContext: ToolPermissionContext;
  helpOpen: boolean;
  suppressHint: boolean;
  isLoading: boolean;
  tasksSelected: boolean;
  teamsSelected: boolean;
  bridgeSelected: boolean;
  tmuxSelected: boolean;

```

---


### `src/components/PromptInput/PromptInputFooterLeftSide.tsx`

**信息:**
- 行数: 517
- 大小: 87315 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
import { feature } from 'bun:bundle';
// Dead code elimination: conditional import for COORDINATOR_MODE
/* eslint-disable @typescript-eslint/no-require-imports */
const coordinatorModule = feature('COORDINATOR_MODE') ? require('../../coordinator/coordinatorMode.js') as typeof import('../../coordinator/coordinatorMode.js') : undefined;
/* eslint-enable @typescript-eslint/no-require-imports */
import { Box, Text, Link } from '../../ink.js';
import * as React from 'react';
import figures from 'figures';
import { useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import type { VimMode, PromptInputMode } from '../../types/textInputTypes.js';
import type { ToolPermissionContext } from '../../Tool.js';
import { isVimModeEnabled } from './utils.js';
import { useShortcutDisplay } from '../../keybindings/useShortcutDisplay.js';
import { isDefaultMode, permissionModeSymbol, permissionModeTitle, getModeColor } from '../../utils/permissions/PermissionMode.js';
import { BackgroundTaskStatus } from '../tasks/BackgroundTaskStatus.js';
import { isBackgroundTask } from '../../tasks/types.js';
import { isPanelAgentTask } from '../../tasks/LocalAgentTask/LocalAgentTask.js';
import { getVisibleAgentTasks } from '../CoordinatorAgentStatus.js';
import { count } from '../../utils/array.js';
import { shouldHideTasksFooter } from '../tasks/taskStatusUtils.js';
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js';
import { TeamStatus } from '../teams/TeamStatus.js';
import { isInProcessEnabled } from '../../utils/swarm/backends/registry.js';
import { useAppState, useAppStateStore } from 'src/state/AppState.js';
import { getIsRemoteMode } from '../../bootstrap/state.js';
import HistorySearchInput from './HistorySearchInput.js';
import { usePrStatus } from '../../hooks/usePrStatus.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import { Byline } from '../design-system/Byline.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { useTasksV2 } from '../../hooks/useTasksV2.js';
import { formatDuration } from '../../utils/format.js';
import { VoiceWarmupHint } from './VoiceIndicator.js';
import { useVoiceEnabled } from '../../hooks/useVoiceEnabled.js';
import { useVoiceState } from '../../context/voice.js';
import { isFullscreenEnvEnabled } from '../../utils/fullscreen.js';
import { isXtermJs } from '../../ink/terminal.js';
import { useHasSelection, useSelection } from '../../ink/hooks/use-selection.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { getPlatform } from '../../utils/platform.js';
import { PrBadge } from '../PrBadge.js';

// Dead code elimination: conditional import for proactive mode
/* eslint-disable @typescript-eslint/no-require-imports */
const proactiveModule = feature('PROACTIVE') || feature('KAIROS') ? require('../../proactive/index.js') : null;
/* eslint-enable @typescript-eslint/no-require-imports */
const NO_OP_SUBSCRIBE = (_cb: () => void) => () => {};
const NULL = () => null;

```

---


### `src/components/PromptInput/PromptInputFooterSuggestions.tsx`

**信息:**
- 行数: 293
- 大小: 34158 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { memo, type ReactNode } from 'react';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { Box, Text } from '../../ink.js';
import { truncatePathMiddle, truncateToWidth } from '../../utils/format.js';
import type { Theme } from '../../utils/theme.js';
export type SuggestionItem = {
  id: string;
  displayText: string;
  tag?: string;
  description?: string;
  metadata?: unknown;
  color?: keyof Theme;
};
export type SuggestionType = 'command' | 'file' | 'directory' | 'agent' | 'shell' | 'custom-title' | 'slack-channel' | 'none';
export const OVERLAY_MAX_ITEMS = 5;

/**
 * Get the icon for a suggestion based on its type
 * Icons: + for files, ◇ for MCP resources, * for agents
 */
function getIcon(itemId: string): string {
  if (itemId.startsWith('file-')) return '+';
  if (itemId.startsWith('mcp-resource-')) return '◇';
  if (itemId.startsWith('agent-')) return '*';
  return '+';
}

/**
 * Check if an item is a unified suggestion type (file, mcp-resource, or agent)
 */
function isUnifiedSuggestion(itemId: string): boolean {
  return itemId.startsWith('file-') || itemId.startsWith('mcp-resource-') || itemId.startsWith('agent-');
}
const SuggestionItemRow = memo(function SuggestionItemRow(t0) {
  const $ = _c(36);
  const {
    item,
    maxColumnWidth,
    isSelected
  } = t0;
  const columns = useTerminalSize().columns;
  const isUnified = isUnifiedSuggestion(item.id);
  if (isUnified) {
    let t1;
    if ($[0] !== item.id) {
      t1 = getIcon(item.id);
      $[0] = item.id;

```

---


### `src/components/PromptInput/PromptInputHelpMenu.tsx`

**信息:**
- 行数: 358
- 大小: 32811 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import * as React from 'react';
import { Box, Text } from 'src/ink.js';
import { getPlatform } from 'src/utils/platform.js';
import { isKeybindingCustomizationEnabled } from '../../keybindings/loadUserBindings.js';
import { useShortcutDisplay } from '../../keybindings/useShortcutDisplay.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js';
import { isFastModeAvailable, isFastModeEnabled } from '../../utils/fastMode.js';
import { getNewlineInstructions } from './utils.js';

/** Format a shortcut for display in the help menu (e.g., "ctrl+o" → "ctrl + o") */
function formatShortcut(shortcut: string): string {
  return shortcut.replace(/\+/g, ' + ');
}
type Props = {
  dimColor?: boolean;
  fixedWidth?: boolean;
  gap?: number;
  paddingX?: number;
};
export function PromptInputHelpMenu(props) {
  const $ = _c(99);
  const {
    dimColor,
    fixedWidth,
    gap,
    paddingX
  } = props;
  const t0 = useShortcutDisplay("app:toggleTranscript", "Global", "ctrl+o");
  let t1;
  if ($[0] !== t0) {
    t1 = formatShortcut(t0);
    $[0] = t0;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const transcriptShortcut = t1;
  const t2 = useShortcutDisplay("app:toggleTodos", "Global", "ctrl+t");
  let t3;
  if ($[2] !== t2) {
    t3 = formatShortcut(t2);
    $[2] = t2;
    $[3] = t3;
  } else {
    t3 = $[3];
  }
  const todosShortcut = t3;
  const t4 = useShortcutDisplay("chat:undo", "Chat", "ctrl+_");

```

---


### `src/components/PromptInput/PromptInputModeIndicator.tsx`

**信息:**
- 行数: 93
- 大小: 11127 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { Box, Text } from 'src/ink.js';
import { AGENT_COLOR_TO_THEME_COLOR, AGENT_COLORS, type AgentColorName } from 'src/tools/AgentTool/agentColorManager.js';
import type { PromptInputMode } from 'src/types/textInputTypes.js';
import { getTeammateColor } from 'src/utils/teammate.js';
import type { Theme } from 'src/utils/theme.js';
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js';
type Props = {
  mode: PromptInputMode;
  isLoading: boolean;
  viewingAgentName?: string;
  viewingAgentColor?: AgentColorName;
};

/**
 * Gets the theme color key for the teammate's assigned color.
 * Returns undefined if not a teammate or if the color is invalid.
 */
function getTeammateThemeColor(): keyof Theme | undefined {
  if (!isAgentSwarmsEnabled()) {
    return undefined;
  }
  const colorName = getTeammateColor();
  if (!colorName) {
    return undefined;
  }
  if (AGENT_COLORS.includes(colorName as AgentColorName)) {
    return AGENT_COLOR_TO_THEME_COLOR[colorName as AgentColorName];
  }
  return undefined;
}
type PromptCharProps = {
  isLoading: boolean;
  // Dead code elimination: parameter named themeColor to avoid "teammate" string in external builds
  themeColor?: keyof Theme;
};

/**
 * Renders the prompt character (❯).
 * Teammate color overrides the default color when set.
 */
function PromptChar(t0) {
  const $ = _c(3);
  const {
    isLoading,
    themeColor
  } = t0;
  const teammateColor = themeColor;

```

---


### `src/components/PromptInput/PromptInputQueuedCommands.tsx`

**信息:**
- 行数: 117
- 大小: 19587 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import * as React from 'react';
import { useMemo } from 'react';
import { Box } from 'src/ink.js';
import { useAppState } from 'src/state/AppState.js';
import { STATUS_TAG, SUMMARY_TAG, TASK_NOTIFICATION_TAG } from '../../constants/xml.js';
import { QueuedMessageProvider } from '../../context/QueuedMessageContext.js';
import { useCommandQueue } from '../../hooks/useCommandQueue.js';
import type { QueuedCommand } from '../../types/textInputTypes.js';
import { isQueuedCommandVisible } from '../../utils/messageQueueManager.js';
import { createUserMessage, EMPTY_LOOKUPS, normalizeMessages } from '../../utils/messages.js';
import { jsonParse } from '../../utils/slowOperations.js';
import { Message } from '../Message.js';
const EMPTY_SET = new Set<string>();

/**
 * Check if a command value is an idle notification that should be hidden.
 * Idle notifications are processed silently without showing to the user.
 */
function isIdleNotification(value: string): boolean {
  try {
    const parsed = jsonParse(value);
    return parsed?.type === 'idle_notification';
  } catch {
    return false;
  }
}

// Maximum number of task notification lines to show
const MAX_VISIBLE_NOTIFICATIONS = 3;

/**
 * Create a synthetic overflow notification message for capped task notifications.
 */
function createOverflowNotificationMessage(count: number): string {
  return `<${TASK_NOTIFICATION_TAG}>
<${SUMMARY_TAG}>+${count} more tasks completed</${SUMMARY_TAG}>
<${STATUS_TAG}>completed</${STATUS_TAG}>
</${TASK_NOTIFICATION_TAG}>`;
}

/**
 * Process queued commands to cap task notifications at MAX_VISIBLE_NOTIFICATIONS lines.
 * Other command types are always shown in full.
 * Idle notifications are filtered out entirely.
 */
function processQueuedCommands(queuedCommands: QueuedCommand[]): QueuedCommand[] {
  // Filter out idle notifications - they are processed silently
  const filteredCommands = queuedCommands.filter(cmd => typeof cmd.value !== 'string' || !isIdleNotification(cmd.value));


```

---


### `src/components/PromptInput/PromptInputStashNotice.tsx`

**信息:**
- 行数: 25
- 大小: 2291 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { Box, Text } from 'src/ink.js';
type Props = {
  hasStash: boolean;
};
export function PromptInputStashNotice(t0) {
  const $ = _c(1);
  const {
    hasStash
  } = t0;
  if (!hasStash) {
    return null;
  }
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Box paddingLeft={2}><Text dimColor={true}>{figures.pointerSmall} Stashed (auto-restores after submit)</Text></Box>;
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  return t1;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJmaWd1cmVzIiwiUmVhY3QiLCJCb3giLCJUZXh0IiwiUHJvcHMiLCJoYXNTdGFzaCIsIlByb21wdElucHV0U3Rhc2hOb3RpY2UiLCJ0MCIsIiQiLCJfYyIsInQxIiwiU3ltYm9sIiwiZm9yIiwicG9pbnRlclNtYWxsIl0sInNvdXJjZXMiOlsiUHJvbXB0SW5wdXRTdGFzaE5vdGljZS50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IGZpZ3VyZXMgZnJvbSAnZmlndXJlcydcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgQm94LCBUZXh0IH0gZnJvbSAnc3JjL2luay5qcydcblxudHlwZSBQcm9wcyA9IHtcbiAgaGFzU3Rhc2g6IGJvb2xlYW5cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIFByb21wdElucHV0U3Rhc2hOb3RpY2UoeyBoYXNTdGFzaCB9OiBQcm9wcyk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIGlmICghaGFzU3Rhc2gpIHtcbiAgICByZXR1cm4gbnVsbFxuICB9XG5cbiAgcmV0dXJuIChcbiAgICA8Qm94IHBhZGRpbmdMZWZ0PXsyfT5cbiAgICAgIDxUZXh0IGRpbUNvbG9yPlxuICAgICAgICB7ZmlndXJlcy5wb2ludGVyU21hbGx9IFN0YXNoZWQgKGF1dG8tcmVzdG9yZXMgYWZ0ZXIgc3VibWl0KVxuICAgICAgPC9UZXh0PlxuICAgIDwvQm94PlxuICApXG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxPQUFPQSxPQUFPLE1BQU0sU0FBUztBQUM3QixPQUFPLEtBQUtDLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxRQUFRLFlBQVk7QUFFdEMsS0FBS0MsS0FBSyxHQUFHO0VBQ1hDLFFBQVEsRUFBRSxPQUFPO0FBQ25CLENBQUM7QUFFRCxPQUFPLFNBQUFDLHVCQUFBQyxFQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQWdDO0lBQUFKO0VBQUEsSUFBQUUsRUFBbUI7RUFDeEQsSUFBSSxDQUFDRixRQUFRO0lBQUEsT0FDSixJQUFJO0VBQUE7RUFDWixJQUFBSyxFQUFBO0VBQUEsSUFBQUYsQ0FBQSxRQUFBRyxNQUFBLENBQUFDLEdBQUE7SUFHQ0YsRUFBQSxJQUFDLEdBQUcsQ0FBYyxXQUFDLENBQUQsR0FBQyxDQUNqQixDQUFDLElBQUksQ0FBQyxRQUFRLENBQVIsS0FBTyxDQUFDLENBQ1gsQ0FBQVYsT0FBTyxDQUFBYSxZQUFZLENBQUUscUNBQ3hCLEVBRkMsSUFBSSxDQUdQLEVBSkMsR0FBRyxDQUlFO0lBQUFMLENBQUEsTUFBQUUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUYsQ0FBQTtFQUFBO0VBQUEsT0FKTkUsRUFJTTtBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/PromptInput/SandboxPromptFooterHint.tsx`

**信息:**
- 行数: 64
- 大小: 8031 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { type ReactNode, useEffect, useRef, useState } from 'react';
import { Box, Text } from '../../ink.js';
import { useShortcutDisplay } from '../../keybindings/useShortcutDisplay.js';
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js';
export function SandboxPromptFooterHint() {
  const $ = _c(6);
  const [recentViolationCount, setRecentViolationCount] = useState(0);
  const timerRef = useRef(null);
  const detailsShortcut = useShortcutDisplay("app:toggleTranscript", "Global", "ctrl+o");
  let t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = () => {
      if (!SandboxManager.isSandboxingEnabled()) {
        return;
      }
      const store = SandboxManager.getSandboxViolationStore();
      let lastCount = store.getTotalCount();
      const unsubscribe = store.subscribe(() => {
        const currentCount = store.getTotalCount();
        const newViolations = currentCount - lastCount;
        if (newViolations > 0) {
          setRecentViolationCount(newViolations);
          lastCount = currentCount;
          if (timerRef.current) {
            clearTimeout(timerRef.current);
          }
          timerRef.current = setTimeout(setRecentViolationCount, 5000, 0);
        }
      });
      return () => {
        unsubscribe();
        if (timerRef.current) {
          clearTimeout(timerRef.current);
        }
      };
    };
    t1 = [];
    $[0] = t0;
    $[1] = t1;
  } else {
    t0 = $[0];
    t1 = $[1];
  }
  useEffect(t0, t1);
  if (!SandboxManager.isSandboxingEnabled() || recentViolationCount === 0) {
    return null;
  }

```

---


### `src/components/PromptInput/ShimmeredInput.tsx`

**信息:**
- 行数: 143
- 大小: 16680 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Ansi, Box, Text, useAnimationFrame } from '../../ink.js';
import { segmentTextByHighlights, type TextHighlight } from '../../utils/textHighlighting.js';
import { ShimmerChar } from '../Spinner/ShimmerChar.js';
type Props = {
  text: string;
  highlights: TextHighlight[];
};
type LinePart = {
  text: string;
  highlight: TextHighlight | undefined;
  start: number;
};
export function HighlightedInput(t0) {
  const $ = _c(23);
  const {
    text,
    highlights
  } = t0;
  let lines;
  if ($[0] !== highlights || $[1] !== text) {
    const segments = segmentTextByHighlights(text, highlights);
    lines = [[]];
    let pos = 0;
    for (const segment of segments) {
      const parts = segment.text.split("\n");
      for (let i = 0; i < parts.length; i++) {
        if (i > 0) {
          lines.push([]);
          pos = pos + 1;
        }
        const part = parts[i];
        if (part.length > 0) {
          lines[lines.length - 1].push({
            text: part,
            highlight: segment.highlight,
            start: pos
          });
        }
        pos = pos + part.length;
      }
    }
    $[0] = highlights;
    $[1] = text;
    $[2] = lines;
  } else {
    lines = $[2];
  }
  let t1;

```

---


### `src/components/PromptInput/VoiceIndicator.tsx`

**信息:**
- 行数: 137
- 大小: 10810 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import * as React from 'react';
import { useSettings } from '../../hooks/useSettings.js';
import { Box, Text, useAnimationFrame } from '../../ink.js';
import { interpolateColor, toRGBColor } from '../Spinner/utils.js';
type Props = {
  voiceState: 'idle' | 'recording' | 'processing';
};

// Processing shimmer colors: dim gray to lighter gray (matches ThinkingShimmerText)
const PROCESSING_DIM = {
  r: 153,
  g: 153,
  b: 153
};
const PROCESSING_BRIGHT = {
  r: 185,
  g: 185,
  b: 185
};
const PULSE_PERIOD_S = 2; // 2 second period for all pulsing animations

export function VoiceIndicator(props) {
  const $ = _c(2);
  if (!feature("VOICE_MODE")) {
    return null;
  }
  let t0;
  if ($[0] !== props) {
    t0 = <VoiceIndicatorImpl {...props} />;
    $[0] = props;
    $[1] = t0;
  } else {
    t0 = $[1];
  }
  return t0;
}
function VoiceIndicatorImpl(t0) {
  const $ = _c(2);
  const {
    voiceState
  } = t0;
  switch (voiceState) {
    case "recording":
      {
        let t1;
        if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
          t1 = <Text dimColor={true}>listening…</Text>;
          $[0] = t1;

```

---


### `src/components/PromptInput/inputModes.ts`

**信息:**
- 行数: 33
- 大小: 731 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { HistoryMode } from 'src/hooks/useArrowKeyHistory.js'
import type { PromptInputMode } from 'src/types/textInputTypes.js'

export function prependModeCharacterToInput(
  input: string,
  mode: PromptInputMode,
): string {
  switch (mode) {
    case 'bash':
      return `!${input}`
    default:
      return input
  }
}

export function getModeFromInput(input: string): HistoryMode {
  if (input.startsWith('!')) {
    return 'bash'
  }
  return 'prompt'
}

export function getValueFromInput(input: string): string {
  const mode = getModeFromInput(input)
  if (mode === 'prompt') {
    return input
  }
  return input.slice(1)
}

export function isInputModeCharacter(input: string): boolean {
  return input === '!'
}

```

---


### `src/components/PromptInput/inputPaste.ts`

**信息:**
- 行数: 90
- 大小: 2693 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getPastedTextRefNumLines } from 'src/history.js'
import type { PastedContent } from 'src/utils/config.js'

const TRUNCATION_THRESHOLD = 10000 // Characters before we truncate
const PREVIEW_LENGTH = 1000 // Characters to show at start and end

type TruncatedMessage = {
  truncatedText: string
  placeholderContent: string
}

/**
 * Determines whether the input text should be truncated. If so, it adds a
 * truncated text placeholder and neturns
 *
 * @param text The input text
 * @param nextPasteId The reference id to use
 * @returns The new text to display and separate placeholder content if applicable.
 */
export function maybeTruncateMessageForInput(
  text: string,
  nextPasteId: number,
): TruncatedMessage {
  // If the text is short enough, return it as-is
  if (text.length <= TRUNCATION_THRESHOLD) {
    return {
      truncatedText: text,
      placeholderContent: '',
    }
  }

  // Calculate how much text to keep from start and end
  const startLength = Math.floor(PREVIEW_LENGTH / 2)
  const endLength = Math.floor(PREVIEW_LENGTH / 2)

  // Extract the portions we'll keep
  const startText = text.slice(0, startLength)
  const endText = text.slice(-endLength)

  // Calculate the number of lines that will be truncated
  const placeholderContent = text.slice(startLength, -endLength)
  const truncatedLines = getPastedTextRefNumLines(placeholderContent)

  // Create a placeholder reference similar to pasted text
  const placeholderId = nextPasteId
  const placeholderRef = formatTruncatedTextRef(placeholderId, truncatedLines)

  // Combine the parts with the placeholder
  const truncatedText = startText + placeholderRef + endText


```

---


### `src/components/PromptInput/useMaybeTruncateInput.ts`

**信息:**
- 行数: 58
- 大小: 1468 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useState } from 'react'
import type { PastedContent } from 'src/utils/config.js'
import { maybeTruncateInput } from './inputPaste.js'

type Props = {
  input: string
  pastedContents: Record<number, PastedContent>
  onInputChange: (input: string) => void
  setCursorOffset: (offset: number) => void
  setPastedContents: (contents: Record<number, PastedContent>) => void
}

export function useMaybeTruncateInput({
  input,
  pastedContents,
  onInputChange,
  setCursorOffset,
  setPastedContents,
}: Props) {
  // Track if we've initialized this specific input value
  const [hasAppliedTruncationToInput, setHasAppliedTruncationToInput] =
    useState(false)

  // Process input for truncation and pasted images from MessageSelector.
  useEffect(() => {
    if (hasAppliedTruncationToInput) {
      return
    }

    if (input.length <= 10_000) {
      return
    }

    const { newInput, newPastedContents } = maybeTruncateInput(
      input,
      pastedContents,
    )

    onInputChange(newInput)
    setCursorOffset(newInput.length)
    setPastedContents(newPastedContents)
    setHasAppliedTruncationToInput(true)
  }, [
    input,
    hasAppliedTruncationToInput,
    pastedContents,
    onInputChange,
    setPastedContents,
    setCursorOffset,
  ])

```

---


### `src/components/PromptInput/usePromptInputPlaceholder.ts`

**信息:**
- 行数: 76
- 大小: 2391 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { useMemo } from 'react'
import { useCommandQueue } from 'src/hooks/useCommandQueue.js'
import { useAppState } from 'src/state/AppState.js'
import { getGlobalConfig } from 'src/utils/config.js'
import { getExampleCommandFromCache } from 'src/utils/exampleCommands.js'
import { isQueuedCommandEditable } from 'src/utils/messageQueueManager.js'

// Dead code elimination: conditional import for proactive mode
/* eslint-disable @typescript-eslint/no-require-imports */
const proactiveModule =
  feature('PROACTIVE') || feature('KAIROS')
    ? require('../../proactive/index.js')
    : null

type Props = {
  input: string
  submitCount: number
  viewingAgentName?: string
}

const NUM_TIMES_QUEUE_HINT_SHOWN = 3
const MAX_TEAMMATE_NAME_LENGTH = 20

export function usePromptInputPlaceholder({
  input,
  submitCount,
  viewingAgentName,
}: Props): string | undefined {
  const queuedCommands = useCommandQueue()
  const promptSuggestionEnabled = useAppState(s => s.promptSuggestionEnabled)
  const placeholder = useMemo(() => {
    if (input !== '') {
      return
    }

    // Show teammate hint when viewing teammate
    if (viewingAgentName) {
      const displayName =
        viewingAgentName.length > MAX_TEAMMATE_NAME_LENGTH
          ? viewingAgentName.slice(0, MAX_TEAMMATE_NAME_LENGTH - 3) + '...'
          : viewingAgentName
      return `Message @${displayName}…`
    }

    // Show queue hint if user has not seen it yet.
    // Only count user-editable commands — task-notification and isMeta
    // are hidden from the prompt area (see PromptInputQueuedCommands).
    if (
      queuedCommands.some(isQueuedCommandEditable) &&

```

---


### `src/components/PromptInput/useShowFastIconHint.ts`

**信息:**
- 行数: 31
- 大小: 696 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useState } from 'react'

const HINT_DISPLAY_DURATION_MS = 5000

let hasShownThisSession = false

/**
 * Hook to manage the /fast hint display next to the fast icon.
 * Shows the hint for 5 seconds once per session.
 */
export function useShowFastIconHint(showFastIcon: boolean): boolean {
  const [showHint, setShowHint] = useState(false)

  useEffect(() => {
    if (hasShownThisSession || !showFastIcon) {
      return
    }

    hasShownThisSession = true
    setShowHint(true)

    const timer = setTimeout(setShowHint, HINT_DISPLAY_DURATION_MS, false)

    return () => {
      clearTimeout(timer)
      setShowHint(false)
    }
  }, [showFastIcon])

  return showHint
}

```

---


### `src/components/PromptInput/useSwarmBanner.ts`

**信息:**
- 行数: 155
- 大小: 5344 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import * as React from 'react'
import { useAppState, useAppStateStore } from '../../state/AppState.js'
import {
  getActiveAgentForInput,
  getViewedTeammateTask,
} from '../../state/selectors.js'
import {
  AGENT_COLOR_TO_THEME_COLOR,
  AGENT_COLORS,
  type AgentColorName,
  getAgentColor,
} from '../../tools/AgentTool/agentColorManager.js'
import { getStandaloneAgentName } from '../../utils/standaloneAgent.js'
import { isInsideTmux } from '../../utils/swarm/backends/detection.js'
import {
  getCachedDetectionResult,
  isInProcessEnabled,
} from '../../utils/swarm/backends/registry.js'
import { getSwarmSocketName } from '../../utils/swarm/constants.js'
import {
  getAgentName,
  getTeammateColor,
  getTeamName,
  isTeammate,
} from '../../utils/teammate.js'
import { isInProcessTeammate } from '../../utils/teammateContext.js'
import type { Theme } from '../../utils/theme.js'

type SwarmBannerInfo = {
  text: string
  bgColor: keyof Theme
} | null

/**
 * Hook that returns banner information for swarm, standalone agent, or --agent CLI context.
 * - Leader (not in tmux): Returns "tmux -L ... attach" command with cyan background
 * - Leader (in tmux / in-process): Falls through to standalone-agent check — shows
 *   /rename name + /color background if set, else null
 * - Teammate: Returns "teammate@team" format with their assigned color background
 * - Viewing a background agent (CoordinatorTaskPanel): Returns agent name with its color
 * - Standalone agent: Returns agent name with their color background (no @team)
 * - --agent CLI flag: Returns "@agentName" with cyan background
 */
export function useSwarmBanner(): SwarmBannerInfo {
  const teamContext = useAppState(s => s.teamContext)
  const standaloneAgentContext = useAppState(s => s.standaloneAgentContext)
  const agent = useAppState(s => s.agent)
  // Subscribe so the banner updates on enter/exit teammate view even though
  // getActiveAgentForInput reads it from store.getState().
  useAppState(s => s.viewingAgentTaskId)

```

---


### `src/components/PromptInput/utils.ts`

**信息:**
- 行数: 60
- 大小: 1744 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  hasUsedBackslashReturn,
  isShiftEnterKeyBindingInstalled,
} from '../../commands/terminalSetup/terminalSetup.js'
import type { Key } from '../../ink.js'
import { getGlobalConfig } from '../../utils/config.js'
import { env } from '../../utils/env.js'
/**
 * Helper function to check if vim mode is currently enabled
 * @returns boolean indicating if vim mode is active
 */
export function isVimModeEnabled(): boolean {
  const config = getGlobalConfig()
  return config.editorMode === 'vim'
}

export function getNewlineInstructions(): string {
  // Apple Terminal on macOS uses native modifier key detection for Shift+Enter
  if (env.terminal === 'Apple_Terminal' && process.platform === 'darwin') {
    return 'shift + ⏎ for newline'
  }

  // For iTerm2 and VSCode, show Shift+Enter instructions if installed
  if (isShiftEnterKeyBindingInstalled()) {
    return 'shift + ⏎ for newline'
  }

  // Otherwise show backslash+return instructions
  return hasUsedBackslashReturn()
    ? '\\⏎ for newline'
    : 'backslash (\\) + return (⏎) for newline'
}

/**
 * True when the keystroke is a printable character that does not begin
 * with whitespace — i.e., a normal letter/digit/symbol the user typed.
 * Used to gate the lazy space inserted after an image pill.
 */
export function isNonSpacePrintable(input: string, key: Key): boolean {
  if (
    key.ctrl ||
    key.meta ||
    key.escape ||
    key.return ||
    key.tab ||
    key.backspace ||
    key.delete ||
    key.upArrow ||
    key.downArrow ||
    key.leftArrow ||

```

---


### `src/components/QuickOpenDialog.tsx`

**信息:**
- 行数: 244
- 大小: 28556 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as path from 'path';
import * as React from 'react';
import { useEffect, useRef, useState } from 'react';
import { useRegisterOverlay } from '../context/overlayContext.js';
import { generateFileSuggestions } from '../hooks/fileSuggestions.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { Text } from '../ink.js';
import { logEvent } from '../services/analytics/index.js';
import { getCwd } from '../utils/cwd.js';
import { openFileInExternalEditor } from '../utils/editor.js';
import { truncatePathMiddle, truncateToWidth } from '../utils/format.js';
import { highlightMatch } from '../utils/highlightMatch.js';
import { readFileInRange } from '../utils/readFileInRange.js';
import { FuzzyPicker } from './design-system/FuzzyPicker.js';
import { LoadingState } from './design-system/LoadingState.js';
type Props = {
  onDone: () => void;
  onInsert: (text: string) => void;
};
const VISIBLE_RESULTS = 8;
const PREVIEW_LINES = 20;

/**
 * Quick Open dialog (ctrl+shift+p / cmd+shift+p).
 * Fuzzy file finder with a syntax-highlighted preview of the focused file.
 */
export function QuickOpenDialog(t0) {
  const $ = _c(35);
  const {
    onDone,
    onInsert
  } = t0;
  useRegisterOverlay("quick-open");
  const {
    columns,
    rows
  } = useTerminalSize();
  const visibleResults = Math.min(VISIBLE_RESULTS, Math.max(4, rows - 14));
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = [];
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const [results, setResults] = useState(t1);
  const [query, setQuery] = useState("");
  const [focusedPath, setFocusedPath] = useState(undefined);
  const [preview, setPreview] = useState(null);

```

---


### `src/components/RemoteCallout.tsx`

**信息:**
- 行数: 76
- 大小: 9978 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React, { useCallback, useEffect, useRef } from 'react';
import { isBridgeEnabled } from '../bridge/bridgeEnabled.js';
import { Box, Text } from '../ink.js';
import { getClaudeAIOAuthTokens } from '../utils/auth.js';
import { getGlobalConfig, saveGlobalConfig } from '../utils/config.js';
import type { OptionWithDescription } from './CustomSelect/select.js';
import { Select } from './CustomSelect/select.js';
import { PermissionDialog } from './permissions/PermissionDialog.js';
type RemoteCalloutSelection = 'enable' | 'dismiss';
type Props = {
  onDone: (selection: RemoteCalloutSelection) => void;
};
export function RemoteCallout({
  onDone
}: Props): React.ReactNode {
  const onDoneRef = useRef(onDone);
  onDoneRef.current = onDone;
  const handleCancel = useCallback((): void => {
    onDoneRef.current('dismiss');
  }, []);

  // Permanently mark as seen on mount so it only shows once
  useEffect(() => {
    saveGlobalConfig(current => {
      if (current.remoteDialogSeen) return current;
      return {
        ...current,
        remoteDialogSeen: true
      };
    });
  }, []);
  const handleSelect = useCallback((value: RemoteCalloutSelection): void => {
    onDoneRef.current(value);
  }, []);
  const options: OptionWithDescription<RemoteCalloutSelection>[] = [{
    label: 'Enable Remote Control for this session',
    description: 'Opens a secure connection to claude.ai.',
    value: 'enable'
  }, {
    label: 'Never mind',
    description: 'You can always enable it later with /remote-control.',
    value: 'dismiss'
  }];
  return <PermissionDialog title="Remote Control">
      <Box flexDirection="column" paddingX={2} paddingY={1}>
        <Box marginBottom={1} flexDirection="column">
          <Text>
            Remote Control lets you access this CLI session from the web
            (claude.ai/code) or the Claude app, so you can pick up where you
            left off on any device.

```

---


### `src/components/RemoteEnvironmentDialog.tsx`

**信息:**
- 行数: 340
- 大小: 33519 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import figures from 'figures';
import * as React from 'react';
import { useEffect, useState } from 'react';
import { Text } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { toError } from '../utils/errors.js';
import { logError } from '../utils/log.js';
import { getSettingSourceName, type SettingSource } from '../utils/settings/constants.js';
import { updateSettingsForSource } from '../utils/settings/settings.js';
import { getEnvironmentSelectionInfo } from '../utils/teleport/environmentSelection.js';
import type { EnvironmentResource } from '../utils/teleport/environments.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { Select } from './CustomSelect/select.js';
import { Byline } from './design-system/Byline.js';
import { Dialog } from './design-system/Dialog.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import { LoadingState } from './design-system/LoadingState.js';
const DIALOG_TITLE = 'Select Remote Environment';
const SETUP_HINT = `Configure environments at: https://claude.ai/code`;
type Props = {
  onDone: (message?: string) => void;
};
type LoadingState = 'loading' | 'updating' | null;
export function RemoteEnvironmentDialog(t0) {
  const $ = _c(27);
  const {
    onDone
  } = t0;
  const [loadingState, setLoadingState] = useState("loading");
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = [];
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const [environments, setEnvironments] = useState(t1);
  const [selectedEnvironment, setSelectedEnvironment] = useState(null);
  const [selectedEnvironmentSource, setSelectedEnvironmentSource] = useState(null);
  const [error, setError] = useState(null);
  let t2;
  let t3;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = () => {
      let cancelled = false;
      const fetchInfo = async function fetchInfo() {
        ;
        try {

```

---


### `src/components/ResumeTask.tsx`

**信息:**
- 行数: 268
- 大小: 38550 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React, { useCallback, useState } from 'react';
import { useTerminalSize } from 'src/hooks/useTerminalSize.js';
import { type CodeSession, fetchCodeSessionsFromSessionsAPI } from 'src/utils/teleport/api.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- raw j/k/arrow list navigation
import { Box, Text, useInput } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { useShortcutDisplay } from '../keybindings/useShortcutDisplay.js';
import { logForDebugging } from '../utils/debug.js';
import { detectCurrentRepository } from '../utils/detectRepository.js';
import { formatRelativeTime } from '../utils/format.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { Select } from './CustomSelect/index.js';
import { Byline } from './design-system/Byline.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import { Spinner } from './Spinner.js';
import { TeleportError } from './TeleportError.js';
type Props = {
  onSelect: (session: CodeSession) => void;
  onCancel: () => void;
  isEmbedded?: boolean;
};
type LoadErrorType = 'network' | 'auth' | 'api' | 'other';
const UPDATED_STRING = 'Updated';
const SPACE_BETWEEN_TABLE_COLUMNS = '  ';
export function ResumeTask({
  onSelect,
  onCancel,
  isEmbedded = false
}: Props): React.ReactNode {
  const {
    rows
  } = useTerminalSize();
  const [sessions, setSessions] = useState<CodeSession[]>([]);
  const [currentRepo, setCurrentRepo] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadErrorType, setLoadErrorType] = useState<LoadErrorType | null>(null);
  const [retrying, setRetrying] = useState(false);
  const [hasCompletedTeleportErrorFlow, setHasCompletedTeleportErrorFlow] = useState(false);

  // Track focused index for scroll position display in title
  const [focusedIndex, setFocusedIndex] = useState(1);
  const escKey = useShortcutDisplay('confirm:no', 'Confirmation', 'Esc');
  const loadSessions = useCallback(async () => {
    try {
      setLoading(true);
      setLoadErrorType(null);

      // Detect current repository
      const detectedRepo = await detectCurrentRepository();
      setCurrentRepo(detectedRepo);

```

---


### `src/components/SandboxViolationExpandedView.tsx`

**信息:**
- 行数: 99
- 大小: 11401 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { type ReactNode, useEffect, useState } from 'react';
import { Box, Text } from '../ink.js';
import type { SandboxViolationEvent } from '../utils/sandbox/sandbox-adapter.js';
import { SandboxManager } from '../utils/sandbox/sandbox-adapter.js';

/**
 * Format a timestamp as "h:mm:ssa" (e.g., "1:30:45pm").
 * Replaces date-fns format() to avoid pulling in a 39MB dependency for one call.
 */
function formatTime(date: Date): string {
  const h = date.getHours() % 12 || 12;
  const m = String(date.getMinutes()).padStart(2, '0');
  const s = String(date.getSeconds()).padStart(2, '0');
  const ampm = date.getHours() < 12 ? 'am' : 'pm';
  return `${h}:${m}:${s}${ampm}`;
}
import { getPlatform } from 'src/utils/platform.js';
export function SandboxViolationExpandedView() {
  const $ = _c(15);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = [];
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  const [violations, setViolations] = useState(t0);
  const [totalCount, setTotalCount] = useState(0);
  let t1;
  let t2;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = () => {
      const store = SandboxManager.getSandboxViolationStore();
      const unsubscribe = store.subscribe(allViolations => {
        setViolations(allViolations.slice(-10));
        setTotalCount(store.getTotalCount());
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
  if (!SandboxManager.isSandboxingEnabled() || getPlatform() === "linux") {

```

---


### `src/components/ScrollKeybindingHandler.tsx`

**信息:**
- 行数: 1012
- 大小: 149202 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React, { type RefObject, useEffect, useRef } from 'react';
import { useNotifications } from '../context/notifications.js';
import { useCopyOnSelect, useSelectionBgColor } from '../hooks/useCopyOnSelect.js';
import type { ScrollBoxHandle } from '../ink/components/ScrollBox.js';
import { useSelection } from '../ink/hooks/use-selection.js';
import type { FocusMove, SelectionState } from '../ink/selection.js';
import { isXtermJs } from '../ink/terminal.js';
import { getClipboardPath } from '../ink/termio/osc.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- Esc needs conditional propagation based on selection state
import { type Key, useInput } from '../ink.js';
import { useKeybindings } from '../keybindings/useKeybinding.js';
import { logForDebugging } from '../utils/debug.js';
type Props = {
  scrollRef: RefObject<ScrollBoxHandle | null>;
  isActive: boolean;
  /** Called after every scroll action with the resulting sticky state and
   *  the handle (for reading scrollTop/scrollHeight post-scroll). */
  onScroll?: (sticky: boolean, handle: ScrollBoxHandle) => void;
  /** Enables modal pager keys (g/G, ctrl+u/d/b/f). Only safe when there
   *  is no text input competing for those characters — i.e. transcript
   *  mode. Defaults to false. When true, G works regardless of editorMode
   *  and sticky state; ctrl+u/d/b/f don't conflict with kill-line/exit/
   *  task:background/kill-agents (none are mounted, or they mount after
   *  this component so stopImmediatePropagation wins). */
  isModal?: boolean;
};

// Terminals send one SGR wheel event per intended row (verified in Ghostty
// src/Surface.zig: `for (0..@abs(y.delta)) |_| { mouseReport(.four, ...) }`).
// Ghostty already 3×'s discrete wheel ticks before that loop; trackpad
// precision scroll is pixels/cell_size. 1 event = 1 row intended — use it
// as the base, and ramp a multiplier when events arrive rapidly. The
// pendingScrollDelta accumulator + proportional drain in
// render-node-to-output handles smooth catch-up on big bursts.
//
// xterm.js (VS Code/Cursor/Windsurf integrated terminals) sends exactly 1
// event per wheel notch — no pre-amplification. A separate exponential
// decay curve (below) compensates for the lower event rate, with burst
// detection and gap-dependent caps tuned to VS Code's event patterns.

// Native terminals: hard-window linear ramp. Events closer than the window
// ramp the multiplier; idle gaps reset to `base` (default 1). Some emulators
// pre-multiply at their layer (ghostty discrete=3 sends 3 SGR events/notch;
// iTerm2 "faster scroll" similar) — base=1 is correct there. Others send 1
// event/notch — users on those can set CLAUDE_CODE_SCROLL_SPEED=3 to match
// vim/nvim/opencode app-side defaults. We can't detect which, so knob it.
const WHEEL_ACCEL_WINDOW_MS = 40;
const WHEEL_ACCEL_STEP = 0.3;
const WHEEL_ACCEL_MAX = 6;


```

---


### `src/components/SearchBox.tsx`

**信息:**
- 行数: 72
- 大小: 9421 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../ink.js';
type Props = {
  query: string;
  placeholder?: string;
  isFocused: boolean;
  isTerminalFocused: boolean;
  prefix?: string;
  width?: number | string;
  cursorOffset?: number;
  borderless?: boolean;
};
export function SearchBox(t0) {
  const $ = _c(17);
  const {
    query,
    placeholder: t1,
    isFocused,
    isTerminalFocused,
    prefix: t2,
    width,
    cursorOffset,
    borderless: t3
  } = t0;
  const placeholder = t1 === undefined ? "Search\u2026" : t1;
  const prefix = t2 === undefined ? "\u2315" : t2;
  const borderless = t3 === undefined ? false : t3;
  const offset = cursorOffset ?? query.length;
  const t4 = borderless ? undefined : "round";
  const t5 = isFocused ? "suggestion" : undefined;
  const t6 = !isFocused;
  const t7 = borderless ? 0 : 1;
  const t8 = !isFocused;
  let t9;
  if ($[0] !== isFocused || $[1] !== isTerminalFocused || $[2] !== offset || $[3] !== placeholder || $[4] !== query) {
    t9 = isFocused ? <>{query ? isTerminalFocused ? <><Text>{query.slice(0, offset)}</Text><Text inverse={true}>{offset < query.length ? query[offset] : " "}</Text>{offset < query.length && <Text>{query.slice(offset + 1)}</Text>}</> : <Text>{query}</Text> : isTerminalFocused ? <><Text inverse={true}>{placeholder.charAt(0)}</Text><Text dimColor={true}>{placeholder.slice(1)}</Text></> : <Text dimColor={true}>{placeholder}</Text>}</> : query ? <Text>{query}</Text> : <Text>{placeholder}</Text>;
    $[0] = isFocused;
    $[1] = isTerminalFocused;
    $[2] = offset;
    $[3] = placeholder;
    $[4] = query;
    $[5] = t9;
  } else {
    t9 = $[5];
  }
  let t10;
  if ($[6] !== prefix || $[7] !== t8 || $[8] !== t9) {
    t10 = <Text dimColor={t8}>{prefix}{" "}{t9}</Text>;
    $[6] = prefix;

```

---


### `src/components/SentryErrorBoundary.ts`

**信息:**
- 行数: 28
- 大小: 487 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import * as React from 'react'

interface Props {
  children: React.ReactNode
}

interface State {
  hasError: boolean
}

export class SentryErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(): State {
    return { hasError: true }
  }

  render(): React.ReactNode {
    if (this.state.hasError) {
      return null
    }

    return this.props.children
  }
}

```

---


### `src/components/SessionBackgroundHint.tsx`

**信息:**
- 行数: 108
- 大小: 13154 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useCallback, useState } from 'react';
import { useDoublePress } from '../hooks/useDoublePress.js';
import { Box, Text } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { useShortcutDisplay } from '../keybindings/useShortcutDisplay.js';
import { useAppState, useAppStateStore, useSetAppState } from '../state/AppState.js';
import { backgroundAll, hasForegroundTasks } from '../tasks/LocalShellTask/LocalShellTask.js';
import { getGlobalConfig, saveGlobalConfig } from '../utils/config.js';
import { env } from '../utils/env.js';
import { isEnvTruthy } from '../utils/envUtils.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
type Props = {
  onBackgroundSession: () => void;
  isLoading: boolean;
};

/**
 * Shows a hint when user presses Ctrl+B to background the current session.
 * Uses double-press pattern: first press shows hint, second press within 800ms backgrounds.
 *
 * Only activates when:
 * 1. isLoading is true (a query is in progress)
 * 2. No foreground tasks (bash/agent) are running (those take priority for Ctrl+B)
 */
export function SessionBackgroundHint(t0) {
  const $ = _c(10);
  const {
    onBackgroundSession,
    isLoading
  } = t0;
  const setAppState = useSetAppState();
  const appStateStore = useAppStateStore();
  const [showSessionHint, setShowSessionHint] = useState(false);
  const handleDoublePress = useDoublePress(setShowSessionHint, onBackgroundSession, _temp);
  let t1;
  if ($[0] !== appStateStore || $[1] !== handleDoublePress || $[2] !== isLoading || $[3] !== setAppState) {
    t1 = () => {
      if (isEnvTruthy(process.env.CLAUDE_CODE_DISABLE_BACKGROUND_TASKS)) {
        return;
      }
      const state = appStateStore.getState();
      if (hasForegroundTasks(state)) {
        backgroundAll(() => appStateStore.getState(), setAppState);
        if (!getGlobalConfig().hasUsedBackgroundTask) {
          saveGlobalConfig(_temp2);
        }
      } else {
        if (isEnvTruthy("false") && isLoading) {

```

---


### `src/components/SessionPreview.tsx`

**信息:**
- 行数: 194
- 大小: 19227 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { UUID } from 'crypto';
import React, { useCallback } from 'react';
import { Box, Text } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { getAllBaseTools } from '../tools.js';
import type { LogOption } from '../types/logs.js';
import { formatRelativeTimeAgo } from '../utils/format.js';
import { getSessionIdFromLog, isLiteLog, loadFullLog } from '../utils/sessionStorage.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { Byline } from './design-system/Byline.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import { LoadingState } from './design-system/LoadingState.js';
import { Messages } from './Messages.js';
type Props = {
  log: LogOption;
  onExit: () => void;
  onSelect: (log: LogOption) => void;
};
export function SessionPreview(t0) {
  const $ = _c(33);
  const {
    log,
    onExit,
    onSelect
  } = t0;
  const [fullLog, setFullLog] = React.useState(null);
  let t1;
  let t2;
  if ($[0] !== log) {
    t1 = () => {
      setFullLog(null);
      if (isLiteLog(log)) {
        loadFullLog(log).then(setFullLog);
      }
    };
    t2 = [log];
    $[0] = log;
    $[1] = t1;
    $[2] = t2;
  } else {
    t1 = $[1];
    t2 = $[2];
  }
  React.useEffect(t1, t2);
  const isLoading = isLiteLog(log) && fullLog === null;
  const displayLog = fullLog ?? log;
  let t3;
  if ($[3] !== displayLog) {
    t3 = getSessionIdFromLog(displayLog) || "" as UUID;

```

---


### `src/components/Settings/Config.tsx`

**信息:**
- 行数: 1822
- 大小: 271407 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
import { feature } from 'bun:bundle';
import { Box, Text, useTheme, useThemeSetting, useTerminalFocus } from '../../ink.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import * as React from 'react';
import { useState, useCallback } from 'react';
import { useKeybinding, useKeybindings } from '../../keybindings/useKeybinding.js';
import figures from 'figures';
import { type GlobalConfig, saveGlobalConfig, getCurrentProjectConfig, type OutputStyle } from '../../utils/config.js';
import { normalizeApiKeyForConfig } from '../../utils/authPortable.js';
import { getGlobalConfig, getAutoUpdaterDisabledReason, formatAutoUpdaterDisabledReason, getRemoteControlAtStartup } from '../../utils/config.js';
import chalk from 'chalk';
import { permissionModeTitle, permissionModeFromString, toExternalPermissionMode, isExternalPermissionMode, EXTERNAL_PERMISSION_MODES, PERMISSION_MODES, type ExternalPermissionMode, type PermissionMode } from '../../utils/permissions/PermissionMode.js';
import { getAutoModeEnabledState, hasAutoModeOptInAnySource, transitionPlanAutoMode } from '../../utils/permissions/permissionSetup.js';
import { logError } from '../../utils/log.js';
import { logEvent, type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS } from 'src/services/analytics/index.js';
import { isBridgeEnabled } from '../../bridge/bridgeEnabled.js';
import { ThemePicker } from '../ThemePicker.js';
import { useAppState, useSetAppState, useAppStateStore } from '../../state/AppState.js';
import { ModelPicker } from '../ModelPicker.js';
import { modelDisplayString, isOpus1mMergeEnabled } from '../../utils/model/model.js';
import { isBilledAsExtraUsage } from '../../utils/extraUsage.js';
import { ClaudeMdExternalIncludesDialog } from '../ClaudeMdExternalIncludesDialog.js';
import { ChannelDowngradeDialog, type ChannelDowngradeChoice } from '../ChannelDowngradeDialog.js';
import { Dialog } from '../design-system/Dialog.js';
import { Select } from '../CustomSelect/index.js';
import { OutputStylePicker } from '../OutputStylePicker.js';
import { LanguagePicker } from '../LanguagePicker.js';
import { getExternalClaudeMdIncludes, getMemoryFiles, hasExternalClaudeMdIncludes } from 'src/utils/claudemd.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Byline } from '../design-system/Byline.js';
import { useTabHeaderFocus } from '../design-system/Tabs.js';
import { useIsInsideModal } from '../../context/modalContext.js';
import { SearchBox } from '../SearchBox.js';
import { isSupportedTerminal, hasAccessToIDEExtensionDiffFeature } from '../../utils/ide.js';
import { getInitialSettings, getSettingsForSource, updateSettingsForSource } from '../../utils/settings/settings.js';
import { getUserMsgOptIn, setUserMsgOptIn } from '../../bootstrap/state.js';
import { DEFAULT_OUTPUT_STYLE_NAME } from 'src/constants/outputStyles.js';
import { isEnvTruthy, isRunningOnHomespace } from 'src/utils/envUtils.js';
import type { LocalJSXCommandContext, CommandResultDisplay } from '../../commands.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js';
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js';
import { getCliTeammateModeOverride, clearCliTeammateModeOverride } from '../../utils/swarm/backends/teammateModeSnapshot.js';
import { getHardcodedTeammateModelFallback } from '../../utils/swarm/teammateModel.js';
import { useSearchInput } from '../../hooks/useSearchInput.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { clearFastModeCooldown, FAST_MODE_MODEL_DISPLAY, isFastModeAvailable, isFastModeEnabled, getFastModeModel, isFastModeSupportedByModel } from '../../utils/fastMode.js';
import { isFullscreenEnvEnabled } from '../../utils/fullscreen.js';

```

---


### `src/components/Settings/Settings.tsx`

**信息:**
- 行数: 137
- 大小: 18641 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
import * as React from 'react';
import { Suspense, useState } from 'react';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { useIsInsideModal, useModalOrTerminalSize } from '../../context/modalContext.js';
import { Pane } from '../design-system/Pane.js';
import { Tabs, Tab } from '../design-system/Tabs.js';
import { Status, buildDiagnostics } from './Status.js';
import { Config } from './Config.js';
import { Usage } from './Usage.js';
import type { LocalJSXCommandContext, CommandResultDisplay } from '../../commands.js';
type Props = {
  onClose: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  context: LocalJSXCommandContext;
  defaultTab: 'Status' | 'Config' | 'Usage' | 'Gates';
};
export function Settings(t0) {
  const $ = _c(25);
  const {
    onClose,
    context,
    defaultTab
  } = t0;
  const [selectedTab, setSelectedTab] = useState(defaultTab);
  const [tabsHidden, setTabsHidden] = useState(false);
  const [configOwnsEsc, setConfigOwnsEsc] = useState(false);
  const [gatesOwnsEsc, setGatesOwnsEsc] = useState(false);
  const insideModal = useIsInsideModal();
  const {
    rows
  } = useModalOrTerminalSize(useTerminalSize());
  const contentHeight = insideModal ? rows + 1 : Math.max(15, Math.min(Math.floor(rows * 0.8), 30));
  const [diagnosticsPromise] = useState(_temp2);
  useExitOnCtrlCDWithKeybindings();
  let t1;
  if ($[0] !== onClose || $[1] !== tabsHidden) {
    t1 = () => {
      if (tabsHidden) {
        return;
      }
      onClose("Status dialog dismissed", {
        display: "system"
      });
    };
    $[0] = onClose;

```

---


### `src/components/Settings/Status.tsx`

**信息:**
- 行数: 241
- 大小: 25871 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { Suspense, use } from 'react';
import { getSessionId } from '../../bootstrap/state.js';
import type { LocalJSXCommandContext } from '../../commands.js';
import { useIsInsideModal } from '../../context/modalContext.js';
import { Box, Text, useTheme } from '../../ink.js';
import { type AppState, useAppState } from '../../state/AppState.js';
import { getCwd } from '../../utils/cwd.js';
import { getCurrentSessionTitle } from '../../utils/sessionStorage.js';
import { buildAccountProperties, buildAPIProviderProperties, buildIDEProperties, buildInstallationDiagnostics, buildInstallationHealthDiagnostics, buildMcpProperties, buildMemoryDiagnostics, buildSandboxProperties, buildSettingSourcesProperties, type Diagnostic, getModelDisplayLabel, type Property } from '../../utils/status.js';
import type { ThemeName } from '../../utils/theme.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
type Props = {
  context: LocalJSXCommandContext;
  diagnosticsPromise: Promise<Diagnostic[]>;
};
function buildPrimarySection(): Property[] {
  const sessionId = getSessionId();
  const customTitle = getCurrentSessionTitle(sessionId);
  const nameValue = customTitle ?? <Text dimColor>/rename to add a name</Text>;
  return [{
    label: 'Version',
    value: MACRO.VERSION
  }, {
    label: 'Session name',
    value: nameValue
  }, {
    label: 'Session ID',
    value: sessionId
  }, {
    label: 'cwd',
    value: getCwd()
  }, ...buildAccountProperties(), ...buildAPIProviderProperties()];
}
function buildSecondarySection({
  mainLoopModel,
  mcp,
  theme,
  context
}: {
  mainLoopModel: AppState['mainLoopModel'];
  mcp: AppState['mcp'];
  theme: ThemeName;
  context: LocalJSXCommandContext;
}): Property[] {
  const modelLabel = getModelDisplayLabel(mainLoopModel);
  return [{
    label: 'Model',

```

---


### `src/components/Settings/Usage.tsx`

**信息:**
- 行数: 377
- 大小: 39524 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useEffect, useState } from 'react';
import { extraUsage as extraUsageCommand } from 'src/commands/extra-usage/index.js';
import { formatCost } from 'src/cost-tracker.js';
import { getSubscriptionType } from 'src/utils/auth.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { type ExtraUsage, fetchUtilization, type RateLimit, type Utilization } from '../../services/api/usage.js';
import { formatResetText } from '../../utils/format.js';
import { logError } from '../../utils/log.js';
import { jsonStringify } from '../../utils/slowOperations.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Byline } from '../design-system/Byline.js';
import { ProgressBar } from '../design-system/ProgressBar.js';
import { isEligibleForOverageCreditGrant, OverageCreditUpsell } from '../LogoV2/OverageCreditUpsell.js';
type LimitBarProps = {
  title: string;
  limit: RateLimit;
  maxWidth: number;
  showTimeInReset?: boolean;
  extraSubtext?: string;
};
function LimitBar(t0) {
  const $ = _c(34);
  const {
    title,
    limit,
    maxWidth,
    showTimeInReset: t1,
    extraSubtext
  } = t0;
  const showTimeInReset = t1 === undefined ? true : t1;
  const {
    utilization,
    resets_at
  } = limit;
  if (utilization === null) {
    return null;
  }
  const usedText = `${Math.floor(utilization)}% used`;
  let subtext;
  if (resets_at) {
    let t2;
    if ($[0] !== resets_at || $[1] !== showTimeInReset) {
      t2 = formatResetText(resets_at, true, showTimeInReset);
      $[0] = resets_at;
      $[1] = showTimeInReset;
      $[2] = t2;

```

---


### `src/components/ShowInIDEPrompt.tsx`

**信息:**
- 行数: 170
- 大小: 17230 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { basename, relative } from 'path';
import React from 'react';
import { Box, Text } from '../ink.js';
import { getCwd } from '../utils/cwd.js';
import { isSupportedVSCodeTerminal } from '../utils/ide.js';
import { Select } from './CustomSelect/index.js';
import { Pane } from './design-system/Pane.js';
import type { PermissionOption, PermissionOptionWithLabel } from './permissions/FilePermissionDialog/permissionOptions.js';
type Props<A> = {
  filePath: string;
  input: A;
  onChange: (option: PermissionOption, args: A, feedback?: string) => void;
  options: PermissionOptionWithLabel[];
  ideName: string;
  symlinkTarget?: string | null;
  rejectFeedback: string;
  acceptFeedback: string;
  setFocusedOption: (value: string) => void;
  onInputModeToggle: (value: string) => void;
  focusedOption: string;
  yesInputMode: boolean;
  noInputMode: boolean;
};
export function ShowInIDEPrompt(t0) {
  const $ = _c(36);
  const {
    onChange,
    options,
    input,
    filePath,
    ideName,
    symlinkTarget,
    rejectFeedback,
    acceptFeedback,
    setFocusedOption,
    onInputModeToggle,
    focusedOption,
    yesInputMode,
    noInputMode
  } = t0;
  let t1;
  if ($[0] !== ideName) {
    t1 = <Text bold={true} color="permission">Opened changes in {ideName} ⧉</Text>;
    $[0] = ideName;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;

```

---


### `src/components/SkillImprovementSurvey.tsx`

**信息:**
- 行数: 152
- 大小: 15172 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useEffect, useRef } from 'react';
import { BLACK_CIRCLE, BULLET_OPERATOR } from '../constants/figures.js';
import { Box, Text } from '../ink.js';
import type { SkillUpdate } from '../utils/hooks/skillImprovement.js';
import { normalizeFullWidthDigits } from '../utils/stringUtils.js';
import { isValidResponseInput } from './FeedbackSurvey/FeedbackSurveyView.js';
import type { FeedbackSurveyResponse } from './FeedbackSurvey/utils.js';
type Props = {
  isOpen: boolean;
  skillName: string;
  updates: SkillUpdate[];
  handleSelect: (selected: FeedbackSurveyResponse) => void;
  inputValue: string;
  setInputValue: (value: string) => void;
};
export function SkillImprovementSurvey(t0) {
  const $ = _c(6);
  const {
    isOpen,
    skillName,
    updates,
    handleSelect,
    inputValue,
    setInputValue
  } = t0;
  if (!isOpen) {
    return null;
  }
  if (inputValue && !isValidResponseInput(inputValue)) {
    return null;
  }
  let t1;
  if ($[0] !== handleSelect || $[1] !== inputValue || $[2] !== setInputValue || $[3] !== skillName || $[4] !== updates) {
    t1 = <SkillImprovementSurveyView skillName={skillName} updates={updates} onSelect={handleSelect} inputValue={inputValue} setInputValue={setInputValue} />;
    $[0] = handleSelect;
    $[1] = inputValue;
    $[2] = setInputValue;
    $[3] = skillName;
    $[4] = updates;
    $[5] = t1;
  } else {
    t1 = $[5];
  }
  return t1;
}
type ViewProps = {
  skillName: string;
  updates: SkillUpdate[];
  onSelect: (option: FeedbackSurveyResponse) => void;

```

---


### `src/components/Spinner/FlashingChar.tsx`

**信息:**
- 行数: 61
- 大小: 6310 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Text, useTheme } from '../../ink.js';
import { getTheme, type Theme } from '../../utils/theme.js';
import { interpolateColor, parseRGB, toRGBColor } from './utils.js';
type Props = {
  char: string;
  flashOpacity: number;
  messageColor: keyof Theme;
  shimmerColor: keyof Theme;
};
export function FlashingChar(t0) {
  const $ = _c(9);
  const {
    char,
    flashOpacity,
    messageColor,
    shimmerColor
  } = t0;
  const [themeName] = useTheme();
  let t1;
  if ($[0] !== char || $[1] !== flashOpacity || $[2] !== messageColor || $[3] !== shimmerColor || $[4] !== themeName) {
    t1 = Symbol.for("react.early_return_sentinel");
    bb0: {
      const theme = getTheme(themeName);
      const baseColorStr = theme[messageColor];
      const shimmerColorStr = theme[shimmerColor];
      const baseRGB = baseColorStr ? parseRGB(baseColorStr) : null;
      const shimmerRGB = shimmerColorStr ? parseRGB(shimmerColorStr) : null;
      if (baseRGB && shimmerRGB) {
        const interpolated = interpolateColor(baseRGB, shimmerRGB, flashOpacity);
        t1 = <Text color={toRGBColor(interpolated)}>{char}</Text>;
        break bb0;
      }
    }
    $[0] = char;
    $[1] = flashOpacity;
    $[2] = messageColor;
    $[3] = shimmerColor;
    $[4] = themeName;
    $[5] = t1;
  } else {
    t1 = $[5];
  }
  if (t1 !== Symbol.for("react.early_return_sentinel")) {
    return t1;
  }
  const shouldUseShimmer = flashOpacity > 0.5;
  const t2 = shouldUseShimmer ? shimmerColor : messageColor;
  let t3;

```

---


### `src/components/Spinner/GlimmerMessage.tsx`

**信息:**
- 行数: 328
- 大小: 26955 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { stringWidth } from '../../ink/stringWidth.js';
import { Text, useTheme } from '../../ink.js';
import { getGraphemeSegmenter } from '../../utils/intl.js';
import { getTheme, type Theme } from '../../utils/theme.js';
import type { SpinnerMode } from './types.js';
import { interpolateColor, parseRGB, toRGBColor } from './utils.js';
type Props = {
  message: string;
  mode: SpinnerMode;
  messageColor: keyof Theme;
  glimmerIndex: number;
  flashOpacity: number;
  shimmerColor: keyof Theme;
  stalledIntensity?: number;
};
const ERROR_RED = {
  r: 171,
  g: 43,
  b: 63
};
export function GlimmerMessage(t0) {
  const $ = _c(75);
  const {
    message,
    mode,
    messageColor,
    glimmerIndex,
    flashOpacity,
    shimmerColor,
    stalledIntensity: t1
  } = t0;
  const stalledIntensity = t1 === undefined ? 0 : t1;
  const [themeName] = useTheme();
  let messageWidth;
  let segments;
  let t2;
  if ($[0] !== flashOpacity || $[1] !== message || $[2] !== messageColor || $[3] !== mode || $[4] !== shimmerColor || $[5] !== stalledIntensity || $[6] !== themeName) {
    t2 = Symbol.for("react.early_return_sentinel");
    bb0: {
      const theme = getTheme(themeName);
      let segs;
      if ($[10] !== message) {
        segs = [];
        for (const {
          segment
        } of getGraphemeSegmenter().segment(message)) {
          segs.push({
            segment,

```

---


### `src/components/Spinner/ShimmerChar.tsx`

**信息:**
- 行数: 36
- 大小: 3357 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Text } from '../../ink.js';
import type { Theme } from '../../utils/theme.js';
type Props = {
  char: string;
  index: number;
  glimmerIndex: number;
  messageColor: keyof Theme;
  shimmerColor: keyof Theme;
};
export function ShimmerChar(t0) {
  const $ = _c(3);
  const {
    char,
    index,
    glimmerIndex,
    messageColor,
    shimmerColor
  } = t0;
  const isHighlighted = index === glimmerIndex;
  const isNearHighlight = Math.abs(index - glimmerIndex) === 1;
  const shouldUseShimmer = isHighlighted || isNearHighlight;
  const t1 = shouldUseShimmer ? shimmerColor : messageColor;
  let t2;
  if ($[0] !== char || $[1] !== t1) {
    t2 = <Text color={t1}>{char}</Text>;
    $[0] = char;
    $[1] = t1;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  return t2;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlRleHQiLCJUaGVtZSIsIlByb3BzIiwiY2hhciIsImluZGV4IiwiZ2xpbW1lckluZGV4IiwibWVzc2FnZUNvbG9yIiwic2hpbW1lckNvbG9yIiwiU2hpbW1lckNoYXIiLCJ0MCIsIiQiLCJfYyIsImlzSGlnaGxpZ2h0ZWQiLCJpc05lYXJIaWdobGlnaHQiLCJNYXRoIiwiYWJzIiwic2hvdWxkVXNlU2hpbW1lciIsInQxIiwidDIiXSwic291cmNlcyI6WyJTaGltbWVyQ2hhci50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBUZXh0IH0gZnJvbSAnLi4vLi4vaW5rLmpzJ1xuaW1wb3J0IHR5cGUgeyBUaGVtZSB9IGZyb20gJy4uLy4uL3V0aWxzL3RoZW1lLmpzJ1xuXG50eXBlIFByb3BzID0ge1xuICBjaGFyOiBzdHJpbmdcbiAgaW5kZXg6IG51bWJlclxuICBnbGltbWVySW5kZXg6IG51bWJlclxuICBtZXNzYWdlQ29sb3I6IGtleW9mIFRoZW1lXG4gIHNoaW1tZXJDb2xvcjoga2V5b2YgVGhlbWVcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIFNoaW1tZXJDaGFyKHtcbiAgY2hhcixcbiAgaW5kZXgsXG4gIGdsaW1tZXJJbmRleCxcbiAgbWVzc2FnZUNvbG9yLFxuICBzaGltbWVyQ29sb3IsXG59OiBQcm9wcyk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIGNvbnN0IGlzSGlnaGxpZ2h0ZWQgPSBpbmRleCA9PT0gZ2xpbW1lckluZGV4XG4gIGNvbnN0IGlzTmVhckhpZ2hsaWdodCA9IE1hdGguYWJzKGluZGV4IC0gZ2xpbW1lckluZGV4KSA9PT0gMVxuICBjb25zdCBzaG91bGRVc2VTaGltbWVyID0gaXNIaWdobGlnaHRlZCB8fCBpc05lYXJIaWdobGlnaHRcblxuICByZXR1cm4gKFxuICAgIDxUZXh0IGNvbG9yPXtzaG91bGRVc2VTaGltbWVyID8gc2hpbW1lckNvbG9yIDogbWVzc2FnZUNvbG9yfT57Y2hhcn08L1RleHQ+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsSUFBSSxRQUFRLGNBQWM7QUFDbkMsY0FBY0MsS0FBSyxRQUFRLHNCQUFzQjtBQUVqRCxLQUFLQyxLQUFLLEdBQUc7RUFDWEMsSUFBSSxFQUFFLE1BQU07RUFDWkMsS0FBSyxFQUFFLE1BQU07RUFDYkMsWUFBWSxFQUFFLE1BQU07RUFDcEJDLFlBQVksRUFBRSxNQUFNTCxLQUFLO0VBQ3pCTSxZQUFZLEVBQUUsTUFBTU4sS0FBSztBQUMzQixDQUFDO0FBRUQsT0FBTyxTQUFBTyxZQUFBQyxFQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQXFCO0lBQUFSLElBQUE7SUFBQUMsS0FBQTtJQUFBQyxZQUFBO0lBQUFDLFlBQUE7SUFBQUM7RUFBQSxJQUFBRSxFQU1wQjtFQUNOLE1BQUFHLGFBQUEsR0FBc0JSLEtBQUssS0FBS0MsWUFBWTtFQUM1QyxNQUFBUSxlQUFBLEdBQXdCQyxJQUFJLENBQUFDLEdBQUksQ0FBQ1gsS0FBSyxHQUFHQyxZQUFZLENBQUMsS0FBSyxDQUFDO0VBQzVELE1BQUFXLGdCQUFBLEdBQXlCSixhQUFnQyxJQUFoQ0MsZUFBZ0M7RUFHMUMsTUFBQUksRUFBQSxHQUFBRCxnQkFBZ0IsR0FBaEJULFlBQThDLEdBQTlDRCxZQUE4QztFQUFBLElBQUFZLEVBQUE7RUFBQSxJQUFBUixDQUFBLFFBQUFQLElBQUEsSUFBQU8sQ0FBQSxRQUFBTyxFQUFBO0lBQTNEQyxFQUFBLElBQUMsSUFBSSxDQUFRLEtBQThDLENBQTlDLENBQUFELEVBQTZDLENBQUMsQ0FBR2QsS0FBRyxDQUFFLEVBQWxFLElBQUksQ0FBcUU7SUFBQU8sQ0FBQSxNQUFBUCxJQUFBO0lBQUFPLENBQUEsTUFBQU8sRUFBQTtJQUFBUCxDQUFBLE1BQUFRLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFSLENBQUE7RUFBQTtFQUFBLE9BQTFFUSxFQUEwRTtBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/Spinner/SpinnerAnimationRow.tsx`

**信息:**
- 行数: 265
- 大小: 42767 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useMemo, useRef } from 'react';
import { stringWidth } from '../../ink/stringWidth.js';
import { Box, Text, useAnimationFrame } from '../../ink.js';
import type { InProcessTeammateTaskState } from '../../tasks/InProcessTeammateTask/types.js';
import { formatDuration, formatNumber } from '../../utils/format.js';
import { toInkColor } from '../../utils/ink.js';
import type { Theme } from '../../utils/theme.js';
import { Byline } from '../design-system/Byline.js';
import { GlimmerMessage } from './GlimmerMessage.js';
import { SpinnerGlyph } from './SpinnerGlyph.js';
import type { SpinnerMode } from './types.js';
import { useStalledAnimation } from './useStalledAnimation.js';
import { interpolateColor, toRGBColor } from './utils.js';
const SEP_WIDTH = stringWidth(' · ');
const THINKING_BARE_WIDTH = stringWidth('thinking');
const SHOW_TOKENS_AFTER_MS = 30_000;

// Thinking shimmer constants. Previously lived in a separate ThinkingShimmerText
// component with its own useAnimationFrame(50) — inlined here to reuse our
// existing 50ms clock and eliminate the redundant subscriber.
const THINKING_INACTIVE = {
  r: 153,
  g: 153,
  b: 153
};
const THINKING_INACTIVE_SHIMMER = {
  r: 185,
  g: 185,
  b: 185
};
const THINKING_DELAY_MS = 3000;
const THINKING_GLOW_PERIOD_S = 2;
export type SpinnerAnimationRowProps = {
  // Animation inputs
  mode: SpinnerMode;
  reducedMotion: boolean;
  hasActiveTools: boolean;
  responseLengthRef: React.RefObject<number>;

  // Message (stable within a turn)
  message: string;
  messageColor: keyof Theme;
  shimmerColor: keyof Theme;
  overrideColor?: keyof Theme | null;

  // Timer refs (stable references)
  loadingStartTimeRef: React.RefObject<number>;

```

---


### `src/components/Spinner/SpinnerGlyph.tsx`

**信息:**
- 行数: 80
- 大小: 10291 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text, useTheme } from '../../ink.js';
import { getTheme, type Theme } from '../../utils/theme.js';
import { getDefaultCharacters, interpolateColor, parseRGB, toRGBColor } from './utils.js';
const DEFAULT_CHARACTERS = getDefaultCharacters();
const SPINNER_FRAMES = [...DEFAULT_CHARACTERS, ...[...DEFAULT_CHARACTERS].reverse()];
const REDUCED_MOTION_DOT = '●';
const REDUCED_MOTION_CYCLE_MS = 2000; // 2-second cycle: 1s visible, 1s dim
const ERROR_RED = {
  r: 171,
  g: 43,
  b: 63
};
type Props = {
  frame: number;
  messageColor: keyof Theme;
  stalledIntensity?: number;
  reducedMotion?: boolean;
  time?: number;
};
export function SpinnerGlyph(t0) {
  const $ = _c(9);
  const {
    frame,
    messageColor,
    stalledIntensity: t1,
    reducedMotion: t2,
    time: t3
  } = t0;
  const stalledIntensity = t1 === undefined ? 0 : t1;
  const reducedMotion = t2 === undefined ? false : t2;
  const time = t3 === undefined ? 0 : t3;
  const [themeName] = useTheme();
  const theme = getTheme(themeName);
  if (reducedMotion) {
    const isDim = Math.floor(time / (REDUCED_MOTION_CYCLE_MS / 2)) % 2 === 1;
    let t4;
    if ($[0] !== isDim || $[1] !== messageColor) {
      t4 = <Box flexWrap="wrap" height={1} width={2}><Text color={messageColor} dimColor={isDim}>{REDUCED_MOTION_DOT}</Text></Box>;
      $[0] = isDim;
      $[1] = messageColor;
      $[2] = t4;
    } else {
      t4 = $[2];
    }
    return t4;
  }
  const spinnerChar = SPINNER_FRAMES[frame % SPINNER_FRAMES.length];
  if (stalledIntensity > 0) {

```

---


### `src/components/Spinner/TeammateSpinnerLine.tsx`

**信息:**
- 行数: 233
- 大小: 38859 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import figures from 'figures';
import sample from 'lodash-es/sample.js';
import * as React from 'react';
import { useRef, useState } from 'react';
import { getSpinnerVerbs } from '../../constants/spinnerVerbs.js';
import { TURN_COMPLETION_VERBS } from '../../constants/turnCompletionVerbs.js';
import { useElapsedTime } from '../../hooks/useElapsedTime.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { Box, Text } from '../../ink.js';
import type { InProcessTeammateTaskState } from '../../tasks/InProcessTeammateTask/types.js';
import { summarizeRecentActivities } from '../../utils/collapseReadSearch.js';
import { formatDuration, formatNumber, truncateToWidth } from '../../utils/format.js';
import { toInkColor } from '../../utils/ink.js';
import { TEAMMATE_SELECT_HINT } from './teammateSelectHint.js';
type Props = {
  teammate: InProcessTeammateTaskState;
  isLast: boolean;
  isSelected?: boolean;
  isForegrounded?: boolean;
  allIdle?: boolean;
  showPreview?: boolean;
};

/**
 * Extract the last 3 lines of content from a teammate's conversation.
 * Shows recent activity from any message type (user or assistant).
 */
function getMessagePreview(messages: InProcessTeammateTaskState['messages']): string[] {
  if (!messages?.length) return [];
  const allLines: string[] = [];
  const maxLineLength = 80;

  // Collect lines from recent messages (newest first)
  for (let i = messages.length - 1; i >= 0 && allLines.length < 3; i--) {
    const msg = messages[i];
    // Only process messages that have content (user/assistant messages)
    if (!msg || msg.type !== 'user' && msg.type !== 'assistant' || !msg.message?.content?.length) {
      continue;
    }
    const content = msg.message.content;
    for (const block of content) {
      if (allLines.length >= 3) break;
      if (!block || typeof block !== 'object') continue;
      if ('type' in block && block.type === 'tool_use' && 'name' in block) {
        // Try to show meaningful info from tool input
        const input = 'input' in block ? block.input as Record<string, unknown> : null;
        let toolLine = `Using ${block.name}…`;
        if (input) {
          // Look for common descriptive fields

```

---


### `src/components/Spinner/TeammateSpinnerTree.tsx`

**信息:**
- 行数: 272
- 大小: 28052 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { Box, Text, type TextProps } from '../../ink.js';
import { useAppState } from '../../state/AppState.js';
import { getRunningTeammatesSorted } from '../../tasks/InProcessTeammateTask/InProcessTeammateTask.js';
import { formatNumber } from '../../utils/format.js';
import { TeammateSpinnerLine } from './TeammateSpinnerLine.js';
import { TEAMMATE_SELECT_HINT } from './teammateSelectHint.js';
type Props = {
  selectedIndex?: number;
  isInSelectionMode?: boolean;
  allIdle?: boolean;
  /** Leader's active verb (when leader is actively processing) */
  leaderVerb?: string;
  /** Leader's token count (when leader is actively processing) */
  leaderTokenCount?: number;
  /** Leader's idle status text (when leader is idle, e.g. "✻ Idle for 3s") */
  leaderIdleText?: string;
};
export function TeammateSpinnerTree(t0) {
  const $ = _c(61);
  const {
    selectedIndex,
    isInSelectionMode,
    allIdle,
    leaderVerb,
    leaderTokenCount,
    leaderIdleText
  } = t0;
  const tasks = useAppState(_temp);
  const viewingAgentTaskId = useAppState(_temp2);
  const showTeammateMessagePreview = useAppState(_temp3);
  let T0;
  let isHideSelected;
  let t1;
  let t2;
  let t3;
  let t4;
  let t5;
  if ($[0] !== allIdle || $[1] !== isInSelectionMode || $[2] !== leaderIdleText || $[3] !== leaderTokenCount || $[4] !== leaderVerb || $[5] !== selectedIndex || $[6] !== showTeammateMessagePreview || $[7] !== tasks || $[8] !== viewingAgentTaskId) {
    t5 = Symbol.for("react.early_return_sentinel");
    bb0: {
      const teammateTasks = getRunningTeammatesSorted(tasks);
      if (teammateTasks.length === 0) {
        t5 = null;
        break bb0;
      }
      const isLeaderForegrounded = viewingAgentTaskId === undefined;
      const isLeaderSelected = isInSelectionMode && selectedIndex === -1;

```

---


### `src/components/Spinner/index.ts`

**信息:**
- 行数: 10
- 大小: 602 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export { FlashingChar } from './FlashingChar.js'
export { GlimmerMessage } from './GlimmerMessage.js'
export { ShimmerChar } from './ShimmerChar.js'
export { SpinnerGlyph } from './SpinnerGlyph.js'
export type { SpinnerMode } from './types.js'
export { useShimmerAnimation } from './useShimmerAnimation.js'
export { useStalledAnimation } from './useStalledAnimation.js'
export { getDefaultCharacters, interpolateColor } from './utils.js'
// Teammate components are NOT exported here - use dynamic require() to enable dead code elimination
// See REPL.tsx and Spinner.tsx for the correct import pattern

```

---


### `src/components/Spinner/teammateSelectHint.ts`

**信息:**
- 行数: 1
- 大小: 64 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TEAMMATE_SELECT_HINT = 'shift + ↑/↓ to select'

```

---


### `src/components/Spinner/types.ts`

**信息:**
- 行数: 6
- 大小: 96 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type SpinnerMode = string
export type RGBColor = {
  r: number
  g: number
  b: number
}

```

---


### `src/components/Spinner/useShimmerAnimation.ts`

**信息:**
- 行数: 31
- 大小: 1236 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useMemo } from 'react'
import { stringWidth } from '../../ink/stringWidth.js'
import { type DOMElement, useAnimationFrame } from '../../ink.js'
import type { SpinnerMode } from './types.js'

export function useShimmerAnimation(
  mode: SpinnerMode,
  message: string,
  isStalled: boolean,
): [ref: (element: DOMElement | null) => void, glimmerIndex: number] {
  const glimmerSpeed = mode === 'requesting' ? 50 : 200
  // Pass null when stalled to unsubscribe from the clock — otherwise the
  // setInterval keeps firing at 20fps even when the shimmer isn't visible.
  // Notably, if the caller never attaches `ref` (e.g. conditional JSX),
  // useTerminalViewport stays at its initial isVisible:true and the
  // viewport-pause never kicks in, so this is the only stop mechanism.
  const [ref, time] = useAnimationFrame(isStalled ? null : glimmerSpeed)
  const messageWidth = useMemo(() => stringWidth(message), [message])

  if (isStalled) {
    return [ref, -100]
  }

  const cyclePosition = Math.floor(time / glimmerSpeed)
  const cycleLength = messageWidth + 20

  if (mode === 'requesting') {
    return [ref, (cyclePosition % cycleLength) - 10]
  }
  return [ref, messageWidth + 10 - (cyclePosition % cycleLength)]
}

```

---


### `src/components/Spinner/useStalledAnimation.ts`

**信息:**
- 行数: 75
- 大小: 2500 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useRef } from 'react'

// Hook to handle the transition to red when tokens stop flowing.
// Driven by the parent's animation clock time instead of independent intervals,
// so it slows down when the terminal is blurred.
export function useStalledAnimation(
  time: number,
  currentResponseLength: number,
  hasActiveTools = false,
  reducedMotion = false,
): {
  isStalled: boolean
  stalledIntensity: number
} {
  const lastTokenTime = useRef(time)
  const lastResponseLength = useRef(currentResponseLength)
  const mountTime = useRef(time)
  const stalledIntensityRef = useRef(0)
  const lastSmoothTime = useRef(time)

  // Reset timer when new tokens arrive (check actual length change)
  if (currentResponseLength > lastResponseLength.current) {
    lastTokenTime.current = time
    lastResponseLength.current = currentResponseLength
    stalledIntensityRef.current = 0
    lastSmoothTime.current = time
  }

  // Derive time since last token from animation clock
  let timeSinceLastToken: number
  if (hasActiveTools) {
    timeSinceLastToken = 0
    lastTokenTime.current = time
  } else if (currentResponseLength > 0) {
    timeSinceLastToken = time - lastTokenTime.current
  } else {
    timeSinceLastToken = time - mountTime.current
  }

  // Calculate stalled intensity based on time since last token
  // Start showing red after 3 seconds of no new tokens (only when no tools are active)
  const isStalled = timeSinceLastToken > 3000 && !hasActiveTools
  const intensity = isStalled
    ? Math.min((timeSinceLastToken - 3000) / 2000, 1) // Fade over 2 seconds
    : 0

  // Smooth intensity transition driven by animation frame ticks
  if (!reducedMotion && (intensity > 0 || stalledIntensityRef.current > 0)) {
    const dt = time - lastSmoothTime.current
    if (dt >= 50) {

```

---


### `src/components/Spinner/utils.ts`

**信息:**
- 行数: 84
- 大小: 2261 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { RGBColor as RGBColorString } from '../../ink/styles.js'
import type { RGBColor as RGBColorType } from './types.js'

export function getDefaultCharacters(): string[] {
  if (process.env.TERM === 'xterm-ghostty') {
    return ['·', '✢', '✳', '✶', '✻', '*'] // Use * instead of ✽ for Ghostty because the latter renders in a way that's slightly offset
  }
  return process.platform === 'darwin'
    ? ['·', '✢', '✳', '✶', '✻', '✽']
    : ['·', '✢', '*', '✶', '✻', '✽']
}

// Interpolate between two RGB colors
export function interpolateColor(
  color1: RGBColorType,
  color2: RGBColorType,
  t: number, // 0 to 1
): RGBColorType {
  return {
    r: Math.round(color1.r + (color2.r - color1.r) * t),
    g: Math.round(color1.g + (color2.g - color1.g) * t),
    b: Math.round(color1.b + (color2.b - color1.b) * t),
  }
}

// Convert RGB object to rgb() color string for Text component
export function toRGBColor(color: RGBColorType): RGBColorString {
  return `rgb(${color.r},${color.g},${color.b})`
}

// HSL hue (0-360) to RGB, using voice-mode waveform parameters (s=0.7, l=0.6).
export function hueToRgb(hue: number): RGBColorType {
  const h = ((hue % 360) + 360) % 360
  const s = 0.7
  const l = 0.6
  const c = (1 - Math.abs(2 * l - 1)) * s
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1))
  const m = l - c / 2
  let r = 0
  let g = 0
  let b = 0
  if (h < 60) {
    r = c
    g = x
  } else if (h < 120) {
    r = x
    g = c
  } else if (h < 180) {
    g = c
    b = x

```

---


### `src/components/Spinner.tsx`

**信息:**
- 行数: 562
- 大小: 87940 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
import { Box, Text } from '../ink.js';
import * as React from 'react';
import { useEffect, useMemo, useRef, useState } from 'react';
import { computeGlimmerIndex, computeShimmerSegments, SHIMMER_INTERVAL_MS } from '../bridge/bridgeStatusUtil.js';
import { feature } from 'bun:bundle';
import { getKairosActive, getUserMsgOptIn } from '../bootstrap/state.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js';
import { isEnvTruthy } from '../utils/envUtils.js';
import { count } from '../utils/array.js';
import sample from 'lodash-es/sample.js';
import { formatDuration, formatNumber, formatSecondsShort } from '../utils/format.js';
import type { Theme } from 'src/utils/theme.js';
import { activityManager } from '../utils/activityManager.js';
import { getSpinnerVerbs } from '../constants/spinnerVerbs.js';
import { MessageResponse } from './MessageResponse.js';
import { TaskListV2 } from './TaskListV2.js';
import { useTasksV2 } from '../hooks/useTasksV2.js';
import type { Task } from '../utils/tasks.js';
import { useAppState } from '../state/AppState.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { stringWidth } from '../ink/stringWidth.js';
import { getDefaultCharacters, type SpinnerMode } from './Spinner/index.js';
import { SpinnerAnimationRow } from './Spinner/SpinnerAnimationRow.js';
import { useSettings } from '../hooks/useSettings.js';
import { isInProcessTeammateTask } from '../tasks/InProcessTeammateTask/types.js';
import { isBackgroundTask } from '../tasks/types.js';
import { getAllInProcessTeammateTasks } from '../tasks/InProcessTeammateTask/InProcessTeammateTask.js';
import { getEffortSuffix } from '../utils/effort.js';
import { getMainLoopModel } from '../utils/model/model.js';
import { getViewedTeammateTask } from '../state/selectors.js';
import { TEARDROP_ASTERISK } from '../constants/figures.js';
import figures from 'figures';
import { getCurrentTurnTokenBudget, getTurnOutputTokens } from '../bootstrap/state.js';
import { TeammateSpinnerTree } from './Spinner/TeammateSpinnerTree.js';
import { useAnimationFrame } from '../ink.js';
import { getGlobalConfig } from '../utils/config.js';
export type { SpinnerMode } from './Spinner/index.js';
const DEFAULT_CHARACTERS = getDefaultCharacters();
const SPINNER_FRAMES = [...DEFAULT_CHARACTERS, ...[...DEFAULT_CHARACTERS].reverse()];
type Props = {
  mode: SpinnerMode;
  loadingStartTimeRef: React.RefObject<number>;
  totalPausedMsRef: React.RefObject<number>;
  pauseStartTimeRef: React.RefObject<number | null>;
  spinnerTip?: string;
  responseLengthRef: React.RefObject<number>;
  overrideColor?: keyof Theme | null;
  overrideShimmerColor?: keyof Theme | null;

```

---


### `src/components/Stats.tsx`

**信息:**
- 行数: 1228
- 大小: 152782 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import { plot as asciichart } from 'asciichart';
import chalk from 'chalk';
import figures from 'figures';
import React, { Suspense, use, useCallback, useEffect, useMemo, useState } from 'react';
import stripAnsi from 'strip-ansi';
import type { CommandResultDisplay } from '../commands.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { applyColor } from '../ink/colorize.js';
import { stringWidth as getStringWidth } from '../ink/stringWidth.js';
import type { Color } from '../ink/styles.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- raw j/k/arrow stats navigation
import { Ansi, Box, Text, useInput } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { getGlobalConfig } from '../utils/config.js';
import { formatDuration, formatNumber } from '../utils/format.js';
import { generateHeatmap } from '../utils/heatmap.js';
import { renderModelName } from '../utils/model/model.js';
import { copyAnsiToClipboard } from '../utils/screenshotClipboard.js';
import { aggregateClaudeCodeStatsForRange, type ClaudeCodeStats, type DailyModelTokens, type StatsDateRange } from '../utils/stats.js';
import { resolveThemeSetting } from '../utils/systemTheme.js';
import { getTheme, themeColorToAnsi } from '../utils/theme.js';
import { Pane } from './design-system/Pane.js';
import { Tab, Tabs, useTabHeaderFocus } from './design-system/Tabs.js';
import { Spinner } from './Spinner.js';
function formatPeakDay(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  });
}
type Props = {
  onClose: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
type StatsResult = {
  type: 'success';
  data: ClaudeCodeStats;
} | {
  type: 'error';
  message: string;
} | {
  type: 'empty';
};
const DATE_RANGE_LABELS: Record<StatsDateRange, string> = {
  '7d': 'Last 7 days',
  '30d': 'Last 30 days',

```

---


### `src/components/StatusLine.tsx`

**信息:**
- 行数: 324
- 大小: 49465 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import * as React from 'react';
import { memo, useCallback, useEffect, useRef } from 'react';
import { logEvent } from 'src/services/analytics/index.js';
import { useAppState, useSetAppState } from 'src/state/AppState.js';
import type { PermissionMode } from 'src/utils/permissions/PermissionMode.js';
import { getIsRemoteMode, getKairosActive, getMainThreadAgentType, getOriginalCwd, getSdkBetas, getSessionId } from '../bootstrap/state.js';
import { DEFAULT_OUTPUT_STYLE_NAME } from '../constants/outputStyles.js';
import { useNotifications } from '../context/notifications.js';
import { getTotalAPIDuration, getTotalCost, getTotalDuration, getTotalInputTokens, getTotalLinesAdded, getTotalLinesRemoved, getTotalOutputTokens } from '../cost-tracker.js';
import { useMainLoopModel } from '../hooks/useMainLoopModel.js';
import { type ReadonlySettings, useSettings } from '../hooks/useSettings.js';
import { Ansi, Box, Text } from '../ink.js';
import { getRawUtilization } from '../services/claudeAiLimits.js';
import type { Message } from '../types/message.js';
import type { StatusLineCommandInput } from '../types/statusLine.js';
import type { VimMode } from '../types/textInputTypes.js';
import { checkHasTrustDialogAccepted } from '../utils/config.js';
import { calculateContextPercentages, getContextWindowForModel } from '../utils/context.js';
import { getCwd } from '../utils/cwd.js';
import { logForDebugging } from '../utils/debug.js';
import { isFullscreenEnvEnabled } from '../utils/fullscreen.js';
import { createBaseHookInput, executeStatusLineCommand } from '../utils/hooks.js';
import { getLastAssistantMessage } from '../utils/messages.js';
import { getRuntimeMainLoopModel, type ModelName, renderModelName } from '../utils/model/model.js';
import { getCurrentSessionTitle } from '../utils/sessionStorage.js';
import { doesMostRecentAssistantMessageExceed200k, getCurrentUsage } from '../utils/tokens.js';
import { getCurrentWorktreeSession } from '../utils/worktree.js';
import { isVimModeEnabled } from './PromptInput/utils.js';
export function statusLineShouldDisplay(settings: ReadonlySettings): boolean {
  // Assistant mode: statusline fields (model, permission mode, cwd) reflect the
  // REPL/daemon process, not what the agent child is actually running. Hide it.
  if (feature('KAIROS') && getKairosActive()) return false;
  return settings?.statusLine !== undefined;
}
function buildStatusLineCommandInput(permissionMode: PermissionMode, exceeds200kTokens: boolean, settings: ReadonlySettings, messages: Message[], addedDirs: string[], mainLoopModel: ModelName, vimMode?: VimMode): StatusLineCommandInput {
  const agentType = getMainThreadAgentType();
  const worktreeSession = getCurrentWorktreeSession();
  const runtimeModel = getRuntimeMainLoopModel({
    permissionMode,
    mainLoopModel,
    exceeds200kTokens
  });
  const outputStyleName = settings?.outputStyle || DEFAULT_OUTPUT_STYLE_NAME;
  const currentUsage = getCurrentUsage(messages);
  const contextWindowSize = getContextWindowForModel(runtimeModel, getSdkBetas());
  const contextPercentages = calculateContextPercentages(currentUsage, contextWindowSize);
  const sessionId = getSessionId();
  const sessionName = getCurrentSessionTitle(sessionId);
  const rawUtil = getRawUtilization();

```

---


### `src/components/StatusNotices.tsx`

**信息:**
- 行数: 55
- 大小: 5694 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { use } from 'react';
import { Box } from '../ink.js';
import type { AgentDefinitionsResult } from '../tools/AgentTool/loadAgentsDir.js';
import { getMemoryFiles } from '../utils/claudemd.js';
import { getGlobalConfig } from '../utils/config.js';
import { getActiveNotices, type StatusNoticeContext } from '../utils/statusNoticeDefinitions.js';
type Props = {
  agentDefinitions?: AgentDefinitionsResult;
};

/**
 * StatusNotices contains the information displayed to users at startup. We have
 * moved neutral or positive status to src/components/Status.tsx instead, which
 * users can access through /status.
 */
export function StatusNotices(t0) {
  const $ = _c(4);
  const {
    agentDefinitions
  } = t0 === undefined ? {} : t0;
  const t1 = getGlobalConfig();
  let t2;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = getMemoryFiles();
    $[0] = t2;
  } else {
    t2 = $[0];
  }
  const context = {
    config: t1,
    agentDefinitions,
    memoryFiles: use(t2)
  };
  const activeNotices = getActiveNotices(context);
  if (activeNotices.length === 0) {
    return null;
  }
  const T0 = Box;
  const t3 = "column";
  const t4 = 1;
  const t5 = activeNotices.map(notice => <React.Fragment key={notice.id}>{notice.render(context)}</React.Fragment>);
  let t6;
  if ($[1] !== T0 || $[2] !== t5) {
    t6 = <T0 flexDirection={t3} paddingLeft={t4}>{t5}</T0>;
    $[1] = T0;
    $[2] = t5;
    $[3] = t6;
  } else {

```

---


### `src/components/StructuredDiff/Fallback.tsx`

**信息:**
- 行数: 487
- 大小: 56579 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { diffWordsWithSpace, type StructuredPatchHunk } from 'diff';
import * as React from 'react';
import { useMemo } from 'react';
import type { ThemeName } from 'src/utils/theme.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { Box, NoSelect, Text, useTheme, wrapText } from '../../ink.js';

/*
 * StructuredDiffFallback Component: Word-Level Diff Highlighting Example
 *
 * This component shows diff changes with word-level highlighting. Here's a walkthrough:
 *
 * Example:
 * ```
 * // Original code
 * function oldName(param) {
 *   return param.oldProperty;
 * }
 *
 * // Changed code
 * function newName(param) {
 *   return param.newProperty;
 * }
 * ```
 *
 * Processing flow:
 * 1. Component receives a patch with lines including '+' and '-' prefixes
 * 2. Lines are transformed into objects with type (add/remove/nochange)
 * 3. Related add/remove lines are paired (e.g., oldName with newName)
 * 4. Word-level diffing identifies specific changed parts:
 *    [
 *      { value: 'function ', added: undefined, removed: undefined },  // Common
 *      { value: 'oldName', removed: true },                           // Removed
 *      { value: 'newName', added: true },                             // Added
 *      { value: '(param) {', added: undefined, removed: undefined }   // Common
 *    ]
 * 5. Renders with enhanced highlighting:
 *    - Common parts are shown normally
 *    - Removed words get a darker red background
 *    - Added words get a darker green background
 *
 * This produces a visually clear diff where users can see exactly which words
 * changed rather than just which lines were modified.
 */

// Define DiffLine interface to be used throughout the file
interface DiffLine {
  code: string;
  type: 'add' | 'remove' | 'nochange';

```

---


### `src/components/StructuredDiff/colorDiff.ts`

**信息:**
- 行数: 37
- 大小: 1137 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  ColorDiff,
  ColorFile,
  getSyntaxTheme as nativeGetSyntaxTheme,
  type SyntaxTheme,
} from 'color-diff-napi'
import { isEnvDefinedFalsy } from '../../utils/envUtils.js'

export type ColorModuleUnavailableReason = 'env'

/**
 * Returns a static reason why the color-diff module is unavailable, or null if available.
 * 'env' = disabled via CLAUDE_CODE_SYNTAX_HIGHLIGHT
 *
 * The TS port of color-diff works in all build modes, so the only way to
 * disable it is via the env var.
 */
export function getColorModuleUnavailableReason(): ColorModuleUnavailableReason | null {
  if (isEnvDefinedFalsy(process.env.CLAUDE_CODE_SYNTAX_HIGHLIGHT)) {
    return 'env'
  }
  return null
}

export function expectColorDiff(): typeof ColorDiff | null {
  return getColorModuleUnavailableReason() === null ? ColorDiff : null
}

export function expectColorFile(): typeof ColorFile | null {
  return getColorModuleUnavailableReason() === null ? ColorFile : null
}

export function getSyntaxTheme(themeName: string): SyntaxTheme | null {
  return getColorModuleUnavailableReason() === null
    ? nativeGetSyntaxTheme(themeName)
    : null
}

```

---


### `src/components/StructuredDiff.tsx`

**信息:**
- 行数: 190
- 大小: 25007 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { StructuredPatchHunk } from 'diff';
import * as React from 'react';
import { memo } from 'react';
import { useSettings } from '../hooks/useSettings.js';
import { Box, NoSelect, RawAnsi, useTheme } from '../ink.js';
import { isFullscreenEnvEnabled } from '../utils/fullscreen.js';
import sliceAnsi from '../utils/sliceAnsi.js';
import { expectColorDiff } from './StructuredDiff/colorDiff.js';
import { StructuredDiffFallback } from './StructuredDiff/Fallback.js';
type Props = {
  patch: StructuredPatchHunk;
  dim: boolean;
  filePath: string; // File path for language detection
  firstLine: string | null; // First line of file for shebang detection
  fileContent?: string; // Full file content for syntax context (multiline strings, etc.)
  width: number;
  skipHighlighting?: boolean; // Skip syntax highlighting
};

// REPL.tsx renders <Messages> at two disjoint tree positions (transcript
// early-return vs prompt-mode nested in FullscreenLayout), so ctrl+o
// unmounts/remounts the entire message tree and React's memo cache is lost.
// Keep both the NAPI result AND the pre-split gutter/content columns at
// module level so the only work on remount is a WeakMap lookup plus two
// <ink-raw-ansi> leaves — not a fresh syntax highlight, nor N sliceAnsi
// calls + 6N Yoga nodes.
//
// PR #21439 (fullscreen default-on) made gutterWidth>0 the default path,
// reactivating the per-line <DiffLine> branch that PR #20378 had bypassed.
// Caching the split here restores the O(1)-leaves-per-diff invariant.
type CachedRender = {
  lines: string[];
  // Two RawAnsi columns replace what was N DiffLine rows. sliceAnsi work
  // moves from per-remount to cold-cache-only; parseToSpans is eliminated
  // entirely (RawAnsi bypasses Ansi parsing).
  gutterWidth: number;
  gutters: string[] | null;
  contents: string[] | null;
};
const RENDER_CACHE = new WeakMap<StructuredPatchHunk, Map<string, CachedRender>>();

// Gutter width matches the Rust module's layout: marker (1) + space +
// right-aligned line number (max_digits) + space. Depends only on patch
// identity (the WeakMap key), so it's cacheable alongside the NAPI output.
function computeGutterWidth(patch: StructuredPatchHunk): number {
  const maxLineNumber = Math.max(patch.oldStart + patch.oldLines - 1, patch.newStart + patch.newLines - 1, 1);
  return maxLineNumber.toString().length + 3; // marker + 2 padding spaces
}
function renderColorDiff(patch: StructuredPatchHunk, firstLine: string | null, filePath: string, fileContent: string | null, theme: string, width: number, dim: boolean, splitGutter: boolean): CachedRender | null {

```

---


### `src/components/StructuredDiffList.tsx`

**信息:**
- 行数: 30
- 大小: 4252 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { StructuredPatchHunk } from 'diff';
import * as React from 'react';
import { Box, NoSelect, Text } from '../ink.js';
import { intersperse } from '../utils/array.js';
import { StructuredDiff } from './StructuredDiff.js';
type Props = {
  hunks: StructuredPatchHunk[];
  dim: boolean;
  width: number;
  filePath: string;
  firstLine: string | null;
  fileContent?: string;
};

/** Renders a list of diff hunks with ellipsis separators between them. */
export function StructuredDiffList({
  hunks,
  dim,
  width,
  filePath,
  firstLine,
  fileContent
}: Props): React.ReactNode {
  return intersperse(hunks.map(hunk => <Box flexDirection="column" key={hunk.newStart}>
        <StructuredDiff patch={hunk} dim={dim} width={width} filePath={filePath} firstLine={firstLine} fileContent={fileContent} />
      </Box>), i => <NoSelect fromLeftEdge key={`ellipsis-${i}`}>
        <Text dimColor>...</Text>
      </NoSelect>);
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJTdHJ1Y3R1cmVkUGF0Y2hIdW5rIiwiUmVhY3QiLCJCb3giLCJOb1NlbGVjdCIsIlRleHQiLCJpbnRlcnNwZXJzZSIsIlN0cnVjdHVyZWREaWZmIiwiUHJvcHMiLCJodW5rcyIsImRpbSIsIndpZHRoIiwiZmlsZVBhdGgiLCJmaXJzdExpbmUiLCJmaWxlQ29udGVudCIsIlN0cnVjdHVyZWREaWZmTGlzdCIsIlJlYWN0Tm9kZSIsIm1hcCIsImh1bmsiLCJuZXdTdGFydCIsImkiXSwic291cmNlcyI6WyJTdHJ1Y3R1cmVkRGlmZkxpc3QudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB0eXBlIHsgU3RydWN0dXJlZFBhdGNoSHVuayB9IGZyb20gJ2RpZmYnXG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IEJveCwgTm9TZWxlY3QsIFRleHQgfSBmcm9tICcuLi9pbmsuanMnXG5pbXBvcnQgeyBpbnRlcnNwZXJzZSB9IGZyb20gJy4uL3V0aWxzL2FycmF5LmpzJ1xuaW1wb3J0IHsgU3RydWN0dXJlZERpZmYgfSBmcm9tICcuL1N0cnVjdHVyZWREaWZmLmpzJ1xuXG50eXBlIFByb3BzID0ge1xuICBodW5rczogU3RydWN0dXJlZFBhdGNoSHVua1tdXG4gIGRpbTogYm9vbGVhblxuICB3aWR0aDogbnVtYmVyXG4gIGZpbGVQYXRoOiBzdHJpbmdcbiAgZmlyc3RMaW5lOiBzdHJpbmcgfCBudWxsXG4gIGZpbGVDb250ZW50Pzogc3RyaW5nXG59XG5cbi8qKiBSZW5kZXJzIGEgbGlzdCBvZiBkaWZmIGh1bmtzIHdpdGggZWxsaXBzaXMgc2VwYXJhdG9ycyBiZXR3ZWVuIHRoZW0uICovXG5leHBvcnQgZnVuY3Rpb24gU3RydWN0dXJlZERpZmZMaXN0KHtcbiAgaHVua3MsXG4gIGRpbSxcbiAgd2lkdGgsXG4gIGZpbGVQYXRoLFxuICBmaXJzdExpbmUsXG4gIGZpbGVDb250ZW50LFxufTogUHJvcHMpOiBSZWFjdC5SZWFjdE5vZGUge1xuICByZXR1cm4gaW50ZXJzcGVyc2UoXG4gICAgaHVua3MubWFwKGh1bmsgPT4gKFxuICAgICAgPEJveCBmbGV4RGlyZWN0aW9uPVwiY29sdW1uXCIga2V5PXtodW5rLm5ld1N0YXJ0fT5cbiAgICAgICAgPFN0cnVjdHVyZWREaWZmXG4gICAgICAgICAgcGF0Y2g9e2h1bmt9XG4gICAgICAgICAgZGltPXtkaW19XG4gICAgICAgICAgd2lkdGg9e3dpZHRofVxuICAgICAgICAgIGZpbGVQYXRoPXtmaWxlUGF0aH1cbiAgICAgICAgICBmaXJzdExpbmU9e2ZpcnN0TGluZX1cbiAgICAgICAgICBmaWxlQ29udGVudD17ZmlsZUNvbnRlbnR9XG4gICAgICAgIC8+XG4gICAgICA8L0JveD5cbiAgICApKSxcbiAgICBpID0+IChcbiAgICAgIDxOb1NlbGVjdCBmcm9tTGVmdEVkZ2Uga2V5PXtgZWxsaXBzaXMtJHtpfWB9PlxuICAgICAgICA8VGV4dCBkaW1Db2xvcj4uLi48L1RleHQ+XG4gICAgICA8L05vU2VsZWN0PlxuICAgICksXG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsY0FBY0EsbUJBQW1CLFFBQVEsTUFBTTtBQUMvQyxPQUFPLEtBQUtDLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLEdBQUcsRUFBRUMsUUFBUSxFQUFFQyxJQUFJLFFBQVEsV0FBVztBQUMvQyxTQUFTQyxXQUFXLFFBQVEsbUJBQW1CO0FBQy9DLFNBQVNDLGNBQWMsUUFBUSxxQkFBcUI7QUFFcEQsS0FBS0MsS0FBSyxHQUFHO0VBQ1hDLEtBQUssRUFBRVIsbUJBQW1CLEVBQUU7RUFDNUJTLEdBQUcsRUFBRSxPQUFPO0VBQ1pDLEtBQUssRUFBRSxNQUFNO0VBQ2JDLFFBQVEsRUFBRSxNQUFNO0VBQ2hCQyxTQUFTLEVBQUUsTUFBTSxHQUFHLElBQUk7RUFDeEJDLFdBQVcsQ0FBQyxFQUFFLE1BQU07QUFDdEIsQ0FBQzs7QUFFRDtBQUNBLE9BQU8sU0FBU0Msa0JBQWtCQSxDQUFDO0VBQ2pDTixLQUFLO0VBQ0xDLEdBQUc7RUFDSEMsS0FBSztFQUNMQyxRQUFRO0VBQ1JDLFNBQVM7RUFDVEM7QUFDSyxDQUFOLEVBQUVOLEtBQUssQ0FBQyxFQUFFTixLQUFLLENBQUNjLFNBQVMsQ0FBQztFQUN6QixPQUFPVixXQUFXLENBQ2hCRyxLQUFLLENBQUNRLEdBQUcsQ0FBQ0MsSUFBSSxJQUNaLENBQUMsR0FBRyxDQUFDLGFBQWEsQ0FBQyxRQUFRLENBQUMsR0FBRyxDQUFDLENBQUNBLElBQUksQ0FBQ0MsUUFBUSxDQUFDO0FBQ3JELFFBQVEsQ0FBQyxjQUFjLENBQ2IsS0FBSyxDQUFDLENBQUNELElBQUksQ0FBQyxDQUNaLEdBQUcsQ0FBQyxDQUFDUixHQUFHLENBQUMsQ0FDVCxLQUFLLENBQUMsQ0FBQ0MsS0FBSyxDQUFDLENBQ2IsUUFBUSxDQUFDLENBQUNDLFFBQVEsQ0FBQyxDQUNuQixTQUFTLENBQUMsQ0FBQ0MsU0FBUyxDQUFDLENBQ3JCLFdBQVcsQ0FBQyxDQUFDQyxXQUFXLENBQUM7QUFFbkMsTUFBTSxFQUFFLEdBQUcsQ0FDTixDQUFDLEVBQ0ZNLENBQUMsSUFDQyxDQUFDLFFBQVEsQ0FBQyxZQUFZLENBQUMsR0FBRyxDQUFDLENBQUMsWUFBWUEsQ0FBQyxFQUFFLENBQUM7QUFDbEQsUUFBUSxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsR0FBRyxFQUFFLElBQUk7QUFDaEMsTUFBTSxFQUFFLFFBQVEsQ0FFZCxDQUFDO0FBQ0giLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/components/TagTabs.tsx`

**信息:**
- 行数: 139
- 大小: 20853 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { stringWidth } from '../ink/stringWidth.js';
import { Box, Text } from '../ink.js';
import { truncateToWidth } from '../utils/format.js';

// Constants for width calculations - derived from actual rendered strings
const ALL_TAB_LABEL = 'All';
const TAB_PADDING = 2; // Space before and after tab text: " {tab} "
const HASH_PREFIX_LENGTH = 1; // "#" prefix for non-All tabs
const LEFT_ARROW_PREFIX = '← ';
const RIGHT_HINT_WITH_COUNT_PREFIX = '→';
const RIGHT_HINT_SUFFIX = ' (tab to cycle)';
const RIGHT_HINT_NO_COUNT = '(tab to cycle)';
const MAX_OVERFLOW_DIGITS = 2; // Assume max 99 hidden tabs for width calculation

// Computed widths
const LEFT_ARROW_WIDTH = LEFT_ARROW_PREFIX.length + MAX_OVERFLOW_DIGITS + 1; // "← NN " with gap
const RIGHT_HINT_WIDTH_WITH_COUNT = RIGHT_HINT_WITH_COUNT_PREFIX.length + MAX_OVERFLOW_DIGITS + RIGHT_HINT_SUFFIX.length; // "→NN (tab to cycle)"
const RIGHT_HINT_WIDTH_NO_COUNT = RIGHT_HINT_NO_COUNT.length;
type Props = {
  tabs: string[];
  selectedIndex: number;
  availableWidth: number;
  showAllProjects?: boolean;
};

/**
 * Calculate the display width of a tab
 */
function getTabWidth(tab: string, maxWidth?: number): number {
  if (tab === ALL_TAB_LABEL) {
    return ALL_TAB_LABEL.length + TAB_PADDING;
  }
  // For non-All tabs: " #{tag} " but truncate tag if needed
  const tagWidth = stringWidth(tab);
  const effectiveTagWidth = maxWidth ? Math.min(tagWidth, maxWidth - TAB_PADDING - HASH_PREFIX_LENGTH) : tagWidth;
  return Math.max(0, effectiveTagWidth) + TAB_PADDING + HASH_PREFIX_LENGTH;
}

/**
 * Truncate a tag to fit within maxWidth, accounting for padding and hash prefix
 */
function truncateTag(tag: string, maxWidth: number): string {
  // Available space for the tag text itself: maxWidth - " #" - " "
  const availableForTag = maxWidth - TAB_PADDING - HASH_PREFIX_LENGTH;
  if (stringWidth(tag) <= availableForTag) {
    return tag;
  }
  if (availableForTag <= 1) {
    return tag.charAt(0);

```

---


### `src/components/TaskListV2.tsx`

**信息:**
- 行数: 378
- 大小: 50200 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { stringWidth } from '../ink/stringWidth.js';
import { Box, Text } from '../ink.js';
import { useAppState } from '../state/AppState.js';
import { isInProcessTeammateTask } from '../tasks/InProcessTeammateTask/types.js';
import { AGENT_COLOR_TO_THEME_COLOR, type AgentColorName } from '../tools/AgentTool/agentColorManager.js';
import { isAgentSwarmsEnabled } from '../utils/agentSwarmsEnabled.js';
import { count } from '../utils/array.js';
import { summarizeRecentActivities } from '../utils/collapseReadSearch.js';
import { truncateToWidth } from '../utils/format.js';
import { isTodoV2Enabled, type Task } from '../utils/tasks.js';
import type { Theme } from '../utils/theme.js';
import ThemedText from './design-system/ThemedText.js';
type Props = {
  tasks: Task[];
  isStandalone?: boolean;
};
const RECENT_COMPLETED_TTL_MS = 30_000;
function byIdAsc(a: Task, b: Task): number {
  const aNum = parseInt(a.id, 10);
  const bNum = parseInt(b.id, 10);
  if (!isNaN(aNum) && !isNaN(bNum)) {
    return aNum - bNum;
  }
  return a.id.localeCompare(b.id);
}
export function TaskListV2({
  tasks,
  isStandalone = false
}: Props): React.ReactNode {
  const teamContext = useAppState(s => s.teamContext);
  const appStateTasks = useAppState(s_0 => s_0.tasks);
  const [, forceUpdate] = React.useState(0);
  const {
    rows,
    columns
  } = useTerminalSize();

  // Track when each task was last observed transitioning to completed
  const completionTimestampsRef = React.useRef(new Map<string, number>());
  const previousCompletedIdsRef = React.useRef<Set<string> | null>(null);
  if (previousCompletedIdsRef.current === null) {
    previousCompletedIdsRef.current = new Set(tasks.filter(t => t.status === 'completed').map(t_0 => t_0.id));
  }
  const maxDisplay = rows <= 10 ? 0 : Math.min(10, Math.max(3, rows - 14));

  // Update completion timestamps: reset when a task transitions to completed

```

---


### `src/components/TeammateViewHeader.tsx`

**信息:**
- 行数: 82
- 大小: 7415 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../ink.js';
import { useAppState } from '../state/AppState.js';
import { getViewedTeammateTask } from '../state/selectors.js';
import { toInkColor } from '../utils/ink.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import { OffscreenFreeze } from './OffscreenFreeze.js';

/**
 * Header shown when viewing a teammate's transcript.
 * Displays teammate name (colored), task description, and exit hint.
 */
export function TeammateViewHeader() {
  const $ = _c(14);
  const viewedTeammate = useAppState(_temp);
  if (!viewedTeammate) {
    return null;
  }
  let t0;
  if ($[0] !== viewedTeammate.identity.color) {
    t0 = toInkColor(viewedTeammate.identity.color);
    $[0] = viewedTeammate.identity.color;
    $[1] = t0;
  } else {
    t0 = $[1];
  }
  const nameColor = t0;
  let t1;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Text>Viewing </Text>;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  let t2;
  if ($[3] !== nameColor || $[4] !== viewedTeammate.identity.agentName) {
    t2 = <Text color={nameColor} bold={true}>@{viewedTeammate.identity.agentName}</Text>;
    $[3] = nameColor;
    $[4] = viewedTeammate.identity.agentName;
    $[5] = t2;
  } else {
    t2 = $[5];
  }
  let t3;
  if ($[6] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = <Text dimColor={true}>{" \xB7 "}<KeyboardShortcutHint shortcut="esc" action="return" /></Text>;
    $[6] = t3;
  } else {
    t3 = $[6];

```

---


### `src/components/TeleportError.tsx`

**信息:**
- 行数: 189
- 大小: 18824 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useEffect, useState } from 'react';
import { checkIsGitClean, checkNeedsClaudeAiLogin } from 'src/utils/background/remote/preconditions.js';
import { gracefulShutdownSync } from 'src/utils/gracefulShutdown.js';
import { Box, Text } from '../ink.js';
import { ConsoleOAuthFlow } from './ConsoleOAuthFlow.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
import { TeleportStash } from './TeleportStash.js';
export type TeleportLocalErrorType = 'needsLogin' | 'needsGitStash';
type TeleportErrorProps = {
  onComplete: () => void;
  errorsToIgnore?: ReadonlySet<TeleportLocalErrorType>;
};

// Module-level sentinel so the default parameter has stable identity.
// Previously `= new Set()` created a fresh Set every render, which put
// a new object in checkErrors' deps and caused the mount effect to
// re-fire on every render.
const EMPTY_ERRORS_TO_IGNORE: ReadonlySet<TeleportLocalErrorType> = new Set();
export function TeleportError(t0) {
  const $ = _c(18);
  const {
    onComplete,
    errorsToIgnore: t1
  } = t0;
  const errorsToIgnore = t1 === undefined ? EMPTY_ERRORS_TO_IGNORE : t1;
  const [currentError, setCurrentError] = useState(null);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  let t2;
  if ($[0] !== errorsToIgnore || $[1] !== onComplete) {
    t2 = async () => {
      const currentErrors = await getTeleportErrors();
      const filteredErrors = new Set(Array.from(currentErrors).filter(error => !errorsToIgnore.has(error)));
      if (filteredErrors.size === 0) {
        onComplete();
        return;
      }
      if (filteredErrors.has("needsLogin")) {
        setCurrentError("needsLogin");
      } else {
        if (filteredErrors.has("needsGitStash")) {
          setCurrentError("needsGitStash");
        }
      }
    };
    $[0] = errorsToIgnore;
    $[1] = onComplete;
    $[2] = t2;
  } else {

```

---


### `src/components/TeleportProgress.tsx`

**信息:**
- 行数: 140
- 大小: 16142 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useState } from 'react';
import type { Root } from '../ink.js';
import { Box, Text, useAnimationFrame } from '../ink.js';
import { AppStateProvider } from '../state/AppState.js';
import { checkOutTeleportedSessionBranch, processMessagesForTeleportResume, type TeleportProgressStep, type TeleportResult, teleportResumeCodeSession } from '../utils/teleport.js';
type Props = {
  currentStep: TeleportProgressStep;
  sessionId?: string;
};
const SPINNER_FRAMES = ['◐', '◓', '◑', '◒'];
const STEPS: {
  key: TeleportProgressStep;
  label: string;
}[] = [{
  key: 'validating',
  label: 'Validating session'
}, {
  key: 'fetching_logs',
  label: 'Fetching session logs'
}, {
  key: 'fetching_branch',
  label: 'Getting branch info'
}, {
  key: 'checking_out',
  label: 'Checking out branch'
}];
export function TeleportProgress(t0) {
  const $ = _c(16);
  const {
    currentStep,
    sessionId
  } = t0;
  const [ref, time] = useAnimationFrame(100);
  const frame = Math.floor(time / 100) % SPINNER_FRAMES.length;
  let t1;
  if ($[0] !== currentStep) {
    t1 = s => s.key === currentStep;
    $[0] = currentStep;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const currentStepIndex = STEPS.findIndex(t1);
  const t2 = SPINNER_FRAMES[frame];
  let t3;
  if ($[2] !== t2) {
    t3 = <Box marginBottom={1}><Text bold={true} color="claude">{t2} Teleporting session…</Text></Box>;

```

---


### `src/components/TeleportRepoMismatchDialog.tsx`

**信息:**
- 行数: 104
- 大小: 13046 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useState } from 'react';
import { Box, Text } from '../ink.js';
import { getDisplayPath } from '../utils/file.js';
import { removePathFromRepo, validateRepoAtPath } from '../utils/githubRepoPathMapping.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
import { Spinner } from './Spinner.js';
type Props = {
  targetRepo: string;
  initialPaths: string[];
  onSelectPath: (path: string) => void;
  onCancel: () => void;
};
export function TeleportRepoMismatchDialog(t0) {
  const $ = _c(18);
  const {
    targetRepo,
    initialPaths,
    onSelectPath,
    onCancel
  } = t0;
  const [availablePaths, setAvailablePaths] = useState(initialPaths);
  const [errorMessage, setErrorMessage] = useState(null);
  const [validating, setValidating] = useState(false);
  let t1;
  if ($[0] !== availablePaths || $[1] !== onCancel || $[2] !== onSelectPath || $[3] !== targetRepo) {
    t1 = async value => {
      if (value === "cancel") {
        onCancel();
        return;
      }
      setValidating(true);
      setErrorMessage(null);
      const isValid = await validateRepoAtPath(value, targetRepo);
      if (isValid) {
        onSelectPath(value);
        return;
      }
      removePathFromRepo(targetRepo, value);
      const updatedPaths = availablePaths.filter(p => p !== value);
      setAvailablePaths(updatedPaths);
      setValidating(false);
      setErrorMessage(`${getDisplayPath(value)} no longer contains the correct repository. Select another path.`);
    };
    $[0] = availablePaths;
    $[1] = onCancel;
    $[2] = onSelectPath;
    $[3] = targetRepo;
    $[4] = t1;

```

---


### `src/components/TeleportResumeWrapper.tsx`

**信息:**
- 行数: 167
- 大小: 15381 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useEffect } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import type { TeleportRemoteResponse } from 'src/utils/conversationRecovery.js';
import type { CodeSession } from 'src/utils/teleport/api.js';
import { type TeleportSource, useTeleportResume } from '../hooks/useTeleportResume.js';
import { Box, Text } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { ResumeTask } from './ResumeTask.js';
import { Spinner } from './Spinner.js';
interface TeleportResumeWrapperProps {
  onComplete: (result: TeleportRemoteResponse) => void;
  onCancel: () => void;
  onError?: (error: string, formattedMessage?: string) => void;
  isEmbedded?: boolean;
  source: TeleportSource;
}

/**
 * Wrapper component that manages the full teleport resume flow,
 * including session selection, loading state, and error handling
 */
export function TeleportResumeWrapper(t0) {
  const $ = _c(25);
  const {
    onComplete,
    onCancel,
    onError,
    isEmbedded: t1,
    source
  } = t0;
  const isEmbedded = t1 === undefined ? false : t1;
  const {
    resumeSession,
    isResuming,
    error,
    selectedSession
  } = useTeleportResume(source);
  let t2;
  let t3;
  if ($[0] !== source) {
    t2 = () => {
      logEvent("tengu_teleport_started", {
        source: source as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS
      });
    };
    t3 = [source];
    $[0] = source;
    $[1] = t2;
    $[2] = t3;

```

---


### `src/components/TeleportStash.tsx`

**信息:**
- 行数: 116
- 大小: 15582 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import figures from 'figures';
import React, { useEffect, useState } from 'react';
import { Box, Text } from '../ink.js';
import { logForDebugging } from '../utils/debug.js';
import type { GitFileStatus } from '../utils/git.js';
import { getFileStatus, stashToCleanState } from '../utils/git.js';
import { Select } from './CustomSelect/index.js';
import { Dialog } from './design-system/Dialog.js';
import { Spinner } from './Spinner.js';
type TeleportStashProps = {
  onStashAndContinue: () => void;
  onCancel: () => void;
};
export function TeleportStash({
  onStashAndContinue,
  onCancel
}: TeleportStashProps): React.ReactNode {
  const [gitFileStatus, setGitFileStatus] = useState<GitFileStatus | null>(null);
  const changedFiles = gitFileStatus !== null ? [...gitFileStatus.tracked, ...gitFileStatus.untracked] : [];
  const [loading, setLoading] = useState(true);
  const [stashing, setStashing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load changed files on mount
  useEffect(() => {
    const loadChangedFiles = async () => {
      try {
        const fileStatus = await getFileStatus();
        setGitFileStatus(fileStatus);
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : String(err);
        logForDebugging(`Error getting changed files: ${errorMessage}`, {
          level: 'error'
        });
        setError('Failed to get changed files');
      } finally {
        setLoading(false);
      }
    };
    void loadChangedFiles();
  }, []);
  const handleStash = async () => {
    setStashing(true);
    try {
      logForDebugging('Stashing changes before teleport...');
      const success = await stashToCleanState('Teleport auto-stash');
      if (success) {
        logForDebugging('Successfully stashed changes');
        onStashAndContinue();
      } else {

```

---


### `src/components/TextInput.tsx`

**信息:**
- 行数: 124
- 大小: 20998 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import chalk from 'chalk';
import React, { useMemo, useRef } from 'react';
import { useVoiceState } from '../context/voice.js';
import { useClipboardImageHint } from '../hooks/useClipboardImageHint.js';
import { useSettings } from '../hooks/useSettings.js';
import { useTextInput } from '../hooks/useTextInput.js';
import { Box, color, useAnimationFrame, useTerminalFocus, useTheme } from '../ink.js';
import type { BaseTextInputProps } from '../types/textInputTypes.js';
import { isEnvTruthy } from '../utils/envUtils.js';
import type { TextHighlight } from '../utils/textHighlighting.js';
import { BaseTextInput } from './BaseTextInput.js';
import { hueToRgb } from './Spinner/utils.js';

// Block characters for waveform bars: space (silent) + 8 rising block elements.
const BARS = ' \u2581\u2582\u2583\u2584\u2585\u2586\u2587\u2588';

// Mini waveform cursor width
const CURSOR_WAVEFORM_WIDTH = 1;

// Smoothing factor (0 = instant, 1 = frozen). Applied as EMA to
// smooth both rises and falls for a steady, non-jittery bar.
const SMOOTH = 0.7;

// Boost factor for audio levels — computeLevel normalizes with a
// conservative divisor (rms/2000), so normal speech sits around
// 0.3-0.5. This multiplier lets the bar use the full range.
const LEVEL_BOOST = 1.8;

// Raw audio level threshold (pre-boost) below which the cursor is
// grey. computeLevel returns sqrt(rms/2000), so ambient mic noise
// typically sits at 0.05-0.15. Speech starts around 0.2+.
const SILENCE_THRESHOLD = 0.15;
export type Props = BaseTextInputProps & {
  highlights?: TextHighlight[];
};
export default function TextInput(props: Props): React.ReactNode {
  const [theme] = useTheme();
  const isTerminalFocused = useTerminalFocus();
  // Hoisted to mount-time — this component re-renders on every keystroke.
  const accessibilityEnabled = useMemo(() => isEnvTruthy(process.env.CLAUDE_CODE_ACCESSIBILITY), []);
  const settings = useSettings();
  const reducedMotion = settings.prefersReducedMotion ?? false;
  const voiceState = feature('VOICE_MODE') ?
  // biome-ignore lint/correctness/useHookAtTopLevel: feature() is a compile-time constant
  useVoiceState(s => s.voiceState) : 'idle' as const;
  const isVoiceRecording = voiceState === 'recording';
  const audioLevels = feature('VOICE_MODE') ?
  // biome-ignore lint/correctness/useHookAtTopLevel: feature() is a compile-time constant
  useVoiceState(s_0 => s_0.voiceAudioLevels) : [];

```

---


### `src/components/ThemePicker.tsx`

**信息:**
- 行数: 333
- 大小: 35662 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import * as React from 'react';
import { useExitOnCtrlCDWithKeybindings } from '../hooks/useExitOnCtrlCDWithKeybindings.js';
import { useTerminalSize } from '../hooks/useTerminalSize.js';
import { Box, Text, usePreviewTheme, useTheme, useThemeSetting } from '../ink.js';
import { useRegisterKeybindingContext } from '../keybindings/KeybindingContext.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { useShortcutDisplay } from '../keybindings/useShortcutDisplay.js';
import { useAppState, useSetAppState } from '../state/AppState.js';
import { gracefulShutdown } from '../utils/gracefulShutdown.js';
import { updateSettingsForSource } from '../utils/settings/settings.js';
import type { ThemeSetting } from '../utils/theme.js';
import { Select } from './CustomSelect/index.js';
import { Byline } from './design-system/Byline.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import { getColorModuleUnavailableReason, getSyntaxTheme } from './StructuredDiff/colorDiff.js';
import { StructuredDiff } from './StructuredDiff.js';
export type ThemePickerProps = {
  onThemeSelect: (setting: ThemeSetting) => void;
  showIntroText?: boolean;
  helpText?: string;
  showHelpTextBelow?: boolean;
  hideEscToCancel?: boolean;
  /** Skip exit handling when running in a context that already has it (e.g., onboarding) */
  skipExitHandling?: boolean;
  /** Called when the user cancels (presses Escape). If skipExitHandling is true and this is provided, it will be called instead of just saving the preview. */
  onCancel?: () => void;
};
export function ThemePicker(t0) {
  const $ = _c(59);
  const {
    onThemeSelect,
    showIntroText: t1,
    helpText: t2,
    showHelpTextBelow: t3,
    hideEscToCancel: t4,
    skipExitHandling: t5,
    onCancel: onCancelProp
  } = t0;
  const showIntroText = t1 === undefined ? false : t1;
  const helpText = t2 === undefined ? "" : t2;
  const showHelpTextBelow = t3 === undefined ? false : t3;
  const hideEscToCancel = t4 === undefined ? false : t4;
  const skipExitHandling = t5 === undefined ? false : t5;
  const [theme] = useTheme();
  const themeSetting = useThemeSetting();
  const {
    columns
  } = useTerminalSize();

```

---


### `src/components/ThinkingToggle.tsx`

**信息:**
- 行数: 153
- 大小: 18209 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useState } from 'react';
import { useExitOnCtrlCDWithKeybindings } from 'src/hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Text } from '../ink.js';
import { useKeybinding } from '../keybindings/useKeybinding.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { Select } from './CustomSelect/index.js';
import { Byline } from './design-system/Byline.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
import { Pane } from './design-system/Pane.js';
export type Props = {
  currentValue: boolean;
  onSelect: (enabled: boolean) => void;
  onCancel?: () => void;
  isMidConversation?: boolean;
};
export function ThinkingToggle(t0) {
  const $ = _c(27);
  const {
    currentValue,
    onSelect,
    onCancel,
    isMidConversation
  } = t0;
  const exitState = useExitOnCtrlCDWithKeybindings();
  const [confirmationPending, setConfirmationPending] = useState(null);
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = [{
      value: "true",
      label: "Enabled",
      description: "Claude will think before responding"
    }, {
      value: "false",
      label: "Disabled",
      description: "Claude will respond without extended thinking"
    }];
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const options = t1;
  let t2;
  if ($[1] !== confirmationPending || $[2] !== onCancel) {
    t2 = () => {
      if (confirmationPending !== null) {
        setConfirmationPending(null);
      } else {
        onCancel?.();

```

---


### `src/components/TokenWarning.tsx`

**信息:**
- 行数: 179
- 大小: 21485 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import * as React from 'react';
import { useSyncExternalStore } from 'react';
import { Box, Text } from '../ink.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js';
import { calculateTokenWarningState, getEffectiveContextWindowSize, isAutoCompactEnabled } from '../services/compact/autoCompact.js';
import { useCompactWarningSuppression } from '../services/compact/compactWarningHook.js';
import { getUpgradeMessage } from '../utils/model/contextWindowUpgradeCheck.js';
type Props = {
  tokenUsage: number;
  model: string;
};

/**
 * Live collapse progress: "x / y summarized". Sub-component so
 * useSyncExternalStore can subscribe to store mutations unconditionally
 * (hooks-in-conditionals would violate React rules). The parent only
 * renders this when feature('CONTEXT_COLLAPSE') + isContextCollapseEnabled().
 */
function CollapseLabel(t0) {
  const $ = _c(8);
  const {
    upgradeMessage
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = require("../services/contextCollapse/index.js");
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const {
    getStats,
    subscribe
  } = t1 as typeof import('../services/contextCollapse/index.js');
  let t2;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = () => {
      const s = getStats();
      const idleWarn = s.health.emptySpawnWarningEmitted ? 1 : 0;
      return `${s.collapsedSpans}|${s.stagedSpans}|${s.health.totalErrors}|${s.health.totalEmptySpawns}|${idleWarn}`;
    };
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  const snapshot = useSyncExternalStore(subscribe, t2);
  let t3;
  if ($[2] !== snapshot) {

```

---


### `src/components/ToolUseLoader.tsx`

**信息:**
- 行数: 42
- 大小: 4843 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { BLACK_CIRCLE } from '../constants/figures.js';
import { useBlink } from '../hooks/useBlink.js';
import { Box, Text } from '../ink.js';
type Props = {
  isError: boolean;
  isUnresolved: boolean;
  shouldAnimate: boolean;
};
export function ToolUseLoader(t0) {
  const $ = _c(7);
  const {
    isError,
    isUnresolved,
    shouldAnimate
  } = t0;
  const [ref, isBlinking] = useBlink(shouldAnimate);
  const color = isUnresolved ? undefined : isError ? "error" : "success";
  const t1 = !shouldAnimate || isBlinking || isError || !isUnresolved ? BLACK_CIRCLE : " ";
  let t2;
  if ($[0] !== color || $[1] !== isUnresolved || $[2] !== t1) {
    t2 = <Text color={color} dimColor={isUnresolved}>{t1}</Text>;
    $[0] = color;
    $[1] = isUnresolved;
    $[2] = t1;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  let t3;
  if ($[4] !== ref || $[5] !== t2) {
    t3 = <Box ref={ref} minWidth={2}>{t2}</Box>;
    $[4] = ref;
    $[5] = t2;
    $[6] = t3;
  } else {
    t3 = $[6];
  }
  return t3;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJMQUNLX0NJUkNMRSIsInVzZUJsaW5rIiwiQm94IiwiVGV4dCIsIlByb3BzIiwiaXNFcnJvciIsImlzVW5yZXNvbHZlZCIsInNob3VsZEFuaW1hdGUiLCJUb29sVXNlTG9hZGVyIiwidDAiLCIkIiwiX2MiLCJyZWYiLCJpc0JsaW5raW5nIiwiY29sb3IiLCJ1bmRlZmluZWQiLCJ0MSIsInQyIiwidDMiXSwic291cmNlcyI6WyJUb29sVXNlTG9hZGVyLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBCTEFDS19DSVJDTEUgfSBmcm9tICcuLi9jb25zdGFudHMvZmlndXJlcy5qcydcbmltcG9ydCB7IHVzZUJsaW5rIH0gZnJvbSAnLi4vaG9va3MvdXNlQmxpbmsuanMnXG5pbXBvcnQgeyBCb3gsIFRleHQgfSBmcm9tICcuLi9pbmsuanMnXG5cbnR5cGUgUHJvcHMgPSB7XG4gIGlzRXJyb3I6IGJvb2xlYW5cbiAgaXNVbnJlc29sdmVkOiBib29sZWFuXG4gIHNob3VsZEFuaW1hdGU6IGJvb2xlYW5cbn1cblxuZXhwb3J0IGZ1bmN0aW9uIFRvb2xVc2VMb2FkZXIoe1xuICBpc0Vycm9yLFxuICBpc1VucmVzb2x2ZWQsXG4gIHNob3VsZEFuaW1hdGUsXG59OiBQcm9wcyk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIGNvbnN0IFtyZWYsIGlzQmxpbmtpbmddID0gdXNlQmxpbmsoc2hvdWxkQW5pbWF0ZSlcblxuICBjb25zdCBjb2xvciA9IGlzVW5yZXNvbHZlZCA/IHVuZGVmaW5lZCA6IGlzRXJyb3IgPyAnZXJyb3InIDogJ3N1Y2Nlc3MnXG5cbiAgLy8gV0FSTklORzogVGhlIGNvZGUgaGVyZSBhbmQgaW4gQXNzaXN0YW50VG9vbFVzZU1lc3NhZ2UgaXMgcGFydGljdWxhcmx5XG4gIC8vIHNlbnNpdGl2ZSB0byB3aGF0ICpzaG91bGQqIGp1c3QgYmUgdHJpdmlhbCByZWZhY3RvcmluZ3MuIEEgYDxkaW0+eDwvZGltPmBcbiAgLy8gZm9sbG93ZWQgKmltbWVkaWF0ZWx5KiBieSBgPGJvbGQ+eTwvYm9sZD5gIHRhZyBpbmNvcnJlY3RseSByZW5kZXJzIGB5YCBhc1xuICAvLyBkaW0hIFRoaXMgaXMgYmVjYXVzZSBgPC9kaW0+YCBhbmQgYDwvYm9sZD5gIGFyZSBib3RoIHJlc2V0IGJ5IFxceDFiWzIybVxuICAvLyBkdWUgdG8gaGlzdG9yaWNhbCByZWFzb25zLCBhbmQgY2hhbGsgY2FuJ3QgZGlzdGluZ3Vpc2ggYmV0d2VlbiB0aGVtLlxuICAvLyBUaGUgc3ltcHRvbSB5b3UnbGwgc2VlIGlmIHdlIGdldCB0aGlzIHdyb25nIGlzIHRoZSB0b29sIG5hbWUgYmxpbmtzIGFsb25nXG4gIC8vIHdpdGggdGhpcyBsb2FkaW5nIGluZGljYXRvciwgd2hpY2ggbG9va3MgcXVpdGUgYmFkLlxuICAvLyBodHRwczovL2dpdGh1Yi5jb20vY2hhbGsvY2hhbGsvaXNzdWVzLzI5MFxuICByZXR1cm4gKFxuICAgIDxCb3ggcmVmPXtyZWZ9IG1pbldpZHRoPXsyfT5cbiAgICAgIDxUZXh0IGNvbG9yPXtjb2xvcn0gZGltQ29sb3I9e2lzVW5yZXNvbHZlZH0+XG4gICAgICAgIHshc2hvdWxkQW5pbWF0ZSB8fCBpc0JsaW5raW5nIHx8IGlzRXJyb3IgfHwgIWlzVW5yZXNvbHZlZFxuICAgICAgICAgID8gQkxBQ0tfQ0lSQ0xFXG4gICAgICAgICAgOiAnICd9XG4gICAgICA8L1RleHQ+XG4gICAgPC9Cb3g+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU9BLEtBQUssTUFBTSxPQUFPO0FBQ3pCLFNBQVNDLFlBQVksUUFBUSx5QkFBeUI7QUFDdEQsU0FBU0MsUUFBUSxRQUFRLHNCQUFzQjtBQUMvQyxTQUFTQyxHQUFHLEVBQUVDLElBQUksUUFBUSxXQUFXO0FBRXJDLEtBQUtDLEtBQUssR0FBRztFQUNYQyxPQUFPLEVBQUUsT0FBTztFQUNoQkMsWUFBWSxFQUFFLE9BQU87RUFDckJDLGFBQWEsRUFBRSxPQUFPO0FBQ3hCLENBQUM7QUFFRCxPQUFPLFNBQUFDLGNBQUFDLEVBQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFBdUI7SUFBQU4sT0FBQTtJQUFBQyxZQUFBO0lBQUFDO0VBQUEsSUFBQUUsRUFJdEI7RUFDTixPQUFBRyxHQUFBLEVBQUFDLFVBQUEsSUFBMEJaLFFBQVEsQ0FBQ00sYUFBYSxDQUFDO0VBRWpELE1BQUFPLEtBQUEsR0FBY1IsWUFBWSxHQUFaUyxTQUF3RCxHQUE3QlYsT0FBTyxHQUFQLE9BQTZCLEdBQTdCLFNBQTZCO0VBYS9ELE1BQUFXLEVBQUEsSUFBQ1QsYUFBMkIsSUFBNUJNLFVBQXVDLElBQXZDUixPQUF3RCxJQUF4RCxDQUE0Q0MsWUFFdEMsR0FGTk4sWUFFTSxHQUZOLEdBRU07RUFBQSxJQUFBaUIsRUFBQTtFQUFBLElBQUFQLENBQUEsUUFBQUksS0FBQSxJQUFBSixDQUFBLFFBQUFKLFlBQUEsSUFBQUksQ0FBQSxRQUFBTSxFQUFBO0lBSFRDLEVBQUEsSUFBQyxJQUFJLENBQVFILEtBQUssQ0FBTEEsTUFBSSxDQUFDLENBQVlSLFFBQVksQ0FBWkEsYUFBVyxDQUFDLENBQ3ZDLENBQUFVLEVBRUssQ0FDUixFQUpDLElBQUksQ0FJRTtJQUFBTixDQUFBLE1BQUFJLEtBQUE7SUFBQUosQ0FBQSxNQUFBSixZQUFBO0lBQUFJLENBQUEsTUFBQU0sRUFBQTtJQUFBTixDQUFBLE1BQUFPLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFQLENBQUE7RUFBQTtFQUFBLElBQUFRLEVBQUE7RUFBQSxJQUFBUixDQUFBLFFBQUFFLEdBQUEsSUFBQUYsQ0FBQSxRQUFBTyxFQUFBO0lBTFRDLEVBQUEsSUFBQyxHQUFHLENBQU1OLEdBQUcsQ0FBSEEsSUFBRSxDQUFDLENBQVksUUFBQyxDQUFELEdBQUMsQ0FDeEIsQ0FBQUssRUFJTSxDQUNSLEVBTkMsR0FBRyxDQU1FO0lBQUFQLENBQUEsTUFBQUUsR0FBQTtJQUFBRixDQUFBLE1BQUFPLEVBQUE7SUFBQVAsQ0FBQSxNQUFBUSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBUixDQUFBO0VBQUE7RUFBQSxPQU5OUSxFQU1NO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/components/TrustDialog/TrustDialog.tsx`

**信息:**
- 行数: 290
- 大小: 32481 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { homedir } from 'os';
import React from 'react';
import { logEvent } from 'src/services/analytics/index.js';
import { setSessionTrustAccepted } from '../../bootstrap/state.js';
import type { Command } from '../../commands.js';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Link, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { getMcpConfigsByScope } from '../../services/mcp/config.js';
import { BASH_TOOL_NAME } from '../../tools/BashTool/toolName.js';
import { checkHasTrustDialogAccepted, saveCurrentProjectConfig } from '../../utils/config.js';
import { getCwd } from '../../utils/cwd.js';
import { getFsImplementation } from '../../utils/fsOperations.js';
import { gracefulShutdownSync } from '../../utils/gracefulShutdown.js';
import { Select } from '../CustomSelect/index.js';
import { PermissionDialog } from '../permissions/PermissionDialog.js';
import { getApiKeyHelperSources, getAwsCommandsSources, getBashPermissionSources, getDangerousEnvVarsSources, getGcpCommandsSources, getHooksSources, getOtelHeadersHelperSources } from './utils.js';
type Props = {
  onDone(): void;
  commands?: Command[];
};
export function TrustDialog(t0) {
  const $ = _c(33);
  const {
    onDone,
    commands
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = getMcpConfigsByScope("project");
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const {
    servers: projectServers
  } = t1;
  let t2;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = Object.keys(projectServers);
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  const hasMcpServers = t2.length > 0;
  let t3;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = getHooksSources();
    $[2] = t3;

```

---


### `src/components/TrustDialog/utils.ts`

**信息:**
- 行数: 245
- 大小: 7005 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { PermissionRule } from 'src/utils/permissions/PermissionRule.js'
import { getSettingsForSource } from 'src/utils/settings/settings.js'
import type { SettingsJson } from 'src/utils/settings/types.js'
import { BASH_TOOL_NAME } from '../../tools/BashTool/toolName.js'
import { SAFE_ENV_VARS } from '../../utils/managedEnvConstants.js'
import { getPermissionRulesForSource } from '../../utils/permissions/permissionsLoader.js'

function hasHooks(settings: SettingsJson | null): boolean {
  if (settings === null || settings.disableAllHooks) {
    return false
  }
  if (settings.statusLine) {
    return true
  }
  if (settings.fileSuggestion) {
    return true
  }
  if (!settings.hooks) {
    return false
  }
  for (const hookConfig of Object.values(settings.hooks)) {
    if (hookConfig.length > 0) {
      return true
    }
  }
  return false
}

export function getHooksSources(): string[] {
  const sources: string[] = []

  const projectSettings = getSettingsForSource('projectSettings')
  if (hasHooks(projectSettings)) {
    sources.push('.claude/settings.json')
  }

  const localSettings = getSettingsForSource('localSettings')
  if (hasHooks(localSettings)) {
    sources.push('.claude/settings.local.json')
  }

  return sources
}

function hasBashPermission(rules: PermissionRule[]): boolean {
  return rules.some(
    rule =>
      rule.ruleBehavior === 'allow' &&
      (rule.ruleValue.toolName === BASH_TOOL_NAME ||
        rule.ruleValue.toolName.startsWith(BASH_TOOL_NAME + '(')),

```

---


### `src/components/UndercoverAutoCallout.tsx`

**信息:**
- 行数: 3
- 大小: 58 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function UndercoverAutoCallout() {
  return null
}

```

---


### `src/components/ValidationErrorsList.tsx`

**信息:**
- 行数: 148
- 大小: 19567 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import setWith from 'lodash-es/setWith.js';
import * as React from 'react';
import { Box, Text, useTheme } from '../ink.js';
import type { ValidationError } from '../utils/settings/validation.js';
import { type TreeNode, treeify } from '../utils/treeify.js';

/**
 * Builds a nested tree structure from dot-notation paths
 * Uses lodash setWith to avoid automatic array creation
 */
function buildNestedTree(errors: ValidationError[]): TreeNode {
  const tree: TreeNode = {};
  errors.forEach(error => {
    if (!error.path) {
      // Root level error - use empty string as key
      tree[''] = error.message;
      return;
    }

    // Try to enhance the path with meaningful values
    const pathParts = error.path.split('.');
    let modifiedPath = error.path;

    // If we have an invalid value, try to make the path more readable
    if (error.invalidValue !== null && error.invalidValue !== undefined && pathParts.length > 0) {
      const newPathParts: string[] = [];
      for (let i = 0; i < pathParts.length; i++) {
        const part = pathParts[i];
        if (!part) continue;
        const numericPart = parseInt(part, 10);

        // If this is a numeric index and it's the last part where we have the invalid value
        if (!isNaN(numericPart) && i === pathParts.length - 1) {
          // Format the value for display
          let displayValue: string;
          if (typeof error.invalidValue === 'string') {
            displayValue = `"${error.invalidValue}"`;
          } else if (error.invalidValue === null) {
            displayValue = 'null';
          } else if (error.invalidValue === undefined) {
            displayValue = 'undefined';
          } else {
            displayValue = String(error.invalidValue);
          }
          newPathParts.push(displayValue);
        } else {
          // Keep other parts as-is
          newPathParts.push(part);
        }

```

---


### `src/components/VimTextInput.tsx`

**信息:**
- 行数: 140
- 大小: 16170 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import React from 'react';
import { useClipboardImageHint } from '../hooks/useClipboardImageHint.js';
import { useVimInput } from '../hooks/useVimInput.js';
import { Box, color, useTerminalFocus, useTheme } from '../ink.js';
import type { VimTextInputProps } from '../types/textInputTypes.js';
import type { TextHighlight } from '../utils/textHighlighting.js';
import { BaseTextInput } from './BaseTextInput.js';
export type Props = VimTextInputProps & {
  highlights?: TextHighlight[];
};
export default function VimTextInput(props) {
  const $ = _c(38);
  const [theme] = useTheme();
  const isTerminalFocused = useTerminalFocus();
  useClipboardImageHint(isTerminalFocused, !!props.onImagePaste);
  const t0 = props.value;
  const t1 = props.onChange;
  const t2 = props.onSubmit;
  const t3 = props.onExit;
  const t4 = props.onExitMessage;
  const t5 = props.onHistoryReset;
  const t6 = props.onHistoryUp;
  const t7 = props.onHistoryDown;
  const t8 = props.onClearInput;
  const t9 = props.focus;
  const t10 = props.mask;
  const t11 = props.multiline;
  const t12 = props.showCursor ? " " : "";
  const t13 = props.highlightPastedText;
  const t14 = isTerminalFocused ? chalk.inverse : _temp;
  let t15;
  if ($[0] !== theme) {
    t15 = color("text", theme);
    $[0] = theme;
    $[1] = t15;
  } else {
    t15 = $[1];
  }
  let t16;
  if ($[2] !== props.columns || $[3] !== props.cursorOffset || $[4] !== props.disableCursorMovementForUpDownKeys || $[5] !== props.disableEscapeDoublePress || $[6] !== props.focus || $[7] !== props.highlightPastedText || $[8] !== props.inputFilter || $[9] !== props.mask || $[10] !== props.maxVisibleLines || $[11] !== props.multiline || $[12] !== props.onChange || $[13] !== props.onChangeCursorOffset || $[14] !== props.onClearInput || $[15] !== props.onExit || $[16] !== props.onExitMessage || $[17] !== props.onHistoryDown || $[18] !== props.onHistoryReset || $[19] !== props.onHistoryUp || $[20] !== props.onImagePaste || $[21] !== props.onModeChange || $[22] !== props.onSubmit || $[23] !== props.onUndo || $[24] !== props.value || $[25] !== t12 || $[26] !== t14 || $[27] !== t15) {
    t16 = {
      value: t0,
      onChange: t1,
      onSubmit: t2,
      onExit: t3,
      onExitMessage: t4,
      onHistoryReset: t5,
      onHistoryUp: t6,

```

---


### `src/components/VirtualMessageList.tsx`

**信息:**
- 行数: 1082
- 大小: 148516 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { RefObject } from 'react';
import * as React from 'react';
import { useCallback, useContext, useEffect, useImperativeHandle, useRef, useState, useSyncExternalStore } from 'react';
import { useVirtualScroll } from '../hooks/useVirtualScroll.js';
import type { ScrollBoxHandle } from '../ink/components/ScrollBox.js';
import type { DOMElement } from '../ink/dom.js';
import type { MatchPosition } from '../ink/render-to-screen.js';
import { Box } from '../ink.js';
import type { RenderableMessage } from '../types/message.js';
import { TextHoverColorContext } from './design-system/ThemedText.js';
import { ScrollChromeContext } from './FullscreenLayout.js';

// Rows of breathing room above the target when we scrollTo.
const HEADROOM = 3;
import { logForDebugging } from '../utils/debug.js';
import { sleep } from '../utils/sleep.js';
import { renderableSearchText } from '../utils/transcriptSearch.js';
import { isNavigableMessage, type MessageActionsNav, type MessageActionsState, type NavigableMessage, stripSystemReminders, toolCallOf } from './messageActions.js';

// Fallback extractor: lower + cache here for callers without the
// Messages.tsx tool-lookup path (tests, static contexts). Messages.tsx
// provides its own lowering cache that also handles tool extractSearchText.
const fallbackLowerCache = new WeakMap<RenderableMessage, string>();
function defaultExtractSearchText(msg: RenderableMessage): string {
  const cached = fallbackLowerCache.get(msg);
  if (cached !== undefined) return cached;
  const lowered = renderableSearchText(msg);
  fallbackLowerCache.set(msg, lowered);
  return lowered;
}
export type StickyPrompt = {
  text: string;
  scrollTo: () => void;
}
// Click sets this — header HIDES but padding stays collapsed (0) so
// the content ❯ lands at screen row 0 instead of row 1. Cleared on
// the next sticky-prompt compute (user scrolls again).
| 'clicked';

/** Huge pasted prompts (cat file | claude) can be MBs. Header wraps into
 *  2 rows via overflow:hidden — this just bounds the React prop size. */
const STICKY_TEXT_CAP = 500;

/** Imperative handle for transcript navigation. Methods compute matches
 *  HERE (renderableMessages indices are only valid inside this component —
 *  Messages.tsx filters and reorders, REPL can't compute externally). */
export type JumpHandle = {
  jumpToIndex: (i: number) => void;
  setSearchQuery: (q: string) => void;

```

---


### `src/components/WorkflowMultiselectDialog.tsx`

**信息:**
- 行数: 128
- 大小: 14276 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useState } from 'react';
import type { Workflow } from '../commands/install-github-app/types.js';
import type { ExitState } from '../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Link, Text } from '../ink.js';
import { ConfigurableShortcutHint } from './ConfigurableShortcutHint.js';
import { SelectMulti } from './CustomSelect/SelectMulti.js';
import { Byline } from './design-system/Byline.js';
import { Dialog } from './design-system/Dialog.js';
import { KeyboardShortcutHint } from './design-system/KeyboardShortcutHint.js';
type WorkflowOption = {
  value: Workflow;
  label: string;
};
type Props = {
  onSubmit: (selectedWorkflows: Workflow[]) => void;
  defaultSelections: Workflow[];
};
const WORKFLOWS: WorkflowOption[] = [{
  value: 'claude' as const,
  label: '@Claude Code - Tag @claude in issues and PR comments'
}, {
  value: 'claude-review' as const,
  label: 'Claude Code Review - Automated code review on new PRs'
}];
function renderInputGuide(exitState: ExitState): React.ReactNode {
  if (exitState.pending) {
    return <Text>Press {exitState.keyName} again to exit</Text>;
  }
  return <Byline>
      <KeyboardShortcutHint shortcut="↑↓" action="navigate" />
      <KeyboardShortcutHint shortcut="Space" action="toggle" />
      <KeyboardShortcutHint shortcut="Enter" action="confirm" />
      <ConfigurableShortcutHint action="confirm:no" context="Confirmation" fallback="Esc" description="cancel" />
    </Byline>;
}
export function WorkflowMultiselectDialog(t0) {
  const $ = _c(14);
  const {
    onSubmit,
    defaultSelections
  } = t0;
  const [showError, setShowError] = useState(false);
  let t1;
  if ($[0] !== onSubmit) {
    t1 = selectedValues => {
      if (selectedValues.length === 0) {
        setShowError(true);
        return;
      }

```

---


### `src/components/WorktreeExitDialog.tsx`

**信息:**
- 行数: 231
- 大小: 35484 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React, { useEffect, useState } from 'react';
import type { CommandResultDisplay } from 'src/commands.js';
import { logEvent } from 'src/services/analytics/index.js';
import { logForDebugging } from 'src/utils/debug.js';
import { Box, Text } from '../ink.js';
import { execFileNoThrow } from '../utils/execFileNoThrow.js';
import { getPlansDirectory } from '../utils/plans.js';
import { setCwd } from '../utils/Shell.js';
import { cleanupWorktree, getCurrentWorktreeSession, keepWorktree, killTmuxSession } from '../utils/worktree.js';
import { Select } from './CustomSelect/select.js';
import { Dialog } from './design-system/Dialog.js';
import { Spinner } from './Spinner.js';

// Inline require breaks the cycle this file would otherwise close:
// sessionStorage → commands → exit → ExitFlow → here. All call sites
// are inside callbacks, so the lazy require never sees an undefined import.
function recordWorktreeExit(): void {
  /* eslint-disable @typescript-eslint/no-require-imports */
  ;
  (require('../utils/sessionStorage.js') as typeof import('../utils/sessionStorage.js')).saveWorktreeState(null);
  /* eslint-enable @typescript-eslint/no-require-imports */
}
type Props = {
  onDone: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  onCancel?: () => void;
};
export function WorktreeExitDialog({
  onDone,
  onCancel
}: Props): React.ReactNode {
  const [status, setStatus] = useState<'loading' | 'asking' | 'keeping' | 'removing' | 'done'>('loading');
  const [changes, setChanges] = useState<string[]>([]);
  const [commitCount, setCommitCount] = useState<number>(0);
  const [resultMessage, setResultMessage] = useState<string | undefined>();
  const worktreeSession = getCurrentWorktreeSession();
  useEffect(() => {
    async function loadChanges() {
      let changeLines: string[] = [];
      const gitStatus = await execFileNoThrow('git', ['status', '--porcelain']);
      if (gitStatus.stdout) {
        changeLines = gitStatus.stdout.split('\n').filter(_ => _.trim() !== '');
        setChanges(changeLines);
      }

      // Check for commits to eject
      if (worktreeSession) {
        // Get commits in worktree that are not in original branch
        const {

```

---


### `src/components/agents/AgentDetail.tsx`

**信息:**
- 行数: 220
- 大小: 23566 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import type { Tools } from '../../Tool.js';
import { getAgentColor } from '../../tools/AgentTool/agentColorManager.js';
import { getMemoryScopeDisplay } from '../../tools/AgentTool/agentMemory.js';
import { resolveAgentTools } from '../../tools/AgentTool/agentToolUtils.js';
import { type AgentDefinition, isBuiltInAgent } from '../../tools/AgentTool/loadAgentsDir.js';
import { getAgentModelDisplay } from '../../utils/model/agent.js';
import { Markdown } from '../Markdown.js';
import { getActualRelativeAgentFilePath } from './agentFileUtils.js';
type Props = {
  agent: AgentDefinition;
  tools: Tools;
  allAgents?: AgentDefinition[];
  onBack: () => void;
};
export function AgentDetail(t0) {
  const $ = _c(48);
  const {
    agent,
    tools,
    onBack
  } = t0;
  const resolvedTools = resolveAgentTools(agent, tools, false);
  let t1;
  if ($[0] !== agent) {
    t1 = getActualRelativeAgentFilePath(agent);
    $[0] = agent;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const filePath = t1;
  let t2;
  if ($[2] !== agent.agentType) {
    t2 = getAgentColor(agent.agentType);
    $[2] = agent.agentType;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  const backgroundColor = t2;
  let t3;
  if ($[4] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = {
      context: "Confirmation"

```

---


### `src/components/agents/AgentEditor.tsx`

**信息:**
- 行数: 178
- 大小: 26437 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import chalk from 'chalk';
import figures from 'figures';
import * as React from 'react';
import { useCallback, useMemo, useState } from 'react';
import { useSetAppState } from 'src/state/AppState.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import type { Tools } from '../../Tool.js';
import { type AgentColorName, setAgentColor } from '../../tools/AgentTool/agentColorManager.js';
import { type AgentDefinition, getActiveAgentsFromList, isCustomAgent, isPluginAgent } from '../../tools/AgentTool/loadAgentsDir.js';
import { editFileInEditor } from '../../utils/promptEditor.js';
import { getActualAgentFilePath, updateAgentFile } from './agentFileUtils.js';
import { ColorPicker } from './ColorPicker.js';
import { ModelSelector } from './ModelSelector.js';
import { ToolSelector } from './ToolSelector.js';
import { getAgentSourceDisplayName } from './utils.js';
type Props = {
  agent: AgentDefinition;
  tools: Tools;
  onSaved: (message: string) => void;
  onBack: () => void;
};
type EditMode = 'menu' | 'edit-tools' | 'edit-color' | 'edit-model';
type SaveChanges = {
  tools?: string[];
  color?: AgentColorName;
  model?: string;
};
export function AgentEditor({
  agent,
  tools,
  onSaved,
  onBack
}: Props): React.ReactNode {
  const setAppState = useSetAppState();
  const [editMode, setEditMode] = useState<EditMode>('menu');
  const [selectedMenuIndex, setSelectedMenuIndex] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [selectedColor, setSelectedColor] = useState<AgentColorName | undefined>(agent.color as AgentColorName | undefined);
  const handleOpenInEditor = useCallback(async () => {
    const filePath = getActualAgentFilePath(agent);
    const result = await editFileInEditor(filePath);
    if (result.error) {
      setError(result.error);
    } else {
      onSaved(`Opened ${agent.agentType} in editor. If you made edits, restart to load the latest version.`);
    }
  }, [agent, onSaved]);
  const handleSave = useCallback(async (changes: SaveChanges = {}) => {

```

---


### `src/components/agents/AgentNavigationFooter.tsx`

**信息:**
- 行数: 26
- 大小: 3067 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Text } from '../../ink.js';
type Props = {
  instructions?: string;
};
export function AgentNavigationFooter(t0) {
  const $ = _c(2);
  const {
    instructions: t1
  } = t0;
  const instructions = t1 === undefined ? "Press \u2191\u2193 to navigate \xB7 Enter to select \xB7 Esc to go back" : t1;
  const exitState = useExitOnCtrlCDWithKeybindings();
  const t2 = exitState.pending ? `Press ${exitState.keyName} again to exit` : instructions;
  let t3;
  if ($[0] !== t2) {
    t3 = <Box marginLeft={2}><Text dimColor={true}>{t2}</Text></Box>;
    $[0] = t2;
    $[1] = t3;
  } else {
    t3 = $[1];
  }
  return t3;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsInVzZUV4aXRPbkN0cmxDRFdpdGhLZXliaW5kaW5ncyIsIkJveCIsIlRleHQiLCJQcm9wcyIsImluc3RydWN0aW9ucyIsIkFnZW50TmF2aWdhdGlvbkZvb3RlciIsInQwIiwiJCIsIl9jIiwidDEiLCJ1bmRlZmluZWQiLCJleGl0U3RhdGUiLCJ0MiIsInBlbmRpbmciLCJrZXlOYW1lIiwidDMiXSwic291cmNlcyI6WyJBZ2VudE5hdmlnYXRpb25Gb290ZXIudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgdXNlRXhpdE9uQ3RybENEV2l0aEtleWJpbmRpbmdzIH0gZnJvbSAnLi4vLi4vaG9va3MvdXNlRXhpdE9uQ3RybENEV2l0aEtleWJpbmRpbmdzLmpzJ1xuaW1wb3J0IHsgQm94LCBUZXh0IH0gZnJvbSAnLi4vLi4vaW5rLmpzJ1xuXG50eXBlIFByb3BzID0ge1xuICBpbnN0cnVjdGlvbnM/OiBzdHJpbmdcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIEFnZW50TmF2aWdhdGlvbkZvb3Rlcih7XG4gIGluc3RydWN0aW9ucyA9ICdQcmVzcyDihpHihpMgdG8gbmF2aWdhdGUgwrcgRW50ZXIgdG8gc2VsZWN0IMK3IEVzYyB0byBnbyBiYWNrJyxcbn06IFByb3BzKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgY29uc3QgZXhpdFN0YXRlID0gdXNlRXhpdE9uQ3RybENEV2l0aEtleWJpbmRpbmdzKClcblxuICByZXR1cm4gKFxuICAgIDxCb3ggbWFyZ2luTGVmdD17Mn0+XG4gICAgICA8VGV4dCBkaW1Db2xvcj5cbiAgICAgICAge2V4aXRTdGF0ZS5wZW5kaW5nXG4gICAgICAgICAgPyBgUHJlc3MgJHtleGl0U3RhdGUua2V5TmFtZX0gYWdhaW4gdG8gZXhpdGBcbiAgICAgICAgICA6IGluc3RydWN0aW9uc31cbiAgICAgIDwvVGV4dD5cbiAgICA8L0JveD5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiO0FBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixTQUFTQyw4QkFBOEIsUUFBUSwrQ0FBK0M7QUFDOUYsU0FBU0MsR0FBRyxFQUFFQyxJQUFJLFFBQVEsY0FBYztBQUV4QyxLQUFLQyxLQUFLLEdBQUc7RUFDWEMsWUFBWSxDQUFDLEVBQUUsTUFBTTtBQUN2QixDQUFDO0FBRUQsT0FBTyxTQUFBQyxzQkFBQUMsRUFBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUErQjtJQUFBSixZQUFBLEVBQUFLO0VBQUEsSUFBQUgsRUFFOUI7RUFETixNQUFBRixZQUFBLEdBQUFLLEVBQXdFLEtBQXhFQyxTQUF3RSxHQUF4RSx5RUFBd0UsR0FBeEVELEVBQXdFO0VBRXhFLE1BQUFFLFNBQUEsR0FBa0JYLDhCQUE4QixDQUFDLENBQUM7RUFLM0MsTUFBQVksRUFBQSxHQUFBRCxTQUFTLENBQUFFLE9BRU0sR0FGZixTQUNZRixTQUFTLENBQUFHLE9BQVEsZ0JBQ2QsR0FGZlYsWUFFZTtFQUFBLElBQUFXLEVBQUE7RUFBQSxJQUFBUixDQUFBLFFBQUFLLEVBQUE7SUFKcEJHLEVBQUEsSUFBQyxHQUFHLENBQWEsVUFBQyxDQUFELEdBQUMsQ0FDaEIsQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFSLEtBQU8sQ0FBQyxDQUNYLENBQUFILEVBRWMsQ0FDakIsRUFKQyxJQUFJLENBS1AsRUFOQyxHQUFHLENBTUU7SUFBQUwsQ0FBQSxNQUFBSyxFQUFBO0lBQUFMLENBQUEsTUFBQVEsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQVIsQ0FBQTtFQUFBO0VBQUEsT0FOTlEsRUFNTTtBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/agents/AgentsList.tsx`

**信息:**
- 行数: 440
- 大小: 52257 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import type { SettingSource } from 'src/utils/settings/constants.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text } from '../../ink.js';
import type { ResolvedAgent } from '../../tools/AgentTool/agentDisplay.js';
import { AGENT_SOURCE_GROUPS, compareAgentsByName, getOverrideSourceLabel, resolveAgentModelDisplay } from '../../tools/AgentTool/agentDisplay.js';
import type { AgentDefinition } from '../../tools/AgentTool/loadAgentsDir.js';
import { count } from '../../utils/array.js';
import { Dialog } from '../design-system/Dialog.js';
import { Divider } from '../design-system/Divider.js';
import { getAgentSourceDisplayName } from './utils.js';
type Props = {
  source: SettingSource | 'all' | 'built-in' | 'plugin';
  agents: ResolvedAgent[];
  onBack: () => void;
  onSelect: (agent: AgentDefinition) => void;
  onCreateNew?: () => void;
  changes?: string[];
};
export function AgentsList(t0) {
  const $ = _c(96);
  const {
    source,
    agents,
    onBack,
    onSelect,
    onCreateNew,
    changes
  } = t0;
  const [selectedAgent, setSelectedAgent] = React.useState(null);
  const [isCreateNewSelected, setIsCreateNewSelected] = React.useState(true);
  let t1;
  if ($[0] !== agents) {
    t1 = [...agents].sort(compareAgentsByName);
    $[0] = agents;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const sortedAgents = t1;
  const getOverrideInfo = _temp;
  let t2;
  if ($[2] !== isCreateNewSelected) {
    t2 = () => <Box><Text color={isCreateNewSelected ? "suggestion" : undefined}>{isCreateNewSelected ? `${figures.pointer} ` : "  "}</Text><Text color={isCreateNewSelected ? "suggestion" : undefined}>Create new agent</Text></Box>;
    $[2] = isCreateNewSelected;
    $[3] = t2;
  } else {
    t2 = $[3];

```

---


### `src/components/agents/AgentsMenu.tsx`

**信息:**
- 行数: 800
- 大小: 70586 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import * as React from 'react';
import { useCallback, useMemo, useState } from 'react';
import type { SettingSource } from 'src/utils/settings/constants.js';
import type { CommandResultDisplay } from '../../commands.js';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { useMergedTools } from '../../hooks/useMergedTools.js';
import { Box, Text } from '../../ink.js';
import { useAppState, useSetAppState } from '../../state/AppState.js';
import type { Tools } from '../../Tool.js';
import { type ResolvedAgent, resolveAgentOverrides } from '../../tools/AgentTool/agentDisplay.js';
import { type AgentDefinition, getActiveAgentsFromList } from '../../tools/AgentTool/loadAgentsDir.js';
import { toError } from '../../utils/errors.js';
import { logError } from '../../utils/log.js';
import { Select } from '../CustomSelect/select.js';
import { Dialog } from '../design-system/Dialog.js';
import { AgentDetail } from './AgentDetail.js';
import { AgentEditor } from './AgentEditor.js';
import { AgentNavigationFooter } from './AgentNavigationFooter.js';
import { AgentsList } from './AgentsList.js';
import { deleteAgentFromFile } from './agentFileUtils.js';
import { CreateAgentWizard } from './new-agent-creation/CreateAgentWizard.js';
import type { ModeState } from './types.js';
type Props = {
  tools: Tools;
  onExit: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
export function AgentsMenu(t0) {
  const $ = _c(157);
  const {
    tools,
    onExit
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = {
      mode: "list-agents",
      source: "all"
    };
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const [modeState, setModeState] = useState(t1);
  const agentDefinitions = useAppState(_temp);
  const mcpTools = useAppState(_temp2);
  const toolPermissionContext = useAppState(_temp3);

```

---


### `src/components/agents/ColorPicker.tsx`

**信息:**
- 行数: 112
- 大小: 14204 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { useState } from 'react';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text } from '../../ink.js';
import { AGENT_COLOR_TO_THEME_COLOR, AGENT_COLORS, type AgentColorName } from '../../tools/AgentTool/agentColorManager.js';
import { capitalize } from '../../utils/stringUtils.js';
type ColorOption = AgentColorName | 'automatic';
const COLOR_OPTIONS: ColorOption[] = ['automatic', ...AGENT_COLORS];
type Props = {
  agentName: string;
  currentColor?: AgentColorName | 'automatic';
  onConfirm: (color: AgentColorName | undefined) => void;
};
export function ColorPicker(t0) {
  const $ = _c(17);
  const {
    agentName,
    currentColor: t1,
    onConfirm
  } = t0;
  const currentColor = t1 === undefined ? "automatic" : t1;
  let t2;
  if ($[0] !== currentColor) {
    t2 = COLOR_OPTIONS.findIndex(opt => opt === currentColor);
    $[0] = currentColor;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  const [selectedIndex, setSelectedIndex] = useState(Math.max(0, t2));
  let t3;
  if ($[2] !== onConfirm || $[3] !== selectedIndex) {
    t3 = e => {
      if (e.key === "up") {
        e.preventDefault();
        setSelectedIndex(_temp);
      } else {
        if (e.key === "down") {
          e.preventDefault();
          setSelectedIndex(_temp2);
        } else {
          if (e.key === "return") {
            e.preventDefault();
            const selected = COLOR_OPTIONS[selectedIndex];
            onConfirm(selected === "automatic" ? undefined : selected);
          }
        }
      }
    };

```

---


### `src/components/agents/ModelSelector.tsx`

**信息:**
- 行数: 68
- 大小: 6927 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { getAgentModelOptions } from '../../utils/model/agent.js';
import { Select } from '../CustomSelect/select.js';
interface ModelSelectorProps {
  initialModel?: string;
  onComplete: (model?: string) => void;
  onCancel?: () => void;
}
export function ModelSelector(t0) {
  const $ = _c(11);
  const {
    initialModel,
    onComplete,
    onCancel
  } = t0;
  let t1;
  if ($[0] !== initialModel) {
    bb0: {
      const base = getAgentModelOptions();
      if (initialModel && !base.some(o => o.value === initialModel)) {
        t1 = [{
          value: initialModel,
          label: initialModel,
          description: "Current model (custom ID)"
        }, ...base];
        break bb0;
      }
      t1 = base;
    }
    $[0] = initialModel;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const modelOptions = t1;
  const defaultModel = initialModel ?? "sonnet";
  let t2;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Box marginBottom={1}><Text dimColor={true}>Model determines the agent's reasoning capabilities and speed.</Text></Box>;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  let t3;
  if ($[3] !== onCancel || $[4] !== onComplete) {
    t3 = () => onCancel ? onCancel() : onComplete(undefined);
    $[3] = onCancel;
    $[4] = onComplete;

```

---


### `src/components/agents/ToolSelector.tsx`

**信息:**
- 行数: 562
- 大小: 64871 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { useCallback, useMemo, useState } from 'react';
import { mcpInfoFromString } from 'src/services/mcp/mcpStringUtils.js';
import { isMcpTool } from 'src/services/mcp/utils.js';
import type { Tool, Tools } from 'src/Tool.js';
import { filterToolsForAgent } from 'src/tools/AgentTool/agentToolUtils.js';
import { AGENT_TOOL_NAME } from 'src/tools/AgentTool/constants.js';
import { BashTool } from 'src/tools/BashTool/BashTool.js';
import { ExitPlanModeV2Tool } from 'src/tools/ExitPlanModeTool/ExitPlanModeV2Tool.js';
import { FileEditTool } from 'src/tools/FileEditTool/FileEditTool.js';
import { FileReadTool } from 'src/tools/FileReadTool/FileReadTool.js';
import { FileWriteTool } from 'src/tools/FileWriteTool/FileWriteTool.js';
import { GlobTool } from 'src/tools/GlobTool/GlobTool.js';
import { GrepTool } from 'src/tools/GrepTool/GrepTool.js';
import { ListMcpResourcesTool } from 'src/tools/ListMcpResourcesTool/ListMcpResourcesTool.js';
import { NotebookEditTool } from 'src/tools/NotebookEditTool/NotebookEditTool.js';
import { ReadMcpResourceTool } from 'src/tools/ReadMcpResourceTool/ReadMcpResourceTool.js';
import { TaskOutputTool } from 'src/tools/TaskOutputTool/TaskOutputTool.js';
import { TaskStopTool } from 'src/tools/TaskStopTool/TaskStopTool.js';
import { TodoWriteTool } from 'src/tools/TodoWriteTool/TodoWriteTool.js';
import { TungstenTool } from 'src/tools/TungstenTool/TungstenTool.js';
import { WebFetchTool } from 'src/tools/WebFetchTool/WebFetchTool.js';
import { WebSearchTool } from 'src/tools/WebSearchTool/WebSearchTool.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { count } from '../../utils/array.js';
import { plural } from '../../utils/stringUtils.js';
import { Divider } from '../design-system/Divider.js';
type Props = {
  tools: Tools;
  initialTools: string[] | undefined;
  onComplete: (selectedTools: string[] | undefined) => void;
  onCancel?: () => void;
};
type ToolBucket = {
  name: string;
  toolNames: Set<string>;
  isMcp?: boolean;
};
type ToolBuckets = {
  READ_ONLY: ToolBucket;
  EDIT: ToolBucket;
  EXECUTION: ToolBucket;
  MCP: ToolBucket;
  OTHER: ToolBucket;
};
function getToolBuckets(): ToolBuckets {
  return {

```

---


### `src/components/agents/agentFileUtils.ts`

**信息:**
- 行数: 272
- 大小: 7487 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { mkdir, open, unlink } from 'fs/promises'
import { join } from 'path'
import type { SettingSource } from 'src/utils/settings/constants.js'
import { getManagedFilePath } from 'src/utils/settings/managedPath.js'
import type { AgentMemoryScope } from '../../tools/AgentTool/agentMemory.js'
import {
  type AgentDefinition,
  isBuiltInAgent,
  isPluginAgent,
} from '../../tools/AgentTool/loadAgentsDir.js'
import { getCwd } from '../../utils/cwd.js'
import type { EffortValue } from '../../utils/effort.js'
import { getClaudeConfigHomeDir } from '../../utils/envUtils.js'
import { getErrnoCode } from '../../utils/errors.js'
import { AGENT_PATHS } from './types.js'

/**
 * Formats agent data as markdown file content
 */
export function formatAgentAsMarkdown(
  agentType: string,
  whenToUse: string,
  tools: string[] | undefined,
  systemPrompt: string,
  color?: string,
  model?: string,
  memory?: AgentMemoryScope,
  effort?: EffortValue,
): string {
  // For YAML double-quoted strings, we need to escape:
  // - Backslashes: \ -> \\
  // - Double quotes: " -> \"
  // - Newlines: \n -> \\n (so yaml reads it as literal backslash-n, not newline)
  const escapedWhenToUse = whenToUse
    .replace(/\\/g, '\\\\') // Escape backslashes first
    .replace(/"/g, '\\"') // Escape double quotes
    .replace(/\n/g, '\\\\n') // Escape newlines as \\n so yaml preserves them as \n

  // Omit tools field entirely when tools is undefined or ['*'] (all tools allowed)
  const isAllTools =
    tools === undefined || (tools.length === 1 && tools[0] === '*')
  const toolsLine = isAllTools ? '' : `\ntools: ${tools.join(', ')}`
  const modelLine = model ? `\nmodel: ${model}` : ''
  const effortLine = effort !== undefined ? `\neffort: ${effort}` : ''
  const colorLine = color ? `\ncolor: ${color}` : ''
  const memoryLine = memory ? `\nmemory: ${memory}` : ''

  return `---
name: ${agentType}
description: "${escapedWhenToUse}"${toolsLine}${modelLine}${effortLine}${colorLine}${memoryLine}

```

---


### `src/components/agents/generateAgent.ts`

**信息:**
- 行数: 197
- 大小: 10151 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ContentBlock } from '@anthropic-ai/sdk/resources/index.mjs'
import { getUserContext } from 'src/context.js'
import { queryModelWithoutStreaming } from 'src/services/api/claude.js'
import { getEmptyToolPermissionContext } from 'src/Tool.js'
import { AGENT_TOOL_NAME } from 'src/tools/AgentTool/constants.js'
import { prependUserContext } from 'src/utils/api.js'
import {
  createUserMessage,
  normalizeMessagesForAPI,
} from 'src/utils/messages.js'
import type { ModelName } from 'src/utils/model/model.js'
import { isAutoMemoryEnabled } from '../../memdir/paths.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import { jsonParse } from '../../utils/slowOperations.js'
import { asSystemPrompt } from '../../utils/systemPromptType.js'

type GeneratedAgent = {
  identifier: string
  whenToUse: string
  systemPrompt: string
}

const AGENT_CREATION_SYSTEM_PROMPT = `You are an elite AI agent architect specializing in crafting high-performance agent configurations. Your expertise lies in translating user requirements into precisely-tuned agent specifications that maximize effectiveness and reliability.

**Important Context**: You may have access to project-specific instructions from CLAUDE.md files and other context that may include coding standards, project structure, and custom requirements. Consider this context when creating agents to ensure they align with the project's established patterns and practices.

When a user describes what they want an agent to do, you will:

1. **Extract Core Intent**: Identify the fundamental purpose, key responsibilities, and success criteria for the agent. Look for both explicit requirements and implicit needs. Consider any project-specific context from CLAUDE.md files. For agents that are meant to review code, you should assume that the user is asking to review recently written code and not the whole codebase, unless the user has explicitly instructed you otherwise.

2. **Design Expert Persona**: Create a compelling expert identity that embodies deep domain knowledge relevant to the task. The persona should inspire confidence and guide the agent's decision-making approach.

3. **Architect Comprehensive Instructions**: Develop a system prompt that:
   - Establishes clear behavioral boundaries and operational parameters
   - Provides specific methodologies and best practices for task execution
   - Anticipates edge cases and provides guidance for handling them
   - Incorporates any specific requirements or preferences mentioned by the user
   - Defines output format expectations when relevant
   - Aligns with project-specific coding standards and patterns from CLAUDE.md

4. **Optimize for Performance**: Include:
   - Decision-making frameworks appropriate to the domain
   - Quality control mechanisms and self-verification steps
   - Efficient workflow patterns
   - Clear escalation or fallback strategies

5. **Create Identifier**: Design a concise, descriptive identifier that:

```

---


### `src/components/agents/new-agent-creation/CreateAgentWizard.tsx`

**信息:**
- 行数: 97
- 大小: 10427 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode } from 'react';
import { isAutoMemoryEnabled } from '../../../memdir/paths.js';
import type { Tools } from '../../../Tool.js';
import type { AgentDefinition } from '../../../tools/AgentTool/loadAgentsDir.js';
import { WizardProvider } from '../../wizard/index.js';
import type { WizardStepComponent } from '../../wizard/types.js';
import type { AgentWizardData } from './types.js';
import { ColorStep } from './wizard-steps/ColorStep.js';
import { ConfirmStepWrapper } from './wizard-steps/ConfirmStepWrapper.js';
import { DescriptionStep } from './wizard-steps/DescriptionStep.js';
import { GenerateStep } from './wizard-steps/GenerateStep.js';
import { LocationStep } from './wizard-steps/LocationStep.js';
import { MemoryStep } from './wizard-steps/MemoryStep.js';
import { MethodStep } from './wizard-steps/MethodStep.js';
import { ModelStep } from './wizard-steps/ModelStep.js';
import { PromptStep } from './wizard-steps/PromptStep.js';
import { ToolsStep } from './wizard-steps/ToolsStep.js';
import { TypeStep } from './wizard-steps/TypeStep.js';
type Props = {
  tools: Tools;
  existingAgents: AgentDefinition[];
  onComplete: (message: string) => void;
  onCancel: () => void;
};
export function CreateAgentWizard(t0) {
  const $ = _c(17);
  const {
    tools,
    existingAgents,
    onComplete,
    onCancel
  } = t0;
  let t1;
  if ($[0] !== existingAgents) {
    t1 = () => <TypeStep existingAgents={existingAgents} />;
    $[0] = existingAgents;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] !== tools) {
    t2 = () => <ToolsStep tools={tools} />;
    $[2] = tools;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  let t3;

```

---


### `src/components/agents/new-agent-creation/types.ts`

**信息:**
- 行数: 1
- 大小: 54 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type AgentWizardData = Record<string, unknown>

```

---


### `src/components/agents/new-agent-creation/wizard-steps/ColorStep.tsx`

**信息:**
- 行数: 84
- 大小: 10430 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode } from 'react';
import { Box } from '../../../../ink.js';
import { useKeybinding } from '../../../../keybindings/useKeybinding.js';
import type { AgentColorName } from '../../../../tools/AgentTool/agentColorManager.js';
import { ConfigurableShortcutHint } from '../../../ConfigurableShortcutHint.js';
import { Byline } from '../../../design-system/Byline.js';
import { KeyboardShortcutHint } from '../../../design-system/KeyboardShortcutHint.js';
import { useWizard } from '../../../wizard/index.js';
import { WizardDialogLayout } from '../../../wizard/WizardDialogLayout.js';
import { ColorPicker } from '../../ColorPicker.js';
import type { AgentWizardData } from '../types.js';
export function ColorStep() {
  const $ = _c(14);
  const {
    goNext,
    goBack,
    updateWizardData,
    wizardData
  } = useWizard();
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = {
      context: "Confirmation"
    };
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  useKeybinding("confirm:no", goBack, t0);
  let t1;
  if ($[1] !== goNext || $[2] !== updateWizardData || $[3] !== wizardData.agentType || $[4] !== wizardData.location || $[5] !== wizardData.selectedModel || $[6] !== wizardData.selectedTools || $[7] !== wizardData.systemPrompt || $[8] !== wizardData.whenToUse) {
    t1 = color => {
      updateWizardData({
        selectedColor: color,
        finalAgent: {
          agentType: wizardData.agentType,
          whenToUse: wizardData.whenToUse,
          getSystemPrompt: () => wizardData.systemPrompt,
          tools: wizardData.selectedTools,
          ...(wizardData.selectedModel ? {
            model: wizardData.selectedModel
          } : {}),
          ...(color ? {
            color: color as AgentColorName
          } : {}),
          source: wizardData.location
        }
      });
      goNext();

```

---


### `src/components/agents/new-agent-creation/wizard-steps/ConfirmStep.tsx`

**信息:**
- 行数: 378
- 大小: 35034 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode } from 'react';
import type { KeyboardEvent } from '../../../../ink/events/keyboard-event.js';
import { Box, Text } from '../../../../ink.js';
import { useKeybinding } from '../../../../keybindings/useKeybinding.js';
import { isAutoMemoryEnabled } from '../../../../memdir/paths.js';
import type { Tools } from '../../../../Tool.js';
import { getMemoryScopeDisplay } from '../../../../tools/AgentTool/agentMemory.js';
import type { AgentDefinition } from '../../../../tools/AgentTool/loadAgentsDir.js';
import { truncateToWidth } from '../../../../utils/format.js';
import { getAgentModelDisplay } from '../../../../utils/model/agent.js';
import { ConfigurableShortcutHint } from '../../../ConfigurableShortcutHint.js';
import { Byline } from '../../../design-system/Byline.js';
import { KeyboardShortcutHint } from '../../../design-system/KeyboardShortcutHint.js';
import { useWizard } from '../../../wizard/index.js';
import { WizardDialogLayout } from '../../../wizard/WizardDialogLayout.js';
import { getNewRelativeAgentFilePath } from '../../agentFileUtils.js';
import { validateAgent } from '../../validateAgent.js';
import type { AgentWizardData } from '../types.js';
type Props = {
  tools: Tools;
  existingAgents: AgentDefinition[];
  onSave: () => void;
  onSaveAndEdit: () => void;
  error?: string | null;
};
export function ConfirmStep(t0) {
  const $ = _c(88);
  const {
    tools,
    existingAgents,
    onSave,
    onSaveAndEdit,
    error
  } = t0;
  const {
    goBack,
    wizardData
  } = useWizard();
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = {
      context: "Confirmation"
    };
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  useKeybinding("confirm:no", goBack, t1);
  let t2;

```

---


### `src/components/agents/new-agent-creation/wizard-steps/ConfirmStepWrapper.tsx`

**信息:**
- 行数: 74
- 大小: 14450 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import chalk from 'chalk';
import React, { type ReactNode, useCallback, useState } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { useSetAppState } from 'src/state/AppState.js';
import type { Tools } from '../../../../Tool.js';
import type { AgentDefinition } from '../../../../tools/AgentTool/loadAgentsDir.js';
import { getActiveAgentsFromList } from '../../../../tools/AgentTool/loadAgentsDir.js';
import { editFileInEditor } from '../../../../utils/promptEditor.js';
import { useWizard } from '../../../wizard/index.js';
import { getNewAgentFilePath, saveAgentToFile } from '../../agentFileUtils.js';
import type { AgentWizardData } from '../types.js';
import { ConfirmStep } from './ConfirmStep.js';
type Props = {
  tools: Tools;
  existingAgents: AgentDefinition[];
  onComplete: (message: string) => void;
};
export function ConfirmStepWrapper({
  tools,
  existingAgents,
  onComplete
}: Props): ReactNode {
  const {
    wizardData
  } = useWizard<AgentWizardData>();
  const [saveError, setSaveError] = useState<string | null>(null);
  const setAppState = useSetAppState();
  const saveAgent = useCallback(async (openInEditor: boolean): Promise<void> => {
    if (!wizardData?.finalAgent) return;
    try {
      await saveAgentToFile(wizardData.location!, wizardData.finalAgent.agentType, wizardData.finalAgent.whenToUse, wizardData.finalAgent.tools, wizardData.finalAgent.getSystemPrompt(), true, wizardData.finalAgent.color, wizardData.finalAgent.model, wizardData.finalAgent.memory);
      setAppState(state => {
        if (!wizardData.finalAgent) return state;
        const allAgents = state.agentDefinitions.allAgents.concat(wizardData.finalAgent);
        return {
          ...state,
          agentDefinitions: {
            ...state.agentDefinitions,
            activeAgents: getActiveAgentsFromList(allAgents),
            allAgents
          }
        };
      });
      if (openInEditor) {
        const filePath = getNewAgentFilePath({
          source: wizardData.location!,
          agentType: wizardData.finalAgent.agentType
        });
        await editFileInEditor(filePath);
      }

```

---


### `src/components/agents/new-agent-creation/wizard-steps/DescriptionStep.tsx`

**信息:**
- 行数: 123
- 大小: 14331 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode, useCallback, useState } from 'react';
import { Box, Text } from '../../../../ink.js';
import { useKeybinding } from '../../../../keybindings/useKeybinding.js';
import { editPromptInEditor } from '../../../../utils/promptEditor.js';
import { ConfigurableShortcutHint } from '../../../ConfigurableShortcutHint.js';
import { Byline } from '../../../design-system/Byline.js';
import { KeyboardShortcutHint } from '../../../design-system/KeyboardShortcutHint.js';
import TextInput from '../../../TextInput.js';
import { useWizard } from '../../../wizard/index.js';
import { WizardDialogLayout } from '../../../wizard/WizardDialogLayout.js';
import type { AgentWizardData } from '../types.js';
export function DescriptionStep() {
  const $ = _c(18);
  const {
    goNext,
    goBack,
    updateWizardData,
    wizardData
  } = useWizard();
  const [whenToUse, setWhenToUse] = useState(wizardData.whenToUse || "");
  const [cursorOffset, setCursorOffset] = useState(whenToUse.length);
  const [error, setError] = useState(null);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = {
      context: "Settings"
    };
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  useKeybinding("confirm:no", goBack, t0);
  let t1;
  if ($[1] !== whenToUse) {
    t1 = async () => {
      const result = await editPromptInEditor(whenToUse);
      if (result.content !== null) {
        setWhenToUse(result.content);
        setCursorOffset(result.content.length);
      }
    };
    $[1] = whenToUse;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  const handleExternalEditor = t1;
  let t2;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {

```

---


### `src/components/agents/new-agent-creation/wizard-steps/GenerateStep.tsx`

**信息:**
- 行数: 143
- 大小: 22113 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { APIUserAbortError } from '@anthropic-ai/sdk';
import React, { type ReactNode, useCallback, useRef, useState } from 'react';
import { useMainLoopModel } from '../../../../hooks/useMainLoopModel.js';
import { Box, Text } from '../../../../ink.js';
import { useKeybinding } from '../../../../keybindings/useKeybinding.js';
import { createAbortController } from '../../../../utils/abortController.js';
import { editPromptInEditor } from '../../../../utils/promptEditor.js';
import { ConfigurableShortcutHint } from '../../../ConfigurableShortcutHint.js';
import { Byline } from '../../../design-system/Byline.js';
import { Spinner } from '../../../Spinner.js';
import TextInput from '../../../TextInput.js';
import { useWizard } from '../../../wizard/index.js';
import { WizardDialogLayout } from '../../../wizard/WizardDialogLayout.js';
import { generateAgent } from '../../generateAgent.js';
import type { AgentWizardData } from '../types.js';
export function GenerateStep(): ReactNode {
  const {
    updateWizardData,
    goBack,
    goToStep,
    wizardData
  } = useWizard<AgentWizardData>();
  const [prompt, setPrompt] = useState(wizardData.generationPrompt || '');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [cursorOffset, setCursorOffset] = useState(prompt.length);
  const model = useMainLoopModel();
  const abortControllerRef = useRef<AbortController | null>(null);

  // Cancel generation when escape pressed during generation
  const handleCancelGeneration = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
      setIsGenerating(false);
      setError('Generation cancelled');
    }
  }, []);

  // Use Settings context so 'n' key doesn't cancel (allows typing 'n' in prompt input)
  useKeybinding('confirm:no', handleCancelGeneration, {
    context: 'Settings',
    isActive: isGenerating
  });
  const handleExternalEditor = useCallback(async () => {
    const result = await editPromptInEditor(prompt);
    if (result.content !== null) {
      setPrompt(result.content);
      setCursorOffset(result.content.length);
    }

```

---


### `src/components/agents/new-agent-creation/wizard-steps/LocationStep.tsx`

**信息:**
- 行数: 80
- 大小: 8280 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode } from 'react';
import { Box } from '../../../../ink.js';
import type { SettingSource } from '../../../../utils/settings/constants.js';
import { ConfigurableShortcutHint } from '../../../ConfigurableShortcutHint.js';
import { Select } from '../../../CustomSelect/select.js';
import { Byline } from '../../../design-system/Byline.js';
import { KeyboardShortcutHint } from '../../../design-system/KeyboardShortcutHint.js';
import { useWizard } from '../../../wizard/index.js';
import { WizardDialogLayout } from '../../../wizard/WizardDialogLayout.js';
import type { AgentWizardData } from '../types.js';
export function LocationStep() {
  const $ = _c(11);
  const {
    goNext,
    updateWizardData,
    cancel
  } = useWizard();
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = {
      label: "Project (.claude/agents/)",
      value: "projectSettings" as SettingSource
    };
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  let t1;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = [t0, {
      label: "Personal (~/.claude/agents/)",
      value: "userSettings" as SettingSource
    }];
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const locationOptions = t1;
  let t2;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Byline><KeyboardShortcutHint shortcut={"\u2191\u2193"} action="navigate" /><KeyboardShortcutHint shortcut="Enter" action="select" /><ConfigurableShortcutHint action="confirm:no" context="Confirmation" fallback="Esc" description="cancel" /></Byline>;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  let t3;
  if ($[3] !== goNext || $[4] !== updateWizardData) {
    t3 = value => {
      updateWizardData({

```

---


### `src/components/agents/new-agent-creation/wizard-steps/MemoryStep.tsx`

**信息:**
- 行数: 113
- 大小: 14084 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode } from 'react';
import { Box } from '../../../../ink.js';
import { useKeybinding } from '../../../../keybindings/useKeybinding.js';
import { isAutoMemoryEnabled } from '../../../../memdir/paths.js';
import { type AgentMemoryScope, loadAgentMemoryPrompt } from '../../../../tools/AgentTool/agentMemory.js';
import { ConfigurableShortcutHint } from '../../../ConfigurableShortcutHint.js';
import { Select } from '../../../CustomSelect/select.js';
import { Byline } from '../../../design-system/Byline.js';
import { KeyboardShortcutHint } from '../../../design-system/KeyboardShortcutHint.js';
import { useWizard } from '../../../wizard/index.js';
import { WizardDialogLayout } from '../../../wizard/WizardDialogLayout.js';
import type { AgentWizardData } from '../types.js';
type MemoryOption = {
  label: string;
  value: AgentMemoryScope | 'none';
};
export function MemoryStep() {
  const $ = _c(13);
  const {
    goNext,
    goBack,
    updateWizardData,
    wizardData
  } = useWizard();
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = {
      context: "Confirmation"
    };
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  useKeybinding("confirm:no", goBack, t0);
  const isUserScope = wizardData.location === "userSettings";
  let t1;
  if ($[1] !== isUserScope) {
    t1 = isUserScope ? [{
      label: "User scope (~/.claude/agent-memory/) (Recommended)",
      value: "user"
    }, {
      label: "None (no persistent memory)",
      value: "none"
    }, {
      label: "Project scope (.claude/agent-memory/)",
      value: "project"
    }, {
      label: "Local scope (.claude/agent-memory-local/)",
      value: "local"

```

---


### `src/components/agents/new-agent-creation/wizard-steps/MethodStep.tsx`

**信息:**
- 行数: 80
- 大小: 8516 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode } from 'react';
import { Box } from '../../../../ink.js';
import { ConfigurableShortcutHint } from '../../../ConfigurableShortcutHint.js';
import { Select } from '../../../CustomSelect/select.js';
import { Byline } from '../../../design-system/Byline.js';
import { KeyboardShortcutHint } from '../../../design-system/KeyboardShortcutHint.js';
import { useWizard } from '../../../wizard/index.js';
import { WizardDialogLayout } from '../../../wizard/WizardDialogLayout.js';
import type { AgentWizardData } from '../types.js';
export function MethodStep() {
  const $ = _c(11);
  const {
    goNext,
    goBack,
    updateWizardData,
    goToStep
  } = useWizard();
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = [{
      label: "Generate with Claude (recommended)",
      value: "generate"
    }, {
      label: "Manual configuration",
      value: "manual"
    }];
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  const methodOptions = t0;
  let t1;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Byline><KeyboardShortcutHint shortcut={"\u2191\u2193"} action="navigate" /><KeyboardShortcutHint shortcut="Enter" action="select" /><ConfigurableShortcutHint action="confirm:no" context="Confirmation" fallback="Esc" description="go back" /></Byline>;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] !== goNext || $[3] !== goToStep || $[4] !== updateWizardData) {
    t2 = value => {
      const method = value as 'generate' | 'manual';
      updateWizardData({
        method,
        wasGenerated: method === "generate"
      });
      if (method === "generate") {
        goNext();
      } else {

```

---


### `src/components/agents/new-agent-creation/wizard-steps/ModelStep.tsx`

**信息:**
- 行数: 52
- 大小: 6321 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode } from 'react';
import { ConfigurableShortcutHint } from '../../../ConfigurableShortcutHint.js';
import { Byline } from '../../../design-system/Byline.js';
import { KeyboardShortcutHint } from '../../../design-system/KeyboardShortcutHint.js';
import { useWizard } from '../../../wizard/index.js';
import { WizardDialogLayout } from '../../../wizard/WizardDialogLayout.js';
import { ModelSelector } from '../../ModelSelector.js';
import type { AgentWizardData } from '../types.js';
export function ModelStep() {
  const $ = _c(8);
  const {
    goNext,
    goBack,
    updateWizardData,
    wizardData
  } = useWizard();
  let t0;
  if ($[0] !== goNext || $[1] !== updateWizardData) {
    t0 = model => {
      updateWizardData({
        selectedModel: model
      });
      goNext();
    };
    $[0] = goNext;
    $[1] = updateWizardData;
    $[2] = t0;
  } else {
    t0 = $[2];
  }
  const handleComplete = t0;
  let t1;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Byline><KeyboardShortcutHint shortcut={"\u2191\u2193"} action="navigate" /><KeyboardShortcutHint shortcut="Enter" action="select" /><ConfigurableShortcutHint action="confirm:no" context="Confirmation" fallback="Esc" description="go back" /></Byline>;
    $[3] = t1;
  } else {
    t1 = $[3];
  }
  let t2;
  if ($[4] !== goBack || $[5] !== handleComplete || $[6] !== wizardData.selectedModel) {
    t2 = <WizardDialogLayout subtitle="Select model" footerText={t1}><ModelSelector initialModel={wizardData.selectedModel} onComplete={handleComplete} onCancel={goBack} /></WizardDialogLayout>;
    $[4] = goBack;
    $[5] = handleComplete;
    $[6] = wizardData.selectedModel;
    $[7] = t2;
  } else {
    t2 = $[7];
  }
  return t2;

```

---


### `src/components/agents/new-agent-creation/wizard-steps/PromptStep.tsx`

**信息:**
- 行数: 128
- 大小: 14831 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode, useCallback, useState } from 'react';
import { Box, Text } from '../../../../ink.js';
import { useKeybinding } from '../../../../keybindings/useKeybinding.js';
import { editPromptInEditor } from '../../../../utils/promptEditor.js';
import { ConfigurableShortcutHint } from '../../../ConfigurableShortcutHint.js';
import { Byline } from '../../../design-system/Byline.js';
import { KeyboardShortcutHint } from '../../../design-system/KeyboardShortcutHint.js';
import TextInput from '../../../TextInput.js';
import { useWizard } from '../../../wizard/index.js';
import { WizardDialogLayout } from '../../../wizard/WizardDialogLayout.js';
import type { AgentWizardData } from '../types.js';
export function PromptStep() {
  const $ = _c(20);
  const {
    goNext,
    goBack,
    updateWizardData,
    wizardData
  } = useWizard();
  const [systemPrompt, setSystemPrompt] = useState(wizardData.systemPrompt || "");
  const [cursorOffset, setCursorOffset] = useState(systemPrompt.length);
  const [error, setError] = useState(null);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = {
      context: "Settings"
    };
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  useKeybinding("confirm:no", goBack, t0);
  let t1;
  if ($[1] !== systemPrompt) {
    t1 = async () => {
      const result = await editPromptInEditor(systemPrompt);
      if (result.content !== null) {
        setSystemPrompt(result.content);
        setCursorOffset(result.content.length);
      }
    };
    $[1] = systemPrompt;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  const handleExternalEditor = t1;
  let t2;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {

```

---


### `src/components/agents/new-agent-creation/wizard-steps/ToolsStep.tsx`

**信息:**
- 行数: 61
- 大小: 7220 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode } from 'react';
import type { Tools } from '../../../../Tool.js';
import { ConfigurableShortcutHint } from '../../../ConfigurableShortcutHint.js';
import { Byline } from '../../../design-system/Byline.js';
import { KeyboardShortcutHint } from '../../../design-system/KeyboardShortcutHint.js';
import { useWizard } from '../../../wizard/index.js';
import { WizardDialogLayout } from '../../../wizard/WizardDialogLayout.js';
import { ToolSelector } from '../../ToolSelector.js';
import type { AgentWizardData } from '../types.js';
type Props = {
  tools: Tools;
};
export function ToolsStep(t0) {
  const $ = _c(9);
  const {
    tools
  } = t0;
  const {
    goNext,
    goBack,
    updateWizardData,
    wizardData
  } = useWizard();
  let t1;
  if ($[0] !== goNext || $[1] !== updateWizardData) {
    t1 = selectedTools => {
      updateWizardData({
        selectedTools
      });
      goNext();
    };
    $[0] = goNext;
    $[1] = updateWizardData;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  const handleComplete = t1;
  const initialTools = wizardData.selectedTools;
  let t2;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Byline><KeyboardShortcutHint shortcut="Enter" action="toggle selection" /><KeyboardShortcutHint shortcut={"\u2191\u2193"} action="navigate" /><ConfigurableShortcutHint action="confirm:no" context="Confirmation" fallback="Esc" description="go back" /></Byline>;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  let t3;
  if ($[4] !== goBack || $[5] !== handleComplete || $[6] !== initialTools || $[7] !== tools) {
    t3 = <WizardDialogLayout subtitle="Select tools" footerText={t2}><ToolSelector tools={tools} initialTools={initialTools} onComplete={handleComplete} onCancel={goBack} /></WizardDialogLayout>;

```

---


### `src/components/agents/new-agent-creation/wizard-steps/TypeStep.tsx`

**信息:**
- 行数: 103
- 大小: 12474 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode, useState } from 'react';
import { Box, Text } from '../../../../ink.js';
import { useKeybinding } from '../../../../keybindings/useKeybinding.js';
import type { AgentDefinition } from '../../../../tools/AgentTool/loadAgentsDir.js';
import { ConfigurableShortcutHint } from '../../../ConfigurableShortcutHint.js';
import { Byline } from '../../../design-system/Byline.js';
import { KeyboardShortcutHint } from '../../../design-system/KeyboardShortcutHint.js';
import TextInput from '../../../TextInput.js';
import { useWizard } from '../../../wizard/index.js';
import { WizardDialogLayout } from '../../../wizard/WizardDialogLayout.js';
import { validateAgentType } from '../../validateAgent.js';
import type { AgentWizardData } from '../types.js';
type Props = {
  existingAgents: AgentDefinition[];
};
export function TypeStep(_props) {
  const $ = _c(15);
  const {
    goNext,
    goBack,
    updateWizardData,
    wizardData
  } = useWizard();
  const [agentType, setAgentType] = useState(wizardData.agentType || "");
  const [error, setError] = useState(null);
  const [cursorOffset, setCursorOffset] = useState(agentType.length);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = {
      context: "Settings"
    };
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  useKeybinding("confirm:no", goBack, t0);
  let t1;
  if ($[1] !== goNext || $[2] !== updateWizardData) {
    t1 = value => {
      const trimmedValue = value.trim();
      const validationError = validateAgentType(trimmedValue);
      if (validationError) {
        setError(validationError);
        return;
      }
      setError(null);
      updateWizardData({
        agentType: trimmedValue
      });

```

---


### `src/components/agents/types.ts`

**信息:**
- 行数: 6
- 大小: 129 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const AGENT_PATHS = {
  project: '.claude/agents',
  user: '~/.claude/agents',
} as const

export type ModeState = string

```

---


### `src/components/agents/utils.ts`

**信息:**
- 行数: 18
- 大小: 528 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import capitalize from 'lodash-es/capitalize.js'
import type { SettingSource } from 'src/utils/settings/constants.js'
import { getSettingSourceName } from 'src/utils/settings/constants.js'

export function getAgentSourceDisplayName(
  source: SettingSource | 'all' | 'built-in' | 'plugin',
): string {
  if (source === 'all') {
    return 'Agents'
  }
  if (source === 'built-in') {
    return 'Built-in agents'
  }
  if (source === 'plugin') {
    return 'Plugin agents'
  }
  return capitalize(getSettingSourceName(source))
}

```

---


### `src/components/agents/validateAgent.ts`

**信息:**
- 行数: 109
- 大小: 3150 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Tools } from '../../Tool.js'
import { resolveAgentTools } from '../../tools/AgentTool/agentToolUtils.js'
import type {
  AgentDefinition,
  CustomAgentDefinition,
} from '../../tools/AgentTool/loadAgentsDir.js'
import { getAgentSourceDisplayName } from './utils.js'

export type AgentValidationResult = {
  isValid: boolean
  errors: string[]
  warnings: string[]
}

export function validateAgentType(agentType: string): string | null {
  if (!agentType) {
    return 'Agent type is required'
  }

  if (!/^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$/.test(agentType)) {
    return 'Agent type must start and end with alphanumeric characters and contain only letters, numbers, and hyphens'
  }

  if (agentType.length < 3) {
    return 'Agent type must be at least 3 characters long'
  }

  if (agentType.length > 50) {
    return 'Agent type must be less than 50 characters'
  }

  return null
}

export function validateAgent(
  agent: Omit<CustomAgentDefinition, 'location'>,
  availableTools: Tools,
  existingAgents: AgentDefinition[],
): AgentValidationResult {
  const errors: string[] = []
  const warnings: string[] = []

  // Validate agent type
  if (!agent.agentType) {
    errors.push('Agent type is required')
  } else {
    const typeError = validateAgentType(agent.agentType)
    if (typeError) {
      errors.push(typeError)
    }

```

---


### `src/components/design-system/Byline.tsx`

**信息:**
- 行数: 77
- 大小: 6493 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { Children, isValidElement } from 'react';
import { Text } from '../../ink.js';
type Props = {
  /** The items to join with a middot separator */
  children: React.ReactNode;
};

/**
 * Joins children with a middot separator (" · ") for inline metadata display.
 *
 * Named after the publishing term "byline" - the line of metadata typically
 * shown below a title (e.g., "John Doe · 5 min read · Mar 12").
 *
 * Automatically filters out null/undefined/false children and only renders
 * separators between valid elements.
 *
 * @example
 * // Basic usage: "Enter to confirm · Esc to cancel"
 * <Text dimColor>
 *   <Byline>
 *     <KeyboardShortcutHint shortcut="Enter" action="confirm" />
 *     <KeyboardShortcutHint shortcut="Esc" action="cancel" />
 *   </Byline>
 * </Text>
 *
 * @example
 * // With conditional children: "Esc to cancel" (only one item shown)
 * <Text dimColor>
 *   <Byline>
 *     {showEnter && <KeyboardShortcutHint shortcut="Enter" action="confirm" />}
 *     <KeyboardShortcutHint shortcut="Esc" action="cancel" />
 *   </Byline>
 * </Text>
 *
 */
export function Byline(t0) {
  const $ = _c(5);
  const {
    children
  } = t0;
  let t1;
  let t2;
  if ($[0] !== children) {
    t2 = Symbol.for("react.early_return_sentinel");
    bb0: {
      const validChildren = Children.toArray(children);
      if (validChildren.length === 0) {
        t2 = null;
        break bb0;

```

---


### `src/components/design-system/Dialog.tsx`

**信息:**
- 行数: 138
- 大小: 14112 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { type ExitState, useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import type { Theme } from '../../utils/theme.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Byline } from './Byline.js';
import { KeyboardShortcutHint } from './KeyboardShortcutHint.js';
import { Pane } from './Pane.js';
type DialogProps = {
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  children: React.ReactNode;
  onCancel: () => void;
  color?: keyof Theme;
  hideInputGuide?: boolean;
  hideBorder?: boolean;
  /** Custom input guide content. Receives exitState for Ctrl+C/D pending display. */
  inputGuide?: (exitState: ExitState) => React.ReactNode;
  /**
   * Controls whether Dialog's built-in confirm:no (Esc/n) and app:exit/interrupt
   * (Ctrl-C/D) keybindings are active. Set to `false` while an embedded text
   * field is being edited so those keys reach the field instead of being
   * consumed by Dialog. TextInput has its own ctrl+c/d handlers (cancel on
   * press, delete-forward on ctrl+d with text). Defaults to `true`.
   */
  isCancelActive?: boolean;
};
export function Dialog(t0) {
  const $ = _c(27);
  const {
    title,
    subtitle,
    children,
    onCancel,
    color: t1,
    hideInputGuide,
    hideBorder,
    inputGuide,
    isCancelActive: t2
  } = t0;
  const color = t1 === undefined ? "permission" : t1;
  const isCancelActive = t2 === undefined ? true : t2;
  const exitState = useExitOnCtrlCDWithKeybindings(undefined, undefined, isCancelActive);
  let t3;
  if ($[0] !== isCancelActive) {
    t3 = {
      context: "Confirmation",
      isActive: isCancelActive

```

---


### `src/components/design-system/Divider.tsx`

**信息:**
- 行数: 149
- 大小: 11094 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { Ansi, Text } from '../../ink.js';
import type { Theme } from '../../utils/theme.js';
type DividerProps = {
  /**
   * Width of the divider in characters.
   * Defaults to terminal width.
   */
  width?: number;

  /**
   * Theme color for the divider.
   * If not provided, dimColor is used.
   */
  color?: keyof Theme;

  /**
   * Character to use for the divider line.
   * @default '─'
   */
  char?: string;

  /**
   * Padding to subtract from the width (e.g., for indentation).
   * @default 0
   */
  padding?: number;

  /**
   * Title shown in the middle of the divider.
   * May contain ANSI codes (e.g., chalk-styled text).
   *
   * @example
   * // ─────────── Title ───────────
   * <Divider title="Title" />
   */
  title?: string;
};

/**
 * A horizontal divider line.
 *
 * @example
 * // Full-width dimmed divider
 * <Divider />
 *
 * @example

```

---


### `src/components/design-system/FuzzyPicker.tsx`

**信息:**
- 行数: 312
- 大小: 40862 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useEffect, useState } from 'react';
import { useSearchInput } from '../../hooks/useSearchInput.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { clamp } from '../../ink/layout/geometry.js';
import { Box, Text, useTerminalFocus } from '../../ink.js';
import { SearchBox } from '../SearchBox.js';
import { Byline } from './Byline.js';
import { KeyboardShortcutHint } from './KeyboardShortcutHint.js';
import { ListItem } from './ListItem.js';
import { Pane } from './Pane.js';
type PickerAction<T> = {
  /** Hint label shown in the byline, e.g. "mention" → "Tab to mention". */
  action: string;
  handler: (item: T) => void;
};
type Props<T> = {
  title: string;
  placeholder?: string;
  initialQuery?: string;
  items: readonly T[];
  getKey: (item: T) => string;
  /** Keep to one line — preview handles overflow. */
  renderItem: (item: T, isFocused: boolean) => React.ReactNode;
  renderPreview?: (item: T) => React.ReactNode;
  /** 'right' keeps hints stable (no bounce), but needs width. */
  previewPosition?: 'bottom' | 'right';
  visibleCount?: number;
  /**
   * 'up' puts items[0] at the bottom next to the input (atuin-style). Arrows
   * always match screen direction — ↑ walks visually up regardless.
   */
  direction?: 'down' | 'up';
  /** Caller owns filtering: re-filter on each call and pass new items. */
  onQueryChange: (query: string) => void;
  /** Enter key. Primary action. */
  onSelect: (item: T) => void;
  /**
   * Tab key. If provided, Tab no longer aliases Enter — it gets its own
   * handler and hint. Shift+Tab falls through to this if onShiftTab is unset.
   */
  onTab?: PickerAction<T>;
  /** Shift+Tab key. Gets its own hint. */
  onShiftTab?: PickerAction<T>;
  /**
   * Fires when the focused item changes (via arrows or when items reset).
   * Useful for async preview loading — keeps I/O out of renderPreview.
   */

```

---


### `src/components/design-system/KeyboardShortcutHint.tsx`

**信息:**
- 行数: 81
- 大小: 6847 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import Text from '../../ink/components/Text.js';
type Props = {
  /** The key or chord to display (e.g., "ctrl+o", "Enter", "↑/↓") */
  shortcut: string;
  /** The action the key performs (e.g., "expand", "select", "navigate") */
  action: string;
  /** Whether to wrap the hint in parentheses. Default: false */
  parens?: boolean;
  /** Whether to render the shortcut in bold. Default: false */
  bold?: boolean;
};

/**
 * Renders a keyboard shortcut hint like "ctrl+o to expand" or "(tab to toggle)"
 *
 * Wrap in <Text dimColor> for the common dim styling.
 *
 * @example
 * // Simple hint wrapped in dim Text
 * <Text dimColor><KeyboardShortcutHint shortcut="esc" action="cancel" /></Text>
 *
 * // With parentheses: "(ctrl+o to expand)"
 * <Text dimColor><KeyboardShortcutHint shortcut="ctrl+o" action="expand" parens /></Text>
 *
 * // With bold shortcut: "Enter to confirm" (Enter is bold)
 * <Text dimColor><KeyboardShortcutHint shortcut="Enter" action="confirm" bold /></Text>
 *
 * // Multiple hints with middot separator - use Byline
 * <Text dimColor>
 *   <Byline>
 *     <KeyboardShortcutHint shortcut="Enter" action="confirm" />
 *     <KeyboardShortcutHint shortcut="Esc" action="cancel" />
 *   </Byline>
 * </Text>
 */
export function KeyboardShortcutHint(t0) {
  const $ = _c(9);
  const {
    shortcut,
    action,
    parens: t1,
    bold: t2
  } = t0;
  const parens = t1 === undefined ? false : t1;
  const bold = t2 === undefined ? false : t2;
  let t3;
  if ($[0] !== bold || $[1] !== shortcut) {
    t3 = bold ? <Text bold={true}>{shortcut}</Text> : shortcut;

```

---


### `src/components/design-system/ListItem.tsx`

**信息:**
- 行数: 244
- 大小: 19535 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import type { ReactNode } from 'react';
import React from 'react';
import { useDeclaredCursor } from '../../ink/hooks/use-declared-cursor.js';
import { Box, Text } from '../../ink.js';
type ListItemProps = {
  /**
   * Whether this item is currently focused (keyboard selection).
   * Shows the pointer indicator (❯) when true.
   */
  isFocused: boolean;

  /**
   * Whether this item is selected (chosen/checked).
   * Shows the checkmark indicator (✓) when true.
   * @default false
   */
  isSelected?: boolean;

  /**
   * The content to display for this item.
   */
  children: ReactNode;

  /**
   * Optional description text displayed below the main content.
   */
  description?: string;

  /**
   * Show a down arrow indicator instead of pointer (for scroll hints).
   * Only applies when not focused.
   */
  showScrollDown?: boolean;

  /**
   * Show an up arrow indicator instead of pointer (for scroll hints).
   * Only applies when not focused.
   */
  showScrollUp?: boolean;

  /**
   * Whether to apply automatic styling to the children based on focus/selection state.
   * - When true (default): children are wrapped in Text with state-based colors
   * - When false: children are rendered as-is, allowing custom styling
   * @default true
   */
  styled?: boolean;


```

---


### `src/components/design-system/LoadingState.tsx`

**信息:**
- 行数: 94
- 大小: 6448 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../../ink.js';
import { Spinner } from '../Spinner.js';
type LoadingStateProps = {
  /**
   * The loading message to display next to the spinner.
   */
  message: string;

  /**
   * Display the message in bold.
   * @default false
   */
  bold?: boolean;

  /**
   * Display the message in dimmed color.
   * @default false
   */
  dimColor?: boolean;

  /**
   * Optional subtitle displayed below the main message.
   */
  subtitle?: string;
};

/**
 * A spinner with loading message for async operations.
 *
 * @example
 * // Basic loading
 * <LoadingState message="Loading..." />
 *
 * @example
 * // Bold loading message
 * <LoadingState message="Loading sessions" bold />
 *
 * @example
 * // With subtitle
 * <LoadingState
 *   message="Loading sessions"
 *   bold
 *   subtitle="Fetching your Claude Code sessions..."
 * />
 */
export function LoadingState(t0) {
  const $ = _c(10);
  const {

```

---


### `src/components/design-system/Pane.tsx`

**信息:**
- 行数: 77
- 大小: 6907 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { useIsInsideModal } from '../../context/modalContext.js';
import { Box } from '../../ink.js';
import type { Theme } from '../../utils/theme.js';
import { Divider } from './Divider.js';
type PaneProps = {
  children: React.ReactNode;
  /**
   * Theme color for the top border line.
   */
  color?: keyof Theme;
};

/**
 * A pane — a region of the terminal that appears below the REPL prompt,
 * bounded by a colored top line with a one-row gap above and horizontal
 * padding. Used by all slash-command screens: /config, /help, /plugins,
 * /sandbox, /stats, /permissions.
 *
 * For confirm/cancel dialogs (Esc to dismiss, Enter to confirm), use
 * `<Dialog>` instead — it registers its own keybindings. For a full
 * rounded-border card, use `<Panel>`.
 *
 * Submenus rendered inside a Pane should use `hideBorder` on their Dialog
 * so the Pane's border remains the single frame.
 *
 * @example
 * <Pane color="permission">
 *   <Tabs title="Sandbox:">...</Tabs>
 * </Pane>
 */
export function Pane(t0) {
  const $ = _c(9);
  const {
    children,
    color
  } = t0;
  if (useIsInsideModal()) {
    let t1;
    if ($[0] !== children) {
      t1 = <Box flexDirection="column" paddingX={1} flexShrink={0}>{children}</Box>;
      $[0] = children;
      $[1] = t1;
    } else {
      t1 = $[1];
    }
    return t1;
  }
  let t1;

```

---


### `src/components/design-system/ProgressBar.tsx`

**信息:**
- 行数: 86
- 大小: 7170 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Text } from '../../ink.js';
import type { Theme } from '../../utils/theme.js';
type Props = {
  /**
   * How much progress to display, between 0 and 1 inclusive
   */
  ratio: number; // [0, 1]

  /**
   * How many characters wide to draw the progress bar
   */
  width: number; // how many characters wide

  /**
   * Optional color for the filled portion of the bar
   */
  fillColor?: keyof Theme;

  /**
   * Optional color for the empty portion of the bar
   */
  emptyColor?: keyof Theme;
};
const BLOCKS = [' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█'];
export function ProgressBar(t0) {
  const $ = _c(13);
  const {
    ratio: inputRatio,
    width,
    fillColor,
    emptyColor
  } = t0;
  const ratio = Math.min(1, Math.max(0, inputRatio));
  const whole = Math.floor(ratio * width);
  let t1;
  if ($[0] !== whole) {
    t1 = BLOCKS[BLOCKS.length - 1].repeat(whole);
    $[0] = whole;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let segments;
  if ($[2] !== ratio || $[3] !== t1 || $[4] !== whole || $[5] !== width) {
    segments = [t1];
    if (whole < width) {
      const remainder = ratio * width - whole;
      const middle = Math.floor(remainder * BLOCKS.length);

```

---


### `src/components/design-system/Ratchet.tsx`

**信息:**
- 行数: 80
- 大小: 7166 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useLayoutEffect, useRef, useState } from 'react';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { useTerminalViewport } from '../../ink/hooks/use-terminal-viewport.js';
import { Box, type DOMElement, measureElement } from '../../ink.js';
type Props = {
  children: React.ReactNode;
  lock?: 'always' | 'offscreen';
};
export function Ratchet(t0) {
  const $ = _c(10);
  const {
    children,
    lock: t1
  } = t0;
  const lock = t1 === undefined ? "always" : t1;
  const [viewportRef, t2] = useTerminalViewport();
  const {
    isVisible
  } = t2;
  const {
    rows
  } = useTerminalSize();
  const innerRef = useRef(null);
  const maxHeight = useRef(0);
  const [minHeight, setMinHeight] = useState(0);
  let t3;
  if ($[0] !== viewportRef) {
    t3 = el => {
      viewportRef(el);
    };
    $[0] = viewportRef;
    $[1] = t3;
  } else {
    t3 = $[1];
  }
  const outerRef = t3;
  const engaged = lock === "always" || !isVisible;
  let t4;
  if ($[2] !== rows) {
    t4 = () => {
      if (!innerRef.current) {
        return;
      }
      const {
        height
      } = measureElement(innerRef.current);
      if (height > maxHeight.current) {
        maxHeight.current = Math.min(height, rows);
        setMinHeight(maxHeight.current);

```

---


### `src/components/design-system/StatusIcon.tsx`

**信息:**
- 行数: 95
- 大小: 7568 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React from 'react';
import { Text } from '../../ink.js';
type Status = 'success' | 'error' | 'warning' | 'info' | 'pending' | 'loading';
type Props = {
  /**
   * The status to display. Determines both the icon and color.
   *
   * - `success`: Green checkmark (✓)
   * - `error`: Red cross (✗)
   * - `warning`: Yellow warning symbol (⚠)
   * - `info`: Blue info symbol (ℹ)
   * - `pending`: Dimmed circle (○)
   * - `loading`: Dimmed ellipsis (…)
   */
  status: Status;
  /**
   * Include a trailing space after the icon. Useful when followed by text.
   * @default false
   */
  withSpace?: boolean;
};
const STATUS_CONFIG: Record<Status, {
  icon: string;
  color: 'success' | 'error' | 'warning' | 'suggestion' | undefined;
}> = {
  success: {
    icon: figures.tick,
    color: 'success'
  },
  error: {
    icon: figures.cross,
    color: 'error'
  },
  warning: {
    icon: figures.warning,
    color: 'warning'
  },
  info: {
    icon: figures.info,
    color: 'suggestion'
  },
  pending: {
    icon: figures.circle,
    color: undefined
  },
  loading: {
    icon: '…',
    color: undefined

```

---


### `src/components/design-system/Tabs.tsx`

**信息:**
- 行数: 340
- 大小: 41447 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { useIsInsideModal, useModalScrollRef } from '../../context/modalContext.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import ScrollBox from '../../ink/components/ScrollBox.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { Box, Text } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import type { Theme } from '../../utils/theme.js';
type TabsProps = {
  children: Array<React.ReactElement<TabProps>>;
  title?: string;
  color?: keyof Theme;
  defaultTab?: string;
  hidden?: boolean;
  useFullWidth?: boolean;
  /** Controlled mode: current selected tab id/title */
  selectedTab?: string;
  /** Controlled mode: callback when tab changes */
  onTabChange?: (tabId: string) => void;
  /** Optional banner to display below tabs header */
  banner?: React.ReactNode;
  /** Disable keyboard navigation (e.g. when a child component handles arrow keys) */
  disableNavigation?: boolean;
  /**
   * Initial focus state for the tab header row. Defaults to true (header
   * focused, nav always works). Keep the default for Select/list content —
   * those only use up/down so there's no conflict; pass
   * isDisabled={headerFocused} to the Select instead. Only set false when
   * content actually binds left/right/tab (e.g. enum cycling), and show a
   * "↑ tabs" footer hint — without it tabs look broken.
   */
  initialHeaderFocused?: boolean;
  /**
   * Fixed height for the content area. When set, all tabs render within the
   * same height (overflow hidden) so switching tabs doesn't cause layout
   * shifts. Shorter tabs get whitespace; taller tabs are clipped.
   */
  contentHeight?: number;
  /**
   * Let Tab/←/→ switch tabs from focused content. Opt-in since some
   * content uses those keys; pass a reactive boolean to cede them when
   * needed. Switching from content focuses the header.
   */
  navFromContent?: boolean;
};
type TabsContextValue = {
  selectedTab: string | undefined;
  width: number | undefined;

```

---


### `src/components/design-system/ThemeProvider.tsx`

**信息:**
- 行数: 170
- 大小: 18852 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import React, { createContext, useContext, useEffect, useMemo, useState } from 'react';
import useStdin from '../../ink/hooks/use-stdin.js';
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js';
import { getSystemThemeName, type SystemTheme } from '../../utils/systemTheme.js';
import type { ThemeName, ThemeSetting } from '../../utils/theme.js';
type ThemeContextValue = {
  /** The saved user preference. May be 'auto'. */
  themeSetting: ThemeSetting;
  setThemeSetting: (setting: ThemeSetting) => void;
  setPreviewTheme: (setting: ThemeSetting) => void;
  savePreview: () => void;
  cancelPreview: () => void;
  /** The resolved theme to render with. Never 'auto'. */
  currentTheme: ThemeName;
};

// Non-'auto' default so useTheme() works without a provider (tests, tooling).
const DEFAULT_THEME: ThemeName = 'dark';
const ThemeContext = createContext<ThemeContextValue>({
  themeSetting: DEFAULT_THEME,
  setThemeSetting: () => {},
  setPreviewTheme: () => {},
  savePreview: () => {},
  cancelPreview: () => {},
  currentTheme: DEFAULT_THEME
});
type Props = {
  children: React.ReactNode;
  initialState?: ThemeSetting;
  onThemeSave?: (setting: ThemeSetting) => void;
};
function defaultInitialTheme(): ThemeSetting {
  return getGlobalConfig().theme;
}
function defaultSaveTheme(setting: ThemeSetting): void {
  saveGlobalConfig(current => ({
    ...current,
    theme: setting
  }));
}
export function ThemeProvider({
  children,
  initialState,
  onThemeSave = defaultSaveTheme
}: Props) {
  const [themeSetting, setThemeSetting] = useState(initialState ?? defaultInitialTheme);
  const [previewTheme, setPreviewTheme] = useState<ThemeSetting | null>(null);


```

---


### `src/components/design-system/ThemedBox.tsx`

**信息:**
- 行数: 156
- 大小: 18043 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type PropsWithChildren, type Ref } from 'react';
import Box from '../../ink/components/Box.js';
import type { DOMElement } from '../../ink/dom.js';
import type { ClickEvent } from '../../ink/events/click-event.js';
import type { FocusEvent } from '../../ink/events/focus-event.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import type { Color, Styles } from '../../ink/styles.js';
import { getTheme, type Theme } from '../../utils/theme.js';
import { useTheme } from './ThemeProvider.js';

// Color props that accept theme keys
type ThemedColorProps = {
  readonly borderColor?: keyof Theme | Color;
  readonly borderTopColor?: keyof Theme | Color;
  readonly borderBottomColor?: keyof Theme | Color;
  readonly borderLeftColor?: keyof Theme | Color;
  readonly borderRightColor?: keyof Theme | Color;
  readonly backgroundColor?: keyof Theme | Color;
};

// Base Styles without color props (they'll be overridden)
type BaseStylesWithoutColors = Omit<Styles, 'textWrap' | 'borderColor' | 'borderTopColor' | 'borderBottomColor' | 'borderLeftColor' | 'borderRightColor' | 'backgroundColor'>;
export type Props = BaseStylesWithoutColors & ThemedColorProps & {
  ref?: Ref<DOMElement>;
  tabIndex?: number;
  autoFocus?: boolean;
  onClick?: (event: ClickEvent) => void;
  onFocus?: (event: FocusEvent) => void;
  onFocusCapture?: (event: FocusEvent) => void;
  onBlur?: (event: FocusEvent) => void;
  onBlurCapture?: (event: FocusEvent) => void;
  onKeyDown?: (event: KeyboardEvent) => void;
  onKeyDownCapture?: (event: KeyboardEvent) => void;
  onMouseEnter?: () => void;
  onMouseLeave?: () => void;
};

/**
 * Resolves a color value that may be a theme key to a raw Color.
 */
function resolveColor(color: keyof Theme | Color | undefined, theme: Theme): Color | undefined {
  if (!color) return undefined;
  // Check if it's a raw color (starts with rgb(, #, ansi256(, or ansi:)
  if (color.startsWith('rgb(') || color.startsWith('#') || color.startsWith('ansi256(') || color.startsWith('ansi:')) {
    return color as Color;
  }
  // It's a theme key - resolve it
  return theme[color as keyof Theme] as Color;
}

```

---


### `src/components/design-system/ThemedText.tsx`

**信息:**
- 行数: 124
- 大小: 13877 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ReactNode } from 'react';
import React, { useContext } from 'react';
import Text from '../../ink/components/Text.js';
import type { Color, Styles } from '../../ink/styles.js';
import { getTheme, type Theme } from '../../utils/theme.js';
import { useTheme } from './ThemeProvider.js';

/** Colors uncolored ThemedText in the subtree. Precedence: explicit `color` >
 *  this > dimColor. Crosses Box boundaries (Ink's style cascade doesn't). */
export const TextHoverColorContext = React.createContext<keyof Theme | undefined>(undefined);
export type Props = {
  /**
   * Change text color. Accepts a theme key or raw color value.
   */
  readonly color?: keyof Theme | Color;

  /**
   * Same as `color`, but for background. Must be a theme key.
   */
  readonly backgroundColor?: keyof Theme;

  /**
   * Dim the color using the theme's inactive color.
   * This is compatible with bold (unlike ANSI dim).
   */
  readonly dimColor?: boolean;

  /**
   * Make the text bold.
   */
  readonly bold?: boolean;

  /**
   * Make the text italic.
   */
  readonly italic?: boolean;

  /**
   * Make the text underlined.
   */
  readonly underline?: boolean;

  /**
   * Make the text crossed with a line.
   */
  readonly strikethrough?: boolean;

  /**
   * Inverse background and foreground colors.

```

---


### `src/components/design-system/color.ts`

**信息:**
- 行数: 30
- 大小: 853 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { type ColorType, colorize } from '../../ink/colorize.js'
import type { Color } from '../../ink/styles.js'
import { getTheme, type Theme, type ThemeName } from '../../utils/theme.js'

/**
 * Curried theme-aware color function. Resolves theme keys to raw color
 * values before delegating to the ink renderer's colorize.
 */
export function color(
  c: keyof Theme | Color | undefined,
  theme: ThemeName,
  type: ColorType = 'foreground',
): (text: string) => string {
  return text => {
    if (!c) {
      return text
    }
    // Raw color values bypass theme lookup
    if (
      c.startsWith('rgb(') ||
      c.startsWith('#') ||
      c.startsWith('ansi256(') ||
      c.startsWith('ansi:')
    ) {
      return colorize(text, c, type)
    }
    // Theme key lookup
    return colorize(text, getTheme(theme)[c as keyof Theme], type)
  }
}

```

---


### `src/components/diff/DiffDetailView.tsx`

**信息:**
- 行数: 281
- 大小: 22615 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { StructuredPatchHunk } from 'diff';
import { resolve } from 'path';
import React, { useMemo } from 'react';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { Box, Text } from '../../ink.js';
import { getCwd } from '../../utils/cwd.js';
import { readFileSafe } from '../../utils/file.js';
import { Divider } from '../design-system/Divider.js';
import { StructuredDiff } from '../StructuredDiff.js';
type Props = {
  filePath: string;
  hunks: StructuredPatchHunk[];
  isLargeFile?: boolean;
  isBinary?: boolean;
  isTruncated?: boolean;
  isUntracked?: boolean;
};

/**
 * Displays the diff content for a single file.
 * Uses StructuredDiff for word-level diffing and syntax highlighting.
 * No scrolling - renders all lines (max 400 due to parsing limits).
 */
export function DiffDetailView(t0) {
  const $ = _c(53);
  const {
    filePath,
    hunks,
    isLargeFile,
    isBinary,
    isTruncated,
    isUntracked
  } = t0;
  const {
    columns
  } = useTerminalSize();
  let t1;
  bb0: {
    if (!filePath) {
      let t2;
      if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
        t2 = {
          firstLine: null,
          fileContent: undefined
        };
        $[0] = t2;
      } else {
        t2 = $[0];
      }

```

---


### `src/components/diff/DiffDialog.tsx`

**信息:**
- 行数: 383
- 大小: 43407 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { StructuredPatchHunk } from 'diff';
import React, { useEffect, useMemo, useRef, useState } from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { useRegisterOverlay } from '../../context/overlayContext.js';
import { type DiffData, useDiffData } from '../../hooks/useDiffData.js';
import { type TurnDiff, useTurnDiffs } from '../../hooks/useTurnDiffs.js';
import { Box, Text } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import { useShortcutDisplay } from '../../keybindings/useShortcutDisplay.js';
import type { Message } from '../../types/message.js';
import { plural } from '../../utils/stringUtils.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { DiffDetailView } from './DiffDetailView.js';
import { DiffFileList } from './DiffFileList.js';
type Props = {
  messages: Message[];
  onDone: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
type ViewMode = 'list' | 'detail';
type DiffSource = {
  type: 'current';
} | {
  type: 'turn';
  turn: TurnDiff;
};
function turnDiffToDiffData(turn: TurnDiff): DiffData {
  const files = Array.from(turn.files.values()).map(f => ({
    path: f.filePath,
    linesAdded: f.linesAdded,
    linesRemoved: f.linesRemoved,
    isBinary: false,
    isLargeFile: false,
    isTruncated: false,
    isNewFile: f.isNewFile
  })).sort((a, b) => a.path.localeCompare(b.path));
  const hunks = new Map<string, StructuredPatchHunk[]>();
  for (const f of turn.files.values()) {
    hunks.set(f.filePath, f.hunks);
  }
  return {
    stats: {
      filesCount: turn.stats.filesChanged,
      linesAdded: turn.stats.linesAdded,
      linesRemoved: turn.stats.linesRemoved
    },
    files,

```

---


### `src/components/diff/DiffFileList.tsx`

**信息:**
- 行数: 292
- 大小: 25342 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { useMemo } from 'react';
import type { DiffFile } from '../../hooks/useDiffData.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { Box, Text } from '../../ink.js';
import { truncateStartToWidth } from '../../utils/format.js';
import { plural } from '../../utils/stringUtils.js';
const MAX_VISIBLE_FILES = 5;
type Props = {
  files: DiffFile[];
  selectedIndex: number;
};
export function DiffFileList(t0) {
  const $ = _c(36);
  const {
    files,
    selectedIndex
  } = t0;
  const {
    columns
  } = useTerminalSize();
  let t1;
  bb0: {
    if (files.length === 0 || files.length <= MAX_VISIBLE_FILES) {
      let t2;
      if ($[0] !== files.length) {
        t2 = {
          startIndex: 0,
          endIndex: files.length
        };
        $[0] = files.length;
        $[1] = t2;
      } else {
        t2 = $[1];
      }
      t1 = t2;
      break bb0;
    }
    let start = Math.max(0, selectedIndex - Math.floor(MAX_VISIBLE_FILES / 2));
    let end = start + MAX_VISIBLE_FILES;
    if (end > files.length) {
      end = files.length;
      start = Math.max(0, end - MAX_VISIBLE_FILES);
    }
    let t2;
    if ($[2] !== end || $[3] !== start) {
      t2 = {
        startIndex: start,
        endIndex: end

```

---


### `src/components/grove/Grove.tsx`

**信息:**
- 行数: 463
- 大小: 49525 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useEffect, useState } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { Box, Link, Text, useInput } from '../../ink.js';
import { type AccountSettings, calculateShouldShowGrove, type GroveConfig, getGroveNoticeConfig, getGroveSettings, markGroveNoticeViewed, updateGroveSettings } from '../../services/api/grove.js';
import { Select } from '../CustomSelect/index.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
export type GroveDecision = 'accept_opt_in' | 'accept_opt_out' | 'defer' | 'escape' | 'skip_rendering';
type Props = {
  showIfAlreadyViewed: boolean;
  location: 'settings' | 'policy_update_modal' | 'onboarding';
  onDone(decision: GroveDecision): void;
};
const NEW_TERMS_ASCII = ` _____________
 |          \\  \\
 | NEW TERMS \\__\\
 |              |
 |  ----------  |
 |  ----------  |
 |  ----------  |
 |  ----------  |
 |  ----------  |
 |              |
 |______________|`;
function GracePeriodContentBody() {
  const $ = _c(9);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <Text>An update to our Consumer Terms and Privacy Policy will take effect on{" "}<Text bold={true}>October 8, 2025</Text>. You can accept the updated terms today.</Text>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  let t1;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Text>What's changing?</Text>;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  let t3;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Text>· </Text>;
    t3 = <Text bold={true}>You can help improve Claude </Text>;
    $[2] = t2;
    $[3] = t3;
  } else {

```

---


### `src/components/hooks/HooksConfigMenu.tsx`

**信息:**
- 行数: 578
- 大小: 54469 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * HooksConfigMenu is a read-only browser for configured hooks.
 *
 * Users can drill into each hook event, see configured matchers and hooks
 * (of any type: command, prompt, agent, http), and view individual hook
 * details. To add or modify hooks, users should edit settings.json directly
 * or ask Claude — the menu directs them there.
 *
 * The menu is read-only because the old editing UI only supported
 * command-type hooks and duplicating the settings.json editing surface
 * in-menu for all four types would be a maintenance burden.
 */
import * as React from 'react';
import { useCallback, useMemo, useState } from 'react';
import type { HookEvent } from 'src/entrypoints/agentSdkTypes.js';
import { useAppState, useAppStateStore } from 'src/state/AppState.js';
import type { CommandResultDisplay } from '../../commands.js';
import { useSettingsChange } from '../../hooks/useSettingsChange.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { getHookEventMetadata, getHooksForMatcher, getMatcherMetadata, getSortedMatchersForEvent, groupHooksByEventAndMatcher } from '../../utils/hooks/hooksConfigManager.js';
import type { IndividualHookConfig } from '../../utils/hooks/hooksSettings.js';
import { getSettings_DEPRECATED, getSettingsForSource } from '../../utils/settings/settings.js';
import { plural } from '../../utils/stringUtils.js';
import { Dialog } from '../design-system/Dialog.js';
import { SelectEventMode } from './SelectEventMode.js';
import { SelectHookMode } from './SelectHookMode.js';
import { SelectMatcherMode } from './SelectMatcherMode.js';
import { ViewHookMode } from './ViewHookMode.js';
type Props = {
  toolNames: string[];
  onExit: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
type ModeState = {
  mode: 'select-event';
} | {
  mode: 'select-matcher';
  event: HookEvent;
} | {
  mode: 'select-hook';
  event: HookEvent;
  matcher: string;
} | {
  mode: 'view-hook';
  event: HookEvent;
  hook: IndividualHookConfig;
};

```

---


### `src/components/hooks/PromptDialog.tsx`

**信息:**
- 行数: 90
- 大小: 7482 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import type { PromptRequest } from '../../types/hooks.js';
import { Select } from '../CustomSelect/select.js';
import { PermissionDialog } from '../permissions/PermissionDialog.js';
type Props = {
  title: string;
  toolInputSummary?: string | null;
  request: PromptRequest;
  onRespond: (key: string) => void;
  onAbort: () => void;
};
export function PromptDialog(t0) {
  const $ = _c(15);
  const {
    title,
    toolInputSummary,
    request,
    onRespond,
    onAbort
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = {
      isActive: true
    };
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  useKeybinding("app:interrupt", onAbort, t1);
  let t2;
  if ($[1] !== request.options) {
    t2 = request.options.map(_temp);
    $[1] = request.options;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  const options = t2;
  let t3;
  if ($[3] !== toolInputSummary) {
    t3 = toolInputSummary ? <Text dimColor={true}>{toolInputSummary}</Text> : undefined;
    $[3] = toolInputSummary;
    $[4] = t3;
  } else {
    t3 = $[4];
  }

```

---


### `src/components/hooks/SelectEventMode.tsx`

**信息:**
- 行数: 127
- 大小: 13555 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * SelectEventMode is the entrypoint of the Hooks config menu, where the user
 * sees the list of available hook events.
 *
 * The /hooks menu is read-only: selecting an event lets you browse its
 * configured hooks but not modify them. To add or change hooks, users should
 * edit settings.json directly or ask Claude.
 */

import figures from 'figures';
import * as React from 'react';
import type { HookEvent } from 'src/entrypoints/agentSdkTypes.js';
import type { HookEventMetadata } from 'src/utils/hooks/hooksConfigManager.js';
import { Box, Link, Text } from '../../ink.js';
import { plural } from '../../utils/stringUtils.js';
import { Select } from '../CustomSelect/select.js';
import { Dialog } from '../design-system/Dialog.js';
type Props = {
  hookEventMetadata: Record<HookEvent, HookEventMetadata>;
  hooksByEvent: Partial<Record<HookEvent, number>>;
  totalHooksCount: number;
  restrictedByPolicy: boolean;
  onSelectEvent: (event: HookEvent) => void;
  onCancel: () => void;
};
export function SelectEventMode(t0) {
  const $ = _c(23);
  const {
    hookEventMetadata,
    hooksByEvent,
    totalHooksCount,
    restrictedByPolicy,
    onSelectEvent,
    onCancel
  } = t0;
  let t1;
  if ($[0] !== totalHooksCount) {
    t1 = plural(totalHooksCount, "hook");
    $[0] = totalHooksCount;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const subtitle = `${totalHooksCount} ${t1} configured`;
  let t2;
  if ($[2] !== restrictedByPolicy) {
    t2 = restrictedByPolicy && <Box flexDirection="column"><Text color="suggestion">{figures.info} Hooks Restricted by Policy</Text><Text dimColor={true}>Only hooks from managed settings can run. User-defined hooks from ~/.claude/settings.json, .claude/settings.json, and .claude/settings.local.json are blocked.</Text></Box>;
    $[2] = restrictedByPolicy;
    $[3] = t2;

```

---


### `src/components/hooks/SelectHookMode.tsx`

**信息:**
- 行数: 112
- 大小: 12907 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * SelectHookMode shows all hooks configured for a given event+matcher pair.
 *
 * The /hooks menu is read-only: this view no longer offers "add new hook"
 * and selecting a hook shows its read-only details instead of a delete
 * confirmation.
 */
import * as React from 'react';
import type { HookEvent } from 'src/entrypoints/agentSdkTypes.js';
import type { HookEventMetadata } from 'src/utils/hooks/hooksConfigManager.js';
import { Box, Text } from '../../ink.js';
import { getHookDisplayText, hookSourceHeaderDisplayString, type IndividualHookConfig } from '../../utils/hooks/hooksSettings.js';
import { Select } from '../CustomSelect/select.js';
import { Dialog } from '../design-system/Dialog.js';
type Props = {
  selectedEvent: HookEvent;
  selectedMatcher: string | null;
  hooksForSelectedMatcher: IndividualHookConfig[];
  hookEventMetadata: HookEventMetadata;
  onSelect: (hook: IndividualHookConfig) => void;
  onCancel: () => void;
};
export function SelectHookMode(t0) {
  const $ = _c(19);
  const {
    selectedEvent,
    selectedMatcher,
    hooksForSelectedMatcher,
    hookEventMetadata,
    onSelect,
    onCancel
  } = t0;
  const title = hookEventMetadata.matcherMetadata !== undefined ? `${selectedEvent} - Matcher: ${selectedMatcher || "(all)"}` : selectedEvent;
  if (hooksForSelectedMatcher.length === 0) {
    let t1;
    if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
      t1 = <Box flexDirection="column" gap={1}><Text dimColor={true}>No hooks configured for this event.</Text><Text dimColor={true}>To add hooks, edit settings.json directly or ask Claude.</Text></Box>;
      $[0] = t1;
    } else {
      t1 = $[0];
    }
    let t2;
    if ($[1] !== hookEventMetadata.description || $[2] !== onCancel || $[3] !== title) {
      t2 = <Dialog title={title} subtitle={hookEventMetadata.description} onCancel={onCancel} inputGuide={_temp}>{t1}</Dialog>;
      $[1] = hookEventMetadata.description;
      $[2] = onCancel;
      $[3] = title;
      $[4] = t2;
    } else {

```

---


### `src/components/hooks/SelectMatcherMode.tsx`

**信息:**
- 行数: 144
- 大小: 14809 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * SelectMatcherMode shows the configured matchers for a selected hook event.
 *
 * The /hooks menu is read-only: this view no longer offers "add new matcher"
 * and simply lets the user drill into each matcher to see its hooks.
 */
import * as React from 'react';
import type { HookEvent } from 'src/entrypoints/agentSdkTypes.js';
import { Box, Text } from '../../ink.js';
import { type HookSource, hookSourceInlineDisplayString, type IndividualHookConfig } from '../../utils/hooks/hooksSettings.js';
import { plural } from '../../utils/stringUtils.js';
import { Select } from '../CustomSelect/select.js';
import { Dialog } from '../design-system/Dialog.js';
type MatcherWithSource = {
  matcher: string;
  sources: HookSource[];
  hookCount: number;
};
type Props = {
  selectedEvent: HookEvent;
  matchersForSelectedEvent: string[];
  hooksByEventAndMatcher: Record<HookEvent, Record<string, IndividualHookConfig[]>>;
  eventDescription: string;
  onSelect: (matcher: string) => void;
  onCancel: () => void;
};
export function SelectMatcherMode(t0) {
  const $ = _c(25);
  const {
    selectedEvent,
    matchersForSelectedEvent,
    hooksByEventAndMatcher,
    eventDescription,
    onSelect,
    onCancel
  } = t0;
  let t1;
  if ($[0] !== hooksByEventAndMatcher || $[1] !== matchersForSelectedEvent || $[2] !== selectedEvent) {
    let t2;
    if ($[4] !== hooksByEventAndMatcher || $[5] !== selectedEvent) {
      t2 = matcher => {
        const hooks = hooksByEventAndMatcher[selectedEvent]?.[matcher] || [];
        const sources = Array.from(new Set(hooks.map(_temp)));
        return {
          matcher,
          sources,
          hookCount: hooks.length
        };
      };

```

---


### `src/components/hooks/ViewHookMode.tsx`

**信息:**
- 行数: 199
- 大小: 17969 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * ViewHookMode shows read-only details for a single configured hook.
 *
 * The /hooks menu is read-only; this view replaces the former delete-hook
 * confirmation screen and directs users to settings.json or Claude for edits.
 */
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { hookSourceDescriptionDisplayString, type IndividualHookConfig } from '../../utils/hooks/hooksSettings.js';
import { Dialog } from '../design-system/Dialog.js';
type Props = {
  selectedHook: IndividualHookConfig;
  eventSupportsMatcher: boolean;
  onCancel: () => void;
};
export function ViewHookMode(t0) {
  const $ = _c(40);
  const {
    selectedHook,
    eventSupportsMatcher,
    onCancel
  } = t0;
  let t1;
  if ($[0] !== selectedHook.event) {
    t1 = <Text>Event: <Text bold={true}>{selectedHook.event}</Text></Text>;
    $[0] = selectedHook.event;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] !== eventSupportsMatcher || $[3] !== selectedHook.matcher) {
    t2 = eventSupportsMatcher && <Text>Matcher: <Text bold={true}>{selectedHook.matcher || "(all)"}</Text></Text>;
    $[2] = eventSupportsMatcher;
    $[3] = selectedHook.matcher;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  let t3;
  if ($[5] !== selectedHook.config.type) {
    t3 = <Text>Type: <Text bold={true}>{selectedHook.config.type}</Text></Text>;
    $[5] = selectedHook.config.type;
    $[6] = t3;
  } else {
    t3 = $[6];
  }
  let t4;
  if ($[7] !== selectedHook.source) {

```

---


### `src/components/mcp/CapabilitiesSection.tsx`

**信息:**
- 行数: 61
- 大小: 4957 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../../ink.js';
import { Byline } from '../design-system/Byline.js';
type Props = {
  serverToolsCount: number;
  serverPromptsCount: number;
  serverResourcesCount: number;
};
export function CapabilitiesSection(t0) {
  const $ = _c(9);
  const {
    serverToolsCount,
    serverPromptsCount,
    serverResourcesCount
  } = t0;
  let capabilities;
  if ($[0] !== serverPromptsCount || $[1] !== serverResourcesCount || $[2] !== serverToolsCount) {
    capabilities = [];
    if (serverToolsCount > 0) {
      capabilities.push("tools");
    }
    if (serverResourcesCount > 0) {
      capabilities.push("resources");
    }
    if (serverPromptsCount > 0) {
      capabilities.push("prompts");
    }
    $[0] = serverPromptsCount;
    $[1] = serverResourcesCount;
    $[2] = serverToolsCount;
    $[3] = capabilities;
  } else {
    capabilities = $[3];
  }
  let t1;
  if ($[4] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Text bold={true}>Capabilities: </Text>;
    $[4] = t1;
  } else {
    t1 = $[4];
  }
  let t2;
  if ($[5] !== capabilities) {
    t2 = capabilities.length > 0 ? <Byline>{capabilities}</Byline> : "none";
    $[5] = capabilities;
    $[6] = t2;
  } else {
    t2 = $[6];
  }

```

---


### `src/components/mcp/ElicitationDialog.tsx`

**信息:**
- 行数: 1169
- 大小: 179643 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ElicitRequestFormParams, ElicitRequestURLParams, ElicitResult, PrimitiveSchemaDefinition } from '@modelcontextprotocol/sdk/types.js';
import figures from 'figures';
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useRegisterOverlay } from '../../context/overlayContext.js';
import { useNotifyAfterTimeout } from '../../hooks/useNotifyAfterTimeout.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- raw text input for elicitation form
import { Box, Text, useInput } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import type { ElicitationRequestEvent } from '../../services/mcp/elicitationHandler.js';
import { openBrowser } from '../../utils/browser.js';
import { getEnumLabel, getEnumValues, getMultiSelectLabel, getMultiSelectValues, isDateTimeSchema, isEnumSchema, isMultiSelectEnumSchema, validateElicitationInput, validateElicitationInputAsync } from '../../utils/mcp/elicitationValidation.js';
import { plural } from '../../utils/stringUtils.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import TextInput from '../TextInput.js';
type Props = {
  event: ElicitationRequestEvent;
  onResponse: (action: ElicitResult['action'], content?: ElicitResult['content']) => void;
  /** Called when the phase 2 waiting state is dismissed (URL elicitations only). */
  onWaitingDismiss?: (action: 'dismiss' | 'retry' | 'cancel') => void;
};
const isTextField = (s: PrimitiveSchemaDefinition) => ['string', 'number', 'integer'].includes(s.type);
const RESOLVING_SPINNER_CHARS = '\u280B\u2819\u2839\u2838\u283C\u2834\u2826\u2827\u2807\u280F';
const advanceSpinnerFrame = (f: number) => (f + 1) % RESOLVING_SPINNER_CHARS.length;

/** Timer callback for enumTypeaheadRef — module-scope to avoid closure capture. */
function resetTypeahead(ta: {
  buffer: string;
  timer: ReturnType<typeof setTimeout> | undefined;
}): void {
  ta.buffer = '';
  ta.timer = undefined;
}

/**
 * Isolated spinner glyph for a field that is being resolved asynchronously.
 * Owns its own 80ms animation timer so ticks only re-render this tiny leaf,
 * not the entire ElicitationFormDialog (~1200 lines + renderFormFields).
 * Mounted/unmounted by the parent via the `isResolving` condition.
 *
 * Not using the shared <Spinner /> from ../Spinner.js: that one renders in a
 * <Box width={2}> with color="text", which would break the 1-col checkbox
 * column alignment here (other checkbox states are width-1 glyphs).
 */
function ResolvingSpinner() {
  const $ = _c(4);

```

---


### `src/components/mcp/MCPAgentServerMenu.tsx`

**信息:**
- 行数: 183
- 大小: 26662 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import figures from 'figures';
import React, { useCallback, useEffect, useRef, useState } from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { Box, color, Link, Text, useTheme } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { AuthenticationCancelledError, performMCPOAuthFlow } from '../../services/mcp/auth.js';
import { capitalize } from '../../utils/stringUtils.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Select } from '../CustomSelect/index.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import { Spinner } from '../Spinner.js';
import type { AgentMcpServerInfo } from './types.js';
type Props = {
  agentServer: AgentMcpServerInfo;
  onCancel: () => void;
  onComplete?: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};

/**
 * Menu for agent-specific MCP servers.
 * These servers are defined in agent frontmatter and only connect when the agent runs.
 * For HTTP/SSE servers, this allows pre-authentication before using the agent.
 */
export function MCPAgentServerMenu({
  agentServer,
  onCancel,
  onComplete
}: Props): React.ReactNode {
  const [theme] = useTheme();
  const [isAuthenticating, setIsAuthenticating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [authorizationUrl, setAuthorizationUrl] = useState<string | null>(null);
  const authAbortControllerRef = useRef<AbortController | null>(null);

  // Abort OAuth flow on unmount so the callback server is closed even if a
  // parent component's Esc handler navigates away before ours fires.
  useEffect(() => () => authAbortControllerRef.current?.abort(), []);

  // Handle ESC to cancel authentication flow
  const handleEscCancel = useCallback(() => {
    if (isAuthenticating) {
      authAbortControllerRef.current?.abort();
      authAbortControllerRef.current = null;
      setIsAuthenticating(false);
      setAuthorizationUrl(null);
    }

```

---


### `src/components/mcp/MCPListPanel.tsx`

**信息:**
- 行数: 504
- 大小: 58231 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { useCallback, useState } from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { Box, color, Link, Text, useTheme } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import type { ConfigScope } from '../../services/mcp/types.js';
import { describeMcpConfigFilePath } from '../../services/mcp/utils.js';
import { isDebugMode } from '../../utils/debug.js';
import { plural } from '../../utils/stringUtils.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import { McpParsingWarnings } from './McpParsingWarnings.js';
import type { AgentMcpServerInfo, ServerInfo } from './types.js';
type Props = {
  servers: ServerInfo[];
  agentServers?: AgentMcpServerInfo[];
  onSelectServer: (server: ServerInfo) => void;
  onSelectAgentServer?: (agentServer: AgentMcpServerInfo) => void;
  onComplete: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  defaultTab?: string;
};
type SelectableItem = {
  type: 'server';
  server: ServerInfo;
} | {
  type: 'agent-server';
  agentServer: AgentMcpServerInfo;
};

// Define scope order for display (constant, outside component)
// 'dynamic' (built-in) is rendered separately at the end
const SCOPE_ORDER: ConfigScope[] = ['project', 'local', 'user', 'enterprise'];

// Get scope heading parts (label is bold, path is grey)
function getScopeHeading(scope: ConfigScope): {
  label: string;
  path?: string;
} {
  switch (scope) {
    case 'project':
      return {
        label: 'Project MCPs',
        path: describeMcpConfigFilePath(scope)
      };
    case 'user':

```

---


### `src/components/mcp/MCPReconnect.tsx`

**信息:**
- 行数: 167
- 大小: 16195 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { useEffect, useState } from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { Box, color, Text, useTheme } from '../../ink.js';
import { useMcpReconnect } from '../../services/mcp/MCPConnectionManager.js';
import { useAppStateStore } from '../../state/AppState.js';
import { Spinner } from '../Spinner.js';
type Props = {
  serverName: string;
  onComplete: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
export function MCPReconnect(t0) {
  const $ = _c(25);
  const {
    serverName,
    onComplete
  } = t0;
  const [theme] = useTheme();
  const store = useAppStateStore();
  const reconnectMcpServer = useMcpReconnect();
  const [isReconnecting, setIsReconnecting] = useState(true);
  const [error, setError] = useState(null);
  let t1;
  let t2;
  if ($[0] !== onComplete || $[1] !== reconnectMcpServer || $[2] !== serverName || $[3] !== store) {
    t1 = () => {
      const attemptReconnect = async function attemptReconnect() {
        ;
        try {
          const server = store.getState().mcp.clients.find(c => c.name === serverName);
          if (!server) {
            setError(`MCP server "${serverName}" not found`);
            setIsReconnecting(false);
            onComplete(`MCP server "${serverName}" not found`);
            return;
          }
          const result = await reconnectMcpServer(serverName);
          bb43: switch (result.client.type) {
            case "connected":
              {
                setIsReconnecting(false);
                onComplete(`Successfully reconnected to ${serverName}`);
                break bb43;
              }
            case "needs-auth":
              {
                setError(`${serverName} requires authentication`);

```

---


### `src/components/mcp/MCPRemoteServerMenu.tsx`

**信息:**
- 行数: 649
- 大小: 102489 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import figures from 'figures';
import React, { useEffect, useRef, useState } from 'react';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import type { CommandResultDisplay } from '../../commands.js';
import { getOauthConfig } from '../../constants/oauth.js';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { setClipboard } from '../../ink/termio/osc.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- raw j/k/arrow menu navigation
import { Box, color, Link, Text, useInput, useTheme } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { AuthenticationCancelledError, performMCPOAuthFlow, revokeServerTokens } from '../../services/mcp/auth.js';
import { clearServerCache } from '../../services/mcp/client.js';
import { useMcpReconnect, useMcpToggleEnabled } from '../../services/mcp/MCPConnectionManager.js';
import { describeMcpConfigFilePath, excludeCommandsByServer, excludeResourcesByServer, excludeToolsByServer, filterMcpPromptsByServer } from '../../services/mcp/utils.js';
import { useAppState, useSetAppState } from '../../state/AppState.js';
import { getOauthAccountInfo } from '../../utils/auth.js';
import { openBrowser } from '../../utils/browser.js';
import { errorMessage } from '../../utils/errors.js';
import { logMCPDebug } from '../../utils/log.js';
import { capitalize } from '../../utils/stringUtils.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Select } from '../CustomSelect/index.js';
import { Byline } from '../design-system/Byline.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import { Spinner } from '../Spinner.js';
import TextInput from '../TextInput.js';
import { CapabilitiesSection } from './CapabilitiesSection.js';
import type { ClaudeAIServerInfo, HTTPServerInfo, SSEServerInfo } from './types.js';
import { handleReconnectError, handleReconnectResult } from './utils/reconnectHelpers.js';
type Props = {
  server: SSEServerInfo | HTTPServerInfo | ClaudeAIServerInfo;
  serverToolsCount: number;
  onViewTools: () => void;
  onCancel: () => void;
  onComplete?: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  borderless?: boolean;
};
export function MCPRemoteServerMenu({
  server,
  serverToolsCount,
  onViewTools,
  onCancel,
  onComplete,
  borderless = false
}: Props): React.ReactNode {
  const [theme] = useTheme();
  const exitState = useExitOnCtrlCDWithKeybindings();

```

---


### `src/components/mcp/MCPSettings.tsx`

**信息:**
- 行数: 398
- 大小: 40386 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useEffect, useMemo } from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { ClaudeAuthProvider } from '../../services/mcp/auth.js';
import type { McpClaudeAIProxyServerConfig, McpHTTPServerConfig, McpSSEServerConfig, McpStdioServerConfig } from '../../services/mcp/types.js';
import { extractAgentMcpServers, filterToolsByServer } from '../../services/mcp/utils.js';
import { useAppState } from '../../state/AppState.js';
import { getSessionIngressAuthToken } from '../../utils/sessionIngressAuth.js';
import { MCPAgentServerMenu } from './MCPAgentServerMenu.js';
import { MCPListPanel } from './MCPListPanel.js';
import { MCPRemoteServerMenu } from './MCPRemoteServerMenu.js';
import { MCPStdioServerMenu } from './MCPStdioServerMenu.js';
import { MCPToolDetailView } from './MCPToolDetailView.js';
import { MCPToolListView } from './MCPToolListView.js';
import type { AgentMcpServerInfo, MCPViewState, ServerInfo } from './types.js';
type Props = {
  onComplete: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
export function MCPSettings(t0) {
  const $ = _c(66);
  const {
    onComplete
  } = t0;
  const mcp = useAppState(_temp);
  const agentDefinitions = useAppState(_temp2);
  const mcpClients = mcp.clients;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = {
      type: "list"
    };
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const [viewState, setViewState] = React.useState(t1);
  let t2;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = [];
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  const [servers, setServers] = React.useState(t2);
  let t3;
  if ($[2] !== agentDefinitions.allAgents) {
    t3 = extractAgentMcpServers(agentDefinitions.allAgents);
    $[2] = agentDefinitions.allAgents;

```

---


### `src/components/mcp/MCPStdioServerMenu.tsx`

**信息:**
- 行数: 177
- 大小: 28394 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import figures from 'figures';
import React, { useState } from 'react';
import type { CommandResultDisplay } from '../../commands.js';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, color, Text, useTheme } from '../../ink.js';
import { getMcpConfigByName } from '../../services/mcp/config.js';
import { useMcpReconnect, useMcpToggleEnabled } from '../../services/mcp/MCPConnectionManager.js';
import { describeMcpConfigFilePath, filterMcpPromptsByServer } from '../../services/mcp/utils.js';
import { useAppState } from '../../state/AppState.js';
import { errorMessage } from '../../utils/errors.js';
import { capitalize } from '../../utils/stringUtils.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Select } from '../CustomSelect/index.js';
import { Byline } from '../design-system/Byline.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import { Spinner } from '../Spinner.js';
import { CapabilitiesSection } from './CapabilitiesSection.js';
import type { StdioServerInfo } from './types.js';
import { handleReconnectError, handleReconnectResult } from './utils/reconnectHelpers.js';
type Props = {
  server: StdioServerInfo;
  serverToolsCount: number;
  onViewTools: () => void;
  onCancel: () => void;
  onComplete: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  borderless?: boolean;
};
export function MCPStdioServerMenu({
  server,
  serverToolsCount,
  onViewTools,
  onCancel,
  onComplete,
  borderless = false
}: Props): React.ReactNode {
  const [theme] = useTheme();
  const exitState = useExitOnCtrlCDWithKeybindings();
  const mcp = useAppState(s => s.mcp);
  const reconnectMcpServer = useMcpReconnect();
  const toggleMcpServer = useMcpToggleEnabled();
  const [isReconnecting, setIsReconnecting] = useState(false);
  const handleToggleEnabled = React.useCallback(async () => {
    const wasEnabled = server.client.type !== 'disabled';
    try {
      await toggleMcpServer(server.name);
      // Return to the server list so user can continue managing other servers
      onCancel();
    } catch (err) {

```

---


### `src/components/mcp/MCPToolDetailView.tsx`

**信息:**
- 行数: 212
- 大小: 23139 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../../ink.js';
import { extractMcpToolDisplayName, getMcpDisplayName } from '../../services/mcp/mcpStringUtils.js';
import type { Tool } from '../../Tool.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Dialog } from '../design-system/Dialog.js';
import type { ServerInfo } from './types.js';
type Props = {
  tool: Tool;
  server: ServerInfo;
  onBack: () => void;
};
export function MCPToolDetailView(t0) {
  const $ = _c(44);
  const {
    tool,
    server,
    onBack
  } = t0;
  const [toolDescription, setToolDescription] = React.useState("");
  let t1;
  let toolName;
  if ($[0] !== server.name || $[1] !== tool) {
    toolName = getMcpDisplayName(tool.name, server.name);
    const fullDisplayName = tool.userFacingName ? tool.userFacingName({}) : toolName;
    t1 = extractMcpToolDisplayName(fullDisplayName);
    $[0] = server.name;
    $[1] = tool;
    $[2] = t1;
    $[3] = toolName;
  } else {
    t1 = $[2];
    toolName = $[3];
  }
  const displayName = t1;
  let t2;
  if ($[4] !== tool) {
    t2 = tool.isReadOnly?.({}) ?? false;
    $[4] = tool;
    $[5] = t2;
  } else {
    t2 = $[5];
  }
  const isReadOnly = t2;
  let t3;
  if ($[6] !== tool) {
    t3 = tool.isDestructive?.({}) ?? false;
    $[6] = tool;
    $[7] = t3;

```

---


### `src/components/mcp/MCPToolListView.tsx`

**信息:**
- 行数: 141
- 大小: 16252 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Text } from '../../ink.js';
import { extractMcpToolDisplayName, getMcpDisplayName } from '../../services/mcp/mcpStringUtils.js';
import { filterToolsByServer } from '../../services/mcp/utils.js';
import { useAppState } from '../../state/AppState.js';
import type { Tool } from '../../Tool.js';
import { plural } from '../../utils/stringUtils.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Select } from '../CustomSelect/index.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import type { ServerInfo } from './types.js';
type Props = {
  server: ServerInfo;
  onSelectTool: (tool: Tool, index: number) => void;
  onBack: () => void;
};
export function MCPToolListView(t0) {
  const $ = _c(21);
  const {
    server,
    onSelectTool,
    onBack
  } = t0;
  const mcpTools = useAppState(_temp);
  let t1;
  bb0: {
    if (server.client.type !== "connected") {
      let t2;
      if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
        t2 = [];
        $[0] = t2;
      } else {
        t2 = $[0];
      }
      t1 = t2;
      break bb0;
    }
    let t2;
    if ($[1] !== mcpTools || $[2] !== server.name) {
      t2 = filterToolsByServer(mcpTools, server.name);
      $[1] = mcpTools;
      $[2] = server.name;
      $[3] = t2;
    } else {
      t2 = $[3];
    }
    t1 = t2;

```

---


### `src/components/mcp/McpParsingWarnings.tsx`

**信息:**
- 行数: 213
- 大小: 22079 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useMemo } from 'react';
import { getMcpConfigsByScope } from 'src/services/mcp/config.js';
import type { ConfigScope } from 'src/services/mcp/types.js';
import { describeMcpConfigFilePath, getScopeLabel } from 'src/services/mcp/utils.js';
import type { ValidationError } from 'src/utils/settings/validation.js';
import { Box, Link, Text } from '../../ink.js';
function McpConfigErrorSection(t0) {
  const $ = _c(26);
  const {
    scope,
    parsingErrors,
    warnings
  } = t0;
  const hasErrors = parsingErrors.length > 0;
  const hasWarnings = warnings.length > 0;
  if (!hasErrors && !hasWarnings) {
    return null;
  }
  let t1;
  if ($[0] !== hasErrors || $[1] !== hasWarnings) {
    t1 = (hasErrors || hasWarnings) && <Text color={hasErrors ? "error" : "warning"}>[{hasErrors ? "Failed to parse" : "Contains warnings"}]{" "}</Text>;
    $[0] = hasErrors;
    $[1] = hasWarnings;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  let t2;
  if ($[3] !== scope) {
    t2 = getScopeLabel(scope);
    $[3] = scope;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  let t3;
  if ($[5] !== t2) {
    t3 = <Text>{t2}</Text>;
    $[5] = t2;
    $[6] = t3;
  } else {
    t3 = $[6];
  }
  let t4;
  if ($[7] !== t1 || $[8] !== t3) {
    t4 = <Box>{t1}{t3}</Box>;
    $[7] = t1;
    $[8] = t3;
    $[9] = t4;

```

---


### `src/components/mcp/index.ts`

**信息:**
- 行数: 9
- 大小: 523 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export { MCPAgentServerMenu } from './MCPAgentServerMenu.js'
export { MCPListPanel } from './MCPListPanel.js'
export { MCPReconnect } from './MCPReconnect.js'
export { MCPRemoteServerMenu } from './MCPRemoteServerMenu.js'
export { MCPSettings } from './MCPSettings.js'
export { MCPStdioServerMenu } from './MCPStdioServerMenu.js'
export { MCPToolDetailView } from './MCPToolDetailView.js'
export { MCPToolListView } from './MCPToolListView.js'
export type { AgentMcpServerInfo, MCPViewState, ServerInfo } from './types.js'

```

---


### `src/components/mcp/types.ts`

**信息:**
- 行数: 7
- 大小: 356 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type ServerInfo = Record<string, unknown>
export type AgentMcpServerInfo = Record<string, unknown>
export type ClaudeAIServerInfo = Record<string, unknown>
export type HTTPServerInfo = Record<string, unknown>
export type SSEServerInfo = Record<string, unknown>
export type StdioServerInfo = Record<string, unknown>
export type MCPViewState = string

```

---


### `src/components/mcp/utils/reconnectHelpers.tsx`

**信息:**
- 行数: 49
- 大小: 5292 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { Command } from '../../../commands.js';
import type { MCPServerConnection, ServerResource } from '../../../services/mcp/types.js';
import type { Tool } from '../../../Tool.js';
export interface ReconnectResult {
  message: string;
  success: boolean;
}

/**
 * Handles the result of a reconnect attempt and returns an appropriate user message
 */
export function handleReconnectResult(result: {
  client: MCPServerConnection;
  tools: Tool[];
  commands: Command[];
  resources?: ServerResource[];
}, serverName: string): ReconnectResult {
  switch (result.client.type) {
    case 'connected':
      return {
        message: `Reconnected to ${serverName}.`,
        success: true
      };
    case 'needs-auth':
      return {
        message: `${serverName} requires authentication. Use the 'Authenticate' option.`,
        success: false
      };
    case 'failed':
      return {
        message: `Failed to reconnect to ${serverName}.`,
        success: false
      };
    default:
      return {
        message: `Unknown result when reconnecting to ${serverName}.`,
        success: false
      };
  }
}

/**
 * Handles errors from reconnect attempts
 */
export function handleReconnectError(error: unknown, serverName: string): string {
  const errorMessage = error instanceof Error ? error.message : String(error);
  return `Error reconnecting to ${serverName}: ${errorMessage}`;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJDb21tYW5kIiwiTUNQU2VydmVyQ29ubmVjdGlvbiIsIlNlcnZlclJlc291cmNlIiwiVG9vbCIsIlJlY29ubmVjdFJlc3VsdCIsIm1lc3NhZ2UiLCJzdWNjZXNzIiwiaGFuZGxlUmVjb25uZWN0UmVzdWx0IiwicmVzdWx0IiwiY2xpZW50IiwidG9vbHMiLCJjb21tYW5kcyIsInJlc291cmNlcyIsInNlcnZlck5hbWUiLCJ0eXBlIiwiaGFuZGxlUmVjb25uZWN0RXJyb3IiLCJlcnJvciIsImVycm9yTWVzc2FnZSIsIkVycm9yIiwiU3RyaW5nIl0sInNvdXJjZXMiOlsicmVjb25uZWN0SGVscGVycy50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHR5cGUgeyBDb21tYW5kIH0gZnJvbSAnLi4vLi4vLi4vY29tbWFuZHMuanMnXG5pbXBvcnQgdHlwZSB7XG4gIE1DUFNlcnZlckNvbm5lY3Rpb24sXG4gIFNlcnZlclJlc291cmNlLFxufSBmcm9tICcuLi8uLi8uLi9zZXJ2aWNlcy9tY3AvdHlwZXMuanMnXG5pbXBvcnQgdHlwZSB7IFRvb2wgfSBmcm9tICcuLi8uLi8uLi9Ub29sLmpzJ1xuXG5leHBvcnQgaW50ZXJmYWNlIFJlY29ubmVjdFJlc3VsdCB7XG4gIG1lc3NhZ2U6IHN0cmluZ1xuICBzdWNjZXNzOiBib29sZWFuXG59XG5cbi8qKlxuICogSGFuZGxlcyB0aGUgcmVzdWx0IG9mIGEgcmVjb25uZWN0IGF0dGVtcHQgYW5kIHJldHVybnMgYW4gYXBwcm9wcmlhdGUgdXNlciBtZXNzYWdlXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBoYW5kbGVSZWNvbm5lY3RSZXN1bHQoXG4gIHJlc3VsdDoge1xuICAgIGNsaWVudDogTUNQU2VydmVyQ29ubmVjdGlvblxuICAgIHRvb2xzOiBUb29sW11cbiAgICBjb21tYW5kczogQ29tbWFuZFtdXG4gICAgcmVzb3VyY2VzPzogU2VydmVyUmVzb3VyY2VbXVxuICB9LFxuICBzZXJ2ZXJOYW1lOiBzdHJpbmcsXG4pOiBSZWNvbm5lY3RSZXN1bHQge1xuICBzd2l0Y2ggKHJlc3VsdC5jbGllbnQudHlwZSkge1xuICAgIGNhc2UgJ2Nvbm5lY3RlZCc6XG4gICAgICByZXR1cm4ge1xuICAgICAgICBtZXNzYWdlOiBgUmVjb25uZWN0ZWQgdG8gJHtzZXJ2ZXJOYW1lfS5gLFxuICAgICAgICBzdWNjZXNzOiB0cnVlLFxuICAgICAgfVxuXG4gICAgY2FzZSAnbmVlZHMtYXV0aCc6XG4gICAgICByZXR1cm4ge1xuICAgICAgICBtZXNzYWdlOiBgJHtzZXJ2ZXJOYW1lfSByZXF1aXJlcyBhdXRoZW50aWNhdGlvbi4gVXNlIHRoZSAnQXV0aGVudGljYXRlJyBvcHRpb24uYCxcbiAgICAgICAgc3VjY2VzczogZmFsc2UsXG4gICAgICB9XG5cbiAgICBjYXNlICdmYWlsZWQnOlxuICAgICAgcmV0dXJuIHtcbiAgICAgICAgbWVzc2FnZTogYEZhaWxlZCB0byByZWNvbm5lY3QgdG8gJHtzZXJ2ZXJOYW1lfS5gLFxuICAgICAgICBzdWNjZXNzOiBmYWxzZSxcbiAgICAgIH1cblxuICAgIGRlZmF1bHQ6XG4gICAgICByZXR1cm4ge1xuICAgICAgICBtZXNzYWdlOiBgVW5rbm93biByZXN1bHQgd2hlbiByZWNvbm5lY3RpbmcgdG8gJHtzZXJ2ZXJOYW1lfS5gLFxuICAgICAgICBzdWNjZXNzOiBmYWxzZSxcbiAgICAgIH1cbiAgfVxufVxuXG4vKipcbiAqIEhhbmRsZXMgZXJyb3JzIGZyb20gcmVjb25uZWN0IGF0dGVtcHRzXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBoYW5kbGVSZWNvbm5lY3RFcnJvcihcbiAgZXJyb3I6IHVua25vd24sXG4gIHNlcnZlck5hbWU6IHN0cmluZyxcbik6IHN0cmluZyB7XG4gIGNvbnN0IGVycm9yTWVzc2FnZSA9IGVycm9yIGluc3RhbmNlb2YgRXJyb3IgPyBlcnJvci5tZXNzYWdlIDogU3RyaW5nKGVycm9yKVxuICByZXR1cm4gYEVycm9yIHJlY29ubmVjdGluZyB0byAke3NlcnZlck5hbWV9OiAke2Vycm9yTWVzc2FnZX1gXG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLGNBQWNBLE9BQU8sUUFBUSxzQkFBc0I7QUFDbkQsY0FDRUMsbUJBQW1CLEVBQ25CQyxjQUFjLFFBQ1QsZ0NBQWdDO0FBQ3ZDLGNBQWNDLElBQUksUUFBUSxrQkFBa0I7QUFFNUMsT0FBTyxVQUFVQyxlQUFlLENBQUM7RUFDL0JDLE9BQU8sRUFBRSxNQUFNO0VBQ2ZDLE9BQU8sRUFBRSxPQUFPO0FBQ2xCOztBQUVBO0FBQ0E7QUFDQTtBQUNBLE9BQU8sU0FBU0MscUJBQXFCQSxDQUNuQ0MsTUFBTSxFQUFFO0VBQ05DLE1BQU0sRUFBRVIsbUJBQW1CO0VBQzNCUyxLQUFLLEVBQUVQLElBQUksRUFBRTtFQUNiUSxRQUFRLEVBQUVYLE9BQU8sRUFBRTtFQUNuQlksU0FBUyxDQUFDLEVBQUVWLGNBQWMsRUFBRTtBQUM5QixDQUFDLEVBQ0RXLFVBQVUsRUFBRSxNQUFNLENBQ25CLEVBQUVULGVBQWUsQ0FBQztFQUNqQixRQUFRSSxNQUFNLENBQUNDLE1BQU0sQ0FBQ0ssSUFBSTtJQUN4QixLQUFLLFdBQVc7TUFDZCxPQUFPO1FBQ0xULE9BQU8sRUFBRSxrQkFBa0JRLFVBQVUsR0FBRztRQUN4Q1AsT0FBTyxFQUFFO01BQ1gsQ0FBQztJQUVILEtBQUssWUFBWTtNQUNmLE9BQU87UUFDTEQsT0FBTyxFQUFFLEdBQUdRLFVBQVUsMERBQTBEO1FBQ2hGUCxPQUFPLEVBQUU7TUFDWCxDQUFDO0lBRUgsS0FBSyxRQUFRO01BQ1gsT0FBTztRQUNMRCxPQUFPLEVBQUUsMEJBQTBCUSxVQUFVLEdBQUc7UUFDaERQLE9BQU8sRUFBRTtNQUNYLENBQUM7SUFFSDtNQUNFLE9BQU87UUFDTEQsT0FBTyxFQUFFLHVDQUF1Q1EsVUFBVSxHQUFHO1FBQzdEUCxPQUFPLEVBQUU7TUFDWCxDQUFDO0VBQ0w7QUFDRjs7QUFFQTtBQUNBO0FBQ0E7QUFDQSxPQUFPLFNBQVNTLG9CQUFvQkEsQ0FDbENDLEtBQUssRUFBRSxPQUFPLEVBQ2RILFVBQVUsRUFBRSxNQUFNLENBQ25CLEVBQUUsTUFBTSxDQUFDO0VBQ1IsTUFBTUksWUFBWSxHQUFHRCxLQUFLLFlBQVlFLEtBQUssR0FBR0YsS0FBSyxDQUFDWCxPQUFPLEdBQUdjLE1BQU0sQ0FBQ0gsS0FBSyxDQUFDO0VBQzNFLE9BQU8seUJBQXlCSCxVQUFVLEtBQUtJLFlBQVksRUFBRTtBQUMvRCIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/components/memory/MemoryFileSelector.tsx`

**信息:**
- 行数: 438
- 大小: 48121 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import chalk from 'chalk';
import { mkdir } from 'fs/promises';
import { join } from 'path';
import * as React from 'react';
import { use, useEffect, useState } from 'react';
import { getOriginalCwd } from '../../bootstrap/state.js';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { getAutoMemPath, isAutoMemoryEnabled } from '../../memdir/paths.js';
import { logEvent } from '../../services/analytics/index.js';
import { isAutoDreamEnabled } from '../../services/autoDream/config.js';
import { readLastConsolidatedAt } from '../../services/autoDream/consolidationLock.js';
import { useAppState } from '../../state/AppState.js';
import { getAgentMemoryDir } from '../../tools/AgentTool/agentMemory.js';
import { openPath } from '../../utils/browser.js';
import { getMemoryFiles, type MemoryFileInfo } from '../../utils/claudemd.js';
import { getClaudeConfigHomeDir } from '../../utils/envUtils.js';
import { getDisplayPath } from '../../utils/file.js';
import { formatRelativeTimeAgo } from '../../utils/format.js';
import { projectIsInGitRepo } from '../../utils/memory/versions.js';
import { updateSettingsForSource } from '../../utils/settings/settings.js';
import { Select } from '../CustomSelect/index.js';
import { ListItem } from '../design-system/ListItem.js';

/* eslint-disable @typescript-eslint/no-require-imports */
const teamMemPaths = feature('TEAMMEM') ? require('../../memdir/teamMemPaths.js') as typeof import('../../memdir/teamMemPaths.js') : null;
/* eslint-enable @typescript-eslint/no-require-imports */

interface ExtendedMemoryFileInfo extends MemoryFileInfo {
  isNested?: boolean;
  exists: boolean;
}

// Remember last selected path
let lastSelectedPath: string | undefined;
const OPEN_FOLDER_PREFIX = '__open_folder__';
type Props = {
  onSelect: (path: string) => void;
  onCancel: () => void;
};
export function MemoryFileSelector(t0) {
  const $ = _c(58);
  const {
    onSelect,
    onCancel
  } = t0;
  const existingMemoryFiles = use(getMemoryFiles());

```

---


### `src/components/memory/MemoryUpdateNotification.tsx`

**信息:**
- 行数: 45
- 大小: 5100 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { homedir } from 'os';
import { relative } from 'path';
import React from 'react';
import { Box, Text } from '../../ink.js';
import { getCwd } from '../../utils/cwd.js';
export function getRelativeMemoryPath(path: string): string {
  const homeDir = homedir();
  const cwd = getCwd();

  // Calculate relative paths
  const relativeToHome = path.startsWith(homeDir) ? '~' + path.slice(homeDir.length) : null;
  const relativeToCwd = path.startsWith(cwd) ? './' + relative(cwd, path) : null;

  // Return the shorter path, or absolute if neither is applicable
  if (relativeToHome && relativeToCwd) {
    return relativeToHome.length <= relativeToCwd.length ? relativeToHome : relativeToCwd;
  }
  return relativeToHome || relativeToCwd || path;
}
export function MemoryUpdateNotification(t0) {
  const $ = _c(4);
  const {
    memoryPath
  } = t0;
  let t1;
  if ($[0] !== memoryPath) {
    t1 = getRelativeMemoryPath(memoryPath);
    $[0] = memoryPath;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const displayPath = t1;
  let t2;
  if ($[2] !== displayPath) {
    t2 = <Box flexDirection="column" flexGrow={1}><Text color="text">Memory updated in {displayPath} · /memory to edit</Text></Box>;
    $[2] = displayPath;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  return t2;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJob21lZGlyIiwicmVsYXRpdmUiLCJSZWFjdCIsIkJveCIsIlRleHQiLCJnZXRDd2QiLCJnZXRSZWxhdGl2ZU1lbW9yeVBhdGgiLCJwYXRoIiwiaG9tZURpciIsImN3ZCIsInJlbGF0aXZlVG9Ib21lIiwic3RhcnRzV2l0aCIsInNsaWNlIiwibGVuZ3RoIiwicmVsYXRpdmVUb0N3ZCIsIk1lbW9yeVVwZGF0ZU5vdGlmaWNhdGlvbiIsInQwIiwiJCIsIl9jIiwibWVtb3J5UGF0aCIsInQxIiwiZGlzcGxheVBhdGgiLCJ0MiJdLCJzb3VyY2VzIjpbIk1lbW9yeVVwZGF0ZU5vdGlmaWNhdGlvbi50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgaG9tZWRpciB9IGZyb20gJ29zJ1xuaW1wb3J0IHsgcmVsYXRpdmUgfSBmcm9tICdwYXRoJ1xuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgQm94LCBUZXh0IH0gZnJvbSAnLi4vLi4vaW5rLmpzJ1xuaW1wb3J0IHsgZ2V0Q3dkIH0gZnJvbSAnLi4vLi4vdXRpbHMvY3dkLmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gZ2V0UmVsYXRpdmVNZW1vcnlQYXRoKHBhdGg6IHN0cmluZyk6IHN0cmluZyB7XG4gIGNvbnN0IGhvbWVEaXIgPSBob21lZGlyKClcbiAgY29uc3QgY3dkID0gZ2V0Q3dkKClcblxuICAvLyBDYWxjdWxhdGUgcmVsYXRpdmUgcGF0aHNcbiAgY29uc3QgcmVsYXRpdmVUb0hvbWUgPSBwYXRoLnN0YXJ0c1dpdGgoaG9tZURpcilcbiAgICA/ICd+JyArIHBhdGguc2xpY2UoaG9tZURpci5sZW5ndGgpXG4gICAgOiBudWxsXG5cbiAgY29uc3QgcmVsYXRpdmVUb0N3ZCA9IHBhdGguc3RhcnRzV2l0aChjd2QpID8gJy4vJyArIHJlbGF0aXZlKGN3ZCwgcGF0aCkgOiBudWxsXG5cbiAgLy8gUmV0dXJuIHRoZSBzaG9ydGVyIHBhdGgsIG9yIGFic29sdXRlIGlmIG5laXRoZXIgaXMgYXBwbGljYWJsZVxuICBpZiAocmVsYXRpdmVUb0hvbWUgJiYgcmVsYXRpdmVUb0N3ZCkge1xuICAgIHJldHVybiByZWxhdGl2ZVRvSG9tZS5sZW5ndGggPD0gcmVsYXRpdmVUb0N3ZC5sZW5ndGhcbiAgICAgID8gcmVsYXRpdmVUb0hvbWVcbiAgICAgIDogcmVsYXRpdmVUb0N3ZFxuICB9XG5cbiAgcmV0dXJuIHJlbGF0aXZlVG9Ib21lIHx8IHJlbGF0aXZlVG9Dd2QgfHwgcGF0aFxufVxuXG5leHBvcnQgZnVuY3Rpb24gTWVtb3J5VXBkYXRlTm90aWZpY2F0aW9uKHtcbiAgbWVtb3J5UGF0aCxcbn06IHtcbiAgbWVtb3J5UGF0aDogc3RyaW5nXG59KTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgY29uc3QgZGlzcGxheVBhdGggPSBnZXRSZWxhdGl2ZU1lbW9yeVBhdGgobWVtb3J5UGF0aClcblxuICByZXR1cm4gKFxuICAgIDxCb3ggZmxleERpcmVjdGlvbj1cImNvbHVtblwiIGZsZXhHcm93PXsxfT5cbiAgICAgIDxUZXh0IGNvbG9yPVwidGV4dFwiPlxuICAgICAgICBNZW1vcnkgdXBkYXRlZCBpbiB7ZGlzcGxheVBhdGh9IMK3IC9tZW1vcnkgdG8gZWRpdFxuICAgICAgPC9UZXh0PlxuICAgIDwvQm94PlxuICApXG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxTQUFTQSxPQUFPLFFBQVEsSUFBSTtBQUM1QixTQUFTQyxRQUFRLFFBQVEsTUFBTTtBQUMvQixPQUFPQyxLQUFLLE1BQU0sT0FBTztBQUN6QixTQUFTQyxHQUFHLEVBQUVDLElBQUksUUFBUSxjQUFjO0FBQ3hDLFNBQVNDLE1BQU0sUUFBUSxvQkFBb0I7QUFFM0MsT0FBTyxTQUFTQyxxQkFBcUJBLENBQUNDLElBQUksRUFBRSxNQUFNLENBQUMsRUFBRSxNQUFNLENBQUM7RUFDMUQsTUFBTUMsT0FBTyxHQUFHUixPQUFPLENBQUMsQ0FBQztFQUN6QixNQUFNUyxHQUFHLEdBQUdKLE1BQU0sQ0FBQyxDQUFDOztFQUVwQjtFQUNBLE1BQU1LLGNBQWMsR0FBR0gsSUFBSSxDQUFDSSxVQUFVLENBQUNILE9BQU8sQ0FBQyxHQUMzQyxHQUFHLEdBQUdELElBQUksQ0FBQ0ssS0FBSyxDQUFDSixPQUFPLENBQUNLLE1BQU0sQ0FBQyxHQUNoQyxJQUFJO0VBRVIsTUFBTUMsYUFBYSxHQUFHUCxJQUFJLENBQUNJLFVBQVUsQ0FBQ0YsR0FBRyxDQUFDLEdBQUcsSUFBSSxHQUFHUixRQUFRLENBQUNRLEdBQUcsRUFBRUYsSUFBSSxDQUFDLEdBQUcsSUFBSTs7RUFFOUU7RUFDQSxJQUFJRyxjQUFjLElBQUlJLGFBQWEsRUFBRTtJQUNuQyxPQUFPSixjQUFjLENBQUNHLE1BQU0sSUFBSUMsYUFBYSxDQUFDRCxNQUFNLEdBQ2hESCxjQUFjLEdBQ2RJLGFBQWE7RUFDbkI7RUFFQSxPQUFPSixjQUFjLElBQUlJLGFBQWEsSUFBSVAsSUFBSTtBQUNoRDtBQUVBLE9BQU8sU0FBQVEseUJBQUFDLEVBQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFBa0M7SUFBQUM7RUFBQSxJQUFBSCxFQUl4QztFQUFBLElBQUFJLEVBQUE7RUFBQSxJQUFBSCxDQUFBLFFBQUFFLFVBQUE7SUFDcUJDLEVBQUEsR0FBQWQscUJBQXFCLENBQUNhLFVBQVUsQ0FBQztJQUFBRixDQUFBLE1BQUFFLFVBQUE7SUFBQUYsQ0FBQSxNQUFBRyxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBSCxDQUFBO0VBQUE7RUFBckQsTUFBQUksV0FBQSxHQUFvQkQsRUFBaUM7RUFBQSxJQUFBRSxFQUFBO0VBQUEsSUFBQUwsQ0FBQSxRQUFBSSxXQUFBO0lBR25EQyxFQUFBLElBQUMsR0FBRyxDQUFlLGFBQVEsQ0FBUixRQUFRLENBQVcsUUFBQyxDQUFELEdBQUMsQ0FDckMsQ0FBQyxJQUFJLENBQU8sS0FBTSxDQUFOLE1BQU0sQ0FBQyxrQkFDRUQsWUFBVSxDQUFFLGtCQUNqQyxFQUZDLElBQUksQ0FHUCxFQUpDLEdBQUcsQ0FJRTtJQUFBSixDQUFBLE1BQUFJLFdBQUE7SUFBQUosQ0FBQSxNQUFBSyxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBTCxDQUFBO0VBQUE7RUFBQSxPQUpOSyxFQUlNO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/components/messageActions.tsx`

**信息:**
- 行数: 450
- 大小: 54948 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import type { RefObject } from 'react';
import React, { useCallback, useMemo, useRef } from 'react';
import { Box, Text } from '../ink.js';
import { useKeybindings } from '../keybindings/useKeybinding.js';
import { logEvent } from '../services/analytics/index.js';
import type { NormalizedUserMessage, RenderableMessage } from '../types/message.js';
import { isEmptyMessageText, SYNTHETIC_MESSAGES } from '../utils/messages.js';
const NAVIGABLE_TYPES = ['user', 'assistant', 'grouped_tool_use', 'collapsed_read_search', 'system', 'attachment'] as const;
export type NavigableType = (typeof NAVIGABLE_TYPES)[number];
export type NavigableOf<T extends NavigableType> = Extract<RenderableMessage, {
  type: T;
}>;
export type NavigableMessage = RenderableMessage;

// Tier-2 blocklist (tier-1 is height > 0) — things that render but aren't actionable.
export function isNavigableMessage(msg: NavigableMessage): boolean {
  switch (msg.type) {
    case 'assistant':
      {
        const b = msg.message.content[0];
        // Text responses (minus AssistantTextMessage's return-null cases — tier-1
        // misses unmeasured virtual items), or tool calls with extractable input.
        return b?.type === 'text' && !isEmptyMessageText(b.text) && !SYNTHETIC_MESSAGES.has(b.text) || b?.type === 'tool_use' && b.name in PRIMARY_INPUT;
      }
    case 'user':
      {
        if (msg.isMeta || msg.isCompactSummary) return false;
        const b = msg.message.content[0];
        if (b?.type !== 'text') return false;
        // Interrupt etc. — synthetic, not user-authored.
        if (SYNTHETIC_MESSAGES.has(b.text)) return false;
        // Same filter as VirtualMessageList sticky-prompt: XML-wrapped (command
        // expansions, bash-stdout, etc.) aren't real prompts.
        return !stripSystemReminders(b.text).startsWith('<');
      }
    case 'system':
      // biome-ignore lint/nursery/useExhaustiveSwitchCases: blocklist — fallthrough return-true is the design
      switch (msg.subtype) {
        case 'api_metrics':
        case 'stop_hook_summary':
        case 'turn_duration':
        case 'memory_saved':
        case 'agents_killed':
        case 'away_summary':
        case 'thinking':
          return false;
      }
      return true;

```

---


### `src/components/messages/AdvisorMessage.tsx`

**信息:**
- 行数: 158
- 大小: 14479 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React from 'react';
import { Box, Text } from '../../ink.js';
import type { AdvisorBlock } from '../../utils/advisor.js';
import { renderModelName } from '../../utils/model/model.js';
import { jsonStringify } from '../../utils/slowOperations.js';
import { CtrlOToExpand } from '../CtrlOToExpand.js';
import { MessageResponse } from '../MessageResponse.js';
import { ToolUseLoader } from '../ToolUseLoader.js';
type Props = {
  block: AdvisorBlock;
  addMargin: boolean;
  resolvedToolUseIDs: Set<string>;
  erroredToolUseIDs: Set<string>;
  shouldAnimate: boolean;
  verbose: boolean;
  advisorModel?: string;
};
export function AdvisorMessage(t0) {
  const $ = _c(30);
  const {
    block,
    addMargin,
    resolvedToolUseIDs,
    erroredToolUseIDs,
    shouldAnimate,
    verbose,
    advisorModel
  } = t0;
  if (block.type === "server_tool_use") {
    let t1;
    if ($[0] !== block.input) {
      t1 = block.input && Object.keys(block.input).length > 0 ? jsonStringify(block.input) : null;
      $[0] = block.input;
      $[1] = t1;
    } else {
      t1 = $[1];
    }
    const input = t1;
    const t2 = addMargin ? 1 : 0;
    let t3;
    if ($[2] !== block.id || $[3] !== resolvedToolUseIDs) {
      t3 = resolvedToolUseIDs.has(block.id);
      $[2] = block.id;
      $[3] = resolvedToolUseIDs;
      $[4] = t3;
    } else {
      t3 = $[4];
    }

```

---


### `src/components/messages/AssistantRedactedThinkingMessage.tsx`

**信息:**
- 行数: 31
- 大小: 2603 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../../ink.js';
type Props = {
  addMargin: boolean;
};
export function AssistantRedactedThinkingMessage(t0) {
  const $ = _c(3);
  const {
    addMargin: t1
  } = t0;
  const addMargin = t1 === undefined ? false : t1;
  const t2 = addMargin ? 1 : 0;
  let t3;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = <Text dimColor={true} italic={true}>✻ Thinking…</Text>;
    $[0] = t3;
  } else {
    t3 = $[0];
  }
  let t4;
  if ($[1] !== t2) {
    t4 = <Box marginTop={t2}>{t3}</Box>;
    $[1] = t2;
    $[2] = t4;
  } else {
    t4 = $[2];
  }
  return t4;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJveCIsIlRleHQiLCJQcm9wcyIsImFkZE1hcmdpbiIsIkFzc2lzdGFudFJlZGFjdGVkVGhpbmtpbmdNZXNzYWdlIiwidDAiLCIkIiwiX2MiLCJ0MSIsInVuZGVmaW5lZCIsInQyIiwidDMiLCJTeW1ib2wiLCJmb3IiLCJ0NCJdLCJzb3VyY2VzIjpbIkFzc2lzdGFudFJlZGFjdGVkVGhpbmtpbmdNZXNzYWdlLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBCb3gsIFRleHQgfSBmcm9tICcuLi8uLi9pbmsuanMnXG5cbnR5cGUgUHJvcHMgPSB7XG4gIGFkZE1hcmdpbjogYm9vbGVhblxufVxuXG5leHBvcnQgZnVuY3Rpb24gQXNzaXN0YW50UmVkYWN0ZWRUaGlua2luZ01lc3NhZ2Uoe1xuICBhZGRNYXJnaW4gPSBmYWxzZSxcbn06IFByb3BzKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgcmV0dXJuIChcbiAgICA8Qm94IG1hcmdpblRvcD17YWRkTWFyZ2luID8gMSA6IDB9PlxuICAgICAgPFRleHQgZGltQ29sb3IgaXRhbGljPlxuICAgICAgICDinLsgVGhpbmtpbmfigKZcbiAgICAgIDwvVGV4dD5cbiAgICA8L0JveD5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiO0FBQUEsT0FBT0EsS0FBSyxNQUFNLE9BQU87QUFDekIsU0FBU0MsR0FBRyxFQUFFQyxJQUFJLFFBQVEsY0FBYztBQUV4QyxLQUFLQyxLQUFLLEdBQUc7RUFDWEMsU0FBUyxFQUFFLE9BQU87QUFDcEIsQ0FBQztBQUVELE9BQU8sU0FBQUMsaUNBQUFDLEVBQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFBMEM7SUFBQUosU0FBQSxFQUFBSztFQUFBLElBQUFILEVBRXpDO0VBRE4sTUFBQUYsU0FBQSxHQUFBSyxFQUFpQixLQUFqQkMsU0FBaUIsR0FBakIsS0FBaUIsR0FBakJELEVBQWlCO0VBR0MsTUFBQUUsRUFBQSxHQUFBUCxTQUFTLEdBQVQsQ0FBaUIsR0FBakIsQ0FBaUI7RUFBQSxJQUFBUSxFQUFBO0VBQUEsSUFBQUwsQ0FBQSxRQUFBTSxNQUFBLENBQUFDLEdBQUE7SUFDL0JGLEVBQUEsSUFBQyxJQUFJLENBQUMsUUFBUSxDQUFSLEtBQU8sQ0FBQyxDQUFDLE1BQU0sQ0FBTixLQUFLLENBQUMsQ0FBQyxXQUV0QixFQUZDLElBQUksQ0FFRTtJQUFBTCxDQUFBLE1BQUFLLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFMLENBQUE7RUFBQTtFQUFBLElBQUFRLEVBQUE7RUFBQSxJQUFBUixDQUFBLFFBQUFJLEVBQUE7SUFIVEksRUFBQSxJQUFDLEdBQUcsQ0FBWSxTQUFpQixDQUFqQixDQUFBSixFQUFnQixDQUFDLENBQy9CLENBQUFDLEVBRU0sQ0FDUixFQUpDLEdBQUcsQ0FJRTtJQUFBTCxDQUFBLE1BQUFJLEVBQUE7SUFBQUosQ0FBQSxNQUFBUSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBUixDQUFBO0VBQUE7RUFBQSxPQUpOUSxFQUlNO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/components/messages/AssistantTextMessage.tsx`

**信息:**
- 行数: 270
- 大小: 30427 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import React, { useContext } from 'react';
import { ERROR_MESSAGE_USER_ABORT } from 'src/services/compact/compact.js';
import { isRateLimitErrorMessage } from 'src/services/rateLimitMessages.js';
import { BLACK_CIRCLE } from '../../constants/figures.js';
import { Box, NoSelect, Text } from '../../ink.js';
import { API_ERROR_MESSAGE_PREFIX, API_TIMEOUT_ERROR_MESSAGE, CREDIT_BALANCE_TOO_LOW_ERROR_MESSAGE, CUSTOM_OFF_SWITCH_MESSAGE, INVALID_API_KEY_ERROR_MESSAGE, INVALID_API_KEY_ERROR_MESSAGE_EXTERNAL, ORG_DISABLED_ERROR_MESSAGE_ENV_KEY, ORG_DISABLED_ERROR_MESSAGE_ENV_KEY_WITH_OAUTH, PROMPT_TOO_LONG_ERROR_MESSAGE, startsWithApiErrorPrefix, TOKEN_REVOKED_ERROR_MESSAGE } from '../../services/api/errors.js';
import { isEmptyMessageText, NO_RESPONSE_REQUESTED } from '../../utils/messages.js';
import { getUpgradeMessage } from '../../utils/model/contextWindowUpgradeCheck.js';
import { getDefaultSonnetModel, renderModelName } from '../../utils/model/model.js';
import { isMacOsKeychainLocked } from '../../utils/secureStorage/macOsKeychainStorage.js';
import { CtrlOToExpand } from '../CtrlOToExpand.js';
import { InterruptedByUser } from '../InterruptedByUser.js';
import { Markdown } from '../Markdown.js';
import { MessageResponse } from '../MessageResponse.js';
import { MessageActionsSelectedContext } from '../messageActions.js';
import { RateLimitMessage } from './RateLimitMessage.js';
const MAX_API_ERROR_CHARS = 1000;
type Props = {
  param: TextBlockParam;
  addMargin: boolean;
  shouldShowDot: boolean;
  verbose: boolean;
  width?: number | string;
  onOpenRateLimitOptions?: () => void;
};
function InvalidApiKeyMessage() {
  const $ = _c(2);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = isMacOsKeychainLocked();
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  const isKeychainLocked = t0;
  let t1;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <MessageResponse><Box flexDirection="column"><Text color="error">{INVALID_API_KEY_ERROR_MESSAGE}</Text>{isKeychainLocked && <Text dimColor={true}>· Run in another terminal: security unlock-keychain</Text>}</Box></MessageResponse>;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  return t1;
}
export function AssistantTextMessage(t0) {
  const $ = _c(34);
  const {
    param: t1,

```

---


### `src/components/messages/AssistantThinkingMessage.tsx`

**信息:**
- 行数: 86
- 大小: 8082 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ThinkingBlock, ThinkingBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import React from 'react';
import { Box, Text } from '../../ink.js';
import { CtrlOToExpand } from '../CtrlOToExpand.js';
import { Markdown } from '../Markdown.js';
type Props = {
  // Accept either full ThinkingBlock/ThinkingBlockParam or a minimal shape with just type and thinking
  param: ThinkingBlock | ThinkingBlockParam | {
    type: 'thinking';
    thinking: string;
  };
  addMargin: boolean;
  isTranscriptMode: boolean;
  verbose: boolean;
  /** When true, hide this thinking block entirely (used for past thinking in transcript mode) */
  hideInTranscript?: boolean;
};
export function AssistantThinkingMessage(t0) {
  const $ = _c(9);
  const {
    param: t1,
    addMargin: t2,
    isTranscriptMode,
    verbose,
    hideInTranscript: t3
  } = t0;
  const {
    thinking
  } = t1;
  const addMargin = t2 === undefined ? false : t2;
  const hideInTranscript = t3 === undefined ? false : t3;
  if (!thinking) {
    return null;
  }
  if (hideInTranscript) {
    return null;
  }
  const shouldShowFullThinking = isTranscriptMode || verbose;
  if (!shouldShowFullThinking) {
    const t4 = addMargin ? 1 : 0;
    let t5;
    if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
      t5 = <Text dimColor={true} italic={true}>{"\u2234 Thinking"} <CtrlOToExpand /></Text>;
      $[0] = t5;
    } else {
      t5 = $[0];
    }
    let t6;
    if ($[1] !== t4) {

```

---


### `src/components/messages/AssistantToolUseMessage.tsx`

**信息:**
- 行数: 368
- 大小: 45285 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ToolUseBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import React, { useMemo } from 'react';
import { useTerminalSize } from 'src/hooks/useTerminalSize.js';
import type { ThemeName } from 'src/utils/theme.js';
import type { Command } from '../../commands.js';
import { BLACK_CIRCLE } from '../../constants/figures.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { Box, Text, useTheme } from '../../ink.js';
import { useAppStateMaybeOutsideOfProvider } from '../../state/AppState.js';
import { findToolByName, type Tool, type ToolProgressData, type Tools } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import { useIsClassifierChecking } from '../../utils/classifierApprovalsHook.js';
import { logError } from '../../utils/log.js';
import type { buildMessageLookups } from '../../utils/messages.js';
import { MessageResponse } from '../MessageResponse.js';
import { useSelectedMessageBg } from '../messageActions.js';
import { SentryErrorBoundary } from '../SentryErrorBoundary.js';
import { ToolUseLoader } from '../ToolUseLoader.js';
import { HookProgressMessage } from './HookProgressMessage.js';
type Props = {
  param: ToolUseBlockParam;
  addMargin: boolean;
  tools: Tools;
  commands: Command[];
  verbose: boolean;
  inProgressToolUseIDs: Set<string>;
  progressMessagesForMessage: ProgressMessage[];
  shouldAnimate: boolean;
  shouldShowDot: boolean;
  inProgressToolCallCount?: number;
  lookups: ReturnType<typeof buildMessageLookups>;
  isTranscriptMode?: boolean;
};
export function AssistantToolUseMessage(t0) {
  const $ = _c(81);
  const {
    param,
    addMargin,
    tools,
    commands,
    verbose,
    inProgressToolUseIDs,
    progressMessagesForMessage,
    shouldAnimate,
    shouldShowDot,
    inProgressToolCallCount,
    lookups,
    isTranscriptMode
  } = t0;

```

---


### `src/components/messages/AttachmentMessage.tsx`

**信息:**
- 行数: 536
- 大小: 71430 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
import React, { useMemo } from 'react';
import { Ansi, Box, Text } from '../../ink.js';
import type { Attachment } from 'src/utils/attachments.js';
import type { NullRenderingAttachmentType } from './nullRenderingAttachments.js';
import { useAppState } from '../../state/AppState.js';
import { getDisplayPath } from 'src/utils/file.js';
import { formatFileSize } from 'src/utils/format.js';
import { MessageResponse } from '../MessageResponse.js';
import { basename, sep } from 'path';
import { UserTextMessage } from './UserTextMessage.js';
import { DiagnosticsDisplay } from '../DiagnosticsDisplay.js';
import { getContentText } from 'src/utils/messages.js';
import type { Theme } from 'src/utils/theme.js';
import { UserImageMessage } from './UserImageMessage.js';
import { toInkColor } from '../../utils/ink.js';
import { jsonParse } from '../../utils/slowOperations.js';
import { plural } from '../../utils/stringUtils.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js';
import { tryRenderPlanApprovalMessage, formatTeammateMessageContent } from './PlanApprovalMessage.js';
import { BLACK_CIRCLE } from '../../constants/figures.js';
import { TeammateMessageContent } from './UserTeammateMessage.js';
import { isShutdownApproved } from '../../utils/teammateMailbox.js';
import { CtrlOToExpand } from '../CtrlOToExpand.js';
import { FilePathLink } from '../FilePathLink.js';
import { feature } from 'bun:bundle';
import { useSelectedMessageBg } from '../messageActions.js';
type Props = {
  addMargin: boolean;
  attachment: Attachment;
  verbose: boolean;
  isTranscriptMode?: boolean;
};
export function AttachmentMessage({
  attachment,
  addMargin,
  verbose,
  isTranscriptMode
}: Props): React.ReactNode {
  const bg = useSelectedMessageBg();
  // Hoisted to mount-time — per-message component, re-renders on every scroll.
  const isDemoEnv = feature('EXPERIMENTAL_SKILL_SEARCH') ?
  // biome-ignore lint/correctness/useHookAtTopLevel: feature() is a compile-time constant
  useMemo(() => isEnvTruthy(process.env.IS_DEMO), []) : false;
  // Handle teammate_mailbox BEFORE switch
  if (isAgentSwarmsEnabled() && attachment.type === 'teammate_mailbox') {
    // Filter out idle notifications BEFORE counting - they are hidden in the UI
    // so showing them in the count would be confusing ("2 messages in mailbox:" with nothing shown)

```

---


### `src/components/messages/CollapsedReadSearchContent.tsx`

**信息:**
- 行数: 484
- 大小: 78078 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import { basename } from 'path';
import React, { useRef } from 'react';
import { useMinDisplayTime } from '../../hooks/useMinDisplayTime.js';
import { Ansi, Box, Text, useTheme } from '../../ink.js';
import { findToolByName, type Tools } from '../../Tool.js';
import { getReplPrimitiveTools } from '../../tools/REPLTool/primitiveTools.js';
import type { CollapsedReadSearchGroup, NormalizedAssistantMessage } from '../../types/message.js';
import { uniq } from '../../utils/array.js';
import { getToolUseIdsFromCollapsedGroup } from '../../utils/collapseReadSearch.js';
import { getDisplayPath } from '../../utils/file.js';
import { formatDuration, formatSecondsShort } from '../../utils/format.js';
import { isFullscreenEnvEnabled } from '../../utils/fullscreen.js';
import type { buildMessageLookups } from '../../utils/messages.js';
import type { ThemeName } from '../../utils/theme.js';
import { CtrlOToExpand } from '../CtrlOToExpand.js';
import { useSelectedMessageBg } from '../messageActions.js';
import { PrBadge } from '../PrBadge.js';
import { ToolUseLoader } from '../ToolUseLoader.js';

/* eslint-disable @typescript-eslint/no-require-imports */
const teamMemCollapsed = feature('TEAMMEM') ? require('./teamMemCollapsed.js') as typeof import('./teamMemCollapsed.js') : null;
/* eslint-enable @typescript-eslint/no-require-imports */

// Hold each ⤿ hint for a minimum duration so fast-completing tool calls
// (bash commands, file reads, search patterns) are actually readable instead
// of flickering past in a single frame.
const MIN_HINT_DISPLAY_MS = 700;
type Props = {
  message: CollapsedReadSearchGroup;
  inProgressToolUseIDs: Set<string>;
  shouldAnimate: boolean;
  verbose: boolean;
  tools: Tools;
  lookups: ReturnType<typeof buildMessageLookups>;
  /** True if this is the currently active collapsed group (last one, still loading) */
  isActiveGroup?: boolean;
};

/** Render a single tool use in verbose mode */
function VerboseToolUse(t0) {
  const $ = _c(24);
  const {
    content,
    tools,
    lookups,
    inProgressToolUseIDs,
    shouldAnimate,
    theme

```

---


### `src/components/messages/CompactBoundaryMessage.tsx`

**信息:**
- 行数: 18
- 大小: 2275 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { useShortcutDisplay } from '../../keybindings/useShortcutDisplay.js';
export function CompactBoundaryMessage() {
  const $ = _c(2);
  const historyShortcut = useShortcutDisplay("app:toggleTranscript", "Global", "ctrl+o");
  let t0;
  if ($[0] !== historyShortcut) {
    t0 = <Box marginY={1}><Text dimColor={true}>✻ Conversation compacted ({historyShortcut} for history)</Text></Box>;
    $[0] = historyShortcut;
    $[1] = t0;
  } else {
    t0 = $[1];
  }
  return t0;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJveCIsIlRleHQiLCJ1c2VTaG9ydGN1dERpc3BsYXkiLCJDb21wYWN0Qm91bmRhcnlNZXNzYWdlIiwiJCIsIl9jIiwiaGlzdG9yeVNob3J0Y3V0IiwidDAiXSwic291cmNlcyI6WyJDb21wYWN0Qm91bmRhcnlNZXNzYWdlLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IEJveCwgVGV4dCB9IGZyb20gJy4uLy4uL2luay5qcydcbmltcG9ydCB7IHVzZVNob3J0Y3V0RGlzcGxheSB9IGZyb20gJy4uLy4uL2tleWJpbmRpbmdzL3VzZVNob3J0Y3V0RGlzcGxheS5qcydcblxuZXhwb3J0IGZ1bmN0aW9uIENvbXBhY3RCb3VuZGFyeU1lc3NhZ2UoKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgY29uc3QgaGlzdG9yeVNob3J0Y3V0ID0gdXNlU2hvcnRjdXREaXNwbGF5KFxuICAgICdhcHA6dG9nZ2xlVHJhbnNjcmlwdCcsXG4gICAgJ0dsb2JhbCcsXG4gICAgJ2N0cmwrbycsXG4gIClcblxuICByZXR1cm4gKFxuICAgIDxCb3ggbWFyZ2luWT17MX0+XG4gICAgICA8VGV4dCBkaW1Db2xvcj5cbiAgICAgICAg4py7IENvbnZlcnNhdGlvbiBjb21wYWN0ZWQgKHtoaXN0b3J5U2hvcnRjdXR9IGZvciBoaXN0b3J5KVxuICAgICAgPC9UZXh0PlxuICAgIDwvQm94PlxuICApXG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxRQUFRLGNBQWM7QUFDeEMsU0FBU0Msa0JBQWtCLFFBQVEseUNBQXlDO0FBRTVFLE9BQU8sU0FBQUMsdUJBQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFDTCxNQUFBQyxlQUFBLEdBQXdCSixrQkFBa0IsQ0FDeEMsc0JBQXNCLEVBQ3RCLFFBQVEsRUFDUixRQUNGLENBQUM7RUFBQSxJQUFBSyxFQUFBO0VBQUEsSUFBQUgsQ0FBQSxRQUFBRSxlQUFBO0lBR0NDLEVBQUEsSUFBQyxHQUFHLENBQVUsT0FBQyxDQUFELEdBQUMsQ0FDYixDQUFDLElBQUksQ0FBQyxRQUFRLENBQVIsS0FBTyxDQUFDLENBQUMsMEJBQ2NELGdCQUFjLENBQUUsYUFDN0MsRUFGQyxJQUFJLENBR1AsRUFKQyxHQUFHLENBSUU7SUFBQUYsQ0FBQSxNQUFBRSxlQUFBO0lBQUFGLENBQUEsTUFBQUcsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUgsQ0FBQTtFQUFBO0VBQUEsT0FKTkcsRUFJTTtBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/messages/GroupedToolUseContent.tsx`

**信息:**
- 行数: 58
- 大小: 8289 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { ToolResultBlockParam, ToolUseBlockParam } from '@anthropic-ai/sdk/resources/messages/messages.mjs';
import * as React from 'react';
import { filterToolProgressMessages, findToolByName, type Tools } from '../../Tool.js';
import type { GroupedToolUseMessage } from '../../types/message.js';
import type { buildMessageLookups } from '../../utils/messages.js';
type Props = {
  message: GroupedToolUseMessage;
  tools: Tools;
  lookups: ReturnType<typeof buildMessageLookups>;
  inProgressToolUseIDs: Set<string>;
  shouldAnimate: boolean;
};
export function GroupedToolUseContent({
  message,
  tools,
  lookups,
  inProgressToolUseIDs,
  shouldAnimate
}: Props): React.ReactNode {
  const tool = findToolByName(tools, message.toolName);
  if (!tool?.renderGroupedToolUse) {
    return null;
  }

  // Build a map from tool_use_id to result data
  const resultsByToolUseId = new Map<string, {
    param: ToolResultBlockParam;
    output: unknown;
  }>();
  for (const resultMsg of message.results) {
    for (const content of resultMsg.message.content) {
      if (content.type === 'tool_result') {
        resultsByToolUseId.set(content.tool_use_id, {
          param: content,
          output: resultMsg.toolUseResult
        });
      }
    }
  }
  const toolUsesData = message.messages.map(msg => {
    const content = msg.message.content[0];
    const result = resultsByToolUseId.get(content.id);
    return {
      param: content as ToolUseBlockParam,
      isResolved: lookups.resolvedToolUseIDs.has(content.id),
      isError: lookups.erroredToolUseIDs.has(content.id),
      isInProgress: inProgressToolUseIDs.has(content.id),
      progressMessages: filterToolProgressMessages(lookups.progressMessagesByToolUseID.get(content.id) ?? []),
      result
    };

```

---


### `src/components/messages/HighlightedThinkingText.tsx`

**信息:**
- 行数: 162
- 大小: 14902 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useContext } from 'react';
import { useQueuedMessage } from '../../context/QueuedMessageContext.js';
import { Box, Text } from '../../ink.js';
import { formatBriefTimestamp } from '../../utils/formatBriefTimestamp.js';
import { findThinkingTriggerPositions, getRainbowColor, isUltrathinkEnabled } from '../../utils/thinking.js';
import { MessageActionsSelectedContext } from '../messageActions.js';
type Props = {
  text: string;
  useBriefLayout?: boolean;
  timestamp?: string;
};
export function HighlightedThinkingText(t0) {
  const $ = _c(31);
  const {
    text,
    useBriefLayout,
    timestamp
  } = t0;
  const isQueued = useQueuedMessage()?.isQueued ?? false;
  const isSelected = useContext(MessageActionsSelectedContext);
  const pointerColor = isSelected ? "suggestion" : "subtle";
  if (useBriefLayout) {
    let t1;
    if ($[0] !== timestamp) {
      t1 = timestamp ? formatBriefTimestamp(timestamp) : "";
      $[0] = timestamp;
      $[1] = t1;
    } else {
      t1 = $[1];
    }
    const ts = t1;
    const t2 = isQueued ? "subtle" : "briefLabelYou";
    let t3;
    if ($[2] !== t2) {
      t3 = <Text color={t2}>You</Text>;
      $[2] = t2;
      $[3] = t3;
    } else {
      t3 = $[3];
    }
    let t4;
    if ($[4] !== ts) {
      t4 = ts ? <Text dimColor={true}> {ts}</Text> : null;
      $[4] = ts;
      $[5] = t4;
    } else {
      t4 = $[5];

```

---


### `src/components/messages/HookProgressMessage.tsx`

**信息:**
- 行数: 116
- 大小: 10613 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import type { HookEvent } from 'src/entrypoints/agentSdkTypes.js';
import type { buildMessageLookups } from 'src/utils/messages.js';
import { Box, Text } from '../../ink.js';
import { MessageResponse } from '../MessageResponse.js';
type Props = {
  hookEvent: HookEvent;
  lookups: ReturnType<typeof buildMessageLookups>;
  toolUseID: string;
  verbose: boolean;
  isTranscriptMode?: boolean;
};
export function HookProgressMessage(t0) {
  const $ = _c(22);
  const {
    hookEvent,
    lookups,
    toolUseID,
    isTranscriptMode
  } = t0;
  let t1;
  if ($[0] !== hookEvent || $[1] !== lookups.inProgressHookCounts || $[2] !== toolUseID) {
    t1 = lookups.inProgressHookCounts.get(toolUseID)?.get(hookEvent) ?? 0;
    $[0] = hookEvent;
    $[1] = lookups.inProgressHookCounts;
    $[2] = toolUseID;
    $[3] = t1;
  } else {
    t1 = $[3];
  }
  const inProgressHookCount = t1;
  const resolvedHookCount = lookups.resolvedHookCounts.get(toolUseID)?.get(hookEvent) ?? 0;
  if (inProgressHookCount === 0) {
    return null;
  }
  if (hookEvent === "PreToolUse" || hookEvent === "PostToolUse") {
    if (isTranscriptMode) {
      let t2;
      if ($[4] !== inProgressHookCount) {
        t2 = <Text dimColor={true}>{inProgressHookCount} </Text>;
        $[4] = inProgressHookCount;
        $[5] = t2;
      } else {
        t2 = $[5];
      }
      let t3;
      if ($[6] !== hookEvent) {
        t3 = <Text dimColor={true} bold={true}>{hookEvent}</Text>;
        $[6] = hookEvent;

```

---


### `src/components/messages/PlanApprovalMessage.tsx`

**信息:**
- 行数: 222
- 大小: 25339 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Markdown } from '../../components/Markdown.js';
import { Box, Text } from '../../ink.js';
import { jsonParse } from '../../utils/slowOperations.js';
import { type IdleNotificationMessage, isIdleNotification, isPlanApprovalRequest, isPlanApprovalResponse, type PlanApprovalRequestMessage, type PlanApprovalResponseMessage } from '../../utils/teammateMailbox.js';
import { getShutdownMessageSummary } from './ShutdownMessage.js';
import { getTaskAssignmentSummary } from './TaskAssignmentMessage.js';
type PlanApprovalRequestProps = {
  request: PlanApprovalRequestMessage;
};

/**
 * Renders a plan approval request with a planMode-colored border,
 * showing the plan content and instructions for approving/rejecting.
 */
export function PlanApprovalRequestDisplay(t0) {
  const $ = _c(10);
  const {
    request
  } = t0;
  let t1;
  if ($[0] !== request.from) {
    t1 = <Box marginBottom={1}><Text color="planMode" bold={true}>Plan Approval Request from {request.from}</Text></Box>;
    $[0] = request.from;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] !== request.planContent) {
    t2 = <Box borderStyle="dashed" borderColor="subtle" borderLeft={false} borderRight={false} flexDirection="column" paddingX={1} marginBottom={1}><Markdown>{request.planContent}</Markdown></Box>;
    $[2] = request.planContent;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  let t3;
  if ($[4] !== request.planFilePath) {
    t3 = <Text dimColor={true}>Plan file: {request.planFilePath}</Text>;
    $[4] = request.planFilePath;
    $[5] = t3;
  } else {
    t3 = $[5];
  }
  let t4;
  if ($[6] !== t1 || $[7] !== t2 || $[8] !== t3) {
    t4 = <Box flexDirection="column" marginY={1}><Box borderStyle="round" borderColor="planMode" flexDirection="column" paddingX={1}>{t1}{t2}{t3}</Box></Box>;
    $[6] = t1;
    $[7] = t2;

```

---


### `src/components/messages/RateLimitMessage.tsx`

**信息:**
- 行数: 161
- 大小: 17162 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useEffect, useMemo, useState } from 'react';
import { extraUsage } from 'src/commands/extra-usage/index.js';
import { Box, Text } from 'src/ink.js';
import { useClaudeAiLimits } from 'src/services/claudeAiLimitsHook.js';
import { shouldProcessMockLimits } from 'src/services/rateLimitMocking.js'; // Used for /mock-limits command
import { getRateLimitTier, getSubscriptionType, isClaudeAISubscriber } from 'src/utils/auth.js';
import { hasClaudeAiBillingAccess } from 'src/utils/billing.js';
import { MessageResponse } from '../MessageResponse.js';
type UpsellParams = {
  shouldShowUpsell: boolean;
  isMax20x: boolean;
  isExtraUsageCommandEnabled: boolean;
  shouldAutoOpenRateLimitOptionsMenu: boolean;
  isTeamOrEnterprise: boolean;
  hasBillingAccess: boolean;
};
export function getUpsellMessage({
  shouldShowUpsell,
  isMax20x,
  isExtraUsageCommandEnabled,
  shouldAutoOpenRateLimitOptionsMenu,
  isTeamOrEnterprise,
  hasBillingAccess
}: UpsellParams): string | null {
  if (!shouldShowUpsell) return null;
  if (isMax20x) {
    if (isExtraUsageCommandEnabled) {
      return '/extra-usage to finish what you\u2019re working on.';
    }
    return '/login to switch to an API usage-billed account.';
  }
  if (shouldAutoOpenRateLimitOptionsMenu) {
    return 'Opening your options\u2026';
  }
  if (!isTeamOrEnterprise && !isExtraUsageCommandEnabled) {
    return '/upgrade to increase your usage limit.';
  }
  if (isTeamOrEnterprise) {
    if (!isExtraUsageCommandEnabled) return null;
    if (hasBillingAccess) {
      return '/extra-usage to finish what you\u2019re working on.';
    }
    return '/extra-usage to request more usage from your admin.';
  }
  return '/upgrade or /extra-usage to finish what you\u2019re working on.';
}
type RateLimitMessageProps = {
  text: string;
  onOpenRateLimitOptions?: () => void;

```

---


### `src/components/messages/ShutdownMessage.tsx`

**信息:**
- 行数: 132
- 大小: 14493 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { isShutdownApproved, isShutdownRejected, isShutdownRequest, type ShutdownRejectedMessage, type ShutdownRequestMessage } from '../../utils/teammateMailbox.js';
type ShutdownRequestProps = {
  request: ShutdownRequestMessage;
};

/**
 * Renders a shutdown request with a warning-colored border.
 */
export function ShutdownRequestDisplay(t0) {
  const $ = _c(7);
  const {
    request
  } = t0;
  let t1;
  if ($[0] !== request.from) {
    t1 = <Box marginBottom={1}><Text color="warning" bold={true}>Shutdown request from {request.from}</Text></Box>;
    $[0] = request.from;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] !== request.reason) {
    t2 = request.reason && <Box><Text>Reason: {request.reason}</Text></Box>;
    $[2] = request.reason;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  let t3;
  if ($[4] !== t1 || $[5] !== t2) {
    t3 = <Box flexDirection="column" marginY={1}><Box borderStyle="round" borderColor="warning" flexDirection="column" paddingX={1} paddingY={1}>{t1}{t2}</Box></Box>;
    $[4] = t1;
    $[5] = t2;
    $[6] = t3;
  } else {
    t3 = $[6];
  }
  return t3;
}
type ShutdownRejectedProps = {
  response: ShutdownRejectedMessage;
};

/**
 * Renders a shutdown rejected message with a subtle (grey) border.
 */

```

---


### `src/components/messages/SnipBoundaryMessage.tsx`

**信息:**
- 行数: 3
- 大小: 56 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function SnipBoundaryMessage() {
  return null
}

```

---


### `src/components/messages/SystemAPIErrorMessage.tsx`

**信息:**
- 行数: 141
- 大小: 12285 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useState } from 'react';
import { Box, Text } from 'src/ink.js';
import { formatAPIError } from 'src/services/api/errorUtils.js';
import type { SystemAPIErrorMessage } from 'src/types/message.js';
import { useInterval } from 'usehooks-ts';
import { CtrlOToExpand } from '../CtrlOToExpand.js';
import { MessageResponse } from '../MessageResponse.js';
const MAX_API_ERROR_CHARS = 1000;
type Props = {
  message: SystemAPIErrorMessage;
  verbose: boolean;
};
export function SystemAPIErrorMessage(t0) {
  const $ = _c(33);
  const {
    message: t1,
    verbose
  } = t0;
  const {
    retryAttempt,
    error,
    retryInMs,
    maxRetries
  } = t1;
  const hidden = true && retryAttempt < 4;
  const [countdownMs, setCountdownMs] = useState(0);
  const done = countdownMs >= retryInMs;
  let t2;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = () => setCountdownMs(_temp);
    $[0] = t2;
  } else {
    t2 = $[0];
  }
  useInterval(t2, hidden || done ? null : 1000);
  if (hidden) {
    return null;
  }
  let t3;
  if ($[1] !== countdownMs || $[2] !== retryInMs) {
    t3 = Math.round((retryInMs - countdownMs) / 1000);
    $[1] = countdownMs;
    $[2] = retryInMs;
    $[3] = t3;
  } else {
    t3 = $[3];
  }
  const retryInSecondsLive = Math.max(0, t3);

```

---


### `src/components/messages/SystemTextMessage.tsx`

**信息:**
- 行数: 827
- 大小: 79395 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
import { Box, Text, type TextProps } from '../../ink.js';
import { feature } from 'bun:bundle';
import * as React from 'react';
import { useState } from 'react';
import sample from 'lodash-es/sample.js';
import { BLACK_CIRCLE, REFERENCE_MARK, TEARDROP_ASTERISK } from '../../constants/figures.js';
import figures from 'figures';
import { basename } from 'path';
import { MessageResponse } from '../MessageResponse.js';
import { FilePathLink } from '../FilePathLink.js';
import { openPath } from '../../utils/browser.js';
/* eslint-disable @typescript-eslint/no-require-imports */
const teamMemSaved = feature('TEAMMEM') ? require('./teamMemSaved.js') as typeof import('./teamMemSaved.js') : null;
/* eslint-enable @typescript-eslint/no-require-imports */
import { TURN_COMPLETION_VERBS } from '../../constants/turnCompletionVerbs.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import type { SystemMessage, SystemStopHookSummaryMessage, SystemBridgeStatusMessage, SystemTurnDurationMessage, SystemThinkingMessage, SystemMemorySavedMessage } from '../../types/message.js';
import { SystemAPIErrorMessage } from './SystemAPIErrorMessage.js';
import { formatDuration, formatNumber, formatSecondsShort } from '../../utils/format.js';
import { getGlobalConfig } from '../../utils/config.js';
import Link from '../../ink/components/Link.js';
import ThemedText from '../design-system/ThemedText.js';
import { CtrlOToExpand } from '../CtrlOToExpand.js';
import { useAppStateStore } from '../../state/AppState.js';
import { isBackgroundTask, type TaskState } from '../../tasks/types.js';
import { getPillLabel } from '../../tasks/pillLabel.js';
import { useSelectedMessageBg } from '../messageActions.js';
type Props = {
  message: SystemMessage;
  addMargin: boolean;
  verbose: boolean;
  isTranscriptMode?: boolean;
};
export function SystemTextMessage(t0) {
  const $ = _c(51);
  const {
    message,
    addMargin,
    verbose,
    isTranscriptMode
  } = t0;
  const bg = useSelectedMessageBg();
  if (message.subtype === "turn_duration") {
    let t1;
    if ($[0] !== addMargin || $[1] !== message) {
      t1 = <TurnDurationMessage message={message} addMargin={addMargin} />;
      $[0] = addMargin;
      $[1] = message;

```

---


### `src/components/messages/TaskAssignmentMessage.tsx`

**信息:**
- 行数: 76
- 大小: 8186 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { isTaskAssignment, type TaskAssignmentMessage } from '../../utils/teammateMailbox.js';
type Props = {
  assignment: TaskAssignmentMessage;
};

/**
 * Renders a task assignment with a cyan border (team-related color).
 */
export function TaskAssignmentDisplay(t0) {
  const $ = _c(11);
  const {
    assignment
  } = t0;
  let t1;
  if ($[0] !== assignment.assignedBy || $[1] !== assignment.taskId) {
    t1 = <Box marginBottom={1}><Text color="cyan_FOR_SUBAGENTS_ONLY" bold={true}>Task #{assignment.taskId} assigned by {assignment.assignedBy}</Text></Box>;
    $[0] = assignment.assignedBy;
    $[1] = assignment.taskId;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  let t2;
  if ($[3] !== assignment.subject) {
    t2 = <Box><Text bold={true}>{assignment.subject}</Text></Box>;
    $[3] = assignment.subject;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  let t3;
  if ($[5] !== assignment.description) {
    t3 = assignment.description && <Box marginTop={1}><Text dimColor={true}>{assignment.description}</Text></Box>;
    $[5] = assignment.description;
    $[6] = t3;
  } else {
    t3 = $[6];
  }
  let t4;
  if ($[7] !== t1 || $[8] !== t2 || $[9] !== t3) {
    t4 = <Box flexDirection="column" marginY={1}><Box borderStyle="round" borderColor="cyan_FOR_SUBAGENTS_ONLY" flexDirection="column" paddingX={1} paddingY={1}>{t1}{t2}{t3}</Box></Box>;
    $[7] = t1;
    $[8] = t2;
    $[9] = t3;
    $[10] = t4;
  } else {
    t4 = $[10];

```

---


### `src/components/messages/UserAgentNotificationMessage.tsx`

**信息:**
- 行数: 83
- 大小: 6151 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import { BLACK_CIRCLE } from '../../constants/figures.js';
import { Box, Text, type TextProps } from '../../ink.js';
import { extractTag } from '../../utils/messages.js';
type Props = {
  addMargin: boolean;
  param: TextBlockParam;
};
function getStatusColor(status: string | null): TextProps['color'] {
  switch (status) {
    case 'completed':
      return 'success';
    case 'failed':
      return 'error';
    case 'killed':
      return 'warning';
    default:
      return 'text';
  }
}
export function UserAgentNotificationMessage(t0) {
  const $ = _c(12);
  const {
    addMargin,
    param: t1
  } = t0;
  const {
    text
  } = t1;
  let t2;
  if ($[0] !== text) {
    t2 = extractTag(text, "summary");
    $[0] = text;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  const summary = t2;
  if (!summary) {
    return null;
  }
  let t3;
  if ($[2] !== text) {
    const status = extractTag(text, "status");
    t3 = getStatusColor(status);
    $[2] = text;
    $[3] = t3;
  } else {

```

---


### `src/components/messages/UserBashInputMessage.tsx`

**信息:**
- 行数: 58
- 大小: 4503 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { extractTag } from '../../utils/messages.js';
type Props = {
  addMargin: boolean;
  param: TextBlockParam;
};
export function UserBashInputMessage(t0) {
  const $ = _c(8);
  const {
    param: t1,
    addMargin
  } = t0;
  const {
    text
  } = t1;
  let t2;
  if ($[0] !== text) {
    t2 = extractTag(text, "bash-input");
    $[0] = text;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  const input = t2;
  if (!input) {
    return null;
  }
  const t3 = addMargin ? 1 : 0;
  let t4;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t4 = <Text color="bashBorder">! </Text>;
    $[2] = t4;
  } else {
    t4 = $[2];
  }
  let t5;
  if ($[3] !== input) {
    t5 = <Text color="text">{input}</Text>;
    $[3] = input;
    $[4] = t5;
  } else {
    t5 = $[4];
  }
  let t6;
  if ($[5] !== t3 || $[6] !== t5) {
    t6 = <Box flexDirection="row" marginTop={t3} backgroundColor="bashMessageBackgroundColor" paddingRight={1}>{t4}{t5}</Box>;
    $[5] = t3;

```

---


### `src/components/messages/UserBashOutputMessage.tsx`

**信息:**
- 行数: 54
- 大小: 4188 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import BashToolResultMessage from '../../tools/BashTool/BashToolResultMessage.js';
import { extractTag } from '../../utils/messages.js';
export function UserBashOutputMessage(t0) {
  const $ = _c(10);
  const {
    content,
    verbose
  } = t0;
  let t1;
  if ($[0] !== content) {
    const rawStdout = extractTag(content, "bash-stdout") ?? "";
    t1 = extractTag(rawStdout, "persisted-output") ?? rawStdout;
    $[0] = content;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const stdout = t1;
  let t2;
  if ($[2] !== content) {
    t2 = extractTag(content, "bash-stderr") ?? "";
    $[2] = content;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  const stderr = t2;
  let t3;
  if ($[4] !== stderr || $[5] !== stdout) {
    t3 = {
      stdout,
      stderr
    };
    $[4] = stderr;
    $[5] = stdout;
    $[6] = t3;
  } else {
    t3 = $[6];
  }
  const t4 = !!verbose;
  let t5;
  if ($[7] !== t3 || $[8] !== t4) {
    t5 = <BashToolResultMessage content={t3} verbose={t4} />;
    $[7] = t3;
    $[8] = t4;
    $[9] = t5;
  } else {
    t5 = $[9];

```

---


### `src/components/messages/UserChannelMessage.tsx`

**信息:**
- 行数: 137
- 大小: 11325 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import { CHANNEL_ARROW } from '../../constants/figures.js';
import { CHANNEL_TAG } from '../../constants/xml.js';
import { Box, Text } from '../../ink.js';
import { truncateToWidth } from '../../utils/format.js';
type Props = {
  addMargin: boolean;
  param: TextBlockParam;
};

// <channel source="..." user="..." chat_id="...">content</channel>
// source is always first (wrapChannelMessage writes it), user is optional.
const CHANNEL_RE = new RegExp(`<${CHANNEL_TAG}\\s+source="([^"]+)"([^>]*)>\\n?([\\s\\S]*?)\\n?</${CHANNEL_TAG}>`);
const USER_ATTR_RE = /\buser="([^"]+)"/;

// Plugin-provided servers get names like plugin:slack-channel:slack via
// addPluginScopeToServers — show just the leaf. Matches the suffix-match
// logic in isServerInChannels.
function displayServerName(name: string): string {
  const i = name.lastIndexOf(':');
  return i === -1 ? name : name.slice(i + 1);
}
const TRUNCATE_AT = 60;
export function UserChannelMessage(t0) {
  const $ = _c(29);
  const {
    addMargin,
    param: t1
  } = t0;
  const {
    text
  } = t1;
  let T0;
  let T1;
  let T2;
  let t2;
  let t3;
  let t4;
  let t5;
  let t6;
  let t7;
  let truncated;
  let user;
  if ($[0] !== addMargin || $[1] !== text) {
    t7 = Symbol.for("react.early_return_sentinel");
    bb0: {
      const m = CHANNEL_RE.exec(text);
      if (!m) {

```

---


### `src/components/messages/UserCommandMessage.tsx`

**信息:**
- 行数: 108
- 大小: 9210 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import figures from 'figures';
import * as React from 'react';
import { COMMAND_MESSAGE_TAG } from '../../constants/xml.js';
import { Box, Text } from '../../ink.js';
import { extractTag } from '../../utils/messages.js';
type Props = {
  addMargin: boolean;
  param: TextBlockParam;
};
export function UserCommandMessage(t0) {
  const $ = _c(19);
  const {
    addMargin,
    param: t1
  } = t0;
  const {
    text
  } = t1;
  let t2;
  if ($[0] !== text) {
    t2 = extractTag(text, COMMAND_MESSAGE_TAG);
    $[0] = text;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  const commandMessage = t2;
  let t3;
  if ($[2] !== text) {
    t3 = extractTag(text, "command-args");
    $[2] = text;
    $[3] = t3;
  } else {
    t3 = $[3];
  }
  const args = t3;
  const isSkillFormat = extractTag(text, "skill-format") === "true";
  if (!commandMessage) {
    return null;
  }
  if (isSkillFormat) {
    const t4 = addMargin ? 1 : 0;
    let t5;
    if ($[4] === Symbol.for("react.memo_cache_sentinel")) {
      t5 = <Text color="subtle">{figures.pointer} </Text>;
      $[4] = t5;
    } else {
      t5 = $[4];

```

---


### `src/components/messages/UserCrossSessionMessage.tsx`

**信息:**
- 行数: 3
- 大小: 60 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function UserCrossSessionMessage() {
  return null
}

```

---


### `src/components/messages/UserForkBoilerplateMessage.tsx`

**信息:**
- 行数: 3
- 大小: 63 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function UserForkBoilerplateMessage() {
  return null
}

```

---


### `src/components/messages/UserGitHubWebhookMessage.tsx`

**信息:**
- 行数: 3
- 大小: 61 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function UserGitHubWebhookMessage() {
  return null
}

```

---


### `src/components/messages/UserImageMessage.tsx`

**信息:**
- 行数: 59
- 大小: 5897 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { pathToFileURL } from 'url';
import Link from '../../ink/components/Link.js';
import { supportsHyperlinks } from '../../ink/supports-hyperlinks.js';
import { Box, Text } from '../../ink.js';
import { getStoredImagePath } from '../../utils/imageStore.js';
import { MessageResponse } from '../MessageResponse.js';
type Props = {
  imageId?: number;
  addMargin?: boolean;
};

/**
 * Renders an image attachment in user messages.
 * Shows as a clickable link if the image is stored and terminal supports hyperlinks.
 * Uses MessageResponse styling to appear connected to the message above,
 * unless addMargin is true (image starts a new user turn without text).
 */
export function UserImageMessage(t0) {
  const $ = _c(7);
  const {
    imageId,
    addMargin
  } = t0;
  const label = imageId ? `[Image #${imageId}]` : "[Image]";
  let t1;
  if ($[0] !== imageId || $[1] !== label) {
    const imagePath = imageId ? getStoredImagePath(imageId) : null;
    t1 = imagePath && supportsHyperlinks() ? <Link url={pathToFileURL(imagePath).href}><Text>{label}</Text></Link> : <Text>{label}</Text>;
    $[0] = imageId;
    $[1] = label;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  const content = t1;
  if (addMargin) {
    let t2;
    if ($[3] !== content) {
      t2 = <Box marginTop={1}>{content}</Box>;
      $[3] = content;
      $[4] = t2;
    } else {
      t2 = $[4];
    }
    return t2;
  }
  let t2;
  if ($[5] !== content) {

```

---


### `src/components/messages/UserLocalCommandOutputMessage.tsx`

**信息:**
- 行数: 167
- 大小: 14566 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { DIAMOND_FILLED, DIAMOND_OPEN } from '../../constants/figures.js';
import { NO_CONTENT_MESSAGE } from '../../constants/messages.js';
import { Box, Text } from '../../ink.js';
import { extractTag } from '../../utils/messages.js';
import { Markdown } from '../Markdown.js';
import { MessageResponse } from '../MessageResponse.js';
type Props = {
  content: string;
};
export function UserLocalCommandOutputMessage(t0) {
  const $ = _c(4);
  const {
    content
  } = t0;
  let lines;
  let t1;
  if ($[0] !== content) {
    t1 = Symbol.for("react.early_return_sentinel");
    bb0: {
      const stdout = extractTag(content, "local-command-stdout");
      const stderr = extractTag(content, "local-command-stderr");
      if (!stdout && !stderr) {
        let t2;
        if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
          t2 = <MessageResponse><Text dimColor={true}>{NO_CONTENT_MESSAGE}</Text></MessageResponse>;
          $[3] = t2;
        } else {
          t2 = $[3];
        }
        t1 = t2;
        break bb0;
      }
      lines = [];
      if (stdout?.trim()) {
        lines.push(<IndentedContent key="stdout">{stdout.trim()}</IndentedContent>);
      }
      if (stderr?.trim()) {
        lines.push(<IndentedContent key="stderr">{stderr.trim()}</IndentedContent>);
      }
    }
    $[0] = content;
    $[1] = lines;
    $[2] = t1;
  } else {
    lines = $[1];
    t1 = $[2];
  }
  if (t1 !== Symbol.for("react.early_return_sentinel")) {

```

---


### `src/components/messages/UserMemoryInputMessage.tsx`

**信息:**
- 行数: 75
- 大小: 6516 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import sample from 'lodash-es/sample.js';
import * as React from 'react';
import { useMemo } from 'react';
import { Box, Text } from '../../ink.js';
import { extractTag } from '../../utils/messages.js';
import { MessageResponse } from '../MessageResponse.js';
function getSavingMessage(): string {
  return sample(['Got it.', 'Good to know.', 'Noted.']);
}
type Props = {
  addMargin: boolean;
  text: string;
};
export function UserMemoryInputMessage(t0) {
  const $ = _c(10);
  const {
    text,
    addMargin
  } = t0;
  let t1;
  if ($[0] !== text) {
    t1 = extractTag(text, "user-memory-input");
    $[0] = text;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const input = t1;
  let t2;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = getSavingMessage();
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  const savingText = t2;
  if (!input) {
    return null;
  }
  const t3 = addMargin ? 1 : 0;
  let t4;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
    t4 = <Text color="remember" backgroundColor="memoryBackgroundColor">#</Text>;
    $[3] = t4;
  } else {
    t4 = $[3];
  }
  let t5;
  if ($[4] !== input) {

```

---


### `src/components/messages/UserPlanMessage.tsx`

**信息:**
- 行数: 42
- 大小: 3743 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { Markdown } from '../Markdown.js';
type Props = {
  addMargin: boolean;
  planContent: string;
};
export function UserPlanMessage(t0) {
  const $ = _c(6);
  const {
    addMargin,
    planContent
  } = t0;
  const t1 = addMargin ? 1 : 0;
  let t2;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = <Box marginBottom={1}><Text bold={true} color="planMode">Plan to implement</Text></Box>;
    $[0] = t2;
  } else {
    t2 = $[0];
  }
  let t3;
  if ($[1] !== planContent) {
    t3 = <Markdown>{planContent}</Markdown>;
    $[1] = planContent;
    $[2] = t3;
  } else {
    t3 = $[2];
  }
  let t4;
  if ($[3] !== t1 || $[4] !== t3) {
    t4 = <Box flexDirection="column" borderStyle="round" borderColor="planMode" marginTop={t1} paddingX={1}>{t2}{t3}</Box>;
    $[3] = t1;
    $[4] = t3;
    $[5] = t4;
  } else {
    t4 = $[5];
  }
  return t4;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJveCIsIlRleHQiLCJNYXJrZG93biIsIlByb3BzIiwiYWRkTWFyZ2luIiwicGxhbkNvbnRlbnQiLCJVc2VyUGxhbk1lc3NhZ2UiLCJ0MCIsIiQiLCJfYyIsInQxIiwidDIiLCJTeW1ib2wiLCJmb3IiLCJ0MyIsInQ0Il0sInNvdXJjZXMiOlsiVXNlclBsYW5NZXNzYWdlLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IEJveCwgVGV4dCB9IGZyb20gJy4uLy4uL2luay5qcydcbmltcG9ydCB7IE1hcmtkb3duIH0gZnJvbSAnLi4vTWFya2Rvd24uanMnXG5cbnR5cGUgUHJvcHMgPSB7XG4gIGFkZE1hcmdpbjogYm9vbGVhblxuICBwbGFuQ29udGVudDogc3RyaW5nXG59XG5cbmV4cG9ydCBmdW5jdGlvbiBVc2VyUGxhbk1lc3NhZ2Uoe1xuICBhZGRNYXJnaW4sXG4gIHBsYW5Db250ZW50LFxufTogUHJvcHMpOiBSZWFjdC5SZWFjdE5vZGUge1xuICByZXR1cm4gKFxuICAgIDxCb3hcbiAgICAgIGZsZXhEaXJlY3Rpb249XCJjb2x1bW5cIlxuICAgICAgYm9yZGVyU3R5bGU9XCJyb3VuZFwiXG4gICAgICBib3JkZXJDb2xvcj1cInBsYW5Nb2RlXCJcbiAgICAgIG1hcmdpblRvcD17YWRkTWFyZ2luID8gMSA6IDB9XG4gICAgICBwYWRkaW5nWD17MX1cbiAgICA+XG4gICAgICA8Qm94IG1hcmdpbkJvdHRvbT17MX0+XG4gICAgICAgIDxUZXh0IGJvbGQgY29sb3I9XCJwbGFuTW9kZVwiPlxuICAgICAgICAgIFBsYW4gdG8gaW1wbGVtZW50XG4gICAgICAgIDwvVGV4dD5cbiAgICAgIDwvQm94PlxuICAgICAgPE1hcmtkb3duPntwbGFuQ29udGVudH08L01hcmtkb3duPlxuICAgIDwvQm94PlxuICApXG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxRQUFRLGNBQWM7QUFDeEMsU0FBU0MsUUFBUSxRQUFRLGdCQUFnQjtBQUV6QyxLQUFLQyxLQUFLLEdBQUc7RUFDWEMsU0FBUyxFQUFFLE9BQU87RUFDbEJDLFdBQVcsRUFBRSxNQUFNO0FBQ3JCLENBQUM7QUFFRCxPQUFPLFNBQUFDLGdCQUFBQyxFQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQXlCO0lBQUFMLFNBQUE7SUFBQUM7RUFBQSxJQUFBRSxFQUd4QjtFQU1TLE1BQUFHLEVBQUEsR0FBQU4sU0FBUyxHQUFULENBQWlCLEdBQWpCLENBQWlCO0VBQUEsSUFBQU8sRUFBQTtFQUFBLElBQUFILENBQUEsUUFBQUksTUFBQSxDQUFBQyxHQUFBO0lBRzVCRixFQUFBLElBQUMsR0FBRyxDQUFlLFlBQUMsQ0FBRCxHQUFDLENBQ2xCLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBSixLQUFHLENBQUMsQ0FBTyxLQUFVLENBQVYsVUFBVSxDQUFDLGlCQUU1QixFQUZDLElBQUksQ0FHUCxFQUpDLEdBQUcsQ0FJRTtJQUFBSCxDQUFBLE1BQUFHLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFILENBQUE7RUFBQTtFQUFBLElBQUFNLEVBQUE7RUFBQSxJQUFBTixDQUFBLFFBQUFILFdBQUE7SUFDTlMsRUFBQSxJQUFDLFFBQVEsQ0FBRVQsWUFBVSxDQUFFLEVBQXRCLFFBQVEsQ0FBeUI7SUFBQUcsQ0FBQSxNQUFBSCxXQUFBO0lBQUFHLENBQUEsTUFBQU0sRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQU4sQ0FBQTtFQUFBO0VBQUEsSUFBQU8sRUFBQTtFQUFBLElBQUFQLENBQUEsUUFBQUUsRUFBQSxJQUFBRixDQUFBLFFBQUFNLEVBQUE7SUFacENDLEVBQUEsSUFBQyxHQUFHLENBQ1ksYUFBUSxDQUFSLFFBQVEsQ0FDVixXQUFPLENBQVAsT0FBTyxDQUNQLFdBQVUsQ0FBVixVQUFVLENBQ1gsU0FBaUIsQ0FBakIsQ0FBQUwsRUFBZ0IsQ0FBQyxDQUNsQixRQUFDLENBQUQsR0FBQyxDQUVYLENBQUFDLEVBSUssQ0FDTCxDQUFBRyxFQUFpQyxDQUNuQyxFQWJDLEdBQUcsQ0FhRTtJQUFBTixDQUFBLE1BQUFFLEVBQUE7SUFBQUYsQ0FBQSxNQUFBTSxFQUFBO0lBQUFOLENBQUEsTUFBQU8sRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQVAsQ0FBQTtFQUFBO0VBQUEsT0FiTk8sRUFhTTtBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/messages/UserPromptMessage.tsx`

**信息:**
- 行数: 80
- 大小: 15172 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import type { TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import React, { useContext, useMemo } from 'react';
import { getKairosActive, getUserMsgOptIn } from '../../bootstrap/state.js';
import { Box } from '../../ink.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js';
import { useAppState } from '../../state/AppState.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import { logError } from '../../utils/log.js';
import { countCharInString } from '../../utils/stringUtils.js';
import { MessageActionsSelectedContext } from '../messageActions.js';
import { HighlightedThinkingText } from './HighlightedThinkingText.js';
type Props = {
  addMargin: boolean;
  param: TextBlockParam;
  isTranscriptMode?: boolean;
  timestamp?: string;
};

// Hard cap on displayed prompt text. Piping large files via stdin
// (e.g. `cat 11k-line-file | claude`) creates a single user message whose
// <Text> node the fullscreen Ink renderer must wrap/output on every frame,
// causing 500ms+ keystroke latency. React.memo skips the React render but
// the Ink output pass still iterates the full mounted text. Non-fullscreen
// avoids this via <Static> (print-and-forget to terminal scrollback).
// Head+tail because `{ cat file; echo prompt; } | claude` puts the user's
// actual question at the end.
const MAX_DISPLAY_CHARS = 10_000;
const TRUNCATE_HEAD_CHARS = 2_500;
const TRUNCATE_TAIL_CHARS = 2_500;
export function UserPromptMessage({
  addMargin,
  param: {
    text
  },
  isTranscriptMode,
  timestamp
}: Props): React.ReactNode {
  // REPL.tsx passes isBriefOnly={viewedTeammateTask ? false : isBriefOnly}
  // but that prop isn't threaded this deep — replicate the override by
  // reading viewingAgentTaskId directly. Computed here (not in the child)
  // so the parent Box can drop its backgroundColor: in brief mode the
  // child renders a label-style layout, and Box backgroundColor paints
  // behind children unconditionally (they can't opt out).
  //
  // Hooks stay INSIDE feature() ternaries so external builds don't pay
  // the per-scrollback-message store subscription (useSyncExternalStore
  // bypasses React.memo). Runtime-gated like isBriefEnabled() but inlined
  // to avoid pulling BriefTool.ts → prompt.ts tool-name strings into
  // external builds.

```

---


### `src/components/messages/UserResourceUpdateMessage.tsx`

**信息:**
- 行数: 121
- 大小: 12363 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import { REFRESH_ARROW } from '../../constants/figures.js';
import { Box, Text } from '../../ink.js';
type Props = {
  addMargin: boolean;
  param: TextBlockParam;
};
type ParsedUpdate = {
  kind: 'resource' | 'polling';
  server: string;
  /** URI for resource updates, tool name for polling updates */
  target: string;
  reason?: string;
};

// Parse resource and polling updates from XML format
function parseUpdates(text: string): ParsedUpdate[] {
  const updates: ParsedUpdate[] = [];

  // Match <mcp-resource-update server="..." uri="...">
  const resourceRegex = /<mcp-resource-update\s+server="([^"]+)"\s+uri="([^"]+)"[^>]*>(?:[\s\S]*?<reason>([^<]+)<\/reason>)?/g;
  let match;
  while ((match = resourceRegex.exec(text)) !== null) {
    updates.push({
      kind: 'resource',
      server: match[1] ?? '',
      target: match[2] ?? '',
      reason: match[3]
    });
  }

  // Match <mcp-polling-update type="tool" server="..." tool="...">
  const pollingRegex = /<mcp-polling-update\s+type="([^"]+)"\s+server="([^"]+)"\s+tool="([^"]+)"[^>]*>(?:[\s\S]*?<reason>([^<]+)<\/reason>)?/g;
  while ((match = pollingRegex.exec(text)) !== null) {
    updates.push({
      kind: 'polling',
      server: match[2] ?? '',
      target: match[3] ?? '',
      reason: match[4]
    });
  }
  return updates;
}

// Format URI for display - show just the meaningful part
function formatUri(uri: string): string {
  // For file:// URIs, show just the filename
  if (uri.startsWith('file://')) {

```

---


### `src/components/messages/UserTeammateMessage.tsx`

**信息:**
- 行数: 206
- 大小: 24126 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import figures from 'figures';
import * as React from 'react';
import { TEAMMATE_MESSAGE_TAG } from '../../constants/xml.js';
import { Ansi, Box, Text, type TextProps } from '../../ink.js';
import { toInkColor } from '../../utils/ink.js';
import { jsonParse } from '../../utils/slowOperations.js';
import { isShutdownApproved } from '../../utils/teammateMailbox.js';
import { MessageResponse } from '../MessageResponse.js';
import { tryRenderPlanApprovalMessage } from './PlanApprovalMessage.js';
import { tryRenderShutdownMessage } from './ShutdownMessage.js';
import { tryRenderTaskAssignmentMessage } from './TaskAssignmentMessage.js';
type Props = {
  addMargin: boolean;
  param: TextBlockParam;
  isTranscriptMode?: boolean;
};
type ParsedMessage = {
  teammateId: string;
  content: string;
  color?: string;
  summary?: string;
};
const TEAMMATE_MSG_REGEX = new RegExp(`<${TEAMMATE_MESSAGE_TAG}\\s+teammate_id="([^"]+)"(?:\\s+color="([^"]+)")?(?:\\s+summary="([^"]+)")?>\\n?([\\s\\S]*?)\\n?<\\/${TEAMMATE_MESSAGE_TAG}>`, 'g');

/**
 * Parse all teammate messages from XML format:
 * <teammate-message teammate_id="alice" color="red" summary="Brief update">message content</teammate-message>
 * Supports multiple messages in a single text block.
 */
function parseTeammateMessages(text: string): ParsedMessage[] {
  const messages: ParsedMessage[] = [];
  // Use matchAll to find all matches (this is a RegExp method, not child_process)
  for (const match of text.matchAll(TEAMMATE_MSG_REGEX)) {
    if (match[1] && match[4]) {
      messages.push({
        teammateId: match[1],
        color: match[2],
        // may be undefined
        summary: match[3],
        // may be undefined
        content: match[4].trim()
      });
    }
  }
  return messages;
}
function getDisplayName(teammateId: string): string {
  if (teammateId === 'leader') {

```

---


### `src/components/messages/UserTextMessage.tsx`

**信息:**
- 行数: 275
- 大小: 29051 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import type { TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import { NO_CONTENT_MESSAGE } from '../../constants/messages.js';
import { COMMAND_MESSAGE_TAG, LOCAL_COMMAND_CAVEAT_TAG, TASK_NOTIFICATION_TAG, TEAMMATE_MESSAGE_TAG, TICK_TAG } from '../../constants/xml.js';
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js';
import { extractTag, INTERRUPT_MESSAGE, INTERRUPT_MESSAGE_FOR_TOOL_USE } from '../../utils/messages.js';
import { InterruptedByUser } from '../InterruptedByUser.js';
import { MessageResponse } from '../MessageResponse.js';
import { UserAgentNotificationMessage } from './UserAgentNotificationMessage.js';
import { UserBashInputMessage } from './UserBashInputMessage.js';
import { UserBashOutputMessage } from './UserBashOutputMessage.js';
import { UserCommandMessage } from './UserCommandMessage.js';
import { UserLocalCommandOutputMessage } from './UserLocalCommandOutputMessage.js';
import { UserMemoryInputMessage } from './UserMemoryInputMessage.js';
import { UserPlanMessage } from './UserPlanMessage.js';
import { UserPromptMessage } from './UserPromptMessage.js';
import { UserResourceUpdateMessage } from './UserResourceUpdateMessage.js';
import { UserTeammateMessage } from './UserTeammateMessage.js';
type Props = {
  addMargin: boolean;
  param: TextBlockParam;
  verbose: boolean;
  planContent?: string;
  isTranscriptMode?: boolean;
  timestamp?: string;
};
export function UserTextMessage(t0) {
  const $ = _c(49);
  const {
    addMargin,
    param,
    verbose,
    planContent,
    isTranscriptMode,
    timestamp
  } = t0;
  if (param.text.trim() === NO_CONTENT_MESSAGE) {
    return null;
  }
  if (planContent) {
    let t1;
    if ($[0] !== addMargin || $[1] !== planContent) {
      t1 = <UserPlanMessage addMargin={addMargin} planContent={planContent} />;
      $[0] = addMargin;
      $[1] = planContent;
      $[2] = t1;
    } else {
      t1 = $[2];

```

---


### `src/components/messages/UserToolResultMessage/RejectedPlanMessage.tsx`

**信息:**
- 行数: 31
- 大小: 3409 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Markdown } from 'src/components/Markdown.js';
import { MessageResponse } from 'src/components/MessageResponse.js';
import { Box, Text } from '../../../ink.js';
type Props = {
  plan: string;
};
export function RejectedPlanMessage(t0) {
  const $ = _c(3);
  const {
    plan
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Text color="subtle">User rejected Claude's plan:</Text>;
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  let t2;
  if ($[1] !== plan) {
    t2 = <MessageResponse><Box flexDirection="column">{t1}<Box borderStyle="round" borderColor="planMode" paddingX={1} overflow="hidden"><Markdown>{plan}</Markdown></Box></Box></MessageResponse>;
    $[1] = plan;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  return t2;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIk1hcmtkb3duIiwiTWVzc2FnZVJlc3BvbnNlIiwiQm94IiwiVGV4dCIsIlByb3BzIiwicGxhbiIsIlJlamVjdGVkUGxhbk1lc3NhZ2UiLCJ0MCIsIiQiLCJfYyIsInQxIiwiU3ltYm9sIiwiZm9yIiwidDIiXSwic291cmNlcyI6WyJSZWplY3RlZFBsYW5NZXNzYWdlLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IE1hcmtkb3duIH0gZnJvbSAnc3JjL2NvbXBvbmVudHMvTWFya2Rvd24uanMnXG5pbXBvcnQgeyBNZXNzYWdlUmVzcG9uc2UgfSBmcm9tICdzcmMvY29tcG9uZW50cy9NZXNzYWdlUmVzcG9uc2UuanMnXG5pbXBvcnQgeyBCb3gsIFRleHQgfSBmcm9tICcuLi8uLi8uLi9pbmsuanMnXG5cbnR5cGUgUHJvcHMgPSB7XG4gIHBsYW46IHN0cmluZ1xufVxuXG5leHBvcnQgZnVuY3Rpb24gUmVqZWN0ZWRQbGFuTWVzc2FnZSh7IHBsYW4gfTogUHJvcHMpOiBSZWFjdC5SZWFjdE5vZGUge1xuICByZXR1cm4gKFxuICAgIDxNZXNzYWdlUmVzcG9uc2U+XG4gICAgICA8Qm94IGZsZXhEaXJlY3Rpb249XCJjb2x1bW5cIj5cbiAgICAgICAgPFRleHQgY29sb3I9XCJzdWJ0bGVcIj5Vc2VyIHJlamVjdGVkIENsYXVkZSZhcG9zO3MgcGxhbjo8L1RleHQ+XG4gICAgICAgIDxCb3hcbiAgICAgICAgICBib3JkZXJTdHlsZT1cInJvdW5kXCJcbiAgICAgICAgICBib3JkZXJDb2xvcj1cInBsYW5Nb2RlXCJcbiAgICAgICAgICBwYWRkaW5nWD17MX1cbiAgICAgICAgICAvLyBOZWNlc3NhcnkgZm9yIFdpbmRvd3MgVGVybWluYWwgdG8gcmVuZGVyIHByb3Blcmx5XG4gICAgICAgICAgb3ZlcmZsb3c9XCJoaWRkZW5cIlxuICAgICAgICA+XG4gICAgICAgICAgPE1hcmtkb3duPntwbGFufTwvTWFya2Rvd24+XG4gICAgICAgIDwvQm94PlxuICAgICAgPC9Cb3g+XG4gICAgPC9NZXNzYWdlUmVzcG9uc2U+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsUUFBUSxRQUFRLDRCQUE0QjtBQUNyRCxTQUFTQyxlQUFlLFFBQVEsbUNBQW1DO0FBQ25FLFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxRQUFRLGlCQUFpQjtBQUUzQyxLQUFLQyxLQUFLLEdBQUc7RUFDWEMsSUFBSSxFQUFFLE1BQU07QUFDZCxDQUFDO0FBRUQsT0FBTyxTQUFBQyxvQkFBQUMsRUFBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUE2QjtJQUFBSjtFQUFBLElBQUFFLEVBQWU7RUFBQSxJQUFBRyxFQUFBO0VBQUEsSUFBQUYsQ0FBQSxRQUFBRyxNQUFBLENBQUFDLEdBQUE7SUFJM0NGLEVBQUEsSUFBQyxJQUFJLENBQU8sS0FBUSxDQUFSLFFBQVEsQ0FBQyw0QkFBaUMsRUFBckQsSUFBSSxDQUF3RDtJQUFBRixDQUFBLE1BQUFFLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFGLENBQUE7RUFBQTtFQUFBLElBQUFLLEVBQUE7RUFBQSxJQUFBTCxDQUFBLFFBQUFILElBQUE7SUFGakVRLEVBQUEsSUFBQyxlQUFlLENBQ2QsQ0FBQyxHQUFHLENBQWUsYUFBUSxDQUFSLFFBQVEsQ0FDekIsQ0FBQUgsRUFBNEQsQ0FDNUQsQ0FBQyxHQUFHLENBQ1UsV0FBTyxDQUFQLE9BQU8sQ0FDUCxXQUFVLENBQVYsVUFBVSxDQUNaLFFBQUMsQ0FBRCxHQUFDLENBRUYsUUFBUSxDQUFSLFFBQVEsQ0FFakIsQ0FBQyxRQUFRLENBQUVMLEtBQUcsQ0FBRSxFQUFmLFFBQVEsQ0FDWCxFQVJDLEdBQUcsQ0FTTixFQVhDLEdBQUcsQ0FZTixFQWJDLGVBQWUsQ0FhRTtJQUFBRyxDQUFBLE1BQUFILElBQUE7SUFBQUcsQ0FBQSxNQUFBSyxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBTCxDQUFBO0VBQUE7RUFBQSxPQWJsQkssRUFha0I7QUFBQSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/components/messages/UserToolResultMessage/RejectedToolUseMessage.tsx`

**信息:**
- 行数: 16
- 大小: 1763 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Text } from '../../../ink.js';
import { MessageResponse } from '../../MessageResponse.js';
export function RejectedToolUseMessage() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <MessageResponse height={1}><Text dimColor={true}>Tool use rejected</Text></MessageResponse>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlRleHQiLCJNZXNzYWdlUmVzcG9uc2UiLCJSZWplY3RlZFRvb2xVc2VNZXNzYWdlIiwiJCIsIl9jIiwidDAiLCJTeW1ib2wiLCJmb3IiXSwic291cmNlcyI6WyJSZWplY3RlZFRvb2xVc2VNZXNzYWdlLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IFRleHQgfSBmcm9tICcuLi8uLi8uLi9pbmsuanMnXG5pbXBvcnQgeyBNZXNzYWdlUmVzcG9uc2UgfSBmcm9tICcuLi8uLi9NZXNzYWdlUmVzcG9uc2UuanMnXG5cbmV4cG9ydCBmdW5jdGlvbiBSZWplY3RlZFRvb2xVc2VNZXNzYWdlKCk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIHJldHVybiAoXG4gICAgPE1lc3NhZ2VSZXNwb25zZSBoZWlnaHQ9ezF9PlxuICAgICAgPFRleHQgZGltQ29sb3I+VG9vbCB1c2UgcmVqZWN0ZWQ8L1RleHQ+XG4gICAgPC9NZXNzYWdlUmVzcG9uc2U+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsSUFBSSxRQUFRLGlCQUFpQjtBQUN0QyxTQUFTQyxlQUFlLFFBQVEsMEJBQTBCO0FBRTFELE9BQU8sU0FBQUMsdUJBQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFBQSxJQUFBQyxFQUFBO0VBQUEsSUFBQUYsQ0FBQSxRQUFBRyxNQUFBLENBQUFDLEdBQUE7SUFFSEYsRUFBQSxJQUFDLGVBQWUsQ0FBUyxNQUFDLENBQUQsR0FBQyxDQUN4QixDQUFDLElBQUksQ0FBQyxRQUFRLENBQVIsS0FBTyxDQUFDLENBQUMsaUJBQWlCLEVBQS9CLElBQUksQ0FDUCxFQUZDLGVBQWUsQ0FFRTtJQUFBRixDQUFBLE1BQUFFLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFGLENBQUE7RUFBQTtFQUFBLE9BRmxCRSxFQUVrQjtBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/messages/UserToolResultMessage/UserToolCanceledMessage.tsx`

**信息:**
- 行数: 16
- 大小: 1777 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { InterruptedByUser } from 'src/components/InterruptedByUser.js';
import { MessageResponse } from 'src/components/MessageResponse.js';
export function UserToolCanceledMessage() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <MessageResponse height={1}><InterruptedByUser /></MessageResponse>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkludGVycnVwdGVkQnlVc2VyIiwiTWVzc2FnZVJlc3BvbnNlIiwiVXNlclRvb2xDYW5jZWxlZE1lc3NhZ2UiLCIkIiwiX2MiLCJ0MCIsIlN5bWJvbCIsImZvciJdLCJzb3VyY2VzIjpbIlVzZXJUb29sQ2FuY2VsZWRNZXNzYWdlLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IEludGVycnVwdGVkQnlVc2VyIH0gZnJvbSAnc3JjL2NvbXBvbmVudHMvSW50ZXJydXB0ZWRCeVVzZXIuanMnXG5pbXBvcnQgeyBNZXNzYWdlUmVzcG9uc2UgfSBmcm9tICdzcmMvY29tcG9uZW50cy9NZXNzYWdlUmVzcG9uc2UuanMnXG5cbmV4cG9ydCBmdW5jdGlvbiBVc2VyVG9vbENhbmNlbGVkTWVzc2FnZSgpOiBSZWFjdC5SZWFjdE5vZGUge1xuICByZXR1cm4gKFxuICAgIDxNZXNzYWdlUmVzcG9uc2UgaGVpZ2h0PXsxfT5cbiAgICAgIDxJbnRlcnJ1cHRlZEJ5VXNlciAvPlxuICAgIDwvTWVzc2FnZVJlc3BvbnNlPlxuICApXG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLGlCQUFpQixRQUFRLHFDQUFxQztBQUN2RSxTQUFTQyxlQUFlLFFBQVEsbUNBQW1DO0FBRW5FLE9BQU8sU0FBQUMsd0JBQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFBQSxJQUFBQyxFQUFBO0VBQUEsSUFBQUYsQ0FBQSxRQUFBRyxNQUFBLENBQUFDLEdBQUE7SUFFSEYsRUFBQSxJQUFDLGVBQWUsQ0FBUyxNQUFDLENBQUQsR0FBQyxDQUN4QixDQUFDLGlCQUFpQixHQUNwQixFQUZDLGVBQWUsQ0FFRTtJQUFBRixDQUFBLE1BQUFFLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFGLENBQUE7RUFBQTtFQUFBLE9BRmxCRSxFQUVrQjtBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/components/messages/UserToolResultMessage/UserToolErrorMessage.tsx`

**信息:**
- 行数: 103
- 大小: 12222 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import { BULLET_OPERATOR } from '../../../constants/figures.js';
import { Text } from '../../../ink.js';
import { filterToolProgressMessages, type Tool, type Tools } from '../../../Tool.js';
import type { ProgressMessage } from '../../../types/message.js';
import { INTERRUPT_MESSAGE_FOR_TOOL_USE, isClassifierDenial, PLAN_REJECTION_PREFIX, REJECT_MESSAGE_WITH_REASON_PREFIX } from '../../../utils/messages.js';
import { FallbackToolUseErrorMessage } from '../../FallbackToolUseErrorMessage.js';
import { InterruptedByUser } from '../../InterruptedByUser.js';
import { MessageResponse } from '../../MessageResponse.js';
import { RejectedPlanMessage } from './RejectedPlanMessage.js';
import { RejectedToolUseMessage } from './RejectedToolUseMessage.js';
type Props = {
  progressMessagesForMessage: ProgressMessage[];
  tool?: Tool; // undefined when resuming an old conversation that uses an old tool
  tools: Tools;
  param: ToolResultBlockParam;
  verbose: boolean;
  isTranscriptMode?: boolean;
};
export function UserToolErrorMessage(t0) {
  const $ = _c(14);
  const {
    progressMessagesForMessage,
    tool,
    tools,
    param,
    verbose,
    isTranscriptMode
  } = t0;
  if (typeof param.content === "string" && param.content.includes(INTERRUPT_MESSAGE_FOR_TOOL_USE)) {
    let t1;
    if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
      t1 = <MessageResponse height={1}><InterruptedByUser /></MessageResponse>;
      $[0] = t1;
    } else {
      t1 = $[0];
    }
    return t1;
  }
  if (typeof param.content === "string" && param.content.startsWith(PLAN_REJECTION_PREFIX)) {
    let t1;
    if ($[1] !== param.content) {
      t1 = param.content.substring(PLAN_REJECTION_PREFIX.length);
      $[1] = param.content;
      $[2] = t1;
    } else {
      t1 = $[2];

```

---


### `src/components/messages/UserToolResultMessage/UserToolRejectMessage.tsx`

**信息:**
- 行数: 95
- 大小: 8570 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useTerminalSize } from '../../../hooks/useTerminalSize.js';
import { useTheme } from '../../../ink.js';
import { filterToolProgressMessages, type Tool, type Tools } from '../../../Tool.js';
import type { ProgressMessage } from '../../../types/message.js';
import type { buildMessageLookups } from '../../../utils/messages.js';
import { FallbackToolUseRejectedMessage } from '../../FallbackToolUseRejectedMessage.js';
type Props = {
  input: {
    [key: string]: unknown;
  };
  progressMessagesForMessage: ProgressMessage[];
  style?: 'condensed';
  tool?: Tool;
  tools: Tools;
  lookups: ReturnType<typeof buildMessageLookups>;
  verbose: boolean;
  isTranscriptMode?: boolean;
};
export function UserToolRejectMessage(t0) {
  const $ = _c(13);
  const {
    input,
    progressMessagesForMessage,
    style,
    tool,
    tools,
    verbose,
    isTranscriptMode
  } = t0;
  const {
    columns
  } = useTerminalSize();
  const [theme] = useTheme();
  if (!tool || !tool.renderToolUseRejectedMessage) {
    let t1;
    if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
      t1 = <FallbackToolUseRejectedMessage />;
      $[0] = t1;
    } else {
      t1 = $[0];
    }
    return t1;
  }
  const t1 = tool.inputSchema;
  let t2;
  let t3;
  if ($[1] !== columns || $[2] !== input || $[3] !== isTranscriptMode || $[4] !== progressMessagesForMessage || $[5] !== style || $[6] !== theme || $[7] !== tool || $[8] !== tools || $[9] !== verbose) {
    t3 = Symbol.for("react.early_return_sentinel");

```

---


### `src/components/messages/UserToolResultMessage/UserToolResultMessage.tsx`

**信息:**
- 行数: 106
- 大小: 13742 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import type { Tools } from '../../../Tool.js';
import type { NormalizedUserMessage, ProgressMessage } from '../../../types/message.js';
import { type buildMessageLookups, CANCEL_MESSAGE, INTERRUPT_MESSAGE_FOR_TOOL_USE, REJECT_MESSAGE } from '../../../utils/messages.js';
import { UserToolCanceledMessage } from './UserToolCanceledMessage.js';
import { UserToolErrorMessage } from './UserToolErrorMessage.js';
import { UserToolRejectMessage } from './UserToolRejectMessage.js';
import { UserToolSuccessMessage } from './UserToolSuccessMessage.js';
import { useGetToolFromMessages } from './utils.js';
type Props = {
  param: ToolResultBlockParam;
  message: NormalizedUserMessage;
  lookups: ReturnType<typeof buildMessageLookups>;
  progressMessagesForMessage: ProgressMessage[];
  style?: 'condensed';
  tools: Tools;
  verbose: boolean;
  width: number | string;
  isTranscriptMode?: boolean;
};
export function UserToolResultMessage(t0) {
  const $ = _c(28);
  const {
    param,
    message,
    lookups,
    progressMessagesForMessage,
    style,
    tools,
    verbose,
    width,
    isTranscriptMode
  } = t0;
  const toolUse = useGetToolFromMessages(param.tool_use_id, tools, lookups);
  if (!toolUse) {
    return null;
  }
  if (typeof param.content === "string" && param.content.startsWith(CANCEL_MESSAGE)) {
    let t1;
    if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
      t1 = <UserToolCanceledMessage />;
      $[0] = t1;
    } else {
      t1 = $[0];
    }
    return t1;
  }
  if (typeof param.content === "string" && param.content.startsWith(REJECT_MESSAGE) || param.content === INTERRUPT_MESSAGE_FOR_TOOL_USE) {

```

---


### `src/components/messages/UserToolResultMessage/UserToolSuccessMessage.tsx`

**信息:**
- 行数: 104
- 大小: 16409 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import figures from 'figures';
import * as React from 'react';
import { SentryErrorBoundary } from 'src/components/SentryErrorBoundary.js';
import { Box, Text, useTheme } from '../../../ink.js';
import { useAppState } from '../../../state/AppState.js';
import { filterToolProgressMessages, type Tool, type Tools } from '../../../Tool.js';
import type { NormalizedUserMessage, ProgressMessage } from '../../../types/message.js';
import { deleteClassifierApproval, getClassifierApproval, getYoloClassifierApproval } from '../../../utils/classifierApprovals.js';
import type { buildMessageLookups } from '../../../utils/messages.js';
import { MessageResponse } from '../../MessageResponse.js';
import { HookProgressMessage } from '../HookProgressMessage.js';
type Props = {
  message: NormalizedUserMessage;
  lookups: ReturnType<typeof buildMessageLookups>;
  toolUseID: string;
  progressMessagesForMessage: ProgressMessage[];
  style?: 'condensed';
  tool?: Tool;
  tools: Tools;
  verbose: boolean;
  width: number | string;
  isTranscriptMode?: boolean;
};
export function UserToolSuccessMessage({
  message,
  lookups,
  toolUseID,
  progressMessagesForMessage,
  style,
  tool,
  tools,
  verbose,
  width,
  isTranscriptMode
}: Props): React.ReactNode {
  const [theme] = useTheme();
  // Hook stays inside feature() ternary so external builds don't pay a
  // per-scrollback-message store subscription — same pattern as
  // UserPromptMessage.tsx.
  const isBriefOnly = feature('KAIROS') || feature('KAIROS_BRIEF') ?
  // biome-ignore lint/correctness/useHookAtTopLevel: feature() is a compile-time constant
  useAppState(s => s.isBriefOnly) : false;

  // Capture classifier approval once on mount, then delete from Map to prevent linear growth.
  // useState lazy initializer ensures the value persists across re-renders.
  const [classifierRule] = React.useState(() => getClassifierApproval(toolUseID));
  const [yoloReason] = React.useState(() => getYoloClassifierApproval(toolUseID));
  React.useEffect(() => {
    deleteClassifierApproval(toolUseID);

```

---


### `src/components/messages/UserToolResultMessage/utils.tsx`

**信息:**
- 行数: 44
- 大小: 3938 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ToolUseBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import { useMemo } from 'react';
import { findToolByName, type Tool, type Tools } from '../../../Tool.js';
import type { buildMessageLookups } from '../../../utils/messages.js';
export function useGetToolFromMessages(toolUseID, tools, lookups) {
  const $ = _c(7);
  let t0;
  if ($[0] !== lookups.toolUseByToolUseID || $[1] !== toolUseID || $[2] !== tools) {
    bb0: {
      const toolUse = lookups.toolUseByToolUseID.get(toolUseID);
      if (!toolUse) {
        t0 = null;
        break bb0;
      }
      const tool = findToolByName(tools, toolUse.name);
      if (!tool) {
        t0 = null;
        break bb0;
      }
      let t1;
      if ($[4] !== tool || $[5] !== toolUse) {
        t1 = {
          tool,
          toolUse
        };
        $[4] = tool;
        $[5] = toolUse;
        $[6] = t1;
      } else {
        t1 = $[6];
      }
      t0 = t1;
    }
    $[0] = lookups.toolUseByToolUseID;
    $[1] = toolUseID;
    $[2] = tools;
    $[3] = t0;
  } else {
    t0 = $[3];
  }
  return t0;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJUb29sVXNlQmxvY2tQYXJhbSIsInVzZU1lbW8iLCJmaW5kVG9vbEJ5TmFtZSIsIlRvb2wiLCJUb29scyIsImJ1aWxkTWVzc2FnZUxvb2t1cHMiLCJ1c2VHZXRUb29sRnJvbU1lc3NhZ2VzIiwidG9vbFVzZUlEIiwidG9vbHMiLCJsb29rdXBzIiwiJCIsIl9jIiwidDAiLCJ0b29sVXNlQnlUb29sVXNlSUQiLCJiYjAiLCJ0b29sVXNlIiwiZ2V0IiwidG9vbCIsIm5hbWUiLCJ0MSJdLCJzb3VyY2VzIjpbInV0aWxzLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgdHlwZSB7IFRvb2xVc2VCbG9ja1BhcmFtIH0gZnJvbSAnQGFudGhyb3BpYy1haS9zZGsvcmVzb3VyY2VzL2luZGV4Lm1qcydcbmltcG9ydCB7IHVzZU1lbW8gfSBmcm9tICdyZWFjdCdcbmltcG9ydCB7IGZpbmRUb29sQnlOYW1lLCB0eXBlIFRvb2wsIHR5cGUgVG9vbHMgfSBmcm9tICcuLi8uLi8uLi9Ub29sLmpzJ1xuaW1wb3J0IHR5cGUgeyBidWlsZE1lc3NhZ2VMb29rdXBzIH0gZnJvbSAnLi4vLi4vLi4vdXRpbHMvbWVzc2FnZXMuanMnXG5cbmV4cG9ydCBmdW5jdGlvbiB1c2VHZXRUb29sRnJvbU1lc3NhZ2VzKFxuICB0b29sVXNlSUQ6IHN0cmluZyxcbiAgdG9vbHM6IFRvb2xzLFxuICBsb29rdXBzOiBSZXR1cm5UeXBlPHR5cGVvZiBidWlsZE1lc3NhZ2VMb29rdXBzPixcbik6IHsgdG9vbDogVG9vbDsgdG9vbFVzZTogVG9vbFVzZUJsb2NrUGFyYW0gfSB8IG51bGwge1xuICByZXR1cm4gdXNlTWVtbygoKSA9PiB7XG4gICAgY29uc3QgdG9vbFVzZSA9IGxvb2t1cHMudG9vbFVzZUJ5VG9vbFVzZUlELmdldCh0b29sVXNlSUQpXG4gICAgaWYgKCF0b29sVXNlKSB7XG4gICAgICByZXR1cm4gbnVsbFxuICAgIH1cbiAgICBjb25zdCB0b29sID0gZmluZFRvb2xCeU5hbWUodG9vbHMsIHRvb2xVc2UubmFtZSlcbiAgICBpZiAoIXRvb2wpIHtcbiAgICAgIHJldHVybiBudWxsXG4gICAgfVxuICAgIHJldHVybiB7IHRvb2wsIHRvb2xVc2UgfVxuICB9LCBbdG9vbFVzZUlELCBsb29rdXBzLCB0b29sc10pXG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxjQUFjQSxpQkFBaUIsUUFBUSx1Q0FBdUM7QUFDOUUsU0FBU0MsT0FBTyxRQUFRLE9BQU87QUFDL0IsU0FBU0MsY0FBYyxFQUFFLEtBQUtDLElBQUksRUFBRSxLQUFLQyxLQUFLLFFBQVEsa0JBQWtCO0FBQ3hFLGNBQWNDLG1CQUFtQixRQUFRLDRCQUE0QjtBQUVyRSxPQUFPLFNBQUFDLHVCQUFBQyxTQUFBLEVBQUFDLEtBQUEsRUFBQUMsT0FBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUFBLElBQUFDLEVBQUE7RUFBQSxJQUFBRixDQUFBLFFBQUFELE9BQUEsQ0FBQUksa0JBQUEsSUFBQUgsQ0FBQSxRQUFBSCxTQUFBLElBQUFHLENBQUEsUUFBQUYsS0FBQTtJQUFBTSxHQUFBO01BTUgsTUFBQUMsT0FBQSxHQUFnQk4sT0FBTyxDQUFBSSxrQkFBbUIsQ0FBQUcsR0FBSSxDQUFDVCxTQUFTLENBQUM7TUFDekQsSUFBSSxDQUFDUSxPQUFPO1FBQ1ZILEVBQUEsR0FBTyxJQUFJO1FBQVgsTUFBQUUsR0FBQTtNQUFXO01BRWIsTUFBQUcsSUFBQSxHQUFhZixjQUFjLENBQUNNLEtBQUssRUFBRU8sT0FBTyxDQUFBRyxJQUFLLENBQUM7TUFDaEQsSUFBSSxDQUFDRCxJQUFJO1FBQ1BMLEVBQUEsR0FBTyxJQUFJO1FBQVgsTUFBQUUsR0FBQTtNQUFXO01BQ1osSUFBQUssRUFBQTtNQUFBLElBQUFULENBQUEsUUFBQU8sSUFBQSxJQUFBUCxDQUFBLFFBQUFLLE9BQUE7UUFDTUksRUFBQTtVQUFBRixJQUFBO1VBQUFGO1FBQWdCLENBQUM7UUFBQUwsQ0FBQSxNQUFBTyxJQUFBO1FBQUFQLENBQUEsTUFBQUssT0FBQTtRQUFBTCxDQUFBLE1BQUFTLEVBQUE7TUFBQTtRQUFBQSxFQUFBLEdBQUFULENBQUE7TUFBQTtNQUF4QkUsRUFBQSxHQUFPTyxFQUFpQjtJQUFBO0lBQUFULENBQUEsTUFBQUQsT0FBQSxDQUFBSSxrQkFBQTtJQUFBSCxDQUFBLE1BQUFILFNBQUE7SUFBQUcsQ0FBQSxNQUFBRixLQUFBO0lBQUFFLENBQUEsTUFBQUUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUYsQ0FBQTtFQUFBO0VBQUEsT0FUbkJFLEVBVXdCO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/components/messages/nullRenderingAttachments.ts`

**信息:**
- 行数: 70
- 大小: 2257 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Attachment } from 'src/utils/attachments.js'
import type { Message, NormalizedMessage } from '../../types/message.js'

/**
 * Attachment types that AttachmentMessage renders as `null` unconditionally
 * (no visible output regardless of runtime state). Messages.tsx filters these
 * out BEFORE the render cap / message count so invisible entries don't consume
 * the 200-message render budget (CC-724).
 *
 * Sync is enforced by TypeScript: AttachmentMessage's switch `default:` branch
 * asserts `attachment.type satisfies NullRenderingAttachmentType`. Adding a new
 * Attachment type without either a case or an entry here will fail typecheck.
 */
const NULL_RENDERING_TYPES = [
  'hook_success',
  'hook_additional_context',
  'hook_cancelled',
  'command_permissions',
  'agent_mention',
  'budget_usd',
  'critical_system_reminder',
  'edited_image_file',
  'edited_text_file',
  'opened_file_in_ide',
  'output_style',
  'plan_mode',
  'plan_mode_exit',
  'plan_mode_reentry',
  'structured_output',
  'team_context',
  'todo_reminder',
  'context_efficiency',
  'deferred_tools_delta',
  'mcp_instructions_delta',
  'companion_intro',
  'token_usage',
  'ultrathink_effort',
  'max_turns_reached',
  'task_reminder',
  'auto_mode',
  'auto_mode_exit',
  'output_token_usage',
  'pen_mode_enter',
  'pen_mode_exit',
  'verify_plan_reminder',
  'current_session_memory',
  'compaction_reminder',
  'date_change',
] as const satisfies readonly Attachment['type'][]


```

---


### `src/components/messages/teamMemCollapsed.tsx`

**信息:**
- 行数: 140
- 大小: 13711 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Text } from '../../ink.js';
import type { CollapsedReadSearchGroup } from '../../types/message.js';

/**
 * Plain function (not a React component) so the React Compiler won't
 * hoist the teamMemory* property accesses for memoization. This module
 * is only loaded when feature('TEAMMEM') is true.
 */
export function checkHasTeamMemOps(message: CollapsedReadSearchGroup): boolean {
  return (message.teamMemorySearchCount ?? 0) > 0 || (message.teamMemoryReadCount ?? 0) > 0 || (message.teamMemoryWriteCount ?? 0) > 0;
}

/**
 * Renders team memory count parts for the collapsed read/search UI.
 * This module is only loaded when feature('TEAMMEM') is true,
 * so DCE removes it entirely from external builds.
 */
export function TeamMemCountParts(t0) {
  const $ = _c(23);
  const {
    message,
    isActiveGroup,
    hasPrecedingParts
  } = t0;
  const tmReadCount = message.teamMemoryReadCount ?? 0;
  const tmSearchCount = message.teamMemorySearchCount ?? 0;
  const tmWriteCount = message.teamMemoryWriteCount ?? 0;
  if (tmReadCount === 0 && tmSearchCount === 0 && tmWriteCount === 0) {
    return null;
  }
  let t1;
  if ($[0] !== hasPrecedingParts || $[1] !== isActiveGroup || $[2] !== tmReadCount || $[3] !== tmSearchCount || $[4] !== tmWriteCount) {
    const nodes = [];
    let count = hasPrecedingParts ? 1 : 0;
    if (tmReadCount > 0) {
      const verb = isActiveGroup ? count === 0 ? "Recalling" : "recalling" : count === 0 ? "Recalled" : "recalled";
      if (count > 0) {
        let t2;
        if ($[6] === Symbol.for("react.memo_cache_sentinel")) {
          t2 = <Text key="comma-tmr">, </Text>;
          $[6] = t2;
        } else {
          t2 = $[6];
        }
        nodes.push(t2);
      }
      let t2;
      if ($[7] !== tmReadCount) {

```

---


### `src/components/messages/teamMemSaved.ts`

**信息:**
- 行数: 19
- 大小: 711 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { SystemMemorySavedMessage } from '../../types/message.js'

/**
 * Returns the team-memory segment for the memory-saved UI, plus the count so
 * the caller can derive the private count without accessing teamCount itself.
 * Plain function (not a React component) so the React Compiler won't hoist
 * the teamCount property access for memoization. This module is only loaded
 * when feature('TEAMMEM') is true.
 */
export function teamMemSavedPart(
  message: SystemMemorySavedMessage,
): { segment: string; count: number } | null {
  const count = message.teamCount ?? 0
  if (count === 0) return null
  return {
    segment: `${count} team ${count === 1 ? 'memory' : 'memories'}`,
    count,
  }
}

```

---


### `src/components/permissions/AskUserQuestionPermissionRequest/AskUserQuestionPermissionRequest.tsx`

**信息:**
- 行数: 645
- 大小: 82469 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { Base64ImageSource, ImageBlockParam } from '@anthropic-ai/sdk/resources/messages.mjs';
import React, { Suspense, use, useCallback, useMemo, useRef, useState } from 'react';
import { useSettings } from '../../../hooks/useSettings.js';
import { useTerminalSize } from '../../../hooks/useTerminalSize.js';
import { stringWidth } from '../../../ink/stringWidth.js';
import { useTheme } from '../../../ink.js';
import { useKeybindings } from '../../../keybindings/useKeybinding.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../../services/analytics/index.js';
import { useAppState } from '../../../state/AppState.js';
import type { Question } from '../../../tools/AskUserQuestionTool/AskUserQuestionTool.js';
import { AskUserQuestionTool } from '../../../tools/AskUserQuestionTool/AskUserQuestionTool.js';
import { type CliHighlight, getCliHighlightPromise } from '../../../utils/cliHighlight.js';
import type { PastedContent } from '../../../utils/config.js';
import type { ImageDimensions } from '../../../utils/imageResizer.js';
import { maybeResizeAndDownsampleImageBlock } from '../../../utils/imageResizer.js';
import { cacheImagePath, storeImage } from '../../../utils/imageStore.js';
import { logError } from '../../../utils/log.js';
import { applyMarkdown } from '../../../utils/markdown.js';
import { isPlanModeInterviewPhaseEnabled } from '../../../utils/planModeV2.js';
import { getPlanFilePath } from '../../../utils/plans.js';
import type { PermissionRequestProps } from '../PermissionRequest.js';
import { QuestionView } from './QuestionView.js';
import { SubmitQuestionsView } from './SubmitQuestionsView.js';
import { useMultipleChoiceState } from './use-multiple-choice-state.js';
const MIN_CONTENT_HEIGHT = 12;
const MIN_CONTENT_WIDTH = 40;
// Lines used by chrome around the content area (nav bar, title, footer, help text, etc.)
const CONTENT_CHROME_OVERHEAD = 15;
export function AskUserQuestionPermissionRequest(props) {
  const $ = _c(4);
  const settings = useSettings();
  if (settings.syntaxHighlightingDisabled) {
    let t0;
    if ($[0] !== props) {
      t0 = <AskUserQuestionPermissionRequestBody {...props} highlight={null} />;
      $[0] = props;
      $[1] = t0;
    } else {
      t0 = $[1];
    }
    return t0;
  }
  let t0;
  if ($[2] !== props) {
    t0 = <Suspense fallback={<AskUserQuestionPermissionRequestBody {...props} highlight={null} />}><AskUserQuestionWithHighlight {...props} /></Suspense>;
    $[2] = props;
    $[3] = t0;
  } else {
    t0 = $[3];

```

---


### `src/components/permissions/AskUserQuestionPermissionRequest/PreviewBox.tsx`

**信息:**
- 行数: 229
- 大小: 25959 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { Suspense, use, useMemo } from 'react';
import { useSettings } from '../../../hooks/useSettings.js';
import { useTerminalSize } from '../../../hooks/useTerminalSize.js';
import { stringWidth } from '../../../ink/stringWidth.js';
import { Ansi, Box, Text, useTheme } from '../../../ink.js';
import { type CliHighlight, getCliHighlightPromise } from '../../../utils/cliHighlight.js';
import { applyMarkdown } from '../../../utils/markdown.js';
import sliceAnsi from '../../../utils/sliceAnsi.js';
type PreviewBoxProps = {
  /** The preview content to display. Markdown is rendered with syntax highlighting
   * for code blocks (```ts, ```py, etc.). Also supports plain multi-line text. */
  content: string;
  /** Maximum number of lines to display before truncating. @default 20 */
  maxLines?: number;
  /** Minimum height (in lines) for the preview box. Content will be padded if shorter. */
  minHeight?: number;
  /** Minimum width for the preview box. @default 40 */
  minWidth?: number;
  /** Maximum width available for this box (e.g., the container width). */
  maxWidth?: number;
};
const BOX_CHARS = {
  topLeft: '┌',
  topRight: '┐',
  bottomLeft: '└',
  bottomRight: '┘',
  horizontal: '─',
  vertical: '│',
  teeLeft: '├',
  teeRight: '┤'
};

/**
 * A bordered monospace box for displaying preview content.
 * Truncates content that exceeds maxLines with an indicator.
 * The parent component should pass maxLines based on its available height budget.
 */
export function PreviewBox(props) {
  const $ = _c(4);
  const settings = useSettings();
  if (settings.syntaxHighlightingDisabled) {
    let t0;
    if ($[0] !== props) {
      t0 = <PreviewBoxBody {...props} highlight={null} />;
      $[0] = props;
      $[1] = t0;
    } else {
      t0 = $[1];
    }

```

---


### `src/components/permissions/AskUserQuestionPermissionRequest/PreviewQuestionView.tsx`

**信息:**
- 行数: 328
- 大小: 52983 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import figures from 'figures';
import React, { useCallback, useMemo, useRef, useState } from 'react';
import { useTerminalSize } from '../../../hooks/useTerminalSize.js';
import type { KeyboardEvent } from '../../../ink/events/keyboard-event.js';
import { Box, Text } from '../../../ink.js';
import { useKeybinding, useKeybindings } from '../../../keybindings/useKeybinding.js';
import { useAppState } from '../../../state/AppState.js';
import type { Question } from '../../../tools/AskUserQuestionTool/AskUserQuestionTool.js';
import { getExternalEditor } from '../../../utils/editor.js';
import { toIDEDisplayName } from '../../../utils/ide.js';
import { editPromptInEditor } from '../../../utils/promptEditor.js';
import { Divider } from '../../design-system/Divider.js';
import TextInput from '../../TextInput.js';
import { PermissionRequestTitle } from '../PermissionRequestTitle.js';
import { PreviewBox } from './PreviewBox.js';
import { QuestionNavigationBar } from './QuestionNavigationBar.js';
import type { QuestionState } from './use-multiple-choice-state.js';
type Props = {
  question: Question;
  questions: Question[];
  currentQuestionIndex: number;
  answers: Record<string, string>;
  questionStates: Record<string, QuestionState>;
  hideSubmitTab?: boolean;
  minContentHeight?: number;
  minContentWidth?: number;
  onUpdateQuestionState: (questionText: string, updates: Partial<QuestionState>, isMultiSelect: boolean) => void;
  onAnswer: (questionText: string, label: string | string[], textInput?: string, shouldAdvance?: boolean) => void;
  onTextInputFocus: (isInInput: boolean) => void;
  onCancel: () => void;
  onTabPrev?: () => void;
  onTabNext?: () => void;
  onRespondToClaude: () => void;
  onFinishPlanInterview: () => void;
};

/**
 * A side-by-side question view for questions with preview content.
 * Displays a vertical option list on the left with a preview panel on the right.
 */
export function PreviewQuestionView({
  question,
  questions,
  currentQuestionIndex,
  answers,
  questionStates,
  hideSubmitTab = false,
  minContentHeight,
  minContentWidth,
  onUpdateQuestionState,

```

---


### `src/components/permissions/AskUserQuestionPermissionRequest/QuestionNavigationBar.tsx`

**信息:**
- 行数: 178
- 大小: 22963 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { useMemo } from 'react';
import { useTerminalSize } from '../../../hooks/useTerminalSize.js';
import { stringWidth } from '../../../ink/stringWidth.js';
import { Box, Text } from '../../../ink.js';
import type { Question } from '../../../tools/AskUserQuestionTool/AskUserQuestionTool.js';
import { truncateToWidth } from '../../../utils/format.js';
type Props = {
  questions: Question[];
  currentQuestionIndex: number;
  answers: Record<string, string>;
  hideSubmitTab?: boolean;
};
export function QuestionNavigationBar(t0) {
  const $ = _c(39);
  const {
    questions,
    currentQuestionIndex,
    answers,
    hideSubmitTab: t1
  } = t0;
  const hideSubmitTab = t1 === undefined ? false : t1;
  const {
    columns
  } = useTerminalSize();
  let t2;
  if ($[0] !== columns || $[1] !== currentQuestionIndex || $[2] !== hideSubmitTab || $[3] !== questions) {
    bb0: {
      const submitText = hideSubmitTab ? "" : ` ${figures.tick} Submit `;
      const fixedWidth = stringWidth("\u2190 ") + stringWidth(" \u2192") + stringWidth(submitText);
      const availableForTabs = columns - fixedWidth;
      if (availableForTabs <= 0) {
        let t3;
        if ($[5] !== currentQuestionIndex || $[6] !== questions) {
          let t4;
          if ($[8] !== currentQuestionIndex) {
            t4 = (q, index) => {
              const header = q?.header || `Q${index + 1}`;
              return index === currentQuestionIndex ? header.slice(0, 3) : "";
            };
            $[8] = currentQuestionIndex;
            $[9] = t4;
          } else {
            t4 = $[9];
          }
          t3 = questions.map(t4);
          $[5] = currentQuestionIndex;
          $[6] = questions;
          $[7] = t3;

```

---


### `src/components/permissions/AskUserQuestionPermissionRequest/QuestionView.tsx`

**信息:**
- 行数: 465
- 大小: 58579 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { useCallback, useState } from 'react';
import type { KeyboardEvent } from '../../../ink/events/keyboard-event.js';
import { Box, Text } from '../../../ink.js';
import { useAppState } from '../../../state/AppState.js';
import type { Question, QuestionOption } from '../../../tools/AskUserQuestionTool/AskUserQuestionTool.js';
import type { PastedContent } from '../../../utils/config.js';
import { getExternalEditor } from '../../../utils/editor.js';
import { toIDEDisplayName } from '../../../utils/ide.js';
import type { ImageDimensions } from '../../../utils/imageResizer.js';
import { editPromptInEditor } from '../../../utils/promptEditor.js';
import { type OptionWithDescription, Select, SelectMulti } from '../../CustomSelect/index.js';
import { Divider } from '../../design-system/Divider.js';
import { FilePathLink } from '../../FilePathLink.js';
import { PermissionRequestTitle } from '../PermissionRequestTitle.js';
import { PreviewQuestionView } from './PreviewQuestionView.js';
import { QuestionNavigationBar } from './QuestionNavigationBar.js';
import type { QuestionState } from './use-multiple-choice-state.js';
type Props = {
  question: Question;
  questions: Question[];
  currentQuestionIndex: number;
  answers: Record<string, string>;
  questionStates: Record<string, QuestionState>;
  hideSubmitTab?: boolean;
  planFilePath?: string;
  pastedContents?: Record<number, PastedContent>;
  minContentHeight?: number;
  minContentWidth?: number;
  onUpdateQuestionState: (questionText: string, updates: Partial<QuestionState>, isMultiSelect: boolean) => void;
  onAnswer: (questionText: string, label: string | string[], textInput?: string, shouldAdvance?: boolean) => void;
  onTextInputFocus: (isInInput: boolean) => void;
  onCancel: () => void;
  onSubmit: () => void;
  onTabPrev?: () => void;
  onTabNext?: () => void;
  onRespondToClaude: () => void;
  onFinishPlanInterview: () => void;
  onImagePaste?: (base64Image: string, mediaType?: string, filename?: string, dimensions?: ImageDimensions, sourcePath?: string) => void;
  onRemoveImage?: (id: number) => void;
};
export function QuestionView(t0) {
  const $ = _c(114);
  const {
    question,
    questions,
    currentQuestionIndex,
    answers,
    questionStates,

```

---


### `src/components/permissions/AskUserQuestionPermissionRequest/SubmitQuestionsView.tsx`

**信息:**
- 行数: 144
- 大小: 16641 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React from 'react';
import { Box, Text } from '../../../ink.js';
import type { Question } from '../../../tools/AskUserQuestionTool/AskUserQuestionTool.js';
import type { PermissionDecision } from '../../../utils/permissions/PermissionResult.js';
import { Select } from '../../CustomSelect/index.js';
import { Divider } from '../../design-system/Divider.js';
import { PermissionRequestTitle } from '../PermissionRequestTitle.js';
import { PermissionRuleExplanation } from '../PermissionRuleExplanation.js';
import { QuestionNavigationBar } from './QuestionNavigationBar.js';
type Props = {
  questions: Question[];
  currentQuestionIndex: number;
  answers: Record<string, string>;
  allQuestionsAnswered: boolean;
  permissionResult: PermissionDecision;
  minContentHeight?: number;
  onFinalResponse: (value: 'submit' | 'cancel') => void;
};
export function SubmitQuestionsView(t0) {
  const $ = _c(27);
  const {
    questions,
    currentQuestionIndex,
    answers,
    allQuestionsAnswered,
    permissionResult,
    minContentHeight,
    onFinalResponse
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = <Divider color="inactive" />;
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  let t2;
  if ($[1] !== answers || $[2] !== currentQuestionIndex || $[3] !== questions) {
    t2 = <QuestionNavigationBar questions={questions} currentQuestionIndex={currentQuestionIndex} answers={answers} />;
    $[1] = answers;
    $[2] = currentQuestionIndex;
    $[3] = questions;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  let t3;
  if ($[5] === Symbol.for("react.memo_cache_sentinel")) {

```

---


### `src/components/permissions/AskUserQuestionPermissionRequest/use-multiple-choice-state.ts`

**信息:**
- 行数: 179
- 大小: 4142 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useReducer } from 'react'

export type AnswerValue = string

export type QuestionState = {
  selectedValue?: string | string[]
  textInputValue: string
}

type State = {
  currentQuestionIndex: number
  answers: Record<string, AnswerValue>
  questionStates: Record<string, QuestionState>
  isInTextInput: boolean
}

type Action =
  | { type: 'next-question' }
  | { type: 'prev-question' }
  | {
      type: 'update-question-state'
      questionText: string
      updates: Partial<QuestionState>
      isMultiSelect: boolean
    }
  | {
      type: 'set-answer'
      questionText: string
      answer: string
      shouldAdvance: boolean
    }
  | { type: 'set-text-input-mode'; isInInput: boolean }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'next-question':
      return {
        ...state,
        currentQuestionIndex: state.currentQuestionIndex + 1,
        isInTextInput: false,
      }

    case 'prev-question':
      return {
        ...state,
        currentQuestionIndex: Math.max(0, state.currentQuestionIndex - 1),
        isInTextInput: false,
      }

    case 'update-question-state': {

```

---


### `src/components/permissions/BashPermissionRequest/BashPermissionRequest.tsx`

**信息:**
- 行数: 482
- 大小: 75744 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import figures from 'figures';
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Box, Text, useTheme } from '../../../ink.js';
import { useKeybinding } from '../../../keybindings/useKeybinding.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../../services/analytics/growthbook.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../../services/analytics/index.js';
import { sanitizeToolNameForAnalytics } from '../../../services/analytics/metadata.js';
import { useAppState } from '../../../state/AppState.js';
import { BashTool } from '../../../tools/BashTool/BashTool.js';
import { getFirstWordPrefix, getSimpleCommandPrefix } from '../../../tools/BashTool/bashPermissions.js';
import { getDestructiveCommandWarning } from '../../../tools/BashTool/destructiveCommandWarning.js';
import { parseSedEditCommand } from '../../../tools/BashTool/sedEditParser.js';
import { shouldUseSandbox } from '../../../tools/BashTool/shouldUseSandbox.js';
import { getCompoundCommandPrefixesStatic } from '../../../utils/bash/prefix.js';
import { createPromptRuleContent, generateGenericDescription, getBashPromptAllowDescriptions, isClassifierPermissionsEnabled } from '../../../utils/permissions/bashClassifier.js';
import { extractRules } from '../../../utils/permissions/PermissionUpdate.js';
import type { PermissionUpdate } from '../../../utils/permissions/PermissionUpdateSchema.js';
import { SandboxManager } from '../../../utils/sandbox/sandbox-adapter.js';
import { Select } from '../../CustomSelect/select.js';
import { ShimmerChar } from '../../Spinner/ShimmerChar.js';
import { useShimmerAnimation } from '../../Spinner/useShimmerAnimation.js';
import { type UnaryEvent, usePermissionRequestLogging } from '../hooks.js';
import { PermissionDecisionDebugInfo } from '../PermissionDecisionDebugInfo.js';
import { PermissionDialog } from '../PermissionDialog.js';
import { PermissionExplainerContent, usePermissionExplainerUI } from '../PermissionExplanation.js';
import type { PermissionRequestProps } from '../PermissionRequest.js';
import { PermissionRuleExplanation } from '../PermissionRuleExplanation.js';
import { SedEditPermissionRequest } from '../SedEditPermissionRequest/SedEditPermissionRequest.js';
import { useShellPermissionFeedback } from '../useShellPermissionFeedback.js';
import { logUnaryPermissionEvent } from '../utils.js';
import { bashToolUseOptions } from './bashToolUseOptions.js';
const CHECKING_TEXT = 'Attempting to auto-approve\u2026';

// Isolates the 20fps shimmer clock from BashPermissionRequestInner. Before this
// extraction, useShimmerAnimation lived inside the 535-line Inner body, so every
// 50ms clock tick re-rendered the entire dialog (PermissionDialog + Select +
// all children) for the ~1-3 seconds the classifier typically takes. Inner also
// has a Compiler bailout (see below), so nothing was auto-memoized — the full
// JSX tree was reconstructed 20-60 times per classifier check.
function ClassifierCheckingSubtitle() {
  const $ = _c(6);
  const [ref, glimmerIndex] = useShimmerAnimation("requesting", CHECKING_TEXT, false);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = [...CHECKING_TEXT];
    $[0] = t0;
  } else {
    t0 = $[0];

```

---


### `src/components/permissions/BashPermissionRequest/bashToolUseOptions.tsx`

**信息:**
- 行数: 147
- 大小: 21446 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { BASH_TOOL_NAME } from '../../../tools/BashTool/toolName.js';
import { extractOutputRedirections } from '../../../utils/bash/commands.js';
import { isClassifierPermissionsEnabled } from '../../../utils/permissions/bashClassifier.js';
import type { PermissionDecisionReason } from '../../../utils/permissions/PermissionResult.js';
import type { PermissionUpdate } from '../../../utils/permissions/PermissionUpdateSchema.js';
import { shouldShowAlwaysAllowOptions } from '../../../utils/permissions/permissionsLoader.js';
import type { OptionWithDescription } from '../../CustomSelect/select.js';
import { generateShellSuggestionsLabel } from '../shellPermissionHelpers.js';
export type BashToolUseOption = 'yes' | 'yes-apply-suggestions' | 'yes-prefix-edited' | 'yes-classifier-reviewed' | 'no';

/**
 * Check if a description already exists in the allow list.
 * Compares lowercase and trailing-whitespace-trimmed versions.
 */
function descriptionAlreadyExists(description: string, existingDescriptions: string[]): boolean {
  const normalized = description.toLowerCase().trimEnd();
  return existingDescriptions.some(existing => existing.toLowerCase().trimEnd() === normalized);
}

/**
 * Strip output redirections so filenames don't show as commands in the label.
 */
function stripBashRedirections(command: string): string {
  const {
    commandWithoutRedirections,
    redirections
  } = extractOutputRedirections(command);
  // Only use stripped version if there were actual redirections
  return redirections.length > 0 ? commandWithoutRedirections : command;
}
export function bashToolUseOptions({
  suggestions = [],
  decisionReason,
  onRejectFeedbackChange,
  onAcceptFeedbackChange,
  onClassifierDescriptionChange,
  classifierDescription,
  initialClassifierDescriptionEmpty = false,
  existingAllowDescriptions = [],
  yesInputMode = false,
  noInputMode = false,
  editablePrefix,
  onEditablePrefixChange
}: {
  suggestions?: PermissionUpdate[];
  decisionReason?: PermissionDecisionReason;
  onRejectFeedbackChange: (value: string) => void;
  onAcceptFeedbackChange: (value: string) => void;
  onClassifierDescriptionChange?: (value: string) => void;
  classifierDescription?: string;

```

---


### `src/components/permissions/ComputerUseApproval/ComputerUseApproval.tsx`

**信息:**
- 行数: 441
- 大小: 44745 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { getSentinelCategory } from '@ant/computer-use-mcp/sentinelApps';
import type { CuPermissionRequest, CuPermissionResponse } from '@ant/computer-use-mcp/types';
import { DEFAULT_GRANT_FLAGS } from '@ant/computer-use-mcp/types';
import figures from 'figures';
import * as React from 'react';
import { useMemo, useState } from 'react';
import { Box, Text } from '../../../ink.js';
import { execFileNoThrow } from '../../../utils/execFileNoThrow.js';
import { plural } from '../../../utils/stringUtils.js';
import type { OptionWithDescription } from '../../CustomSelect/select.js';
import { Select } from '../../CustomSelect/select.js';
import { Dialog } from '../../design-system/Dialog.js';
type ComputerUseApprovalProps = {
  request: CuPermissionRequest;
  onDone: (response: CuPermissionResponse) => void;
};
const DENY_ALL_RESPONSE: CuPermissionResponse = {
  granted: [],
  denied: [],
  flags: DEFAULT_GRANT_FLAGS
};

/**
 * Two-panel dispatcher. When `request.tccState` is present, macOS permissions
 * (Accessibility / Screen Recording) are missing and the app list is
 * irrelevant — show a TCC panel that opens System Settings. Otherwise show the
 * app allowlist + grant-flags panel.
 */
export function ComputerUseApproval(t0) {
  const $ = _c(3);
  const {
    request,
    onDone
  } = t0;
  let t1;
  if ($[0] !== onDone || $[1] !== request) {
    t1 = request.tccState ? <ComputerUseTccPanel tccState={request.tccState} onDone={() => onDone(DENY_ALL_RESPONSE)} /> : <ComputerUseAppListPanel request={request} onDone={onDone} />;
    $[0] = onDone;
    $[1] = request;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  return t1;
}

// ── TCC panel ─────────────────────────────────────────────────────────────

type TccOption = 'open_accessibility' | 'open_screen_recording' | 'retry';

```

---


### `src/components/permissions/EnterPlanModePermissionRequest/EnterPlanModePermissionRequest.tsx`

**信息:**
- 行数: 122
- 大小: 13340 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { handlePlanModeTransition } from '../../../bootstrap/state.js';
import { Box, Text } from '../../../ink.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../../services/analytics/index.js';
import { useAppState } from '../../../state/AppState.js';
import { isPlanModeInterviewPhaseEnabled } from '../../../utils/planModeV2.js';
import { Select } from '../../CustomSelect/index.js';
import { PermissionDialog } from '../PermissionDialog.js';
import type { PermissionRequestProps } from '../PermissionRequest.js';
export function EnterPlanModePermissionRequest(t0) {
  const $ = _c(18);
  const {
    toolUseConfirm,
    onDone,
    onReject,
    workerBadge
  } = t0;
  const toolPermissionContextMode = useAppState(_temp);
  let t1;
  if ($[0] !== onDone || $[1] !== onReject || $[2] !== toolPermissionContextMode || $[3] !== toolUseConfirm) {
    t1 = function handleResponse(value) {
      if (value === "yes") {
        logEvent("tengu_plan_enter", {
          interviewPhaseEnabled: isPlanModeInterviewPhaseEnabled(),
          entryMethod: "tool" as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS
        });
        handlePlanModeTransition(toolPermissionContextMode, "plan");
        onDone();
        toolUseConfirm.onAllow({}, [{
          type: "setMode",
          mode: "plan",
          destination: "session"
        }]);
      } else {
        onDone();
        onReject();
        toolUseConfirm.onReject();
      }
    };
    $[0] = onDone;
    $[1] = onReject;
    $[2] = toolPermissionContextMode;
    $[3] = toolUseConfirm;
    $[4] = t1;
  } else {
    t1 = $[4];
  }
  const handleResponse = t1;
  let t2;

```

---


### `src/components/permissions/ExitPlanModePermissionRequest/ExitPlanModePermissionRequest.tsx`

**信息:**
- 行数: 768
- 大小: 121607 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import type { UUID } from 'crypto';
import figures from 'figures';
import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { useNotifications } from 'src/context/notifications.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from 'src/services/analytics/index.js';
import { useAppState, useAppStateStore, useSetAppState } from 'src/state/AppState.js';
import { getSdkBetas, getSessionId, isSessionPersistenceDisabled, setHasExitedPlanMode, setNeedsAutoModeExitAttachment, setNeedsPlanModeExitAttachment } from '../../../bootstrap/state.js';
import { generateSessionName } from '../../../commands/rename/generateSessionName.js';
import { launchUltraplan } from '../../../commands/ultraplan.js';
import type { KeyboardEvent } from '../../../ink/events/keyboard-event.js';
import { Box, Text } from '../../../ink.js';
import type { AppState } from '../../../state/AppStateStore.js';
import { AGENT_TOOL_NAME } from '../../../tools/AgentTool/constants.js';
import { EXIT_PLAN_MODE_V2_TOOL_NAME } from '../../../tools/ExitPlanModeTool/constants.js';
import type { AllowedPrompt } from '../../../tools/ExitPlanModeTool/ExitPlanModeV2Tool.js';
import { TEAM_CREATE_TOOL_NAME } from '../../../tools/TeamCreateTool/constants.js';
import { isAgentSwarmsEnabled } from '../../../utils/agentSwarmsEnabled.js';
import { calculateContextPercentages, getContextWindowForModel } from '../../../utils/context.js';
import { getExternalEditor } from '../../../utils/editor.js';
import { getDisplayPath } from '../../../utils/file.js';
import { toIDEDisplayName } from '../../../utils/ide.js';
import { logError } from '../../../utils/log.js';
import { enqueuePendingNotification } from '../../../utils/messageQueueManager.js';
import { createUserMessage } from '../../../utils/messages.js';
import { getMainLoopModel, getRuntimeMainLoopModel } from '../../../utils/model/model.js';
import { createPromptRuleContent, isClassifierPermissionsEnabled, PROMPT_PREFIX } from '../../../utils/permissions/bashClassifier.js';
import { type PermissionMode, toExternalPermissionMode } from '../../../utils/permissions/PermissionMode.js';
import type { PermissionUpdate } from '../../../utils/permissions/PermissionUpdateSchema.js';
import { isAutoModeGateEnabled, restoreDangerousPermissions, stripDangerousPermissionsForAutoMode } from '../../../utils/permissions/permissionSetup.js';
import { getPewterLedgerVariant, isPlanModeInterviewPhaseEnabled } from '../../../utils/planModeV2.js';
import { getPlan, getPlanFilePath } from '../../../utils/plans.js';
import { editFileInEditor, editPromptInEditor } from '../../../utils/promptEditor.js';
import { getCurrentSessionTitle, getTranscriptPath, saveAgentName, saveCustomTitle } from '../../../utils/sessionStorage.js';
import { getSettings_DEPRECATED } from '../../../utils/settings/settings.js';
import { type OptionWithDescription, Select } from '../../CustomSelect/index.js';
import { Markdown } from '../../Markdown.js';
import { PermissionDialog } from '../PermissionDialog.js';
import type { PermissionRequestProps } from '../PermissionRequest.js';
import { PermissionRuleExplanation } from '../PermissionRuleExplanation.js';

/* eslint-disable @typescript-eslint/no-require-imports */
const autoModeStateModule = feature('TRANSCRIPT_CLASSIFIER') ? require('../../../utils/permissions/autoModeState.js') as typeof import('../../../utils/permissions/autoModeState.js') : null;
import type { Base64ImageSource, ImageBlockParam } from '@anthropic-ai/sdk/resources/messages.mjs';
/* eslint-enable @typescript-eslint/no-require-imports */
import type { PastedContent } from '../../../utils/config.js';
import type { ImageDimensions } from '../../../utils/imageResizer.js';
import { maybeResizeAndDownsampleImageBlock } from '../../../utils/imageResizer.js';
import { cacheImagePath, storeImage } from '../../../utils/imageStore.js';
type ResponseValue = 'yes-bypass-permissions' | 'yes-accept-edits' | 'yes-accept-edits-keep-context' | 'yes-default-keep-context' | 'yes-resume-auto-mode' | 'yes-auto-clear-context' | 'ultraplan' | 'no';

```

---


### `src/components/permissions/FallbackPermissionRequest.tsx`

**信息:**
- 行数: 333
- 大小: 30677 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useMemo } from 'react';
import { getOriginalCwd } from '../../bootstrap/state.js';
import { Box, Text, useTheme } from '../../ink.js';
import { sanitizeToolNameForAnalytics } from '../../services/analytics/metadata.js';
import { env } from '../../utils/env.js';
import { shouldShowAlwaysAllowOptions } from '../../utils/permissions/permissionsLoader.js';
import { truncateToLines } from '../../utils/stringUtils.js';
import { logUnaryEvent } from '../../utils/unaryLogging.js';
import { type UnaryEvent, usePermissionRequestLogging } from './hooks.js';
import { PermissionDialog } from './PermissionDialog.js';
import { PermissionPrompt, type PermissionPromptOption, type ToolAnalyticsContext } from './PermissionPrompt.js';
import type { PermissionRequestProps } from './PermissionRequest.js';
import { PermissionRuleExplanation } from './PermissionRuleExplanation.js';
type FallbackOptionValue = 'yes' | 'yes-dont-ask-again' | 'no';
export function FallbackPermissionRequest(t0) {
  const $ = _c(58);
  const {
    toolUseConfirm,
    onDone,
    onReject,
    workerBadge
  } = t0;
  const [theme] = useTheme();
  let originalUserFacingName;
  let t1;
  if ($[0] !== toolUseConfirm.input || $[1] !== toolUseConfirm.tool) {
    originalUserFacingName = toolUseConfirm.tool.userFacingName(toolUseConfirm.input as never);
    t1 = originalUserFacingName.endsWith(" (MCP)") ? originalUserFacingName.slice(0, -6) : originalUserFacingName;
    $[0] = toolUseConfirm.input;
    $[1] = toolUseConfirm.tool;
    $[2] = originalUserFacingName;
    $[3] = t1;
  } else {
    originalUserFacingName = $[2];
    t1 = $[3];
  }
  const userFacingName = t1;
  let t2;
  if ($[4] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = {
      completion_type: "tool_use_single",
      language_name: "none"
    };
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  const unaryEvent = t2;
  usePermissionRequestLogging(toolUseConfirm, unaryEvent);

```

---


### `src/components/permissions/FileEditPermissionRequest/FileEditPermissionRequest.tsx`

**信息:**
- 行数: 182
- 大小: 16257 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { basename, relative } from 'path';
import React from 'react';
import { FileEditToolDiff } from 'src/components/FileEditToolDiff.js';
import { getCwd } from 'src/utils/cwd.js';
import type { z } from 'zod/v4';
import { Text } from '../../../ink.js';
import { FileEditTool } from '../../../tools/FileEditTool/FileEditTool.js';
import { FilePermissionDialog } from '../FilePermissionDialog/FilePermissionDialog.js';
import { createSingleEditDiffConfig, type FileEdit, type IDEDiffSupport } from '../FilePermissionDialog/ideDiffConfig.js';
import type { PermissionRequestProps } from '../PermissionRequest.js';
type FileEditInput = z.infer<typeof FileEditTool.inputSchema>;
const ideDiffSupport: IDEDiffSupport<FileEditInput> = {
  getConfig: (input: FileEditInput) => createSingleEditDiffConfig(input.file_path, input.old_string, input.new_string, input.replace_all),
  applyChanges: (input: FileEditInput, modifiedEdits: FileEdit[]) => {
    const firstEdit = modifiedEdits[0];
    if (firstEdit) {
      return {
        ...input,
        old_string: firstEdit.old_string,
        new_string: firstEdit.new_string,
        replace_all: firstEdit.replace_all
      };
    }
    return input;
  }
};
export function FileEditPermissionRequest(props) {
  const $ = _c(51);
  const parseInput = _temp;
  let T0;
  let T1;
  let T2;
  let file_path;
  let new_string;
  let old_string;
  let replace_all;
  let t0;
  let t1;
  let t10;
  let t2;
  let t3;
  let t4;
  let t5;
  let t6;
  let t7;
  let t8;
  let t9;
  if ($[0] !== props.onDone || $[1] !== props.onReject || $[2] !== props.toolUseConfirm || $[3] !== props.toolUseContext || $[4] !== props.workerBadge) {
    const parsed = parseInput(props.toolUseConfirm.input);

```

---


### `src/components/permissions/FilePermissionDialog/FilePermissionDialog.tsx`

**信息:**
- 行数: 204
- 大小: 30317 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { relative } from 'path';
import React, { useMemo } from 'react';
import { useDiffInIDE } from '../../../hooks/useDiffInIDE.js';
import { Box, Text } from '../../../ink.js';
import type { ToolUseContext } from '../../../Tool.js';
import { getLanguageName } from '../../../utils/cliHighlight.js';
import { getCwd } from '../../../utils/cwd.js';
import { getFsImplementation, safeResolvePath } from '../../../utils/fsOperations.js';
import { expandPath } from '../../../utils/path.js';
import type { CompletionType } from '../../../utils/unaryLogging.js';
import { Select } from '../../CustomSelect/index.js';
import { ShowInIDEPrompt } from '../../ShowInIDEPrompt.js';
import { usePermissionRequestLogging } from '../hooks.js';
import { PermissionDialog } from '../PermissionDialog.js';
import type { ToolUseConfirm } from '../PermissionRequest.js';
import type { WorkerBadgeProps } from '../WorkerBadge.js';
import type { IDEDiffSupport } from './ideDiffConfig.js';
import type { FileOperationType, PermissionOption } from './permissionOptions.js';
import { type ToolInput, useFilePermissionDialog } from './useFilePermissionDialog.js';
export type FilePermissionDialogProps<T extends ToolInput = ToolInput> = {
  // Required props from PermissionRequestProps
  toolUseConfirm: ToolUseConfirm;
  toolUseContext: ToolUseContext;
  onDone: () => void;
  onReject: () => void;

  // Dialog customization
  title: string;
  subtitle?: React.ReactNode;
  question?: string | React.ReactNode;
  content?: React.ReactNode; // Can be general content or diff component

  // Logging
  completionType?: CompletionType;
  languageName?: string; // override — derived from path when omitted

  // File/directory operations
  path: string | null;
  parseInput: (input: unknown) => T;
  operationType?: FileOperationType;

  // IDE diff support
  ideDiffSupport?: IDEDiffSupport<T>;

  // Worker badge for teammate permission requests
  workerBadge: WorkerBadgeProps | undefined;
};
export function FilePermissionDialog<T extends ToolInput = ToolInput>({
  toolUseConfirm,
  toolUseContext,

```

---


### `src/components/permissions/FilePermissionDialog/ideDiffConfig.ts`

**信息:**
- 行数: 42
- 大小: 858 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ToolInput } from './useFilePermissionDialog.js'

export interface FileEdit {
  old_string: string
  new_string: string
  replace_all?: boolean
}

export interface IDEDiffConfig {
  filePath: string
  edits?: FileEdit[]
  editMode?: 'single' | 'multiple'
}

export interface IDEDiffChangeInput {
  file_path: string
  edits: FileEdit[]
}

export interface IDEDiffSupport<TInput extends ToolInput> {
  getConfig(input: TInput): IDEDiffConfig
  applyChanges(input: TInput, modifiedEdits: FileEdit[]): TInput
}

export function createSingleEditDiffConfig(
  filePath: string,
  oldString: string,
  newString: string,
  replaceAll?: boolean,
): IDEDiffConfig {
  return {
    filePath,
    edits: [
      {
        old_string: oldString,
        new_string: newString,
        replace_all: replaceAll,
      },
    ],
    editMode: 'single',
  }
}

```

---


### `src/components/permissions/FilePermissionDialog/permissionOptions.tsx`

**信息:**
- 行数: 177
- 大小: 22367 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { homedir } from 'os';
import { basename, join, sep } from 'path';
import React, { type ReactNode } from 'react';
import { getOriginalCwd } from '../../../bootstrap/state.js';
import { Text } from '../../../ink.js';
import { getShortcutDisplay } from '../../../keybindings/shortcutFormat.js';
import type { ToolPermissionContext } from '../../../Tool.js';
import { expandPath, getDirectoryForPath } from '../../../utils/path.js';
import { normalizeCaseForComparison, pathInAllowedWorkingPath } from '../../../utils/permissions/filesystem.js';
import type { OptionWithDescription } from '../../CustomSelect/select.js';
/**
 * Check if a path is within the project's .claude/ folder.
 * This is used to determine whether to show the special ".claude folder" permission option.
 */
export function isInClaudeFolder(filePath: string): boolean {
  const absolutePath = expandPath(filePath);
  const claudeFolderPath = expandPath(`${getOriginalCwd()}/.claude`);

  // Check if the path is within the project's .claude folder
  const normalizedAbsolutePath = normalizeCaseForComparison(absolutePath);
  const normalizedClaudeFolderPath = normalizeCaseForComparison(claudeFolderPath);

  // Path must start with the .claude folder path (and be inside it, not just the folder itself)
  return normalizedAbsolutePath.startsWith(normalizedClaudeFolderPath + sep.toLowerCase()) ||
  // Also match case where sep is / on posix systems
  normalizedAbsolutePath.startsWith(normalizedClaudeFolderPath + '/');
}

/**
 * Check if a path is within the global ~/.claude/ folder.
 * This is used to determine whether to show the special ".claude folder" permission option
 * for files in the user's home directory.
 */
export function isInGlobalClaudeFolder(filePath: string): boolean {
  const absolutePath = expandPath(filePath);
  const globalClaudeFolderPath = join(homedir(), '.claude');
  const normalizedAbsolutePath = normalizeCaseForComparison(absolutePath);
  const normalizedGlobalClaudeFolderPath = normalizeCaseForComparison(globalClaudeFolderPath);
  return normalizedAbsolutePath.startsWith(normalizedGlobalClaudeFolderPath + sep.toLowerCase()) || normalizedAbsolutePath.startsWith(normalizedGlobalClaudeFolderPath + '/');
}
export type PermissionOption = {
  type: 'accept-once';
} | {
  type: 'accept-session';
  scope?: 'claude-folder' | 'global-claude-folder';
} | {
  type: 'reject';
};
export type PermissionOptionWithLabel = OptionWithDescription<string> & {
  option: PermissionOption;

```

---


### `src/components/permissions/FilePermissionDialog/useFilePermissionDialog.ts`

**信息:**
- 行数: 212
- 大小: 6809 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useMemo, useState } from 'react'
import { useAppState } from 'src/state/AppState.js'
import { useKeybindings } from '../../../keybindings/useKeybinding.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../../services/analytics/index.js'
import { sanitizeToolNameForAnalytics } from '../../../services/analytics/metadata.js'
import type { PermissionUpdate } from '../../../utils/permissions/PermissionUpdateSchema.js'
import type { CompletionType } from '../../../utils/unaryLogging.js'
import type { ToolUseConfirm } from '../PermissionRequest.js'
import {
  type FileOperationType,
  getFilePermissionOptions,
  type PermissionOption,
  type PermissionOptionWithLabel,
} from './permissionOptions.js'
import {
  PERMISSION_HANDLERS,
  type PermissionHandlerParams,
} from './usePermissionHandler.js'

export interface ToolInput {
  [key: string]: unknown
}

export type UseFilePermissionDialogProps<T extends ToolInput> = {
  filePath: string
  completionType: CompletionType
  languageName: string | Promise<string>
  toolUseConfirm: ToolUseConfirm
  onDone: () => void
  onReject: () => void
  parseInput: (input: unknown) => T
  operationType?: FileOperationType
}

export type UseFilePermissionDialogResult<T> = {
  options: PermissionOptionWithLabel[]
  onChange: (option: PermissionOption, input: T, feedback?: string) => void
  acceptFeedback: string
  rejectFeedback: string
  focusedOption: string
  setFocusedOption: (option: string) => void
  handleInputModeToggle: (value: string) => void
  yesInputMode: boolean
  noInputMode: boolean
}

/**

```

---


### `src/components/permissions/FilePermissionDialog/usePermissionHandler.ts`

**信息:**
- 行数: 185
- 大小: 5105 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../../services/analytics/index.js'
import { sanitizeToolNameForAnalytics } from '../../../services/analytics/metadata.js'
import type { ToolPermissionContext } from '../../../Tool.js'
import {
  CLAUDE_FOLDER_PERMISSION_PATTERN,
  FILE_EDIT_TOOL_NAME,
  GLOBAL_CLAUDE_FOLDER_PERMISSION_PATTERN,
} from '../../../tools/FileEditTool/constants.js'
import { env } from '../../../utils/env.js'
import { generateSuggestions } from '../../../utils/permissions/filesystem.js'
import type { PermissionUpdate } from '../../../utils/permissions/PermissionUpdateSchema.js'
import {
  type CompletionType,
  logUnaryEvent,
} from '../../../utils/unaryLogging.js'
import type { ToolUseConfirm } from '../PermissionRequest.js'
import type {
  FileOperationType,
  PermissionOption,
} from './permissionOptions.js'

function logPermissionEvent(
  event: 'accept' | 'reject',
  completionType: CompletionType,
  languageName: string | Promise<string>,
  messageId: string,
  hasFeedback?: boolean,
): void {
  void logUnaryEvent({
    completion_type: completionType,
    event,
    metadata: {
      language_name: languageName,
      message_id: messageId,
      platform: env.platform,
      hasFeedback: hasFeedback ?? false,
    },
  })
}

export type PermissionHandlerParams = {
  messageId: string
  path: string | null
  toolUseConfirm: ToolUseConfirm
  toolPermissionContext: ToolPermissionContext
  onDone: () => void
  onReject: () => void

```

---


### `src/components/permissions/FileWritePermissionRequest/FileWritePermissionRequest.tsx`

**信息:**
- 行数: 161
- 大小: 16526 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { basename, relative } from 'path';
import React, { useMemo } from 'react';
import type { z } from 'zod/v4';
import { Text } from '../../../ink.js';
import { FileWriteTool } from '../../../tools/FileWriteTool/FileWriteTool.js';
import { getCwd } from '../../../utils/cwd.js';
import { isENOENT } from '../../../utils/errors.js';
import { readFileSync } from '../../../utils/fileRead.js';
import { FilePermissionDialog } from '../FilePermissionDialog/FilePermissionDialog.js';
import { createSingleEditDiffConfig, type FileEdit, type IDEDiffSupport } from '../FilePermissionDialog/ideDiffConfig.js';
import type { PermissionRequestProps } from '../PermissionRequest.js';
import { FileWriteToolDiff } from './FileWriteToolDiff.js';
type FileWriteToolInput = z.infer<typeof FileWriteTool.inputSchema>;
const ideDiffSupport: IDEDiffSupport<FileWriteToolInput> = {
  getConfig: (input: FileWriteToolInput) => {
    let oldContent: string;
    try {
      oldContent = readFileSync(input.file_path);
    } catch (e) {
      if (!isENOENT(e)) throw e;
      oldContent = '';
    }
    return createSingleEditDiffConfig(input.file_path, oldContent, input.content, false // For file writes, we replace the entire content
    );
  },
  applyChanges: (input: FileWriteToolInput, modifiedEdits: FileEdit[]) => {
    const firstEdit = modifiedEdits[0];
    if (firstEdit) {
      return {
        ...input,
        content: firstEdit.new_string
      };
    }
    return input;
  }
};
export function FileWritePermissionRequest(props) {
  const $ = _c(30);
  const parseInput = _temp;
  let t0;
  if ($[0] !== props.toolUseConfirm.input) {
    t0 = parseInput(props.toolUseConfirm.input);
    $[0] = props.toolUseConfirm.input;
    $[1] = t0;
  } else {
    t0 = $[1];
  }
  const parsed = t0;
  const {

```

---


### `src/components/permissions/FileWritePermissionRequest/FileWriteToolDiff.tsx`

**信息:**
- 行数: 89
- 大小: 9672 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useMemo } from 'react';
import { useTerminalSize } from '../../../hooks/useTerminalSize.js';
import { Box, NoSelect, Text } from '../../../ink.js';
import { intersperse } from '../../../utils/array.js';
import { getPatchForDisplay } from '../../../utils/diff.js';
import { HighlightedCode } from '../../HighlightedCode.js';
import { StructuredDiff } from '../../StructuredDiff.js';
type Props = {
  file_path: string;
  content: string;
  fileExists: boolean;
  oldContent: string;
};
export function FileWriteToolDiff(t0) {
  const $ = _c(15);
  const {
    file_path,
    content,
    fileExists,
    oldContent
  } = t0;
  const {
    columns
  } = useTerminalSize();
  let t1;
  bb0: {
    if (!fileExists) {
      t1 = null;
      break bb0;
    }
    let t2;
    if ($[0] !== content || $[1] !== file_path || $[2] !== oldContent) {
      t2 = getPatchForDisplay({
        filePath: file_path,
        fileContents: oldContent,
        edits: [{
          old_string: oldContent,
          new_string: content,
          replace_all: false
        }]
      });
      $[0] = content;
      $[1] = file_path;
      $[2] = oldContent;
      $[3] = t2;
    } else {
      t2 = $[3];
    }

```

---


### `src/components/permissions/FilesystemPermissionRequest/FilesystemPermissionRequest.tsx`

**信息:**
- 行数: 115
- 大小: 13085 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text, useTheme } from '../../../ink.js';
import { FallbackPermissionRequest } from '../FallbackPermissionRequest.js';
import { FilePermissionDialog } from '../FilePermissionDialog/FilePermissionDialog.js';
import type { ToolInput } from '../FilePermissionDialog/useFilePermissionDialog.js';
import type { PermissionRequestProps, ToolUseConfirm } from '../PermissionRequest.js';
function pathFromToolUse(toolUseConfirm: ToolUseConfirm): string | null {
  const tool = toolUseConfirm.tool;
  if ('getPath' in tool && typeof tool.getPath === 'function') {
    try {
      return tool.getPath(toolUseConfirm.input);
    } catch {
      return null;
    }
  }
  return null;
}
export function FilesystemPermissionRequest(t0) {
  const $ = _c(30);
  const {
    toolUseConfirm,
    onDone,
    onReject,
    verbose,
    toolUseContext,
    workerBadge
  } = t0;
  const [theme] = useTheme();
  let t1;
  if ($[0] !== toolUseConfirm) {
    t1 = pathFromToolUse(toolUseConfirm);
    $[0] = toolUseConfirm;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const path = t1;
  let t2;
  if ($[2] !== toolUseConfirm.input || $[3] !== toolUseConfirm.tool) {
    t2 = toolUseConfirm.tool.userFacingName(toolUseConfirm.input as never);
    $[2] = toolUseConfirm.input;
    $[3] = toolUseConfirm.tool;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  const userFacingName = t2;
  const isReadOnly = toolUseConfirm.tool.isReadOnly(toolUseConfirm.input);
  const userFacingReadOrEdit = isReadOnly ? "Read" : "Edit";

```

---


### `src/components/permissions/MonitorPermissionRequest/MonitorPermissionRequest.tsx`

**信息:**
- 行数: 3
- 大小: 61 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function MonitorPermissionRequest() {
  return null
}

```

---


### `src/components/permissions/NotebookEditPermissionRequest/NotebookEditPermissionRequest.tsx`

**信息:**
- 行数: 166
- 大小: 16494 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { basename } from 'path';
import React from 'react';
import type { z } from 'zod/v4';
import { Text } from '../../../ink.js';
import { NotebookEditTool } from '../../../tools/NotebookEditTool/NotebookEditTool.js';
import { logError } from '../../../utils/log.js';
import { FilePermissionDialog } from '../FilePermissionDialog/FilePermissionDialog.js';
import type { PermissionRequestProps } from '../PermissionRequest.js';
import { NotebookEditToolDiff } from './NotebookEditToolDiff.js';
type NotebookEditInput = z.infer<typeof NotebookEditTool.inputSchema>;
export function NotebookEditPermissionRequest(props) {
  const $ = _c(52);
  const parseInput = _temp;
  let T0;
  let T1;
  let T2;
  let language;
  let notebook_path;
  let parsed;
  let t0;
  let t1;
  let t10;
  let t2;
  let t3;
  let t4;
  let t5;
  let t6;
  let t7;
  let t8;
  let t9;
  if ($[0] !== props.onDone || $[1] !== props.onReject || $[2] !== props.toolUseConfirm || $[3] !== props.toolUseContext || $[4] !== props.workerBadge) {
    parsed = parseInput(props.toolUseConfirm.input);
    const {
      notebook_path: t11,
      edit_mode,
      cell_type
    } = parsed;
    notebook_path = t11;
    language = cell_type === "markdown" ? "markdown" : "python";
    const editTypeText = edit_mode === "insert" ? "insert this cell into" : edit_mode === "delete" ? "delete this cell from" : "make this edit to";
    T2 = FilePermissionDialog;
    t5 = props.toolUseConfirm;
    t6 = props.toolUseContext;
    t7 = props.onDone;
    t8 = props.onReject;
    t9 = props.workerBadge;
    t10 = "Edit notebook";
    T1 = Text;
    t2 = "Do you want to ";

```

---


### `src/components/permissions/NotebookEditPermissionRequest/NotebookEditToolDiff.tsx`

**信息:**
- 行数: 235
- 大小: 24680 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { relative } from 'path';
import * as React from 'react';
import { Suspense, use, useMemo } from 'react';
import { Box, NoSelect, Text } from '../../../ink.js';
import type { NotebookCellType, NotebookContent } from '../../../types/notebook.js';
import { intersperse } from '../../../utils/array.js';
import { getCwd } from '../../../utils/cwd.js';
import { getPatchForDisplay } from '../../../utils/diff.js';
import { getFsImplementation } from '../../../utils/fsOperations.js';
import { safeParseJSON } from '../../../utils/json.js';
import { parseCellId } from '../../../utils/notebook.js';
import { HighlightedCode } from '../../HighlightedCode.js';
import { StructuredDiff } from '../../StructuredDiff.js';
type Props = {
  notebook_path: string;
  cell_id: string | undefined;
  new_source: string;
  cell_type?: NotebookCellType;
  edit_mode?: string;
  verbose: boolean;
  width: number;
};
type InnerProps = {
  notebook_path: string;
  cell_id: string | undefined;
  new_source: string;
  cell_type?: NotebookCellType;
  edit_mode?: string;
  verbose: boolean;
  width: number;
  promise: Promise<NotebookContent | null>;
};
export function NotebookEditToolDiff(props) {
  const $ = _c(5);
  let t0;
  if ($[0] !== props.notebook_path) {
    t0 = getFsImplementation().readFile(props.notebook_path, {
      encoding: "utf-8"
    }).then(_temp).catch(_temp2);
    $[0] = props.notebook_path;
    $[1] = t0;
  } else {
    t0 = $[1];
  }
  const notebookDataPromise = t0;
  let t1;
  if ($[2] !== notebookDataPromise || $[3] !== props) {
    t1 = <Suspense fallback={null}><NotebookEditToolDiffInner {...props} promise={notebookDataPromise} /></Suspense>;
    $[2] = notebookDataPromise;

```

---


### `src/components/permissions/PermissionDecisionDebugInfo.tsx`

**信息:**
- 行数: 460
- 大小: 52533 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import chalk from 'chalk';
import figures from 'figures';
import React, { useMemo } from 'react';
import { Ansi, Box, color, Text, useTheme } from '../../ink.js';
import { useAppState } from '../../state/AppState.js';
import type { PermissionMode } from '../../utils/permissions/PermissionMode.js';
import { permissionModeTitle } from '../../utils/permissions/PermissionMode.js';
import type { PermissionDecision, PermissionDecisionReason } from '../../utils/permissions/PermissionResult.js';
import { extractRules } from '../../utils/permissions/PermissionUpdate.js';
import type { PermissionUpdate } from '../../utils/permissions/PermissionUpdateSchema.js';
import { permissionRuleValueToString } from '../../utils/permissions/permissionRuleParser.js';
import { detectUnreachableRules } from '../../utils/permissions/shadowedRuleDetection.js';
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js';
import { getSettingSourceDisplayNameLowercase } from '../../utils/settings/constants.js';
type PermissionDecisionInfoItemProps = {
  title?: string;
  decisionReason: PermissionDecisionReason;
};
function decisionReasonDisplayString(decisionReason: PermissionDecisionReason & {
  type: Exclude<PermissionDecisionReason['type'], 'subcommandResults'>;
}): string {
  if ((feature('BASH_CLASSIFIER') || feature('TRANSCRIPT_CLASSIFIER')) && decisionReason.type === 'classifier') {
    return `${chalk.bold(decisionReason.classifier)} classifier: ${decisionReason.reason}`;
  }
  switch (decisionReason.type) {
    case 'rule':
      return `${chalk.bold(permissionRuleValueToString(decisionReason.rule.ruleValue))} rule from ${getSettingSourceDisplayNameLowercase(decisionReason.rule.source)}`;
    case 'mode':
      return `${permissionModeTitle(decisionReason.mode)} mode`;
    case 'sandboxOverride':
      return 'Requires permission to bypass sandbox';
    case 'workingDir':
      return decisionReason.reason;
    case 'safetyCheck':
    case 'other':
      return decisionReason.reason;
    case 'permissionPromptTool':
      return `${chalk.bold(decisionReason.permissionPromptToolName)} permission prompt tool`;
    case 'hook':
      return decisionReason.reason ? `${chalk.bold(decisionReason.hookName)} hook: ${decisionReason.reason}` : `${chalk.bold(decisionReason.hookName)} hook`;
    case 'asyncAgent':
      return decisionReason.reason;
    default:
      return '';
  }
}
function PermissionDecisionInfoItem(t0) {
  const $ = _c(10);

```

---


### `src/components/permissions/PermissionDialog.tsx`

**信息:**
- 行数: 72
- 大小: 7317 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box } from '../../ink.js';
import type { Theme } from '../../utils/theme.js';
import { PermissionRequestTitle } from './PermissionRequestTitle.js';
import type { WorkerBadgeProps } from './WorkerBadge.js';
type Props = {
  title: string;
  subtitle?: React.ReactNode;
  color?: keyof Theme;
  titleColor?: keyof Theme;
  innerPaddingX?: number;
  workerBadge?: WorkerBadgeProps;
  titleRight?: React.ReactNode;
  children: React.ReactNode;
};
export function PermissionDialog(t0) {
  const $ = _c(15);
  const {
    title,
    subtitle,
    color: t1,
    titleColor,
    innerPaddingX: t2,
    workerBadge,
    titleRight,
    children
  } = t0;
  const color = t1 === undefined ? "permission" : t1;
  const innerPaddingX = t2 === undefined ? 1 : t2;
  let t3;
  if ($[0] !== subtitle || $[1] !== title || $[2] !== titleColor || $[3] !== workerBadge) {
    t3 = <PermissionRequestTitle title={title} subtitle={subtitle} color={titleColor} workerBadge={workerBadge} />;
    $[0] = subtitle;
    $[1] = title;
    $[2] = titleColor;
    $[3] = workerBadge;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  let t4;
  if ($[5] !== t3 || $[6] !== titleRight) {
    t4 = <Box paddingX={1} flexDirection="column"><Box justifyContent="space-between">{t3}{titleRight}</Box></Box>;
    $[5] = t3;
    $[6] = titleRight;
    $[7] = t4;
  } else {
    t4 = $[7];
  }

```

---


### `src/components/permissions/PermissionExplanation.tsx`

**信息:**
- 行数: 272
- 大小: 23700 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { Suspense, use, useState } from 'react';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { logEvent } from '../../services/analytics/index.js';
import type { Message } from '../../types/message.js';
import { generatePermissionExplanation, isPermissionExplainerEnabled, type PermissionExplanation as PermissionExplanationType, type RiskLevel } from '../../utils/permissions/permissionExplainer.js';
import { ShimmerChar } from '../Spinner/ShimmerChar.js';
import { useShimmerAnimation } from '../Spinner/useShimmerAnimation.js';
const LOADING_MESSAGE = 'Loading explanation…';
function ShimmerLoadingText() {
  const $ = _c(7);
  const [ref, glimmerIndex] = useShimmerAnimation("responding", LOADING_MESSAGE, false);
  let t0;
  if ($[0] !== glimmerIndex) {
    t0 = LOADING_MESSAGE.split("").map((char, index) => <ShimmerChar key={index} char={char} index={index} glimmerIndex={glimmerIndex} messageColor="inactive" shimmerColor="text" />);
    $[0] = glimmerIndex;
    $[1] = t0;
  } else {
    t0 = $[1];
  }
  let t1;
  if ($[2] !== t0) {
    t1 = <Text>{t0}</Text>;
    $[2] = t0;
    $[3] = t1;
  } else {
    t1 = $[3];
  }
  let t2;
  if ($[4] !== ref || $[5] !== t1) {
    t2 = <Box ref={ref}>{t1}</Box>;
    $[4] = ref;
    $[5] = t1;
    $[6] = t2;
  } else {
    t2 = $[6];
  }
  return t2;
}
function getRiskColor(riskLevel: RiskLevel): 'success' | 'warning' | 'error' {
  switch (riskLevel) {
    case 'LOW':
      return 'success';
    case 'MEDIUM':
      return 'warning';
    case 'HIGH':
      return 'error';
  }
}

```

---


### `src/components/permissions/PermissionPrompt.tsx`

**信息:**
- 行数: 336
- 大小: 37391 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode, useCallback, useMemo, useState } from 'react';
import { Box, Text } from '../../ink.js';
import type { KeybindingAction } from '../../keybindings/types.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../services/analytics/index.js';
import { useSetAppState } from '../../state/AppState.js';
import { type OptionWithDescription, Select } from '../CustomSelect/select.js';
export type FeedbackType = 'accept' | 'reject';
export type PermissionPromptOption<T extends string> = {
  value: T;
  label: ReactNode;
  feedbackConfig?: {
    type: FeedbackType;
    placeholder?: string;
  };
  keybinding?: KeybindingAction;
};
export type ToolAnalyticsContext = {
  toolName: string;
  isMcp: boolean;
};
export type PermissionPromptProps<T extends string> = {
  options: PermissionPromptOption<T>[];
  onSelect: (value: T, feedback?: string) => void;
  onCancel?: () => void;
  question?: string | ReactNode;
  toolAnalyticsContext?: ToolAnalyticsContext;
};
const DEFAULT_PLACEHOLDERS: Record<FeedbackType, string> = {
  accept: 'tell Claude what to do next',
  reject: 'tell Claude what to do differently'
};

/**
 * Shared component for permission prompts with optional feedback input.
 *
 * Handles:
 * - "Do you want to proceed?" question with optional Tab hint
 * - Feature flag check for feedback capability
 * - Input mode toggling (Tab to expand feedback input)
 * - Analytics events for feedback interactions
 * - Transforming options to Select-compatible format
 */
export function PermissionPrompt(t0) {
  const $ = _c(54);
  const {
    options,
    onSelect,
    onCancel,

```

---


### `src/components/permissions/PermissionRequest.tsx`

**信息:**
- 行数: 217
- 大小: 33579 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import * as React from 'react';
import { EnterPlanModeTool } from 'src/tools/EnterPlanModeTool/EnterPlanModeTool.js';
import { ExitPlanModeV2Tool } from 'src/tools/ExitPlanModeTool/ExitPlanModeV2Tool.js';
import { useNotifyAfterTimeout } from '../../hooks/useNotifyAfterTimeout.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import type { AnyObject, Tool, ToolUseContext } from '../../Tool.js';
import { AskUserQuestionTool } from '../../tools/AskUserQuestionTool/AskUserQuestionTool.js';
import { BashTool } from '../../tools/BashTool/BashTool.js';
import { FileEditTool } from '../../tools/FileEditTool/FileEditTool.js';
import { FileReadTool } from '../../tools/FileReadTool/FileReadTool.js';
import { FileWriteTool } from '../../tools/FileWriteTool/FileWriteTool.js';
import { GlobTool } from '../../tools/GlobTool/GlobTool.js';
import { GrepTool } from '../../tools/GrepTool/GrepTool.js';
import { NotebookEditTool } from '../../tools/NotebookEditTool/NotebookEditTool.js';
import { PowerShellTool } from '../../tools/PowerShellTool/PowerShellTool.js';
import { SkillTool } from '../../tools/SkillTool/SkillTool.js';
import { WebFetchTool } from '../../tools/WebFetchTool/WebFetchTool.js';
import type { AssistantMessage } from '../../types/message.js';
import type { PermissionDecision } from '../../utils/permissions/PermissionResult.js';
import { AskUserQuestionPermissionRequest } from './AskUserQuestionPermissionRequest/AskUserQuestionPermissionRequest.js';
import { BashPermissionRequest } from './BashPermissionRequest/BashPermissionRequest.js';
import { EnterPlanModePermissionRequest } from './EnterPlanModePermissionRequest/EnterPlanModePermissionRequest.js';
import { ExitPlanModePermissionRequest } from './ExitPlanModePermissionRequest/ExitPlanModePermissionRequest.js';
import { FallbackPermissionRequest } from './FallbackPermissionRequest.js';
import { FileEditPermissionRequest } from './FileEditPermissionRequest/FileEditPermissionRequest.js';
import { FilesystemPermissionRequest } from './FilesystemPermissionRequest/FilesystemPermissionRequest.js';
import { FileWritePermissionRequest } from './FileWritePermissionRequest/FileWritePermissionRequest.js';
import { NotebookEditPermissionRequest } from './NotebookEditPermissionRequest/NotebookEditPermissionRequest.js';
import { PowerShellPermissionRequest } from './PowerShellPermissionRequest/PowerShellPermissionRequest.js';
import { SkillPermissionRequest } from './SkillPermissionRequest/SkillPermissionRequest.js';
import { WebFetchPermissionRequest } from './WebFetchPermissionRequest/WebFetchPermissionRequest.js';

/* eslint-disable @typescript-eslint/no-require-imports */
const ReviewArtifactTool = feature('REVIEW_ARTIFACT') ? (require('../../tools/ReviewArtifactTool/ReviewArtifactTool.js') as typeof import('../../tools/ReviewArtifactTool/ReviewArtifactTool.js')).ReviewArtifactTool : null;
const ReviewArtifactPermissionRequest = feature('REVIEW_ARTIFACT') ? (require('./ReviewArtifactPermissionRequest/ReviewArtifactPermissionRequest.js') as typeof import('./ReviewArtifactPermissionRequest/ReviewArtifactPermissionRequest.js')).ReviewArtifactPermissionRequest : null;
const WorkflowTool = feature('WORKFLOW_SCRIPTS') ? (require('../../tools/WorkflowTool/WorkflowTool.js') as typeof import('../../tools/WorkflowTool/WorkflowTool.js')).WorkflowTool : null;
const WorkflowPermissionRequest = feature('WORKFLOW_SCRIPTS') ? (require('../../tools/WorkflowTool/WorkflowPermissionRequest.js') as typeof import('../../tools/WorkflowTool/WorkflowPermissionRequest.js')).WorkflowPermissionRequest : null;
const MonitorTool = feature('MONITOR_TOOL') ? (require('../../tools/MonitorTool/MonitorTool.js') as typeof import('../../tools/MonitorTool/MonitorTool.js')).MonitorTool : null;
const MonitorPermissionRequest = feature('MONITOR_TOOL') ? (require('./MonitorPermissionRequest/MonitorPermissionRequest.js') as typeof import('./MonitorPermissionRequest/MonitorPermissionRequest.js')).MonitorPermissionRequest : null;
import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/messages.mjs';
/* eslint-enable @typescript-eslint/no-require-imports */
import type { z } from 'zod/v4';
import type { PermissionUpdate } from '../../utils/permissions/PermissionUpdateSchema.js';
import type { WorkerBadgeProps } from './WorkerBadge.js';
function permissionComponentForTool(tool: Tool): React.ComponentType<PermissionRequestProps> {
  switch (tool) {
    case FileEditTool:
      return FileEditPermissionRequest;

```

---


### `src/components/permissions/PermissionRequestTitle.tsx`

**信息:**
- 行数: 66
- 大小: 5781 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import type { Theme } from '../../utils/theme.js';
import type { WorkerBadgeProps } from './WorkerBadge.js';
type Props = {
  title: string;
  subtitle?: React.ReactNode;
  color?: keyof Theme;
  workerBadge?: WorkerBadgeProps;
};
export function PermissionRequestTitle(t0) {
  const $ = _c(13);
  const {
    title,
    subtitle,
    color: t1,
    workerBadge
  } = t0;
  const color = t1 === undefined ? "permission" : t1;
  let t2;
  if ($[0] !== color || $[1] !== title) {
    t2 = <Text bold={true} color={color}>{title}</Text>;
    $[0] = color;
    $[1] = title;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  let t3;
  if ($[3] !== workerBadge) {
    t3 = workerBadge && <Text dimColor={true}>{"\xB7 "}@{workerBadge.name}</Text>;
    $[3] = workerBadge;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  let t4;
  if ($[5] !== t2 || $[6] !== t3) {
    t4 = <Box flexDirection="row" gap={1}>{t2}{t3}</Box>;
    $[5] = t2;
    $[6] = t3;
    $[7] = t4;
  } else {
    t4 = $[7];
  }
  let t5;
  if ($[8] !== subtitle) {
    t5 = subtitle != null && (typeof subtitle === "string" ? <Text dimColor={true} wrap="truncate-start">{subtitle}</Text> : subtitle);
    $[8] = subtitle;

```

---


### `src/components/permissions/PermissionRuleExplanation.tsx`

**信息:**
- 行数: 121
- 大小: 14921 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import chalk from 'chalk';
import React from 'react';
import { Ansi, Box, Text } from '../../ink.js';
import { useAppState } from '../../state/AppState.js';
import type { PermissionDecision, PermissionDecisionReason } from '../../utils/permissions/PermissionResult.js';
import { permissionRuleValueToString } from '../../utils/permissions/permissionRuleParser.js';
import type { Theme } from '../../utils/theme.js';
import ThemedText from '../design-system/ThemedText.js';
export type PermissionRuleExplanationProps = {
  permissionResult: PermissionDecision;
  toolType: 'tool' | 'command' | 'edit' | 'read';
};
type DecisionReasonStrings = {
  reasonString: string;
  configString?: string;
  /** When set, reasonString is plain text rendered with this theme color instead of <Ansi>. */
  themeColor?: keyof Theme;
};
function stringsForDecisionReason(reason: PermissionDecisionReason | undefined, toolType: 'tool' | 'command' | 'edit' | 'read'): DecisionReasonStrings | null {
  if (!reason) {
    return null;
  }
  if ((feature('BASH_CLASSIFIER') || feature('TRANSCRIPT_CLASSIFIER')) && reason.type === 'classifier') {
    if (reason.classifier === 'auto-mode') {
      return {
        reasonString: `Auto mode classifier requires confirmation for this ${toolType}.\n${reason.reason}`,
        configString: undefined,
        themeColor: 'error'
      };
    }
    return {
      reasonString: `Classifier ${chalk.bold(reason.classifier)} requires confirmation for this ${toolType}.\n${reason.reason}`,
      configString: undefined
    };
  }
  switch (reason.type) {
    case 'rule':
      return {
        reasonString: `Permission rule ${chalk.bold(permissionRuleValueToString(reason.rule.ruleValue))} requires confirmation for this ${toolType}.`,
        configString: reason.rule.source === 'policySettings' ? undefined : '/permissions to update rules'
      };
    case 'hook':
      {
        const hookReasonString = reason.reason ? `:\n${reason.reason}` : '.';
        const sourceLabel = reason.hookSource ? ` ${chalk.dim(`[${reason.hookSource}]`)}` : '';
        return {
          reasonString: `Hook ${chalk.bold(reason.hookName)} requires confirmation for this ${toolType}${hookReasonString}${sourceLabel}`,
          configString: '/hooks to update'

```

---


### `src/components/permissions/PowerShellPermissionRequest/PowerShellPermissionRequest.tsx`

**信息:**
- 行数: 235
- 大小: 38696 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Box, Text, useTheme } from '../../../ink.js';
import { useKeybinding } from '../../../keybindings/useKeybinding.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../../services/analytics/growthbook.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../../services/analytics/index.js';
import { sanitizeToolNameForAnalytics } from '../../../services/analytics/metadata.js';
import { getDestructiveCommandWarning } from '../../../tools/PowerShellTool/destructiveCommandWarning.js';
import { PowerShellTool } from '../../../tools/PowerShellTool/PowerShellTool.js';
import { isAllowlistedCommand } from '../../../tools/PowerShellTool/readOnlyValidation.js';
import type { PermissionUpdate } from '../../../utils/permissions/PermissionUpdateSchema.js';
import { getCompoundCommandPrefixesStatic } from '../../../utils/powershell/staticPrefix.js';
import { Select } from '../../CustomSelect/select.js';
import { type UnaryEvent, usePermissionRequestLogging } from '../hooks.js';
import { PermissionDecisionDebugInfo } from '../PermissionDecisionDebugInfo.js';
import { PermissionDialog } from '../PermissionDialog.js';
import { PermissionExplainerContent, usePermissionExplainerUI } from '../PermissionExplanation.js';
import type { PermissionRequestProps } from '../PermissionRequest.js';
import { PermissionRuleExplanation } from '../PermissionRuleExplanation.js';
import { useShellPermissionFeedback } from '../useShellPermissionFeedback.js';
import { logUnaryPermissionEvent } from '../utils.js';
import { powershellToolUseOptions } from './powershellToolUseOptions.js';
export function PowerShellPermissionRequest(props: PermissionRequestProps): React.ReactNode {
  const {
    toolUseConfirm,
    toolUseContext,
    onDone,
    onReject,
    workerBadge
  } = props;
  const {
    command,
    description
  } = PowerShellTool.inputSchema.parse(toolUseConfirm.input);
  const [theme] = useTheme();
  const explainerState = usePermissionExplainerUI({
    toolName: toolUseConfirm.tool.name,
    toolInput: toolUseConfirm.input,
    toolDescription: toolUseConfirm.description,
    messages: toolUseContext.messages
  });
  const {
    yesInputMode,
    noInputMode,
    yesFeedbackModeEntered,
    noFeedbackModeEntered,
    acceptFeedback,
    rejectFeedback,
    setAcceptFeedback,
    setRejectFeedback,
    focusedOption,

```

---


### `src/components/permissions/PowerShellPermissionRequest/powershellToolUseOptions.tsx`

**信息:**
- 行数: 91
- 大小: 11950 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { POWERSHELL_TOOL_NAME } from '../../../tools/PowerShellTool/toolName.js';
import type { PermissionUpdate } from '../../../utils/permissions/PermissionUpdateSchema.js';
import { shouldShowAlwaysAllowOptions } from '../../../utils/permissions/permissionsLoader.js';
import type { OptionWithDescription } from '../../CustomSelect/select.js';
import { generateShellSuggestionsLabel } from '../shellPermissionHelpers.js';
export type PowerShellToolUseOption = 'yes' | 'yes-apply-suggestions' | 'yes-prefix-edited' | 'no';
export function powershellToolUseOptions({
  suggestions = [],
  onRejectFeedbackChange,
  onAcceptFeedbackChange,
  yesInputMode = false,
  noInputMode = false,
  editablePrefix,
  onEditablePrefixChange
}: {
  suggestions?: PermissionUpdate[];
  onRejectFeedbackChange: (value: string) => void;
  onAcceptFeedbackChange: (value: string) => void;
  yesInputMode?: boolean;
  noInputMode?: boolean;
  editablePrefix?: string;
  onEditablePrefixChange?: (value: string) => void;
}): OptionWithDescription<PowerShellToolUseOption>[] {
  const options: OptionWithDescription<PowerShellToolUseOption>[] = [];
  if (yesInputMode) {
    options.push({
      type: 'input',
      label: 'Yes',
      value: 'yes',
      placeholder: 'and tell Claude what to do next',
      onChange: onAcceptFeedbackChange,
      allowEmptySubmitToCancel: true
    });
  } else {
    options.push({
      label: 'Yes',
      value: 'yes'
    });
  }

  // Note: No sandbox toggle for PowerShell - sandbox is not supported on Windows
  // Note: No classifier-reviewed option for PowerShell (ANT-ONLY feature for Bash)

  // Only show "always allow" options when not restricted by allowManagedPermissionRulesOnly.
  // Prefer the editable prefix input (static extractor + user edits) over the
  // non-editable suggestions label. The editable input can't represent
  // directory permissions or Read-tool rules, so fall back to the label when
  // those are present.
  if (shouldShowAlwaysAllowOptions() && suggestions.length > 0) {
    const hasNonPowerShellSuggestions = suggestions.some(s => s.type === 'addDirectories' || s.type === 'addRules' && s.rules?.some(r => r.toolName !== POWERSHELL_TOOL_NAME));

```

---


### `src/components/permissions/ReviewArtifactPermissionRequest/ReviewArtifactPermissionRequest.tsx`

**信息:**
- 行数: 3
- 大小: 68 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function ReviewArtifactPermissionRequest() {
  return null
}

```

---


### `src/components/permissions/SandboxPermissionRequest.tsx`

**信息:**
- 行数: 163
- 大小: 14272 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from 'src/ink.js';
import { type NetworkHostPattern, shouldAllowManagedSandboxDomainsOnly } from 'src/utils/sandbox/sandbox-adapter.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../services/analytics/index.js';
import { Select } from '../CustomSelect/select.js';
import { PermissionDialog } from './PermissionDialog.js';
export type SandboxPermissionRequestProps = {
  hostPattern: NetworkHostPattern;
  onUserResponse: (response: {
    allow: boolean;
    persistToSettings: boolean;
  }) => void;
};
export function SandboxPermissionRequest(t0) {
  const $ = _c(22);
  const {
    hostPattern: t1,
    onUserResponse
  } = t0;
  const {
    host
  } = t1;
  let t2;
  if ($[0] !== onUserResponse) {
    t2 = function onSelect(value) {
      bb4: switch (value) {
        case "yes":
          {
            onUserResponse({
              allow: true,
              persistToSettings: false
            });
            break bb4;
          }
        case "yes-dont-ask-again":
          {
            onUserResponse({
              allow: true,
              persistToSettings: true
            });
            break bb4;
          }
        case "no":
          {
            onUserResponse({
              allow: false,
              persistToSettings: false
            });
          }

```

---


### `src/components/permissions/SedEditPermissionRequest/SedEditPermissionRequest.tsx`

**信息:**
- 行数: 230
- 大小: 20862 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { basename, relative } from 'path';
import React, { Suspense, use, useMemo } from 'react';
import { FileEditToolDiff } from 'src/components/FileEditToolDiff.js';
import { getCwd } from 'src/utils/cwd.js';
import { isENOENT } from 'src/utils/errors.js';
import { detectEncodingForResolvedPath } from 'src/utils/fileRead.js';
import { getFsImplementation } from 'src/utils/fsOperations.js';
import { Text } from '../../../ink.js';
import { BashTool } from '../../../tools/BashTool/BashTool.js';
import { applySedSubstitution, type SedEditInfo } from '../../../tools/BashTool/sedEditParser.js';
import { FilePermissionDialog } from '../FilePermissionDialog/FilePermissionDialog.js';
import type { PermissionRequestProps } from '../PermissionRequest.js';
type SedEditPermissionRequestProps = PermissionRequestProps & {
  sedInfo: SedEditInfo;
};
type FileReadResult = {
  oldContent: string;
  fileExists: boolean;
};
export function SedEditPermissionRequest(t0) {
  const $ = _c(9);
  let props;
  let sedInfo;
  if ($[0] !== t0) {
    ({
      sedInfo,
      ...props
    } = t0);
    $[0] = t0;
    $[1] = props;
    $[2] = sedInfo;
  } else {
    props = $[1];
    sedInfo = $[2];
  }
  const {
    filePath
  } = sedInfo;
  let t1;
  if ($[3] !== filePath) {
    t1 = (async () => {
      const encoding = detectEncodingForResolvedPath(filePath);
      const raw = await getFsImplementation().readFile(filePath, {
        encoding
      });
      return {
        oldContent: raw.replaceAll("\r\n", "\n"),
        fileExists: true
      };

```

---


### `src/components/permissions/SkillPermissionRequest/SkillPermissionRequest.tsx`

**信息:**
- 行数: 369
- 大小: 36531 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useCallback, useMemo } from 'react';
import { logError } from 'src/utils/log.js';
import { getOriginalCwd } from '../../../bootstrap/state.js';
import { Box, Text } from '../../../ink.js';
import { sanitizeToolNameForAnalytics } from '../../../services/analytics/metadata.js';
import { SKILL_TOOL_NAME } from '../../../tools/SkillTool/constants.js';
import { SkillTool } from '../../../tools/SkillTool/SkillTool.js';
import { env } from '../../../utils/env.js';
import { shouldShowAlwaysAllowOptions } from '../../../utils/permissions/permissionsLoader.js';
import { logUnaryEvent } from '../../../utils/unaryLogging.js';
import { type UnaryEvent, usePermissionRequestLogging } from '../hooks.js';
import { PermissionDialog } from '../PermissionDialog.js';
import { PermissionPrompt, type PermissionPromptOption, type ToolAnalyticsContext } from '../PermissionPrompt.js';
import type { PermissionRequestProps } from '../PermissionRequest.js';
import { PermissionRuleExplanation } from '../PermissionRuleExplanation.js';
type SkillOptionValue = 'yes' | 'yes-exact' | 'yes-prefix' | 'no';
export function SkillPermissionRequest(props) {
  const $ = _c(51);
  const {
    toolUseConfirm,
    onDone,
    onReject,
    workerBadge
  } = props;
  const parseInput = _temp;
  let t0;
  if ($[0] !== toolUseConfirm.input) {
    t0 = parseInput(toolUseConfirm.input);
    $[0] = toolUseConfirm.input;
    $[1] = t0;
  } else {
    t0 = $[1];
  }
  const skill = t0;
  const commandObj = toolUseConfirm.permissionResult.behavior === "ask" && toolUseConfirm.permissionResult.metadata && "command" in toolUseConfirm.permissionResult.metadata ? toolUseConfirm.permissionResult.metadata.command : undefined;
  let t1;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = {
      completion_type: "tool_use_single",
      language_name: "none"
    };
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  const unaryEvent = t1;
  usePermissionRequestLogging(toolUseConfirm, unaryEvent);
  let t2;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {

```

---


### `src/components/permissions/WebFetchPermissionRequest/WebFetchPermissionRequest.tsx`

**信息:**
- 行数: 258
- 大小: 22888 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useMemo } from 'react';
import { Box, Text, useTheme } from '../../../ink.js';
import { WebFetchTool } from '../../../tools/WebFetchTool/WebFetchTool.js';
import { shouldShowAlwaysAllowOptions } from '../../../utils/permissions/permissionsLoader.js';
import { type OptionWithDescription, Select } from '../../CustomSelect/select.js';
import { type UnaryEvent, usePermissionRequestLogging } from '../hooks.js';
import { PermissionDialog } from '../PermissionDialog.js';
import type { PermissionRequestProps } from '../PermissionRequest.js';
import { PermissionRuleExplanation } from '../PermissionRuleExplanation.js';
import { logUnaryPermissionEvent } from '../utils.js';
function inputToPermissionRuleContent(input: {
  [k: string]: unknown;
}): string {
  try {
    const parsedInput = WebFetchTool.inputSchema.safeParse(input);
    if (!parsedInput.success) {
      return `input:${input.toString()}`;
    }
    const {
      url
    } = parsedInput.data;
    const hostname = new URL(url).hostname;
    return `domain:${hostname}`;
  } catch {
    return `input:${input.toString()}`;
  }
}
export function WebFetchPermissionRequest(t0) {
  const $ = _c(41);
  const {
    toolUseConfirm,
    onDone,
    onReject,
    verbose,
    workerBadge
  } = t0;
  const [theme] = useTheme();
  const {
    url
  } = toolUseConfirm.input as {
    url: string;
  };
  let t1;
  if ($[0] !== url) {
    t1 = new URL(url);
    $[0] = url;
    $[1] = t1;
  } else {
    t1 = $[1];

```

---


### `src/components/permissions/WorkerBadge.tsx`

**信息:**
- 行数: 49
- 大小: 3850 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { BLACK_CIRCLE } from '../../constants/figures.js';
import { Box, Text } from '../../ink.js';
import { toInkColor } from '../../utils/ink.js';
export type WorkerBadgeProps = {
  name: string;
  color: string;
};

/**
 * Renders a colored badge showing the worker's name for permission prompts.
 * Used to indicate which swarm worker is requesting the permission.
 */
export function WorkerBadge(t0) {
  const $ = _c(7);
  const {
    name,
    color
  } = t0;
  let t1;
  if ($[0] !== color) {
    t1 = toInkColor(color);
    $[0] = color;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const inkColor = t1;
  let t2;
  if ($[2] !== name) {
    t2 = <Text bold={true}>@{name}</Text>;
    $[2] = name;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  let t3;
  if ($[4] !== inkColor || $[5] !== t2) {
    t3 = <Box flexDirection="row" gap={1}><Text color={inkColor}>{BLACK_CIRCLE} {t2}</Text></Box>;
    $[4] = inkColor;
    $[5] = t2;
    $[6] = t3;
  } else {
    t3 = $[6];
  }
  return t3;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJMQUNLX0NJUkNMRSIsIkJveCIsIlRleHQiLCJ0b0lua0NvbG9yIiwiV29ya2VyQmFkZ2VQcm9wcyIsIm5hbWUiLCJjb2xvciIsIldvcmtlckJhZGdlIiwidDAiLCIkIiwiX2MiLCJ0MSIsImlua0NvbG9yIiwidDIiLCJ0MyJdLCJzb3VyY2VzIjpbIldvcmtlckJhZGdlLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IEJMQUNLX0NJUkNMRSB9IGZyb20gJy4uLy4uL2NvbnN0YW50cy9maWd1cmVzLmpzJ1xuaW1wb3J0IHsgQm94LCBUZXh0IH0gZnJvbSAnLi4vLi4vaW5rLmpzJ1xuaW1wb3J0IHsgdG9JbmtDb2xvciB9IGZyb20gJy4uLy4uL3V0aWxzL2luay5qcydcblxuZXhwb3J0IHR5cGUgV29ya2VyQmFkZ2VQcm9wcyA9IHtcbiAgbmFtZTogc3RyaW5nXG4gIGNvbG9yOiBzdHJpbmdcbn1cblxuLyoqXG4gKiBSZW5kZXJzIGEgY29sb3JlZCBiYWRnZSBzaG93aW5nIHRoZSB3b3JrZXIncyBuYW1lIGZvciBwZXJtaXNzaW9uIHByb21wdHMuXG4gKiBVc2VkIHRvIGluZGljYXRlIHdoaWNoIHN3YXJtIHdvcmtlciBpcyByZXF1ZXN0aW5nIHRoZSBwZXJtaXNzaW9uLlxuICovXG5leHBvcnQgZnVuY3Rpb24gV29ya2VyQmFkZ2Uoe1xuICBuYW1lLFxuICBjb2xvcixcbn06IFdvcmtlckJhZGdlUHJvcHMpOiBSZWFjdC5SZWFjdE5vZGUge1xuICBjb25zdCBpbmtDb2xvciA9IHRvSW5rQ29sb3IoY29sb3IpXG4gIHJldHVybiAoXG4gICAgPEJveCBmbGV4RGlyZWN0aW9uPVwicm93XCIgZ2FwPXsxfT5cbiAgICAgIDxUZXh0IGNvbG9yPXtpbmtDb2xvcn0+XG4gICAgICAgIHtCTEFDS19DSVJDTEV9IDxUZXh0IGJvbGQ+QHtuYW1lfTwvVGV4dD5cbiAgICAgIDwvVGV4dD5cbiAgICA8L0JveD5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiO0FBQUEsT0FBTyxLQUFLQSxLQUFLLE1BQU0sT0FBTztBQUM5QixTQUFTQyxZQUFZLFFBQVEsNEJBQTRCO0FBQ3pELFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxRQUFRLGNBQWM7QUFDeEMsU0FBU0MsVUFBVSxRQUFRLG9CQUFvQjtBQUUvQyxPQUFPLEtBQUtDLGdCQUFnQixHQUFHO0VBQzdCQyxJQUFJLEVBQUUsTUFBTTtFQUNaQyxLQUFLLEVBQUUsTUFBTTtBQUNmLENBQUM7O0FBRUQ7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPLFNBQUFDLFlBQUFDLEVBQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFBcUI7SUFBQUwsSUFBQTtJQUFBQztFQUFBLElBQUFFLEVBR1Q7RUFBQSxJQUFBRyxFQUFBO0VBQUEsSUFBQUYsQ0FBQSxRQUFBSCxLQUFBO0lBQ0FLLEVBQUEsR0FBQVIsVUFBVSxDQUFDRyxLQUFLLENBQUM7SUFBQUcsQ0FBQSxNQUFBSCxLQUFBO0lBQUFHLENBQUEsTUFBQUUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUYsQ0FBQTtFQUFBO0VBQWxDLE1BQUFHLFFBQUEsR0FBaUJELEVBQWlCO0VBQUEsSUFBQUUsRUFBQTtFQUFBLElBQUFKLENBQUEsUUFBQUosSUFBQTtJQUliUSxFQUFBLElBQUMsSUFBSSxDQUFDLElBQUksQ0FBSixLQUFHLENBQUMsQ0FBQyxDQUFFUixLQUFHLENBQUUsRUFBakIsSUFBSSxDQUFvQjtJQUFBSSxDQUFBLE1BQUFKLElBQUE7SUFBQUksQ0FBQSxNQUFBSSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBSixDQUFBO0VBQUE7RUFBQSxJQUFBSyxFQUFBO0VBQUEsSUFBQUwsQ0FBQSxRQUFBRyxRQUFBLElBQUFILENBQUEsUUFBQUksRUFBQTtJQUY1Q0MsRUFBQSxJQUFDLEdBQUcsQ0FBZSxhQUFLLENBQUwsS0FBSyxDQUFNLEdBQUMsQ0FBRCxHQUFDLENBQzdCLENBQUMsSUFBSSxDQUFRRixLQUFRLENBQVJBLFNBQU8sQ0FBQyxDQUNsQlosYUFBVyxDQUFFLENBQUMsQ0FBQWEsRUFBd0IsQ0FDekMsRUFGQyxJQUFJLENBR1AsRUFKQyxHQUFHLENBSUU7SUFBQUosQ0FBQSxNQUFBRyxRQUFBO0lBQUFILENBQUEsTUFBQUksRUFBQTtJQUFBSixDQUFBLE1BQUFLLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFMLENBQUE7RUFBQTtFQUFBLE9BSk5LLEVBSU07QUFBQSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/components/permissions/WorkerPendingPermission.tsx`

**信息:**
- 行数: 105
- 大小: 9365 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { getAgentName, getTeammateColor, getTeamName } from '../../utils/teammate.js';
import { Spinner } from '../Spinner.js';
import { WorkerBadge } from './WorkerBadge.js';
type Props = {
  toolName: string;
  description: string;
};

/**
 * Visual indicator shown on workers while waiting for leader to approve a permission request.
 * Displays the pending tool with a spinner and information about what's being requested.
 */
export function WorkerPendingPermission(t0) {
  const $ = _c(15);
  const {
    toolName,
    description
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = getTeamName();
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const teamName = t1;
  let t2;
  if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = getAgentName();
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  const agentName = t2;
  let t3;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t3 = getTeammateColor();
    $[2] = t3;
  } else {
    t3 = $[2];
  }
  const agentColor = t3;
  let t4;
  let t5;
  if ($[3] === Symbol.for("react.memo_cache_sentinel")) {
    t4 = <Box marginBottom={1}><Spinner /><Text color="warning" bold={true}>{" "}Waiting for team lead approval</Text></Box>;
    t5 = agentName && agentColor && <Box marginBottom={1}><WorkerBadge name={agentName} color={agentColor} /></Box>;

```

---


### `src/components/permissions/hooks.ts`

**信息:**
- 行数: 209
- 大小: 8453 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { useEffect, useRef } from 'react'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from 'src/services/analytics/index.js'
import { sanitizeToolNameForAnalytics } from 'src/services/analytics/metadata.js'
import { BashTool } from 'src/tools/BashTool/BashTool.js'
import { splitCommand_DEPRECATED } from 'src/utils/bash/commands.js'
import type {
  PermissionDecisionReason,
  PermissionResult,
} from 'src/utils/permissions/PermissionResult.js'
import {
  extractRules,
  hasRules,
} from 'src/utils/permissions/PermissionUpdate.js'
import { permissionRuleValueToString } from 'src/utils/permissions/permissionRuleParser.js'
import { SandboxManager } from 'src/utils/sandbox/sandbox-adapter.js'
import type { ToolUseConfirm } from '../../components/permissions/PermissionRequest.js'
import { useSetAppState } from '../../state/AppState.js'
import { env } from '../../utils/env.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { type CompletionType, logUnaryEvent } from '../../utils/unaryLogging.js'

export type UnaryEvent = {
  completion_type: CompletionType
  language_name: string | Promise<string>
}

function permissionResultToLog(permissionResult: PermissionResult): string {
  switch (permissionResult.behavior) {
    case 'allow':
      return 'allow'
    case 'ask': {
      const rules = extractRules(permissionResult.suggestions)
      const suggestions =
        rules.length > 0
          ? rules.map(r => permissionRuleValueToString(r)).join(', ')
          : 'none'
      return `ask: ${permissionResult.message}, 
suggestions: ${suggestions}
reason: ${decisionReasonToString(permissionResult.decisionReason)}`
    }
    case 'deny':
      return `deny: ${permissionResult.message},
reason: ${decisionReasonToString(permissionResult.decisionReason)}`
    case 'passthrough': {
      const rules = extractRules(permissionResult.suggestions)
      const suggestions =

```

---


### `src/components/permissions/rules/AddPermissionRules.tsx`

**信息:**
- 行数: 180
- 大小: 22020 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useCallback } from 'react';
import { Select } from '../../../components/CustomSelect/select.js';
import { Box, Text } from '../../../ink.js';
import type { ToolPermissionContext } from '../../../Tool.js';
import type { PermissionBehavior, PermissionRule, PermissionRuleValue } from '../../../utils/permissions/PermissionRule.js';
import { applyPermissionUpdate, persistPermissionUpdate } from '../../../utils/permissions/PermissionUpdate.js';
import { permissionRuleValueToString } from '../../../utils/permissions/permissionRuleParser.js';
import { detectUnreachableRules, type UnreachableRule } from '../../../utils/permissions/shadowedRuleDetection.js';
import { SandboxManager } from '../../../utils/sandbox/sandbox-adapter.js';
import { type EditableSettingSource, SOURCES } from '../../../utils/settings/constants.js';
import { getRelativeSettingsFilePathForSource } from '../../../utils/settings/settings.js';
import { plural } from '../../../utils/stringUtils.js';
import type { OptionWithDescription } from '../../CustomSelect/select.js';
import { Dialog } from '../../design-system/Dialog.js';
import { PermissionRuleDescription } from './PermissionRuleDescription.js';
export function optionForPermissionSaveDestination(saveDestination: EditableSettingSource): OptionWithDescription {
  switch (saveDestination) {
    case 'localSettings':
      return {
        label: 'Project settings (local)',
        description: `Saved in ${getRelativeSettingsFilePathForSource('localSettings')}`,
        value: saveDestination
      };
    case 'projectSettings':
      return {
        label: 'Project settings',
        description: `Checked in at ${getRelativeSettingsFilePathForSource('projectSettings')}`,
        value: saveDestination
      };
    case 'userSettings':
      return {
        label: 'User settings',
        description: `Saved in at ~/.claude/settings.json`,
        value: saveDestination
      };
  }
}
type Props = {
  onAddRules: (rules: PermissionRule[], unreachable?: UnreachableRule[]) => void;
  onCancel: () => void;
  ruleValues: PermissionRuleValue[];
  ruleBehavior: PermissionBehavior;
  initialContext: ToolPermissionContext;
  setToolPermissionContext: (newContext: ToolPermissionContext) => void;
};
export function AddPermissionRules(t0) {
  const $ = _c(26);
  const {

```

---


### `src/components/permissions/rules/AddWorkspaceDirectory.tsx`

**信息:**
- 行数: 340
- 大小: 37741 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useDebounceCallback } from 'usehooks-ts';
import { addDirHelpMessage, validateDirectoryForWorkspace } from '../../../commands/add-dir/validation.js';
import TextInput from '../../../components/TextInput.js';
import type { KeyboardEvent } from '../../../ink/events/keyboard-event.js';
import { Box, Text } from '../../../ink.js';
import { useKeybinding } from '../../../keybindings/useKeybinding.js';
import type { ToolPermissionContext } from '../../../Tool.js';
import { getDirectoryCompletions } from '../../../utils/suggestions/directoryCompletion.js';
import { ConfigurableShortcutHint } from '../../ConfigurableShortcutHint.js';
import { Select } from '../../CustomSelect/select.js';
import { Byline } from '../../design-system/Byline.js';
import { Dialog } from '../../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../../design-system/KeyboardShortcutHint.js';
import { PromptInputFooterSuggestions, type SuggestionItem } from '../../PromptInput/PromptInputFooterSuggestions.js';
type Props = {
  onAddDirectory: (path: string, remember?: boolean) => void;
  onCancel: () => void;
  permissionContext: ToolPermissionContext;
  directoryPath?: string; // When directoryPath is provided, show selection options instead of input
};
type RememberDirectoryOption = 'yes-session' | 'yes-remember' | 'no';
const REMEMBER_DIRECTORY_OPTIONS: Array<{
  value: RememberDirectoryOption;
  label: string;
}> = [{
  value: 'yes-session',
  label: 'Yes, for this session'
}, {
  value: 'yes-remember',
  label: 'Yes, and remember this directory'
}, {
  value: 'no',
  label: 'No'
}];
function PermissionDescription() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <Text dimColor={true}>Claude Code will be able to read files in this directory and make edits when auto-accept edits is on.</Text>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}
function DirectoryDisplay(t0) {

```

---


### `src/components/permissions/rules/PermissionRuleDescription.tsx`

**信息:**
- 行数: 76
- 大小: 6900 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Text } from '../../../ink.js';
import { BashTool } from '../../../tools/BashTool/BashTool.js';
import type { PermissionRuleValue } from '../../../utils/permissions/PermissionRule.js';
type RuleSubtitleProps = {
  ruleValue: PermissionRuleValue;
};
export function PermissionRuleDescription(t0) {
  const $ = _c(9);
  const {
    ruleValue
  } = t0;
  switch (ruleValue.toolName) {
    case BashTool.name:
      {
        if (ruleValue.ruleContent) {
          if (ruleValue.ruleContent.endsWith(":*")) {
            let t1;
            if ($[0] !== ruleValue.ruleContent) {
              t1 = ruleValue.ruleContent.slice(0, -2);
              $[0] = ruleValue.ruleContent;
              $[1] = t1;
            } else {
              t1 = $[1];
            }
            let t2;
            if ($[2] !== t1) {
              t2 = <Text dimColor={true}>Any Bash command starting with{" "}<Text bold={true}>{t1}</Text></Text>;
              $[2] = t1;
              $[3] = t2;
            } else {
              t2 = $[3];
            }
            return t2;
          } else {
            let t1;
            if ($[4] !== ruleValue.ruleContent) {
              t1 = <Text dimColor={true}>The Bash command <Text bold={true}>{ruleValue.ruleContent}</Text></Text>;
              $[4] = ruleValue.ruleContent;
              $[5] = t1;
            } else {
              t1 = $[5];
            }
            return t1;
          }
        } else {
          let t1;
          if ($[6] === Symbol.for("react.memo_cache_sentinel")) {
            t1 = <Text dimColor={true}>Any Bash command</Text>;

```

---


### `src/components/permissions/rules/PermissionRuleInput.tsx`

**信息:**
- 行数: 138
- 大小: 16427 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useState } from 'react';
import TextInput from '../../../components/TextInput.js';
import { useExitOnCtrlCDWithKeybindings } from '../../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { useTerminalSize } from '../../../hooks/useTerminalSize.js';
import { Box, Newline, Text } from '../../../ink.js';
import { useKeybinding } from '../../../keybindings/useKeybinding.js';
import { BashTool } from '../../../tools/BashTool/BashTool.js';
import { WebFetchTool } from '../../../tools/WebFetchTool/WebFetchTool.js';
import type { PermissionBehavior, PermissionRuleValue } from '../../../utils/permissions/PermissionRule.js';
import { permissionRuleValueFromString, permissionRuleValueToString } from '../../../utils/permissions/permissionRuleParser.js';
export type PermissionRuleInputProps = {
  onCancel: () => void;
  onSubmit: (ruleValue: PermissionRuleValue, ruleBehavior: PermissionBehavior) => void;
  ruleBehavior: PermissionBehavior;
};
export function PermissionRuleInput(t0) {
  const $ = _c(24);
  const {
    onCancel,
    onSubmit,
    ruleBehavior
  } = t0;
  const [inputValue, setInputValue] = useState("");
  const [cursorOffset, setCursorOffset] = useState(0);
  const exitState = useExitOnCtrlCDWithKeybindings();
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = {
      context: "Settings"
    };
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  useKeybinding("confirm:no", onCancel, t1);
  const {
    columns
  } = useTerminalSize();
  const textInputColumns = columns - 6;
  let t2;
  if ($[1] !== onSubmit || $[2] !== ruleBehavior) {
    t2 = value => {
      const trimmedValue = value.trim();
      if (trimmedValue.length === 0) {
        return;
      }
      const ruleValue = permissionRuleValueFromString(trimmedValue);

```

---


### `src/components/permissions/rules/PermissionRuleList.tsx`

**信息:**
- 行数: 1179
- 大小: 118930 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import chalk from 'chalk';
import figures from 'figures';
import * as React from 'react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useAppState, useSetAppState } from 'src/state/AppState.js';
import { applyPermissionUpdate, persistPermissionUpdate } from 'src/utils/permissions/PermissionUpdate.js';
import type { PermissionUpdateDestination } from 'src/utils/permissions/PermissionUpdateSchema.js';
import type { CommandResultDisplay } from '../../../commands.js';
import { Select } from '../../../components/CustomSelect/select.js';
import { useExitOnCtrlCDWithKeybindings } from '../../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { useSearchInput } from '../../../hooks/useSearchInput.js';
import type { KeyboardEvent } from '../../../ink/events/keyboard-event.js';
import { Box, Text, useTerminalFocus } from '../../../ink.js';
import { useKeybinding } from '../../../keybindings/useKeybinding.js';
import { type AutoModeDenial, getAutoModeDenials } from '../../../utils/autoModeDenials.js';
import type { PermissionBehavior, PermissionRule, PermissionRuleValue } from '../../../utils/permissions/PermissionRule.js';
import { permissionRuleValueToString } from '../../../utils/permissions/permissionRuleParser.js';
import { deletePermissionRule, getAllowRules, getAskRules, getDenyRules, permissionRuleSourceDisplayString } from '../../../utils/permissions/permissions.js';
import type { UnreachableRule } from '../../../utils/permissions/shadowedRuleDetection.js';
import { jsonStringify } from '../../../utils/slowOperations.js';
import { Pane } from '../../design-system/Pane.js';
import { Tab, Tabs, useTabHeaderFocus, useTabsWidth } from '../../design-system/Tabs.js';
import { SearchBox } from '../../SearchBox.js';
import type { Option } from '../../ui/option.js';
import { AddPermissionRules } from './AddPermissionRules.js';
import { AddWorkspaceDirectory } from './AddWorkspaceDirectory.js';
import { PermissionRuleDescription } from './PermissionRuleDescription.js';
import { PermissionRuleInput } from './PermissionRuleInput.js';
import { RecentDenialsTab } from './RecentDenialsTab.js';
import { RemoveWorkspaceDirectory } from './RemoveWorkspaceDirectory.js';
import { WorkspaceTab } from './WorkspaceTab.js';
type TabType = 'recent' | 'allow' | 'ask' | 'deny' | 'workspace';
type RuleSourceTextProps = {
  rule: PermissionRule;
};
function RuleSourceText(t0) {
  const $ = _c(4);
  const {
    rule
  } = t0;
  let t1;
  if ($[0] !== rule.source) {
    t1 = permissionRuleSourceDisplayString(rule.source);
    $[0] = rule.source;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const t2 = `From ${t1}`;

```

---


### `src/components/permissions/rules/RecentDenialsTab.tsx`

**信息:**
- 行数: 207
- 大小: 18857 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useCallback, useEffect, useState } from 'react';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- 'r' is a view-specific key, not a global keybinding
import { Box, Text, useInput } from '../../../ink.js';
import { type AutoModeDenial, getAutoModeDenials } from '../../../utils/autoModeDenials.js';
import { Select } from '../../CustomSelect/select.js';
import { StatusIcon } from '../../design-system/StatusIcon.js';
import { useTabHeaderFocus } from '../../design-system/Tabs.js';
type Props = {
  onHeaderFocusChange?: (focused: boolean) => void;
  /** Called when approved/retry state changes so parent can act on exit */
  onStateChange: (state: {
    approved: Set<number>;
    retry: Set<number>;
    denials: readonly AutoModeDenial[];
  }) => void;
};
export function RecentDenialsTab(t0) {
  const $ = _c(30);
  const {
    onHeaderFocusChange,
    onStateChange
  } = t0;
  const {
    headerFocused,
    focusHeader
  } = useTabHeaderFocus();
  let t1;
  let t2;
  if ($[0] !== headerFocused || $[1] !== onHeaderFocusChange) {
    t1 = () => {
      onHeaderFocusChange?.(headerFocused);
    };
    t2 = [headerFocused, onHeaderFocusChange];
    $[0] = headerFocused;
    $[1] = onHeaderFocusChange;
    $[2] = t1;
    $[3] = t2;
  } else {
    t1 = $[2];
    t2 = $[3];
  }
  useEffect(t1, t2);
  const [denials] = useState(_temp);
  const [approved, setApproved] = useState(_temp2);
  const [retry, setRetry] = useState(_temp3);
  const [focusedIdx, setFocusedIdx] = useState(0);
  let t3;
  let t4;

```

---


### `src/components/permissions/rules/RemoveWorkspaceDirectory.tsx`

**信息:**
- 行数: 110
- 大小: 9757 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useCallback } from 'react';
import { Select } from '../../../components/CustomSelect/select.js';
import { Box, Text } from '../../../ink.js';
import type { ToolPermissionContext } from '../../../Tool.js';
import { applyPermissionUpdate } from '../../../utils/permissions/PermissionUpdate.js';
import { Dialog } from '../../design-system/Dialog.js';
type Props = {
  directoryPath: string;
  onRemove: () => void;
  onCancel: () => void;
  permissionContext: ToolPermissionContext;
  setPermissionContext: (context: ToolPermissionContext) => void;
};
export function RemoveWorkspaceDirectory(t0) {
  const $ = _c(19);
  const {
    directoryPath,
    onRemove,
    onCancel,
    permissionContext,
    setPermissionContext
  } = t0;
  let t1;
  if ($[0] !== directoryPath || $[1] !== onRemove || $[2] !== permissionContext || $[3] !== setPermissionContext) {
    t1 = () => {
      const updatedContext = applyPermissionUpdate(permissionContext, {
        type: "removeDirectories",
        directories: [directoryPath],
        destination: "session"
      });
      setPermissionContext(updatedContext);
      onRemove();
    };
    $[0] = directoryPath;
    $[1] = onRemove;
    $[2] = permissionContext;
    $[3] = setPermissionContext;
    $[4] = t1;
  } else {
    t1 = $[4];
  }
  const handleRemove = t1;
  let t2;
  if ($[5] !== handleRemove || $[6] !== onCancel) {
    t2 = value => {
      if (value === "yes") {
        handleRemove();
      } else {

```

---


### `src/components/permissions/rules/WorkspaceTab.tsx`

**信息:**
- 行数: 150
- 大小: 15172 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useCallback, useEffect } from 'react';
import { getOriginalCwd } from '../../../bootstrap/state.js';
import type { CommandResultDisplay } from '../../../commands.js';
import { Select } from '../../../components/CustomSelect/select.js';
import { Box, Text } from '../../../ink.js';
import type { ToolPermissionContext } from '../../../Tool.js';
import { useTabHeaderFocus } from '../../design-system/Tabs.js';
type Props = {
  onExit: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  toolPermissionContext: ToolPermissionContext;
  onRequestAddDirectory: () => void;
  onRequestRemoveDirectory: (path: string) => void;
  onHeaderFocusChange?: (focused: boolean) => void;
};
type DirectoryItem = {
  path: string;
  isCurrent: boolean;
  isDeletable: boolean;
};
export function WorkspaceTab(t0) {
  const $ = _c(23);
  const {
    onExit,
    toolPermissionContext,
    onRequestAddDirectory,
    onRequestRemoveDirectory,
    onHeaderFocusChange
  } = t0;
  const {
    headerFocused,
    focusHeader
  } = useTabHeaderFocus();
  let t1;
  let t2;
  if ($[0] !== headerFocused || $[1] !== onHeaderFocusChange) {
    t1 = () => {
      onHeaderFocusChange?.(headerFocused);
    };
    t2 = [headerFocused, onHeaderFocusChange];
    $[0] = headerFocused;
    $[1] = onHeaderFocusChange;
    $[2] = t1;
    $[3] = t2;
  } else {
    t1 = $[2];

```

---


### `src/components/permissions/shellPermissionHelpers.tsx`

**信息:**
- 行数: 164
- 大小: 22517 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { basename, sep } from 'path';
import React, { type ReactNode } from 'react';
import { getOriginalCwd } from '../../bootstrap/state.js';
import { Text } from '../../ink.js';
import type { PermissionUpdate } from '../../utils/permissions/PermissionUpdateSchema.js';
import { permissionRuleExtractPrefix } from '../../utils/permissions/shellRuleMatching.js';
function commandListDisplay(commands: string[]): ReactNode {
  switch (commands.length) {
    case 0:
      return '';
    case 1:
      return <Text bold>{commands[0]}</Text>;
    case 2:
      return <Text>
          <Text bold>{commands[0]}</Text> and <Text bold>{commands[1]}</Text>
        </Text>;
    default:
      return <Text>
          <Text bold>{commands.slice(0, -1).join(', ')}</Text>, and{' '}
          <Text bold>{commands.slice(-1)[0]}</Text>
        </Text>;
  }
}
function commandListDisplayTruncated(commands: string[]): ReactNode {
  // Check if the plain text representation would be too long
  const plainText = commands.join(', ');
  if (plainText.length > 50) {
    return 'similar';
  }
  return commandListDisplay(commands);
}
function formatPathList(paths: string[]): ReactNode {
  if (paths.length === 0) return '';

  // Extract directory names from paths
  const names = paths.map(p => basename(p) || p);
  if (names.length === 1) {
    return <Text>
        <Text bold>{names[0]}</Text>
        {sep}
      </Text>;
  }
  if (names.length === 2) {
    return <Text>
        <Text bold>{names[0]}</Text>
        {sep} and <Text bold>{names[1]}</Text>
        {sep}
      </Text>;
  }


```

---


### `src/components/permissions/useShellPermissionFeedback.ts`

**信息:**
- 行数: 148
- 大小: 4605 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useState } from 'react'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import { sanitizeToolNameForAnalytics } from '../../services/analytics/metadata.js'
import { useSetAppState } from '../../state/AppState.js'
import type { ToolUseConfirm } from './PermissionRequest.js'
import { logUnaryPermissionEvent } from './utils.js'

/**
 * Shared feedback-mode state + handlers for shell permission dialogs (Bash,
 * PowerShell). Encapsulates the yes/no input-mode toggle, feedback text state,
 * focus tracking, and reject handling.
 */
export function useShellPermissionFeedback({
  toolUseConfirm,
  onDone,
  onReject,
  explainerVisible,
}: {
  toolUseConfirm: ToolUseConfirm
  onDone: () => void
  onReject: () => void
  explainerVisible: boolean
}): {
  yesInputMode: boolean
  noInputMode: boolean
  yesFeedbackModeEntered: boolean
  noFeedbackModeEntered: boolean
  acceptFeedback: string
  rejectFeedback: string
  setAcceptFeedback: (v: string) => void
  setRejectFeedback: (v: string) => void
  focusedOption: string
  handleInputModeToggle: (option: string) => void
  handleReject: (feedback?: string) => void
  handleFocus: (value: string) => void
} {
  const setAppState = useSetAppState()
  const [rejectFeedback, setRejectFeedback] = useState('')
  const [acceptFeedback, setAcceptFeedback] = useState('')
  const [yesInputMode, setYesInputMode] = useState(false)
  const [noInputMode, setNoInputMode] = useState(false)
  const [focusedOption, setFocusedOption] = useState('yes')
  // Track whether user ever entered feedback mode (persists after collapse)
  const [yesFeedbackModeEntered, setYesFeedbackModeEntered] = useState(false)
  const [noFeedbackModeEntered, setNoFeedbackModeEntered] = useState(false)

  // Handle Tab key toggling input mode for Yes/No options

```

---


### `src/components/permissions/utils.ts`

**信息:**
- 行数: 25
- 大小: 660 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getHostPlatformForAnalytics } from '../../utils/env.js'
import { type CompletionType, logUnaryEvent } from '../../utils/unaryLogging.js'
import type { ToolUseConfirm } from './PermissionRequest.js'

export function logUnaryPermissionEvent(
  completion_type: CompletionType,
  {
    assistantMessage: {
      message: { id: message_id },
    },
  }: ToolUseConfirm,
  event: 'accept' | 'reject',
  hasFeedback?: boolean,
): void {
  void logUnaryEvent({
    completion_type,
    event,
    metadata: {
      language_name: 'none',
      message_id,
      platform: getHostPlatformForAnalytics(),
      hasFeedback: hasFeedback ?? false,
    },
  })
}

```

---


### `src/components/sandbox/SandboxConfigTab.tsx`

**信息:**
- 行数: 45
- 大小: 16895 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import { SandboxManager, shouldAllowManagedSandboxDomainsOnly } from '../../utils/sandbox/sandbox-adapter.js';
export function SandboxConfigTab() {
  const $ = _c(3);
  const isEnabled = SandboxManager.isSandboxingEnabled();
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    const depCheck = SandboxManager.checkDependencies();
    t0 = depCheck.warnings.length > 0 ? <Box marginTop={1} flexDirection="column">{depCheck.warnings.map(_temp)}</Box> : null;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  const warningsNote = t0;
  if (!isEnabled) {
    let t1;
    if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
      t1 = <Box flexDirection="column" paddingY={1}><Text color="subtle">Sandbox is not enabled</Text>{warningsNote}</Box>;
      $[1] = t1;
    } else {
      t1 = $[1];
    }
    return t1;
  }
  let t1;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    const fsReadConfig = SandboxManager.getFsReadConfig();
    const fsWriteConfig = SandboxManager.getFsWriteConfig();
    const networkConfig = SandboxManager.getNetworkRestrictionConfig();
    const allowUnixSockets = SandboxManager.getAllowUnixSockets();
    const excludedCommands = SandboxManager.getExcludedCommands();
    const globPatternWarnings = SandboxManager.getLinuxGlobPatternWarnings();
    t1 = <Box flexDirection="column" paddingY={1}><Box flexDirection="column"><Text bold={true} color="permission">Excluded Commands:</Text><Text dimColor={true}>{excludedCommands.length > 0 ? excludedCommands.join(", ") : "None"}</Text></Box>{fsReadConfig.denyOnly.length > 0 && <Box marginTop={1} flexDirection="column"><Text bold={true} color="permission">Filesystem Read Restrictions:</Text><Text dimColor={true}>Denied: {fsReadConfig.denyOnly.join(", ")}</Text>{fsReadConfig.allowWithinDeny && fsReadConfig.allowWithinDeny.length > 0 && <Text dimColor={true}>Allowed within denied: {fsReadConfig.allowWithinDeny.join(", ")}</Text>}</Box>}{fsWriteConfig.allowOnly.length > 0 && <Box marginTop={1} flexDirection="column"><Text bold={true} color="permission">Filesystem Write Restrictions:</Text><Text dimColor={true}>Allowed: {fsWriteConfig.allowOnly.join(", ")}</Text>{fsWriteConfig.denyWithinAllow.length > 0 && <Text dimColor={true}>Denied within allowed: {fsWriteConfig.denyWithinAllow.join(", ")}</Text>}</Box>}{(networkConfig.allowedHosts && networkConfig.allowedHosts.length > 0 || networkConfig.deniedHosts && networkConfig.deniedHosts.length > 0) && <Box marginTop={1} flexDirection="column"><Text bold={true} color="permission">Network Restrictions{shouldAllowManagedSandboxDomainsOnly() ? " (Managed)" : ""}:</Text>{networkConfig.allowedHosts && networkConfig.allowedHosts.length > 0 && <Text dimColor={true}>Allowed: {networkConfig.allowedHosts.join(", ")}</Text>}{networkConfig.deniedHosts && networkConfig.deniedHosts.length > 0 && <Text dimColor={true}>Denied: {networkConfig.deniedHosts.join(", ")}</Text>}</Box>}{allowUnixSockets && allowUnixSockets.length > 0 && <Box marginTop={1} flexDirection="column"><Text bold={true} color="permission">Allowed Unix Sockets:</Text><Text dimColor={true}>{allowUnixSockets.join(", ")}</Text></Box>}{globPatternWarnings.length > 0 && <Box marginTop={1} flexDirection="column"><Text bold={true} color="warning">⚠ Warning: Glob patterns not fully supported on Linux</Text><Text dimColor={true}>The following patterns will be ignored:{" "}{globPatternWarnings.slice(0, 3).join(", ")}{globPatternWarnings.length > 3 && ` (${globPatternWarnings.length - 3} more)`}</Text></Box>}{warningsNote}</Box>;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  return t1;
}
function _temp(w, i) {
  return <Text key={i} dimColor={true}>{w}</Text>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJveCIsIlRleHQiLCJTYW5kYm94TWFuYWdlciIsInNob3VsZEFsbG93TWFuYWdlZFNhbmRib3hEb21haW5zT25seSIsIlNhbmRib3hDb25maWdUYWIiLCIkIiwiX2MiLCJpc0VuYWJsZWQiLCJpc1NhbmRib3hpbmdFbmFibGVkIiwidDAiLCJTeW1ib2wiLCJmb3IiLCJkZXBDaGVjayIsImNoZWNrRGVwZW5kZW5jaWVzIiwid2FybmluZ3MiLCJsZW5ndGgiLCJtYXAiLCJfdGVtcCIsIndhcm5pbmdzTm90ZSIsInQxIiwiZnNSZWFkQ29uZmlnIiwiZ2V0RnNSZWFkQ29uZmlnIiwiZnNXcml0ZUNvbmZpZyIsImdldEZzV3JpdGVDb25maWciLCJuZXR3b3JrQ29uZmlnIiwiZ2V0TmV0d29ya1Jlc3RyaWN0aW9uQ29uZmlnIiwiYWxsb3dVbml4U29ja2V0cyIsImdldEFsbG93VW5peFNvY2tldHMiLCJleGNsdWRlZENvbW1hbmRzIiwiZ2V0RXhjbHVkZWRDb21tYW5kcyIsImdsb2JQYXR0ZXJuV2FybmluZ3MiLCJnZXRMaW51eEdsb2JQYXR0ZXJuV2FybmluZ3MiLCJqb2luIiwiZGVueU9ubHkiLCJhbGxvd1dpdGhpbkRlbnkiLCJhbGxvd09ubHkiLCJkZW55V2l0aGluQWxsb3ciLCJhbGxvd2VkSG9zdHMiLCJkZW5pZWRIb3N0cyIsInNsaWNlIiwidyIsImkiXSwic291cmNlcyI6WyJTYW5kYm94Q29uZmlnVGFiLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IEJveCwgVGV4dCB9IGZyb20gJy4uLy4uL2luay5qcydcbmltcG9ydCB7XG4gIFNhbmRib3hNYW5hZ2VyLFxuICBzaG91bGRBbGxvd01hbmFnZWRTYW5kYm94RG9tYWluc09ubHksXG59IGZyb20gJy4uLy4uL3V0aWxzL3NhbmRib3gvc2FuZGJveC1hZGFwdGVyLmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gU2FuZGJveENvbmZpZ1RhYigpOiBSZWFjdC5SZWFjdE5vZGUge1xuICBjb25zdCBpc0VuYWJsZWQgPSBTYW5kYm94TWFuYWdlci5pc1NhbmRib3hpbmdFbmFibGVkKClcblxuICAvLyBTaG93IHdhcm5pbmdzIChlLmcuLCBzZWNjb21wIG5vdCBhdmFpbGFibGUgb24gTGludXgpXG4gIGNvbnN0IGRlcENoZWNrID0gU2FuZGJveE1hbmFnZXIuY2hlY2tEZXBlbmRlbmNpZXMoKVxuICBjb25zdCB3YXJuaW5nc05vdGUgPVxuICAgIGRlcENoZWNrLndhcm5pbmdzLmxlbmd0aCA+IDAgPyAoXG4gICAgICA8Qm94IG1hcmdpblRvcD17MX0gZmxleERpcmVjdGlvbj1cImNvbHVtblwiPlxuICAgICAgICB7ZGVwQ2hlY2sud2FybmluZ3MubWFwKCh3LCBpKSA9PiAoXG4gICAgICAgICAgPFRleHQga2V5PXtpfSBkaW1Db2xvcj5cbiAgICAgICAgICAgIHt3fVxuICAgICAgICAgIDwvVGV4dD5cbiAgICAgICAgKSl9XG4gICAgICA8L0JveD5cbiAgICApIDogbnVsbFxuXG4gIGlmICghaXNFbmFibGVkKSB7XG4gICAgcmV0dXJuIChcbiAgICAgIDxCb3ggZmxleERpcmVjdGlvbj1cImNvbHVtblwiIHBhZGRpbmdZPXsxfT5cbiAgICAgICAgPFRleHQgY29sb3I9XCJzdWJ0bGVcIj5TYW5kYm94IGlzIG5vdCBlbmFibGVkPC9UZXh0PlxuICAgICAgICB7d2FybmluZ3NOb3RlfVxuICAgICAgPC9Cb3g+XG4gICAgKVxuICB9XG5cbiAgY29uc3QgZnNSZWFkQ29uZmlnID0gU2FuZGJveE1hbmFnZXIuZ2V0RnNSZWFkQ29uZmlnKClcbiAgY29uc3QgZnNXcml0ZUNvbmZpZyA9IFNhbmRib3hNYW5hZ2VyLmdldEZzV3JpdGVDb25maWcoKVxuICBjb25zdCBuZXR3b3JrQ29uZmlnID0gU2FuZGJveE1hbmFnZXIuZ2V0TmV0d29ya1Jlc3RyaWN0aW9uQ29uZmlnKClcbiAgY29uc3QgYWxsb3dVbml4U29ja2V0cyA9IFNhbmRib3hNYW5hZ2VyLmdldEFsbG93VW5peFNvY2tldHMoKVxuICBjb25zdCBleGNsdWRlZENvbW1hbmRzID0gU2FuZGJveE1hbmFnZXIuZ2V0RXhjbHVkZWRDb21tYW5kcygpXG4gIGNvbnN0IGdsb2JQYXR0ZXJuV2FybmluZ3MgPSBTYW5kYm94TWFuYWdlci5nZXRMaW51eEdsb2JQYXR0ZXJuV2FybmluZ3MoKVxuXG4gIHJldHVybiAoXG4gICAgPEJveCBmbGV4RGlyZWN0aW9uPVwiY29sdW1uXCIgcGFkZGluZ1k9ezF9PlxuICAgICAgey8qIEV4Y2x1ZGVkIENvbW1hbmRzICovfVxuICAgICAgPEJveCBmbGV4RGlyZWN0aW9uPVwiY29sdW1uXCI+XG4gICAgICAgIDxUZXh0IGJvbGQgY29sb3I9XCJwZXJtaXNzaW9uXCI+XG4gICAgICAgICAgRXhjbHVkZWQgQ29tbWFuZHM6XG4gICAgICAgIDwvVGV4dD5cbiAgICAgICAgPFRleHQgZGltQ29sb3I+XG4gICAgICAgICAge2V4Y2x1ZGVkQ29tbWFuZHMubGVuZ3RoID4gMCA/IGV4Y2x1ZGVkQ29tbWFuZHMuam9pbignLCAnKSA6ICdOb25lJ31cbiAgICAgICAgPC9UZXh0PlxuICAgICAgPC9Cb3g+XG5cbiAgICAgIHsvKiBGaWxlc3lzdGVtIFJlYWQgUmVzdHJpY3Rpb25zICovfVxuICAgICAge2ZzUmVhZENvbmZpZy5kZW55T25seS5sZW5ndGggPiAwICYmIChcbiAgICAgICAgPEJveCBtYXJnaW5Ub3A9ezF9IGZsZXhEaXJlY3Rpb249XCJjb2x1bW5cIj5cbiAgICAgICAgICA8VGV4dCBib2xkIGNvbG9yPVwicGVybWlzc2lvblwiPlxuICAgICAgICAgICAgRmlsZXN5c3RlbSBSZWFkIFJlc3RyaWN0aW9uczpcbiAgICAgICAgICA8L1RleHQ+XG4gICAgICAgICAgPFRleHQgZGltQ29sb3I+RGVuaWVkOiB7ZnNSZWFkQ29uZmlnLmRlbnlPbmx5LmpvaW4oJywgJyl9PC9UZXh0PlxuICAgICAgICAgIHtmc1JlYWRDb25maWcuYWxsb3dXaXRoaW5EZW55ICYmXG4gICAgICAgICAgICBmc1JlYWRDb25maWcuYWxsb3dXaXRoaW5EZW55Lmxlbmd0aCA+IDAgJiYgKFxuICAgICAgICAgICAgICA8VGV4dCBkaW1Db2xvcj5cbiAgICAgICAgICAgICAgICBBbGxvd2VkIHdpdGhpbiBkZW5pZWQ6IHtmc1JlYWRDb25maWcuYWxsb3dXaXRoaW5EZW55LmpvaW4oJywgJyl9XG4gICAgICAgICAgICAgIDwvVGV4dD5cbiAgICAgICAgICAgICl9XG4gICAgICAgIDwvQm94PlxuICAgICAgKX1cblxuICAgICAgey8qIEZpbGVzeXN0ZW0gV3JpdGUgUmVzdHJpY3Rpb25zICovfVxuICAgICAge2ZzV3JpdGVDb25maWcuYWxsb3dPbmx5Lmxlbmd0aCA+IDAgJiYgKFxuICAgICAgICA8Qm94IG1hcmdpblRvcD17MX0gZmxleERpcmVjdGlvbj1cImNvbHVtblwiPlxuICAgICAgICAgIDxUZXh0IGJvbGQgY29sb3I9XCJwZXJtaXNzaW9uXCI+XG4gICAgICAgICAgICBGaWxlc3lzdGVtIFdyaXRlIFJlc3RyaWN0aW9uczpcbiAgICAgICAgICA8L1RleHQ+XG4gICAgICAgICAgPFRleHQgZGltQ29sb3I+QWxsb3dlZDoge2ZzV3JpdGVDb25maWcuYWxsb3dPbmx5LmpvaW4oJywgJyl9PC9UZXh0PlxuICAgICAgICAgIHtmc1dyaXRlQ29uZmlnLmRlbnlXaXRoaW5BbGxvdy5sZW5ndGggPiAwICYmIChcbiAgICAgICAgICAgIDxUZXh0IGRpbUNvbG9yPlxuICAgICAgICAgICAgICBEZW5pZWQgd2l0aGluIGFsbG93ZWQ6IHtmc1dyaXRlQ29uZmlnLmRlbnlXaXRoaW5BbGxvdy5qb2luKCcsICcpfVxuICAgICAgICAgICAgPC9UZXh0PlxuICAgICAgICAgICl9XG4gICAgICAgIDwvQm94PlxuICAgICAgKX1cblxuICAgICAgey8qIE5ldHdvcmsgUmVzdHJpY3Rpb25zICovfVxuICAgICAgeygobmV0d29ya0NvbmZpZy5hbGxvd2VkSG9zdHMgJiYgbmV0d29ya0NvbmZpZy5hbGxvd2VkSG9zdHMubGVuZ3RoID4gMCkgfHxcbiAgICAgICAgKG5ldHdvcmtDb25maWcuZGVuaWVkSG9zdHMgJiZcbiAgICAgICAgICBuZXR3b3JrQ29uZmlnLmRlbmllZEhvc3RzLmxlbmd0aCA+IDApKSAmJiAoXG4gICAgICAgIDxCb3ggbWFyZ2luVG9wPXsxfSBmbGV4RGlyZWN0aW9uPVwiY29sdW1uXCI+XG4gICAgICAgICAgPFRleHQgYm9sZCBjb2xvcj1cInBlcm1pc3Npb25cIj5cbiAgICAgICAgICAgIE5ldHdvcmsgUmVzdHJpY3Rpb25zXG4gICAgICAgICAgICB7c2hvdWxkQWxsb3dNYW5hZ2VkU2FuZGJveERvbWFpbnNPbmx5KCkgPyAnIChNYW5hZ2VkKScgOiAnJ306XG4gICAgICAgICAgPC9UZXh0PlxuICAgICAgICAgIHtuZXR3b3JrQ29uZmlnLmFsbG93ZWRIb3N0cyAmJlxuICAgICAgICAgICAgbmV0d29ya0NvbmZpZy5hbGxvd2VkSG9zdHMubGVuZ3RoID4gMCAmJiAoXG4gICAgICAgICAgICAgIDxUZXh0IGRpbUNvbG9yPlxuICAgICAgICAgICAgICAgIEFsbG93ZWQ6IHtuZXR3b3JrQ29uZmlnLmFsbG93ZWRIb3N0cy5qb2luKCcsICcpfVxuICAgICAgICAgICAgICA8L1RleHQ+XG4gICAgICAgICAgICApfVxuICAgICAgICAgIHtuZXR3b3JrQ29uZmlnLmRlbmllZEhvc3RzICYmXG4gICAgICAgICAgICBuZXR3b3JrQ29uZmlnLmRlbmllZEhvc3RzLmxlbmd0aCA+IDAgJiYgKFxuICAgICAgICAgICAgICA8VGV4dCBkaW1Db2xvcj5cbiAgICAgICAgICAgICAgICBEZW5pZWQ6IHtuZXR3b3JrQ29uZmlnLmRlbmllZEhvc3RzLmpvaW4oJywgJyl9XG4gICAgICAgICAgICAgIDwvVGV4dD5cbiAgICAgICAgICAgICl9XG4gICAgICAgIDwvQm94PlxuICAgICAgKX1cblxuICAgICAgey8qIFVuaXggU29ja2V0cyAqL31cbiAgICAgIHthbGxvd1VuaXhTb2NrZXRzICYmIGFsbG93VW5peFNvY2tldHMubGVuZ3RoID4gMCAmJiAoXG4gICAgICAgIDxCb3ggbWFyZ2luVG9wPXsxfSBmbGV4RGlyZWN0aW9uPVwiY29sdW1uXCI+XG4gICAgICAgICAgPFRleHQgYm9sZCBjb2xvcj1cInBlcm1pc3Npb25cIj5cbiAgICAgICAgICAgIEFsbG93ZWQgVW5peCBTb2NrZXRzOlxuICAgICAgICAgIDwvVGV4dD5cbiAgICAgICAgICA8VGV4dCBkaW1Db2xvcj57YWxsb3dVbml4U29ja2V0cy5qb2luKCcsICcpfTwvVGV4dD5cbiAgICAgICAgPC9Cb3g+XG4gICAgICApfVxuXG4gICAgICB7LyogTGludXggR2xvYiBQYXR0ZXJuIFdhcm5pbmcgKi99XG4gICAgICB7Z2xvYlBhdHRlcm5XYXJuaW5ncy5sZW5ndGggPiAwICYmIChcbiAgICAgICAgPEJveCBtYXJnaW5Ub3A9ezF9IGZsZXhEaXJlY3Rpb249XCJjb2x1bW5cIj5cbiAgICAgICAgICA8VGV4dCBib2xkIGNvbG9yPVwid2FybmluZ1wiPlxuICAgICAgICAgICAg4pqgIFdhcm5pbmc6IEdsb2IgcGF0dGVybnMgbm90IGZ1bGx5IHN1cHBvcnRlZCBvbiBMaW51eFxuICAgICAgICAgIDwvVGV4dD5cbiAgICAgICAgICA8VGV4dCBkaW1Db2xvcj5cbiAgICAgICAgICAgIFRoZSBmb2xsb3dpbmcgcGF0dGVybnMgd2lsbCBiZSBpZ25vcmVkOnsnICd9XG4gICAgICAgICAgICB7Z2xvYlBhdHRlcm5XYXJuaW5ncy5zbGljZSgwLCAzKS5qb2luKCcsICcpfVxuICAgICAgICAgICAge2dsb2JQYXR0ZXJuV2FybmluZ3MubGVuZ3RoID4gMyAmJlxuICAgICAgICAgICAgICBgICgke2dsb2JQYXR0ZXJuV2FybmluZ3MubGVuZ3RoIC0gM30gbW9yZSlgfVxuICAgICAgICAgIDwvVGV4dD5cbiAgICAgICAgPC9Cb3g+XG4gICAgICApfVxuXG4gICAgICB7d2FybmluZ3NOb3RlfVxuICAgIDwvQm94PlxuICApXG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxRQUFRLGNBQWM7QUFDeEMsU0FDRUMsY0FBYyxFQUNkQyxvQ0FBb0MsUUFDL0Isd0NBQXdDO0FBRS9DLE9BQU8sU0FBQUMsaUJBQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFDTCxNQUFBQyxTQUFBLEdBQWtCTCxjQUFjLENBQUFNLG1CQUFvQixDQUFDLENBQUM7RUFBQSxJQUFBQyxFQUFBO0VBQUEsSUFBQUosQ0FBQSxRQUFBSyxNQUFBLENBQUFDLEdBQUE7SUFHdEQsTUFBQUMsUUFBQSxHQUFpQlYsY0FBYyxDQUFBVyxpQkFBa0IsQ0FBQyxDQUFDO0lBRWpESixFQUFBLEdBQUFHLFFBQVEsQ0FBQUUsUUFBUyxDQUFBQyxNQUFPLEdBQUcsQ0FRbkIsR0FQTixDQUFDLEdBQUcsQ0FBWSxTQUFDLENBQUQsR0FBQyxDQUFnQixhQUFRLENBQVIsUUFBUSxDQUN0QyxDQUFBSCxRQUFRLENBQUFFLFFBQVMsQ0FBQUUsR0FBSSxDQUFDQyxLQUl0QixFQUNILEVBTkMsR0FBRyxDQU9FLEdBUlIsSUFRUTtJQUFBWixDQUFBLE1BQUFJLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFKLENBQUE7RUFBQTtFQVRWLE1BQUFhLFlBQUEsR0FDRVQsRUFRUTtFQUVWLElBQUksQ0FBQ0YsU0FBUztJQUFBLElBQUFZLEVBQUE7SUFBQSxJQUFBZCxDQUFBLFFBQUFLLE1BQUEsQ0FBQUMsR0FBQTtNQUVWUSxFQUFBLElBQUMsR0FBRyxDQUFlLGFBQVEsQ0FBUixRQUFRLENBQVcsUUFBQyxDQUFELEdBQUMsQ0FDckMsQ0FBQyxJQUFJLENBQU8sS0FBUSxDQUFSLFFBQVEsQ0FBQyxzQkFBc0IsRUFBMUMsSUFBSSxDQUNKRCxhQUFXLENBQ2QsRUFIQyxHQUFHLENBR0U7TUFBQWIsQ0FBQSxNQUFBYyxFQUFBO0lBQUE7TUFBQUEsRUFBQSxHQUFBZCxDQUFBO0lBQUE7SUFBQSxPQUhOYyxFQUdNO0VBQUE7RUFFVCxJQUFBQSxFQUFBO0VBQUEsSUFBQWQsQ0FBQSxRQUFBSyxNQUFBLENBQUFDLEdBQUE7SUFFRCxNQUFBUyxZQUFBLEdBQXFCbEIsY0FBYyxDQUFBbUIsZUFBZ0IsQ0FBQyxDQUFDO0lBQ3JELE1BQUFDLGFBQUEsR0FBc0JwQixjQUFjLENBQUFxQixnQkFBaUIsQ0FBQyxDQUFDO0lBQ3ZELE1BQUFDLGFBQUEsR0FBc0J0QixjQUFjLENBQUF1QiwyQkFBNEIsQ0FBQyxDQUFDO0lBQ2xFLE1BQUFDLGdCQUFBLEdBQXlCeEIsY0FBYyxDQUFBeUIsbUJBQW9CLENBQUMsQ0FBQztJQUM3RCxNQUFBQyxnQkFBQSxHQUF5QjFCLGNBQWMsQ0FBQTJCLG1CQUFvQixDQUFDLENBQUM7SUFDN0QsTUFBQUMsbUJBQUEsR0FBNEI1QixjQUFjLENBQUE2QiwyQkFBNEIsQ0FBQyxDQUFDO0lBR3RFWixFQUFBLElBQUMsR0FBRyxDQUFlLGFBQVEsQ0FBUixRQUFRLENBQVcsUUFBQyxDQUFELEdBQUMsQ0FFckMsQ0FBQyxHQUFHLENBQWUsYUFBUSxDQUFSLFFBQVEsQ0FDekIsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFKLEtBQUcsQ0FBQyxDQUFPLEtBQVksQ0FBWixZQUFZLENBQUMsa0JBRTlCLEVBRkMsSUFBSSxDQUdMLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBUixLQUFPLENBQUMsQ0FDWCxDQUFBUyxnQkFBZ0IsQ0FBQWIsTUFBTyxHQUFHLENBQXdDLEdBQXBDYSxnQkFBZ0IsQ0FBQUksSUFBSyxDQUFDLElBQWEsQ0FBQyxHQUFsRSxNQUFpRSxDQUNwRSxFQUZDLElBQUksQ0FHUCxFQVBDLEdBQUcsQ0FVSCxDQUFBWixZQUFZLENBQUFhLFFBQVMsQ0FBQWxCLE1BQU8sR0FBRyxDQWEvQixJQVpDLENBQUMsR0FBRyxDQUFZLFNBQUMsQ0FBRCxHQUFDLENBQWdCLGFBQVEsQ0FBUixRQUFRLENBQ3ZDLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBSixLQUFHLENBQUMsQ0FBTyxLQUFZLENBQVosWUFBWSxDQUFDLDZCQUU5QixFQUZDLElBQUksQ0FHTCxDQUFDLElBQUksQ0FBQyxRQUFRLENBQVIsS0FBTyxDQUFDLENBQUMsUUFBUyxDQUFBSyxZQUFZLENBQUFhLFFBQVMsQ0FBQUQsSUFBSyxDQUFDLElBQUksRUFBRSxFQUF4RCxJQUFJLENBQ0osQ0FBQVosWUFBWSxDQUFBYyxlQUM0QixJQUF2Q2QsWUFBWSxDQUFBYyxlQUFnQixDQUFBbkIsTUFBTyxHQUFHLENBSXJDLElBSEMsQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFSLEtBQU8sQ0FBQyxDQUFDLHVCQUNXLENBQUFLLFlBQVksQ0FBQWMsZUFBZ0IsQ0FBQUYsSUFBSyxDQUFDLElBQUksRUFDaEUsRUFGQyxJQUFJLENBR1AsQ0FDSixFQVhDLEdBQUcsQ0FZTixDQUdDLENBQUFWLGFBQWEsQ0FBQWEsU0FBVSxDQUFBcEIsTUFBTyxHQUFHLENBWWpDLElBWEMsQ0FBQyxHQUFHLENBQVksU0FBQyxDQUFELEdBQUMsQ0FBZ0IsYUFBUSxDQUFSLFFBQVEsQ0FDdkMsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFKLEtBQUcsQ0FBQyxDQUFPLEtBQVksQ0FBWixZQUFZLENBQUMsOEJBRTlCLEVBRkMsSUFBSSxDQUdMLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBUixLQUFPLENBQUMsQ0FBQyxTQUFVLENBQUFPLGFBQWEsQ0FBQWEsU0FBVSxDQUFBSCxJQUFLLENBQUMsSUFBSSxFQUFFLEVBQTNELElBQUksQ0FDSixDQUFBVixhQUFhLENBQUFjLGVBQWdCLENBQUFyQixNQUFPLEdBQUcsQ0FJdkMsSUFIQyxDQUFDLElBQUksQ0FBQyxRQUFRLENBQVIsS0FBTyxDQUFDLENBQUMsdUJBQ1csQ0FBQU8sYUFBYSxDQUFBYyxlQUFnQixDQUFBSixJQUFLLENBQUMsSUFBSSxFQUNqRSxFQUZDLElBQUksQ0FHUCxDQUNGLEVBVkMsR0FBRyxDQVdOLENBR0MsRUFBRVIsYUFBYSxDQUFBYSxZQUFzRCxJQUFyQ2IsYUFBYSxDQUFBYSxZQUFhLENBQUF0QixNQUFPLEdBQUcsQ0FFNUIsSUFEdENTLGFBQWEsQ0FBQWMsV0FDd0IsSUFBcENkLGFBQWEsQ0FBQWMsV0FBWSxDQUFBdkIsTUFBTyxHQUFHLENBbUJ0QyxLQWxCQyxDQUFDLEdBQUcsQ0FBWSxTQUFDLENBQUQsR0FBQyxDQUFnQixhQUFRLENBQVIsUUFBUSxDQUN2QyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUosS0FBRyxDQUFDLENBQU8sS0FBWSxDQUFaLFlBQVksQ0FBQyxvQkFFM0IsQ0FBQVosb0NBQW9DLENBQXFCLENBQUMsR0FBMUQsWUFBMEQsR0FBMUQsRUFBeUQsQ0FBRSxDQUM5RCxFQUhDLElBQUksQ0FJSixDQUFBcUIsYUFBYSxDQUFBYSxZQUN5QixJQUFyQ2IsYUFBYSxDQUFBYSxZQUFhLENBQUF0QixNQUFPLEdBQUcsQ0FJbkMsSUFIQyxDQUFDLElBQUksQ0FBQyxRQUFRLENBQVIsS0FBTyxDQUFDLENBQUMsU0FDSCxDQUFBUyxhQUFhLENBQUFhLFlBQWEsQ0FBQUwsSUFBSyxDQUFDLElBQUksRUFDaEQsRUFGQyxJQUFJLENBR1AsQ0FDRCxDQUFBUixhQUFhLENBQUFjLFdBQ3dCLElBQXBDZCxhQUFhLENBQUFjLFdBQVksQ0FBQXZCLE1BQU8sR0FBRyxDQUlsQyxJQUhDLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBUixLQUFPLENBQUMsQ0FBQyxRQUNKLENBQUFTLGFBQWEsQ0FBQWMsV0FBWSxDQUFBTixJQUFLLENBQUMsSUFBSSxFQUM5QyxFQUZDLElBQUksQ0FHUCxDQUNKLEVBakJDLEdBQUcsQ0FrQk4sQ0FHQyxDQUFBTixnQkFBK0MsSUFBM0JBLGdCQUFnQixDQUFBWCxNQUFPLEdBQUcsQ0FPOUMsSUFOQyxDQUFDLEdBQUcsQ0FBWSxTQUFDLENBQUQsR0FBQyxDQUFnQixhQUFRLENBQVIsUUFBUSxDQUN2QyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUosS0FBRyxDQUFDLENBQU8sS0FBWSxDQUFaLFlBQVksQ0FBQyxxQkFFOUIsRUFGQyxJQUFJLENBR0wsQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFSLEtBQU8sQ0FBQyxDQUFFLENBQUFXLGdCQUFnQixDQUFBTSxJQUFLLENBQUMsSUFBSSxFQUFFLEVBQTNDLElBQUksQ0FDUCxFQUxDLEdBQUcsQ0FNTixDQUdDLENBQUFGLG1CQUFtQixDQUFBZixNQUFPLEdBQUcsQ0FZN0IsSUFYQyxDQUFDLEdBQUcsQ0FBWSxTQUFDLENBQUQsR0FBQyxDQUFnQixhQUFRLENBQVIsUUFBUSxDQUN2QyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUosS0FBRyxDQUFDLENBQU8sS0FBUyxDQUFULFNBQVMsQ0FBQyxxREFFM0IsRUFGQyxJQUFJLENBR0wsQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFSLEtBQU8sQ0FBQyxDQUFDLHVDQUMyQixJQUFFLENBQ3pDLENBQUFlLG1CQUFtQixDQUFBUyxLQUFNLENBQUMsQ0FBQyxFQUFFLENBQUMsQ0FBQyxDQUFBUCxJQUFLLENBQUMsSUFBSSxFQUN6QyxDQUFBRixtQkFBbUIsQ0FBQWYsTUFBTyxHQUFHLENBQ2UsSUFENUMsS0FDTWUsbUJBQW1CLENBQUFmLE1BQU8sR0FBRyxDQUFDLFFBQU8sQ0FDOUMsRUFMQyxJQUFJLENBTVAsRUFWQyxHQUFHLENBV04sQ0FFQ0csYUFBVyxDQUNkLEVBNUZDLEdBQUcsQ0E0RkU7SUFBQWIsQ0FBQSxNQUFBYyxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBZCxDQUFBO0VBQUE7RUFBQSxPQTVGTmMsRUE0Rk07QUFBQTtBQTdISCxTQUFBRixNQUFBdUIsQ0FBQSxFQUFBQyxDQUFBO0VBQUEsT0FTRyxDQUFDLElBQUksQ0FBTUEsR0FBQyxDQUFEQSxFQUFBLENBQUMsQ0FBRSxRQUFRLENBQVIsS0FBTyxDQUFDLENBQ25CRCxFQUFBLENBQ0gsRUFGQyxJQUFJLENBRUU7QUFBQSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/components/sandbox/SandboxDependenciesTab.tsx`

**信息:**
- 行数: 120
- 大小: 17402 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../../ink.js';
import { getPlatform } from '../../utils/platform.js';
import type { SandboxDependencyCheck } from '../../utils/sandbox/sandbox-adapter.js';
type Props = {
  depCheck: SandboxDependencyCheck;
};
export function SandboxDependenciesTab(t0) {
  const $ = _c(24);
  const {
    depCheck
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = getPlatform();
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const platform = t1;
  const isMac = platform === "macos";
  let t2;
  if ($[1] !== depCheck.errors) {
    t2 = depCheck.errors.some(_temp);
    $[1] = depCheck.errors;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  const rgMissing = t2;
  let t3;
  if ($[3] !== depCheck.errors) {
    t3 = depCheck.errors.some(_temp2);
    $[3] = depCheck.errors;
    $[4] = t3;
  } else {
    t3 = $[4];
  }
  const bwrapMissing = t3;
  let t4;
  if ($[5] !== depCheck.errors) {
    t4 = depCheck.errors.some(_temp3);
    $[5] = depCheck.errors;
    $[6] = t4;
  } else {
    t4 = $[6];
  }
  const socatMissing = t4;
  const seccompMissing = depCheck.warnings.length > 0;

```

---


### `src/components/sandbox/SandboxDoctorSection.tsx`

**信息:**
- 行数: 46
- 大小: 6190 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, Text } from '../../ink.js';
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js';
export function SandboxDoctorSection() {
  const $ = _c(2);
  if (!SandboxManager.isSupportedPlatform()) {
    return null;
  }
  if (!SandboxManager.isSandboxEnabledInSettings()) {
    return null;
  }
  let t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = Symbol.for("react.early_return_sentinel");
    bb0: {
      const depCheck = SandboxManager.checkDependencies();
      const hasErrors = depCheck.errors.length > 0;
      const hasWarnings = depCheck.warnings.length > 0;
      if (!hasErrors && !hasWarnings) {
        t1 = null;
        break bb0;
      }
      const statusColor = hasErrors ? "error" as const : "warning" as const;
      const statusText = hasErrors ? "Missing dependencies" : "Available (with warnings)";
      t0 = <Box flexDirection="column"><Text bold={true}>Sandbox</Text><Text>└ Status: <Text color={statusColor}>{statusText}</Text></Text>{depCheck.errors.map(_temp)}{depCheck.warnings.map(_temp2)}{hasErrors && <Text dimColor={true}>└ Run /sandbox for install instructions</Text>}</Box>;
    }
    $[0] = t0;
    $[1] = t1;
  } else {
    t0 = $[0];
    t1 = $[1];
  }
  if (t1 !== Symbol.for("react.early_return_sentinel")) {
    return t1;
  }
  return t0;
}
function _temp2(w, i_0) {
  return <Text key={i_0} color="warning">└ {w}</Text>;
}
function _temp(e, i) {
  return <Text key={i} color="error">└ {e}</Text>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJveCIsIlRleHQiLCJTYW5kYm94TWFuYWdlciIsIlNhbmRib3hEb2N0b3JTZWN0aW9uIiwiJCIsIl9jIiwiaXNTdXBwb3J0ZWRQbGF0Zm9ybSIsImlzU2FuZGJveEVuYWJsZWRJblNldHRpbmdzIiwidDAiLCJ0MSIsIlN5bWJvbCIsImZvciIsImJiMCIsImRlcENoZWNrIiwiY2hlY2tEZXBlbmRlbmNpZXMiLCJoYXNFcnJvcnMiLCJlcnJvcnMiLCJsZW5ndGgiLCJoYXNXYXJuaW5ncyIsIndhcm5pbmdzIiwic3RhdHVzQ29sb3IiLCJjb25zdCIsInN0YXR1c1RleHQiLCJtYXAiLCJfdGVtcCIsIl90ZW1wMiIsInciLCJpXzAiLCJpIiwiZSJdLCJzb3VyY2VzIjpbIlNhbmRib3hEb2N0b3JTZWN0aW9uLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBCb3gsIFRleHQgfSBmcm9tICcuLi8uLi9pbmsuanMnXG5pbXBvcnQgeyBTYW5kYm94TWFuYWdlciB9IGZyb20gJy4uLy4uL3V0aWxzL3NhbmRib3gvc2FuZGJveC1hZGFwdGVyLmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gU2FuZGJveERvY3RvclNlY3Rpb24oKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgaWYgKCFTYW5kYm94TWFuYWdlci5pc1N1cHBvcnRlZFBsYXRmb3JtKCkpIHtcbiAgICByZXR1cm4gbnVsbFxuICB9XG5cbiAgaWYgKCFTYW5kYm94TWFuYWdlci5pc1NhbmRib3hFbmFibGVkSW5TZXR0aW5ncygpKSB7XG4gICAgcmV0dXJuIG51bGxcbiAgfVxuXG4gIGNvbnN0IGRlcENoZWNrID0gU2FuZGJveE1hbmFnZXIuY2hlY2tEZXBlbmRlbmNpZXMoKVxuICBjb25zdCBoYXNFcnJvcnMgPSBkZXBDaGVjay5lcnJvcnMubGVuZ3RoID4gMFxuICBjb25zdCBoYXNXYXJuaW5ncyA9IGRlcENoZWNrLndhcm5pbmdzLmxlbmd0aCA+IDBcblxuICBpZiAoIWhhc0Vycm9ycyAmJiAhaGFzV2FybmluZ3MpIHtcbiAgICByZXR1cm4gbnVsbFxuICB9XG5cbiAgY29uc3Qgc3RhdHVzQ29sb3IgPSBoYXNFcnJvcnMgPyAoJ2Vycm9yJyBhcyBjb25zdCkgOiAoJ3dhcm5pbmcnIGFzIGNvbnN0KVxuICBjb25zdCBzdGF0dXNUZXh0ID0gaGFzRXJyb3JzXG4gICAgPyAnTWlzc2luZyBkZXBlbmRlbmNpZXMnXG4gICAgOiAnQXZhaWxhYmxlICh3aXRoIHdhcm5pbmdzKSdcblxuICByZXR1cm4gKFxuICAgIDxCb3ggZmxleERpcmVjdGlvbj1cImNvbHVtblwiPlxuICAgICAgPFRleHQgYm9sZD5TYW5kYm94PC9UZXh0PlxuICAgICAgPFRleHQ+XG4gICAgICAgIOKUlCBTdGF0dXM6IDxUZXh0IGNvbG9yPXtzdGF0dXNDb2xvcn0+e3N0YXR1c1RleHR9PC9UZXh0PlxuICAgICAgPC9UZXh0PlxuICAgICAge2RlcENoZWNrLmVycm9ycy5tYXAoKGUsIGkpID0+IChcbiAgICAgICAgPFRleHQga2V5PXtpfSBjb2xvcj1cImVycm9yXCI+XG4gICAgICAgICAg4pSUIHtlfVxuICAgICAgICA8L1RleHQ+XG4gICAgICApKX1cbiAgICAgIHtkZXBDaGVjay53YXJuaW5ncy5tYXAoKHcsIGkpID0+IChcbiAgICAgICAgPFRleHQga2V5PXtpfSBjb2xvcj1cIndhcm5pbmdcIj5cbiAgICAgICAgICDilJQge3d9XG4gICAgICAgIDwvVGV4dD5cbiAgICAgICkpfVxuICAgICAge2hhc0Vycm9ycyAmJiAoXG4gICAgICAgIDxUZXh0IGRpbUNvbG9yPuKUlCBSdW4gL3NhbmRib3ggZm9yIGluc3RhbGwgaW5zdHJ1Y3Rpb25zPC9UZXh0PlxuICAgICAgKX1cbiAgICA8L0JveD5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiO0FBQUEsT0FBT0EsS0FBSyxNQUFNLE9BQU87QUFDekIsU0FBU0MsR0FBRyxFQUFFQyxJQUFJLFFBQVEsY0FBYztBQUN4QyxTQUFTQyxjQUFjLFFBQVEsd0NBQXdDO0FBRXZFLE9BQU8sU0FBQUMscUJBQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFDTCxJQUFJLENBQUNILGNBQWMsQ0FBQUksbUJBQW9CLENBQUMsQ0FBQztJQUFBLE9BQ2hDLElBQUk7RUFBQTtFQUdiLElBQUksQ0FBQ0osY0FBYyxDQUFBSywwQkFBMkIsQ0FBQyxDQUFDO0lBQUEsT0FDdkMsSUFBSTtFQUFBO0VBQ1osSUFBQUMsRUFBQTtFQUFBLElBQUFDLEVBQUE7RUFBQSxJQUFBTCxDQUFBLFFBQUFNLE1BQUEsQ0FBQUMsR0FBQTtJQU9RRixFQUFBLEdBQUFDLE1BQUksQ0FBQUMsR0FBQSxDQUFKLDZCQUFHLENBQUM7SUFBQUMsR0FBQTtNQUxiLE1BQUFDLFFBQUEsR0FBaUJYLGNBQWMsQ0FBQVksaUJBQWtCLENBQUMsQ0FBQztNQUNuRCxNQUFBQyxTQUFBLEdBQWtCRixRQUFRLENBQUFHLE1BQU8sQ0FBQUMsTUFBTyxHQUFHLENBQUM7TUFDNUMsTUFBQUMsV0FBQSxHQUFvQkwsUUFBUSxDQUFBTSxRQUFTLENBQUFGLE1BQU8sR0FBRyxDQUFDO01BRWhELElBQUksQ0FBQ0YsU0FBeUIsSUFBMUIsQ0FBZUcsV0FBVztRQUNyQlQsRUFBQSxPQUFJO1FBQUosTUFBQUcsR0FBQTtNQUFJO01BR2IsTUFBQVEsV0FBQSxHQUFvQkwsU0FBUyxHQUFJLE9BQU8sSUFBSU0sS0FBNkIsR0FBbkIsU0FBUyxJQUFJQSxLQUFNO01BQ3pFLE1BQUFDLFVBQUEsR0FBbUJQLFNBQVMsR0FBVCxzQkFFWSxHQUZaLDJCQUVZO01BRzdCUCxFQUFBLElBQUMsR0FBRyxDQUFlLGFBQVEsQ0FBUixRQUFRLENBQ3pCLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBSixLQUFHLENBQUMsQ0FBQyxPQUFPLEVBQWpCLElBQUksQ0FDTCxDQUFDLElBQUksQ0FBQyxVQUNNLENBQUMsSUFBSSxDQUFRWSxLQUFXLENBQVhBLFlBQVUsQ0FBQyxDQUFHRSxXQUFTLENBQUUsRUFBckMsSUFBSSxDQUNqQixFQUZDLElBQUksQ0FHSixDQUFBVCxRQUFRLENBQUFHLE1BQU8sQ0FBQU8sR0FBSSxDQUFDQyxLQUlwQixFQUNBLENBQUFYLFFBQVEsQ0FBQU0sUUFBUyxDQUFBSSxHQUFJLENBQUNFLE1BSXRCLEVBQ0EsQ0FBQVYsU0FFQSxJQURDLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBUixLQUFPLENBQUMsQ0FBQyx1Q0FBdUMsRUFBckQsSUFBSSxDQUNQLENBQ0YsRUFsQkMsR0FBRyxDQWtCRTtJQUFBO0lBQUFYLENBQUEsTUFBQUksRUFBQTtJQUFBSixDQUFBLE1BQUFLLEVBQUE7RUFBQTtJQUFBRCxFQUFBLEdBQUFKLENBQUE7SUFBQUssRUFBQSxHQUFBTCxDQUFBO0VBQUE7RUFBQSxJQUFBSyxFQUFBLEtBQUFDLE1BQUEsQ0FBQUMsR0FBQTtJQUFBLE9BQUFGLEVBQUE7RUFBQTtFQUFBLE9BbEJORCxFQWtCTTtBQUFBO0FBekNILFNBQUFpQixPQUFBQyxDQUFBLEVBQUFDLEdBQUE7RUFBQSxPQWtDQyxDQUFDLElBQUksQ0FBTUMsR0FBQyxDQUFEQSxJQUFBLENBQUMsQ0FBUSxLQUFTLENBQVQsU0FBUyxDQUFDLEVBQ3pCRixFQUFBLENBQ0wsRUFGQyxJQUFJLENBRUU7QUFBQTtBQXBDUixTQUFBRixNQUFBSyxDQUFBLEVBQUFELENBQUE7RUFBQSxPQTZCQyxDQUFDLElBQUksQ0FBTUEsR0FBQyxDQUFEQSxFQUFBLENBQUMsQ0FBUSxLQUFPLENBQVAsT0FBTyxDQUFDLEVBQ3ZCQyxFQUFBLENBQ0wsRUFGQyxJQUFJLENBRUU7QUFBQSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/components/sandbox/SandboxOverridesTab.tsx`

**信息:**
- 行数: 193
- 大小: 20473 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, color, Link, Text, useTheme } from '../../ink.js';
import type { CommandResultDisplay } from '../../types/command.js';
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js';
import { Select } from '../CustomSelect/select.js';
import { useTabHeaderFocus } from '../design-system/Tabs.js';
type Props = {
  onComplete: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
};
type OverrideMode = 'open' | 'closed';
export function SandboxOverridesTab(t0) {
  const $ = _c(5);
  const {
    onComplete
  } = t0;
  const isEnabled = SandboxManager.isSandboxingEnabled();
  const isLocked = SandboxManager.areSandboxSettingsLockedByPolicy();
  const currentAllowUnsandboxed = SandboxManager.areUnsandboxedCommandsAllowed();
  if (!isEnabled) {
    let t1;
    if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
      t1 = <Box flexDirection="column" paddingY={1}><Text color="subtle">Sandbox is not enabled. Enable sandbox to configure override settings.</Text></Box>;
      $[0] = t1;
    } else {
      t1 = $[0];
    }
    return t1;
  }
  if (isLocked) {
    let t1;
    if ($[1] === Symbol.for("react.memo_cache_sentinel")) {
      t1 = <Text color="subtle">Override settings are managed by a higher-priority configuration and cannot be changed locally.</Text>;
      $[1] = t1;
    } else {
      t1 = $[1];
    }
    let t2;
    if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
      t2 = <Box flexDirection="column" paddingY={1}>{t1}<Box marginTop={1}><Text dimColor={true}>Current setting:{" "}{currentAllowUnsandboxed ? "Allow unsandboxed fallback" : "Strict sandbox mode"}</Text></Box></Box>;
      $[2] = t2;
    } else {
      t2 = $[2];
    }
    return t2;
  }
  let t1;
  if ($[3] !== onComplete) {

```

---


### `src/components/sandbox/SandboxSettings.tsx`

**信息:**
- 行数: 296
- 大小: 29988 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Box, color, Link, Text, useTheme } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import type { CommandResultDisplay } from '../../types/command.js';
import type { SandboxDependencyCheck } from '../../utils/sandbox/sandbox-adapter.js';
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js';
import { getSettings_DEPRECATED } from '../../utils/settings/settings.js';
import { Select } from '../CustomSelect/select.js';
import { Pane } from '../design-system/Pane.js';
import { Tab, Tabs, useTabHeaderFocus } from '../design-system/Tabs.js';
import { SandboxConfigTab } from './SandboxConfigTab.js';
import { SandboxDependenciesTab } from './SandboxDependenciesTab.js';
import { SandboxOverridesTab } from './SandboxOverridesTab.js';
type Props = {
  onComplete: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  depCheck: SandboxDependencyCheck;
};
type SandboxMode = 'auto-allow' | 'regular' | 'disabled';
export function SandboxSettings(t0) {
  const $ = _c(34);
  const {
    onComplete,
    depCheck
  } = t0;
  const [theme] = useTheme();
  const currentEnabled = SandboxManager.isSandboxingEnabled();
  const currentAutoAllow = SandboxManager.isAutoAllowBashIfSandboxedEnabled();
  const hasWarnings = depCheck.warnings.length > 0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = getSettings_DEPRECATED();
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const settings = t1;
  const allowAllUnixSockets = settings.sandbox?.network?.allowAllUnixSockets;
  const showSocketWarning = hasWarnings && !allowAllUnixSockets;
  const getCurrentMode = () => {
    if (!currentEnabled) {
      return "disabled";
    }
    if (currentAutoAllow) {
      return "auto-allow";
    }
    return "regular";
  };

```

---


### `src/components/shell/ExpandShellOutputContext.tsx`

**信息:**
- 行数: 36
- 大小: 3504 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useContext } from 'react';

/**
 * Context to indicate that shell output should be shown in full (not truncated).
 * Used to auto-expand the most recent user `!` command output.
 *
 * This follows the same pattern as MessageResponseContext and SubAgentContext -
 * a boolean context that child components can check to modify their behavior.
 */
const ExpandShellOutputContext = React.createContext(false);
export function ExpandShellOutputProvider(t0) {
  const $ = _c(2);
  const {
    children
  } = t0;
  let t1;
  if ($[0] !== children) {
    t1 = <ExpandShellOutputContext.Provider value={true}>{children}</ExpandShellOutputContext.Provider>;
    $[0] = children;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  return t1;
}

/**
 * Returns true if this component is rendered inside an ExpandShellOutputProvider,
 * indicating the shell output should be shown in full rather than truncated.
 */
export function useExpandShellOutput() {
  return useContext(ExpandShellOutputContext);
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsInVzZUNvbnRleHQiLCJFeHBhbmRTaGVsbE91dHB1dENvbnRleHQiLCJjcmVhdGVDb250ZXh0IiwiRXhwYW5kU2hlbGxPdXRwdXRQcm92aWRlciIsInQwIiwiJCIsIl9jIiwiY2hpbGRyZW4iLCJ0MSIsInVzZUV4cGFuZFNoZWxsT3V0cHV0Il0sInNvdXJjZXMiOlsiRXhwYW5kU2hlbGxPdXRwdXRDb250ZXh0LnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IHVzZUNvbnRleHQgfSBmcm9tICdyZWFjdCdcblxuLyoqXG4gKiBDb250ZXh0IHRvIGluZGljYXRlIHRoYXQgc2hlbGwgb3V0cHV0IHNob3VsZCBiZSBzaG93biBpbiBmdWxsIChub3QgdHJ1bmNhdGVkKS5cbiAqIFVzZWQgdG8gYXV0by1leHBhbmQgdGhlIG1vc3QgcmVjZW50IHVzZXIgYCFgIGNvbW1hbmQgb3V0cHV0LlxuICpcbiAqIFRoaXMgZm9sbG93cyB0aGUgc2FtZSBwYXR0ZXJuIGFzIE1lc3NhZ2VSZXNwb25zZUNvbnRleHQgYW5kIFN1YkFnZW50Q29udGV4dCAtXG4gKiBhIGJvb2xlYW4gY29udGV4dCB0aGF0IGNoaWxkIGNvbXBvbmVudHMgY2FuIGNoZWNrIHRvIG1vZGlmeSB0aGVpciBiZWhhdmlvci5cbiAqL1xuY29uc3QgRXhwYW5kU2hlbGxPdXRwdXRDb250ZXh0ID0gUmVhY3QuY3JlYXRlQ29udGV4dChmYWxzZSlcblxuZXhwb3J0IGZ1bmN0aW9uIEV4cGFuZFNoZWxsT3V0cHV0UHJvdmlkZXIoe1xuICBjaGlsZHJlbixcbn06IHtcbiAgY2hpbGRyZW46IFJlYWN0LlJlYWN0Tm9kZVxufSk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIHJldHVybiAoXG4gICAgPEV4cGFuZFNoZWxsT3V0cHV0Q29udGV4dC5Qcm92aWRlciB2YWx1ZT17dHJ1ZX0+XG4gICAgICB7Y2hpbGRyZW59XG4gICAgPC9FeHBhbmRTaGVsbE91dHB1dENvbnRleHQuUHJvdmlkZXI+XG4gIClcbn1cblxuLyoqXG4gKiBSZXR1cm5zIHRydWUgaWYgdGhpcyBjb21wb25lbnQgaXMgcmVuZGVyZWQgaW5zaWRlIGFuIEV4cGFuZFNoZWxsT3V0cHV0UHJvdmlkZXIsXG4gKiBpbmRpY2F0aW5nIHRoZSBzaGVsbCBvdXRwdXQgc2hvdWxkIGJlIHNob3duIGluIGZ1bGwgcmF0aGVyIHRoYW4gdHJ1bmNhdGVkLlxuICovXG5leHBvcnQgZnVuY3Rpb24gdXNlRXhwYW5kU2hlbGxPdXRwdXQoKTogYm9vbGVhbiB7XG4gIHJldHVybiB1c2VDb250ZXh0KEV4cGFuZFNoZWxsT3V0cHV0Q29udGV4dClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsVUFBVSxRQUFRLE9BQU87O0FBRWxDO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsTUFBTUMsd0JBQXdCLEdBQUdGLEtBQUssQ0FBQ0csYUFBYSxDQUFDLEtBQUssQ0FBQztBQUUzRCxPQUFPLFNBQUFDLDBCQUFBQyxFQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQW1DO0lBQUFDO0VBQUEsSUFBQUgsRUFJekM7RUFBQSxJQUFBSSxFQUFBO0VBQUEsSUFBQUgsQ0FBQSxRQUFBRSxRQUFBO0lBRUdDLEVBQUEsc0NBQTBDLEtBQUksQ0FBSixLQUFHLENBQUMsQ0FDM0NELFNBQU8sQ0FDVixvQ0FBb0M7SUFBQUYsQ0FBQSxNQUFBRSxRQUFBO0lBQUFGLENBQUEsTUFBQUcsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUgsQ0FBQTtFQUFBO0VBQUEsT0FGcENHLEVBRW9DO0FBQUE7O0FBSXhDO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsT0FBTyxTQUFBQyxxQkFBQTtFQUFBLE9BQ0VULFVBQVUsQ0FBQ0Msd0JBQXdCLENBQUM7QUFBQSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/components/shell/OutputLine.tsx`

**信息:**
- 行数: 118
- 大小: 14388 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { useMemo } from 'react';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { Ansi, Text } from '../../ink.js';
import { createHyperlink } from '../../utils/hyperlink.js';
import { jsonParse, jsonStringify } from '../../utils/slowOperations.js';
import { renderTruncatedContent } from '../../utils/terminal.js';
import { MessageResponse } from '../MessageResponse.js';
import { InVirtualListContext } from '../messageActions.js';
import { useExpandShellOutput } from './ExpandShellOutputContext.js';
export function tryFormatJson(line: string): string {
  try {
    const parsed = jsonParse(line);
    const stringified = jsonStringify(parsed);

    // Check if precision was lost during JSON round-trip
    // This happens when large integers exceed Number.MAX_SAFE_INTEGER
    // We normalize both strings by removing whitespace and unnecessary
    // escapes (\/ is valid but optional in JSON) for comparison
    const normalizedOriginal = line.replace(/\\\//g, '/').replace(/\s+/g, '');
    const normalizedStringified = stringified.replace(/\s+/g, '');
    if (normalizedOriginal !== normalizedStringified) {
      // Precision loss detected - return original line unformatted
      return line;
    }
    return jsonStringify(parsed, null, 2);
  } catch {
    return line;
  }
}
const MAX_JSON_FORMAT_LENGTH = 10_000;
export function tryJsonFormatContent(content: string): string {
  if (content.length > MAX_JSON_FORMAT_LENGTH) {
    return content;
  }
  const allLines = content.split('\n');
  return allLines.map(tryFormatJson).join('\n');
}

// Match http(s) URLs inside JSON string values. Conservative: no quotes,
// no whitespace, no trailing comma/brace that'd be JSON structure.
const URL_IN_JSON = /https?:\/\/[^\s"'<>\\]+/g;
export function linkifyUrlsInText(content: string): string {
  return content.replace(URL_IN_JSON, url => createHyperlink(url));
}
export function OutputLine(t0) {
  const $ = _c(11);
  const {
    content,

```

---


### `src/components/shell/ShellProgressMessage.tsx`

**信息:**
- 行数: 150
- 大小: 14373 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import stripAnsi from 'strip-ansi';
import { Box, Text } from '../../ink.js';
import { formatFileSize } from '../../utils/format.js';
import { MessageResponse } from '../MessageResponse.js';
import { OffscreenFreeze } from '../OffscreenFreeze.js';
import { ShellTimeDisplay } from './ShellTimeDisplay.js';
type Props = {
  output: string;
  fullOutput: string;
  elapsedTimeSeconds?: number;
  totalLines?: number;
  totalBytes?: number;
  timeoutMs?: number;
  taskId?: string;
  verbose: boolean;
};
export function ShellProgressMessage(t0) {
  const $ = _c(30);
  const {
    output,
    fullOutput,
    elapsedTimeSeconds,
    totalLines,
    totalBytes,
    timeoutMs,
    verbose
  } = t0;
  let t1;
  if ($[0] !== fullOutput) {
    t1 = stripAnsi(fullOutput.trim());
    $[0] = fullOutput;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const strippedFullOutput = t1;
  let lines;
  let t2;
  if ($[2] !== output || $[3] !== strippedFullOutput || $[4] !== verbose) {
    const strippedOutput = stripAnsi(output.trim());
    lines = strippedOutput.split("\n").filter(_temp);
    t2 = verbose ? strippedFullOutput : lines.slice(-5).join("\n");
    $[2] = output;
    $[3] = strippedFullOutput;
    $[4] = verbose;
    $[5] = lines;
    $[6] = t2;
  } else {

```

---


### `src/components/shell/ShellTimeDisplay.tsx`

**信息:**
- 行数: 74
- 大小: 5229 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { Text } from '../../ink.js';
import { formatDuration } from '../../utils/format.js';
type Props = {
  elapsedTimeSeconds?: number;
  timeoutMs?: number;
};
export function ShellTimeDisplay(t0) {
  const $ = _c(10);
  const {
    elapsedTimeSeconds,
    timeoutMs
  } = t0;
  if (elapsedTimeSeconds === undefined && !timeoutMs) {
    return null;
  }
  let t1;
  if ($[0] !== timeoutMs) {
    t1 = timeoutMs ? formatDuration(timeoutMs, {
      hideTrailingZeros: true
    }) : undefined;
    $[0] = timeoutMs;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const timeout = t1;
  if (elapsedTimeSeconds === undefined) {
    const t2 = `(timeout ${timeout})`;
    let t3;
    if ($[2] !== t2) {
      t3 = <Text dimColor={true}>{t2}</Text>;
      $[2] = t2;
      $[3] = t3;
    } else {
      t3 = $[3];
    }
    return t3;
  }
  const t2 = elapsedTimeSeconds * 1000;
  let t3;
  if ($[4] !== t2) {
    t3 = formatDuration(t2);
    $[4] = t2;
    $[5] = t3;
  } else {
    t3 = $[5];
  }
  const elapsed = t3;

```

---


### `src/components/skills/SkillsMenu.tsx`

**信息:**
- 行数: 237
- 大小: 27508 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import capitalize from 'lodash-es/capitalize.js';
import * as React from 'react';
import { useMemo } from 'react';
import { type Command, type CommandBase, type CommandResultDisplay, getCommandName, type PromptCommand } from '../../commands.js';
import { Box, Text } from '../../ink.js';
import { estimateSkillFrontmatterTokens, getSkillsPath } from '../../skills/loadSkillsDir.js';
import { getDisplayPath } from '../../utils/file.js';
import { formatTokens } from '../../utils/format.js';
import { getSettingSourceName, type SettingSource } from '../../utils/settings/constants.js';
import { plural } from '../../utils/stringUtils.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Dialog } from '../design-system/Dialog.js';

// Skills are always PromptCommands with CommandBase properties
type SkillCommand = CommandBase & PromptCommand;
type SkillSource = SettingSource | 'plugin' | 'mcp';
type Props = {
  onExit: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  commands: Command[];
};
function getSourceTitle(source: SkillSource): string {
  if (source === 'plugin') {
    return 'Plugin skills';
  }
  if (source === 'mcp') {
    return 'MCP skills';
  }
  return `${capitalize(getSettingSourceName(source))} skills`;
}
function getSourceSubtitle(source: SkillSource, skills: SkillCommand[]): string | undefined {
  // MCP skills show server names; file-based skills show filesystem paths.
  // Skill names are `<server>:<skill>`, not `mcp__<server>__…`.
  if (source === 'mcp') {
    const servers = [...new Set(skills.map(s => {
      const idx = s.name.indexOf(':');
      return idx > 0 ? s.name.slice(0, idx) : null;
    }).filter((n): n is string => n != null))];
    return servers.length > 0 ? servers.join(', ') : undefined;
  }
  const skillsPath = getDisplayPath(getSkillsPath(source, 'skills'));
  const hasCommandsSkills = skills.some(s => s.loadedFrom === 'commands_DEPRECATED');
  return hasCommandsSkills ? `${skillsPath}, ${getDisplayPath(getSkillsPath(source, 'commands'))}` : skillsPath;
}
export function SkillsMenu(t0) {
  const $ = _c(35);
  const {
    onExit,

```

---


### `src/components/tasks/AsyncAgentDetailDialog.tsx`

**信息:**
- 行数: 229
- 大小: 29805 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useMemo } from 'react';
import type { DeepImmutable } from 'src/types/utils.js';
import { useElapsedTime } from '../../hooks/useElapsedTime.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text, useTheme } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import { getEmptyToolPermissionContext } from '../../Tool.js';
import type { LocalAgentTaskState } from '../../tasks/LocalAgentTask/LocalAgentTask.js';
import { getTools } from '../../tools.js';
import { formatNumber } from '../../utils/format.js';
import { extractTag } from '../../utils/messages.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import { UserPlanMessage } from '../messages/UserPlanMessage.js';
import { renderToolActivity } from './renderToolActivity.js';
import { getTaskStatusColor, getTaskStatusIcon } from './taskStatusUtils.js';
type Props = {
  agent: DeepImmutable<LocalAgentTaskState>;
  onDone: () => void;
  onKillAgent?: () => void;
  onBack?: () => void;
};
export function AsyncAgentDetailDialog(t0) {
  const $ = _c(54);
  const {
    agent,
    onDone,
    onKillAgent,
    onBack
  } = t0;
  const [theme] = useTheme();
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = getTools(getEmptyToolPermissionContext());
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const tools = t1;
  const elapsedTime = useElapsedTime(agent.startTime, agent.status === "running", 1000, agent.totalPausedMs ?? 0);
  let t2;
  if ($[1] !== onDone) {
    t2 = {
      "confirm:yes": onDone
    };
    $[1] = onDone;
    $[2] = t2;
  } else {

```

---


### `src/components/tasks/BackgroundTask.tsx`

**信息:**
- 行数: 345
- 大小: 31248 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Text } from 'src/ink.js';
import type { BackgroundTaskState } from 'src/tasks/types.js';
import type { DeepImmutable } from 'src/types/utils.js';
import { truncate } from 'src/utils/format.js';
import { toInkColor } from 'src/utils/ink.js';
import { plural } from 'src/utils/stringUtils.js';
import { DIAMOND_FILLED, DIAMOND_OPEN } from '../../constants/figures.js';
import { RemoteSessionProgress } from './RemoteSessionProgress.js';
import { ShellProgress, TaskStatusText } from './ShellProgress.js';
import { describeTeammateActivity } from './taskStatusUtils.js';
type Props = {
  task: DeepImmutable<BackgroundTaskState>;
  maxActivityWidth?: number;
};
export function BackgroundTask(t0) {
  const $ = _c(92);
  const {
    task,
    maxActivityWidth
  } = t0;
  const activityLimit = maxActivityWidth ?? 40;
  switch (task.type) {
    case "local_bash":
      {
        const t1 = task.kind === "monitor" ? task.description : task.command;
        let t2;
        if ($[0] !== activityLimit || $[1] !== t1) {
          t2 = truncate(t1, activityLimit, true);
          $[0] = activityLimit;
          $[1] = t1;
          $[2] = t2;
        } else {
          t2 = $[2];
        }
        let t3;
        if ($[3] !== task) {
          t3 = <ShellProgress shell={task} />;
          $[3] = task;
          $[4] = t3;
        } else {
          t3 = $[4];
        }
        let t4;
        if ($[5] !== t2 || $[6] !== t3) {
          t4 = <Text>{t2}{" "}{t3}</Text>;
          $[5] = t2;
          $[6] = t3;
          $[7] = t4;

```

---


### `src/components/tasks/BackgroundTaskStatus.tsx`

**信息:**
- 行数: 429
- 大小: 43375 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import * as React from 'react';
import { useMemo, useState } from 'react';
import { useTerminalSize } from 'src/hooks/useTerminalSize.js';
import { stringWidth } from 'src/ink/stringWidth.js';
import { useAppState, useSetAppState } from 'src/state/AppState.js';
import { enterTeammateView, exitTeammateView } from 'src/state/teammateViewHelpers.js';
import { isPanelAgentTask } from 'src/tasks/LocalAgentTask/LocalAgentTask.js';
import { getPillLabel, pillNeedsCta } from 'src/tasks/pillLabel.js';
import { type BackgroundTaskState, isBackgroundTask, type TaskState } from 'src/tasks/types.js';
import { calculateHorizontalScrollWindow } from 'src/utils/horizontalScroll.js';
import { Box, Text } from '../../ink.js';
import { AGENT_COLOR_TO_THEME_COLOR, AGENT_COLORS, type AgentColorName } from '../../tools/AgentTool/agentColorManager.js';
import type { Theme } from '../../utils/theme.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import { shouldHideTasksFooter } from './taskStatusUtils.js';
type Props = {
  tasksSelected: boolean;
  isViewingTeammate?: boolean;
  teammateFooterIndex?: number;
  isLeaderIdle?: boolean;
  onOpenDialog?: (taskId?: string) => void;
};
export function BackgroundTaskStatus(t0) {
  const $ = _c(48);
  const {
    tasksSelected,
    isViewingTeammate,
    teammateFooterIndex: t1,
    isLeaderIdle: t2,
    onOpenDialog
  } = t0;
  const teammateFooterIndex = t1 === undefined ? 0 : t1;
  const isLeaderIdle = t2 === undefined ? false : t2;
  const setAppState = useSetAppState();
  const {
    columns
  } = useTerminalSize();
  const tasks = useAppState(_temp);
  const viewingAgentTaskId = useAppState(_temp2);
  let t3;
  if ($[0] !== tasks) {
    t3 = (Object.values(tasks ?? {}) as TaskState[]).filter(_temp3);
    $[0] = tasks;
    $[1] = t3;
  } else {
    t3 = $[1];
  }
  const runningTasks = t3;

```

---


### `src/components/tasks/BackgroundTasksDialog.tsx`

**信息:**
- 行数: 652
- 大小: 116395 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import figures from 'figures';
import React, { type ReactNode, useEffect, useEffectEvent, useMemo, useRef, useState } from 'react';
import { isCoordinatorMode } from 'src/coordinator/coordinatorMode.js';
import { useTerminalSize } from 'src/hooks/useTerminalSize.js';
import { useAppState, useSetAppState } from 'src/state/AppState.js';
import { enterTeammateView, exitTeammateView } from 'src/state/teammateViewHelpers.js';
import type { ToolUseContext } from 'src/Tool.js';
import { DreamTask, type DreamTaskState } from 'src/tasks/DreamTask/DreamTask.js';
import { InProcessTeammateTask } from 'src/tasks/InProcessTeammateTask/InProcessTeammateTask.js';
import type { InProcessTeammateTaskState } from 'src/tasks/InProcessTeammateTask/types.js';
import type { LocalAgentTaskState } from 'src/tasks/LocalAgentTask/LocalAgentTask.js';
import { LocalAgentTask } from 'src/tasks/LocalAgentTask/LocalAgentTask.js';
import type { LocalShellTaskState } from 'src/tasks/LocalShellTask/guards.js';
import { LocalShellTask } from 'src/tasks/LocalShellTask/LocalShellTask.js';
// Type import is erased at build time — safe even though module is ant-gated.
import type { LocalWorkflowTaskState } from 'src/tasks/LocalWorkflowTask/LocalWorkflowTask.js';
import type { MonitorMcpTaskState } from 'src/tasks/MonitorMcpTask/MonitorMcpTask.js';
import { RemoteAgentTask, type RemoteAgentTaskState } from 'src/tasks/RemoteAgentTask/RemoteAgentTask.js';
import { type BackgroundTaskState, isBackgroundTask, type TaskState } from 'src/tasks/types.js';
import type { DeepImmutable } from 'src/types/utils.js';
import { intersperse } from 'src/utils/array.js';
import { TEAM_LEAD_NAME } from 'src/utils/swarm/constants.js';
import { stopUltraplan } from '../../commands/ultraplan.js';
import type { CommandResultDisplay } from '../../commands.js';
import { useRegisterOverlay } from '../../context/overlayContext.js';
import type { ExitState } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import { useShortcutDisplay } from '../../keybindings/useShortcutDisplay.js';
import { count } from '../../utils/array.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import { AsyncAgentDetailDialog } from './AsyncAgentDetailDialog.js';
import { BackgroundTask as BackgroundTaskComponent } from './BackgroundTask.js';
import { DreamDetailDialog } from './DreamDetailDialog.js';
import { InProcessTeammateDetailDialog } from './InProcessTeammateDetailDialog.js';
import { RemoteSessionDetailDialog } from './RemoteSessionDetailDialog.js';
import { ShellDetailDialog } from './ShellDetailDialog.js';
type ViewState = {
  mode: 'list';
} | {
  mode: 'detail';
  itemId: string;
};
type Props = {
  onDone: (result?: string, options?: {

```

---


### `src/components/tasks/DreamDetailDialog.tsx`

**信息:**
- 行数: 251
- 大小: 25889 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import type { DeepImmutable } from 'src/types/utils.js';
import { useElapsedTime } from '../../hooks/useElapsedTime.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import type { DreamTaskState } from '../../tasks/DreamTask/DreamTask.js';
import { plural } from '../../utils/stringUtils.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
type Props = {
  task: DeepImmutable<DreamTaskState>;
  onDone: () => void;
  onBack?: () => void;
  onKill?: () => void;
};

// How many recent turns to render. Earlier turns collapse to a count.
const VISIBLE_TURNS = 6;
export function DreamDetailDialog(t0) {
  const $ = _c(70);
  const {
    task,
    onDone,
    onBack,
    onKill
  } = t0;
  const elapsedTime = useElapsedTime(task.startTime, task.status === "running", 1000, 0);
  let t1;
  if ($[0] !== onDone) {
    t1 = {
      "confirm:yes": onDone
    };
    $[0] = onDone;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t2 = {
      context: "Confirmation"
    };
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  useKeybindings(t1, t2);

```

---


### `src/components/tasks/InProcessTeammateDetailDialog.tsx`

**信息:**
- 行数: 266
- 大小: 31018 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useMemo } from 'react';
import type { DeepImmutable } from 'src/types/utils.js';
import { useElapsedTime } from '../../hooks/useElapsedTime.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text, useTheme } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import { getEmptyToolPermissionContext } from '../../Tool.js';
import type { InProcessTeammateTaskState } from '../../tasks/InProcessTeammateTask/types.js';
import { getTools } from '../../tools.js';
import { formatNumber, truncateToWidth } from '../../utils/format.js';
import { toInkColor } from '../../utils/ink.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import { renderToolActivity } from './renderToolActivity.js';
import { describeTeammateActivity } from './taskStatusUtils.js';
type Props = {
  teammate: DeepImmutable<InProcessTeammateTaskState>;
  onDone: () => void;
  onKill?: () => void;
  onBack?: () => void;
  onForeground?: () => void;
};
export function InProcessTeammateDetailDialog(t0) {
  const $ = _c(63);
  const {
    teammate,
    onDone,
    onKill,
    onBack,
    onForeground
  } = t0;
  const [theme] = useTheme();
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = getTools(getEmptyToolPermissionContext());
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const tools = t1;
  const elapsedTime = useElapsedTime(teammate.startTime, teammate.status === "running", 1000, teammate.totalPausedMs ?? 0);
  let t2;
  if ($[1] !== onDone) {
    t2 = {
      "confirm:yes": onDone
    };
    $[1] = onDone;
    $[2] = t2;

```

---


### `src/components/tasks/MonitorMcpDetailDialog.tsx`

**信息:**
- 行数: 3
- 大小: 59 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function MonitorMcpDetailDialog() {
  return null
}

```

---


### `src/components/tasks/RemoteSessionDetailDialog.tsx`

**信息:**
- 行数: 904
- 大小: 96185 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React, { useMemo, useState } from 'react';
import type { SDKMessage } from 'src/entrypoints/agentSdkTypes.js';
import type { ToolUseContext } from 'src/Tool.js';
import type { DeepImmutable } from 'src/types/utils.js';
import type { CommandResultDisplay } from '../../commands.js';
import { DIAMOND_FILLED, DIAMOND_OPEN } from '../../constants/figures.js';
import { useElapsedTime } from '../../hooks/useElapsedTime.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Link, Text } from '../../ink.js';
import type { RemoteAgentTaskState } from '../../tasks/RemoteAgentTask/RemoteAgentTask.js';
import { getRemoteTaskSessionUrl } from '../../tasks/RemoteAgentTask/RemoteAgentTask.js';
import { AGENT_TOOL_NAME, LEGACY_AGENT_TOOL_NAME } from '../../tools/AgentTool/constants.js';
import { ASK_USER_QUESTION_TOOL_NAME } from '../../tools/AskUserQuestionTool/prompt.js';
import { EXIT_PLAN_MODE_V2_TOOL_NAME } from '../../tools/ExitPlanModeTool/constants.js';
import { openBrowser } from '../../utils/browser.js';
import { errorMessage } from '../../utils/errors.js';
import { formatDuration, truncateToWidth } from '../../utils/format.js';
import { toInternalMessages } from '../../utils/messages/mappers.js';
import { EMPTY_LOOKUPS, normalizeMessages } from '../../utils/messages.js';
import { plural } from '../../utils/stringUtils.js';
import { teleportResumeCodeSession } from '../../utils/teleport.js';
import { Select } from '../CustomSelect/select.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
import { Message } from '../Message.js';
import { formatReviewStageCounts, RemoteSessionProgress } from './RemoteSessionProgress.js';
type Props = {
  session: DeepImmutable<RemoteAgentTaskState>;
  toolUseContext: ToolUseContext;
  onDone: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  onBack?: () => void;
  onKill?: () => void;
};

// Compact one-line summary: tool name + first meaningful string arg.
// Lighter than tool.renderToolUseMessage (no registry lookup / schema parse).
// Collapses whitespace so multi-line inputs (e.g. Bash command text)
// render on one line.
export function formatToolUseSummary(name: string, input: unknown): string {
  // plan_ready phase is only reached via ExitPlanMode tool
  if (name === EXIT_PLAN_MODE_V2_TOOL_NAME) {
    return 'Review the plan in Claude Code on the web';
  }
  if (!input || typeof input !== 'object') return name;
  // AskUserQuestion: show the question text as a CTA, not the tool name.

```

---


### `src/components/tasks/RemoteSessionProgress.tsx`

**信息:**
- 行数: 243
- 大小: 27859 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { useRef } from 'react';
import type { RemoteAgentTaskState } from 'src/tasks/RemoteAgentTask/RemoteAgentTask.js';
import type { DeepImmutable } from 'src/types/utils.js';
import { DIAMOND_FILLED, DIAMOND_OPEN } from '../../constants/figures.js';
import { useSettings } from '../../hooks/useSettings.js';
import { Text, useAnimationFrame } from '../../ink.js';
import { count } from '../../utils/array.js';
import { getRainbowColor } from '../../utils/thinking.js';
const TICK_MS = 80;
type ReviewStage = NonNullable<NonNullable<RemoteAgentTaskState['reviewProgress']>['stage']>;

/**
 * Stage-appropriate counts line for a running review. Shared between the
 * one-line pill (below) and RemoteSessionDetailDialog's reviewCountsLine so
 * the two can't drift — they have historically disagreed on whether to show
 * refuted counts and what to call the synthesizing stage.
 *
 * Canonical behavior: word labels (not ✓/✗), hide refuted when 0, "deduping"
 * for the synthesizing stage (matches STAGE_LABELS in the detail dialog).
 */
export function formatReviewStageCounts(stage: ReviewStage | undefined, found: number, verified: number, refuted: number): string {
  // Pre-stage orchestrator images don't write the stage field.
  if (!stage) return `${found} found · ${verified} verified`;
  if (stage === 'synthesizing') {
    const parts = [`${verified} verified`];
    if (refuted > 0) parts.push(`${refuted} refuted`);
    parts.push('deduping');
    return parts.join(' · ');
  }
  if (stage === 'verifying') {
    const parts = [`${found} found`, `${verified} verified`];
    if (refuted > 0) parts.push(`${refuted} refuted`);
    return parts.join(' · ');
  }
  // stage === 'finding'
  return found > 0 ? `${found} found` : 'finding';
}

// Per-character rainbow gradient, same treatment as the ultraplan keyword.
// The phase offset lets the gradient cycle — so the colors sweep along the
// text on each animation frame instead of being static.
function RainbowText(t0) {
  const $ = _c(5);
  const {
    text,
    phase: t1
  } = t0;
  const phase = t1 === undefined ? 0 : t1;
  let t2;

```

---


### `src/components/tasks/ShellDetailDialog.tsx`

**信息:**
- 行数: 404
- 大小: 39167 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { Suspense, use, useDeferredValue, useEffect, useState } from 'react';
import type { DeepImmutable } from 'src/types/utils.js';
import type { CommandResultDisplay } from '../../commands.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box, Text } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import type { LocalShellTaskState } from '../../tasks/LocalShellTask/guards.js';
import { formatDuration, formatFileSize, truncateToWidth } from '../../utils/format.js';
import { tailFile } from '../../utils/fsOperations.js';
import { getTaskOutputPath } from '../../utils/task/diskOutput.js';
import { Byline } from '../design-system/Byline.js';
import { Dialog } from '../design-system/Dialog.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
type Props = {
  shell: DeepImmutable<LocalShellTaskState>;
  onDone: (result?: string, options?: {
    display?: CommandResultDisplay;
  }) => void;
  onKillShell?: () => void;
  onBack?: () => void;
};
const SHELL_DETAIL_TAIL_BYTES = 8192;
type TaskOutputResult = {
  content: string;
  bytesTotal: number;
};

/**
 * Read the tail of the task output file. Only reads the last few KB,
 * not the entire file.
 */
async function getTaskOutput(shell: DeepImmutable<LocalShellTaskState>): Promise<TaskOutputResult> {
  const path = getTaskOutputPath(shell.id);
  try {
    const result = await tailFile(path, SHELL_DETAIL_TAIL_BYTES);
    return {
      content: result.content,
      bytesTotal: result.bytesTotal
    };
  } catch {
    return {
      content: '',
      bytesTotal: 0
    };
  }
}
export function ShellDetailDialog(t0) {
  const $ = _c(57);

```

---


### `src/components/tasks/ShellProgress.tsx`

**信息:**
- 行数: 87
- 大小: 7004 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ReactNode } from 'react';
import React from 'react';
import { Text } from 'src/ink.js';
import type { TaskStatus } from 'src/Task.js';
import type { LocalShellTaskState } from 'src/tasks/LocalShellTask/guards.js';
import type { DeepImmutable } from 'src/types/utils.js';
type TaskStatusTextProps = {
  status: TaskStatus;
  label?: string;
  suffix?: string;
};
export function TaskStatusText(t0) {
  const $ = _c(4);
  const {
    status,
    label,
    suffix
  } = t0;
  const displayLabel = label ?? status;
  const color = status === "completed" ? "success" : status === "failed" ? "error" : status === "killed" ? "warning" : undefined;
  let t1;
  if ($[0] !== color || $[1] !== displayLabel || $[2] !== suffix) {
    t1 = <Text color={color} dimColor={true}>({displayLabel}{suffix})</Text>;
    $[0] = color;
    $[1] = displayLabel;
    $[2] = suffix;
    $[3] = t1;
  } else {
    t1 = $[3];
  }
  return t1;
}
export function ShellProgress(t0) {
  const $ = _c(4);
  const {
    shell
  } = t0;
  switch (shell.status) {
    case "completed":
      {
        let t1;
        if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
          t1 = <TaskStatusText status="completed" label="done" />;
          $[0] = t1;
        } else {
          t1 = $[0];
        }
        return t1;
      }

```

---


### `src/components/tasks/WorkflowDetailDialog.tsx`

**信息:**
- 行数: 3
- 大小: 57 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function WorkflowDetailDialog() {
  return null
}

```

---


### `src/components/tasks/renderToolActivity.tsx`

**信息:**
- 行数: 33
- 大小: 4414 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { Text } from '../../ink.js';
import type { Tools } from '../../Tool.js';
import { findToolByName } from '../../Tool.js';
import type { ToolActivity } from '../../tasks/LocalAgentTask/LocalAgentTask.js';
import type { ThemeName } from '../../utils/theme.js';
export function renderToolActivity(activity: ToolActivity, tools: Tools, theme: ThemeName): React.ReactNode {
  const tool = findToolByName(tools, activity.toolName);
  if (!tool) {
    return activity.toolName;
  }
  try {
    const parsed = tool.inputSchema.safeParse(activity.input);
    const parsedInput = parsed.success ? parsed.data : {};
    const userFacingName = tool.userFacingName(parsedInput);
    if (!userFacingName) {
      return activity.toolName;
    }
    const toolArgs = tool.renderToolUseMessage(parsedInput, {
      theme,
      verbose: false
    });
    if (toolArgs) {
      return <Text>
          {userFacingName}({toolArgs})
        </Text>;
    }
    return userFacingName;
  } catch {
    return activity.toolName;
  }
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlRleHQiLCJUb29scyIsImZpbmRUb29sQnlOYW1lIiwiVG9vbEFjdGl2aXR5IiwiVGhlbWVOYW1lIiwicmVuZGVyVG9vbEFjdGl2aXR5IiwiYWN0aXZpdHkiLCJ0b29scyIsInRoZW1lIiwiUmVhY3ROb2RlIiwidG9vbCIsInRvb2xOYW1lIiwicGFyc2VkIiwiaW5wdXRTY2hlbWEiLCJzYWZlUGFyc2UiLCJpbnB1dCIsInBhcnNlZElucHV0Iiwic3VjY2VzcyIsImRhdGEiLCJ1c2VyRmFjaW5nTmFtZSIsInRvb2xBcmdzIiwicmVuZGVyVG9vbFVzZU1lc3NhZ2UiLCJ2ZXJib3NlIl0sInNvdXJjZXMiOlsicmVuZGVyVG9vbEFjdGl2aXR5LnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBUZXh0IH0gZnJvbSAnLi4vLi4vaW5rLmpzJ1xuaW1wb3J0IHR5cGUgeyBUb29scyB9IGZyb20gJy4uLy4uL1Rvb2wuanMnXG5pbXBvcnQgeyBmaW5kVG9vbEJ5TmFtZSB9IGZyb20gJy4uLy4uL1Rvb2wuanMnXG5pbXBvcnQgdHlwZSB7IFRvb2xBY3Rpdml0eSB9IGZyb20gJy4uLy4uL3Rhc2tzL0xvY2FsQWdlbnRUYXNrL0xvY2FsQWdlbnRUYXNrLmpzJ1xuaW1wb3J0IHR5cGUgeyBUaGVtZU5hbWUgfSBmcm9tICcuLi8uLi91dGlscy90aGVtZS5qcydcblxuZXhwb3J0IGZ1bmN0aW9uIHJlbmRlclRvb2xBY3Rpdml0eShcbiAgYWN0aXZpdHk6IFRvb2xBY3Rpdml0eSxcbiAgdG9vbHM6IFRvb2xzLFxuICB0aGVtZTogVGhlbWVOYW1lLFxuKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgY29uc3QgdG9vbCA9IGZpbmRUb29sQnlOYW1lKHRvb2xzLCBhY3Rpdml0eS50b29sTmFtZSlcbiAgaWYgKCF0b29sKSB7XG4gICAgcmV0dXJuIGFjdGl2aXR5LnRvb2xOYW1lXG4gIH1cbiAgdHJ5IHtcbiAgICBjb25zdCBwYXJzZWQgPSB0b29sLmlucHV0U2NoZW1hLnNhZmVQYXJzZShhY3Rpdml0eS5pbnB1dClcbiAgICBjb25zdCBwYXJzZWRJbnB1dCA9IHBhcnNlZC5zdWNjZXNzID8gcGFyc2VkLmRhdGEgOiB7fVxuICAgIGNvbnN0IHVzZXJGYWNpbmdOYW1lID0gdG9vbC51c2VyRmFjaW5nTmFtZShwYXJzZWRJbnB1dClcbiAgICBpZiAoIXVzZXJGYWNpbmdOYW1lKSB7XG4gICAgICByZXR1cm4gYWN0aXZpdHkudG9vbE5hbWVcbiAgICB9XG4gICAgY29uc3QgdG9vbEFyZ3MgPSB0b29sLnJlbmRlclRvb2xVc2VNZXNzYWdlKHBhcnNlZElucHV0LCB7XG4gICAgICB0aGVtZSxcbiAgICAgIHZlcmJvc2U6IGZhbHNlLFxuICAgIH0pXG4gICAgaWYgKHRvb2xBcmdzKSB7XG4gICAgICByZXR1cm4gKFxuICAgICAgICA8VGV4dD5cbiAgICAgICAgICB7dXNlckZhY2luZ05hbWV9KHt0b29sQXJnc30pXG4gICAgICAgIDwvVGV4dD5cbiAgICAgIClcbiAgICB9XG4gICAgcmV0dXJuIHVzZXJGYWNpbmdOYW1lXG4gIH0gY2F0Y2gge1xuICAgIHJldHVybiBhY3Rpdml0eS50b29sTmFtZVxuICB9XG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU9BLEtBQUssTUFBTSxPQUFPO0FBQ3pCLFNBQVNDLElBQUksUUFBUSxjQUFjO0FBQ25DLGNBQWNDLEtBQUssUUFBUSxlQUFlO0FBQzFDLFNBQVNDLGNBQWMsUUFBUSxlQUFlO0FBQzlDLGNBQWNDLFlBQVksUUFBUSw4Q0FBOEM7QUFDaEYsY0FBY0MsU0FBUyxRQUFRLHNCQUFzQjtBQUVyRCxPQUFPLFNBQVNDLGtCQUFrQkEsQ0FDaENDLFFBQVEsRUFBRUgsWUFBWSxFQUN0QkksS0FBSyxFQUFFTixLQUFLLEVBQ1pPLEtBQUssRUFBRUosU0FBUyxDQUNqQixFQUFFTCxLQUFLLENBQUNVLFNBQVMsQ0FBQztFQUNqQixNQUFNQyxJQUFJLEdBQUdSLGNBQWMsQ0FBQ0ssS0FBSyxFQUFFRCxRQUFRLENBQUNLLFFBQVEsQ0FBQztFQUNyRCxJQUFJLENBQUNELElBQUksRUFBRTtJQUNULE9BQU9KLFFBQVEsQ0FBQ0ssUUFBUTtFQUMxQjtFQUNBLElBQUk7SUFDRixNQUFNQyxNQUFNLEdBQUdGLElBQUksQ0FBQ0csV0FBVyxDQUFDQyxTQUFTLENBQUNSLFFBQVEsQ0FBQ1MsS0FBSyxDQUFDO0lBQ3pELE1BQU1DLFdBQVcsR0FBR0osTUFBTSxDQUFDSyxPQUFPLEdBQUdMLE1BQU0sQ0FBQ00sSUFBSSxHQUFHLENBQUMsQ0FBQztJQUNyRCxNQUFNQyxjQUFjLEdBQUdULElBQUksQ0FBQ1MsY0FBYyxDQUFDSCxXQUFXLENBQUM7SUFDdkQsSUFBSSxDQUFDRyxjQUFjLEVBQUU7TUFDbkIsT0FBT2IsUUFBUSxDQUFDSyxRQUFRO0lBQzFCO0lBQ0EsTUFBTVMsUUFBUSxHQUFHVixJQUFJLENBQUNXLG9CQUFvQixDQUFDTCxXQUFXLEVBQUU7TUFDdERSLEtBQUs7TUFDTGMsT0FBTyxFQUFFO0lBQ1gsQ0FBQyxDQUFDO0lBQ0YsSUFBSUYsUUFBUSxFQUFFO01BQ1osT0FDRSxDQUFDLElBQUk7QUFDYixVQUFVLENBQUNELGNBQWMsQ0FBQyxDQUFDLENBQUNDLFFBQVEsQ0FBQztBQUNyQyxRQUFRLEVBQUUsSUFBSSxDQUFDO0lBRVg7SUFDQSxPQUFPRCxjQUFjO0VBQ3ZCLENBQUMsQ0FBQyxNQUFNO0lBQ04sT0FBT2IsUUFBUSxDQUFDSyxRQUFRO0VBQzFCO0FBQ0YiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/components/tasks/taskStatusUtils.tsx`

**信息:**
- 行数: 107
- 大小: 13548 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
/**
 * Shared utilities for displaying task status across different task types.
 */

import figures from 'figures';
import type { TaskStatus } from 'src/Task.js';
import type { InProcessTeammateTaskState } from 'src/tasks/InProcessTeammateTask/types.js';
import { isPanelAgentTask } from 'src/tasks/LocalAgentTask/LocalAgentTask.js';
import { isBackgroundTask, type TaskState } from 'src/tasks/types.js';
import type { DeepImmutable } from 'src/types/utils.js';
import { summarizeRecentActivities } from 'src/utils/collapseReadSearch.js';

/**
 * Returns true if the given task status represents a terminal (finished) state.
 */
export function isTerminalStatus(status: TaskStatus): boolean {
  return status === 'completed' || status === 'failed' || status === 'killed';
}

/**
 * Returns the appropriate icon for a task based on status and state flags.
 */
export function getTaskStatusIcon(status: TaskStatus, options?: {
  isIdle?: boolean;
  awaitingApproval?: boolean;
  hasError?: boolean;
  shutdownRequested?: boolean;
}): string {
  const {
    isIdle,
    awaitingApproval,
    hasError,
    shutdownRequested
  } = options ?? {};
  if (hasError) return figures.cross;
  if (awaitingApproval) return figures.questionMarkPrefix;
  if (shutdownRequested) return figures.warning;
  if (status === 'running') {
    if (isIdle) return figures.ellipsis;
    return figures.play;
  }
  if (status === 'completed') return figures.tick;
  if (status === 'failed' || status === 'killed') return figures.cross;
  return figures.bullet;
}

/**
 * Returns the appropriate semantic color for a task based on status and state flags.
 */
export function getTaskStatusColor(status: TaskStatus, options?: {

```

---


### `src/components/teams/TeamStatus.tsx`

**信息:**
- 行数: 80
- 大小: 6897 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Text } from '../../ink.js';
import { useAppState } from '../../state/AppState.js';
type Props = {
  teamsSelected: boolean;
  showHint: boolean;
};

/**
 * Footer status indicator showing teammate count
 * Similar to BackgroundTaskStatus but for teammates
 */
export function TeamStatus(t0) {
  const $ = _c(14);
  const {
    teamsSelected,
    showHint
  } = t0;
  const teamContext = useAppState(_temp);
  let t1;
  if ($[0] !== teamContext) {
    t1 = teamContext ? Object.values(teamContext.teammates).filter(_temp2).length : 0;
    $[0] = teamContext;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const totalTeammates = t1;
  if (totalTeammates === 0) {
    return null;
  }
  let t2;
  if ($[2] !== showHint || $[3] !== teamsSelected) {
    t2 = showHint && teamsSelected ? <><Text dimColor={true}>· </Text><Text dimColor={true}>Enter to view</Text></> : null;
    $[2] = showHint;
    $[3] = teamsSelected;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  const hint = t2;
  const statusText = `${totalTeammates} ${totalTeammates === 1 ? "teammate" : "teammates"}`;
  const t3 = teamsSelected ? "selected" : "normal";
  let t4;
  if ($[5] !== statusText || $[6] !== t3 || $[7] !== teamsSelected) {
    t4 = <Text key={t3} color="background" inverse={teamsSelected}>{statusText}</Text>;
    $[5] = statusText;
    $[6] = t3;
    $[7] = teamsSelected;

```

---


### `src/components/teams/TeamsDialog.tsx`

**信息:**
- 行数: 715
- 大小: 94680 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { randomUUID } from 'crypto';
import figures from 'figures';
import * as React from 'react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useInterval } from 'usehooks-ts';
import { useRegisterOverlay } from '../../context/overlayContext.js';
import { stringWidth } from '../../ink/stringWidth.js';
// eslint-disable-next-line custom-rules/prefer-use-keybindings -- raw j/k/arrow dialog navigation
import { Box, Text, useInput } from '../../ink.js';
import { useKeybindings } from '../../keybindings/useKeybinding.js';
import { useShortcutDisplay } from '../../keybindings/useShortcutDisplay.js';
import { type AppState, useAppState, useSetAppState } from '../../state/AppState.js';
import { getEmptyToolPermissionContext } from '../../Tool.js';
import { AGENT_COLOR_TO_THEME_COLOR } from '../../tools/AgentTool/agentColorManager.js';
import { logForDebugging } from '../../utils/debug.js';
import { execFileNoThrow } from '../../utils/execFileNoThrow.js';
import { truncateToWidth } from '../../utils/format.js';
import { getNextPermissionMode } from '../../utils/permissions/getNextPermissionMode.js';
import { getModeColor, type PermissionMode, permissionModeFromString, permissionModeSymbol } from '../../utils/permissions/PermissionMode.js';
import { jsonStringify } from '../../utils/slowOperations.js';
import { IT2_COMMAND, isInsideTmuxSync } from '../../utils/swarm/backends/detection.js';
import { ensureBackendsRegistered, getBackendByType, getCachedBackend } from '../../utils/swarm/backends/registry.js';
import type { PaneBackendType } from '../../utils/swarm/backends/types.js';
import { getSwarmSocketName, TMUX_COMMAND } from '../../utils/swarm/constants.js';
import { addHiddenPaneId, removeHiddenPaneId, removeMemberFromTeam, setMemberMode, setMultipleMemberModes } from '../../utils/swarm/teamHelpers.js';
import { listTasks, type Task, unassignTeammateTasks } from '../../utils/tasks.js';
import { getTeammateStatuses, type TeammateStatus, type TeamSummary } from '../../utils/teamDiscovery.js';
import { createModeSetRequestMessage, sendShutdownRequestToMailbox, writeToMailbox } from '../../utils/teammateMailbox.js';
import { Dialog } from '../design-system/Dialog.js';
import ThemedText from '../design-system/ThemedText.js';
type Props = {
  initialTeams?: TeamSummary[];
  onDone: () => void;
};
type DialogLevel = {
  type: 'teammateList';
  teamName: string;
} | {
  type: 'teammateDetail';
  teamName: string;
  memberName: string;
};

/**
 * Dialog for viewing teammates in the current team
 */
export function TeamsDialog({
  initialTeams,
  onDone

```

---


### `src/components/ui/OrderedList.tsx`

**信息:**
- 行数: 71
- 大小: 7294 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, isValidElement, type ReactNode, useContext } from 'react';
import { Box } from '../../ink.js';
import { OrderedListItem, OrderedListItemContext } from './OrderedListItem.js';
const OrderedListContext = createContext({
  marker: ''
});
type OrderedListProps = {
  children: ReactNode;
};
function OrderedListComponent(t0) {
  const $ = _c(9);
  const {
    children
  } = t0;
  const {
    marker: parentMarker
  } = useContext(OrderedListContext);
  let numberOfItems = 0;
  for (const child of React.Children.toArray(children)) {
    if (!isValidElement(child) || child.type !== OrderedListItem) {
      continue;
    }
    numberOfItems++;
  }
  const maxMarkerWidth = String(numberOfItems).length;
  let t1;
  if ($[0] !== children || $[1] !== maxMarkerWidth || $[2] !== parentMarker) {
    let t2;
    if ($[4] !== maxMarkerWidth || $[5] !== parentMarker) {
      t2 = (child_0, index) => {
        if (!isValidElement(child_0) || child_0.type !== OrderedListItem) {
          return child_0;
        }
        const paddedMarker = `${String(index + 1).padStart(maxMarkerWidth)}.`;
        const marker = `${parentMarker}${paddedMarker}`;
        return <OrderedListContext.Provider value={{
          marker
        }}><OrderedListItemContext.Provider value={{
            marker
          }}>{child_0}</OrderedListItemContext.Provider></OrderedListContext.Provider>;
      };
      $[4] = maxMarkerWidth;
      $[5] = parentMarker;
      $[6] = t2;
    } else {
      t2 = $[6];
    }
    t1 = React.Children.map(children, t2);
    $[0] = children;

```

---


### `src/components/ui/OrderedListItem.tsx`

**信息:**
- 行数: 45
- 大小: 3477 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, type ReactNode, useContext } from 'react';
import { Box, Text } from '../../ink.js';
export const OrderedListItemContext = createContext({
  marker: ''
});
type OrderedListItemProps = {
  children: ReactNode;
};
export function OrderedListItem(t0) {
  const $ = _c(7);
  const {
    children
  } = t0;
  const {
    marker
  } = useContext(OrderedListItemContext);
  let t1;
  if ($[0] !== marker) {
    t1 = <Text dimColor={true}>{marker}</Text>;
    $[0] = marker;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] !== children) {
    t2 = <Box flexDirection="column">{children}</Box>;
    $[2] = children;
    $[3] = t2;
  } else {
    t2 = $[3];
  }
  let t3;
  if ($[4] !== t1 || $[5] !== t2) {
    t3 = <Box gap={1}>{t1}{t2}</Box>;
    $[4] = t1;
    $[5] = t2;
    $[6] = t3;
  } else {
    t3 = $[6];
  }
  return t3;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsImNyZWF0ZUNvbnRleHQiLCJSZWFjdE5vZGUiLCJ1c2VDb250ZXh0IiwiQm94IiwiVGV4dCIsIk9yZGVyZWRMaXN0SXRlbUNvbnRleHQiLCJtYXJrZXIiLCJPcmRlcmVkTGlzdEl0ZW1Qcm9wcyIsImNoaWxkcmVuIiwiT3JkZXJlZExpc3RJdGVtIiwidDAiLCIkIiwiX2MiLCJ0MSIsInQyIiwidDMiXSwic291cmNlcyI6WyJPcmRlcmVkTGlzdEl0ZW0udHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCBSZWFjdCwgeyBjcmVhdGVDb250ZXh0LCB0eXBlIFJlYWN0Tm9kZSwgdXNlQ29udGV4dCB9IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgQm94LCBUZXh0IH0gZnJvbSAnLi4vLi4vaW5rLmpzJ1xuXG5leHBvcnQgY29uc3QgT3JkZXJlZExpc3RJdGVtQ29udGV4dCA9IGNyZWF0ZUNvbnRleHQoeyBtYXJrZXI6ICcnIH0pXG5cbnR5cGUgT3JkZXJlZExpc3RJdGVtUHJvcHMgPSB7XG4gIGNoaWxkcmVuOiBSZWFjdE5vZGVcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIE9yZGVyZWRMaXN0SXRlbSh7XG4gIGNoaWxkcmVuLFxufTogT3JkZXJlZExpc3RJdGVtUHJvcHMpOiBSZWFjdC5SZWFjdE5vZGUge1xuICBjb25zdCB7IG1hcmtlciB9ID0gdXNlQ29udGV4dChPcmRlcmVkTGlzdEl0ZW1Db250ZXh0KVxuXG4gIHJldHVybiAoXG4gICAgPEJveCBnYXA9ezF9PlxuICAgICAgPFRleHQgZGltQ29sb3I+e21hcmtlcn08L1RleHQ+XG4gICAgICA8Qm94IGZsZXhEaXJlY3Rpb249XCJjb2x1bW5cIj57Y2hpbGRyZW59PC9Cb3g+XG4gICAgPC9Cb3g+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLE9BQU9BLEtBQUssSUFBSUMsYUFBYSxFQUFFLEtBQUtDLFNBQVMsRUFBRUMsVUFBVSxRQUFRLE9BQU87QUFDeEUsU0FBU0MsR0FBRyxFQUFFQyxJQUFJLFFBQVEsY0FBYztBQUV4QyxPQUFPLE1BQU1DLHNCQUFzQixHQUFHTCxhQUFhLENBQUM7RUFBRU0sTUFBTSxFQUFFO0FBQUcsQ0FBQyxDQUFDO0FBRW5FLEtBQUtDLG9CQUFvQixHQUFHO0VBQzFCQyxRQUFRLEVBQUVQLFNBQVM7QUFDckIsQ0FBQztBQUVELE9BQU8sU0FBQVEsZ0JBQUFDLEVBQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFBeUI7SUFBQUo7RUFBQSxJQUFBRSxFQUVUO0VBQ3JCO0lBQUFKO0VBQUEsSUFBbUJKLFVBQVUsQ0FBQ0csc0JBQXNCLENBQUM7RUFBQSxJQUFBUSxFQUFBO0VBQUEsSUFBQUYsQ0FBQSxRQUFBTCxNQUFBO0lBSWpETyxFQUFBLElBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBUixLQUFPLENBQUMsQ0FBRVAsT0FBSyxDQUFFLEVBQXRCLElBQUksQ0FBeUI7SUFBQUssQ0FBQSxNQUFBTCxNQUFBO0lBQUFLLENBQUEsTUFBQUUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUYsQ0FBQTtFQUFBO0VBQUEsSUFBQUcsRUFBQTtFQUFBLElBQUFILENBQUEsUUFBQUgsUUFBQTtJQUM5Qk0sRUFBQSxJQUFDLEdBQUcsQ0FBZSxhQUFRLENBQVIsUUFBUSxDQUFFTixTQUFPLENBQUUsRUFBckMsR0FBRyxDQUF3QztJQUFBRyxDQUFBLE1BQUFILFFBQUE7SUFBQUcsQ0FBQSxNQUFBRyxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBSCxDQUFBO0VBQUE7RUFBQSxJQUFBSSxFQUFBO0VBQUEsSUFBQUosQ0FBQSxRQUFBRSxFQUFBLElBQUFGLENBQUEsUUFBQUcsRUFBQTtJQUY5Q0MsRUFBQSxJQUFDLEdBQUcsQ0FBTSxHQUFDLENBQUQsR0FBQyxDQUNULENBQUFGLEVBQTZCLENBQzdCLENBQUFDLEVBQTJDLENBQzdDLEVBSEMsR0FBRyxDQUdFO0lBQUFILENBQUEsTUFBQUUsRUFBQTtJQUFBRixDQUFBLE1BQUFHLEVBQUE7SUFBQUgsQ0FBQSxNQUFBSSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBSixDQUFBO0VBQUE7RUFBQSxPQUhOSSxFQUdNO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/components/ui/TreeSelect.tsx`

**信息:**
- 行数: 397
- 大小: 38964 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import type { KeyboardEvent } from '../../ink/events/keyboard-event.js';
import { Box } from '../../ink.js';
import { type OptionWithDescription, Select } from '../CustomSelect/select.js';
export type TreeNode<T> = {
  id: string | number;
  value: T;
  label: string;
  description?: string;
  dimDescription?: boolean;
  children?: TreeNode<T>[];
  metadata?: Record<string, unknown>;
};
type FlattenedNode<T> = {
  node: TreeNode<T>;
  depth: number;
  isExpanded: boolean;
  hasChildren: boolean;
  parentId?: string | number;
};
export type TreeSelectProps<T> = {
  /**
   * Tree nodes to display.
   */
  readonly nodes: TreeNode<T>[];

  /**
   * Callback when a node is selected.
   */
  readonly onSelect: (node: TreeNode<T>) => void;

  /**
   * Callback when cancel is pressed.
   */
  readonly onCancel?: () => void;

  /**
   * Callback when focused node changes.
   */
  readonly onFocus?: (node: TreeNode<T>) => void;

  /**
   * Node to focus by ID.
   */
  readonly focusNodeId?: string | number;

  /**
   * Number of visible options.
   */

```

---


### `src/components/ui/option.tsx`

**信息:**
- 行数: 3
- 大小: 43 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function Option() {
  return null
}

```

---


### `src/components/wizard/WizardDialogLayout.tsx`

**信息:**
- 行数: 65
- 大小: 6271 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type ReactNode } from 'react';
import type { Theme } from '../../utils/theme.js';
import { Dialog } from '../design-system/Dialog.js';
import { useWizard } from './useWizard.js';
import { WizardNavigationFooter } from './WizardNavigationFooter.js';
type Props = {
  title?: string;
  color?: keyof Theme;
  children: ReactNode;
  subtitle?: string;
  footerText?: ReactNode;
};
export function WizardDialogLayout(t0) {
  const $ = _c(11);
  const {
    title: titleOverride,
    color: t1,
    children,
    subtitle,
    footerText
  } = t0;
  const color = t1 === undefined ? "suggestion" : t1;
  const {
    currentStepIndex,
    totalSteps,
    title: providerTitle,
    showStepCounter,
    goBack
  } = useWizard();
  const title = titleOverride || providerTitle || "Wizard";
  const stepSuffix = showStepCounter !== false ? ` (${currentStepIndex + 1}/${totalSteps})` : "";
  const t2 = `${title}${stepSuffix}`;
  let t3;
  if ($[0] !== children || $[1] !== color || $[2] !== goBack || $[3] !== subtitle || $[4] !== t2) {
    t3 = <Dialog title={t2} subtitle={subtitle} onCancel={goBack} color={color} hideInputGuide={true} isCancelActive={false}>{children}</Dialog>;
    $[0] = children;
    $[1] = color;
    $[2] = goBack;
    $[3] = subtitle;
    $[4] = t2;
    $[5] = t3;
  } else {
    t3 = $[5];
  }
  let t4;
  if ($[6] !== footerText) {
    t4 = <WizardNavigationFooter instructions={footerText} />;
    $[6] = footerText;
    $[7] = t4;

```

---


### `src/components/wizard/WizardNavigationFooter.tsx`

**信息:**
- 行数: 24
- 大小: 4246 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React, { type ReactNode } from 'react';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import { Box, Text } from '../../ink.js';
import { ConfigurableShortcutHint } from '../ConfigurableShortcutHint.js';
import { Byline } from '../design-system/Byline.js';
import { KeyboardShortcutHint } from '../design-system/KeyboardShortcutHint.js';
type Props = {
  instructions?: ReactNode;
};
export function WizardNavigationFooter({
  instructions = <Byline>
      <KeyboardShortcutHint shortcut="↑↓" action="navigate" />
      <KeyboardShortcutHint shortcut="Enter" action="select" />
      <ConfigurableShortcutHint action="confirm:no" context="Confirmation" fallback="Esc" description="go back" />
    </Byline>
}: Props): ReactNode {
  const exitState = useExitOnCtrlCDWithKeybindings();
  return <Box marginLeft={3} marginTop={1}>
      <Text dimColor>
        {exitState.pending ? `Press ${exitState.keyName} again to exit` : instructions}
      </Text>
    </Box>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlJlYWN0Tm9kZSIsInVzZUV4aXRPbkN0cmxDRFdpdGhLZXliaW5kaW5ncyIsIkJveCIsIlRleHQiLCJDb25maWd1cmFibGVTaG9ydGN1dEhpbnQiLCJCeWxpbmUiLCJLZXlib2FyZFNob3J0Y3V0SGludCIsIlByb3BzIiwiaW5zdHJ1Y3Rpb25zIiwiV2l6YXJkTmF2aWdhdGlvbkZvb3RlciIsImV4aXRTdGF0ZSIsInBlbmRpbmciLCJrZXlOYW1lIl0sInNvdXJjZXMiOlsiV2l6YXJkTmF2aWdhdGlvbkZvb3Rlci50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0LCB7IHR5cGUgUmVhY3ROb2RlIH0gZnJvbSAncmVhY3QnXG5pbXBvcnQgeyB1c2VFeGl0T25DdHJsQ0RXaXRoS2V5YmluZGluZ3MgfSBmcm9tICcuLi8uLi9ob29rcy91c2VFeGl0T25DdHJsQ0RXaXRoS2V5YmluZGluZ3MuanMnXG5pbXBvcnQgeyBCb3gsIFRleHQgfSBmcm9tICcuLi8uLi9pbmsuanMnXG5pbXBvcnQgeyBDb25maWd1cmFibGVTaG9ydGN1dEhpbnQgfSBmcm9tICcuLi9Db25maWd1cmFibGVTaG9ydGN1dEhpbnQuanMnXG5pbXBvcnQgeyBCeWxpbmUgfSBmcm9tICcuLi9kZXNpZ24tc3lzdGVtL0J5bGluZS5qcydcbmltcG9ydCB7IEtleWJvYXJkU2hvcnRjdXRIaW50IH0gZnJvbSAnLi4vZGVzaWduLXN5c3RlbS9LZXlib2FyZFNob3J0Y3V0SGludC5qcydcblxudHlwZSBQcm9wcyA9IHtcbiAgaW5zdHJ1Y3Rpb25zPzogUmVhY3ROb2RlXG59XG5cbmV4cG9ydCBmdW5jdGlvbiBXaXphcmROYXZpZ2F0aW9uRm9vdGVyKHtcbiAgaW5zdHJ1Y3Rpb25zID0gKFxuICAgIDxCeWxpbmU+XG4gICAgICA8S2V5Ym9hcmRTaG9ydGN1dEhpbnQgc2hvcnRjdXQ9XCLihpHihpNcIiBhY3Rpb249XCJuYXZpZ2F0ZVwiIC8+XG4gICAgICA8S2V5Ym9hcmRTaG9ydGN1dEhpbnQgc2hvcnRjdXQ9XCJFbnRlclwiIGFjdGlvbj1cInNlbGVjdFwiIC8+XG4gICAgICA8Q29uZmlndXJhYmxlU2hvcnRjdXRIaW50XG4gICAgICAgIGFjdGlvbj1cImNvbmZpcm06bm9cIlxuICAgICAgICBjb250ZXh0PVwiQ29uZmlybWF0aW9uXCJcbiAgICAgICAgZmFsbGJhY2s9XCJFc2NcIlxuICAgICAgICBkZXNjcmlwdGlvbj1cImdvIGJhY2tcIlxuICAgICAgLz5cbiAgICA8L0J5bGluZT5cbiAgKSxcbn06IFByb3BzKTogUmVhY3ROb2RlIHtcbiAgY29uc3QgZXhpdFN0YXRlID0gdXNlRXhpdE9uQ3RybENEV2l0aEtleWJpbmRpbmdzKClcblxuICByZXR1cm4gKFxuICAgIDxCb3ggbWFyZ2luTGVmdD17M30gbWFyZ2luVG9wPXsxfT5cbiAgICAgIDxUZXh0IGRpbUNvbG9yPlxuICAgICAgICB7ZXhpdFN0YXRlLnBlbmRpbmdcbiAgICAgICAgICA/IGBQcmVzcyAke2V4aXRTdGF0ZS5rZXlOYW1lfSBhZ2FpbiB0byBleGl0YFxuICAgICAgICAgIDogaW5zdHJ1Y3Rpb25zfVxuICAgICAgPC9UZXh0PlxuICAgIDwvQm94PlxuICApXG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU9BLEtBQUssSUFBSSxLQUFLQyxTQUFTLFFBQVEsT0FBTztBQUM3QyxTQUFTQyw4QkFBOEIsUUFBUSwrQ0FBK0M7QUFDOUYsU0FBU0MsR0FBRyxFQUFFQyxJQUFJLFFBQVEsY0FBYztBQUN4QyxTQUFTQyx3QkFBd0IsUUFBUSxnQ0FBZ0M7QUFDekUsU0FBU0MsTUFBTSxRQUFRLDRCQUE0QjtBQUNuRCxTQUFTQyxvQkFBb0IsUUFBUSwwQ0FBMEM7QUFFL0UsS0FBS0MsS0FBSyxHQUFHO0VBQ1hDLFlBQVksQ0FBQyxFQUFFUixTQUFTO0FBQzFCLENBQUM7QUFFRCxPQUFPLFNBQVNTLHNCQUFzQkEsQ0FBQztFQUNyQ0QsWUFBWSxHQUNWLENBQUMsTUFBTTtBQUNYLE1BQU0sQ0FBQyxvQkFBb0IsQ0FBQyxRQUFRLENBQUMsSUFBSSxDQUFDLE1BQU0sQ0FBQyxVQUFVO0FBQzNELE1BQU0sQ0FBQyxvQkFBb0IsQ0FBQyxRQUFRLENBQUMsT0FBTyxDQUFDLE1BQU0sQ0FBQyxRQUFRO0FBQzVELE1BQU0sQ0FBQyx3QkFBd0IsQ0FDdkIsTUFBTSxDQUFDLFlBQVksQ0FDbkIsT0FBTyxDQUFDLGNBQWMsQ0FDdEIsUUFBUSxDQUFDLEtBQUssQ0FDZCxXQUFXLENBQUMsU0FBUztBQUU3QixJQUFJLEVBQUUsTUFBTTtBQUVMLENBQU4sRUFBRUQsS0FBSyxDQUFDLEVBQUVQLFNBQVMsQ0FBQztFQUNuQixNQUFNVSxTQUFTLEdBQUdULDhCQUE4QixDQUFDLENBQUM7RUFFbEQsT0FDRSxDQUFDLEdBQUcsQ0FBQyxVQUFVLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxTQUFTLENBQUMsQ0FBQyxDQUFDLENBQUM7QUFDckMsTUFBTSxDQUFDLElBQUksQ0FBQyxRQUFRO0FBQ3BCLFFBQVEsQ0FBQ1MsU0FBUyxDQUFDQyxPQUFPLEdBQ2QsU0FBU0QsU0FBUyxDQUFDRSxPQUFPLGdCQUFnQixHQUMxQ0osWUFBWTtBQUN4QixNQUFNLEVBQUUsSUFBSTtBQUNaLElBQUksRUFBRSxHQUFHLENBQUM7QUFFViIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/components/wizard/WizardProvider.tsx`

**信息:**
- 行数: 213
- 大小: 18665 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, type ReactNode, useCallback, useEffect, useMemo, useState } from 'react';
import { useExitOnCtrlCDWithKeybindings } from '../../hooks/useExitOnCtrlCDWithKeybindings.js';
import type { WizardContextValue, WizardProviderProps } from './types.js';

// Use any here for the context since it will be cast properly when used
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const WizardContext = createContext<WizardContextValue<any> | null>(null);
export function WizardProvider(t0) {
  const $ = _c(38);
  const {
    steps,
    initialData: t1,
    onComplete,
    onCancel,
    children,
    title,
    showStepCounter: t2
  } = t0;
  let t3;
  if ($[0] !== t1) {
    t3 = t1 === undefined ? {} as T : t1;
    $[0] = t1;
    $[1] = t3;
  } else {
    t3 = $[1];
  }
  const initialData = t3;
  const showStepCounter = t2 === undefined ? true : t2;
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [wizardData, setWizardData] = useState(initialData);
  const [isCompleted, setIsCompleted] = useState(false);
  let t4;
  if ($[2] === Symbol.for("react.memo_cache_sentinel")) {
    t4 = [];
    $[2] = t4;
  } else {
    t4 = $[2];
  }
  const [navigationHistory, setNavigationHistory] = useState(t4);
  useExitOnCtrlCDWithKeybindings();
  let t5;
  let t6;
  if ($[3] !== isCompleted || $[4] !== onComplete || $[5] !== wizardData) {
    t5 = () => {
      if (isCompleted) {
        setNavigationHistory([]);
        onComplete(wizardData);
      }
    };

```

---


### `src/components/wizard/index.ts`

**信息:**
- 行数: 9
- 大小: 328 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type {
  WizardContextValue,
  WizardProviderProps,
  WizardStepComponent,
} from './types.js'
export { useWizard } from './useWizard.js'
export { WizardDialogLayout } from './WizardDialogLayout.js'
export { WizardNavigationFooter } from './WizardNavigationFooter.js'
export { WizardProvider } from './WizardProvider.js'

```

---


### `src/components/wizard/types.ts`

**信息:**
- 行数: 13
- 大小: 263 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type * as React from 'react'

export type WizardContextValue = {
  currentStep?: number
  totalSteps?: number
  next?: () => void
  back?: () => void
  goToStep?: (step: number) => void
}

export type WizardProviderProps = {
  children?: React.ReactNode
}

```

---


### `src/components/wizard/useWizard.ts`

**信息:**
- 行数: 13
- 大小: 447 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useContext } from 'react'
import type { WizardContextValue } from './types.js'
import { WizardContext } from './WizardProvider.js'

export function useWizard<
  T extends Record<string, unknown> = Record<string, unknown>,
>(): WizardContextValue<T> {
  const context = useContext(WizardContext) as WizardContextValue<T> | null
  if (!context) {
    throw new Error('useWizard must be used within a WizardProvider')
  }
  return context
}

```

---

