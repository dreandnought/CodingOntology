# services 模块

## 概述

**位置:** `src/services/`

## 文件统计

- TypeScript 文件: 145
- TypeScript React 文件: 3
- 总计: 148

## 文件详情

---


### `src/services/AgentSummary/agentSummary.ts`

**信息:**
- 行数: 179
- 大小: 6407 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Periodic background summarization for coordinator mode sub-agents.
 *
 * Forks the sub-agent's conversation every ~30s using runForkedAgent()
 * to generate a 1-2 sentence progress summary. The summary is stored
 * on AgentProgress for UI display.
 *
 * Cache sharing: uses the same CacheSafeParams as the parent agent
 * to share the prompt cache. Tools are kept in the request for cache
 * key matching but denied via canUseTool callback.
 */

import type { TaskContext } from '../../Task.js'
import { updateAgentSummary } from '../../tasks/LocalAgentTask/LocalAgentTask.js'
import { filterIncompleteToolCalls } from '../../tools/AgentTool/runAgent.js'
import type { AgentId } from '../../types/ids.js'
import { logForDebugging } from '../../utils/debug.js'
import {
  type CacheSafeParams,
  runForkedAgent,
} from '../../utils/forkedAgent.js'
import { logError } from '../../utils/log.js'
import { createUserMessage } from '../../utils/messages.js'
import { getAgentTranscript } from '../../utils/sessionStorage.js'

const SUMMARY_INTERVAL_MS = 30_000

function buildSummaryPrompt(previousSummary: string | null): string {
  const prevLine = previousSummary
    ? `\nPrevious: "${previousSummary}" — say something NEW.\n`
    : ''

  return `Describe your most recent action in 3-5 words using present tense (-ing). Name the file or function, not the branch. Do not use tools.
${prevLine}
Good: "Reading runAgent.ts"
Good: "Fixing null check in validate.ts"
Good: "Running auth module tests"
Good: "Adding retry logic to fetchUser"

Bad (past tense): "Analyzed the branch diff"
Bad (too vague): "Investigating the issue"
Bad (too long): "Reviewing full branch diff and AgentTool.tsx integration"
Bad (branch name): "Analyzed adam/background-summary branch diff"`
}

export function startAgentSummarization(
  taskId: string,
  agentId: AgentId,
  cacheSafeParams: CacheSafeParams,
  setAppState: TaskContext['setAppState'],

```

---


### `src/services/MagicDocs/magicDocs.ts`

**信息:**
- 行数: 254
- 大小: 7683 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Magic Docs automatically maintains markdown documentation files marked with special headers.
 * When a file with "# MAGIC DOC: [title]" is read, it runs periodically in the background
 * using a forked subagent to update the document with new learnings from the conversation.
 *
 * See docs/magic-docs.md for more information.
 */

import type { Tool, ToolUseContext } from '../../Tool.js'
import type { BuiltInAgentDefinition } from '../../tools/AgentTool/loadAgentsDir.js'
import { runAgent } from '../../tools/AgentTool/runAgent.js'
import { FILE_EDIT_TOOL_NAME } from '../../tools/FileEditTool/constants.js'
import {
  FileReadTool,
  type Output as FileReadToolOutput,
  registerFileReadListener,
} from '../../tools/FileReadTool/FileReadTool.js'
import { isFsInaccessible } from '../../utils/errors.js'
import { cloneFileStateCache } from '../../utils/fileStateCache.js'
import {
  type REPLHookContext,
  registerPostSamplingHook,
} from '../../utils/hooks/postSamplingHooks.js'
import {
  createUserMessage,
  hasToolCallsInLastAssistantTurn,
} from '../../utils/messages.js'
import { sequential } from '../../utils/sequential.js'
import { buildMagicDocsUpdatePrompt } from './prompts.js'

// Magic Doc header pattern: # MAGIC DOC: [title]
// Matches at the start of the file (first line)
const MAGIC_DOC_HEADER_PATTERN = /^#\s*MAGIC\s+DOC:\s*(.+)$/im
// Pattern to match italics on the line immediately after the header
const ITALICS_PATTERN = /^[_*](.+?)[_*]\s*$/m

// Track magic docs
type MagicDocInfo = {
  path: string
}

const trackedMagicDocs = new Map<string, MagicDocInfo>()

export function clearTrackedMagicDocs(): void {
  trackedMagicDocs.clear()
}

/**
 * Detect if a file content contains a Magic Doc header
 * Returns an object with title and optional instructions, or null if not a magic doc

```

---


### `src/services/MagicDocs/prompts.ts`

**信息:**
- 行数: 127
- 大小: 5595 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { join } from 'path'
import { getClaudeConfigHomeDir } from '../../utils/envUtils.js'
import { getFsImplementation } from '../../utils/fsOperations.js'

/**
 * Get the Magic Docs update prompt template
 */
function getUpdatePromptTemplate(): string {
  return `IMPORTANT: This message and these instructions are NOT part of the actual user conversation. Do NOT include any references to "documentation updates", "magic docs", or these update instructions in the document content.

Based on the user conversation above (EXCLUDING this documentation update instruction message), update the Magic Doc file to incorporate any NEW learnings, insights, or information that would be valuable to preserve.

The file {{docPath}} has already been read for you. Here are its current contents:
<current_doc_content>
{{docContents}}
</current_doc_content>

Document title: {{docTitle}}
{{customInstructions}}

Your ONLY task is to use the Edit tool to update the documentation file if there is substantial new information to add, then stop. You can make multiple edits (update multiple sections as needed) - make all Edit tool calls in parallel in a single message. If there's nothing substantial to add, simply respond with a brief explanation and do not call any tools.

CRITICAL RULES FOR EDITING:
- Preserve the Magic Doc header exactly as-is: # MAGIC DOC: {{docTitle}}
- If there's an italicized line immediately after the header, preserve it exactly as-is
- Keep the document CURRENT with the latest state of the codebase - this is NOT a changelog or history
- Update information IN-PLACE to reflect the current state - do NOT append historical notes or track changes over time
- Remove or replace outdated information rather than adding "Previously..." or "Updated to..." notes
- Clean up or DELETE sections that are no longer relevant or don't align with the document's purpose
- Fix obvious errors: typos, grammar mistakes, broken formatting, incorrect information, or confusing statements
- Keep the document well organized: use clear headings, logical section order, consistent formatting, and proper nesting

DOCUMENTATION PHILOSOPHY - READ CAREFULLY:
- BE TERSE. High signal only. No filler words or unnecessary elaboration.
- Documentation is for OVERVIEWS, ARCHITECTURE, and ENTRY POINTS - not detailed code walkthroughs
- Do NOT duplicate information that's already obvious from reading the source code
- Do NOT document every function, parameter, or line number reference
- Focus on: WHY things exist, HOW components connect, WHERE to start reading, WHAT patterns are used
- Skip: detailed implementation steps, exhaustive API docs, play-by-play narratives

What TO document:
- High-level architecture and system design
- Non-obvious patterns, conventions, or gotchas
- Key entry points and where to start reading code
- Important design decisions and their rationale
- Critical dependencies or integration points
- References to related files, docs, or code (like a wiki) - help readers navigate to relevant context

What NOT to document:
- Anything obvious from reading the code itself

```

---


### `src/services/PromptSuggestion/promptSuggestion.ts`

**信息:**
- 行数: 523
- 大小: 17065 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getIsNonInteractiveSession } from '../../bootstrap/state.js'
import type { AppState } from '../../state/AppState.js'
import type { Message } from '../../types/message.js'
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js'
import { count } from '../../utils/array.js'
import { isEnvDefinedFalsy, isEnvTruthy } from '../../utils/envUtils.js'
import { toError } from '../../utils/errors.js'
import {
  type CacheSafeParams,
  createCacheSafeParams,
  runForkedAgent,
} from '../../utils/forkedAgent.js'
import type { REPLHookContext } from '../../utils/hooks/postSamplingHooks.js'
import { logError } from '../../utils/log.js'
import {
  createUserMessage,
  getLastAssistantMessage,
} from '../../utils/messages.js'
import { getInitialSettings } from '../../utils/settings/settings.js'
import { isTeammate } from '../../utils/teammate.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../analytics/growthbook.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'
import { currentLimits } from '../claudeAiLimits.js'
import { isSpeculationEnabled, startSpeculation } from './speculation.js'

let currentAbortController: AbortController | null = null

export type PromptVariant = 'user_intent' | 'stated_intent'

export function getPromptVariant(): PromptVariant {
  return 'user_intent'
}

export function shouldEnablePromptSuggestion(): boolean {
  // Env var overrides everything (for testing)
  const envOverride = process.env.CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION
  if (isEnvDefinedFalsy(envOverride)) {
    logEvent('tengu_prompt_suggestion_init', {
      enabled: false,
      source:
        'env' as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
    })
    return false
  }
  if (isEnvTruthy(envOverride)) {
    logEvent('tengu_prompt_suggestion_init', {
      enabled: true,

```

---


### `src/services/PromptSuggestion/speculation.ts`

**信息:**
- 行数: 991
- 大小: 30680 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { randomUUID } from 'crypto'
import { rm } from 'fs'
import { appendFile, copyFile, mkdir } from 'fs/promises'
import { dirname, isAbsolute, join, relative } from 'path'
import { getCwdState } from '../../bootstrap/state.js'
import type { CompletionBoundary } from '../../state/AppStateStore.js'
import {
  type AppState,
  IDLE_SPECULATION_STATE,
  type SpeculationResult,
  type SpeculationState,
} from '../../state/AppStateStore.js'
import { commandHasAnyCd } from '../../tools/BashTool/bashPermissions.js'
import { checkReadOnlyConstraints } from '../../tools/BashTool/readOnlyValidation.js'
import type { SpeculationAcceptMessage } from '../../types/logs.js'
import type { Message } from '../../types/message.js'
import { createChildAbortController } from '../../utils/abortController.js'
import { count } from '../../utils/array.js'
import { getGlobalConfig } from '../../utils/config.js'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import {
  type FileStateCache,
  mergeFileStateCaches,
  READ_FILE_STATE_CACHE_SIZE,
} from '../../utils/fileStateCache.js'
import {
  type CacheSafeParams,
  createCacheSafeParams,
  runForkedAgent,
} from '../../utils/forkedAgent.js'
import { formatDuration, formatNumber } from '../../utils/format.js'
import type { REPLHookContext } from '../../utils/hooks/postSamplingHooks.js'
import { logError } from '../../utils/log.js'
import type { SetAppState } from '../../utils/messageQueueManager.js'
import {
  createSystemMessage,
  createUserMessage,
  INTERRUPT_MESSAGE,
  INTERRUPT_MESSAGE_FOR_TOOL_USE,
} from '../../utils/messages.js'
import { getClaudeTempDir } from '../../utils/permissions/filesystem.js'
import { extractReadFilesFromMessages } from '../../utils/queryHelpers.js'
import { getTranscriptPath } from '../../utils/sessionStorage.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'
import {

```

---


### `src/services/SessionMemory/prompts.ts`

**信息:**
- 行数: 324
- 大小: 12629 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { readFile } from 'fs/promises'
import { join } from 'path'
import { roughTokenCountEstimation } from '../../services/tokenEstimation.js'
import { getClaudeConfigHomeDir } from '../../utils/envUtils.js'
import { getErrnoCode, toError } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'

const MAX_SECTION_LENGTH = 2000
const MAX_TOTAL_SESSION_MEMORY_TOKENS = 12000

export const DEFAULT_SESSION_MEMORY_TEMPLATE = `
# Session Title
_A short and distinctive 5-10 word descriptive title for the session. Super info dense, no filler_

# Current State
_What is actively being worked on right now? Pending tasks not yet completed. Immediate next steps._

# Task specification
_What did the user ask to build? Any design decisions or other explanatory context_

# Files and Functions
_What are the important files? In short, what do they contain and why are they relevant?_

# Workflow
_What bash commands are usually run and in what order? How to interpret their output if not obvious?_

# Errors & Corrections
_Errors encountered and how they were fixed. What did the user correct? What approaches failed and should not be tried again?_

# Codebase and System Documentation
_What are the important system components? How do they work/fit together?_

# Learnings
_What has worked well? What has not? What to avoid? Do not duplicate items from other sections_

# Key results
_If the user asked a specific output such as an answer to a question, a table, or other document, repeat the exact result here_

# Worklog
_Step by step, what was attempted, done? Very terse summary for each step_
`

function getDefaultUpdatePrompt(): string {
  return `IMPORTANT: This message and these instructions are NOT part of the actual user conversation. Do NOT include any references to "note-taking", "session notes extraction", or these update instructions in the notes content.

Based on the user conversation above (EXCLUDING this note-taking instruction message as well as system prompt, claude.md entries, or any past session summaries), update the session notes file.

The file {{notesPath}} has already been read for you. Here are its current contents:
<current_notes_content>
{{currentNotes}}

```

---


### `src/services/SessionMemory/sessionMemory.ts`

**信息:**
- 行数: 495
- 大小: 16561 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Session Memory automatically maintains a markdown file with notes about the current conversation.
 * It runs periodically in the background using a forked subagent to extract key information
 * without interrupting the main conversation flow.
 */

import { writeFile } from 'fs/promises'
import memoize from 'lodash-es/memoize.js'
import { getIsRemoteMode } from '../../bootstrap/state.js'
import { getSystemPrompt } from '../../constants/prompts.js'
import { getSystemContext, getUserContext } from '../../context.js'
import type { CanUseToolFn } from '../../hooks/useCanUseTool.js'
import type { Tool, ToolUseContext } from '../../Tool.js'
import { FILE_EDIT_TOOL_NAME } from '../../tools/FileEditTool/constants.js'
import {
  FileReadTool,
  type Output as FileReadToolOutput,
} from '../../tools/FileReadTool/FileReadTool.js'
import type { Message } from '../../types/message.js'
import { count } from '../../utils/array.js'
import {
  createCacheSafeParams,
  createSubagentContext,
  runForkedAgent,
} from '../../utils/forkedAgent.js'
import { getFsImplementation } from '../../utils/fsOperations.js'
import {
  type REPLHookContext,
  registerPostSamplingHook,
} from '../../utils/hooks/postSamplingHooks.js'
import {
  createUserMessage,
  hasToolCallsInLastAssistantTurn,
} from '../../utils/messages.js'
import {
  getSessionMemoryDir,
  getSessionMemoryPath,
} from '../../utils/permissions/filesystem.js'
import { sequential } from '../../utils/sequential.js'
import { asSystemPrompt } from '../../utils/systemPromptType.js'
import { getTokenUsage, tokenCountWithEstimation } from '../../utils/tokens.js'
import { logEvent } from '../analytics/index.js'
import { isAutoCompactEnabled } from '../compact/autoCompact.js'
import {
  buildSessionMemoryUpdatePrompt,
  loadSessionMemoryTemplate,
} from './prompts.js'
import {
  DEFAULT_SESSION_MEMORY_CONFIG,
  getSessionMemoryConfig,

```

---


### `src/services/SessionMemory/sessionMemoryUtils.ts`

**信息:**
- 行数: 207
- 大小: 6110 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Session Memory utility functions that can be imported without circular dependencies.
 * These are separate from the main sessionMemory.ts to avoid importing runAgent.
 */

import { isFsInaccessible } from '../../utils/errors.js'
import { getFsImplementation } from '../../utils/fsOperations.js'
import { getSessionMemoryPath } from '../../utils/permissions/filesystem.js'
import { sleep } from '../../utils/sleep.js'
import { logEvent } from '../analytics/index.js'

const EXTRACTION_WAIT_TIMEOUT_MS = 15000
const EXTRACTION_STALE_THRESHOLD_MS = 60000 // 1 minute

/**
 * Configuration for session memory extraction thresholds
 */
export type SessionMemoryConfig = {
  /** Minimum context window tokens before initializing session memory.
   * Uses the same token counting as autocompact (input + output + cache tokens)
   * to ensure consistent behavior between the two features. */
  minimumMessageTokensToInit: number
  /** Minimum context window growth (in tokens) between session memory updates.
   * Uses the same token counting as autocompact (tokenCountWithEstimation)
   * to measure actual context growth, not cumulative API usage. */
  minimumTokensBetweenUpdate: number
  /** Number of tool calls between session memory updates */
  toolCallsBetweenUpdates: number
}

// Default configuration values
export const DEFAULT_SESSION_MEMORY_CONFIG: SessionMemoryConfig = {
  minimumMessageTokensToInit: 10000,
  minimumTokensBetweenUpdate: 5000,
  toolCallsBetweenUpdates: 3,
}

// Current session memory configuration
let sessionMemoryConfig: SessionMemoryConfig = {
  ...DEFAULT_SESSION_MEMORY_CONFIG,
}

// Track the last summarized message ID (shared state)
let lastSummarizedMessageId: string | undefined

// Track extraction state with timestamp (set by sessionMemory.ts)
let extractionStartedAt: number | undefined

// Track context size at last memory extraction (for minimumTokensBetweenUpdate)
let tokensAtLastExtraction = 0

```

---


### `src/services/analytics/config.ts`

**信息:**
- 行数: 38
- 大小: 1237 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Shared analytics configuration
 *
 * Common logic for determining when analytics should be disabled
 * across all analytics systems (Datadog, 1P)
 */

import { isEnvTruthy } from '../../utils/envUtils.js'
import { isTelemetryDisabled } from '../../utils/privacyLevel.js'

/**
 * Check if analytics operations should be disabled
 *
 * Analytics is disabled in the following cases:
 * - Test environment (NODE_ENV === 'test')
 * - Third-party cloud providers (Bedrock/Vertex)
 * - Privacy level is no-telemetry or essential-traffic
 */
export function isAnalyticsDisabled(): boolean {
  return (
    process.env.NODE_ENV === 'test' ||
    isEnvTruthy(process.env.CLAUDE_CODE_USE_BEDROCK) ||
    isEnvTruthy(process.env.CLAUDE_CODE_USE_VERTEX) ||
    isEnvTruthy(process.env.CLAUDE_CODE_USE_FOUNDRY) ||
    isTelemetryDisabled()
  )
}

/**
 * Check if the feedback survey should be suppressed.
 *
 * Unlike isAnalyticsDisabled(), this does NOT block on 3P providers
 * (Bedrock/Vertex/Foundry). The survey is a local UI prompt with no
 * transcript data — enterprise customers capture responses via OTEL.
 */
export function isFeedbackSurveyDisabled(): boolean {
  return process.env.NODE_ENV === 'test' || isTelemetryDisabled()
}

```

---


### `src/services/analytics/datadog.ts`

**信息:**
- 行数: 307
- 大小: 9101 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { createHash } from 'crypto'
import memoize from 'lodash-es/memoize.js'
import { getOrCreateUserID } from '../../utils/config.js'
import { logError } from '../../utils/log.js'
import { getCanonicalName } from '../../utils/model/model.js'
import { getAPIProvider } from '../../utils/model/providers.js'
import { MODEL_COSTS } from '../../utils/modelCost.js'
import { isAnalyticsDisabled } from './config.js'
import { getEventMetadata } from './metadata.js'

const DATADOG_LOGS_ENDPOINT =
  'https://http-intake.logs.us5.datadoghq.com/api/v2/logs'
const DATADOG_CLIENT_TOKEN = 'pubbbf48e6d78dae54bceaa4acf463299bf'
const DEFAULT_FLUSH_INTERVAL_MS = 15000
const MAX_BATCH_SIZE = 100
const NETWORK_TIMEOUT_MS = 5000

const DATADOG_ALLOWED_EVENTS = new Set([
  'chrome_bridge_connection_succeeded',
  'chrome_bridge_connection_failed',
  'chrome_bridge_disconnected',
  'chrome_bridge_tool_call_completed',
  'chrome_bridge_tool_call_error',
  'chrome_bridge_tool_call_started',
  'chrome_bridge_tool_call_timeout',
  'tengu_api_error',
  'tengu_api_success',
  'tengu_brief_mode_enabled',
  'tengu_brief_mode_toggled',
  'tengu_brief_send',
  'tengu_cancel',
  'tengu_compact_failed',
  'tengu_exit',
  'tengu_flicker',
  'tengu_init',
  'tengu_model_fallback_triggered',
  'tengu_oauth_error',
  'tengu_oauth_success',
  'tengu_oauth_token_refresh_failure',
  'tengu_oauth_token_refresh_success',
  'tengu_oauth_token_refresh_lock_acquiring',
  'tengu_oauth_token_refresh_lock_acquired',
  'tengu_oauth_token_refresh_starting',
  'tengu_oauth_token_refresh_completed',
  'tengu_oauth_token_refresh_lock_releasing',
  'tengu_oauth_token_refresh_lock_released',
  'tengu_query_error',
  'tengu_session_file_read',
  'tengu_started',

```

---


### `src/services/analytics/firstPartyEventLogger.ts`

**信息:**
- 行数: 449
- 大小: 14590 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { AnyValueMap, Logger, logs } from '@opentelemetry/api-logs'
import { resourceFromAttributes } from '@opentelemetry/resources'
import {
  BatchLogRecordProcessor,
  LoggerProvider,
} from '@opentelemetry/sdk-logs'
import {
  ATTR_SERVICE_NAME,
  ATTR_SERVICE_VERSION,
} from '@opentelemetry/semantic-conventions'
import { randomUUID } from 'crypto'
import { isEqual } from 'lodash-es'
import { getOrCreateUserID } from '../../utils/config.js'
import { logForDebugging } from '../../utils/debug.js'
import { logError } from '../../utils/log.js'
import { getPlatform, getWslVersion } from '../../utils/platform.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { profileCheckpoint } from '../../utils/startupProfiler.js'
import { getCoreUserData } from '../../utils/user.js'
import { isAnalyticsDisabled } from './config.js'
import { FirstPartyEventLoggingExporter } from './firstPartyEventLoggingExporter.js'
import type { GrowthBookUserAttributes } from './growthbook.js'
import { getDynamicConfig_CACHED_MAY_BE_STALE } from './growthbook.js'
import { getEventMetadata } from './metadata.js'
import { isSinkKilled } from './sinkKillswitch.js'

/**
 * Configuration for sampling individual event types.
 * Each event name maps to an object containing sample_rate (0-1).
 * Events not in the config are logged at 100% rate.
 */
export type EventSamplingConfig = {
  [eventName: string]: {
    sample_rate: number
  }
}

const EVENT_SAMPLING_CONFIG_NAME = 'tengu_event_sampling_config'
/**
 * Get the event sampling configuration from GrowthBook.
 * Uses cached value if available, updates cache in background.
 */
export function getEventSamplingConfig(): EventSamplingConfig {
  return getDynamicConfig_CACHED_MAY_BE_STALE<EventSamplingConfig>(
    EVENT_SAMPLING_CONFIG_NAME,
    {},
  )
}

/**

```

---


### `src/services/analytics/firstPartyEventLoggingExporter.ts`

**信息:**
- 行数: 806
- 大小: 26362 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { HrTime } from '@opentelemetry/api'
import { type ExportResult, ExportResultCode } from '@opentelemetry/core'
import type {
  LogRecordExporter,
  ReadableLogRecord,
} from '@opentelemetry/sdk-logs'
import axios from 'axios'
import { randomUUID } from 'crypto'
import { appendFile, mkdir, readdir, unlink, writeFile } from 'fs/promises'
import * as path from 'path'
import type { CoreUserData } from 'src/utils/user.js'
import {
  getIsNonInteractiveSession,
  getSessionId,
} from '../../bootstrap/state.js'
import { ClaudeCodeInternalEvent } from '../../types/generated/events_mono/claude_code/v1/claude_code_internal_event.js'
import { GrowthbookExperimentEvent } from '../../types/generated/events_mono/growthbook/v1/growthbook_experiment_event.js'
import {
  getClaudeAIOAuthTokens,
  hasProfileScope,
  isClaudeAISubscriber,
} from '../../utils/auth.js'
import { checkHasTrustDialogAccepted } from '../../utils/config.js'
import { logForDebugging } from '../../utils/debug.js'
import { getClaudeConfigHomeDir } from '../../utils/envUtils.js'
import { errorMessage, isFsInaccessible, toError } from '../../utils/errors.js'
import { getAuthHeaders } from '../../utils/http.js'
import { readJSONLFile } from '../../utils/json.js'
import { logError } from '../../utils/log.js'
import { sleep } from '../../utils/sleep.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { getClaudeCodeUserAgent } from '../../utils/userAgent.js'
import { isOAuthTokenExpired } from '../oauth/client.js'
import { stripProtoFields } from './index.js'
import { type EventMetadata, to1PEventFormat } from './metadata.js'

// Unique ID for this process run - used to isolate failed event files between runs
const BATCH_UUID = randomUUID()

// File prefix for failed event storage
const FILE_PREFIX = '1p_failed_events.'

// Storage directory for failed events - evaluated at runtime to respect CLAUDE_CONFIG_DIR in tests
function getStorageDir(): string {
  return path.join(getClaudeConfigHomeDir(), 'telemetry')
}

// API envelope - event_data is the JSON output from proto toJSON()
type FirstPartyEventLoggingEvent = {
  event_type: 'ClaudeCodeInternalEvent' | 'GrowthbookExperimentEvent'

```

---


### `src/services/analytics/growthbook.ts`

**信息:**
- 行数: 1155
- 大小: 40526 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { GrowthBook } from '@growthbook/growthbook'
import { isEqual, memoize } from 'lodash-es'
import {
  getIsNonInteractiveSession,
  getSessionTrustAccepted,
} from '../../bootstrap/state.js'
import { getGrowthBookClientKey } from '../../constants/keys.js'
import {
  checkHasTrustDialogAccepted,
  getGlobalConfig,
  saveGlobalConfig,
} from '../../utils/config.js'
import { logForDebugging } from '../../utils/debug.js'
import { toError } from '../../utils/errors.js'
import { getAuthHeaders } from '../../utils/http.js'
import { logError } from '../../utils/log.js'
import { createSignal } from '../../utils/signal.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import {
  type GitHubActionsMetadata,
  getUserForGrowthBook,
} from '../../utils/user.js'
import {
  is1PEventLoggingEnabled,
  logGrowthBookExperimentTo1P,
} from './firstPartyEventLogger.js'

/**
 * User attributes sent to GrowthBook for targeting.
 * Uses UUID suffix (not Uuid) to align with GrowthBook conventions.
 */
export type GrowthBookUserAttributes = {
  id: string
  sessionId: string
  deviceID: string
  platform: 'win32' | 'darwin' | 'linux'
  apiBaseUrlHost?: string
  organizationUUID?: string
  accountUUID?: string
  userType?: string
  subscriptionType?: string
  rateLimitTier?: string
  firstTokenTime?: number
  email?: string
  appVersion?: string
  github?: GitHubActionsMetadata
}

/**
 * Malformed feature response from API that uses "value" instead of "defaultValue".

```

---


### `src/services/analytics/index.ts`

**信息:**
- 行数: 173
- 大小: 5542 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Analytics service - public API for event logging
 *
 * This module serves as the main entry point for analytics events in Claude CLI.
 *
 * DESIGN: This module has NO dependencies to avoid import cycles.
 * Events are queued until attachAnalyticsSink() is called during app initialization.
 * The sink handles routing to Datadog and 1P event logging.
 */

/**
 * Marker type for verifying analytics metadata doesn't contain sensitive data
 *
 * This type forces explicit verification that string values being logged
 * don't contain code snippets, file paths, or other sensitive information.
 *
 * Usage: `myString as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS`
 */
export type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS = never

/**
 * Marker type for values routed to PII-tagged proto columns via `_PROTO_*`
 * payload keys. The destination BQ column has privileged access controls,
 * so unredacted values are acceptable — unlike general-access backends.
 *
 * sink.ts strips `_PROTO_*` keys before Datadog fanout; only the 1P
 * exporter (firstPartyEventLoggingExporter) sees them and hoists them to the
 * top-level proto field. A single stripProtoFields call guards all non-1P
 * sinks — no per-sink filtering to forget.
 *
 * Usage: `rawName as AnalyticsMetadata_I_VERIFIED_THIS_IS_PII_TAGGED`
 */
export type AnalyticsMetadata_I_VERIFIED_THIS_IS_PII_TAGGED = never

/**
 * Strip `_PROTO_*` keys from a payload destined for general-access storage.
 * Used by:
 *   - sink.ts: before Datadog fanout (never sees PII-tagged values)
 *   - firstPartyEventLoggingExporter: defensive strip of additional_metadata
 *     after hoisting known _PROTO_* keys to proto fields — prevents a future
 *     unrecognized _PROTO_foo from silently landing in the BQ JSON blob.
 *
 * Returns the input unchanged (same reference) when no _PROTO_ keys present.
 */
export function stripProtoFields<V>(
  metadata: Record<string, V>,
): Record<string, V> {
  let result: Record<string, V> | undefined
  for (const key in metadata) {
    if (key.startsWith('_PROTO_')) {

```

---


### `src/services/analytics/metadata.ts`

**信息:**
- 行数: 973
- 大小: 32617 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
/**
 * Shared event metadata enrichment for analytics systems
 *
 * This module provides a single source of truth for collecting and formatting
 * event metadata across all analytics systems (Datadog, 1P).
 */

import { extname } from 'path'
import memoize from 'lodash-es/memoize.js'
import { env, getHostPlatformForAnalytics } from '../../utils/env.js'
import { envDynamic } from '../../utils/envDynamic.js'
import { getModelBetas } from '../../utils/betas.js'
import { getMainLoopModel } from '../../utils/model/model.js'
import {
  getSessionId,
  getIsInteractive,
  getKairosActive,
  getClientType,
  getParentSessionId as getParentSessionIdFromState,
} from '../../bootstrap/state.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { isOfficialMcpUrl } from '../mcp/officialRegistry.js'
import { isClaudeAISubscriber, getSubscriptionType } from '../../utils/auth.js'
import { getRepoRemoteHash } from '../../utils/git.js'
import {
  getWslVersion,
  getLinuxDistroInfo,
  detectVcs,
} from '../../utils/platform.js'
import type { CoreUserData } from 'src/utils/user.js'
import { getAgentContext } from '../../utils/agentContext.js'
import type { EnvironmentMetadata } from '../../types/generated/events_mono/claude_code/v1/claude_code_internal_event.js'
import type { PublicApiAuth } from '../../types/generated/events_mono/common/v1/auth.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import {
  getAgentId,
  getParentSessionId as getTeammateParentSessionId,
  getTeamName,
  isTeammate,
} from '../../utils/teammate.js'
import { feature } from 'bun:bundle'

/**
 * Marker type for verifying analytics metadata doesn't contain sensitive data
 *
 * This type forces explicit verification that string values being logged
 * don't contain code snippets, file paths, or other sensitive information.
 *
 * The metadata is expected to be JSON-serializable.

```

---


### `src/services/analytics/sink.ts`

**信息:**
- 行数: 114
- 大小: 3542 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Analytics sink implementation
 *
 * This module contains the actual analytics routing logic and should be
 * initialized during app startup. It routes events to Datadog and 1P event
 * logging.
 *
 * Usage: Call initializeAnalyticsSink() during app startup to attach the sink.
 */

import { trackDatadogEvent } from './datadog.js'
import { logEventTo1P, shouldSampleEvent } from './firstPartyEventLogger.js'
import { checkStatsigFeatureGate_CACHED_MAY_BE_STALE } from './growthbook.js'
import { attachAnalyticsSink, stripProtoFields } from './index.js'
import { isSinkKilled } from './sinkKillswitch.js'

// Local type matching the logEvent metadata signature
type LogEventMetadata = { [key: string]: boolean | number | undefined }

const DATADOG_GATE_NAME = 'tengu_log_datadog_events'

// Module-level gate state - starts undefined, initialized during startup
let isDatadogGateEnabled: boolean | undefined = undefined

/**
 * Check if Datadog tracking is enabled.
 * Falls back to cached value from previous session if not yet initialized.
 */
function shouldTrackDatadog(): boolean {
  if (isSinkKilled('datadog')) {
    return false
  }
  if (isDatadogGateEnabled !== undefined) {
    return isDatadogGateEnabled
  }

  // Fallback to cached value from previous session
  try {
    return checkStatsigFeatureGate_CACHED_MAY_BE_STALE(DATADOG_GATE_NAME)
  } catch {
    return false
  }
}

/**
 * Log an event (synchronous implementation)
 */
function logEventImpl(eventName: string, metadata: LogEventMetadata): void {
  // Check if this event should be sampled
  const sampleResult = shouldSampleEvent(eventName)

```

---


### `src/services/analytics/sinkKillswitch.ts`

**信息:**
- 行数: 25
- 大小: 1063 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getDynamicConfig_CACHED_MAY_BE_STALE } from './growthbook.js'

// Mangled name: per-sink analytics killswitch
const SINK_KILLSWITCH_CONFIG_NAME = 'tengu_frond_boric'

export type SinkName = 'datadog' | 'firstParty'

/**
 * GrowthBook JSON config that disables individual analytics sinks.
 * Shape: { datadog?: boolean, firstParty?: boolean }
 * A value of true for a key stops all dispatch to that sink.
 * Default {} (nothing killed). Fail-open: missing/malformed config = sink stays on.
 *
 * NOTE: Must NOT be called from inside is1PEventLoggingEnabled() -
 * growthbook.ts:isGrowthBookEnabled() calls that, so a lookup here would recurse.
 * Call at per-event dispatch sites instead.
 */
export function isSinkKilled(sink: SinkName): boolean {
  const config = getDynamicConfig_CACHED_MAY_BE_STALE<
    Partial<Record<SinkName, boolean>>
  >(SINK_KILLSWITCH_CONFIG_NAME, {})
  // getFeatureValue_CACHED_MAY_BE_STALE guards on `!== undefined`, so a
  // cached JSON null leaks through instead of falling back to {}.
  return config?.[sink] === true
}

```

---


### `src/services/api/adminRequests.ts`

**信息:**
- 行数: 119
- 大小: 3208 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { getOauthConfig } from '../../constants/oauth.js'
import { getOAuthHeaders, prepareApiRequest } from '../../utils/teleport/api.js'

export type AdminRequestType = 'limit_increase' | 'seat_upgrade'

export type AdminRequestStatus = 'pending' | 'approved' | 'dismissed'

export type AdminRequestSeatUpgradeDetails = {
  message?: string | null
  current_seat_tier?: string | null
}

export type AdminRequestCreateParams =
  | {
      request_type: 'limit_increase'
      details: null
    }
  | {
      request_type: 'seat_upgrade'
      details: AdminRequestSeatUpgradeDetails
    }

export type AdminRequest = {
  uuid: string
  status: AdminRequestStatus
  requester_uuid?: string | null
  created_at: string
} & (
  | {
      request_type: 'limit_increase'
      details: null
    }
  | {
      request_type: 'seat_upgrade'
      details: AdminRequestSeatUpgradeDetails
    }
)

/**
 * Create an admin request (limit increase or seat upgrade).
 *
 * For Team/Enterprise users who don't have billing/admin permissions,
 * this creates a request that their admin can act on.
 *
 * If a pending request of the same type already exists for this user,
 * returns the existing request instead of creating a new one.
 */
export async function createAdminRequest(
  params: AdminRequestCreateParams,

```

---


### `src/services/api/bootstrap.ts`

**信息:**
- 行数: 141
- 大小: 4634 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import isEqual from 'lodash-es/isEqual.js'
import {
  getAnthropicApiKey,
  getClaudeAIOAuthTokens,
  hasProfileScope,
} from 'src/utils/auth.js'
import { z } from 'zod'
import { getOauthConfig, OAUTH_BETA_HEADER } from '../../constants/oauth.js'
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js'
import { logForDebugging } from '../../utils/debug.js'
import { withOAuth401Retry } from '../../utils/http.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { logError } from '../../utils/log.js'
import { getAPIProvider } from '../../utils/model/providers.js'
import { isEssentialTrafficOnly } from '../../utils/privacyLevel.js'
import { getClaudeCodeUserAgent } from '../../utils/userAgent.js'

const bootstrapResponseSchema = lazySchema(() =>
  z.object({
    client_data: z.record(z.unknown()).nullish(),
    additional_model_options: z
      .array(
        z
          .object({
            model: z.string(),
            name: z.string(),
            description: z.string(),
          })
          .transform(({ model, name, description }) => ({
            value: model,
            label: name,
            description,
          })),
      )
      .nullish(),
  }),
)

type BootstrapResponse = z.infer<ReturnType<typeof bootstrapResponseSchema>>

async function fetchBootstrapAPI(): Promise<BootstrapResponse | null> {
  if (isEssentialTrafficOnly()) {
    logForDebugging('[Bootstrap] Skipped: Nonessential traffic disabled')
    return null
  }

  if (getAPIProvider() !== 'firstParty') {
    logForDebugging('[Bootstrap] Skipped: 3P provider')
    return null

```

---


### `src/services/api/claude.ts`

**信息:**
- 行数: 3419
- 大小: 125779 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type {
  BetaContentBlock,
  BetaContentBlockParam,
  BetaImageBlockParam,
  BetaJSONOutputFormat,
  BetaMessage,
  BetaMessageDeltaUsage,
  BetaMessageStreamParams,
  BetaOutputConfig,
  BetaRawMessageStreamEvent,
  BetaRequestDocumentBlock,
  BetaStopReason,
  BetaToolChoiceAuto,
  BetaToolChoiceTool,
  BetaToolResultBlockParam,
  BetaToolUnion,
  BetaUsage,
  BetaMessageParam as MessageParam,
} from '@anthropic-ai/sdk/resources/beta/messages/messages.mjs'
import type { TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs'
import type { Stream } from '@anthropic-ai/sdk/streaming.mjs'
import { randomUUID } from 'crypto'
import {
  getAPIProvider,
  isFirstPartyAnthropicBaseUrl,
} from 'src/utils/model/providers.js'
import {
  getAttributionHeader,
  getCLISyspromptPrefix,
} from '../../constants/system.js'
import {
  getEmptyToolPermissionContext,
  type QueryChainTracking,
  type Tool,
  type ToolPermissionContext,
  type Tools,
  toolMatchesName,
} from '../../Tool.js'
import type { AgentDefinition } from '../../tools/AgentTool/loadAgentsDir.js'
import {
  type ConnectorTextBlock,
  type ConnectorTextDelta,
  isConnectorTextBlock,
} from '../../types/connectorText.js'
import type {
  AssistantMessage,
  Message,
  StreamEvent,
  SystemAPIErrorMessage,
  UserMessage,

```

---


### `src/services/api/client.ts`

**信息:**
- 行数: 197
- 大小: 6845 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import Anthropic, { type ClientOptions } from '@anthropic-ai/sdk'
import { randomUUID } from 'crypto'
// RESTORED WORKSPACE: Google auth library import removed for compilation
// import type { GoogleAuth } from 'google-auth-library'
import {
  checkAndRefreshOAuthTokenIfNeeded,
  getAnthropicApiKey,
  getApiKeyFromApiKeyHelper,
  getClaudeAIOAuthTokens,
  isClaudeAISubscriber,
  refreshAndGetAwsCredentials,
  refreshGcpCredentialsIfNeeded,
} from 'src/utils/auth.js'
import { getUserAgent } from 'src/utils/http.js'
import { getSmallFastModel } from 'src/utils/model/model.js'
import {
  getAPIProvider,
  isFirstPartyAnthropicBaseUrl,
} from 'src/utils/model/providers.js'
import { getProxyFetchOptions } from 'src/utils/proxy.js'
import {
  getIsNonInteractiveSession,
  getSessionId,
} from '../../bootstrap/state.js'
import { getOauthConfig } from '../../constants/oauth.js'
import { isDebugToStdErr, logForDebugging } from '../../utils/debug.js'
import {
  getAWSRegion,
  getVertexRegionForModel,
  isEnvTruthy,
} from '../../utils/envUtils.js'

function createStderrLogger(): ClientOptions['logger'] {
  return {
    error: (msg, ...args) =>
      // biome-ignore lint/suspicious/noConsole:: intentional console output -- SDK logger must use console
      console.error('[Anthropic SDK ERROR]', msg, ...args),
    // biome-ignore lint/suspicious/noConsole:: intentional console output -- SDK logger must use console
    warn: (msg, ...args) => console.error('[Anthropic SDK WARN]', msg, ...args),
    // biome-ignore lint/suspicious/noConsole:: intentional console output -- SDK logger must use console
    info: (msg, ...args) => console.error('[Anthropic SDK INFO]', msg, ...args),
    debug: (msg, ...args) =>
      // biome-ignore lint/suspicious/noConsole:: intentional console output -- SDK logger must use console
      console.error('[Anthropic SDK DEBUG]', msg, ...args),
  }
}

export async function getAnthropicClient({
  apiKey,
  maxRetries,

```

---


### `src/services/api/dumpPrompts.ts`

**信息:**
- 行数: 226
- 大小: 7332 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ClientOptions } from '@anthropic-ai/sdk'
import { createHash } from 'crypto'
import { promises as fs } from 'fs'
import { dirname, join } from 'path'
import { getSessionId } from 'src/bootstrap/state.js'
import { getClaudeConfigHomeDir } from '../../utils/envUtils.js'
import { jsonParse, jsonStringify } from '../../utils/slowOperations.js'

function hashString(str: string): string {
  return createHash('sha256').update(str).digest('hex')
}

// Cache last few API requests for ant users (e.g., for /issue command)
const MAX_CACHED_REQUESTS = 5
const cachedApiRequests: Array<{ timestamp: string; request: unknown }> = []

type DumpState = {
  initialized: boolean
  messageCountSeen: number
  lastInitDataHash: string
  // Cheap proxy for change detection — skips the expensive stringify+hash
  // when model/tools/system are structurally identical to the last call.
  lastInitFingerprint: string
}

// Track state per session to avoid duplicating data
const dumpState = new Map<string, DumpState>()

export function getLastApiRequests(): Array<{
  timestamp: string
  request: unknown
}> {
  return [...cachedApiRequests]
}

export function clearApiRequestCache(): void {
  cachedApiRequests.length = 0
}

export function clearDumpState(agentIdOrSessionId: string): void {
  dumpState.delete(agentIdOrSessionId)
}

export function clearAllDumpState(): void {
  dumpState.clear()
}

export function addApiRequestToCache(requestData: unknown): void {
  if (process.env.USER_TYPE !== 'ant') return
  cachedApiRequests.push({

```

---


### `src/services/api/emptyUsage.ts`

**信息:**
- 行数: 22
- 大小: 712 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { NonNullableUsage } from '../../entrypoints/sdk/sdkUtilityTypes.js'

/**
 * Zero-initialized usage object. Extracted from logging.ts so that
 * bridge/replBridge.ts can import it without transitively pulling in
 * api/errors.ts → utils/messages.ts → BashTool.tsx → the world.
 */
export const EMPTY_USAGE: Readonly<NonNullableUsage> = {
  input_tokens: 0,
  cache_creation_input_tokens: 0,
  cache_read_input_tokens: 0,
  output_tokens: 0,
  server_tool_use: { web_search_requests: 0, web_fetch_requests: 0 },
  service_tier: 'standard',
  cache_creation: {
    ephemeral_1h_input_tokens: 0,
    ephemeral_5m_input_tokens: 0,
  },
  inference_geo: '',
  iterations: [],
  speed: 'standard',
}

```

---


### `src/services/api/errorUtils.ts`

**信息:**
- 行数: 260
- 大小: 8405 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { APIError } from '@anthropic-ai/sdk'

// SSL/TLS error codes from OpenSSL (used by both Node.js and Bun)
// See: https://www.openssl.org/docs/man3.1/man3/X509_STORE_CTX_get_error.html
const SSL_ERROR_CODES = new Set([
  // Certificate verification errors
  'UNABLE_TO_VERIFY_LEAF_SIGNATURE',
  'UNABLE_TO_GET_ISSUER_CERT',
  'UNABLE_TO_GET_ISSUER_CERT_LOCALLY',
  'CERT_SIGNATURE_FAILURE',
  'CERT_NOT_YET_VALID',
  'CERT_HAS_EXPIRED',
  'CERT_REVOKED',
  'CERT_REJECTED',
  'CERT_UNTRUSTED',
  // Self-signed certificate errors
  'DEPTH_ZERO_SELF_SIGNED_CERT',
  'SELF_SIGNED_CERT_IN_CHAIN',
  // Chain errors
  'CERT_CHAIN_TOO_LONG',
  'PATH_LENGTH_EXCEEDED',
  // Hostname/altname errors
  'ERR_TLS_CERT_ALTNAME_INVALID',
  'HOSTNAME_MISMATCH',
  // TLS handshake errors
  'ERR_TLS_HANDSHAKE_TIMEOUT',
  'ERR_SSL_WRONG_VERSION_NUMBER',
  'ERR_SSL_DECRYPTION_FAILED_OR_BAD_RECORD_MAC',
])

export type ConnectionErrorDetails = {
  code: string
  message: string
  isSSLError: boolean
}

/**
 * Extracts connection error details from the error cause chain.
 * The Anthropic SDK wraps underlying errors in the `cause` property.
 * This function walks the cause chain to find the root error code/message.
 */
export function extractConnectionErrorDetails(
  error: unknown,
): ConnectionErrorDetails | null {
  if (!error || typeof error !== 'object') {
    return null
  }

  // Walk the cause chain to find the root error with a code
  let current: unknown = error

```

---


### `src/services/api/errors.ts`

**信息:**
- 行数: 1207
- 大小: 41735 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  APIConnectionError,
  APIConnectionTimeoutError,
  APIError,
} from '@anthropic-ai/sdk'
import type {
  BetaMessage,
  BetaStopReason,
} from '@anthropic-ai/sdk/resources/beta/messages/messages.mjs'
import { AFK_MODE_BETA_HEADER } from 'src/constants/betas.js'
import type { SDKAssistantMessageError } from 'src/entrypoints/agentSdkTypes.js'
import type {
  AssistantMessage,
  Message,
  UserMessage,
} from 'src/types/message.js'
import {
  getAnthropicApiKeyWithSource,
  getClaudeAIOAuthTokens,
  getOauthAccountInfo,
  isClaudeAISubscriber,
} from 'src/utils/auth.js'
import {
  createAssistantAPIErrorMessage,
  NO_RESPONSE_REQUESTED,
} from 'src/utils/messages.js'
import {
  getDefaultMainLoopModelSetting,
  isNonCustomOpusModel,
} from 'src/utils/model/model.js'
import { getModelStrings } from 'src/utils/model/modelStrings.js'
import { getAPIProvider } from 'src/utils/model/providers.js'
import { getIsNonInteractiveSession } from '../../bootstrap/state.js'
import {
  API_PDF_MAX_PAGES,
  PDF_TARGET_RAW_SIZE,
} from '../../constants/apiLimits.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { formatFileSize } from '../../utils/format.js'
import { ImageResizeError } from '../../utils/imageResizer.js'
import { ImageSizeError } from '../../utils/imageValidation.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'
import {
  type ClaudeAILimits,
  getRateLimitErrorMessage,
  type OverageDisabledReason,
} from '../claudeAiLimits.js'

```

---


### `src/services/api/filesApi.ts`

**信息:**
- 行数: 748
- 大小: 21494 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Files API client for managing files
 *
 * This module provides functionality to download and upload files to Anthropic Public Files API.
 * Used by the Claude Code agent to download file attachments at session startup.
 *
 * API Reference: https://docs.anthropic.com/en/api/files-content
 */

import axios from 'axios'
import { randomUUID } from 'crypto'
import * as fs from 'fs/promises'
import * as path from 'path'
import { count } from '../../utils/array.js'
import { getCwd } from '../../utils/cwd.js'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'
import { sleep } from '../../utils/sleep.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'

// Files API is currently in beta. oauth-2025-04-20 enables Bearer OAuth
// on public-api routes (auth.py: "oauth_auth" not in beta_versions → 404).
const FILES_API_BETA_HEADER = 'files-api-2025-04-14,oauth-2025-04-20'
const ANTHROPIC_VERSION = '2023-06-01'

// API base URL - uses ANTHROPIC_BASE_URL set by env-manager for the appropriate environment
// Falls back to public API for standalone usage
function getDefaultApiBaseUrl(): string {
  return (
    process.env.ANTHROPIC_BASE_URL ||
    process.env.CLAUDE_CODE_API_BASE_URL ||
    'https://api.anthropic.com'
  )
}

function logDebugError(message: string): void {
  logForDebugging(`[files-api] ${message}`, { level: 'error' })
}

function logDebug(message: string): void {
  logForDebugging(`[files-api] ${message}`)
}

/**
 * File specification parsed from CLI args
 * Format: --file=<file_id>:<relative_path>

```

---


### `src/services/api/firstTokenDate.ts`

**信息:**
- 行数: 60
- 大小: 1765 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { getOauthConfig } from '../../constants/oauth.js'
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js'
import { getAuthHeaders } from '../../utils/http.js'
import { logError } from '../../utils/log.js'
import { getClaudeCodeUserAgent } from '../../utils/userAgent.js'

/**
 * Fetch the user's first Claude Code token date and store in config.
 * This is called after successful login to cache when they started using Claude Code.
 */
export async function fetchAndStoreClaudeCodeFirstTokenDate(): Promise<void> {
  try {
    const config = getGlobalConfig()

    if (config.claudeCodeFirstTokenDate !== undefined) {
      return
    }

    const authHeaders = getAuthHeaders()
    if (authHeaders.error) {
      logError(new Error(`Failed to get auth headers: ${authHeaders.error}`))
      return
    }

    const oauthConfig = getOauthConfig()
    const url = `${oauthConfig.BASE_API_URL}/api/organization/claude_code_first_token_date`

    const response = await axios.get(url, {
      headers: {
        ...authHeaders.headers,
        'User-Agent': getClaudeCodeUserAgent(),
      },
      timeout: 10000,
    })

    const firstTokenDate = response.data?.first_token_date ?? null

    // Validate the date if it's not null
    if (firstTokenDate !== null) {
      const dateTime = new Date(firstTokenDate).getTime()
      if (isNaN(dateTime)) {
        logError(
          new Error(
            `Received invalid first_token_date from API: ${firstTokenDate}`,
          ),
        )
        // Don't save invalid dates
        return
      }

```

---


### `src/services/api/grove.ts`

**信息:**
- 行数: 357
- 大小: 11543 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import memoize from 'lodash-es/memoize.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from 'src/services/analytics/index.js'
import { getOauthAccountInfo, isConsumerSubscriber } from 'src/utils/auth.js'
import { logForDebugging } from 'src/utils/debug.js'
import { gracefulShutdown } from 'src/utils/gracefulShutdown.js'
import { isEssentialTrafficOnly } from 'src/utils/privacyLevel.js'
import { writeToStderr } from 'src/utils/process.js'
import { getOauthConfig } from '../../constants/oauth.js'
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js'
import {
  getAuthHeaders,
  getUserAgent,
  withOAuth401Retry,
} from '../../utils/http.js'
import { logError } from '../../utils/log.js'
import { getClaudeCodeUserAgent } from '../../utils/userAgent.js'

// Cache expiration: 24 hours
const GROVE_CACHE_EXPIRATION_MS = 24 * 60 * 60 * 1000

export type AccountSettings = {
  grove_enabled: boolean | null
  grove_notice_viewed_at: string | null
}

export type GroveConfig = {
  grove_enabled: boolean
  domain_excluded: boolean
  notice_is_grace_period: boolean
  notice_reminder_frequency: number | null
}

/**
 * Result type that distinguishes between API failure and success.
 * - success: true means API call succeeded (data may still contain null fields)
 * - success: false means API call failed after retry
 */
export type ApiResult<T> = { success: true; data: T } | { success: false }

/**
 * Get the current Grove settings for the user account.
 * Returns ApiResult to distinguish between API failure and success.
 * Uses existing OAuth 401 retry, then returns failure if that doesn't help.
 *
 * Memoized for the session to avoid redundant per-render requests.
 * Cache is invalidated in updateGroveSettings() so post-toggle reads are fresh.

```

---


### `src/services/api/logging.ts`

**信息:**
- 行数: 788
- 大小: 24191 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { APIError } from '@anthropic-ai/sdk'
import type {
  BetaStopReason,
  BetaUsage as Usage,
} from '@anthropic-ai/sdk/resources/beta/messages/messages.mjs'
import {
  addToTotalDurationState,
  consumePostCompaction,
  getIsNonInteractiveSession,
  getLastApiCompletionTimestamp,
  getTeleportedSessionInfo,
  markFirstTeleportMessageLogged,
  setLastApiCompletionTimestamp,
} from 'src/bootstrap/state.js'
import type { QueryChainTracking } from 'src/Tool.js'
import { isConnectorTextBlock } from 'src/types/connectorText.js'
import type { AssistantMessage } from 'src/types/message.js'
import { logForDebugging } from 'src/utils/debug.js'
import type { EffortLevel } from 'src/utils/effort.js'
import { logError } from 'src/utils/log.js'
import { getAPIProviderForStatsig } from 'src/utils/model/providers.js'
import type { PermissionMode } from 'src/utils/permissions/PermissionMode.js'
import { jsonStringify } from 'src/utils/slowOperations.js'
import { logOTelEvent } from 'src/utils/telemetry/events.js'
import {
  endLLMRequestSpan,
  isBetaTracingEnabled,
  type Span,
} from 'src/utils/telemetry/sessionTracing.js'
import type { NonNullableUsage } from '../../entrypoints/sdk/sdkUtilityTypes.js'
import { consumeInvokingRequestId } from '../../utils/agentContext.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'
import { sanitizeToolNameForAnalytics } from '../analytics/metadata.js'
import { EMPTY_USAGE } from './emptyUsage.js'
import { classifyAPIError } from './errors.js'
import { extractConnectionErrorDetails } from './errorUtils.js'

export type { NonNullableUsage }
export { EMPTY_USAGE }

// Strategy used for global prompt caching
export type GlobalCacheStrategy = 'tool_based' | 'system_prompt' | 'none'

function getErrorMessage(error: unknown): string {
  if (error instanceof APIError) {
    const body = error.error as { error?: { message?: string } } | undefined

```

---


### `src/services/api/metricsOptOut.ts`

**信息:**
- 行数: 159
- 大小: 5355 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { hasProfileScope, isClaudeAISubscriber } from '../../utils/auth.js'
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { getAuthHeaders, withOAuth401Retry } from '../../utils/http.js'
import { logError } from '../../utils/log.js'
import { memoizeWithTTLAsync } from '../../utils/memoize.js'
import { isEssentialTrafficOnly } from '../../utils/privacyLevel.js'
import { getClaudeCodeUserAgent } from '../../utils/userAgent.js'

type MetricsEnabledResponse = {
  metrics_logging_enabled: boolean
}

type MetricsStatus = {
  enabled: boolean
  hasError: boolean
}

// In-memory TTL — dedupes calls within a single process
const CACHE_TTL_MS = 60 * 60 * 1000

// Disk TTL — org settings rarely change. When disk cache is fresher than this,
// we skip the network entirely (no background refresh). This is what collapses
// N `claude -p` invocations into ~1 API call/day.
const DISK_CACHE_TTL_MS = 24 * 60 * 60 * 1000

/**
 * Internal function to call the API and check if metrics are enabled
 * This is wrapped by memoizeWithTTLAsync to add caching behavior
 */
async function _fetchMetricsEnabled(): Promise<MetricsEnabledResponse> {
  const authResult = getAuthHeaders()
  if (authResult.error) {
    throw new Error(`Auth error: ${authResult.error}`)
  }

  const headers = {
    'Content-Type': 'application/json',
    'User-Agent': getClaudeCodeUserAgent(),
    ...authResult.headers,
  }

  const endpoint = `https://api.anthropic.com/api/claude_code/organizations/metrics_enabled`
  const response = await axios.get<MetricsEnabledResponse>(endpoint, {
    headers,
    timeout: 5000,
  })
  return response.data

```

---


### `src/services/api/overageCreditGrant.ts`

**信息:**
- 行数: 137
- 大小: 4913 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { getOauthConfig } from '../../constants/oauth.js'
import { getOauthAccountInfo } from '../../utils/auth.js'
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js'
import { logError } from '../../utils/log.js'
import { isEssentialTrafficOnly } from '../../utils/privacyLevel.js'
import { getOAuthHeaders, prepareApiRequest } from '../../utils/teleport/api.js'

export type OverageCreditGrantInfo = {
  available: boolean
  eligible: boolean
  granted: boolean
  amount_minor_units: number | null
  currency: string | null
}

type CachedGrantEntry = {
  info: OverageCreditGrantInfo
  timestamp: number
}

const CACHE_TTL_MS = 60 * 60 * 1000 // 1 hour

/**
 * Fetch the current user's overage credit grant eligibility from the backend.
 * The backend resolves tier-specific amounts and role-based claim permission,
 * so the CLI just reads the response without replicating that logic.
 */
async function fetchOverageCreditGrant(): Promise<OverageCreditGrantInfo | null> {
  try {
    const { accessToken, orgUUID } = await prepareApiRequest()
    const url = `${getOauthConfig().BASE_API_URL}/api/oauth/organizations/${orgUUID}/overage_credit_grant`
    const response = await axios.get<OverageCreditGrantInfo>(url, {
      headers: getOAuthHeaders(accessToken),
    })
    return response.data
  } catch (err) {
    logError(err)
    return null
  }
}

/**
 * Get cached grant info. Returns null if no cache or cache is stale.
 * Callers should render nothing (not block) when this returns null —
 * refreshOverageCreditGrantCache fires lazily to populate it.
 */
export function getCachedOverageCreditGrant(): OverageCreditGrantInfo | null {
  const orgId = getOauthAccountInfo()?.organizationUuid
  if (!orgId) return null

```

---


### `src/services/api/promptCacheBreakDetection.ts`

**信息:**
- 行数: 727
- 大小: 26288 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { BetaToolUnion } from '@anthropic-ai/sdk/resources/beta/messages/messages.mjs'
import type { TextBlockParam } from '@anthropic-ai/sdk/resources/index.mjs'
import { createPatch } from 'diff'
import { mkdir, writeFile } from 'fs/promises'
import { join } from 'path'
import type { AgentId } from 'src/types/ids.js'
import type { Message } from 'src/types/message.js'
import { logForDebugging } from 'src/utils/debug.js'
import { djb2Hash } from 'src/utils/hash.js'
import { logError } from 'src/utils/log.js'
import { getClaudeTempDir } from 'src/utils/permissions/filesystem.js'
import { jsonStringify } from 'src/utils/slowOperations.js'
import type { QuerySource } from '../../constants/querySource.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'

function getCacheBreakDiffPath(): string {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
  let suffix = ''
  for (let i = 0; i < 4; i++) {
    suffix += chars[Math.floor(Math.random() * chars.length)]
  }
  return join(getClaudeTempDir(), `cache-break-${suffix}.diff`)
}

type PreviousState = {
  systemHash: number
  toolsHash: number
  /** Hash of system blocks WITH cache_control intact. Catches scope/TTL flips
   *  (global↔org, 1h↔5m) that stripCacheControl erases from systemHash. */
  cacheControlHash: number
  toolNames: string[]
  /** Per-tool schema hash. Diffed to name which tool's description changed
   *  when toolSchemasChanged but added=removed=0 (77% of tool breaks per
   *  BQ 2026-03-22). AgentTool/SkillTool embed dynamic agent/command lists. */
  perToolHashes: Record<string, number>
  systemCharCount: number
  model: string
  fastMode: boolean
  /** 'tool_based' | 'system_prompt' | 'none' — flips when MCP tools are
   *  discovered/removed. */
  globalCacheStrategy: string
  /** Sorted beta header list. Diffed to show which headers were added/removed. */
  betas: string[]
  /** AFK_MODE_BETA_HEADER presence — should NOT break cache anymore
   *  (sticky-on latched in claude.ts). Tracked to verify the fix. */
  autoModeActive: boolean
  /** Overage state flip — should NOT break cache anymore (eligibility is

```

---


### `src/services/api/referral.ts`

**信息:**
- 行数: 281
- 大小: 7985 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { getOauthConfig } from '../../constants/oauth.js'
import {
  getOauthAccountInfo,
  getSubscriptionType,
  isClaudeAISubscriber,
} from '../../utils/auth.js'
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js'
import { logForDebugging } from '../../utils/debug.js'
import { logError } from '../../utils/log.js'
import { isEssentialTrafficOnly } from '../../utils/privacyLevel.js'
import { getOAuthHeaders, prepareApiRequest } from '../../utils/teleport/api.js'
import type {
  ReferralCampaign,
  ReferralEligibilityResponse,
  ReferralRedemptionsResponse,
  ReferrerRewardInfo,
} from '../oauth/types.js'

// Cache expiration time: 24 hours (eligibility changes only on subscription/experiment changes)
const CACHE_EXPIRATION_MS = 24 * 60 * 60 * 1000

// Track in-flight fetch to prevent duplicate API calls
let fetchInProgress: Promise<ReferralEligibilityResponse | null> | null = null

export async function fetchReferralEligibility(
  campaign: ReferralCampaign = 'claude_code_guest_pass',
): Promise<ReferralEligibilityResponse> {
  const { accessToken, orgUUID } = await prepareApiRequest()

  const headers = {
    ...getOAuthHeaders(accessToken),
    'x-organization-uuid': orgUUID,
  }

  const url = `${getOauthConfig().BASE_API_URL}/api/oauth/organizations/${orgUUID}/referral/eligibility`

  const response = await axios.get(url, {
    headers,
    params: { campaign },
    timeout: 5000, // 5 second timeout for background fetch
  })

  return response.data
}

export async function fetchReferralRedemptions(
  campaign: string = 'claude_code_guest_pass',
): Promise<ReferralRedemptionsResponse> {
  const { accessToken, orgUUID } = await prepareApiRequest()

```

---


### `src/services/api/sessionIngress.ts`

**信息:**
- 行数: 514
- 大小: 17055 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios, { type AxiosError } from 'axios'
import type { UUID } from 'crypto'
import { getOauthConfig } from '../../constants/oauth.js'
import type { Entry, TranscriptMessage } from '../../types/logs.js'
import { logForDebugging } from '../../utils/debug.js'
import { logForDiagnosticsNoPII } from '../../utils/diagLogs.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { logError } from '../../utils/log.js'
import { sequential } from '../../utils/sequential.js'
import { getSessionIngressAuthToken } from '../../utils/sessionIngressAuth.js'
import { sleep } from '../../utils/sleep.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { getOAuthHeaders } from '../../utils/teleport/api.js'

interface SessionIngressError {
  error?: {
    message?: string
    type?: string
  }
}

// Module-level state
const lastUuidMap: Map<string, UUID> = new Map()

const MAX_RETRIES = 10
const BASE_DELAY_MS = 500

// Per-session sequential wrappers to prevent concurrent log writes
const sequentialAppendBySession: Map<
  string,
  (
    entry: TranscriptMessage,
    url: string,
    headers: Record<string, string>,
  ) => Promise<boolean>
> = new Map()

/**
 * Gets or creates a sequential wrapper for a session
 * This ensures that log appends for a session are processed one at a time
 */
function getOrCreateSequentialAppend(sessionId: string) {
  let sequentialAppend = sequentialAppendBySession.get(sessionId)
  if (!sequentialAppend) {
    sequentialAppend = sequential(
      async (
        entry: TranscriptMessage,
        url: string,
        headers: Record<string, string>,
      ) => await appendSessionLogImpl(sessionId, entry, url, headers),

```

---


### `src/services/api/ultrareviewQuota.ts`

**信息:**
- 行数: 38
- 大小: 1219 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { getOauthConfig } from '../../constants/oauth.js'
import { isClaudeAISubscriber } from '../../utils/auth.js'
import { logForDebugging } from '../../utils/debug.js'
import { getOAuthHeaders, prepareApiRequest } from '../../utils/teleport/api.js'

export type UltrareviewQuotaResponse = {
  reviews_used: number
  reviews_limit: number
  reviews_remaining: number
  is_overage: boolean
}

/**
 * Peek the ultrareview quota for display and nudge decisions. Consume
 * happens server-side at session creation. Null when not a subscriber or
 * the endpoint errors.
 */
export async function fetchUltrareviewQuota(): Promise<UltrareviewQuotaResponse | null> {
  if (!isClaudeAISubscriber()) return null
  try {
    const { accessToken, orgUUID } = await prepareApiRequest()
    const response = await axios.get<UltrareviewQuotaResponse>(
      `${getOauthConfig().BASE_API_URL}/v1/ultrareview/quota`,
      {
        headers: {
          ...getOAuthHeaders(accessToken),
          'x-organization-uuid': orgUUID,
        },
        timeout: 5000,
      },
    )
    return response.data
  } catch (error) {
    logForDebugging(`fetchUltrareviewQuota failed: ${error}`)
    return null
  }
}

```

---


### `src/services/api/usage.ts`

**信息:**
- 行数: 63
- 大小: 1685 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { getOauthConfig } from '../../constants/oauth.js'
import {
  getClaudeAIOAuthTokens,
  hasProfileScope,
  isClaudeAISubscriber,
} from '../../utils/auth.js'
import { getAuthHeaders } from '../../utils/http.js'
import { getClaudeCodeUserAgent } from '../../utils/userAgent.js'
import { isOAuthTokenExpired } from '../oauth/client.js'

export type RateLimit = {
  utilization: number | null // a percentage from 0 to 100
  resets_at: string | null // ISO 8601 timestamp
}

export type ExtraUsage = {
  is_enabled: boolean
  monthly_limit: number | null
  used_credits: number | null
  utilization: number | null
}

export type Utilization = {
  five_hour?: RateLimit | null
  seven_day?: RateLimit | null
  seven_day_oauth_apps?: RateLimit | null
  seven_day_opus?: RateLimit | null
  seven_day_sonnet?: RateLimit | null
  extra_usage?: ExtraUsage | null
}

export async function fetchUtilization(): Promise<Utilization | null> {
  if (!isClaudeAISubscriber() || !hasProfileScope()) {
    return {}
  }

  // Skip API call if OAuth token is expired to avoid 401 errors
  const tokens = getClaudeAIOAuthTokens()
  if (tokens && isOAuthTokenExpired(tokens.expiresAt)) {
    return null
  }

  const authResult = getAuthHeaders()
  if (authResult.error) {
    throw new Error(`Auth error: ${authResult.error}`)
  }

  const headers = {
    'Content-Type': 'application/json',

```

---


### `src/services/api/withRetry.ts`

**信息:**
- 行数: 822
- 大小: 28238 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type Anthropic from '@anthropic-ai/sdk'
import {
  APIConnectionError,
  APIError,
  APIUserAbortError,
} from '@anthropic-ai/sdk'
import type { QuerySource } from 'src/constants/querySource.js'
import type { SystemAPIErrorMessage } from 'src/types/message.js'
import { isAwsCredentialsProviderError } from 'src/utils/aws.js'
import { logForDebugging } from 'src/utils/debug.js'
import { logError } from 'src/utils/log.js'
import { createSystemAPIErrorMessage } from 'src/utils/messages.js'
import { getAPIProviderForStatsig } from 'src/utils/model/providers.js'
import {
  clearApiKeyHelperCache,
  clearAwsCredentialsCache,
  clearGcpCredentialsCache,
  getClaudeAIOAuthTokens,
  handleOAuth401Error,
  isClaudeAISubscriber,
  isEnterpriseSubscriber,
} from '../../utils/auth.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { errorMessage } from '../../utils/errors.js'
import {
  type CooldownReason,
  handleFastModeOverageRejection,
  handleFastModeRejectedByAPI,
  isFastModeCooldown,
  isFastModeEnabled,
  triggerFastModeCooldown,
} from '../../utils/fastMode.js'
import { isNonCustomOpusModel } from '../../utils/model/model.js'
import { disableKeepAlive } from '../../utils/proxy.js'
import { sleep } from '../../utils/sleep.js'
import type { ThinkingConfig } from '../../utils/thinking.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../analytics/growthbook.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'
import {
  checkMockRateLimitError,
  isMockRateLimitError,
} from '../rateLimitMocking.js'
import { REPEATED_529_ERROR_MESSAGE } from './errors.js'
import { extractConnectionErrorDetails } from './errorUtils.js'

const abortError = () => new APIUserAbortError()

```

---


### `src/services/autoDream/autoDream.ts`

**信息:**
- 行数: 324
- 大小: 11259 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// biome-ignore-all assist/source/organizeImports: ANT-ONLY import markers must not be reordered
// Background memory consolidation. Fires the /dream prompt as a forked
// subagent when time-gate passes AND enough sessions have accumulated.
//
// Gate order (cheapest first):
//   1. Time: hours since lastConsolidatedAt >= minHours (one stat)
//   2. Sessions: transcript count with mtime > lastConsolidatedAt >= minSessions
//   3. Lock: no other process mid-consolidation
//
// State is closure-scoped inside initAutoDream() rather than module-level
// (tests call initAutoDream() in beforeEach for a fresh closure).

import type { REPLHookContext } from '../../utils/hooks/postSamplingHooks.js'
import {
  createCacheSafeParams,
  runForkedAgent,
} from '../../utils/forkedAgent.js'
import {
  createUserMessage,
  createMemorySavedMessage,
} from '../../utils/messages.js'
import type { Message } from '../../types/message.js'
import { logForDebugging } from '../../utils/debug.js'
import type { ToolUseContext } from '../../Tool.js'
import { logEvent } from '../analytics/index.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../analytics/growthbook.js'
import { isAutoMemoryEnabled, getAutoMemPath } from '../../memdir/paths.js'
import { isAutoDreamEnabled } from './config.js'
import { getProjectDir } from '../../utils/sessionStorage.js'
import {
  getOriginalCwd,
  getKairosActive,
  getIsRemoteMode,
  getSessionId,
} from '../../bootstrap/state.js'
import { createAutoMemCanUseTool } from '../extractMemories/extractMemories.js'
import { buildConsolidationPrompt } from './consolidationPrompt.js'
import {
  readLastConsolidatedAt,
  listSessionsTouchedSince,
  tryAcquireConsolidationLock,
  rollbackConsolidationLock,
} from './consolidationLock.js'
import {
  registerDreamTask,
  addDreamTurn,
  completeDreamTask,
  failDreamTask,
  isDreamTask,
} from '../../tasks/DreamTask/DreamTask.js'

```

---


### `src/services/autoDream/config.ts`

**信息:**
- 行数: 21
- 大小: 892 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Leaf config module — intentionally minimal imports so UI components
// can read the auto-dream enabled state without dragging in the forked
// agent / task registry / message builder chain that autoDream.ts pulls in.

import { getInitialSettings } from '../../utils/settings/settings.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../analytics/growthbook.js'

/**
 * Whether background memory consolidation should run. User setting
 * (autoDreamEnabled in settings.json) overrides the GrowthBook default
 * when explicitly set; otherwise falls through to tengu_onyx_plover.
 */
export function isAutoDreamEnabled(): boolean {
  const setting = getInitialSettings().autoDreamEnabled
  if (setting !== undefined) return setting
  const gb = getFeatureValue_CACHED_MAY_BE_STALE<{ enabled?: unknown } | null>(
    'tengu_onyx_plover',
    null,
  )
  return gb?.enabled === true
}

```

---


### `src/services/autoDream/consolidationLock.ts`

**信息:**
- 行数: 140
- 大小: 4548 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Lock file whose mtime IS lastConsolidatedAt. Body is the holder's PID.
//
// Lives inside the memory dir (getAutoMemPath) so it keys on git-root
// like memory does, and so it's writable even when the memory path comes
// from an env/settings override whose parent may not be.

import { mkdir, readFile, stat, unlink, utimes, writeFile } from 'fs/promises'
import { join } from 'path'
import { getOriginalCwd } from '../../bootstrap/state.js'
import { getAutoMemPath } from '../../memdir/paths.js'
import { logForDebugging } from '../../utils/debug.js'
import { isProcessRunning } from '../../utils/genericProcessUtils.js'
import { listCandidates } from '../../utils/listSessionsImpl.js'
import { getProjectDir } from '../../utils/sessionStorage.js'

const LOCK_FILE = '.consolidate-lock'

// Stale past this even if the PID is live (PID reuse guard).
const HOLDER_STALE_MS = 60 * 60 * 1000

function lockPath(): string {
  return join(getAutoMemPath(), LOCK_FILE)
}

/**
 * mtime of the lock file = lastConsolidatedAt. 0 if absent.
 * Per-turn cost: one stat.
 */
export async function readLastConsolidatedAt(): Promise<number> {
  try {
    const s = await stat(lockPath())
    return s.mtimeMs
  } catch {
    return 0
  }
}

/**
 * Acquire: write PID → mtime = now. Returns the pre-acquire mtime
 * (for rollback), or null if blocked / lost a race.
 *
 *   Success → do nothing. mtime stays at now.
 *   Failure → rollbackConsolidationLock(priorMtime) rewinds mtime.
 *   Crash   → mtime stuck, dead PID → next process reclaims.
 */
export async function tryAcquireConsolidationLock(): Promise<number | null> {
  const path = lockPath()

  let mtimeMs: number | undefined
  let holderPid: number | undefined

```

---


### `src/services/autoDream/consolidationPrompt.ts`

**信息:**
- 行数: 65
- 大小: 3225 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Extracted from dream.ts so auto-dream ships independently of KAIROS
// feature flags (dream.ts is behind a feature()-gated require).

import {
  DIR_EXISTS_GUIDANCE,
  ENTRYPOINT_NAME,
  MAX_ENTRYPOINT_LINES,
} from '../../memdir/memdir.js'

export function buildConsolidationPrompt(
  memoryRoot: string,
  transcriptDir: string,
  extra: string,
): string {
  return `# Dream: Memory Consolidation

You are performing a dream — a reflective pass over your memory files. Synthesize what you've learned recently into durable, well-organized memories so that future sessions can orient quickly.

Memory directory: \`${memoryRoot}\`
${DIR_EXISTS_GUIDANCE}

Session transcripts: \`${transcriptDir}\` (large JSONL files — grep narrowly, don't read whole files)

---

## Phase 1 — Orient

- \`ls\` the memory directory to see what already exists
- Read \`${ENTRYPOINT_NAME}\` to understand the current index
- Skim existing topic files so you improve them rather than creating duplicates
- If \`logs/\` or \`sessions/\` subdirectories exist (assistant-mode layout), review recent entries there

## Phase 2 — Gather recent signal

Look for new information worth persisting. Sources in rough priority order:

1. **Daily logs** (\`logs/YYYY/MM/YYYY-MM-DD.md\`) if present — these are the append-only stream
2. **Existing memories that drifted** — facts that contradict something you see in the codebase now
3. **Transcript search** — if you need specific context (e.g., "what was the error message from yesterday's build failure?"), grep the JSONL transcripts for narrow terms:
   \`grep -rn "<narrow term>" ${transcriptDir}/ --include="*.jsonl" | tail -50\`

Don't exhaustively read transcripts. Look only for things you already suspect matter.

## Phase 3 — Consolidate

For each thing worth remembering, write or update a memory file at the top level of the memory directory. Use the memory file format and type conventions from your system prompt's auto-memory section — it's the source of truth for what to save, how to structure it, and what NOT to save.

Focus on:
- Merging new signal into existing topic files rather than creating near-duplicates
- Converting relative dates ("yesterday", "last week") to absolute dates so they remain interpretable after time passes

```

---


### `src/services/awaySummary.ts`

**信息:**
- 行数: 74
- 大小: 2671 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { APIUserAbortError } from '@anthropic-ai/sdk'
import { getEmptyToolPermissionContext } from '../Tool.js'
import type { Message } from '../types/message.js'
import { logForDebugging } from '../utils/debug.js'
import {
  createUserMessage,
  getAssistantMessageText,
} from '../utils/messages.js'
import { getSmallFastModel } from '../utils/model/model.js'
import { asSystemPrompt } from '../utils/systemPromptType.js'
import { queryModelWithoutStreaming } from './api/claude.js'
import { getSessionMemoryContent } from './SessionMemory/sessionMemoryUtils.js'

// Recap only needs recent context — truncate to avoid "prompt too long" on
// large sessions. 30 messages ≈ ~15 exchanges, plenty for "where we left off."
const RECENT_MESSAGE_WINDOW = 30

function buildAwaySummaryPrompt(memory: string | null): string {
  const memoryBlock = memory
    ? `Session memory (broader context):\n${memory}\n\n`
    : ''
  return `${memoryBlock}The user stepped away and is coming back. Write exactly 1-3 short sentences. Start by stating the high-level task — what they are building or debugging, not implementation details. Next: the concrete next step. Skip status reports and commit recaps.`
}

/**
 * Generates a short session recap for the "while you were away" card.
 * Returns null on abort, empty transcript, or error.
 */
export async function generateAwaySummary(
  messages: readonly Message[],
  signal: AbortSignal,
): Promise<string | null> {
  if (messages.length === 0) {
    return null
  }

  try {
    const memory = await getSessionMemoryContent()
    const recent = messages.slice(-RECENT_MESSAGE_WINDOW)
    recent.push(createUserMessage({ content: buildAwaySummaryPrompt(memory) }))
    const response = await queryModelWithoutStreaming({
      messages: recent,
      systemPrompt: asSystemPrompt([]),
      thinkingConfig: { type: 'disabled' },
      tools: [],
      signal,
      options: {
        getToolPermissionContext: async () => getEmptyToolPermissionContext(),
        model: getSmallFastModel(),
        toolChoice: undefined,

```

---


### `src/services/claudeAiLimits.ts`

**信息:**
- 行数: 515
- 大小: 16803 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { APIError } from '@anthropic-ai/sdk'
import type { MessageParam } from '@anthropic-ai/sdk/resources/index.mjs'
import isEqual from 'lodash-es/isEqual.js'
import { getIsNonInteractiveSession } from '../bootstrap/state.js'
import { isClaudeAISubscriber } from '../utils/auth.js'
import { getModelBetas } from '../utils/betas.js'
import { getGlobalConfig, saveGlobalConfig } from '../utils/config.js'
import { logError } from '../utils/log.js'
import { getSmallFastModel } from '../utils/model/model.js'
import { isEssentialTrafficOnly } from '../utils/privacyLevel.js'
import type { AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS } from './analytics/index.js'
import { logEvent } from './analytics/index.js'
import { getAPIMetadata } from './api/claude.js'
import { getAnthropicClient } from './api/client.js'
import {
  processRateLimitHeaders,
  shouldProcessRateLimits,
} from './rateLimitMocking.js'

// Re-export message functions from centralized location
export {
  getRateLimitErrorMessage,
  getRateLimitWarning,
  getUsingOverageText,
} from './rateLimitMessages.js'

type QuotaStatus = 'allowed' | 'allowed_warning' | 'rejected'

type RateLimitType =
  | 'five_hour'
  | 'seven_day'
  | 'seven_day_opus'
  | 'seven_day_sonnet'
  | 'overage'

export type { RateLimitType }

type EarlyWarningThreshold = {
  utilization: number // 0-1 scale: trigger warning when usage >= this
  timePct: number // 0-1 scale: trigger warning when time elapsed <= this
}

type EarlyWarningConfig = {
  rateLimitType: RateLimitType
  claimAbbrev: '5h' | '7d'
  windowSeconds: number
  thresholds: EarlyWarningThreshold[]
}

// Early warning configurations in priority order (checked first to last)

```

---


### `src/services/claudeAiLimitsHook.ts`

**信息:**
- 行数: 23
- 大小: 515 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useState } from 'react'
import {
  type ClaudeAILimits,
  currentLimits,
  statusListeners,
} from './claudeAiLimits.js'

export function useClaudeAiLimits(): ClaudeAILimits {
  const [limits, setLimits] = useState<ClaudeAILimits>({ ...currentLimits })

  useEffect(() => {
    const listener = (newLimits: ClaudeAILimits) => {
      setLimits({ ...newLimits })
    }
    statusListeners.add(listener)

    return () => {
      statusListeners.delete(listener)
    }
  }, [])

  return limits
}

```

---


### `src/services/compact/apiMicrocompact.ts`

**信息:**
- 行数: 153
- 大小: 4996 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { FILE_EDIT_TOOL_NAME } from 'src/tools/FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from 'src/tools/FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from 'src/tools/FileWriteTool/prompt.js'
import { GLOB_TOOL_NAME } from 'src/tools/GlobTool/prompt.js'
import { GREP_TOOL_NAME } from 'src/tools/GrepTool/prompt.js'
import { NOTEBOOK_EDIT_TOOL_NAME } from 'src/tools/NotebookEditTool/constants.js'
import { WEB_FETCH_TOOL_NAME } from 'src/tools/WebFetchTool/prompt.js'
import { WEB_SEARCH_TOOL_NAME } from 'src/tools/WebSearchTool/prompt.js'
import { SHELL_TOOL_NAMES } from 'src/utils/shell/shellToolUtils.js'
import { isEnvTruthy } from '../../utils/envUtils.js'

// docs: https://docs.google.com/document/d/1oCT4evvWTh3P6z-kcfNQwWTCxAhkoFndSaNS9Gm40uw/edit?tab=t.0

// Default values for context management strategies
// Match client-side microcompact token values
const DEFAULT_MAX_INPUT_TOKENS = 180_000 // Typical warning threshold
const DEFAULT_TARGET_INPUT_TOKENS = 40_000 // Keep last 40k tokens like client-side

const TOOLS_CLEARABLE_RESULTS = [
  ...SHELL_TOOL_NAMES,
  GLOB_TOOL_NAME,
  GREP_TOOL_NAME,
  FILE_READ_TOOL_NAME,
  WEB_FETCH_TOOL_NAME,
  WEB_SEARCH_TOOL_NAME,
]

const TOOLS_CLEARABLE_USES = [
  FILE_EDIT_TOOL_NAME,
  FILE_WRITE_TOOL_NAME,
  NOTEBOOK_EDIT_TOOL_NAME,
]

// Context management strategy types matching API documentation
export type ContextEditStrategy =
  | {
      type: 'clear_tool_uses_20250919'
      trigger?: {
        type: 'input_tokens'
        value: number
      }
      keep?: {
        type: 'tool_uses'
        value: number
      }
      clear_tool_inputs?: boolean | string[]
      exclude_tools?: string[]
      clear_at_least?: {
        type: 'input_tokens'
        value: number

```

---


### `src/services/compact/autoCompact.ts`

**信息:**
- 行数: 351
- 大小: 12905 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { markPostCompaction } from 'src/bootstrap/state.js'
import { getSdkBetas } from '../../bootstrap/state.js'
import type { QuerySource } from '../../constants/querySource.js'
import type { ToolUseContext } from '../../Tool.js'
import type { Message } from '../../types/message.js'
import { getGlobalConfig } from '../../utils/config.js'
import { getContextWindowForModel } from '../../utils/context.js'
import { logForDebugging } from '../../utils/debug.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { hasExactErrorMessage } from '../../utils/errors.js'
import type { CacheSafeParams } from '../../utils/forkedAgent.js'
import { logError } from '../../utils/log.js'
import { tokenCountWithEstimation } from '../../utils/tokens.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../analytics/growthbook.js'
import { getMaxOutputTokensForModel } from '../api/claude.js'
import { notifyCompaction } from '../api/promptCacheBreakDetection.js'
import { setLastSummarizedMessageId } from '../SessionMemory/sessionMemoryUtils.js'
import {
  type CompactionResult,
  compactConversation,
  ERROR_MESSAGE_USER_ABORT,
  type RecompactionInfo,
} from './compact.js'
import { runPostCompactCleanup } from './postCompactCleanup.js'
import { trySessionMemoryCompaction } from './sessionMemoryCompact.js'

// Reserve this many tokens for output during compaction
// Based on p99.99 of compact summary output being 17,387 tokens.
const MAX_OUTPUT_TOKENS_FOR_SUMMARY = 20_000

// Returns the context window size minus the max output tokens for the model
export function getEffectiveContextWindowSize(model: string): number {
  const reservedTokensForSummary = Math.min(
    getMaxOutputTokensForModel(model),
    MAX_OUTPUT_TOKENS_FOR_SUMMARY,
  )
  let contextWindow = getContextWindowForModel(model, getSdkBetas())

  const autoCompactWindow = process.env.CLAUDE_CODE_AUTO_COMPACT_WINDOW
  if (autoCompactWindow) {
    const parsed = parseInt(autoCompactWindow, 10)
    if (!isNaN(parsed) && parsed > 0) {
      contextWindow = Math.min(contextWindow, parsed)
    }
  }

  return contextWindow - reservedTokensForSummary
}


```

---


### `src/services/compact/cachedMCConfig.ts`

**信息:**
- 行数: 3
- 大小: 54 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function getCachedMCConfig() {
  return null
}

```

---


### `src/services/compact/cachedMicrocompact.ts`

**信息:**
- 行数: 20
- 大小: 376 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export interface CachedMCState {
  // 简单的状态接口
}

export interface CacheEditsBlock {
  // 缓存编辑接口
}

export interface PinnedCacheEdits {
  // 固定缓存编辑接口
}

export function createCachedMCState(): CachedMCState {
  return {}
}

// 其他需要的函数可以在这里添加默认实现
export function someFunction(): any {
  return null
}

```

---


### `src/services/compact/compact.ts`

**信息:**
- 行数: 1705
- 大小: 60814 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { UUID } from 'crypto'
import uniqBy from 'lodash-es/uniqBy.js'

/* eslint-disable @typescript-eslint/no-require-imports */
const sessionTranscriptModule = feature('KAIROS')
  ? (require('../sessionTranscript/sessionTranscript.js') as typeof import('../sessionTranscript/sessionTranscript.js'))
  : null

import { APIUserAbortError } from '@anthropic-ai/sdk'
import { markPostCompaction } from 'src/bootstrap/state.js'
import { getInvokedSkillsForAgent } from '../../bootstrap/state.js'
import type { QuerySource } from '../../constants/querySource.js'
import type { CanUseToolFn } from '../../hooks/useCanUseTool.js'
import type { Tool, ToolUseContext } from '../../Tool.js'
import type { LocalAgentTaskState } from '../../tasks/LocalAgentTask/LocalAgentTask.js'
import { FileReadTool } from '../../tools/FileReadTool/FileReadTool.js'
import {
  FILE_READ_TOOL_NAME,
  FILE_UNCHANGED_STUB,
} from '../../tools/FileReadTool/prompt.js'
import { ToolSearchTool } from '../../tools/ToolSearchTool/ToolSearchTool.js'
import type { AgentId } from '../../types/ids.js'
import type {
  AssistantMessage,
  AttachmentMessage,
  HookResultMessage,
  Message,
  PartialCompactDirection,
  SystemCompactBoundaryMessage,
  SystemMessage,
  UserMessage,
} from '../../types/message.js'
import {
  createAttachmentMessage,
  generateFileAttachment,
  getAgentListingDeltaAttachment,
  getDeferredToolsDeltaAttachment,
  getMcpInstructionsDeltaAttachment,
} from '../../utils/attachments.js'
import { getMemoryPath } from '../../utils/config.js'
import { COMPACT_MAX_OUTPUT_TOKENS } from '../../utils/context.js'
import {
  analyzeContext,
  tokenStatsToStatsigMetrics,
} from '../../utils/contextAnalysis.js'
import { logForDebugging } from '../../utils/debug.js'
import { hasExactErrorMessage } from '../../utils/errors.js'
import { cacheToObject } from '../../utils/fileStateCache.js'
import {

```

---


### `src/services/compact/compactWarningHook.ts`

**信息:**
- 行数: 16
- 大小: 568 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useSyncExternalStore } from 'react'
import { compactWarningStore } from './compactWarningState.js'

/**
 * React hook to subscribe to compact warning suppression state.
 *
 * Lives in its own file so that compactWarningState.ts stays React-free:
 * microCompact.ts imports the pure state functions, and pulling React into
 * that module graph would drag it into the print-mode startup path.
 */
export function useCompactWarningSuppression(): boolean {
  return useSyncExternalStore(
    compactWarningStore.subscribe,
    compactWarningStore.getState,
  )
}

```

---


### `src/services/compact/compactWarningState.ts`

**信息:**
- 行数: 18
- 大小: 693 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { createStore } from '../../state/store.js'

/**
 * Tracks whether the "context left until autocompact" warning should be suppressed.
 * We suppress immediately after successful compaction since we don't have accurate
 * token counts until the next API response.
 */
export const compactWarningStore = createStore<boolean>(false)

/** Suppress the compact warning. Call after successful compaction. */
export function suppressCompactWarning(): void {
  compactWarningStore.setState(() => true)
}

/** Clear the compact warning suppression. Called at start of new compact attempt. */
export function clearCompactWarningSuppression(): void {
  compactWarningStore.setState(() => false)
}

```

---


### `src/services/compact/grouping.ts`

**信息:**
- 行数: 63
- 大小: 2794 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Message } from '../../types/message.js'

/**
 * Groups messages at API-round boundaries: one group per API round-trip.
 * A boundary fires when a NEW assistant response begins (different
 * message.id from the prior assistant). For well-formed conversations
 * this is an API-safe split point — the API contract requires every
 * tool_use to be resolved before the next assistant turn, so pairing
 * validity falls out of the assistant-id boundary. For malformed inputs
 * (dangling tool_use after resume/truncation) the fork's
 * ensureToolResultPairing repairs the split at API time.
 *
 * Replaces the prior human-turn grouping (boundaries only at real user
 * prompts) with finer-grained API-round grouping, allowing reactive
 * compact to operate on single-prompt agentic sessions (SDK/CCR/eval
 * callers) where the entire workload is one human turn.
 *
 * Extracted to its own file to break the compact.ts ↔ compactMessages.ts
 * cycle (CC-1180) — the cycle shifted module-init order enough to surface
 * a latent ws CJS/ESM resolution race in CI shard-2.
 */
export function groupMessagesByApiRound(messages: Message[]): Message[][] {
  const groups: Message[][] = []
  let current: Message[] = []
  // message.id of the most recently seen assistant. This is the sole
  // boundary gate: streaming chunks from the same API response share an
  // id, so boundaries only fire at the start of a genuinely new round.
  // normalizeMessages yields one AssistantMessage per content block, and
  // StreamingToolExecutor interleaves tool_results between chunks live
  // (yield order, not concat order — see query.ts:613). The id check
  // correctly keeps `[tu_A(id=X), result_A, tu_B(id=X)]` in one group.
  let lastAssistantId: string | undefined

  // In a well-formed conversation the API contract guarantees every
  // tool_use is resolved before the next assistant turn, so lastAssistantId
  // alone is a sufficient boundary gate. Tracking unresolved tool_use IDs
  // would only do work when the conversation is malformed (dangling tool_use
  // after resume-from-partial-batch or max_tokens truncation) — and in that
  // case it pins the gate shut forever, merging all subsequent rounds into
  // one group. We let those boundaries fire; the summarizer fork's own
  // ensureToolResultPairing at claude.ts:1136 repairs the dangling tu at
  // API time.
  for (const msg of messages) {
    if (
      msg.type === 'assistant' &&
      msg.message.id !== lastAssistantId &&
      current.length > 0
    ) {
      groups.push(current)
      current = [msg]

```

---


### `src/services/compact/microCompact.ts`

**信息:**
- 行数: 530
- 大小: 19544 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs'
import type { QuerySource } from '../../constants/querySource.js'
import type { ToolUseContext } from '../../Tool.js'
import { FILE_EDIT_TOOL_NAME } from '../../tools/FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from '../../tools/FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from '../../tools/FileWriteTool/prompt.js'
import { GLOB_TOOL_NAME } from '../../tools/GlobTool/prompt.js'
import { GREP_TOOL_NAME } from '../../tools/GrepTool/prompt.js'
import { WEB_FETCH_TOOL_NAME } from '../../tools/WebFetchTool/prompt.js'
import { WEB_SEARCH_TOOL_NAME } from '../../tools/WebSearchTool/prompt.js'
import type { Message } from '../../types/message.js'
import { logForDebugging } from '../../utils/debug.js'
import { getMainLoopModel } from '../../utils/model/model.js'
import { SHELL_TOOL_NAMES } from '../../utils/shell/shellToolUtils.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'
import { notifyCacheDeletion } from '../api/promptCacheBreakDetection.js'
import { roughTokenCountEstimation } from '../tokenEstimation.js'
import {
  clearCompactWarningSuppression,
  suppressCompactWarning,
} from './compactWarningState.js'
import {
  getTimeBasedMCConfig,
  type TimeBasedMCConfig,
} from './timeBasedMCConfig.js'

// Inline from utils/toolResultStorage.ts — importing that file pulls in
// sessionStorage → utils/messages → services/api/errors, completing a
// circular-deps loop back through this file via promptCacheBreakDetection.
// Drift is caught by a test asserting equality with the source-of-truth.
export const TIME_BASED_MC_CLEARED_MESSAGE = '[Old tool result content cleared]'

const IMAGE_MAX_TOKEN_SIZE = 2000

// Only compact these tools
const COMPACTABLE_TOOLS = new Set<string>([
  FILE_READ_TOOL_NAME,
  ...SHELL_TOOL_NAMES,
  GREP_TOOL_NAME,
  GLOB_TOOL_NAME,
  WEB_SEARCH_TOOL_NAME,
  WEB_FETCH_TOOL_NAME,
  FILE_EDIT_TOOL_NAME,
  FILE_WRITE_TOOL_NAME,
])

```

---


### `src/services/compact/postCompactCleanup.ts`

**信息:**
- 行数: 77
- 大小: 3778 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { QuerySource } from '../../constants/querySource.js'
import { clearSystemPromptSections } from '../../constants/systemPromptSections.js'
import { getUserContext } from '../../context.js'
import { clearSpeculativeChecks } from '../../tools/BashTool/bashPermissions.js'
import { clearClassifierApprovals } from '../../utils/classifierApprovals.js'
import { resetGetMemoryFilesCache } from '../../utils/claudemd.js'
import { clearSessionMessagesCache } from '../../utils/sessionStorage.js'
import { clearBetaTracingState } from '../../utils/telemetry/betaSessionTracing.js'
import { resetMicrocompactState } from './microCompact.js'

/**
 * Run cleanup of caches and tracking state after compaction.
 * Call this after both auto-compact and manual /compact to free memory
 * held by tracking structures that are invalidated by compaction.
 *
 * Note: We intentionally do NOT clear invoked skill content here.
 * Skill content must survive across multiple compactions so that
 * createSkillAttachmentIfNeeded() can include the full skill text
 * in subsequent compaction attachments.
 *
 * querySource: pass the compacting query's source so we can skip
 * resets that would clobber main-thread module-level state. Subagents
 * (agent:*) run in the same process and share module-level state
 * (context-collapse store, getMemoryFiles one-shot hook flag,
 * getUserContext cache); resetting those when a SUBAGENT compacts
 * would corrupt the MAIN thread's state. All compaction callers should
 * pass querySource — undefined is only safe for callers that are
 * genuinely main-thread-only (/compact, /clear).
 */
export function runPostCompactCleanup(querySource?: QuerySource): void {
  // Subagents (agent:*) run in the same process and share module-level
  // state with the main thread. Only reset main-thread module-level state
  // (context-collapse, memory file cache) for main-thread compacts.
  // Same startsWith pattern as isMainThread (index.ts:188).
  const isMainThreadCompact =
    querySource === undefined ||
    querySource.startsWith('repl_main_thread') ||
    querySource === 'sdk'

  resetMicrocompactState()
  if (feature('CONTEXT_COLLAPSE')) {
    if (isMainThreadCompact) {
      /* eslint-disable @typescript-eslint/no-require-imports */
      ;(
        require('../contextCollapse/index.js') as typeof import('../contextCollapse/index.js')
      ).resetContextCollapse()
      /* eslint-enable @typescript-eslint/no-require-imports */
    }
  }

```

---


### `src/services/compact/prompt.ts`

**信息:**
- 行数: 374
- 大小: 16278 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { PartialCompactDirection } from '../../types/message.js'

// Dead code elimination: conditional import for proactive mode
/* eslint-disable @typescript-eslint/no-require-imports */
const proactiveModule =
  feature('PROACTIVE') || feature('KAIROS')
    ? (require('../../proactive/index.js') as typeof import('../../proactive/index.js'))
    : null
/* eslint-enable @typescript-eslint/no-require-imports */

// Aggressive no-tools preamble. The cache-sharing fork path inherits the
// parent's full tool set (required for cache-key match), and on Sonnet 4.6+
// adaptive-thinking models the model sometimes attempts a tool call despite
// the weaker trailer instruction. With maxTurns: 1, a denied tool call means
// no text output → falls through to the streaming fallback (2.79% on 4.6 vs
// 0.01% on 4.5). Putting this FIRST and making it explicit about rejection
// consequences prevents the wasted turn.
const NO_TOOLS_PREAMBLE = `CRITICAL: Respond with TEXT ONLY. Do NOT call any tools.

- Do NOT use Read, Bash, Grep, Glob, Edit, Write, or ANY other tool.
- You already have all the context you need in the conversation above.
- Tool calls will be REJECTED and will waste your only turn — you will fail the task.
- Your entire response must be plain text: an <analysis> block followed by a <summary> block.

`

// Two variants: BASE scopes to "the conversation", PARTIAL scopes to "the
// recent messages". The <analysis> block is a drafting scratchpad that
// formatCompactSummary() strips before the summary reaches context.
const DETAILED_ANALYSIS_INSTRUCTION_BASE = `Before providing your final summary, wrap your analysis in <analysis> tags to organize your thoughts and ensure you've covered all necessary points. In your analysis process:

1. Chronologically analyze each message and section of the conversation. For each section thoroughly identify:
   - The user's explicit requests and intents
   - Your approach to addressing the user's requests
   - Key decisions, technical concepts and code patterns
   - Specific details like:
     - file names
     - full code snippets
     - function signatures
     - file edits
   - Errors that you ran into and how you fixed them
   - Pay special attention to specific user feedback that you received, especially if the user told you to do something differently.
2. Double-check for technical accuracy and completeness, addressing each required element thoroughly.`

const DETAILED_ANALYSIS_INSTRUCTION_PARTIAL = `Before providing your final summary, wrap your analysis in <analysis> tags to organize your thoughts and ensure you've covered all necessary points. In your analysis process:

1. Analyze the recent messages chronologically. For each section thoroughly identify:
   - The user's explicit requests and intents
   - Your approach to addressing the user's requests

```

---


### `src/services/compact/reactiveCompact.ts`

**信息:**
- 行数: 3
- 大小: 91 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export async function runReactiveCompact<T>(messages: T): Promise<T> {
  return messages
}

```

---


### `src/services/compact/sessionMemoryCompact.ts`

**信息:**
- 行数: 630
- 大小: 21058 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * EXPERIMENT: Session memory compaction
 */

import type { AgentId } from '../../types/ids.js'
import type { HookResultMessage, Message } from '../../types/message.js'
import { logForDebugging } from '../../utils/debug.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { errorMessage } from '../../utils/errors.js'
import {
  createCompactBoundaryMessage,
  createUserMessage,
  isCompactBoundaryMessage,
} from '../../utils/messages.js'
import { getMainLoopModel } from '../../utils/model/model.js'
import { getSessionMemoryPath } from '../../utils/permissions/filesystem.js'
import { processSessionStartHooks } from '../../utils/sessionStart.js'
import { getTranscriptPath } from '../../utils/sessionStorage.js'
import { tokenCountFromLastAPIResponse } from '../../utils/tokens.js'
import { extractDiscoveredToolNames } from '../../utils/toolSearch.js'
import {
  getDynamicConfig_BLOCKS_ON_INIT,
  getFeatureValue_CACHED_MAY_BE_STALE,
} from '../analytics/growthbook.js'
import { logEvent } from '../analytics/index.js'
import {
  isSessionMemoryEmpty,
  truncateSessionMemoryForCompact,
} from '../SessionMemory/prompts.js'
import {
  getLastSummarizedMessageId,
  getSessionMemoryContent,
  waitForSessionMemoryExtraction,
} from '../SessionMemory/sessionMemoryUtils.js'
import {
  annotateBoundaryWithPreservedSegment,
  buildPostCompactMessages,
  type CompactionResult,
  createPlanAttachmentIfNeeded,
} from './compact.js'
import { estimateMessageTokens } from './microCompact.js'
import { getCompactUserSummaryMessage } from './prompt.js'

/**
 * Configuration for session memory compaction thresholds
 */
export type SessionMemoryCompactConfig = {
  /** Minimum tokens to preserve after compaction */
  minTokens: number
  /** Minimum number of messages with text blocks to keep */

```

---


### `src/services/compact/snipCompact.ts`

**信息:**
- 行数: 10
- 大小: 221 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function snipCompactIfNeeded<T>(messages: T, _options?: unknown): {
  messages: T
  changed: boolean
} {
  return { messages, changed: false }
}

export function isSnipBoundaryMessage(): boolean {
  return false
}

```

---


### `src/services/compact/snipProjection.ts`

**信息:**
- 行数: 7
- 大小: 149 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function isSnipBoundaryMessage(): boolean {
  return false
}

export function projectSnippedMessages<T>(messages: T): T {
  return messages
}

```

---


### `src/services/compact/timeBasedMCConfig.ts`

**信息:**
- 行数: 43
- 大小: 1766 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../analytics/growthbook.js'

/**
 * GrowthBook config for time-based microcompact.
 *
 * Triggers content-clearing microcompact when the gap since the last main-loop
 * assistant message exceeds a threshold — the server-side prompt cache has
 * almost certainly expired, so the full prefix will be rewritten anyway.
 * Clearing old tool results before the request shrinks what gets rewritten.
 *
 * Runs BEFORE the API call (in microcompactMessages, upstream of callModel)
 * so the shrunk prompt is what actually gets sent. Running after the first
 * miss would only help subsequent turns.
 *
 * Main thread only — subagents have short lifetimes where gap-based eviction
 * doesn't apply.
 */
export type TimeBasedMCConfig = {
  /** Master switch. When false, time-based microcompact is a no-op. */
  enabled: boolean
  /** Trigger when (now − last assistant timestamp) exceeds this many minutes.
   *  60 is the safe choice: the server's 1h cache TTL is guaranteed expired
   *  for all users, so we never force a miss that wouldn't have happened. */
  gapThresholdMinutes: number
  /** Keep this many most-recent compactable tool results.
   *  When set, takes priority over any default; older results are cleared. */
  keepRecent: number
}

const TIME_BASED_MC_CONFIG_DEFAULTS: TimeBasedMCConfig = {
  enabled: false,
  gapThresholdMinutes: 60,
  keepRecent: 5,
}

export function getTimeBasedMCConfig(): TimeBasedMCConfig {
  // Hoist the GB read so exposure fires on every eval path, not just when
  // the caller's other conditions (querySource, messages.length) pass.
  return getFeatureValue_CACHED_MAY_BE_STALE<TimeBasedMCConfig>(
    'tengu_slate_heron',
    TIME_BASED_MC_CONFIG_DEFAULTS,
  )
}

```

---


### `src/services/contextCollapse/index.ts`

**信息:**
- 行数: 51
- 大小: 984 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
type Stats = {
  collapsedSpans: number
  stagedSpans: number
  health: {
    totalErrors: number
    totalEmptySpawns: number
    emptySpawnWarningEmitted: boolean
  }
}

const stats: Stats = {
  collapsedSpans: 0,
  stagedSpans: 0,
  health: {
    totalErrors: 0,
    totalEmptySpawns: 0,
    emptySpawnWarningEmitted: false,
  },
}

const listeners = new Set<() => void>()

export function subscribe(listener: () => void): () => void {
  listeners.add(listener)
  return () => listeners.delete(listener)
}

export function getStats(): Stats {
  return stats
}

export function isContextCollapseEnabled(): boolean {
  return false
}

export function resetContextCollapse(): void {}

export async function applyCollapsesIfNeeded<T>(messages: T): Promise<{
  messages: T
  changed: boolean
}> {
  return { messages, changed: false }
}

export function isWithheldPromptTooLong(): boolean {
  return false
}

export function recoverFromOverflow<T>(messages: T): T {
  return messages

```

---


### `src/services/contextCollapse/operations.ts`

**信息:**
- 行数: 7
- 大小: 127 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function summarizeContextCollapseState() {
  return null
}

export function getContextCollapsePreview() {
  return []
}

```

---


### `src/services/contextCollapse/persist.ts`

**信息:**
- 行数: 1
- 大小: 46 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function restoreFromEntries(): void {}

```

---


### `src/services/diagnosticTracking.ts`

**信息:**
- 行数: 397
- 大小: 12315 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import figures from 'figures'
import { logError } from 'src/utils/log.js'
import { callIdeRpc } from '../services/mcp/client.js'
import type { MCPServerConnection } from '../services/mcp/types.js'
import { ClaudeError } from '../utils/errors.js'
import { normalizePathForComparison, pathsEqual } from '../utils/file.js'
import { getConnectedIdeClient } from '../utils/ide.js'
import { jsonParse } from '../utils/slowOperations.js'

class DiagnosticsTrackingError extends ClaudeError {}

const MAX_DIAGNOSTICS_SUMMARY_CHARS = 4000

export interface Diagnostic {
  message: string
  severity: 'Error' | 'Warning' | 'Info' | 'Hint'
  range: {
    start: { line: number; character: number }
    end: { line: number; character: number }
  }
  source?: string
  code?: string
}

export interface DiagnosticFile {
  uri: string
  diagnostics: Diagnostic[]
}

export class DiagnosticTrackingService {
  private static instance: DiagnosticTrackingService | undefined
  private baseline: Map<string, Diagnostic[]> = new Map()

  private initialized = false
  private mcpClient: MCPServerConnection | undefined

  // Track when files were last processed/fetched
  private lastProcessedTimestamps: Map<string, number> = new Map()

  // Track which files have received right file diagnostics and if they've changed
  // Map<normalizedPath, lastClaudeFsRightDiagnostics>
  private rightFileDiagnosticsState: Map<string, Diagnostic[]> = new Map()

  static getInstance(): DiagnosticTrackingService {
    if (!DiagnosticTrackingService.instance) {
      DiagnosticTrackingService.instance = new DiagnosticTrackingService()
    }
    return DiagnosticTrackingService.instance
  }


```

---


### `src/services/extractMemories/extractMemories.ts`

**信息:**
- 行数: 615
- 大小: 21684 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Extracts durable memories from the current session transcript
 * and writes them to the auto-memory directory (~/.claude/projects/<path>/memory/).
 *
 * It runs once at the end of each complete query loop (when the model produces
 * a final response with no tool calls) via handleStopHooks in stopHooks.ts.
 *
 * Uses the forked agent pattern (runForkedAgent) — a perfect fork of the main
 * conversation that shares the parent's prompt cache.
 *
 * State is closure-scoped inside initExtractMemories() rather than module-level,
 * following the same pattern as confidenceRating.ts. Tests call
 * initExtractMemories() in beforeEach to get a fresh closure.
 */

import { feature } from 'bun:bundle'
import { basename } from 'path'
import { getIsRemoteMode } from '../../bootstrap/state.js'
import type { CanUseToolFn } from '../../hooks/useCanUseTool.js'
import { ENTRYPOINT_NAME } from '../../memdir/memdir.js'
import {
  formatMemoryManifest,
  scanMemoryFiles,
} from '../../memdir/memoryScan.js'
import {
  getAutoMemPath,
  isAutoMemoryEnabled,
  isAutoMemPath,
} from '../../memdir/paths.js'
import type { Tool } from '../../Tool.js'
import { BASH_TOOL_NAME } from '../../tools/BashTool/toolName.js'
import { FILE_EDIT_TOOL_NAME } from '../../tools/FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from '../../tools/FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from '../../tools/FileWriteTool/prompt.js'
import { GLOB_TOOL_NAME } from '../../tools/GlobTool/prompt.js'
import { GREP_TOOL_NAME } from '../../tools/GrepTool/prompt.js'
import { REPL_TOOL_NAME } from '../../tools/REPLTool/constants.js'
import type {
  AssistantMessage,
  Message,
  SystemLocalCommandMessage,
  SystemMessage,
} from '../../types/message.js'
import { createAbortController } from '../../utils/abortController.js'
import { count, uniq } from '../../utils/array.js'
import { logForDebugging } from '../../utils/debug.js'
import {
  createCacheSafeParams,
  runForkedAgent,
} from '../../utils/forkedAgent.js'

```

---


### `src/services/extractMemories/prompts.ts`

**信息:**
- 行数: 154
- 大小: 7673 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Prompt templates for the background memory extraction agent.
 *
 * The extraction agent runs as a perfect fork of the main conversation — same
 * system prompt, same message prefix. The main agent's system prompt always
 * has full save instructions; when the main agent writes memories itself,
 * extractMemories.ts skips that turn (hasMemoryWritesSince). This prompt
 * fires only when the main agent didn't write, so the save-criteria here
 * overlap the system prompt's harmlessly.
 */

import { feature } from 'bun:bundle'
import {
  MEMORY_FRONTMATTER_EXAMPLE,
  TYPES_SECTION_COMBINED,
  TYPES_SECTION_INDIVIDUAL,
  WHAT_NOT_TO_SAVE_SECTION,
} from '../../memdir/memoryTypes.js'
import { BASH_TOOL_NAME } from '../../tools/BashTool/toolName.js'
import { FILE_EDIT_TOOL_NAME } from '../../tools/FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from '../../tools/FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from '../../tools/FileWriteTool/prompt.js'
import { GLOB_TOOL_NAME } from '../../tools/GlobTool/prompt.js'
import { GREP_TOOL_NAME } from '../../tools/GrepTool/prompt.js'

/**
 * Shared opener for both extract-prompt variants.
 */
function opener(newMessageCount: number, existingMemories: string): string {
  const manifest =
    existingMemories.length > 0
      ? `\n\n## Existing memory files\n\n${existingMemories}\n\nCheck this list before writing — update an existing file rather than creating a duplicate.`
      : ''
  return [
    `You are now acting as the memory extraction subagent. Analyze the most recent ~${newMessageCount} messages above and use them to update your persistent memory systems.`,
    '',
    `Available tools: ${FILE_READ_TOOL_NAME}, ${GREP_TOOL_NAME}, ${GLOB_TOOL_NAME}, read-only ${BASH_TOOL_NAME} (ls/find/cat/stat/wc/head/tail and similar), and ${FILE_EDIT_TOOL_NAME}/${FILE_WRITE_TOOL_NAME} for paths inside the memory directory only. ${BASH_TOOL_NAME} rm is not permitted. All other tools — MCP, Agent, write-capable ${BASH_TOOL_NAME}, etc — will be denied.`,
    '',
    `You have a limited turn budget. ${FILE_EDIT_TOOL_NAME} requires a prior ${FILE_READ_TOOL_NAME} of the same file, so the efficient strategy is: turn 1 — issue all ${FILE_READ_TOOL_NAME} calls in parallel for every file you might update; turn 2 — issue all ${FILE_WRITE_TOOL_NAME}/${FILE_EDIT_TOOL_NAME} calls in parallel. Do not interleave reads and writes across multiple turns.`,
    '',
    `You MUST only use content from the last ~${newMessageCount} messages to update your persistent memories. Do not waste any turns attempting to investigate or verify that content further — no grepping source files, no reading code to confirm a pattern exists, no git commands.` +
      manifest,
  ].join('\n')
}

/**
 * Build the extraction prompt for auto-only memory (no team memory).
 * Four-type taxonomy, no scope guidance (single directory).
 */
export function buildExtractAutoOnlyPrompt(

```

---


### `src/services/internalLogging.ts`

**信息:**
- 行数: 90
- 大小: 2799 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { readFile } from 'fs/promises'
import memoize from 'lodash-es/memoize.js'
import type { ToolPermissionContext } from '../Tool.js'
import { jsonStringify } from '../utils/slowOperations.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from './analytics/index.js'

/**
 * Get the current Kubernetes namespace:
 * Returns null on laptops/local development,
 * "default" for devboxes in default namespace,
 * "ts" for devboxes in ts namespace,
 * ...
 */
const getKubernetesNamespace = memoize(async (): Promise<string | null> => {
  if (process.env.USER_TYPE !== 'ant') {
    return null
  }
  const namespacePath =
    '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
  const namespaceNotFound = 'namespace not found'
  try {
    const content = await readFile(namespacePath, { encoding: 'utf8' })
    return content.trim()
  } catch {
    return namespaceNotFound
  }
})

/**
 * Get the OCI container ID from within a running container
 */
export const getContainerId = memoize(async (): Promise<string | null> => {
  if (process.env.USER_TYPE !== 'ant') {
    return null
  }
  const containerIdPath = '/proc/self/mountinfo'
  const containerIdNotFound = 'container ID not found'
  const containerIdNotFoundInMountinfo = 'container ID not found in mountinfo'
  try {
    const mountinfo = (
      await readFile(containerIdPath, { encoding: 'utf8' })
    ).trim()

    // Pattern to match both Docker and containerd/CRI-O container IDs
    // Docker: /docker/containers/[64-char-hex]
    // Containerd: /sandboxes/[64-char-hex]
    const containerIdPattern =

```

---


### `src/services/lsp/LSPClient.ts`

**信息:**
- 行数: 447
- 大小: 14361 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { type ChildProcess, spawn } from 'child_process'
import {
  createMessageConnection,
  type MessageConnection,
  StreamMessageReader,
  StreamMessageWriter,
  Trace,
} from 'vscode-jsonrpc/node.js'
import type {
  InitializeParams,
  InitializeResult,
  ServerCapabilities,
} from 'vscode-languageserver-protocol'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'
import { subprocessEnv } from '../../utils/subprocessEnv.js'
/**
 * LSP client interface.
 */
export type LSPClient = {
  readonly capabilities: ServerCapabilities | undefined
  readonly isInitialized: boolean
  start: (
    command: string,
    args: string[],
    options?: {
      env?: Record<string, string>
      cwd?: string
    },
  ) => Promise<void>
  initialize: (params: InitializeParams) => Promise<InitializeResult>
  sendRequest: <TResult>(method: string, params: unknown) => Promise<TResult>
  sendNotification: (method: string, params: unknown) => Promise<void>
  onNotification: (method: string, handler: (params: unknown) => void) => void
  onRequest: <TParams, TResult>(
    method: string,
    handler: (params: TParams) => TResult | Promise<TResult>,
  ) => void
  stop: () => Promise<void>
}

/**
 * Create an LSP client wrapper using vscode-jsonrpc.
 * Manages communication with an LSP server process via stdio.
 *
 * @param onCrash - Called when the server process exits unexpectedly (non-zero
 *   exit code during operation, not during intentional stop). Allows the owner
 *   to propagate crash state so the server can be restarted on next use.
 */

```

---


### `src/services/lsp/LSPDiagnosticRegistry.ts`

**信息:**
- 行数: 386
- 大小: 11957 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { randomUUID } from 'crypto'
import { LRUCache } from 'lru-cache'
import { logForDebugging } from '../../utils/debug.js'
import { toError } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import type { DiagnosticFile } from '../diagnosticTracking.js'

/**
 * Pending LSP diagnostic notification
 */
export type PendingLSPDiagnostic = {
  /** Server that sent the diagnostic */
  serverName: string
  /** Diagnostic files */
  files: DiagnosticFile[]
  /** When diagnostic was received */
  timestamp: number
  /** Whether attachment was already sent to conversation */
  attachmentSent: boolean
}

/**
 * LSP Diagnostic Registry
 *
 * Stores LSP diagnostics received asynchronously from LSP servers via
 * textDocument/publishDiagnostics notifications. Follows the same pattern
 * as AsyncHookRegistry for consistent async attachment delivery.
 *
 * Pattern:
 * 1. LSP server sends publishDiagnostics notification
 * 2. registerPendingLSPDiagnostic() stores diagnostic
 * 3. checkForLSPDiagnostics() retrieves pending diagnostics
 * 4. getLSPDiagnosticAttachments() converts to Attachment[]
 * 5. getAttachments() delivers to conversation automatically
 *
 * Similar to AsyncHookRegistry but simpler since diagnostics arrive
 * synchronously (no need to accumulate output over time).
 */

// Volume limiting constants
const MAX_DIAGNOSTICS_PER_FILE = 10
const MAX_TOTAL_DIAGNOSTICS = 30

// Max files to track for deduplication - prevents unbounded memory growth
const MAX_DELIVERED_FILES = 500

// Global registry state
const pendingDiagnostics = new Map<string, PendingLSPDiagnostic>()


```

---


### `src/services/lsp/LSPServerInstance.ts`

**信息:**
- 行数: 511
- 大小: 16864 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import * as path from 'path'
import { pathToFileURL } from 'url'
import type { InitializeParams } from 'vscode-languageserver-protocol'
import { getCwd } from '../../utils/cwd.js'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'
import { sleep } from '../../utils/sleep.js'
import type { createLSPClient as createLSPClientType } from './LSPClient.js'
import type { LspServerState, ScopedLspServerConfig } from './types.js'

/**
 * LSP error code for "content modified" - indicates the server's state changed
 * during request processing (e.g., rust-analyzer still indexing the project).
 * This is a transient error that can be retried.
 */
const LSP_ERROR_CONTENT_MODIFIED = -32801

/**
 * Maximum number of retries for transient LSP errors like "content modified".
 */
const MAX_RETRIES_FOR_TRANSIENT_ERRORS = 3

/**
 * Base delay in milliseconds for exponential backoff on transient errors.
 * Actual delays: 500ms, 1000ms, 2000ms
 */
const RETRY_BASE_DELAY_MS = 500
/**
 * LSP server instance interface returned by createLSPServerInstance.
 * Manages the lifecycle of a single LSP server with state tracking and health monitoring.
 */
export type LSPServerInstance = {
  /** Unique server identifier */
  readonly name: string
  /** Server configuration */
  readonly config: ScopedLspServerConfig
  /** Current server state */
  readonly state: LspServerState
  /** When the server was last started */
  readonly startTime: Date | undefined
  /** Last error encountered */
  readonly lastError: Error | undefined
  /** Number of times restart() has been called */
  readonly restartCount: number
  /** Start the server and initialize it */
  start(): Promise<void>
  /** Stop the server gracefully */
  stop(): Promise<void>
  /** Manually restart the server (stop then start) */

```

---


### `src/services/lsp/LSPServerManager.ts`

**信息:**
- 行数: 420
- 大小: 13394 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import * as path from 'path'
import { pathToFileURL } from 'url'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'
import { getAllLspServers } from './config.js'
import {
  createLSPServerInstance,
  type LSPServerInstance,
} from './LSPServerInstance.js'
import type { ScopedLspServerConfig } from './types.js'
/**
 * LSP Server Manager interface returned by createLSPServerManager.
 * Manages multiple LSP server instances and routes requests based on file extensions.
 */
export type LSPServerManager = {
  /** Initialize the manager by loading all configured LSP servers */
  initialize(): Promise<void>
  /** Shutdown all running servers and clear state */
  shutdown(): Promise<void>
  /** Get the LSP server instance for a given file path */
  getServerForFile(filePath: string): LSPServerInstance | undefined
  /** Ensure the appropriate LSP server is started for the given file */
  ensureServerStarted(filePath: string): Promise<LSPServerInstance | undefined>
  /** Send a request to the appropriate LSP server for the given file */
  sendRequest<T>(
    filePath: string,
    method: string,
    params: unknown,
  ): Promise<T | undefined>
  /** Get all running server instances */
  getAllServers(): Map<string, LSPServerInstance>
  /** Synchronize file open to LSP server (sends didOpen notification) */
  openFile(filePath: string, content: string): Promise<void>
  /** Synchronize file change to LSP server (sends didChange notification) */
  changeFile(filePath: string, content: string): Promise<void>
  /** Synchronize file save to LSP server (sends didSave notification) */
  saveFile(filePath: string): Promise<void>
  /** Synchronize file close to LSP server (sends didClose notification) */
  closeFile(filePath: string): Promise<void>
  /** Check if a file is already open on a compatible LSP server */
  isFileOpen(filePath: string): boolean
}

/**
 * Creates an LSP server manager instance.
 *
 * Manages multiple LSP server instances and routes requests based on file extensions.
 * Uses factory function pattern with closures for state encapsulation (avoiding classes).
 *

```

---


### `src/services/lsp/config.ts`

**信息:**
- 行数: 79
- 大小: 2857 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { PluginError } from '../../types/plugin.js'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage, toError } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'
import { getPluginLspServers } from '../../utils/plugins/lspPluginIntegration.js'
import { loadAllPluginsCacheOnly } from '../../utils/plugins/pluginLoader.js'
import type { ScopedLspServerConfig } from './types.js'

/**
 * Get all configured LSP servers from plugins.
 * LSP servers are only supported via plugins, not user/project settings.
 *
 * @returns Object containing servers configuration keyed by scoped server name
 */
export async function getAllLspServers(): Promise<{
  servers: Record<string, ScopedLspServerConfig>
}> {
  const allServers: Record<string, ScopedLspServerConfig> = {}

  try {
    // Get all enabled plugins
    const { enabled: plugins } = await loadAllPluginsCacheOnly()

    // Load LSP servers from each plugin in parallel.
    // Each plugin is independent — results are merged in original order so
    // Object.assign collision precedence (later plugins win) is preserved.
    const results = await Promise.all(
      plugins.map(async plugin => {
        const errors: PluginError[] = []
        try {
          const scopedServers = await getPluginLspServers(plugin, errors)
          return { plugin, scopedServers, errors }
        } catch (e) {
          // Defensive: if one plugin throws, don't lose results from the
          // others. The previous serial loop implicitly tolerated this.
          logForDebugging(
            `Failed to load LSP servers for plugin ${plugin.name}: ${e}`,
            { level: 'error' },
          )
          return { plugin, scopedServers: undefined, errors }
        }
      }),
    )

    for (const { plugin, scopedServers, errors } of results) {
      const serverCount = scopedServers ? Object.keys(scopedServers).length : 0
      if (serverCount > 0) {
        // Merge into all servers (already scoped by getPluginLspServers)
        Object.assign(allServers, scopedServers)


```

---


### `src/services/lsp/manager.ts`

**信息:**
- 行数: 289
- 大小: 10067 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { logForDebugging } from '../../utils/debug.js'
import { isBareMode } from '../../utils/envUtils.js'
import { errorMessage } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'
import {
  createLSPServerManager,
  type LSPServerManager,
} from './LSPServerManager.js'
import { registerLSPNotificationHandlers } from './passiveFeedback.js'

/**
 * Initialization state of the LSP server manager
 */
type InitializationState = 'not-started' | 'pending' | 'success' | 'failed'

/**
 * Global singleton instance of the LSP server manager.
 * Initialized during Claude Code startup.
 */
let lspManagerInstance: LSPServerManager | undefined

/**
 * Current initialization state
 */
let initializationState: InitializationState = 'not-started'

/**
 * Error from last initialization attempt, if any
 */
let initializationError: Error | undefined

/**
 * Generation counter to prevent stale initialization promises from updating state
 */
let initializationGeneration = 0

/**
 * Promise that resolves when initialization completes (success or failure)
 */
let initializationPromise: Promise<void> | undefined

/**
 * Test-only sync reset. shutdownLspServerManager() is async and tears down
 * real connections; this only clears the module-scope singleton state so
 * reinitializeLspServerManager() early-returns on 'not-started' in downstream
 * tests on the same shard.
 */
export function _resetLspManagerForTesting(): void {
  initializationState = 'not-started'
  initializationError = undefined

```

---


### `src/services/lsp/passiveFeedback.ts`

**信息:**
- 行数: 328
- 大小: 11190 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { fileURLToPath } from 'url'
import type { PublishDiagnosticsParams } from 'vscode-languageserver-protocol'
import { logForDebugging } from '../../utils/debug.js'
import { toError } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import type { DiagnosticFile } from '../diagnosticTracking.js'
import { registerPendingLSPDiagnostic } from './LSPDiagnosticRegistry.js'
import type { LSPServerManager } from './LSPServerManager.js'

/**
 * Map LSP severity to Claude diagnostic severity
 *
 * Maps LSP severity numbers to Claude diagnostic severity strings.
 * Accepts numeric severity values (1=Error, 2=Warning, 3=Information, 4=Hint)
 * or undefined, defaulting to 'Error' for invalid/missing values.
 */
function mapLSPSeverity(
  lspSeverity: number | undefined,
): 'Error' | 'Warning' | 'Info' | 'Hint' {
  // LSP DiagnosticSeverity enum:
  // 1 = Error, 2 = Warning, 3 = Information, 4 = Hint
  switch (lspSeverity) {
    case 1:
      return 'Error'
    case 2:
      return 'Warning'
    case 3:
      return 'Info'
    case 4:
      return 'Hint'
    default:
      return 'Error'
  }
}

/**
 * Convert LSP diagnostics to Claude diagnostic format
 *
 * Converts LSP PublishDiagnosticsParams to DiagnosticFile[] format
 * used by Claude's attachment system.
 */
export function formatDiagnosticsForAttachment(
  params: PublishDiagnosticsParams,
): DiagnosticFile[] {
  // Parse URI (may be file:// or plain path) and normalize to file system path
  let uri: string
  try {
    // Handle both file:// URIs and plain paths
    uri = params.uri.startsWith('file://')

```

---


### `src/services/lsp/types.ts`

**信息:**
- 行数: 2
- 大小: 96 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type ScopedLspServerConfig = Record<string, unknown>
export type LspServerState = string

```

---


### `src/services/mcp/InProcessTransport.ts`

**信息:**
- 行数: 63
- 大小: 1772 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Transport } from '@modelcontextprotocol/sdk/shared/transport.js'
import type { JSONRPCMessage } from '@modelcontextprotocol/sdk/types.js'

/**
 * In-process linked transport pair for running an MCP server and client
 * in the same process without spawning a subprocess.
 *
 * `send()` on one side delivers to `onmessage` on the other.
 * `close()` on either side calls `onclose` on both.
 */
class InProcessTransport implements Transport {
  private peer: InProcessTransport | undefined
  private closed = false

  onclose?: () => void
  onerror?: (error: Error) => void
  onmessage?: (message: JSONRPCMessage) => void

  /** @internal */
  _setPeer(peer: InProcessTransport): void {
    this.peer = peer
  }

  async start(): Promise<void> {}

  async send(message: JSONRPCMessage): Promise<void> {
    if (this.closed) {
      throw new Error('Transport is closed')
    }
    // Deliver to the other side asynchronously to avoid stack depth issues
    // with synchronous request/response cycles
    queueMicrotask(() => {
      this.peer?.onmessage?.(message)
    })
  }

  async close(): Promise<void> {
    if (this.closed) {
      return
    }
    this.closed = true
    this.onclose?.()
    // Close the peer if it hasn't already closed
    if (this.peer && !this.peer.closed) {
      this.peer.closed = true
      this.peer.onclose?.()
    }
  }
}


```

---


### `src/services/mcp/MCPConnectionManager.tsx`

**信息:**
- 行数: 73
- 大小: 8186 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, type ReactNode, useContext, useMemo } from 'react';
import type { Command } from '../../commands.js';
import type { Tool } from '../../Tool.js';
import type { MCPServerConnection, ScopedMcpServerConfig, ServerResource } from './types.js';
import { useManageMCPConnections } from './useManageMCPConnections.js';
interface MCPConnectionContextValue {
  reconnectMcpServer: (serverName: string) => Promise<{
    client: MCPServerConnection;
    tools: Tool[];
    commands: Command[];
    resources?: ServerResource[];
  }>;
  toggleMcpServer: (serverName: string) => Promise<void>;
}
const MCPConnectionContext = createContext<MCPConnectionContextValue | null>(null);
export function useMcpReconnect() {
  const context = useContext(MCPConnectionContext);
  if (!context) {
    throw new Error("useMcpReconnect must be used within MCPConnectionManager");
  }
  return context.reconnectMcpServer;
}
export function useMcpToggleEnabled() {
  const context = useContext(MCPConnectionContext);
  if (!context) {
    throw new Error("useMcpToggleEnabled must be used within MCPConnectionManager");
  }
  return context.toggleMcpServer;
}
interface MCPConnectionManagerProps {
  children: ReactNode;
  dynamicMcpConfig: Record<string, ScopedMcpServerConfig> | undefined;
  isStrictMcpConfig: boolean;
}

// TODO (ollie): We may be able to get rid of this context by putting these function on app state
export function MCPConnectionManager(t0) {
  const $ = _c(6);
  const {
    children,
    dynamicMcpConfig,
    isStrictMcpConfig
  } = t0;
  const {
    reconnectMcpServer,
    toggleMcpServer
  } = useManageMCPConnections(dynamicMcpConfig, isStrictMcpConfig);
  let t1;
  if ($[0] !== reconnectMcpServer || $[1] !== toggleMcpServer) {

```

---


### `src/services/mcp/SdkControlTransport.ts`

**信息:**
- 行数: 136
- 大小: 4503 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * SDK MCP Transport Bridge
 *
 * This file implements a transport bridge that allows MCP servers running in the SDK process
 * to communicate with the Claude Code CLI process through control messages.
 *
 * ## Architecture Overview
 *
 * Unlike regular MCP servers that run as separate processes, SDK MCP servers run in-process
 * within the SDK. This requires a special transport mechanism to bridge communication between:
 * - The CLI process (where the MCP client runs)
 * - The SDK process (where the SDK MCP server runs)
 *
 * ## Message Flow
 *
 * ### CLI → SDK (via SdkControlClientTransport)
 * 1. CLI's MCP Client calls a tool → sends JSONRPC request to SdkControlClientTransport
 * 2. Transport wraps the message in a control request with server_name and request_id
 * 3. Control request is sent via stdout to the SDK process
 * 4. SDK's StructuredIO receives the control response and routes it back to the transport
 * 5. Transport unwraps the response and returns it to the MCP Client
 *
 * ### SDK → CLI (via SdkControlServerTransport)
 * 1. Query receives control request with MCP message and calls transport.onmessage
 * 2. MCP server processes the message and calls transport.send() with response
 * 3. Transport calls sendMcpMessage callback with the response
 * 4. Query's callback resolves the pending promise with the response
 * 5. Query returns the response to complete the control request
 *
 * ## Key Design Points
 *
 * - SdkControlClientTransport: StructuredIO tracks pending requests
 * - SdkControlServerTransport: Query tracks pending requests
 * - The control request wrapper includes server_name to route to the correct SDK server
 * - The system supports multiple SDK MCP servers running simultaneously
 * - Message IDs are preserved through the entire flow for proper correlation
 */

import type { Transport } from '@modelcontextprotocol/sdk/shared/transport.js'
import type { JSONRPCMessage } from '@modelcontextprotocol/sdk/types.js'

/**
 * Callback function to send an MCP message and get the response
 */
export type SendMcpMessageCallback = (
  serverName: string,
  message: JSONRPCMessage,
) => Promise<JSONRPCMessage>

/**

```

---


### `src/services/mcp/auth.ts`

**信息:**
- 行数: 2465
- 大小: 88879 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  discoverAuthorizationServerMetadata,
  discoverOAuthServerInfo,
  type OAuthClientProvider,
  type OAuthDiscoveryState,
  auth as sdkAuth,
  refreshAuthorization as sdkRefreshAuthorization,
} from '@modelcontextprotocol/sdk/client/auth.js'
import {
  InvalidGrantError,
  OAuthError,
  ServerError,
  TemporarilyUnavailableError,
  TooManyRequestsError,
} from '@modelcontextprotocol/sdk/server/auth/errors.js'
import {
  type AuthorizationServerMetadata,
  type OAuthClientInformation,
  type OAuthClientInformationFull,
  type OAuthClientMetadata,
  OAuthErrorResponseSchema,
  OAuthMetadataSchema,
  type OAuthTokens,
  OAuthTokensSchema,
} from '@modelcontextprotocol/sdk/shared/auth.js'
import type { FetchLike } from '@modelcontextprotocol/sdk/shared/transport.js'
import axios from 'axios'
import { createHash, randomBytes, randomUUID } from 'crypto'
import { mkdir } from 'fs/promises'
import { createServer, type Server } from 'http'
import { join } from 'path'
import { parse } from 'url'
import xss from 'xss'
import { MCP_CLIENT_METADATA_URL } from '../../constants/oauth.js'
import { openBrowser } from '../../utils/browser.js'
import { getClaudeConfigHomeDir } from '../../utils/envUtils.js'
import { errorMessage, getErrnoCode } from '../../utils/errors.js'
import * as lockfile from '../../utils/lockfile.js'
import { logMCPDebug } from '../../utils/log.js'
import { getPlatform } from '../../utils/platform.js'
import { getSecureStorage } from '../../utils/secureStorage/index.js'
import { clearKeychainCache } from '../../utils/secureStorage/macOsKeychainHelpers.js'
import type { SecureStorageData } from '../../utils/secureStorage/types.js'
import { sleep } from '../../utils/sleep.js'
import { jsonParse, jsonStringify } from '../../utils/slowOperations.js'
import { logEvent } from '../analytics/index.js'
import type { AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS } from '../analytics/metadata.js'
import { buildRedirectUri, findAvailablePort } from './oauthPort.js'
import type { McpHTTPServerConfig, McpSSEServerConfig } from './types.js'
import { getLoggingSafeMcpBaseUrl } from './utils.js'

```

---


### `src/services/mcp/channelAllowlist.ts`

**信息:**
- 行数: 76
- 大小: 2838 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Approved channel plugins allowlist. --channels plugin:name@marketplace
 * entries only register if {marketplace, plugin} is on this list. server:
 * entries always fail (schema is plugin-only). The
 * --dangerously-load-development-channels flag bypasses for both kinds.
 * Lives in GrowthBook so it can be updated without a release.
 *
 * Plugin-level granularity: if a plugin is approved, all its channel
 * servers are. Per-server gating was overengineering — a plugin that
 * sprouts a malicious second server is already compromised, and per-server
 * entries would break on harmless plugin refactors.
 *
 * The allowlist check is a pure {marketplace, plugin} comparison against
 * the user's typed tag. The gate's separate 'marketplace' step verifies
 * the tag matches what's actually installed before this check runs.
 */

import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'
import { parsePluginIdentifier } from '../../utils/plugins/pluginIdentifier.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../analytics/growthbook.js'

export type ChannelAllowlistEntry = {
  marketplace: string
  plugin: string
}

const ChannelAllowlistSchema = lazySchema(() =>
  z.array(
    z.object({
      marketplace: z.string(),
      plugin: z.string(),
    }),
  ),
)

export function getChannelAllowlist(): ChannelAllowlistEntry[] {
  const raw = getFeatureValue_CACHED_MAY_BE_STALE<unknown>(
    'tengu_harbor_ledger',
    [],
  )
  const parsed = ChannelAllowlistSchema().safeParse(raw)
  return parsed.success ? parsed.data : []
}

/**
 * Overall channels on/off. Checked before any per-server gating —
 * when false, --channels is a no-op and no handlers register.
 * Default false; GrowthBook 5-min refresh.
 */

```

---


### `src/services/mcp/channelNotification.ts`

**信息:**
- 行数: 316
- 大小: 12540 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Channel notifications — lets an MCP server push user messages into the
 * conversation. A "channel" (Discord, Slack, SMS, etc.) is just an MCP server
 * that:
 *   - exposes tools for outbound messages (e.g. `send_message`) — standard MCP
 *   - sends `notifications/claude/channel` notifications for inbound — this file
 *
 * The notification handler wraps the content in a <channel> tag and
 * enqueues it. SleepTool polls hasCommandsInQueue() and wakes within 1s.
 * The model sees where the message came from and decides which tool to reply
 * with (the channel's MCP tool, SendUserMessage, or both).
 *
 * feature('KAIROS') || feature('KAIROS_CHANNELS'). Runtime gate tengu_harbor.
 * Requires claude.ai OAuth auth — API key users are blocked until
 * console gets a channelsEnabled admin surface. Teams/Enterprise orgs
 * must explicitly opt in via channelsEnabled: true in managed settings.
 */

import type { ServerCapabilities } from '@modelcontextprotocol/sdk/types.js'
import { z } from 'zod/v4'
import { type ChannelEntry, getAllowedChannels } from '../../bootstrap/state.js'
import { CHANNEL_TAG } from '../../constants/xml.js'
import {
  getClaudeAIOAuthTokens,
  getSubscriptionType,
} from '../../utils/auth.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { parsePluginIdentifier } from '../../utils/plugins/pluginIdentifier.js'
import { getSettingsForSource } from '../../utils/settings/settings.js'
import { escapeXmlAttr } from '../../utils/xml.js'
import {
  type ChannelAllowlistEntry,
  getChannelAllowlist,
  isChannelsEnabled,
} from './channelAllowlist.js'

export const ChannelMessageNotificationSchema = lazySchema(() =>
  z.object({
    method: z.literal('notifications/claude/channel'),
    params: z.object({
      content: z.string(),
      // Opaque passthrough — thread_id, user, whatever the channel wants the
      // model to see. Rendered as attributes on the <channel> tag.
      meta: z.record(z.string(), z.string()).optional(),
    }),
  }),
)

/**
 * Structured permission reply from a channel server. Servers that support

```

---


### `src/services/mcp/channelPermissions.ts`

**信息:**
- 行数: 240
- 大小: 8981 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Permission prompts over channels (Telegram, iMessage, Discord).
 *
 * Mirrors `BridgePermissionCallbacks` — when CC hits a permission dialog,
 * it ALSO sends the prompt via active channels and races the reply against
 * local UI / bridge / hooks / classifier. First resolver wins via claim().
 *
 * Inbound is a structured event: the server parses the user's "yes tbxkq"
 * reply and emits notifications/claude/channel/permission with
 * {request_id, behavior}. CC never sees the reply as text — approval
 * requires the server to deliberately emit that specific event, not just
 * relay content. Servers opt in by declaring
 * capabilities.experimental['claude/channel/permission'].
 *
 * Kenneth's "would this let Claude self-approve?": the approving party is
 * the human via the channel, not Claude. But the trust boundary isn't the
 * terminal — it's the allowlist (tengu_harbor_ledger). A compromised
 * channel server CAN fabricate "yes <id>" without the human seeing the
 * prompt. Accepted risk: a compromised channel already has unlimited
 * conversation-injection turns (social-engineer over time, wait for
 * acceptEdits, etc.); inject-then-self-approve is faster, not more
 * capable. The dialog slows a compromised channel; it doesn't stop one.
 * See PR discussion 2956440848.
 */

import { jsonStringify } from '../../utils/slowOperations.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../analytics/growthbook.js'

/**
 * GrowthBook runtime gate — separate from the channels gate (tengu_harbor)
 * so channels can ship without permission-relay riding along (Kenneth: "no
 * bake time if it goes out tomorrow"). Default false; flip without a release.
 * Checked once at useManageMCPConnections mount — mid-session flag changes
 * don't apply until restart.
 */
export function isChannelPermissionRelayEnabled(): boolean {
  return getFeatureValue_CACHED_MAY_BE_STALE('tengu_harbor_permissions', false)
}

export type ChannelPermissionResponse = {
  behavior: 'allow' | 'deny'
  /** Which channel server the reply came from (e.g., "plugin:telegram:tg"). */
  fromServer: string
}

export type ChannelPermissionCallbacks = {
  /** Register a resolver for a request ID. Returns unsubscribe. */
  onResponse(
    requestId: string,
    handler: (response: ChannelPermissionResponse) => void,

```

---


### `src/services/mcp/claudeai.ts`

**信息:**
- 行数: 164
- 大小: 6126 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import memoize from 'lodash-es/memoize.js'
import { getOauthConfig } from 'src/constants/oauth.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from 'src/services/analytics/index.js'
import { getClaudeAIOAuthTokens } from 'src/utils/auth.js'
import { getGlobalConfig, saveGlobalConfig } from 'src/utils/config.js'
import { logForDebugging } from 'src/utils/debug.js'
import { isEnvDefinedFalsy } from 'src/utils/envUtils.js'
import { clearMcpAuthCache } from './client.js'
import { normalizeNameForMCP } from './normalization.js'
import type { ScopedMcpServerConfig } from './types.js'

type ClaudeAIMcpServer = {
  type: 'mcp_server'
  id: string
  display_name: string
  url: string
  created_at: string
}

type ClaudeAIMcpServersResponse = {
  data: ClaudeAIMcpServer[]
  has_more: boolean
  next_page: string | null
}

const FETCH_TIMEOUT_MS = 5000
const MCP_SERVERS_BETA_HEADER = 'mcp-servers-2025-12-04'

/**
 * Fetches MCP server configurations from Claude.ai org configs.
 * These servers are managed by the organization via Claude.ai.
 *
 * Results are memoized for the session lifetime (fetch once per CLI session).
 */
export const fetchClaudeAIMcpConfigsIfEligible = memoize(
  async (): Promise<Record<string, ScopedMcpServerConfig>> => {
    try {
      if (isEnvDefinedFalsy(process.env.ENABLE_CLAUDEAI_MCP_SERVERS)) {
        logForDebugging('[claudeai-mcp] Disabled via env var')
        logEvent('tengu_claudeai_mcp_eligibility', {
          state:
            'disabled_env_var' as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
        })
        return {}
      }


```

---


### `src/services/mcp/client.ts`

**信息:**
- 行数: 3348
- 大小: 119060 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type {
  Base64ImageSource,
  ContentBlockParam,
  MessageParam,
} from '@anthropic-ai/sdk/resources/index.mjs'
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import {
  SSEClientTransport,
  type SSEClientTransportOptions,
} from '@modelcontextprotocol/sdk/client/sse.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'
import {
  StreamableHTTPClientTransport,
  type StreamableHTTPClientTransportOptions,
} from '@modelcontextprotocol/sdk/client/streamableHttp.js'
import {
  createFetchWithInit,
  type FetchLike,
  type Transport,
} from '@modelcontextprotocol/sdk/shared/transport.js'
import {
  CallToolResultSchema,
  ElicitRequestSchema,
  type ElicitRequestURLParams,
  type ElicitResult,
  ErrorCode,
  type JSONRPCMessage,
  type ListPromptsResult,
  ListPromptsResultSchema,
  ListResourcesResultSchema,
  ListRootsRequestSchema,
  type ListToolsResult,
  ListToolsResultSchema,
  McpError,
  type PromptMessage,
  type ResourceLink,
} from '@modelcontextprotocol/sdk/types.js'
import mapValues from 'lodash-es/mapValues.js'
import memoize from 'lodash-es/memoize.js'
import zipObject from 'lodash-es/zipObject.js'
import pMap from 'p-map'
import { getOriginalCwd, getSessionId } from '../../bootstrap/state.js'
import type { Command } from '../../commands.js'
import { getOauthConfig } from '../../constants/oauth.js'
import { PRODUCT_URL } from '../../constants/product.js'
import type { AppState } from '../../state/AppState.js'
import {
  type Tool,
  type ToolCallProgress,

```

---


### `src/services/mcp/config.ts`

**信息:**
- 行数: 1578
- 大小: 51130 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { chmod, open, rename, stat, unlink } from 'fs/promises'
import mapValues from 'lodash-es/mapValues.js'
import memoize from 'lodash-es/memoize.js'
import { dirname, join, parse } from 'path'
import { getPlatform } from 'src/utils/platform.js'
import type { PluginError } from '../../types/plugin.js'
import { getPluginErrorMessage } from '../../types/plugin.js'
import { isClaudeInChromeMCPServer } from '../../utils/claudeInChrome/common.js'
import {
  getCurrentProjectConfig,
  getGlobalConfig,
  saveCurrentProjectConfig,
  saveGlobalConfig,
} from '../../utils/config.js'
import { getCwd } from '../../utils/cwd.js'
import { logForDebugging } from '../../utils/debug.js'
import { getErrnoCode } from '../../utils/errors.js'
import { getFsImplementation } from '../../utils/fsOperations.js'
import { safeParseJSON } from '../../utils/json.js'
import { logError } from '../../utils/log.js'
import { getPluginMcpServers } from '../../utils/plugins/mcpPluginIntegration.js'
import { loadAllPluginsCacheOnly } from '../../utils/plugins/pluginLoader.js'
import { isSettingSourceEnabled } from '../../utils/settings/constants.js'
import { getManagedFilePath } from '../../utils/settings/managedPath.js'
import { isRestrictedToPluginOnly } from '../../utils/settings/pluginOnlyPolicy.js'
import {
  getInitialSettings,
  getSettingsForSource,
} from '../../utils/settings/settings.js'
import {
  isMcpServerCommandEntry,
  isMcpServerNameEntry,
  isMcpServerUrlEntry,
  type SettingsJson,
} from '../../utils/settings/types.js'
import type { ValidationError } from '../../utils/settings/validation.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'
import { fetchClaudeAIMcpConfigsIfEligible } from './claudeai.js'
import { expandEnvVarsInString } from './envExpansion.js'
import {
  type ConfigScope,
  type McpHTTPServerConfig,
  type McpJsonConfig,
  McpJsonConfigSchema,
  type McpServerConfig,

```

---


### `src/services/mcp/elicitationHandler.ts`

**信息:**
- 行数: 313
- 大小: 10166 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Client } from '@modelcontextprotocol/sdk/client/index.js'
import {
  ElicitationCompleteNotificationSchema,
  type ElicitRequestParams,
  ElicitRequestSchema,
  type ElicitResult,
} from '@modelcontextprotocol/sdk/types.js'
import type { AppState } from '../../state/AppState.js'
import {
  executeElicitationHooks,
  executeElicitationResultHooks,
  executeNotificationHooks,
} from '../../utils/hooks.js'
import { logMCPDebug, logMCPError } from '../../utils/log.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'

/** Configuration for the waiting state shown after the user opens a URL. */
export type ElicitationWaitingState = {
  /** Button label, e.g. "Retry now" or "Skip confirmation" */
  actionLabel: string
  /** Whether to show a visible Cancel button (e.g. for error-based retry flow) */
  showCancel?: boolean
}

export type ElicitationRequestEvent = {
  serverName: string
  /** The JSON-RPC request ID, unique per server connection. */
  requestId: string | number
  params: ElicitRequestParams
  signal: AbortSignal
  /**
   * Resolves the elicitation. For explicit elicitations, all actions are
   * meaningful. For error-based retry (-32042), 'accept' is a no-op —
   * the retry is driven by onWaitingDismiss instead.
   */
  respond: (response: ElicitResult) => void
  /** For URL elicitations: shown after user opens the browser. */
  waitingState?: ElicitationWaitingState
  /** Called when phase 2 (waiting) is dismissed by user action or completion. */
  onWaitingDismiss?: (action: 'dismiss' | 'retry' | 'cancel') => void
  /** Set to true by the completion notification handler when the server confirms completion. */
  completed?: boolean
}

function getElicitationMode(params: ElicitRequestParams): 'form' | 'url' {
  return params.mode === 'url' ? 'url' : 'form'

```

---


### `src/services/mcp/envExpansion.ts`

**信息:**
- 行数: 38
- 大小: 1047 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Shared utilities for expanding environment variables in MCP server configurations
 */

/**
 * Expand environment variables in a string value
 * Handles ${VAR} and ${VAR:-default} syntax
 * @returns Object with expanded string and list of missing variables
 */
export function expandEnvVarsInString(value: string): {
  expanded: string
  missingVars: string[]
} {
  const missingVars: string[] = []

  const expanded = value.replace(/\$\{([^}]+)\}/g, (match, varContent) => {
    // Split on :- to support default values (limit to 2 parts to preserve :- in defaults)
    const [varName, defaultValue] = varContent.split(':-', 2)
    const envValue = process.env[varName]

    if (envValue !== undefined) {
      return envValue
    }
    if (defaultValue !== undefined) {
      return defaultValue
    }

    // Track missing variable for error reporting
    missingVars.push(varName)
    // Return original if not found (allows debugging but will be reported as error)
    return match
  })

  return {
    expanded,
    missingVars,
  }
}

```

---


### `src/services/mcp/headersHelper.ts`

**信息:**
- 行数: 138
- 大小: 4718 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getIsNonInteractiveSession } from '../../bootstrap/state.js'
import { checkHasTrustDialogAccepted } from '../../utils/config.js'
import { logAntError } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { execFileNoThrowWithCwd } from '../../utils/execFileNoThrow.js'
import { logError, logMCPDebug, logMCPError } from '../../utils/log.js'
import { jsonParse } from '../../utils/slowOperations.js'
import { logEvent } from '../analytics/index.js'
import type {
  McpHTTPServerConfig,
  McpSSEServerConfig,
  McpWebSocketServerConfig,
  ScopedMcpServerConfig,
} from './types.js'

/**
 * Check if the MCP server config comes from project settings (projectSettings or localSettings)
 * This is important for security checks
 */
function isMcpServerFromProjectOrLocalSettings(
  config: ScopedMcpServerConfig,
): boolean {
  return config.scope === 'project' || config.scope === 'local'
}

/**
 * Get dynamic headers for an MCP server using the headersHelper script
 * @param serverName The name of the MCP server
 * @param config The MCP server configuration
 * @returns Headers object or null if not configured or failed
 */
export async function getMcpHeadersFromHelper(
  serverName: string,
  config: McpSSEServerConfig | McpHTTPServerConfig | McpWebSocketServerConfig,
): Promise<Record<string, string> | null> {
  if (!config.headersHelper) {
    return null
  }

  // Security check for project/local settings
  // Skip trust check in non-interactive mode (e.g., CI/CD, automation)
  if (
    'scope' in config &&
    isMcpServerFromProjectOrLocalSettings(config as ScopedMcpServerConfig) &&
    !getIsNonInteractiveSession()
  ) {
    // Check if trust has been established for this project
    const hasTrust = checkHasTrustDialogAccepted()
    if (!hasTrust) {
      const error = new Error(

```

---


### `src/services/mcp/mcpStringUtils.ts`

**信息:**
- 行数: 106
- 大小: 3968 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Pure string utility functions for MCP tool/server name parsing.
 * This file has no heavy dependencies to keep it lightweight for
 * consumers that only need string parsing (e.g., permissionValidation).
 */

import { normalizeNameForMCP } from './normalization.js'

/*
 * Extracts MCP server information from a tool name string
 * @param toolString The string to parse. Expected format: "mcp__serverName__toolName"
 * @returns An object containing server name and optional tool name, or null if not a valid MCP rule
 *
 * Known limitation: If a server name contains "__", parsing will be incorrect.
 * For example, "mcp__my__server__tool" would parse as server="my" and tool="server__tool"
 * instead of server="my__server" and tool="tool". This is rare in practice since server
 * names typically don't contain double underscores.
 */
export function mcpInfoFromString(toolString: string): {
  serverName: string
  toolName: string | undefined
} | null {
  const parts = toolString.split('__')
  const [mcpPart, serverName, ...toolNameParts] = parts
  if (mcpPart !== 'mcp' || !serverName) {
    return null
  }
  // Join all parts after server name to preserve double underscores in tool names
  const toolName =
    toolNameParts.length > 0 ? toolNameParts.join('__') : undefined
  return { serverName, toolName }
}

/**
 * Generates the MCP tool/command name prefix for a given server
 * @param serverName Name of the MCP server
 * @returns The prefix string
 */
export function getMcpPrefix(serverName: string): string {
  return `mcp__${normalizeNameForMCP(serverName)}__`
}

/**
 * Builds a fully qualified MCP tool name from server and tool names.
 * Inverse of mcpInfoFromString().
 * @param serverName Name of the MCP server (unnormalized)
 * @param toolName Name of the tool (unnormalized)
 * @returns The fully qualified name, e.g., "mcp__server__tool"
 */
export function buildMcpToolName(serverName: string, toolName: string): string {

```

---


### `src/services/mcp/normalization.ts`

**信息:**
- 行数: 23
- 大小: 879 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Pure utility functions for MCP name normalization.
 * This file has no dependencies to avoid circular imports.
 */

// Claude.ai server names are prefixed with this string
const CLAUDEAI_SERVER_PREFIX = 'claude.ai '

/**
 * Normalize server names to be compatible with the API pattern ^[a-zA-Z0-9_-]{1,64}$
 * Replaces any invalid characters (including dots and spaces) with underscores.
 *
 * For claude.ai servers (names starting with "claude.ai "), also collapses
 * consecutive underscores and strips leading/trailing underscores to prevent
 * interference with the __ delimiter used in MCP tool names.
 */
export function normalizeNameForMCP(name: string): string {
  let normalized = name.replace(/[^a-zA-Z0-9_-]/g, '_')
  if (name.startsWith(CLAUDEAI_SERVER_PREFIX)) {
    normalized = normalized.replace(/_+/g, '_').replace(/^_|_$/g, '')
  }
  return normalized
}

```

---


### `src/services/mcp/oauthPort.ts`

**信息:**
- 行数: 78
- 大小: 2325 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * OAuth redirect port helpers — extracted from auth.ts to break the
 * auth.ts ↔ xaaIdpLogin.ts circular dependency.
 */
import { createServer } from 'http'
import { getPlatform } from '../../utils/platform.js'

// Windows dynamic port range 49152-65535 is reserved
const REDIRECT_PORT_RANGE =
  getPlatform() === 'windows'
    ? { min: 39152, max: 49151 }
    : { min: 49152, max: 65535 }
const REDIRECT_PORT_FALLBACK = 3118

/**
 * Builds a redirect URI on localhost with the given port and a fixed `/callback` path.
 *
 * RFC 8252 Section 7.3 (OAuth for Native Apps): loopback redirect URIs match any
 * port as long as the path matches.
 */
export function buildRedirectUri(
  port: number = REDIRECT_PORT_FALLBACK,
): string {
  return `http://localhost:${port}/callback`
}

function getMcpOAuthCallbackPort(): number | undefined {
  const port = parseInt(process.env.MCP_OAUTH_CALLBACK_PORT || '', 10)
  return port > 0 ? port : undefined
}

/**
 * Finds an available port in the specified range for OAuth redirect
 * Uses random selection for better security
 */
export async function findAvailablePort(): Promise<number> {
  // First, try the configured port if specified
  const configuredPort = getMcpOAuthCallbackPort()
  if (configuredPort) {
    return configuredPort
  }

  const { min, max } = REDIRECT_PORT_RANGE
  const range = max - min + 1
  const maxAttempts = Math.min(range, 100) // Don't try forever

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const port = min + Math.floor(Math.random() * range)

    try {

```

---


### `src/services/mcp/officialRegistry.ts`

**信息:**
- 行数: 72
- 大小: 2013 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'

type RegistryServer = {
  server: {
    remotes?: Array<{ url: string }>
  }
}

type RegistryResponse = {
  servers: RegistryServer[]
}

// URLs stripped of query string and trailing slash — matches the normalization
// done by getLoggingSafeMcpBaseUrl so direct Set.has() lookup works.
let officialUrls: Set<string> | undefined = undefined

function normalizeUrl(url: string): string | undefined {
  try {
    const u = new URL(url)
    u.search = ''
    return u.toString().replace(/\/$/, '')
  } catch {
    return undefined
  }
}

/**
 * Fire-and-forget fetch of the official MCP registry.
 * Populates officialUrls for isOfficialMcpUrl lookups.
 */
export async function prefetchOfficialMcpUrls(): Promise<void> {
  if (process.env.CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC) {
    return
  }

  try {
    const response = await axios.get<RegistryResponse>(
      'https://api.anthropic.com/mcp-registry/v0/servers?version=latest&visibility=commercial',
      { timeout: 5000 },
    )

    const urls = new Set<string>()
    for (const entry of response.data.servers) {
      for (const remote of entry.server.remotes ?? []) {
        const normalized = normalizeUrl(remote.url)
        if (normalized) {
          urls.add(normalized)
        }

```

---


### `src/services/mcp/types.ts`

**信息:**
- 行数: 258
- 大小: 6962 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Client } from '@modelcontextprotocol/sdk/client/index.js'
import type {
  Resource,
  ServerCapabilities,
} from '@modelcontextprotocol/sdk/types.js'
import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'

// Configuration schemas and types
export const ConfigScopeSchema = lazySchema(() =>
  z.enum([
    'local',
    'user',
    'project',
    'dynamic',
    'enterprise',
    'claudeai',
    'managed',
  ]),
)
export type ConfigScope = z.infer<ReturnType<typeof ConfigScopeSchema>>

export const TransportSchema = lazySchema(() =>
  z.enum(['stdio', 'sse', 'sse-ide', 'http', 'ws', 'sdk']),
)
export type Transport = z.infer<ReturnType<typeof TransportSchema>>

export const McpStdioServerConfigSchema = lazySchema(() =>
  z.object({
    type: z.literal('stdio').optional(), // Optional for backwards compatibility
    command: z.string().min(1, 'Command cannot be empty'),
    args: z.array(z.string()).default([]),
    env: z.record(z.string(), z.string()).optional(),
  }),
)

// Cross-App Access (XAA / SEP-990): just a per-server flag. IdP connection
// details (issuer, clientId, callbackPort) come from settings.xaaIdp — configured
// once, shared across all XAA-enabled servers. clientId/clientSecret (parent
// oauth config + keychain slot) are for the MCP server's AS.
const McpXaaConfigSchema = lazySchema(() => z.boolean())

const McpOAuthConfigSchema = lazySchema(() =>
  z.object({
    clientId: z.string().optional(),
    callbackPort: z.number().int().positive().optional(),
    authServerMetadataUrl: z
      .string()
      .url()
      .startsWith('https://', {

```

---


### `src/services/mcp/useManageMCPConnections.ts`

**信息:**
- 行数: 1141
- 大小: 44866 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { basename } from 'path'
import { useCallback, useEffect, useRef } from 'react'
import { getSessionId } from '../../bootstrap/state.js'
import type { Command } from '../../commands.js'
import type { Tool } from '../../Tool.js'
import {
  clearServerCache,
  fetchCommandsForClient,
  fetchResourcesForClient,
  fetchToolsForClient,
  getMcpToolsCommandsAndResources,
  reconnectMcpServerImpl,
} from './client.js'
import type {
  MCPServerConnection,
  ScopedMcpServerConfig,
  ServerResource,
} from './types.js'

/* eslint-disable @typescript-eslint/no-require-imports */
const fetchMcpSkillsForClient = feature('MCP_SKILLS')
  ? (
      require('../../skills/mcpSkills.js') as typeof import('../../skills/mcpSkills.js')
    ).fetchMcpSkillsForClient
  : null
const clearSkillIndexCache = feature('EXPERIMENTAL_SKILL_SEARCH')
  ? (
      require('../skillSearch/localSearch.js') as typeof import('../skillSearch/localSearch.js')
    ).clearSkillIndexCache
  : null

import {
  PromptListChangedNotificationSchema,
  ResourceListChangedNotificationSchema,
  ToolListChangedNotificationSchema,
} from '@modelcontextprotocol/sdk/types.js'
import omit from 'lodash-es/omit.js'
import reject from 'lodash-es/reject.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from 'src/services/analytics/index.js'
import {
  dedupClaudeAiMcpServers,
  doesEnterpriseMcpConfigExist,
  filterMcpServersByPolicy,
  getClaudeCodeMcpConfigs,
  isMcpServerDisabled,
  setMcpServerEnabled,

```

---


### `src/services/mcp/utils.ts`

**信息:**
- 行数: 575
- 大小: 17931 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { createHash } from 'crypto'
import { join } from 'path'
import { getIsNonInteractiveSession } from '../../bootstrap/state.js'
import type { Command } from '../../commands.js'
import type { AgentMcpServerInfo } from '../../components/mcp/types.js'
import type { Tool } from '../../Tool.js'
import type { AgentDefinition } from '../../tools/AgentTool/loadAgentsDir.js'
import { getCwd } from '../../utils/cwd.js'
import { getGlobalClaudeFile } from '../../utils/env.js'
import { isSettingSourceEnabled } from '../../utils/settings/constants.js'
import {
  getSettings_DEPRECATED,
  hasSkipDangerousModePermissionPrompt,
} from '../../utils/settings/settings.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { getEnterpriseMcpFilePath, getMcpConfigByName } from './config.js'
import { mcpInfoFromString } from './mcpStringUtils.js'
import { normalizeNameForMCP } from './normalization.js'
import {
  type ConfigScope,
  ConfigScopeSchema,
  type MCPServerConnection,
  type McpHTTPServerConfig,
  type McpServerConfig,
  type McpSSEServerConfig,
  type McpStdioServerConfig,
  type McpWebSocketServerConfig,
  type ScopedMcpServerConfig,
  type ServerResource,
} from './types.js'

/**
 * Filters tools by MCP server name
 *
 * @param tools Array of tools to filter
 * @param serverName Name of the MCP server
 * @returns Tools belonging to the specified server
 */
export function filterToolsByServer(tools: Tool[], serverName: string): Tool[] {
  const prefix = `mcp__${normalizeNameForMCP(serverName)}__`
  return tools.filter(tool => tool.name?.startsWith(prefix))
}

/**
 * True when a command belongs to the given MCP server.
 *
 * MCP **prompts** are named `mcp__<server>__<prompt>` (wire-format constraint);
 * MCP **skills** are named `<server>:<skill>` (matching plugin/nested-dir skill
 * naming). Both live in `mcp.commands`, so cleanup and filtering must match
 * either shape.

```

---


### `src/services/mcp/vscodeSdkMcp.ts`

**信息:**
- 行数: 112
- 大小: 3703 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { logForDebugging } from 'src/utils/debug.js'
import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'
import {
  checkStatsigFeatureGate_CACHED_MAY_BE_STALE,
  getFeatureValue_CACHED_MAY_BE_STALE,
} from '../analytics/growthbook.js'
import { logEvent } from '../analytics/index.js'
import type { ConnectedMCPServer, MCPServerConnection } from './types.js'

// Mirror of AutoModeEnabledState in permissionSetup.ts — inlined because that
// file pulls in too many deps for this thin IPC module.
type AutoModeEnabledState = 'enabled' | 'disabled' | 'opt-in'
function readAutoModeEnabledState(): AutoModeEnabledState | undefined {
  const v = getFeatureValue_CACHED_MAY_BE_STALE<{ enabled?: string }>(
    'tengu_auto_mode_config',
    {},
  )?.enabled
  return v === 'enabled' || v === 'disabled' || v === 'opt-in' ? v : undefined
}

export const LogEventNotificationSchema = lazySchema(() =>
  z.object({
    method: z.literal('log_event'),
    params: z.object({
      eventName: z.string(),
      eventData: z.object({}).passthrough(),
    }),
  }),
)

// Store the VSCode MCP client reference for sending notifications
let vscodeMcpClient: ConnectedMCPServer | null = null

/**
 * Sends a file_updated notification to the VSCode MCP server. This is used to
 * notify VSCode when files are edited or written by Claude.
 */
export function notifyVscodeFileUpdated(
  filePath: string,
  oldContent: string | null,
  newContent: string | null,
): void {
  if (process.env.USER_TYPE !== 'ant' || !vscodeMcpClient) {
    return
  }

  void vscodeMcpClient.client
    .notification({
      method: 'file_updated',

```

---


### `src/services/mcp/xaa.ts`

**信息:**
- 行数: 511
- 大小: 18286 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Cross-App Access (XAA) / Enterprise Managed Authorization (SEP-990)
 *
 * Obtains an MCP access token WITHOUT a browser consent screen by chaining:
 *   1. RFC 8693 Token Exchange at the IdP: id_token → ID-JAG
 *   2. RFC 7523 JWT Bearer Grant at the AS: ID-JAG → access_token
 *
 * Spec refs:
 *   - ID-JAG (IETF draft): https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-assertion-authz-grant/
 *   - MCP ext-auth (SEP-990): https://github.com/modelcontextprotocol/ext-auth
 *   - RFC 8693 (Token Exchange), RFC 7523 (JWT Bearer), RFC 9728 (PRM)
 *
 * Reference impl: ~/code/mcp/conformance/examples/clients/typescript/everything-client.ts:375-522
 *
 * Structure: four Layer-2 ops (aligned with TS SDK PR #1593's Layer-2 shapes so
 * a future SDK swap is mechanical) + one Layer-3 orchestrator that composes them.
 */

import {
  discoverAuthorizationServerMetadata,
  discoverOAuthProtectedResourceMetadata,
} from '@modelcontextprotocol/sdk/client/auth.js'
import type { FetchLike } from '@modelcontextprotocol/sdk/shared/transport.js'
import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'
import { logMCPDebug } from '../../utils/log.js'
import { jsonStringify } from '../../utils/slowOperations.js'

const XAA_REQUEST_TIMEOUT_MS = 30000

const TOKEN_EXCHANGE_GRANT = 'urn:ietf:params:oauth:grant-type:token-exchange'
const JWT_BEARER_GRANT = 'urn:ietf:params:oauth:grant-type:jwt-bearer'
const ID_JAG_TOKEN_TYPE = 'urn:ietf:params:oauth:token-type:id-jag'
const ID_TOKEN_TYPE = 'urn:ietf:params:oauth:token-type:id_token'

/**
 * Creates a fetch wrapper that enforces the XAA request timeout and optionally
 * composes a caller-provided abort signal. Using AbortSignal.any ensures the
 * user's cancel (e.g. Esc in the auth menu) actually aborts in-flight requests
 * rather than being clobbered by the timeout signal.
 */
function makeXaaFetch(abortSignal?: AbortSignal): FetchLike {
  return (url, init) => {
    const timeout = AbortSignal.timeout(XAA_REQUEST_TIMEOUT_MS)
    const signal = abortSignal
      ? // eslint-disable-next-line eslint-plugin-n/no-unsupported-features/node-builtins
        AbortSignal.any([timeout, abortSignal])
      : timeout
    // eslint-disable-next-line eslint-plugin-n/no-unsupported-features/node-builtins
    return fetch(url, { ...init, signal })

```

---


### `src/services/mcp/xaaIdpLogin.ts`

**信息:**
- 行数: 487
- 大小: 16271 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * XAA IdP Login — acquires an OIDC id_token from an enterprise IdP via the
 * standard authorization_code + PKCE flow, then caches it by IdP issuer.
 *
 * This is the "one browser pop" in the XAA value prop: one IdP login → N silent
 * MCP server auths. The id_token is cached in the keychain and reused until expiry.
 */

import {
  exchangeAuthorization,
  startAuthorization,
} from '@modelcontextprotocol/sdk/client/auth.js'
import {
  type OAuthClientInformation,
  type OpenIdProviderDiscoveryMetadata,
  OpenIdProviderDiscoveryMetadataSchema,
} from '@modelcontextprotocol/sdk/shared/auth.js'
import { randomBytes } from 'crypto'
import { createServer, type Server } from 'http'
import { parse } from 'url'
import xss from 'xss'
import { openBrowser } from '../../utils/browser.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { toError } from '../../utils/errors.js'
import { logMCPDebug } from '../../utils/log.js'
import { getPlatform } from '../../utils/platform.js'
import { getSecureStorage } from '../../utils/secureStorage/index.js'
import { getInitialSettings } from '../../utils/settings/settings.js'
import { jsonParse } from '../../utils/slowOperations.js'
import { buildRedirectUri, findAvailablePort } from './oauthPort.js'

export function isXaaEnabled(): boolean {
  return isEnvTruthy(process.env.CLAUDE_CODE_ENABLE_XAA)
}

export type XaaIdpSettings = {
  issuer: string
  clientId: string
  callbackPort?: number
}

/**
 * Typed accessor for settings.xaaIdp. The field is env-gated in SettingsSchema
 * so it doesn't surface in SDK types/docs — which means the inferred settings
 * type doesn't have it at compile time. This is the one cast.
 */
export function getXaaIdpSettings(): XaaIdpSettings | undefined {
  return (getInitialSettings() as { xaaIdp?: XaaIdpSettings }).xaaIdp
}


```

---


### `src/services/mcpServerApproval.tsx`

**信息:**
- 行数: 41
- 大小: 6400 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { MCPServerApprovalDialog } from '../components/MCPServerApprovalDialog.js';
import { MCPServerMultiselectDialog } from '../components/MCPServerMultiselectDialog.js';
import type { Root } from '../ink.js';
import { KeybindingSetup } from '../keybindings/KeybindingProviderSetup.js';
import { AppStateProvider } from '../state/AppState.js';
import { getMcpConfigsByScope } from './mcp/config.js';
import { getProjectMcpServerStatus } from './mcp/utils.js';

/**
 * Show MCP server approval dialogs for pending project servers.
 * Uses the provided Ink root to render (reusing the existing instance
 * from main.tsx instead of creating a separate one).
 */
export async function handleMcpjsonServerApprovals(root: Root): Promise<void> {
  const {
    servers: projectServers
  } = getMcpConfigsByScope('project');
  const pendingServers = Object.keys(projectServers).filter(serverName => getProjectMcpServerStatus(serverName) === 'pending');
  if (pendingServers.length === 0) {
    return;
  }
  await new Promise<void>(resolve => {
    const done = (): void => void resolve();
    if (pendingServers.length === 1 && pendingServers[0] !== undefined) {
      const serverName = pendingServers[0];
      root.render(<AppStateProvider>
          <KeybindingSetup>
            <MCPServerApprovalDialog serverName={serverName} onDone={done} />
          </KeybindingSetup>
        </AppStateProvider>);
    } else {
      root.render(<AppStateProvider>
          <KeybindingSetup>
            <MCPServerMultiselectDialog serverNames={pendingServers} onDone={done} />
          </KeybindingSetup>
        </AppStateProvider>);
    }
  });
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIk1DUFNlcnZlckFwcHJvdmFsRGlhbG9nIiwiTUNQU2VydmVyTXVsdGlzZWxlY3REaWFsb2ciLCJSb290IiwiS2V5YmluZGluZ1NldHVwIiwiQXBwU3RhdGVQcm92aWRlciIsImdldE1jcENvbmZpZ3NCeVNjb3BlIiwiZ2V0UHJvamVjdE1jcFNlcnZlclN0YXR1cyIsImhhbmRsZU1jcGpzb25TZXJ2ZXJBcHByb3ZhbHMiLCJyb290IiwiUHJvbWlzZSIsInNlcnZlcnMiLCJwcm9qZWN0U2VydmVycyIsInBlbmRpbmdTZXJ2ZXJzIiwiT2JqZWN0Iiwia2V5cyIsImZpbHRlciIsInNlcnZlck5hbWUiLCJsZW5ndGgiLCJyZXNvbHZlIiwiZG9uZSIsInVuZGVmaW5lZCIsInJlbmRlciJdLCJzb3VyY2VzIjpbIm1jcFNlcnZlckFwcHJvdmFsLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBNQ1BTZXJ2ZXJBcHByb3ZhbERpYWxvZyB9IGZyb20gJy4uL2NvbXBvbmVudHMvTUNQU2VydmVyQXBwcm92YWxEaWFsb2cuanMnXG5pbXBvcnQgeyBNQ1BTZXJ2ZXJNdWx0aXNlbGVjdERpYWxvZyB9IGZyb20gJy4uL2NvbXBvbmVudHMvTUNQU2VydmVyTXVsdGlzZWxlY3REaWFsb2cuanMnXG5pbXBvcnQgdHlwZSB7IFJvb3QgfSBmcm9tICcuLi9pbmsuanMnXG5pbXBvcnQgeyBLZXliaW5kaW5nU2V0dXAgfSBmcm9tICcuLi9rZXliaW5kaW5ncy9LZXliaW5kaW5nUHJvdmlkZXJTZXR1cC5qcydcbmltcG9ydCB7IEFwcFN0YXRlUHJvdmlkZXIgfSBmcm9tICcuLi9zdGF0ZS9BcHBTdGF0ZS5qcydcbmltcG9ydCB7IGdldE1jcENvbmZpZ3NCeVNjb3BlIH0gZnJvbSAnLi9tY3AvY29uZmlnLmpzJ1xuaW1wb3J0IHsgZ2V0UHJvamVjdE1jcFNlcnZlclN0YXR1cyB9IGZyb20gJy4vbWNwL3V0aWxzLmpzJ1xuXG4vKipcbiAqIFNob3cgTUNQIHNlcnZlciBhcHByb3ZhbCBkaWFsb2dzIGZvciBwZW5kaW5nIHByb2plY3Qgc2VydmVycy5cbiAqIFVzZXMgdGhlIHByb3ZpZGVkIEluayByb290IHRvIHJlbmRlciAocmV1c2luZyB0aGUgZXhpc3RpbmcgaW5zdGFuY2VcbiAqIGZyb20gbWFpbi50c3ggaW5zdGVhZCBvZiBjcmVhdGluZyBhIHNlcGFyYXRlIG9uZSkuXG4gKi9cbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBoYW5kbGVNY3Bqc29uU2VydmVyQXBwcm92YWxzKHJvb3Q6IFJvb3QpOiBQcm9taXNlPHZvaWQ+IHtcbiAgY29uc3QgeyBzZXJ2ZXJzOiBwcm9qZWN0U2VydmVycyB9ID0gZ2V0TWNwQ29uZmlnc0J5U2NvcGUoJ3Byb2plY3QnKVxuICBjb25zdCBwZW5kaW5nU2VydmVycyA9IE9iamVjdC5rZXlzKHByb2plY3RTZXJ2ZXJzKS5maWx0ZXIoXG4gICAgc2VydmVyTmFtZSA9PiBnZXRQcm9qZWN0TWNwU2VydmVyU3RhdHVzKHNlcnZlck5hbWUpID09PSAncGVuZGluZycsXG4gIClcblxuICBpZiAocGVuZGluZ1NlcnZlcnMubGVuZ3RoID09PSAwKSB7XG4gICAgcmV0dXJuXG4gIH1cblxuICBhd2FpdCBuZXcgUHJvbWlzZTx2b2lkPihyZXNvbHZlID0+IHtcbiAgICBjb25zdCBkb25lID0gKCk6IHZvaWQgPT4gdm9pZCByZXNvbHZlKClcbiAgICBpZiAocGVuZGluZ1NlcnZlcnMubGVuZ3RoID09PSAxICYmIHBlbmRpbmdTZXJ2ZXJzWzBdICE9PSB1bmRlZmluZWQpIHtcbiAgICAgIGNvbnN0IHNlcnZlck5hbWUgPSBwZW5kaW5nU2VydmVyc1swXVxuICAgICAgcm9vdC5yZW5kZXIoXG4gICAgICAgIDxBcHBTdGF0ZVByb3ZpZGVyPlxuICAgICAgICAgIDxLZXliaW5kaW5nU2V0dXA+XG4gICAgICAgICAgICA8TUNQU2VydmVyQXBwcm92YWxEaWFsb2cgc2VydmVyTmFtZT17c2VydmVyTmFtZX0gb25Eb25lPXtkb25lfSAvPlxuICAgICAgICAgIDwvS2V5YmluZGluZ1NldHVwPlxuICAgICAgICA8L0FwcFN0YXRlUHJvdmlkZXI+LFxuICAgICAgKVxuICAgIH0gZWxzZSB7XG4gICAgICByb290LnJlbmRlcihcbiAgICAgICAgPEFwcFN0YXRlUHJvdmlkZXI+XG4gICAgICAgICAgPEtleWJpbmRpbmdTZXR1cD5cbiAgICAgICAgICAgIDxNQ1BTZXJ2ZXJNdWx0aXNlbGVjdERpYWxvZ1xuICAgICAgICAgICAgICBzZXJ2ZXJOYW1lcz17cGVuZGluZ1NlcnZlcnN9XG4gICAgICAgICAgICAgIG9uRG9uZT17ZG9uZX1cbiAgICAgICAgICAgIC8+XG4gICAgICAgICAgPC9LZXliaW5kaW5nU2V0dXA+XG4gICAgICAgIDwvQXBwU3RhdGVQcm92aWRlcj4sXG4gICAgICApXG4gICAgfVxuICB9KVxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPQSxLQUFLLE1BQU0sT0FBTztBQUN6QixTQUFTQyx1QkFBdUIsUUFBUSwwQ0FBMEM7QUFDbEYsU0FBU0MsMEJBQTBCLFFBQVEsNkNBQTZDO0FBQ3hGLGNBQWNDLElBQUksUUFBUSxXQUFXO0FBQ3JDLFNBQVNDLGVBQWUsUUFBUSwyQ0FBMkM7QUFDM0UsU0FBU0MsZ0JBQWdCLFFBQVEsc0JBQXNCO0FBQ3ZELFNBQVNDLG9CQUFvQixRQUFRLGlCQUFpQjtBQUN0RCxTQUFTQyx5QkFBeUIsUUFBUSxnQkFBZ0I7O0FBRTFEO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxPQUFPLGVBQWVDLDRCQUE0QkEsQ0FBQ0MsSUFBSSxFQUFFTixJQUFJLENBQUMsRUFBRU8sT0FBTyxDQUFDLElBQUksQ0FBQyxDQUFDO0VBQzVFLE1BQU07SUFBRUMsT0FBTyxFQUFFQztFQUFlLENBQUMsR0FBR04sb0JBQW9CLENBQUMsU0FBUyxDQUFDO0VBQ25FLE1BQU1PLGNBQWMsR0FBR0MsTUFBTSxDQUFDQyxJQUFJLENBQUNILGNBQWMsQ0FBQyxDQUFDSSxNQUFNLENBQ3ZEQyxVQUFVLElBQUlWLHlCQUF5QixDQUFDVSxVQUFVLENBQUMsS0FBSyxTQUMxRCxDQUFDO0VBRUQsSUFBSUosY0FBYyxDQUFDSyxNQUFNLEtBQUssQ0FBQyxFQUFFO0lBQy9CO0VBQ0Y7RUFFQSxNQUFNLElBQUlSLE9BQU8sQ0FBQyxJQUFJLENBQUMsQ0FBQ1MsT0FBTyxJQUFJO0lBQ2pDLE1BQU1DLElBQUksR0FBR0EsQ0FBQSxDQUFFLEVBQUUsSUFBSSxJQUFJLEtBQUtELE9BQU8sQ0FBQyxDQUFDO0lBQ3ZDLElBQUlOLGNBQWMsQ0FBQ0ssTUFBTSxLQUFLLENBQUMsSUFBSUwsY0FBYyxDQUFDLENBQUMsQ0FBQyxLQUFLUSxTQUFTLEVBQUU7TUFDbEUsTUFBTUosVUFBVSxHQUFHSixjQUFjLENBQUMsQ0FBQyxDQUFDO01BQ3BDSixJQUFJLENBQUNhLE1BQU0sQ0FDVCxDQUFDLGdCQUFnQjtBQUN6QixVQUFVLENBQUMsZUFBZTtBQUMxQixZQUFZLENBQUMsdUJBQXVCLENBQUMsVUFBVSxDQUFDLENBQUNMLFVBQVUsQ0FBQyxDQUFDLE1BQU0sQ0FBQyxDQUFDRyxJQUFJLENBQUM7QUFDMUUsVUFBVSxFQUFFLGVBQWU7QUFDM0IsUUFBUSxFQUFFLGdCQUFnQixDQUNwQixDQUFDO0lBQ0gsQ0FBQyxNQUFNO01BQ0xYLElBQUksQ0FBQ2EsTUFBTSxDQUNULENBQUMsZ0JBQWdCO0FBQ3pCLFVBQVUsQ0FBQyxlQUFlO0FBQzFCLFlBQVksQ0FBQywwQkFBMEIsQ0FDekIsV0FBVyxDQUFDLENBQUNULGNBQWMsQ0FBQyxDQUM1QixNQUFNLENBQUMsQ0FBQ08sSUFBSSxDQUFDO0FBRTNCLFVBQVUsRUFBRSxlQUFlO0FBQzNCLFFBQVEsRUFBRSxnQkFBZ0IsQ0FDcEIsQ0FBQztJQUNIO0VBQ0YsQ0FBQyxDQUFDO0FBQ0oiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/services/mockRateLimits.ts`

**信息:**
- 行数: 882
- 大小: 29698 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Mock rate limits for testing [ANT-ONLY]
// This allows testing various rate limit scenarios without hitting actual limits
//
// ⚠️  WARNING: This is for internal testing/demo purposes only!
// The mock headers may not exactly match the API specification or real-world behavior.
// Always validate against actual API responses before relying on this for production features.

import type { SubscriptionType } from '../services/oauth/types.js'
import { setMockBillingAccessOverride } from '../utils/billing.js'
import type { OverageDisabledReason } from './claudeAiLimits.js'

type MockHeaders = {
  'anthropic-ratelimit-unified-status'?:
    | 'allowed'
    | 'allowed_warning'
    | 'rejected'
  'anthropic-ratelimit-unified-reset'?: string
  'anthropic-ratelimit-unified-representative-claim'?:
    | 'five_hour'
    | 'seven_day'
    | 'seven_day_opus'
    | 'seven_day_sonnet'
  'anthropic-ratelimit-unified-overage-status'?:
    | 'allowed'
    | 'allowed_warning'
    | 'rejected'
  'anthropic-ratelimit-unified-overage-reset'?: string
  'anthropic-ratelimit-unified-overage-disabled-reason'?: OverageDisabledReason
  'anthropic-ratelimit-unified-fallback'?: 'available'
  'anthropic-ratelimit-unified-fallback-percentage'?: string
  'retry-after'?: string
  // Early warning utilization headers
  'anthropic-ratelimit-unified-5h-utilization'?: string
  'anthropic-ratelimit-unified-5h-reset'?: string
  'anthropic-ratelimit-unified-5h-surpassed-threshold'?: string
  'anthropic-ratelimit-unified-7d-utilization'?: string
  'anthropic-ratelimit-unified-7d-reset'?: string
  'anthropic-ratelimit-unified-7d-surpassed-threshold'?: string
  'anthropic-ratelimit-unified-overage-utilization'?: string
  'anthropic-ratelimit-unified-overage-surpassed-threshold'?: string
}

export type MockHeaderKey =
  | 'status'
  | 'reset'
  | 'claim'
  | 'overage-status'
  | 'overage-reset'
  | 'overage-disabled-reason'
  | 'fallback'

```

---


### `src/services/notifier.ts`

**信息:**
- 行数: 156
- 大小: 4256 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { TerminalNotification } from '../ink/useTerminalNotification.js'
import { getGlobalConfig } from '../utils/config.js'
import { env } from '../utils/env.js'
import { execFileNoThrow } from '../utils/execFileNoThrow.js'
import { executeNotificationHooks } from '../utils/hooks.js'
import { logError } from '../utils/log.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from './analytics/index.js'

export type NotificationOptions = {
  message: string
  title?: string
  notificationType: string
}

export async function sendNotification(
  notif: NotificationOptions,
  terminal: TerminalNotification,
): Promise<void> {
  const config = getGlobalConfig()
  const channel = config.preferredNotifChannel

  await executeNotificationHooks(notif)

  const methodUsed = await sendToChannel(channel, notif, terminal)

  logEvent('tengu_notification_method_used', {
    configured_channel:
      channel as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
    method_used:
      methodUsed as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
    term: env.terminal as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  })
}

const DEFAULT_TITLE = 'Claude Code'

async function sendToChannel(
  channel: string,
  opts: NotificationOptions,
  terminal: TerminalNotification,
): Promise<string> {
  const title = opts.title || DEFAULT_TITLE

  try {
    switch (channel) {
      case 'auto':
        return sendAuto(opts, terminal)

```

---


### `src/services/oauth/auth-code-listener.ts`

**信息:**
- 行数: 211
- 大小: 6650 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { IncomingMessage, ServerResponse } from 'http'
import { createServer, type Server } from 'http'
import type { AddressInfo } from 'net'
import { logEvent } from 'src/services/analytics/index.js'
import { getOauthConfig } from '../../constants/oauth.js'
import { logError } from '../../utils/log.js'
import { shouldUseClaudeAIAuth } from './client.js'

/**
 * Temporary localhost HTTP server that listens for OAuth authorization code redirects.
 *
 * When the user authorizes in their browser, the OAuth provider redirects to:
 * http://localhost:[port]/callback?code=AUTH_CODE&state=STATE
 *
 * This server captures that redirect and extracts the auth code.
 * Note: This is NOT an OAuth server - it's just a redirect capture mechanism.
 */
export class AuthCodeListener {
  private localServer: Server
  private port: number = 0
  private promiseResolver: ((authorizationCode: string) => void) | null = null
  private promiseRejecter: ((error: Error) => void) | null = null
  private expectedState: string | null = null // State parameter for CSRF protection
  private pendingResponse: ServerResponse | null = null // Response object for final redirect
  private callbackPath: string // Configurable callback path

  constructor(callbackPath: string = '/callback') {
    this.localServer = createServer()
    this.callbackPath = callbackPath
  }

  /**
   * Starts listening on an OS-assigned port and returns the port number.
   * This avoids race conditions by keeping the server open until it's used.
   * @param port Optional specific port to use. If not provided, uses OS-assigned port.
   */
  async start(port?: number): Promise<number> {
    return new Promise((resolve, reject) => {
      this.localServer.once('error', err => {
        reject(
          new Error(`Failed to start OAuth callback server: ${err.message}`),
        )
      })

      // Listen on specified port or 0 to let the OS assign an available port
      this.localServer.listen(port ?? 0, 'localhost', () => {
        const address = this.localServer.address() as AddressInfo
        this.port = address.port
        resolve(this.port)
      })

```

---


### `src/services/oauth/client.ts`

**信息:**
- 行数: 577
- 大小: 18647 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// OAuth client for handling authentication flows with Claude services
import axios from 'axios'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from 'src/services/analytics/index.js'
import {
  ALL_OAUTH_SCOPES,
  CLAUDE_AI_INFERENCE_SCOPE,
  CLAUDE_AI_OAUTH_SCOPES,
  getOauthConfig,
} from '../../constants/oauth.js'
import {
  checkAndRefreshOAuthTokenIfNeeded,
  getClaudeAIOAuthTokens,
  hasProfileScope,
  isClaudeAISubscriber,
  saveApiKey,
} from '../../utils/auth.js'
import type { AccountInfo } from '../../utils/config.js'
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js'
import { logForDebugging } from '../../utils/debug.js'
import { getOauthProfileFromOauthToken } from './getOauthProfile.js'
import type {
  BillingType,
  OAuthProfileResponse,
  OAuthTokenExchangeResponse,
  OAuthTokens,
  RateLimitTier,
  SubscriptionType,
  UserRolesResponse,
} from './types.js'

/**
 * Check if the user has Claude.ai authentication scope
 * @private Only call this if you're OAuth / auth related code!
 */
export function shouldUseClaudeAIAuth(scopes: string[] | undefined): boolean {
  return Boolean(scopes?.includes(CLAUDE_AI_INFERENCE_SCOPE))
}

export function parseScopes(scopeString?: string): string[] {
  return scopeString?.split(' ').filter(Boolean) ?? []
}

export function buildAuthUrl({
  codeChallenge,
  state,
  port,
  isManual,

```

---


### `src/services/oauth/crypto.ts`

**信息:**
- 行数: 23
- 大小: 566 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { createHash, randomBytes } from 'crypto'

function base64URLEncode(buffer: Buffer): string {
  return buffer
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '')
}

export function generateCodeVerifier(): string {
  return base64URLEncode(randomBytes(32))
}

export function generateCodeChallenge(verifier: string): string {
  const hash = createHash('sha256')
  hash.update(verifier)
  return base64URLEncode(hash.digest())
}

export function generateState(): string {
  return base64URLEncode(randomBytes(32))
}

```

---


### `src/services/oauth/getOauthProfile.ts`

**信息:**
- 行数: 53
- 大小: 1611 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { getOauthConfig, OAUTH_BETA_HEADER } from 'src/constants/oauth.js'
import type { OAuthProfileResponse } from 'src/services/oauth/types.js'
import { getAnthropicApiKey } from 'src/utils/auth.js'
import { getGlobalConfig } from 'src/utils/config.js'
import { logError } from 'src/utils/log.js'
export async function getOauthProfileFromApiKey(): Promise<
  OAuthProfileResponse | undefined
> {
  // Assumes interactive session
  const config = getGlobalConfig()
  const accountUuid = config.oauthAccount?.accountUuid
  const apiKey = getAnthropicApiKey()

  // Need both account UUID and API key to check
  if (!accountUuid || !apiKey) {
    return
  }
  const endpoint = `${getOauthConfig().BASE_API_URL}/api/claude_cli_profile`
  try {
    const response = await axios.get<OAuthProfileResponse>(endpoint, {
      headers: {
        'x-api-key': apiKey,
        'anthropic-beta': OAUTH_BETA_HEADER,
      },
      params: {
        account_uuid: accountUuid,
      },
      timeout: 10000,
    })
    return response.data
  } catch (error) {
    logError(error as Error)
  }
}

export async function getOauthProfileFromOauthToken(
  accessToken: string,
): Promise<OAuthProfileResponse | undefined> {
  const endpoint = `${getOauthConfig().BASE_API_URL}/api/oauth/profile`
  try {
    const response = await axios.get<OAuthProfileResponse>(endpoint, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      timeout: 10000,
    })
    return response.data
  } catch (error) {

```

---


### `src/services/oauth/index.ts`

**信息:**
- 行数: 198
- 大小: 6554 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { logEvent } from 'src/services/analytics/index.js'
import { openBrowser } from '../../utils/browser.js'
import { AuthCodeListener } from './auth-code-listener.js'
import * as client from './client.js'
import * as crypto from './crypto.js'
import type {
  OAuthProfileResponse,
  OAuthTokenExchangeResponse,
  OAuthTokens,
  RateLimitTier,
  SubscriptionType,
} from './types.js'

/**
 * OAuth service that handles the OAuth 2.0 authorization code flow with PKCE.
 *
 * Supports two ways to get authorization codes:
 * 1. Automatic: Opens browser, redirects to localhost where we capture the code
 * 2. Manual: User manually copies and pastes the code (used in non-browser environments)
 */
export class OAuthService {
  private codeVerifier: string
  private authCodeListener: AuthCodeListener | null = null
  private port: number | null = null
  private manualAuthCodeResolver: ((authorizationCode: string) => void) | null =
    null

  constructor() {
    this.codeVerifier = crypto.generateCodeVerifier()
  }

  async startOAuthFlow(
    authURLHandler: (url: string, automaticUrl?: string) => Promise<void>,
    options?: {
      loginWithClaudeAi?: boolean
      inferenceOnly?: boolean
      expiresIn?: number
      orgUUID?: string
      loginHint?: string
      loginMethod?: string
      /**
       * Don't call openBrowser(). Caller takes both URLs via authURLHandler
       * and decides how/where to open them. Used by the SDK control protocol
       * (claude_authenticate) where the SDK client owns the user's display,
       * not this process.
       */
      skipBrowserOpen?: boolean
    },
  ): Promise<OAuthTokens> {
    // Create OAuth callback listener and start it

```

---


### `src/services/oauth/types.ts`

**信息:**
- 行数: 13
- 大小: 443 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type OAuthTokens = {
  accessToken?: string
  refreshToken?: string
  expiresAt?: number
  [key: string]: unknown
}

export type SubscriptionType = string
export type BillingType = string
export type OAuthProfileResponse = Record<string, unknown>
export type ReferralEligibilityResponse = Record<string, unknown>
export type ReferralRedemptionsResponse = Record<string, unknown>
export type ReferrerRewardInfo = Record<string, unknown>

```

---


### `src/services/plugins/PluginInstallationManager.ts`

**信息:**
- 行数: 184
- 大小: 6017 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Background plugin and marketplace installation manager
 *
 * This module handles automatic installation of plugins and marketplaces
 * from trusted sources (repository and user settings) without blocking startup.
 */

import type { AppState } from '../../state/AppState.js'
import { logForDebugging } from '../../utils/debug.js'
import { logForDiagnosticsNoPII } from '../../utils/diagLogs.js'
import { logError } from '../../utils/log.js'
import {
  clearMarketplacesCache,
  getDeclaredMarketplaces,
  loadKnownMarketplacesConfig,
} from '../../utils/plugins/marketplaceManager.js'
import { clearPluginCache } from '../../utils/plugins/pluginLoader.js'
import {
  diffMarketplaces,
  reconcileMarketplaces,
} from '../../utils/plugins/reconciler.js'
import { refreshActivePlugins } from '../../utils/plugins/refresh.js'
import { logEvent } from '../analytics/index.js'

type SetAppState = (f: (prevState: AppState) => AppState) => void

/**
 * Update marketplace installation status in app state
 */
function updateMarketplaceStatus(
  setAppState: SetAppState,
  name: string,
  status: 'pending' | 'installing' | 'installed' | 'failed',
  error?: string,
): void {
  setAppState(prevState => ({
    ...prevState,
    plugins: {
      ...prevState.plugins,
      installationStatus: {
        ...prevState.plugins.installationStatus,
        marketplaces: prevState.plugins.installationStatus.marketplaces.map(
          m => (m.name === name ? { ...m, status, error } : m),
        ),
      },
    },
  }))
}

/**

```

---


### `src/services/plugins/pluginCliCommands.ts`

**信息:**
- 行数: 344
- 大小: 10894 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * CLI command wrappers for plugin operations
 *
 * This module provides thin wrappers around the core plugin operations
 * that handle CLI-specific concerns like console output and process exit.
 *
 * For the core operations (without CLI side effects), see pluginOperations.ts
 */
import figures from 'figures'
import { errorMessage } from '../../utils/errors.js'
import { gracefulShutdown } from '../../utils/gracefulShutdown.js'
import { logError } from '../../utils/log.js'
import { getManagedPluginNames } from '../../utils/plugins/managedPlugins.js'
import { parsePluginIdentifier } from '../../utils/plugins/pluginIdentifier.js'
import type { PluginScope } from '../../utils/plugins/schemas.js'
import { writeToStdout } from '../../utils/process.js'
import {
  buildPluginTelemetryFields,
  classifyPluginCommandError,
} from '../../utils/telemetry/pluginTelemetry.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_PII_TAGGED,
  logEvent,
} from '../analytics/index.js'
import {
  disableAllPluginsOp,
  disablePluginOp,
  enablePluginOp,
  type InstallableScope,
  installPluginOp,
  uninstallPluginOp,
  updatePluginOp,
  VALID_INSTALLABLE_SCOPES,
  VALID_UPDATE_SCOPES,
} from './pluginOperations.js'

export { VALID_INSTALLABLE_SCOPES, VALID_UPDATE_SCOPES }

type PluginCliCommand =
  | 'install'
  | 'uninstall'
  | 'enable'
  | 'disable'
  | 'disable-all'
  | 'update'

/**
 * Generic error handler for plugin CLI commands. Emits
 * tengu_plugin_command_failed before exit so dashboards can compute a

```

---


### `src/services/plugins/pluginOperations.ts`

**信息:**
- 行数: 1088
- 大小: 35619 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Core plugin operations (install, uninstall, enable, disable, update)
 *
 * This module provides pure library functions that can be used by both:
 * - CLI commands (`claude plugin install/uninstall/enable/disable/update`)
 * - Interactive UI (ManagePlugins.tsx)
 *
 * Functions in this module:
 * - Do NOT call process.exit()
 * - Do NOT write to console
 * - Return result objects indicating success/failure with messages
 * - Can throw errors for unexpected failures
 */
import { dirname, join } from 'path'
import { getOriginalCwd } from '../../bootstrap/state.js'
import { isBuiltinPluginId } from '../../plugins/builtinPlugins.js'
import type { LoadedPlugin, PluginManifest } from '../../types/plugin.js'
import { isENOENT, toError } from '../../utils/errors.js'
import { getFsImplementation } from '../../utils/fsOperations.js'
import { logError } from '../../utils/log.js'
import {
  clearAllCaches,
  markPluginVersionOrphaned,
} from '../../utils/plugins/cacheUtils.js'
import {
  findReverseDependents,
  formatReverseDependentsSuffix,
} from '../../utils/plugins/dependencyResolver.js'
import {
  loadInstalledPluginsFromDisk,
  loadInstalledPluginsV2,
  removePluginInstallation,
  updateInstallationPathOnDisk,
} from '../../utils/plugins/installedPluginsManager.js'
import {
  getMarketplace,
  getPluginById,
  loadKnownMarketplacesConfig,
} from '../../utils/plugins/marketplaceManager.js'
import { deletePluginDataDir } from '../../utils/plugins/pluginDirectories.js'
import {
  parsePluginIdentifier,
  scopeToSettingSource,
} from '../../utils/plugins/pluginIdentifier.js'
import {
  formatResolutionError,
  installResolvedPlugin,
} from '../../utils/plugins/pluginInstallationHelpers.js'
import {
  cachePlugin,

```

---


### `src/services/policyLimits/index.ts`

**信息:**
- 行数: 663
- 大小: 18064 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Policy Limits Service
 *
 * Fetches organization-level policy restrictions from the API and uses them
 * to disable CLI features. Follows the same patterns as remote managed settings
 * (fail open, ETag caching, background polling, retry logic).
 *
 * Eligibility:
 * - Console users (API key): All eligible
 * - OAuth users (Claude.ai): Only Team and Enterprise/C4E subscribers are eligible
 * - API fails open (non-blocking) - if fetch fails, continues without restrictions
 * - API returns empty restrictions for users without policy limits
 */

import axios from 'axios'
import { createHash } from 'crypto'
import { readFileSync as fsReadFileSync } from 'fs'
import { unlink, writeFile } from 'fs/promises'
import { join } from 'path'
import {
  CLAUDE_AI_INFERENCE_SCOPE,
  getOauthConfig,
  OAUTH_BETA_HEADER,
} from '../../constants/oauth.js'
import {
  checkAndRefreshOAuthTokenIfNeeded,
  getAnthropicApiKeyWithSource,
  getClaudeAIOAuthTokens,
} from '../../utils/auth.js'
import { registerCleanup } from '../../utils/cleanupRegistry.js'
import { logForDebugging } from '../../utils/debug.js'
import { getClaudeConfigHomeDir } from '../../utils/envUtils.js'
import { classifyAxiosError } from '../../utils/errors.js'
import { safeParseJSON } from '../../utils/json.js'
import {
  getAPIProvider,
  isFirstPartyAnthropicBaseUrl,
} from '../../utils/model/providers.js'
import { isEssentialTrafficOnly } from '../../utils/privacyLevel.js'
import { sleep } from '../../utils/sleep.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { getClaudeCodeUserAgent } from '../../utils/userAgent.js'
import { getRetryDelay } from '../api/withRetry.js'
import {
  type PolicyLimitsFetchResult,
  type PolicyLimitsResponse,
  PolicyLimitsResponseSchema,
} from './types.js'

function isNodeError(e: unknown): e is NodeJS.ErrnoException {

```

---


### `src/services/policyLimits/types.ts`

**信息:**
- 行数: 27
- 大小: 792 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'

/**
 * Schema for the policy limits API response
 * Only blocked policies are included. If a policy key is absent, it's allowed.
 */
export const PolicyLimitsResponseSchema = lazySchema(() =>
  z.object({
    restrictions: z.record(z.string(), z.object({ allowed: z.boolean() })),
  }),
)

export type PolicyLimitsResponse = z.infer<
  ReturnType<typeof PolicyLimitsResponseSchema>
>

/**
 * Result of fetching policy limits
 */
export type PolicyLimitsFetchResult = {
  success: boolean
  restrictions?: PolicyLimitsResponse['restrictions'] | null // null means 304 Not Modified (cache is valid)
  etag?: string
  error?: string
  skipRetry?: boolean // If true, don't retry on failure (e.g., auth errors)
}

```

---


### `src/services/preventSleep.ts`

**信息:**
- 行数: 165
- 大小: 4586 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Prevents macOS from sleeping while Claude is working.
 *
 * Uses the built-in `caffeinate` command to create a power assertion that
 * prevents idle sleep. This keeps the Mac awake during API requests and
 * tool execution so long-running operations don't get interrupted.
 *
 * The caffeinate process is spawned with a timeout and periodically restarted.
 * This provides self-healing behavior: if the Node process is killed with
 * SIGKILL (which doesn't run cleanup handlers), the orphaned caffeinate will
 * automatically exit after the timeout expires.
 *
 * Only runs on macOS - no-op on other platforms.
 */
import { type ChildProcess, spawn } from 'child_process'
import { registerCleanup } from '../utils/cleanupRegistry.js'
import { logForDebugging } from '../utils/debug.js'

// Caffeinate timeout in seconds. Process auto-exits after this duration.
// We restart it before expiry to maintain continuous sleep prevention.
const CAFFEINATE_TIMEOUT_SECONDS = 300 // 5 minutes

// Restart interval - restart caffeinate before it expires.
// Use 4 minutes to give plenty of buffer before the 5 minute timeout.
const RESTART_INTERVAL_MS = 4 * 60 * 1000

let caffeinateProcess: ChildProcess | null = null
let restartInterval: ReturnType<typeof setInterval> | null = null
let refCount = 0
let cleanupRegistered = false

/**
 * Increment the reference count and start preventing sleep if needed.
 * Call this when starting work that should keep the Mac awake.
 */
export function startPreventSleep(): void {
  refCount++

  if (refCount === 1) {
    spawnCaffeinate()
    startRestartInterval()
  }
}

/**
 * Decrement the reference count and allow sleep if no more work is pending.
 * Call this when work completes.
 */
export function stopPreventSleep(): void {
  if (refCount > 0) {

```

---


### `src/services/rateLimitMessages.ts`

**信息:**
- 行数: 344
- 大小: 10858 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Centralized rate limit message generation
 * Single source of truth for all rate limit-related messages
 */

import {
  getOauthAccountInfo,
  getSubscriptionType,
  isOverageProvisioningAllowed,
} from '../utils/auth.js'
import { hasClaudeAiBillingAccess } from '../utils/billing.js'
import { formatResetTime } from '../utils/format.js'
import type { ClaudeAILimits } from './claudeAiLimits.js'

const FEEDBACK_CHANNEL_ANT = '#briarpatch-cc'

/**
 * All possible rate limit error message prefixes
 * Export this to avoid fragile string matching in UI components
 */
export const RATE_LIMIT_ERROR_PREFIXES = [
  "You've hit your",
  "You've used",
  "You're now using extra usage",
  "You're close to",
  "You're out of extra usage",
] as const

/**
 * Check if a message is a rate limit error
 */
export function isRateLimitErrorMessage(text: string): boolean {
  return RATE_LIMIT_ERROR_PREFIXES.some(prefix => text.startsWith(prefix))
}

export type RateLimitMessage = {
  message: string
  severity: 'error' | 'warning'
}

/**
 * Get the appropriate rate limit message based on limit state
 * Returns null if no message should be shown
 */
export function getRateLimitMessage(
  limits: ClaudeAILimits,
  model: string,
): RateLimitMessage | null {
  // Check overage scenarios first (when subscription is rejected but overage is available)
  // getUsingOverageText is rendered separately from warning.

```

---


### `src/services/rateLimitMocking.ts`

**信息:**
- 行数: 144
- 大小: 4420 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Facade for rate limit header processing
 * This isolates mock logic from production code
 */

import { APIError } from '@anthropic-ai/sdk'
import {
  applyMockHeaders,
  checkMockFastModeRateLimit,
  getMockHeaderless429Message,
  getMockHeaders,
  isMockFastModeRateLimitScenario,
  shouldProcessMockLimits,
} from './mockRateLimits.js'

/**
 * Process headers, applying mocks if /mock-limits command is active
 */
export function processRateLimitHeaders(
  headers: globalThis.Headers,
): globalThis.Headers {
  // Only apply mocks for Ant employees using /mock-limits command
  if (shouldProcessMockLimits()) {
    return applyMockHeaders(headers)
  }
  return headers
}

/**
 * Check if we should process rate limits (either real subscriber or /mock-limits command)
 */
export function shouldProcessRateLimits(isSubscriber: boolean): boolean {
  return isSubscriber || shouldProcessMockLimits()
}

/**
 * Check if mock rate limits should throw a 429 error
 * Returns the error to throw, or null if no error should be thrown
 * @param currentModel The model being used for the current request
 * @param isFastModeActive Whether fast mode is currently active (for fast-mode-only mocks)
 */
export function checkMockRateLimitError(
  currentModel: string,
  isFastModeActive?: boolean,
): APIError | null {
  if (!shouldProcessMockLimits()) {
    return null
  }

  const headerlessMessage = getMockHeaderless429Message()

```

---


### `src/services/remoteManagedSettings/index.ts`

**信息:**
- 行数: 638
- 大小: 20911 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Remote Managed Settings Service
 *
 * Manages fetching, caching, and validation of remote-managed settings
 * for enterprise customers. Uses checksum-based validation to minimize
 * network traffic and provides graceful degradation on failures.
 *
 * Eligibility:
 * - Console users (API key): All eligible
 * - OAuth users (Claude.ai): Only Enterprise/C4E and Team subscribers are eligible
 * - API fails open (non-blocking) - if fetch fails, continues without remote settings
 * - API returns empty settings for users without managed settings
 */

import axios from 'axios'
import { createHash } from 'crypto'
import { open, unlink } from 'fs/promises'
import { getOauthConfig, OAUTH_BETA_HEADER } from '../../constants/oauth.js'
import {
  checkAndRefreshOAuthTokenIfNeeded,
  getAnthropicApiKeyWithSource,
  getClaudeAIOAuthTokens,
} from '../../utils/auth.js'
import { registerCleanup } from '../../utils/cleanupRegistry.js'
import { logForDebugging } from '../../utils/debug.js'
import { classifyAxiosError, getErrnoCode } from '../../utils/errors.js'
import { settingsChangeDetector } from '../../utils/settings/changeDetector.js'
import {
  type SettingsJson,
  SettingsSchema,
} from '../../utils/settings/types.js'
import { sleep } from '../../utils/sleep.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { getClaudeCodeUserAgent } from '../../utils/userAgent.js'
import { getRetryDelay } from '../api/withRetry.js'
import {
  checkManagedSettingsSecurity,
  handleSecurityCheckResult,
} from './securityCheck.jsx'
import { isRemoteManagedSettingsEligible, resetSyncCache } from './syncCache.js'
import {
  getRemoteManagedSettingsSyncFromCache,
  getSettingsPath,
  setSessionCache,
} from './syncCacheState.js'
import {
  type RemoteManagedSettingsFetchResult,
  RemoteManagedSettingsResponseSchema,
} from './types.js'


```

---


### `src/services/remoteManagedSettings/securityCheck.tsx`

**信息:**
- 行数: 74
- 大小: 10513 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { getIsInteractive } from '../../bootstrap/state.js';
import { ManagedSettingsSecurityDialog } from '../../components/ManagedSettingsSecurityDialog/ManagedSettingsSecurityDialog.js';
import { extractDangerousSettings, hasDangerousSettings, hasDangerousSettingsChanged } from '../../components/ManagedSettingsSecurityDialog/utils.js';
import { render } from '../../ink.js';
import { KeybindingSetup } from '../../keybindings/KeybindingProviderSetup.js';
import { AppStateProvider } from '../../state/AppState.js';
import { gracefulShutdownSync } from '../../utils/gracefulShutdown.js';
import { getBaseRenderOptions } from '../../utils/renderOptions.js';
import type { SettingsJson } from '../../utils/settings/types.js';
import { logEvent } from '../analytics/index.js';
export type SecurityCheckResult = 'approved' | 'rejected' | 'no_check_needed';

/**
 * Check if new remote managed settings contain dangerous settings that require user approval.
 * Shows a blocking dialog if dangerous settings have changed or been added.
 *
 * @param cachedSettings The current cached settings (may be null for first run)
 * @param newSettings The new settings fetched from the API
 * @returns 'approved' if user accepts, 'rejected' if user declines, 'no_check_needed' if no dangerous changes
 */
export async function checkManagedSettingsSecurity(cachedSettings: SettingsJson | null, newSettings: SettingsJson | null): Promise<SecurityCheckResult> {
  // If new settings don't have dangerous settings, no check needed
  if (!newSettings || !hasDangerousSettings(extractDangerousSettings(newSettings))) {
    return 'no_check_needed';
  }

  // If dangerous settings haven't changed, no check needed
  if (!hasDangerousSettingsChanged(cachedSettings, newSettings)) {
    return 'no_check_needed';
  }

  // Skip dialog in non-interactive mode (consistent with trust dialog behavior)
  if (!getIsInteractive()) {
    return 'no_check_needed';
  }

  // Log that dialog is being shown
  logEvent('tengu_managed_settings_security_dialog_shown', {});

  // Show blocking dialog
  return new Promise<SecurityCheckResult>(resolve => {
    void (async () => {
      const {
        unmount
      } = await render(<AppStateProvider>
          <KeybindingSetup>
            <ManagedSettingsSecurityDialog settings={newSettings} onAccept={() => {
            logEvent('tengu_managed_settings_security_dialog_accepted', {});
            unmount();

```

---


### `src/services/remoteManagedSettings/syncCache.ts`

**信息:**
- 行数: 112
- 大小: 4229 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Eligibility check for remote managed settings.
 *
 * The cache state itself lives in syncCacheState.ts (a leaf, no auth import).
 * This file keeps isRemoteManagedSettingsEligible — the one function that
 * needs auth.ts — plus resetSyncCache wrapped to clear the local eligibility
 * mirror alongside the leaf's state.
 */

import { CLAUDE_AI_INFERENCE_SCOPE } from '../../constants/oauth.js'
import {
  getAnthropicApiKeyWithSource,
  getClaudeAIOAuthTokens,
} from '../../utils/auth.js'
import {
  getAPIProvider,
  isFirstPartyAnthropicBaseUrl,
} from '../../utils/model/providers.js'

import {
  resetSyncCache as resetLeafCache,
  setEligibility,
} from './syncCacheState.js'

let cached: boolean | undefined

export function resetSyncCache(): void {
  cached = undefined
  resetLeafCache()
}

/**
 * Check if the current user is eligible for remote managed settings
 *
 * Eligibility:
 * - Console users (API key): All eligible (must have actual key, not just apiKeyHelper)
 * - OAuth users with known subscriptionType: Only Enterprise/C4E and Team
 * - OAuth users with subscriptionType === null (externally-injected tokens via
 *   CLAUDE_CODE_OAUTH_TOKEN / FD, or keychain tokens missing metadata): Eligible —
 *   the API returns empty settings for ineligible orgs, so the cost of a false
 *   positive is one round-trip
 *
 * This is a pre-check to determine if we should query the API.
 * The API will return empty settings for users without managed settings.
 *
 * IMPORTANT: This function must NOT call getSettings() or any function that calls
 * getSettings() to avoid circular dependencies during settings loading.
 */
export function isRemoteManagedSettingsEligible(): boolean {
  if (cached !== undefined) return cached

```

---


### `src/services/remoteManagedSettings/syncCacheState.ts`

**信息:**
- 行数: 96
- 大小: 4004 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Leaf state module for the remote-managed-settings sync cache.
 *
 * Split from syncCache.ts to break the settings.ts → syncCache.ts → auth.ts →
 * settings.ts cycle. auth.ts sits inside the large settings SCC; importing it
 * from settings.ts's own dependency chain pulls hundreds of modules into the
 * eagerly-evaluated SCC at startup.
 *
 * This module imports only leaves (path, envUtils, file, json, types,
 * settings/settingsCache — also a leaf, only type-imports validation). settings.ts
 * reads the cache from here. syncCache.ts keeps isRemoteManagedSettingsEligible
 * (the auth-touching part) and re-exports everything from here for callers that
 * don't care about the cycle.
 *
 * Eligibility is a tri-state here: undefined (not yet determined — return
 * null), false (ineligible — return null), true (proceed). managedEnv.ts
 * calls isRemoteManagedSettingsEligible() just before the policySettings
 * read — after userSettings/flagSettings env vars are applied, so the check
 * sees config-provided CLAUDE_CODE_USE_BEDROCK/ANTHROPIC_BASE_URL. That call
 * computes once and mirrors the result here via setEligibility(). Every
 * subsequent read hits the cached bool instead of re-running the auth chain.
 */

import { join } from 'path'
import { getClaudeConfigHomeDir } from '../../utils/envUtils.js'
import { readFileSync } from '../../utils/fileRead.js'
import { stripBOM } from '../../utils/jsonRead.js'
import { resetSettingsCache } from '../../utils/settings/settingsCache.js'
import type { SettingsJson } from '../../utils/settings/types.js'
import { jsonParse } from '../../utils/slowOperations.js'

const SETTINGS_FILENAME = 'remote-settings.json'

let sessionCache: SettingsJson | null = null
let eligible: boolean | undefined

export function setSessionCache(value: SettingsJson | null): void {
  sessionCache = value
}

export function resetSyncCache(): void {
  sessionCache = null
  eligible = undefined
}

export function setEligibility(v: boolean): boolean {
  eligible = v
  return v
}


```

---


### `src/services/remoteManagedSettings/types.ts`

**信息:**
- 行数: 31
- 大小: 1060 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'
import type { SettingsJson } from '../../utils/settings/types.js'

/**
 * Schema for the remotely managed settings response.
 * Note: Uses permissive z.record() instead of SettingsSchema to avoid circular dependency.
 * Full validation is performed in index.ts after parsing using SettingsSchema.safeParse().
 */
export const RemoteManagedSettingsResponseSchema = lazySchema(() =>
  z.object({
    uuid: z.string(), // Settings UUID
    checksum: z.string(),
    settings: z.record(z.string(), z.unknown()) as z.ZodType<SettingsJson>,
  }),
)

export type RemoteManagedSettingsResponse = z.infer<
  ReturnType<typeof RemoteManagedSettingsResponseSchema>
>

/**
 * Result of fetching remotely managed settings
 */
export type RemoteManagedSettingsFetchResult = {
  success: boolean
  settings?: SettingsJson | null // null means 304 Not Modified (cache is valid)
  checksum?: string
  error?: string
  skipRetry?: boolean // If true, don't retry on failure (e.g., auth errors)
}

```

---


### `src/services/settingsSync/index.ts`

**信息:**
- 行数: 581
- 大小: 17924 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Settings Sync Service
 *
 * Syncs user settings and memory files across Claude Code environments.
 *
 * - Interactive CLI: Uploads local settings to remote (incremental, only changed entries)
 * - CCR: Downloads remote settings to local before plugin installation
 *
 * Backend API: anthropic/anthropic#218817
 */

import { feature } from 'bun:bundle'
import axios from 'axios'
import { mkdir, readFile, stat, writeFile } from 'fs/promises'
import pickBy from 'lodash-es/pickBy.js'
import { dirname } from 'path'
import { getIsInteractive } from '../../bootstrap/state.js'
import {
  CLAUDE_AI_INFERENCE_SCOPE,
  getOauthConfig,
  OAUTH_BETA_HEADER,
} from '../../constants/oauth.js'
import {
  checkAndRefreshOAuthTokenIfNeeded,
  getClaudeAIOAuthTokens,
} from '../../utils/auth.js'
import { clearMemoryFileCaches } from '../../utils/claudemd.js'
import { getMemoryPath } from '../../utils/config.js'
import { logForDiagnosticsNoPII } from '../../utils/diagLogs.js'
import { classifyAxiosError } from '../../utils/errors.js'
import { getRepoRemoteHash } from '../../utils/git.js'
import {
  getAPIProvider,
  isFirstPartyAnthropicBaseUrl,
} from '../../utils/model/providers.js'
import { markInternalWrite } from '../../utils/settings/internalWrites.js'
import { getSettingsFilePathForSource } from '../../utils/settings/settings.js'
import { resetSettingsCache } from '../../utils/settings/settingsCache.js'
import { sleep } from '../../utils/sleep.js'
import { getClaudeCodeUserAgent } from '../../utils/userAgent.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../analytics/growthbook.js'
import { logEvent } from '../analytics/index.js'
import { getRetryDelay } from '../api/withRetry.js'
import {
  type SettingsSyncFetchResult,
  type SettingsSyncUploadResult,
  SYNC_KEYS,
  UserSyncDataSchema,
} from './types.js'


```

---


### `src/services/settingsSync/types.ts`

**信息:**
- 行数: 67
- 大小: 1668 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Settings Sync Types
 *
 * Zod schemas and types for the user settings sync API.
 * Based on the backend API contract from anthropic/anthropic#218817.
 */

import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'

/**
 * Content portion of user sync data - flat key-value storage.
 * Keys are opaque strings (typically file paths).
 * Values are UTF-8 string content (JSON, Markdown, etc).
 */
export const UserSyncContentSchema = lazySchema(() =>
  z.object({
    entries: z.record(z.string(), z.string()),
  }),
)

/**
 * Full response from GET /api/claude_code/user_settings
 */
export const UserSyncDataSchema = lazySchema(() =>
  z.object({
    userId: z.string(),
    version: z.number(),
    lastModified: z.string(), // ISO 8601 timestamp
    checksum: z.string(), // MD5 hash
    content: UserSyncContentSchema(),
  }),
)

export type UserSyncData = z.infer<ReturnType<typeof UserSyncDataSchema>>

/**
 * Result from fetching user settings
 */
export type SettingsSyncFetchResult = {
  success: boolean
  data?: UserSyncData
  isEmpty?: boolean // true if 404 (no data exists)
  error?: string
  skipRetry?: boolean
}

/**
 * Result from uploading user settings
 */

```

---


### `src/services/skillSearch/featureCheck.ts`

**信息:**
- 行数: 3
- 大小: 67 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function isSkillSearchEnabled(): boolean {
  return false
}

```

---


### `src/services/skillSearch/localSearch.ts`

**信息:**
- 行数: 3
- 大小: 57 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export async function localSkillSearch() {
  return []
}

```

---


### `src/services/skillSearch/prefetch.ts`

**信息:**
- 行数: 1
- 大小: 47 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export async function prefetchSkillSearch() {}

```

---


### `src/services/skillSearch/remoteSkillLoader.ts`

**信息:**
- 行数: 3
- 大小: 58 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export async function loadRemoteSkill() {
  return null
}

```

---


### `src/services/skillSearch/remoteSkillState.ts`

**信息:**
- 行数: 3
- 大小: 56 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function getRemoteSkillState() {
  return null
}

```

---


### `src/services/skillSearch/signals.ts`

**信息:**
- 行数: 3
- 大小: 60 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function createSkillSearchSignal() {
  return null
}

```

---


### `src/services/skillSearch/telemetry.ts`

**信息:**
- 行数: 1
- 大小: 51 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function logSkillSearchTelemetry(): void {}

```

---


### `src/services/teamMemorySync/index.ts`

**信息:**
- 行数: 1256
- 大小: 44153 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Team Memory Sync Service
 *
 * Syncs team memory files between the local filesystem and the server API.
 * Team memory is scoped per-repo (identified by git remote hash) and shared
 * across all authenticated org members.
 *
 * API contract (anthropic/anthropic#250711 + #283027):
 *   GET  /api/claude_code/team_memory?repo={owner/repo}            → TeamMemoryData (includes entryChecksums)
 *   GET  /api/claude_code/team_memory?repo={owner/repo}&view=hashes → metadata + entryChecksums only (no entry bodies)
 *   PUT  /api/claude_code/team_memory?repo={owner/repo}            → upload entries (upsert semantics)
 *   404 = no data exists yet
 *
 * Sync semantics:
 *   - Pull overwrites local files with server content (server wins per-key).
 *   - Push uploads only keys whose content hash differs from serverChecksums
 *     (delta upload). Server uses upsert: keys not in the PUT are preserved.
 *   - File deletions do NOT propagate: deleting a local file won't remove it
 *     from the server, and the next pull will restore it locally.
 *
 * State management:
 *   All mutable state (ETag tracking, watcher suppression) lives in a
 *   SyncState object created by the caller and threaded through every call.
 *   This avoids module-level mutable state and gives tests natural isolation.
 */

import axios from 'axios'
import { createHash } from 'crypto'
import { mkdir, readdir, readFile, stat, writeFile } from 'fs/promises'
import { join, relative, sep } from 'path'
import {
  CLAUDE_AI_INFERENCE_SCOPE,
  CLAUDE_AI_PROFILE_SCOPE,
  getOauthConfig,
  OAUTH_BETA_HEADER,
} from '../../constants/oauth.js'
import {
  getTeamMemPath,
  PathTraversalError,
  validateTeamMemKey,
} from '../../memdir/teamMemPaths.js'
import { count } from '../../utils/array.js'
import {
  checkAndRefreshOAuthTokenIfNeeded,
  getClaudeAIOAuthTokens,
} from '../../utils/auth.js'
import { logForDebugging } from '../../utils/debug.js'
import { classifyAxiosError } from '../../utils/errors.js'
import { getGithubRepo } from '../../utils/git.js'
import {

```

---


### `src/services/teamMemorySync/secretScanner.ts`

**信息:**
- 行数: 324
- 大小: 9458 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Client-side secret scanner for team memory (PSR M22174).
 *
 * Scans content for credentials before upload so secrets never leave the
 * user's machine. Uses a curated subset of high-confidence rules from
 * gitleaks (https://github.com/gitleaks/gitleaks, MIT license) — only
 * rules with distinctive prefixes that have near-zero false-positive
 * rates are included. Generic keyword-context rules are omitted.
 *
 * Rule IDs and regexes sourced directly from the public gitleaks config:
 * https://github.com/gitleaks/gitleaks/blob/master/config/gitleaks.toml
 *
 * JS regex notes:
 *   - gitleaks uses Go regex; inline (?i) and mode groups (?-i:...) are
 *     not portable to JS. Affected rules are rewritten with explicit
 *     character classes ([a-zA-Z0-9] instead of (?i)[a-z0-9]).
 *   - Trailing boundary alternations like (?:[\x60'"\s;]|\\[nr]|$) from
 *     Go regex are kept (JS $ matches end-of-string in default mode).
 */

import { capitalize } from '../../utils/stringUtils.js'

type SecretRule = {
  /** Gitleaks rule ID (kebab-case), used in labels and analytics */
  id: string
  /** Regex source, lazily compiled on first scan */
  source: string
  /** Optional JS regex flags (most rules are case-sensitive by default) */
  flags?: string
}

export type SecretMatch = {
  /** Gitleaks rule ID that matched (e.g., "github-pat", "aws-access-token") */
  ruleId: string
  /** Human-readable label derived from the rule ID */
  label: string
}

// ─── Curated rules ──────────────────────────────────────────────
// High-confidence patterns from gitleaks with distinctive prefixes.
// Ordered roughly by likelihood of appearing in dev-team content.

// Anthropic API key prefix, assembled at runtime so the literal byte
// sequence isn't present in the external bundle (excluded-strings check).
// join() is not constant-folded by the minifier.
const ANT_KEY_PFX = ['sk', 'ant', 'api'].join('-')

const SECRET_RULES: SecretRule[] = [
  // — Cloud providers —
  {

```

---


### `src/services/teamMemorySync/teamMemSecretGuard.ts`

**信息:**
- 行数: 44
- 大小: 1552 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'

/**
 * Check if a file write/edit to a team memory path contains secrets.
 * Returns an error message if secrets are detected, or null if safe.
 *
 * This is called from FileWriteTool and FileEditTool validateInput to
 * prevent the model from writing secrets into team memory files, which
 * would be synced to all repository collaborators.
 *
 * Callers can import and call this unconditionally — the internal
 * feature('TEAMMEM') guard keeps it inert when the build flag is off.
 * secretScanner assembles sensitive prefixes at runtime (ANT_KEY_PFX).
 */
export function checkTeamMemSecrets(
  filePath: string,
  content: string,
): string | null {
  if (feature('TEAMMEM')) {
    /* eslint-disable @typescript-eslint/no-require-imports */
    const { isTeamMemPath } =
      require('../../memdir/teamMemPaths.js') as typeof import('../../memdir/teamMemPaths.js')
    const { scanForSecrets } =
      require('./secretScanner.js') as typeof import('./secretScanner.js')
    /* eslint-enable @typescript-eslint/no-require-imports */

    if (!isTeamMemPath(filePath)) {
      return null
    }

    const matches = scanForSecrets(content)
    if (matches.length === 0) {
      return null
    }

    const labels = matches.map(m => m.label).join(', ')
    return (
      `Content contains potential secrets (${labels}) and cannot be written to team memory. ` +
      'Team memory is shared with all repository collaborators. ' +
      'Remove the sensitive content and try again.'
    )
  }
  return null
}

```

---


### `src/services/teamMemorySync/types.ts`

**信息:**
- 行数: 156
- 大小: 4906 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Team Memory Sync Types
 *
 * Zod schemas and types for the repo-scoped team memory sync API.
 * Based on the backend API contract from anthropic/anthropic#250711.
 */

import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'

/**
 * Content portion of team memory data - flat key-value storage.
 * Keys are file paths relative to the team memory directory (e.g. "MEMORY.md", "patterns.md").
 * Values are UTF-8 string content (typically Markdown).
 */
export const TeamMemoryContentSchema = lazySchema(() =>
  z.object({
    entries: z.record(z.string(), z.string()),
    // Per-key SHA-256 of entry content (`sha256:<hex>`). Added in
    // anthropic/anthropic#283027. Optional for forward-compat with older
    // server deployments; empty map when entries is empty.
    entryChecksums: z.record(z.string(), z.string()).optional(),
  }),
)

/**
 * Full response from GET /api/claude_code/team_memory
 */
export const TeamMemoryDataSchema = lazySchema(() =>
  z.object({
    organizationId: z.string(),
    repo: z.string(),
    version: z.number(),
    lastModified: z.string(), // ISO 8601 timestamp
    checksum: z.string(), // SHA256 with 'sha256:' prefix
    content: TeamMemoryContentSchema(),
  }),
)

/**
 * Structured 413 error body from the server (anthropic/anthropic#293258).
 * The server's RequestTooLargeException serializes error_code and the
 * extra_details dict flattened into error.details. We only model the
 * too-many-entries case; entry-too-large is handled via MAX_FILE_SIZE_BYTES
 * pre-check on the client side and would need a separate schema.
 */
export const TeamMemoryTooManyEntriesSchema = lazySchema(() =>
  z.object({
    error: z.object({
      details: z.object({

```

---


### `src/services/teamMemorySync/watcher.ts`

**信息:**
- 行数: 387
- 大小: 13405 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Team Memory File Watcher
 *
 * Watches the team memory directory for changes and triggers
 * a debounced push to the server when files are modified.
 * Performs an initial pull on startup, then starts a directory-level
 * fs.watch so first-time writes to a fresh repo get picked up.
 */

import { feature } from 'bun:bundle'
import { type FSWatcher, watch } from 'fs'
import { mkdir, stat } from 'fs/promises'
import { join } from 'path'
import {
  getTeamMemPath,
  isTeamMemoryEnabled,
} from '../../memdir/teamMemPaths.js'
import { registerCleanup } from '../../utils/cleanupRegistry.js'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { getGithubRepo } from '../../utils/git.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'
import {
  createSyncState,
  isTeamMemorySyncAvailable,
  pullTeamMemory,
  pushTeamMemory,
  type SyncState,
} from './index.js'
import type { TeamMemorySyncPushResult } from './types.js'

const DEBOUNCE_MS = 2000 // Wait 2s after last change before pushing

// ─── Watcher state ──────────────────────────────────────────
let watcher: FSWatcher | null = null
let debounceTimer: ReturnType<typeof setTimeout> | null = null
let pushInProgress = false
let hasPendingChanges = false
let currentPushPromise: Promise<void> | null = null
let watcherStarted = false

// Set after a push fails for a reason that can't self-heal on retry.
// Prevents watch events from other sessions' writes to the shared team
// dir driving an infinite retry loop (BQ Mar 14-16: one no_oauth device
// emitted 167K push events over 2.5 days). Cleared on unlink — file deletion
// is a recovery action for the too-many-entries case, and for no_oauth the
// suppression persisting until session restart is correct.

```

---


### `src/services/tips/tipHistory.ts`

**信息:**
- 行数: 17
- 大小: 601 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getGlobalConfig, saveGlobalConfig } from '../../utils/config.js'

export function recordTipShown(tipId: string): void {
  const numStartups = getGlobalConfig().numStartups
  saveGlobalConfig(c => {
    const history = c.tipsHistory ?? {}
    if (history[tipId] === numStartups) return c
    return { ...c, tipsHistory: { ...history, [tipId]: numStartups } }
  })
}

export function getSessionsSinceLastShown(tipId: string): number {
  const config = getGlobalConfig()
  const lastShown = config.tipsHistory?.[tipId]
  if (!lastShown) return Infinity
  return config.numStartups - lastShown
}

```

---


### `src/services/tips/tipRegistry.ts`

**信息:**
- 行数: 686
- 大小: 23154 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import chalk from 'chalk'
import { logForDebugging } from 'src/utils/debug.js'
import { fileHistoryEnabled } from 'src/utils/fileHistory.js'
import {
  getInitialSettings,
  getSettings_DEPRECATED,
  getSettingsForSource,
} from 'src/utils/settings/settings.js'
import { shouldOfferTerminalSetup } from '../../commands/terminalSetup/terminalSetup.js'
import { getDesktopUpsellConfig } from '../../components/DesktopUpsell/DesktopUpsellStartup.js'
import { color } from '../../components/design-system/color.js'
import { shouldShowOverageCreditUpsell } from '../../components/LogoV2/OverageCreditUpsell.js'
import { getShortcutDisplay } from '../../keybindings/shortcutFormat.js'
import { isKairosCronEnabled } from '../../tools/ScheduleCronTool/prompt.js'
import { is1PApiCustomer } from '../../utils/auth.js'
import { countConcurrentSessions } from '../../utils/concurrentSessions.js'
import { getGlobalConfig } from '../../utils/config.js'
import {
  getEffortEnvOverride,
  modelSupportsEffort,
} from '../../utils/effort.js'
import { env } from '../../utils/env.js'
import { cacheKeys } from '../../utils/fileStateCache.js'
import { getWorktreeCount } from '../../utils/git.js'
import {
  detectRunningIDEsCached,
  getSortedIdeLockfiles,
  isCursorInstalled,
  isSupportedTerminal,
  isSupportedVSCodeTerminal,
  isVSCodeInstalled,
  isWindsurfInstalled,
} from '../../utils/ide.js'
import {
  getMainLoopModel,
  getUserSpecifiedModelSetting,
} from '../../utils/model/model.js'
import { getPlatform } from '../../utils/platform.js'
import { isPluginInstalled } from '../../utils/plugins/installedPluginsManager.js'
import { loadKnownMarketplacesConfigSafe } from '../../utils/plugins/marketplaceManager.js'
import { OFFICIAL_MARKETPLACE_NAME } from '../../utils/plugins/officialMarketplace.js'
import {
  getCurrentSessionAgentColor,
  isCustomTitleEnabled,
} from '../../utils/sessionStorage.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../analytics/growthbook.js'
import {
  formatGrantAmount,
  getCachedOverageCreditGrant,
} from '../api/overageCreditGrant.js'

```

---


### `src/services/tips/tipScheduler.ts`

**信息:**
- 行数: 58
- 大小: 1664 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getSettings_DEPRECATED } from '../../utils/settings/settings.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../analytics/index.js'
import { getSessionsSinceLastShown, recordTipShown } from './tipHistory.js'
import { getRelevantTips } from './tipRegistry.js'
import type { Tip, TipContext } from './types.js'

export function selectTipWithLongestTimeSinceShown(
  availableTips: Tip[],
): Tip | undefined {
  if (availableTips.length === 0) {
    return undefined
  }

  if (availableTips.length === 1) {
    return availableTips[0]
  }

  // Sort tips by sessions since last shown (descending) and take the first one
  // This is the tip that hasn't been shown for the longest time
  const tipsWithSessions = availableTips.map(tip => ({
    tip,
    sessions: getSessionsSinceLastShown(tip.id),
  }))

  tipsWithSessions.sort((a, b) => b.sessions - a.sessions)
  return tipsWithSessions[0]?.tip
}

export async function getTipToShowOnSpinner(
  context?: TipContext,
): Promise<Tip | undefined> {
  // Check if tips are disabled (default to true if not set)
  if (getSettings_DEPRECATED().spinnerTipsEnabled === false) {
    return undefined
  }

  const tips = await getRelevantTips(context)
  if (tips.length === 0) {
    return undefined
  }

  return selectTipWithLongestTimeSinceShown(tips)
}

export function recordShownTip(tip: Tip): void {
  // Record in history
  recordTipShown(tip.id)

```

---


### `src/services/tips/types.ts`

**信息:**
- 行数: 2
- 大小: 91 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type Tip = Record<string, unknown>
export type TipContext = Record<string, unknown>

```

---


### `src/services/tokenEstimation.ts`

**信息:**
- 行数: 495
- 大小: 16883 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Anthropic } from '@anthropic-ai/sdk'
import type { BetaMessageParam as MessageParam } from '@anthropic-ai/sdk/resources/beta/messages/messages.mjs'
// @aws-sdk/client-bedrock-runtime is imported dynamically in countTokensWithBedrock()
// to defer ~279KB of AWS SDK code until a Bedrock call is actually made
import type { CountTokensCommandInput } from '@aws-sdk/client-bedrock-runtime'
import { getAPIProvider } from 'src/utils/model/providers.js'
import { VERTEX_COUNT_TOKENS_ALLOWED_BETAS } from '../constants/betas.js'
import type { Attachment } from '../utils/attachments.js'
import { getModelBetas } from '../utils/betas.js'
import { getVertexRegionForModel, isEnvTruthy } from '../utils/envUtils.js'
import { logError } from '../utils/log.js'
import { normalizeAttachmentForAPI } from '../utils/messages.js'
import {
  createBedrockRuntimeClient,
  getInferenceProfileBackingModel,
  isFoundationModel,
} from '../utils/model/bedrock.js'
import {
  getDefaultSonnetModel,
  getMainLoopModel,
  getSmallFastModel,
  normalizeModelStringForAPI,
} from '../utils/model/model.js'
import { jsonStringify } from '../utils/slowOperations.js'
import { isToolReferenceBlock } from '../utils/toolSearch.js'
import { getAPIMetadata, getExtraBodyParams } from './api/claude.js'
import { getAnthropicClient } from './api/client.js'
import { withTokenCountVCR } from './vcr.js'

// Minimal values for token counting with thinking enabled
// API constraint: max_tokens must be greater than thinking.budget_tokens
const TOKEN_COUNT_THINKING_BUDGET = 1024
const TOKEN_COUNT_MAX_TOKENS = 2048

/**
 * Check if messages contain thinking blocks
 */
function hasThinkingBlocks(
  messages: Anthropic.Beta.Messages.BetaMessageParam[],
): boolean {
  for (const message of messages) {
    if (message.role === 'assistant' && Array.isArray(message.content)) {
      for (const block of message.content) {
        if (
          typeof block === 'object' &&
          block !== null &&
          'type' in block &&
          (block.type === 'thinking' || block.type === 'redacted_thinking')
        ) {
          return true

```

---


### `src/services/toolUseSummary/toolUseSummaryGenerator.ts`

**信息:**
- 行数: 112
- 大小: 3376 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Tool Use Summary Generator
 *
 * Generates human-readable summaries of completed tool batches using Haiku.
 * Used by the SDK to provide high-level progress updates to clients.
 */

import { E_TOOL_USE_SUMMARY_GENERATION_FAILED } from '../../constants/errorIds.js'
import { toError } from '../../utils/errors.js'
import { logError } from '../../utils/log.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { asSystemPrompt } from '../../utils/systemPromptType.js'
import { queryHaiku } from '../api/claude.js'

const TOOL_USE_SUMMARY_SYSTEM_PROMPT = `Write a short summary label describing what these tool calls accomplished. It appears as a single-line row in a mobile app and truncates around 30 characters, so think git-commit-subject, not sentence.

Keep the verb in past tense and the most distinctive noun. Drop articles, connectors, and long location context first.

Examples:
- Searched in auth/
- Fixed NPE in UserService
- Created signup endpoint
- Read config.json
- Ran failing tests`

type ToolInfo = {
  name: string
  input: unknown
  output: unknown
}

export type GenerateToolUseSummaryParams = {
  tools: ToolInfo[]
  signal: AbortSignal
  isNonInteractiveSession: boolean
  lastAssistantText?: string
}

/**
 * Generates a human-readable summary of completed tools.
 *
 * @param params - Parameters including tools executed and their results
 * @returns A brief summary string, or null if generation fails
 */
export async function generateToolUseSummary({
  tools,
  signal,
  isNonInteractiveSession,
  lastAssistantText,
}: GenerateToolUseSummaryParams): Promise<string | null> {

```

---


### `src/services/tools/StreamingToolExecutor.ts`

**信息:**
- 行数: 530
- 大小: 17196 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ToolUseBlock } from '@anthropic-ai/sdk/resources/index.mjs'
import {
  createUserMessage,
  REJECT_MESSAGE,
  withMemoryCorrectionHint,
} from 'src/utils/messages.js'
import type { CanUseToolFn } from '../../hooks/useCanUseTool.js'
import { findToolByName, type Tools, type ToolUseContext } from '../../Tool.js'
import { BASH_TOOL_NAME } from '../../tools/BashTool/toolName.js'
import type { AssistantMessage, Message } from '../../types/message.js'
import { createChildAbortController } from '../../utils/abortController.js'
import { runToolUse } from './toolExecution.js'

type MessageUpdate = {
  message?: Message
  newContext?: ToolUseContext
}

type ToolStatus = 'queued' | 'executing' | 'completed' | 'yielded'

type TrackedTool = {
  id: string
  block: ToolUseBlock
  assistantMessage: AssistantMessage
  status: ToolStatus
  isConcurrencySafe: boolean
  promise?: Promise<void>
  results?: Message[]
  // Progress messages are stored separately and yielded immediately
  pendingProgress: Message[]
  contextModifiers?: Array<(context: ToolUseContext) => ToolUseContext>
}

/**
 * Executes tools as they stream in with concurrency control.
 * - Concurrent-safe tools can execute in parallel with other concurrent-safe tools
 * - Non-concurrent tools must execute alone (exclusive access)
 * - Results are buffered and emitted in the order tools were received
 */
export class StreamingToolExecutor {
  private tools: TrackedTool[] = []
  private toolUseContext: ToolUseContext
  private hasErrored = false
  private erroredToolDescription = ''
  // Child of toolUseContext.abortController. Fires when a Bash tool errors
  // so sibling subprocesses die immediately instead of running to completion.
  // Aborting this does NOT abort the parent — query.ts won't end the turn.
  private siblingAbortController: AbortController
  private discarded = false
  // Signal to wake up getRemainingResults when progress is available

```

---


### `src/services/tools/toolExecution.ts`

**信息:**
- 行数: 1745
- 大小: 60309 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type {
  ContentBlockParam,
  ToolResultBlockParam,
  ToolUseBlock,
} from '@anthropic-ai/sdk/resources/index.mjs'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from 'src/services/analytics/index.js'
import {
  extractMcpToolDetails,
  extractSkillName,
  extractToolInputForTelemetry,
  getFileExtensionForAnalytics,
  getFileExtensionsFromBashCommand,
  isToolDetailsLoggingEnabled,
  mcpToolDetailsForAnalytics,
  sanitizeToolNameForAnalytics,
} from 'src/services/analytics/metadata.js'
import {
  addToToolDuration,
  getCodeEditToolDecisionCounter,
  getStatsStore,
} from '../../bootstrap/state.js'
import {
  buildCodeEditToolAttributes,
  isCodeEditingTool,
} from '../../hooks/toolPermission/permissionLogging.js'
import type { CanUseToolFn } from '../../hooks/useCanUseTool.js'
import {
  findToolByName,
  type Tool,
  type ToolProgress,
  type ToolProgressData,
  type ToolUseContext,
} from '../../Tool.js'
import type { BashToolInput } from '../../tools/BashTool/BashTool.js'
import { startSpeculativeClassifierCheck } from '../../tools/BashTool/bashPermissions.js'
import { BASH_TOOL_NAME } from '../../tools/BashTool/toolName.js'
import { FILE_EDIT_TOOL_NAME } from '../../tools/FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from '../../tools/FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from '../../tools/FileWriteTool/prompt.js'
import { NOTEBOOK_EDIT_TOOL_NAME } from '../../tools/NotebookEditTool/constants.js'
import { POWERSHELL_TOOL_NAME } from '../../tools/PowerShellTool/toolName.js'
import { parseGitCommitId } from '../../tools/shared/gitOperationTracking.js'
import {
  isDeferredTool,
  TOOL_SEARCH_TOOL_NAME,
} from '../../tools/ToolSearchTool/prompt.js'

```

---


### `src/services/tools/toolHooks.ts`

**信息:**
- 行数: 650
- 大小: 22333 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from 'src/services/analytics/index.js'
import { sanitizeToolNameForAnalytics } from 'src/services/analytics/metadata.js'
import type z from 'zod/v4'
import type { CanUseToolFn } from '../../hooks/useCanUseTool.js'
import type { AnyObject, Tool, ToolUseContext } from '../../Tool.js'
import type { HookProgress } from '../../types/hooks.js'
import type {
  AssistantMessage,
  AttachmentMessage,
  ProgressMessage,
} from '../../types/message.js'
import type { PermissionDecision } from '../../types/permissions.js'
import { createAttachmentMessage } from '../../utils/attachments.js'
import { logForDebugging } from '../../utils/debug.js'
import {
  executePostToolHooks,
  executePostToolUseFailureHooks,
  executePreToolHooks,
  getPreToolHookBlockingMessage,
} from '../../utils/hooks.js'
import { logError } from '../../utils/log.js'
import {
  getRuleBehaviorDescription,
  type PermissionDecisionReason,
  type PermissionResult,
} from '../../utils/permissions/PermissionResult.js'
import { checkRuleBasedPermissions } from '../../utils/permissions/permissions.js'
import { formatError } from '../../utils/toolErrors.js'
import { isMcpTool } from '../mcp/utils.js'
import type { McpServerType, MessageUpdateLazy } from './toolExecution.js'

export type PostToolUseHooksResult<Output> =
  | MessageUpdateLazy<AttachmentMessage | ProgressMessage<HookProgress>>
  | { updatedMCPToolOutput: Output }

export async function* runPostToolUseHooks<Input extends AnyObject, Output>(
  toolUseContext: ToolUseContext,
  tool: Tool<Input, Output>,
  toolUseID: string,
  messageId: string,
  toolInput: Record<string, unknown>,
  toolResponse: Output,
  requestId: string | undefined,
  mcpServerType: McpServerType,
  mcpServerBaseUrl: string | undefined,
): AsyncGenerator<PostToolUseHooksResult<Output>> {
  const postToolStartTime = Date.now()

```

---


### `src/services/tools/toolOrchestration.ts`

**信息:**
- 行数: 188
- 大小: 5501 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ToolUseBlock } from '@anthropic-ai/sdk/resources/index.mjs'
import type { CanUseToolFn } from '../../hooks/useCanUseTool.js'
import { findToolByName, type ToolUseContext } from '../../Tool.js'
import type { AssistantMessage, Message } from '../../types/message.js'
import { all } from '../../utils/generators.js'
import { type MessageUpdateLazy, runToolUse } from './toolExecution.js'

function getMaxToolUseConcurrency(): number {
  return (
    parseInt(process.env.CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY || '', 10) || 10
  )
}

export type MessageUpdate = {
  message?: Message
  newContext: ToolUseContext
}

export async function* runTools(
  toolUseMessages: ToolUseBlock[],
  assistantMessages: AssistantMessage[],
  canUseTool: CanUseToolFn,
  toolUseContext: ToolUseContext,
): AsyncGenerator<MessageUpdate, void> {
  let currentContext = toolUseContext
  for (const { isConcurrencySafe, blocks } of partitionToolCalls(
    toolUseMessages,
    currentContext,
  )) {
    if (isConcurrencySafe) {
      const queuedContextModifiers: Record<
        string,
        ((context: ToolUseContext) => ToolUseContext)[]
      > = {}
      // Run read-only batch concurrently
      for await (const update of runToolsConcurrently(
        blocks,
        assistantMessages,
        canUseTool,
        currentContext,
      )) {
        if (update.contextModifier) {
          const { toolUseID, modifyContext } = update.contextModifier
          if (!queuedContextModifiers[toolUseID]) {
            queuedContextModifiers[toolUseID] = []
          }
          queuedContextModifiers[toolUseID].push(modifyContext)
        }
        yield {
          message: update.message,

```

---


### `src/services/vcr.ts`

**信息:**
- 行数: 406
- 大小: 12166 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { BetaContentBlock } from '@anthropic-ai/sdk/resources/beta/messages/messages.mjs'
import { createHash, randomUUID, type UUID } from 'crypto'
import { mkdir, readFile, writeFile } from 'fs/promises'
import isPlainObject from 'lodash-es/isPlainObject.js'
import mapValues from 'lodash-es/mapValues.js'
import { dirname, join } from 'path'
import { addToTotalSessionCost } from 'src/cost-tracker.js'
import { calculateUSDCost } from 'src/utils/modelCost.js'
import type {
  AssistantMessage,
  Message,
  StreamEvent,
  SystemAPIErrorMessage,
  UserMessage,
} from '../types/message.js'
import { getCwd } from '../utils/cwd.js'
import { env } from '../utils/env.js'
import { getClaudeConfigHomeDir, isEnvTruthy } from '../utils/envUtils.js'
import { getErrnoCode } from '../utils/errors.js'
import { normalizeMessagesForAPI } from '../utils/messages.js'
import { jsonParse, jsonStringify } from '../utils/slowOperations.js'

function shouldUseVCR(): boolean {
  if (process.env.NODE_ENV === 'test') {
    return true
  }

  if (process.env.USER_TYPE === 'ant' && isEnvTruthy(process.env.FORCE_VCR)) {
    return true
  }

  return false
}

/**
 * Generic fixture management helper
 * Handles caching, reading, writing fixtures for any data type
 */
async function withFixture<T>(
  input: unknown,
  fixtureName: string,
  f: () => Promise<T>,
): Promise<T> {
  if (!shouldUseVCR()) {
    return await f()
  }

  // Create hash of input for fixture filename
  const hash = createHash('sha1')
    .update(jsonStringify(input))

```

---


### `src/services/voice.ts`

**信息:**
- 行数: 525
- 大小: 17116 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Voice service: audio recording for push-to-talk voice input.
//
// Recording uses native audio capture (cpal) on macOS, Linux, and Windows
// for in-process mic access. Falls back to SoX `rec` or arecord (ALSA)
// on Linux if the native module is unavailable.

import { type ChildProcess, spawn, spawnSync } from 'child_process'
import { readFile } from 'fs/promises'
import { logForDebugging } from '../utils/debug.js'
import { isEnvTruthy, isRunningOnHomespace } from '../utils/envUtils.js'
import { logError } from '../utils/log.js'
import { getPlatform } from '../utils/platform.js'

// Lazy-loaded native audio module. audio-capture.node links against
// CoreAudio.framework + AudioUnit.framework; dlopen is synchronous and
// blocks the event loop for ~1s warm, up to ~8s on cold coreaudiod
// (post-wake, post-boot). Load happens on first voice keypress — no
// preload, because there's no way to make dlopen non-blocking and a
// startup freeze is worse than a first-press delay.
type AudioNapi = typeof import('audio-capture-napi')
let audioNapi: AudioNapi | null = null
let audioNapiPromise: Promise<AudioNapi> | null = null

function loadAudioNapi(): Promise<AudioNapi> {
  audioNapiPromise ??= (async () => {
    const t0 = Date.now()
    const mod = await import('audio-capture-napi')
    // vendor/audio-capture-src/index.ts defers require(...node) until the
    // first function call — trigger it here so timing reflects real cost.
    mod.isNativeAudioAvailable()
    audioNapi = mod
    logForDebugging(`[voice] audio-capture-napi loaded in ${Date.now() - t0}ms`)
    return mod
  })()
  return audioNapiPromise
}

// ─── Constants ───────────────────────────────────────────────────────

const RECORDING_SAMPLE_RATE = 16000
const RECORDING_CHANNELS = 1

// SoX silence detection: stop after this duration of silence
const SILENCE_DURATION_SECS = '2.0'
const SILENCE_THRESHOLD = '3%'

// ─── Dependency check ────────────────────────────────────────────────

function hasCommand(cmd: string): boolean {
  // Spawn the target directly instead of `which cmd`. On Termux/Android

```

---


### `src/services/voiceKeyterms.ts`

**信息:**
- 行数: 106
- 大小: 3462 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Voice keyterms for improving STT accuracy in the voice_stream endpoint.
//
// Provides domain-specific vocabulary hints (Deepgram "keywords") so the STT
// engine correctly recognises coding terminology, project names, and branch
// names that would otherwise be misheard.

import { basename } from 'path'
import { getProjectRoot } from '../bootstrap/state.js'
import { getBranch } from '../utils/git.js'

// ─── Global keyterms ────────────────────────────────────────────────

const GLOBAL_KEYTERMS: readonly string[] = [
  // Terms Deepgram consistently mangles without keyword hints.
  // Note: "Claude" and "Anthropic" are already server-side base keyterms.
  // Avoid terms nobody speaks aloud as-spelled (stdout → "standard out").
  'MCP',
  'symlink',
  'grep',
  'regex',
  'localhost',
  'codebase',
  'TypeScript',
  'JSON',
  'OAuth',
  'webhook',
  'gRPC',
  'dotfiles',
  'subagent',
  'worktree',
]

// ─── Helpers ────────────────────────────────────────────────────────

/**
 * Split an identifier (camelCase, PascalCase, kebab-case, snake_case, or
 * path segments) into individual words.  Fragments of 2 chars or fewer are
 * discarded to avoid noise.
 */
export function splitIdentifier(name: string): string[] {
  return name
    .replace(/([a-z])([A-Z])/g, '$1 $2')
    .split(/[-_./\s]+/)
    .map(w => w.trim())
    .filter(w => w.length > 2 && w.length <= 20)
}

function fileNameWords(filePath: string): string[] {
  const stem = basename(filePath).replace(/\.[^.]+$/, '')
  return splitIdentifier(stem)

```

---


### `src/services/voiceStreamSTT.ts`

**信息:**
- 行数: 544
- 大小: 21375 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Anthropic voice_stream speech-to-text client for push-to-talk.
//
// Only reachable in ant builds (gated by feature('VOICE_MODE') in useVoice.ts import).
//
// Connects to Anthropic's voice_stream WebSocket endpoint using the same
// OAuth credentials as Claude Code.  The endpoint uses conversation_engine
// backed models for speech-to-text.  Designed for hold-to-talk: hold the
// keybinding to record, release to stop and submit.
//
// The wire protocol uses JSON control messages (KeepAlive, CloseStream) and
// binary audio frames.  The server responds with TranscriptText and
// TranscriptEndpoint JSON messages.

import type { ClientRequest, IncomingMessage } from 'http'
import WebSocket from 'ws'
import { getOauthConfig } from '../constants/oauth.js'
import {
  checkAndRefreshOAuthTokenIfNeeded,
  getClaudeAIOAuthTokens,
  isAnthropicAuthEnabled,
} from '../utils/auth.js'
import { logForDebugging } from '../utils/debug.js'
import { getUserAgent } from '../utils/http.js'
import { logError } from '../utils/log.js'
import { getWebSocketTLSOptions } from '../utils/mtls.js'
import { getWebSocketProxyAgent, getWebSocketProxyUrl } from '../utils/proxy.js'
import { jsonParse, jsonStringify } from '../utils/slowOperations.js'

const KEEPALIVE_MSG = '{"type":"KeepAlive"}'
const CLOSE_STREAM_MSG = '{"type":"CloseStream"}'

import { getFeatureValue_CACHED_MAY_BE_STALE } from './analytics/growthbook.js'

// ─── Constants ───────────────────────────────────────────────────────

const VOICE_STREAM_PATH = '/api/ws/speech_to_text/voice_stream'

const KEEPALIVE_INTERVAL_MS = 8_000

// finalize() resolution timers. `noData` fires when no TranscriptText
// arrives post-CloseStream — the server has nothing; don't wait out the
// full ~3-5s WS teardown to confirm emptiness. `safety` is the last-
// resort cap if the WS hangs. Exported so tests can shorten them.
export const FINALIZE_TIMEOUTS_MS = {
  safety: 5_000,
  noData: 1_500,
}

// ─── Types ──────────────────────────────────────────────────────────


```

---

