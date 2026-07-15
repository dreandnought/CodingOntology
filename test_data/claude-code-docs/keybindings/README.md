# keybindings 模块

## 概述

**位置:** `src/keybindings/`

## 文件统计

- TypeScript 文件: 13
- TypeScript React 文件: 2
- 总计: 15

## 文件详情

---


### `src/keybindings/KeybindingContext.tsx`

**信息:**
- 行数: 243
- 大小: 26000 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, type RefObject, useContext, useLayoutEffect, useMemo } from 'react';
import type { Key } from '../ink.js';
import { type ChordResolveResult, getBindingDisplayText, resolveKeyWithChordState } from './resolver.js';
import type { KeybindingContextName, ParsedBinding, ParsedKeystroke } from './types.js';

/** Handler registration for action callbacks */
type HandlerRegistration = {
  action: string;
  context: KeybindingContextName;
  handler: () => void;
};
type KeybindingContextValue = {
  /** Resolve a key input to an action name (with chord support) */
  resolve: (input: string, key: Key, activeContexts: KeybindingContextName[]) => ChordResolveResult;

  /** Update the pending chord state */
  setPendingChord: (pending: ParsedKeystroke[] | null) => void;

  /** Get display text for an action (e.g., "ctrl+t") */
  getDisplayText: (action: string, context: KeybindingContextName) => string | undefined;

  /** All parsed bindings (for help display) */
  bindings: ParsedBinding[];

  /** Current pending chord keystrokes (null if not in a chord) */
  pendingChord: ParsedKeystroke[] | null;

  /** Currently active keybinding contexts (for priority resolution) */
  activeContexts: Set<KeybindingContextName>;

  /** Register a context as active (call on mount) */
  registerActiveContext: (context: KeybindingContextName) => void;

  /** Unregister a context (call on unmount) */
  unregisterActiveContext: (context: KeybindingContextName) => void;

  /** Register a handler for an action (used by useKeybinding) */
  registerHandler: (registration: HandlerRegistration) => () => void;

  /** Invoke all handlers for an action (used by ChordInterceptor) */
  invokeAction: (action: string) => boolean;
};
const KeybindingContext = createContext<KeybindingContextValue | null>(null);
type ProviderProps = {
  bindings: ParsedBinding[];
  /** Ref for immediate access to pending chord (avoids React state delay) */
  pendingChordRef: RefObject<ParsedKeystroke[] | null>;
  /** State value for re-renders (UI updates) */
  pendingChord: ParsedKeystroke[] | null;

```

---


### `src/keybindings/KeybindingProviderSetup.tsx`

**信息:**
- 行数: 308
- 大小: 41452 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * Setup utilities for integrating KeybindingProvider into the app.
 *
 * This file provides the bindings and a composed provider that can be
 * added to the app's component tree. It loads both default bindings and
 * user-defined bindings from ~/.claude/keybindings.json, with hot-reload
 * support when the file changes.
 */
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useNotifications } from '../context/notifications.js';
import type { InputEvent } from '../ink/events/input-event.js';
// ChordInterceptor intentionally uses useInput to intercept all keystrokes before
// other handlers process them - this is required for chord sequence support
// eslint-disable-next-line custom-rules/prefer-use-keybindings
import { type Key, useInput } from '../ink.js';
import { count } from '../utils/array.js';
import { logForDebugging } from '../utils/debug.js';
import { plural } from '../utils/stringUtils.js';
import { KeybindingProvider } from './KeybindingContext.js';
import { initializeKeybindingWatcher, type KeybindingsLoadResult, loadKeybindingsSyncWithWarnings, subscribeToKeybindingChanges } from './loadUserBindings.js';
import { resolveKeyWithChordState } from './resolver.js';
import type { KeybindingContextName, ParsedBinding, ParsedKeystroke } from './types.js';
import type { KeybindingWarning } from './validate.js';

/**
 * Timeout for chord sequences in milliseconds.
 * If the user doesn't complete the chord within this time, it's cancelled.
 */
const CHORD_TIMEOUT_MS = 1000;
type Props = {
  children: React.ReactNode;
};

/**
 * Keybinding provider with default + user bindings and hot-reload support.
 *
 * Usage: Wrap your app with this provider to enable keybinding support.
 *
 * ```tsx
 * <AppStateProvider>
 *   <KeybindingSetup>
 *     <REPL ... />
 *   </KeybindingSetup>
 * </AppStateProvider>
 * ```
 *
 * Features:
 * - Loads default bindings from code
 * - Merges with user bindings from ~/.claude/keybindings.json

```

---


### `src/keybindings/defaultBindings.ts`

**信息:**
- 行数: 340
- 大小: 11635 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { satisfies } from 'src/utils/semver.js'
import { isRunningWithBun } from '../utils/bundledMode.js'
import { getPlatform } from '../utils/platform.js'
import type { KeybindingBlock } from './types.js'

/**
 * Default keybindings that match current Claude Code behavior.
 * These are loaded first, then user keybindings.json overrides them.
 */

// Platform-specific image paste shortcut:
// - Windows: alt+v (ctrl+v is system paste)
// - Other platforms: ctrl+v
const IMAGE_PASTE_KEY = getPlatform() === 'windows' ? 'alt+v' : 'ctrl+v'

// Modifier-only chords (like shift+tab) may fail on Windows Terminal without VT mode
// See: https://github.com/microsoft/terminal/issues/879#issuecomment-618801651
// Node enabled VT mode in 24.2.0 / 22.17.0: https://github.com/nodejs/node/pull/58358
// Bun enabled VT mode in 1.2.23: https://github.com/oven-sh/bun/pull/21161
const SUPPORTS_TERMINAL_VT_MODE =
  getPlatform() !== 'windows' ||
  (isRunningWithBun()
    ? satisfies(process.versions.bun, '>=1.2.23')
    : satisfies(process.versions.node, '>=22.17.0 <23.0.0 || >=24.2.0'))

// Platform-specific mode cycle shortcut:
// - Windows without VT mode: meta+m (shift+tab doesn't work reliably)
// - Other platforms: shift+tab
const MODE_CYCLE_KEY = SUPPORTS_TERMINAL_VT_MODE ? 'shift+tab' : 'meta+m'

export const DEFAULT_BINDINGS: KeybindingBlock[] = [
  {
    context: 'Global',
    bindings: {
      // ctrl+c and ctrl+d use special time-based double-press handling.
      // They ARE defined here so the resolver can find them, but they
      // CANNOT be rebound by users - validation in reservedShortcuts.ts
      // will show an error if users try to override these keys.
      'ctrl+c': 'app:interrupt',
      'ctrl+d': 'app:exit',
      'ctrl+l': 'app:redraw',
      'ctrl+t': 'app:toggleTodos',
      'ctrl+o': 'app:toggleTranscript',
      ...(feature('KAIROS') || feature('KAIROS_BRIEF')
        ? { 'ctrl+shift+b': 'app:toggleBrief' as const }
        : {}),
      'ctrl+shift+o': 'app:toggleTeammatePreview',
      'ctrl+r': 'history:search',
      // File navigation. cmd+ bindings only fire on kitty-protocol terminals;

```

---


### `src/keybindings/loadUserBindings.ts`

**信息:**
- 行数: 472
- 大小: 14551 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * User keybinding configuration loader with hot-reload support.
 *
 * Loads keybindings from ~/.claude/keybindings.json and watches
 * for changes to reload them automatically.
 *
 * NOTE: User keybinding customization is currently only available for
 * Anthropic employees (USER_TYPE === 'ant'). External users always
 * use the default bindings.
 */

import chokidar, { type FSWatcher } from 'chokidar'
import { readFileSync } from 'fs'
import { readFile, stat } from 'fs/promises'
import { dirname, join } from 'path'
import { getFeatureValue_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js'
import { logEvent } from '../services/analytics/index.js'
import { registerCleanup } from '../utils/cleanupRegistry.js'
import { logForDebugging } from '../utils/debug.js'
import { getClaudeConfigHomeDir } from '../utils/envUtils.js'
import { errorMessage, isENOENT } from '../utils/errors.js'
import { createSignal } from '../utils/signal.js'
import { jsonParse } from '../utils/slowOperations.js'
import { DEFAULT_BINDINGS } from './defaultBindings.js'
import { parseBindings } from './parser.js'
import type { KeybindingBlock, ParsedBinding } from './types.js'
import {
  checkDuplicateKeysInJson,
  type KeybindingWarning,
  validateBindings,
} from './validate.js'

/**
 * Check if keybinding customization is enabled.
 *
 * Returns true if the tengu_keybinding_customization_release GrowthBook gate is enabled.
 *
 * This function is exported so other parts of the codebase (e.g., /doctor)
 * can check the same condition consistently.
 */
export function isKeybindingCustomizationEnabled(): boolean {
  return getFeatureValue_CACHED_MAY_BE_STALE(
    'tengu_keybinding_customization_release',
    false,
  )
}

/**
 * Time in milliseconds to wait for file writes to stabilize.
 */

```

---


### `src/keybindings/match.ts`

**信息:**
- 行数: 120
- 大小: 3797 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Key } from '../ink.js'
import type { ParsedBinding, ParsedKeystroke } from './types.js'

/**
 * Modifier keys from Ink's Key type that we care about for matching.
 * Note: `fn` from Key is intentionally excluded as it's rarely used and
 * not commonly configurable in terminal applications.
 */
type InkModifiers = Pick<Key, 'ctrl' | 'shift' | 'meta' | 'super'>

/**
 * Extract modifiers from an Ink Key object.
 * This function ensures we're explicitly extracting the modifiers we care about.
 */
function getInkModifiers(key: Key): InkModifiers {
  return {
    ctrl: key.ctrl,
    shift: key.shift,
    meta: key.meta,
    super: key.super,
  }
}

/**
 * Extract the normalized key name from Ink's Key + input.
 * Maps Ink's boolean flags (key.escape, key.return, etc.) to string names
 * that match our ParsedKeystroke.key format.
 */
export function getKeyName(input: string, key: Key): string | null {
  if (key.escape) return 'escape'
  if (key.return) return 'enter'
  if (key.tab) return 'tab'
  if (key.backspace) return 'backspace'
  if (key.delete) return 'delete'
  if (key.upArrow) return 'up'
  if (key.downArrow) return 'down'
  if (key.leftArrow) return 'left'
  if (key.rightArrow) return 'right'
  if (key.pageUp) return 'pageup'
  if (key.pageDown) return 'pagedown'
  if (key.wheelUp) return 'wheelup'
  if (key.wheelDown) return 'wheeldown'
  if (key.home) return 'home'
  if (key.end) return 'end'
  if (input.length === 1) return input.toLowerCase()
  return null
}

/**
 * Check if all modifiers match between Ink Key and ParsedKeystroke.

```

---


### `src/keybindings/parser.ts`

**信息:**
- 行数: 203
- 大小: 4972 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type {
  Chord,
  KeybindingBlock,
  ParsedBinding,
  ParsedKeystroke,
} from './types.js'

/**
 * Parse a keystroke string like "ctrl+shift+k" into a ParsedKeystroke.
 * Supports various modifier aliases (ctrl/control, alt/opt/option/meta,
 * cmd/command/super/win).
 */
export function parseKeystroke(input: string): ParsedKeystroke {
  const parts = input.split('+')
  const keystroke: ParsedKeystroke = {
    key: '',
    ctrl: false,
    alt: false,
    shift: false,
    meta: false,
    super: false,
  }
  for (const part of parts) {
    const lower = part.toLowerCase()
    switch (lower) {
      case 'ctrl':
      case 'control':
        keystroke.ctrl = true
        break
      case 'alt':
      case 'opt':
      case 'option':
        keystroke.alt = true
        break
      case 'shift':
        keystroke.shift = true
        break
      case 'meta':
        keystroke.meta = true
        break
      case 'cmd':
      case 'command':
      case 'super':
      case 'win':
        keystroke.super = true
        break
      case 'esc':
        keystroke.key = 'escape'
        break
      case 'return':

```

---


### `src/keybindings/reservedShortcuts.ts`

**信息:**
- 行数: 127
- 大小: 3610 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { getPlatform } from '../utils/platform.js'

/**
 * Shortcuts that are typically intercepted by the OS, terminal, or shell
 * and will likely never reach the application.
 */
export type ReservedShortcut = {
  key: string
  reason: string
  severity: 'error' | 'warning'
}

/**
 * Shortcuts that cannot be rebound - they are hardcoded in Claude Code.
 */
export const NON_REBINDABLE: ReservedShortcut[] = [
  {
    key: 'ctrl+c',
    reason: 'Cannot be rebound - used for interrupt/exit (hardcoded)',
    severity: 'error',
  },
  {
    key: 'ctrl+d',
    reason: 'Cannot be rebound - used for exit (hardcoded)',
    severity: 'error',
  },
  {
    key: 'ctrl+m',
    reason:
      'Cannot be rebound - identical to Enter in terminals (both send CR)',
    severity: 'error',
  },
]

/**
 * Terminal control shortcuts that are intercepted by the terminal/OS.
 * These will likely never reach the application.
 *
 * Note: ctrl+s (XOFF) and ctrl+q (XON) are NOT included here because:
 * - Most modern terminals disable flow control by default
 * - We use ctrl+s for the stash feature
 */
export const TERMINAL_RESERVED: ReservedShortcut[] = [
  {
    key: 'ctrl+z',
    reason: 'Unix process suspend (SIGTSTP)',
    severity: 'warning',
  },
  {
    key: 'ctrl+\\',

```

---


### `src/keybindings/resolver.ts`

**信息:**
- 行数: 244
- 大小: 7087 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Key } from '../ink.js'
import { getKeyName, matchesBinding } from './match.js'
import { chordToString } from './parser.js'
import type {
  KeybindingContextName,
  ParsedBinding,
  ParsedKeystroke,
} from './types.js'

export type ResolveResult =
  | { type: 'match'; action: string }
  | { type: 'none' }
  | { type: 'unbound' }

export type ChordResolveResult =
  | { type: 'match'; action: string }
  | { type: 'none' }
  | { type: 'unbound' }
  | { type: 'chord_started'; pending: ParsedKeystroke[] }
  | { type: 'chord_cancelled' }

/**
 * Resolve a key input to an action.
 * Pure function - no state, no side effects, just matching logic.
 *
 * @param input - The character input from Ink
 * @param key - The Key object from Ink with modifier flags
 * @param activeContexts - Array of currently active contexts (e.g., ['Chat', 'Global'])
 * @param bindings - All parsed bindings to search through
 * @returns The resolution result
 */
export function resolveKey(
  input: string,
  key: Key,
  activeContexts: KeybindingContextName[],
  bindings: ParsedBinding[],
): ResolveResult {
  // Find matching bindings (last one wins for user overrides)
  let match: ParsedBinding | undefined
  const ctxSet = new Set(activeContexts)

  for (const binding of bindings) {
    // Phase 1: Only single-keystroke bindings
    if (binding.chord.length !== 1) continue
    if (!ctxSet.has(binding.context)) continue

    if (matchesBinding(input, key, binding)) {
      match = binding
    }
  }

```

---


### `src/keybindings/schema.ts`

**信息:**
- 行数: 236
- 大小: 6269 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Zod schema for keybindings.json configuration.
 * Used for validation and JSON schema generation.
 */

import { z } from 'zod/v4'
import { lazySchema } from '../utils/lazySchema.js'

/**
 * Valid context names where keybindings can be applied.
 */
export const KEYBINDING_CONTEXTS = [
  'Global',
  'Chat',
  'Autocomplete',
  'Confirmation',
  'Help',
  'Transcript',
  'HistorySearch',
  'Task',
  'ThemePicker',
  'Settings',
  'Tabs',
  // New contexts for keybindings migration
  'Attachments',
  'Footer',
  'MessageSelector',
  'DiffDialog',
  'ModelPicker',
  'Select',
  'Plugin',
] as const

/**
 * Human-readable descriptions for each keybinding context.
 */
export const KEYBINDING_CONTEXT_DESCRIPTIONS: Record<
  (typeof KEYBINDING_CONTEXTS)[number],
  string
> = {
  Global: 'Active everywhere, regardless of focus',
  Chat: 'When the chat input is focused',
  Autocomplete: 'When autocomplete menu is visible',
  Confirmation: 'When a confirmation/permission dialog is shown',
  Help: 'When the help overlay is open',
  Transcript: 'When viewing the transcript',
  HistorySearch: 'When searching command history (ctrl+r)',
  Task: 'When a task/agent is running in the foreground',
  ThemePicker: 'When the theme picker is open',
  Settings: 'When the settings menu is open',

```

---


### `src/keybindings/shortcutFormat.ts`

**信息:**
- 行数: 63
- 大小: 2575 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import { loadKeybindingsSync } from './loadUserBindings.js'
import { getBindingDisplayText } from './resolver.js'
import type { KeybindingContextName } from './types.js'

// TODO(keybindings-migration): Remove fallback parameter after migration is
// complete and we've confirmed no 'keybinding_fallback_used' events are being
// logged. The fallback exists as a safety net during migration - if bindings
// fail to load or an action isn't found, we fall back to hardcoded values.
// Once stable, callers should be able to trust that getBindingDisplayText
// always returns a value for known actions, and we can remove this defensive
// pattern.

// Track which action+context pairs have already logged a fallback event
// to avoid duplicate events from repeated calls in non-React contexts.
const LOGGED_FALLBACKS = new Set<string>()

/**
 * Get the display text for a configured shortcut without React hooks.
 * Use this in non-React contexts (commands, services, etc.).
 *
 * This lives in its own module (not useShortcutDisplay.ts) so that
 * non-React callers like query/stopHooks.ts don't pull React into their
 * module graph via the sibling hook.
 *
 * @param action - The action name (e.g., 'app:toggleTranscript')
 * @param context - The keybinding context (e.g., 'Global')
 * @param fallback - Fallback text if binding not found
 * @returns The configured shortcut display text
 *
 * @example
 * const expandShortcut = getShortcutDisplay('app:toggleTranscript', 'Global', 'ctrl+o')
 * // Returns the user's configured binding, or 'ctrl+o' as default
 */
export function getShortcutDisplay(
  action: string,
  context: KeybindingContextName,
  fallback: string,
): string {
  const bindings = loadKeybindingsSync()
  const resolved = getBindingDisplayText(action, context, bindings)
  if (resolved === undefined) {
    const key = `${action}:${context}`
    if (!LOGGED_FALLBACKS.has(key)) {
      LOGGED_FALLBACKS.add(key)
      logEvent('tengu_keybinding_fallback_used', {
        action:

```

---


### `src/keybindings/template.ts`

**信息:**
- 行数: 52
- 大小: 1721 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Keybindings template generator.
 * Generates a well-documented template file for ~/.claude/keybindings.json
 */

import { jsonStringify } from '../utils/slowOperations.js'
import { DEFAULT_BINDINGS } from './defaultBindings.js'
import {
  NON_REBINDABLE,
  normalizeKeyForComparison,
} from './reservedShortcuts.js'
import type { KeybindingBlock } from './types.js'

/**
 * Filter out reserved shortcuts that cannot be rebound.
 * These would cause /doctor to warn, so we exclude them from the template.
 */
function filterReservedShortcuts(blocks: KeybindingBlock[]): KeybindingBlock[] {
  const reservedKeys = new Set(
    NON_REBINDABLE.map(r => normalizeKeyForComparison(r.key)),
  )

  return blocks
    .map(block => {
      const filteredBindings: Record<string, string | null> = {}
      for (const [key, action] of Object.entries(block.bindings)) {
        if (!reservedKeys.has(normalizeKeyForComparison(key))) {
          filteredBindings[key] = action
        }
      }
      return { context: block.context, bindings: filteredBindings }
    })
    .filter(block => Object.keys(block.bindings).length > 0)
}

/**
 * Generate a template keybindings.json file content.
 * Creates a fully valid JSON file with all default bindings that users can customize.
 */
export function generateKeybindingsTemplate(): string {
  // Filter out reserved shortcuts that cannot be rebound
  const bindings = filterReservedShortcuts(DEFAULT_BINDINGS)

  // Format as object wrapper with bindings array
  const config = {
    $schema: 'https://www.schemastore.org/claude-code-keybindings.json',
    $docs: 'https://code.claude.com/docs/en/keybindings',
    bindings,
  }


```

---


### `src/keybindings/types.ts`

**信息:**
- 行数: 17
- 大小: 370 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type KeybindingContextName = string
export type KeybindingAction = string
export type ParsedKeystroke = {
  key?: string
  ctrl?: boolean
  alt?: boolean
  shift?: boolean
  meta?: boolean
}
export type ParsedBinding = {
  action: string
  keys: ParsedKeystroke[]
}
export type KeybindingBlock = {
  context?: KeybindingContextName
  bindings?: ParsedBinding[]
}

```

---


### `src/keybindings/useKeybinding.ts`

**信息:**
- 行数: 196
- 大小: 6862 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useEffect } from 'react'
import type { InputEvent } from '../ink/events/input-event.js'
import { type Key, useInput } from '../ink.js'
import { useOptionalKeybindingContext } from './KeybindingContext.js'
import type { KeybindingContextName } from './types.js'

type Options = {
  /** Which context this binding belongs to (default: 'Global') */
  context?: KeybindingContextName
  /** Only handle when active (like useInput's isActive) */
  isActive?: boolean
}

/**
 * Ink-native hook for handling a keybinding.
 *
 * The handler stays in the component (React way).
 * The binding (keystroke → action) comes from config.
 *
 * Supports chord sequences (e.g., "ctrl+k ctrl+s"). When a chord is started,
 * the hook will manage the pending state automatically.
 *
 * Uses stopImmediatePropagation() to prevent other handlers from firing
 * once this binding is handled.
 *
 * @example
 * ```tsx
 * useKeybinding('app:toggleTodos', () => {
 *   setShowTodos(prev => !prev)
 * }, { context: 'Global' })
 * ```
 */
export function useKeybinding(
  action: string,
  handler: () => void | false | Promise<void>,
  options: Options = {},
): void {
  const { context = 'Global', isActive = true } = options
  const keybindingContext = useOptionalKeybindingContext()

  // Register handler with the context for ChordInterceptor to invoke
  useEffect(() => {
    if (!keybindingContext || !isActive) return
    return keybindingContext.registerHandler({ action, context, handler })
  }, [action, context, handler, keybindingContext, isActive])

  const handleInput = useCallback(
    (input: string, key: Key, event: InputEvent) => {
      // If no keybinding context available, skip resolution
      if (!keybindingContext) return

```

---


### `src/keybindings/useShortcutDisplay.ts`

**信息:**
- 行数: 59
- 大小: 2510 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useRef } from 'react'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import { useOptionalKeybindingContext } from './KeybindingContext.js'
import type { KeybindingContextName } from './types.js'

// TODO(keybindings-migration): Remove fallback parameter after migration is complete
// and we've confirmed no 'keybinding_fallback_used' events are being logged.
// The fallback exists as a safety net during migration - if bindings fail to load
// or an action isn't found, we fall back to hardcoded values. Once stable, callers
// should be able to trust that getBindingDisplayText always returns a value for
// known actions, and we can remove this defensive pattern.

/**
 * Hook to get the display text for a configured shortcut.
 * Returns the configured binding or a fallback if unavailable.
 *
 * @param action - The action name (e.g., 'app:toggleTranscript')
 * @param context - The keybinding context (e.g., 'Global')
 * @param fallback - Fallback text if keybinding context unavailable
 * @returns The configured shortcut display text
 *
 * @example
 * const expandShortcut = useShortcutDisplay('app:toggleTranscript', 'Global', 'ctrl+o')
 * // Returns the user's configured binding, or 'ctrl+o' as default
 */
export function useShortcutDisplay(
  action: string,
  context: KeybindingContextName,
  fallback: string,
): string {
  const keybindingContext = useOptionalKeybindingContext()
  const resolved = keybindingContext?.getDisplayText(action, context)
  const isFallback = resolved === undefined
  const reason = keybindingContext ? 'action_not_found' : 'no_context'

  // Log fallback usage once per mount (not on every render) to avoid
  // flooding analytics with events from frequent re-renders.
  const hasLoggedRef = useRef(false)
  useEffect(() => {
    if (isFallback && !hasLoggedRef.current) {
      hasLoggedRef.current = true
      logEvent('tengu_keybinding_fallback_used', {
        action:
          action as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
        context:
          context as AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
        fallback:

```

---


### `src/keybindings/validate.ts`

**信息:**
- 行数: 498
- 大小: 13667 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { plural } from '../utils/stringUtils.js'
import { chordToString, parseChord, parseKeystroke } from './parser.js'
import {
  getReservedShortcuts,
  normalizeKeyForComparison,
} from './reservedShortcuts.js'
import type {
  KeybindingBlock,
  KeybindingContextName,
  ParsedBinding,
} from './types.js'

/**
 * Types of validation issues that can occur with keybindings.
 */
export type KeybindingWarningType =
  | 'parse_error'
  | 'duplicate'
  | 'reserved'
  | 'invalid_context'
  | 'invalid_action'

/**
 * A warning or error about a keybinding configuration issue.
 */
export type KeybindingWarning = {
  type: KeybindingWarningType
  severity: 'error' | 'warning'
  message: string
  key?: string
  context?: string
  action?: string
  suggestion?: string
}

/**
 * Type guard to check if an object is a valid KeybindingBlock.
 */
function isKeybindingBlock(obj: unknown): obj is KeybindingBlock {
  if (typeof obj !== 'object' || obj === null) return false
  const b = obj as Record<string, unknown>
  return (
    typeof b.context === 'string' &&
    typeof b.bindings === 'object' &&
    b.bindings !== null
  )
}

/**
 * Type guard to check if an array contains only valid KeybindingBlocks.

```

---

