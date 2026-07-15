# memdir 模块

## 概述

**位置:** `src/memdir/`

## 文件统计

- TypeScript 文件: 9
- TypeScript React 文件: 0
- 总计: 9

## 文件详情

---


### `src/memdir/findRelevantMemories.ts`

**信息:**
- 行数: 141
- 大小: 5305 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { logForDebugging } from '../utils/debug.js'
import { errorMessage } from '../utils/errors.js'
import { getDefaultSonnetModel } from '../utils/model/model.js'
import { sideQuery } from '../utils/sideQuery.js'
import { jsonParse } from '../utils/slowOperations.js'
import {
  formatMemoryManifest,
  type MemoryHeader,
  scanMemoryFiles,
} from './memoryScan.js'

export type RelevantMemory = {
  path: string
  mtimeMs: number
}

const SELECT_MEMORIES_SYSTEM_PROMPT = `You are selecting memories that will be useful to Claude Code as it processes a user's query. You will be given the user's query and a list of available memory files with their filenames and descriptions.

Return a list of filenames for the memories that will clearly be useful to Claude Code as it processes the user's query (up to 5). Only include memories that you are certain will be helpful based on their name and description.
- If you are unsure if a memory will be useful in processing the user's query, then do not include it in your list. Be selective and discerning.
- If there are no memories in the list that would clearly be useful, feel free to return an empty list.
- If a list of recently-used tools is provided, do not select memories that are usage reference or API documentation for those tools (Claude Code is already exercising them). DO still select memories containing warnings, gotchas, or known issues about those tools — active use is exactly when those matter.
`

/**
 * Find memory files relevant to a query by scanning memory file headers
 * and asking Sonnet to select the most relevant ones.
 *
 * Returns absolute file paths + mtime of the most relevant memories
 * (up to 5). Excludes MEMORY.md (already loaded in system prompt).
 * mtime is threaded through so callers can surface freshness to the
 * main model without a second stat.
 *
 * `alreadySurfaced` filters paths shown in prior turns before the
 * Sonnet call, so the selector spends its 5-slot budget on fresh
 * candidates instead of re-picking files the caller will discard.
 */
export async function findRelevantMemories(
  query: string,
  memoryDir: string,
  signal: AbortSignal,
  recentTools: readonly string[] = [],
  alreadySurfaced: ReadonlySet<string> = new Set(),
): Promise<RelevantMemory[]> {
  const memories = (await scanMemoryFiles(memoryDir, signal)).filter(
    m => !alreadySurfaced.has(m.filePath),
  )
  if (memories.length === 0) {
    return []

```

---


### `src/memdir/memdir.ts`

**信息:**
- 行数: 507
- 大小: 21174 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { join } from 'path'
import { getFsImplementation } from '../utils/fsOperations.js'
import { getAutoMemPath, isAutoMemoryEnabled } from './paths.js'

/* eslint-disable @typescript-eslint/no-require-imports */
const teamMemPaths = feature('TEAMMEM')
  ? (require('./teamMemPaths.js') as typeof import('./teamMemPaths.js'))
  : null

import { getKairosActive, getOriginalCwd } from '../bootstrap/state.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js'
/* eslint-enable @typescript-eslint/no-require-imports */
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import { GREP_TOOL_NAME } from '../tools/GrepTool/prompt.js'
import { isReplModeEnabled } from '../tools/REPLTool/constants.js'
import { logForDebugging } from '../utils/debug.js'
import { hasEmbeddedSearchTools } from '../utils/embeddedTools.js'
import { isEnvTruthy } from '../utils/envUtils.js'
import { formatFileSize } from '../utils/format.js'
import { getProjectDir } from '../utils/sessionStorage.js'
import { getInitialSettings } from '../utils/settings/settings.js'
import {
  MEMORY_FRONTMATTER_EXAMPLE,
  TRUSTING_RECALL_SECTION,
  TYPES_SECTION_INDIVIDUAL,
  WHAT_NOT_TO_SAVE_SECTION,
  WHEN_TO_ACCESS_SECTION,
} from './memoryTypes.js'

export const ENTRYPOINT_NAME = 'MEMORY.md'
export const MAX_ENTRYPOINT_LINES = 200
// ~125 chars/line at 200 lines. At p97 today; catches long-line indexes that
// slip past the line cap (p100 observed: 197KB under 200 lines).
export const MAX_ENTRYPOINT_BYTES = 25_000
const AUTO_MEM_DISPLAY_NAME = 'auto memory'

export type EntrypointTruncation = {
  content: string
  lineCount: number
  byteCount: number
  wasLineTruncated: boolean
  wasByteTruncated: boolean
}

/**
 * Truncate MEMORY.md content to the line AND byte caps, appending a warning

```

---


### `src/memdir/memoryAge.ts`

**信息:**
- 行数: 53
- 大小: 1931 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Days elapsed since mtime.  Floor-rounded — 0 for today, 1 for
 * yesterday, 2+ for older.  Negative inputs (future mtime, clock skew)
 * clamp to 0.
 */
export function memoryAgeDays(mtimeMs: number): number {
  return Math.max(0, Math.floor((Date.now() - mtimeMs) / 86_400_000))
}

/**
 * Human-readable age string.  Models are poor at date arithmetic —
 * a raw ISO timestamp doesn't trigger staleness reasoning the way
 * "47 days ago" does.
 */
export function memoryAge(mtimeMs: number): string {
  const d = memoryAgeDays(mtimeMs)
  if (d === 0) return 'today'
  if (d === 1) return 'yesterday'
  return `${d} days ago`
}

/**
 * Plain-text staleness caveat for memories >1 day old.  Returns ''
 * for fresh (today/yesterday) memories — warning there is noise.
 *
 * Use this when the consumer already provides its own wrapping
 * (e.g. messages.ts relevant_memories → wrapMessagesInSystemReminder).
 *
 * Motivated by user reports of stale code-state memories (file:line
 * citations to code that has since changed) being asserted as fact —
 * the citation makes the stale claim sound more authoritative, not less.
 */
export function memoryFreshnessText(mtimeMs: number): string {
  const d = memoryAgeDays(mtimeMs)
  if (d <= 1) return ''
  return (
    `This memory is ${d} days old. ` +
    `Memories are point-in-time observations, not live state — ` +
    `claims about code behavior or file:line citations may be outdated. ` +
    `Verify against current code before asserting as fact.`
  )
}

/**
 * Per-memory staleness note wrapped in <system-reminder> tags.
 * Returns '' for memories ≤ 1 day old.  Use this for callers that
 * don't add their own system-reminder wrapper (e.g. FileReadTool output).
 */
export function memoryFreshnessNote(mtimeMs: number): string {
  const text = memoryFreshnessText(mtimeMs)

```

---


### `src/memdir/memoryScan.ts`

**信息:**
- 行数: 94
- 大小: 3105 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Memory-directory scanning primitives. Split out of findRelevantMemories.ts
 * so extractMemories can import the scan without pulling in sideQuery and
 * the API-client chain (which closed a cycle through memdir.ts — #25372).
 */

import { readdir } from 'fs/promises'
import { basename, join } from 'path'
import { parseFrontmatter } from '../utils/frontmatterParser.js'
import { readFileInRange } from '../utils/readFileInRange.js'
import { type MemoryType, parseMemoryType } from './memoryTypes.js'

export type MemoryHeader = {
  filename: string
  filePath: string
  mtimeMs: number
  description: string | null
  type: MemoryType | undefined
}

const MAX_MEMORY_FILES = 200
const FRONTMATTER_MAX_LINES = 30

/**
 * Scan a memory directory for .md files, read their frontmatter, and return
 * a header list sorted newest-first (capped at MAX_MEMORY_FILES). Shared by
 * findRelevantMemories (query-time recall) and extractMemories (pre-injects
 * the listing so the extraction agent doesn't spend a turn on `ls`).
 *
 * Single-pass: readFileInRange stats internally and returns mtimeMs, so we
 * read-then-sort rather than stat-sort-read. For the common case (N ≤ 200)
 * this halves syscalls vs a separate stat round; for large N we read a few
 * extra small files but still avoid the double-stat on the surviving 200.
 */
export async function scanMemoryFiles(
  memoryDir: string,
  signal: AbortSignal,
): Promise<MemoryHeader[]> {
  try {
    const entries = await readdir(memoryDir, { recursive: true })
    const mdFiles = entries.filter(
      f => f.endsWith('.md') && basename(f) !== 'MEMORY.md',
    )

    const headerResults = await Promise.allSettled(
      mdFiles.map(async (relativePath): Promise<MemoryHeader> => {
        const filePath = join(memoryDir, relativePath)
        const { content, mtimeMs } = await readFileInRange(
          filePath,
          0,

```

---


### `src/memdir/memoryShapeTelemetry.ts`

**信息:**
- 行数: 1
- 大小: 54 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function recordMemoryShapeTelemetry(): void {}

```

---


### `src/memdir/memoryTypes.ts`

**信息:**
- 行数: 271
- 大小: 22866 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Memory type taxonomy.
 *
 * Memories are constrained to four types capturing context NOT derivable
 * from the current project state. Code patterns, architecture, git history,
 * and file structure are derivable (via grep/git/CLAUDE.md) and should NOT
 * be saved as memories.
 *
 * The two TYPES_SECTION_* exports below are intentionally duplicated rather
 * than generated from a shared spec — keeping them flat makes per-mode edits
 * trivial without reasoning through a helper's conditional rendering.
 */

export const MEMORY_TYPES = [
  'user',
  'feedback',
  'project',
  'reference',
] as const

export type MemoryType = (typeof MEMORY_TYPES)[number]

/**
 * Parse a raw frontmatter value into a MemoryType.
 * Invalid or missing values return undefined — legacy files without a
 * `type:` field keep working, files with unknown types degrade gracefully.
 */
export function parseMemoryType(raw: unknown): MemoryType | undefined {
  if (typeof raw !== 'string') return undefined
  return MEMORY_TYPES.find(t => t === raw)
}

/**
 * `## Types of memory` section for COMBINED mode (private + team directories).
 * Includes <scope> tags and team/private qualifiers in examples.
 */
export const TYPES_SECTION_COMBINED: readonly string[] = [
  '## Types of memory',
  '',
  'There are several discrete types of memory that you can store in your memory system. Each type below declares a <scope> of `private`, `team`, or guidance for choosing between the two.',
  '',
  '<types>',
  '<type>',
  '    <name>user</name>',
  '    <scope>always private</scope>',
  "    <description>Contain information about the user's role, goals, responsibilities, and knowledge. Great user memories help you tailor your future behavior to the user's preferences and perspective. Your goal in reading and writing these memories is to build up an understanding of who the user is and how you can be most helpful to them specifically. For example, you should collaborate with a senior software engineer differently than a student who is coding for the very first time. Keep in mind, that the aim here is to be helpful to the user. Avoid writing memories about the user that could be viewed as a negative judgement or that are not relevant to the work you're trying to accomplish together.</description>",
  "    <when_to_save>When you learn any details about the user's role, preferences, responsibilities, or knowledge</when_to_save>",
  "    <how_to_use>When your work should be informed by the user's profile or perspective. For example, if the user is asking you to explain a part of the code, you should answer that question in a way that is tailored to the specific details that they will find most valuable or that helps them build their mental model in relation to domain knowledge they already have.</how_to_use>",
  '    <examples>',
  "    user: I'm a data scientist investigating what logging we have in place",

```

---


### `src/memdir/paths.ts`

**信息:**
- 行数: 278
- 大小: 10668 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import memoize from 'lodash-es/memoize.js'
import { homedir } from 'os'
import { isAbsolute, join, normalize, sep } from 'path'
import {
  getIsNonInteractiveSession,
  getProjectRoot,
} from '../bootstrap/state.js'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js'
import {
  getClaudeConfigHomeDir,
  isEnvDefinedFalsy,
  isEnvTruthy,
} from '../utils/envUtils.js'
import { findCanonicalGitRoot } from '../utils/git.js'
import { sanitizePath } from '../utils/path.js'
import {
  getInitialSettings,
  getSettingsForSource,
} from '../utils/settings/settings.js'

/**
 * Whether auto-memory features are enabled (memdir, agent memory, past session search).
 * Enabled by default. Priority chain (first defined wins):
 *   1. CLAUDE_CODE_DISABLE_AUTO_MEMORY env var (1/true → OFF, 0/false → ON)
 *   2. CLAUDE_CODE_SIMPLE (--bare) → OFF
 *   3. CCR without persistent storage → OFF (no CLAUDE_CODE_REMOTE_MEMORY_DIR)
 *   4. autoMemoryEnabled in settings.json (supports project-level opt-out)
 *   5. Default: enabled
 */
export function isAutoMemoryEnabled(): boolean {
  const envVal = process.env.CLAUDE_CODE_DISABLE_AUTO_MEMORY
  if (isEnvTruthy(envVal)) {
    return false
  }
  if (isEnvDefinedFalsy(envVal)) {
    return true
  }
  // --bare / SIMPLE: prompts.ts already drops the memory section from the
  // system prompt via its SIMPLE early-return; this gate stops the other half
  // (extractMemories turn-end fork, autoDream, /remember, /dream, team sync).
  if (isEnvTruthy(process.env.CLAUDE_CODE_SIMPLE)) {
    return false
  }
  if (
    isEnvTruthy(process.env.CLAUDE_CODE_REMOTE) &&
    !process.env.CLAUDE_CODE_REMOTE_MEMORY_DIR
  ) {
    return false
  }
  const settings = getInitialSettings()

```

---


### `src/memdir/teamMemPaths.ts`

**信息:**
- 行数: 292
- 大小: 11691 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { lstat, realpath } from 'fs/promises'
import { dirname, join, resolve, sep } from 'path'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js'
import { getErrnoCode } from '../utils/errors.js'
import { getAutoMemPath, isAutoMemoryEnabled } from './paths.js'

/**
 * Error thrown when a path validation detects a traversal or injection attempt.
 */
export class PathTraversalError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'PathTraversalError'
  }
}

/**
 * Sanitize a file path key by rejecting dangerous patterns.
 * Checks for null bytes, URL-encoded traversals, and other injection vectors.
 * Returns the sanitized string or throws PathTraversalError.
 */
function sanitizePathKey(key: string): string {
  // Null bytes can truncate paths in C-based syscalls
  if (key.includes('\0')) {
    throw new PathTraversalError(`Null byte in path key: "${key}"`)
  }
  // URL-encoded traversals (e.g. %2e%2e%2f = ../)
  let decoded: string
  try {
    decoded = decodeURIComponent(key)
  } catch {
    // Malformed percent-encoding (e.g. %ZZ, lone %) — not valid URL-encoding,
    // so no URL-encoded traversal is possible
    decoded = key
  }
  if (decoded !== key && (decoded.includes('..') || decoded.includes('/'))) {
    throw new PathTraversalError(`URL-encoded traversal in path key: "${key}"`)
  }
  // Unicode normalization attacks: fullwidth ．．／ (U+FF0E U+FF0F) normalize
  // to ASCII ../ under NFKC. While path.resolve/fs.writeFile treat these as
  // literal bytes (not separators), downstream layers or filesystems may
  // normalize — reject for defense-in-depth (PSR M22187 vector 4).
  const normalized = key.normalize('NFKC')
  if (
    normalized !== key &&
    (normalized.includes('..') ||
      normalized.includes('/') ||
      normalized.includes('\\') ||
      normalized.includes('\0'))
  ) {

```

---


### `src/memdir/teamMemPrompts.ts`

**信息:**
- 行数: 100
- 大小: 5998 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  buildSearchingPastContextSection,
  DIRS_EXIST_GUIDANCE,
  ENTRYPOINT_NAME,
  MAX_ENTRYPOINT_LINES,
} from './memdir.js'
import {
  MEMORY_DRIFT_CAVEAT,
  MEMORY_FRONTMATTER_EXAMPLE,
  TRUSTING_RECALL_SECTION,
  TYPES_SECTION_COMBINED,
  WHAT_NOT_TO_SAVE_SECTION,
} from './memoryTypes.js'
import { getAutoMemPath } from './paths.js'
import { getTeamMemPath } from './teamMemPaths.js'

/**
 * Build the combined prompt when both auto memory and team memory are enabled.
 * Closed four-type taxonomy (user / feedback / project / reference) with
 * per-type <scope> guidance embedded in XML-style <type> blocks.
 */
export function buildCombinedMemoryPrompt(
  extraGuidelines?: string[],
  skipIndex = false,
): string {
  const autoDir = getAutoMemPath()
  const teamDir = getTeamMemPath()

  const howToSave = skipIndex
    ? [
        '## How to save memories',
        '',
        "Write each memory to its own file in the chosen directory (private or team, per the type's scope guidance) using this frontmatter format:",
        '',
        ...MEMORY_FRONTMATTER_EXAMPLE,
        '',
        '- Keep the name, description, and type fields in memory files up-to-date with the content',
        '- Organize memory semantically by topic, not chronologically',
        '- Update or remove memories that turn out to be wrong or outdated',
        '- Do not write duplicate memories. First check if there is an existing memory you can update before writing a new one.',
      ]
    : [
        '## How to save memories',
        '',
        'Saving a memory is a two-step process:',
        '',
        "**Step 1** — write the memory to its own file in the chosen directory (private or team, per the type's scope guidance) using this frontmatter format:",
        '',
        ...MEMORY_FRONTMATTER_EXAMPLE,
        '',

```

---

