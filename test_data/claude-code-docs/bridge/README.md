# bridge 模块

## 概述

**位置:** `src/bridge/`

## 文件统计

- TypeScript 文件: 33
- TypeScript React 文件: 0
- 总计: 33

## 文件详情

---


### `src/bridge/bridgeApi.ts`

**信息:**
- 行数: 539
- 大小: 18066 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'

import { debugBody, extractErrorDetail } from './debugUtils.js'
import {
  BRIDGE_LOGIN_INSTRUCTION,
  type BridgeApiClient,
  type BridgeConfig,
  type PermissionResponseEvent,
  type WorkResponse,
} from './types.js'

type BridgeApiDeps = {
  baseUrl: string
  getAccessToken: () => string | undefined
  runnerVersion: string
  onDebug?: (msg: string) => void
  /**
   * Called on 401 to attempt OAuth token refresh. Returns true if refreshed,
   * in which case the request is retried once. Injected because
   * handleOAuth401Error from utils/auth.ts transitively pulls in config.ts →
   * file.ts → permissions/filesystem.ts → sessionStorage.ts → commands.ts
   * (~1300 modules). Daemon callers using env-var tokens omit this — their
   * tokens don't refresh, so 401 goes straight to BridgeFatalError.
   */
  onAuth401?: (staleAccessToken: string) => Promise<boolean>
  /**
   * Returns the trusted device token to send as X-Trusted-Device-Token on
   * bridge API calls. Bridge sessions have SecurityTier=ELEVATED on the
   * server (CCR v2); when the server's enforcement flag is on,
   * ConnectBridgeWorker requires a trusted device at JWT-issuance.
   * Optional — when absent or returning undefined, the header is omitted
   * and the server falls through to its flag-off/no-op path. The CLI-side
   * gate is tengu_sessions_elevated_auth_enforcement (see trustedDevice.ts).
   */
  getTrustedDeviceToken?: () => string | undefined
}

const BETA_HEADER = 'environments-2025-11-01'

/** Allowlist pattern for server-provided IDs used in URL path segments. */
const SAFE_ID_PATTERN = /^[a-zA-Z0-9_-]+$/

/**
 * Validate that a server-provided ID is safe to interpolate into a URL path.
 * Prevents path traversal (e.g. `../../admin`) and injection via IDs that
 * contain slashes, dots, or other special characters.
 */
export function validateBridgeId(id: string, label: string): string {
  if (!id || !SAFE_ID_PATTERN.test(id)) {
    throw new Error(`Invalid ${label}: contains unsafe characters`)

```

---


### `src/bridge/bridgeConfig.ts`

**信息:**
- 行数: 48
- 大小: 1695 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Shared bridge auth/URL resolution. Consolidates the ant-only
 * CLAUDE_BRIDGE_* dev overrides that were previously copy-pasted across
 * a dozen files — inboundAttachments, BriefTool/upload, bridgeMain,
 * initReplBridge, remoteBridgeCore, daemon workers, /rename,
 * /remote-control.
 *
 * Two layers: *Override() returns the ant-only env var (or undefined);
 * the non-Override versions fall through to the real OAuth store/config.
 * Callers that compose with a different auth source (e.g. daemon workers
 * using IPC auth) use the Override getters directly.
 */

import { getOauthConfig } from '../constants/oauth.js'
import { getClaudeAIOAuthTokens } from '../utils/auth.js'

/** Ant-only dev override: CLAUDE_BRIDGE_OAUTH_TOKEN, else undefined. */
export function getBridgeTokenOverride(): string | undefined {
  return (
    (process.env.USER_TYPE === 'ant' &&
      process.env.CLAUDE_BRIDGE_OAUTH_TOKEN) ||
    undefined
  )
}

/** Ant-only dev override: CLAUDE_BRIDGE_BASE_URL, else undefined. */
export function getBridgeBaseUrlOverride(): string | undefined {
  return (
    (process.env.USER_TYPE === 'ant' && process.env.CLAUDE_BRIDGE_BASE_URL) ||
    undefined
  )
}

/**
 * Access token for bridge API calls: dev override first, then the OAuth
 * keychain. Undefined means "not logged in".
 */
export function getBridgeAccessToken(): string | undefined {
  return getBridgeTokenOverride() ?? getClaudeAIOAuthTokens()?.accessToken
}

/**
 * Base URL for bridge API calls: dev override first, then the production
 * OAuth config. Always returns a URL.
 */
export function getBridgeBaseUrl(): string {
  return getBridgeBaseUrlOverride() ?? getOauthConfig().BASE_API_URL
}

```

---


### `src/bridge/bridgeDebug.ts`

**信息:**
- 行数: 135
- 大小: 4926 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { logForDebugging } from '../utils/debug.js'
import { BridgeFatalError } from './bridgeApi.js'
import type { BridgeApiClient } from './types.js'

/**
 * Ant-only fault injection for manually testing bridge recovery paths.
 *
 * Real failure modes this targets (BQ 2026-03-12, 7-day window):
 *   poll 404 not_found_error   — 147K sessions/week, dead onEnvironmentLost gate
 *   ws_closed 1002/1006        —  22K sessions/week, zombie poll after close
 *   register transient failure —  residual: network blips during doReconnect
 *
 * Usage: /bridge-kick <subcommand> from the REPL while Remote Control is
 * connected, then tail debug.log to watch the recovery machinery react.
 *
 * Module-level state is intentional here: one bridge per REPL process, the
 * /bridge-kick slash command has no other way to reach into initBridgeCore's
 * closures, and teardown clears the slot.
 */

/** One-shot fault to inject on the next matching api call. */
type BridgeFault = {
  method:
    | 'pollForWork'
    | 'registerBridgeEnvironment'
    | 'reconnectSession'
    | 'heartbeatWork'
  /** Fatal errors go through handleErrorStatus → BridgeFatalError. Transient
   *  errors surface as plain axios rejections (5xx / network). Recovery code
   *  distinguishes the two: fatal → teardown, transient → retry/backoff. */
  kind: 'fatal' | 'transient'
  status: number
  errorType?: string
  /** Remaining injections. Decremented on consume; removed at 0. */
  count: number
}

export type BridgeDebugHandle = {
  /** Invoke the transport's permanent-close handler directly. Tests the
   *  ws_closed → reconnectEnvironmentWithSession escalation (#22148). */
  fireClose: (code: number) => void
  /** Call reconnectEnvironmentWithSession() — same as SIGUSR2 but
   *  reachable from the slash command. */
  forceReconnect: () => void
  /** Queue a fault for the next N calls to the named api method. */
  injectFault: (fault: BridgeFault) => void
  /** Abort the at-capacity sleep so an injected poll fault lands
   *  immediately instead of up to 10min later. */
  wakePollLoop: () => void
  /** env/session IDs for the debug.log grep. */

```

---


### `src/bridge/bridgeEnabled.ts`

**信息:**
- 行数: 202
- 大小: 8442 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import {
  checkGate_CACHED_OR_BLOCKING,
  getDynamicConfig_CACHED_MAY_BE_STALE,
  getFeatureValue_CACHED_MAY_BE_STALE,
} from '../services/analytics/growthbook.js'
// Namespace import breaks the bridgeEnabled → auth → config → bridgeEnabled
// cycle — authModule.foo is a live binding, so by the time the helpers below
// call it, auth.js is fully loaded. Previously used require() for the same
// deferral, but require() hits a CJS cache that diverges from the ESM
// namespace after mock.module() (daemon/auth.test.ts), breaking spyOn.
import * as authModule from '../utils/auth.js'
import { isEnvTruthy } from '../utils/envUtils.js'
import { lt } from '../utils/semver.js'

/**
 * Runtime check for bridge mode entitlement.
 *
 * Remote Control requires a claude.ai subscription (the bridge auths to CCR
 * with the claude.ai OAuth token). isClaudeAISubscriber() excludes
 * Bedrock/Vertex/Foundry, apiKeyHelper/gateway deployments, env-var API keys,
 * and Console API logins — none of which have the OAuth token CCR needs.
 * See github.com/deshaw/anthropic-issues/issues/24.
 *
 * The `feature('BRIDGE_MODE')` guard ensures the GrowthBook string literal
 * is only referenced when bridge mode is enabled at build time.
 */
export function isBridgeEnabled(): boolean {
  // Positive ternary pattern — see docs/feature-gating.md.
  // Negative pattern (if (!feature(...)) return) does not eliminate
  // inline string literals from external builds.
  return feature('BRIDGE_MODE')
    ? isClaudeAISubscriber() &&
        getFeatureValue_CACHED_MAY_BE_STALE('tengu_ccr_bridge', false)
    : false
}

/**
 * Blocking entitlement check for Remote Control.
 *
 * Returns cached `true` immediately (fast path). If the disk cache says
 * `false` or is missing, awaits GrowthBook init and fetches the fresh
 * server value (slow path, max ~5s), then writes it to disk.
 *
 * Use at entitlement gates where a stale `false` would unfairly block access.
 * For user-facing error paths, prefer `getBridgeDisabledReason()` which gives
 * a specific diagnostic. For render-body UI visibility checks, use
 * `isBridgeEnabled()` instead.
 */
export async function isBridgeEnabledBlocking(): Promise<boolean> {

```

---


### `src/bridge/bridgeMain.ts`

**信息:**
- 行数: 2999
- 大小: 115571 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { randomUUID } from 'crypto'
import { hostname, tmpdir } from 'os'
import { basename, join, resolve } from 'path'
import { getRemoteSessionUrl } from '../constants/product.js'
import { shutdownDatadog } from '../services/analytics/datadog.js'
import { shutdown1PEventLogging } from '../services/analytics/firstPartyEventLogger.js'
import { checkGate_CACHED_OR_BLOCKING } from '../services/analytics/growthbook.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
  logEventAsync,
} from '../services/analytics/index.js'
import { isInBundledMode } from '../utils/bundledMode.js'
import { logForDebugging } from '../utils/debug.js'
import { logForDiagnosticsNoPII } from '../utils/diagLogs.js'
import { isEnvTruthy, isInProtectedNamespace } from '../utils/envUtils.js'
import { errorMessage } from '../utils/errors.js'
import { truncateToWidth } from '../utils/format.js'
import { logError } from '../utils/log.js'
import { sleep } from '../utils/sleep.js'
import { createAgentWorktree, removeAgentWorktree } from '../utils/worktree.js'
import {
  BridgeFatalError,
  createBridgeApiClient,
  isExpiredErrorType,
  isSuppressible403,
  validateBridgeId,
} from './bridgeApi.js'
import { formatDuration } from './bridgeStatusUtil.js'
import { createBridgeLogger } from './bridgeUI.js'
import { createCapacityWake } from './capacityWake.js'
import { describeAxiosError } from './debugUtils.js'
import { createTokenRefreshScheduler } from './jwtUtils.js'
import { getPollIntervalConfig } from './pollConfig.js'
import { toCompatSessionId, toInfraSessionId } from './sessionIdCompat.js'
import { createSessionSpawner, safeFilenameId } from './sessionRunner.js'
import { getTrustedDeviceToken } from './trustedDevice.js'
import {
  BRIDGE_LOGIN_ERROR,
  type BridgeApiClient,
  type BridgeConfig,
  type BridgeLogger,
  DEFAULT_SESSION_TIMEOUT_MS,
  type SessionDoneStatus,
  type SessionHandle,
  type SessionSpawner,
  type SessionSpawnOpts,
  type SpawnMode,
} from './types.js'

```

---


### `src/bridge/bridgeMessaging.ts`

**信息:**
- 行数: 461
- 大小: 15703 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Shared transport-layer helpers for bridge message handling.
 *
 * Extracted from replBridge.ts so both the env-based core (initBridgeCore)
 * and the env-less core (initEnvLessBridgeCore) can use the same ingress
 * parsing, control-request handling, and echo-dedup machinery.
 *
 * Everything here is pure — no closure over bridge-specific state. All
 * collaborators (transport, sessionId, UUID sets, callbacks) are passed
 * as params.
 */

import { randomUUID } from 'crypto'
import type { SDKMessage } from '../entrypoints/agentSdkTypes.js'
import type {
  SDKControlRequest,
  SDKControlResponse,
} from '../entrypoints/sdk/controlTypes.js'
import type { SDKResultSuccess } from '../entrypoints/sdk/coreTypes.js'
import { logEvent } from '../services/analytics/index.js'
import { EMPTY_USAGE } from '../services/api/emptyUsage.js'
import type { Message } from '../types/message.js'
import { normalizeControlMessageKeys } from '../utils/controlMessageCompat.js'
import { logForDebugging } from '../utils/debug.js'
import { stripDisplayTagsAllowEmpty } from '../utils/displayTags.js'
import { errorMessage } from '../utils/errors.js'
import type { PermissionMode } from '../utils/permissions/PermissionMode.js'
import { jsonParse } from '../utils/slowOperations.js'
import type { ReplBridgeTransport } from './replBridgeTransport.js'

// ─── Type guards ─────────────────────────────────────────────────────────────

/** Type predicate for parsed WebSocket messages. SDKMessage is a
 *  discriminated union on `type` — validating the discriminant is
 *  sufficient for the predicate; callers narrow further via the union. */
export function isSDKMessage(value: unknown): value is SDKMessage {
  return (
    value !== null &&
    typeof value === 'object' &&
    'type' in value &&
    typeof value.type === 'string'
  )
}

/** Type predicate for control_response messages from the server. */
export function isSDKControlResponse(
  value: unknown,
): value is SDKControlResponse {
  return (
    value !== null &&

```

---


### `src/bridge/bridgePermissionCallbacks.ts`

**信息:**
- 行数: 43
- 大小: 1411 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { PermissionUpdate } from '../utils/permissions/PermissionUpdateSchema.js'

type BridgePermissionResponse = {
  behavior: 'allow' | 'deny'
  updatedInput?: Record<string, unknown>
  updatedPermissions?: PermissionUpdate[]
  message?: string
}

type BridgePermissionCallbacks = {
  sendRequest(
    requestId: string,
    toolName: string,
    input: Record<string, unknown>,
    toolUseId: string,
    description: string,
    permissionSuggestions?: PermissionUpdate[],
    blockedPath?: string,
  ): void
  sendResponse(requestId: string, response: BridgePermissionResponse): void
  /** Cancel a pending control_request so the web app can dismiss its prompt. */
  cancelRequest(requestId: string): void
  onResponse(
    requestId: string,
    handler: (response: BridgePermissionResponse) => void,
  ): () => void // returns unsubscribe
}

/** Type predicate for validating a parsed control_response payload
 *  as a BridgePermissionResponse. Checks the required `behavior`
 *  discriminant rather than using an unsafe `as` cast. */
function isBridgePermissionResponse(
  value: unknown,
): value is BridgePermissionResponse {
  if (!value || typeof value !== 'object') return false
  return (
    'behavior' in value &&
    (value.behavior === 'allow' || value.behavior === 'deny')
  )
}

export { isBridgePermissionResponse }
export type { BridgePermissionCallbacks, BridgePermissionResponse }

```

---


### `src/bridge/bridgePointer.ts`

**信息:**
- 行数: 210
- 大小: 7611 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { mkdir, readFile, stat, unlink, writeFile } from 'fs/promises'
import { dirname, join } from 'path'
import { z } from 'zod/v4'
import { logForDebugging } from '../utils/debug.js'
import { isENOENT } from '../utils/errors.js'
import { getWorktreePathsPortable } from '../utils/getWorktreePathsPortable.js'
import { lazySchema } from '../utils/lazySchema.js'
import {
  getProjectsDir,
  sanitizePath,
} from '../utils/sessionStoragePortable.js'
import { jsonParse, jsonStringify } from '../utils/slowOperations.js'

/**
 * Upper bound on worktree fanout. git worktree list is naturally bounded
 * (50 is a LOT), but this caps the parallel stat() burst and guards against
 * pathological setups. Above this, --continue falls back to current-dir-only.
 */
const MAX_WORKTREE_FANOUT = 50

/**
 * Crash-recovery pointer for Remote Control sessions.
 *
 * Written immediately after a bridge session is created, periodically
 * refreshed during the session, and cleared on clean shutdown. If the
 * process dies unclean (crash, kill -9, terminal closed), the pointer
 * persists. On next startup, `claude remote-control` detects it and offers
 * to resume via the --session-id flow from #20460.
 *
 * Staleness is checked against the file's mtime (not an embedded timestamp)
 * so that a periodic re-write with the same content serves as a refresh —
 * matches the backend's rolling BRIDGE_LAST_POLL_TTL (4h) semantics. A
 * bridge that's been polling for 5+ hours and then crashes still has a
 * fresh pointer as long as the refresh ran within the window.
 *
 * Scoped per working directory (alongside transcript JSONL files) so two
 * concurrent bridges in different repos don't clobber each other.
 */

export const BRIDGE_POINTER_TTL_MS = 4 * 60 * 60 * 1000

const BridgePointerSchema = lazySchema(() =>
  z.object({
    sessionId: z.string(),
    environmentId: z.string(),
    source: z.enum(['standalone', 'repl']),
  }),
)

export type BridgePointer = z.infer<ReturnType<typeof BridgePointerSchema>>

```

---


### `src/bridge/bridgeStatusUtil.ts`

**信息:**
- 行数: 163
- 大小: 5143 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  getClaudeAiBaseUrl,
  getRemoteSessionUrl,
} from '../constants/product.js'
import { stringWidth } from '../ink/stringWidth.js'
import { formatDuration, truncateToWidth } from '../utils/format.js'
import { getGraphemeSegmenter } from '../utils/intl.js'

/** Bridge status state machine states. */
export type StatusState =
  | 'idle'
  | 'attached'
  | 'titled'
  | 'reconnecting'
  | 'failed'

/** How long a tool activity line stays visible after last tool_start (ms). */
export const TOOL_DISPLAY_EXPIRY_MS = 30_000

/** Interval for the shimmer animation tick (ms). */
export const SHIMMER_INTERVAL_MS = 150

export function timestamp(): string {
  const now = new Date()
  const h = String(now.getHours()).padStart(2, '0')
  const m = String(now.getMinutes()).padStart(2, '0')
  const s = String(now.getSeconds()).padStart(2, '0')
  return `${h}:${m}:${s}`
}

export { formatDuration, truncateToWidth as truncatePrompt }

/** Abbreviate a tool activity summary for the trail display. */
export function abbreviateActivity(summary: string): string {
  return truncateToWidth(summary, 30)
}

/** Build the connect URL shown when the bridge is idle. */
export function buildBridgeConnectUrl(
  environmentId: string,
  ingressUrl?: string,
): string {
  const baseUrl = getClaudeAiBaseUrl(undefined, ingressUrl)
  return `${baseUrl}/code?bridge=${environmentId}`
}

/**
 * Build the session URL shown when a session is attached. Delegates to
 * getRemoteSessionUrl for the cse_→session_ prefix translation, then appends
 * the v1-specific ?bridge={environmentId} query.

```

---


### `src/bridge/bridgeUI.ts`

**信息:**
- 行数: 530
- 大小: 16780 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import chalk from 'chalk'
import { toString as qrToString } from 'qrcode'
import {
  BRIDGE_FAILED_INDICATOR,
  BRIDGE_READY_INDICATOR,
  BRIDGE_SPINNER_FRAMES,
} from '../constants/figures.js'
import { stringWidth } from '../ink/stringWidth.js'
import { logForDebugging } from '../utils/debug.js'
import {
  buildActiveFooterText,
  buildBridgeConnectUrl,
  buildBridgeSessionUrl,
  buildIdleFooterText,
  FAILED_FOOTER_TEXT,
  formatDuration,
  type StatusState,
  TOOL_DISPLAY_EXPIRY_MS,
  timestamp,
  truncatePrompt,
  wrapWithOsc8Link,
} from './bridgeStatusUtil.js'
import type {
  BridgeConfig,
  BridgeLogger,
  SessionActivity,
  SpawnMode,
} from './types.js'

const QR_OPTIONS = {
  type: 'utf8' as const,
  errorCorrectionLevel: 'L' as const,
  small: true,
}

/** Generate a QR code and return its lines. */
async function generateQr(url: string): Promise<string[]> {
  const qr = await qrToString(url, QR_OPTIONS)
  return qr.split('\n').filter((line: string) => line.length > 0)
}

export function createBridgeLogger(options: {
  verbose: boolean
  write?: (s: string) => void
}): BridgeLogger {
  const write = options.write ?? ((s: string) => process.stdout.write(s))
  const verbose = options.verbose

  // Track how many status lines are currently displayed at the bottom
  let statusLineCount = 0

```

---


### `src/bridge/capacityWake.ts`

**信息:**
- 行数: 56
- 大小: 1841 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Shared capacity-wake primitive for bridge poll loops.
 *
 * Both replBridge.ts and bridgeMain.ts need to sleep while "at capacity"
 * but wake early when either (a) the outer loop signal aborts (shutdown),
 * or (b) capacity frees up (session done / transport lost). This module
 * encapsulates the mutable wake-controller + two-signal merger that both
 * poll loops previously duplicated byte-for-byte.
 */

export type CapacitySignal = { signal: AbortSignal; cleanup: () => void }

export type CapacityWake = {
  /**
   * Create a signal that aborts when either the outer loop signal or the
   * capacity-wake controller fires. Returns the merged signal and a cleanup
   * function that removes listeners when the sleep resolves normally
   * (without abort).
   */
  signal(): CapacitySignal
  /**
   * Abort the current at-capacity sleep and arm a fresh controller so the
   * poll loop immediately re-checks for new work.
   */
  wake(): void
}

export function createCapacityWake(outerSignal: AbortSignal): CapacityWake {
  let wakeController = new AbortController()

  function wake(): void {
    wakeController.abort()
    wakeController = new AbortController()
  }

  function signal(): CapacitySignal {
    const merged = new AbortController()
    const abort = (): void => merged.abort()
    if (outerSignal.aborted || wakeController.signal.aborted) {
      merged.abort()
      return { signal: merged.signal, cleanup: () => {} }
    }
    outerSignal.addEventListener('abort', abort, { once: true })
    const capSig = wakeController.signal
    capSig.addEventListener('abort', abort, { once: true })
    return {
      signal: merged.signal,
      cleanup: () => {
        outerSignal.removeEventListener('abort', abort)
        capSig.removeEventListener('abort', abort)

```

---


### `src/bridge/codeSessionApi.ts`

**信息:**
- 行数: 168
- 大小: 4840 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Thin HTTP wrappers for the CCR v2 code-session API.
 *
 * Separate file from remoteBridgeCore.ts so the SDK /bridge subpath can
 * export createCodeSession + fetchRemoteCredentials without bundling the
 * heavy CLI tree (analytics, transport, etc.). Callers supply explicit
 * accessToken + baseUrl — no implicit auth or config reads.
 */

import axios from 'axios'
import { logForDebugging } from '../utils/debug.js'
import { errorMessage } from '../utils/errors.js'
import { jsonStringify } from '../utils/slowOperations.js'
import { extractErrorDetail } from './debugUtils.js'

const ANTHROPIC_VERSION = '2023-06-01'

function oauthHeaders(accessToken: string): Record<string, string> {
  return {
    Authorization: `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
    'anthropic-version': ANTHROPIC_VERSION,
  }
}

export async function createCodeSession(
  baseUrl: string,
  accessToken: string,
  title: string,
  timeoutMs: number,
  tags?: string[],
): Promise<string | null> {
  const url = `${baseUrl}/v1/code/sessions`
  let response
  try {
    response = await axios.post(
      url,
      // bridge: {} is the positive signal for the oneof runner — omitting it
      // (or sending environment_id: "") now 400s. BridgeRunner is an empty
      // message today; it's a placeholder for future bridge-specific options.
      { title, bridge: {}, ...(tags?.length ? { tags } : {}) },
      {
        headers: oauthHeaders(accessToken),
        timeout: timeoutMs,
        validateStatus: s => s < 500,
      },
    )
  } catch (err: unknown) {
    logForDebugging(
      `[code-session] Session create request failed: ${errorMessage(err)}`,

```

---


### `src/bridge/createSession.ts`

**信息:**
- 行数: 384
- 大小: 12157 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { SDKMessage } from '../entrypoints/agentSdkTypes.js'
import { logForDebugging } from '../utils/debug.js'
import { errorMessage } from '../utils/errors.js'
import { extractErrorDetail } from './debugUtils.js'
import { toCompatSessionId } from './sessionIdCompat.js'

type GitSource = {
  type: 'git_repository'
  url: string
  revision?: string
}

type GitOutcome = {
  type: 'git_repository'
  git_info: { type: 'github'; repo: string; branches: string[] }
}

// Events must be wrapped in { type: 'event', data: <sdk_message> } for the
// POST /v1/sessions endpoint (discriminated union format).
type SessionEvent = {
  type: 'event'
  data: SDKMessage
}

/**
 * Create a session on a bridge environment via POST /v1/sessions.
 *
 * Used by both `claude remote-control` (empty session so the user has somewhere to
 * type immediately) and `/remote-control` (session pre-populated with conversation
 * history).
 *
 * Returns the session ID on success, or null if creation fails (non-fatal).
 */
export async function createBridgeSession({
  environmentId,
  title,
  events,
  gitRepoUrl,
  branch,
  signal,
  baseUrl: baseUrlOverride,
  getAccessToken,
  permissionMode,
}: {
  environmentId: string
  title?: string
  events: SessionEvent[]
  gitRepoUrl: string | null
  branch: string
  signal: AbortSignal

```

---


### `src/bridge/debugUtils.ts`

**信息:**
- 行数: 141
- 大小: 4240 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import { logForDebugging } from '../utils/debug.js'
import { errorMessage } from '../utils/errors.js'
import { jsonStringify } from '../utils/slowOperations.js'

const DEBUG_MSG_LIMIT = 2000

const SECRET_FIELD_NAMES = [
  'session_ingress_token',
  'environment_secret',
  'access_token',
  'secret',
  'token',
]

const SECRET_PATTERN = new RegExp(
  `"(${SECRET_FIELD_NAMES.join('|')})"\\s*:\\s*"([^"]*)"`,
  'g',
)

const REDACT_MIN_LENGTH = 16

export function redactSecrets(s: string): string {
  return s.replace(SECRET_PATTERN, (_match, field: string, value: string) => {
    if (value.length < REDACT_MIN_LENGTH) {
      return `"${field}":"[REDACTED]"`
    }
    const redacted = `${value.slice(0, 8)}...${value.slice(-4)}`
    return `"${field}":"${redacted}"`
  })
}

/** Truncate a string for debug logging, collapsing newlines. */
export function debugTruncate(s: string): string {
  const flat = s.replace(/\n/g, '\\n')
  if (flat.length <= DEBUG_MSG_LIMIT) {
    return flat
  }
  return flat.slice(0, DEBUG_MSG_LIMIT) + `... (${flat.length} chars)`
}

/** Truncate a JSON-serializable value for debug logging. */
export function debugBody(data: unknown): string {
  const raw = typeof data === 'string' ? data : jsonStringify(data)
  const s = redactSecrets(raw)
  if (s.length <= DEBUG_MSG_LIMIT) {
    return s

```

---


### `src/bridge/envLessBridgeConfig.ts`

**信息:**
- 行数: 165
- 大小: 7250 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { getFeatureValue_DEPRECATED } from '../services/analytics/growthbook.js'
import { lazySchema } from '../utils/lazySchema.js'
import { lt } from '../utils/semver.js'
import { isEnvLessBridgeEnabled } from './bridgeEnabled.js'

export type EnvLessBridgeConfig = {
  // withRetry — init-phase backoff (createSession, POST /bridge, recovery /bridge)
  init_retry_max_attempts: number
  init_retry_base_delay_ms: number
  init_retry_jitter_fraction: number
  init_retry_max_delay_ms: number
  // axios timeout for POST /sessions, POST /bridge, POST /archive
  http_timeout_ms: number
  // BoundedUUIDSet ring size (echo + re-delivery dedup)
  uuid_dedup_buffer_size: number
  // CCRClient worker heartbeat cadence. Server TTL is 60s — 20s gives 3× margin.
  heartbeat_interval_ms: number
  // ±fraction of interval — per-beat jitter to spread fleet load.
  heartbeat_jitter_fraction: number
  // Fire proactive JWT refresh this long before expires_in. Larger buffer =
  // more frequent refresh (refresh cadence ≈ expires_in - buffer).
  token_refresh_buffer_ms: number
  // Archive POST timeout in teardown(). Distinct from http_timeout_ms because
  // gracefulShutdown races runCleanupFunctions() against a 2s cap — a 10s
  // axios timeout on a slow/stalled archive burns the whole budget on a
  // request that forceExit will kill anyway.
  teardown_archive_timeout_ms: number
  // Deadline for onConnect after transport.connect(). If neither onConnect
  // nor onClose fires before this, emit tengu_bridge_repl_connect_timeout
  // — the only telemetry for the ~1% of sessions that emit `started` then
  // go silent (no error, no event, just nothing).
  connect_timeout_ms: number
  // Semver floor for the env-less bridge path. Separate from the v1
  // tengu_bridge_min_version config so a v2-specific bug can force upgrades
  // without blocking v1 (env-based) clients, and vice versa.
  min_version: string
  // When true, tell users their claude.ai app may be too old to see v2
  // sessions — lets us roll the v2 bridge before the app ships the new
  // session-list query.
  should_show_app_upgrade_message: boolean
}

export const DEFAULT_ENV_LESS_BRIDGE_CONFIG: EnvLessBridgeConfig = {
  init_retry_max_attempts: 3,
  init_retry_base_delay_ms: 500,
  init_retry_jitter_fraction: 0.25,
  init_retry_max_delay_ms: 4000,
  http_timeout_ms: 10_000,
  uuid_dedup_buffer_size: 2000,

```

---


### `src/bridge/flushGate.ts`

**信息:**
- 行数: 71
- 大小: 1981 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * State machine for gating message writes during an initial flush.
 *
 * When a bridge session starts, historical messages are flushed to the
 * server via a single HTTP POST. During that flush, new messages must
 * be queued to prevent them from arriving at the server interleaved
 * with the historical messages.
 *
 * Lifecycle:
 *   start() → enqueue() returns true, items are queued
 *   end()   → returns queued items for draining, enqueue() returns false
 *   drop()  → discards queued items (permanent transport close)
 *   deactivate() → clears active flag without dropping items
 *                   (transport replacement — new transport will drain)
 */
export class FlushGate<T> {
  private _active = false
  private _pending: T[] = []

  get active(): boolean {
    return this._active
  }

  get pendingCount(): number {
    return this._pending.length
  }

  /** Mark flush as in-progress. enqueue() will start queuing items. */
  start(): void {
    this._active = true
  }

  /**
   * End the flush and return any queued items for draining.
   * Caller is responsible for sending the returned items.
   */
  end(): T[] {
    this._active = false
    return this._pending.splice(0)
  }

  /**
   * If flush is active, queue the items and return true.
   * If flush is not active, return false (caller should send directly).
   */
  enqueue(...items: T[]): boolean {
    if (!this._active) return false
    this._pending.push(...items)
    return true
  }

```

---


### `src/bridge/inboundAttachments.ts`

**信息:**
- 行数: 175
- 大小: 6267 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Resolve file_uuid attachments on inbound bridge user messages.
 *
 * Web composer uploads via cookie-authed /api/{org}/upload, sends file_uuid
 * alongside the message. Here we fetch each via GET /api/oauth/files/{uuid}/content
 * (oauth-authed, same store), write to ~/.claude/uploads/{sessionId}/, and
 * return @path refs to prepend. Claude's Read tool takes it from there.
 *
 * Best-effort: any failure (no token, network, non-2xx, disk) logs debug and
 * skips that attachment. The message still reaches Claude, just without @path.
 */

import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/messages.mjs'
import axios from 'axios'
import { randomUUID } from 'crypto'
import { mkdir, writeFile } from 'fs/promises'
import { basename, join } from 'path'
import { z } from 'zod/v4'
import { getSessionId } from '../bootstrap/state.js'
import { logForDebugging } from '../utils/debug.js'
import { getClaudeConfigHomeDir } from '../utils/envUtils.js'
import { lazySchema } from '../utils/lazySchema.js'
import { getBridgeAccessToken, getBridgeBaseUrl } from './bridgeConfig.js'

const DOWNLOAD_TIMEOUT_MS = 30_000

function debug(msg: string): void {
  logForDebugging(`[bridge:inbound-attach] ${msg}`)
}

const attachmentSchema = lazySchema(() =>
  z.object({
    file_uuid: z.string(),
    file_name: z.string(),
  }),
)
const attachmentsArraySchema = lazySchema(() => z.array(attachmentSchema()))

export type InboundAttachment = z.infer<ReturnType<typeof attachmentSchema>>

/** Pull file_attachments off a loosely-typed inbound message. */
export function extractInboundAttachments(msg: unknown): InboundAttachment[] {
  if (typeof msg !== 'object' || msg === null || !('file_attachments' in msg)) {
    return []
  }
  const parsed = attachmentsArraySchema().safeParse(msg.file_attachments)
  return parsed.success ? parsed.data : []
}

/**

```

---


### `src/bridge/inboundMessages.ts`

**信息:**
- 行数: 80
- 大小: 2727 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type {
  Base64ImageSource,
  ContentBlockParam,
  ImageBlockParam,
} from '@anthropic-ai/sdk/resources/messages.mjs'
import type { UUID } from 'crypto'
import type { SDKMessage } from '../entrypoints/agentSdkTypes.js'
import { detectImageFormatFromBase64 } from '../utils/imageResizer.js'

/**
 * Process an inbound user message from the bridge, extracting content
 * and UUID for enqueueing. Supports both string content and
 * ContentBlockParam[] (e.g. messages containing images).
 *
 * Normalizes image blocks from bridge clients that may use camelCase
 * `mediaType` instead of snake_case `media_type` (mobile-apps#5825).
 *
 * Returns the extracted fields, or undefined if the message should be
 * skipped (non-user type, missing/empty content).
 */
export function extractInboundMessageFields(
  msg: SDKMessage,
):
  | { content: string | Array<ContentBlockParam>; uuid: UUID | undefined }
  | undefined {
  if (msg.type !== 'user') return undefined
  const content = msg.message?.content
  if (!content) return undefined
  if (Array.isArray(content) && content.length === 0) return undefined

  const uuid =
    'uuid' in msg && typeof msg.uuid === 'string'
      ? (msg.uuid as UUID)
      : undefined

  return {
    content: Array.isArray(content) ? normalizeImageBlocks(content) : content,
    uuid,
  }
}

/**
 * Normalize image content blocks from bridge clients. iOS/web clients may
 * send `mediaType` (camelCase) instead of `media_type` (snake_case), or
 * omit the field entirely. Without normalization, the bad block poisons
 * the session — every subsequent API call fails with
 * "media_type: Field required".
 *
 * Fast-path scan returns the original array reference when no
 * normalization is needed (zero allocation on the happy path).

```

---


### `src/bridge/initReplBridge.ts`

**信息:**
- 行数: 569
- 大小: 23849 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * REPL-specific wrapper around initBridgeCore. Owns the parts that read
 * bootstrap state — gates, cwd, session ID, git context, OAuth, title
 * derivation — then delegates to the bootstrap-free core.
 *
 * Split out of replBridge.ts because the sessionStorage import
 * (getCurrentSessionTitle) transitively pulls in src/commands.ts → the
 * entire slash command + React component tree (~1300 modules). Keeping
 * initBridgeCore in a file that doesn't touch sessionStorage lets
 * daemonBridge.ts import the core without bloating the Agent SDK bundle.
 *
 * Called via dynamic import by useReplBridge (auto-start) and print.ts
 * (SDK -p mode via query.enableRemoteControl).
 */

import { feature } from 'bun:bundle'
import { hostname } from 'os'
import { getOriginalCwd, getSessionId } from '../bootstrap/state.js'
import type { SDKMessage } from '../entrypoints/agentSdkTypes.js'
import type { SDKControlResponse } from '../entrypoints/sdk/controlTypes.js'
import { getFeatureValue_CACHED_WITH_REFRESH } from '../services/analytics/growthbook.js'
import { getOrganizationUUID } from '../services/oauth/client.js'
import {
  isPolicyAllowed,
  waitForPolicyLimitsToLoad,
} from '../services/policyLimits/index.js'
import type { Message } from '../types/message.js'
import {
  checkAndRefreshOAuthTokenIfNeeded,
  getClaudeAIOAuthTokens,
  handleOAuth401Error,
} from '../utils/auth.js'
import { getGlobalConfig, saveGlobalConfig } from '../utils/config.js'
import { logForDebugging } from '../utils/debug.js'
import { stripDisplayTagsAllowEmpty } from '../utils/displayTags.js'
import { errorMessage } from '../utils/errors.js'
import { getBranch, getRemoteUrl } from '../utils/git.js'
import { toSDKMessages } from '../utils/messages/mappers.js'
import {
  getContentText,
  getMessagesAfterCompactBoundary,
  isSyntheticMessage,
} from '../utils/messages.js'
import type { PermissionMode } from '../utils/permissions/PermissionMode.js'
import { getCurrentSessionTitle } from '../utils/sessionStorage.js'
import {
  extractConversationText,
  generateSessionTitle,
} from '../utils/sessionTitle.js'
import { generateShortWordSlug } from '../utils/words.js'

```

---


### `src/bridge/jwtUtils.ts`

**信息:**
- 行数: 256
- 大小: 9444 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { logEvent } from '../services/analytics/index.js'
import { logForDebugging } from '../utils/debug.js'
import { logForDiagnosticsNoPII } from '../utils/diagLogs.js'
import { errorMessage } from '../utils/errors.js'
import { jsonParse } from '../utils/slowOperations.js'

/** Format a millisecond duration as a human-readable string (e.g. "5m 30s"). */
function formatDuration(ms: number): string {
  if (ms < 60_000) return `${Math.round(ms / 1000)}s`
  const m = Math.floor(ms / 60_000)
  const s = Math.round((ms % 60_000) / 1000)
  return s > 0 ? `${m}m ${s}s` : `${m}m`
}

/**
 * Decode a JWT's payload segment without verifying the signature.
 * Strips the `sk-ant-si-` session-ingress prefix if present.
 * Returns the parsed JSON payload as `unknown`, or `null` if the
 * token is malformed or the payload is not valid JSON.
 */
export function decodeJwtPayload(token: string): unknown | null {
  const jwt = token.startsWith('sk-ant-si-')
    ? token.slice('sk-ant-si-'.length)
    : token
  const parts = jwt.split('.')
  if (parts.length !== 3 || !parts[1]) return null
  try {
    return jsonParse(Buffer.from(parts[1], 'base64url').toString('utf8'))
  } catch {
    return null
  }
}

/**
 * Decode the `exp` (expiry) claim from a JWT without verifying the signature.
 * @returns The `exp` value in Unix seconds, or `null` if unparseable
 */
export function decodeJwtExpiry(token: string): number | null {
  const payload = decodeJwtPayload(token)
  if (
    payload !== null &&
    typeof payload === 'object' &&
    'exp' in payload &&
    typeof payload.exp === 'number'
  ) {
    return payload.exp
  }
  return null
}


```

---


### `src/bridge/peerSessions.ts`

**信息:**
- 行数: 3
- 大小: 51 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function listPeerSessions() {
  return []
}

```

---


### `src/bridge/pollConfig.ts`

**信息:**
- 行数: 110
- 大小: 4562 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { getFeatureValue_CACHED_WITH_REFRESH } from '../services/analytics/growthbook.js'
import { lazySchema } from '../utils/lazySchema.js'
import {
  DEFAULT_POLL_CONFIG,
  type PollIntervalConfig,
} from './pollConfigDefaults.js'

// .min(100) on the seek-work intervals restores the old Math.max(..., 100)
// defense-in-depth floor against fat-fingered GrowthBook values. Unlike a
// clamp, Zod rejects the whole object on violation — a config with one bad
// field falls back to DEFAULT_POLL_CONFIG entirely rather than being
// partially trusted.
//
// The at_capacity intervals use a 0-or-≥100 refinement: 0 means "disabled"
// (heartbeat-only mode), ≥100 is the fat-finger floor. Values 1–99 are
// rejected so unit confusion (ops thinks seconds, enters 10) doesn't poll
// every 10ms against the VerifyEnvironmentSecretAuth DB path.
//
// The object-level refines require at least one at-capacity liveness
// mechanism enabled: heartbeat OR the relevant poll interval. Without this,
// the hb=0, atCapMs=0 drift config (ops disables heartbeat without
// restoring at_capacity) falls through every throttle site with no sleep —
// tight-looping /poll at HTTP-round-trip speed.
const zeroOrAtLeast100 = {
  message: 'must be 0 (disabled) or ≥100ms',
}
const pollIntervalConfigSchema = lazySchema(() =>
  z
    .object({
      poll_interval_ms_not_at_capacity: z.number().int().min(100),
      // 0 = no at-capacity polling. Independent of heartbeat — both can be
      // enabled (heartbeat runs, periodically breaks out to poll).
      poll_interval_ms_at_capacity: z
        .number()
        .int()
        .refine(v => v === 0 || v >= 100, zeroOrAtLeast100),
      // 0 = disabled; positive value = heartbeat at this interval while at
      // capacity. Runs alongside at-capacity polling, not instead of it.
      // Named non_exclusive to distinguish from the old heartbeat_interval_ms
      // (either-or semantics in pre-#22145 clients). .default(0) so existing
      // GrowthBook configs without this field parse successfully.
      non_exclusive_heartbeat_interval_ms: z.number().int().min(0).default(0),
      // Multisession (bridgeMain.ts) intervals. Defaults match the
      // single-session values so existing configs without these fields
      // preserve current behavior.
      multisession_poll_interval_ms_not_at_capacity: z
        .number()
        .int()
        .min(100)

```

---


### `src/bridge/pollConfigDefaults.ts`

**信息:**
- 行数: 82
- 大小: 4018 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Bridge poll interval defaults. Extracted from pollConfig.ts so callers
 * that don't need live GrowthBook tuning (daemon via Agent SDK) can avoid
 * the growthbook.ts → config.ts → file.ts → sessionStorage.ts → commands.ts
 * transitive dependency chain.
 */

/**
 * Poll interval when actively seeking work (no transport / below maxSessions).
 * Governs user-visible "connecting…" latency on initial work pickup and
 * recovery speed after the server re-dispatches a work item.
 */
const POLL_INTERVAL_MS_NOT_AT_CAPACITY = 2000

/**
 * Poll interval when the transport is connected. Runs independently of
 * heartbeat — when both are enabled, the heartbeat loop breaks out to poll
 * at this interval. Set to 0 to disable at-capacity polling entirely.
 *
 * Server-side constraints that bound this value:
 * - BRIDGE_LAST_POLL_TTL = 4h (Redis key expiry → environment auto-archived)
 * - max_poll_stale_seconds = 24h (session-creation health gate, currently disabled)
 *
 * 10 minutes gives 24× headroom on the Redis TTL while still picking up
 * server-initiated token-rotation redispatches within one poll cycle.
 * The transport auto-reconnects internally for 10 minutes on transient WS
 * failures, so poll is not the recovery path — it's strictly a liveness
 * signal plus a backstop for permanent close.
 */
const POLL_INTERVAL_MS_AT_CAPACITY = 600_000

/**
 * Multisession bridge (bridgeMain.ts) poll intervals. Defaults match the
 * single-session values so existing GrowthBook configs without these fields
 * preserve current behavior. Ops can tune these independently via the
 * tengu_bridge_poll_interval_config GB flag.
 */
const MULTISESSION_POLL_INTERVAL_MS_NOT_AT_CAPACITY =
  POLL_INTERVAL_MS_NOT_AT_CAPACITY
const MULTISESSION_POLL_INTERVAL_MS_PARTIAL_CAPACITY =
  POLL_INTERVAL_MS_NOT_AT_CAPACITY
const MULTISESSION_POLL_INTERVAL_MS_AT_CAPACITY = POLL_INTERVAL_MS_AT_CAPACITY

export type PollIntervalConfig = {
  poll_interval_ms_not_at_capacity: number
  poll_interval_ms_at_capacity: number
  non_exclusive_heartbeat_interval_ms: number
  multisession_poll_interval_ms_not_at_capacity: number
  multisession_poll_interval_ms_partial_capacity: number
  multisession_poll_interval_ms_at_capacity: number

```

---


### `src/bridge/remoteBridgeCore.ts`

**信息:**
- 行数: 1008
- 大小: 39434 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
/**
 * Env-less Remote Control bridge core.
 *
 * "Env-less" = no Environments API layer. Distinct from "CCR v2" (the
 * /worker/* transport protocol) — the env-based path (replBridge.ts) can also
 * use CCR v2 transport via CLAUDE_CODE_USE_CCR_V2. This file is about removing
 * the poll/dispatch layer, not about which transport protocol is underneath.
 *
 * Unlike initBridgeCore (env-based, ~2400 lines), this connects directly
 * to the session-ingress layer without the Environments API work-dispatch
 * layer:
 *
 *   1. POST /v1/code/sessions              (OAuth, no env_id)  → session.id
 *   2. POST /v1/code/sessions/{id}/bridge  (OAuth)             → {worker_jwt, expires_in, api_base_url, worker_epoch}
 *      Each /bridge call bumps epoch — it IS the register. No separate /worker/register.
 *   3. createV2ReplTransport(worker_jwt, worker_epoch)         → SSE + CCRClient
 *   4. createTokenRefreshScheduler                             → proactive /bridge re-call (new JWT + new epoch)
 *   5. 401 on SSE → rebuild transport with fresh /bridge credentials (same seq-num)
 *
 * No register/poll/ack/stop/heartbeat/deregister environment lifecycle.
 * The Environments API historically existed because CCR's /worker/*
 * endpoints required a session_id+role=worker JWT that only the work-dispatch
 * layer could mint. Server PR #292605 (renamed in #293280) adds the /bridge endpoint as a direct
 * OAuth→worker_jwt exchange, making the env layer optional for REPL sessions.
 *
 * Gated by `tengu_bridge_repl_v2` GrowthBook flag in initReplBridge.ts.
 * REPL-only — daemon/print stay on env-based.
 */

import { feature } from 'bun:bundle'
import axios from 'axios'
import {
  createV2ReplTransport,
  type ReplBridgeTransport,
} from './replBridgeTransport.js'
import { buildCCRv2SdkUrl } from './workSecret.js'
import { toCompatSessionId } from './sessionIdCompat.js'
import { FlushGate } from './flushGate.js'
import { createTokenRefreshScheduler } from './jwtUtils.js'
import { getTrustedDeviceToken } from './trustedDevice.js'
import {
  getEnvLessBridgeConfig,
  type EnvLessBridgeConfig,
} from './envLessBridgeConfig.js'
import {
  handleIngressMessage,
  handleServerControlRequest,
  makeResultMessage,
  isEligibleBridgeMessage,

```

---


### `src/bridge/replBridge.ts`

**信息:**
- 行数: 2406
- 大小: 100537 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
import { randomUUID } from 'crypto'
import {
  createBridgeApiClient,
  BridgeFatalError,
  isExpiredErrorType,
  isSuppressible403,
} from './bridgeApi.js'
import type { BridgeConfig, BridgeApiClient } from './types.js'
import { logForDebugging } from '../utils/debug.js'
import { logForDiagnosticsNoPII } from '../utils/diagLogs.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import { registerCleanup } from '../utils/cleanupRegistry.js'
import {
  handleIngressMessage,
  handleServerControlRequest,
  makeResultMessage,
  isEligibleBridgeMessage,
  extractTitleText,
  BoundedUUIDSet,
} from './bridgeMessaging.js'
import {
  decodeWorkSecret,
  buildSdkUrl,
  buildCCRv2SdkUrl,
  sameSessionId,
} from './workSecret.js'
import { toCompatSessionId, toInfraSessionId } from './sessionIdCompat.js'
import { updateSessionBridgeId } from '../utils/concurrentSessions.js'
import { getTrustedDeviceToken } from './trustedDevice.js'
import { HybridTransport } from '../cli/transports/HybridTransport.js'
import {
  type ReplBridgeTransport,
  createV1ReplTransport,
  createV2ReplTransport,
} from './replBridgeTransport.js'
import { updateSessionIngressAuthToken } from '../utils/sessionIngressAuth.js'
import { isEnvTruthy, isInProtectedNamespace } from '../utils/envUtils.js'
import { validateBridgeId } from './bridgeApi.js'
import {
  describeAxiosError,
  extractHttpStatus,
  logBridgeSkip,
} from './debugUtils.js'
import type { Message } from '../types/message.js'
import type { SDKMessage } from '../entrypoints/agentSdkTypes.js'
import type { PermissionMode } from '../utils/permissions/PermissionMode.js'

```

---


### `src/bridge/replBridgeHandle.ts`

**信息:**
- 行数: 36
- 大小: 1473 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { updateSessionBridgeId } from '../utils/concurrentSessions.js'
import type { ReplBridgeHandle } from './replBridge.js'
import { toCompatSessionId } from './sessionIdCompat.js'

/**
 * Global pointer to the active REPL bridge handle, so callers outside
 * useReplBridge's React tree (tools, slash commands) can invoke handle methods
 * like subscribePR. Same one-bridge-per-process justification as bridgeDebug.ts
 * — the handle's closure captures the sessionId and getAccessToken that created
 * the session, and re-deriving those independently (BriefTool/upload.ts pattern)
 * risks staging/prod token divergence.
 *
 * Set from useReplBridge.tsx when init completes; cleared on teardown.
 */

let handle: ReplBridgeHandle | null = null

export function setReplBridgeHandle(h: ReplBridgeHandle | null): void {
  handle = h
  // Publish (or clear) our bridge session ID in the session record so other
  // local peers can dedup us out of their bridge list — local is preferred.
  void updateSessionBridgeId(getSelfBridgeCompatId() ?? null).catch(() => {})
}

export function getReplBridgeHandle(): ReplBridgeHandle | null {
  return handle
}

/**
 * Our own bridge session ID in the session_* compat format the API returns
 * in /v1/sessions responses — or undefined if bridge isn't connected.
 */
export function getSelfBridgeCompatId(): string | undefined {
  const h = getReplBridgeHandle()
  return h ? toCompatSessionId(h.bridgeSessionId) : undefined
}

```

---


### `src/bridge/replBridgeTransport.ts`

**信息:**
- 行数: 370
- 大小: 15523 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { StdoutMessage } from 'src/entrypoints/sdk/controlTypes.js'
import { CCRClient } from '../cli/transports/ccrClient.js'
import type { HybridTransport } from '../cli/transports/HybridTransport.js'
import { SSETransport } from '../cli/transports/SSETransport.js'
import { logForDebugging } from '../utils/debug.js'
import { errorMessage } from '../utils/errors.js'
import { updateSessionIngressAuthToken } from '../utils/sessionIngressAuth.js'
import type { SessionState } from '../utils/sessionState.js'
import { registerWorker } from './workSecret.js'

/**
 * Transport abstraction for replBridge. Covers exactly the surface that
 * replBridge.ts uses against HybridTransport so the v1/v2 choice is
 * confined to the construction site.
 *
 * - v1: HybridTransport (WS reads + POST writes to Session-Ingress)
 * - v2: SSETransport (reads) + CCRClient (writes to CCR v2 /worker/*)
 *
 * The v2 write path goes through CCRClient.writeEvent → SerialBatchEventUploader,
 * NOT through SSETransport.write() — SSETransport.write() targets the
 * Session-Ingress POST URL shape, which is wrong for CCR v2.
 */
export type ReplBridgeTransport = {
  write(message: StdoutMessage): Promise<void>
  writeBatch(messages: StdoutMessage[]): Promise<void>
  close(): void
  isConnectedStatus(): boolean
  getStateLabel(): string
  setOnData(callback: (data: string) => void): void
  setOnClose(callback: (closeCode?: number) => void): void
  setOnConnect(callback: () => void): void
  connect(): void
  /**
   * High-water mark of the underlying read stream's event sequence numbers.
   * replBridge reads this before swapping transports so the new one can
   * resume from where the old one left off (otherwise the server replays
   * the entire session history from seq 0).
   *
   * v1 returns 0 — Session-Ingress WS doesn't use SSE sequence numbers;
   * replay-on-reconnect is handled by the server-side message cursor.
   */
  getLastSequenceNum(): number
  /**
   * Monotonic count of batches dropped via maxConsecutiveFailures.
   * Snapshot before writeBatch() and compare after to detect silent drops
   * (writeBatch() resolves normally even when batches were dropped).
   * v2 returns 0 — the v2 write path doesn't set maxConsecutiveFailures.
   */
  readonly droppedBatchCount: number
  /**

```

---


### `src/bridge/sessionIdCompat.ts`

**信息:**
- 行数: 57
- 大小: 2536 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Session ID tag translation helpers for the CCR v2 compat layer.
 *
 * Lives in its own file (rather than workSecret.ts) so that sessionHandle.ts
 * and replBridgeTransport.ts (bridge.mjs entry points) can import from
 * workSecret.ts without pulling in these retag functions.
 *
 * The isCseShimEnabled kill switch is injected via setCseShimGate() to avoid
 * a static import of bridgeEnabled.ts → growthbook.ts → config.ts — all
 * banned from the sdk.mjs bundle (scripts/build-agent-sdk.sh). Callers that
 * already import bridgeEnabled.ts register the gate; the SDK path never does,
 * so the shim defaults to active (matching isCseShimEnabled()'s own default).
 */

let _isCseShimEnabled: (() => boolean) | undefined

/**
 * Register the GrowthBook gate for the cse_ shim. Called from bridge
 * init code that already imports bridgeEnabled.ts.
 */
export function setCseShimGate(gate: () => boolean): void {
  _isCseShimEnabled = gate
}

/**
 * Re-tag a `cse_*` session ID to `session_*` for use with the v1 compat API.
 *
 * Worker endpoints (/v1/code/sessions/{id}/worker/*) want `cse_*`; that's
 * what the work poll delivers. Client-facing compat endpoints
 * (/v1/sessions/{id}, /v1/sessions/{id}/archive, /v1/sessions/{id}/events)
 * want `session_*` — compat/convert.go:27 validates TagSession. Same UUID,
 * different costume. No-op for IDs that aren't `cse_*`.
 *
 * bridgeMain holds one sessionId variable for both worker registration and
 * session-management calls. It arrives as `cse_*` from the work poll under
 * the compat gate, so archiveSession/fetchSessionTitle need this re-tag.
 */
export function toCompatSessionId(id: string): string {
  if (!id.startsWith('cse_')) return id
  if (_isCseShimEnabled && !_isCseShimEnabled()) return id
  return 'session_' + id.slice('cse_'.length)
}

/**
 * Re-tag a `session_*` session ID to `cse_*` for infrastructure-layer calls.
 *
 * Inverse of toCompatSessionId. POST /v1/environments/{id}/bridge/reconnect
 * lives below the compat layer: once ccr_v2_compat_enabled is on server-side,
 * it looks sessions up by their infra tag (`cse_*`). createBridgeSession still
 * returns `session_*` (compat/convert.go:41) and that's what bridge-pointer

```

---


### `src/bridge/sessionRunner.ts`

**信息:**
- 行数: 550
- 大小: 18020 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { type ChildProcess, spawn } from 'child_process'
import { createWriteStream, type WriteStream } from 'fs'
import { tmpdir } from 'os'
import { dirname, join } from 'path'
import { createInterface } from 'readline'
import { jsonParse, jsonStringify } from '../utils/slowOperations.js'
import { debugTruncate } from './debugUtils.js'
import type {
  SessionActivity,
  SessionDoneStatus,
  SessionHandle,
  SessionSpawner,
  SessionSpawnOpts,
} from './types.js'

const MAX_ACTIVITIES = 10
const MAX_STDERR_LINES = 10

/**
 * Sanitize a session ID for use in file names.
 * Strips any characters that could cause path traversal (e.g. `../`, `/`)
 * or other filesystem issues, replacing them with underscores.
 */
export function safeFilenameId(id: string): string {
  return id.replace(/[^a-zA-Z0-9_-]/g, '_')
}

/**
 * A control_request emitted by the child CLI when it needs permission to
 * execute a **specific** tool invocation (not a general capability check).
 * The bridge forwards this to the server so the user can approve/deny.
 */
export type PermissionRequest = {
  type: 'control_request'
  request_id: string
  request: {
    /** Per-invocation permission check — "may I run this tool with these inputs?" */
    subtype: 'can_use_tool'
    tool_name: string
    input: Record<string, unknown>
    tool_use_id: string
  }
}

type SessionSpawnerDeps = {
  execPath: string
  /**
   * Arguments that must precede the CLI flags when spawning. Empty for
   * compiled binaries (where execPath is the claude binary itself); contains
   * the script path (process.argv[1]) for npm installs where execPath is the

```

---


### `src/bridge/trustedDevice.ts`

**信息:**
- 行数: 210
- 大小: 7764 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import memoize from 'lodash-es/memoize.js'
import { hostname } from 'os'
import { getOauthConfig } from '../constants/oauth.js'
import {
  checkGate_CACHED_OR_BLOCKING,
  getFeatureValue_CACHED_MAY_BE_STALE,
} from '../services/analytics/growthbook.js'
import { logForDebugging } from '../utils/debug.js'
import { errorMessage } from '../utils/errors.js'
import { isEssentialTrafficOnly } from '../utils/privacyLevel.js'
import { getSecureStorage } from '../utils/secureStorage/index.js'
import { jsonStringify } from '../utils/slowOperations.js'

/**
 * Trusted device token source for bridge (remote-control) sessions.
 *
 * Bridge sessions have SecurityTier=ELEVATED on the server (CCR v2).
 * The server gates ConnectBridgeWorker on its own flag
 * (sessions_elevated_auth_enforcement in Anthropic Main); this CLI-side
 * flag controls whether the CLI sends X-Trusted-Device-Token at all.
 * Two flags so rollout can be staged: flip CLI-side first (headers
 * start flowing, server still no-ops), then flip server-side.
 *
 * Enrollment (POST /auth/trusted_devices) is gated server-side by
 * account_session.created_at < 10min, so it must happen during /login.
 * Token is persistent (90d rolling expiry) and stored in keychain.
 *
 * See anthropics/anthropic#274559 (spec), #310375 (B1b tenant RPCs),
 * #295987 (B2 Python routes), #307150 (C1' CCR v2 gate).
 */

const TRUSTED_DEVICE_GATE = 'tengu_sessions_elevated_auth_enforcement'

function isGateEnabled(): boolean {
  return getFeatureValue_CACHED_MAY_BE_STALE(TRUSTED_DEVICE_GATE, false)
}

// Memoized — secureStorage.read() spawns a macOS `security` subprocess (~40ms).
// bridgeApi.ts calls this from getHeaders() on every poll/heartbeat/ack.
// Cache cleared after enrollment (below) and on logout (clearAuthRelatedCaches).
//
// Only the storage read is memoized — the GrowthBook gate is checked live so
// that a gate flip after GrowthBook refresh takes effect without a restart.
const readStoredToken = memoize((): string | undefined => {
  // Env var takes precedence for testing/canary.
  const envToken = process.env.CLAUDE_TRUSTED_DEVICE_TOKEN
  if (envToken) {
    return envToken
  }

```

---


### `src/bridge/types.ts`

**信息:**
- 行数: 262
- 大小: 10161 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/** Default per-session timeout (24 hours). */
export const DEFAULT_SESSION_TIMEOUT_MS = 24 * 60 * 60 * 1000

/** Reusable login guidance appended to bridge auth errors. */
export const BRIDGE_LOGIN_INSTRUCTION =
  'Remote Control is only available with claude.ai subscriptions. Please use `/login` to sign in with your claude.ai account.'

/** Full error printed when `claude remote-control` is run without auth. */
export const BRIDGE_LOGIN_ERROR =
  'Error: You must be logged in to use Remote Control.\n\n' +
  BRIDGE_LOGIN_INSTRUCTION

/** Shown when the user disconnects Remote Control (via /remote-control or ultraplan launch). */
export const REMOTE_CONTROL_DISCONNECTED_MSG = 'Remote Control disconnected.'

// --- Protocol types for the environments API ---

export type WorkData = {
  type: 'session' | 'healthcheck'
  id: string
}

export type WorkResponse = {
  id: string
  type: 'work'
  environment_id: string
  state: string
  data: WorkData
  secret: string // base64url-encoded JSON
  created_at: string
}

export type WorkSecret = {
  version: number
  session_ingress_token: string
  api_base_url: string
  sources: Array<{
    type: string
    git_info?: { type: string; repo: string; ref?: string; token?: string }
  }>
  auth: Array<{ type: string; token: string }>
  claude_code_args?: Record<string, string> | null
  mcp_config?: unknown | null
  environment_variables?: Record<string, string> | null
  /**
   * Server-driven CCR v2 selector. Set by prepare_work_secret() when the
   * session was created via the v2 compat layer (ccr_v2_compat_enabled).
   * Same field the BYOC runner reads at environment-runner/sessionExecutor.ts.
   */
  use_code_sessions?: boolean

```

---


### `src/bridge/webhookSanitizer.ts`

**信息:**
- 行数: 3
- 大小: 74 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function sanitizeWebhookPayload<T>(value: T): T {
  return value
}

```

---


### `src/bridge/workSecret.ts`

**信息:**
- 行数: 127
- 大小: 4672 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { jsonParse, jsonStringify } from '../utils/slowOperations.js'
import type { WorkSecret } from './types.js'

/** Decode a base64url-encoded work secret and validate its version. */
export function decodeWorkSecret(secret: string): WorkSecret {
  const json = Buffer.from(secret, 'base64url').toString('utf-8')
  const parsed: unknown = jsonParse(json)
  if (
    !parsed ||
    typeof parsed !== 'object' ||
    !('version' in parsed) ||
    parsed.version !== 1
  ) {
    throw new Error(
      `Unsupported work secret version: ${parsed && typeof parsed === 'object' && 'version' in parsed ? parsed.version : 'unknown'}`,
    )
  }
  const obj = parsed as Record<string, unknown>
  if (
    typeof obj.session_ingress_token !== 'string' ||
    obj.session_ingress_token.length === 0
  ) {
    throw new Error(
      'Invalid work secret: missing or empty session_ingress_token',
    )
  }
  if (typeof obj.api_base_url !== 'string') {
    throw new Error('Invalid work secret: missing api_base_url')
  }
  return parsed as WorkSecret
}

/**
 * Build a WebSocket SDK URL from the API base URL and session ID.
 * Strips the HTTP(S) protocol and constructs a ws(s):// ingress URL.
 *
 * Uses /v2/ for localhost (direct to session-ingress, no Envoy rewrite)
 * and /v1/ for production (Envoy rewrites /v1/ → /v2/).
 */
export function buildSdkUrl(apiBaseUrl: string, sessionId: string): string {
  const isLocalhost =
    apiBaseUrl.includes('localhost') || apiBaseUrl.includes('127.0.0.1')
  const protocol = isLocalhost ? 'ws' : 'wss'
  const version = isLocalhost ? 'v2' : 'v1'
  const host = apiBaseUrl.replace(/^https?:\/\//, '').replace(/\/+$/, '')
  return `${protocol}://${host}/${version}/session_ingress/ws/${sessionId}`
}

/**

```

---

