# native-ts 模块

## 概述

**位置:** `src/native-ts/`

## 文件统计

- TypeScript 文件: 4
- TypeScript React 文件: 0
- 总计: 4

## 文件详情

---


### `src/native-ts/color-diff/index.ts`

**信息:**
- 行数: 999
- 大小: 30042 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Pure TypeScript port of vendor/color-diff-src.
 *
 * The Rust version uses syntect+bat for syntax highlighting and the similar
 * crate for word diffing. This port uses highlight.js (already a dep via
 * cli-highlight) and the diff npm package's diffArrays.
 *
 * API matches vendor/color-diff-src/index.d.ts exactly so callers don't change.
 *
 * Key semantic differences from the native module:
 * - Syntax highlighting uses highlight.js. Scope colors were measured from
 *   syntect's output so most tokens match, but hljs's grammar has gaps:
 *   plain identifiers and operators like `=` `:` aren't scoped, so they
 *   render in default fg instead of white/pink. Output structure (line
 *   numbers, markers, backgrounds, word-diff) is identical.
 * - BAT_THEME env support is a stub: highlight.js has no bat theme set, so
 *   getSyntaxTheme always returns the default for the given Claude theme.
 */

import { diffArrays } from 'diff'
import type * as hljsNamespace from 'highlight.js'
import { basename, extname } from 'path'

// Lazy: defers loading highlight.js until first render. The full bundle
// registers 190+ language grammars at require time (~50MB, 100-200ms on
// macOS, several× that on Windows). With a top-level import, any caller
// chunk that reaches this module — including test/preload.ts via
// StructuredDiff.tsx → colorDiff.ts — pays that cost at module-eval time
// and carries the heap for the rest of the process. On Windows CI this
// pushed later tests in the same shard into GC-pause territory and a
// beforeEach/afterEach hook timeout (officialRegistry.test.ts, PR #24150).
// Same lazy pattern the NAPI wrapper used for dlopen.
type HLJSApi = typeof hljsNamespace
let cachedHljs: HLJSApi | null = null
function hljs(): HLJSApi {
  if (cachedHljs) return cachedHljs
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const mod = require('highlight.js')
  // highlight.js uses `export =` (CJS). Under bun/ESM the interop wraps it
  // in .default; under node CJS the module IS the API. Check at runtime.
  cachedHljs = 'default' in mod && mod.default ? mod.default : mod
  return cachedHljs!
}

import { stringWidth } from '../../ink/stringWidth.js'
import { logError } from '../../utils/log.js'

// ---------------------------------------------------------------------------
// Public API types (match vendor/color-diff-src/index.d.ts)
// ---------------------------------------------------------------------------

```

---


### `src/native-ts/file-index/index.ts`

**信息:**
- 行数: 370
- 大小: 12006 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Pure-TypeScript port of vendor/file-index-src (Rust NAPI module).
 *
 * The native module wraps nucleo (https://github.com/helix-editor/nucleo) for
 * high-performance fuzzy file searching. This port reimplements the same API
 * and scoring behavior without native dependencies.
 *
 * Key API:
 *   new FileIndex()
 *   .loadFromFileList(fileList: string[]): void   — dedupe + index paths
 *   .search(query: string, limit: number): SearchResult[]
 *
 * Score semantics: lower = better. Score is position-in-results / result-count,
 * so the best match is 0.0. Paths containing "test" get a 1.05× penalty (capped
 * at 1.0) so non-test files rank slightly higher.
 */

export type SearchResult = {
  path: string
  score: number
}

// nucleo-style scoring constants (approximating fzf-v2 / nucleo bonuses)
const SCORE_MATCH = 16
const BONUS_BOUNDARY = 8
const BONUS_CAMEL = 6
const BONUS_CONSECUTIVE = 4
const BONUS_FIRST_CHAR = 8
const PENALTY_GAP_START = 3
const PENALTY_GAP_EXTENSION = 1

const TOP_LEVEL_CACHE_LIMIT = 100
const MAX_QUERY_LEN = 64
// Yield to event loop after this many ms of sync work. Chunk sizes are
// time-based (not count-based) so slow machines get smaller chunks and
// stay responsive — 5k paths is ~2ms on M-series but could be 15ms+ on
// older Windows hardware.
const CHUNK_MS = 4

// Reusable buffer: records where each needle char matched during the indexOf scan
const posBuf = new Int32Array(MAX_QUERY_LEN)

export class FileIndex {
  private paths: string[] = []
  private lowerPaths: string[] = []
  private charBits: Int32Array = new Int32Array(0)
  private pathLens: Uint16Array = new Uint16Array(0)
  private topLevelCache: SearchResult[] | null = null
  // During async build, tracks how many paths have bitmap/lowerPath filled.
  // search() uses this to search the ready prefix while build continues.

```

---


### `src/native-ts/yoga-layout/enums.ts`

**信息:**
- 行数: 134
- 大小: 2823 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Yoga enums — ported from yoga-layout/src/generated/YGEnums.ts
 * Kept as `const` objects (not TS enums) per repo convention.
 * Values match upstream exactly so callers don't change.
 */

export const Align = {
  Auto: 0,
  FlexStart: 1,
  Center: 2,
  FlexEnd: 3,
  Stretch: 4,
  Baseline: 5,
  SpaceBetween: 6,
  SpaceAround: 7,
  SpaceEvenly: 8,
} as const
export type Align = (typeof Align)[keyof typeof Align]

export const BoxSizing = {
  BorderBox: 0,
  ContentBox: 1,
} as const
export type BoxSizing = (typeof BoxSizing)[keyof typeof BoxSizing]

export const Dimension = {
  Width: 0,
  Height: 1,
} as const
export type Dimension = (typeof Dimension)[keyof typeof Dimension]

export const Direction = {
  Inherit: 0,
  LTR: 1,
  RTL: 2,
} as const
export type Direction = (typeof Direction)[keyof typeof Direction]

export const Display = {
  Flex: 0,
  None: 1,
  Contents: 2,
} as const
export type Display = (typeof Display)[keyof typeof Display]

export const Edge = {
  Left: 0,
  Top: 1,
  Right: 2,
  Bottom: 3,

```

---


### `src/native-ts/yoga-layout/index.ts`

**信息:**
- 行数: 2578
- 大小: 83377 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Pure-TypeScript port of yoga-layout (Meta's flexbox engine).
 *
 * This matches the `yoga-layout/load` API surface used by src/ink/layout/yoga.ts.
 * The upstream C++ source is ~2500 lines in CalculateLayout.cpp alone; this port
 * is a simplified single-pass flexbox implementation that covers the subset of
 * features Ink actually uses:
 *   - flex-direction (row/column + reverse)
 *   - flex-grow / flex-shrink / flex-basis
 *   - align-items / align-self (stretch, flex-start, center, flex-end)
 *   - justify-content (all six values)
 *   - margin / padding / border / gap
 *   - width / height / min / max (point, percent, auto)
 *   - position: relative / absolute
 *   - display: flex / none
 *   - measure functions (for text nodes)
 *
 * Also implemented for spec parity (not used by Ink):
 *   - margin: auto (main + cross axis, overrides justify/align)
 *   - multi-pass flex clamping when children hit min/max constraints
 *   - flex-grow/shrink against container min/max when size is indefinite
 *
 * Also implemented for spec parity (not used by Ink):
 *   - flex-wrap: wrap / wrap-reverse (multi-line flex)
 *   - align-content (positions wrapped lines on cross axis)
 *
 * Also implemented for spec parity (not used by Ink):
 *   - display: contents (children lifted to grandparent, box removed)
 *
 * Also implemented for spec parity (not used by Ink):
 *   - baseline alignment (align-items/align-self: baseline)
 *
 * Not implemented (not used by Ink):
 *   - aspect-ratio
 *   - box-sizing: content-box
 *   - RTL direction (Ink always passes Direction.LTR)
 *
 * Upstream: https://github.com/facebook/yoga
 */

import {
  Align,
  BoxSizing,
  Dimension,
  Direction,
  Display,
  Edge,
  Errata,
  ExperimentalFeature,
  FlexDirection,

```

---

