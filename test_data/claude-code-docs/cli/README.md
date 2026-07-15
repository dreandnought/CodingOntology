# cli 模块

## 概述

**位置:** `src/cli/`

## 文件统计

- TypeScript 文件: 18
- TypeScript React 文件: 2
- 总计: 20

## 文件详情

---


### `src/cli/exit.ts`

**信息:**
- 行数: 31
- 大小: 1310 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * CLI exit helpers for subcommand handlers.
 *
 * Consolidates the 4-5 line "print + lint-suppress + exit" block that was
 * copy-pasted ~60 times across `claude mcp *` / `claude plugin *` handlers.
 * The `: never` return type lets TypeScript narrow control flow at call sites
 * without a trailing `return`.
 */
/* eslint-disable custom-rules/no-process-exit -- centralized CLI exit point */

// `return undefined as never` (not a post-exit throw) — tests spy on
// process.exit and let it return. Call sites write `return cliError(...)`
// where subsequent code would dereference narrowed-away values under mock.
// cliError uses console.error (tests spy on console.error); cliOk uses
// process.stdout.write (tests spy on process.stdout.write — Bun's console.log
// doesn't route through a spied process.stdout.write).

/** Write an error message to stderr (if given) and exit with code 1. */
export function cliError(msg?: string): never {
  // biome-ignore lint/suspicious/noConsole: centralized CLI error output
  if (msg) console.error(msg)
  process.exit(1)
  return undefined as never
}

/** Write a message to stdout (if given) and exit with code 0. */
export function cliOk(msg?: string): never {
  if (msg) process.stdout.write(msg + '\n')
  process.exit(0)
  return undefined as never
}

```

---


### `src/cli/handlers/agents.ts`

**信息:**
- 行数: 70
- 大小: 2089 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Agents subcommand handler — prints the list of configured agents.
 * Dynamically imported only when `claude agents` runs.
 */

import {
  AGENT_SOURCE_GROUPS,
  compareAgentsByName,
  getOverrideSourceLabel,
  type ResolvedAgent,
  resolveAgentModelDisplay,
  resolveAgentOverrides,
} from '../../tools/AgentTool/agentDisplay.js'
import {
  getActiveAgentsFromList,
  getAgentDefinitionsWithOverrides,
} from '../../tools/AgentTool/loadAgentsDir.js'
import { getCwd } from '../../utils/cwd.js'

function formatAgent(agent: ResolvedAgent): string {
  const model = resolveAgentModelDisplay(agent)
  const parts = [agent.agentType]
  if (model) {
    parts.push(model)
  }
  if (agent.memory) {
    parts.push(`${agent.memory} memory`)
  }
  return parts.join(' · ')
}

export async function agentsHandler(): Promise<void> {
  const cwd = getCwd()
  const { allAgents } = await getAgentDefinitionsWithOverrides(cwd)
  const activeAgents = getActiveAgentsFromList(allAgents)
  const resolvedAgents = resolveAgentOverrides(allAgents, activeAgents)

  const lines: string[] = []
  let totalActive = 0

  for (const { label, source } of AGENT_SOURCE_GROUPS) {
    const groupAgents = resolvedAgents
      .filter(a => a.source === source)
      .sort(compareAgentsByName)

    if (groupAgents.length === 0) continue

    lines.push(`${label}:`)
    for (const agent of groupAgents) {
      if (agent.overriddenBy) {

```

---


### `src/cli/handlers/auth.ts`

**信息:**
- 行数: 330
- 大小: 10756 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/* eslint-disable custom-rules/no-process-exit -- CLI subcommand handler intentionally exits */

import {
  clearAuthRelatedCaches,
  performLogout,
} from '../../commands/logout/logout.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import { getSSLErrorHint } from '../../services/api/errorUtils.js'
import { fetchAndStoreClaudeCodeFirstTokenDate } from '../../services/api/firstTokenDate.js'
import {
  createAndStoreApiKey,
  fetchAndStoreUserRoles,
  refreshOAuthToken,
  shouldUseClaudeAIAuth,
  storeOAuthAccountInfo,
} from '../../services/oauth/client.js'
import { getOauthProfileFromOauthToken } from '../../services/oauth/getOauthProfile.js'
import { OAuthService } from '../../services/oauth/index.js'
import type { OAuthTokens } from '../../services/oauth/types.js'
import {
  clearOAuthTokenCache,
  getAnthropicApiKeyWithSource,
  getAuthTokenSource,
  getOauthAccountInfo,
  getSubscriptionType,
  isUsing3PServices,
  saveOAuthTokensIfNeeded,
  validateForceLoginOrg,
} from '../../utils/auth.js'
import { saveGlobalConfig } from '../../utils/config.js'
import { logForDebugging } from '../../utils/debug.js'
import { isRunningOnHomespace } from '../../utils/envUtils.js'
import { errorMessage } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'
import { getAPIProvider } from '../../utils/model/providers.js'
import { getInitialSettings } from '../../utils/settings/settings.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import {
  buildAccountProperties,
  buildAPIProviderProperties,
} from '../../utils/status.js'

/**
 * Shared post-token-acquisition logic. Saves tokens, fetches profile/roles,
 * and sets up the local auth state.
 */
export async function installOAuthTokens(tokens: OAuthTokens): Promise<void> {

```

---


### `src/cli/handlers/autoMode.ts`

**信息:**
- 行数: 170
- 大小: 5742 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Auto mode subcommand handlers — dump default/merged classifier rules and
 * critique user-written rules. Dynamically imported when `claude auto-mode ...` runs.
 */

import { errorMessage } from '../../utils/errors.js'
import {
  getMainLoopModel,
  parseUserSpecifiedModel,
} from '../../utils/model/model.js'
import {
  type AutoModeRules,
  buildDefaultExternalSystemPrompt,
  getDefaultExternalAutoModeRules,
} from '../../utils/permissions/yoloClassifier.js'
import { getAutoModeConfig } from '../../utils/settings/settings.js'
import { sideQuery } from '../../utils/sideQuery.js'
import { jsonStringify } from '../../utils/slowOperations.js'

function writeRules(rules: AutoModeRules): void {
  process.stdout.write(jsonStringify(rules, null, 2) + '\n')
}

export function autoModeDefaultsHandler(): void {
  writeRules(getDefaultExternalAutoModeRules())
}

/**
 * Dump the effective auto mode config: user settings where provided, external
 * defaults otherwise. Per-section REPLACE semantics — matches how
 * buildYoloSystemPrompt resolves the external template (a non-empty user
 * section replaces that section's defaults entirely; an empty/absent section
 * falls through to defaults).
 */
export function autoModeConfigHandler(): void {
  const config = getAutoModeConfig()
  const defaults = getDefaultExternalAutoModeRules()
  writeRules({
    allow: config?.allow?.length ? config.allow : defaults.allow,
    soft_deny: config?.soft_deny?.length
      ? config.soft_deny
      : defaults.soft_deny,
    environment: config?.environment?.length
      ? config.environment
      : defaults.environment,
  })
}

const CRITIQUE_SYSTEM_PROMPT =
  'You are an expert reviewer of auto mode classifier rules for Claude Code.\n' +

```

---


### `src/cli/handlers/mcp.tsx`

**信息:**
- 行数: 362
- 大小: 56167 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
/**
 * MCP subcommand handlers — extracted from main.tsx for lazy loading.
 * These are dynamically imported only when the corresponding `claude mcp *` command runs.
 */

import { stat } from 'fs/promises';
import pMap from 'p-map';
import { cwd } from 'process';
import React from 'react';
import { MCPServerDesktopImportDialog } from '../../components/MCPServerDesktopImportDialog.js';
import { render } from '../../ink.js';
import { KeybindingSetup } from '../../keybindings/KeybindingProviderSetup.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../services/analytics/index.js';
import { clearMcpClientConfig, clearServerTokensFromLocalStorage, getMcpClientConfig, readClientSecret, saveMcpClientSecret } from '../../services/mcp/auth.js';
import { connectToServer, getMcpServerConnectionBatchSize } from '../../services/mcp/client.js';
import { addMcpConfig, getAllMcpConfigs, getMcpConfigByName, getMcpConfigsByScope, removeMcpConfig } from '../../services/mcp/config.js';
import type { ConfigScope, ScopedMcpServerConfig } from '../../services/mcp/types.js';
import { describeMcpConfigFilePath, ensureConfigScope, getScopeLabel } from '../../services/mcp/utils.js';
import { AppStateProvider } from '../../state/AppState.js';
import { getCurrentProjectConfig, getGlobalConfig, saveCurrentProjectConfig } from '../../utils/config.js';
import { isFsInaccessible } from '../../utils/errors.js';
import { gracefulShutdown } from '../../utils/gracefulShutdown.js';
import { safeParseJSON } from '../../utils/json.js';
import { getPlatform } from '../../utils/platform.js';
import { cliError, cliOk } from '../exit.js';
async function checkMcpServerHealth(name: string, server: ScopedMcpServerConfig): Promise<string> {
  try {
    const result = await connectToServer(name, server);
    if (result.type === 'connected') {
      return '✓ Connected';
    } else if (result.type === 'needs-auth') {
      return '! Needs authentication';
    } else {
      return '✗ Failed to connect';
    }
  } catch (_error) {
    return '✗ Connection error';
  }
}

// mcp serve (lines 4512–4532)
export async function mcpServeHandler({
  debug,
  verbose
}: {
  debug?: boolean;
  verbose?: boolean;
}): Promise<void> {
  const providedCwd = cwd();
  logEvent('tengu_mcp_start', {});

```

---


### `src/cli/handlers/plugins.ts`

**信息:**
- 行数: 878
- 大小: 31073 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Plugin and marketplace subcommand handlers — extracted from main.tsx for lazy loading.
 * These are dynamically imported only when `claude plugin *` or `claude plugin marketplace *` runs.
 */
/* eslint-disable custom-rules/no-process-exit -- CLI subcommand handlers intentionally exit */
import figures from 'figures'
import { basename, dirname } from 'path'
import { setUseCoworkPlugins } from '../../bootstrap/state.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_PII_TAGGED,
  logEvent,
} from '../../services/analytics/index.js'
import {
  disableAllPlugins,
  disablePlugin,
  enablePlugin,
  installPlugin,
  uninstallPlugin,
  updatePluginCli,
  VALID_INSTALLABLE_SCOPES,
  VALID_UPDATE_SCOPES,
} from '../../services/plugins/pluginCliCommands.js'
import { getPluginErrorMessage } from '../../types/plugin.js'
import { errorMessage } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'
import { clearAllCaches } from '../../utils/plugins/cacheUtils.js'
import { getInstallCounts } from '../../utils/plugins/installCounts.js'
import {
  isPluginInstalled,
  loadInstalledPluginsV2,
} from '../../utils/plugins/installedPluginsManager.js'
import {
  createPluginId,
  loadMarketplacesWithGracefulDegradation,
} from '../../utils/plugins/marketplaceHelpers.js'
import {
  addMarketplaceSource,
  loadKnownMarketplacesConfig,
  refreshAllMarketplaces,
  refreshMarketplace,
  removeMarketplaceSource,
  saveMarketplaceToSettings,
} from '../../utils/plugins/marketplaceManager.js'
import { loadPluginMcpServers } from '../../utils/plugins/mcpPluginIntegration.js'
import { parseMarketplaceInput } from '../../utils/plugins/parseMarketplaceInput.js'
import {
  parsePluginIdentifier,
  scopeToSettingSource,
} from '../../utils/plugins/pluginIdentifier.js'

```

---


### `src/cli/handlers/util.tsx`

**信息:**
- 行数: 110
- 大小: 14501 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * Miscellaneous subcommand handlers — extracted from main.tsx for lazy loading.
 * setup-token, doctor, install
 */
/* eslint-disable custom-rules/no-process-exit -- CLI subcommand handlers intentionally exit */

import { cwd } from 'process';
import React from 'react';
import { WelcomeV2 } from '../../components/LogoV2/WelcomeV2.js';
import { useManagePlugins } from '../../hooks/useManagePlugins.js';
import type { Root } from '../../ink.js';
import { Box, Text } from '../../ink.js';
import { KeybindingSetup } from '../../keybindings/KeybindingProviderSetup.js';
import { logEvent } from '../../services/analytics/index.js';
import { MCPConnectionManager } from '../../services/mcp/MCPConnectionManager.js';
import { AppStateProvider } from '../../state/AppState.js';
import { onChangeAppState } from '../../state/onChangeAppState.js';
import { isAnthropicAuthEnabled } from '../../utils/auth.js';
export async function setupTokenHandler(root: Root): Promise<void> {
  logEvent('tengu_setup_token_command', {});
  const showAuthWarning = !isAnthropicAuthEnabled();
  const {
    ConsoleOAuthFlow
  } = await import('../../components/ConsoleOAuthFlow.js');
  await new Promise<void>(resolve => {
    root.render(<AppStateProvider onChangeAppState={onChangeAppState}>
        <KeybindingSetup>
          <Box flexDirection="column" gap={1}>
            <WelcomeV2 />
            {showAuthWarning && <Box flexDirection="column">
                <Text color="warning">
                  Warning: You already have authentication configured via
                  environment variable or API key helper.
                </Text>
                <Text color="warning">
                  The setup-token command will create a new OAuth token which
                  you can use instead.
                </Text>
              </Box>}
            <ConsoleOAuthFlow onDone={() => {
            void resolve();
          }} mode="setup-token" startingMessage="This will guide you through long-lived (1-year) auth token setup for your Claude account. Claude subscription required." />
          </Box>
        </KeybindingSetup>
      </AppStateProvider>);
  });
  root.unmount();
  process.exit(0);
}

```

---


### `src/cli/ndjsonSafeStringify.ts`

**信息:**
- 行数: 32
- 大小: 1408 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { jsonStringify } from '../utils/slowOperations.js'

// JSON.stringify emits U+2028/U+2029 raw (valid per ECMA-404). When the
// output is a single NDJSON line, any receiver that uses JavaScript
// line-terminator semantics (ECMA-262 §11.3 — \n \r U+2028 U+2029) to
// split the stream will cut the JSON mid-string. ProcessTransport now
// silently skips non-JSON lines rather than crashing (gh-28405), but
// the truncated fragment is still lost — the message is silently dropped.
//
// The \uXXXX form is equivalent JSON (parses to the same string) but
// can never be mistaken for a line terminator by ANY receiver. This is
// what ES2019's "Subsume JSON" proposal and Node's util.inspect do.
//
// Single regex with alternation: the callback's one dispatch per match
// is cheaper than two full-string scans.
const JS_LINE_TERMINATORS = /\u2028|\u2029/g

function escapeJsLineTerminators(json: string): string {
  return json.replace(JS_LINE_TERMINATORS, c =>
    c === '\u2028' ? '\\u2028' : '\\u2029',
  )
}

/**
 * JSON.stringify for one-message-per-line transports. Escapes U+2028
 * LINE SEPARATOR and U+2029 PARAGRAPH SEPARATOR so the serialized output
 * cannot be broken by a line-splitting receiver. Output is still valid
 * JSON and parses to the same value.
 */
export function ndjsonSafeStringify(value: unknown): string {
  return escapeJsLineTerminators(jsonStringify(value))
}

```

---


### `src/cli/print.ts`

**信息:**
- 行数: 5594
- 大小: 212735 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
import { feature } from 'bun:bundle'
import { readFile, stat } from 'fs/promises'
import { dirname } from 'path'
import {
  downloadUserSettings,
  redownloadUserSettings,
} from 'src/services/settingsSync/index.js'
import { waitForRemoteManagedSettingsToLoad } from 'src/services/remoteManagedSettings/index.js'
import { StructuredIO } from 'src/cli/structuredIO.js'
import { RemoteIO } from 'src/cli/remoteIO.js'
import {
  type Command,
  formatDescriptionWithSource,
  getCommandName,
} from 'src/commands.js'
import { createStreamlinedTransformer } from 'src/utils/streamlinedTransform.js'
import { installStreamJsonStdoutGuard } from 'src/utils/streamJsonStdoutGuard.js'
import type { ToolPermissionContext } from 'src/Tool.js'
import type { ThinkingConfig } from 'src/utils/thinking.js'
import { assembleToolPool, filterToolsByDenyRules } from 'src/tools.js'
import uniqBy from 'lodash-es/uniqBy.js'
import { uniq } from 'src/utils/array.js'
import { mergeAndFilterTools } from 'src/utils/toolPool.js'
import {
  logEvent,
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
} from 'src/services/analytics/index.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from 'src/services/analytics/growthbook.js'
import { logForDebugging } from 'src/utils/debug.js'
import {
  logForDiagnosticsNoPII,
  withDiagnosticsTiming,
} from 'src/utils/diagLogs.js'
import { toolMatchesName, type Tool, type Tools } from 'src/Tool.js'
import {
  type AgentDefinition,
  isBuiltInAgent,
  parseAgentsFromJson,
} from 'src/tools/AgentTool/loadAgentsDir.js'
import type { Message, NormalizedUserMessage } from 'src/types/message.js'
import type { QueuedCommand } from 'src/types/textInputTypes.js'
import {
  dequeue,
  dequeueAllMatching,
  enqueue,
  hasCommandsInQueue,
  peek,
  subscribeToCommandQueue,
  getCommandsByMaxPriority,

```

---


### `src/cli/remoteIO.ts`

**信息:**
- 行数: 255
- 大小: 9946 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { StdoutMessage } from 'src/entrypoints/sdk/controlTypes.js'
import { PassThrough } from 'stream'
import { URL } from 'url'
import { getSessionId } from '../bootstrap/state.js'
import { getPollIntervalConfig } from '../bridge/pollConfig.js'
import { registerCleanup } from '../utils/cleanupRegistry.js'
import { setCommandLifecycleListener } from '../utils/commandLifecycle.js'
import { isDebugMode, logForDebugging } from '../utils/debug.js'
import { logForDiagnosticsNoPII } from '../utils/diagLogs.js'
import { isEnvTruthy } from '../utils/envUtils.js'
import { errorMessage } from '../utils/errors.js'
import { gracefulShutdown } from '../utils/gracefulShutdown.js'
import { logError } from '../utils/log.js'
import { writeToStdout } from '../utils/process.js'
import { getSessionIngressAuthToken } from '../utils/sessionIngressAuth.js'
import {
  setSessionMetadataChangedListener,
  setSessionStateChangedListener,
} from '../utils/sessionState.js'
import {
  setInternalEventReader,
  setInternalEventWriter,
} from '../utils/sessionStorage.js'
import { ndjsonSafeStringify } from './ndjsonSafeStringify.js'
import { StructuredIO } from './structuredIO.js'
import { CCRClient, CCRInitError } from './transports/ccrClient.js'
import { SSETransport } from './transports/SSETransport.js'
import type { Transport } from './transports/Transport.js'
import { getTransportForUrl } from './transports/transportUtils.js'

/**
 * Bidirectional streaming for SDK mode with session tracking
 * Supports WebSocket transport
 */
export class RemoteIO extends StructuredIO {
  private url: URL
  private transport: Transport
  private inputStream: PassThrough
  private readonly isBridge: boolean = false
  private readonly isDebug: boolean = false
  private ccrClient: CCRClient | null = null
  private keepAliveTimer: ReturnType<typeof setInterval> | null = null

  constructor(
    streamUrl: string,
    initialPrompt?: AsyncIterable<string>,
    replayUserMessages?: boolean,
  ) {
    const inputStream = new PassThrough({ encoding: 'utf8' })
    super(inputStream, replayUserMessages)

```

---


### `src/cli/structuredIO.ts`

**信息:**
- 行数: 859
- 大小: 28720 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type {
  ElicitResult,
  JSONRPCMessage,
} from '@modelcontextprotocol/sdk/types.js'
import { randomUUID } from 'crypto'
import type { AssistantMessage } from 'src//types/message.js'
import type {
  HookInput,
  HookJSONOutput,
  PermissionUpdate,
  SDKMessage,
  SDKUserMessage,
} from 'src/entrypoints/agentSdkTypes.js'
import { SDKControlElicitationResponseSchema } from 'src/entrypoints/sdk/controlSchemas.js'
import type {
  SDKControlRequest,
  SDKControlResponse,
  StdinMessage,
  StdoutMessage,
} from 'src/entrypoints/sdk/controlTypes.js'
import type { CanUseToolFn } from 'src/hooks/useCanUseTool.js'
import type { Tool, ToolUseContext } from 'src/Tool.js'
import { type HookCallback, hookJSONOutputSchema } from 'src/types/hooks.js'
import { logForDebugging } from 'src/utils/debug.js'
import { logForDiagnosticsNoPII } from 'src/utils/diagLogs.js'
import { AbortError } from 'src/utils/errors.js'
import {
  type Output as PermissionToolOutput,
  permissionPromptToolResultToPermissionDecision,
  outputSchema as permissionToolOutputSchema,
} from 'src/utils/permissions/PermissionPromptToolResultSchema.js'
import type {
  PermissionDecision,
  PermissionDecisionReason,
} from 'src/utils/permissions/PermissionResult.js'
import { hasPermissionsToUseTool } from 'src/utils/permissions/permissions.js'
import { writeToStdout } from 'src/utils/process.js'
import { jsonStringify } from 'src/utils/slowOperations.js'
import { z } from 'zod/v4'
import { notifyCommandLifecycle } from '../utils/commandLifecycle.js'
import { normalizeControlMessageKeys } from '../utils/controlMessageCompat.js'
import { executePermissionRequestHooks } from '../utils/hooks.js'
import {
  applyPermissionUpdates,
  persistPermissionUpdates,
} from '../utils/permissions/PermissionUpdate.js'
import {
  notifySessionStateChanged,
  type RequiresActionDetails,

```

---


### `src/cli/transports/HybridTransport.ts`

**信息:**
- 行数: 282
- 大小: 10883 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios, { type AxiosError } from 'axios'
import type { StdoutMessage } from 'src/entrypoints/sdk/controlTypes.js'
import { logForDebugging } from '../../utils/debug.js'
import { logForDiagnosticsNoPII } from '../../utils/diagLogs.js'
import { getSessionIngressAuthToken } from '../../utils/sessionIngressAuth.js'
import { SerialBatchEventUploader } from './SerialBatchEventUploader.js'
import {
  WebSocketTransport,
  type WebSocketTransportOptions,
} from './WebSocketTransport.js'

const BATCH_FLUSH_INTERVAL_MS = 100
// Per-attempt POST timeout. Bounds how long a single stuck POST can block
// the serialized queue. Without this, a hung connection stalls all writes.
const POST_TIMEOUT_MS = 15_000
// Grace period for queued writes on close(). Covers a healthy POST (~100ms)
// plus headroom; best-effort, not a delivery guarantee under degraded network.
// Void-ed (nothing awaits it) so this is a last resort — replBridge teardown
// now closes AFTER archive so archive latency is the primary drain window.
// NOTE: gracefulShutdown's cleanup budget is 2s (not the 5s outer failsafe);
// 3s here exceeds it, but the process lives ~2s longer for hooks+analytics.
const CLOSE_GRACE_MS = 3000

/**
 * Hybrid transport: WebSocket for reads, HTTP POST for writes.
 *
 * Write flow:
 *
 *   write(stream_event) ─┐
 *                        │ (100ms timer)
 *                        │
 *                        ▼
 *   write(other) ────► uploader.enqueue()  (SerialBatchEventUploader)
 *                        ▲    │
 *   writeBatch() ────────┘    │ serial, batched, retries indefinitely,
 *                             │ backpressure at maxQueueSize
 *                             ▼
 *                        postOnce()  (single HTTP POST, throws on retryable)
 *
 * stream_event messages accumulate in streamEventBuffer for up to 100ms
 * before enqueue (reduces POST count for high-volume content deltas). A
 * non-stream write flushes any buffered stream_events first to preserve order.
 *
 * Serialization + retry + backpressure are delegated to SerialBatchEventUploader
 * (same primitive CCR uses). At most one POST in-flight; events arriving during
 * a POST batch into the next one. On failure, the uploader re-queues and retries
 * with exponential backoff + jitter. If the queue fills past maxQueueSize,
 * enqueue() blocks — giving awaiting callers backpressure.
 *
 * Why serialize? Bridge mode fires writes via `void transport.write()`

```

---


### `src/cli/transports/SSETransport.ts`

**信息:**
- 行数: 711
- 大小: 23758 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios, { type AxiosError } from 'axios'
import type { StdoutMessage } from 'src/entrypoints/sdk/controlTypes.js'
import { logForDebugging } from '../../utils/debug.js'
import { logForDiagnosticsNoPII } from '../../utils/diagLogs.js'
import { errorMessage } from '../../utils/errors.js'
import { getSessionIngressAuthHeaders } from '../../utils/sessionIngressAuth.js'
import { sleep } from '../../utils/sleep.js'
import { jsonParse, jsonStringify } from '../../utils/slowOperations.js'
import { getClaudeCodeUserAgent } from '../../utils/userAgent.js'
import type { Transport } from './Transport.js'

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

const RECONNECT_BASE_DELAY_MS = 1000
const RECONNECT_MAX_DELAY_MS = 30_000
/** Time budget for reconnection attempts before giving up (10 minutes). */
const RECONNECT_GIVE_UP_MS = 600_000
/** Server sends keepalives every 15s; treat connection as dead after 45s of silence. */
const LIVENESS_TIMEOUT_MS = 45_000

/**
 * HTTP status codes that indicate a permanent server-side rejection.
 * The transport transitions to 'closed' immediately without retrying.
 */
const PERMANENT_HTTP_CODES = new Set([401, 403, 404])

// POST retry configuration (matches HybridTransport)
const POST_MAX_RETRIES = 10
const POST_BASE_DELAY_MS = 500
const POST_MAX_DELAY_MS = 8000

/** Hoisted TextDecoder options to avoid per-chunk allocation in readStream. */
const STREAM_DECODE_OPTS: TextDecodeOptions = { stream: true }

/** Hoisted axios validateStatus callback to avoid per-request closure allocation. */
function alwaysValidStatus(): boolean {
  return true
}

// ---------------------------------------------------------------------------
// SSE Frame Parser
// ---------------------------------------------------------------------------

type SSEFrame = {
  event?: string
  id?: string
  data?: string
}

```

---


### `src/cli/transports/SerialBatchEventUploader.ts`

**信息:**
- 行数: 275
- 大小: 9089 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { jsonStringify } from '../../utils/slowOperations.js'

/**
 * Serial ordered event uploader with batching, retry, and backpressure.
 *
 * - enqueue() adds events to a pending buffer
 * - At most 1 POST in-flight at a time
 * - Drains up to maxBatchSize items per POST
 * - New events accumulate while in-flight
 * - On failure: exponential backoff (clamped), retries indefinitely
 *   until success or close() — unless maxConsecutiveFailures is set,
 *   in which case the failing batch is dropped and drain advances
 * - flush() blocks until pending is empty and kicks drain if needed
 * - Backpressure: enqueue() blocks when maxQueueSize is reached
 */

/**
 * Throw from config.send() to make the uploader wait a server-supplied
 * duration before retrying (e.g. 429 with Retry-After). When retryAfterMs
 * is set, it overrides exponential backoff for that attempt — clamped to
 * [baseDelayMs, maxDelayMs] and jittered so a misbehaving server can
 * neither hot-loop nor stall the client, and many sessions sharing a rate
 * limit don't all pounce at the same instant. Without retryAfterMs, behaves
 * like any other thrown error (exponential backoff).
 */
export class RetryableError extends Error {
  constructor(
    message: string,
    readonly retryAfterMs?: number,
  ) {
    super(message)
  }
}

type SerialBatchEventUploaderConfig<T> = {
  /** Max items per POST (1 = no batching) */
  maxBatchSize: number
  /**
   * Max serialized bytes per POST. First item always goes in regardless of
   * size; subsequent items only if cumulative JSON bytes stay under this.
   * Undefined = no byte limit (count-only batching).
   */
  maxBatchBytes?: number
  /** Max pending items before enqueue() blocks */
  maxQueueSize: number
  /** The actual HTTP call — caller controls payload format */
  send: (batch: T[]) => Promise<void>
  /** Base delay for exponential backoff (ms) */
  baseDelayMs: number
  /** Max delay cap (ms) */

```

---


### `src/cli/transports/Transport.ts`

**信息:**
- 行数: 7
- 大小: 234 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export interface Transport {
  connect?(): Promise<void>
  close?(): void | Promise<void>
  send?(data: string): Promise<void>
  onData?(handler: (data: string) => void): void
  onClose?(handler: (closeCode?: number) => void): void
}

```

---


### `src/cli/transports/WebSocketTransport.ts`

**信息:**
- 行数: 800
- 大小: 28195 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { StdoutMessage } from 'src/entrypoints/sdk/controlTypes.js'
import type WsWebSocket from 'ws'
import { logEvent } from '../../services/analytics/index.js'
import { CircularBuffer } from '../../utils/CircularBuffer.js'
import { logForDebugging } from '../../utils/debug.js'
import { logForDiagnosticsNoPII } from '../../utils/diagLogs.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { getWebSocketTLSOptions } from '../../utils/mtls.js'
import {
  getWebSocketProxyAgent,
  getWebSocketProxyUrl,
} from '../../utils/proxy.js'
import {
  registerSessionActivityCallback,
  unregisterSessionActivityCallback,
} from '../../utils/sessionActivity.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import type { Transport } from './Transport.js'

const KEEP_ALIVE_FRAME = '{"type":"keep_alive"}\n'

const DEFAULT_MAX_BUFFER_SIZE = 1000
const DEFAULT_BASE_RECONNECT_DELAY = 1000
const DEFAULT_MAX_RECONNECT_DELAY = 30000
/** Time budget for reconnection attempts before giving up (10 minutes). */
const DEFAULT_RECONNECT_GIVE_UP_MS = 600_000
const DEFAULT_PING_INTERVAL = 10000
const DEFAULT_KEEPALIVE_INTERVAL = 300_000 // 5 minutes

/**
 * Threshold for detecting system sleep/wake. If the gap between consecutive
 * reconnection attempts exceeds this, the machine likely slept. We reset
 * the reconnection budget and retry — the server will reject with permanent
 * close codes (4001/1002) if the session was reaped during sleep.
 */
const SLEEP_DETECTION_THRESHOLD_MS = DEFAULT_MAX_RECONNECT_DELAY * 2 // 60s

/**
 * WebSocket close codes that indicate a permanent server-side rejection.
 * The transport transitions to 'closed' immediately without retrying.
 */
const PERMANENT_CLOSE_CODES = new Set([
  1002, // protocol error — server rejected handshake (e.g. session reaped)
  4001, // session expired / not found
  4003, // unauthorized
])

export type WebSocketTransportOptions = {
  /** When false, the transport does not attempt automatic reconnection on
   *  disconnect. Use this when the caller has its own recovery mechanism

```

---


### `src/cli/transports/WorkerStateUploader.ts`

**信息:**
- 行数: 131
- 大小: 3879 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { sleep } from '../../utils/sleep.js'

/**
 * Coalescing uploader for PUT /worker (session state + metadata).
 *
 * - 1 in-flight PUT + 1 pending patch
 * - New calls coalesce into pending (never grows beyond 1 slot)
 * - On success: send pending if exists
 * - On failure: exponential backoff (clamped), retries indefinitely
 *   until success or close(). Absorbs any pending patches before each retry.
 * - No backpressure needed — naturally bounded at 2 slots
 *
 * Coalescing rules:
 * - Top-level keys (worker_status, external_metadata) — last value wins
 * - Inside external_metadata / internal_metadata — RFC 7396 merge:
 *   keys are added/overwritten, null values preserved (server deletes)
 */

type WorkerStateUploaderConfig = {
  send: (body: Record<string, unknown>) => Promise<boolean>
  /** Base delay for exponential backoff (ms) */
  baseDelayMs: number
  /** Max delay cap (ms) */
  maxDelayMs: number
  /** Random jitter range added to retry delay (ms) */
  jitterMs: number
}

export class WorkerStateUploader {
  private inflight: Promise<void> | null = null
  private pending: Record<string, unknown> | null = null
  private closed = false
  private readonly config: WorkerStateUploaderConfig

  constructor(config: WorkerStateUploaderConfig) {
    this.config = config
  }

  /**
   * Enqueue a patch to PUT /worker. Coalesces with any existing pending
   * patch. Fire-and-forget — callers don't need to await.
   */
  enqueue(patch: Record<string, unknown>): void {
    if (this.closed) return
    this.pending = this.pending ? coalescePatches(this.pending, patch) : patch
    void this.drain()
  }

  close(): void {
    this.closed = true

```

---


### `src/cli/transports/ccrClient.ts`

**信息:**
- 行数: 998
- 大小: 33775 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { randomUUID } from 'crypto'
import type {
  SDKPartialAssistantMessage,
  StdoutMessage,
} from 'src/entrypoints/sdk/controlTypes.js'
import { decodeJwtExpiry } from '../../bridge/jwtUtils.js'
import { logForDebugging } from '../../utils/debug.js'
import { logForDiagnosticsNoPII } from '../../utils/diagLogs.js'
import { errorMessage, getErrnoCode } from '../../utils/errors.js'
import { createAxiosInstance } from '../../utils/proxy.js'
import {
  registerSessionActivityCallback,
  unregisterSessionActivityCallback,
} from '../../utils/sessionActivity.js'
import {
  getSessionIngressAuthHeaders,
  getSessionIngressAuthToken,
} from '../../utils/sessionIngressAuth.js'
import type {
  RequiresActionDetails,
  SessionState,
} from '../../utils/sessionState.js'
import { sleep } from '../../utils/sleep.js'
import { getClaudeCodeUserAgent } from '../../utils/userAgent.js'
import {
  RetryableError,
  SerialBatchEventUploader,
} from './SerialBatchEventUploader.js'
import type { SSETransport, StreamClientEvent } from './SSETransport.js'
import { WorkerStateUploader } from './WorkerStateUploader.js'

/** Default interval between heartbeat events (20s; server TTL is 60s). */
const DEFAULT_HEARTBEAT_INTERVAL_MS = 20_000

/**
 * stream_event messages accumulate in a delay buffer for up to this many ms
 * before enqueue. Mirrors HybridTransport's batching window. text_delta
 * events for the same content block accumulate into a single full-so-far
 * snapshot per flush — each emitted event is self-contained so a client
 * connecting mid-stream sees complete text, not a fragment.
 */
const STREAM_EVENT_FLUSH_INTERVAL_MS = 100

/** Hoisted axios validateStatus callback to avoid per-request closure allocation. */
function alwaysValidStatus(): boolean {
  return true
}

export type CCRInitFailReason =
  | 'no_auth_headers'

```

---


### `src/cli/transports/transportUtils.ts`

**信息:**
- 行数: 45
- 大小: 1767 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { URL } from 'url'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { HybridTransport } from './HybridTransport.js'
import { SSETransport } from './SSETransport.js'
import type { Transport } from './Transport.js'
import { WebSocketTransport } from './WebSocketTransport.js'

/**
 * Helper function to get the appropriate transport for a URL.
 *
 * Transport selection priority:
 * 1. SSETransport (SSE reads + POST writes) when CLAUDE_CODE_USE_CCR_V2 is set
 * 2. HybridTransport (WS reads + POST writes) when CLAUDE_CODE_POST_FOR_SESSION_INGRESS_V2 is set
 * 3. WebSocketTransport (WS reads + WS writes) — default
 */
export function getTransportForUrl(
  url: URL,
  headers: Record<string, string> = {},
  sessionId?: string,
  refreshHeaders?: () => Record<string, string>,
): Transport {
  if (isEnvTruthy(process.env.CLAUDE_CODE_USE_CCR_V2)) {
    // v2: SSE for reads, HTTP POST for writes
    // --sdk-url is the session URL (.../sessions/{id});
    // derive the SSE stream URL by appending /worker/events/stream
    const sseUrl = new URL(url.href)
    if (sseUrl.protocol === 'wss:') {
      sseUrl.protocol = 'https:'
    } else if (sseUrl.protocol === 'ws:') {
      sseUrl.protocol = 'http:'
    }
    sseUrl.pathname =
      sseUrl.pathname.replace(/\/$/, '') + '/worker/events/stream'
    return new SSETransport(sseUrl, headers, sessionId, refreshHeaders)
  }

  if (url.protocol === 'ws:' || url.protocol === 'wss:') {
    if (isEnvTruthy(process.env.CLAUDE_CODE_POST_FOR_SESSION_INGRESS_V2)) {
      return new HybridTransport(url, headers, sessionId, refreshHeaders)
    }
    return new WebSocketTransport(url, headers, sessionId, refreshHeaders)
  } else {
    throw new Error(`Unsupported protocol: ${url.protocol}`)
  }
}

```

---


### `src/cli/update.ts`

**信息:**
- 行数: 422
- 大小: 14487 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import chalk from 'chalk'
import { logEvent } from 'src/services/analytics/index.js'
import {
  getLatestVersion,
  type InstallStatus,
  installGlobalPackage,
} from 'src/utils/autoUpdater.js'
import { regenerateCompletionCache } from 'src/utils/completionCache.js'
import {
  getGlobalConfig,
  type InstallMethod,
  saveGlobalConfig,
} from 'src/utils/config.js'
import { logForDebugging } from 'src/utils/debug.js'
import { getDoctorDiagnostic } from 'src/utils/doctorDiagnostic.js'
import { gracefulShutdown } from 'src/utils/gracefulShutdown.js'
import {
  installOrUpdateClaudePackage,
  localInstallationExists,
} from 'src/utils/localInstaller.js'
import {
  installLatest as installLatestNative,
  removeInstalledSymlink,
} from 'src/utils/nativeInstaller/index.js'
import { getPackageManager } from 'src/utils/nativeInstaller/packageManagers.js'
import { writeToStdout } from 'src/utils/process.js'
import { gte } from 'src/utils/semver.js'
import { getInitialSettings } from 'src/utils/settings/settings.js'

export async function update() {
  logEvent('tengu_update_check', {})
  writeToStdout(`Current version: ${MACRO.VERSION}\n`)

  const channel = getInitialSettings()?.autoUpdatesChannel ?? 'latest'
  writeToStdout(`Checking for updates to ${channel} version...\n`)

  logForDebugging('update: Starting update check')

  // Run diagnostic to detect potential issues
  logForDebugging('update: Running diagnostic')
  const diagnostic = await getDoctorDiagnostic()
  logForDebugging(`update: Installation type: ${diagnostic.installationType}`)
  logForDebugging(
    `update: Config install method: ${diagnostic.configInstallMethod}`,
  )

  // Check for multiple installations
  if (diagnostic.multipleInstallations.length > 1) {
    writeToStdout('\n')
    writeToStdout(chalk.yellow('Warning: Multiple installations found') + '\n')

```

---

