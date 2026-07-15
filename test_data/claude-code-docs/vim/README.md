# vim 模块

## 概述

**位置:** `src/vim/`

## 文件统计

- TypeScript 文件: 5
- TypeScript React 文件: 0
- 总计: 5

## 文件详情

---


### `src/vim/motions.ts`

**信息:**
- 行数: 82
- 大小: 1902 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Vim Motion Functions
 *
 * Pure functions for resolving vim motions to cursor positions.
 */

import type { Cursor } from '../utils/Cursor.js'

/**
 * Resolve a motion to a target cursor position.
 * Does not modify anything - pure calculation.
 */
export function resolveMotion(
  key: string,
  cursor: Cursor,
  count: number,
): Cursor {
  let result = cursor
  for (let i = 0; i < count; i++) {
    const next = applySingleMotion(key, result)
    if (next.equals(result)) break
    result = next
  }
  return result
}

/**
 * Apply a single motion step.
 */
function applySingleMotion(key: string, cursor: Cursor): Cursor {
  switch (key) {
    case 'h':
      return cursor.left()
    case 'l':
      return cursor.right()
    case 'j':
      return cursor.downLogicalLine()
    case 'k':
      return cursor.upLogicalLine()
    case 'gj':
      return cursor.down()
    case 'gk':
      return cursor.up()
    case 'w':
      return cursor.nextVimWord()
    case 'b':
      return cursor.prevVimWord()
    case 'e':
      return cursor.endOfVimWord()
    case 'W':

```

---


### `src/vim/operators.ts`

**信息:**
- 行数: 556
- 大小: 15966 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Vim Operator Functions
 *
 * Pure functions for executing vim operators (delete, change, yank, etc.)
 */

import { Cursor } from '../utils/Cursor.js'
import { firstGrapheme, lastGrapheme } from '../utils/intl.js'
import { countCharInString } from '../utils/stringUtils.js'
import {
  isInclusiveMotion,
  isLinewiseMotion,
  resolveMotion,
} from './motions.js'
import { findTextObject } from './textObjects.js'
import type {
  FindType,
  Operator,
  RecordedChange,
  TextObjScope,
} from './types.js'

/**
 * Context for operator execution.
 */
export type OperatorContext = {
  cursor: Cursor
  text: string
  setText: (text: string) => void
  setOffset: (offset: number) => void
  enterInsert: (offset: number) => void
  getRegister: () => string
  setRegister: (content: string, linewise: boolean) => void
  getLastFind: () => { type: FindType; char: string } | null
  setLastFind: (type: FindType, char: string) => void
  recordChange: (change: RecordedChange) => void
}

/**
 * Execute an operator with a simple motion.
 */
export function executeOperatorMotion(
  op: Operator,
  motion: string,
  count: number,
  ctx: OperatorContext,
): void {
  const target = resolveMotion(motion, ctx.cursor, count)
  if (target.equals(ctx.cursor)) return


```

---


### `src/vim/textObjects.ts`

**信息:**
- 行数: 186
- 大小: 5029 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Vim Text Object Finding
 *
 * Functions for finding text object boundaries (iw, aw, i", a(, etc.)
 */

import {
  isVimPunctuation,
  isVimWhitespace,
  isVimWordChar,
} from '../utils/Cursor.js'
import { getGraphemeSegmenter } from '../utils/intl.js'

export type TextObjectRange = { start: number; end: number } | null

/**
 * Delimiter pairs for text objects.
 */
const PAIRS: Record<string, [string, string]> = {
  '(': ['(', ')'],
  ')': ['(', ')'],
  b: ['(', ')'],
  '[': ['[', ']'],
  ']': ['[', ']'],
  '{': ['{', '}'],
  '}': ['{', '}'],
  B: ['{', '}'],
  '<': ['<', '>'],
  '>': ['<', '>'],
  '"': ['"', '"'],
  "'": ["'", "'"],
  '`': ['`', '`'],
}

/**
 * Find a text object at the given position.
 */
export function findTextObject(
  text: string,
  offset: number,
  objectType: string,
  isInner: boolean,
): TextObjectRange {
  if (objectType === 'w')
    return findWordObject(text, offset, isInner, isVimWordChar)
  if (objectType === 'W')
    return findWordObject(text, offset, isInner, ch => !isVimWhitespace(ch))

  const pair = PAIRS[objectType]
  if (pair) {

```

---


### `src/vim/transitions.ts`

**信息:**
- 行数: 490
- 大小: 12381 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Vim State Transition Table
 *
 * This is the scannable source of truth for state transitions.
 * To understand what happens in any state, look up that state's transition function.
 */

import { resolveMotion } from './motions.js'
import {
  executeIndent,
  executeJoin,
  executeLineOp,
  executeOpenLine,
  executeOperatorFind,
  executeOperatorG,
  executeOperatorGg,
  executeOperatorMotion,
  executeOperatorTextObj,
  executePaste,
  executeReplace,
  executeToggleCase,
  executeX,
  type OperatorContext,
} from './operators.js'
import {
  type CommandState,
  FIND_KEYS,
  type FindType,
  isOperatorKey,
  isTextObjScopeKey,
  MAX_VIM_COUNT,
  OPERATORS,
  type Operator,
  SIMPLE_MOTIONS,
  TEXT_OBJ_SCOPES,
  TEXT_OBJ_TYPES,
  type TextObjScope,
} from './types.js'

/**
 * Context passed to transition functions.
 */
export type TransitionContext = OperatorContext & {
  onUndo?: () => void
  onDotRepeat?: () => void
}

/**
 * Result of a transition.
 */

```

---


### `src/vim/types.ts`

**信息:**
- 行数: 199
- 大小: 6332 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Vim Mode State Machine Types
 *
 * This file defines the complete state machine for vim input handling.
 * The types ARE the documentation - reading them tells you how the system works.
 *
 * State Diagram:
 * ```
 *                              VimState
 *   ┌──────────────────────────────┬──────────────────────────────────────┐
 *   │  INSERT                      │  NORMAL                              │
 *   │  (tracks insertedText)       │  (CommandState machine)              │
 *   │                              │                                      │
 *   │                              │  idle ──┬─[d/c/y]──► operator        │
 *   │                              │         ├─[1-9]────► count           │
 *   │                              │         ├─[fFtT]───► find            │
 *   │                              │         ├─[g]──────► g               │
 *   │                              │         ├─[r]──────► replace         │
 *   │                              │         └─[><]─────► indent          │
 *   │                              │                                      │
 *   │                              │  operator ─┬─[motion]──► execute     │
 *   │                              │            ├─[0-9]────► operatorCount│
 *   │                              │            ├─[ia]─────► operatorTextObj
 *   │                              │            └─[fFtT]───► operatorFind │
 *   └──────────────────────────────┴──────────────────────────────────────┘
 * ```
 */

// ============================================================================
// Core Types
// ============================================================================

export type Operator = 'delete' | 'change' | 'yank'

export type FindType = 'f' | 'F' | 't' | 'T'

export type TextObjScope = 'inner' | 'around'

// ============================================================================
// State Machine Types
// ============================================================================

/**
 * Complete vim state. Mode determines what data is tracked.
 *
 * INSERT mode: Track text being typed (for dot-repeat)
 * NORMAL mode: Track command being parsed (state machine)
 */
export type VimState =
  | { mode: 'INSERT'; insertedText: string }

```

---

