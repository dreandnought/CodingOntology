# tools 模块

## 概述

**位置:** `src/tools/`

## 文件统计

- TypeScript 文件: 161
- TypeScript React 文件: 38
- 总计: 199

## 文件详情

---


### `src/tools/AgentTool/AgentTool.tsx`

**信息:**
- 行数: 1398
- 大小: 233734 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import * as React from 'react';
import { buildTool, type ToolDef, toolMatchesName } from 'src/Tool.js';
import type { Message as MessageType, NormalizedUserMessage } from 'src/types/message.js';
import { getQuerySourceForAgent } from 'src/utils/promptCategory.js';
import { z } from 'zod/v4';
import { clearInvokedSkillsForAgent, getSdkAgentProgressSummariesEnabled } from '../../bootstrap/state.js';
import { enhanceSystemPromptWithEnvDetails, getSystemPrompt } from '../../constants/prompts.js';
import { isCoordinatorMode } from '../../coordinator/coordinatorMode.js';
import { startAgentSummarization } from '../../services/AgentSummary/agentSummary.js';
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../services/analytics/index.js';
import { clearDumpState } from '../../services/api/dumpPrompts.js';
import { completeAgentTask as completeAsyncAgent, createActivityDescriptionResolver, createProgressTracker, enqueueAgentNotification, failAgentTask as failAsyncAgent, getProgressUpdate, getTokenCountFromTracker, isLocalAgentTask, killAsyncAgent, registerAgentForeground, registerAsyncAgent, unregisterAgentForeground, updateAgentProgress as updateAsyncAgentProgress, updateProgressFromMessage } from '../../tasks/LocalAgentTask/LocalAgentTask.js';
import { checkRemoteAgentEligibility, formatPreconditionError, getRemoteTaskSessionUrl, registerRemoteAgentTask } from '../../tasks/RemoteAgentTask/RemoteAgentTask.js';
import { assembleToolPool } from '../../tools.js';
import { asAgentId } from '../../types/ids.js';
import { runWithAgentContext } from '../../utils/agentContext.js';
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js';
import { getCwd, runWithCwdOverride } from '../../utils/cwd.js';
import { logForDebugging } from '../../utils/debug.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import { AbortError, errorMessage, toError } from '../../utils/errors.js';
import type { CacheSafeParams } from '../../utils/forkedAgent.js';
import { lazySchema } from '../../utils/lazySchema.js';
import { createUserMessage, extractTextContent, isSyntheticMessage, normalizeMessages } from '../../utils/messages.js';
import { getAgentModel } from '../../utils/model/agent.js';
import { permissionModeSchema } from '../../utils/permissions/PermissionMode.js';
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js';
import { filterDeniedAgents, getDenyRuleForAgent } from '../../utils/permissions/permissions.js';
import { enqueueSdkEvent } from '../../utils/sdkEventQueue.js';
import { writeAgentMetadata } from '../../utils/sessionStorage.js';
import { sleep } from '../../utils/sleep.js';
import { buildEffectiveSystemPrompt } from '../../utils/systemPrompt.js';
import { asSystemPrompt } from '../../utils/systemPromptType.js';
import { getTaskOutputPath } from '../../utils/task/diskOutput.js';
import { getParentSessionId, isTeammate } from '../../utils/teammate.js';
import { isInProcessTeammate } from '../../utils/teammateContext.js';
import { teleportToRemote } from '../../utils/teleport.js';
import { getAssistantMessageContentLength } from '../../utils/tokens.js';
import { createAgentId } from '../../utils/uuid.js';
import { createAgentWorktree, hasWorktreeChanges, removeAgentWorktree } from '../../utils/worktree.js';
import { BASH_TOOL_NAME } from '../BashTool/toolName.js';
import { BackgroundHint } from '../BashTool/UI.js';
import { FILE_READ_TOOL_NAME } from '../FileReadTool/prompt.js';
import { spawnTeammate } from '../shared/spawnMultiAgent.js';
import { setAgentColor } from './agentColorManager.js';
import { agentToolResultSchema, classifyHandoffIfNeeded, emitTaskProgress, extractPartialResult, finalizeAgentTool, getLastToolUseName, runAsyncAgentLifecycle } from './agentToolUtils.js';
import { GENERAL_PURPOSE_AGENT } from './built-in/generalPurposeAgent.js';
import { AGENT_TOOL_NAME, LEGACY_AGENT_TOOL_NAME, ONE_SHOT_BUILTIN_AGENT_TYPES } from './constants.js';

```

---


### `src/tools/AgentTool/UI.tsx`

**信息:**
- 行数: 872
- 大小: 125359 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ToolResultBlockParam, ToolUseBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import { ConfigurableShortcutHint } from 'src/components/ConfigurableShortcutHint.js';
import { CtrlOToExpand, SubAgentProvider } from 'src/components/CtrlOToExpand.js';
import { Byline } from 'src/components/design-system/Byline.js';
import { KeyboardShortcutHint } from 'src/components/design-system/KeyboardShortcutHint.js';
import type { z } from 'zod/v4';
import { AgentProgressLine } from '../../components/AgentProgressLine.js';
import { FallbackToolUseErrorMessage } from '../../components/FallbackToolUseErrorMessage.js';
import { FallbackToolUseRejectedMessage } from '../../components/FallbackToolUseRejectedMessage.js';
import { Markdown } from '../../components/Markdown.js';
import { Message as MessageComponent } from '../../components/Message.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { ToolUseLoader } from '../../components/ToolUseLoader.js';
import { Box, Text } from '../../ink.js';
import { getDumpPromptsPath } from '../../services/api/dumpPrompts.js';
import { findToolByName, type Tools } from '../../Tool.js';
import type { Message, ProgressMessage } from '../../types/message.js';
import type { AgentToolProgress } from '../../types/tools.js';
import { count } from '../../utils/array.js';
import { getSearchOrReadFromContent, getSearchReadSummaryText } from '../../utils/collapseReadSearch.js';
import { getDisplayPath } from '../../utils/file.js';
import { formatDuration, formatNumber } from '../../utils/format.js';
import { buildSubagentLookups, createAssistantMessage, EMPTY_LOOKUPS } from '../../utils/messages.js';
import type { ModelAlias } from '../../utils/model/aliases.js';
import { getMainLoopModel, parseUserSpecifiedModel, renderModelName } from '../../utils/model/model.js';
import type { Theme, ThemeName } from '../../utils/theme.js';
import type { outputSchema, Progress, RemoteLaunchedOutput } from './AgentTool.js';
import { inputSchema } from './AgentTool.js';
import { getAgentColor } from './agentColorManager.js';
import { GENERAL_PURPOSE_AGENT } from './built-in/generalPurposeAgent.js';
const MAX_PROGRESS_MESSAGES_TO_SHOW = 3;

/**
 * Guard: checks if progress data has a `message` field (agent_progress or
 * skill_progress).  Other progress types (e.g. bash_progress forwarded from
 * sub-agents) lack this field and must be skipped by UI helpers.
 */
function hasProgressMessage(data: Progress): data is AgentToolProgress {
  if (!('message' in data)) {
    return false;
  }
  const msg = (data as AgentToolProgress).message;
  return msg != null && typeof msg === 'object' && 'type' in msg;
}

/**
 * Check if a progress message is a search/read/REPL operation (tool use or result).
 * Returns { isSearch, isRead, isREPL } if it's a collapsible operation, null otherwise.

```

---


### `src/tools/AgentTool/agentColorManager.ts`

**信息:**
- 行数: 66
- 大小: 1499 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getAgentColorMap } from '../../bootstrap/state.js'
import type { Theme } from '../../utils/theme.js'

export type AgentColorName =
  | 'red'
  | 'blue'
  | 'green'
  | 'yellow'
  | 'purple'
  | 'orange'
  | 'pink'
  | 'cyan'

export const AGENT_COLORS: readonly AgentColorName[] = [
  'red',
  'blue',
  'green',
  'yellow',
  'purple',
  'orange',
  'pink',
  'cyan',
] as const

export const AGENT_COLOR_TO_THEME_COLOR = {
  red: 'red_FOR_SUBAGENTS_ONLY',
  blue: 'blue_FOR_SUBAGENTS_ONLY',
  green: 'green_FOR_SUBAGENTS_ONLY',
  yellow: 'yellow_FOR_SUBAGENTS_ONLY',
  purple: 'purple_FOR_SUBAGENTS_ONLY',
  orange: 'orange_FOR_SUBAGENTS_ONLY',
  pink: 'pink_FOR_SUBAGENTS_ONLY',
  cyan: 'cyan_FOR_SUBAGENTS_ONLY',
} as const satisfies Record<AgentColorName, keyof Theme>

export function getAgentColor(agentType: string): keyof Theme | undefined {
  if (agentType === 'general-purpose') {
    return undefined
  }

  const agentColorMap = getAgentColorMap()

  // Check if color already assigned
  const existingColor = agentColorMap.get(agentType)
  if (existingColor && AGENT_COLORS.includes(existingColor)) {
    return AGENT_COLOR_TO_THEME_COLOR[existingColor]
  }

  return undefined
}

```

---


### `src/tools/AgentTool/agentDisplay.ts`

**信息:**
- 行数: 104
- 大小: 3269 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Shared utilities for displaying agent information.
 * Used by both the CLI `claude agents` handler and the interactive `/agents` command.
 */

import { getDefaultSubagentModel } from '../../utils/model/agent.js'
import {
  getSourceDisplayName,
  type SettingSource,
} from '../../utils/settings/constants.js'
import type { AgentDefinition } from './loadAgentsDir.js'

type AgentSource = SettingSource | 'built-in' | 'plugin'

export type AgentSourceGroup = {
  label: string
  source: AgentSource
}

/**
 * Ordered list of agent source groups for display.
 * Both the CLI and interactive UI should use this to ensure consistent ordering.
 */
export const AGENT_SOURCE_GROUPS: AgentSourceGroup[] = [
  { label: 'User agents', source: 'userSettings' },
  { label: 'Project agents', source: 'projectSettings' },
  { label: 'Local agents', source: 'localSettings' },
  { label: 'Managed agents', source: 'policySettings' },
  { label: 'Plugin agents', source: 'plugin' },
  { label: 'CLI arg agents', source: 'flagSettings' },
  { label: 'Built-in agents', source: 'built-in' },
]

export type ResolvedAgent = AgentDefinition & {
  overriddenBy?: AgentSource
}

/**
 * Annotate agents with override information by comparing against the active
 * (winning) agent list. An agent is "overridden" when another agent with the
 * same type from a higher-priority source takes precedence.
 *
 * Also deduplicates by (agentType, source) to handle git worktree duplicates
 * where the same agent file is loaded from both the worktree and main repo.
 */
export function resolveAgentOverrides(
  allAgents: AgentDefinition[],
  activeAgents: AgentDefinition[],
): ResolvedAgent[] {
  const activeMap = new Map<string, AgentDefinition>()

```

---


### `src/tools/AgentTool/agentMemory.ts`

**信息:**
- 行数: 177
- 大小: 5853 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { join, normalize, sep } from 'path'
import { getProjectRoot } from '../../bootstrap/state.js'
import {
  buildMemoryPrompt,
  ensureMemoryDirExists,
} from '../../memdir/memdir.js'
import { getMemoryBaseDir } from '../../memdir/paths.js'
import { getCwd } from '../../utils/cwd.js'
import { findCanonicalGitRoot } from '../../utils/git.js'
import { sanitizePath } from '../../utils/path.js'

// Persistent agent memory scope: 'user' (~/.claude/agent-memory/), 'project' (.claude/agent-memory/), or 'local' (.claude/agent-memory-local/)
export type AgentMemoryScope = 'user' | 'project' | 'local'

/**
 * Sanitize an agent type name for use as a directory name.
 * Replaces colons (invalid on Windows, used in plugin-namespaced agent
 * types like "my-plugin:my-agent") with dashes.
 */
function sanitizeAgentTypeForPath(agentType: string): string {
  return agentType.replace(/:/g, '-')
}

/**
 * Returns the local agent memory directory, which is project-specific and not checked into VCS.
 * When CLAUDE_CODE_REMOTE_MEMORY_DIR is set, persists to the mount with project namespacing.
 * Otherwise, uses <cwd>/.claude/agent-memory-local/<agentType>/.
 */
function getLocalAgentMemoryDir(dirName: string): string {
  if (process.env.CLAUDE_CODE_REMOTE_MEMORY_DIR) {
    return (
      join(
        process.env.CLAUDE_CODE_REMOTE_MEMORY_DIR,
        'projects',
        sanitizePath(
          findCanonicalGitRoot(getProjectRoot()) ?? getProjectRoot(),
        ),
        'agent-memory-local',
        dirName,
      ) + sep
    )
  }
  return join(getCwd(), '.claude', 'agent-memory-local', dirName) + sep
}

/**
 * Returns the agent memory directory for a given agent type and scope.
 * - 'user' scope: <memoryBase>/agent-memory/<agentType>/
 * - 'project' scope: <cwd>/.claude/agent-memory/<agentType>/
 * - 'local' scope: see getLocalAgentMemoryDir()

```

---


### `src/tools/AgentTool/agentMemorySnapshot.ts`

**信息:**
- 行数: 197
- 大小: 5633 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { mkdir, readdir, readFile, unlink, writeFile } from 'fs/promises'
import { join } from 'path'
import { z } from 'zod/v4'
import { getCwd } from '../../utils/cwd.js'
import { logForDebugging } from '../../utils/debug.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { jsonParse, jsonStringify } from '../../utils/slowOperations.js'
import { type AgentMemoryScope, getAgentMemoryDir } from './agentMemory.js'

const SNAPSHOT_BASE = 'agent-memory-snapshots'
const SNAPSHOT_JSON = 'snapshot.json'
const SYNCED_JSON = '.snapshot-synced.json'

const snapshotMetaSchema = lazySchema(() =>
  z.object({
    updatedAt: z.string().min(1),
  }),
)

const syncedMetaSchema = lazySchema(() =>
  z.object({
    syncedFrom: z.string().min(1),
  }),
)
type SyncedMeta = z.infer<ReturnType<typeof syncedMetaSchema>>

/**
 * Returns the path to the snapshot directory for an agent in the current project.
 * e.g., <cwd>/.claude/agent-memory-snapshots/<agentType>/
 */
export function getSnapshotDirForAgent(agentType: string): string {
  return join(getCwd(), '.claude', SNAPSHOT_BASE, agentType)
}

function getSnapshotJsonPath(agentType: string): string {
  return join(getSnapshotDirForAgent(agentType), SNAPSHOT_JSON)
}

function getSyncedJsonPath(agentType: string, scope: AgentMemoryScope): string {
  return join(getAgentMemoryDir(agentType, scope), SYNCED_JSON)
}

async function readJsonFile<T>(
  path: string,
  schema: z.ZodType<T>,
): Promise<T | null> {
  try {
    const content = await readFile(path, { encoding: 'utf-8' })
    const result = schema.safeParse(jsonParse(content))
    return result.success ? result.data : null

```

---


### `src/tools/AgentTool/agentToolUtils.ts`

**信息:**
- 行数: 686
- 大小: 22739 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { z } from 'zod/v4'
import { clearInvokedSkillsForAgent } from '../../bootstrap/state.js'
import {
  ALL_AGENT_DISALLOWED_TOOLS,
  ASYNC_AGENT_ALLOWED_TOOLS,
  CUSTOM_AGENT_DISALLOWED_TOOLS,
  IN_PROCESS_TEAMMATE_ALLOWED_TOOLS,
} from '../../constants/tools.js'
import { startAgentSummarization } from '../../services/AgentSummary/agentSummary.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import { clearDumpState } from '../../services/api/dumpPrompts.js'
import type { AppState } from '../../state/AppState.js'
import type {
  Tool,
  ToolPermissionContext,
  Tools,
  ToolUseContext,
} from '../../Tool.js'
import { toolMatchesName } from '../../Tool.js'
import {
  completeAgentTask as completeAsyncAgent,
  createActivityDescriptionResolver,
  createProgressTracker,
  enqueueAgentNotification,
  failAgentTask as failAsyncAgent,
  getProgressUpdate,
  getTokenCountFromTracker,
  isLocalAgentTask,
  killAsyncAgent,
  type ProgressTracker,
  updateAgentProgress as updateAsyncAgentProgress,
  updateProgressFromMessage,
} from '../../tasks/LocalAgentTask/LocalAgentTask.js'
import { asAgentId } from '../../types/ids.js'
import type { Message as MessageType } from '../../types/message.js'
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js'
import { logForDebugging } from '../../utils/debug.js'
import { isInProtectedNamespace } from '../../utils/envUtils.js'
import { AbortError, errorMessage } from '../../utils/errors.js'
import type { CacheSafeParams } from '../../utils/forkedAgent.js'
import { lazySchema } from '../../utils/lazySchema.js'
import {
  extractTextContent,
  getLastAssistantMessage,
} from '../../utils/messages.js'
import type { PermissionMode } from '../../utils/permissions/PermissionMode.js'

```

---


### `src/tools/AgentTool/built-in/claudeCodeGuideAgent.ts`

**信息:**
- 行数: 205
- 大小: 8959 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { BASH_TOOL_NAME } from 'src/tools/BashTool/toolName.js'
import { FILE_READ_TOOL_NAME } from 'src/tools/FileReadTool/prompt.js'
import { GLOB_TOOL_NAME } from 'src/tools/GlobTool/prompt.js'
import { GREP_TOOL_NAME } from 'src/tools/GrepTool/prompt.js'
import { SEND_MESSAGE_TOOL_NAME } from 'src/tools/SendMessageTool/constants.js'
import { WEB_FETCH_TOOL_NAME } from 'src/tools/WebFetchTool/prompt.js'
import { WEB_SEARCH_TOOL_NAME } from 'src/tools/WebSearchTool/prompt.js'
import { isUsing3PServices } from 'src/utils/auth.js'
import { hasEmbeddedSearchTools } from 'src/utils/embeddedTools.js'
import { getSettings_DEPRECATED } from 'src/utils/settings/settings.js'
import { jsonStringify } from '../../../utils/slowOperations.js'
import type {
  AgentDefinition,
  BuiltInAgentDefinition,
} from '../loadAgentsDir.js'

const CLAUDE_CODE_DOCS_MAP_URL =
  'https://code.claude.com/docs/en/claude_code_docs_map.md'
const CDP_DOCS_MAP_URL = 'https://platform.claude.com/llms.txt'

export const CLAUDE_CODE_GUIDE_AGENT_TYPE = 'claude-code-guide'

function getClaudeCodeGuideBasePrompt(): string {
  // Ant-native builds alias find/grep to embedded bfs/ugrep and remove the
  // dedicated Glob/Grep tools, so point at find/grep instead.
  const localSearchHint = hasEmbeddedSearchTools()
    ? `${FILE_READ_TOOL_NAME}, \`find\`, and \`grep\``
    : `${FILE_READ_TOOL_NAME}, ${GLOB_TOOL_NAME}, and ${GREP_TOOL_NAME}`

  return `You are the Claude guide agent. Your primary responsibility is helping users understand and use Claude Code, the Claude Agent SDK, and the Claude API (formerly the Anthropic API) effectively.

**Your expertise spans three domains:**

1. **Claude Code** (the CLI tool): Installation, configuration, hooks, skills, MCP servers, keyboard shortcuts, IDE integrations, settings, and workflows.

2. **Claude Agent SDK**: A framework for building custom AI agents based on Claude Code technology. Available for Node.js/TypeScript and Python.

3. **Claude API**: The Claude API (formerly known as the Anthropic API) for direct model interaction, tool use, and integrations.

**Documentation sources:**

- **Claude Code docs** (${CLAUDE_CODE_DOCS_MAP_URL}): Fetch this for questions about the Claude Code CLI tool, including:
  - Installation, setup, and getting started
  - Hooks (pre/post command execution)
  - Custom skills
  - MCP server configuration
  - IDE integrations (VS Code, JetBrains)
  - Settings files and configuration
  - Keyboard shortcuts and hotkeys
  - Subagents and plugins

```

---


### `src/tools/AgentTool/built-in/exploreAgent.ts`

**信息:**
- 行数: 83
- 大小: 4686 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { BASH_TOOL_NAME } from 'src/tools/BashTool/toolName.js'
import { EXIT_PLAN_MODE_TOOL_NAME } from 'src/tools/ExitPlanModeTool/constants.js'
import { FILE_EDIT_TOOL_NAME } from 'src/tools/FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from 'src/tools/FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from 'src/tools/FileWriteTool/prompt.js'
import { GLOB_TOOL_NAME } from 'src/tools/GlobTool/prompt.js'
import { GREP_TOOL_NAME } from 'src/tools/GrepTool/prompt.js'
import { NOTEBOOK_EDIT_TOOL_NAME } from 'src/tools/NotebookEditTool/constants.js'
import { hasEmbeddedSearchTools } from 'src/utils/embeddedTools.js'
import { AGENT_TOOL_NAME } from '../constants.js'
import type { BuiltInAgentDefinition } from '../loadAgentsDir.js'

function getExploreSystemPrompt(): string {
  // Ant-native builds alias find/grep to embedded bfs/ugrep and remove the
  // dedicated Glob/Grep tools, so point at find/grep via Bash instead.
  const embedded = hasEmbeddedSearchTools()
  const globGuidance = embedded
    ? `- Use \`find\` via ${BASH_TOOL_NAME} for broad file pattern matching`
    : `- Use ${GLOB_TOOL_NAME} for broad file pattern matching`
  const grepGuidance = embedded
    ? `- Use \`grep\` via ${BASH_TOOL_NAME} for searching file contents with regex`
    : `- Use ${GREP_TOOL_NAME} for searching file contents with regex`

  return `You are a file search specialist for Claude Code, Anthropic's official CLI for Claude. You excel at thoroughly navigating and exploring codebases.

=== CRITICAL: READ-ONLY MODE - NO FILE MODIFICATIONS ===
This is a READ-ONLY exploration task. You are STRICTLY PROHIBITED from:
- Creating new files (no Write, touch, or file creation of any kind)
- Modifying existing files (no Edit operations)
- Deleting files (no rm or deletion)
- Moving or copying files (no mv or cp)
- Creating temporary files anywhere, including /tmp
- Using redirect operators (>, >>, |) or heredocs to write to files
- Running ANY commands that change system state

Your role is EXCLUSIVELY to search and analyze existing code. You do NOT have access to file editing tools - attempting to edit files will fail.

Your strengths:
- Rapidly finding files using glob patterns
- Searching code and text with powerful regex patterns
- Reading and analyzing file contents

Guidelines:
${globGuidance}
${grepGuidance}
- Use ${FILE_READ_TOOL_NAME} when you know the specific file path you need to read
- Use ${BASH_TOOL_NAME} ONLY for read-only operations (ls, git status, git log, git diff, find${embedded ? ', grep' : ''}, cat, head, tail)
- NEVER use ${BASH_TOOL_NAME} for: mkdir, touch, rm, cp, mv, git add, git commit, npm install, pip install, or any file creation/modification
- Adapt your search approach based on the thoroughness level specified by the caller
- Communicate your final report directly as a regular message - do NOT attempt to create files

```

---


### `src/tools/AgentTool/built-in/generalPurposeAgent.ts`

**信息:**
- 行数: 34
- 大小: 2185 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { BuiltInAgentDefinition } from '../loadAgentsDir.js'

const SHARED_PREFIX = `You are an agent for Claude Code, Anthropic's official CLI for Claude. Given the user's message, you should use the tools available to complete the task. Complete the task fully—don't gold-plate, but don't leave it half-done.`

const SHARED_GUIDELINES = `Your strengths:
- Searching for code, configurations, and patterns across large codebases
- Analyzing multiple files to understand system architecture
- Investigating complex questions that require exploring many files
- Performing multi-step research tasks

Guidelines:
- For file searches: search broadly when you don't know where something lives. Use Read when you know the specific file path.
- For analysis: Start broad and narrow down. Use multiple search strategies if the first doesn't yield results.
- Be thorough: Check multiple locations, consider different naming conventions, look for related files.
- NEVER create files unless they're absolutely necessary for achieving your goal. ALWAYS prefer editing an existing file to creating a new one.
- NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested.`

// Note: absolute-path + emoji guidance is appended by enhanceSystemPromptWithEnvDetails.
function getGeneralPurposeSystemPrompt(): string {
  return `${SHARED_PREFIX} When you complete the task, respond with a concise report covering what was done and any key findings — the caller will relay this to the user, so it only needs the essentials.

${SHARED_GUIDELINES}`
}

export const GENERAL_PURPOSE_AGENT: BuiltInAgentDefinition = {
  agentType: 'general-purpose',
  whenToUse:
    'General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks. When you are searching for a keyword or file and are not confident that you will find the right match in the first few tries use this agent to perform the search for you.',
  tools: ['*'],
  source: 'built-in',
  baseDir: 'built-in',
  // model is intentionally omitted - uses getDefaultSubagentModel().
  getSystemPrompt: getGeneralPurposeSystemPrompt,
}

```

---


### `src/tools/AgentTool/built-in/planAgent.ts`

**信息:**
- 行数: 92
- 大小: 4318 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { BASH_TOOL_NAME } from 'src/tools/BashTool/toolName.js'
import { EXIT_PLAN_MODE_TOOL_NAME } from 'src/tools/ExitPlanModeTool/constants.js'
import { FILE_EDIT_TOOL_NAME } from 'src/tools/FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from 'src/tools/FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from 'src/tools/FileWriteTool/prompt.js'
import { GLOB_TOOL_NAME } from 'src/tools/GlobTool/prompt.js'
import { GREP_TOOL_NAME } from 'src/tools/GrepTool/prompt.js'
import { NOTEBOOK_EDIT_TOOL_NAME } from 'src/tools/NotebookEditTool/constants.js'
import { hasEmbeddedSearchTools } from 'src/utils/embeddedTools.js'
import { AGENT_TOOL_NAME } from '../constants.js'
import type { BuiltInAgentDefinition } from '../loadAgentsDir.js'
import { EXPLORE_AGENT } from './exploreAgent.js'

function getPlanV2SystemPrompt(): string {
  // Ant-native builds alias find/grep to embedded bfs/ugrep and remove the
  // dedicated Glob/Grep tools, so point at find/grep instead.
  const searchToolsHint = hasEmbeddedSearchTools()
    ? `\`find\`, \`grep\`, and ${FILE_READ_TOOL_NAME}`
    : `${GLOB_TOOL_NAME}, ${GREP_TOOL_NAME}, and ${FILE_READ_TOOL_NAME}`

  return `You are a software architect and planning specialist for Claude Code. Your role is to explore the codebase and design implementation plans.

=== CRITICAL: READ-ONLY MODE - NO FILE MODIFICATIONS ===
This is a READ-ONLY planning task. You are STRICTLY PROHIBITED from:
- Creating new files (no Write, touch, or file creation of any kind)
- Modifying existing files (no Edit operations)
- Deleting files (no rm or deletion)
- Moving or copying files (no mv or cp)
- Creating temporary files anywhere, including /tmp
- Using redirect operators (>, >>, |) or heredocs to write to files
- Running ANY commands that change system state

Your role is EXCLUSIVELY to explore the codebase and design implementation plans. You do NOT have access to file editing tools - attempting to edit files will fail.

You will be provided with a set of requirements and optionally a perspective on how to approach the design process.

## Your Process

1. **Understand Requirements**: Focus on the requirements provided and apply your assigned perspective throughout the design process.

2. **Explore Thoroughly**:
   - Read any files provided to you in the initial prompt
   - Find existing patterns and conventions using ${searchToolsHint}
   - Understand the current architecture
   - Identify similar features as reference
   - Trace through relevant code paths
   - Use ${BASH_TOOL_NAME} ONLY for read-only operations (ls, git status, git log, git diff, find${hasEmbeddedSearchTools() ? ', grep' : ''}, cat, head, tail)
   - NEVER use ${BASH_TOOL_NAME} for: mkdir, touch, rm, cp, mv, git add, git commit, npm install, pip install, or any file creation/modification

3. **Design Solution**:

```

---


### `src/tools/AgentTool/built-in/statuslineSetup.ts`

**信息:**
- 行数: 144
- 大小: 7477 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { BuiltInAgentDefinition } from '../loadAgentsDir.js'

const STATUSLINE_SYSTEM_PROMPT = `You are a status line setup agent for Claude Code. Your job is to create or update the statusLine command in the user's Claude Code settings.

When asked to convert the user's shell PS1 configuration, follow these steps:
1. Read the user's shell configuration files in this order of preference:
   - ~/.zshrc
   - ~/.bashrc  
   - ~/.bash_profile
   - ~/.profile

2. Extract the PS1 value using this regex pattern: /(?:^|\\n)\\s*(?:export\\s+)?PS1\\s*=\\s*["']([^"']+)["']/m

3. Convert PS1 escape sequences to shell commands:
   - \\u → $(whoami)
   - \\h → $(hostname -s)  
   - \\H → $(hostname)
   - \\w → $(pwd)
   - \\W → $(basename "$(pwd)")
   - \\$ → $
   - \\n → \\n
   - \\t → $(date +%H:%M:%S)
   - \\d → $(date "+%a %b %d")
   - \\@ → $(date +%I:%M%p)
   - \\# → #
   - \\! → !

4. When using ANSI color codes, be sure to use \`printf\`. Do not remove colors. Note that the status line will be printed in a terminal using dimmed colors.

5. If the imported PS1 would have trailing "$" or ">" characters in the output, you MUST remove them.

6. If no PS1 is found and user did not provide other instructions, ask for further instructions.

How to use the statusLine command:
1. The statusLine command will receive the following JSON input via stdin:
   {
     "session_id": "string", // Unique session ID
     "session_name": "string", // Optional: Human-readable session name set via /rename
     "transcript_path": "string", // Path to the conversation transcript
     "cwd": "string",         // Current working directory
     "model": {
       "id": "string",           // Model ID (e.g., "claude-3-5-sonnet-20241022")
       "display_name": "string"  // Display name (e.g., "Claude 3.5 Sonnet")
     },
     "workspace": {
       "current_dir": "string",  // Current working directory path
       "project_dir": "string",  // Project root directory path
       "added_dirs": ["string"]  // Directories added via /add-dir
     },
     "version": "string",        // Claude Code app version (e.g., "1.0.71")

```

---


### `src/tools/AgentTool/built-in/verificationAgent.ts`

**信息:**
- 行数: 152
- 大小: 11410 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { BASH_TOOL_NAME } from 'src/tools/BashTool/toolName.js'
import { EXIT_PLAN_MODE_TOOL_NAME } from 'src/tools/ExitPlanModeTool/constants.js'
import { FILE_EDIT_TOOL_NAME } from 'src/tools/FileEditTool/constants.js'
import { FILE_WRITE_TOOL_NAME } from 'src/tools/FileWriteTool/prompt.js'
import { NOTEBOOK_EDIT_TOOL_NAME } from 'src/tools/NotebookEditTool/constants.js'
import { WEB_FETCH_TOOL_NAME } from 'src/tools/WebFetchTool/prompt.js'
import { AGENT_TOOL_NAME } from '../constants.js'
import type { BuiltInAgentDefinition } from '../loadAgentsDir.js'

const VERIFICATION_SYSTEM_PROMPT = `You are a verification specialist. Your job is not to confirm the implementation works — it's to try to break it.

You have two documented failure patterns. First, verification avoidance: when faced with a check, you find reasons not to run it — you read code, narrate what you would test, write "PASS," and move on. Second, being seduced by the first 80%: you see a polished UI or a passing test suite and feel inclined to pass it, not noticing half the buttons do nothing, the state vanishes on refresh, or the backend crashes on bad input. The first 80% is the easy part. Your entire value is in finding the last 20%. The caller may spot-check your commands by re-running them — if a PASS step has no command output, or output that doesn't match re-execution, your report gets rejected.

=== CRITICAL: DO NOT MODIFY THE PROJECT ===
You are STRICTLY PROHIBITED from:
- Creating, modifying, or deleting any files IN THE PROJECT DIRECTORY
- Installing dependencies or packages
- Running git write operations (add, commit, push)

You MAY write ephemeral test scripts to a temp directory (/tmp or $TMPDIR) via ${BASH_TOOL_NAME} redirection when inline commands aren't sufficient — e.g., a multi-step race harness or a Playwright test. Clean up after yourself.

Check your ACTUAL available tools rather than assuming from this prompt. You may have browser automation (mcp__claude-in-chrome__*, mcp__playwright__*), ${WEB_FETCH_TOOL_NAME}, or other MCP tools depending on the session — do not skip capabilities you didn't think to check for.

=== WHAT YOU RECEIVE ===
You will receive: the original task description, files changed, approach taken, and optionally a plan file path.

=== VERIFICATION STRATEGY ===
Adapt your strategy based on what was changed:

**Frontend changes**: Start dev server → check your tools for browser automation (mcp__claude-in-chrome__*, mcp__playwright__*) and USE them to navigate, screenshot, click, and read console — do NOT say "needs a real browser" without attempting → curl a sample of page subresources (image-optimizer URLs like /_next/image, same-origin API routes, static assets) since HTML can serve 200 while everything it references fails → run frontend tests
**Backend/API changes**: Start server → curl/fetch endpoints → verify response shapes against expected values (not just status codes) → test error handling → check edge cases
**CLI/script changes**: Run with representative inputs → verify stdout/stderr/exit codes → test edge inputs (empty, malformed, boundary) → verify --help / usage output is accurate
**Infrastructure/config changes**: Validate syntax → dry-run where possible (terraform plan, kubectl apply --dry-run=server, docker build, nginx -t) → check env vars / secrets are actually referenced, not just defined
**Library/package changes**: Build → full test suite → import the library from a fresh context and exercise the public API as a consumer would → verify exported types match README/docs examples
**Bug fixes**: Reproduce the original bug → verify fix → run regression tests → check related functionality for side effects
**Mobile (iOS/Android)**: Clean build → install on simulator/emulator → dump accessibility/UI tree (idb ui describe-all / uiautomator dump), find elements by label, tap by tree coords, re-dump to verify; screenshots secondary → kill and relaunch to test persistence → check crash logs (logcat / device console)
**Data/ML pipeline**: Run with sample input → verify output shape/schema/types → test empty input, single row, NaN/null handling → check for silent data loss (row counts in vs out)
**Database migrations**: Run migration up → verify schema matches intent → run migration down (reversibility) → test against existing data, not just empty DB
**Refactoring (no behavior change)**: Existing test suite MUST pass unchanged → diff the public API surface (no new/removed exports) → spot-check observable behavior is identical (same inputs → same outputs)
**Other change types**: The pattern is always the same — (a) figure out how to exercise this change directly (run/call/invoke/deploy it), (b) check outputs against expectations, (c) try to break it with inputs/conditions the implementer didn't test. The strategies above are worked examples for common cases.

=== REQUIRED STEPS (universal baseline) ===
1. Read the project's CLAUDE.md / README for build/test commands and conventions. Check package.json / Makefile / pyproject.toml for script names. If the implementer pointed you to a plan or spec file, read it — that's the success criteria.
2. Run the build (if applicable). A broken build is an automatic FAIL.
3. Run the project's test suite (if it has one). Failing tests are an automatic FAIL.
4. Run linters/type-checkers if configured (eslint, tsc, mypy, etc.).
5. Check for regressions in related code.

Then apply the type-specific strategy above. Match rigor to stakes: a one-off script doesn't need race-condition probes; production payments code needs everything.


```

---


### `src/tools/AgentTool/builtInAgents.ts`

**信息:**
- 行数: 72
- 大小: 2756 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { getIsNonInteractiveSession } from '../../bootstrap/state.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { CLAUDE_CODE_GUIDE_AGENT } from './built-in/claudeCodeGuideAgent.js'
import { EXPLORE_AGENT } from './built-in/exploreAgent.js'
import { GENERAL_PURPOSE_AGENT } from './built-in/generalPurposeAgent.js'
import { PLAN_AGENT } from './built-in/planAgent.js'
import { STATUSLINE_SETUP_AGENT } from './built-in/statuslineSetup.js'
import { VERIFICATION_AGENT } from './built-in/verificationAgent.js'
import type { AgentDefinition } from './loadAgentsDir.js'

export function areExplorePlanAgentsEnabled(): boolean {
  if (feature('BUILTIN_EXPLORE_PLAN_AGENTS')) {
    // 3P default: true — Bedrock/Vertex keep agents enabled (matches pre-experiment
    // external behavior). A/B test treatment sets false to measure impact of removal.
    return getFeatureValue_CACHED_MAY_BE_STALE('tengu_amber_stoat', true)
  }
  return false
}

export function getBuiltInAgents(): AgentDefinition[] {
  // Allow disabling all built-in agents via env var (useful for SDK users who want a blank slate)
  // Only applies in noninteractive mode (SDK/API usage)
  if (
    isEnvTruthy(process.env.CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS) &&
    getIsNonInteractiveSession()
  ) {
    return []
  }

  // Use lazy require inside the function body to avoid circular dependency
  // issues at module init time. The coordinatorMode module depends on tools
  // which depend on AgentTool which imports this file.
  if (feature('COORDINATOR_MODE')) {
    if (isEnvTruthy(process.env.CLAUDE_CODE_COORDINATOR_MODE)) {
      /* eslint-disable @typescript-eslint/no-require-imports */
      const { getCoordinatorAgents } =
        require('../../coordinator/workerAgent.js') as typeof import('../../coordinator/workerAgent.js')
      /* eslint-enable @typescript-eslint/no-require-imports */
      return getCoordinatorAgents()
    }
  }

  const agents: AgentDefinition[] = [
    GENERAL_PURPOSE_AGENT,
    STATUSLINE_SETUP_AGENT,
  ]

  if (areExplorePlanAgentsEnabled()) {

```

---


### `src/tools/AgentTool/constants.ts`

**信息:**
- 行数: 12
- 大小: 547 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const AGENT_TOOL_NAME = 'Agent'
// Legacy wire name for backward compat (permission rules, hooks, resumed sessions)
export const LEGACY_AGENT_TOOL_NAME = 'Task'
export const VERIFICATION_AGENT_TYPE = 'verification'

// Built-in agents that run once and return a report — the parent never
// SendMessages back to continue them. Skip the agentId/SendMessage/usage
// trailer for these to save tokens (~135 chars × 34M Explore runs/week).
export const ONE_SHOT_BUILTIN_AGENT_TYPES: ReadonlySet<string> = new Set([
  'Explore',
  'Plan',
])

```

---


### `src/tools/AgentTool/forkSubagent.ts`

**信息:**
- 行数: 210
- 大小: 8678 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { BetaToolUseBlock } from '@anthropic-ai/sdk/resources/beta/messages/messages.mjs'
import { randomUUID } from 'crypto'
import { getIsNonInteractiveSession } from '../../bootstrap/state.js'
import {
  FORK_BOILERPLATE_TAG,
  FORK_DIRECTIVE_PREFIX,
} from '../../constants/xml.js'
import { isCoordinatorMode } from '../../coordinator/coordinatorMode.js'
import type {
  AssistantMessage,
  Message as MessageType,
} from '../../types/message.js'
import { logForDebugging } from '../../utils/debug.js'
import { createUserMessage } from '../../utils/messages.js'
import type { BuiltInAgentDefinition } from './loadAgentsDir.js'

/**
 * Fork subagent feature gate.
 *
 * When enabled:
 * - `subagent_type` becomes optional on the Agent tool schema
 * - Omitting `subagent_type` triggers an implicit fork: the child inherits
 *   the parent's full conversation context and system prompt
 * - All agent spawns run in the background (async) for a unified
 *   `<task-notification>` interaction model
 * - `/fork <directive>` slash command is available
 *
 * Mutually exclusive with coordinator mode — coordinator already owns the
 * orchestration role and has its own delegation model.
 */
export function isForkSubagentEnabled(): boolean {
  if (feature('FORK_SUBAGENT')) {
    if (isCoordinatorMode()) return false
    if (getIsNonInteractiveSession()) return false
    return true
  }
  return false
}

/** Synthetic agent type name used for analytics when the fork path fires. */
export const FORK_SUBAGENT_TYPE = 'fork'

/**
 * Synthetic agent definition for the fork path.
 *
 * Not registered in builtInAgents — used only when `!subagent_type` and the
 * experiment is active. `tools: ['*']` with `useExactTools` means the fork
 * child receives the parent's exact tool pool (for cache-identical API
 * prefixes). `permissionMode: 'bubble'` surfaces permission prompts to the

```

---


### `src/tools/AgentTool/loadAgentsDir.ts`

**信息:**
- 行数: 755
- 大小: 26220 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import memoize from 'lodash-es/memoize.js'
import { basename } from 'path'
import type { SettingSource } from 'src/utils/settings/constants.js'
import { z } from 'zod/v4'
import { isAutoMemoryEnabled } from '../../memdir/paths.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import {
  type McpServerConfig,
  McpServerConfigSchema,
} from '../../services/mcp/types.js'
import type { ToolUseContext } from '../../Tool.js'
import { logForDebugging } from '../../utils/debug.js'
import {
  EFFORT_LEVELS,
  type EffortValue,
  parseEffortValue,
} from '../../utils/effort.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { parsePositiveIntFromFrontmatter } from '../../utils/frontmatterParser.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { logError } from '../../utils/log.js'
import {
  loadMarkdownFilesForSubdir,
  parseAgentToolsFromFrontmatter,
  parseSlashCommandToolsFromFrontmatter,
} from '../../utils/markdownConfigLoader.js'
import {
  PERMISSION_MODES,
  type PermissionMode,
} from '../../utils/permissions/PermissionMode.js'
import {
  clearPluginAgentCache,
  loadPluginAgents,
} from '../../utils/plugins/loadPluginAgents.js'
import { HooksSchema, type HooksSettings } from '../../utils/settings/types.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { FILE_EDIT_TOOL_NAME } from '../FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from '../FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from '../FileWriteTool/prompt.js'
import {
  AGENT_COLORS,
  type AgentColorName,
  setAgentColor,
} from './agentColorManager.js'
import { type AgentMemoryScope, loadAgentMemoryPrompt } from './agentMemory.js'
import {

```

---


### `src/tools/AgentTool/prompt.ts`

**信息:**
- 行数: 287
- 大小: 16671 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import { getSubscriptionType } from '../../utils/auth.js'
import { hasEmbeddedSearchTools } from '../../utils/embeddedTools.js'
import { isEnvDefinedFalsy, isEnvTruthy } from '../../utils/envUtils.js'
import { isTeammate } from '../../utils/teammate.js'
import { isInProcessTeammate } from '../../utils/teammateContext.js'
import { FILE_READ_TOOL_NAME } from '../FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from '../FileWriteTool/prompt.js'
import { GLOB_TOOL_NAME } from '../GlobTool/prompt.js'
import { SEND_MESSAGE_TOOL_NAME } from '../SendMessageTool/constants.js'
import { AGENT_TOOL_NAME } from './constants.js'
import { isForkSubagentEnabled } from './forkSubagent.js'
import type { AgentDefinition } from './loadAgentsDir.js'

function getToolsDescription(agent: AgentDefinition): string {
  const { tools, disallowedTools } = agent
  const hasAllowlist = tools && tools.length > 0
  const hasDenylist = disallowedTools && disallowedTools.length > 0

  if (hasAllowlist && hasDenylist) {
    // Both defined: filter allowlist by denylist to match runtime behavior
    const denySet = new Set(disallowedTools)
    const effectiveTools = tools.filter(t => !denySet.has(t))
    if (effectiveTools.length === 0) {
      return 'None'
    }
    return effectiveTools.join(', ')
  } else if (hasAllowlist) {
    // Allowlist only: show the specific tools available
    return tools.join(', ')
  } else if (hasDenylist) {
    // Denylist only: show "All tools except X, Y, Z"
    return `All tools except ${disallowedTools.join(', ')}`
  }
  // No restrictions
  return 'All tools'
}

/**
 * Format one agent line for the agent_listing_delta attachment message:
 * `- type: whenToUse (Tools: ...)`.
 */
export function formatAgentLine(agent: AgentDefinition): string {
  const toolsDescription = getToolsDescription(agent)
  return `- ${agent.agentType}: ${agent.whenToUse} (Tools: ${toolsDescription})`
}

/**
 * Whether the agent list should be injected as an attachment message instead
 * of embedded in the tool description. When true, getPrompt() returns a static

```

---


### `src/tools/AgentTool/resumeAgent.ts`

**信息:**
- 行数: 265
- 大小: 9339 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { promises as fsp } from 'fs'
import { getSdkAgentProgressSummariesEnabled } from '../../bootstrap/state.js'
import { getSystemPrompt } from '../../constants/prompts.js'
import { isCoordinatorMode } from '../../coordinator/coordinatorMode.js'
import type { CanUseToolFn } from '../../hooks/useCanUseTool.js'
import type { ToolUseContext } from '../../Tool.js'
import { registerAsyncAgent } from '../../tasks/LocalAgentTask/LocalAgentTask.js'
import { assembleToolPool } from '../../tools.js'
import { asAgentId } from '../../types/ids.js'
import { runWithAgentContext } from '../../utils/agentContext.js'
import { runWithCwdOverride } from '../../utils/cwd.js'
import { logForDebugging } from '../../utils/debug.js'
import {
  createUserMessage,
  filterOrphanedThinkingOnlyMessages,
  filterUnresolvedToolUses,
  filterWhitespaceOnlyAssistantMessages,
} from '../../utils/messages.js'
import { getAgentModel } from '../../utils/model/agent.js'
import { getQuerySourceForAgent } from '../../utils/promptCategory.js'
import {
  getAgentTranscript,
  readAgentMetadata,
} from '../../utils/sessionStorage.js'
import { buildEffectiveSystemPrompt } from '../../utils/systemPrompt.js'
import type { SystemPrompt } from '../../utils/systemPromptType.js'
import { getTaskOutputPath } from '../../utils/task/diskOutput.js'
import { getParentSessionId } from '../../utils/teammate.js'
import { reconstructForSubagentResume } from '../../utils/toolResultStorage.js'
import { runAsyncAgentLifecycle } from './agentToolUtils.js'
import { GENERAL_PURPOSE_AGENT } from './built-in/generalPurposeAgent.js'
import { FORK_AGENT, isForkSubagentEnabled } from './forkSubagent.js'
import type { AgentDefinition } from './loadAgentsDir.js'
import { isBuiltInAgent } from './loadAgentsDir.js'
import { runAgent } from './runAgent.js'

export type ResumeAgentResult = {
  agentId: string
  description: string
  outputFile: string
}
export async function resumeAgentBackground({
  agentId,
  prompt,
  toolUseContext,
  canUseTool,
  invokingRequestId,
}: {
  agentId: string
  prompt: string

```

---


### `src/tools/AgentTool/runAgent.ts`

**信息:**
- 行数: 973
- 大小: 35768 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { UUID } from 'crypto'
import { randomUUID } from 'crypto'
import uniqBy from 'lodash-es/uniqBy.js'
import { logForDebugging } from 'src/utils/debug.js'
import { getProjectRoot, getSessionId } from '../../bootstrap/state.js'
import { getCommand, getSkillToolCommands, hasCommand } from '../../commands.js'
import {
  DEFAULT_AGENT_PROMPT,
  enhanceSystemPromptWithEnvDetails,
} from '../../constants/prompts.js'
import type { QuerySource } from '../../constants/querySource.js'
import { getSystemContext, getUserContext } from '../../context.js'
import type { CanUseToolFn } from '../../hooks/useCanUseTool.js'
import { query } from '../../query.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import { getDumpPromptsPath } from '../../services/api/dumpPrompts.js'
import { cleanupAgentTracking } from '../../services/api/promptCacheBreakDetection.js'
import {
  connectToServer,
  fetchToolsForClient,
} from '../../services/mcp/client.js'
import { getMcpConfigByName } from '../../services/mcp/config.js'
import type {
  MCPServerConnection,
  ScopedMcpServerConfig,
} from '../../services/mcp/types.js'
import type { Tool, Tools, ToolUseContext } from '../../Tool.js'
import { killShellTasksForAgent } from '../../tasks/LocalShellTask/killShellTasks.js'
import type { Command } from '../../types/command.js'
import type { AgentId } from '../../types/ids.js'
import type {
  AssistantMessage,
  Message,
  ProgressMessage,
  RequestStartEvent,
  StreamEvent,
  SystemCompactBoundaryMessage,
  TombstoneMessage,
  ToolUseSummaryMessage,
  UserMessage,
} from '../../types/message.js'
import { createAttachmentMessage } from '../../utils/attachments.js'
import { AbortError } from '../../utils/errors.js'
import { getDisplayPath } from '../../utils/file.js'
import {
  cloneFileStateCache,
  createFileStateCacheWithSizeLimit,
  READ_FILE_STATE_CACHE_SIZE,
} from '../../utils/fileStateCache.js'

```

---


### `src/tools/AskUserQuestionTool/AskUserQuestionTool.tsx`

**信息:**
- 行数: 266
- 大小: 39887 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import * as React from 'react';
import { getAllowedChannels, getQuestionPreviewFormat } from 'src/bootstrap/state.js';
import { MessageResponse } from 'src/components/MessageResponse.js';
import { BLACK_CIRCLE } from 'src/constants/figures.js';
import { getModeColor } from 'src/utils/permissions/PermissionMode.js';
import { z } from 'zod/v4';
import { Box, Text } from '../../ink.js';
import type { Tool } from '../../Tool.js';
import { buildTool, type ToolDef } from '../../Tool.js';
import { lazySchema } from '../../utils/lazySchema.js';
import { ASK_USER_QUESTION_TOOL_CHIP_WIDTH, ASK_USER_QUESTION_TOOL_NAME, ASK_USER_QUESTION_TOOL_PROMPT, DESCRIPTION, PREVIEW_FEATURE_PROMPT } from './prompt.js';
const questionOptionSchema = lazySchema(() => z.object({
  label: z.string().describe('The display text for this option that the user will see and select. Should be concise (1-5 words) and clearly describe the choice.'),
  description: z.string().describe('Explanation of what this option means or what will happen if chosen. Useful for providing context about trade-offs or implications.'),
  preview: z.string().optional().describe('Optional preview content rendered when this option is focused. Use for mockups, code snippets, or visual comparisons that help users compare options. See the tool description for the expected content format.')
}));
const questionSchema = lazySchema(() => z.object({
  question: z.string().describe('The complete question to ask the user. Should be clear, specific, and end with a question mark. Example: "Which library should we use for date formatting?" If multiSelect is true, phrase it accordingly, e.g. "Which features do you want to enable?"'),
  header: z.string().describe(`Very short label displayed as a chip/tag (max ${ASK_USER_QUESTION_TOOL_CHIP_WIDTH} chars). Examples: "Auth method", "Library", "Approach".`),
  options: z.array(questionOptionSchema()).min(2).max(4).describe(`The available choices for this question. Must have 2-4 options. Each option should be a distinct, mutually exclusive choice (unless multiSelect is enabled). There should be no 'Other' option, that will be provided automatically.`),
  multiSelect: z.boolean().default(false).describe('Set to true to allow the user to select multiple options instead of just one. Use when choices are not mutually exclusive.')
}));
const annotationsSchema = lazySchema(() => {
  const annotationSchema = z.object({
    preview: z.string().optional().describe('The preview content of the selected option, if the question used previews.'),
    notes: z.string().optional().describe('Free-text notes the user added to their selection.')
  });
  return z.record(z.string(), annotationSchema).optional().describe('Optional per-question annotations from the user (e.g., notes on preview selections). Keyed by question text.');
});
const UNIQUENESS_REFINE = {
  check: (data: {
    questions: {
      question: string;
      options: {
        label: string;
      }[];
    }[];
  }) => {
    const questions = data.questions.map(q => q.question);
    if (questions.length !== new Set(questions).size) {
      return false;
    }
    for (const question of data.questions) {
      const labels = question.options.map(opt => opt.label);
      if (labels.length !== new Set(labels).size) {
        return false;
      }
    }

```

---


### `src/tools/AskUserQuestionTool/prompt.ts`

**信息:**
- 行数: 44
- 大小: 2903 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { EXIT_PLAN_MODE_TOOL_NAME } from '../ExitPlanModeTool/constants.js'

export const ASK_USER_QUESTION_TOOL_NAME = 'AskUserQuestion'

export const ASK_USER_QUESTION_TOOL_CHIP_WIDTH = 12

export const DESCRIPTION =
  'Asks the user multiple choice questions to gather information, clarify ambiguity, understand preferences, make decisions or offer them choices.'

export const PREVIEW_FEATURE_PROMPT = {
  markdown: `
Preview feature:
Use the optional \`preview\` field on options when presenting concrete artifacts that users need to visually compare:
- ASCII mockups of UI layouts or components
- Code snippets showing different implementations
- Diagram variations
- Configuration examples

Preview content is rendered as markdown in a monospace box. Multi-line text with newlines is supported. When any option has a preview, the UI switches to a side-by-side layout with a vertical option list on the left and preview on the right. Do not use previews for simple preference questions where labels and descriptions suffice. Note: previews are only supported for single-select questions (not multiSelect).
`,
  html: `
Preview feature:
Use the optional \`preview\` field on options when presenting concrete artifacts that users need to visually compare:
- HTML mockups of UI layouts or components
- Formatted code snippets showing different implementations
- Visual comparisons or diagrams

Preview content must be a self-contained HTML fragment (no <html>/<body> wrapper, no <script> or <style> tags — use inline style attributes instead). Do not use previews for simple preference questions where labels and descriptions suffice. Note: previews are only supported for single-select questions (not multiSelect).
`,
} as const

export const ASK_USER_QUESTION_TOOL_PROMPT = `Use this tool when you need to ask the user questions during execution. This allows you to:
1. Gather user preferences or requirements
2. Clarify ambiguous instructions
3. Get decisions on implementation choices as you work
4. Offer choices to the user about what direction to take.

Usage notes:
- Users will always be able to select "Other" to provide custom text input
- Use multiSelect: true to allow multiple answers to be selected for a question
- If you recommend a specific option, make that the first option in the list and add "(Recommended)" at the end of the label

Plan mode note: In plan mode, use this tool to clarify requirements or choose between approaches BEFORE finalizing your plan. Do NOT use this tool to ask "Is my plan ready?" or "Should I proceed?" - use ${EXIT_PLAN_MODE_TOOL_NAME} for plan approval. IMPORTANT: Do not reference "the plan" in your questions (e.g., "Do you have feedback about the plan?", "Does the plan look good?") because the user cannot see the plan in the UI until you call ${EXIT_PLAN_MODE_TOOL_NAME}. If you need plan approval, use ${EXIT_PLAN_MODE_TOOL_NAME} instead.
`

```

---


### `src/tools/BashTool/BashTool.tsx`

**信息:**
- 行数: 1144
- 大小: 160530 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import { copyFile, stat as fsStat, truncate as fsTruncate, link } from 'fs/promises';
import * as React from 'react';
import type { CanUseToolFn } from 'src/hooks/useCanUseTool.js';
import type { AppState } from 'src/state/AppState.js';
import { z } from 'zod/v4';
import { getKairosActive } from '../../bootstrap/state.js';
import { TOOL_SUMMARY_MAX_LENGTH } from '../../constants/toolLimits.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../services/analytics/index.js';
import { notifyVscodeFileUpdated } from '../../services/mcp/vscodeSdkMcp.js';
import type { SetToolJSXFn, ToolCallProgress, ToolUseContext, ValidationResult } from '../../Tool.js';
import { buildTool, type ToolDef } from '../../Tool.js';
import { backgroundExistingForegroundTask, markTaskNotified, registerForeground, spawnShellTask, unregisterForeground } from '../../tasks/LocalShellTask/LocalShellTask.js';
import type { AgentId } from '../../types/ids.js';
import type { AssistantMessage } from '../../types/message.js';
import { parseForSecurity } from '../../utils/bash/ast.js';
import { splitCommand_DEPRECATED, splitCommandWithOperators } from '../../utils/bash/commands.js';
import { extractClaudeCodeHints } from '../../utils/claudeCodeHints.js';
import { detectCodeIndexingFromCommand } from '../../utils/codeIndexing.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import { isENOENT, ShellError } from '../../utils/errors.js';
import { detectFileEncoding, detectLineEndings, getFileModificationTime, writeTextContent } from '../../utils/file.js';
import { fileHistoryEnabled, fileHistoryTrackEdit } from '../../utils/fileHistory.js';
import { truncate } from '../../utils/format.js';
import { getFsImplementation } from '../../utils/fsOperations.js';
import { lazySchema } from '../../utils/lazySchema.js';
import { expandPath } from '../../utils/path.js';
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js';
import { maybeRecordPluginHint } from '../../utils/plugins/hintRecommendation.js';
import { exec } from '../../utils/Shell.js';
import type { ExecResult } from '../../utils/ShellCommand.js';
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js';
import { semanticBoolean } from '../../utils/semanticBoolean.js';
import { semanticNumber } from '../../utils/semanticNumber.js';
import { EndTruncatingAccumulator } from '../../utils/stringUtils.js';
import { getTaskOutputPath } from '../../utils/task/diskOutput.js';
import { TaskOutput } from '../../utils/task/TaskOutput.js';
import { isOutputLineTruncated } from '../../utils/terminal.js';
import { buildLargeToolResultMessage, ensureToolResultsDir, generatePreview, getToolResultPath, PREVIEW_SIZE_BYTES } from '../../utils/toolResultStorage.js';
import { userFacingName as fileEditUserFacingName } from '../FileEditTool/UI.js';
import { trackGitOperations } from '../shared/gitOperationTracking.js';
import { bashToolHasPermission, commandHasAnyCd, matchWildcardPattern, permissionRuleExtractPrefix } from './bashPermissions.js';
import { interpretCommandResult } from './commandSemantics.js';
import { getDefaultTimeoutMs, getMaxTimeoutMs, getSimplePrompt } from './prompt.js';
import { checkReadOnlyConstraints } from './readOnlyValidation.js';
import { parseSedEditCommand } from './sedEditParser.js';
import { shouldUseSandbox } from './shouldUseSandbox.js';
import { BASH_TOOL_NAME } from './toolName.js';
import { BackgroundHint, renderToolResultMessage, renderToolUseErrorMessage, renderToolUseMessage, renderToolUseProgressMessage, renderToolUseQueuedMessage } from './UI.js';

```

---


### `src/tools/BashTool/BashToolResultMessage.tsx`

**信息:**
- 行数: 191
- 大小: 19215 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { removeSandboxViolationTags } from 'src/utils/sandbox/sandbox-ui-utils.js';
import { KeyboardShortcutHint } from '../../components/design-system/KeyboardShortcutHint.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { OutputLine } from '../../components/shell/OutputLine.js';
import { ShellTimeDisplay } from '../../components/shell/ShellTimeDisplay.js';
import { Box, Text } from '../../ink.js';
import type { Out as BashOut } from './BashTool.js';
type Props = {
  content: Omit<BashOut, 'interrupted'>;
  verbose: boolean;
  timeoutMs?: number;
};

// Pattern to match "Shell cwd was reset to <path>" message
// Use (?:^|\n) to match either start of string or after a newline
const SHELL_CWD_RESET_PATTERN = /(?:^|\n)(Shell cwd was reset to .+)$/;

/**
 * Extracts sandbox violations from stderr if present
 * Returns both the cleaned stderr and the violations content
 */
function extractSandboxViolations(stderr: string): {
  cleanedStderr: string;
} {
  const violationsMatch = stderr.match(/<sandbox_violations>([\s\S]*?)<\/sandbox_violations>/);
  if (!violationsMatch) {
    return {
      cleanedStderr: stderr
    };
  }

  // Remove the sandbox violations section from stderr
  const cleanedStderr = removeSandboxViolationTags(stderr).trim();
  return {
    cleanedStderr
  };
}

/**
 * Extracts the "Shell cwd was reset" warning message from stderr
 * Returns the cleaned stderr and the warning message separately
 */
function extractCwdResetWarning(stderr: string): {
  cleanedStderr: string;
  cwdResetWarning: string | null;
} {
  const match = stderr.match(SHELL_CWD_RESET_PATTERN);
  if (!match) {

```

---


### `src/tools/BashTool/UI.tsx`

**信息:**
- 行数: 185
- 大小: 25213 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import { KeyboardShortcutHint } from '../../components/design-system/KeyboardShortcutHint.js';
import { FallbackToolUseErrorMessage } from '../../components/FallbackToolUseErrorMessage.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { ShellProgressMessage } from '../../components/shell/ShellProgressMessage.js';
import { Box, Text } from '../../ink.js';
import { useKeybinding } from '../../keybindings/useKeybinding.js';
import { useShortcutDisplay } from '../../keybindings/useShortcutDisplay.js';
import { useAppStateStore, useSetAppState } from '../../state/AppState.js';
import type { Tool } from '../../Tool.js';
import { backgroundAll } from '../../tasks/LocalShellTask/LocalShellTask.js';
import type { ProgressMessage } from '../../types/message.js';
import { env } from '../../utils/env.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import { getDisplayPath } from '../../utils/file.js';
import { isFullscreenEnvEnabled } from '../../utils/fullscreen.js';
import type { ThemeName } from '../../utils/theme.js';
import type { BashProgress, BashToolInput, Out } from './BashTool.js';
import BashToolResultMessage from './BashToolResultMessage.js';
import { extractBashCommentLabel } from './commentLabel.js';
import { parseSedEditCommand } from './sedEditParser.js';

// Constants for command display
const MAX_COMMAND_DISPLAY_LINES = 2;
const MAX_COMMAND_DISPLAY_CHARS = 160;

// Simple component to show background hint and handle ctrl+b
// When ctrl+b is pressed, backgrounds ALL running foreground commands
export function BackgroundHint(t0) {
  const $ = _c(9);
  let t1;
  if ($[0] !== t0) {
    t1 = t0 === undefined ? {} : t0;
    $[0] = t0;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const {
    onBackground
  } = t1;
  const store = useAppStateStore();
  const setAppState = useSetAppState();
  let t2;
  if ($[2] !== onBackground || $[3] !== setAppState || $[4] !== store) {
    t2 = () => {
      backgroundAll(() => store.getState(), setAppState);
      onBackground?.();

```

---


### `src/tools/BashTool/bashCommandHelpers.ts`

**信息:**
- 行数: 265
- 大小: 8589 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { z } from 'zod/v4'
import {
  isUnsafeCompoundCommand_DEPRECATED,
  splitCommand_DEPRECATED,
} from '../../utils/bash/commands.js'
import {
  buildParsedCommandFromRoot,
  type IParsedCommand,
  ParsedCommand,
} from '../../utils/bash/ParsedCommand.js'
import { type Node, PARSE_ABORTED } from '../../utils/bash/parser.js'
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js'
import type { PermissionUpdate } from '../../utils/permissions/PermissionUpdateSchema.js'
import { createPermissionRequestMessage } from '../../utils/permissions/permissions.js'
import { BashTool } from './BashTool.js'
import { bashCommandIsSafeAsync_DEPRECATED } from './bashSecurity.js'

export type CommandIdentityCheckers = {
  isNormalizedCdCommand: (command: string) => boolean
  isNormalizedGitCommand: (command: string) => boolean
}

async function segmentedCommandPermissionResult(
  input: z.infer<typeof BashTool.inputSchema>,
  segments: string[],
  bashToolHasPermissionFn: (
    input: z.infer<typeof BashTool.inputSchema>,
  ) => Promise<PermissionResult>,
  checkers: CommandIdentityCheckers,
): Promise<PermissionResult> {
  // Check for multiple cd commands across all segments
  const cdCommands = segments.filter(segment => {
    const trimmed = segment.trim()
    return checkers.isNormalizedCdCommand(trimmed)
  })
  if (cdCommands.length > 1) {
    const decisionReason = {
      type: 'other' as const,
      reason:
        'Multiple directory changes in one command require approval for clarity',
    }
    return {
      behavior: 'ask',
      decisionReason,
      message: createPermissionRequestMessage(BashTool.name, decisionReason),
    }
  }

  // SECURITY: Check for cd+git across pipe segments to prevent bare repo fsmonitor bypass.
  // When cd and git are in different pipe segments (e.g., "cd sub && echo | git status"),

```

---


### `src/tools/BashTool/bashPermissions.ts`

**信息:**
- 行数: 2621
- 大小: 98756 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { APIUserAbortError } from '@anthropic-ai/sdk'
import type { z } from 'zod/v4'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import type { ToolPermissionContext, ToolUseContext } from '../../Tool.js'
import type { PendingClassifierCheck } from '../../types/permissions.js'
import { count } from '../../utils/array.js'
import {
  checkSemantics,
  nodeTypeId,
  type ParseForSecurityResult,
  parseForSecurityFromAst,
  type Redirect,
  type SimpleCommand,
} from '../../utils/bash/ast.js'
import {
  type CommandPrefixResult,
  extractOutputRedirections,
  getCommandSubcommandPrefix,
  splitCommand_DEPRECATED,
} from '../../utils/bash/commands.js'
import { parseCommandRaw } from '../../utils/bash/parser.js'
import { tryParseShellCommand } from '../../utils/bash/shellQuote.js'
import { getCwd } from '../../utils/cwd.js'
import { logForDebugging } from '../../utils/debug.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { AbortError } from '../../utils/errors.js'
import type {
  ClassifierBehavior,
  ClassifierResult,
} from '../../utils/permissions/bashClassifier.js'
import {
  classifyBashCommand,
  getBashPromptAllowDescriptions,
  getBashPromptAskDescriptions,
  getBashPromptDenyDescriptions,
  isClassifierPermissionsEnabled,
} from '../../utils/permissions/bashClassifier.js'
import type {
  PermissionDecisionReason,
  PermissionResult,
} from '../../utils/permissions/PermissionResult.js'
import type {
  PermissionRule,
  PermissionRuleValue,
} from '../../utils/permissions/PermissionRule.js'

```

---


### `src/tools/BashTool/bashSecurity.ts`

**信息:**
- 行数: 2592
- 大小: 102561 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { logEvent } from 'src/services/analytics/index.js'
import { extractHeredocs } from '../../utils/bash/heredoc.js'
import { ParsedCommand } from '../../utils/bash/ParsedCommand.js'
import {
  hasMalformedTokens,
  hasShellQuoteSingleQuoteBug,
  tryParseShellCommand,
} from '../../utils/bash/shellQuote.js'
import type { TreeSitterAnalysis } from '../../utils/bash/treeSitterAnalysis.js'
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js'

const HEREDOC_IN_SUBSTITUTION = /\$\(.*<</

// Note: Backtick pattern is handled separately in validateDangerousPatterns
// to distinguish between escaped and unescaped backticks
const COMMAND_SUBSTITUTION_PATTERNS = [
  { pattern: /<\(/, message: 'process substitution <()' },
  { pattern: />\(/, message: 'process substitution >()' },
  { pattern: /=\(/, message: 'Zsh process substitution =()' },
  // Zsh EQUALS expansion: =cmd at word start expands to $(which cmd).
  // `=curl evil.com` → `/usr/bin/curl evil.com`, bypassing Bash(curl:*) deny
  // rules since the parser sees `=curl` as the base command, not `curl`.
  // Only matches word-initial = followed by a command-name char (not VAR=val).
  {
    pattern: /(?:^|[\s;&|])=[a-zA-Z_]/,
    message: 'Zsh equals expansion (=cmd)',
  },
  { pattern: /\$\(/, message: '$() command substitution' },
  { pattern: /\$\{/, message: '${} parameter substitution' },
  { pattern: /\$\[/, message: '$[] legacy arithmetic expansion' },
  { pattern: /~\[/, message: 'Zsh-style parameter expansion' },
  { pattern: /\(e:/, message: 'Zsh-style glob qualifiers' },
  { pattern: /\(\+/, message: 'Zsh glob qualifier with command execution' },
  {
    pattern: /\}\s*always\s*\{/,
    message: 'Zsh always block (try/always construct)',
  },
  // Defense in depth: Block PowerShell comment syntax even though we don't execute in PowerShell
  // Added as protection against future changes that might introduce PowerShell execution
  { pattern: /<#/, message: 'PowerShell comment syntax' },
]

// Zsh-specific dangerous commands that can bypass security checks.
// These are checked against the base command (first word) of each command segment.
const ZSH_DANGEROUS_COMMANDS = new Set([
  // zmodload is the gateway to many dangerous module-based attacks:
  // zsh/mapfile (invisible file I/O via array assignment),
  // zsh/system (sysopen/syswrite two-step file access),
  // zsh/zpty (pseudo-terminal command execution),
  // zsh/net/tcp (network exfiltration via ztcp),

```

---


### `src/tools/BashTool/commandSemantics.ts`

**信息:**
- 行数: 140
- 大小: 3658 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Command semantics configuration for interpreting exit codes in different contexts.
 *
 * Many commands use exit codes to convey information other than just success/failure.
 * For example, grep returns 1 when no matches are found, which is not an error condition.
 */

import { splitCommand_DEPRECATED } from '../../utils/bash/commands.js'

export type CommandSemantic = (
  exitCode: number,
  stdout: string,
  stderr: string,
) => {
  isError: boolean
  message?: string
}

/**
 * Default semantic: treat only 0 as success, everything else as error
 */
const DEFAULT_SEMANTIC: CommandSemantic = (exitCode, _stdout, _stderr) => ({
  isError: exitCode !== 0,
  message:
    exitCode !== 0 ? `Command failed with exit code ${exitCode}` : undefined,
})

/**
 * Command-specific semantics
 */
const COMMAND_SEMANTICS: Map<string, CommandSemantic> = new Map([
  // grep: 0=matches found, 1=no matches, 2+=error
  [
    'grep',
    (exitCode, _stdout, _stderr) => ({
      isError: exitCode >= 2,
      message: exitCode === 1 ? 'No matches found' : undefined,
    }),
  ],

  // ripgrep has same semantics as grep
  [
    'rg',
    (exitCode, _stdout, _stderr) => ({
      isError: exitCode >= 2,
      message: exitCode === 1 ? 'No matches found' : undefined,
    }),
  ],

  // find: 0=success, 1=partial success (some dirs inaccessible), 2+=error

```

---


### `src/tools/BashTool/commentLabel.ts`

**信息:**
- 行数: 13
- 大小: 637 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * If the first line of a bash command is a `# comment` (not a `#!` shebang),
 * return the comment text stripped of the `#` prefix. Otherwise undefined.
 *
 * Under fullscreen mode this is the non-verbose tool-use label AND the
 * collapse-group ⎿ hint — it's what Claude wrote for the human to read.
 */
export function extractBashCommentLabel(command: string): string | undefined {
  const nl = command.indexOf('\n')
  const firstLine = (nl === -1 ? command : command.slice(0, nl)).trim()
  if (!firstLine.startsWith('#') || firstLine.startsWith('#!')) return undefined
  return firstLine.replace(/^#+\s*/, '') || undefined
}

```

---


### `src/tools/BashTool/destructiveCommandWarning.ts`

**信息:**
- 行数: 102
- 大小: 2935 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Detects potentially destructive bash commands and returns a warning string
 * for display in the permission dialog. This is purely informational — it
 * doesn't affect permission logic or auto-approval.
 */

type DestructivePattern = {
  pattern: RegExp
  warning: string
}

const DESTRUCTIVE_PATTERNS: DestructivePattern[] = [
  // Git — data loss / hard to reverse
  {
    pattern: /\bgit\s+reset\s+--hard\b/,
    warning: 'Note: may discard uncommitted changes',
  },
  {
    pattern: /\bgit\s+push\b[^;&|\n]*[ \t](--force|--force-with-lease|-f)\b/,
    warning: 'Note: may overwrite remote history',
  },
  {
    pattern:
      /\bgit\s+clean\b(?![^;&|\n]*(?:-[a-zA-Z]*n|--dry-run))[^;&|\n]*-[a-zA-Z]*f/,
    warning: 'Note: may permanently delete untracked files',
  },
  {
    pattern: /\bgit\s+checkout\s+(--\s+)?\.[ \t]*($|[;&|\n])/,
    warning: 'Note: may discard all working tree changes',
  },
  {
    pattern: /\bgit\s+restore\s+(--\s+)?\.[ \t]*($|[;&|\n])/,
    warning: 'Note: may discard all working tree changes',
  },
  {
    pattern: /\bgit\s+stash[ \t]+(drop|clear)\b/,
    warning: 'Note: may permanently remove stashed changes',
  },
  {
    pattern:
      /\bgit\s+branch\s+(-D[ \t]|--delete\s+--force|--force\s+--delete)\b/,
    warning: 'Note: may force-delete a branch',
  },

  // Git — safety bypass
  {
    pattern: /\bgit\s+(commit|push|merge)\b[^;&|\n]*--no-verify\b/,
    warning: 'Note: may skip safety hooks',
  },
  {

```

---


### `src/tools/BashTool/modeValidation.ts`

**信息:**
- 行数: 115
- 大小: 3266 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { z } from 'zod/v4'
import type { ToolPermissionContext } from '../../Tool.js'
import { splitCommand_DEPRECATED } from '../../utils/bash/commands.js'
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js'
import type { BashTool } from './BashTool.js'

const ACCEPT_EDITS_ALLOWED_COMMANDS = [
  'mkdir',
  'touch',
  'rm',
  'rmdir',
  'mv',
  'cp',
  'sed',
] as const

type FilesystemCommand = (typeof ACCEPT_EDITS_ALLOWED_COMMANDS)[number]

function isFilesystemCommand(command: string): command is FilesystemCommand {
  return ACCEPT_EDITS_ALLOWED_COMMANDS.includes(command as FilesystemCommand)
}

function validateCommandForMode(
  cmd: string,
  toolPermissionContext: ToolPermissionContext,
): PermissionResult {
  const trimmedCmd = cmd.trim()
  const [baseCmd] = trimmedCmd.split(/\s+/)

  if (!baseCmd) {
    return {
      behavior: 'passthrough',
      message: 'Base command not found',
    }
  }

  // In Accept Edits mode, auto-allow filesystem operations
  if (
    toolPermissionContext.mode === 'acceptEdits' &&
    isFilesystemCommand(baseCmd)
  ) {
    return {
      behavior: 'allow',
      updatedInput: { command: cmd },
      decisionReason: {
        type: 'mode',
        mode: 'acceptEdits',
      },
    }
  }

```

---


### `src/tools/BashTool/pathValidation.ts`

**信息:**
- 行数: 1303
- 大小: 43679 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { homedir } from 'os'
import { isAbsolute, resolve } from 'path'
import type { z } from 'zod/v4'
import type { ToolPermissionContext } from '../../Tool.js'
import type { Redirect, SimpleCommand } from '../../utils/bash/ast.js'
import {
  extractOutputRedirections,
  splitCommand_DEPRECATED,
} from '../../utils/bash/commands.js'
import { tryParseShellCommand } from '../../utils/bash/shellQuote.js'
import { getDirectoryForPath } from '../../utils/path.js'
import { allWorkingDirectories } from '../../utils/permissions/filesystem.js'
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js'
import { createReadRuleSuggestion } from '../../utils/permissions/PermissionUpdate.js'
import type { PermissionUpdate } from '../../utils/permissions/PermissionUpdateSchema.js'
import {
  expandTilde,
  type FileOperationType,
  formatDirectoryList,
  isDangerousRemovalPath,
  validatePath,
} from '../../utils/permissions/pathValidation.js'
import type { BashTool } from './BashTool.js'
import { stripSafeWrappers } from './bashPermissions.js'
import { sedCommandIsAllowedByAllowlist } from './sedValidation.js'

export type PathCommand =
  | 'cd'
  | 'ls'
  | 'find'
  | 'mkdir'
  | 'touch'
  | 'rm'
  | 'rmdir'
  | 'mv'
  | 'cp'
  | 'cat'
  | 'head'
  | 'tail'
  | 'sort'
  | 'uniq'
  | 'wc'
  | 'cut'
  | 'paste'
  | 'column'
  | 'tr'
  | 'file'
  | 'stat'
  | 'diff'
  | 'awk'

```

---


### `src/tools/BashTool/prompt.ts`

**信息:**
- 行数: 369
- 大小: 21130 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { prependBullets } from '../../constants/prompts.js'
import { getAttributionTexts } from '../../utils/attribution.js'
import { hasEmbeddedSearchTools } from '../../utils/embeddedTools.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { shouldIncludeGitInstructions } from '../../utils/gitSettings.js'
import { getClaudeTempDir } from '../../utils/permissions/filesystem.js'
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import {
  getDefaultBashTimeoutMs,
  getMaxBashTimeoutMs,
} from '../../utils/timeouts.js'
import {
  getUndercoverInstructions,
  isUndercover,
} from '../../utils/undercover.js'
import { AGENT_TOOL_NAME } from '../AgentTool/constants.js'
import { FILE_EDIT_TOOL_NAME } from '../FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from '../FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from '../FileWriteTool/prompt.js'
import { GLOB_TOOL_NAME } from '../GlobTool/prompt.js'
import { GREP_TOOL_NAME } from '../GrepTool/prompt.js'
import { TodoWriteTool } from '../TodoWriteTool/TodoWriteTool.js'
import { BASH_TOOL_NAME } from './toolName.js'

export function getDefaultTimeoutMs(): number {
  return getDefaultBashTimeoutMs()
}

export function getMaxTimeoutMs(): number {
  return getMaxBashTimeoutMs()
}

function getBackgroundUsageNote(): string | null {
  if (isEnvTruthy(process.env.CLAUDE_CODE_DISABLE_BACKGROUND_TASKS)) {
    return null
  }
  return "You can use the `run_in_background` parameter to run the command in the background. Only use this if you don't need the result immediately and are OK being notified when the command completes later. You do not need to check the output right away - you'll be notified when it finishes. You do not need to use '&' at the end of the command when using this parameter."
}

function getCommitAndPRInstructions(): string {
  // Defense-in-depth: undercover instructions must survive even if the user
  // has disabled git instructions entirely. Attribution stripping and model-ID
  // hiding are mechanical and work regardless, but the explicit "don't blow
  // your cover" instructions are the last line of defense against the model
  // volunteering an internal codename in a commit message.
  const undercoverSection =
    process.env.USER_TYPE === 'ant' && isUndercover()
      ? getUndercoverInstructions() + '\n'

```

---


### `src/tools/BashTool/readOnlyValidation.ts`

**信息:**
- 行数: 1990
- 大小: 68322 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { z } from 'zod/v4'
import { getOriginalCwd } from '../../bootstrap/state.js'
import {
  extractOutputRedirections,
  splitCommand_DEPRECATED,
} from '../../utils/bash/commands.js'
import { tryParseShellCommand } from '../../utils/bash/shellQuote.js'
import { getCwd } from '../../utils/cwd.js'
import { isCurrentDirectoryBareGitRepo } from '../../utils/git.js'
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js'
import { getPlatform } from '../../utils/platform.js'
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js'
import {
  containsVulnerableUncPath,
  DOCKER_READ_ONLY_COMMANDS,
  EXTERNAL_READONLY_COMMANDS,
  type FlagArgType,
  GH_READ_ONLY_COMMANDS,
  GIT_READ_ONLY_COMMANDS,
  PYRIGHT_READ_ONLY_COMMANDS,
  RIPGREP_READ_ONLY_COMMANDS,
  validateFlags,
} from '../../utils/shell/readOnlyCommandValidation.js'
import type { BashTool } from './BashTool.js'
import { isNormalizedGitCommand } from './bashPermissions.js'
import { bashCommandIsSafe_DEPRECATED } from './bashSecurity.js'
import {
  COMMAND_OPERATION_TYPE,
  PATH_EXTRACTORS,
  type PathCommand,
} from './pathValidation.js'
import { sedCommandIsAllowedByAllowlist } from './sedValidation.js'

// Unified command validation configuration system
type CommandConfig = {
  // A Record mapping from the command (e.g. `xargs` or `git diff`) to its safe flags and the values they accept
  safeFlags: Record<string, FlagArgType>
  // An optional regex that is used for additional validation beyond flag parsing
  regex?: RegExp
  // An optional callback for additional custom validation logic. Returns true if the command is dangerous,
  // false if it appears to be safe. Meant to be used in conjunction with the safeFlags-based validation.
  additionalCommandIsDangerousCallback?: (
    rawCommand: string,
    args: string[],
  ) => boolean
  // When false, the tool does NOT respect POSIX `--` end-of-options.
  // validateFlags will continue checking flags after `--` instead of breaking.
  // Default: true (most tools respect `--`).
  respectsDoubleDash?: boolean
}

```

---


### `src/tools/BashTool/sedEditParser.ts`

**信息:**
- 行数: 322
- 大小: 9562 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Parser for sed edit commands (-i flag substitutions)
 * Extracts file paths and substitution patterns to enable file-edit-style rendering
 */

import { randomBytes } from 'crypto'
import { tryParseShellCommand } from '../../utils/bash/shellQuote.js'

// BRE→ERE conversion placeholders (null-byte sentinels, never appear in user input)
const BACKSLASH_PLACEHOLDER = '\x00BACKSLASH\x00'
const PLUS_PLACEHOLDER = '\x00PLUS\x00'
const QUESTION_PLACEHOLDER = '\x00QUESTION\x00'
const PIPE_PLACEHOLDER = '\x00PIPE\x00'
const LPAREN_PLACEHOLDER = '\x00LPAREN\x00'
const RPAREN_PLACEHOLDER = '\x00RPAREN\x00'
const BACKSLASH_PLACEHOLDER_RE = new RegExp(BACKSLASH_PLACEHOLDER, 'g')
const PLUS_PLACEHOLDER_RE = new RegExp(PLUS_PLACEHOLDER, 'g')
const QUESTION_PLACEHOLDER_RE = new RegExp(QUESTION_PLACEHOLDER, 'g')
const PIPE_PLACEHOLDER_RE = new RegExp(PIPE_PLACEHOLDER, 'g')
const LPAREN_PLACEHOLDER_RE = new RegExp(LPAREN_PLACEHOLDER, 'g')
const RPAREN_PLACEHOLDER_RE = new RegExp(RPAREN_PLACEHOLDER, 'g')

export type SedEditInfo = {
  /** The file path being edited */
  filePath: string
  /** The search pattern (regex) */
  pattern: string
  /** The replacement string */
  replacement: string
  /** Substitution flags (g, i, etc.) */
  flags: string
  /** Whether to use extended regex (-E or -r flag) */
  extendedRegex: boolean
}

/**
 * Check if a command is a sed in-place edit command
 * Returns true only for simple sed -i 's/pattern/replacement/flags' file commands
 */
export function isSedInPlaceEdit(command: string): boolean {
  const info = parseSedEditCommand(command)
  return info !== null
}

/**
 * Parse a sed edit command and extract the edit information
 * Returns null if the command is not a valid sed in-place edit
 */
export function parseSedEditCommand(command: string): SedEditInfo | null {
  const trimmed = command.trim()

```

---


### `src/tools/BashTool/sedValidation.ts`

**信息:**
- 行数: 684
- 大小: 21518 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ToolPermissionContext } from '../../Tool.js'
import { splitCommand_DEPRECATED } from '../../utils/bash/commands.js'
import { tryParseShellCommand } from '../../utils/bash/shellQuote.js'
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js'

/**
 * Helper: Validate flags against an allowlist
 * Handles both single flags and combined flags (e.g., -nE)
 * @param flags Array of flags to validate
 * @param allowedFlags Array of allowed single-character and long flags
 * @returns true if all flags are valid, false otherwise
 */
function validateFlagsAgainstAllowlist(
  flags: string[],
  allowedFlags: string[],
): boolean {
  for (const flag of flags) {
    // Handle combined flags like -nE or -Er
    if (flag.startsWith('-') && !flag.startsWith('--') && flag.length > 2) {
      // Check each character in combined flag
      for (let i = 1; i < flag.length; i++) {
        const singleFlag = '-' + flag[i]
        if (!allowedFlags.includes(singleFlag)) {
          return false
        }
      }
    } else {
      // Single flag or long flag
      if (!allowedFlags.includes(flag)) {
        return false
      }
    }
  }
  return true
}

/**
 * Pattern 1: Check if this is a line printing command with -n flag
 * Allows: sed -n 'N' | sed -n 'N,M' with optional -E, -r, -z flags
 * Allows semicolon-separated print commands like: sed -n '1p;2p;3p'
 * File arguments are ALLOWED for this pattern
 * @internal Exported for testing
 */
export function isLinePrintingCommand(
  command: string,
  expressions: string[],
): boolean {
  const sedMatch = command.match(/^\s*sed\s+/)
  if (!sedMatch) return false


```

---


### `src/tools/BashTool/shouldUseSandbox.ts`

**信息:**
- 行数: 153
- 大小: 5185 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getFeatureValue_CACHED_MAY_BE_STALE } from 'src/services/analytics/growthbook.js'
import { splitCommand_DEPRECATED } from '../../utils/bash/commands.js'
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js'
import { getSettings_DEPRECATED } from '../../utils/settings/settings.js'
import {
  BINARY_HIJACK_VARS,
  bashPermissionRule,
  matchWildcardPattern,
  stripAllLeadingEnvVars,
  stripSafeWrappers,
} from './bashPermissions.js'

type SandboxInput = {
  command?: string
  dangerouslyDisableSandbox?: boolean
}

// NOTE: excludedCommands is a user-facing convenience feature, not a security boundary.
// It is not a security bug to be able to bypass excludedCommands — the sandbox permission
// system (which prompts users) is the actual security control.
function containsExcludedCommand(command: string): boolean {
  // Check dynamic config for disabled commands and substrings (only for ants)
  if (process.env.USER_TYPE === 'ant') {
    const disabledCommands = getFeatureValue_CACHED_MAY_BE_STALE<{
      commands: string[]
      substrings: string[]
    }>('tengu_sandbox_disabled_commands', { commands: [], substrings: [] })

    // Check if command contains any disabled substrings
    for (const substring of disabledCommands.substrings) {
      if (command.includes(substring)) {
        return true
      }
    }

    // Check if command starts with any disabled commands
    try {
      const commandParts = splitCommand_DEPRECATED(command)
      for (const part of commandParts) {
        const baseCommand = part.trim().split(' ')[0]
        if (baseCommand && disabledCommands.commands.includes(baseCommand)) {
          return true
        }
      }
    } catch {
      // If we can't parse the command (e.g., malformed bash syntax),
      // treat it as not excluded to allow other validation checks to handle it
      // This prevents crashes when rendering tool use messages
    }
  }

```

---


### `src/tools/BashTool/toolName.ts`

**信息:**
- 行数: 2
- 大小: 89 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Here to break circular dependency from prompt.ts
export const BASH_TOOL_NAME = 'Bash'

```

---


### `src/tools/BashTool/utils.ts`

**信息:**
- 行数: 223
- 大小: 7207 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type {
  Base64ImageSource,
  ContentBlockParam,
  ToolResultBlockParam,
} from '@anthropic-ai/sdk/resources/index.mjs'
import { readFile, stat } from 'fs/promises'
import { getOriginalCwd } from 'src/bootstrap/state.js'
import { logEvent } from 'src/services/analytics/index.js'
import type { ToolPermissionContext } from 'src/Tool.js'
import { getCwd } from 'src/utils/cwd.js'
import { pathInAllowedWorkingPath } from 'src/utils/permissions/filesystem.js'
import { setCwd } from 'src/utils/Shell.js'
import { shouldMaintainProjectWorkingDir } from '../../utils/envUtils.js'
import { maybeResizeAndDownsampleImageBuffer } from '../../utils/imageResizer.js'
import { getMaxOutputLength } from '../../utils/shell/outputLimits.js'
import { countCharInString, plural } from '../../utils/stringUtils.js'
/**
 * Strips leading and trailing lines that contain only whitespace/newlines.
 * Unlike trim(), this preserves whitespace within content lines and only removes
 * completely empty lines from the beginning and end.
 */
export function stripEmptyLines(content: string): string {
  const lines = content.split('\n')

  // Find the first non-empty line
  let startIndex = 0
  while (startIndex < lines.length && lines[startIndex]?.trim() === '') {
    startIndex++
  }

  // Find the last non-empty line
  let endIndex = lines.length - 1
  while (endIndex >= 0 && lines[endIndex]?.trim() === '') {
    endIndex--
  }

  // If all lines are empty, return empty string
  if (startIndex > endIndex) {
    return ''
  }

  // Return the slice with non-empty lines
  return lines.slice(startIndex, endIndex + 1).join('\n')
}

/**
 * Check if content is a base64 encoded image data URL
 */
export function isImageOutput(content: string): boolean {
  return /^data:image\/[a-z0-9.+_-]+;base64,/i.test(content)

```

---


### `src/tools/BriefTool/BriefTool.ts`

**信息:**
- 行数: 204
- 大小: 7677 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { z } from 'zod/v4'
import { getKairosActive, getUserMsgOptIn } from '../../bootstrap/state.js'
import { getFeatureValue_CACHED_WITH_REFRESH } from '../../services/analytics/growthbook.js'
import { logEvent } from '../../services/analytics/index.js'
import type { ValidationResult } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { plural } from '../../utils/stringUtils.js'
import { resolveAttachments, validateAttachmentPaths } from './attachments.js'
import {
  BRIEF_TOOL_NAME,
  BRIEF_TOOL_PROMPT,
  DESCRIPTION,
  LEGACY_BRIEF_TOOL_NAME,
} from './prompt.js'
import { renderToolResultMessage, renderToolUseMessage } from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    message: z
      .string()
      .describe('The message for the user. Supports markdown formatting.'),
    attachments: z
      .array(z.string())
      .optional()
      .describe(
        'Optional file paths (absolute or relative to cwd) to attach. Use for photos, screenshots, diffs, logs, or any file the user should see alongside your message.',
      ),
    status: z
      .enum(['normal', 'proactive'])
      .describe(
        "Use 'proactive' when you're surfacing something the user hasn't asked for and needs to see now — task completion while they're away, a blocker you hit, an unsolicited status update. Use 'normal' when replying to something the user just said.",
      ),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

// attachments MUST remain optional — resumed sessions replay pre-attachment
// outputs verbatim and a required field would crash the UI renderer on resume.
const outputSchema = lazySchema(() =>
  z.object({
    message: z.string().describe('The message'),
    attachments: z
      .array(
        z.object({
          path: z.string(),
          size: z.number(),
          isImage: z.boolean(),

```

---


### `src/tools/BriefTool/UI.tsx`

**信息:**
- 行数: 101
- 大小: 14303 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import figures from 'figures';
import React from 'react';
import { Markdown } from '../../components/Markdown.js';
import { BLACK_CIRCLE } from '../../constants/figures.js';
import { Box, Text } from '../../ink.js';
import type { ProgressMessage } from '../../types/message.js';
import { getDisplayPath } from '../../utils/file.js';
import { formatFileSize } from '../../utils/format.js';
import { formatBriefTimestamp } from '../../utils/formatBriefTimestamp.js';
import type { Output } from './BriefTool.js';
export function renderToolUseMessage(): React.ReactNode {
  return '';
}
export function renderToolResultMessage(output: Output, _progressMessages: ProgressMessage[], options?: {
  isTranscriptMode?: boolean;
  isBriefOnly?: boolean;
}): React.ReactNode {
  const hasAttachments = (output.attachments?.length ?? 0) > 0;
  if (!output.message && !hasAttachments) {
    return null;
  }

  // In transcript mode (ctrl+o), model text is NOT filtered — keep the ⏺ so
  // SendUserMessage is visually distinct from the surrounding text blocks.
  if (options?.isTranscriptMode) {
    return <Box flexDirection="row" marginTop={1}>
        <Box minWidth={2}>
          <Text color="text">{BLACK_CIRCLE}</Text>
        </Box>
        <Box flexDirection="column">
          {output.message ? <Markdown>{output.message}</Markdown> : null}
          <AttachmentList attachments={output.attachments} />
        </Box>
      </Box>;
  }

  // Brief-only (chat) view: "Claude" label + 2-col indent, matching the "You"
  // label UserPromptMessage applies to user input (#20889). The "N in background"
  // spinner status lives in BriefSpinner (Spinner.tsx) — stateless label here.
  if (options?.isBriefOnly) {
    const ts = output.sentAt ? formatBriefTimestamp(output.sentAt) : '';
    return <Box flexDirection="column" marginTop={1} paddingLeft={2}>
        <Box flexDirection="row">
          <Text color="briefLabelClaude">Claude</Text>
          {ts ? <Text dimColor> {ts}</Text> : null}
        </Box>
        <Box flexDirection="column">
          {output.message ? <Markdown>{output.message}</Markdown> : null}
          <AttachmentList attachments={output.attachments} />

```

---


### `src/tools/BriefTool/attachments.ts`

**信息:**
- 行数: 110
- 大小: 3889 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Shared attachment validation + resolution for SendUserMessage and
 * SendUserFile. Lives in BriefTool/ so the dynamic `./upload.js` import
 * inside the feature('BRIDGE_MODE') guard stays relative and upload.ts
 * (axios, crypto, auth utils) remains tree-shakeable from non-bridge builds.
 */

import { feature } from 'bun:bundle'
import { stat } from 'fs/promises'

import type { ValidationResult } from '../../Tool.js'

import { getCwd } from '../../utils/cwd.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { getErrnoCode } from '../../utils/errors.js'
import { IMAGE_EXTENSION_REGEX } from '../../utils/imagePaste.js'
import { expandPath } from '../../utils/path.js'

export type ResolvedAttachment = {
  path: string
  size: number
  isImage: boolean
  file_uuid?: string
}

export async function validateAttachmentPaths(
  rawPaths: string[],
): Promise<ValidationResult> {
  const cwd = getCwd()
  for (const rawPath of rawPaths) {
    const fullPath = expandPath(rawPath)
    try {
      const stats = await stat(fullPath)
      if (!stats.isFile()) {
        return {
          result: false,
          message: `Attachment "${rawPath}" is not a regular file.`,
          errorCode: 1,
        }
      }
    } catch (e) {
      const code = getErrnoCode(e)
      if (code === 'ENOENT') {
        return {
          result: false,
          message: `Attachment "${rawPath}" does not exist. Current working directory: ${cwd}.`,
          errorCode: 1,
        }
      }
      if (code === 'EACCES' || code === 'EPERM') {

```

---


### `src/tools/BriefTool/prompt.ts`

**信息:**
- 行数: 22
- 大小: 1933 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const BRIEF_TOOL_NAME = 'SendUserMessage'
export const LEGACY_BRIEF_TOOL_NAME = 'Brief'

export const DESCRIPTION = 'Send a message to the user'

export const BRIEF_TOOL_PROMPT = `Send a message the user will read. Text outside this tool is visible in the detail view, but most won't open it — the answer lives here.

\`message\` supports markdown. \`attachments\` takes file paths (absolute or cwd-relative) for images, diffs, logs.

\`status\` labels intent: 'normal' when replying to what they just asked; 'proactive' when you're initiating — a scheduled task finished, a blocker surfaced during background work, you need input on something they haven't asked about. Set it honestly; downstream routing uses it.`

export const BRIEF_PROACTIVE_SECTION = `## Talking to the user

${BRIEF_TOOL_NAME} is where your replies go. Text outside it is visible if the user expands the detail view, but most won't — assume unread. Anything you want them to actually see goes through ${BRIEF_TOOL_NAME}. The failure mode: the real answer lives in plain text while ${BRIEF_TOOL_NAME} just says "done!" — they see "done!" and miss everything.

So: every time the user says something, the reply they actually read comes through ${BRIEF_TOOL_NAME}. Even for "hi". Even for "thanks".

If you can answer right away, send the answer. If you need to go look — run a command, read files, check something — ack first in one line ("On it — checking the test output"), then work, then send the result. Without the ack they're staring at a spinner.

For longer work: ack → work → result. Between those, send a checkpoint when something useful happened — a decision you made, a surprise you hit, a phase boundary. Skip the filler ("running tests...") — a checkpoint earns its place by carrying information.

Keep messages tight — the decision, the file:line, the PR number. Second person always ("your config"), never third.`

```

---


### `src/tools/BriefTool/upload.ts`

**信息:**
- 行数: 174
- 大小: 5815 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Upload BriefTool attachments to private_api so web viewers can preview them.
 *
 * When the repl bridge is active, attachment paths are meaningless to a web
 * viewer (they're on Claude's machine). We upload to /api/oauth/file_upload —
 * the same store MessageComposer/SpaceMessage render from — and stash the
 * returned file_uuid alongside the path. Web resolves file_uuid → preview;
 * desktop/local try path first.
 *
 * Best-effort: any failure (no token, bridge off, network error, 4xx) logs
 * debug and returns undefined. The attachment still carries {path, size,
 * isImage}, so local-terminal and same-machine-desktop render unaffected.
 */

import { feature } from 'bun:bundle'
import axios from 'axios'
import { randomUUID } from 'crypto'
import { readFile } from 'fs/promises'
import { basename, extname } from 'path'
import { z } from 'zod/v4'

import {
  getBridgeAccessToken,
  getBridgeBaseUrlOverride,
} from '../../bridge/bridgeConfig.js'
import { getOauthConfig } from '../../constants/oauth.js'
import { logForDebugging } from '../../utils/debug.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { jsonStringify } from '../../utils/slowOperations.js'

// Matches the private_api backend limit
const MAX_UPLOAD_BYTES = 30 * 1024 * 1024

const UPLOAD_TIMEOUT_MS = 30_000

// Backend dispatches on mime: image/* → upload_image_wrapped (writes
// PREVIEW/THUMBNAIL, no ORIGINAL), everything else → upload_generic_file
// (ORIGINAL only, no preview). Only whitelist raster formats the
// transcoder reliably handles — svg/bmp/ico risk a 400, and pdf routes
// to upload_pdf_file_wrapped which also skips ORIGINAL. Dispatch
// viewers use /preview for images and /contents for everything else,
// so images go image/* and the rest go octet-stream.
const MIME_BY_EXT: Record<string, string> = {
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
}


```

---


### `src/tools/ConfigTool/ConfigTool.ts`

**信息:**
- 行数: 467
- 大小: 13478 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { z } from 'zod/v4'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import {
  type GlobalConfig,
  getGlobalConfig,
  getRemoteControlAtStartup,
  saveGlobalConfig,
} from '../../utils/config.js'
import { errorMessage } from '../../utils/errors.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { logError } from '../../utils/log.js'
import {
  getInitialSettings,
  updateSettingsForSource,
} from '../../utils/settings/settings.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { CONFIG_TOOL_NAME } from './constants.js'
import { DESCRIPTION, generatePrompt } from './prompt.js'
import {
  getConfig,
  getOptionsForSetting,
  getPath,
  isSupported,
} from './supportedSettings.js'
import {
  renderToolResultMessage,
  renderToolUseMessage,
  renderToolUseRejectedMessage,
} from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    setting: z
      .string()
      .describe(
        'The setting key (e.g., "theme", "model", "permissions.defaultMode")',
      ),
    value: z
      .union([z.string(), z.boolean(), z.number()])
      .optional()
      .describe('The new value. Omit to get current value.'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>


```

---


### `src/tools/ConfigTool/UI.tsx`

**信息:**
- 行数: 38
- 大小: 5717 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { MessageResponse } from '../../components/MessageResponse.js';
import { Text } from '../../ink.js';
import { jsonStringify } from '../../utils/slowOperations.js';
import type { Input, Output } from './ConfigTool.js';
export function renderToolUseMessage(input: Partial<Input>): React.ReactNode {
  if (!input.setting) return null;
  if (input.value === undefined) {
    return <Text dimColor>Getting {input.setting}</Text>;
  }
  return <Text dimColor>
      Setting {input.setting} to {jsonStringify(input.value)}
    </Text>;
}
export function renderToolResultMessage(content: Output): React.ReactNode {
  if (!content.success) {
    return <MessageResponse>
        <Text color="error">Failed: {content.error}</Text>
      </MessageResponse>;
  }
  if (content.operation === 'get') {
    return <MessageResponse>
        <Text>
          <Text bold>{content.setting}</Text> = {jsonStringify(content.value)}
        </Text>
      </MessageResponse>;
  }
  return <MessageResponse>
      <Text>
        Set <Text bold>{content.setting}</Text> to{' '}
        <Text bold>{jsonStringify(content.newValue)}</Text>
      </Text>
    </MessageResponse>;
}
export function renderToolUseRejectedMessage(): React.ReactNode {
  return <Text color="warning">Config change rejected</Text>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIk1lc3NhZ2VSZXNwb25zZSIsIlRleHQiLCJqc29uU3RyaW5naWZ5IiwiSW5wdXQiLCJPdXRwdXQiLCJyZW5kZXJUb29sVXNlTWVzc2FnZSIsImlucHV0IiwiUGFydGlhbCIsIlJlYWN0Tm9kZSIsInNldHRpbmciLCJ2YWx1ZSIsInVuZGVmaW5lZCIsInJlbmRlclRvb2xSZXN1bHRNZXNzYWdlIiwiY29udGVudCIsInN1Y2Nlc3MiLCJlcnJvciIsIm9wZXJhdGlvbiIsIm5ld1ZhbHVlIiwicmVuZGVyVG9vbFVzZVJlamVjdGVkTWVzc2FnZSJdLCJzb3VyY2VzIjpbIlVJLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBNZXNzYWdlUmVzcG9uc2UgfSBmcm9tICcuLi8uLi9jb21wb25lbnRzL01lc3NhZ2VSZXNwb25zZS5qcydcbmltcG9ydCB7IFRleHQgfSBmcm9tICcuLi8uLi9pbmsuanMnXG5pbXBvcnQgeyBqc29uU3RyaW5naWZ5IH0gZnJvbSAnLi4vLi4vdXRpbHMvc2xvd09wZXJhdGlvbnMuanMnXG5pbXBvcnQgdHlwZSB7IElucHV0LCBPdXRwdXQgfSBmcm9tICcuL0NvbmZpZ1Rvb2wuanMnXG5cbmV4cG9ydCBmdW5jdGlvbiByZW5kZXJUb29sVXNlTWVzc2FnZShpbnB1dDogUGFydGlhbDxJbnB1dD4pOiBSZWFjdC5SZWFjdE5vZGUge1xuICBpZiAoIWlucHV0LnNldHRpbmcpIHJldHVybiBudWxsXG4gIGlmIChpbnB1dC52YWx1ZSA9PT0gdW5kZWZpbmVkKSB7XG4gICAgcmV0dXJuIDxUZXh0IGRpbUNvbG9yPkdldHRpbmcge2lucHV0LnNldHRpbmd9PC9UZXh0PlxuICB9XG4gIHJldHVybiAoXG4gICAgPFRleHQgZGltQ29sb3I+XG4gICAgICBTZXR0aW5nIHtpbnB1dC5zZXR0aW5nfSB0byB7anNvblN0cmluZ2lmeShpbnB1dC52YWx1ZSl9XG4gICAgPC9UZXh0PlxuICApXG59XG5cbmV4cG9ydCBmdW5jdGlvbiByZW5kZXJUb29sUmVzdWx0TWVzc2FnZShjb250ZW50OiBPdXRwdXQpOiBSZWFjdC5SZWFjdE5vZGUge1xuICBpZiAoIWNvbnRlbnQuc3VjY2Vzcykge1xuICAgIHJldHVybiAoXG4gICAgICA8TWVzc2FnZVJlc3BvbnNlPlxuICAgICAgICA8VGV4dCBjb2xvcj1cImVycm9yXCI+RmFpbGVkOiB7Y29udGVudC5lcnJvcn08L1RleHQ+XG4gICAgICA8L01lc3NhZ2VSZXNwb25zZT5cbiAgICApXG4gIH1cbiAgaWYgKGNvbnRlbnQub3BlcmF0aW9uID09PSAnZ2V0Jykge1xuICAgIHJldHVybiAoXG4gICAgICA8TWVzc2FnZVJlc3BvbnNlPlxuICAgICAgICA8VGV4dD5cbiAgICAgICAgICA8VGV4dCBib2xkPntjb250ZW50LnNldHRpbmd9PC9UZXh0PiA9IHtqc29uU3RyaW5naWZ5KGNvbnRlbnQudmFsdWUpfVxuICAgICAgICA8L1RleHQ+XG4gICAgICA8L01lc3NhZ2VSZXNwb25zZT5cbiAgICApXG4gIH1cbiAgcmV0dXJuIChcbiAgICA8TWVzc2FnZVJlc3BvbnNlPlxuICAgICAgPFRleHQ+XG4gICAgICAgIFNldCA8VGV4dCBib2xkPntjb250ZW50LnNldHRpbmd9PC9UZXh0PiB0b3snICd9XG4gICAgICAgIDxUZXh0IGJvbGQ+e2pzb25TdHJpbmdpZnkoY29udGVudC5uZXdWYWx1ZSl9PC9UZXh0PlxuICAgICAgPC9UZXh0PlxuICAgIDwvTWVzc2FnZVJlc3BvbnNlPlxuICApXG59XG5cbmV4cG9ydCBmdW5jdGlvbiByZW5kZXJUb29sVXNlUmVqZWN0ZWRNZXNzYWdlKCk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIHJldHVybiA8VGV4dCBjb2xvcj1cIndhcm5pbmdcIj5Db25maWcgY2hhbmdlIHJlamVjdGVkPC9UZXh0PlxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPQSxLQUFLLE1BQU0sT0FBTztBQUN6QixTQUFTQyxlQUFlLFFBQVEscUNBQXFDO0FBQ3JFLFNBQVNDLElBQUksUUFBUSxjQUFjO0FBQ25DLFNBQVNDLGFBQWEsUUFBUSwrQkFBK0I7QUFDN0QsY0FBY0MsS0FBSyxFQUFFQyxNQUFNLFFBQVEsaUJBQWlCO0FBRXBELE9BQU8sU0FBU0Msb0JBQW9CQSxDQUFDQyxLQUFLLEVBQUVDLE9BQU8sQ0FBQ0osS0FBSyxDQUFDLENBQUMsRUFBRUosS0FBSyxDQUFDUyxTQUFTLENBQUM7RUFDM0UsSUFBSSxDQUFDRixLQUFLLENBQUNHLE9BQU8sRUFBRSxPQUFPLElBQUk7RUFDL0IsSUFBSUgsS0FBSyxDQUFDSSxLQUFLLEtBQUtDLFNBQVMsRUFBRTtJQUM3QixPQUFPLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxRQUFRLENBQUNMLEtBQUssQ0FBQ0csT0FBTyxDQUFDLEVBQUUsSUFBSSxDQUFDO0VBQ3REO0VBQ0EsT0FDRSxDQUFDLElBQUksQ0FBQyxRQUFRO0FBQ2xCLGNBQWMsQ0FBQ0gsS0FBSyxDQUFDRyxPQUFPLENBQUMsSUFBSSxDQUFDUCxhQUFhLENBQUNJLEtBQUssQ0FBQ0ksS0FBSyxDQUFDO0FBQzVELElBQUksRUFBRSxJQUFJLENBQUM7QUFFWDtBQUVBLE9BQU8sU0FBU0UsdUJBQXVCQSxDQUFDQyxPQUFPLEVBQUVULE1BQU0sQ0FBQyxFQUFFTCxLQUFLLENBQUNTLFNBQVMsQ0FBQztFQUN4RSxJQUFJLENBQUNLLE9BQU8sQ0FBQ0MsT0FBTyxFQUFFO0lBQ3BCLE9BQ0UsQ0FBQyxlQUFlO0FBQ3RCLFFBQVEsQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLE9BQU8sQ0FBQyxRQUFRLENBQUNELE9BQU8sQ0FBQ0UsS0FBSyxDQUFDLEVBQUUsSUFBSTtBQUN6RCxNQUFNLEVBQUUsZUFBZSxDQUFDO0VBRXRCO0VBQ0EsSUFBSUYsT0FBTyxDQUFDRyxTQUFTLEtBQUssS0FBSyxFQUFFO0lBQy9CLE9BQ0UsQ0FBQyxlQUFlO0FBQ3RCLFFBQVEsQ0FBQyxJQUFJO0FBQ2IsVUFBVSxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsQ0FBQ0gsT0FBTyxDQUFDSixPQUFPLENBQUMsRUFBRSxJQUFJLENBQUMsR0FBRyxDQUFDUCxhQUFhLENBQUNXLE9BQU8sQ0FBQ0gsS0FBSyxDQUFDO0FBQzdFLFFBQVEsRUFBRSxJQUFJO0FBQ2QsTUFBTSxFQUFFLGVBQWUsQ0FBQztFQUV0QjtFQUNBLE9BQ0UsQ0FBQyxlQUFlO0FBQ3BCLE1BQU0sQ0FBQyxJQUFJO0FBQ1gsWUFBWSxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsQ0FBQ0csT0FBTyxDQUFDSixPQUFPLENBQUMsRUFBRSxJQUFJLENBQUMsR0FBRyxDQUFDLEdBQUc7QUFDdEQsUUFBUSxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsQ0FBQ1AsYUFBYSxDQUFDVyxPQUFPLENBQUNJLFFBQVEsQ0FBQyxDQUFDLEVBQUUsSUFBSTtBQUMxRCxNQUFNLEVBQUUsSUFBSTtBQUNaLElBQUksRUFBRSxlQUFlLENBQUM7QUFFdEI7QUFFQSxPQUFPLFNBQVNDLDRCQUE0QkEsQ0FBQSxDQUFFLEVBQUVuQixLQUFLLENBQUNTLFNBQVMsQ0FBQztFQUM5RCxPQUFPLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxTQUFTLENBQUMsc0JBQXNCLEVBQUUsSUFBSSxDQUFDO0FBQzVEIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/tools/ConfigTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 41 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const CONFIG_TOOL_NAME = 'Config'

```

---


### `src/tools/ConfigTool/prompt.ts`

**信息:**
- 行数: 93
- 大小: 2881 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { getModelOptions } from '../../utils/model/modelOptions.js'
import { isVoiceGrowthBookEnabled } from '../../voice/voiceModeEnabled.js'
import {
  getOptionsForSetting,
  SUPPORTED_SETTINGS,
} from './supportedSettings.js'

export const DESCRIPTION = 'Get or set Claude Code configuration settings.'

/**
 * Generate the prompt documentation from the registry
 */
export function generatePrompt(): string {
  const globalSettings: string[] = []
  const projectSettings: string[] = []

  for (const [key, config] of Object.entries(SUPPORTED_SETTINGS)) {
    // Skip model - it gets its own section with dynamic options
    if (key === 'model') continue
    // Voice settings are registered at build-time but gated by GrowthBook
    // at runtime. Hide from model prompt when the kill-switch is on.
    if (
      feature('VOICE_MODE') &&
      key === 'voiceEnabled' &&
      !isVoiceGrowthBookEnabled()
    )
      continue

    const options = getOptionsForSetting(key)
    let line = `- ${key}`

    if (options) {
      line += `: ${options.map(o => `"${o}"`).join(', ')}`
    } else if (config.type === 'boolean') {
      line += `: true/false`
    }

    line += ` - ${config.description}`

    if (config.source === 'global') {
      globalSettings.push(line)
    } else {
      projectSettings.push(line)
    }
  }

  const modelSection = generateModelSection()

  return `Get or set Claude Code configuration settings.

```

---


### `src/tools/ConfigTool/supportedSettings.ts`

**信息:**
- 行数: 211
- 大小: 6374 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { getRemoteControlAtStartup } from '../../utils/config.js'
import {
  EDITOR_MODES,
  NOTIFICATION_CHANNELS,
  TEAMMATE_MODES,
} from '../../utils/configConstants.js'
import { getModelOptions } from '../../utils/model/modelOptions.js'
import { validateModel } from '../../utils/model/validateModel.js'
import { THEME_NAMES, THEME_SETTINGS } from '../../utils/theme.js'

/** AppState keys that can be synced for immediate UI effect */
type SyncableAppStateKey = 'verbose' | 'mainLoopModel' | 'thinkingEnabled'

type SettingConfig = {
  source: 'global' | 'settings'
  type: 'boolean' | 'string'
  description: string
  path?: string[]
  options?: readonly string[]
  getOptions?: () => string[]
  appStateKey?: SyncableAppStateKey
  /** Async validation called when writing/setting a value */
  validateOnWrite?: (v: unknown) => Promise<{ valid: boolean; error?: string }>
  /** Format value when reading/getting for display */
  formatOnRead?: (v: unknown) => unknown
}

export const SUPPORTED_SETTINGS: Record<string, SettingConfig> = {
  theme: {
    source: 'global',
    type: 'string',
    description: 'Color theme for the UI',
    options: feature('AUTO_THEME') ? THEME_SETTINGS : THEME_NAMES,
  },
  editorMode: {
    source: 'global',
    type: 'string',
    description: 'Key binding mode',
    options: EDITOR_MODES,
  },
  verbose: {
    source: 'global',
    type: 'boolean',
    description: 'Show detailed debug output',
    appStateKey: 'verbose',
  },
  preferredNotifChannel: {
    source: 'global',
    type: 'string',

```

---


### `src/tools/DiscoverSkillsTool/prompt.ts`

**信息:**
- 行数: 1
- 大小: 59 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const DISCOVER_SKILLS_TOOL_NAME = 'discover_skills'

```

---


### `src/tools/EnterPlanModeTool/EnterPlanModeTool.ts`

**信息:**
- 行数: 126
- 大小: 4101 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { z } from 'zod/v4'
import {
  getAllowedChannels,
  handlePlanModeTransition,
} from '../../bootstrap/state.js'
import type { Tool } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { applyPermissionUpdate } from '../../utils/permissions/PermissionUpdate.js'
import { prepareContextForPlanMode } from '../../utils/permissions/permissionSetup.js'
import { isPlanModeInterviewPhaseEnabled } from '../../utils/planModeV2.js'
import { ENTER_PLAN_MODE_TOOL_NAME } from './constants.js'
import { getEnterPlanModeToolPrompt } from './prompt.js'
import {
  renderToolResultMessage,
  renderToolUseMessage,
  renderToolUseRejectedMessage,
} from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    // No parameters needed
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    message: z.string().describe('Confirmation that plan mode was entered'),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>
export type Output = z.infer<OutputSchema>

export const EnterPlanModeTool: Tool<InputSchema, Output> = buildTool({
  name: ENTER_PLAN_MODE_TOOL_NAME,
  searchHint: 'switch to plan mode to design an approach before coding',
  maxResultSizeChars: 100_000,
  async description() {
    return 'Requests permission to enter plan mode for complex tasks requiring exploration and design'
  },
  async prompt() {
    return getEnterPlanModeToolPrompt()
  },
  get inputSchema(): InputSchema {
    return inputSchema()
  },
  get outputSchema(): OutputSchema {
    return outputSchema()

```

---


### `src/tools/EnterPlanModeTool/UI.tsx`

**信息:**
- 行数: 33
- 大小: 5315 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { BLACK_CIRCLE } from 'src/constants/figures.js';
import { getModeColor } from 'src/utils/permissions/PermissionMode.js';
import { Box, Text } from '../../ink.js';
import type { ToolProgressData } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import type { ThemeName } from '../../utils/theme.js';
import type { Output } from './EnterPlanModeTool.js';
export function renderToolUseMessage(): React.ReactNode {
  return null;
}
export function renderToolResultMessage(_output: Output, _progressMessagesForMessage: ProgressMessage<ToolProgressData>[], _options: {
  theme: ThemeName;
}): React.ReactNode {
  return <Box flexDirection="column" marginTop={1}>
      <Box flexDirection="row">
        <Text color={getModeColor('plan')}>{BLACK_CIRCLE}</Text>
        <Text> Entered plan mode</Text>
      </Box>
      <Box paddingLeft={2}>
        <Text dimColor>
          Claude is now exploring and designing an implementation approach.
        </Text>
      </Box>
    </Box>;
}
export function renderToolUseRejectedMessage(): React.ReactNode {
  return <Box flexDirection="row" marginTop={1}>
      <Text color={getModeColor('default')}>{BLACK_CIRCLE}</Text>
      <Text> User declined to enter plan mode</Text>
    </Box>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJMQUNLX0NJUkNMRSIsImdldE1vZGVDb2xvciIsIkJveCIsIlRleHQiLCJUb29sUHJvZ3Jlc3NEYXRhIiwiUHJvZ3Jlc3NNZXNzYWdlIiwiVGhlbWVOYW1lIiwiT3V0cHV0IiwicmVuZGVyVG9vbFVzZU1lc3NhZ2UiLCJSZWFjdE5vZGUiLCJyZW5kZXJUb29sUmVzdWx0TWVzc2FnZSIsIl9vdXRwdXQiLCJfcHJvZ3Jlc3NNZXNzYWdlc0Zvck1lc3NhZ2UiLCJfb3B0aW9ucyIsInRoZW1lIiwicmVuZGVyVG9vbFVzZVJlamVjdGVkTWVzc2FnZSJdLCJzb3VyY2VzIjpbIlVJLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IEJMQUNLX0NJUkNMRSB9IGZyb20gJ3NyYy9jb25zdGFudHMvZmlndXJlcy5qcydcbmltcG9ydCB7IGdldE1vZGVDb2xvciB9IGZyb20gJ3NyYy91dGlscy9wZXJtaXNzaW9ucy9QZXJtaXNzaW9uTW9kZS5qcydcbmltcG9ydCB7IEJveCwgVGV4dCB9IGZyb20gJy4uLy4uL2luay5qcydcbmltcG9ydCB0eXBlIHsgVG9vbFByb2dyZXNzRGF0YSB9IGZyb20gJy4uLy4uL1Rvb2wuanMnXG5pbXBvcnQgdHlwZSB7IFByb2dyZXNzTWVzc2FnZSB9IGZyb20gJy4uLy4uL3R5cGVzL21lc3NhZ2UuanMnXG5pbXBvcnQgdHlwZSB7IFRoZW1lTmFtZSB9IGZyb20gJy4uLy4uL3V0aWxzL3RoZW1lLmpzJ1xuaW1wb3J0IHR5cGUgeyBPdXRwdXQgfSBmcm9tICcuL0VudGVyUGxhbk1vZGVUb29sLmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gcmVuZGVyVG9vbFVzZU1lc3NhZ2UoKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgcmV0dXJuIG51bGxcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHJlbmRlclRvb2xSZXN1bHRNZXNzYWdlKFxuICBfb3V0cHV0OiBPdXRwdXQsXG4gIF9wcm9ncmVzc01lc3NhZ2VzRm9yTWVzc2FnZTogUHJvZ3Jlc3NNZXNzYWdlPFRvb2xQcm9ncmVzc0RhdGE+W10sXG4gIF9vcHRpb25zOiB7IHRoZW1lOiBUaGVtZU5hbWUgfSxcbik6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIHJldHVybiAoXG4gICAgPEJveCBmbGV4RGlyZWN0aW9uPVwiY29sdW1uXCIgbWFyZ2luVG9wPXsxfT5cbiAgICAgIDxCb3ggZmxleERpcmVjdGlvbj1cInJvd1wiPlxuICAgICAgICA8VGV4dCBjb2xvcj17Z2V0TW9kZUNvbG9yKCdwbGFuJyl9PntCTEFDS19DSVJDTEV9PC9UZXh0PlxuICAgICAgICA8VGV4dD4gRW50ZXJlZCBwbGFuIG1vZGU8L1RleHQ+XG4gICAgICA8L0JveD5cbiAgICAgIDxCb3ggcGFkZGluZ0xlZnQ9ezJ9PlxuICAgICAgICA8VGV4dCBkaW1Db2xvcj5cbiAgICAgICAgICBDbGF1ZGUgaXMgbm93IGV4cGxvcmluZyBhbmQgZGVzaWduaW5nIGFuIGltcGxlbWVudGF0aW9uIGFwcHJvYWNoLlxuICAgICAgICA8L1RleHQ+XG4gICAgICA8L0JveD5cbiAgICA8L0JveD5cbiAgKVxufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVuZGVyVG9vbFVzZVJlamVjdGVkTWVzc2FnZSgpOiBSZWFjdC5SZWFjdE5vZGUge1xuICByZXR1cm4gKFxuICAgIDxCb3ggZmxleERpcmVjdGlvbj1cInJvd1wiIG1hcmdpblRvcD17MX0+XG4gICAgICA8VGV4dCBjb2xvcj17Z2V0TW9kZUNvbG9yKCdkZWZhdWx0Jyl9PntCTEFDS19DSVJDTEV9PC9UZXh0PlxuICAgICAgPFRleHQ+IFVzZXIgZGVjbGluZWQgdG8gZW50ZXIgcGxhbiBtb2RlPC9UZXh0PlxuICAgIDwvQm94PlxuICApXG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsU0FBU0MsWUFBWSxRQUFRLDBCQUEwQjtBQUN2RCxTQUFTQyxZQUFZLFFBQVEseUNBQXlDO0FBQ3RFLFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxRQUFRLGNBQWM7QUFDeEMsY0FBY0MsZ0JBQWdCLFFBQVEsZUFBZTtBQUNyRCxjQUFjQyxlQUFlLFFBQVEsd0JBQXdCO0FBQzdELGNBQWNDLFNBQVMsUUFBUSxzQkFBc0I7QUFDckQsY0FBY0MsTUFBTSxRQUFRLHdCQUF3QjtBQUVwRCxPQUFPLFNBQVNDLG9CQUFvQkEsQ0FBQSxDQUFFLEVBQUVULEtBQUssQ0FBQ1UsU0FBUyxDQUFDO0VBQ3RELE9BQU8sSUFBSTtBQUNiO0FBRUEsT0FBTyxTQUFTQyx1QkFBdUJBLENBQ3JDQyxPQUFPLEVBQUVKLE1BQU0sRUFDZkssMkJBQTJCLEVBQUVQLGVBQWUsQ0FBQ0QsZ0JBQWdCLENBQUMsRUFBRSxFQUNoRVMsUUFBUSxFQUFFO0VBQUVDLEtBQUssRUFBRVIsU0FBUztBQUFDLENBQUMsQ0FDL0IsRUFBRVAsS0FBSyxDQUFDVSxTQUFTLENBQUM7RUFDakIsT0FDRSxDQUFDLEdBQUcsQ0FBQyxhQUFhLENBQUMsUUFBUSxDQUFDLFNBQVMsQ0FBQyxDQUFDLENBQUMsQ0FBQztBQUM3QyxNQUFNLENBQUMsR0FBRyxDQUFDLGFBQWEsQ0FBQyxLQUFLO0FBQzlCLFFBQVEsQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLENBQUNSLFlBQVksQ0FBQyxNQUFNLENBQUMsQ0FBQyxDQUFDLENBQUNELFlBQVksQ0FBQyxFQUFFLElBQUk7QUFDL0QsUUFBUSxDQUFDLElBQUksQ0FBQyxrQkFBa0IsRUFBRSxJQUFJO0FBQ3RDLE1BQU0sRUFBRSxHQUFHO0FBQ1gsTUFBTSxDQUFDLEdBQUcsQ0FBQyxXQUFXLENBQUMsQ0FBQyxDQUFDLENBQUM7QUFDMUIsUUFBUSxDQUFDLElBQUksQ0FBQyxRQUFRO0FBQ3RCO0FBQ0EsUUFBUSxFQUFFLElBQUk7QUFDZCxNQUFNLEVBQUUsR0FBRztBQUNYLElBQUksRUFBRSxHQUFHLENBQUM7QUFFVjtBQUVBLE9BQU8sU0FBU2UsNEJBQTRCQSxDQUFBLENBQUUsRUFBRWhCLEtBQUssQ0FBQ1UsU0FBUyxDQUFDO0VBQzlELE9BQ0UsQ0FBQyxHQUFHLENBQUMsYUFBYSxDQUFDLEtBQUssQ0FBQyxTQUFTLENBQUMsQ0FBQyxDQUFDLENBQUM7QUFDMUMsTUFBTSxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsQ0FBQ1IsWUFBWSxDQUFDLFNBQVMsQ0FBQyxDQUFDLENBQUMsQ0FBQ0QsWUFBWSxDQUFDLEVBQUUsSUFBSTtBQUNoRSxNQUFNLENBQUMsSUFBSSxDQUFDLGlDQUFpQyxFQUFFLElBQUk7QUFDbkQsSUFBSSxFQUFFLEdBQUcsQ0FBQztBQUVWIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/tools/EnterPlanModeTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 57 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const ENTER_PLAN_MODE_TOOL_NAME = 'EnterPlanMode'

```

---


### `src/tools/EnterPlanModeTool/prompt.ts`

**信息:**
- 行数: 170
- 大小: 7752 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { isPlanModeInterviewPhaseEnabled } from '../../utils/planModeV2.js'
import { ASK_USER_QUESTION_TOOL_NAME } from '../AskUserQuestionTool/prompt.js'

const WHAT_HAPPENS_SECTION = `## What Happens in Plan Mode

In plan mode, you'll:
1. Thoroughly explore the codebase using Glob, Grep, and Read tools
2. Understand existing patterns and architecture
3. Design an implementation approach
4. Present your plan to the user for approval
5. Use ${ASK_USER_QUESTION_TOOL_NAME} if you need to clarify approaches
6. Exit plan mode with ExitPlanMode when ready to implement

`

function getEnterPlanModeToolPromptExternal(): string {
  // When interview phase is enabled, omit the "What Happens" section —
  // detailed workflow instructions arrive via the plan_mode attachment (messages.ts).
  const whatHappens = isPlanModeInterviewPhaseEnabled()
    ? ''
    : WHAT_HAPPENS_SECTION

  return `Use this tool proactively when you're about to start a non-trivial implementation task. Getting user sign-off on your approach before writing code prevents wasted effort and ensures alignment. This tool transitions you into plan mode where you can explore the codebase and design an implementation approach for user approval.

## When to Use This Tool

**Prefer using EnterPlanMode** for implementation tasks unless they're simple. Use it when ANY of these conditions apply:

1. **New Feature Implementation**: Adding meaningful new functionality
   - Example: "Add a logout button" - where should it go? What should happen on click?
   - Example: "Add form validation" - what rules? What error messages?

2. **Multiple Valid Approaches**: The task can be solved in several different ways
   - Example: "Add caching to the API" - could use Redis, in-memory, file-based, etc.
   - Example: "Improve performance" - many optimization strategies possible

3. **Code Modifications**: Changes that affect existing behavior or structure
   - Example: "Update the login flow" - what exactly should change?
   - Example: "Refactor this component" - what's the target architecture?

4. **Architectural Decisions**: The task requires choosing between patterns or technologies
   - Example: "Add real-time updates" - WebSockets vs SSE vs polling
   - Example: "Implement state management" - Redux vs Context vs custom solution

5. **Multi-File Changes**: The task will likely touch more than 2-3 files
   - Example: "Refactor the authentication system"
   - Example: "Add a new API endpoint with tests"

6. **Unclear Requirements**: You need to explore before understanding the full scope
   - Example: "Make the app faster" - need to profile and identify bottlenecks

```

---


### `src/tools/EnterWorktreeTool/EnterWorktreeTool.ts`

**信息:**
- 行数: 127
- 大小: 4364 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { getSessionId, setOriginalCwd } from '../../bootstrap/state.js'
import { clearSystemPromptSections } from '../../constants/systemPromptSections.js'
import { logEvent } from '../../services/analytics/index.js'
import type { Tool } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { clearMemoryFileCaches } from '../../utils/claudemd.js'
import { getCwd } from '../../utils/cwd.js'
import { findCanonicalGitRoot } from '../../utils/git.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { getPlanSlug, getPlansDirectory } from '../../utils/plans.js'
import { setCwd } from '../../utils/Shell.js'
import { saveWorktreeState } from '../../utils/sessionStorage.js'
import {
  createWorktreeForSession,
  getCurrentWorktreeSession,
  validateWorktreeSlug,
} from '../../utils/worktree.js'
import { ENTER_WORKTREE_TOOL_NAME } from './constants.js'
import { getEnterWorktreeToolPrompt } from './prompt.js'
import { renderToolResultMessage, renderToolUseMessage } from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    name: z
      .string()
      .superRefine((s, ctx) => {
        try {
          validateWorktreeSlug(s)
        } catch (e) {
          ctx.addIssue({ code: 'custom', message: (e as Error).message })
        }
      })
      .optional()
      .describe(
        'Optional name for the worktree. Each "/"-separated segment may contain only letters, digits, dots, underscores, and dashes; max 64 chars total. A random name is generated if not provided.',
      ),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    worktreePath: z.string(),
    worktreeBranch: z.string().optional(),
    message: z.string(),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>
export type Output = z.infer<OutputSchema>

```

---


### `src/tools/EnterWorktreeTool/UI.tsx`

**信息:**
- 行数: 20
- 大小: 3312 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import type { ToolProgressData } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import type { ThemeName } from '../../utils/theme.js';
import type { Output } from './EnterWorktreeTool.js';
export function renderToolUseMessage(): React.ReactNode {
  return 'Creating worktree…';
}
export function renderToolResultMessage(output: Output, _progressMessagesForMessage: ProgressMessage<ToolProgressData>[], _options: {
  theme: ThemeName;
}): React.ReactNode {
  return <Box flexDirection="column">
      <Text>
        Switched to worktree on branch <Text bold>{output.worktreeBranch}</Text>
      </Text>
      <Text dimColor>{output.worktreePath}</Text>
    </Box>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJveCIsIlRleHQiLCJUb29sUHJvZ3Jlc3NEYXRhIiwiUHJvZ3Jlc3NNZXNzYWdlIiwiVGhlbWVOYW1lIiwiT3V0cHV0IiwicmVuZGVyVG9vbFVzZU1lc3NhZ2UiLCJSZWFjdE5vZGUiLCJyZW5kZXJUb29sUmVzdWx0TWVzc2FnZSIsIm91dHB1dCIsIl9wcm9ncmVzc01lc3NhZ2VzRm9yTWVzc2FnZSIsIl9vcHRpb25zIiwidGhlbWUiLCJ3b3JrdHJlZUJyYW5jaCIsIndvcmt0cmVlUGF0aCJdLCJzb3VyY2VzIjpbIlVJLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IEJveCwgVGV4dCB9IGZyb20gJy4uLy4uL2luay5qcydcbmltcG9ydCB0eXBlIHsgVG9vbFByb2dyZXNzRGF0YSB9IGZyb20gJy4uLy4uL1Rvb2wuanMnXG5pbXBvcnQgdHlwZSB7IFByb2dyZXNzTWVzc2FnZSB9IGZyb20gJy4uLy4uL3R5cGVzL21lc3NhZ2UuanMnXG5pbXBvcnQgdHlwZSB7IFRoZW1lTmFtZSB9IGZyb20gJy4uLy4uL3V0aWxzL3RoZW1lLmpzJ1xuaW1wb3J0IHR5cGUgeyBPdXRwdXQgfSBmcm9tICcuL0VudGVyV29ya3RyZWVUb29sLmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gcmVuZGVyVG9vbFVzZU1lc3NhZ2UoKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgcmV0dXJuICdDcmVhdGluZyB3b3JrdHJlZeKApidcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIHJlbmRlclRvb2xSZXN1bHRNZXNzYWdlKFxuICBvdXRwdXQ6IE91dHB1dCxcbiAgX3Byb2dyZXNzTWVzc2FnZXNGb3JNZXNzYWdlOiBQcm9ncmVzc01lc3NhZ2U8VG9vbFByb2dyZXNzRGF0YT5bXSxcbiAgX29wdGlvbnM6IHsgdGhlbWU6IFRoZW1lTmFtZSB9LFxuKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgcmV0dXJuIChcbiAgICA8Qm94IGZsZXhEaXJlY3Rpb249XCJjb2x1bW5cIj5cbiAgICAgIDxUZXh0PlxuICAgICAgICBTd2l0Y2hlZCB0byB3b3JrdHJlZSBvbiBicmFuY2ggPFRleHQgYm9sZD57b3V0cHV0Lndvcmt0cmVlQnJhbmNofTwvVGV4dD5cbiAgICAgIDwvVGV4dD5cbiAgICAgIDxUZXh0IGRpbUNvbG9yPntvdXRwdXQud29ya3RyZWVQYXRofTwvVGV4dD5cbiAgICA8L0JveD5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxRQUFRLGNBQWM7QUFDeEMsY0FBY0MsZ0JBQWdCLFFBQVEsZUFBZTtBQUNyRCxjQUFjQyxlQUFlLFFBQVEsd0JBQXdCO0FBQzdELGNBQWNDLFNBQVMsUUFBUSxzQkFBc0I7QUFDckQsY0FBY0MsTUFBTSxRQUFRLHdCQUF3QjtBQUVwRCxPQUFPLFNBQVNDLG9CQUFvQkEsQ0FBQSxDQUFFLEVBQUVQLEtBQUssQ0FBQ1EsU0FBUyxDQUFDO0VBQ3RELE9BQU8sb0JBQW9CO0FBQzdCO0FBRUEsT0FBTyxTQUFTQyx1QkFBdUJBLENBQ3JDQyxNQUFNLEVBQUVKLE1BQU0sRUFDZEssMkJBQTJCLEVBQUVQLGVBQWUsQ0FBQ0QsZ0JBQWdCLENBQUMsRUFBRSxFQUNoRVMsUUFBUSxFQUFFO0VBQUVDLEtBQUssRUFBRVIsU0FBUztBQUFDLENBQUMsQ0FDL0IsRUFBRUwsS0FBSyxDQUFDUSxTQUFTLENBQUM7RUFDakIsT0FDRSxDQUFDLEdBQUcsQ0FBQyxhQUFhLENBQUMsUUFBUTtBQUMvQixNQUFNLENBQUMsSUFBSTtBQUNYLHVDQUF1QyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsQ0FBQ0UsTUFBTSxDQUFDSSxjQUFjLENBQUMsRUFBRSxJQUFJO0FBQy9FLE1BQU0sRUFBRSxJQUFJO0FBQ1osTUFBTSxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsQ0FBQ0osTUFBTSxDQUFDSyxZQUFZLENBQUMsRUFBRSxJQUFJO0FBQ2hELElBQUksRUFBRSxHQUFHLENBQUM7QUFFViIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/tools/EnterWorktreeTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 56 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const ENTER_WORKTREE_TOOL_NAME = 'EnterWorktree'

```

---


### `src/tools/EnterWorktreeTool/prompt.ts`

**信息:**
- 行数: 30
- 大小: 1412 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function getEnterWorktreeToolPrompt(): string {
  return `Use this tool ONLY when the user explicitly asks to work in a worktree. This tool creates an isolated git worktree and switches the current session into it.

## When to Use

- The user explicitly says "worktree" (e.g., "start a worktree", "work in a worktree", "create a worktree", "use a worktree")

## When NOT to Use

- The user asks to create a branch, switch branches, or work on a different branch — use git commands instead
- The user asks to fix a bug or work on a feature — use normal git workflow unless they specifically mention worktrees
- Never use this tool unless the user explicitly mentions "worktree"

## Requirements

- Must be in a git repository, OR have WorktreeCreate/WorktreeRemove hooks configured in settings.json
- Must not already be in a worktree

## Behavior

- In a git repository: creates a new git worktree inside \`.claude/worktrees/\` with a new branch based on HEAD
- Outside a git repository: delegates to WorktreeCreate/WorktreeRemove hooks for VCS-agnostic isolation
- Switches the session's working directory to the new worktree
- Use ExitWorktree to leave the worktree mid-session (keep or remove). On session exit, if still in the worktree, the user will be prompted to keep or remove it

## Parameters

- \`name\` (optional): A name for the worktree. If not provided, a random name is generated.
`
}

```

---


### `src/tools/ExitPlanModeTool/ExitPlanModeV2Tool.ts`

**信息:**
- 行数: 493
- 大小: 17006 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { writeFile } from 'fs/promises'
import { z } from 'zod/v4'
import {
  getAllowedChannels,
  hasExitedPlanModeInSession,
  setHasExitedPlanMode,
  setNeedsAutoModeExitAttachment,
  setNeedsPlanModeExitAttachment,
} from '../../bootstrap/state.js'
import { logEvent } from '../../services/analytics/index.js'
import type { AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS } from '../../services/analytics/metadata.js'
import {
  buildTool,
  type Tool,
  type ToolDef,
  toolMatchesName,
} from '../../Tool.js'
import { formatAgentId, generateRequestId } from '../../utils/agentId.js'
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js'
import { logForDebugging } from '../../utils/debug.js'
import {
  findInProcessTeammateTaskId,
  setAwaitingPlanApproval,
} from '../../utils/inProcessTeammateHelpers.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { logError } from '../../utils/log.js'
import {
  getPlan,
  getPlanFilePath,
  persistFileSnapshotIfRemote,
} from '../../utils/plans.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import {
  getAgentName,
  getTeamName,
  isPlanModeRequired,
  isTeammate,
} from '../../utils/teammate.js'
import { writeToMailbox } from '../../utils/teammateMailbox.js'
import { AGENT_TOOL_NAME } from '../AgentTool/constants.js'
import { TEAM_CREATE_TOOL_NAME } from '../TeamCreateTool/constants.js'
import { EXIT_PLAN_MODE_V2_TOOL_NAME } from './constants.js'
import { EXIT_PLAN_MODE_V2_TOOL_PROMPT } from './prompt.js'
import {
  renderToolResultMessage,
  renderToolUseMessage,
  renderToolUseRejectedMessage,
} from './UI.js'


```

---


### `src/tools/ExitPlanModeTool/UI.tsx`

**信息:**
- 行数: 82
- 大小: 11418 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { Markdown } from 'src/components/Markdown.js';
import { MessageResponse } from 'src/components/MessageResponse.js';
import { RejectedPlanMessage } from 'src/components/messages/UserToolResultMessage/RejectedPlanMessage.js';
import { BLACK_CIRCLE } from 'src/constants/figures.js';
import { getModeColor } from 'src/utils/permissions/PermissionMode.js';
import { Box, Text } from '../../ink.js';
import type { ToolProgressData } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import { getDisplayPath } from '../../utils/file.js';
import { getPlan } from '../../utils/plans.js';
import type { ThemeName } from '../../utils/theme.js';
import type { Output } from './ExitPlanModeV2Tool.js';
export function renderToolUseMessage(): React.ReactNode {
  return null;
}
export function renderToolResultMessage(output: Output, _progressMessagesForMessage: ProgressMessage<ToolProgressData>[], {
  theme: _theme
}: {
  theme: ThemeName;
}): React.ReactNode {
  const {
    plan,
    filePath
  } = output;
  const isEmpty = !plan || plan.trim() === '';
  const displayPath = filePath ? getDisplayPath(filePath) : '';
  const awaitingLeaderApproval = output.awaitingLeaderApproval;

  // Simplified message for empty plans
  if (isEmpty) {
    return <Box flexDirection="column" marginTop={1}>
        <Box flexDirection="row">
          <Text color={getModeColor('plan')}>{BLACK_CIRCLE}</Text>
          <Text> Exited plan mode</Text>
        </Box>
      </Box>;
  }

  // When awaiting leader approval, show a different message
  if (awaitingLeaderApproval) {
    return <Box flexDirection="column" marginTop={1}>
        <Box flexDirection="row">
          <Text color={getModeColor('plan')}>{BLACK_CIRCLE}</Text>
          <Text> Plan submitted for team lead approval</Text>
        </Box>
        <MessageResponse>
          <Box flexDirection="column">
            {filePath && <Text dimColor>Plan file: {displayPath}</Text>}
            <Text dimColor>Waiting for team lead to review and approve...</Text>

```

---


### `src/tools/ExitPlanModeTool/constants.ts`

**信息:**
- 行数: 2
- 大小: 113 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const EXIT_PLAN_MODE_TOOL_NAME = 'ExitPlanMode'
export const EXIT_PLAN_MODE_V2_TOOL_NAME = 'ExitPlanMode'

```

---


### `src/tools/ExitPlanModeTool/prompt.ts`

**信息:**
- 行数: 29
- 大小: 2139 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// External stub for ExitPlanModeTool prompt - excludes Ant-only allowedPrompts section

// Hardcoded to avoid relative import issues in stub
const ASK_USER_QUESTION_TOOL_NAME = 'AskUserQuestion'

export const EXIT_PLAN_MODE_V2_TOOL_PROMPT = `Use this tool when you are in plan mode and have finished writing your plan to the plan file and are ready for user approval.

## How This Tool Works
- You should have already written your plan to the plan file specified in the plan mode system message
- This tool does NOT take the plan content as a parameter - it will read the plan from the file you wrote
- This tool simply signals that you're done planning and ready for the user to review and approve
- The user will see the contents of your plan file when they review it

## When to Use This Tool
IMPORTANT: Only use this tool when the task requires planning the implementation steps of a task that requires writing code. For research tasks where you're gathering information, searching files, reading files or in general trying to understand the codebase - do NOT use this tool.

## Before Using This Tool
Ensure your plan is complete and unambiguous:
- If you have unresolved questions about requirements or approach, use ${ASK_USER_QUESTION_TOOL_NAME} first (in earlier phases)
- Once your plan is finalized, use THIS tool to request approval

**Important:** Do NOT use ${ASK_USER_QUESTION_TOOL_NAME} to ask "Is this plan okay?" or "Should I proceed?" - that's exactly what THIS tool does. ExitPlanMode inherently requests user approval of your plan.

## Examples

1. Initial task: "Search for and understand the implementation of vim mode in the codebase" - Do not use the exit plan mode tool because you are not planning the implementation steps of a task.
2. Initial task: "Help me implement yank mode for vim" - Use the exit plan mode tool after you have finished planning the implementation steps of the task.
3. Initial task: "Add a new feature to handle user authentication" - If unsure about auth method (OAuth, JWT, etc.), use ${ASK_USER_QUESTION_TOOL_NAME} first, then use exit plan mode tool after clarifying the approach.
`

```

---


### `src/tools/ExitWorktreeTool/ExitWorktreeTool.ts`

**信息:**
- 行数: 329
- 大小: 11649 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import {
  getOriginalCwd,
  getProjectRoot,
  setOriginalCwd,
  setProjectRoot,
} from '../../bootstrap/state.js'
import { clearSystemPromptSections } from '../../constants/systemPromptSections.js'
import { logEvent } from '../../services/analytics/index.js'
import type { Tool } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { count } from '../../utils/array.js'
import { clearMemoryFileCaches } from '../../utils/claudemd.js'
import { execFileNoThrow } from '../../utils/execFileNoThrow.js'
import { updateHooksConfigSnapshot } from '../../utils/hooks/hooksConfigSnapshot.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { getPlansDirectory } from '../../utils/plans.js'
import { setCwd } from '../../utils/Shell.js'
import { saveWorktreeState } from '../../utils/sessionStorage.js'
import {
  cleanupWorktree,
  getCurrentWorktreeSession,
  keepWorktree,
  killTmuxSession,
} from '../../utils/worktree.js'
import { EXIT_WORKTREE_TOOL_NAME } from './constants.js'
import { getExitWorktreeToolPrompt } from './prompt.js'
import { renderToolResultMessage, renderToolUseMessage } from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    action: z
      .enum(['keep', 'remove'])
      .describe(
        '"keep" leaves the worktree and branch on disk; "remove" deletes both.',
      ),
    discard_changes: z
      .boolean()
      .optional()
      .describe(
        'Required true when action is "remove" and the worktree has uncommitted files or unmerged commits. The tool will refuse and list them otherwise.',
      ),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    action: z.enum(['keep', 'remove']),
    originalCwd: z.string(),

```

---


### `src/tools/ExitWorktreeTool/UI.tsx`

**信息:**
- 行数: 25
- 大小: 4044 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { Box, Text } from '../../ink.js';
import type { ToolProgressData } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import type { ThemeName } from '../../utils/theme.js';
import type { Output } from './ExitWorktreeTool.js';
export function renderToolUseMessage(): React.ReactNode {
  return 'Exiting worktree…';
}
export function renderToolResultMessage(output: Output, _progressMessagesForMessage: ProgressMessage<ToolProgressData>[], _options: {
  theme: ThemeName;
}): React.ReactNode {
  const actionLabel = output.action === 'keep' ? 'Kept worktree' : 'Removed worktree';
  return <Box flexDirection="column">
      <Text>
        {actionLabel}
        {output.worktreeBranch ? <>
            {' '}
            (branch <Text bold>{output.worktreeBranch}</Text>)
          </> : null}
      </Text>
      <Text dimColor>Returned to {output.originalCwd}</Text>
    </Box>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJveCIsIlRleHQiLCJUb29sUHJvZ3Jlc3NEYXRhIiwiUHJvZ3Jlc3NNZXNzYWdlIiwiVGhlbWVOYW1lIiwiT3V0cHV0IiwicmVuZGVyVG9vbFVzZU1lc3NhZ2UiLCJSZWFjdE5vZGUiLCJyZW5kZXJUb29sUmVzdWx0TWVzc2FnZSIsIm91dHB1dCIsIl9wcm9ncmVzc01lc3NhZ2VzRm9yTWVzc2FnZSIsIl9vcHRpb25zIiwidGhlbWUiLCJhY3Rpb25MYWJlbCIsImFjdGlvbiIsIndvcmt0cmVlQnJhbmNoIiwib3JpZ2luYWxDd2QiXSwic291cmNlcyI6WyJVSS50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBCb3gsIFRleHQgfSBmcm9tICcuLi8uLi9pbmsuanMnXG5pbXBvcnQgdHlwZSB7IFRvb2xQcm9ncmVzc0RhdGEgfSBmcm9tICcuLi8uLi9Ub29sLmpzJ1xuaW1wb3J0IHR5cGUgeyBQcm9ncmVzc01lc3NhZ2UgfSBmcm9tICcuLi8uLi90eXBlcy9tZXNzYWdlLmpzJ1xuaW1wb3J0IHR5cGUgeyBUaGVtZU5hbWUgfSBmcm9tICcuLi8uLi91dGlscy90aGVtZS5qcydcbmltcG9ydCB0eXBlIHsgT3V0cHV0IH0gZnJvbSAnLi9FeGl0V29ya3RyZWVUb29sLmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gcmVuZGVyVG9vbFVzZU1lc3NhZ2UoKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgcmV0dXJuICdFeGl0aW5nIHdvcmt0cmVl4oCmJ1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVuZGVyVG9vbFJlc3VsdE1lc3NhZ2UoXG4gIG91dHB1dDogT3V0cHV0LFxuICBfcHJvZ3Jlc3NNZXNzYWdlc0Zvck1lc3NhZ2U6IFByb2dyZXNzTWVzc2FnZTxUb29sUHJvZ3Jlc3NEYXRhPltdLFxuICBfb3B0aW9uczogeyB0aGVtZTogVGhlbWVOYW1lIH0sXG4pOiBSZWFjdC5SZWFjdE5vZGUge1xuICBjb25zdCBhY3Rpb25MYWJlbCA9XG4gICAgb3V0cHV0LmFjdGlvbiA9PT0gJ2tlZXAnID8gJ0tlcHQgd29ya3RyZWUnIDogJ1JlbW92ZWQgd29ya3RyZWUnXG4gIHJldHVybiAoXG4gICAgPEJveCBmbGV4RGlyZWN0aW9uPVwiY29sdW1uXCI+XG4gICAgICA8VGV4dD5cbiAgICAgICAge2FjdGlvbkxhYmVsfVxuICAgICAgICB7b3V0cHV0Lndvcmt0cmVlQnJhbmNoID8gKFxuICAgICAgICAgIDw+XG4gICAgICAgICAgICB7JyAnfVxuICAgICAgICAgICAgKGJyYW5jaCA8VGV4dCBib2xkPntvdXRwdXQud29ya3RyZWVCcmFuY2h9PC9UZXh0PilcbiAgICAgICAgICA8Lz5cbiAgICAgICAgKSA6IG51bGx9XG4gICAgICA8L1RleHQ+XG4gICAgICA8VGV4dCBkaW1Db2xvcj5SZXR1cm5lZCB0byB7b3V0cHV0Lm9yaWdpbmFsQ3dkfTwvVGV4dD5cbiAgICA8L0JveD5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxRQUFRLGNBQWM7QUFDeEMsY0FBY0MsZ0JBQWdCLFFBQVEsZUFBZTtBQUNyRCxjQUFjQyxlQUFlLFFBQVEsd0JBQXdCO0FBQzdELGNBQWNDLFNBQVMsUUFBUSxzQkFBc0I7QUFDckQsY0FBY0MsTUFBTSxRQUFRLHVCQUF1QjtBQUVuRCxPQUFPLFNBQVNDLG9CQUFvQkEsQ0FBQSxDQUFFLEVBQUVQLEtBQUssQ0FBQ1EsU0FBUyxDQUFDO0VBQ3RELE9BQU8sbUJBQW1CO0FBQzVCO0FBRUEsT0FBTyxTQUFTQyx1QkFBdUJBLENBQ3JDQyxNQUFNLEVBQUVKLE1BQU0sRUFDZEssMkJBQTJCLEVBQUVQLGVBQWUsQ0FBQ0QsZ0JBQWdCLENBQUMsRUFBRSxFQUNoRVMsUUFBUSxFQUFFO0VBQUVDLEtBQUssRUFBRVIsU0FBUztBQUFDLENBQUMsQ0FDL0IsRUFBRUwsS0FBSyxDQUFDUSxTQUFTLENBQUM7RUFDakIsTUFBTU0sV0FBVyxHQUNmSixNQUFNLENBQUNLLE1BQU0sS0FBSyxNQUFNLEdBQUcsZUFBZSxHQUFHLGtCQUFrQjtFQUNqRSxPQUNFLENBQUMsR0FBRyxDQUFDLGFBQWEsQ0FBQyxRQUFRO0FBQy9CLE1BQU0sQ0FBQyxJQUFJO0FBQ1gsUUFBUSxDQUFDRCxXQUFXO0FBQ3BCLFFBQVEsQ0FBQ0osTUFBTSxDQUFDTSxjQUFjLEdBQ3BCO0FBQ1YsWUFBWSxDQUFDLEdBQUc7QUFDaEIsb0JBQW9CLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxDQUFDTixNQUFNLENBQUNNLGNBQWMsQ0FBQyxFQUFFLElBQUksQ0FBQztBQUM3RCxVQUFVLEdBQUcsR0FDRCxJQUFJO0FBQ2hCLE1BQU0sRUFBRSxJQUFJO0FBQ1osTUFBTSxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsWUFBWSxDQUFDTixNQUFNLENBQUNPLFdBQVcsQ0FBQyxFQUFFLElBQUk7QUFDM0QsSUFBSSxFQUFFLEdBQUcsQ0FBQztBQUVWIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/tools/ExitWorktreeTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 54 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const EXIT_WORKTREE_TOOL_NAME = 'ExitWorktree'

```

---


### `src/tools/ExitWorktreeTool/prompt.ts`

**信息:**
- 行数: 32
- 大小: 2021 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function getExitWorktreeToolPrompt(): string {
  return `Exit a worktree session created by EnterWorktree and return the session to the original working directory.

## Scope

This tool ONLY operates on worktrees created by EnterWorktree in this session. It will NOT touch:
- Worktrees you created manually with \`git worktree add\`
- Worktrees from a previous session (even if created by EnterWorktree then)
- The directory you're in if EnterWorktree was never called

If called outside an EnterWorktree session, the tool is a **no-op**: it reports that no worktree session is active and takes no action. Filesystem state is unchanged.

## When to Use

- The user explicitly asks to "exit the worktree", "leave the worktree", "go back", or otherwise end the worktree session
- Do NOT call this proactively — only when the user asks

## Parameters

- \`action\` (required): \`"keep"\` or \`"remove"\`
  - \`"keep"\` — leave the worktree directory and branch intact on disk. Use this if the user wants to come back to the work later, or if there are changes to preserve.
  - \`"remove"\` — delete the worktree directory and its branch. Use this for a clean exit when the work is done or abandoned.
- \`discard_changes\` (optional, default false): only meaningful with \`action: "remove"\`. If the worktree has uncommitted files or commits not on the original branch, the tool will REFUSE to remove it unless this is set to \`true\`. If the tool returns an error listing changes, confirm with the user before re-invoking with \`discard_changes: true\`.

## Behavior

- Restores the session's working directory to where it was before EnterWorktree
- Clears CWD-dependent caches (system prompt sections, memory files, plans directory) so the session state reflects the original directory
- If a tmux session was attached to the worktree: killed on \`remove\`, left running on \`keep\` (its name is returned so the user can reattach)
- Once exited, EnterWorktree can be called again to create a fresh worktree
`
}

```

---


### `src/tools/FileEditTool/FileEditTool.ts`

**信息:**
- 行数: 625
- 大小: 20502 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { dirname, isAbsolute, sep } from 'path'
import { logEvent } from 'src/services/analytics/index.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import { diagnosticTracker } from '../../services/diagnosticTracking.js'
import { clearDeliveredDiagnosticsForFile } from '../../services/lsp/LSPDiagnosticRegistry.js'
import { getLspServerManager } from '../../services/lsp/manager.js'
import { notifyVscodeFileUpdated } from '../../services/mcp/vscodeSdkMcp.js'
import { checkTeamMemSecrets } from '../../services/teamMemorySync/teamMemSecretGuard.js'
import {
  activateConditionalSkillsForPaths,
  addSkillDirectories,
  discoverSkillDirsForPaths,
} from '../../skills/loadSkillsDir.js'
import type { ToolUseContext } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { getCwd } from '../../utils/cwd.js'
import { logForDebugging } from '../../utils/debug.js'
import { countLinesChanged } from '../../utils/diff.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { isENOENT } from '../../utils/errors.js'
import {
  FILE_NOT_FOUND_CWD_NOTE,
  findSimilarFile,
  getFileModificationTime,
  suggestPathUnderCwd,
  writeTextContent,
} from '../../utils/file.js'
import {
  fileHistoryEnabled,
  fileHistoryTrackEdit,
} from '../../utils/fileHistory.js'
import { logFileOperation } from '../../utils/fileOperationAnalytics.js'
import {
  type LineEndingType,
  readFileSyncWithMetadata,
} from '../../utils/fileRead.js'
import { formatFileSize } from '../../utils/format.js'
import { getFsImplementation } from '../../utils/fsOperations.js'
import {
  fetchSingleFileGitDiff,
  type ToolUseDiff,
} from '../../utils/gitDiff.js'
import { logError } from '../../utils/log.js'
import { expandPath } from '../../utils/path.js'
import {
  checkWritePermissionForTool,
  matchingRuleForInput,
} from '../../utils/permissions/filesystem.js'
import type { PermissionDecision } from '../../utils/permissions/PermissionResult.js'
import { matchWildcardPattern } from '../../utils/permissions/shellRuleMatching.js'

```

---


### `src/tools/FileEditTool/UI.tsx`

**信息:**
- 行数: 289
- 大小: 34832 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import type { StructuredPatchHunk } from 'diff';
import * as React from 'react';
import { Suspense, use, useState } from 'react';
import { FileEditToolUseRejectedMessage } from 'src/components/FileEditToolUseRejectedMessage.js';
import { MessageResponse } from 'src/components/MessageResponse.js';
import { extractTag } from 'src/utils/messages.js';
import { FallbackToolUseErrorMessage } from '../../components/FallbackToolUseErrorMessage.js';
import { FileEditToolUpdatedMessage } from '../../components/FileEditToolUpdatedMessage.js';
import { FilePathLink } from '../../components/FilePathLink.js';
import { Text } from '../../ink.js';
import type { Tools } from '../../Tool.js';
import type { Message, ProgressMessage } from '../../types/message.js';
import { adjustHunkLineNumbers, CONTEXT_LINES } from '../../utils/diff.js';
import { FILE_NOT_FOUND_CWD_NOTE, getDisplayPath } from '../../utils/file.js';
import { logError } from '../../utils/log.js';
import { getPlansDirectory } from '../../utils/plans.js';
import { readEditContext } from '../../utils/readEditContext.js';
import { firstLineOf } from '../../utils/stringUtils.js';
import type { ThemeName } from '../../utils/theme.js';
import type { FileEditOutput } from './types.js';
import { findActualString, getPatchForEdit, preserveQuoteStyle } from './utils.js';
export function userFacingName(input: Partial<{
  file_path: string;
  old_string: string;
  new_string: string;
  replace_all: boolean;
  edits: unknown[];
}> | undefined): string {
  if (!input) {
    return 'Update';
  }
  if (input.file_path?.startsWith(getPlansDirectory())) {
    return 'Updated plan';
  }
  // Hashline edits always modify an existing file (line-ref based)
  if (input.edits != null) {
    return 'Update';
  }
  if (input.old_string === '') {
    return 'Create';
  }
  return 'Update';
}
export function getToolUseSummary(input: Partial<{
  file_path: string;
  old_string: string;
  new_string: string;
  replace_all: boolean;

```

---


### `src/tools/FileEditTool/constants.ts`

**信息:**
- 行数: 11
- 大小: 538 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// In its own file to avoid circular dependencies
export const FILE_EDIT_TOOL_NAME = 'Edit'

// Permission pattern for granting session-level access to the project's .claude/ folder
export const CLAUDE_FOLDER_PERMISSION_PATTERN = '/.claude/**'

// Permission pattern for granting session-level access to the global ~/.claude/ folder
export const GLOBAL_CLAUDE_FOLDER_PERMISSION_PATTERN = '~/.claude/**'

export const FILE_UNEXPECTEDLY_MODIFIED_ERROR =
  'File has been unexpectedly modified. Read it again before attempting to write it.'

```

---


### `src/tools/FileEditTool/prompt.ts`

**信息:**
- 行数: 28
- 大小: 1895 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { isCompactLinePrefixEnabled } from '../../utils/file.js'
import { FILE_READ_TOOL_NAME } from '../FileReadTool/prompt.js'

function getPreReadInstruction(): string {
  return `\n- You must use your \`${FILE_READ_TOOL_NAME}\` tool at least once in the conversation before editing. This tool will error if you attempt an edit without reading the file. `
}

export function getEditToolDescription(): string {
  return getDefaultEditDescription()
}

function getDefaultEditDescription(): string {
  const prefixFormat = isCompactLinePrefixEnabled()
    ? 'line number + tab'
    : 'spaces + line number + arrow'
  const minimalUniquenessHint =
    process.env.USER_TYPE === 'ant'
      ? `\n- Use the smallest old_string that's clearly unique — usually 2-4 adjacent lines is sufficient. Avoid including 10+ lines of context when less uniquely identifies the target.`
      : ''
  return `Performs exact string replacements in files.

Usage:${getPreReadInstruction()}
- When editing text from Read tool output, ensure you preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix. The line number prefix format is: ${prefixFormat}. Everything after that is the actual file content to match. Never include any part of the line number prefix in the old_string or new_string.
- ALWAYS prefer editing existing files in the codebase. NEVER write new files unless explicitly required.
- Only use emojis if the user explicitly requests it. Avoid adding emojis to files unless asked.
- The edit will FAIL if \`old_string\` is not unique in the file. Either provide a larger string with more surrounding context to make it unique or use \`replace_all\` to change every instance of \`old_string\`.${minimalUniquenessHint}
- Use \`replace_all\` for replacing and renaming strings across the file. This parameter is useful if you want to rename a variable for instance.`
}

```

---


### `src/tools/FileEditTool/types.ts`

**信息:**
- 行数: 85
- 大小: 2612 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'
import { semanticBoolean } from '../../utils/semanticBoolean.js'

// The input schema with optional replace_all
const inputSchema = lazySchema(() =>
  z.strictObject({
    file_path: z.string().describe('The absolute path to the file to modify'),
    old_string: z.string().describe('The text to replace'),
    new_string: z
      .string()
      .describe(
        'The text to replace it with (must be different from old_string)',
      ),
    replace_all: semanticBoolean(
      z.boolean().default(false).optional(),
    ).describe('Replace all occurrences of old_string (default false)'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

// Parsed output — what call() receives. z.output not z.input: with
// semanticBoolean the input side is unknown (preprocess accepts anything).
export type FileEditInput = z.output<InputSchema>

// Individual edit without file_path
export type EditInput = Omit<FileEditInput, 'file_path'>

// Runtime version where replace_all is always defined
export type FileEdit = {
  old_string: string
  new_string: string
  replace_all: boolean
}

export const hunkSchema = lazySchema(() =>
  z.object({
    oldStart: z.number(),
    oldLines: z.number(),
    newStart: z.number(),
    newLines: z.number(),
    lines: z.array(z.string()),
  }),
)

export const gitDiffSchema = lazySchema(() =>
  z.object({
    filename: z.string(),
    status: z.enum(['modified', 'added']),
    additions: z.number(),

```

---


### `src/tools/FileEditTool/utils.ts`

**信息:**
- 行数: 775
- 大小: 22516 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { type StructuredPatchHunk, structuredPatch } from 'diff'
import { logError } from 'src/utils/log.js'
import { expandPath } from 'src/utils/path.js'
import { countCharInString } from 'src/utils/stringUtils.js'
import {
  DIFF_TIMEOUT_MS,
  getPatchForDisplay,
  getPatchFromContents,
} from '../../utils/diff.js'
import { errorMessage, isENOENT } from '../../utils/errors.js'
import {
  addLineNumbers,
  convertLeadingTabsToSpaces,
  readFileSyncCached,
} from '../../utils/file.js'
import type { EditInput, FileEdit } from './types.js'

// Claude can't output curly quotes, so we define them as constants here for Claude to use
// in the code. We do this because we normalize curly quotes to straight quotes
// when applying edits.
export const LEFT_SINGLE_CURLY_QUOTE = '‘'
export const RIGHT_SINGLE_CURLY_QUOTE = '’'
export const LEFT_DOUBLE_CURLY_QUOTE = '“'
export const RIGHT_DOUBLE_CURLY_QUOTE = '”'

/**
 * Normalizes quotes in a string by converting curly quotes to straight quotes
 * @param str The string to normalize
 * @returns The string with all curly quotes replaced by straight quotes
 */
export function normalizeQuotes(str: string): string {
  return str
    .replaceAll(LEFT_SINGLE_CURLY_QUOTE, "'")
    .replaceAll(RIGHT_SINGLE_CURLY_QUOTE, "'")
    .replaceAll(LEFT_DOUBLE_CURLY_QUOTE, '"')
    .replaceAll(RIGHT_DOUBLE_CURLY_QUOTE, '"')
}

/**
 * Strips trailing whitespace from each line in a string while preserving line endings
 * @param str The string to process
 * @returns The string with trailing whitespace removed from each line
 */
export function stripTrailingWhitespace(str: string): string {
  // Handle different line endings: CRLF, LF, CR
  // Use a regex that matches line endings and captures them
  const lines = str.split(/(\r\n|\n|\r)/)

  let result = ''
  for (let i = 0; i < lines.length; i++) {

```

---


### `src/tools/FileReadTool/FileReadTool.ts`

**信息:**
- 行数: 1183
- 大小: 39073 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Base64ImageSource } from '@anthropic-ai/sdk/resources/index.mjs'
import { readdir, readFile as readFileAsync } from 'fs/promises'
import * as path from 'path'
import { posix, win32 } from 'path'
import { z } from 'zod/v4'
import {
  PDF_AT_MENTION_INLINE_THRESHOLD,
  PDF_EXTRACT_SIZE_THRESHOLD,
  PDF_MAX_PAGES_PER_READ,
} from '../../constants/apiLimits.js'
import { hasBinaryExtension } from '../../constants/files.js'
import { memoryFreshnessNote } from '../../memdir/memoryAge.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import { logEvent } from '../../services/analytics/index.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  getFileExtensionForAnalytics,
} from '../../services/analytics/metadata.js'
import {
  countTokensWithAPI,
  roughTokenCountEstimationForFileType,
} from '../../services/tokenEstimation.js'
import {
  activateConditionalSkillsForPaths,
  addSkillDirectories,
  discoverSkillDirsForPaths,
} from '../../skills/loadSkillsDir.js'
import type { ToolUseContext } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { getCwd } from '../../utils/cwd.js'
import { getClaudeConfigHomeDir, isEnvTruthy } from '../../utils/envUtils.js'
import { getErrnoCode, isENOENT } from '../../utils/errors.js'
import {
  addLineNumbers,
  FILE_NOT_FOUND_CWD_NOTE,
  findSimilarFile,
  getFileModificationTimeAsync,
  suggestPathUnderCwd,
} from '../../utils/file.js'
import { logFileOperation } from '../../utils/fileOperationAnalytics.js'
import { formatFileSize } from '../../utils/format.js'
import { getFsImplementation } from '../../utils/fsOperations.js'
import {
  compressImageBufferWithTokenLimit,
  createImageMetadataText,
  detectImageFormatFromBuffer,
  type ImageDimensions,
  ImageResizeError,
  maybeResizeAndDownsampleImageBuffer,
} from '../../utils/imageResizer.js'

```

---


### `src/tools/FileReadTool/UI.tsx`

**信息:**
- 行数: 185
- 大小: 22540 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import { extractTag } from 'src/utils/messages.js';
import { FallbackToolUseErrorMessage } from '../../components/FallbackToolUseErrorMessage.js';
import { FilePathLink } from '../../components/FilePathLink.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { Text } from '../../ink.js';
import { FILE_NOT_FOUND_CWD_NOTE, getDisplayPath } from '../../utils/file.js';
import { formatFileSize } from '../../utils/format.js';
import { getPlansDirectory } from '../../utils/plans.js';
import { getTaskOutputDir } from '../../utils/task/diskOutput.js';
import type { Input, Output } from './FileReadTool.js';

/**
 * Check if a file path is an agent output file and extract the task ID.
 * Agent output files follow the pattern: {projectTempDir}/tasks/{taskId}.output
 */
function getAgentOutputTaskId(filePath: string): string | null {
  const prefix = `${getTaskOutputDir()}/`;
  const suffix = '.output';
  if (filePath.startsWith(prefix) && filePath.endsWith(suffix)) {
    const taskId = filePath.slice(prefix.length, -suffix.length);
    // Validate it looks like a task ID (alphanumeric, reasonable length)
    if (taskId.length > 0 && taskId.length <= 20 && /^[a-zA-Z0-9_-]+$/.test(taskId)) {
      return taskId;
    }
  }
  return null;
}
export function renderToolUseMessage({
  file_path,
  offset,
  limit,
  pages
}: Partial<Input>, {
  verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  if (!file_path) {
    return null;
  }

  // For agent output files, return empty string so no parentheses are shown
  // The task ID is displayed separately by AssistantToolUseMessage
  if (getAgentOutputTaskId(file_path)) {
    return '';
  }
  const displayPath = verbose ? file_path : getDisplayPath(file_path);
  if (pages) {

```

---


### `src/tools/FileReadTool/imageProcessor.ts`

**信息:**
- 行数: 94
- 大小: 2881 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Buffer } from 'buffer'
import { isInBundledMode } from '../../utils/bundledMode.js'

export type SharpInstance = {
  metadata(): Promise<{ width: number; height: number; format: string }>
  resize(
    width: number,
    height: number,
    options?: { fit?: string; withoutEnlargement?: boolean },
  ): SharpInstance
  jpeg(options?: { quality?: number }): SharpInstance
  png(options?: {
    compressionLevel?: number
    palette?: boolean
    colors?: number
  }): SharpInstance
  webp(options?: { quality?: number }): SharpInstance
  toBuffer(): Promise<Buffer>
}

export type SharpFunction = (input: Buffer) => SharpInstance

type SharpCreatorOptions = {
  create: {
    width: number
    height: number
    channels: 3 | 4
    background: { r: number; g: number; b: number }
  }
}

type SharpCreator = (options: SharpCreatorOptions) => SharpInstance

let imageProcessorModule: { default: SharpFunction } | null = null
let imageCreatorModule: { default: SharpCreator } | null = null

export async function getImageProcessor(): Promise<SharpFunction> {
  if (imageProcessorModule) {
    return imageProcessorModule.default
  }

  if (isInBundledMode()) {
    // Try to load the native image processor first
    try {
      // Use the native image processor module
      const imageProcessor = await import('image-processor-napi')
      const sharp = imageProcessor.sharp || imageProcessor.default
      imageProcessorModule = { default: sharp }
      return sharp
    } catch {

```

---


### `src/tools/FileReadTool/limits.ts`

**信息:**
- 行数: 92
- 大小: 3219 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Read tool output limits.  Two caps apply to text reads:
 *
 *   | limit         | default | checks                    | cost          | on overflow     |
 *   |---------------|---------|---------------------------|---------------|-----------------|
 *   | maxSizeBytes  | 256 KB  | TOTAL FILE SIZE (not out) | 1 stat        | throws pre-read |
 *   | maxTokens     | 25000   | actual output tokens      | API roundtrip | throws post-read|
 *
 * Known mismatch: maxSizeBytes gates on total file size, not the slice.
 * Tested truncating instead of throwing for explicit-limit reads that
 * exceed the byte cap (#21841, Mar 2026).  Reverted: tool error rate
 * dropped but mean tokens rose — the throw path yields a ~100-byte error
 * tool-result while truncation yields ~25K tokens of content at the cap.
 */
import memoize from 'lodash-es/memoize.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from 'src/services/analytics/growthbook.js'
import { MAX_OUTPUT_SIZE } from 'src/utils/file.js'
export const DEFAULT_MAX_OUTPUT_TOKENS = 25000

/**
 * Env var override for max output tokens. Returns undefined when unset/invalid
 * so the caller can fall through to the next precedence tier.
 */
function getEnvMaxTokens(): number | undefined {
  const override = process.env.CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS
  if (override) {
    const parsed = parseInt(override, 10)
    if (!isNaN(parsed) && parsed > 0) {
      return parsed
    }
  }
  return undefined
}

export type FileReadingLimits = {
  maxTokens: number
  maxSizeBytes: number
  includeMaxSizeInPrompt?: boolean
  targetedRangeNudge?: boolean
}

/**
 * Default limits for Read tool when the ToolUseContext doesn't supply an
 * override. Memoized so the GrowthBook value is fixed at first call — avoids
 * the cap changing mid-session as the flag refreshes in the background.
 *
 * Precedence for maxTokens: env var > GrowthBook > DEFAULT_MAX_OUTPUT_TOKENS.
 * (Env var is a user-set override, should beat experiment infrastructure.)
 *
 * Defensive: each field is individually validated; invalid values fall

```

---


### `src/tools/FileReadTool/prompt.ts`

**信息:**
- 行数: 49
- 大小: 2868 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { isPDFSupported } from '../../utils/pdfUtils.js'
import { BASH_TOOL_NAME } from '../BashTool/toolName.js'

// Use a string constant for tool names to avoid circular dependencies
export const FILE_READ_TOOL_NAME = 'Read'

export const FILE_UNCHANGED_STUB =
  'File unchanged since last read. The content from the earlier Read tool_result in this conversation is still current — refer to that instead of re-reading.'

export const MAX_LINES_TO_READ = 2000

export const DESCRIPTION = 'Read a file from the local filesystem.'

export const LINE_FORMAT_INSTRUCTION =
  '- Results are returned using cat -n format, with line numbers starting at 1'

export const OFFSET_INSTRUCTION_DEFAULT =
  "- You can optionally specify a line offset and limit (especially handy for long files), but it's recommended to read the whole file by not providing these parameters"

export const OFFSET_INSTRUCTION_TARGETED =
  '- When you already know which part of the file you need, only read that part. This can be important for larger files.'

/**
 * Renders the Read tool prompt template.  The caller (FileReadTool) supplies
 * the runtime-computed parts.
 */
export function renderPromptTemplate(
  lineFormat: string,
  maxSizeInstruction: string,
  offsetInstruction: string,
): string {
  return `Reads a file from the local filesystem. You can access any file directly by using this tool.
Assume this tool is able to read all files on the machine. If the User provides a path to a file assume that path is valid. It is okay to read a file that does not exist; an error will be returned.

Usage:
- The file_path parameter must be an absolute path, not a relative path
- By default, it reads up to ${MAX_LINES_TO_READ} lines starting from the beginning of the file${maxSizeInstruction}
${offsetInstruction}
${lineFormat}
- This tool allows Claude Code to read images (eg PNG, JPG, etc). When reading an image file the contents are presented visually as Claude Code is a multimodal LLM.${
    isPDFSupported()
      ? '\n- This tool can read PDF files (.pdf). For large PDFs (more than 10 pages), you MUST provide the pages parameter to read specific page ranges (e.g., pages: "1-5"). Reading a large PDF without the pages parameter will fail. Maximum 20 pages per request.'
      : ''
  }
- This tool can read Jupyter notebooks (.ipynb files) and returns all cells with their outputs, combining code, text, and visualizations.
- This tool can only read files, not directories. To read a directory, use an ls command via the ${BASH_TOOL_NAME} tool.
- You will regularly be asked to read screenshots. If the user provides a path to a screenshot, ALWAYS use this tool to view the file at the path. This tool will work with all temporary file paths.
- If you read a file that exists but has empty contents you will receive a system reminder warning in place of file contents.`
}

```

---


### `src/tools/FileWriteTool/FileWriteTool.ts`

**信息:**
- 行数: 434
- 大小: 14927 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { dirname, sep } from 'path'
import { logEvent } from 'src/services/analytics/index.js'
import { z } from 'zod/v4'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import { diagnosticTracker } from '../../services/diagnosticTracking.js'
import { clearDeliveredDiagnosticsForFile } from '../../services/lsp/LSPDiagnosticRegistry.js'
import { getLspServerManager } from '../../services/lsp/manager.js'
import { notifyVscodeFileUpdated } from '../../services/mcp/vscodeSdkMcp.js'
import { checkTeamMemSecrets } from '../../services/teamMemorySync/teamMemSecretGuard.js'
import {
  activateConditionalSkillsForPaths,
  addSkillDirectories,
  discoverSkillDirsForPaths,
} from '../../skills/loadSkillsDir.js'
import type { ToolUseContext } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { getCwd } from '../../utils/cwd.js'
import { logForDebugging } from '../../utils/debug.js'
import { countLinesChanged, getPatchForDisplay } from '../../utils/diff.js'
import { isEnvTruthy } from '../../utils/envUtils.js'
import { isENOENT } from '../../utils/errors.js'
import { getFileModificationTime, writeTextContent } from '../../utils/file.js'
import {
  fileHistoryEnabled,
  fileHistoryTrackEdit,
} from '../../utils/fileHistory.js'
import { logFileOperation } from '../../utils/fileOperationAnalytics.js'
import { readFileSyncWithMetadata } from '../../utils/fileRead.js'
import { getFsImplementation } from '../../utils/fsOperations.js'
import {
  fetchSingleFileGitDiff,
  type ToolUseDiff,
} from '../../utils/gitDiff.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { logError } from '../../utils/log.js'
import { expandPath } from '../../utils/path.js'
import {
  checkWritePermissionForTool,
  matchingRuleForInput,
} from '../../utils/permissions/filesystem.js'
import type { PermissionDecision } from '../../utils/permissions/PermissionResult.js'
import { matchWildcardPattern } from '../../utils/permissions/shellRuleMatching.js'
import { FILE_UNEXPECTEDLY_MODIFIED_ERROR } from '../FileEditTool/constants.js'
import { gitDiffSchema, hunkSchema } from '../FileEditTool/types.js'
import { FILE_WRITE_TOOL_NAME, getWriteToolDescription } from './prompt.js'
import {
  getToolUseSummary,
  isResultTruncated,
  renderToolResultMessage,
  renderToolUseErrorMessage,

```

---


### `src/tools/FileWriteTool/UI.tsx`

**信息:**
- 行数: 405
- 大小: 43788 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import type { StructuredPatchHunk } from 'diff';
import { isAbsolute, relative, resolve } from 'path';
import * as React from 'react';
import { Suspense, use, useState } from 'react';
import { MessageResponse } from 'src/components/MessageResponse.js';
import { extractTag } from 'src/utils/messages.js';
import { CtrlOToExpand } from '../../components/CtrlOToExpand.js';
import { FallbackToolUseErrorMessage } from '../../components/FallbackToolUseErrorMessage.js';
import { FileEditToolUpdatedMessage } from '../../components/FileEditToolUpdatedMessage.js';
import { FileEditToolUseRejectedMessage } from '../../components/FileEditToolUseRejectedMessage.js';
import { FilePathLink } from '../../components/FilePathLink.js';
import { HighlightedCode } from '../../components/HighlightedCode.js';
import { useTerminalSize } from '../../hooks/useTerminalSize.js';
import { Box, Text } from '../../ink.js';
import type { ToolProgressData } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import { getCwd } from '../../utils/cwd.js';
import { getPatchForDisplay } from '../../utils/diff.js';
import { getDisplayPath } from '../../utils/file.js';
import { logError } from '../../utils/log.js';
import { getPlansDirectory } from '../../utils/plans.js';
import { openForScan, readCapped } from '../../utils/readEditContext.js';
import type { Output } from './FileWriteTool.js';
const MAX_LINES_TO_RENDER = 10;
// Model output uses \n regardless of platform, so always split on \n.
// os.EOL is \r\n on Windows, which would give numLines=1 for all files.
const EOL = '\n';

/**
 * Count visible lines in file content. A trailing newline is treated as a
 * line terminator (not a new empty line), matching editor line numbering.
 */
export function countLines(content: string): number {
  const parts = content.split(EOL);
  return content.endsWith(EOL) ? parts.length - 1 : parts.length;
}
function FileWriteToolCreatedMessage(t0) {
  const $ = _c(25);
  const {
    filePath,
    content,
    verbose
  } = t0;
  const {
    columns
  } = useTerminalSize();
  const contentWithFallback = content || "(No content)";
  const numLines = countLines(content);

```

---


### `src/tools/FileWriteTool/prompt.ts`

**信息:**
- 行数: 18
- 大小: 969 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { FILE_READ_TOOL_NAME } from '../FileReadTool/prompt.js'

export const FILE_WRITE_TOOL_NAME = 'Write'
export const DESCRIPTION = 'Write a file to the local filesystem.'

function getPreReadInstruction(): string {
  return `\n- If this is an existing file, you MUST use the ${FILE_READ_TOOL_NAME} tool first to read the file's contents. This tool will fail if you did not read the file first.`
}

export function getWriteToolDescription(): string {
  return `Writes a file to the local filesystem.

Usage:
- This tool will overwrite the existing file if there is one at the provided path.${getPreReadInstruction()}
- Prefer the Edit tool for modifying existing files \u2014 it only sends the diff. Only use this tool to create new files or for complete rewrites.
- NEVER create documentation files (*.md) or README files unless explicitly requested by the User.
- Only use emojis if the user explicitly requests it. Avoid writing emojis to files unless asked.`
}

```

---


### `src/tools/GlobTool/GlobTool.ts`

**信息:**
- 行数: 198
- 大小: 6064 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import type { ValidationResult } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { getCwd } from '../../utils/cwd.js'
import { isENOENT } from '../../utils/errors.js'
import {
  FILE_NOT_FOUND_CWD_NOTE,
  suggestPathUnderCwd,
} from '../../utils/file.js'
import { getFsImplementation } from '../../utils/fsOperations.js'
import { glob } from '../../utils/glob.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { expandPath, toRelativePath } from '../../utils/path.js'
import { checkReadPermissionForTool } from '../../utils/permissions/filesystem.js'
import type { PermissionDecision } from '../../utils/permissions/PermissionResult.js'
import { matchWildcardPattern } from '../../utils/permissions/shellRuleMatching.js'
import { DESCRIPTION, GLOB_TOOL_NAME } from './prompt.js'
import {
  getToolUseSummary,
  renderToolResultMessage,
  renderToolUseErrorMessage,
  renderToolUseMessage,
  userFacingName,
} from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    pattern: z.string().describe('The glob pattern to match files against'),
    path: z
      .string()
      .optional()
      .describe(
        'The directory to search in. If not specified, the current working directory will be used. IMPORTANT: Omit this field to use the default directory. DO NOT enter "undefined" or "null" - simply omit it for the default behavior. Must be a valid directory path if provided.',
      ),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    durationMs: z
      .number()
      .describe('Time taken to execute the search in milliseconds'),
    numFiles: z.number().describe('Total number of files found'),
    filenames: z
      .array(z.string())
      .describe('Array of file paths that match the pattern'),
    truncated: z
      .boolean()
      .describe('Whether results were truncated (limited to 100 files)'),

```

---


### `src/tools/GlobTool/UI.tsx`

**信息:**
- 行数: 63
- 大小: 8040 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import React from 'react';
import { MessageResponse } from 'src/components/MessageResponse.js';
import { extractTag } from 'src/utils/messages.js';
import { FallbackToolUseErrorMessage } from '../../components/FallbackToolUseErrorMessage.js';
import { TOOL_SUMMARY_MAX_LENGTH } from '../../constants/toolLimits.js';
import { Text } from '../../ink.js';
import { FILE_NOT_FOUND_CWD_NOTE, getDisplayPath } from '../../utils/file.js';
import { truncate } from '../../utils/format.js';
import { GrepTool } from '../GrepTool/GrepTool.js';
export function userFacingName(): string {
  return 'Search';
}
export function renderToolUseMessage({
  pattern,
  path
}: Partial<{
  pattern: string;
  path: string;
}>, {
  verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  if (!pattern) {
    return null;
  }
  if (!path) {
    return `pattern: "${pattern}"`;
  }
  return `pattern: "${pattern}", path: "${verbose ? path : getDisplayPath(path)}"`;
}
export function renderToolUseErrorMessage(result: ToolResultBlockParam['content'], {
  verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  if (!verbose && typeof result === 'string' && extractTag(result, 'tool_use_error')) {
    const errorMessage = extractTag(result, 'tool_use_error');
    if (errorMessage?.includes(FILE_NOT_FOUND_CWD_NOTE)) {
      return <MessageResponse>
          <Text color="error">File not found</Text>
        </MessageResponse>;
    }
    return <MessageResponse>
        <Text color="error">Error searching files</Text>
      </MessageResponse>;
  }
  return <FallbackToolUseErrorMessage result={result} verbose={verbose} />;
}

```

---


### `src/tools/GlobTool/prompt.ts`

**信息:**
- 行数: 7
- 大小: 439 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const GLOB_TOOL_NAME = 'Glob'

export const DESCRIPTION = `- Fast file pattern matching tool that works with any codebase size
- Supports glob patterns like "**/*.js" or "src/**/*.ts"
- Returns matching file paths sorted by modification time
- Use this tool when you need to find files by name patterns
- When you are doing an open ended search that may require multiple rounds of globbing and grepping, use the Agent tool instead`

```

---


### `src/tools/GrepTool/GrepTool.ts`

**信息:**
- 行数: 577
- 大小: 20087 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import type { ValidationResult } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { getCwd } from '../../utils/cwd.js'
import { isENOENT } from '../../utils/errors.js'
import {
  FILE_NOT_FOUND_CWD_NOTE,
  suggestPathUnderCwd,
} from '../../utils/file.js'
import { getFsImplementation } from '../../utils/fsOperations.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { expandPath, toRelativePath } from '../../utils/path.js'
import {
  checkReadPermissionForTool,
  getFileReadIgnorePatterns,
  normalizePatternsToPath,
} from '../../utils/permissions/filesystem.js'
import type { PermissionDecision } from '../../utils/permissions/PermissionResult.js'
import { matchWildcardPattern } from '../../utils/permissions/shellRuleMatching.js'
import { getGlobExclusionsForPluginCache } from '../../utils/plugins/orphanedPluginFilter.js'
import { ripGrep } from '../../utils/ripgrep.js'
import { semanticBoolean } from '../../utils/semanticBoolean.js'
import { semanticNumber } from '../../utils/semanticNumber.js'
import { plural } from '../../utils/stringUtils.js'
import { GREP_TOOL_NAME, getDescription } from './prompt.js'
import {
  getToolUseSummary,
  renderToolResultMessage,
  renderToolUseErrorMessage,
  renderToolUseMessage,
} from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    pattern: z
      .string()
      .describe(
        'The regular expression pattern to search for in file contents',
      ),
    path: z
      .string()
      .optional()
      .describe(
        'File or directory to search in (rg PATH). Defaults to current working directory.',
      ),
    glob: z
      .string()
      .optional()
      .describe(
        'Glob pattern to filter files (e.g. "*.js", "*.{ts,tsx}") - maps to rg --glob',

```

---


### `src/tools/GrepTool/UI.tsx`

**信息:**
- 行数: 201
- 大小: 21784 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import React from 'react';
import { CtrlOToExpand } from '../../components/CtrlOToExpand.js';
import { FallbackToolUseErrorMessage } from '../../components/FallbackToolUseErrorMessage.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { TOOL_SUMMARY_MAX_LENGTH } from '../../constants/toolLimits.js';
import { Box, Text } from '../../ink.js';
import type { ToolProgressData } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import { FILE_NOT_FOUND_CWD_NOTE, getDisplayPath } from '../../utils/file.js';
import { truncate } from '../../utils/format.js';
import { extractTag } from '../../utils/messages.js';

// Reusable component for search result summaries
function SearchResultSummary(t0) {
  const $ = _c(26);
  const {
    count,
    countLabel,
    secondaryCount,
    secondaryLabel,
    content,
    verbose
  } = t0;
  let t1;
  if ($[0] !== count) {
    t1 = <Text bold={true}>{count} </Text>;
    $[0] = count;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] !== count || $[3] !== countLabel) {
    t2 = count === 0 || count > 1 ? countLabel : countLabel.slice(0, -1);
    $[2] = count;
    $[3] = countLabel;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  let t3;
  if ($[5] !== t1 || $[6] !== t2) {
    t3 = <Text>Found {t1}{t2}</Text>;
    $[5] = t1;
    $[6] = t2;
    $[7] = t3;
  } else {
    t3 = $[7];

```

---


### `src/tools/GrepTool/prompt.ts`

**信息:**
- 行数: 18
- 大小: 1150 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { AGENT_TOOL_NAME } from '../AgentTool/constants.js'
import { BASH_TOOL_NAME } from '../BashTool/toolName.js'

export const GREP_TOOL_NAME = 'Grep'

export function getDescription(): string {
  return `A powerful search tool built on ripgrep

  Usage:
  - ALWAYS use ${GREP_TOOL_NAME} for search tasks. NEVER invoke \`grep\` or \`rg\` as a ${BASH_TOOL_NAME} command. The ${GREP_TOOL_NAME} tool has been optimized for correct permissions and access.
  - Supports full regex syntax (e.g., "log.*Error", "function\\s+\\w+")
  - Filter files with glob parameter (e.g., "*.js", "**/*.tsx") or type parameter (e.g., "js", "py", "rust")
  - Output modes: "content" shows matching lines, "files_with_matches" shows only file paths (default), "count" shows match counts
  - Use ${AGENT_TOOL_NAME} tool for open-ended searches requiring multiple rounds
  - Pattern syntax: Uses ripgrep (not grep) - literal braces need escaping (use \`interface\\{\\}\` to find \`interface{}\` in Go code)
  - Multiline matching: By default patterns match within single lines only. For cross-line patterns like \`struct \\{[\\s\\S]*?field\`, use \`multiline: true\`
`
}

```

---


### `src/tools/LSPTool/LSPTool.ts`

**信息:**
- 行数: 860
- 大小: 25710 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { open } from 'fs/promises'
import * as path from 'path'
import { pathToFileURL } from 'url'
import type {
  CallHierarchyIncomingCall,
  CallHierarchyItem,
  CallHierarchyOutgoingCall,
  DocumentSymbol,
  Hover,
  Location,
  LocationLink,
  SymbolInformation,
} from 'vscode-languageserver-types'
import { z } from 'zod/v4'
import {
  getInitializationStatus,
  getLspServerManager,
  isLspConnected,
  waitForInitialization,
} from '../../services/lsp/manager.js'
import type { ValidationResult } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { uniq } from '../../utils/array.js'
import { getCwd } from '../../utils/cwd.js'
import { logForDebugging } from '../../utils/debug.js'
import { isENOENT, toError } from '../../utils/errors.js'
import { execFileNoThrowWithCwd } from '../../utils/execFileNoThrow.js'
import { getFsImplementation } from '../../utils/fsOperations.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { logError } from '../../utils/log.js'
import { expandPath } from '../../utils/path.js'
import { checkReadPermissionForTool } from '../../utils/permissions/filesystem.js'
import type { PermissionDecision } from '../../utils/permissions/PermissionResult.js'
import {
  formatDocumentSymbolResult,
  formatFindReferencesResult,
  formatGoToDefinitionResult,
  formatHoverResult,
  formatIncomingCallsResult,
  formatOutgoingCallsResult,
  formatPrepareCallHierarchyResult,
  formatWorkspaceSymbolResult,
} from './formatters.js'
import { DESCRIPTION, LSP_TOOL_NAME } from './prompt.js'
import { lspToolInputSchema } from './schemas.js'
import {
  renderToolResultMessage,
  renderToolUseErrorMessage,
  renderToolUseMessage,
  userFacingName,

```

---


### `src/tools/LSPTool/UI.tsx`

**信息:**
- 行数: 228
- 大小: 25038 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import React from 'react';
import { CtrlOToExpand } from '../../components/CtrlOToExpand.js';
import { FallbackToolUseErrorMessage } from '../../components/FallbackToolUseErrorMessage.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { Box, Text } from '../../ink.js';
import { getDisplayPath } from '../../utils/file.js';
import { extractTag } from '../../utils/messages.js';
import type { Input, Output } from './LSPTool.js';
import { getSymbolAtPosition } from './symbolContext.js';

// Lookup map for operation-specific labels
const OPERATION_LABELS: Record<Input['operation'], {
  singular: string;
  plural: string;
  special?: string;
}> = {
  goToDefinition: {
    singular: 'definition',
    plural: 'definitions'
  },
  findReferences: {
    singular: 'reference',
    plural: 'references'
  },
  documentSymbol: {
    singular: 'symbol',
    plural: 'symbols'
  },
  workspaceSymbol: {
    singular: 'symbol',
    plural: 'symbols'
  },
  hover: {
    singular: 'hover info',
    plural: 'hover info',
    special: 'available'
  },
  goToImplementation: {
    singular: 'implementation',
    plural: 'implementations'
  },
  prepareCallHierarchy: {
    singular: 'call item',
    plural: 'call items'
  },
  incomingCalls: {
    singular: 'caller',
    plural: 'callers'

```

---


### `src/tools/LSPTool/formatters.ts`

**信息:**
- 行数: 592
- 大小: 17399 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { relative } from 'path'
import type {
  CallHierarchyIncomingCall,
  CallHierarchyItem,
  CallHierarchyOutgoingCall,
  DocumentSymbol,
  Hover,
  Location,
  LocationLink,
  MarkedString,
  MarkupContent,
  SymbolInformation,
  SymbolKind,
} from 'vscode-languageserver-types'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { plural } from '../../utils/stringUtils.js'

/**
 * Formats a URI by converting it to a relative path if possible.
 * Handles URI decoding and gracefully falls back to un-decoded path if malformed.
 * Only uses relative paths when shorter and not starting with ../../
 */
function formatUri(uri: string | undefined, cwd?: string): string {
  // Handle undefined/null URIs - this indicates malformed LSP data
  if (!uri) {
    // NOTE: This should ideally be caught earlier with proper error logging
    // This is a defensive backstop in the formatting layer
    logForDebugging(
      'formatUri called with undefined URI - indicates malformed LSP server response',
      { level: 'warn' },
    )
    return '<unknown location>'
  }

  // Remove file:// protocol if present
  // On Windows, file:///C:/path becomes /C:/path after replacing file://
  // We need to strip the leading slash for Windows drive-letter paths
  let filePath = uri.replace(/^file:\/\//, '')
  if (/^\/[A-Za-z]:/.test(filePath)) {
    filePath = filePath.slice(1)
  }

  // Decode URI encoding - handle malformed URIs gracefully
  try {
    filePath = decodeURIComponent(filePath)
  } catch (error) {
    // Log for debugging but continue with un-decoded path
    const errorMsg = errorMessage(error)
    logForDebugging(

```

---


### `src/tools/LSPTool/prompt.ts`

**信息:**
- 行数: 21
- 大小: 1114 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const LSP_TOOL_NAME = 'LSP' as const

export const DESCRIPTION = `Interact with Language Server Protocol (LSP) servers to get code intelligence features.

Supported operations:
- goToDefinition: Find where a symbol is defined
- findReferences: Find all references to a symbol
- hover: Get hover information (documentation, type info) for a symbol
- documentSymbol: Get all symbols (functions, classes, variables) in a document
- workspaceSymbol: Search for symbols across the entire workspace
- goToImplementation: Find implementations of an interface or abstract method
- prepareCallHierarchy: Get call hierarchy item at a position (functions/methods)
- incomingCalls: Find all functions/methods that call the function at a position
- outgoingCalls: Find all functions/methods called by the function at a position

All operations require:
- filePath: The file to operate on
- line: The line number (1-based, as shown in editors)
- character: The character offset (1-based, as shown in editors)

Note: LSP servers must be configured for the file type. If no server is available, an error will be returned.`

```

---


### `src/tools/LSPTool/schemas.ts`

**信息:**
- 行数: 215
- 大小: 6064 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { lazySchema } from '../../utils/lazySchema.js'

/**
 * Discriminated union of all LSP operations
 * Uses 'operation' as the discriminator field
 */
export const lspToolInputSchema = lazySchema(() => {
  /**
   * Go to Definition operation
   * Finds the definition location of a symbol at the given position
   */
  const goToDefinitionSchema = z.strictObject({
    operation: z.literal('goToDefinition'),
    filePath: z.string().describe('The absolute or relative path to the file'),
    line: z
      .number()
      .int()
      .positive()
      .describe('The line number (1-based, as shown in editors)'),
    character: z
      .number()
      .int()
      .positive()
      .describe('The character offset (1-based, as shown in editors)'),
  })

  /**
   * Find References operation
   * Finds all references to a symbol at the given position
   */
  const findReferencesSchema = z.strictObject({
    operation: z.literal('findReferences'),
    filePath: z.string().describe('The absolute or relative path to the file'),
    line: z
      .number()
      .int()
      .positive()
      .describe('The line number (1-based, as shown in editors)'),
    character: z
      .number()
      .int()
      .positive()
      .describe('The character offset (1-based, as shown in editors)'),
  })

  /**
   * Hover operation
   * Gets hover information (documentation, type info) for a symbol at the given position
   */

```

---


### `src/tools/LSPTool/symbolContext.ts`

**信息:**
- 行数: 90
- 大小: 3392 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { logForDebugging } from '../../utils/debug.js'
import { truncate } from '../../utils/format.js'
import { getFsImplementation } from '../../utils/fsOperations.js'
import { expandPath } from '../../utils/path.js'

const MAX_READ_BYTES = 64 * 1024

/**
 * Extracts the symbol/word at a specific position in a file.
 * Used to show context in tool use messages.
 *
 * @param filePath - The file path (absolute or relative)
 * @param line - 0-indexed line number
 * @param character - 0-indexed character position on the line
 *
 * Note: This uses synchronous file I/O because it is called from
 * renderToolUseMessage (a synchronous React render function). The read is
 * wrapped in try/catch so ENOENT and other errors fall back gracefully.
 * @returns The symbol at that position, or null if extraction fails
 */
export function getSymbolAtPosition(
  filePath: string,
  line: number,
  character: number,
): string | null {
  try {
    const fs = getFsImplementation()
    const absolutePath = expandPath(filePath)

    // Read only the first 64KB instead of the whole file. Most LSP hover/goto
    // targets are near recent edits; 64KB covers ~1000 lines of typical code.
    // If the target line is past this window we fall back to null (the UI
    // already handles that by showing `position: line:char`).
    // eslint-disable-next-line custom-rules/no-sync-fs -- called from sync React render (renderToolUseMessage)
    const { buffer, bytesRead } = fs.readSync(absolutePath, {
      length: MAX_READ_BYTES,
    })
    const content = buffer.toString('utf-8', 0, bytesRead)
    const lines = content.split('\n')

    if (line < 0 || line >= lines.length) {
      return null
    }
    // If we filled the full buffer the file continues past our window,
    // so the last split element may be truncated mid-line.
    if (bytesRead === MAX_READ_BYTES && line === lines.length - 1) {
      return null
    }

    const lineContent = lines[line]

```

---


### `src/tools/ListMcpResourcesTool/ListMcpResourcesTool.ts`

**信息:**
- 行数: 123
- 大小: 3907 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import {
  ensureConnectedClient,
  fetchResourcesForClient,
} from '../../services/mcp/client.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { errorMessage } from '../../utils/errors.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { logMCPError } from '../../utils/log.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { isOutputLineTruncated } from '../../utils/terminal.js'
import { DESCRIPTION, LIST_MCP_RESOURCES_TOOL_NAME, PROMPT } from './prompt.js'
import { renderToolResultMessage, renderToolUseMessage } from './UI.js'

const inputSchema = lazySchema(() =>
  z.object({
    server: z
      .string()
      .optional()
      .describe('Optional server name to filter resources by'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.array(
    z.object({
      uri: z.string().describe('Resource URI'),
      name: z.string().describe('Resource name'),
      mimeType: z.string().optional().describe('MIME type of the resource'),
      description: z.string().optional().describe('Resource description'),
      server: z.string().describe('Server that provides this resource'),
    }),
  ),
)
type OutputSchema = ReturnType<typeof outputSchema>

export type Output = z.infer<OutputSchema>

export const ListMcpResourcesTool = buildTool({
  isConcurrencySafe() {
    return true
  },
  isReadOnly() {
    return true
  },
  toAutoClassifierInput(input) {
    return input.server ?? ''
  },
  shouldDefer: true,

```

---


### `src/tools/ListMcpResourcesTool/UI.tsx`

**信息:**
- 行数: 29
- 大小: 4757 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import { MessageResponse } from '../../components/MessageResponse.js';
import { OutputLine } from '../../components/shell/OutputLine.js';
import { Text } from '../../ink.js';
import type { ToolProgressData } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import { jsonStringify } from '../../utils/slowOperations.js';
import type { Output } from './ListMcpResourcesTool.js';
export function renderToolUseMessage(input: Partial<{
  server?: string;
}>): React.ReactNode {
  return input.server ? `List MCP resources from server "${input.server}"` : `List all MCP resources`;
}
export function renderToolResultMessage(output: Output, _progressMessagesForMessage: ProgressMessage<ToolProgressData>[], {
  verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  if (!output || output.length === 0) {
    return <MessageResponse height={1}>
        <Text dimColor>(No resources found)</Text>
      </MessageResponse>;
  }

  // eslint-disable-next-line no-restricted-syntax -- human-facing UI, not tool_result
  const formattedOutput = jsonStringify(output, null, 2);
  return <OutputLine content={formattedOutput} verbose={verbose} />;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIk1lc3NhZ2VSZXNwb25zZSIsIk91dHB1dExpbmUiLCJUZXh0IiwiVG9vbFByb2dyZXNzRGF0YSIsIlByb2dyZXNzTWVzc2FnZSIsImpzb25TdHJpbmdpZnkiLCJPdXRwdXQiLCJyZW5kZXJUb29sVXNlTWVzc2FnZSIsImlucHV0IiwiUGFydGlhbCIsInNlcnZlciIsIlJlYWN0Tm9kZSIsInJlbmRlclRvb2xSZXN1bHRNZXNzYWdlIiwib3V0cHV0IiwiX3Byb2dyZXNzTWVzc2FnZXNGb3JNZXNzYWdlIiwidmVyYm9zZSIsImxlbmd0aCIsImZvcm1hdHRlZE91dHB1dCJdLCJzb3VyY2VzIjpbIlVJLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IE1lc3NhZ2VSZXNwb25zZSB9IGZyb20gJy4uLy4uL2NvbXBvbmVudHMvTWVzc2FnZVJlc3BvbnNlLmpzJ1xuaW1wb3J0IHsgT3V0cHV0TGluZSB9IGZyb20gJy4uLy4uL2NvbXBvbmVudHMvc2hlbGwvT3V0cHV0TGluZS5qcydcbmltcG9ydCB7IFRleHQgfSBmcm9tICcuLi8uLi9pbmsuanMnXG5pbXBvcnQgdHlwZSB7IFRvb2xQcm9ncmVzc0RhdGEgfSBmcm9tICcuLi8uLi9Ub29sLmpzJ1xuaW1wb3J0IHR5cGUgeyBQcm9ncmVzc01lc3NhZ2UgfSBmcm9tICcuLi8uLi90eXBlcy9tZXNzYWdlLmpzJ1xuaW1wb3J0IHsganNvblN0cmluZ2lmeSB9IGZyb20gJy4uLy4uL3V0aWxzL3Nsb3dPcGVyYXRpb25zLmpzJ1xuaW1wb3J0IHR5cGUgeyBPdXRwdXQgfSBmcm9tICcuL0xpc3RNY3BSZXNvdXJjZXNUb29sLmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gcmVuZGVyVG9vbFVzZU1lc3NhZ2UoXG4gIGlucHV0OiBQYXJ0aWFsPHsgc2VydmVyPzogc3RyaW5nIH0+LFxuKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgcmV0dXJuIGlucHV0LnNlcnZlclxuICAgID8gYExpc3QgTUNQIHJlc291cmNlcyBmcm9tIHNlcnZlciBcIiR7aW5wdXQuc2VydmVyfVwiYFxuICAgIDogYExpc3QgYWxsIE1DUCByZXNvdXJjZXNgXG59XG5cbmV4cG9ydCBmdW5jdGlvbiByZW5kZXJUb29sUmVzdWx0TWVzc2FnZShcbiAgb3V0cHV0OiBPdXRwdXQsXG4gIF9wcm9ncmVzc01lc3NhZ2VzRm9yTWVzc2FnZTogUHJvZ3Jlc3NNZXNzYWdlPFRvb2xQcm9ncmVzc0RhdGE+W10sXG4gIHsgdmVyYm9zZSB9OiB7IHZlcmJvc2U6IGJvb2xlYW4gfSxcbik6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIGlmICghb3V0cHV0IHx8IG91dHB1dC5sZW5ndGggPT09IDApIHtcbiAgICByZXR1cm4gKFxuICAgICAgPE1lc3NhZ2VSZXNwb25zZSBoZWlnaHQ9ezF9PlxuICAgICAgICA8VGV4dCBkaW1Db2xvcj4oTm8gcmVzb3VyY2VzIGZvdW5kKTwvVGV4dD5cbiAgICAgIDwvTWVzc2FnZVJlc3BvbnNlPlxuICAgIClcbiAgfVxuXG4gIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBuby1yZXN0cmljdGVkLXN5bnRheCAtLSBodW1hbi1mYWNpbmcgVUksIG5vdCB0b29sX3Jlc3VsdFxuICBjb25zdCBmb3JtYXR0ZWRPdXRwdXQgPSBqc29uU3RyaW5naWZ5KG91dHB1dCwgbnVsbCwgMilcblxuICByZXR1cm4gPE91dHB1dExpbmUgY29udGVudD17Zm9ybWF0dGVkT3V0cHV0fSB2ZXJib3NlPXt2ZXJib3NlfSAvPlxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPLEtBQUtBLEtBQUssTUFBTSxPQUFPO0FBQzlCLFNBQVNDLGVBQWUsUUFBUSxxQ0FBcUM7QUFDckUsU0FBU0MsVUFBVSxRQUFRLHNDQUFzQztBQUNqRSxTQUFTQyxJQUFJLFFBQVEsY0FBYztBQUNuQyxjQUFjQyxnQkFBZ0IsUUFBUSxlQUFlO0FBQ3JELGNBQWNDLGVBQWUsUUFBUSx3QkFBd0I7QUFDN0QsU0FBU0MsYUFBYSxRQUFRLCtCQUErQjtBQUM3RCxjQUFjQyxNQUFNLFFBQVEsMkJBQTJCO0FBRXZELE9BQU8sU0FBU0Msb0JBQW9CQSxDQUNsQ0MsS0FBSyxFQUFFQyxPQUFPLENBQUM7RUFBRUMsTUFBTSxDQUFDLEVBQUUsTUFBTTtBQUFDLENBQUMsQ0FBQyxDQUNwQyxFQUFFWCxLQUFLLENBQUNZLFNBQVMsQ0FBQztFQUNqQixPQUFPSCxLQUFLLENBQUNFLE1BQU0sR0FDZixtQ0FBbUNGLEtBQUssQ0FBQ0UsTUFBTSxHQUFHLEdBQ2xELHdCQUF3QjtBQUM5QjtBQUVBLE9BQU8sU0FBU0UsdUJBQXVCQSxDQUNyQ0MsTUFBTSxFQUFFUCxNQUFNLEVBQ2RRLDJCQUEyQixFQUFFVixlQUFlLENBQUNELGdCQUFnQixDQUFDLEVBQUUsRUFDaEU7RUFBRVk7QUFBOEIsQ0FBckIsRUFBRTtFQUFFQSxPQUFPLEVBQUUsT0FBTztBQUFDLENBQUMsQ0FDbEMsRUFBRWhCLEtBQUssQ0FBQ1ksU0FBUyxDQUFDO0VBQ2pCLElBQUksQ0FBQ0UsTUFBTSxJQUFJQSxNQUFNLENBQUNHLE1BQU0sS0FBSyxDQUFDLEVBQUU7SUFDbEMsT0FDRSxDQUFDLGVBQWUsQ0FBQyxNQUFNLENBQUMsQ0FBQyxDQUFDLENBQUM7QUFDakMsUUFBUSxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsb0JBQW9CLEVBQUUsSUFBSTtBQUNqRCxNQUFNLEVBQUUsZUFBZSxDQUFDO0VBRXRCOztFQUVBO0VBQ0EsTUFBTUMsZUFBZSxHQUFHWixhQUFhLENBQUNRLE1BQU0sRUFBRSxJQUFJLEVBQUUsQ0FBQyxDQUFDO0VBRXRELE9BQU8sQ0FBQyxVQUFVLENBQUMsT0FBTyxDQUFDLENBQUNJLGVBQWUsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDRixPQUFPLENBQUMsR0FBRztBQUNuRSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/tools/ListMcpResourcesTool/prompt.ts`

**信息:**
- 行数: 20
- 大小: 776 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const LIST_MCP_RESOURCES_TOOL_NAME = 'ListMcpResourcesTool'

export const DESCRIPTION = `
Lists available resources from configured MCP servers.
Each resource object includes a 'server' field indicating which server it's from.

Usage examples:
- List all resources from all servers: \`listMcpResources\`
- List resources from a specific server: \`listMcpResources({ server: "myserver" })\`
`

export const PROMPT = `
List available resources from configured MCP servers.
Each returned resource will include all standard MCP resource fields plus a 'server' field 
indicating which server the resource belongs to.

Parameters:
- server (optional): The name of a specific MCP server to get resources from. If not provided,
  resources from all servers will be returned.
`

```

---


### `src/tools/MCPTool/MCPTool.ts`

**信息:**
- 行数: 77
- 大小: 2170 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { buildTool, type ToolDef } from '../../Tool.js'
import { lazySchema } from '../../utils/lazySchema.js'
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js'
import { isOutputLineTruncated } from '../../utils/terminal.js'
import { DESCRIPTION, PROMPT } from './prompt.js'
import {
  renderToolResultMessage,
  renderToolUseMessage,
  renderToolUseProgressMessage,
} from './UI.js'

// Allow any input object since MCP tools define their own schemas
export const inputSchema = lazySchema(() => z.object({}).passthrough())
type InputSchema = ReturnType<typeof inputSchema>

export const outputSchema = lazySchema(() =>
  z.string().describe('MCP tool execution result'),
)
type OutputSchema = ReturnType<typeof outputSchema>

export type Output = z.infer<OutputSchema>

// Re-export MCPProgress from centralized types to break import cycles
export type { MCPProgress } from '../../types/tools.js'

export const MCPTool = buildTool({
  isMcp: true,
  // Overridden in mcpClient.ts with the real MCP tool name + args
  isOpenWorld() {
    return false
  },
  // Overridden in mcpClient.ts
  name: 'mcp',
  maxResultSizeChars: 100_000,
  // Overridden in mcpClient.ts
  async description() {
    return DESCRIPTION
  },
  // Overridden in mcpClient.ts
  async prompt() {
    return PROMPT
  },
  get inputSchema(): InputSchema {
    return inputSchema()
  },
  get outputSchema(): OutputSchema {
    return outputSchema()
  },
  // Overridden in mcpClient.ts

```

---


### `src/tools/MCPTool/UI.tsx`

**信息:**
- 行数: 403
- 大小: 50730 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { feature } from 'bun:bundle';
import figures from 'figures';
import * as React from 'react';
import type { z } from 'zod/v4';
import { ProgressBar } from '../../components/design-system/ProgressBar.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { linkifyUrlsInText, OutputLine } from '../../components/shell/OutputLine.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { Ansi, Box, Text } from '../../ink.js';
import type { ToolProgressData } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import type { MCPProgress } from '../../types/tools.js';
import { formatNumber } from '../../utils/format.js';
import { createHyperlink } from '../../utils/hyperlink.js';
import { getContentSizeEstimate, type MCPToolResult } from '../../utils/mcpValidation.js';
import { jsonParse, jsonStringify } from '../../utils/slowOperations.js';
import type { inputSchema } from './MCPTool.js';

// Threshold for displaying warning about large MCP responses
const MCP_OUTPUT_WARNING_THRESHOLD_TOKENS = 10_000;

// In non-verbose mode, truncate individual input values to keep the header
// compact. Matches BashTool's philosophy of showing enough to identify the
// call without dumping the entire payload inline.
const MAX_INPUT_VALUE_CHARS = 80;

// Max number of top-level keys before we fall back to raw JSON display.
// Beyond this a flat k:v list is more noise than help.
const MAX_FLAT_JSON_KEYS = 12;

// Don't attempt flat-object parsing for large blobs.
const MAX_FLAT_JSON_CHARS = 5_000;

// Don't attempt to parse JSON blobs larger than this (perf safety).
const MAX_JSON_PARSE_CHARS = 200_000;

// A string value is "dominant text payload" if it has newlines or is
// long enough that inline display would be worse than unwrapping.
const UNWRAP_MIN_STRING_LEN = 200;
export function renderToolUseMessage(input: z.infer<ReturnType<typeof inputSchema>>, {
  verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  if (Object.keys(input).length === 0) {
    return '';
  }
  return Object.entries(input).map(([key, value]) => {
    let rendered = jsonStringify(value);

```

---


### `src/tools/MCPTool/classifyForCollapse.ts`

**信息:**
- 行数: 604
- 大小: 15178 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Classify an MCP tool as a search/read operation for UI collapsing.
 * Returns { isSearch: false, isRead: false } for tools that should not
 * collapse (e.g., send_message, create_*, update_*).
 *
 * Uses explicit per-tool allowlists for the most common MCP servers.
 * Tool names are stable across installs (even when the server name varies,
 * e.g., "slack" vs "claude_ai_Slack"), so matching is keyed on the tool
 * name alone after normalizing camelCase/kebab-case to snake_case.
 * Unknown tool names don't collapse (conservative).
 */

// prettier-ignore
const SEARCH_TOOLS = new Set([
  // Slack (hosted + @modelcontextprotocol/server-slack)
  'slack_search_public',
  'slack_search_public_and_private',
  'slack_search_channels',
  'slack_search_users',
  // GitHub (github/github-mcp-server)
  'search_code',
  'search_repositories',
  'search_issues',
  'search_pull_requests',
  'search_orgs',
  'search_users',
  // Linear (mcp.linear.app)
  'search_documentation',
  // Datadog (mcp.datadoghq.com)
  'search_logs',
  'search_spans',
  'search_rum_events',
  'search_audit_logs',
  'search_monitors',
  'search_monitor_groups',
  'find_slow_spans',
  'find_monitors_matching_pattern',
  // Sentry (getsentry/sentry-mcp)
  'search_docs',
  'search_events',
  'search_issue_events',
  'find_organizations',
  'find_teams',
  'find_projects',
  'find_releases',
  'find_dsns',
  // Notion (mcp.notion.com — kebab-case, normalized)
  'search',
  // Gmail (claude.ai hosted)
  'gmail_search_messages',

```

---


### `src/tools/MCPTool/prompt.ts`

**信息:**
- 行数: 3
- 大小: 119 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Actual prompt and description are overridden in mcpClient.ts
export const PROMPT = ''
export const DESCRIPTION = ''

```

---


### `src/tools/McpAuthTool/McpAuthTool.ts`

**信息:**
- 行数: 215
- 大小: 7873 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import reject from 'lodash-es/reject.js'
import { z } from 'zod/v4'
import { performMCPOAuthFlow } from '../../services/mcp/auth.js'
import {
  clearMcpAuthCache,
  reconnectMcpServerImpl,
} from '../../services/mcp/client.js'
import {
  buildMcpToolName,
  getMcpPrefix,
} from '../../services/mcp/mcpStringUtils.js'
import type {
  McpHTTPServerConfig,
  McpSSEServerConfig,
  ScopedMcpServerConfig,
} from '../../services/mcp/types.js'
import type { Tool } from '../../Tool.js'
import { errorMessage } from '../../utils/errors.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { logMCPDebug, logMCPError } from '../../utils/log.js'
import type { PermissionDecision } from '../../utils/permissions/PermissionResult.js'

const inputSchema = lazySchema(() => z.object({}))
type InputSchema = ReturnType<typeof inputSchema>

export type McpAuthOutput = {
  status: 'auth_url' | 'unsupported' | 'error'
  message: string
  authUrl?: string
}

function getConfigUrl(config: ScopedMcpServerConfig): string | undefined {
  if ('url' in config) return config.url
  return undefined
}

/**
 * Creates a pseudo-tool for an MCP server that is installed but not
 * authenticated. Surfaced in place of the server's real tools so the model
 * knows the server exists and can start the OAuth flow on the user's behalf.
 *
 * When called, starts performMCPOAuthFlow with skipBrowserOpen and returns
 * the authorization URL. The OAuth callback completes in the background;
 * once it fires, reconnectMcpServerImpl runs and the server's real tools
 * are swapped into appState.mcp.tools via the existing prefix-based
 * replacement (useManageMCPConnections.updateServer wipes anything matching
 * mcp__<server>__*, so this pseudo-tool is removed automatically).
 */
export function createMcpAuthTool(
  serverName: string,

```

---


### `src/tools/MonitorTool/MonitorTool.ts`

**信息:**
- 行数: 1
- 大小: 32 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const MonitorTool = null

```

---


### `src/tools/NotebookEditTool/NotebookEditTool.ts`

**信息:**
- 行数: 490
- 大小: 15271 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { extname, isAbsolute, resolve } from 'path'
import {
  fileHistoryEnabled,
  fileHistoryTrackEdit,
} from 'src/utils/fileHistory.js'
import { z } from 'zod/v4'
import { buildTool, type ToolDef, type ToolUseContext } from '../../Tool.js'
import type { NotebookCell, NotebookContent } from '../../types/notebook.js'
import { getCwd } from '../../utils/cwd.js'
import { isENOENT } from '../../utils/errors.js'
import { getFileModificationTime, writeTextContent } from '../../utils/file.js'
import { readFileSyncWithMetadata } from '../../utils/fileRead.js'
import { safeParseJSON } from '../../utils/json.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { parseCellId } from '../../utils/notebook.js'
import { checkWritePermissionForTool } from '../../utils/permissions/filesystem.js'
import type { PermissionDecision } from '../../utils/permissions/PermissionResult.js'
import { jsonParse, jsonStringify } from '../../utils/slowOperations.js'
import { NOTEBOOK_EDIT_TOOL_NAME } from './constants.js'
import { DESCRIPTION, PROMPT } from './prompt.js'
import {
  getToolUseSummary,
  renderToolResultMessage,
  renderToolUseErrorMessage,
  renderToolUseMessage,
  renderToolUseRejectedMessage,
} from './UI.js'

export const inputSchema = lazySchema(() =>
  z.strictObject({
    notebook_path: z
      .string()
      .describe(
        'The absolute path to the Jupyter notebook file to edit (must be absolute, not relative)',
      ),
    cell_id: z
      .string()
      .optional()
      .describe(
        'The ID of the cell to edit. When inserting a new cell, the new cell will be inserted after the cell with this ID, or at the beginning if not specified.',
      ),
    new_source: z.string().describe('The new source for the cell'),
    cell_type: z
      .enum(['code', 'markdown'])
      .optional()
      .describe(
        'The type of the cell (code or markdown). If not specified, it defaults to the current cell type. If using edit_mode=insert, this is required.',
      ),
    edit_mode: z

```

---


### `src/tools/NotebookEditTool/UI.tsx`

**信息:**
- 行数: 93
- 大小: 13540 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import type { Message, ProgressMessage } from 'src/types/message.js';
import { extractTag } from 'src/utils/messages.js';
import type { ThemeName } from 'src/utils/theme.js';
import type { z } from 'zod/v4';
import { FallbackToolUseErrorMessage } from '../../components/FallbackToolUseErrorMessage.js';
import { FilePathLink } from '../../components/FilePathLink.js';
import { HighlightedCode } from '../../components/HighlightedCode.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { NotebookEditToolUseRejectedMessage } from '../../components/NotebookEditToolUseRejectedMessage.js';
import { Box, Text } from '../../ink.js';
import type { Tools } from '../../Tool.js';
import { getDisplayPath } from '../../utils/file.js';
import type { inputSchema, Output } from './NotebookEditTool.js';
export function getToolUseSummary(input: Partial<z.infer<ReturnType<typeof inputSchema>>> | undefined): string | null {
  if (!input?.notebook_path) {
    return null;
  }
  return getDisplayPath(input.notebook_path);
}
export function renderToolUseMessage({
  notebook_path,
  cell_id,
  new_source,
  cell_type,
  edit_mode
}: Partial<z.infer<ReturnType<typeof inputSchema>>>, {
  verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  if (!notebook_path || !new_source || !cell_type) {
    return null;
  }
  const displayPath = verbose ? notebook_path : getDisplayPath(notebook_path);
  if (verbose) {
    return <>
        <FilePathLink filePath={notebook_path}>{displayPath}</FilePathLink>
        {`@${cell_id}, content: ${new_source.slice(0, 30)}…, cell_type: ${cell_type}, edit_mode: ${edit_mode ?? 'replace'}`}
      </>;
  }
  return <>
      <FilePathLink filePath={notebook_path}>{displayPath}</FilePathLink>
      {`@${cell_id}`}
    </>;
}
export function renderToolUseRejectedMessage(input: z.infer<ReturnType<typeof inputSchema>>, {
  verbose
}: {

```

---


### `src/tools/NotebookEditTool/constants.ts`

**信息:**
- 行数: 2
- 大小: 104 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// In its own file to avoid circular dependencies
export const NOTEBOOK_EDIT_TOOL_NAME = 'NotebookEdit'

```

---


### `src/tools/NotebookEditTool/prompt.ts`

**信息:**
- 行数: 3
- 大小: 632 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const DESCRIPTION =
  'Replace the contents of a specific cell in a Jupyter notebook.'
export const PROMPT = `Completely replaces the contents of a specific cell in a Jupyter notebook (.ipynb file) with new source. Jupyter notebooks are interactive documents that combine code, text, and visualizations, commonly used for data analysis and scientific computing. The notebook_path parameter must be an absolute path, not a relative path. The cell_number is 0-indexed. Use edit_mode=insert to add a new cell at the index specified by cell_number. Use edit_mode=delete to delete the cell at the index specified by cell_number.`

```

---


### `src/tools/OverflowTestTool/OverflowTestTool.ts`

**信息:**
- 行数: 1
- 大小: 37 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const OverflowTestTool = null

```

---


### `src/tools/PowerShellTool/PowerShellTool.tsx`

**信息:**
- 行数: 1001
- 大小: 144624 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle';
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import { copyFile, stat as fsStat, truncate as fsTruncate, link } from 'fs/promises';
import * as React from 'react';
import type { CanUseToolFn } from 'src/hooks/useCanUseTool.js';
import type { AppState } from 'src/state/AppState.js';
import { z } from 'zod/v4';
import { getKairosActive } from '../../bootstrap/state.js';
import { TOOL_SUMMARY_MAX_LENGTH } from '../../constants/toolLimits.js';
import { type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS, logEvent } from '../../services/analytics/index.js';
import type { SetToolJSXFn, Tool, ToolCallProgress, ValidationResult } from '../../Tool.js';
import { buildTool, type ToolDef } from '../../Tool.js';
import { backgroundExistingForegroundTask, markTaskNotified, registerForeground, spawnShellTask, unregisterForeground } from '../../tasks/LocalShellTask/LocalShellTask.js';
import type { AgentId } from '../../types/ids.js';
import type { AssistantMessage } from '../../types/message.js';
import { extractClaudeCodeHints } from '../../utils/claudeCodeHints.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import { errorMessage as getErrorMessage, ShellError } from '../../utils/errors.js';
import { truncate } from '../../utils/format.js';
import { lazySchema } from '../../utils/lazySchema.js';
import { logError } from '../../utils/log.js';
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js';
import { getPlatform } from '../../utils/platform.js';
import { maybeRecordPluginHint } from '../../utils/plugins/hintRecommendation.js';
import { exec } from '../../utils/Shell.js';
import type { ExecResult } from '../../utils/ShellCommand.js';
import { SandboxManager } from '../../utils/sandbox/sandbox-adapter.js';
import { semanticBoolean } from '../../utils/semanticBoolean.js';
import { semanticNumber } from '../../utils/semanticNumber.js';
import { getCachedPowerShellPath } from '../../utils/shell/powershellDetection.js';
import { EndTruncatingAccumulator } from '../../utils/stringUtils.js';
import { getTaskOutputPath } from '../../utils/task/diskOutput.js';
import { TaskOutput } from '../../utils/task/TaskOutput.js';
import { isOutputLineTruncated } from '../../utils/terminal.js';
import { buildLargeToolResultMessage, ensureToolResultsDir, generatePreview, getToolResultPath, PREVIEW_SIZE_BYTES } from '../../utils/toolResultStorage.js';
import { shouldUseSandbox } from '../BashTool/shouldUseSandbox.js';
import { BackgroundHint } from '../BashTool/UI.js';
import { buildImageToolResult, isImageOutput, resetCwdIfOutsideProject, resizeShellImageOutput, stdErrAppendShellResetMessage, stripEmptyLines } from '../BashTool/utils.js';
import { trackGitOperations } from '../shared/gitOperationTracking.js';
import { interpretCommandResult } from './commandSemantics.js';
import { powershellToolHasPermission } from './powershellPermissions.js';
import { getDefaultTimeoutMs, getMaxTimeoutMs, getPrompt } from './prompt.js';
import { hasSyncSecurityConcerns, isReadOnlyCommand, resolveToCanonical } from './readOnlyValidation.js';
import { POWERSHELL_TOOL_NAME } from './toolName.js';
import { renderToolResultMessage, renderToolUseErrorMessage, renderToolUseMessage, renderToolUseProgressMessage, renderToolUseQueuedMessage } from './UI.js';

// Never use os.EOL for terminal output — \r\n on Windows breaks Ink rendering
const EOL = '\n';

/**

```

---


### `src/tools/PowerShellTool/UI.tsx`

**信息:**
- 行数: 131
- 大小: 19768 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import { KeyboardShortcutHint } from '../../components/design-system/KeyboardShortcutHint.js';
import { FallbackToolUseErrorMessage } from '../../components/FallbackToolUseErrorMessage.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { OutputLine } from '../../components/shell/OutputLine.js';
import { ShellProgressMessage } from '../../components/shell/ShellProgressMessage.js';
import { ShellTimeDisplay } from '../../components/shell/ShellTimeDisplay.js';
import { Box, Text } from '../../ink.js';
import type { Tool } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import type { PowerShellProgress } from '../../types/tools.js';
import type { ThemeName } from '../../utils/theme.js';
import type { Out, PowerShellToolInput } from './PowerShellTool.js';

// Constants for command display
const MAX_COMMAND_DISPLAY_LINES = 2;
const MAX_COMMAND_DISPLAY_CHARS = 160;
export function renderToolUseMessage(input: Partial<PowerShellToolInput>, {
  verbose,
  theme: _theme
}: {
  verbose: boolean;
  theme: ThemeName;
}): React.ReactNode {
  const {
    command
  } = input;
  if (!command) {
    return null;
  }
  const displayCommand = command;
  if (!verbose) {
    const lines = displayCommand.split('\n');
    const needsLineTruncation = lines.length > MAX_COMMAND_DISPLAY_LINES;
    const needsCharTruncation = displayCommand.length > MAX_COMMAND_DISPLAY_CHARS;
    if (needsLineTruncation || needsCharTruncation) {
      let truncated = displayCommand;
      if (needsLineTruncation) {
        truncated = lines.slice(0, MAX_COMMAND_DISPLAY_LINES).join('\n');
      }
      if (truncated.length > MAX_COMMAND_DISPLAY_CHARS) {
        truncated = truncated.slice(0, MAX_COMMAND_DISPLAY_CHARS);
      }
      return <Text>{truncated.trim()}…</Text>;
    }
  }
  return displayCommand;
}
export function renderToolUseProgressMessage(progressMessagesForMessage: ProgressMessage<PowerShellProgress>[], {

```

---


### `src/tools/PowerShellTool/clmTypes.ts`

**信息:**
- 行数: 211
- 大小: 7229 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * PowerShell Constrained Language Mode allowed types.
 *
 * Microsoft's CLM restricts .NET type usage to this allowlist when PS runs
 * under AppLocker/WDAC system lockdown. Any type NOT in this set is considered
 * unsafe for untrusted code execution.
 *
 * We invert this: type literals not in this set → ask. One canonical check
 * replaces enumerating individual dangerous types (named pipes, reflection,
 * process spawning, P/Invoke marshaling, etc.). Microsoft maintains the list.
 *
 * Source: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_language_modes
 *
 * Normalization: entries stored lowercase, short AND full names where both
 * exist (PS resolves type accelerators like [int] → System.Int32 at runtime;
 * we match against what the AST emits, which is the literal text).
 */
export const CLM_ALLOWED_TYPES: ReadonlySet<string> = new Set(
  [
    // Type accelerators (short names as they appear in AST TypeName.Name)
    // SECURITY: 'adsi' and 'adsisearcher' REMOVED. Both are Active Directory
    // Service Interface types that perform NETWORK BINDS when cast:
    //   [adsi]'LDAP://evil.com/...' → connects to LDAP server
    //   [adsisearcher]'(objectClass=user)' → binds to AD and queries
    // Microsoft's CLM allows these because it's for Windows admins in trusted
    // domains; we block them since the target isn't validated.
    'alias',
    'allowemptycollection',
    'allowemptystring',
    'allownull',
    'argumentcompleter',
    'argumentcompletions',
    'array',
    'bigint',
    'bool',
    'byte',
    'char',
    'cimclass',
    'cimconverter',
    'ciminstance',
    // 'cimsession' REMOVED — see wmi/adsi comment below
    'cimtype',
    'cmdletbinding',
    'cultureinfo',
    'datetime',
    'decimal',
    'double',
    'dsclocalconfigurationmanager',
    'dscproperty',
    'dscresource',

```

---


### `src/tools/PowerShellTool/commandSemantics.ts`

**信息:**
- 行数: 142
- 大小: 5459 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Command semantics configuration for interpreting exit codes in PowerShell.
 *
 * PowerShell-native cmdlets do NOT need exit-code semantics:
 *   - Select-String (grep equivalent) exits 0 on no-match (returns $null)
 *   - Compare-Object (diff equivalent) exits 0 regardless
 *   - Test-Path exits 0 regardless (returns bool via pipeline)
 * Native cmdlets signal failure via terminating errors ($?), not exit codes.
 *
 * However, EXTERNAL executables invoked from PowerShell DO set $LASTEXITCODE,
 * and many use non-zero codes to convey information rather than failure:
 *   - grep.exe / rg.exe (Git for Windows, scoop, etc.): 1 = no match
 *   - findstr.exe (Windows native): 1 = no match
 *   - robocopy.exe (Windows native): 0-7 = success, 8+ = error (notorious!)
 *
 * Without this module, PowerShellTool throws ShellError on any non-zero exit,
 * so `robocopy` reporting "files copied successfully" (exit 1) shows as an error.
 */

export type CommandSemantic = (
  exitCode: number,
  stdout: string,
  stderr: string,
) => {
  isError: boolean
  message?: string
}

/**
 * Default semantic: treat only 0 as success, everything else as error
 */
const DEFAULT_SEMANTIC: CommandSemantic = (exitCode, _stdout, _stderr) => ({
  isError: exitCode !== 0,
  message:
    exitCode !== 0 ? `Command failed with exit code ${exitCode}` : undefined,
})

/**
 * grep / ripgrep: 0 = matches found, 1 = no matches, 2+ = error
 */
const GREP_SEMANTIC: CommandSemantic = (exitCode, _stdout, _stderr) => ({
  isError: exitCode >= 2,
  message: exitCode === 1 ? 'No matches found' : undefined,
})

/**
 * Command-specific semantics for external executables.
 * Keys are lowercase command names WITHOUT .exe suffix.
 *
 * Deliberately omitted:

```

---


### `src/tools/PowerShellTool/commonParameters.ts`

**信息:**
- 行数: 30
- 大小: 894 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * PowerShell Common Parameters (available on all cmdlets via [CmdletBinding()]).
 * Source: about_CommonParameters (PowerShell docs) + Get-Command output.
 *
 * Shared between pathValidation.ts (merges into per-cmdlet known-param sets)
 * and readOnlyValidation.ts (merges into safeFlags check). Split out to break
 * what would otherwise be an import cycle between those two files.
 *
 * Stored lowercase with leading dash — callers `.toLowerCase()` their input.
 */

export const COMMON_SWITCHES = ['-verbose', '-debug']

export const COMMON_VALUE_PARAMS = [
  '-erroraction',
  '-warningaction',
  '-informationaction',
  '-progressaction',
  '-errorvariable',
  '-warningvariable',
  '-informationvariable',
  '-outvariable',
  '-outbuffer',
  '-pipelinevariable',
]

export const COMMON_PARAMETERS: ReadonlySet<string> = new Set([
  ...COMMON_SWITCHES,
  ...COMMON_VALUE_PARAMS,
])

```

---


### `src/tools/PowerShellTool/destructiveCommandWarning.ts`

**信息:**
- 行数: 109
- 大小: 3402 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Detects potentially destructive PowerShell commands and returns a warning
 * string for display in the permission dialog. This is purely informational
 * -- it doesn't affect permission logic or auto-approval.
 */

type DestructivePattern = {
  pattern: RegExp
  warning: string
}

const DESTRUCTIVE_PATTERNS: DestructivePattern[] = [
  // Remove-Item with -Recurse and/or -Force (and common aliases)
  // Anchored to statement start (^, |, ;, &, newline, {, () so `git rm --force`
  // doesn't match — \b would match `rm` after any word boundary. The `{(`
  // chars catch scriptblock/group bodies: `{ rm -Force ./x }`. The stopper
  // adds only `}` (NOT `)`) — `}` ends a block so flags after it belong to a
  // different statement (`if {rm} else {... -Force}`), but `)` closes a path
  // grouping and flags after it are still this command's flags:
  // `Remove-Item (Join-Path $r "tmp") -Recurse -Force` must still warn.
  {
    pattern:
      /(?:^|[|;&\n({])\s*(Remove-Item|rm|del|rd|rmdir|ri)\b[^|;&\n}]*-Recurse\b[^|;&\n}]*-Force\b/i,
    warning: 'Note: may recursively force-remove files',
  },
  {
    pattern:
      /(?:^|[|;&\n({])\s*(Remove-Item|rm|del|rd|rmdir|ri)\b[^|;&\n}]*-Force\b[^|;&\n}]*-Recurse\b/i,
    warning: 'Note: may recursively force-remove files',
  },
  {
    pattern:
      /(?:^|[|;&\n({])\s*(Remove-Item|rm|del|rd|rmdir|ri)\b[^|;&\n}]*-Recurse\b/i,
    warning: 'Note: may recursively remove files',
  },
  {
    pattern:
      /(?:^|[|;&\n({])\s*(Remove-Item|rm|del|rd|rmdir|ri)\b[^|;&\n}]*-Force\b/i,
    warning: 'Note: may force-remove files',
  },

  // Clear-Content on broad paths
  {
    pattern: /\bClear-Content\b[^|;&\n]*\*/i,
    warning: 'Note: may clear content of multiple files',
  },

  // Format-Volume and Clear-Disk
  {
    pattern: /\bFormat-Volume\b/i,

```

---


### `src/tools/PowerShellTool/gitSafety.ts`

**信息:**
- 行数: 176
- 大小: 7695 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Git can be weaponized for sandbox escape via two vectors:
 * 1. Bare-repo attack: if cwd contains HEAD + objects/ + refs/ but no valid
 *    .git/HEAD, Git treats cwd as a bare repository and runs hooks from cwd.
 * 2. Git-internal write + git: a compound command creates HEAD/objects/refs/
 *    hooks/ then runs git — the git subcommand executes the freshly-created
 *    malicious hooks.
 */

import { basename, posix, resolve, sep } from 'path'
import { getCwd } from '../../utils/cwd.js'
import { PS_TOKENIZER_DASH_CHARS } from '../../utils/powershell/parser.js'

/**
 * If a normalized path starts with `../<cwd-basename>/`, it re-enters cwd
 * via the parent — resolve it to the cwd-relative form. posix.normalize
 * preserves leading `..` (no cwd context), so `../project/hooks` with
 * cwd=/x/project stays `../project/hooks` and misses the `hooks/` prefix
 * match even though it resolves to the same directory at runtime.
 * Check/use divergence: validator sees `../project/hooks`, PowerShell
 * resolves against cwd to `hooks`.
 */
function resolveCwdReentry(normalized: string): string {
  if (!normalized.startsWith('../')) return normalized
  const cwdBase = basename(getCwd()).toLowerCase()
  if (!cwdBase) return normalized
  // Iteratively strip `../<cwd-basename>/` pairs (handles `../../p/p/hooks`
  // when cwd has repeated basename segments is unlikely, but one-level is
  // the common attack).
  const prefix = '../' + cwdBase + '/'
  let s = normalized
  while (s.startsWith(prefix)) {
    s = s.slice(prefix.length)
  }
  // Also handle exact `../<cwd-basename>` (no trailing slash)
  if (s === '../' + cwdBase) return '.'
  return s
}

/**
 * Normalize PS arg text → canonical path for git-internal matching.
 * Order matters: structural strips first (colon-bound param, quotes,
 * backtick escapes, provider prefix, drive-relative prefix), then NTFS
 * per-component trailing-strip (spaces always; dots only if not `./..`
 * after space-strip), then posix.normalize (resolves `..`, `.`, `//`),
 * then case-fold.
 */
function normalizeGitPathArg(arg: string): string {
  let s = arg
  // Normalize parameter prefixes: dash chars (–, —, ―) and forward-slash

```

---


### `src/tools/PowerShellTool/modeValidation.ts`

**信息:**
- 行数: 404
- 大小: 17399 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * PowerShell permission mode validation.
 *
 * Checks if commands should be auto-allowed based on the current permission mode.
 * In acceptEdits mode, filesystem-modifying PowerShell cmdlets are auto-allowed.
 * Follows the same patterns as BashTool/modeValidation.ts.
 */

import type { ToolPermissionContext } from '../../Tool.js'
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js'
import type { ParsedPowerShellCommand } from '../../utils/powershell/parser.js'
import {
  deriveSecurityFlags,
  getPipelineSegments,
  PS_TOKENIZER_DASH_CHARS,
} from '../../utils/powershell/parser.js'
import {
  argLeaksValue,
  isAllowlistedPipelineTail,
  isCwdChangingCmdlet,
  isSafeOutputCommand,
  resolveToCanonical,
} from './readOnlyValidation.js'

/**
 * Filesystem-modifying cmdlets that are auto-allowed in acceptEdits mode.
 * Stored as canonical (lowercase) cmdlet names.
 *
 * Tier 3 cmdlets with complex parameter binding removed — they fall through to
 * 'ask'. Only simple write cmdlets (first positional = -Path) are auto-allowed
 * here, and they get path validation via CMDLET_PATH_CONFIG in pathValidation.ts.
 */
const ACCEPT_EDITS_ALLOWED_CMDLETS = new Set([
  'set-content',
  'add-content',
  'remove-item',
  'clear-content',
])

function isAcceptEditsAllowedCmdlet(name: string): boolean {
  // resolveToCanonical handles aliases via COMMON_ALIASES, so e.g. 'rm' → 'remove-item',
  // 'ac' → 'add-content'. Any alias that resolves to an allowed cmdlet is automatically
  // allowed. Tier 3 cmdlets (new-item, copy-item, move-item, etc.) and their aliases
  // (mkdir, ni, cp, mv, etc.) resolve to cmdlets NOT in the set and fall through to 'ask'.
  const canonical = resolveToCanonical(name)
  return ACCEPT_EDITS_ALLOWED_CMDLETS.has(canonical)
}

/**
 * New-Item -ItemType values that create filesystem links (reparse points or

```

---


### `src/tools/PowerShellTool/pathValidation.ts`

**信息:**
- 行数: 2049
- 大小: 73059 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * PowerShell-specific path validation for command arguments.
 *
 * Extracts file paths from PowerShell commands using the AST parser
 * and validates they stay within allowed project directories.
 * Follows the same patterns as BashTool/pathValidation.ts.
 */

import { homedir } from 'os'
import { isAbsolute, resolve } from 'path'
import type { ToolPermissionContext } from '../../Tool.js'
import type { PermissionRule } from '../../types/permissions.js'
import { getCwd } from '../../utils/cwd.js'
import {
  getFsImplementation,
  safeResolvePath,
} from '../../utils/fsOperations.js'
import { containsPathTraversal, getDirectoryForPath } from '../../utils/path.js'
import {
  allWorkingDirectories,
  checkEditableInternalPath,
  checkPathSafetyForAutoEdit,
  checkReadableInternalPath,
  matchingRuleForInput,
  pathInAllowedWorkingPath,
} from '../../utils/permissions/filesystem.js'
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js'
import { createReadRuleSuggestion } from '../../utils/permissions/PermissionUpdate.js'
import type { PermissionUpdate } from '../../utils/permissions/PermissionUpdateSchema.js'
import {
  isDangerousRemovalPath,
  isPathInSandboxWriteAllowlist,
} from '../../utils/permissions/pathValidation.js'
import { getPlatform } from '../../utils/platform.js'
import type {
  ParsedCommandElement,
  ParsedPowerShellCommand,
} from '../../utils/powershell/parser.js'
import {
  isNullRedirectionTarget,
  isPowerShellParameter,
} from '../../utils/powershell/parser.js'
import { COMMON_SWITCHES, COMMON_VALUE_PARAMS } from './commonParameters.js'
import { resolveToCanonical } from './readOnlyValidation.js'

const MAX_DIRS_TO_LIST = 5
// PowerShell wildcards are only * ? [ ] — braces are LITERAL characters
// (no brace expansion). Including {} mis-routed paths like `./{x}/passwd`
// through glob-base truncation instead of full-path symlink resolution.
const GLOB_PATTERN_REGEX = /[*?[\]]/

```

---


### `src/tools/PowerShellTool/powershellPermissions.ts`

**信息:**
- 行数: 1648
- 大小: 67606 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * PowerShell-specific permission checking, adapted from bashPermissions.ts
 * for case-insensitive cmdlet matching.
 */

import { resolve } from 'path'
import type { ToolPermissionContext, ToolUseContext } from '../../Tool.js'
import type {
  PermissionDecisionReason,
  PermissionResult,
} from '../../types/permissions.js'
import { getCwd } from '../../utils/cwd.js'
import { isCurrentDirectoryBareGitRepo } from '../../utils/git.js'
import type { PermissionRule } from '../../utils/permissions/PermissionRule.js'
import type { PermissionUpdate } from '../../utils/permissions/PermissionUpdateSchema.js'
import {
  createPermissionRequestMessage,
  getRuleByContentsForToolName,
} from '../../utils/permissions/permissions.js'
import {
  matchWildcardPattern,
  parsePermissionRule,
  type ShellPermissionRule,
  suggestionForExactCommand as sharedSuggestionForExactCommand,
} from '../../utils/permissions/shellRuleMatching.js'
import {
  classifyCommandName,
  deriveSecurityFlags,
  getAllCommandNames,
  getFileRedirections,
  type ParsedCommandElement,
  type ParsedPowerShellCommand,
  PS_TOKENIZER_DASH_CHARS,
  parsePowerShellCommand,
  stripModulePrefix,
} from '../../utils/powershell/parser.js'
import { containsVulnerableUncPath } from '../../utils/shell/readOnlyCommandValidation.js'
import { isDotGitPathPS, isGitInternalPathPS } from './gitSafety.js'
import {
  checkPermissionMode,
  isSymlinkCreatingCommand,
} from './modeValidation.js'
import {
  checkPathConstraints,
  dangerousRemovalDeny,
  isDangerousRemovalRawPath,
} from './pathValidation.js'
import { powershellCommandIsSafe } from './powershellSecurity.js'
import {
  argLeaksValue,

```

---


### `src/tools/PowerShellTool/powershellSecurity.ts`

**信息:**
- 行数: 1090
- 大小: 37651 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * PowerShell-specific security analysis for command validation.
 *
 * Detects dangerous patterns: code injection, download cradles, privilege
 * escalation, dynamic command names, COM objects, etc.
 *
 * All checks are AST-based. If parsing failed (valid=false), none of the
 * individual checks match and powershellCommandIsSafe returns 'ask'.
 */

import {
  DANGEROUS_SCRIPT_BLOCK_CMDLETS,
  FILEPATH_EXECUTION_CMDLETS,
  MODULE_LOADING_CMDLETS,
} from '../../utils/powershell/dangerousCmdlets.js'
import type {
  ParsedCommandElement,
  ParsedPowerShellCommand,
} from '../../utils/powershell/parser.js'
import {
  COMMON_ALIASES,
  commandHasArgAbbreviation,
  deriveSecurityFlags,
  getAllCommands,
  getVariablesByScope,
  hasCommandNamed,
} from '../../utils/powershell/parser.js'
import { isClmAllowedType } from './clmTypes.js'

type PowerShellSecurityResult = {
  behavior: 'passthrough' | 'ask' | 'allow'
  message?: string
}

const POWERSHELL_EXECUTABLES = new Set([
  'pwsh',
  'pwsh.exe',
  'powershell',
  'powershell.exe',
])

/**
 * Extracts the base executable name from a command, handling full paths
 * like /usr/bin/pwsh, C:\Windows\...\powershell.exe, or .\pwsh.
 */
function isPowerShellExecutable(name: string): boolean {
  const lower = name.toLowerCase()
  if (POWERSHELL_EXECUTABLES.has(lower)) {
    return true
  }

```

---


### `src/tools/PowerShellTool/prompt.ts`

**信息:**
- 行数: 145
- 大小: 9826 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { isEnvTruthy } from '../../utils/envUtils.js'
import { getMaxOutputLength } from '../../utils/shell/outputLimits.js'
import {
  getPowerShellEdition,
  type PowerShellEdition,
} from '../../utils/shell/powershellDetection.js'
import {
  getDefaultBashTimeoutMs,
  getMaxBashTimeoutMs,
} from '../../utils/timeouts.js'
import { FILE_EDIT_TOOL_NAME } from '../FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from '../FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from '../FileWriteTool/prompt.js'
import { GLOB_TOOL_NAME } from '../GlobTool/prompt.js'
import { GREP_TOOL_NAME } from '../GrepTool/prompt.js'
import { POWERSHELL_TOOL_NAME } from './toolName.js'

export function getDefaultTimeoutMs(): number {
  return getDefaultBashTimeoutMs()
}

export function getMaxTimeoutMs(): number {
  return getMaxBashTimeoutMs()
}

function getBackgroundUsageNote(): string | null {
  if (isEnvTruthy(process.env.CLAUDE_CODE_DISABLE_BACKGROUND_TASKS)) {
    return null
  }
  return `  - You can use the \`run_in_background\` parameter to run the command in the background. Only use this if you don't need the result immediately and are OK being notified when the command completes later. You do not need to check the output right away - you'll be notified when it finishes.`
}

function getSleepGuidance(): string | null {
  if (isEnvTruthy(process.env.CLAUDE_CODE_DISABLE_BACKGROUND_TASKS)) {
    return null
  }
  return `  - Avoid unnecessary \`Start-Sleep\` commands:
    - Do not sleep between commands that can run immediately — just run them.
    - If your command is long running and you would like to be notified when it finishes — simply run your command using \`run_in_background\`. There is no need to sleep in this case.
    - Do not retry failing commands in a sleep loop — diagnose the root cause or consider an alternative approach.
    - If waiting for a background task you started with \`run_in_background\`, you will be notified when it completes — do not poll.
    - If you must poll an external process, use a check command rather than sleeping first.
    - If you must sleep, keep the duration short (1-5 seconds) to avoid blocking the user.`
}

/**
 * Version-specific syntax guidance. The model's training data covers both
 * editions but it can't tell which one it's targeting, so it either emits
 * pwsh-7 syntax on 5.1 (parser error → exit 1) or needlessly avoids && on 7.
 */

```

---


### `src/tools/PowerShellTool/readOnlyValidation.ts`

**信息:**
- 行数: 1823
- 大小: 67327 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * PowerShell read-only command validation.
 *
 * Cmdlets are case-insensitive; all matching is done in lowercase.
 */

import type {
  ParsedCommandElement,
  ParsedPowerShellCommand,
} from '../../utils/powershell/parser.js'

type ParsedStatement = ParsedPowerShellCommand['statements'][number]

import { getPlatform } from '../../utils/platform.js'
import {
  COMMON_ALIASES,
  deriveSecurityFlags,
  getPipelineSegments,
  isNullRedirectionTarget,
  isPowerShellParameter,
} from '../../utils/powershell/parser.js'
import type { ExternalCommandConfig } from '../../utils/shell/readOnlyCommandValidation.js'
import {
  DOCKER_READ_ONLY_COMMANDS,
  EXTERNAL_READONLY_COMMANDS,
  GH_READ_ONLY_COMMANDS,
  GIT_READ_ONLY_COMMANDS,
  validateFlags,
} from '../../utils/shell/readOnlyCommandValidation.js'
import { COMMON_PARAMETERS } from './commonParameters.js'

const DOTNET_READ_ONLY_FLAGS = new Set([
  '--version',
  '--info',
  '--list-runtimes',
  '--list-sdks',
])

type CommandConfig = {
  /** Safe subcommands or flags for this command */
  safeFlags?: string[]
  /**
   * When true, all flags are allowed regardless of safeFlags.
   * Use for commands whose entire flag surface is read-only (e.g., hostname).
   * Without this, an empty/missing safeFlags rejects all flags (positional
   * args only).
   */
  allowAllFlags?: boolean
  /** Regex constraint on the original command */
  regex?: RegExp

```

---


### `src/tools/PowerShellTool/toolName.ts`

**信息:**
- 行数: 2
- 大小: 110 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Here to break circular dependency from prompt.ts
export const POWERSHELL_TOOL_NAME = 'PowerShell' as const

```

---


### `src/tools/REPLTool/constants.ts`

**信息:**
- 行数: 46
- 大小: 1799 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { isEnvDefinedFalsy, isEnvTruthy } from '../../utils/envUtils.js'
import { AGENT_TOOL_NAME } from '../AgentTool/constants.js'
import { BASH_TOOL_NAME } from '../BashTool/toolName.js'
import { FILE_EDIT_TOOL_NAME } from '../FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from '../FileReadTool/prompt.js'
import { FILE_WRITE_TOOL_NAME } from '../FileWriteTool/prompt.js'
import { GLOB_TOOL_NAME } from '../GlobTool/prompt.js'
import { GREP_TOOL_NAME } from '../GrepTool/prompt.js'
import { NOTEBOOK_EDIT_TOOL_NAME } from '../NotebookEditTool/constants.js'

export const REPL_TOOL_NAME = 'REPL'

/**
 * REPL mode is default-on for ants in the interactive CLI (opt out with
 * CLAUDE_CODE_REPL=0). The legacy CLAUDE_REPL_MODE=1 also forces it on.
 *
 * SDK entrypoints (sdk-ts, sdk-py, sdk-cli) are NOT defaulted on — SDK
 * consumers script direct tool calls (Bash, Read, etc.) and REPL mode
 * hides those tools. USER_TYPE is a build-time --define, so the ant-native
 * binary would otherwise force REPL mode on every SDK subprocess regardless
 * of the env the caller passes.
 */
export function isReplModeEnabled(): boolean {
  if (isEnvDefinedFalsy(process.env.CLAUDE_CODE_REPL)) return false
  if (isEnvTruthy(process.env.CLAUDE_REPL_MODE)) return true
  return (
    process.env.USER_TYPE === 'ant' &&
    process.env.CLAUDE_CODE_ENTRYPOINT === 'cli'
  )
}

/**
 * Tools that are only accessible via REPL when REPL mode is enabled.
 * When REPL mode is on, these tools are hidden from Claude's direct use,
 * forcing Claude to use REPL for batch operations.
 */
export const REPL_ONLY_TOOLS = new Set([
  FILE_READ_TOOL_NAME,
  FILE_WRITE_TOOL_NAME,
  FILE_EDIT_TOOL_NAME,
  GLOB_TOOL_NAME,
  GREP_TOOL_NAME,
  BASH_TOOL_NAME,
  NOTEBOOK_EDIT_TOOL_NAME,
  AGENT_TOOL_NAME,
])

```

---


### `src/tools/REPLTool/primitiveTools.ts`

**信息:**
- 行数: 39
- 大小: 1532 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Tool } from '../../Tool.js'
import { AgentTool } from '../AgentTool/AgentTool.js'
import { BashTool } from '../BashTool/BashTool.js'
import { FileEditTool } from '../FileEditTool/FileEditTool.js'
import { FileReadTool } from '../FileReadTool/FileReadTool.js'
import { FileWriteTool } from '../FileWriteTool/FileWriteTool.js'
import { GlobTool } from '../GlobTool/GlobTool.js'
import { GrepTool } from '../GrepTool/GrepTool.js'
import { NotebookEditTool } from '../NotebookEditTool/NotebookEditTool.js'

let _primitiveTools: readonly Tool[] | undefined

/**
 * Primitive tools hidden from direct model use when REPL mode is on
 * (REPL_ONLY_TOOLS) but still accessible inside the REPL VM context.
 * Exported so display-side code (collapseReadSearch, renderers) can
 * classify/render virtual messages for these tools even when they're
 * absent from the filtered execution tools list.
 *
 * Lazy getter — the import chain collapseReadSearch.ts → primitiveTools.ts
 * → FileReadTool.tsx → ... loops back through the tool registry, so a
 * top-level const hits "Cannot access before initialization". Deferring
 * to call time avoids the TDZ.
 *
 * Referenced directly rather than via getAllBaseTools() because that
 * excludes Glob/Grep when hasEmbeddedSearchTools() is true.
 */
export function getReplPrimitiveTools(): readonly Tool[] {
  return (_primitiveTools ??= [
    FileReadTool,
    FileWriteTool,
    FileEditTool,
    GlobTool,
    GrepTool,
    BashTool,
    NotebookEditTool,
    AgentTool,
  ])
}

```

---


### `src/tools/ReadMcpResourceTool/ReadMcpResourceTool.ts`

**信息:**
- 行数: 158
- 大小: 4654 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  type ReadResourceResult,
  ReadResourceResultSchema,
} from '@modelcontextprotocol/sdk/types.js'
import { z } from 'zod/v4'
import { ensureConnectedClient } from '../../services/mcp/client.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { lazySchema } from '../../utils/lazySchema.js'
import {
  getBinaryBlobSavedMessage,
  persistBinaryContent,
} from '../../utils/mcpOutputStorage.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { isOutputLineTruncated } from '../../utils/terminal.js'
import { DESCRIPTION, PROMPT } from './prompt.js'
import {
  renderToolResultMessage,
  renderToolUseMessage,
  userFacingName,
} from './UI.js'

export const inputSchema = lazySchema(() =>
  z.object({
    server: z.string().describe('The MCP server name'),
    uri: z.string().describe('The resource URI to read'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

export const outputSchema = lazySchema(() =>
  z.object({
    contents: z.array(
      z.object({
        uri: z.string().describe('Resource URI'),
        mimeType: z.string().optional().describe('MIME type of the content'),
        text: z.string().optional().describe('Text content of the resource'),
        blobSavedTo: z
          .string()
          .optional()
          .describe('Path where binary blob content was saved'),
      }),
    ),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>

export type Output = z.infer<OutputSchema>

export const ReadMcpResourceTool = buildTool({
  isConcurrencySafe() {

```

---


### `src/tools/ReadMcpResourceTool/UI.tsx`

**信息:**
- 行数: 37
- 大小: 6109 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import * as React from 'react';
import type { z } from 'zod/v4';
import { MessageResponse } from '../../components/MessageResponse.js';
import { OutputLine } from '../../components/shell/OutputLine.js';
import { Box, Text } from '../../ink.js';
import type { ToolProgressData } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import { jsonStringify } from '../../utils/slowOperations.js';
import type { inputSchema, Output } from './ReadMcpResourceTool.js';
export function renderToolUseMessage(input: Partial<z.infer<ReturnType<typeof inputSchema>>>): React.ReactNode {
  if (!input.uri || !input.server) {
    return null;
  }
  return `Read resource "${input.uri}" from server "${input.server}"`;
}
export function userFacingName(): string {
  return 'readMcpResource';
}
export function renderToolResultMessage(output: Output, _progressMessagesForMessage: ProgressMessage<ToolProgressData>[], {
  verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  if (!output || !output.contents || output.contents.length === 0) {
    return <Box justifyContent="space-between" overflowX="hidden" width="100%">
        <MessageResponse height={1}>
          <Text dimColor>(No content)</Text>
        </MessageResponse>
      </Box>;
  }

  // Format as JSON for better readability
  // eslint-disable-next-line no-restricted-syntax -- human-facing UI, not tool_result
  const formattedOutput = jsonStringify(output, null, 2);
  return <OutputLine content={formattedOutput} verbose={verbose} />;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsInoiLCJNZXNzYWdlUmVzcG9uc2UiLCJPdXRwdXRMaW5lIiwiQm94IiwiVGV4dCIsIlRvb2xQcm9ncmVzc0RhdGEiLCJQcm9ncmVzc01lc3NhZ2UiLCJqc29uU3RyaW5naWZ5IiwiaW5wdXRTY2hlbWEiLCJPdXRwdXQiLCJyZW5kZXJUb29sVXNlTWVzc2FnZSIsImlucHV0IiwiUGFydGlhbCIsImluZmVyIiwiUmV0dXJuVHlwZSIsIlJlYWN0Tm9kZSIsInVyaSIsInNlcnZlciIsInVzZXJGYWNpbmdOYW1lIiwicmVuZGVyVG9vbFJlc3VsdE1lc3NhZ2UiLCJvdXRwdXQiLCJfcHJvZ3Jlc3NNZXNzYWdlc0Zvck1lc3NhZ2UiLCJ2ZXJib3NlIiwiY29udGVudHMiLCJsZW5ndGgiLCJmb3JtYXR0ZWRPdXRwdXQiXSwic291cmNlcyI6WyJVSS50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgdHlwZSB7IHogfSBmcm9tICd6b2QvdjQnXG5pbXBvcnQgeyBNZXNzYWdlUmVzcG9uc2UgfSBmcm9tICcuLi8uLi9jb21wb25lbnRzL01lc3NhZ2VSZXNwb25zZS5qcydcbmltcG9ydCB7IE91dHB1dExpbmUgfSBmcm9tICcuLi8uLi9jb21wb25lbnRzL3NoZWxsL091dHB1dExpbmUuanMnXG5pbXBvcnQgeyBCb3gsIFRleHQgfSBmcm9tICcuLi8uLi9pbmsuanMnXG5pbXBvcnQgdHlwZSB7IFRvb2xQcm9ncmVzc0RhdGEgfSBmcm9tICcuLi8uLi9Ub29sLmpzJ1xuaW1wb3J0IHR5cGUgeyBQcm9ncmVzc01lc3NhZ2UgfSBmcm9tICcuLi8uLi90eXBlcy9tZXNzYWdlLmpzJ1xuaW1wb3J0IHsganNvblN0cmluZ2lmeSB9IGZyb20gJy4uLy4uL3V0aWxzL3Nsb3dPcGVyYXRpb25zLmpzJ1xuaW1wb3J0IHR5cGUgeyBpbnB1dFNjaGVtYSwgT3V0cHV0IH0gZnJvbSAnLi9SZWFkTWNwUmVzb3VyY2VUb29sLmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gcmVuZGVyVG9vbFVzZU1lc3NhZ2UoXG4gIGlucHV0OiBQYXJ0aWFsPHouaW5mZXI8UmV0dXJuVHlwZTx0eXBlb2YgaW5wdXRTY2hlbWE+Pj4sXG4pOiBSZWFjdC5SZWFjdE5vZGUge1xuICBpZiAoIWlucHV0LnVyaSB8fCAhaW5wdXQuc2VydmVyKSB7XG4gICAgcmV0dXJuIG51bGxcbiAgfVxuICByZXR1cm4gYFJlYWQgcmVzb3VyY2UgXCIke2lucHV0LnVyaX1cIiBmcm9tIHNlcnZlciBcIiR7aW5wdXQuc2VydmVyfVwiYFxufVxuXG5leHBvcnQgZnVuY3Rpb24gdXNlckZhY2luZ05hbWUoKTogc3RyaW5nIHtcbiAgcmV0dXJuICdyZWFkTWNwUmVzb3VyY2UnXG59XG5cbmV4cG9ydCBmdW5jdGlvbiByZW5kZXJUb29sUmVzdWx0TWVzc2FnZShcbiAgb3V0cHV0OiBPdXRwdXQsXG4gIF9wcm9ncmVzc01lc3NhZ2VzRm9yTWVzc2FnZTogUHJvZ3Jlc3NNZXNzYWdlPFRvb2xQcm9ncmVzc0RhdGE+W10sXG4gIHsgdmVyYm9zZSB9OiB7IHZlcmJvc2U6IGJvb2xlYW4gfSxcbik6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIGlmICghb3V0cHV0IHx8ICFvdXRwdXQuY29udGVudHMgfHwgb3V0cHV0LmNvbnRlbnRzLmxlbmd0aCA9PT0gMCkge1xuICAgIHJldHVybiAoXG4gICAgICA8Qm94IGp1c3RpZnlDb250ZW50PVwic3BhY2UtYmV0d2VlblwiIG92ZXJmbG93WD1cImhpZGRlblwiIHdpZHRoPVwiMTAwJVwiPlxuICAgICAgICA8TWVzc2FnZVJlc3BvbnNlIGhlaWdodD17MX0+XG4gICAgICAgICAgPFRleHQgZGltQ29sb3I+KE5vIGNvbnRlbnQpPC9UZXh0PlxuICAgICAgICA8L01lc3NhZ2VSZXNwb25zZT5cbiAgICAgIDwvQm94PlxuICAgIClcbiAgfVxuXG4gIC8vIEZvcm1hdCBhcyBKU09OIGZvciBiZXR0ZXIgcmVhZGFiaWxpdHlcbiAgLy8gZXNsaW50LWRpc2FibGUtbmV4dC1saW5lIG5vLXJlc3RyaWN0ZWQtc3ludGF4IC0tIGh1bWFuLWZhY2luZyBVSSwgbm90IHRvb2xfcmVzdWx0XG4gIGNvbnN0IGZvcm1hdHRlZE91dHB1dCA9IGpzb25TdHJpbmdpZnkob3V0cHV0LCBudWxsLCAyKVxuXG4gIHJldHVybiA8T3V0cHV0TGluZSBjb250ZW50PXtmb3JtYXR0ZWRPdXRwdXR9IHZlcmJvc2U9e3ZlcmJvc2V9IC8+XG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU8sS0FBS0EsS0FBSyxNQUFNLE9BQU87QUFDOUIsY0FBY0MsQ0FBQyxRQUFRLFFBQVE7QUFDL0IsU0FBU0MsZUFBZSxRQUFRLHFDQUFxQztBQUNyRSxTQUFTQyxVQUFVLFFBQVEsc0NBQXNDO0FBQ2pFLFNBQVNDLEdBQUcsRUFBRUMsSUFBSSxRQUFRLGNBQWM7QUFDeEMsY0FBY0MsZ0JBQWdCLFFBQVEsZUFBZTtBQUNyRCxjQUFjQyxlQUFlLFFBQVEsd0JBQXdCO0FBQzdELFNBQVNDLGFBQWEsUUFBUSwrQkFBK0I7QUFDN0QsY0FBY0MsV0FBVyxFQUFFQyxNQUFNLFFBQVEsMEJBQTBCO0FBRW5FLE9BQU8sU0FBU0Msb0JBQW9CQSxDQUNsQ0MsS0FBSyxFQUFFQyxPQUFPLENBQUNaLENBQUMsQ0FBQ2EsS0FBSyxDQUFDQyxVQUFVLENBQUMsT0FBT04sV0FBVyxDQUFDLENBQUMsQ0FBQyxDQUN4RCxFQUFFVCxLQUFLLENBQUNnQixTQUFTLENBQUM7RUFDakIsSUFBSSxDQUFDSixLQUFLLENBQUNLLEdBQUcsSUFBSSxDQUFDTCxLQUFLLENBQUNNLE1BQU0sRUFBRTtJQUMvQixPQUFPLElBQUk7RUFDYjtFQUNBLE9BQU8sa0JBQWtCTixLQUFLLENBQUNLLEdBQUcsa0JBQWtCTCxLQUFLLENBQUNNLE1BQU0sR0FBRztBQUNyRTtBQUVBLE9BQU8sU0FBU0MsY0FBY0EsQ0FBQSxDQUFFLEVBQUUsTUFBTSxDQUFDO0VBQ3ZDLE9BQU8saUJBQWlCO0FBQzFCO0FBRUEsT0FBTyxTQUFTQyx1QkFBdUJBLENBQ3JDQyxNQUFNLEVBQUVYLE1BQU0sRUFDZFksMkJBQTJCLEVBQUVmLGVBQWUsQ0FBQ0QsZ0JBQWdCLENBQUMsRUFBRSxFQUNoRTtFQUFFaUI7QUFBOEIsQ0FBckIsRUFBRTtFQUFFQSxPQUFPLEVBQUUsT0FBTztBQUFDLENBQUMsQ0FDbEMsRUFBRXZCLEtBQUssQ0FBQ2dCLFNBQVMsQ0FBQztFQUNqQixJQUFJLENBQUNLLE1BQU0sSUFBSSxDQUFDQSxNQUFNLENBQUNHLFFBQVEsSUFBSUgsTUFBTSxDQUFDRyxRQUFRLENBQUNDLE1BQU0sS0FBSyxDQUFDLEVBQUU7SUFDL0QsT0FDRSxDQUFDLEdBQUcsQ0FBQyxjQUFjLENBQUMsZUFBZSxDQUFDLFNBQVMsQ0FBQyxRQUFRLENBQUMsS0FBSyxDQUFDLE1BQU07QUFDekUsUUFBUSxDQUFDLGVBQWUsQ0FBQyxNQUFNLENBQUMsQ0FBQyxDQUFDLENBQUM7QUFDbkMsVUFBVSxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsWUFBWSxFQUFFLElBQUk7QUFDM0MsUUFBUSxFQUFFLGVBQWU7QUFDekIsTUFBTSxFQUFFLEdBQUcsQ0FBQztFQUVWOztFQUVBO0VBQ0E7RUFDQSxNQUFNQyxlQUFlLEdBQUdsQixhQUFhLENBQUNhLE1BQU0sRUFBRSxJQUFJLEVBQUUsQ0FBQyxDQUFDO0VBRXRELE9BQU8sQ0FBQyxVQUFVLENBQUMsT0FBTyxDQUFDLENBQUNLLGVBQWUsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDSCxPQUFPLENBQUMsR0FBRztBQUNuRSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/tools/ReadMcpResourceTool/prompt.ts`

**信息:**
- 行数: 16
- 大小: 544 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const DESCRIPTION = `
Reads a specific resource from an MCP server.
- server: The name of the MCP server to read from
- uri: The URI of the resource to read

Usage examples:
- Read a resource from a server: \`readMcpResource({ server: "myserver", uri: "my-resource-uri" })\`
`

export const PROMPT = `
Reads a specific resource from an MCP server, identified by server name and resource URI.

Parameters:
- server (required): The name of the MCP server from which to read the resource
- uri (required): The URI of the resource to read
`

```

---


### `src/tools/RemoteTriggerTool/RemoteTriggerTool.ts`

**信息:**
- 行数: 161
- 大小: 4715 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { z } from 'zod/v4'
import { getOauthConfig } from '../../constants/oauth.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import { getOrganizationUUID } from '../../services/oauth/client.js'
import { isPolicyAllowed } from '../../services/policyLimits/index.js'
import type { ToolUseContext } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import {
  checkAndRefreshOAuthTokenIfNeeded,
  getClaudeAIOAuthTokens,
} from '../../utils/auth.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { DESCRIPTION, PROMPT, REMOTE_TRIGGER_TOOL_NAME } from './prompt.js'
import { renderToolResultMessage, renderToolUseMessage } from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    action: z.enum(['list', 'get', 'create', 'update', 'run']),
    trigger_id: z
      .string()
      .regex(/^[\w-]+$/)
      .optional()
      .describe('Required for get, update, and run'),
    body: z
      .record(z.string(), z.unknown())
      .optional()
      .describe('JSON body for create and update'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>
export type Input = z.infer<InputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    status: z.number(),
    json: z.string(),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>
export type Output = z.infer<OutputSchema>

const TRIGGERS_BETA = 'ccr-triggers-2026-01-30'

export const RemoteTriggerTool = buildTool({
  name: REMOTE_TRIGGER_TOOL_NAME,
  searchHint: 'manage scheduled remote agent triggers',
  maxResultSizeChars: 100_000,
  shouldDefer: true,

```

---


### `src/tools/RemoteTriggerTool/UI.tsx`

**信息:**
- 行数: 17
- 大小: 3096 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { MessageResponse } from '../../components/MessageResponse.js';
import { Text } from '../../ink.js';
import { countCharInString } from '../../utils/stringUtils.js';
import type { Input, Output } from './RemoteTriggerTool.js';
export function renderToolUseMessage(input: Partial<Input>): React.ReactNode {
  return `${input.action ?? ''}${input.trigger_id ? ` ${input.trigger_id}` : ''}`;
}
export function renderToolResultMessage(output: Output): React.ReactNode {
  const lines = countCharInString(output.json, '\n') + 1;
  return <MessageResponse>
      <Text>
        HTTP {output.status} <Text dimColor>({lines} lines)</Text>
      </Text>
    </MessageResponse>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIk1lc3NhZ2VSZXNwb25zZSIsIlRleHQiLCJjb3VudENoYXJJblN0cmluZyIsIklucHV0IiwiT3V0cHV0IiwicmVuZGVyVG9vbFVzZU1lc3NhZ2UiLCJpbnB1dCIsIlBhcnRpYWwiLCJSZWFjdE5vZGUiLCJhY3Rpb24iLCJ0cmlnZ2VyX2lkIiwicmVuZGVyVG9vbFJlc3VsdE1lc3NhZ2UiLCJvdXRwdXQiLCJsaW5lcyIsImpzb24iLCJzdGF0dXMiXSwic291cmNlcyI6WyJVSS50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsgTWVzc2FnZVJlc3BvbnNlIH0gZnJvbSAnLi4vLi4vY29tcG9uZW50cy9NZXNzYWdlUmVzcG9uc2UuanMnXG5pbXBvcnQgeyBUZXh0IH0gZnJvbSAnLi4vLi4vaW5rLmpzJ1xuaW1wb3J0IHsgY291bnRDaGFySW5TdHJpbmcgfSBmcm9tICcuLi8uLi91dGlscy9zdHJpbmdVdGlscy5qcydcbmltcG9ydCB0eXBlIHsgSW5wdXQsIE91dHB1dCB9IGZyb20gJy4vUmVtb3RlVHJpZ2dlclRvb2wuanMnXG5cbmV4cG9ydCBmdW5jdGlvbiByZW5kZXJUb29sVXNlTWVzc2FnZShpbnB1dDogUGFydGlhbDxJbnB1dD4pOiBSZWFjdC5SZWFjdE5vZGUge1xuICByZXR1cm4gYCR7aW5wdXQuYWN0aW9uID8/ICcnfSR7aW5wdXQudHJpZ2dlcl9pZCA/IGAgJHtpbnB1dC50cmlnZ2VyX2lkfWAgOiAnJ31gXG59XG5cbmV4cG9ydCBmdW5jdGlvbiByZW5kZXJUb29sUmVzdWx0TWVzc2FnZShvdXRwdXQ6IE91dHB1dCk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIGNvbnN0IGxpbmVzID0gY291bnRDaGFySW5TdHJpbmcob3V0cHV0Lmpzb24sICdcXG4nKSArIDFcbiAgcmV0dXJuIChcbiAgICA8TWVzc2FnZVJlc3BvbnNlPlxuICAgICAgPFRleHQ+XG4gICAgICAgIEhUVFAge291dHB1dC5zdGF0dXN9IDxUZXh0IGRpbUNvbG9yPih7bGluZXN9IGxpbmVzKTwvVGV4dD5cbiAgICAgIDwvVGV4dD5cbiAgICA8L01lc3NhZ2VSZXNwb25zZT5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPQSxLQUFLLE1BQU0sT0FBTztBQUN6QixTQUFTQyxlQUFlLFFBQVEscUNBQXFDO0FBQ3JFLFNBQVNDLElBQUksUUFBUSxjQUFjO0FBQ25DLFNBQVNDLGlCQUFpQixRQUFRLDRCQUE0QjtBQUM5RCxjQUFjQyxLQUFLLEVBQUVDLE1BQU0sUUFBUSx3QkFBd0I7QUFFM0QsT0FBTyxTQUFTQyxvQkFBb0JBLENBQUNDLEtBQUssRUFBRUMsT0FBTyxDQUFDSixLQUFLLENBQUMsQ0FBQyxFQUFFSixLQUFLLENBQUNTLFNBQVMsQ0FBQztFQUMzRSxPQUFPLEdBQUdGLEtBQUssQ0FBQ0csTUFBTSxJQUFJLEVBQUUsR0FBR0gsS0FBSyxDQUFDSSxVQUFVLEdBQUcsSUFBSUosS0FBSyxDQUFDSSxVQUFVLEVBQUUsR0FBRyxFQUFFLEVBQUU7QUFDakY7QUFFQSxPQUFPLFNBQVNDLHVCQUF1QkEsQ0FBQ0MsTUFBTSxFQUFFUixNQUFNLENBQUMsRUFBRUwsS0FBSyxDQUFDUyxTQUFTLENBQUM7RUFDdkUsTUFBTUssS0FBSyxHQUFHWCxpQkFBaUIsQ0FBQ1UsTUFBTSxDQUFDRSxJQUFJLEVBQUUsSUFBSSxDQUFDLEdBQUcsQ0FBQztFQUN0RCxPQUNFLENBQUMsZUFBZTtBQUNwQixNQUFNLENBQUMsSUFBSTtBQUNYLGFBQWEsQ0FBQ0YsTUFBTSxDQUFDRyxNQUFNLENBQUMsQ0FBQyxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsQ0FBQyxDQUFDRixLQUFLLENBQUMsT0FBTyxFQUFFLElBQUk7QUFDakUsTUFBTSxFQUFFLElBQUk7QUFDWixJQUFJLEVBQUUsZUFBZSxDQUFDO0FBRXRCIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/tools/RemoteTriggerTool/prompt.ts`

**信息:**
- 行数: 15
- 大小: 697 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const REMOTE_TRIGGER_TOOL_NAME = 'RemoteTrigger'

export const DESCRIPTION =
  'Manage scheduled remote Claude Code agents (triggers) via the claude.ai CCR API. Auth is handled in-process — the token never reaches the shell.'

export const PROMPT = `Call the claude.ai remote-trigger API. Use this instead of curl — the OAuth token is added automatically in-process and never exposed.

Actions:
- list: GET /v1/code/triggers
- get: GET /v1/code/triggers/{trigger_id}
- create: POST /v1/code/triggers (requires body)
- update: POST /v1/code/triggers/{trigger_id} (requires body, partial update)
- run: POST /v1/code/triggers/{trigger_id}/run

The response is the raw JSON from the API.`

```

---


### `src/tools/ReviewArtifactTool/ReviewArtifactTool.ts`

**信息:**
- 行数: 1
- 大小: 39 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const ReviewArtifactTool = null

```

---


### `src/tools/ScheduleCronTool/CronCreateTool.ts`

**信息:**
- 行数: 157
- 大小: 5710 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { setScheduledTasksEnabled } from '../../bootstrap/state.js'
import type { ValidationResult } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { cronToHuman, parseCronExpression } from '../../utils/cron.js'
import {
  addCronTask,
  getCronFilePath,
  listAllCronTasks,
  nextCronRunMs,
} from '../../utils/cronTasks.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { semanticBoolean } from '../../utils/semanticBoolean.js'
import { getTeammateContext } from '../../utils/teammateContext.js'
import {
  buildCronCreateDescription,
  buildCronCreatePrompt,
  CRON_CREATE_TOOL_NAME,
  DEFAULT_MAX_AGE_DAYS,
  isDurableCronEnabled,
  isKairosCronEnabled,
} from './prompt.js'
import { renderCreateResultMessage, renderCreateToolUseMessage } from './UI.js'

const MAX_JOBS = 50

const inputSchema = lazySchema(() =>
  z.strictObject({
    cron: z
      .string()
      .describe(
        'Standard 5-field cron expression in local time: "M H DoM Mon DoW" (e.g. "*/5 * * * *" = every 5 minutes, "30 14 28 2 *" = Feb 28 at 2:30pm local once).',
      ),
    prompt: z.string().describe('The prompt to enqueue at each fire time.'),
    recurring: semanticBoolean(z.boolean().optional()).describe(
      `true (default) = fire on every cron match until deleted or auto-expired after ${DEFAULT_MAX_AGE_DAYS} days. false = fire once at the next match, then auto-delete. Use false for "remind me at X" one-shot requests with pinned minute/hour/dom/month.`,
    ),
    durable: semanticBoolean(z.boolean().optional()).describe(
      'true = persist to .claude/scheduled_tasks.json and survive restarts. false (default) = in-memory only, dies when this Claude session ends. Use true only when the user asks the task to survive across sessions.',
    ),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    id: z.string(),
    humanSchedule: z.string(),
    recurring: z.boolean(),
    durable: z.boolean().optional(),

```

---


### `src/tools/ScheduleCronTool/CronDeleteTool.ts`

**信息:**
- 行数: 95
- 大小: 2616 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import type { ValidationResult } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import {
  getCronFilePath,
  listAllCronTasks,
  removeCronTasks,
} from '../../utils/cronTasks.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { getTeammateContext } from '../../utils/teammateContext.js'
import {
  buildCronDeletePrompt,
  CRON_DELETE_DESCRIPTION,
  CRON_DELETE_TOOL_NAME,
  isDurableCronEnabled,
  isKairosCronEnabled,
} from './prompt.js'
import { renderDeleteResultMessage, renderDeleteToolUseMessage } from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    id: z.string().describe('Job ID returned by CronCreate.'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    id: z.string(),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>
export type DeleteOutput = z.infer<OutputSchema>

export const CronDeleteTool = buildTool({
  name: CRON_DELETE_TOOL_NAME,
  searchHint: 'cancel a scheduled cron job',
  maxResultSizeChars: 100_000,
  shouldDefer: true,
  get inputSchema(): InputSchema {
    return inputSchema()
  },
  get outputSchema(): OutputSchema {
    return outputSchema()
  },
  isEnabled() {
    return isKairosCronEnabled()
  },
  toAutoClassifierInput(input) {
    return input.id

```

---


### `src/tools/ScheduleCronTool/CronListTool.ts`

**信息:**
- 行数: 97
- 大小: 2888 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { buildTool, type ToolDef } from '../../Tool.js'
import { cronToHuman } from '../../utils/cron.js'
import { listAllCronTasks } from '../../utils/cronTasks.js'
import { truncate } from '../../utils/format.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { getTeammateContext } from '../../utils/teammateContext.js'
import {
  buildCronListPrompt,
  CRON_LIST_DESCRIPTION,
  CRON_LIST_TOOL_NAME,
  isDurableCronEnabled,
  isKairosCronEnabled,
} from './prompt.js'
import { renderListResultMessage, renderListToolUseMessage } from './UI.js'

const inputSchema = lazySchema(() => z.strictObject({}))
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    jobs: z.array(
      z.object({
        id: z.string(),
        cron: z.string(),
        humanSchedule: z.string(),
        prompt: z.string(),
        recurring: z.boolean().optional(),
        durable: z.boolean().optional(),
      }),
    ),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>
export type ListOutput = z.infer<OutputSchema>

export const CronListTool = buildTool({
  name: CRON_LIST_TOOL_NAME,
  searchHint: 'list active cron jobs',
  maxResultSizeChars: 100_000,
  shouldDefer: true,
  get inputSchema(): InputSchema {
    return inputSchema()
  },
  get outputSchema(): OutputSchema {
    return outputSchema()
  },
  isEnabled() {
    return isKairosCronEnabled()
  },

```

---


### `src/tools/ScheduleCronTool/UI.tsx`

**信息:**
- 行数: 60
- 大小: 8075 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { MessageResponse } from '../../components/MessageResponse.js';
import { Text } from '../../ink.js';
import { truncate } from '../../utils/format.js';
import type { CreateOutput } from './CronCreateTool.js';
import type { DeleteOutput } from './CronDeleteTool.js';
import type { ListOutput } from './CronListTool.js';

// --- CronCreate -------------------------------------------------------------

export function renderCreateToolUseMessage(input: Partial<{
  cron: string;
  prompt: string;
}>): React.ReactNode {
  return `${input.cron ?? ''}${input.prompt ? `: ${truncate(input.prompt, 60, true)}` : ''}`;
}
export function renderCreateResultMessage(output: CreateOutput): React.ReactNode {
  return <MessageResponse>
      <Text>
        Scheduled <Text bold>{output.id}</Text>{' '}
        <Text dimColor>({output.humanSchedule})</Text>
      </Text>
    </MessageResponse>;
}

// --- CronDelete -------------------------------------------------------------

export function renderDeleteToolUseMessage(input: Partial<{
  id: string;
}>): React.ReactNode {
  return input.id ?? '';
}
export function renderDeleteResultMessage(output: DeleteOutput): React.ReactNode {
  return <MessageResponse>
      <Text>
        Cancelled <Text bold>{output.id}</Text>
      </Text>
    </MessageResponse>;
}

// --- CronList ---------------------------------------------------------------

export function renderListToolUseMessage(): React.ReactNode {
  return '';
}
export function renderListResultMessage(output: ListOutput): React.ReactNode {
  if (output.jobs.length === 0) {
    return <MessageResponse>
        <Text dimColor>No scheduled jobs</Text>
      </MessageResponse>;

```

---


### `src/tools/ScheduleCronTool/prompt.ts`

**信息:**
- 行数: 135
- 大小: 7518 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { getFeatureValue_CACHED_WITH_REFRESH } from '../../services/analytics/growthbook.js'
import { DEFAULT_CRON_JITTER_CONFIG } from '../../utils/cronTasks.js'
import { isEnvTruthy } from '../../utils/envUtils.js'

const KAIROS_CRON_REFRESH_MS = 5 * 60 * 1000

export const DEFAULT_MAX_AGE_DAYS =
  DEFAULT_CRON_JITTER_CONFIG.recurringMaxAgeMs / (24 * 60 * 60 * 1000)

/**
 * Unified gate for the cron scheduling system. Combines the build-time
 * `feature('AGENT_TRIGGERS')` flag (dead code elimination) with the runtime
 * `tengu_kairos_cron` GrowthBook gate on a 5-minute refresh window.
 *
 * AGENT_TRIGGERS is independently shippable from KAIROS — the cron module
 * graph (cronScheduler/cronTasks/cronTasksLock/cron.ts + the three tools +
 * /loop skill) has zero imports into src/assistant/ and no feature('KAIROS')
 * calls. The REPL.tsx kairosEnabled read is safe:
 * kairosEnabled is unconditionally in AppStateStore with default false, so
 * when KAIROS is off the scheduler just gets assistantMode: false.
 *
 * Called from Tool.isEnabled() (lazy, post-init) and inside useEffect /
 * imperative setup, never at module scope — so the disk cache has had a
 * chance to populate.
 *
 * The default is `true` — /loop is GA (announced in changelog). GrowthBook
 * is disabled for Bedrock/Vertex/Foundry and when DISABLE_TELEMETRY /
 * CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC are set; a `false` default would
 * break /loop for those users (GH #31759). The GB gate now serves purely as
 * a fleet-wide kill switch — flipping it to `false` stops already-running
 * schedulers on their next isKilled poll tick, not just new ones.
 *
 * `CLAUDE_CODE_DISABLE_CRON` is a local override that wins over GB.
 */
export function isKairosCronEnabled(): boolean {
  return feature('AGENT_TRIGGERS')
    ? !isEnvTruthy(process.env.CLAUDE_CODE_DISABLE_CRON) &&
        getFeatureValue_CACHED_WITH_REFRESH(
          'tengu_kairos_cron',
          true,
          KAIROS_CRON_REFRESH_MS,
        )
    : false
}

/**
 * Kill switch for disk-persistent (durable) cron tasks. Narrower than
 * {@link isKairosCronEnabled} — flipping this off forces `durable: false` at
 * the call() site, leaving session-only cron (in-memory, GA) untouched.

```

---


### `src/tools/SendMessageTool/SendMessageTool.ts`

**信息:**
- 行数: 917
- 大小: 27506 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { z } from 'zod/v4'
import { isReplBridgeActive } from '../../bootstrap/state.js'
import { getReplBridgeHandle } from '../../bridge/replBridgeHandle.js'
import type { Tool, ToolUseContext } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { findTeammateTaskByAgentId } from '../../tasks/InProcessTeammateTask/InProcessTeammateTask.js'
import {
  isLocalAgentTask,
  queuePendingMessage,
} from '../../tasks/LocalAgentTask/LocalAgentTask.js'
import { isMainSessionTask } from '../../tasks/LocalMainSessionTask.js'
import { toAgentId } from '../../types/ids.js'
import { generateRequestId } from '../../utils/agentId.js'
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { truncate } from '../../utils/format.js'
import { gracefulShutdown } from '../../utils/gracefulShutdown.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { parseAddress } from '../../utils/peerAddress.js'
import { semanticBoolean } from '../../utils/semanticBoolean.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import type { BackendType } from '../../utils/swarm/backends/types.js'
import { TEAM_LEAD_NAME } from '../../utils/swarm/constants.js'
import { readTeamFileAsync } from '../../utils/swarm/teamHelpers.js'
import {
  getAgentId,
  getAgentName,
  getTeammateColor,
  getTeamName,
  isTeamLead,
  isTeammate,
} from '../../utils/teammate.js'
import {
  createShutdownApprovedMessage,
  createShutdownRejectedMessage,
  createShutdownRequestMessage,
  writeToMailbox,
} from '../../utils/teammateMailbox.js'
import { resumeAgentBackground } from '../AgentTool/resumeAgent.js'
import { SEND_MESSAGE_TOOL_NAME } from './constants.js'
import { DESCRIPTION, getPrompt } from './prompt.js'
import { renderToolResultMessage, renderToolUseMessage } from './UI.js'

const StructuredMessage = lazySchema(() =>
  z.discriminatedUnion('type', [
    z.object({
      type: z.literal('shutdown_request'),
      reason: z.string().optional(),

```

---


### `src/tools/SendMessageTool/UI.tsx`

**信息:**
- 行数: 31
- 大小: 4679 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { MessageResponse } from '../../components/MessageResponse.js';
import { Text } from '../../ink.js';
import { jsonParse } from '../../utils/slowOperations.js';
import type { Input, SendMessageToolOutput } from './SendMessageTool.js';
export function renderToolUseMessage(input: Partial<Input>): React.ReactNode {
  if (typeof input.message !== 'object' || input.message === null) {
    return null;
  }
  if (input.message.type === 'plan_approval_response') {
    return input.message.approve ? `approve plan from: ${input.to}` : `reject plan from: ${input.to}`;
  }
  return null;
}
export function renderToolResultMessage(content: SendMessageToolOutput | string, _progressMessages: unknown, {
  verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  const result: SendMessageToolOutput = typeof content === 'string' ? jsonParse(content) : content;
  if ('routing' in result && result.routing) {
    return null;
  }
  if ('request_id' in result && 'target' in result) {
    return null;
  }
  return <MessageResponse>
      <Text dimColor>{result.message}</Text>
    </MessageResponse>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIk1lc3NhZ2VSZXNwb25zZSIsIlRleHQiLCJqc29uUGFyc2UiLCJJbnB1dCIsIlNlbmRNZXNzYWdlVG9vbE91dHB1dCIsInJlbmRlclRvb2xVc2VNZXNzYWdlIiwiaW5wdXQiLCJQYXJ0aWFsIiwiUmVhY3ROb2RlIiwibWVzc2FnZSIsInR5cGUiLCJhcHByb3ZlIiwidG8iLCJyZW5kZXJUb29sUmVzdWx0TWVzc2FnZSIsImNvbnRlbnQiLCJfcHJvZ3Jlc3NNZXNzYWdlcyIsInZlcmJvc2UiLCJyZXN1bHQiLCJyb3V0aW5nIl0sInNvdXJjZXMiOlsiVUkudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCdcbmltcG9ydCB7IE1lc3NhZ2VSZXNwb25zZSB9IGZyb20gJy4uLy4uL2NvbXBvbmVudHMvTWVzc2FnZVJlc3BvbnNlLmpzJ1xuaW1wb3J0IHsgVGV4dCB9IGZyb20gJy4uLy4uL2luay5qcydcbmltcG9ydCB7IGpzb25QYXJzZSB9IGZyb20gJy4uLy4uL3V0aWxzL3Nsb3dPcGVyYXRpb25zLmpzJ1xuaW1wb3J0IHR5cGUgeyBJbnB1dCwgU2VuZE1lc3NhZ2VUb29sT3V0cHV0IH0gZnJvbSAnLi9TZW5kTWVzc2FnZVRvb2wuanMnXG5cbmV4cG9ydCBmdW5jdGlvbiByZW5kZXJUb29sVXNlTWVzc2FnZShpbnB1dDogUGFydGlhbDxJbnB1dD4pOiBSZWFjdC5SZWFjdE5vZGUge1xuICBpZiAodHlwZW9mIGlucHV0Lm1lc3NhZ2UgIT09ICdvYmplY3QnIHx8IGlucHV0Lm1lc3NhZ2UgPT09IG51bGwpIHtcbiAgICByZXR1cm4gbnVsbFxuICB9XG4gIGlmIChpbnB1dC5tZXNzYWdlLnR5cGUgPT09ICdwbGFuX2FwcHJvdmFsX3Jlc3BvbnNlJykge1xuICAgIHJldHVybiBpbnB1dC5tZXNzYWdlLmFwcHJvdmVcbiAgICAgID8gYGFwcHJvdmUgcGxhbiBmcm9tOiAke2lucHV0LnRvfWBcbiAgICAgIDogYHJlamVjdCBwbGFuIGZyb206ICR7aW5wdXQudG99YFxuICB9XG4gIHJldHVybiBudWxsXG59XG5cbmV4cG9ydCBmdW5jdGlvbiByZW5kZXJUb29sUmVzdWx0TWVzc2FnZShcbiAgY29udGVudDogU2VuZE1lc3NhZ2VUb29sT3V0cHV0IHwgc3RyaW5nLFxuICBfcHJvZ3Jlc3NNZXNzYWdlczogdW5rbm93bixcbiAgeyB2ZXJib3NlIH06IHsgdmVyYm9zZTogYm9vbGVhbiB9LFxuKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgY29uc3QgcmVzdWx0OiBTZW5kTWVzc2FnZVRvb2xPdXRwdXQgPVxuICAgIHR5cGVvZiBjb250ZW50ID09PSAnc3RyaW5nJyA/IGpzb25QYXJzZShjb250ZW50KSA6IGNvbnRlbnRcblxuICBpZiAoJ3JvdXRpbmcnIGluIHJlc3VsdCAmJiByZXN1bHQucm91dGluZykge1xuICAgIHJldHVybiBudWxsXG4gIH1cblxuICBpZiAoJ3JlcXVlc3RfaWQnIGluIHJlc3VsdCAmJiAndGFyZ2V0JyBpbiByZXN1bHQpIHtcbiAgICByZXR1cm4gbnVsbFxuICB9XG5cbiAgcmV0dXJuIChcbiAgICA8TWVzc2FnZVJlc3BvbnNlPlxuICAgICAgPFRleHQgZGltQ29sb3I+e3Jlc3VsdC5tZXNzYWdlfTwvVGV4dD5cbiAgICA8L01lc3NhZ2VSZXNwb25zZT5cbiAgKVxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPQSxLQUFLLE1BQU0sT0FBTztBQUN6QixTQUFTQyxlQUFlLFFBQVEscUNBQXFDO0FBQ3JFLFNBQVNDLElBQUksUUFBUSxjQUFjO0FBQ25DLFNBQVNDLFNBQVMsUUFBUSwrQkFBK0I7QUFDekQsY0FBY0MsS0FBSyxFQUFFQyxxQkFBcUIsUUFBUSxzQkFBc0I7QUFFeEUsT0FBTyxTQUFTQyxvQkFBb0JBLENBQUNDLEtBQUssRUFBRUMsT0FBTyxDQUFDSixLQUFLLENBQUMsQ0FBQyxFQUFFSixLQUFLLENBQUNTLFNBQVMsQ0FBQztFQUMzRSxJQUFJLE9BQU9GLEtBQUssQ0FBQ0csT0FBTyxLQUFLLFFBQVEsSUFBSUgsS0FBSyxDQUFDRyxPQUFPLEtBQUssSUFBSSxFQUFFO0lBQy9ELE9BQU8sSUFBSTtFQUNiO0VBQ0EsSUFBSUgsS0FBSyxDQUFDRyxPQUFPLENBQUNDLElBQUksS0FBSyx3QkFBd0IsRUFBRTtJQUNuRCxPQUFPSixLQUFLLENBQUNHLE9BQU8sQ0FBQ0UsT0FBTyxHQUN4QixzQkFBc0JMLEtBQUssQ0FBQ00sRUFBRSxFQUFFLEdBQ2hDLHFCQUFxQk4sS0FBSyxDQUFDTSxFQUFFLEVBQUU7RUFDckM7RUFDQSxPQUFPLElBQUk7QUFDYjtBQUVBLE9BQU8sU0FBU0MsdUJBQXVCQSxDQUNyQ0MsT0FBTyxFQUFFVixxQkFBcUIsR0FBRyxNQUFNLEVBQ3ZDVyxpQkFBaUIsRUFBRSxPQUFPLEVBQzFCO0VBQUVDO0FBQThCLENBQXJCLEVBQUU7RUFBRUEsT0FBTyxFQUFFLE9BQU87QUFBQyxDQUFDLENBQ2xDLEVBQUVqQixLQUFLLENBQUNTLFNBQVMsQ0FBQztFQUNqQixNQUFNUyxNQUFNLEVBQUViLHFCQUFxQixHQUNqQyxPQUFPVSxPQUFPLEtBQUssUUFBUSxHQUFHWixTQUFTLENBQUNZLE9BQU8sQ0FBQyxHQUFHQSxPQUFPO0VBRTVELElBQUksU0FBUyxJQUFJRyxNQUFNLElBQUlBLE1BQU0sQ0FBQ0MsT0FBTyxFQUFFO0lBQ3pDLE9BQU8sSUFBSTtFQUNiO0VBRUEsSUFBSSxZQUFZLElBQUlELE1BQU0sSUFBSSxRQUFRLElBQUlBLE1BQU0sRUFBRTtJQUNoRCxPQUFPLElBQUk7RUFDYjtFQUVBLE9BQ0UsQ0FBQyxlQUFlO0FBQ3BCLE1BQU0sQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFDLENBQUNBLE1BQU0sQ0FBQ1IsT0FBTyxDQUFDLEVBQUUsSUFBSTtBQUMzQyxJQUFJLEVBQUUsZUFBZSxDQUFDO0FBRXRCIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/tools/SendMessageTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 52 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const SEND_MESSAGE_TOOL_NAME = 'SendMessage'

```

---


### `src/tools/SendMessageTool/prompt.ts`

**信息:**
- 行数: 49
- 大小: 2356 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'

export const DESCRIPTION = 'Send a message to another agent'

export function getPrompt(): string {
  const udsRow = feature('UDS_INBOX')
    ? `\n| \`"uds:/path/to.sock"\` | Local Claude session's socket (same machine; use \`ListPeers\`) |
| \`"bridge:session_..."\` | Remote Control peer session (cross-machine; use \`ListPeers\`) |`
    : ''
  const udsSection = feature('UDS_INBOX')
    ? `\n\n## Cross-session

Use \`ListPeers\` to discover targets, then:

\`\`\`json
{"to": "uds:/tmp/cc-socks/1234.sock", "message": "check if tests pass over there"}
{"to": "bridge:session_01AbCd...", "message": "what branch are you on?"}
\`\`\`

A listed peer is alive and will process your message — no "busy" state; messages enqueue and drain at the receiver's next tool round. Your message arrives wrapped as \`<cross-session-message from="...">\`. **To reply to an incoming message, copy its \`from\` attribute as your \`to\`.**`
    : ''
  return `
# SendMessage

Send a message to another agent.

\`\`\`json
{"to": "researcher", "summary": "assign task 1", "message": "start on task #1"}
\`\`\`

| \`to\` | |
|---|---|
| \`"researcher"\` | Teammate by name |
| \`"*"\` | Broadcast to all teammates — expensive (linear in team size), use only when everyone genuinely needs it |${udsRow}

Your plain text output is NOT visible to other agents — to communicate, you MUST call this tool. Messages from teammates are delivered automatically; you don't check an inbox. Refer to teammates by name, never by UUID. When relaying, don't quote the original — it's already rendered to the user.${udsSection}

## Protocol responses (legacy)

If you receive a JSON message with \`type: "shutdown_request"\` or \`type: "plan_approval_request"\`, respond with the matching \`_response\` type — echo the \`request_id\`, set \`approve\` true/false:

\`\`\`json
{"to": "team-lead", "message": {"type": "shutdown_response", "request_id": "...", "approve": true}}
{"to": "researcher", "message": {"type": "plan_approval_response", "request_id": "...", "approve": false, "feedback": "add error handling"}}
\`\`\`

Approving shutdown terminates your process. Rejecting plan sends the teammate back to revise. Don't originate \`shutdown_request\` unless asked. Don't send structured JSON status messages — use TaskUpdate.
`.trim()
}

```

---


### `src/tools/SendUserFileTool/prompt.ts`

**信息:**
- 行数: 1
- 大小: 57 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const SEND_USER_FILE_TOOL_NAME = 'send_user_file'

```

---


### `src/tools/SkillTool/SkillTool.ts`

**信息:**
- 行数: 1108
- 大小: 38175 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs'
import uniqBy from 'lodash-es/uniqBy.js'
import { dirname } from 'path'
import { getProjectRoot } from 'src/bootstrap/state.js'
import {
  builtInCommandNames,
  findCommand,
  getCommands,
  type PromptCommand,
} from 'src/commands.js'
import type {
  Tool,
  ToolCallProgress,
  ToolResult,
  ToolUseContext,
  ValidationResult,
} from 'src/Tool.js'
import { buildTool, type ToolDef } from 'src/Tool.js'
import type { Command } from 'src/types/command.js'
import type {
  AssistantMessage,
  AttachmentMessage,
  Message,
  SystemMessage,
  UserMessage,
} from 'src/types/message.js'
import { logForDebugging } from 'src/utils/debug.js'
import type { PermissionDecision } from 'src/utils/permissions/PermissionResult.js'
import { getRuleByContentsForTool } from 'src/utils/permissions/permissions.js'
import {
  isOfficialMarketplaceName,
  parsePluginIdentifier,
} from 'src/utils/plugins/pluginIdentifier.js'
import { buildPluginCommandTelemetryFields } from 'src/utils/telemetry/pluginTelemetry.js'
import { z } from 'zod/v4'
import {
  addInvokedSkill,
  clearInvokedSkillsForAgent,
  getSessionId,
} from '../../bootstrap/state.js'
import { COMMAND_MESSAGE_TAG } from '../../constants/xml.js'
import type { CanUseToolFn } from '../../hooks/useCanUseTool.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_PII_TAGGED,
  logEvent,
} from '../../services/analytics/index.js'
import { getAgentContext } from '../../utils/agentContext.js'
import { errorMessage } from '../../utils/errors.js'

```

---


### `src/tools/SkillTool/UI.tsx`

**信息:**
- 行数: 128
- 大小: 19189 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs';
import * as React from 'react';
import { SubAgentProvider } from 'src/components/CtrlOToExpand.js';
import { FallbackToolUseErrorMessage } from 'src/components/FallbackToolUseErrorMessage.js';
import { FallbackToolUseRejectedMessage } from 'src/components/FallbackToolUseRejectedMessage.js';
import type { z } from 'zod/v4';
import type { Command } from '../../commands.js';
import { Byline } from '../../components/design-system/Byline.js';
import { Message as MessageComponent } from '../../components/Message.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { Box, Text } from '../../ink.js';
import type { Tools } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import { buildSubagentLookups, EMPTY_LOOKUPS } from '../../utils/messages.js';
import { plural } from '../../utils/stringUtils.js';
import type { inputSchema, Output, Progress } from './SkillTool.js';
type Input = z.infer<ReturnType<typeof inputSchema>>;
const MAX_PROGRESS_MESSAGES_TO_SHOW = 3;
const INITIALIZING_TEXT = 'Initializing…';
export function renderToolResultMessage(output: Output): React.ReactNode {
  // Handle forked skill result
  if ('status' in output && output.status === 'forked') {
    return <MessageResponse height={1}>
        <Text>
          <Byline>{['Done']}</Byline>
        </Text>
      </MessageResponse>;
  }
  const parts: string[] = ['Successfully loaded skill'];

  // Show tools count (only for inline skills)
  if ('allowedTools' in output && output.allowedTools && output.allowedTools.length > 0) {
    const count = output.allowedTools.length;
    parts.push(`${count} ${plural(count, 'tool')} allowed`);
  }

  // Show model if non-default (only for inline skills)
  if ('model' in output && output.model) {
    parts.push(output.model);
  }
  return <MessageResponse height={1}>
      <Text>
        <Byline>{parts}</Byline>
      </Text>
    </MessageResponse>;
}
export function renderToolUseMessage({
  skill
}: Partial<Input>, {
  commands

```

---


### `src/tools/SkillTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 39 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const SKILL_TOOL_NAME = 'Skill'

```

---


### `src/tools/SkillTool/prompt.ts`

**信息:**
- 行数: 241
- 大小: 8221 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { memoize } from 'lodash-es'
import type { Command } from 'src/commands.js'
import {
  getCommandName,
  getSkillToolCommands,
  getSlashCommandToolSkills,
} from 'src/commands.js'
import { COMMAND_NAME_TAG } from '../../constants/xml.js'
import { stringWidth } from '../../ink/stringWidth.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import { count } from '../../utils/array.js'
import { logForDebugging } from '../../utils/debug.js'
import { toError } from '../../utils/errors.js'
import { truncate } from '../../utils/format.js'
import { logError } from '../../utils/log.js'

// Skill listing gets 1% of the context window (in characters)
export const SKILL_BUDGET_CONTEXT_PERCENT = 0.01
export const CHARS_PER_TOKEN = 4
export const DEFAULT_CHAR_BUDGET = 8_000 // Fallback: 1% of 200k × 4

// Per-entry hard cap. The listing is for discovery only — the Skill tool loads
// full content on invoke, so verbose whenToUse strings waste turn-1 cache_creation
// tokens without improving match rate. Applies to all entries, including bundled,
// since the cap is generous enough to preserve the core use case.
export const MAX_LISTING_DESC_CHARS = 250

export function getCharBudget(contextWindowTokens?: number): number {
  if (Number(process.env.SLASH_COMMAND_TOOL_CHAR_BUDGET)) {
    return Number(process.env.SLASH_COMMAND_TOOL_CHAR_BUDGET)
  }
  if (contextWindowTokens) {
    return Math.floor(
      contextWindowTokens * CHARS_PER_TOKEN * SKILL_BUDGET_CONTEXT_PERCENT,
    )
  }
  return DEFAULT_CHAR_BUDGET
}

function getCommandDescription(cmd: Command): string {
  const desc = cmd.whenToUse
    ? `${cmd.description} - ${cmd.whenToUse}`
    : cmd.description
  return desc.length > MAX_LISTING_DESC_CHARS
    ? desc.slice(0, MAX_LISTING_DESC_CHARS - 1) + '\u2026'
    : desc
}

```

---


### `src/tools/SleepTool/prompt.ts`

**信息:**
- 行数: 17
- 大小: 774 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { TICK_TAG } from '../../constants/xml.js'

export const SLEEP_TOOL_NAME = 'Sleep'

export const DESCRIPTION = 'Wait for a specified duration'

export const SLEEP_TOOL_PROMPT = `Wait for a specified duration. The user can interrupt the sleep at any time.

Use this when the user tells you to sleep or rest, when you have nothing to do, or when you're waiting for something.

You may receive <${TICK_TAG}> prompts — these are periodic check-ins. Look for useful work to do before sleeping.

You can call this concurrently with other tools — it won't interfere with them.

Prefer this over \`Bash(sleep ...)\` — it doesn't hold a shell process.

Each wake-up costs an API call, but the prompt cache expires after 5 minutes of inactivity — balance accordingly.`

```

---


### `src/tools/SnipTool/prompt.ts`

**信息:**
- 行数: 1
- 大小: 37 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const SNIP_TOOL_NAME = 'snip'

```

---


### `src/tools/SyntheticOutputTool/SyntheticOutputTool.ts`

**信息:**
- 行数: 163
- 大小: 5468 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { Ajv } from 'ajv'
import { z } from 'zod/v4'
import type { Tool, ToolInputJSONSchema } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { TelemetrySafeError_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS } from '../../utils/errors.js'
import { lazySchema } from '../../utils/lazySchema.js'
import type { PermissionResult } from '../../utils/permissions/PermissionResult.js'
import { jsonStringify } from '../../utils/slowOperations.js'

// Allow any input object since the schema is provided dynamically
const inputSchema = lazySchema(() => z.object({}).passthrough())
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.string().describe('Structured output tool result'),
)
type OutputSchema = ReturnType<typeof outputSchema>
export type Output = z.infer<OutputSchema>

export const SYNTHETIC_OUTPUT_TOOL_NAME = 'StructuredOutput'

export function isSyntheticOutputToolEnabled(opts: {
  isNonInteractiveSession: boolean
}): boolean {
  return opts.isNonInteractiveSession
}

export const SyntheticOutputTool = buildTool({
  isMcp: false,
  isEnabled() {
    // This tool is only created when conditions are met (see main.tsx where
    // isSyntheticOutputToolEnabled() gates tool creation). Once created, always enabled.
    return true
  },
  isConcurrencySafe() {
    return true
  },
  isReadOnly() {
    return true
  },
  isOpenWorld() {
    return false
  },
  name: SYNTHETIC_OUTPUT_TOOL_NAME,
  searchHint: 'return the final response as structured JSON',
  maxResultSizeChars: 100_000,
  async description(): Promise<string> {
    return 'Return structured output in the requested format'
  },
  async prompt(): Promise<string> {

```

---


### `src/tools/TaskCreateTool/TaskCreateTool.ts`

**信息:**
- 行数: 138
- 大小: 3441 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { buildTool, type ToolDef } from '../../Tool.js'
import {
  executeTaskCreatedHooks,
  getTaskCreatedHookMessage,
} from '../../utils/hooks.js'
import { lazySchema } from '../../utils/lazySchema.js'
import {
  createTask,
  deleteTask,
  getTaskListId,
  isTodoV2Enabled,
} from '../../utils/tasks.js'
import { getAgentName, getTeamName } from '../../utils/teammate.js'
import { TASK_CREATE_TOOL_NAME } from './constants.js'
import { DESCRIPTION, getPrompt } from './prompt.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    subject: z.string().describe('A brief title for the task'),
    description: z.string().describe('What needs to be done'),
    activeForm: z
      .string()
      .optional()
      .describe(
        'Present continuous form shown in spinner when in_progress (e.g., "Running tests")',
      ),
    metadata: z
      .record(z.string(), z.unknown())
      .optional()
      .describe('Arbitrary metadata to attach to the task'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    task: z.object({
      id: z.string(),
      subject: z.string(),
    }),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>

export type Output = z.infer<OutputSchema>

export const TaskCreateTool = buildTool({
  name: TASK_CREATE_TOOL_NAME,
  searchHint: 'create a task in the task list',

```

---


### `src/tools/TaskCreateTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 50 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TASK_CREATE_TOOL_NAME = 'TaskCreate'

```

---


### `src/tools/TaskCreateTool/prompt.ts`

**信息:**
- 行数: 56
- 大小: 2760 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js'

export const DESCRIPTION = 'Create a new task in the task list'

export function getPrompt(): string {
  const teammateContext = isAgentSwarmsEnabled()
    ? ' and potentially assigned to teammates'
    : ''

  const teammateTips = isAgentSwarmsEnabled()
    ? `- Include enough detail in the description for another agent to understand and complete the task
- New tasks are created with status 'pending' and no owner - use TaskUpdate with the \`owner\` parameter to assign them
`
    : ''

  return `Use this tool to create a structured task list for your current coding session. This helps you track progress, organize complex tasks, and demonstrate thoroughness to the user.
It also helps the user understand the progress of the task and overall progress of their requests.

## When to Use This Tool

Use this tool proactively in these scenarios:

- Complex multi-step tasks - When a task requires 3 or more distinct steps or actions
- Non-trivial and complex tasks - Tasks that require careful planning or multiple operations${teammateContext}
- Plan mode - When using plan mode, create a task list to track the work
- User explicitly requests todo list - When the user directly asks you to use the todo list
- User provides multiple tasks - When users provide a list of things to be done (numbered or comma-separated)
- After receiving new instructions - Immediately capture user requirements as tasks
- When you start working on a task - Mark it as in_progress BEFORE beginning work
- After completing a task - Mark it as completed and add any new follow-up tasks discovered during implementation

## When NOT to Use This Tool

Skip using this tool when:
- There is only a single, straightforward task
- The task is trivial and tracking it provides no organizational benefit
- The task can be completed in less than 3 trivial steps
- The task is purely conversational or informational

NOTE that you should not use this tool if there is only one trivial task to do. In this case you are better off just doing the task directly.

## Task Fields

- **subject**: A brief, actionable title in imperative form (e.g., "Fix authentication bug in login flow")
- **description**: What needs to be done
- **activeForm** (optional): Present continuous form shown in the spinner when the task is in_progress (e.g., "Fixing authentication bug"). If omitted, the spinner shows the subject instead.

All tasks are created with status \`pending\`.

## Tips

```

---


### `src/tools/TaskGetTool/TaskGetTool.ts`

**信息:**
- 行数: 128
- 大小: 2881 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { buildTool, type ToolDef } from '../../Tool.js'
import { lazySchema } from '../../utils/lazySchema.js'
import {
  getTask,
  getTaskListId,
  isTodoV2Enabled,
  TaskStatusSchema,
} from '../../utils/tasks.js'
import { TASK_GET_TOOL_NAME } from './constants.js'
import { DESCRIPTION, PROMPT } from './prompt.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    taskId: z.string().describe('The ID of the task to retrieve'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    task: z
      .object({
        id: z.string(),
        subject: z.string(),
        description: z.string(),
        status: TaskStatusSchema(),
        blocks: z.array(z.string()),
        blockedBy: z.array(z.string()),
      })
      .nullable(),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>

export type Output = z.infer<OutputSchema>

export const TaskGetTool = buildTool({
  name: TASK_GET_TOOL_NAME,
  searchHint: 'retrieve a task by ID',
  maxResultSizeChars: 100_000,
  async description() {
    return DESCRIPTION
  },
  async prompt() {
    return PROMPT
  },
  get inputSchema(): InputSchema {
    return inputSchema()
  },

```

---


### `src/tools/TaskGetTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 44 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TASK_GET_TOOL_NAME = 'TaskGet'

```

---


### `src/tools/TaskGetTool/prompt.ts`

**信息:**
- 行数: 24
- 大小: 823 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const DESCRIPTION = 'Get a task by ID from the task list'

export const PROMPT = `Use this tool to retrieve a task by its ID from the task list.

## When to Use This Tool

- When you need the full description and context before starting work on a task
- To understand task dependencies (what it blocks, what blocks it)
- After being assigned a task, to get complete requirements

## Output

Returns full task details:
- **subject**: Task title
- **description**: Detailed requirements and context
- **status**: 'pending', 'in_progress', or 'completed'
- **blocks**: Tasks waiting on this one to complete
- **blockedBy**: Tasks that must complete before this one can start

## Tips

- After fetching a task, verify its blockedBy list is empty before beginning work.
- Use TaskList to see all tasks in summary form.
`

```

---


### `src/tools/TaskListTool/TaskListTool.ts`

**信息:**
- 行数: 116
- 大小: 2803 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { buildTool, type ToolDef } from '../../Tool.js'
import { lazySchema } from '../../utils/lazySchema.js'
import {
  getTaskListId,
  isTodoV2Enabled,
  listTasks,
  TaskStatusSchema,
} from '../../utils/tasks.js'
import { TASK_LIST_TOOL_NAME } from './constants.js'
import { DESCRIPTION, getPrompt } from './prompt.js'

const inputSchema = lazySchema(() => z.strictObject({}))
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    tasks: z.array(
      z.object({
        id: z.string(),
        subject: z.string(),
        status: TaskStatusSchema(),
        owner: z.string().optional(),
        blockedBy: z.array(z.string()),
      }),
    ),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>

export type Output = z.infer<OutputSchema>

export const TaskListTool = buildTool({
  name: TASK_LIST_TOOL_NAME,
  searchHint: 'list all tasks',
  maxResultSizeChars: 100_000,
  async description() {
    return DESCRIPTION
  },
  async prompt() {
    return getPrompt()
  },
  get inputSchema(): InputSchema {
    return inputSchema()
  },
  get outputSchema(): OutputSchema {
    return outputSchema()
  },
  userFacingName() {
    return 'TaskList'

```

---


### `src/tools/TaskListTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 46 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TASK_LIST_TOOL_NAME = 'TaskList'

```

---


### `src/tools/TaskListTool/prompt.ts`

**信息:**
- 行数: 49
- 大小: 2066 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js'

export const DESCRIPTION = 'List all tasks in the task list'

export function getPrompt(): string {
  const teammateUseCase = isAgentSwarmsEnabled()
    ? `- Before assigning tasks to teammates, to see what's available
`
    : ''

  const idDescription = isAgentSwarmsEnabled()
    ? '- **id**: Task identifier (use with TaskGet, TaskUpdate)'
    : '- **id**: Task identifier (use with TaskGet, TaskUpdate)'

  const teammateWorkflow = isAgentSwarmsEnabled()
    ? `
## Teammate Workflow

When working as a teammate:
1. After completing your current task, call TaskList to find available work
2. Look for tasks with status 'pending', no owner, and empty blockedBy
3. **Prefer tasks in ID order** (lowest ID first) when multiple tasks are available, as earlier tasks often set up context for later ones
4. Claim an available task using TaskUpdate (set \`owner\` to your name), or wait for leader assignment
5. If blocked, focus on unblocking tasks or notify the team lead
`
    : ''

  return `Use this tool to list all tasks in the task list.

## When to Use This Tool

- To see what tasks are available to work on (status: 'pending', no owner, not blocked)
- To check overall progress on the project
- To find tasks that are blocked and need dependencies resolved
${teammateUseCase}- After completing a task, to check for newly unblocked work or claim the next available task
- **Prefer working on tasks in ID order** (lowest ID first) when multiple tasks are available, as earlier tasks often set up context for later ones

## Output

Returns a summary of each task:
${idDescription}
- **subject**: Brief description of the task
- **status**: 'pending', 'in_progress', or 'completed'
- **owner**: Agent ID if assigned, empty if available
- **blockedBy**: List of open task IDs that must be resolved first (tasks with blockedBy cannot be claimed until dependencies resolve)

Use TaskGet with a specific task ID to view full details including description and comments.
${teammateWorkflow}`
}

```

---


### `src/tools/TaskOutputTool/TaskOutputTool.tsx`

**信息:**
- 行数: 584
- 大小: 66568 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import { z } from 'zod/v4';
import { FallbackToolUseErrorMessage } from '../../components/FallbackToolUseErrorMessage.js';
import { FallbackToolUseRejectedMessage } from '../../components/FallbackToolUseRejectedMessage.js';
import { MessageResponse } from '../../components/MessageResponse.js';
import { Box, Text } from '../../ink.js';
import { useShortcutDisplay } from '../../keybindings/useShortcutDisplay.js';
import type { TaskType } from '../../Task.js';
import type { Tool } from '../../Tool.js';
import { buildTool, type ToolDef } from '../../Tool.js';
import type { LocalAgentTaskState } from '../../tasks/LocalAgentTask/LocalAgentTask.js';
import type { LocalShellTaskState } from '../../tasks/LocalShellTask/guards.js';
import type { RemoteAgentTaskState } from '../../tasks/RemoteAgentTask/RemoteAgentTask.js';
import type { TaskState } from '../../tasks/types.js';
import { AbortError } from '../../utils/errors.js';
import { lazySchema } from '../../utils/lazySchema.js';
import { extractTextContent } from '../../utils/messages.js';
import { semanticBoolean } from '../../utils/semanticBoolean.js';
import { sleep } from '../../utils/sleep.js';
import { jsonParse } from '../../utils/slowOperations.js';
import { countCharInString } from '../../utils/stringUtils.js';
import { getTaskOutput } from '../../utils/task/diskOutput.js';
import { updateTaskState } from '../../utils/task/framework.js';
import { formatTaskOutput } from '../../utils/task/outputFormatting.js';
import type { ThemeName } from '../../utils/theme.js';
import { AgentPromptDisplay, AgentResponseDisplay } from '../AgentTool/UI.js';
import BashToolResultMessage from '../BashTool/BashToolResultMessage.js';
import { TASK_OUTPUT_TOOL_NAME } from './constants.js';
const inputSchema = lazySchema(() => z.strictObject({
  task_id: z.string().describe('The task ID to get output from'),
  block: semanticBoolean(z.boolean().default(true)).describe('Whether to wait for completion'),
  timeout: z.number().min(0).max(600000).default(30000).describe('Max wait time in ms')
}));
type InputSchema = ReturnType<typeof inputSchema>;
type TaskOutputToolInput = z.infer<InputSchema>;

// Unified output type covering all task types
type TaskOutput = {
  task_id: string;
  task_type: TaskType;
  status: string;
  description: string;
  output: string;
  exitCode?: number | null;
  error?: string;
  // For agents
  prompt?: string;
  result?: string;
};

```

---


### `src/tools/TaskOutputTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 50 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TASK_OUTPUT_TOOL_NAME = 'TaskOutput'

```

---


### `src/tools/TaskStopTool/TaskStopTool.ts`

**信息:**
- 行数: 131
- 大小: 3935 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import type { TaskStateBase } from '../../Task.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { stopTask } from '../../tasks/stopTask.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { DESCRIPTION, TASK_STOP_TOOL_NAME } from './prompt.js'
import { renderToolResultMessage, renderToolUseMessage } from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    task_id: z
      .string()
      .optional()
      .describe('The ID of the background task to stop'),
    // shell_id is accepted for backward compatibility with the deprecated KillShell tool
    shell_id: z.string().optional().describe('Deprecated: use task_id instead'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    message: z.string().describe('Status message about the operation'),
    task_id: z.string().describe('The ID of the task that was stopped'),
    task_type: z.string().describe('The type of the task that was stopped'),
    // Optional: tool outputs are persisted to transcripts and replayed on --resume
    // without re-validation, so sessions from before this field was added lack it.
    command: z
      .string()
      .optional()
      .describe('The command or description of the stopped task'),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>

export type Output = z.infer<OutputSchema>

export const TaskStopTool = buildTool({
  name: TASK_STOP_TOOL_NAME,
  searchHint: 'kill a running background task',
  // KillShell is the deprecated name - kept as alias for backward compatibility
  // with existing transcripts and SDK users
  aliases: ['KillShell'],
  maxResultSizeChars: 100_000,
  userFacingName: () => (process.env.USER_TYPE === 'ant' ? '' : 'Stop Task'),
  get inputSchema(): InputSchema {
    return inputSchema()
  },
  get outputSchema(): OutputSchema {

```

---


### `src/tools/TaskStopTool/UI.tsx`

**信息:**
- 行数: 41
- 大小: 5672 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { MessageResponse } from '../../components/MessageResponse.js';
import { stringWidth } from '../../ink/stringWidth.js';
import { Text } from '../../ink.js';
import { truncateToWidthNoEllipsis } from '../../utils/format.js';
import type { Output } from './TaskStopTool.js';
export function renderToolUseMessage(): React.ReactNode {
  return '';
}
const MAX_COMMAND_DISPLAY_LINES = 2;
const MAX_COMMAND_DISPLAY_CHARS = 160;
function truncateCommand(command: string): string {
  const lines = command.split('\n');
  let truncated = command;
  if (lines.length > MAX_COMMAND_DISPLAY_LINES) {
    truncated = lines.slice(0, MAX_COMMAND_DISPLAY_LINES).join('\n');
  }
  if (stringWidth(truncated) > MAX_COMMAND_DISPLAY_CHARS) {
    truncated = truncateToWidthNoEllipsis(truncated, MAX_COMMAND_DISPLAY_CHARS);
  }
  return truncated.trim();
}
export function renderToolResultMessage(output: Output, _progressMessagesForMessage: unknown[], {
  verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  if ("external" === 'ant') {
    return null;
  }
  const rawCommand = output.command ?? '';
  const command = verbose ? rawCommand : truncateCommand(rawCommand);
  const suffix = command !== rawCommand ? '… · stopped' : ' · stopped';
  return <MessageResponse>
      <Text>
        {command}
        {suffix}
      </Text>
    </MessageResponse>;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIk1lc3NhZ2VSZXNwb25zZSIsInN0cmluZ1dpZHRoIiwiVGV4dCIsInRydW5jYXRlVG9XaWR0aE5vRWxsaXBzaXMiLCJPdXRwdXQiLCJyZW5kZXJUb29sVXNlTWVzc2FnZSIsIlJlYWN0Tm9kZSIsIk1BWF9DT01NQU5EX0RJU1BMQVlfTElORVMiLCJNQVhfQ09NTUFORF9ESVNQTEFZX0NIQVJTIiwidHJ1bmNhdGVDb21tYW5kIiwiY29tbWFuZCIsImxpbmVzIiwic3BsaXQiLCJ0cnVuY2F0ZWQiLCJsZW5ndGgiLCJzbGljZSIsImpvaW4iLCJ0cmltIiwicmVuZGVyVG9vbFJlc3VsdE1lc3NhZ2UiLCJvdXRwdXQiLCJfcHJvZ3Jlc3NNZXNzYWdlc0Zvck1lc3NhZ2UiLCJ2ZXJib3NlIiwicmF3Q29tbWFuZCIsInN1ZmZpeCJdLCJzb3VyY2VzIjpbIlVJLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBNZXNzYWdlUmVzcG9uc2UgfSBmcm9tICcuLi8uLi9jb21wb25lbnRzL01lc3NhZ2VSZXNwb25zZS5qcydcbmltcG9ydCB7IHN0cmluZ1dpZHRoIH0gZnJvbSAnLi4vLi4vaW5rL3N0cmluZ1dpZHRoLmpzJ1xuaW1wb3J0IHsgVGV4dCB9IGZyb20gJy4uLy4uL2luay5qcydcbmltcG9ydCB7IHRydW5jYXRlVG9XaWR0aE5vRWxsaXBzaXMgfSBmcm9tICcuLi8uLi91dGlscy9mb3JtYXQuanMnXG5pbXBvcnQgdHlwZSB7IE91dHB1dCB9IGZyb20gJy4vVGFza1N0b3BUb29sLmpzJ1xuXG5leHBvcnQgZnVuY3Rpb24gcmVuZGVyVG9vbFVzZU1lc3NhZ2UoKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgcmV0dXJuICcnXG59XG5cbmNvbnN0IE1BWF9DT01NQU5EX0RJU1BMQVlfTElORVMgPSAyXG5jb25zdCBNQVhfQ09NTUFORF9ESVNQTEFZX0NIQVJTID0gMTYwXG5cbmZ1bmN0aW9uIHRydW5jYXRlQ29tbWFuZChjb21tYW5kOiBzdHJpbmcpOiBzdHJpbmcge1xuICBjb25zdCBsaW5lcyA9IGNvbW1hbmQuc3BsaXQoJ1xcbicpXG4gIGxldCB0cnVuY2F0ZWQgPSBjb21tYW5kXG5cbiAgaWYgKGxpbmVzLmxlbmd0aCA+IE1BWF9DT01NQU5EX0RJU1BMQVlfTElORVMpIHtcbiAgICB0cnVuY2F0ZWQgPSBsaW5lcy5zbGljZSgwLCBNQVhfQ09NTUFORF9ESVNQTEFZX0xJTkVTKS5qb2luKCdcXG4nKVxuICB9XG5cbiAgaWYgKHN0cmluZ1dpZHRoKHRydW5jYXRlZCkgPiBNQVhfQ09NTUFORF9ESVNQTEFZX0NIQVJTKSB7XG4gICAgdHJ1bmNhdGVkID0gdHJ1bmNhdGVUb1dpZHRoTm9FbGxpcHNpcyh0cnVuY2F0ZWQsIE1BWF9DT01NQU5EX0RJU1BMQVlfQ0hBUlMpXG4gIH1cblxuICByZXR1cm4gdHJ1bmNhdGVkLnRyaW0oKVxufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVuZGVyVG9vbFJlc3VsdE1lc3NhZ2UoXG4gIG91dHB1dDogT3V0cHV0LFxuICBfcHJvZ3Jlc3NNZXNzYWdlc0Zvck1lc3NhZ2U6IHVua25vd25bXSxcbiAgeyB2ZXJib3NlIH06IHsgdmVyYm9zZTogYm9vbGVhbiB9LFxuKTogUmVhY3QuUmVhY3ROb2RlIHtcbiAgaWYgKFwiZXh0ZXJuYWxcIiA9PT0gJ2FudCcpIHtcbiAgICByZXR1cm4gbnVsbFxuICB9XG5cbiAgY29uc3QgcmF3Q29tbWFuZCA9IG91dHB1dC5jb21tYW5kID8/ICcnXG4gIGNvbnN0IGNvbW1hbmQgPSB2ZXJib3NlID8gcmF3Q29tbWFuZCA6IHRydW5jYXRlQ29tbWFuZChyYXdDb21tYW5kKVxuICBjb25zdCBzdWZmaXggPSBjb21tYW5kICE9PSByYXdDb21tYW5kID8gJ+KApiDCtyBzdG9wcGVkJyA6ICcgwrcgc3RvcHBlZCdcblxuICByZXR1cm4gKFxuICAgIDxNZXNzYWdlUmVzcG9uc2U+XG4gICAgICA8VGV4dD5cbiAgICAgICAge2NvbW1hbmR9XG4gICAgICAgIHtzdWZmaXh9XG4gICAgICA8L1RleHQ+XG4gICAgPC9NZXNzYWdlUmVzcG9uc2U+XG4gIClcbn1cbiJdLCJtYXBwaW5ncyI6IkFBQUEsT0FBT0EsS0FBSyxNQUFNLE9BQU87QUFDekIsU0FBU0MsZUFBZSxRQUFRLHFDQUFxQztBQUNyRSxTQUFTQyxXQUFXLFFBQVEsMEJBQTBCO0FBQ3RELFNBQVNDLElBQUksUUFBUSxjQUFjO0FBQ25DLFNBQVNDLHlCQUF5QixRQUFRLHVCQUF1QjtBQUNqRSxjQUFjQyxNQUFNLFFBQVEsbUJBQW1CO0FBRS9DLE9BQU8sU0FBU0Msb0JBQW9CQSxDQUFBLENBQUUsRUFBRU4sS0FBSyxDQUFDTyxTQUFTLENBQUM7RUFDdEQsT0FBTyxFQUFFO0FBQ1g7QUFFQSxNQUFNQyx5QkFBeUIsR0FBRyxDQUFDO0FBQ25DLE1BQU1DLHlCQUF5QixHQUFHLEdBQUc7QUFFckMsU0FBU0MsZUFBZUEsQ0FBQ0MsT0FBTyxFQUFFLE1BQU0sQ0FBQyxFQUFFLE1BQU0sQ0FBQztFQUNoRCxNQUFNQyxLQUFLLEdBQUdELE9BQU8sQ0FBQ0UsS0FBSyxDQUFDLElBQUksQ0FBQztFQUNqQyxJQUFJQyxTQUFTLEdBQUdILE9BQU87RUFFdkIsSUFBSUMsS0FBSyxDQUFDRyxNQUFNLEdBQUdQLHlCQUF5QixFQUFFO0lBQzVDTSxTQUFTLEdBQUdGLEtBQUssQ0FBQ0ksS0FBSyxDQUFDLENBQUMsRUFBRVIseUJBQXlCLENBQUMsQ0FBQ1MsSUFBSSxDQUFDLElBQUksQ0FBQztFQUNsRTtFQUVBLElBQUlmLFdBQVcsQ0FBQ1ksU0FBUyxDQUFDLEdBQUdMLHlCQUF5QixFQUFFO0lBQ3RESyxTQUFTLEdBQUdWLHlCQUF5QixDQUFDVSxTQUFTLEVBQUVMLHlCQUF5QixDQUFDO0VBQzdFO0VBRUEsT0FBT0ssU0FBUyxDQUFDSSxJQUFJLENBQUMsQ0FBQztBQUN6QjtBQUVBLE9BQU8sU0FBU0MsdUJBQXVCQSxDQUNyQ0MsTUFBTSxFQUFFZixNQUFNLEVBQ2RnQiwyQkFBMkIsRUFBRSxPQUFPLEVBQUUsRUFDdEM7RUFBRUM7QUFBOEIsQ0FBckIsRUFBRTtFQUFFQSxPQUFPLEVBQUUsT0FBTztBQUFDLENBQUMsQ0FDbEMsRUFBRXRCLEtBQUssQ0FBQ08sU0FBUyxDQUFDO0VBQ2pCLElBQUksVUFBVSxLQUFLLEtBQUssRUFBRTtJQUN4QixPQUFPLElBQUk7RUFDYjtFQUVBLE1BQU1nQixVQUFVLEdBQUdILE1BQU0sQ0FBQ1QsT0FBTyxJQUFJLEVBQUU7RUFDdkMsTUFBTUEsT0FBTyxHQUFHVyxPQUFPLEdBQUdDLFVBQVUsR0FBR2IsZUFBZSxDQUFDYSxVQUFVLENBQUM7RUFDbEUsTUFBTUMsTUFBTSxHQUFHYixPQUFPLEtBQUtZLFVBQVUsR0FBRyxhQUFhLEdBQUcsWUFBWTtFQUVwRSxPQUNFLENBQUMsZUFBZTtBQUNwQixNQUFNLENBQUMsSUFBSTtBQUNYLFFBQVEsQ0FBQ1osT0FBTztBQUNoQixRQUFRLENBQUNhLE1BQU07QUFDZixNQUFNLEVBQUUsSUFBSTtBQUNaLElBQUksRUFBRSxlQUFlLENBQUM7QUFFdEIiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/tools/TaskStopTool/prompt.ts`

**信息:**
- 行数: 8
- 大小: 280 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TASK_STOP_TOOL_NAME = 'TaskStop'

export const DESCRIPTION = `
- Stops a running background task by its ID
- Takes a task_id parameter identifying the task to stop
- Returns a success or failure status
- Use this tool when you need to terminate a long-running task
`

```

---


### `src/tools/TaskUpdateTool/TaskUpdateTool.ts`

**信息:**
- 行数: 406
- 大小: 12161 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { z } from 'zod/v4'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js'
import {
  executeTaskCompletedHooks,
  getTaskCompletedHookMessage,
} from '../../utils/hooks.js'
import { lazySchema } from '../../utils/lazySchema.js'
import {
  blockTask,
  deleteTask,
  getTask,
  getTaskListId,
  isTodoV2Enabled,
  listTasks,
  type TaskStatus,
  TaskStatusSchema,
  updateTask,
} from '../../utils/tasks.js'
import {
  getAgentId,
  getAgentName,
  getTeammateColor,
  getTeamName,
} from '../../utils/teammate.js'
import { writeToMailbox } from '../../utils/teammateMailbox.js'
import { VERIFICATION_AGENT_TYPE } from '../AgentTool/constants.js'
import { TASK_UPDATE_TOOL_NAME } from './constants.js'
import { DESCRIPTION, PROMPT } from './prompt.js'

const inputSchema = lazySchema(() => {
  // Extended status schema that includes 'deleted' as a special action
  const TaskUpdateStatusSchema = TaskStatusSchema().or(z.literal('deleted'))

  return z.strictObject({
    taskId: z.string().describe('The ID of the task to update'),
    subject: z.string().optional().describe('New subject for the task'),
    description: z.string().optional().describe('New description for the task'),
    activeForm: z
      .string()
      .optional()
      .describe(
        'Present continuous form shown in spinner when in_progress (e.g., "Running tests")',
      ),
    status: TaskUpdateStatusSchema.optional().describe(
      'New status for the task',
    ),
    addBlocks: z

```

---


### `src/tools/TaskUpdateTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 50 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TASK_UPDATE_TOOL_NAME = 'TaskUpdate'

```

---


### `src/tools/TaskUpdateTool/prompt.ts`

**信息:**
- 行数: 77
- 大小: 2375 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const DESCRIPTION = 'Update a task in the task list'

export const PROMPT = `Use this tool to update a task in the task list.

## When to Use This Tool

**Mark tasks as resolved:**
- When you have completed the work described in a task
- When a task is no longer needed or has been superseded
- IMPORTANT: Always mark your assigned tasks as resolved when you finish them
- After resolving, call TaskList to find your next task

- ONLY mark a task as completed when you have FULLY accomplished it
- If you encounter errors, blockers, or cannot finish, keep the task as in_progress
- When blocked, create a new task describing what needs to be resolved
- Never mark a task as completed if:
  - Tests are failing
  - Implementation is partial
  - You encountered unresolved errors
  - You couldn't find necessary files or dependencies

**Delete tasks:**
- When a task is no longer relevant or was created in error
- Setting status to \`deleted\` permanently removes the task

**Update task details:**
- When requirements change or become clearer
- When establishing dependencies between tasks

## Fields You Can Update

- **status**: The task status (see Status Workflow below)
- **subject**: Change the task title (imperative form, e.g., "Run tests")
- **description**: Change the task description
- **activeForm**: Present continuous form shown in spinner when in_progress (e.g., "Running tests")
- **owner**: Change the task owner (agent name)
- **metadata**: Merge metadata keys into the task (set a key to null to delete it)
- **addBlocks**: Mark tasks that cannot start until this one completes
- **addBlockedBy**: Mark tasks that must complete before this one can start

## Status Workflow

Status progresses: \`pending\` → \`in_progress\` → \`completed\`

Use \`deleted\` to permanently remove a task.

## Staleness

Make sure to read a task's latest state using \`TaskGet\` before updating it.


```

---


### `src/tools/TeamCreateTool/TeamCreateTool.ts`

**信息:**
- 行数: 240
- 大小: 7665 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { getSessionId } from '../../bootstrap/state.js'
import { logEvent } from '../../services/analytics/index.js'
import type { AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS } from '../../services/analytics/metadata.js'
import type { Tool } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { formatAgentId } from '../../utils/agentId.js'
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js'
import { getCwd } from '../../utils/cwd.js'
import { lazySchema } from '../../utils/lazySchema.js'
import {
  getDefaultMainLoopModel,
  parseUserSpecifiedModel,
} from '../../utils/model/model.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { getResolvedTeammateMode } from '../../utils/swarm/backends/registry.js'
import { TEAM_LEAD_NAME } from '../../utils/swarm/constants.js'
import type { TeamFile } from '../../utils/swarm/teamHelpers.js'
import {
  getTeamFilePath,
  readTeamFile,
  registerTeamForSessionCleanup,
  sanitizeName,
  writeTeamFileAsync,
} from '../../utils/swarm/teamHelpers.js'
import { assignTeammateColor } from '../../utils/swarm/teammateLayoutManager.js'
import {
  ensureTasksDir,
  resetTaskList,
  setLeaderTeamName,
} from '../../utils/tasks.js'
import { generateWordSlug } from '../../utils/words.js'
import { TEAM_CREATE_TOOL_NAME } from './constants.js'
import { getPrompt } from './prompt.js'
import { renderToolUseMessage } from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    team_name: z.string().describe('Name for the new team to create.'),
    description: z.string().optional().describe('Team description/purpose.'),
    agent_type: z
      .string()
      .optional()
      .describe(
        'Type/role of the team lead (e.g., "researcher", "test-runner"). ' +
          'Used for team file and inter-agent coordination.',
      ),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

```

---


### `src/tools/TeamCreateTool/UI.tsx`

**信息:**
- 行数: 6
- 大小: 1038 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import type { Input } from './TeamCreateTool.js';
export function renderToolUseMessage(input: Partial<Input>): React.ReactNode {
  return `create team: ${input.team_name}`;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIklucHV0IiwicmVuZGVyVG9vbFVzZU1lc3NhZ2UiLCJpbnB1dCIsIlBhcnRpYWwiLCJSZWFjdE5vZGUiLCJ0ZWFtX25hbWUiXSwic291cmNlcyI6WyJVSS50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHR5cGUgeyBJbnB1dCB9IGZyb20gJy4vVGVhbUNyZWF0ZVRvb2wuanMnXG5cbmV4cG9ydCBmdW5jdGlvbiByZW5kZXJUb29sVXNlTWVzc2FnZShpbnB1dDogUGFydGlhbDxJbnB1dD4pOiBSZWFjdC5SZWFjdE5vZGUge1xuICByZXR1cm4gYGNyZWF0ZSB0ZWFtOiAke2lucHV0LnRlYW1fbmFtZX1gXG59XG4iXSwibWFwcGluZ3MiOiJBQUFBLE9BQU9BLEtBQUssTUFBTSxPQUFPO0FBQ3pCLGNBQWNDLEtBQUssUUFBUSxxQkFBcUI7QUFFaEQsT0FBTyxTQUFTQyxvQkFBb0JBLENBQUNDLEtBQUssRUFBRUMsT0FBTyxDQUFDSCxLQUFLLENBQUMsQ0FBQyxFQUFFRCxLQUFLLENBQUNLLFNBQVMsQ0FBQztFQUMzRSxPQUFPLGdCQUFnQkYsS0FBSyxDQUFDRyxTQUFTLEVBQUU7QUFDMUMiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/tools/TeamCreateTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 50 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TEAM_CREATE_TOOL_NAME = 'TeamCreate'

```

---


### `src/tools/TeamCreateTool/prompt.ts`

**信息:**
- 行数: 113
- 大小: 6900 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function getPrompt(): string {
  return `
# TeamCreate

## When to Use

Use this tool proactively whenever:
- The user explicitly asks to use a team, swarm, or group of agents
- The user mentions wanting agents to work together, coordinate, or collaborate
- A task is complex enough that it would benefit from parallel work by multiple agents (e.g., building a full-stack feature with frontend and backend work, refactoring a codebase while keeping tests passing, implementing a multi-step project with research, planning, and coding phases)

When in doubt about whether a task warrants a team, prefer spawning a team.

## Choosing Agent Types for Teammates

When spawning teammates via the Agent tool, choose the \`subagent_type\` based on what tools the agent needs for its task. Each agent type has a different set of available tools — match the agent to the work:

- **Read-only agents** (e.g., Explore, Plan) cannot edit or write files. Only assign them research, search, or planning tasks. Never assign them implementation work.
- **Full-capability agents** (e.g., general-purpose) have access to all tools including file editing, writing, and bash. Use these for tasks that require making changes.
- **Custom agents** defined in \`.claude/agents/\` may have their own tool restrictions. Check their descriptions to understand what they can and cannot do.

Always review the agent type descriptions and their available tools listed in the Agent tool prompt before selecting a \`subagent_type\` for a teammate.

Create a new team to coordinate multiple agents working on a project. Teams have a 1:1 correspondence with task lists (Team = TaskList).

\`\`\`
{
  "team_name": "my-project",
  "description": "Working on feature X"
}
\`\`\`

This creates:
- A team file at \`~/.claude/teams/{team-name}/config.json\`
- A corresponding task list directory at \`~/.claude/tasks/{team-name}/\`

## Team Workflow

1. **Create a team** with TeamCreate - this creates both the team and its task list
2. **Create tasks** using the Task tools (TaskCreate, TaskList, etc.) - they automatically use the team's task list
3. **Spawn teammates** using the Agent tool with \`team_name\` and \`name\` parameters to create teammates that join the team
4. **Assign tasks** using TaskUpdate with \`owner\` to give tasks to idle teammates
5. **Teammates work on assigned tasks** and mark them completed via TaskUpdate
6. **Teammates go idle between turns** - after each turn, teammates automatically go idle and send a notification. IMPORTANT: Be patient with idle teammates! Don't comment on their idleness until it actually impacts your work.
7. **Shutdown your team** - when the task is completed, gracefully shut down your teammates via SendMessage with \`message: {type: "shutdown_request"}\`.

## Task Ownership

Tasks are assigned using TaskUpdate with the \`owner\` parameter. Any agent can set or change task ownership via TaskUpdate.


```

---


### `src/tools/TeamDeleteTool/TeamDeleteTool.ts`

**信息:**
- 行数: 139
- 大小: 4221 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { logEvent } from '../../services/analytics/index.js'
import type { AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS } from '../../services/analytics/metadata.js'
import type { Tool } from '../../Tool.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { isAgentSwarmsEnabled } from '../../utils/agentSwarmsEnabled.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { TEAM_LEAD_NAME } from '../../utils/swarm/constants.js'
import {
  cleanupTeamDirectories,
  readTeamFile,
  unregisterTeamForSessionCleanup,
} from '../../utils/swarm/teamHelpers.js'
import { clearTeammateColors } from '../../utils/swarm/teammateLayoutManager.js'
import { clearLeaderTeamName } from '../../utils/tasks.js'
import { TEAM_DELETE_TOOL_NAME } from './constants.js'
import { getPrompt } from './prompt.js'
import { renderToolResultMessage, renderToolUseMessage } from './UI.js'

const inputSchema = lazySchema(() => z.strictObject({}))
type InputSchema = ReturnType<typeof inputSchema>

export type Output = {
  success: boolean
  message: string
  team_name?: string
}

export type Input = z.infer<InputSchema>

export const TeamDeleteTool: Tool<InputSchema, Output> = buildTool({
  name: TEAM_DELETE_TOOL_NAME,
  searchHint: 'disband a swarm team and clean up',
  maxResultSizeChars: 100_000,
  shouldDefer: true,

  userFacingName() {
    return ''
  },

  get inputSchema(): InputSchema {
    return inputSchema()
  },

  isEnabled() {
    return isAgentSwarmsEnabled()
  },

  async description() {

```

---


### `src/tools/TeamDeleteTool/UI.tsx`

**信息:**
- 行数: 20
- 大小: 2906 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { jsonParse } from '../../utils/slowOperations.js';
import type { Output } from './TeamDeleteTool.js';
export function renderToolUseMessage(_input: Record<string, unknown>): React.ReactNode {
  return 'cleanup team: current';
}
export function renderToolResultMessage(content: Output | string, _progressMessages: unknown, {
  verbose: _verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  const result: Output = typeof content === 'string' ? jsonParse(content) : content;

  // Suppress cleanup result - the batched shutdown message covers this
  if ('success' in result && 'team_name' in result && 'message' in result) {
    return null;
  }
  return null;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsImpzb25QYXJzZSIsIk91dHB1dCIsInJlbmRlclRvb2xVc2VNZXNzYWdlIiwiX2lucHV0IiwiUmVjb3JkIiwiUmVhY3ROb2RlIiwicmVuZGVyVG9vbFJlc3VsdE1lc3NhZ2UiLCJjb250ZW50IiwiX3Byb2dyZXNzTWVzc2FnZXMiLCJ2ZXJib3NlIiwiX3ZlcmJvc2UiLCJyZXN1bHQiXSwic291cmNlcyI6WyJVSS50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHsganNvblBhcnNlIH0gZnJvbSAnLi4vLi4vdXRpbHMvc2xvd09wZXJhdGlvbnMuanMnXG5pbXBvcnQgdHlwZSB7IE91dHB1dCB9IGZyb20gJy4vVGVhbURlbGV0ZVRvb2wuanMnXG5cbmV4cG9ydCBmdW5jdGlvbiByZW5kZXJUb29sVXNlTWVzc2FnZShcbiAgX2lucHV0OiBSZWNvcmQ8c3RyaW5nLCB1bmtub3duPixcbik6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIHJldHVybiAnY2xlYW51cCB0ZWFtOiBjdXJyZW50J1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcmVuZGVyVG9vbFJlc3VsdE1lc3NhZ2UoXG4gIGNvbnRlbnQ6IE91dHB1dCB8IHN0cmluZyxcbiAgX3Byb2dyZXNzTWVzc2FnZXM6IHVua25vd24sXG4gIHsgdmVyYm9zZTogX3ZlcmJvc2UgfTogeyB2ZXJib3NlOiBib29sZWFuIH0sXG4pOiBSZWFjdC5SZWFjdE5vZGUge1xuICBjb25zdCByZXN1bHQ6IE91dHB1dCA9XG4gICAgdHlwZW9mIGNvbnRlbnQgPT09ICdzdHJpbmcnID8ganNvblBhcnNlKGNvbnRlbnQpIDogY29udGVudFxuXG4gIC8vIFN1cHByZXNzIGNsZWFudXAgcmVzdWx0IC0gdGhlIGJhdGNoZWQgc2h1dGRvd24gbWVzc2FnZSBjb3ZlcnMgdGhpc1xuICBpZiAoJ3N1Y2Nlc3MnIGluIHJlc3VsdCAmJiAndGVhbV9uYW1lJyBpbiByZXN1bHQgJiYgJ21lc3NhZ2UnIGluIHJlc3VsdCkge1xuICAgIHJldHVybiBudWxsXG4gIH1cblxuICByZXR1cm4gbnVsbFxufVxuIl0sIm1hcHBpbmdzIjoiQUFBQSxPQUFPQSxLQUFLLE1BQU0sT0FBTztBQUN6QixTQUFTQyxTQUFTLFFBQVEsK0JBQStCO0FBQ3pELGNBQWNDLE1BQU0sUUFBUSxxQkFBcUI7QUFFakQsT0FBTyxTQUFTQyxvQkFBb0JBLENBQ2xDQyxNQUFNLEVBQUVDLE1BQU0sQ0FBQyxNQUFNLEVBQUUsT0FBTyxDQUFDLENBQ2hDLEVBQUVMLEtBQUssQ0FBQ00sU0FBUyxDQUFDO0VBQ2pCLE9BQU8sdUJBQXVCO0FBQ2hDO0FBRUEsT0FBTyxTQUFTQyx1QkFBdUJBLENBQ3JDQyxPQUFPLEVBQUVOLE1BQU0sR0FBRyxNQUFNLEVBQ3hCTyxpQkFBaUIsRUFBRSxPQUFPLEVBQzFCO0VBQUVDLE9BQU8sRUFBRUM7QUFBK0IsQ0FBckIsRUFBRTtFQUFFRCxPQUFPLEVBQUUsT0FBTztBQUFDLENBQUMsQ0FDNUMsRUFBRVYsS0FBSyxDQUFDTSxTQUFTLENBQUM7RUFDakIsTUFBTU0sTUFBTSxFQUFFVixNQUFNLEdBQ2xCLE9BQU9NLE9BQU8sS0FBSyxRQUFRLEdBQUdQLFNBQVMsQ0FBQ08sT0FBTyxDQUFDLEdBQUdBLE9BQU87O0VBRTVEO0VBQ0EsSUFBSSxTQUFTLElBQUlJLE1BQU0sSUFBSSxXQUFXLElBQUlBLE1BQU0sSUFBSSxTQUFTLElBQUlBLE1BQU0sRUFBRTtJQUN2RSxPQUFPLElBQUk7RUFDYjtFQUVBLE9BQU8sSUFBSTtBQUNiIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/tools/TeamDeleteTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 50 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TEAM_DELETE_TOOL_NAME = 'TeamDelete'

```

---


### `src/tools/TeamDeleteTool/prompt.ts`

**信息:**
- 行数: 16
- 大小: 684 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function getPrompt(): string {
  return `
# TeamDelete

Remove team and task directories when the swarm work is complete.

This operation:
- Removes the team directory (\`~/.claude/teams/{team-name}/\`)
- Removes the task directory (\`~/.claude/tasks/{team-name}/\`)
- Clears team context from the current session

**IMPORTANT**: TeamDelete will fail if the team still has active members. Gracefully terminate teammates first, then call TeamDelete after all teammates have shut down.

Use this when all teammates have finished their work and you want to clean up the team resources. The team name is automatically determined from the current session's team context.
`.trim()
}

```

---


### `src/tools/TerminalCaptureTool/prompt.ts`

**信息:**
- 行数: 1
- 大小: 61 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TERMINAL_CAPTURE_TOOL_NAME = 'terminal_capture'

```

---


### `src/tools/TodoWriteTool/TodoWriteTool.ts`

**信息:**
- 行数: 115
- 大小: 3881 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { z } from 'zod/v4'
import { getSessionId } from '../../bootstrap/state.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { isTodoV2Enabled } from '../../utils/tasks.js'
import { TodoListSchema } from '../../utils/todo/types.js'
import { VERIFICATION_AGENT_TYPE } from '../AgentTool/constants.js'
import { TODO_WRITE_TOOL_NAME } from './constants.js'
import { DESCRIPTION, PROMPT } from './prompt.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    todos: TodoListSchema().describe('The updated todo list'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    oldTodos: TodoListSchema().describe('The todo list before the update'),
    newTodos: TodoListSchema().describe('The todo list after the update'),
    verificationNudgeNeeded: z.boolean().optional(),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>

export type Output = z.infer<OutputSchema>

export const TodoWriteTool = buildTool({
  name: TODO_WRITE_TOOL_NAME,
  searchHint: 'manage the session task checklist',
  maxResultSizeChars: 100_000,
  strict: true,
  async description() {
    return DESCRIPTION
  },
  async prompt() {
    return PROMPT
  },
  get inputSchema(): InputSchema {
    return inputSchema()
  },
  get outputSchema(): OutputSchema {
    return outputSchema()
  },
  userFacingName() {
    return ''
  },

```

---


### `src/tools/TodoWriteTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 48 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TODO_WRITE_TOOL_NAME = 'TodoWrite'

```

---


### `src/tools/TodoWriteTool/prompt.ts`

**信息:**
- 行数: 184
- 大小: 9527 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { FILE_EDIT_TOOL_NAME } from '../FileEditTool/constants.js'

export const PROMPT = `Use this tool to create and manage a structured task list for your current coding session. This helps you track progress, organize complex tasks, and demonstrate thoroughness to the user.
It also helps the user understand the progress of the task and overall progress of their requests.

## When to Use This Tool
Use this tool proactively in these scenarios:

1. Complex multi-step tasks - When a task requires 3 or more distinct steps or actions
2. Non-trivial and complex tasks - Tasks that require careful planning or multiple operations
3. User explicitly requests todo list - When the user directly asks you to use the todo list
4. User provides multiple tasks - When users provide a list of things to be done (numbered or comma-separated)
5. After receiving new instructions - Immediately capture user requirements as todos
6. When you start working on a task - Mark it as in_progress BEFORE beginning work. Ideally you should only have one todo as in_progress at a time
7. After completing a task - Mark it as completed and add any new follow-up tasks discovered during implementation

## When NOT to Use This Tool

Skip using this tool when:
1. There is only a single, straightforward task
2. The task is trivial and tracking it provides no organizational benefit
3. The task can be completed in less than 3 trivial steps
4. The task is purely conversational or informational

NOTE that you should not use this tool if there is only one trivial task to do. In this case you are better off just doing the task directly.

## Examples of When to Use the Todo List

<example>
User: I want to add a dark mode toggle to the application settings. Make sure you run the tests and build when you're done!
Assistant: *Creates todo list with the following items:*
1. Creating dark mode toggle component in Settings page
2. Adding dark mode state management (context/store)
3. Implementing CSS-in-JS styles for dark theme
4. Updating existing components to support theme switching
5. Running tests and build process, addressing any failures or errors that occur
*Begins working on the first task*

<reasoning>
The assistant used the todo list because:
1. Adding dark mode is a multi-step feature requiring UI, state management, and styling changes
2. The user explicitly requested tests and build be run afterward
3. The assistant inferred that tests and build need to pass by adding "Ensure tests and build succeed" as the final task
</reasoning>
</example>

<example>
User: Help me rename the function getCwd to getCurrentWorkingDirectory across my project
Assistant: *Uses grep or search tools to locate all instances of getCwd in the codebase*
I've found 15 instances of 'getCwd' across 8 different files.

```

---


### `src/tools/ToolSearchTool/ToolSearchTool.ts`

**信息:**
- 行数: 471
- 大小: 14275 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ToolResultBlockParam } from '@anthropic-ai/sdk/resources/index.mjs'
import memoize from 'lodash-es/memoize.js'
import { z } from 'zod/v4'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import {
  buildTool,
  findToolByName,
  type Tool,
  type ToolDef,
  type Tools,
} from '../../Tool.js'
import { logForDebugging } from '../../utils/debug.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { escapeRegExp } from '../../utils/stringUtils.js'
import { isToolSearchEnabledOptimistic } from '../../utils/toolSearch.js'
import { getPrompt, isDeferredTool, TOOL_SEARCH_TOOL_NAME } from './prompt.js'

export const inputSchema = lazySchema(() =>
  z.object({
    query: z
      .string()
      .describe(
        'Query to find deferred tools. Use "select:<tool_name>" for direct selection, or keywords to search.',
      ),
    max_results: z
      .number()
      .optional()
      .default(5)
      .describe('Maximum number of results to return (default: 5)'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

export const outputSchema = lazySchema(() =>
  z.object({
    matches: z.array(z.string()),
    query: z.string(),
    total_deferred_tools: z.number(),
    pending_mcp_servers: z.array(z.string()).optional(),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>

export type Output = z.infer<OutputSchema>

// Track deferred tool names to detect when cache should be cleared
let cachedDeferredToolNames: string | null = null

```

---


### `src/tools/ToolSearchTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 50 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const TOOL_SEARCH_TOOL_NAME = 'ToolSearch'

```

---


### `src/tools/ToolSearchTool/prompt.ts`

**信息:**
- 行数: 121
- 大小: 5227 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { isReplBridgeActive } from '../../bootstrap/state.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import type { Tool } from '../../Tool.js'
import { AGENT_TOOL_NAME } from '../AgentTool/constants.js'

// Dead code elimination: Brief tool name only needed when KAIROS or KAIROS_BRIEF is on
/* eslint-disable @typescript-eslint/no-require-imports */
const BRIEF_TOOL_NAME: string | null =
  feature('KAIROS') || feature('KAIROS_BRIEF')
    ? (
        require('../BriefTool/prompt.js') as typeof import('../BriefTool/prompt.js')
      ).BRIEF_TOOL_NAME
    : null
const SEND_USER_FILE_TOOL_NAME: string | null = feature('KAIROS')
  ? (
      require('../SendUserFileTool/prompt.js') as typeof import('../SendUserFileTool/prompt.js')
    ).SEND_USER_FILE_TOOL_NAME
  : null

/* eslint-enable @typescript-eslint/no-require-imports */

export { TOOL_SEARCH_TOOL_NAME } from './constants.js'

import { TOOL_SEARCH_TOOL_NAME } from './constants.js'

const PROMPT_HEAD = `Fetches full schema definitions for deferred tools so they can be called.

`

// Matches isDeferredToolsDeltaEnabled in toolSearch.ts (not imported —
// toolSearch.ts imports from this file). When enabled: tools announced
// via system-reminder attachments. When disabled: prepended
// <available-deferred-tools> block (pre-gate behavior).
function getToolLocationHint(): string {
  const deltaEnabled =
    process.env.USER_TYPE === 'ant' ||
    getFeatureValue_CACHED_MAY_BE_STALE('tengu_glacier_2xr', false)
  return deltaEnabled
    ? 'Deferred tools appear by name in <system-reminder> messages.'
    : 'Deferred tools appear by name in <available-deferred-tools> messages.'
}

const PROMPT_TAIL = ` Until fetched, only the name is known — there is no parameter schema, so the tool cannot be invoked. This tool takes a query, matches it against the deferred tool list, and returns the matched tools' complete JSONSchema definitions inside a <functions> block. Once a tool's schema appears in that result, it is callable exactly like any tool defined at the top of the prompt.

Result format: each matched tool appears as one <function>{"description": "...", "name": "...", "parameters": {...}}</function> line inside the <functions> block — the same encoding as the tool list at the top of this prompt.

Query forms:
- "select:Read,Edit,Grep" — fetch these exact tools by name
- "notebook jupyter" — keyword search, up to max_results best matches

```

---


### `src/tools/TungstenTool/TungstenLiveMonitor.tsx`

**信息:**
- 行数: 3
- 大小: 56 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function TungstenLiveMonitor() {
  return null
}

```

---


### `src/tools/TungstenTool/TungstenTool.ts`

**信息:**
- 行数: 50
- 大小: 1157 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { buildTool } from '../../Tool.js'

export const TungstenTool = buildTool({
  name: 'tungsten',
  userFacingName() {
    return 'Tungsten'
  },
  async description() {
    return (
      'Internal terminal-session bridge used by Anthropic builds. ' +
      'This restored workspace keeps the tool registered so configs and ' +
      'older transcripts remain readable, but the original backend is absent.'
    )
  },
  async prompt() {
    return (
      'Tungsten is not executable in this restored workspace. ' +
      'If the user needs terminal automation, use the standard Bash tool ' +
      'or another available local tool instead.'
    )
  },
  inputSchema: {
    parse(value: unknown) {
      return value
    },
  } as never,
  outputSchema: {
    parse(value: unknown) {
      return value
    },
  } as never,
  isEnabled() {
    return false
  },
  isReadOnly() {
    return true
  },
  isConcurrencySafe() {
    return true
  },
  async call() {
    return {
      data: {
        ok: false,
        error:
          'Tungsten is unavailable in this restored workspace; use Bash or another local tool instead.',
      },
    }
  },
})

```

---


### `src/tools/VerifyPlanExecutionTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 71 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const VERIFY_PLAN_EXECUTION_TOOL_NAME = 'verify_plan_execution'

```

---


### `src/tools/WebBrowserTool/WebBrowserPanel.tsx`

**信息:**
- 行数: 3
- 大小: 52 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function WebBrowserPanel() {
  return null
}

```

---


### `src/tools/WebFetchTool/UI.tsx`

**信息:**
- 行数: 72
- 大小: 8083 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { MessageResponse } from '../../components/MessageResponse.js';
import { TOOL_SUMMARY_MAX_LENGTH } from '../../constants/toolLimits.js';
import { Box, Text } from '../../ink.js';
import type { ToolProgressData } from '../../Tool.js';
import type { ProgressMessage } from '../../types/message.js';
import { formatFileSize, truncate } from '../../utils/format.js';
import type { Output } from './WebFetchTool.js';
export function renderToolUseMessage({
  url,
  prompt
}: Partial<{
  url: string;
  prompt: string;
}>, {
  verbose
}: {
  theme?: string;
  verbose: boolean;
}): React.ReactNode {
  if (!url) {
    return null;
  }
  if (verbose) {
    return `url: "${url}"${verbose && prompt ? `, prompt: "${prompt}"` : ''}`;
  }
  return url;
}
export function renderToolUseProgressMessage(): React.ReactNode {
  return <MessageResponse height={1}>
      <Text dimColor>Fetching…</Text>
    </MessageResponse>;
}
export function renderToolResultMessage({
  bytes,
  code,
  codeText,
  result
}: Output, _progressMessagesForMessage: ProgressMessage<ToolProgressData>[], {
  verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  const formattedSize = formatFileSize(bytes);
  if (verbose) {
    return <Box flexDirection="column">
        <MessageResponse height={1}>
          <Text>
            Received <Text bold>{formattedSize}</Text> ({code} {codeText})
          </Text>

```

---


### `src/tools/WebFetchTool/WebFetchTool.ts`

**信息:**
- 行数: 318
- 大小: 9324 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { z } from 'zod/v4'
import { buildTool, type ToolDef } from '../../Tool.js'
import type { PermissionUpdate } from '../../types/permissions.js'
import { formatFileSize } from '../../utils/format.js'
import { lazySchema } from '../../utils/lazySchema.js'
import type { PermissionDecision } from '../../utils/permissions/PermissionResult.js'
import { getRuleByContentsForTool } from '../../utils/permissions/permissions.js'
import { isPreapprovedHost } from './preapproved.js'
import { DESCRIPTION, WEB_FETCH_TOOL_NAME } from './prompt.js'
import {
  getToolUseSummary,
  renderToolResultMessage,
  renderToolUseMessage,
  renderToolUseProgressMessage,
} from './UI.js'
import {
  applyPromptToMarkdown,
  type FetchedContent,
  getURLMarkdownContent,
  isPreapprovedUrl,
  MAX_MARKDOWN_LENGTH,
} from './utils.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    url: z.string().url().describe('The URL to fetch content from'),
    prompt: z.string().describe('The prompt to run on the fetched content'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

const outputSchema = lazySchema(() =>
  z.object({
    bytes: z.number().describe('Size of the fetched content in bytes'),
    code: z.number().describe('HTTP response code'),
    codeText: z.string().describe('HTTP response code text'),
    result: z
      .string()
      .describe('Processed result from applying the prompt to the content'),
    durationMs: z
      .number()
      .describe('Time taken to fetch and process the content'),
    url: z.string().describe('The URL that was fetched'),
  }),
)
type OutputSchema = ReturnType<typeof outputSchema>

export type Output = z.infer<OutputSchema>

function webFetchToolInputToPermissionRuleContent(input: {

```

---


### `src/tools/WebFetchTool/preapproved.ts`

**信息:**
- 行数: 166
- 大小: 5248 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// For legal and security concerns, we typically only allow Web Fetch to access
// domains that the user has provided in some form. However, we make an
// exception for a list of preapproved domains that are code-related.
//
// SECURITY WARNING: These preapproved domains are ONLY for WebFetch (GET requests only).
// The sandbox system deliberately does NOT inherit this list for network restrictions,
// as arbitrary network access (POST, uploads, etc.) to these domains could enable
// data exfiltration. Some domains like huggingface.co, kaggle.com, and nuget.org
// allow file uploads and would be dangerous for unrestricted network access.
//
// See test/utils/sandbox/webfetch-preapproved-separation.test.ts for verification
// that sandbox network restrictions require explicit user permission rules.

export const PREAPPROVED_HOSTS = new Set([
  // Anthropic
  'platform.claude.com',
  'code.claude.com',
  'modelcontextprotocol.io',
  'github.com/anthropics',
  'agentskills.io',

  // Top Programming Languages
  'docs.python.org', // Python
  'en.cppreference.com', // C/C++ reference
  'docs.oracle.com', // Java
  'learn.microsoft.com', // C#/.NET
  'developer.mozilla.org', // JavaScript/Web APIs (MDN)
  'go.dev', // Go
  'pkg.go.dev', // Go docs
  'www.php.net', // PHP
  'docs.swift.org', // Swift
  'kotlinlang.org', // Kotlin
  'ruby-doc.org', // Ruby
  'doc.rust-lang.org', // Rust
  'www.typescriptlang.org', // TypeScript

  // Web & JavaScript Frameworks/Libraries
  'react.dev', // React
  'angular.io', // Angular
  'vuejs.org', // Vue.js
  'nextjs.org', // Next.js
  'expressjs.com', // Express.js
  'nodejs.org', // Node.js
  'bun.sh', // Bun
  'jquery.com', // jQuery
  'getbootstrap.com', // Bootstrap
  'tailwindcss.com', // Tailwind CSS
  'd3js.org', // D3.js
  'threejs.org', // Three.js
  'redux.js.org', // Redux

```

---


### `src/tools/WebFetchTool/prompt.ts`

**信息:**
- 行数: 46
- 大小: 2200 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const WEB_FETCH_TOOL_NAME = 'WebFetch'

export const DESCRIPTION = `
- Fetches content from a specified URL and processes it using an AI model
- Takes a URL and a prompt as input
- Fetches the URL content, converts HTML to markdown
- Processes the content with the prompt using a small, fast model
- Returns the model's response about the content
- Use this tool when you need to retrieve and analyze web content

Usage notes:
  - IMPORTANT: If an MCP-provided web fetch tool is available, prefer using that tool instead of this one, as it may have fewer restrictions.
  - The URL must be a fully-formed valid URL
  - HTTP URLs will be automatically upgraded to HTTPS
  - The prompt should describe what information you want to extract from the page
  - This tool is read-only and does not modify any files
  - Results may be summarized if the content is very large
  - Includes a self-cleaning 15-minute cache for faster responses when repeatedly accessing the same URL
  - When a URL redirects to a different host, the tool will inform you and provide the redirect URL in a special format. You should then make a new WebFetch request with the redirect URL to fetch the content.
  - For GitHub URLs, prefer using the gh CLI via Bash instead (e.g., gh pr view, gh issue view, gh api).
`

export function makeSecondaryModelPrompt(
  markdownContent: string,
  prompt: string,
  isPreapprovedDomain: boolean,
): string {
  const guidelines = isPreapprovedDomain
    ? `Provide a concise response based on the content above. Include relevant details, code examples, and documentation excerpts as needed.`
    : `Provide a concise response based only on the content above. In your response:
 - Enforce a strict 125-character maximum for quotes from any source document. Open Source Software is ok as long as we respect the license.
 - Use quotation marks for exact language from articles; any language outside of the quotation should never be word-for-word the same.
 - You are not a lawyer and never comment on the legality of your own prompts and responses.
 - Never produce or reproduce exact song lyrics.`

  return `
Web page content:
---
${markdownContent}
---

${prompt}

${guidelines}
`
}

```

---


### `src/tools/WebFetchTool/utils.ts`

**信息:**
- 行数: 530
- 大小: 16761 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios, { type AxiosResponse } from 'axios'
import { LRUCache } from 'lru-cache'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'
import { queryHaiku } from '../../services/api/claude.js'
import { AbortError } from '../../utils/errors.js'
import { getWebFetchUserAgent } from '../../utils/http.js'
import { logError } from '../../utils/log.js'
import {
  isBinaryContentType,
  persistBinaryContent,
} from '../../utils/mcpOutputStorage.js'
import { getSettings_DEPRECATED } from '../../utils/settings/settings.js'
import { asSystemPrompt } from '../../utils/systemPromptType.js'
import { isPreapprovedHost } from './preapproved.js'
import { makeSecondaryModelPrompt } from './prompt.js'

// Custom error classes for domain blocking
class DomainBlockedError extends Error {
  constructor(domain: string) {
    super(`Claude Code is unable to fetch from ${domain}`)
    this.name = 'DomainBlockedError'
  }
}

class DomainCheckFailedError extends Error {
  constructor(domain: string) {
    super(
      `Unable to verify if domain ${domain} is safe to fetch. This may be due to network restrictions or enterprise security policies blocking claude.ai.`,
    )
    this.name = 'DomainCheckFailedError'
  }
}

class EgressBlockedError extends Error {
  constructor(public readonly domain: string) {
    super(
      JSON.stringify({
        error_type: 'EGRESS_BLOCKED',
        domain,
        message: `Access to ${domain} is blocked by the network egress proxy.`,
      }),
    )
    this.name = 'EgressBlockedError'
  }
}

// Cache for storing fetched URL content

```

---


### `src/tools/WebSearchTool/UI.tsx`

**信息:**
- 行数: 101
- 大小: 12160 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React from 'react';
import { MessageResponse } from '../../components/MessageResponse.js';
import { TOOL_SUMMARY_MAX_LENGTH } from '../../constants/toolLimits.js';
import { Box, Text } from '../../ink.js';
import type { ProgressMessage } from '../../types/message.js';
import { truncate } from '../../utils/format.js';
import type { Output, SearchResult, WebSearchProgress } from './WebSearchTool.js';
function getSearchSummary(results: (SearchResult | string | null | undefined)[]): {
  searchCount: number;
  totalResultCount: number;
} {
  let searchCount = 0;
  let totalResultCount = 0;
  for (const result of results) {
    if (result != null && typeof result !== 'string') {
      searchCount++;
      totalResultCount += result.content?.length ?? 0;
    }
  }
  return {
    searchCount,
    totalResultCount
  };
}
export function renderToolUseMessage({
  query,
  allowed_domains,
  blocked_domains
}: Partial<{
  query: string;
  allowed_domains?: string[];
  blocked_domains?: string[];
}>, {
  verbose
}: {
  verbose: boolean;
}): React.ReactNode {
  if (!query) {
    return null;
  }
  let message = '';
  if (query) {
    message += `"${query}"`;
  }
  if (verbose) {
    if (allowed_domains && allowed_domains.length > 0) {
      message += `, only allowing domains: ${allowed_domains.join(', ')}`;
    }
    if (blocked_domains && blocked_domains.length > 0) {
      message += `, blocking domains: ${blocked_domains.join(', ')}`;

```

---


### `src/tools/WebSearchTool/WebSearchTool.ts`

**信息:**
- 行数: 435
- 大小: 13548 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type {
  BetaContentBlock,
  BetaWebSearchTool20250305,
} from '@anthropic-ai/sdk/resources/beta/messages/messages.mjs'
import { getAPIProvider } from 'src/utils/model/providers.js'
import type { PermissionResult } from 'src/utils/permissions/PermissionResult.js'
import { z } from 'zod/v4'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import { queryModelWithStreaming } from '../../services/api/claude.js'
import { buildTool, type ToolDef } from '../../Tool.js'
import { lazySchema } from '../../utils/lazySchema.js'
import { logError } from '../../utils/log.js'
import { createUserMessage } from '../../utils/messages.js'
import { getMainLoopModel, getSmallFastModel } from '../../utils/model/model.js'
import { jsonParse, jsonStringify } from '../../utils/slowOperations.js'
import { asSystemPrompt } from '../../utils/systemPromptType.js'
import { getWebSearchPrompt, WEB_SEARCH_TOOL_NAME } from './prompt.js'
import {
  getToolUseSummary,
  renderToolResultMessage,
  renderToolUseMessage,
  renderToolUseProgressMessage,
} from './UI.js'

const inputSchema = lazySchema(() =>
  z.strictObject({
    query: z.string().min(2).describe('The search query to use'),
    allowed_domains: z
      .array(z.string())
      .optional()
      .describe('Only include search results from these domains'),
    blocked_domains: z
      .array(z.string())
      .optional()
      .describe('Never include search results from these domains'),
  }),
)
type InputSchema = ReturnType<typeof inputSchema>

type Input = z.infer<InputSchema>

const searchResultSchema = lazySchema(() => {
  const searchHitSchema = z.object({
    title: z.string().describe('The title of the search result'),
    url: z.string().describe('The URL of the search result'),
  })

  return z.object({
    tool_use_id: z.string().describe('ID of the tool use'),
    content: z.array(searchHitSchema).describe('Array of search hits'),

```

---


### `src/tools/WebSearchTool/prompt.ts`

**信息:**
- 行数: 34
- 大小: 1545 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getLocalMonthYear } from 'src/constants/common.js'

export const WEB_SEARCH_TOOL_NAME = 'WebSearch'

export function getWebSearchPrompt(): string {
  const currentMonthYear = getLocalMonthYear()
  return `
- Allows Claude to search the web and use the results to inform responses
- Provides up-to-date information for current events and recent data
- Returns search result information formatted as search result blocks, including links as markdown hyperlinks
- Use this tool for accessing information beyond Claude's knowledge cutoff
- Searches are performed automatically within a single API call

CRITICAL REQUIREMENT - You MUST follow this:
  - After answering the user's question, you MUST include a "Sources:" section at the end of your response
  - In the Sources section, list all relevant URLs from the search results as markdown hyperlinks: [Title](URL)
  - This is MANDATORY - never skip including sources in your response
  - Example format:

    [Your answer here]

    Sources:
    - [Source Title 1](https://example.com/1)
    - [Source Title 2](https://example.com/2)

Usage notes:
  - Domain filtering is supported to include or block specific websites
  - Web search is only available in the US

IMPORTANT - Use the correct year in search queries:
  - The current month is ${currentMonthYear}. You MUST use this year when searching for recent information, documentation, or current events.
  - Example: If the user asks for "latest React docs", search for "React documentation" with the current year, NOT last year
`
}

```

---


### `src/tools/WorkflowTool/WorkflowPermissionRequest.tsx`

**信息:**
- 行数: 3
- 大小: 62 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
export function WorkflowPermissionRequest() {
  return null
}

```

---


### `src/tools/WorkflowTool/WorkflowTool.ts`

**信息:**
- 行数: 1
- 大小: 33 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const WorkflowTool = null

```

---


### `src/tools/WorkflowTool/constants.ts`

**信息:**
- 行数: 1
- 大小: 45 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const WORKFLOW_TOOL_NAME = 'workflow'

```

---


### `src/tools/WorkflowTool/createWorkflowCommand.ts`

**信息:**
- 行数: 3
- 大小: 58 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function createWorkflowCommand() {
  return null
}

```

---


### `src/tools/shared/gitOperationTracking.ts`

**信息:**
- 行数: 277
- 大小: 9485 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Shell-agnostic git operation tracking for usage metrics.
 *
 * Detects `git commit`, `git push`, `gh pr create`, `glab mr create`, and
 * curl-based PR creation in command strings, then increments OTLP counters
 * and fires analytics events. The regexes operate on raw command text so they
 * work identically for Bash and PowerShell (both invoke git/gh/glab/curl as
 * external binaries with the same argv syntax).
 */

import { getCommitCounter, getPrCounter } from '../../bootstrap/state.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../../services/analytics/index.js'

/**
 * Build a regex that matches `git <subcmd>` while tolerating git's global
 * options between `git` and the subcommand (e.g. `-c key=val`, `-C path`,
 * `--git-dir=path`). Common when the model retries with
 * `git -c commit.gpgsign=false commit` after a signing failure.
 */
function gitCmdRe(subcmd: string, suffix = ''): RegExp {
  return new RegExp(
    `\\bgit(?:\\s+-[cC]\\s+\\S+|\\s+--\\S+=\\S+)*\\s+${subcmd}\\b${suffix}`,
  )
}

const GIT_COMMIT_RE = gitCmdRe('commit')
const GIT_PUSH_RE = gitCmdRe('push')
const GIT_CHERRY_PICK_RE = gitCmdRe('cherry-pick')
const GIT_MERGE_RE = gitCmdRe('merge', '(?!-)')
const GIT_REBASE_RE = gitCmdRe('rebase')

export type CommitKind = 'committed' | 'amended' | 'cherry-picked'
export type BranchAction = 'merged' | 'rebased'
export type PrAction =
  | 'created'
  | 'edited'
  | 'merged'
  | 'commented'
  | 'closed'
  | 'ready'

const GH_PR_ACTIONS: readonly { re: RegExp; action: PrAction; op: string }[] = [
  { re: /\bgh\s+pr\s+create\b/, action: 'created', op: 'pr_create' },
  { re: /\bgh\s+pr\s+edit\b/, action: 'edited', op: 'pr_edit' },
  { re: /\bgh\s+pr\s+merge\b/, action: 'merged', op: 'pr_merge' },
  { re: /\bgh\s+pr\s+comment\b/, action: 'commented', op: 'pr_comment' },
  { re: /\bgh\s+pr\s+close\b/, action: 'closed', op: 'pr_close' },

```

---


### `src/tools/shared/spawnMultiAgent.ts`

**信息:**
- 行数: 1093
- 大小: 35553 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Shared spawn module for teammate creation.
 * Extracted from TeammateTool to allow reuse by AgentTool.
 */

import React from 'react'
import {
  getChromeFlagOverride,
  getFlagSettingsPath,
  getInlinePlugins,
  getMainLoopModelOverride,
  getSessionBypassPermissionsMode,
  getSessionId,
} from '../../bootstrap/state.js'
import type { AppState } from '../../state/AppState.js'
import { createTaskStateBase, generateTaskId } from '../../Task.js'
import type { ToolUseContext } from '../../Tool.js'
import type { InProcessTeammateTaskState } from '../../tasks/InProcessTeammateTask/types.js'
import { formatAgentId } from '../../utils/agentId.js'
import { quote } from '../../utils/bash/shellQuote.js'
import { isInBundledMode } from '../../utils/bundledMode.js'
import { getGlobalConfig } from '../../utils/config.js'
import { getCwd } from '../../utils/cwd.js'
import { logForDebugging } from '../../utils/debug.js'
import { errorMessage } from '../../utils/errors.js'
import { execFileNoThrow } from '../../utils/execFileNoThrow.js'
import { parseUserSpecifiedModel } from '../../utils/model/model.js'
import type { PermissionMode } from '../../utils/permissions/PermissionMode.js'
import { isTmuxAvailable } from '../../utils/swarm/backends/detection.js'
import {
  detectAndGetBackend,
  getBackendByType,
  isInProcessEnabled,
  markInProcessFallback,
  resetBackendDetection,
} from '../../utils/swarm/backends/registry.js'
import { getTeammateModeFromSnapshot } from '../../utils/swarm/backends/teammateModeSnapshot.js'
import type { BackendType } from '../../utils/swarm/backends/types.js'
import { isPaneBackend } from '../../utils/swarm/backends/types.js'
import {
  SWARM_SESSION_NAME,
  TEAM_LEAD_NAME,
  TEAMMATE_COMMAND_ENV_VAR,
  TMUX_COMMAND,
} from '../../utils/swarm/constants.js'
import { It2SetupPrompt } from '../../utils/swarm/It2SetupPrompt.js'
import { startInProcessTeammate } from '../../utils/swarm/inProcessRunner.js'
import {
  type InProcessSpawnConfig,
  spawnInProcessTeammate,

```

---


### `src/tools/testing/TestingPermissionTool.tsx`

**信息:**
- 行数: 74
- 大小: 7312 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
/**
 * This testing-only tool will always pop up a permission dialog when called by
 * the model.
 */
import { z } from 'zod/v4';
import type { Tool } from '../../Tool.js';
import { buildTool, type ToolDef } from '../../Tool.js';
import { lazySchema } from '../../utils/lazySchema.js';
const NAME = 'TestingPermission';
const inputSchema = lazySchema(() => z.strictObject({}));
type InputSchema = ReturnType<typeof inputSchema>;
export const TestingPermissionTool: Tool<InputSchema, string> = buildTool({
  name: NAME,
  maxResultSizeChars: 100_000,
  async description() {
    return 'Test tool that always asks for permission';
  },
  async prompt() {
    return 'Test tool that always asks for permission before executing. Used for end-to-end testing.';
  },
  get inputSchema(): InputSchema {
    return inputSchema();
  },
  userFacingName() {
    return 'TestingPermission';
  },
  isEnabled() {
    return "production" === 'test';
  },
  isConcurrencySafe() {
    return true;
  },
  isReadOnly() {
    return true;
  },
  async checkPermissions() {
    // This tool always requires permission
    return {
      behavior: 'ask' as const,
      message: `Run test?`
    };
  },
  renderToolUseMessage() {
    return null;
  },
  renderToolUseProgressMessage() {
    return null;
  },
  renderToolUseQueuedMessage() {
    return null;

```

---


### `src/tools/utils.ts`

**信息:**
- 行数: 40
- 大小: 1105 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type {
  AssistantMessage,
  AttachmentMessage,
  SystemMessage,
  UserMessage,
} from 'src/types/message.js'

/**
 * Tags user messages with a sourceToolUseID so they stay transient until the tool resolves.
 * This prevents the "is running" message from being duplicated in the UI.
 */
export function tagMessagesWithToolUseID(
  messages: (UserMessage | AttachmentMessage | SystemMessage)[],
  toolUseID: string | undefined,
): (UserMessage | AttachmentMessage | SystemMessage)[] {
  if (!toolUseID) {
    return messages
  }
  return messages.map(m => {
    if (m.type === 'user') {
      return { ...m, sourceToolUseID: toolUseID }
    }
    return m
  })
}

/**
 * Extracts the tool use ID from a parent message for a given tool name.
 */
export function getToolUseIDFromParentMessage(
  parentMessage: AssistantMessage,
  toolName: string,
): string | undefined {
  const toolUseBlock = parentMessage.message.content.find(
    block => block.type === 'tool_use' && block.name === toolName,
  )
  return toolUseBlock && toolUseBlock.type === 'tool_use'
    ? toolUseBlock.id
    : undefined
}

```

---

