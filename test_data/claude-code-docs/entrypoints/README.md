# entrypoints 模块

## 概述

**位置:** `src/entrypoints/`

## 文件统计

- TypeScript 文件: 13
- TypeScript React 文件: 1
- 总计: 14

## 文件详情

---


### `src/entrypoints/agentSdkTypes.ts`

**信息:**
- 行数: 443
- 大小: 13076 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Main entrypoint for Claude Code Agent SDK types.
 *
 * This file re-exports the public SDK API from:
 * - sdk/coreTypes.ts - Common serializable types (messages, configs)
 * - sdk/runtimeTypes.ts - Non-serializable types (callbacks, interfaces)
 *
 * SDK builders who need control protocol types should import from
 * sdk/controlTypes.ts directly.
 */

import type {
  CallToolResult,
  ToolAnnotations,
} from '@modelcontextprotocol/sdk/types.js'

// Control protocol types for SDK builders (bridge subpath consumers)
/** @alpha */
export type {
  SDKControlRequest,
  SDKControlResponse,
} from './sdk/controlTypes.js'
// Re-export core types (common serializable types)
export * from './sdk/coreTypes.js'
// Re-export runtime types (callbacks, interfaces with methods)
export * from './sdk/runtimeTypes.js'

// Re-export settings types (generated from settings JSON schema)
export type { Settings } from './sdk/settingsTypes.generated.js'
// Re-export tool types (all marked @internal until SDK API stabilizes)
export * from './sdk/toolTypes.js'

// ============================================================================
// Functions
// ============================================================================

import type {
  SDKMessage,
  SDKResultMessage,
  SDKSessionInfo,
  SDKUserMessage,
} from './sdk/coreTypes.js'
// Import types needed for function signatures
import type {
  AnyZodRawShape,
  ForkSessionOptions,
  ForkSessionResult,
  GetSessionInfoOptions,
  GetSessionMessagesOptions,
  InferShape,

```

---


### `src/entrypoints/cli.tsx`

**信息:**
- 行数: 303
- 大小: 39275 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';

// Bugfix for corepack auto-pinning, which adds yarnpkg to peoples' package.jsons
// eslint-disable-next-line custom-rules/no-top-level-side-effects
process.env.COREPACK_ENABLE_AUTO_PIN = '0';

// Set max heap size for child processes in CCR environments (containers have 16GB)
// eslint-disable-next-line custom-rules/no-top-level-side-effects, custom-rules/no-process-env-top-level, custom-rules/safe-env-boolean-check
if (process.env.CLAUDE_CODE_REMOTE === 'true') {
  // eslint-disable-next-line custom-rules/no-top-level-side-effects, custom-rules/no-process-env-top-level
  const existing = process.env.NODE_OPTIONS || '';
  // eslint-disable-next-line custom-rules/no-top-level-side-effects, custom-rules/no-process-env-top-level
  process.env.NODE_OPTIONS = existing ? `${existing} --max-old-space-size=8192` : '--max-old-space-size=8192';
}

// Harness-science L0 ablation baseline. Inlined here (not init.ts) because
// BashTool/AgentTool/PowerShellTool capture DISABLE_BACKGROUND_TASKS into
// module-level consts at import time — init() runs too late. feature() gate
// DCEs this entire block from external builds.
// eslint-disable-next-line custom-rules/no-top-level-side-effects, custom-rules/no-process-env-top-level
if (feature('ABLATION_BASELINE') && process.env.CLAUDE_CODE_ABLATION_BASELINE) {
  for (const k of ['CLAUDE_CODE_SIMPLE', 'CLAUDE_CODE_DISABLE_THINKING', 'DISABLE_INTERLEAVED_THINKING', 'DISABLE_COMPACT', 'DISABLE_AUTO_COMPACT', 'CLAUDE_CODE_DISABLE_AUTO_MEMORY', 'CLAUDE_CODE_DISABLE_BACKGROUND_TASKS']) {
    // eslint-disable-next-line custom-rules/no-top-level-side-effects, custom-rules/no-process-env-top-level
    process.env[k] ??= '1';
  }
}

/**
 * Bootstrap entrypoint - checks for special flags before loading the full CLI.
 * All imports are dynamic to minimize module evaluation for fast paths.
 * Fast-path for --version has zero imports beyond this file.
 */
async function main(): Promise<void> {
  const args = process.argv.slice(2);

  // Fast-path for --version/-v: zero module loading needed
  if (args.length === 1 && (args[0] === '--version' || args[0] === '-v' || args[0] === '-V')) {
    // MACRO.VERSION is inlined at build time
    // biome-ignore lint/suspicious/noConsole:: intentional console output
    console.log(`${MACRO.VERSION} (Claude Code)`);
    return;
  }

  // For all other paths, load the startup profiler
  const {
    profileCheckpoint
  } = await import('../utils/startupProfiler.js');
  profileCheckpoint('cli_entry');

  // Fast-path for --dump-system-prompt: output the rendered system prompt and exit.

```

---


### `src/entrypoints/init.ts`

**信息:**
- 行数: 340
- 大小: 13780 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { profileCheckpoint } from '../utils/startupProfiler.js'
import '../bootstrap/state.js'
import '../utils/config.js'
import type { Attributes, MetricOptions } from '@opentelemetry/api'
import memoize from 'lodash-es/memoize.js'
import { getIsNonInteractiveSession } from 'src/bootstrap/state.js'
import type { AttributedCounter } from '../bootstrap/state.js'
import { getSessionCounter, setMeter } from '../bootstrap/state.js'
import { shutdownLspServerManager } from '../services/lsp/manager.js'
import { populateOAuthAccountInfoIfNeeded } from '../services/oauth/client.js'
import {
  initializePolicyLimitsLoadingPromise,
  isPolicyLimitsEligible,
} from '../services/policyLimits/index.js'
import {
  initializeRemoteManagedSettingsLoadingPromise,
  isEligibleForRemoteManagedSettings,
  waitForRemoteManagedSettingsToLoad,
} from '../services/remoteManagedSettings/index.js'
import { preconnectAnthropicApi } from '../utils/apiPreconnect.js'
import { applyExtraCACertsFromConfig } from '../utils/caCertsConfig.js'
import { registerCleanup } from '../utils/cleanupRegistry.js'
import { enableConfigs, recordFirstStartTime } from '../utils/config.js'
import { logForDebugging } from '../utils/debug.js'
import { detectCurrentRepository } from '../utils/detectRepository.js'
import { logForDiagnosticsNoPII } from '../utils/diagLogs.js'
import { initJetBrainsDetection } from '../utils/envDynamic.js'
import { isEnvTruthy } from '../utils/envUtils.js'
import { ConfigParseError, errorMessage } from '../utils/errors.js'
// showInvalidConfigDialog is dynamically imported in the error path to avoid loading React at init
import {
  gracefulShutdownSync,
  setupGracefulShutdown,
} from '../utils/gracefulShutdown.js'
import {
  applyConfigEnvironmentVariables,
  applySafeConfigEnvironmentVariables,
} from '../utils/managedEnv.js'
import { configureGlobalMTLS } from '../utils/mtls.js'
import {
  ensureScratchpadDir,
  isScratchpadEnabled,
} from '../utils/permissions/filesystem.js'
// initializeTelemetry is loaded lazily via import() in setMeterState() to defer
// ~400KB of OpenTelemetry + protobuf modules until telemetry is actually initialized.
// gRPC exporters (~700KB via @grpc/grpc-js) are further lazy-loaded within instrumentation.ts.
import { configureGlobalAgents } from '../utils/proxy.js'
import { isBetaTracingEnabled } from '../utils/telemetry/betaSessionTracing.js'
import { getTelemetryAttributes } from '../utils/telemetryAttributes.js'
import { setShellIfWindows } from '../utils/windowsPaths.js'

```

---


### `src/entrypoints/mcp.ts`

**信息:**
- 行数: 196
- 大小: 6270 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import {
  CallToolRequestSchema,
  type CallToolResult,
  ListToolsRequestSchema,
  type ListToolsResult,
  type Tool,
} from '@modelcontextprotocol/sdk/types.js'
import { getDefaultAppState } from 'src/state/AppStateStore.js'
import review from '../commands/review.js'
import type { Command } from '../commands.js'
import {
  findToolByName,
  getEmptyToolPermissionContext,
  type ToolUseContext,
} from '../Tool.js'
import { getTools } from '../tools.js'
import { createAbortController } from '../utils/abortController.js'
import { createFileStateCacheWithSizeLimit } from '../utils/fileStateCache.js'
import { logError } from '../utils/log.js'
import { createAssistantMessage } from '../utils/messages.js'
import { getMainLoopModel } from '../utils/model/model.js'
import { hasPermissionsToUseTool } from '../utils/permissions/permissions.js'
import { setCwd } from '../utils/Shell.js'
import { jsonStringify } from '../utils/slowOperations.js'
import { getErrorParts } from '../utils/toolErrors.js'
import { zodToJsonSchema } from '../utils/zodToJsonSchema.js'

type ToolInput = Tool['inputSchema']
type ToolOutput = Tool['outputSchema']

const MCP_COMMANDS: Command[] = [review]

export async function startMCPServer(
  cwd: string,
  debug: boolean,
  verbose: boolean,
): Promise<void> {
  // Use size-limited LRU cache for readFileState to prevent unbounded memory growth
  // 100 files and 25MB limit should be sufficient for MCP server operations
  const READ_FILE_STATE_CACHE_SIZE = 100
  const readFileStateCache = createFileStateCacheWithSizeLimit(
    READ_FILE_STATE_CACHE_SIZE,
  )
  setCwd(cwd)
  const server = new Server(
    {
      name: 'claude/tengu',
      version: MACRO.VERSION,

```

---


### `src/entrypoints/sandboxTypes.ts`

**信息:**
- 行数: 156
- 大小: 5735 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Sandbox types for the Claude Code Agent SDK
 *
 * This file is the single source of truth for sandbox configuration types.
 * Both the SDK and the settings validation import from here.
 */

import { z } from 'zod/v4'
import { lazySchema } from '../utils/lazySchema.js'

/**
 * Network configuration schema for sandbox.
 */
export const SandboxNetworkConfigSchema = lazySchema(() =>
  z
    .object({
      allowedDomains: z.array(z.string()).optional(),
      allowManagedDomainsOnly: z
        .boolean()
        .optional()
        .describe(
          'When true (and set in managed settings), only allowedDomains and WebFetch(domain:...) allow rules from managed settings are respected. ' +
            'User, project, local, and flag settings domains are ignored. Denied domains are still respected from all sources.',
        ),
      allowUnixSockets: z
        .array(z.string())
        .optional()
        .describe(
          'macOS only: Unix socket paths to allow. Ignored on Linux (seccomp cannot filter by path).',
        ),
      allowAllUnixSockets: z
        .boolean()
        .optional()
        .describe(
          'If true, allow all Unix sockets (disables blocking on both platforms).',
        ),
      allowLocalBinding: z.boolean().optional(),
      httpProxyPort: z.number().optional(),
      socksProxyPort: z.number().optional(),
    })
    .optional(),
)

/**
 * Filesystem configuration schema for sandbox.
 */
export const SandboxFilesystemConfigSchema = lazySchema(() =>
  z
    .object({
      allowWrite: z

```

---


### `src/entrypoints/sdk/controlSchemas.ts`

**信息:**
- 行数: 663
- 大小: 19554 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * SDK Control Schemas - Zod schemas for the control protocol.
 *
 * These schemas define the control protocol between SDK implementations and the CLI.
 * Used by SDK builders (e.g., Python SDK) to communicate with the CLI process.
 *
 * SDK consumers should use coreSchemas.ts instead.
 */

import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'
import {
  AccountInfoSchema,
  AgentDefinitionSchema,
  AgentInfoSchema,
  FastModeStateSchema,
  HookEventSchema,
  HookInputSchema,
  McpServerConfigForProcessTransportSchema,
  McpServerStatusSchema,
  ModelInfoSchema,
  PermissionModeSchema,
  PermissionUpdateSchema,
  SDKMessageSchema,
  SDKPostTurnSummaryMessageSchema,
  SDKStreamlinedTextMessageSchema,
  SDKStreamlinedToolUseSummaryMessageSchema,
  SDKUserMessageSchema,
  SlashCommandSchema,
} from './coreSchemas.js'

// ============================================================================
// External Type Placeholders
// ============================================================================

// JSONRPCMessage from @modelcontextprotocol/sdk - treat as unknown
export const JSONRPCMessagePlaceholder = lazySchema(() => z.unknown())

// ============================================================================
// Hook Callback Types
// ============================================================================

export const SDKHookCallbackMatcherSchema = lazySchema(() =>
  z
    .object({
      matcher: z.string().optional(),
      hookCallbackIds: z.array(z.string()),
      timeout: z.number().optional(),
    })
    .describe('Configuration for matching and routing hook callbacks.'),

```

---


### `src/entrypoints/sdk/controlTypes.ts`

**信息:**
- 行数: 62
- 大小: 1204 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type SDKControlInitializeRequest = {
  subtype: 'initialize'
  [key: string]: unknown
}

export type SDKControlCancelRequest = {
  subtype: 'cancel'
  [key: string]: unknown
}

export type SDKControlPermissionRequest = {
  subtype: 'permission'
  [key: string]: unknown
}

export type SDKControlRequestInner =
  | SDKControlInitializeRequest
  | SDKControlCancelRequest
  | SDKControlPermissionRequest
  | { subtype: string; [key: string]: unknown }

export type SDKControlRequest = {
  type: 'control_request'
  request_id: string
  request: SDKControlRequestInner
}

export type SDKControlInitializeResponse = {
  ok?: boolean
  [key: string]: unknown
}

export type SDKControlMcpSetServersResponse = {
  ok?: boolean
  [key: string]: unknown
}

export type SDKControlReloadPluginsResponse = {
  ok?: boolean
  [key: string]: unknown
}

export type SDKControlResponse = {
  type: 'control_response'
  request_id?: string
  response: Record<string, unknown>
}

export type SDKPartialAssistantMessage = {
  type: 'assistant'

```

---


### `src/entrypoints/sdk/coreSchemas.ts`

**信息:**
- 行数: 1889
- 大小: 56493 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * SDK Core Schemas - Zod schemas for serializable SDK data types.
 *
 * These schemas are the single source of truth for SDK data types.
 * TypeScript types are generated from these schemas and committed for IDE support.
 *
 * @see scripts/generate-sdk-types.ts for type generation
 */

import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'

// ============================================================================
// Usage & Model Types
// ============================================================================

export const ModelUsageSchema = lazySchema(() =>
  z.object({
    inputTokens: z.number(),
    outputTokens: z.number(),
    cacheReadInputTokens: z.number(),
    cacheCreationInputTokens: z.number(),
    webSearchRequests: z.number(),
    costUSD: z.number(),
    contextWindow: z.number(),
    maxOutputTokens: z.number(),
  }),
)

// ============================================================================
// Output Format Types
// ============================================================================

export const OutputFormatTypeSchema = lazySchema(() => z.literal('json_schema'))

export const BaseOutputFormatSchema = lazySchema(() =>
  z.object({
    type: OutputFormatTypeSchema(),
  }),
)

export const JsonSchemaOutputFormatSchema = lazySchema(() =>
  z.object({
    type: z.literal('json_schema'),
    schema: z.record(z.string(), z.unknown()),
  }),
)

export const OutputFormatSchema = lazySchema(() =>
  JsonSchemaOutputFormatSchema(),

```

---


### `src/entrypoints/sdk/coreTypes.generated.ts`

**信息:**
- 行数: 10
- 大小: 263 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type SDKMessage = {
  type: string
  uuid?: string
  [key: string]: unknown
}

export type SDKUserMessage = SDKMessage
export type SDKResultMessage = SDKMessage
export type SDKResultSuccess = SDKMessage
export type SDKSessionInfo = Record<string, unknown>

```

---


### `src/entrypoints/sdk/coreTypes.ts`

**信息:**
- 行数: 62
- 大小: 1466 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// SDK Core Types - Common serializable types used by both SDK consumers and SDK builders.
//
// Types are generated from Zod schemas in coreSchemas.ts.
// To modify types:
// 1. Edit Zod schemas in coreSchemas.ts
// 2. Run: bun scripts/generate-sdk-types.ts
//
// Schemas are available in coreSchemas.ts for runtime validation but are not
// part of the public API.

// Re-export sandbox types for SDK consumers
export type {
  SandboxFilesystemConfig,
  SandboxIgnoreViolations,
  SandboxNetworkConfig,
  SandboxSettings,
} from '../sandboxTypes.js'
// Re-export all generated types
export * from './coreTypes.generated.js'

// Re-export utility types that can't be expressed as Zod schemas
export type { NonNullableUsage } from './sdkUtilityTypes.js'

// Const arrays for runtime usage
export const HOOK_EVENTS = [
  'PreToolUse',
  'PostToolUse',
  'PostToolUseFailure',
  'Notification',
  'UserPromptSubmit',
  'SessionStart',
  'SessionEnd',
  'Stop',
  'StopFailure',
  'SubagentStart',
  'SubagentStop',
  'PreCompact',
  'PostCompact',
  'PermissionRequest',
  'PermissionDenied',
  'Setup',
  'TeammateIdle',
  'TaskCreated',
  'TaskCompleted',
  'Elicitation',
  'ElicitationResult',
  'ConfigChange',
  'WorktreeCreate',
  'WorktreeRemove',
  'InstructionsLoaded',

```

---


### `src/entrypoints/sdk/runtimeTypes.ts`

**信息:**
- 行数: 22
- 大小: 1066 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type EffortLevel = 'low' | 'medium' | 'high' | string
export type SDKSession = Record<string, unknown>
export type SDKSessionOptions = Record<string, unknown>
export type SDKSessionInfo = Record<string, unknown>
export type SessionMessage = Record<string, unknown>
export type ListSessionsOptions = Record<string, unknown>
export type GetSessionInfoOptions = Record<string, unknown>
export type GetSessionMessagesOptions = Record<string, unknown>
export type SessionMutationOptions = Record<string, unknown>
export type ForkSessionOptions = Record<string, unknown>
export type ForkSessionResult = Record<string, unknown>
export type Options = Record<string, unknown>
export type InternalOptions = Record<string, unknown>
export type Query = Record<string, unknown>
export type InternalQuery = Record<string, unknown>
export type McpSdkServerConfigWithInstance = Record<string, unknown>
export type AnyZodRawShape = Record<string, unknown>
export type InferShape<T> = T
export type SdkMcpToolDefinition<Schema> = {
  schema?: Schema
  [key: string]: unknown
}

```

---


### `src/entrypoints/sdk/sdkUtilityTypes.ts`

**信息:**
- 行数: 6
- 大小: 156 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type NonNullableUsage = {
  input_tokens: number
  output_tokens: number
  cache_creation_input_tokens?: number
  cache_read_input_tokens?: number
}

```

---


### `src/entrypoints/sdk/settingsTypes.generated.ts`

**信息:**
- 行数: 1
- 大小: 47 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type Settings = Record<string, unknown>

```

---


### `src/entrypoints/sdk/toolTypes.ts`

**信息:**
- 行数: 1
- 大小: 56 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type SDKToolDefinition = Record<string, unknown>

```

---

