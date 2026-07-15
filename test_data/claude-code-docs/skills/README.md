# skills 模块

## 概述

**位置:** `src/skills/`

## 文件统计

- TypeScript 文件: 24
- TypeScript React 文件: 0
- 总计: 24

## 文件详情

---


### `src/skills/bundled/batch.ts`

**信息:**
- 行数: 124
- 大小: 7177 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { AGENT_TOOL_NAME } from '../../tools/AgentTool/constants.js'
import { ASK_USER_QUESTION_TOOL_NAME } from '../../tools/AskUserQuestionTool/prompt.js'
import { ENTER_PLAN_MODE_TOOL_NAME } from '../../tools/EnterPlanModeTool/constants.js'
import { EXIT_PLAN_MODE_TOOL_NAME } from '../../tools/ExitPlanModeTool/constants.js'
import { SKILL_TOOL_NAME } from '../../tools/SkillTool/constants.js'
import { getIsGit } from '../../utils/git.js'
import { registerBundledSkill } from '../bundledSkills.js'

const MIN_AGENTS = 5
const MAX_AGENTS = 30

const WORKER_INSTRUCTIONS = `After you finish implementing the change:
1. **Simplify** — Invoke the \`${SKILL_TOOL_NAME}\` tool with \`skill: "simplify"\` to review and clean up your changes.
2. **Run unit tests** — Run the project's test suite (check for package.json scripts, Makefile targets, or common commands like \`npm test\`, \`bun test\`, \`pytest\`, \`go test\`). If tests fail, fix them.
3. **Test end-to-end** — Follow the e2e test recipe from the coordinator's prompt (below). If the recipe says to skip e2e for this unit, skip it.
4. **Commit and push** — Commit all changes with a clear message, push the branch, and create a PR with \`gh pr create\`. Use a descriptive title. If \`gh\` is not available or the push fails, note it in your final message.
5. **Report** — End with a single line: \`PR: <url>\` so the coordinator can track it. If no PR was created, end with \`PR: none — <reason>\`.`

function buildPrompt(instruction: string): string {
  return `# Batch: Parallel Work Orchestration

You are orchestrating a large, parallelizable change across this codebase.

## User Instruction

${instruction}

## Phase 1: Research and Plan (Plan Mode)

Call the \`${ENTER_PLAN_MODE_TOOL_NAME}\` tool now to enter plan mode, then:

1. **Understand the scope.** Launch one or more subagents (in the foreground — you need their results) to deeply research what this instruction touches. Find all the files, patterns, and call sites that need to change. Understand the existing conventions so the migration is consistent.

2. **Decompose into independent units.** Break the work into ${MIN_AGENTS}–${MAX_AGENTS} self-contained units. Each unit must:
   - Be independently implementable in an isolated git worktree (no shared state with sibling units)
   - Be mergeable on its own without depending on another unit's PR landing first
   - Be roughly uniform in size (split large units, merge trivial ones)

   Scale the count to the actual work: few files → closer to ${MIN_AGENTS}; hundreds of files → closer to ${MAX_AGENTS}. Prefer per-directory or per-module slicing over arbitrary file lists.

3. **Determine the e2e test recipe.** Figure out how a worker can verify its change actually works end-to-end — not just that unit tests pass. Look for:
   - A \`claude-in-chrome\` skill or browser-automation tool (for UI changes: click through the affected flow, screenshot the result)
   - A \`tmux\` or CLI-verifier skill (for CLI changes: launch the app interactively, exercise the changed behavior)
   - A dev-server + curl pattern (for API changes: start the server, hit the affected endpoints)
   - An existing e2e/integration test suite the worker can run

   If you cannot find a concrete e2e path, use the \`${ASK_USER_QUESTION_TOOL_NAME}\` tool to ask the user how to verify this change end-to-end. Offer 2–3 specific options based on what you found (e.g., "Screenshot via chrome extension", "Run \`bun run dev\` and curl the endpoint", "No e2e — unit tests are sufficient"). Do not skip this — the workers cannot ask the user themselves.

   Write the recipe as a short, concrete set of steps that a worker can execute autonomously. Include any setup (start a dev server, build first) and the exact command/interaction to verify.


```

---


### `src/skills/bundled/claudeApi.ts`

**信息:**
- 行数: 196
- 大小: 6323 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { readdir } from 'fs/promises'
import { getCwd } from '../../utils/cwd.js'
import { registerBundledSkill } from '../bundledSkills.js'

// claudeApiContent.js bundles 247KB of .md strings. Lazy-load inside
// getPromptForCommand so they only enter memory when /claude-api is invoked.
type SkillContent = typeof import('./claudeApiContent.js')

type DetectedLanguage =
  | 'python'
  | 'typescript'
  | 'java'
  | 'go'
  | 'ruby'
  | 'csharp'
  | 'php'
  | 'curl'

const LANGUAGE_INDICATORS: Record<DetectedLanguage, string[]> = {
  python: ['.py', 'requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile'],
  typescript: ['.ts', '.tsx', 'tsconfig.json', 'package.json'],
  java: ['.java', 'pom.xml', 'build.gradle'],
  go: ['.go', 'go.mod'],
  ruby: ['.rb', 'Gemfile'],
  csharp: ['.cs', '.csproj'],
  php: ['.php', 'composer.json'],
  curl: [],
}

async function detectLanguage(): Promise<DetectedLanguage | null> {
  const cwd = getCwd()
  let entries: string[]
  try {
    entries = await readdir(cwd)
  } catch {
    return null
  }

  for (const [lang, indicators] of Object.entries(LANGUAGE_INDICATORS) as [
    DetectedLanguage,
    string[],
  ][]) {
    if (indicators.length === 0) continue
    for (const indicator of indicators) {
      if (indicator.startsWith('.')) {
        if (entries.some(e => e.endsWith(indicator))) return lang
      } else {
        if (entries.includes(indicator)) return lang
      }
    }

```

---


### `src/skills/bundled/claudeApiContent.ts`

**信息:**
- 行数: 75
- 大小: 4280 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Content for the claude-api bundled skill.
// Each .md file is inlined as a string at build time via Bun's text loader.

import csharpClaudeApi from './claude-api/csharp/claude-api.md'
import curlExamples from './claude-api/curl/examples.md'
import goClaudeApi from './claude-api/go/claude-api.md'
import javaClaudeApi from './claude-api/java/claude-api.md'
import phpClaudeApi from './claude-api/php/claude-api.md'
import pythonAgentSdkPatterns from './claude-api/python/agent-sdk/patterns.md'
import pythonAgentSdkReadme from './claude-api/python/agent-sdk/README.md'
import pythonClaudeApiBatches from './claude-api/python/claude-api/batches.md'
import pythonClaudeApiFilesApi from './claude-api/python/claude-api/files-api.md'
import pythonClaudeApiReadme from './claude-api/python/claude-api/README.md'
import pythonClaudeApiStreaming from './claude-api/python/claude-api/streaming.md'
import pythonClaudeApiToolUse from './claude-api/python/claude-api/tool-use.md'
import rubyClaudeApi from './claude-api/ruby/claude-api.md'
import skillPrompt from './claude-api/SKILL.md'
import sharedErrorCodes from './claude-api/shared/error-codes.md'
import sharedLiveSources from './claude-api/shared/live-sources.md'
import sharedModels from './claude-api/shared/models.md'
import sharedPromptCaching from './claude-api/shared/prompt-caching.md'
import sharedToolUseConcepts from './claude-api/shared/tool-use-concepts.md'
import typescriptAgentSdkPatterns from './claude-api/typescript/agent-sdk/patterns.md'
import typescriptAgentSdkReadme from './claude-api/typescript/agent-sdk/README.md'
import typescriptClaudeApiBatches from './claude-api/typescript/claude-api/batches.md'
import typescriptClaudeApiFilesApi from './claude-api/typescript/claude-api/files-api.md'
import typescriptClaudeApiReadme from './claude-api/typescript/claude-api/README.md'
import typescriptClaudeApiStreaming from './claude-api/typescript/claude-api/streaming.md'
import typescriptClaudeApiToolUse from './claude-api/typescript/claude-api/tool-use.md'

// @[MODEL LAUNCH]: Update the model IDs/names below. These are substituted into {{VAR}}
// placeholders in the .md files at runtime before the skill prompt is sent.
// After updating these constants, manually update the two files that still hardcode models:
//   - claude-api/SKILL.md (Current Models pricing table)
//   - claude-api/shared/models.md (full model catalog with legacy versions and alias mappings)
export const SKILL_MODEL_VARS = {
  OPUS_ID: 'claude-opus-4-6',
  OPUS_NAME: 'Claude Opus 4.6',
  SONNET_ID: 'claude-sonnet-4-6',
  SONNET_NAME: 'Claude Sonnet 4.6',
  HAIKU_ID: 'claude-haiku-4-5',
  HAIKU_NAME: 'Claude Haiku 4.5',
  // Previous Sonnet ID — used in "do not append date suffixes" example in SKILL.md.
  PREV_SONNET_ID: 'claude-sonnet-4-5',
} satisfies Record<string, string>

export const SKILL_PROMPT: string = skillPrompt

export const SKILL_FILES: Record<string, string> = {
  'csharp/claude-api.md': csharpClaudeApi,

```

---


### `src/skills/bundled/claudeInChrome.ts`

**信息:**
- 行数: 34
- 大小: 1760 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { BROWSER_TOOLS } from '@ant/claude-for-chrome-mcp'
import { BASE_CHROME_PROMPT } from '../../utils/claudeInChrome/prompt.js'
import { shouldAutoEnableClaudeInChrome } from '../../utils/claudeInChrome/setup.js'
import { registerBundledSkill } from '../bundledSkills.js'

const CLAUDE_IN_CHROME_MCP_TOOLS = BROWSER_TOOLS.map(
  tool => `mcp__claude-in-chrome__${tool.name}`,
)

const SKILL_ACTIVATION_MESSAGE = `
Now that this skill is invoked, you have access to Chrome browser automation tools. You can now use the mcp__claude-in-chrome__* tools to interact with web pages.

IMPORTANT: Start by calling mcp__claude-in-chrome__tabs_context_mcp to get information about the user's current browser tabs.
`

export function registerClaudeInChromeSkill(): void {
  registerBundledSkill({
    name: 'claude-in-chrome',
    description:
      'Automates your Chrome browser to interact with web pages - clicking elements, filling forms, capturing screenshots, reading console logs, and navigating sites. Opens pages in new tabs within your existing Chrome session. Requires site-level permissions before executing (configured in the extension).',
    whenToUse:
      'When the user wants to interact with web pages, automate browser tasks, capture screenshots, read console logs, or perform any browser-based actions. Always invoke BEFORE attempting to use any mcp__claude-in-chrome__* tools.',
    allowedTools: CLAUDE_IN_CHROME_MCP_TOOLS,
    userInvocable: true,
    isEnabled: () => shouldAutoEnableClaudeInChrome(),
    async getPromptForCommand(args) {
      let prompt = `${BASE_CHROME_PROMPT}\n${SKILL_ACTIVATION_MESSAGE}`
      if (args) {
        prompt += `\n## Task\n\n${args}`
      }
      return [{ type: 'text', text: prompt }]
    },
  })
}

```

---


### `src/skills/bundled/debug.ts`

**信息:**
- 行数: 103
- 大小: 4219 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { open, stat } from 'fs/promises'
import { CLAUDE_CODE_GUIDE_AGENT_TYPE } from 'src/tools/AgentTool/built-in/claudeCodeGuideAgent.js'
import { getSettingsFilePathForSource } from 'src/utils/settings/settings.js'
import { enableDebugLogging, getDebugLogPath } from '../../utils/debug.js'
import { errorMessage, isENOENT } from '../../utils/errors.js'
import { formatFileSize } from '../../utils/format.js'
import { registerBundledSkill } from '../bundledSkills.js'

const DEFAULT_DEBUG_LINES_READ = 20
const TAIL_READ_BYTES = 64 * 1024

export function registerDebugSkill(): void {
  registerBundledSkill({
    name: 'debug',
    description:
      process.env.USER_TYPE === 'ant'
        ? 'Debug your current Claude Code session by reading the session debug log. Includes all event logging'
        : 'Enable debug logging for this session and help diagnose issues',
    allowedTools: ['Read', 'Grep', 'Glob'],
    argumentHint: '[issue description]',
    // disableModelInvocation so that the user has to explicitly request it in
    // interactive mode and so the description does not take up context.
    disableModelInvocation: true,
    userInvocable: true,
    async getPromptForCommand(args) {
      // Non-ants don't write debug logs by default — turn logging on now so
      // subsequent activity in this session is captured.
      const wasAlreadyLogging = enableDebugLogging()
      const debugLogPath = getDebugLogPath()

      let logInfo: string
      try {
        // Tail the log without reading the whole thing - debug logs grow
        // unbounded in long sessions and reading them in full spikes RSS.
        const stats = await stat(debugLogPath)
        const readSize = Math.min(stats.size, TAIL_READ_BYTES)
        const startOffset = stats.size - readSize
        const fd = await open(debugLogPath, 'r')
        try {
          const { buffer, bytesRead } = await fd.read({
            buffer: Buffer.alloc(readSize),
            position: startOffset,
          })
          const tail = buffer
            .toString('utf-8', 0, bytesRead)
            .split('\n')
            .slice(-DEFAULT_DEBUG_LINES_READ)
            .join('\n')
          logInfo = `Log size: ${formatFileSize(stats.size)}\n\n### Last ${DEFAULT_DEBUG_LINES_READ} lines\n\n\`\`\`\n${tail}\n\`\`\``
        } finally {

```

---


### `src/skills/bundled/dream.ts`

**信息:**
- 行数: 1
- 大小: 46 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function registerDreamSkill(): void {}

```

---


### `src/skills/bundled/hunter.ts`

**信息:**
- 行数: 1
- 大小: 47 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function registerHunterSkill(): void {}

```

---


### `src/skills/bundled/index.ts`

**信息:**
- 行数: 79
- 大小: 3252 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { shouldAutoEnableClaudeInChrome } from 'src/utils/claudeInChrome/setup.js'
import { registerBatchSkill } from './batch.js'
import { registerClaudeInChromeSkill } from './claudeInChrome.js'
import { registerDebugSkill } from './debug.js'
import { registerKeybindingsSkill } from './keybindings.js'
import { registerLoremIpsumSkill } from './loremIpsum.js'
import { registerRememberSkill } from './remember.js'
import { registerSimplifySkill } from './simplify.js'
import { registerSkillifySkill } from './skillify.js'
import { registerStuckSkill } from './stuck.js'
import { registerUpdateConfigSkill } from './updateConfig.js'
import { registerVerifySkill } from './verify.js'

/**
 * Initialize all bundled skills.
 * Called at startup to register skills that ship with the CLI.
 *
 * To add a new bundled skill:
 * 1. Create a new file in src/skills/bundled/ (e.g., myskill.ts)
 * 2. Export a register function that calls registerBundledSkill()
 * 3. Import and call that function here
 */
export function initBundledSkills(): void {
  registerUpdateConfigSkill()
  registerKeybindingsSkill()
  registerVerifySkill()
  registerDebugSkill()
  registerLoremIpsumSkill()
  registerSkillifySkill()
  registerRememberSkill()
  registerSimplifySkill()
  registerBatchSkill()
  registerStuckSkill()
  if (feature('KAIROS') || feature('KAIROS_DREAM')) {
    /* eslint-disable @typescript-eslint/no-require-imports */
    const { registerDreamSkill } = require('./dream.js')
    /* eslint-enable @typescript-eslint/no-require-imports */
    registerDreamSkill()
  }
  if (feature('REVIEW_ARTIFACT')) {
    /* eslint-disable @typescript-eslint/no-require-imports */
    const { registerHunterSkill } = require('./hunter.js')
    /* eslint-enable @typescript-eslint/no-require-imports */
    registerHunterSkill()
  }
  if (feature('AGENT_TRIGGERS')) {
    /* eslint-disable @typescript-eslint/no-require-imports */
    const { registerLoopSkill } = require('./loop.js')
    /* eslint-enable @typescript-eslint/no-require-imports */

```

---


### `src/skills/bundled/keybindings.ts`

**信息:**
- 行数: 339
- 大小: 10412 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { DEFAULT_BINDINGS } from '../../keybindings/defaultBindings.js'
import { isKeybindingCustomizationEnabled } from '../../keybindings/loadUserBindings.js'
import {
  MACOS_RESERVED,
  NON_REBINDABLE,
  TERMINAL_RESERVED,
} from '../../keybindings/reservedShortcuts.js'
import type { KeybindingsSchemaType } from '../../keybindings/schema.js'
import {
  KEYBINDING_ACTIONS,
  KEYBINDING_CONTEXT_DESCRIPTIONS,
  KEYBINDING_CONTEXTS,
} from '../../keybindings/schema.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { registerBundledSkill } from '../bundledSkills.js'

/**
 * Build a markdown table of all contexts.
 */
function generateContextsTable(): string {
  return markdownTable(
    ['Context', 'Description'],
    KEYBINDING_CONTEXTS.map(ctx => [
      `\`${ctx}\``,
      KEYBINDING_CONTEXT_DESCRIPTIONS[ctx],
    ]),
  )
}

/**
 * Build a markdown table of all actions with their default bindings and context.
 */
function generateActionsTable(): string {
  // Build a lookup: action -> { keys, context }
  const actionInfo: Record<string, { keys: string[]; context: string }> = {}
  for (const block of DEFAULT_BINDINGS) {
    for (const [key, action] of Object.entries(block.bindings)) {
      if (action) {
        if (!actionInfo[action]) {
          actionInfo[action] = { keys: [], context: block.context }
        }
        actionInfo[action].keys.push(key)
      }
    }
  }

  return markdownTable(
    ['Action', 'Default Key(s)', 'Context'],
    KEYBINDING_ACTIONS.map(action => {
      const info = actionInfo[action]

```

---


### `src/skills/bundled/loop.ts`

**信息:**
- 行数: 92
- 大小: 4667 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  CRON_CREATE_TOOL_NAME,
  CRON_DELETE_TOOL_NAME,
  DEFAULT_MAX_AGE_DAYS,
  isKairosCronEnabled,
} from '../../tools/ScheduleCronTool/prompt.js'
import { registerBundledSkill } from '../bundledSkills.js'

const DEFAULT_INTERVAL = '10m'

const USAGE_MESSAGE = `Usage: /loop [interval] <prompt>

Run a prompt or slash command on a recurring interval.

Intervals: Ns, Nm, Nh, Nd (e.g. 5m, 30m, 2h, 1d). Minimum granularity is 1 minute.
If no interval is specified, defaults to ${DEFAULT_INTERVAL}.

Examples:
  /loop 5m /babysit-prs
  /loop 30m check the deploy
  /loop 1h /standup 1
  /loop check the deploy          (defaults to ${DEFAULT_INTERVAL})
  /loop check the deploy every 20m`

function buildPrompt(args: string): string {
  return `# /loop — schedule a recurring prompt

Parse the input below into \`[interval] <prompt…>\` and schedule it with ${CRON_CREATE_TOOL_NAME}.

## Parsing (in priority order)

1. **Leading token**: if the first whitespace-delimited token matches \`^\\d+[smhd]$\` (e.g. \`5m\`, \`2h\`), that's the interval; the rest is the prompt.
2. **Trailing "every" clause**: otherwise, if the input ends with \`every <N><unit>\` or \`every <N> <unit-word>\` (e.g. \`every 20m\`, \`every 5 minutes\`, \`every 2 hours\`), extract that as the interval and strip it from the prompt. Only match when what follows "every" is a time expression — \`check every PR\` has no interval.
3. **Default**: otherwise, interval is \`${DEFAULT_INTERVAL}\` and the entire input is the prompt.

If the resulting prompt is empty, show usage \`/loop [interval] <prompt>\` and stop — do not call ${CRON_CREATE_TOOL_NAME}.

Examples:
- \`5m /babysit-prs\` → interval \`5m\`, prompt \`/babysit-prs\` (rule 1)
- \`check the deploy every 20m\` → interval \`20m\`, prompt \`check the deploy\` (rule 2)
- \`run tests every 5 minutes\` → interval \`5m\`, prompt \`run tests\` (rule 2)
- \`check the deploy\` → interval \`${DEFAULT_INTERVAL}\`, prompt \`check the deploy\` (rule 3)
- \`check every PR\` → interval \`${DEFAULT_INTERVAL}\`, prompt \`check every PR\` (rule 3 — "every" not followed by time)
- \`5m\` → empty prompt → show usage

## Interval → cron

Supported suffixes: \`s\` (seconds, rounded up to nearest minute, min 1), \`m\` (minutes), \`h\` (hours), \`d\` (days). Convert:

| Interval pattern      | Cron expression     | Notes                                    |

```

---


### `src/skills/bundled/loremIpsum.ts`

**信息:**
- 行数: 282
- 大小: 4400 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { registerBundledSkill } from '../bundledSkills.js'

// Verified 1-token words (tested via API token counting)
// All common English words confirmed to tokenize as single tokens
const ONE_TOKEN_WORDS = [
  // Articles & pronouns
  'the',
  'a',
  'an',
  'I',
  'you',
  'he',
  'she',
  'it',
  'we',
  'they',
  'me',
  'him',
  'her',
  'us',
  'them',
  'my',
  'your',
  'his',
  'its',
  'our',
  'this',
  'that',
  'what',
  'who',
  // Common verbs
  'is',
  'are',
  'was',
  'were',
  'be',
  'been',
  'have',
  'has',
  'had',
  'do',
  'does',
  'did',
  'will',
  'would',
  'can',
  'could',
  'may',
  'might',
  'must',

```

---


### `src/skills/bundled/remember.ts`

**信息:**
- 行数: 82
- 大小: 4227 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { isAutoMemoryEnabled } from '../../memdir/paths.js'
import { registerBundledSkill } from '../bundledSkills.js'

export function registerRememberSkill(): void {
  if (process.env.USER_TYPE !== 'ant') {
    return
  }

  const SKILL_PROMPT = `# Memory Review

## Goal
Review the user's memory landscape and produce a clear report of proposed changes, grouped by action type. Do NOT apply changes — present proposals for user approval.

## Steps

### 1. Gather all memory layers
Read CLAUDE.md and CLAUDE.local.md from the project root (if they exist). Your auto-memory content is already in your system prompt — review it there. Note which team memory sections exist, if any.

**Success criteria**: You have the contents of all memory layers and can compare them.

### 2. Classify each auto-memory entry
For each substantive entry in auto-memory, determine the best destination:

| Destination | What belongs there | Examples |
|---|---|---|
| **CLAUDE.md** | Project conventions and instructions for Claude that all contributors should follow | "use bun not npm", "API routes use kebab-case", "test command is bun test", "prefer functional style" |
| **CLAUDE.local.md** | Personal instructions for Claude specific to this user, not applicable to other contributors | "I prefer concise responses", "always explain trade-offs", "don't auto-commit", "run tests before committing" |
| **Team memory** | Org-wide knowledge that applies across repositories (only if team memory is configured) | "deploy PRs go through #deploy-queue", "staging is at staging.internal", "platform team owns infra" |
| **Stay in auto-memory** | Working notes, temporary context, or entries that don't clearly fit elsewhere | Session-specific observations, uncertain patterns |

**Important distinctions:**
- CLAUDE.md and CLAUDE.local.md contain instructions for Claude, not user preferences for external tools (editor theme, IDE keybindings, etc. don't belong in either)
- Workflow practices (PR conventions, merge strategies, branch naming) are ambiguous — ask the user whether they're personal or team-wide
- When unsure, ask rather than guess

**Success criteria**: Each entry has a proposed destination or is flagged as ambiguous.

### 3. Identify cleanup opportunities
Scan across all layers for:
- **Duplicates**: Auto-memory entries already captured in CLAUDE.md or CLAUDE.local.md → propose removing from auto-memory
- **Outdated**: CLAUDE.md or CLAUDE.local.md entries contradicted by newer auto-memory entries → propose updating the older layer
- **Conflicts**: Contradictions between any two layers → propose resolution, noting which is more recent

**Success criteria**: All cross-layer issues identified.

### 4. Present the report
Output a structured report grouped by action type:
1. **Promotions** — entries to move, with destination and rationale
2. **Cleanup** — duplicates, outdated entries, conflicts to resolve
3. **Ambiguous** — entries where you need the user's input on destination

```

---


### `src/skills/bundled/runSkillGenerator.ts`

**信息:**
- 行数: 1
- 大小: 58 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function registerRunSkillGeneratorSkill(): void {}

```

---


### `src/skills/bundled/scheduleRemoteAgents.ts`

**信息:**
- 行数: 447
- 大小: 19048 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../../services/analytics/growthbook.js'
import type { MCPServerConnection } from '../../services/mcp/types.js'
import { isPolicyAllowed } from '../../services/policyLimits/index.js'
import type { ToolUseContext } from '../../Tool.js'
import { ASK_USER_QUESTION_TOOL_NAME } from '../../tools/AskUserQuestionTool/prompt.js'
import { REMOTE_TRIGGER_TOOL_NAME } from '../../tools/RemoteTriggerTool/prompt.js'
import { getClaudeAIOAuthTokens } from '../../utils/auth.js'
import { checkRepoForRemoteAccess } from '../../utils/background/remote/preconditions.js'
import { logForDebugging } from '../../utils/debug.js'
import {
  detectCurrentRepositoryWithHost,
  parseGitRemote,
} from '../../utils/detectRepository.js'
import { getRemoteUrl } from '../../utils/git.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import {
  createDefaultCloudEnvironment,
  type EnvironmentResource,
  fetchEnvironments,
} from '../../utils/teleport/environments.js'
import { registerBundledSkill } from '../bundledSkills.js'

// Base58 alphabet (Bitcoin-style) used by the tagged ID system
const BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

/**
 * Decode a mcpsrv_ tagged ID to a UUID string.
 * Tagged IDs have format: mcpsrv_01{base58(uuid.int)}
 * where 01 is the version prefix.
 *
 * TODO(public-ship): Before shipping publicly, the /v1/mcp_servers endpoint
 * should return the raw UUID directly so we don't need this client-side decoding.
 * The tagged ID format is an internal implementation detail that could change.
 */
function taggedIdToUUID(taggedId: string): string | null {
  const prefix = 'mcpsrv_'
  if (!taggedId.startsWith(prefix)) {
    return null
  }
  const rest = taggedId.slice(prefix.length)
  // Skip version prefix (2 chars, always "01")
  const base58Data = rest.slice(2)

  // Decode base58 to bigint
  let n = 0n
  for (const c of base58Data) {
    const idx = BASE58.indexOf(c)
    if (idx === -1) {
      return null
    }

```

---


### `src/skills/bundled/simplify.ts`

**信息:**
- 行数: 69
- 大小: 4466 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { AGENT_TOOL_NAME } from '../../tools/AgentTool/constants.js'
import { registerBundledSkill } from '../bundledSkills.js'

const SIMPLIFY_PROMPT = `# Simplify: Code Review and Cleanup

Review all changed files for reuse, quality, and efficiency. Fix any issues found.

## Phase 1: Identify Changes

Run \`git diff\` (or \`git diff HEAD\` if there are staged changes) to see what changed. If there are no git changes, review the most recently modified files that the user mentioned or that you edited earlier in this conversation.

## Phase 2: Launch Three Review Agents in Parallel

Use the ${AGENT_TOOL_NAME} tool to launch all three agents concurrently in a single message. Pass each agent the full diff so it has the complete context.

### Agent 1: Code Reuse Review

For each change:

1. **Search for existing utilities and helpers** that could replace newly written code. Look for similar patterns elsewhere in the codebase — common locations are utility directories, shared modules, and files adjacent to the changed ones.
2. **Flag any new function that duplicates existing functionality.** Suggest the existing function to use instead.
3. **Flag any inline logic that could use an existing utility** — hand-rolled string manipulation, manual path handling, custom environment checks, ad-hoc type guards, and similar patterns are common candidates.

### Agent 2: Code Quality Review

Review the same changes for hacky patterns:

1. **Redundant state**: state that duplicates existing state, cached values that could be derived, observers/effects that could be direct calls
2. **Parameter sprawl**: adding new parameters to a function instead of generalizing or restructuring existing ones
3. **Copy-paste with slight variation**: near-duplicate code blocks that should be unified with a shared abstraction
4. **Leaky abstractions**: exposing internal details that should be encapsulated, or breaking existing abstraction boundaries
5. **Stringly-typed code**: using raw strings where constants, enums (string unions), or branded types already exist in the codebase
6. **Unnecessary JSX nesting**: wrapper Boxes/elements that add no layout value — check if inner component props (flexShrink, alignItems, etc.) already provide the needed behavior
7. **Unnecessary comments**: comments explaining WHAT the code does (well-named identifiers already do that), narrating the change, or referencing the task/caller — delete; keep only non-obvious WHY (hidden constraints, subtle invariants, workarounds)

### Agent 3: Efficiency Review

Review the same changes for efficiency:

1. **Unnecessary work**: redundant computations, repeated file reads, duplicate network/API calls, N+1 patterns
2. **Missed concurrency**: independent operations run sequentially when they could run in parallel
3. **Hot-path bloat**: new blocking work added to startup or per-request/per-render hot paths
4. **Recurring no-op updates**: state/store updates inside polling loops, intervals, or event handlers that fire unconditionally — add a change-detection guard so downstream consumers aren't notified when nothing changed. Also: if a wrapper function takes an updater/reducer callback, verify it honors same-reference returns (or whatever the "no change" signal is) — otherwise callers' early-return no-ops are silently defeated
5. **Unnecessary existence checks**: pre-checking file/resource existence before operating (TOCTOU anti-pattern) — operate directly and handle the error
6. **Memory**: unbounded data structures, missing cleanup, event listener leaks
7. **Overly broad operations**: reading entire files when only a portion is needed, loading all items when filtering for one

## Phase 3: Fix Issues

Wait for all three agents to complete. Aggregate their findings and fix each issue directly. If a finding is a false positive or not worth addressing, note it and move on — do not argue with the finding, just skip it.

```

---


### `src/skills/bundled/skillify.ts`

**信息:**
- 行数: 197
- 大小: 9483 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getSessionMemoryContent } from '../../services/SessionMemory/sessionMemoryUtils.js'
import type { Message } from '../../types/message.js'
import { getMessagesAfterCompactBoundary } from '../../utils/messages.js'
import { registerBundledSkill } from '../bundledSkills.js'

function extractUserMessages(messages: Message[]): string[] {
  return messages
    .filter((m): m is Extract<typeof m, { type: 'user' }> => m.type === 'user')
    .map(m => {
      const content = m.message.content
      if (typeof content === 'string') return content
      return content
        .filter(
          (b): b is Extract<typeof b, { type: 'text' }> => b.type === 'text',
        )
        .map(b => b.text)
        .join('\n')
    })
    .filter(text => text.trim().length > 0)
}

const SKILLIFY_PROMPT = `# Skillify {{userDescriptionBlock}}

You are capturing this session's repeatable process as a reusable skill.

## Your Session Context

Here is the session memory summary:
<session_memory>
{{sessionMemory}}
</session_memory>

Here are the user's messages during this session. Pay attention to how they steered the process, to help capture their detailed preferences in the skill:
<user_messages>
{{userMessages}}
</user_messages>

## Your Task

### Step 1: Analyze the Session

Before asking any questions, analyze the session to identify:
- What repeatable process was performed
- What the inputs/parameters were
- The distinct steps (in order)
- The success artifacts/criteria (e.g. not just "writing code," but "an open PR with CI fully passing") for each step
- Where the user corrected or steered you
- What tools and permissions were needed
- What agents were used
- What the goals and success artifacts were

```

---


### `src/skills/bundled/stuck.ts`

**信息:**
- 行数: 79
- 大小: 4254 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { registerBundledSkill } from '../bundledSkills.js'

// Prompt text contains `ps` commands as instructions for Claude to run,
// not commands this file executes.
// eslint-disable-next-line custom-rules/no-direct-ps-commands
const STUCK_PROMPT = `# /stuck — diagnose frozen/slow Claude Code sessions

The user thinks another Claude Code session on this machine is frozen, stuck, or very slow. Investigate and post a report to #claude-code-feedback.

## What to look for

Scan for other Claude Code processes (excluding the current one — PID is in \`process.pid\` but for shell commands just exclude the PID you see running this prompt). Process names are typically \`claude\` (installed) or \`cli\` (native dev build).

Signs of a stuck session:
- **High CPU (≥90%) sustained** — likely an infinite loop. Sample twice, 1-2s apart, to confirm it's not a transient spike.
- **Process state \`D\` (uninterruptible sleep)** — often an I/O hang. The \`state\` column in \`ps\` output; first character matters (ignore modifiers like \`+\`, \`s\`, \`<\`).
- **Process state \`T\` (stopped)** — user probably hit Ctrl+Z by accident.
- **Process state \`Z\` (zombie)** — parent isn't reaping.
- **Very high RSS (≥4GB)** — possible memory leak making the session sluggish.
- **Stuck child process** — a hung \`git\`, \`node\`, or shell subprocess can freeze the parent. Check \`pgrep -lP <pid>\` for each session.

## Investigation steps

1. **List all Claude Code processes** (macOS/Linux):
   \`\`\`
   ps -axo pid=,pcpu=,rss=,etime=,state=,comm=,command= | grep -E '(claude|cli)' | grep -v grep
   \`\`\`
   Filter to rows where \`comm\` is \`claude\` or (\`cli\` AND the command path contains "claude").

2. **For anything suspicious**, gather more context:
   - Child processes: \`pgrep -lP <pid>\`
   - If high CPU: sample again after 1-2s to confirm it's sustained
   - If a child looks hung (e.g., a git command), note its full command line with \`ps -p <child_pid> -o command=\`
   - Check the session's debug log if you can infer the session ID: \`~/.claude/debug/<session-id>.txt\` (the last few hundred lines often show what it was doing before hanging)

3. **Consider a stack dump** for a truly frozen process (advanced, optional):
   - macOS: \`sample <pid> 3\` gives a 3-second native stack sample
   - This is big — only grab it if the process is clearly hung and you want to know *why*

## Report

**Only post to Slack if you actually found something stuck.** If every session looks healthy, tell the user that directly — do not post an all-clear to the channel.

If you did find a stuck/slow session, post to **#claude-code-feedback** (channel ID: \`C07VBSHV7EV\`) using the Slack MCP tool. Use ToolSearch to find \`slack_send_message\` if it's not already loaded.

**Use a two-message structure** to keep the channel scannable:

1. **Top-level message** — one short line: hostname, Claude Code version, and a terse symptom (e.g. "session PID 12345 pegged at 100% CPU for 10min" or "git subprocess hung in D state"). No code blocks, no details.
2. **Thread reply** — the full diagnostic dump. Pass the top-level message's \`ts\` as \`thread_ts\`. Include:
   - PID, CPU%, RSS, state, uptime, command line, child processes

```

---


### `src/skills/bundled/updateConfig.ts`

**信息:**
- 行数: 475
- 大小: 17453 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { toJSONSchema } from 'zod/v4'
import { SettingsSchema } from '../../utils/settings/types.js'
import { jsonStringify } from '../../utils/slowOperations.js'
import { registerBundledSkill } from '../bundledSkills.js'

/**
 * Generate JSON Schema from the settings Zod schema.
 * This keeps the skill prompt in sync with the actual types.
 */
function generateSettingsSchema(): string {
  const jsonSchema = toJSONSchema(SettingsSchema(), { io: 'input' })
  return jsonStringify(jsonSchema, null, 2)
}

const SETTINGS_EXAMPLES_DOCS = `## Settings File Locations

Choose the appropriate file based on scope:

| File | Scope | Git | Use For |
|------|-------|-----|---------|
| \`~/.claude/settings.json\` | Global | N/A | Personal preferences for all projects |
| \`.claude/settings.json\` | Project | Commit | Team-wide hooks, permissions, plugins |
| \`.claude/settings.local.json\` | Project | Gitignore | Personal overrides for this project |

Settings load in order: user → project → local (later overrides earlier).

## Settings Schema Reference

### Permissions
\`\`\`json
{
  "permissions": {
    "allow": ["Bash(npm:*)", "Edit(.claude)", "Read"],
    "deny": ["Bash(rm -rf:*)"],
    "ask": ["Write(/etc/*)"],
    "defaultMode": "default" | "plan" | "acceptEdits" | "dontAsk",
    "additionalDirectories": ["/extra/dir"]
  }
}
\`\`\`

**Permission Rule Syntax:**
- Exact match: \`"Bash(npm run test)"\`
- Prefix wildcard: \`"Bash(git:*)"\` - matches \`git status\`, \`git commit\`, etc.
- Tool only: \`"Read"\` - allows all Read operations

### Environment Variables
\`\`\`json
{
  "env": {

```

---


### `src/skills/bundled/verify.ts`

**信息:**
- 行数: 30
- 大小: 893 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { parseFrontmatter } from '../../utils/frontmatterParser.js'
import { registerBundledSkill } from '../bundledSkills.js'
import { SKILL_FILES, SKILL_MD } from './verifyContent.js'

const { frontmatter, content: SKILL_BODY } = parseFrontmatter(SKILL_MD)

const DESCRIPTION =
  typeof frontmatter.description === 'string'
    ? frontmatter.description
    : 'Verify a code change does what it should by running the app.'

export function registerVerifySkill(): void {
  if (process.env.USER_TYPE !== 'ant') {
    return
  }

  registerBundledSkill({
    name: 'verify',
    description: DESCRIPTION,
    userInvocable: true,
    files: SKILL_FILES,
    async getPromptForCommand(args) {
      const parts: string[] = [SKILL_BODY.trimStart()]
      if (args) {
        parts.push(`## User Request\n\n${args}`)
      }
      return [{ type: 'text', text: parts.join('\n\n') }]
    },
  })
}

```

---


### `src/skills/bundled/verifyContent.ts`

**信息:**
- 行数: 13
- 大小: 414 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Content for the verify bundled skill.
// Each .md file is inlined as a string at build time via Bun's text loader.

import cliMd from './verify/examples/cli.md'
import serverMd from './verify/examples/server.md'
import skillMd from './verify/SKILL.md'

export const SKILL_MD: string = skillMd

export const SKILL_FILES: Record<string, string> = {
  'examples/cli.md': cliMd,
  'examples/server.md': serverMd,
}

```

---


### `src/skills/bundledSkills.ts`

**信息:**
- 行数: 220
- 大小: 7497 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ContentBlockParam } from '@anthropic-ai/sdk/resources/index.mjs'
import { constants as fsConstants } from 'fs'
import { mkdir, open } from 'fs/promises'
import { dirname, isAbsolute, join, normalize, sep as pathSep } from 'path'
import type { ToolUseContext } from '../Tool.js'
import type { Command } from '../types/command.js'
import { logForDebugging } from '../utils/debug.js'
import { getBundledSkillsRoot } from '../utils/permissions/filesystem.js'
import type { HooksSettings } from '../utils/settings/types.js'

/**
 * Definition for a bundled skill that ships with the CLI.
 * These are registered programmatically at startup.
 */
export type BundledSkillDefinition = {
  name: string
  description: string
  aliases?: string[]
  whenToUse?: string
  argumentHint?: string
  allowedTools?: string[]
  model?: string
  disableModelInvocation?: boolean
  userInvocable?: boolean
  isEnabled?: () => boolean
  hooks?: HooksSettings
  context?: 'inline' | 'fork'
  agent?: string
  /**
   * Additional reference files to extract to disk on first invocation.
   * Keys are relative paths (forward slashes, no `..`), values are content.
   * When set, the skill prompt is prefixed with a "Base directory for this
   * skill: <dir>" line so the model can Read/Grep these files on demand —
   * same contract as disk-based skills.
   */
  files?: Record<string, string>
  getPromptForCommand: (
    args: string,
    context: ToolUseContext,
  ) => Promise<ContentBlockParam[]>
}

// Internal registry for bundled skills
const bundledSkills: Command[] = []

/**
 * Register a bundled skill that will be available to the model.
 * Call this at module initialization or in an init function.
 *
 * Bundled skills are compiled into the CLI binary and available to all users.

```

---


### `src/skills/loadSkillsDir.ts`

**信息:**
- 行数: 1086
- 大小: 34415 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { realpath } from 'fs/promises'
import ignore from 'ignore'
import memoize from 'lodash-es/memoize.js'
import {
  basename,
  dirname,
  isAbsolute,
  join,
  sep as pathSep,
  relative,
} from 'path'
import {
  getAdditionalDirectoriesForClaudeMd,
  getSessionId,
} from '../bootstrap/state.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import { roughTokenCountEstimation } from '../services/tokenEstimation.js'
import type { Command, PromptCommand } from '../types/command.js'
import {
  parseArgumentNames,
  substituteArguments,
} from '../utils/argumentSubstitution.js'
import { logForDebugging } from '../utils/debug.js'
import {
  EFFORT_LEVELS,
  type EffortValue,
  parseEffortValue,
} from '../utils/effort.js'
import {
  getClaudeConfigHomeDir,
  isBareMode,
  isEnvTruthy,
} from '../utils/envUtils.js'
import { isENOENT, isFsInaccessible } from '../utils/errors.js'
import {
  coerceDescriptionToString,
  type FrontmatterData,
  type FrontmatterShell,
  parseBooleanFrontmatter,
  parseFrontmatter,
  parseShellFrontmatter,
  splitPathInFrontmatter,
} from '../utils/frontmatterParser.js'
import { getFsImplementation } from '../utils/fsOperations.js'
import { isPathGitignored } from '../utils/git/gitignore.js'
import { logError } from '../utils/log.js'
import {

```

---


### `src/skills/mcpSkillBuilders.ts`

**信息:**
- 行数: 44
- 大小: 1627 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type {
  createSkillCommand,
  parseSkillFrontmatterFields,
} from './loadSkillsDir.js'

/**
 * Write-once registry for the two loadSkillsDir functions that MCP skill
 * discovery needs. This module is a dependency-graph leaf: it imports nothing
 * but types, so both mcpSkills.ts and loadSkillsDir.ts can depend on it
 * without forming a cycle (client.ts → mcpSkills.ts → loadSkillsDir.ts → …
 * → client.ts).
 *
 * The non-literal dynamic-import approach ("await import(variable)") fails at
 * runtime in Bun-bundled binaries — the specifier is resolved against the
 * chunk's /$bunfs/root/… path, not the original source tree, yielding "Cannot
 * find module './loadSkillsDir.js'". A literal dynamic import works in bunfs
 * but dependency-cruiser tracks it, and because loadSkillsDir transitively
 * reaches almost everything, the single new edge fans out into many new cycle
 * violations in the diff check.
 *
 * Registration happens at loadSkillsDir.ts module init, which is eagerly
 * evaluated at startup via the static import from commands.ts — long before
 * any MCP server connects.
 */

export type MCPSkillBuilders = {
  createSkillCommand: typeof createSkillCommand
  parseSkillFrontmatterFields: typeof parseSkillFrontmatterFields
}

let builders: MCPSkillBuilders | null = null

export function registerMCPSkillBuilders(b: MCPSkillBuilders): void {
  builders = b
}

export function getMCPSkillBuilders(): MCPSkillBuilders {
  if (!builders) {
    throw new Error(
      'MCP skill builders not registered — loadSkillsDir.ts has not been evaluated yet',
    )
  }
  return builders
}

```

---


### `src/skills/mcpSkills.ts`

**信息:**
- 行数: 3
- 大小: 64 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export async function fetchMcpSkillsForClient() {
  return []
}

```

---

