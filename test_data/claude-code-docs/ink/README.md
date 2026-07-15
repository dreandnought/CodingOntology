# ink 模块

## 概述

**位置:** `src/ink/`

## 文件统计

- TypeScript 文件: 83
- TypeScript React 文件: 17
- 总计: 100

## 文件详情

---


### `src/ink/Ansi.tsx`

**信息:**
- 行数: 292
- 大小: 33264 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import Link from './components/Link.js';
import Text from './components/Text.js';
import type { Color } from './styles.js';
import { type NamedColor, Parser, type Color as TermioColor, type TextStyle } from './termio.js';
type Props = {
  children: string;
  /** When true, force all text to be rendered with dim styling */
  dimColor?: boolean;
};
type SpanProps = {
  color?: Color;
  backgroundColor?: Color;
  dim?: boolean;
  bold?: boolean;
  italic?: boolean;
  underline?: boolean;
  strikethrough?: boolean;
  inverse?: boolean;
  hyperlink?: string;
};

/**
 * Component that parses ANSI escape codes and renders them using Text components.
 *
 * Use this as an escape hatch when you have pre-formatted ANSI strings from
 * external tools (like cli-highlight) that need to be rendered in Ink.
 *
 * Memoized to prevent re-renders when parent changes but children string is the same.
 */
export const Ansi = React.memo(function Ansi(t0) {
  const $ = _c(12);
  const {
    children,
    dimColor
  } = t0;
  if (typeof children !== "string") {
    let t1;
    if ($[0] !== children || $[1] !== dimColor) {
      t1 = dimColor ? <Text dim={true}>{String(children)}</Text> : <Text>{String(children)}</Text>;
      $[0] = children;
      $[1] = dimColor;
      $[2] = t1;
    } else {
      t1 = $[2];
    }
    return t1;
  }
  if (children === "") {

```

---


### `src/ink/bidi.ts`

**信息:**
- 行数: 139
- 大小: 4290 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Bidirectional text reordering for terminal rendering.
 *
 * Terminals on Windows do not implement the Unicode Bidi Algorithm,
 * so RTL text (Hebrew, Arabic, etc.) appears reversed. This module
 * applies the bidi algorithm to reorder ClusteredChar arrays from
 * logical order to visual order before Ink's LTR cell placement loop.
 *
 * On macOS terminals (Terminal.app, iTerm2) bidi works natively.
 * Windows Terminal (including WSL) does not implement bidi
 * (https://github.com/microsoft/terminal/issues/538).
 *
 * Detection: Windows Terminal sets WT_SESSION; native Windows cmd/conhost
 * also lacks bidi. We enable bidi reordering when running on Windows or
 * inside Windows Terminal (covers WSL).
 */
import bidiFactory from 'bidi-js'

type ClusteredChar = {
  value: string
  width: number
  styleId: number
  hyperlink: string | undefined
}

let bidiInstance: ReturnType<typeof bidiFactory> | undefined
let needsSoftwareBidi: boolean | undefined

function needsBidi(): boolean {
  if (needsSoftwareBidi === undefined) {
    needsSoftwareBidi =
      process.platform === 'win32' ||
      typeof process.env['WT_SESSION'] === 'string' || // WSL in Windows Terminal
      process.env['TERM_PROGRAM'] === 'vscode' // VS Code integrated terminal (xterm.js)
  }
  return needsSoftwareBidi
}

function getBidi() {
  if (!bidiInstance) {
    bidiInstance = bidiFactory()
  }
  return bidiInstance
}

/**
 * Reorder an array of ClusteredChars from logical order to visual order
 * using the Unicode Bidi Algorithm. Active on terminals that lack native
 * bidi support (Windows Terminal, conhost, WSL).
 *

```

---


### `src/ink/clearTerminal.ts`

**信息:**
- 行数: 74
- 大小: 1901 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Cross-platform terminal clearing with scrollback support.
 * Detects modern terminals that support ESC[3J for clearing scrollback.
 */

import {
  CURSOR_HOME,
  csi,
  ERASE_SCREEN,
  ERASE_SCROLLBACK,
} from './termio/csi.js'

// HVP (Horizontal Vertical Position) - legacy Windows cursor home
const CURSOR_HOME_WINDOWS = csi(0, 'f')

function isWindowsTerminal(): boolean {
  return process.platform === 'win32' && !!process.env.WT_SESSION
}

function isMintty(): boolean {
  // mintty 3.1.5+ sets TERM_PROGRAM to 'mintty'
  if (process.env.TERM_PROGRAM === 'mintty') {
    return true
  }
  // GitBash/MSYS2/MINGW use mintty and set MSYSTEM
  if (process.platform === 'win32' && process.env.MSYSTEM) {
    return true
  }
  return false
}

function isModernWindowsTerminal(): boolean {
  // Windows Terminal sets WT_SESSION environment variable
  if (isWindowsTerminal()) {
    return true
  }

  // VS Code integrated terminal on Windows with ConPTY support
  if (
    process.platform === 'win32' &&
    process.env.TERM_PROGRAM === 'vscode' &&
    process.env.TERM_PROGRAM_VERSION
  ) {
    return true
  }

  // mintty (GitBash/MSYS2/Cygwin) supports modern escape sequences
  if (isMintty()) {
    return true
  }

```

---


### `src/ink/colorize.ts`

**信息:**
- 行数: 231
- 大小: 7647 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import chalk from 'chalk'
import type { Color, TextStyles } from './styles.js'

/**
 * xterm.js (VS Code, Cursor, code-server, Coder) has supported truecolor
 * since 2017, but code-server/Coder containers often don't set
 * COLORTERM=truecolor. chalk's supports-color doesn't recognize
 * TERM_PROGRAM=vscode (it only knows iTerm.app/Apple_Terminal), so it falls
 * through to the -256color regex → level 2. At level 2, chalk.rgb()
 * downgrades to the nearest 6×6×6 cube color: rgb(215,119,87) (Claude
 * orange) → idx 174 rgb(215,135,135) — washed-out salmon.
 *
 * Gated on level === 2 (not < 3) to respect NO_COLOR / FORCE_COLOR=0 —
 * those yield level 0 and are an explicit "no colors" request. Desktop VS
 * Code sets COLORTERM=truecolor itself, so this is a no-op there (already 3).
 *
 * Must run BEFORE the tmux clamp — if tmux is running inside a VS Code
 * terminal, tmux's passthrough limitation wins and we want level 2.
 */
function boostChalkLevelForXtermJs(): boolean {
  if (process.env.TERM_PROGRAM === 'vscode' && chalk.level === 2) {
    chalk.level = 3
    return true
  }
  return false
}

/**
 * tmux parses truecolor SGR (\e[48;2;r;g;bm) into its cell buffer correctly,
 * but its client-side emitter only re-emits truecolor to the outer terminal if
 * the outer terminal advertises Tc/RGB capability (via terminal-overrides).
 * Default tmux config doesn't set this, so tmux emits the cell to iTerm2/etc
 * WITHOUT the bg sequence — outer terminal's buffer has bg=default → black on
 * dark profiles. Clamping to level 2 makes chalk emit 256-color (\e[48;5;Nm),
 * which tmux passes through cleanly. grey93 (255) is visually identical to
 * rgb(240,240,240).
 *
 * Users who HAVE set `terminal-overrides ,*:Tc` get a technically-unnecessary
 * downgrade, but the visual difference is imperceptible. Querying
 * `tmux show -gv terminal-overrides` to detect this would add a subprocess on
 * startup — not worth it.
 *
 * $TMUX is a pty-lifecycle env var set by tmux itself; it never comes from
 * globalSettings.env, so reading it here is correct. chalk is a singleton, so
 * this clamps ALL truecolor output (fg+bg+hex) across the entire app.
 */
function clampChalkLevelForTmux(): boolean {
  // bg.ts sets terminal-overrides :Tc before attach, so truecolor passes
  // through — skip the clamp. General escape hatch for anyone who's
  // configured their tmux correctly.

```

---


### `src/ink/components/AlternateScreen.tsx`

**信息:**
- 行数: 80
- 大小: 10377 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type PropsWithChildren, useContext, useInsertionEffect } from 'react';
import instances from '../instances.js';
import { DISABLE_MOUSE_TRACKING, ENABLE_MOUSE_TRACKING, ENTER_ALT_SCREEN, EXIT_ALT_SCREEN } from '../termio/dec.js';
import { TerminalWriteContext } from '../useTerminalNotification.js';
import Box from './Box.js';
import { TerminalSizeContext } from './TerminalSizeContext.js';
type Props = PropsWithChildren<{
  /** Enable SGR mouse tracking (wheel + click/drag). Default true. */
  mouseTracking?: boolean;
}>;

/**
 * Run children in the terminal's alternate screen buffer, constrained to
 * the viewport height. While mounted:
 *
 * - Enters the alt screen (DEC 1049), clears it, homes the cursor
 * - Constrains its own height to the terminal row count, so overflow must
 *   be handled via `overflow: scroll` / flexbox (no native scrollback)
 * - Optionally enables SGR mouse tracking (wheel + click/drag) — events
 *   surface as `ParsedKey` (wheel) and update the Ink instance's
 *   selection state (click/drag)
 *
 * On unmount, disables mouse tracking and exits the alt screen, restoring
 * the main screen's content. Safe for use in ctrl-o transcript overlays
 * and similar temporary fullscreen views — the main screen is preserved.
 *
 * Notifies the Ink instance via `setAltScreenActive()` so the renderer
 * keeps the cursor inside the viewport (preventing the cursor-restore LF
 * from scrolling content) and so signal-exit cleanup can exit the alt
 * screen if the component's own unmount doesn't run.
 */
export function AlternateScreen(t0) {
  const $ = _c(7);
  const {
    children,
    mouseTracking: t1
  } = t0;
  const mouseTracking = t1 === undefined ? true : t1;
  const size = useContext(TerminalSizeContext);
  const writeRaw = useContext(TerminalWriteContext);
  let t2;
  let t3;
  if ($[0] !== mouseTracking || $[1] !== writeRaw) {
    t2 = () => {
      const ink = instances.get(process.stdout);
      if (!writeRaw) {
        return;
      }
      writeRaw(ENTER_ALT_SCREEN + "\x1B[2J\x1B[H" + (mouseTracking ? ENABLE_MOUSE_TRACKING : ""));

```

---


### `src/ink/components/App.tsx`

**信息:**
- 行数: 685
- 大小: 99323 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React, { PureComponent, type ReactNode } from 'react';
import { updateLastInteractionTime } from '../../bootstrap/state.js';
import { logForDebugging } from '../../utils/debug.js';
import { stopCapturingEarlyInput } from '../../utils/earlyInput.js';
import { isEnvTruthy } from '../../utils/envUtils.js';
import { isMouseClicksDisabled } from '../../utils/fullscreen.js';
import { logError } from '../../utils/log.js';
import { EventEmitter } from '../events/emitter.js';
import { InputEvent } from '../events/input-event.js';
import { TerminalFocusEvent } from '../events/terminal-focus-event.js';
import { INITIAL_STATE, type ParsedInput, type ParsedKey, type ParsedMouse, parseMultipleKeypresses } from '../parse-keypress.js';
import reconciler from '../reconciler.js';
import { finishSelection, hasSelection, type SelectionState, startSelection } from '../selection.js';
import { isXtermJs, setXtversionName, supportsExtendedKeys } from '../terminal.js';
import { getTerminalFocused, setTerminalFocused } from '../terminal-focus-state.js';
import { TerminalQuerier, xtversion } from '../terminal-querier.js';
import { DISABLE_KITTY_KEYBOARD, DISABLE_MODIFY_OTHER_KEYS, ENABLE_KITTY_KEYBOARD, ENABLE_MODIFY_OTHER_KEYS, FOCUS_IN, FOCUS_OUT } from '../termio/csi.js';
import { DBP, DFE, DISABLE_MOUSE_TRACKING, EBP, EFE, HIDE_CURSOR, SHOW_CURSOR } from '../termio/dec.js';
import AppContext from './AppContext.js';
import { ClockProvider } from './ClockContext.js';
import CursorDeclarationContext, { type CursorDeclarationSetter } from './CursorDeclarationContext.js';
import ErrorOverview from './ErrorOverview.js';
import StdinContext from './StdinContext.js';
import { TerminalFocusProvider } from './TerminalFocusContext.js';
import { TerminalSizeContext } from './TerminalSizeContext.js';

// Platforms that support Unix-style process suspension (SIGSTOP/SIGCONT)
const SUPPORTS_SUSPEND = process.platform !== 'win32';

// After this many milliseconds of stdin silence, the next chunk triggers
// a terminal mode re-assert (mouse tracking). Catches tmux detach→attach,
// ssh reconnect, and laptop wake — the terminal resets DEC private modes
// but no signal reaches us. 5s is well above normal inter-keystroke gaps
// but short enough that the first scroll after reattach works.
const STDIN_RESUME_GAP_MS = 5000;
type Props = {
  readonly children: ReactNode;
  readonly stdin: NodeJS.ReadStream;
  readonly stdout: NodeJS.WriteStream;
  readonly stderr: NodeJS.WriteStream;
  readonly exitOnCtrlC: boolean;
  readonly onExit: (error?: Error) => void;
  readonly terminalColumns: number;
  readonly terminalRows: number;
  // Text selection state. App mutates this directly from mouse events
  // and calls onSelectionChange to trigger a repaint. Mouse events only
  // arrive when <AlternateScreen> (or similar) enables mouse tracking,
  // so the handler is always wired but dormant until tracking is on.
  readonly selection: SelectionState;
  readonly onSelectionChange: () => void;

```

---


### `src/ink/components/AppContext.ts`

**信息:**
- 行数: 21
- 大小: 523 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { createContext } from 'react'

export type Props = {
  /**
   * Exit (unmount) the whole Ink app.
   */
  readonly exit: (error?: Error) => void
}

/**
 * `AppContext` is a React context, which exposes a method to manually exit the app (unmount).
 */
// eslint-disable-next-line @typescript-eslint/naming-convention
const AppContext = createContext<Props>({
  exit() {},
})

// eslint-disable-next-line custom-rules/no-top-level-side-effects
AppContext.displayName = 'InternalAppContext'

export default AppContext

```

---


### `src/ink/components/Box.tsx`

**信息:**
- 行数: 214
- 大小: 21652 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import '../global.d.ts';
import React, { type PropsWithChildren, type Ref } from 'react';
import type { Except } from 'type-fest';
import type { DOMElement } from '../dom.js';
import type { ClickEvent } from '../events/click-event.js';
import type { FocusEvent } from '../events/focus-event.js';
import type { KeyboardEvent } from '../events/keyboard-event.js';
import type { Styles } from '../styles.js';
import * as warn from '../warn.js';
export type Props = Except<Styles, 'textWrap'> & {
  ref?: Ref<DOMElement>;
  /**
   * Tab order index. Nodes with `tabIndex >= 0` participate in
   * Tab/Shift+Tab cycling; `-1` means programmatically focusable only.
   */
  tabIndex?: number;
  /**
   * Focus this element when it mounts. Like the HTML `autofocus`
   * attribute — the FocusManager calls `focus(node)` during the
   * reconciler's `commitMount` phase.
   */
  autoFocus?: boolean;
  /**
   * Fired on left-button click (press + release without drag). Only works
   * inside `<AlternateScreen>` where mouse tracking is enabled — no-op
   * otherwise. The event bubbles from the deepest hit Box up through
   * ancestors; call `event.stopImmediatePropagation()` to stop bubbling.
   */
  onClick?: (event: ClickEvent) => void;
  onFocus?: (event: FocusEvent) => void;
  onFocusCapture?: (event: FocusEvent) => void;
  onBlur?: (event: FocusEvent) => void;
  onBlurCapture?: (event: FocusEvent) => void;
  onKeyDown?: (event: KeyboardEvent) => void;
  onKeyDownCapture?: (event: KeyboardEvent) => void;
  /**
   * Fired when the mouse moves into this Box's rendered rect. Like DOM
   * `mouseenter`, does NOT bubble — moving between children does not
   * re-fire on the parent. Only works inside `<AlternateScreen>` where
   * mode-1003 mouse tracking is enabled.
   */
  onMouseEnter?: () => void;
  /** Fired when the mouse moves out of this Box's rendered rect. */
  onMouseLeave?: () => void;
};

/**
 * `<Box>` is an essential Ink component to build your layout. It's like `<div style="display: flex">` in the browser.
 */

```

---


### `src/ink/components/Button.tsx`

**信息:**
- 行数: 192
- 大小: 16523 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type Ref, useCallback, useEffect, useRef, useState } from 'react';
import type { Except } from 'type-fest';
import type { DOMElement } from '../dom.js';
import type { ClickEvent } from '../events/click-event.js';
import type { FocusEvent } from '../events/focus-event.js';
import type { KeyboardEvent } from '../events/keyboard-event.js';
import type { Styles } from '../styles.js';
import Box from './Box.js';
type ButtonState = {
  focused: boolean;
  hovered: boolean;
  active: boolean;
};
export type Props = Except<Styles, 'textWrap'> & {
  ref?: Ref<DOMElement>;
  /**
   * Called when the button is activated via Enter, Space, or click.
   */
  onAction: () => void;
  /**
   * Tab order index. Defaults to 0 (in tab order).
   * Set to -1 for programmatically focusable only.
   */
  tabIndex?: number;
  /**
   * Focus this button when it mounts.
   */
  autoFocus?: boolean;
  /**
   * Render prop receiving the interactive state. Use this to
   * style children based on focus/hover/active — Button itself
   * is intentionally unstyled.
   *
   * If not provided, children render as-is (no state-dependent styling).
   */
  children: ((state: ButtonState) => React.ReactNode) | React.ReactNode;
};
function Button(t0) {
  const $ = _c(30);
  let autoFocus;
  let children;
  let onAction;
  let ref;
  let style;
  let t1;
  if ($[0] !== t0) {
    ({
      onAction,
      tabIndex: t1,

```

---


### `src/ink/components/ClockContext.tsx`

**信息:**
- 行数: 112
- 大小: 12091 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, useEffect, useState } from 'react';
import { FRAME_INTERVAL_MS } from '../constants.js';
import { useTerminalFocus } from '../hooks/use-terminal-focus.js';
export type Clock = {
  subscribe: (onChange: () => void, keepAlive: boolean) => () => void;
  now: () => number;
  setTickInterval: (ms: number) => void;
};
export function createClock(tickIntervalMs: number): Clock {
  const subscribers = new Map<() => void, boolean>();
  let interval: ReturnType<typeof setInterval> | null = null;
  let currentTickIntervalMs = tickIntervalMs;
  let startTime = 0;
  // Snapshot of the current tick's time, ensuring all subscribers in the same
  // tick see the same value (keeps animations synchronized)
  let tickTime = 0;
  function tick(): void {
    tickTime = Date.now() - startTime;
    for (const onChange of subscribers.keys()) {
      onChange();
    }
  }
  function updateInterval(): void {
    const anyKeepAlive = [...subscribers.values()].some(Boolean);
    if (anyKeepAlive) {
      if (interval) {
        clearInterval(interval);
        interval = null;
      }
      if (startTime === 0) {
        startTime = Date.now();
      }
      interval = setInterval(tick, currentTickIntervalMs);
    } else if (interval) {
      clearInterval(interval);
      interval = null;
    }
  }
  return {
    subscribe(onChange, keepAlive) {
      subscribers.set(onChange, keepAlive);
      updateInterval();
      return () => {
        subscribers.delete(onChange);
        updateInterval();
      };
    },
    now() {
      if (startTime === 0) {

```

---


### `src/ink/components/CursorDeclarationContext.ts`

**信息:**
- 行数: 32
- 大小: 1119 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { createContext } from 'react'
import type { DOMElement } from '../dom.js'

export type CursorDeclaration = {
  /** Display column (terminal cell width) within the declared node */
  readonly relativeX: number
  /** Line number within the declared node */
  readonly relativeY: number
  /** The ink-box DOMElement whose yoga layout provides the absolute origin */
  readonly node: DOMElement
}

/**
 * Setter for the declared cursor position.
 *
 * The optional second argument makes `null` a conditional clear: the
 * declaration is only cleared if the currently-declared node matches
 * `clearIfNode`. This makes the hook safe for sibling components
 * (e.g. list items) that transfer focus among themselves — without the
 * node check, a newly-unfocused item's clear could clobber a
 * newly-focused sibling's set depending on layout-effect order.
 */
export type CursorDeclarationSetter = (
  declaration: CursorDeclaration | null,
  clearIfNode?: DOMElement | null,
) => void

const CursorDeclarationContext = createContext<CursorDeclarationSetter>(
  () => {},
)

export default CursorDeclarationContext

```

---


### `src/ink/components/ErrorOverview.tsx`

**信息:**
- 行数: 109
- 大小: 15405 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import codeExcerpt, { type CodeExcerpt } from 'code-excerpt';
import { readFileSync } from 'fs';
import React from 'react';
import StackUtils from 'stack-utils';
import Box from './Box.js';
import Text from './Text.js';

/* eslint-disable custom-rules/no-process-cwd -- stack trace file:// paths are relative to the real OS cwd, not the virtual cwd */

// Error's source file is reported as file:///home/user/file.js
// This function removes the file://[cwd] part
const cleanupPath = (path: string | undefined): string | undefined => {
  return path?.replace(`file://${process.cwd()}/`, '');
};
let stackUtils: StackUtils | undefined;
function getStackUtils(): StackUtils {
  return stackUtils ??= new StackUtils({
    cwd: process.cwd(),
    internals: StackUtils.nodeInternals()
  });
}

/* eslint-enable custom-rules/no-process-cwd */

type Props = {
  readonly error: Error;
};
export default function ErrorOverview({
  error
}: Props) {
  const stack = error.stack ? error.stack.split('\n').slice(1) : undefined;
  const origin = stack ? getStackUtils().parseLine(stack[0]!) : undefined;
  const filePath = cleanupPath(origin?.file);
  let excerpt: CodeExcerpt[] | undefined;
  let lineWidth = 0;
  if (filePath && origin?.line) {
    try {
      // eslint-disable-next-line custom-rules/no-sync-fs -- sync render path; error overlay can't go async without suspense restructuring
      const sourceCode = readFileSync(filePath, 'utf8');
      excerpt = codeExcerpt(sourceCode, origin.line);
      if (excerpt) {
        for (const {
          line
        } of excerpt) {
          lineWidth = Math.max(lineWidth, String(line).length);
        }
      }
    } catch {
      // file not readable — skip source context
    }

```

---


### `src/ink/components/Link.tsx`

**信息:**
- 行数: 42
- 大小: 3556 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ReactNode } from 'react';
import React from 'react';
import { supportsHyperlinks } from '../supports-hyperlinks.js';
import Text from './Text.js';
export type Props = {
  readonly children?: ReactNode;
  readonly url: string;
  readonly fallback?: ReactNode;
};
export default function Link(t0) {
  const $ = _c(5);
  const {
    children,
    url,
    fallback
  } = t0;
  const content = children ?? url;
  if (supportsHyperlinks()) {
    let t1;
    if ($[0] !== content || $[1] !== url) {
      t1 = <Text><ink-link href={url}>{content}</ink-link></Text>;
      $[0] = content;
      $[1] = url;
      $[2] = t1;
    } else {
      t1 = $[2];
    }
    return t1;
  }
  const t1 = fallback ?? content;
  let t2;
  if ($[3] !== t1) {
    t2 = <Text>{t1}</Text>;
    $[3] = t1;
    $[4] = t2;
  } else {
    t2 = $[4];
  }
  return t2;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdE5vZGUiLCJSZWFjdCIsInN1cHBvcnRzSHlwZXJsaW5rcyIsIlRleHQiLCJQcm9wcyIsImNoaWxkcmVuIiwidXJsIiwiZmFsbGJhY2siLCJMaW5rIiwidDAiLCIkIiwiX2MiLCJjb250ZW50IiwidDEiLCJ0MiJdLCJzb3VyY2VzIjpbIkxpbmsudHN4Il0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB0eXBlIHsgUmVhY3ROb2RlIH0gZnJvbSAncmVhY3QnXG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgeyBzdXBwb3J0c0h5cGVybGlua3MgfSBmcm9tICcuLi9zdXBwb3J0cy1oeXBlcmxpbmtzLmpzJ1xuaW1wb3J0IFRleHQgZnJvbSAnLi9UZXh0LmpzJ1xuXG5leHBvcnQgdHlwZSBQcm9wcyA9IHtcbiAgcmVhZG9ubHkgY2hpbGRyZW4/OiBSZWFjdE5vZGVcbiAgcmVhZG9ubHkgdXJsOiBzdHJpbmdcbiAgcmVhZG9ubHkgZmFsbGJhY2s/OiBSZWFjdE5vZGVcbn1cblxuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gTGluayh7XG4gIGNoaWxkcmVuLFxuICB1cmwsXG4gIGZhbGxiYWNrLFxufTogUHJvcHMpOiBSZWFjdC5SZWFjdE5vZGUge1xuICAvLyBVc2UgY2hpbGRyZW4gaWYgcHJvdmlkZWQsIG90aGVyd2lzZSBkaXNwbGF5IHRoZSBVUkxcbiAgY29uc3QgY29udGVudCA9IGNoaWxkcmVuID8/IHVybFxuXG4gIGlmIChzdXBwb3J0c0h5cGVybGlua3MoKSkge1xuICAgIC8vIFdyYXAgaW4gVGV4dCB0byBlbnN1cmUgd2UncmUgaW4gYSB0ZXh0IGNvbnRleHRcbiAgICAvLyAoaW5rLWxpbmsgaXMgYSB0ZXh0IGVsZW1lbnQgbGlrZSBpbmstdGV4dClcbiAgICByZXR1cm4gKFxuICAgICAgPFRleHQ+XG4gICAgICAgIDxpbmstbGluayBocmVmPXt1cmx9Pntjb250ZW50fTwvaW5rLWxpbms+XG4gICAgICA8L1RleHQ+XG4gICAgKVxuICB9XG5cbiAgcmV0dXJuIDxUZXh0PntmYWxsYmFjayA/PyBjb250ZW50fTwvVGV4dD5cbn1cbiJdLCJtYXBwaW5ncyI6IjtBQUFBLGNBQWNBLFNBQVMsUUFBUSxPQUFPO0FBQ3RDLE9BQU9DLEtBQUssTUFBTSxPQUFPO0FBQ3pCLFNBQVNDLGtCQUFrQixRQUFRLDJCQUEyQjtBQUM5RCxPQUFPQyxJQUFJLE1BQU0sV0FBVztBQUU1QixPQUFPLEtBQUtDLEtBQUssR0FBRztFQUNsQixTQUFTQyxRQUFRLENBQUMsRUFBRUwsU0FBUztFQUM3QixTQUFTTSxHQUFHLEVBQUUsTUFBTTtFQUNwQixTQUFTQyxRQUFRLENBQUMsRUFBRVAsU0FBUztBQUMvQixDQUFDO0FBRUQsZUFBZSxTQUFBUSxLQUFBQyxFQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQWM7SUFBQU4sUUFBQTtJQUFBQyxHQUFBO0lBQUFDO0VBQUEsSUFBQUUsRUFJckI7RUFFTixNQUFBRyxPQUFBLEdBQWdCUCxRQUFlLElBQWZDLEdBQWU7RUFFL0IsSUFBSUosa0JBQWtCLENBQUMsQ0FBQztJQUFBLElBQUFXLEVBQUE7SUFBQSxJQUFBSCxDQUFBLFFBQUFFLE9BQUEsSUFBQUYsQ0FBQSxRQUFBSixHQUFBO01BSXBCTyxFQUFBLElBQUMsSUFBSSxDQUNILFNBQXlDLENBQXpCUCxJQUFHLENBQUhBLElBQUUsQ0FBQyxDQUFHTSxRQUFNLENBQUUsRUFBOUIsUUFBeUMsQ0FDM0MsRUFGQyxJQUFJLENBRUU7TUFBQUYsQ0FBQSxNQUFBRSxPQUFBO01BQUFGLENBQUEsTUFBQUosR0FBQTtNQUFBSSxDQUFBLE1BQUFHLEVBQUE7SUFBQTtNQUFBQSxFQUFBLEdBQUFILENBQUE7SUFBQTtJQUFBLE9BRlBHLEVBRU87RUFBQTtFQUlHLE1BQUFBLEVBQUEsR0FBQU4sUUFBbUIsSUFBbkJLLE9BQW1CO0VBQUEsSUFBQUUsRUFBQTtFQUFBLElBQUFKLENBQUEsUUFBQUcsRUFBQTtJQUExQkMsRUFBQSxJQUFDLElBQUksQ0FBRSxDQUFBRCxFQUFrQixDQUFFLEVBQTFCLElBQUksQ0FBNkI7SUFBQUgsQ0FBQSxNQUFBRyxFQUFBO0lBQUFILENBQUEsTUFBQUksRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUosQ0FBQTtFQUFBO0VBQUEsT0FBbENJLEVBQWtDO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/ink/components/Newline.tsx`

**信息:**
- 行数: 39
- 大小: 2356 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
export type Props = {
  /**
   * Number of newlines to insert.
   *
   * @default 1
   */
  readonly count?: number;
};

/**
 * Adds one or more newline (\n) characters. Must be used within <Text> components.
 */
export default function Newline(t0) {
  const $ = _c(4);
  const {
    count: t1
  } = t0;
  const count = t1 === undefined ? 1 : t1;
  let t2;
  if ($[0] !== count) {
    t2 = "\n".repeat(count);
    $[0] = count;
    $[1] = t2;
  } else {
    t2 = $[1];
  }
  let t3;
  if ($[2] !== t2) {
    t3 = <ink-text>{t2}</ink-text>;
    $[2] = t2;
    $[3] = t3;
  } else {
    t3 = $[3];
  }
  return t3;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIlByb3BzIiwiY291bnQiLCJOZXdsaW5lIiwidDAiLCIkIiwiX2MiLCJ0MSIsInVuZGVmaW5lZCIsInQyIiwicmVwZWF0IiwidDMiXSwic291cmNlcyI6WyJOZXdsaW5lLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5cbmV4cG9ydCB0eXBlIFByb3BzID0ge1xuICAvKipcbiAgICogTnVtYmVyIG9mIG5ld2xpbmVzIHRvIGluc2VydC5cbiAgICpcbiAgICogQGRlZmF1bHQgMVxuICAgKi9cbiAgcmVhZG9ubHkgY291bnQ/OiBudW1iZXJcbn1cblxuLyoqXG4gKiBBZGRzIG9uZSBvciBtb3JlIG5ld2xpbmUgKFxcbikgY2hhcmFjdGVycy4gTXVzdCBiZSB1c2VkIHdpdGhpbiA8VGV4dD4gY29tcG9uZW50cy5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gTmV3bGluZSh7IGNvdW50ID0gMSB9OiBQcm9wcykge1xuICByZXR1cm4gPGluay10ZXh0PnsnXFxuJy5yZXBlYXQoY291bnQpfTwvaW5rLXRleHQ+XG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxPQUFPQSxLQUFLLE1BQU0sT0FBTztBQUV6QixPQUFPLEtBQUtDLEtBQUssR0FBRztFQUNsQjtBQUNGO0FBQ0E7QUFDQTtBQUNBO0VBQ0UsU0FBU0MsS0FBSyxDQUFDLEVBQUUsTUFBTTtBQUN6QixDQUFDOztBQUVEO0FBQ0E7QUFDQTtBQUNBLGVBQWUsU0FBQUMsUUFBQUMsRUFBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUFpQjtJQUFBSixLQUFBLEVBQUFLO0VBQUEsSUFBQUgsRUFBb0I7RUFBbEIsTUFBQUYsS0FBQSxHQUFBSyxFQUFTLEtBQVRDLFNBQVMsR0FBVCxDQUFTLEdBQVRELEVBQVM7RUFBQSxJQUFBRSxFQUFBO0VBQUEsSUFBQUosQ0FBQSxRQUFBSCxLQUFBO0lBQ3ZCTyxFQUFBLE9BQUksQ0FBQUMsTUFBTyxDQUFDUixLQUFLLENBQUM7SUFBQUcsQ0FBQSxNQUFBSCxLQUFBO0lBQUFHLENBQUEsTUFBQUksRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUosQ0FBQTtFQUFBO0VBQUEsSUFBQU0sRUFBQTtFQUFBLElBQUFOLENBQUEsUUFBQUksRUFBQTtJQUE3QkUsRUFBQSxZQUF5QyxDQUE5QixDQUFBRixFQUFpQixDQUFFLEVBQTlCLFFBQXlDO0lBQUFKLENBQUEsTUFBQUksRUFBQTtJQUFBSixDQUFBLE1BQUFNLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFOLENBQUE7RUFBQTtFQUFBLE9BQXpDTSxFQUF5QztBQUFBIiwiaWdub3JlTGlzdCI6W119
```

---


### `src/ink/components/NoSelect.tsx`

**信息:**
- 行数: 68
- 大小: 5899 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { type PropsWithChildren } from 'react';
import Box, { type Props as BoxProps } from './Box.js';
type Props = Omit<BoxProps, 'noSelect'> & {
  /**
   * Extend the exclusion zone from column 0 to this box's right edge,
   * for every row this box occupies. Use for gutters rendered inside a
   * wider indented container (e.g. a diff inside a tool message row):
   * without this, a multi-row drag picks up the container's leading
   * indent on rows below the prefix.
   *
   * @default false
   */
  fromLeftEdge?: boolean;
};

/**
 * Marks its contents as non-selectable in fullscreen text selection.
 * Cells inside this box are skipped by both the selection highlight and
 * the copied text — the gutter stays visually unchanged while the user
 * drags, making it clear what will be copied.
 *
 * Use to fence off gutters (line numbers, diff +/- sigils, list bullets)
 * so click-drag over rendered code yields clean pasteable content:
 *
 *   <Box flexDirection="row">
 *     <NoSelect fromLeftEdge><Text dimColor> 42 +</Text></NoSelect>
 *     <Text>const x = 1</Text>
 *   </Box>
 *
 * Only affects alt-screen text selection (<AlternateScreen> with mouse
 * tracking). No-op in the main-screen scrollback render where the
 * terminal's native selection is used instead.
 */
export function NoSelect(t0) {
  const $ = _c(8);
  let boxProps;
  let children;
  let fromLeftEdge;
  if ($[0] !== t0) {
    ({
      children,
      fromLeftEdge,
      ...boxProps
    } = t0);
    $[0] = t0;
    $[1] = boxProps;
    $[2] = children;
    $[3] = fromLeftEdge;
  } else {

```

---


### `src/ink/components/RawAnsi.tsx`

**信息:**
- 行数: 57
- 大小: 5157 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
type Props = {
  /**
   * Pre-rendered ANSI lines. Each element must be exactly one terminal row
   * (already wrapped to `width` by the producer) with ANSI escape codes inline.
   */
  lines: string[];
  /** Column width the producer wrapped to. Sent to Yoga as the fixed leaf width. */
  width: number;
};

/**
 * Bypass the <Ansi> → React tree → Yoga → squash → re-serialize roundtrip for
 * content that is already terminal-ready.
 *
 * Use this when an external renderer (e.g. the ColorDiff NAPI module) has
 * already produced ANSI-escaped, width-wrapped output. A normal <Ansi> mount
 * reparses that output into one React <Text> per style span, lays out each
 * span as a Yoga flex child, then walks the tree to re-emit the same escape
 * codes it was given. For a long transcript full of syntax-highlighted diffs
 * that roundtrip is the dominant cost of the render.
 *
 * This component emits a single Yoga leaf with a constant-time measure func
 * (width × lines.length) and hands the joined string straight to output.write(),
 * which already splits on '\n' and parses ANSI into the screen buffer.
 */
export function RawAnsi(t0) {
  const $ = _c(6);
  const {
    lines,
    width
  } = t0;
  if (lines.length === 0) {
    return null;
  }
  let t1;
  if ($[0] !== lines) {
    t1 = lines.join("\n");
    $[0] = lines;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  let t2;
  if ($[2] !== lines.length || $[3] !== t1 || $[4] !== width) {
    t2 = <ink-raw-ansi rawText={t1} rawWidth={width} rawHeight={lines.length} />;
    $[2] = lines.length;
    $[3] = t1;
    $[4] = width;

```

---


### `src/ink/components/ScrollBox.tsx`

**信息:**
- 行数: 237
- 大小: 31814 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import React, { type PropsWithChildren, type Ref, useImperativeHandle, useRef, useState } from 'react';
import type { Except } from 'type-fest';
import { markScrollActivity } from '../../bootstrap/state.js';
import type { DOMElement } from '../dom.js';
import { markDirty, scheduleRenderFrom } from '../dom.js';
import { markCommitStart } from '../reconciler.js';
import type { Styles } from '../styles.js';
import '../global.d.ts';
import Box from './Box.js';
export type ScrollBoxHandle = {
  scrollTo: (y: number) => void;
  scrollBy: (dy: number) => void;
  /**
   * Scroll so `el`'s top is at the viewport top (plus `offset`). Unlike
   * scrollTo which bakes a number that's stale by the time the throttled
   * render fires, this defers the position read to render time —
   * render-node-to-output reads `el.yogaNode.getComputedTop()` in the
   * SAME Yoga pass that computes scrollHeight. Deterministic. One-shot.
   */
  scrollToElement: (el: DOMElement, offset?: number) => void;
  scrollToBottom: () => void;
  getScrollTop: () => number;
  getPendingDelta: () => number;
  getScrollHeight: () => number;
  /**
   * Like getScrollHeight, but reads Yoga directly instead of the cached
   * value written by render-node-to-output (throttled, up to 16ms stale).
   * Use when you need a fresh value in useLayoutEffect after a React commit
   * that grew content. Slightly more expensive (native Yoga call).
   */
  getFreshScrollHeight: () => number;
  getViewportHeight: () => number;
  /**
   * Absolute screen-buffer row of the first visible content line (inside
   * padding). Used for drag-to-scroll edge detection.
   */
  getViewportTop: () => number;
  /**
   * True when scroll is pinned to the bottom. Set by scrollToBottom, the
   * initial stickyScroll attribute, and by the renderer when positional
   * follow fires (scrollTop at prevMax, content grows). Cleared by
   * scrollTo/scrollBy. Stable signal for "at bottom" that doesn't depend on
   * layout values (unlike scrollTop+viewportH >= scrollHeight).
   */
  isSticky: () => boolean;
  /**
   * Subscribe to imperative scroll changes (scrollTo/scrollBy/scrollToBottom).
   * Does NOT fire for stickyScroll updates done by the Ink renderer — those
   * happen during Ink's render phase after React has committed. Callers that
   * care about the sticky case should treat "at bottom" as a fallback.

```

---


### `src/ink/components/Spacer.tsx`

**信息:**
- 行数: 20
- 大小: 1563 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React from 'react';
import Box from './Box.js';

/**
 * A flexible space that expands along the major axis of its containing layout.
 * It's useful as a shortcut for filling all the available spaces between elements.
 */
export default function Spacer() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t0 = <Box flexGrow={1} />;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsIkJveCIsIlNwYWNlciIsIiQiLCJfYyIsInQwIiwiU3ltYm9sIiwiZm9yIl0sInNvdXJjZXMiOlsiU3BhY2VyLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnXG5pbXBvcnQgQm94IGZyb20gJy4vQm94LmpzJ1xuXG4vKipcbiAqIEEgZmxleGlibGUgc3BhY2UgdGhhdCBleHBhbmRzIGFsb25nIHRoZSBtYWpvciBheGlzIG9mIGl0cyBjb250YWluaW5nIGxheW91dC5cbiAqIEl0J3MgdXNlZnVsIGFzIGEgc2hvcnRjdXQgZm9yIGZpbGxpbmcgYWxsIHRoZSBhdmFpbGFibGUgc3BhY2VzIGJldHdlZW4gZWxlbWVudHMuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIFNwYWNlcigpIHtcbiAgcmV0dXJuIDxCb3ggZmxleEdyb3c9ezF9IC8+XG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxPQUFPQSxLQUFLLE1BQU0sT0FBTztBQUN6QixPQUFPQyxHQUFHLE1BQU0sVUFBVTs7QUFFMUI7QUFDQTtBQUNBO0FBQ0E7QUFDQSxlQUFlLFNBQUFDLE9BQUE7RUFBQSxNQUFBQyxDQUFBLEdBQUFDLEVBQUE7RUFBQSxJQUFBQyxFQUFBO0VBQUEsSUFBQUYsQ0FBQSxRQUFBRyxNQUFBLENBQUFDLEdBQUE7SUFDTkYsRUFBQSxJQUFDLEdBQUcsQ0FBVyxRQUFDLENBQUQsR0FBQyxHQUFJO0lBQUFGLENBQUEsTUFBQUUsRUFBQTtFQUFBO0lBQUFBLEVBQUEsR0FBQUYsQ0FBQTtFQUFBO0VBQUEsT0FBcEJFLEVBQW9CO0FBQUEiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/ink/components/StdinContext.ts`

**信息:**
- 行数: 49
- 大小: 1678 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { createContext } from 'react'
import { EventEmitter } from '../events/emitter.js'
import type { TerminalQuerier } from '../terminal-querier.js'

export type Props = {
  /**
   * Stdin stream passed to `render()` in `options.stdin` or `process.stdin` by default. Useful if your app needs to handle user input.
   */
  readonly stdin: NodeJS.ReadStream

  /**
   * Ink exposes this function via own `<StdinContext>` to be able to handle Ctrl+C, that's why you should use Ink's `setRawMode` instead of `process.stdin.setRawMode`.
   * If the `stdin` stream passed to Ink does not support setRawMode, this function does nothing.
   */
  readonly setRawMode: (value: boolean) => void

  /**
   * A boolean flag determining if the current `stdin` supports `setRawMode`. A component using `setRawMode` might want to use `isRawModeSupported` to nicely fall back in environments where raw mode is not supported.
   */
  readonly isRawModeSupported: boolean

  readonly internal_exitOnCtrlC: boolean

  readonly internal_eventEmitter: EventEmitter

  /** Query the terminal and await responses (DECRQM, OSC 11, etc.).
   *  Null only in the never-reached default context value. */
  readonly internal_querier: TerminalQuerier | null
}

/**
 * `StdinContext` is a React context, which exposes input stream.
 */

const StdinContext = createContext<Props>({
  stdin: process.stdin,

  internal_eventEmitter: new EventEmitter(),
  setRawMode() {},
  isRawModeSupported: false,

  internal_exitOnCtrlC: true,
  internal_querier: null,
})

// eslint-disable-next-line custom-rules/no-top-level-side-effects
StdinContext.displayName = 'InternalStdinContext'

export default StdinContext

```

---


### `src/ink/components/TerminalFocusContext.tsx`

**信息:**
- 行数: 52
- 大小: 5955 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, useMemo, useSyncExternalStore } from 'react';
import { getTerminalFocused, getTerminalFocusState, subscribeTerminalFocus, type TerminalFocusState } from '../terminal-focus-state.js';
export type { TerminalFocusState };
export type TerminalFocusContextProps = {
  readonly isTerminalFocused: boolean;
  readonly terminalFocusState: TerminalFocusState;
};
const TerminalFocusContext = createContext<TerminalFocusContextProps>({
  isTerminalFocused: true,
  terminalFocusState: 'unknown'
});

// eslint-disable-next-line custom-rules/no-top-level-side-effects
TerminalFocusContext.displayName = 'TerminalFocusContext';

// Separate component so App.tsx doesn't re-render on focus changes.
// Children are a stable prop reference, so they don't re-render either —
// only components that consume the context will re-render.
export function TerminalFocusProvider(t0) {
  const $ = _c(6);
  const {
    children
  } = t0;
  const isTerminalFocused = useSyncExternalStore(subscribeTerminalFocus, getTerminalFocused);
  const terminalFocusState = useSyncExternalStore(subscribeTerminalFocus, getTerminalFocusState);
  let t1;
  if ($[0] !== isTerminalFocused || $[1] !== terminalFocusState) {
    t1 = {
      isTerminalFocused,
      terminalFocusState
    };
    $[0] = isTerminalFocused;
    $[1] = terminalFocusState;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  const value = t1;
  let t2;
  if ($[3] !== children || $[4] !== value) {
    t2 = <TerminalFocusContext.Provider value={value}>{children}</TerminalFocusContext.Provider>;
    $[3] = children;
    $[4] = value;
    $[5] = t2;
  } else {
    t2 = $[5];
  }
  return t2;
}

```

---


### `src/ink/components/TerminalSizeContext.tsx`

**信息:**
- 行数: 7
- 大小: 983 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { createContext } from 'react';
export type TerminalSize = {
  columns: number;
  rows: number;
};
export const TerminalSizeContext = createContext<TerminalSize | null>(null);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJjcmVhdGVDb250ZXh0IiwiVGVybWluYWxTaXplIiwiY29sdW1ucyIsInJvd3MiLCJUZXJtaW5hbFNpemVDb250ZXh0Il0sInNvdXJjZXMiOlsiVGVybWluYWxTaXplQ29udGV4dC50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgY3JlYXRlQ29udGV4dCB9IGZyb20gJ3JlYWN0J1xuXG5leHBvcnQgdHlwZSBUZXJtaW5hbFNpemUgPSB7XG4gIGNvbHVtbnM6IG51bWJlclxuICByb3dzOiBudW1iZXJcbn1cblxuZXhwb3J0IGNvbnN0IFRlcm1pbmFsU2l6ZUNvbnRleHQgPSBjcmVhdGVDb250ZXh0PFRlcm1pbmFsU2l6ZSB8IG51bGw+KG51bGwpXG4iXSwibWFwcGluZ3MiOiJBQUFBLFNBQVNBLGFBQWEsUUFBUSxPQUFPO0FBRXJDLE9BQU8sS0FBS0MsWUFBWSxHQUFHO0VBQ3pCQyxPQUFPLEVBQUUsTUFBTTtFQUNmQyxJQUFJLEVBQUUsTUFBTTtBQUNkLENBQUM7QUFFRCxPQUFPLE1BQU1DLG1CQUFtQixHQUFHSixhQUFhLENBQUNDLFlBQVksR0FBRyxJQUFJLENBQUMsQ0FBQyxJQUFJLENBQUMiLCJpZ25vcmVMaXN0IjpbXX0=
```

---


### `src/ink/components/Text.tsx`

**信息:**
- 行数: 254
- 大小: 16811 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import type { ReactNode } from 'react';
import React from 'react';
import type { Color, Styles, TextStyles } from '../styles.js';
type BaseProps = {
  /**
   * Change text color. Accepts a raw color value (rgb, hex, ansi).
   */
  readonly color?: Color;

  /**
   * Same as `color`, but for background.
   */
  readonly backgroundColor?: Color;

  /**
   * Make the text italic.
   */
  readonly italic?: boolean;

  /**
   * Make the text underlined.
   */
  readonly underline?: boolean;

  /**
   * Make the text crossed with a line.
   */
  readonly strikethrough?: boolean;

  /**
   * Inverse background and foreground colors.
   */
  readonly inverse?: boolean;

  /**
   * This property tells Ink to wrap or truncate text if its width is larger than container.
   * If `wrap` is passed (by default), Ink will wrap text and split it into multiple lines.
   * If `truncate-*` is passed, Ink will truncate text instead, which will result in one line of text with the rest cut off.
   */
  readonly wrap?: Styles['textWrap'];
  readonly children?: ReactNode;
};

/**
 * Bold and dim are mutually exclusive in terminals.
 * This type ensures you can use one or the other, but not both.
 */
type WeightProps = {
  bold?: never;

```

---


### `src/ink/constants.ts`

**信息:**
- 行数: 2
- 大小: 107 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Shared frame interval for render throttling and animations (~60fps)
export const FRAME_INTERVAL_MS = 16

```

---


### `src/ink/cursor.ts`

**信息:**
- 行数: 7
- 大小: 107 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function hideCursor(): string {
  return ''
}

export function showCursor(): string {
  return ''
}

```

---


### `src/ink/dom.ts`

**信息:**
- 行数: 484
- 大小: 15126 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { FocusManager } from './focus.js'
import { createLayoutNode } from './layout/engine.js'
import type { LayoutNode } from './layout/node.js'
import { LayoutDisplay, LayoutMeasureMode } from './layout/node.js'
import measureText from './measure-text.js'
import { addPendingClear, nodeCache } from './node-cache.js'
import squashTextNodes from './squash-text-nodes.js'
import type { Styles, TextStyles } from './styles.js'
import { expandTabs } from './tabstops.js'
import wrapText from './wrap-text.js'

type InkNode = {
  parentNode: DOMElement | undefined
  yogaNode?: LayoutNode
  style: Styles
}

export type TextName = '#text'
export type ElementNames =
  | 'ink-root'
  | 'ink-box'
  | 'ink-text'
  | 'ink-virtual-text'
  | 'ink-link'
  | 'ink-progress'
  | 'ink-raw-ansi'

export type NodeNames = ElementNames | TextName

// eslint-disable-next-line @typescript-eslint/naming-convention
export type DOMElement = {
  nodeName: ElementNames
  attributes: Record<string, DOMNodeAttribute>
  childNodes: DOMNode[]
  textStyles?: TextStyles

  // Internal properties
  onComputeLayout?: () => void
  onRender?: () => void
  onImmediateRender?: () => void
  // Used to skip empty renders during React 19's effect double-invoke in test mode
  hasRenderedContent?: boolean

  // When true, this node needs re-rendering
  dirty: boolean
  // Set by the reconciler's hideInstance/unhideInstance; survives style updates.
  isHidden?: boolean
  // Event handlers set by the reconciler for the capture/bubble dispatcher.
  // Stored separately from attributes so handler identity changes don't
  // mark dirty and defeat the blit optimization.

```

---


### `src/ink/events/click-event.ts`

**信息:**
- 行数: 38
- 大小: 1332 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { Event } from './event.js'

/**
 * Mouse click event. Fired on left-button release without drag, only when
 * mouse tracking is enabled (i.e. inside <AlternateScreen>).
 *
 * Bubbles from the deepest hit node up through parentNode. Call
 * stopImmediatePropagation() to prevent ancestors' onClick from firing.
 */
export class ClickEvent extends Event {
  /** 0-indexed screen column of the click */
  readonly col: number
  /** 0-indexed screen row of the click */
  readonly row: number
  /**
   * Click column relative to the current handler's Box (col - box.x).
   * Recomputed by dispatchClick before each handler fires, so an onClick
   * on a container sees coords relative to that container, not to any
   * child the click landed on.
   */
  localCol = 0
  /** Click row relative to the current handler's Box (row - box.y). */
  localRow = 0
  /**
   * True if the clicked cell has no visible content (unwritten in the
   * screen buffer — both packed words are 0). Handlers can check this to
   * ignore clicks on blank space to the right of text, so accidental
   * clicks on empty terminal space don't toggle state.
   */
  readonly cellIsBlank: boolean

  constructor(col: number, row: number, cellIsBlank: boolean) {
    super()
    this.col = col
    this.row = row
    this.cellIsBlank = cellIsBlank
  }
}

```

---


### `src/ink/events/dispatcher.ts`

**信息:**
- 行数: 233
- 大小: 6004 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  ContinuousEventPriority,
  DefaultEventPriority,
  DiscreteEventPriority,
  NoEventPriority,
} from 'react-reconciler/constants.js'
import { logError } from '../../utils/log.js'
import { HANDLER_FOR_EVENT } from './event-handlers.js'
import type { EventTarget, TerminalEvent } from './terminal-event.js'

// --

type DispatchListener = {
  node: EventTarget
  handler: (event: TerminalEvent) => void
  phase: 'capturing' | 'at_target' | 'bubbling'
}

function getHandler(
  node: EventTarget,
  eventType: string,
  capture: boolean,
): ((event: TerminalEvent) => void) | undefined {
  const handlers = node._eventHandlers
  if (!handlers) return undefined

  const mapping = HANDLER_FOR_EVENT[eventType]
  if (!mapping) return undefined

  const propName = capture ? mapping.capture : mapping.bubble
  if (!propName) return undefined

  return handlers[propName] as ((event: TerminalEvent) => void) | undefined
}

/**
 * Collect all listeners for an event in dispatch order.
 *
 * Uses react-dom's two-phase accumulation pattern:
 * - Walk from target to root
 * - Capture handlers are prepended (unshift) → root-first
 * - Bubble handlers are appended (push) → target-first
 *
 * Result: [root-cap, ..., parent-cap, target-cap, target-bub, parent-bub, ..., root-bub]
 */
function collectListeners(
  target: EventTarget,
  event: TerminalEvent,
): DispatchListener[] {
  const listeners: DispatchListener[] = []

```

---


### `src/ink/events/emitter.ts`

**信息:**
- 行数: 39
- 大小: 1125 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { EventEmitter as NodeEventEmitter } from 'events'
import { Event } from './event.js'

// Similar to node's builtin EventEmitter, but is also aware of our `Event`
// class, and so `emit` respects `stopImmediatePropagation()`.
export class EventEmitter extends NodeEventEmitter {
  constructor() {
    super()
    // Disable the default maxListeners warning. In React, many components
    // can legitimately listen to the same event (e.g., useInput hooks).
    // The default limit of 10 causes spurious warnings.
    this.setMaxListeners(0)
  }

  override emit(type: string | symbol, ...args: unknown[]): boolean {
    // Delegate to node for `error`, since it's not treated like a normal event
    if (type === 'error') {
      return super.emit(type, ...args)
    }

    const listeners = this.rawListeners(type)

    if (listeners.length === 0) {
      return false
    }

    const ccEvent = args[0] instanceof Event ? args[0] : null

    for (const listener of listeners) {
      listener.apply(this, args)

      if (ccEvent?.didStopImmediatePropagation()) {
        break
      }
    }

    return true
  }
}

```

---


### `src/ink/events/event-handlers.ts`

**信息:**
- 行数: 73
- 大小: 2202 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ClickEvent } from './click-event.js'
import type { FocusEvent } from './focus-event.js'
import type { KeyboardEvent } from './keyboard-event.js'
import type { PasteEvent } from './paste-event.js'
import type { ResizeEvent } from './resize-event.js'

type KeyboardEventHandler = (event: KeyboardEvent) => void
type FocusEventHandler = (event: FocusEvent) => void
type PasteEventHandler = (event: PasteEvent) => void
type ResizeEventHandler = (event: ResizeEvent) => void
type ClickEventHandler = (event: ClickEvent) => void
type HoverEventHandler = () => void

/**
 * Props for event handlers on Box and other host components.
 *
 * Follows the React/DOM naming convention:
 * - onEventName: handler for bubble phase
 * - onEventNameCapture: handler for capture phase
 */
export type EventHandlerProps = {
  onKeyDown?: KeyboardEventHandler
  onKeyDownCapture?: KeyboardEventHandler

  onFocus?: FocusEventHandler
  onFocusCapture?: FocusEventHandler
  onBlur?: FocusEventHandler
  onBlurCapture?: FocusEventHandler

  onPaste?: PasteEventHandler
  onPasteCapture?: PasteEventHandler

  onResize?: ResizeEventHandler

  onClick?: ClickEventHandler
  onMouseEnter?: HoverEventHandler
  onMouseLeave?: HoverEventHandler
}

/**
 * Reverse lookup: event type string → handler prop names.
 * Used by the dispatcher for O(1) handler lookup per node.
 */
export const HANDLER_FOR_EVENT: Record<
  string,
  { bubble?: keyof EventHandlerProps; capture?: keyof EventHandlerProps }
> = {
  keydown: { bubble: 'onKeyDown', capture: 'onKeyDownCapture' },
  focus: { bubble: 'onFocus', capture: 'onFocusCapture' },
  blur: { bubble: 'onBlur', capture: 'onBlurCapture' },

```

---


### `src/ink/events/event.ts`

**信息:**
- 行数: 11
- 大小: 250 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export class Event {
  private _didStopImmediatePropagation = false

  didStopImmediatePropagation(): boolean {
    return this._didStopImmediatePropagation
  }

  stopImmediatePropagation(): void {
    this._didStopImmediatePropagation = true
  }
}

```

---


### `src/ink/events/focus-event.ts`

**信息:**
- 行数: 21
- 大小: 687 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { type EventTarget, TerminalEvent } from './terminal-event.js'

/**
 * Focus event for component focus changes.
 *
 * Dispatched when focus moves between elements. 'focus' fires on the
 * newly focused element, 'blur' fires on the previously focused one.
 * Both bubble, matching react-dom's use of focusin/focusout semantics
 * so parent components can observe descendant focus changes.
 */
export class FocusEvent extends TerminalEvent {
  readonly relatedTarget: EventTarget | null

  constructor(
    type: 'focus' | 'blur',
    relatedTarget: EventTarget | null = null,
  ) {
    super(type, { bubbles: true, cancelable: false })
    this.relatedTarget = relatedTarget
  }
}

```

---


### `src/ink/events/input-event.ts`

**信息:**
- 行数: 205
- 大小: 7306 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { nonAlphanumericKeys, type ParsedKey } from '../parse-keypress.js'
import { Event } from './event.js'

export type Key = {
  upArrow: boolean
  downArrow: boolean
  leftArrow: boolean
  rightArrow: boolean
  pageDown: boolean
  pageUp: boolean
  wheelUp: boolean
  wheelDown: boolean
  home: boolean
  end: boolean
  return: boolean
  escape: boolean
  ctrl: boolean
  shift: boolean
  fn: boolean
  tab: boolean
  backspace: boolean
  delete: boolean
  meta: boolean
  super: boolean
}

function parseKey(keypress: ParsedKey): [Key, string] {
  const key: Key = {
    upArrow: keypress.name === 'up',
    downArrow: keypress.name === 'down',
    leftArrow: keypress.name === 'left',
    rightArrow: keypress.name === 'right',
    pageDown: keypress.name === 'pagedown',
    pageUp: keypress.name === 'pageup',
    wheelUp: keypress.name === 'wheelup',
    wheelDown: keypress.name === 'wheeldown',
    home: keypress.name === 'home',
    end: keypress.name === 'end',
    return: keypress.name === 'return',
    escape: keypress.name === 'escape',
    fn: keypress.fn,
    ctrl: keypress.ctrl,
    shift: keypress.shift,
    tab: keypress.name === 'tab',
    backspace: keypress.name === 'backspace',
    delete: keypress.name === 'delete',
    // `parseKeypress` parses \u001B\u001B[A (meta + up arrow) as meta = false
    // but with option = true, so we need to take this into account here
    // to avoid breaking changes in Ink.
    // TODO(vadimdemedes): consider removing this in the next major version.

```

---


### `src/ink/events/keyboard-event.ts`

**信息:**
- 行数: 51
- 大小: 1765 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ParsedKey } from '../parse-keypress.js'
import { TerminalEvent } from './terminal-event.js'

/**
 * Keyboard event dispatched through the DOM tree via capture/bubble.
 *
 * Follows browser KeyboardEvent semantics: `key` is the literal character
 * for printable keys ('a', '3', ' ', '/') and a multi-char name for
 * special keys ('down', 'return', 'escape', 'f1'). The idiomatic
 * printable-char check is `e.key.length === 1`.
 */
export class KeyboardEvent extends TerminalEvent {
  readonly key: string
  readonly ctrl: boolean
  readonly shift: boolean
  readonly meta: boolean
  readonly superKey: boolean
  readonly fn: boolean

  constructor(parsedKey: ParsedKey) {
    super('keydown', { bubbles: true, cancelable: true })

    this.key = keyFromParsed(parsedKey)
    this.ctrl = parsedKey.ctrl
    this.shift = parsedKey.shift
    this.meta = parsedKey.meta || parsedKey.option
    this.superKey = parsedKey.super
    this.fn = parsedKey.fn
  }
}

function keyFromParsed(parsed: ParsedKey): string {
  const seq = parsed.sequence ?? ''
  const name = parsed.name ?? ''

  // Ctrl combos: sequence is a control byte (\x03 for ctrl+c), name is the
  // letter. Browsers report e.key === 'c' with e.ctrlKey === true.
  if (parsed.ctrl) return name

  // Single printable char (space through ~, plus anything above ASCII):
  // use the literal char. Browsers report e.key === '3', not 'Digit3'.
  if (seq.length === 1) {
    const code = seq.charCodeAt(0)
    if (code >= 0x20 && code !== 0x7f) return seq
  }

  // Special keys (arrows, F-keys, return, tab, escape, etc.): sequence is
  // either an escape sequence (\x1b[B) or a control byte (\r, \t), so use
  // the parsed name. Browsers report e.key === 'ArrowDown'.
  return name || seq

```

---


### `src/ink/events/paste-event.ts`

**信息:**
- 行数: 1
- 大小: 27 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export class PasteEvent {}

```

---


### `src/ink/events/resize-event.ts`

**信息:**
- 行数: 1
- 大小: 28 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export class ResizeEvent {}

```

---


### `src/ink/events/terminal-event.ts`

**信息:**
- 行数: 107
- 大小: 2526 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { Event } from './event.js'

type EventPhase = 'none' | 'capturing' | 'at_target' | 'bubbling'

type TerminalEventInit = {
  bubbles?: boolean
  cancelable?: boolean
}

/**
 * Base class for all terminal events with DOM-style propagation.
 *
 * Extends Event so existing event types (ClickEvent, InputEvent,
 * TerminalFocusEvent) share a common ancestor and can migrate later.
 *
 * Mirrors the browser's Event API: target, currentTarget, eventPhase,
 * stopPropagation(), preventDefault(), timeStamp.
 */
export class TerminalEvent extends Event {
  readonly type: string
  readonly timeStamp: number
  readonly bubbles: boolean
  readonly cancelable: boolean

  private _target: EventTarget | null = null
  private _currentTarget: EventTarget | null = null
  private _eventPhase: EventPhase = 'none'
  private _propagationStopped = false
  private _defaultPrevented = false

  constructor(type: string, init?: TerminalEventInit) {
    super()
    this.type = type
    this.timeStamp = performance.now()
    this.bubbles = init?.bubbles ?? true
    this.cancelable = init?.cancelable ?? true
  }

  get target(): EventTarget | null {
    return this._target
  }

  get currentTarget(): EventTarget | null {
    return this._currentTarget
  }

  get eventPhase(): EventPhase {
    return this._eventPhase
  }


```

---


### `src/ink/events/terminal-focus-event.ts`

**信息:**
- 行数: 19
- 大小: 512 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { Event } from './event.js'

export type TerminalFocusEventType = 'terminalfocus' | 'terminalblur'

/**
 * Event fired when the terminal window gains or loses focus.
 *
 * Uses DECSET 1004 focus reporting - the terminal sends:
 * - CSI I (\x1b[I) when the terminal gains focus
 * - CSI O (\x1b[O) when the terminal loses focus
 */
export class TerminalFocusEvent extends Event {
  readonly type: TerminalFocusEventType

  constructor(type: TerminalFocusEventType) {
    super()
    this.type = type
  }
}

```

---


### `src/ink/focus.ts`

**信息:**
- 行数: 181
- 大小: 5142 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { DOMElement } from './dom.js'
import { FocusEvent } from './events/focus-event.js'

const MAX_FOCUS_STACK = 32

/**
 * DOM-like focus manager for the Ink terminal UI.
 *
 * Pure state — tracks activeElement and a focus stack. Has no reference
 * to the tree; callers pass the root when tree walks are needed.
 *
 * Stored on the root DOMElement so any node can reach it by walking
 * parentNode (like browser's `node.ownerDocument`).
 */
export class FocusManager {
  activeElement: DOMElement | null = null
  private dispatchFocusEvent: (target: DOMElement, event: FocusEvent) => boolean
  private enabled = true
  private focusStack: DOMElement[] = []

  constructor(
    dispatchFocusEvent: (target: DOMElement, event: FocusEvent) => boolean,
  ) {
    this.dispatchFocusEvent = dispatchFocusEvent
  }

  focus(node: DOMElement): void {
    if (node === this.activeElement) return
    if (!this.enabled) return

    const previous = this.activeElement
    if (previous) {
      // Deduplicate before pushing to prevent unbounded growth from Tab cycling
      const idx = this.focusStack.indexOf(previous)
      if (idx !== -1) this.focusStack.splice(idx, 1)
      this.focusStack.push(previous)
      if (this.focusStack.length > MAX_FOCUS_STACK) this.focusStack.shift()
      this.dispatchFocusEvent(previous, new FocusEvent('blur', node))
    }
    this.activeElement = node
    this.dispatchFocusEvent(node, new FocusEvent('focus', previous))
  }

  blur(): void {
    if (!this.activeElement) return

    const previous = this.activeElement
    this.activeElement = null
    this.dispatchFocusEvent(previous, new FocusEvent('blur', null))
  }

```

---


### `src/ink/frame.ts`

**信息:**
- 行数: 124
- 大小: 4209 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Cursor } from './cursor.js'
import type { Size } from './layout/geometry.js'
import type { ScrollHint } from './render-node-to-output.js'
import {
  type CharPool,
  createScreen,
  type HyperlinkPool,
  type Screen,
  type StylePool,
} from './screen.js'

export type Frame = {
  readonly screen: Screen
  readonly viewport: Size
  readonly cursor: Cursor
  /** DECSTBM scroll optimization hint (alt-screen only, null otherwise). */
  readonly scrollHint?: ScrollHint | null
  /** A ScrollBox has remaining pendingScrollDelta — schedule another frame. */
  readonly scrollDrainPending?: boolean
}

export function emptyFrame(
  rows: number,
  columns: number,
  stylePool: StylePool,
  charPool: CharPool,
  hyperlinkPool: HyperlinkPool,
): Frame {
  return {
    screen: createScreen(0, 0, stylePool, charPool, hyperlinkPool),
    viewport: { width: columns, height: rows },
    cursor: { x: 0, y: 0, visible: true },
  }
}

export type FlickerReason = 'resize' | 'offscreen' | 'clear'

export type FrameEvent = {
  durationMs: number
  /** Phase breakdown in ms + patch count. Populated when the ink instance
   *  has frame-timing instrumentation enabled (via onFrame wiring). */
  phases?: {
    /** createRenderer output: DOM → yoga layout → screen buffer */
    renderer: number
    /** LogUpdate.render(): screen diff → Patch[] (the hot path this PR optimizes) */
    diff: number
    /** optimize(): patch merge/dedupe */
    optimize: number
    /** writeDiffToTerminal(): serialize patches → ANSI → stdout */
    write: number

```

---


### `src/ink/get-max-width.ts`

**信息:**
- 行数: 27
- 大小: 1149 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { LayoutEdge, type LayoutNode } from './layout/node.js'

/**
 * Returns the yoga node's content width (computed width minus padding and
 * border).
 *
 * Warning: can return a value WIDER than the parent container. In a
 * column-direction flex parent, width is the cross axis — align-items:
 * stretch never shrinks children below their intrinsic size, so the text
 * node overflows (standard CSS behavior). Yoga measures leaf nodes in two
 * passes: the AtMost pass determines width, the Exactly pass determines
 * height. getComputedWidth() reflects the wider AtMost result while
 * getComputedHeight() reflects the narrower Exactly result. Callers that
 * use this for wrapping should clamp to actual available screen space so
 * the rendered line count stays consistent with the layout height.
 */
const getMaxWidth = (yogaNode: LayoutNode): number => {
  return (
    yogaNode.getComputedWidth() -
    yogaNode.getComputedPadding(LayoutEdge.Left) -
    yogaNode.getComputedPadding(LayoutEdge.Right) -
    yogaNode.getComputedBorder(LayoutEdge.Left) -
    yogaNode.getComputedBorder(LayoutEdge.Right)
  )
}

export default getMaxWidth

```

---


### `src/ink/global.d.ts`

**信息:**
- 行数: 1
- 大小: 10 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export {}

```

---


### `src/ink/hit-test.ts`

**信息:**
- 行数: 130
- 大小: 4228 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { DOMElement } from './dom.js'
import { ClickEvent } from './events/click-event.js'
import type { EventHandlerProps } from './events/event-handlers.js'
import { nodeCache } from './node-cache.js'

/**
 * Find the deepest DOM element whose rendered rect contains (col, row).
 *
 * Uses the nodeCache populated by renderNodeToOutput — rects are in screen
 * coordinates with all offsets (including scrollTop translation) already
 * applied. Children are traversed in reverse so later siblings (painted on
 * top) win. Nodes not in nodeCache (not rendered this frame, or lacking a
 * yogaNode) are skipped along with their subtrees.
 *
 * Returns the hit node even if it has no onClick — dispatchClick walks up
 * via parentNode to find handlers.
 */
export function hitTest(
  node: DOMElement,
  col: number,
  row: number,
): DOMElement | null {
  const rect = nodeCache.get(node)
  if (!rect) return null
  if (
    col < rect.x ||
    col >= rect.x + rect.width ||
    row < rect.y ||
    row >= rect.y + rect.height
  ) {
    return null
  }
  // Later siblings paint on top; reversed traversal returns topmost hit.
  for (let i = node.childNodes.length - 1; i >= 0; i--) {
    const child = node.childNodes[i]!
    if (child.nodeName === '#text') continue
    const hit = hitTest(child, col, row)
    if (hit) return hit
  }
  return node
}

/**
 * Hit-test the root at (col, row) and bubble a ClickEvent from the deepest
 * containing node up through parentNode. Only nodes with an onClick handler
 * fire. Stops when a handler calls stopImmediatePropagation(). Returns
 * true if at least one onClick handler fired.
 */
export function dispatchClick(
  root: DOMElement,

```

---


### `src/ink/hooks/use-animation-frame.ts`

**信息:**
- 行数: 57
- 大小: 1933 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useContext, useEffect, useState } from 'react'
import { ClockContext } from '../components/ClockContext.js'
import type { DOMElement } from '../dom.js'
import { useTerminalViewport } from './use-terminal-viewport.js'

/**
 * Hook for synchronized animations that pause when offscreen.
 *
 * Returns a ref to attach to the animated element and the current animation time.
 * All instances share the same clock, so animations stay in sync.
 * The clock only runs when at least one keepAlive subscriber exists.
 *
 * Pass `null` to pause — unsubscribes from the clock so no ticks fire.
 * Time freezes at the last value and resumes from the current clock time
 * when a number is passed again.
 *
 * @param intervalMs - How often to update, or null to pause
 * @returns [ref, time] - Ref to attach to element, elapsed time in ms
 *
 * @example
 * function Spinner() {
 *   const [ref, time] = useAnimationFrame(120)
 *   const frame = Math.floor(time / 120) % FRAMES.length
 *   return <Box ref={ref}>{FRAMES[frame]}</Box>
 * }
 *
 * The clock automatically slows when the terminal is blurred,
 * so consumers don't need to handle focus state.
 */
export function useAnimationFrame(
  intervalMs: number | null = 16,
): [ref: (element: DOMElement | null) => void, time: number] {
  const clock = useContext(ClockContext)
  const [viewportRef, { isVisible }] = useTerminalViewport()
  const [time, setTime] = useState(() => clock?.now() ?? 0)

  const active = isVisible && intervalMs !== null

  useEffect(() => {
    if (!clock || !active) return

    let lastUpdate = clock.now()

    const onChange = (): void => {
      const now = clock.now()
      if (now - lastUpdate >= intervalMs!) {
        lastUpdate = now
        setTime(now)
      }
    }

```

---


### `src/ink/hooks/use-app.ts`

**信息:**
- 行数: 8
- 大小: 251 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useContext } from 'react'
import AppContext from '../components/AppContext.js'

/**
 * `useApp` is a React hook, which exposes a method to manually exit the app (unmount).
 */
const useApp = () => useContext(AppContext)
export default useApp

```

---


### `src/ink/hooks/use-declared-cursor.ts`

**信息:**
- 行数: 73
- 大小: 2996 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useContext, useLayoutEffect, useRef } from 'react'
import CursorDeclarationContext from '../components/CursorDeclarationContext.js'
import type { DOMElement } from '../dom.js'

/**
 * Declares where the terminal cursor should be parked after each frame.
 *
 * Terminal emulators render IME preedit text at the physical cursor
 * position, and screen readers / screen magnifiers track the native
 * cursor — so parking it at the text input's caret makes CJK input
 * appear inline and lets accessibility tools follow the input.
 *
 * Returns a ref callback to attach to the Box that contains the input.
 * The declared (line, column) is interpreted relative to that Box's
 * nodeCache rect (populated by renderNodeToOutput).
 *
 * Timing: Both ref attach and useLayoutEffect fire in React's layout
 * phase — after resetAfterCommit calls scheduleRender. scheduleRender
 * defers onRender via queueMicrotask, so onRender runs AFTER layout
 * effects commit and reads the fresh declaration on the first frame
 * (no one-keystroke lag). Test env uses onImmediateRender (synchronous,
 * no microtask), so tests compensate by calling ink.onRender()
 * explicitly after render.
 */
export function useDeclaredCursor({
  line,
  column,
  active,
}: {
  line: number
  column: number
  active: boolean
}): (element: DOMElement | null) => void {
  const setCursorDeclaration = useContext(CursorDeclarationContext)
  const nodeRef = useRef<DOMElement | null>(null)

  const setNode = useCallback((node: DOMElement | null) => {
    nodeRef.current = node
  }, [])

  // When active, set unconditionally. When inactive, clear conditionally
  // (only if the currently-declared node is ours). The node-identity check
  // handles two hazards:
  //   1. A memo()ized active instance elsewhere (e.g. the search input in
  //      a memo'd Footer) doesn't re-render this commit — an inactive
  //      instance re-rendering here must not clobber it.
  //   2. Sibling handoff (menu focus moving between list items) — when
  //      focus moves opposite to sibling order, the newly-inactive item's
  //      effect runs AFTER the newly-active item's set. Without the node
  //      check it would clobber.

```

---


### `src/ink/hooks/use-input.ts`

**信息:**
- 行数: 92
- 大小: 3107 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useEffect, useLayoutEffect } from 'react'
import { useEventCallback } from 'usehooks-ts'
import type { InputEvent, Key } from '../events/input-event.js'
import useStdin from './use-stdin.js'

type Handler = (input: string, key: Key, event: InputEvent) => void

type Options = {
  /**
   * Enable or disable capturing of user input.
   * Useful when there are multiple useInput hooks used at once to avoid handling the same input several times.
   *
   * @default true
   */
  isActive?: boolean
}

/**
 * This hook is used for handling user input.
 * It's a more convenient alternative to using `StdinContext` and listening to `data` events.
 * The callback you pass to `useInput` is called for each character when user enters any input.
 * However, if user pastes text and it's more than one character, the callback will be called only once and the whole string will be passed as `input`.
 *
 * ```
 * import {useInput} from 'ink';
 *
 * const UserInput = () => {
 *   useInput((input, key) => {
 *     if (input === 'q') {
 *       // Exit program
 *     }
 *
 *     if (key.leftArrow) {
 *       // Left arrow key pressed
 *     }
 *   });
 *
 *   return …
 * };
 * ```
 */
const useInput = (inputHandler: Handler, options: Options = {}) => {
  const { setRawMode, internal_exitOnCtrlC, internal_eventEmitter } = useStdin()

  // useLayoutEffect (not useEffect) so that raw mode is enabled synchronously
  // during React's commit phase, before render() returns. With useEffect, raw
  // mode setup is deferred to the next event loop tick via React's scheduler,
  // leaving the terminal in cooked mode — keystrokes echo and the cursor is
  // visible until the effect fires.
  useLayoutEffect(() => {

```

---


### `src/ink/hooks/use-interval.ts`

**信息:**
- 行数: 67
- 大小: 1796 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useContext, useEffect, useRef, useState } from 'react'
import { ClockContext } from '../components/ClockContext.js'

/**
 * Returns the clock time, updating at the given interval.
 * Subscribes as non-keepAlive — won't keep the clock alive on its own,
 * but updates whenever a keepAlive subscriber (e.g. the spinner)
 * is driving the clock.
 *
 * Use this to drive pure time-based computations (shimmer position,
 * frame index) from the shared clock.
 */
export function useAnimationTimer(intervalMs: number): number {
  const clock = useContext(ClockContext)
  const [time, setTime] = useState(() => clock?.now() ?? 0)

  useEffect(() => {
    if (!clock) return

    let lastUpdate = clock.now()

    const onChange = (): void => {
      const now = clock.now()
      if (now - lastUpdate >= intervalMs) {
        lastUpdate = now
        setTime(now)
      }
    }

    return clock.subscribe(onChange, false)
  }, [clock, intervalMs])

  return time
}

/**
 * Interval hook backed by the shared Clock.
 *
 * Unlike `useInterval` from `usehooks-ts` (which creates its own setInterval),
 * this piggybacks on the single shared clock so all timers consolidate into
 * one wake-up. Pass `null` for intervalMs to pause.
 */
export function useInterval(
  callback: () => void,
  intervalMs: number | null,
): void {
  const callbackRef = useRef(callback)
  callbackRef.current = callback

  const clock = useContext(ClockContext)

```

---


### `src/ink/hooks/use-search-highlight.ts`

**信息:**
- 行数: 53
- 大小: 2158 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useContext, useMemo } from 'react'
import StdinContext from '../components/StdinContext.js'
import type { DOMElement } from '../dom.js'
import instances from '../instances.js'
import type { MatchPosition } from '../render-to-screen.js'

/**
 * Set the search highlight query on the Ink instance. Non-empty → all
 * visible occurrences are inverted on the next frame (SGR 7, screen-buffer
 * overlay, same damage machinery as selection). Empty → clears.
 *
 * This is a screen-space highlight — it matches the RENDERED text, not the
 * source message text. Works for anything visible (bash output, file paths,
 * error messages) regardless of where it came from in the message tree. A
 * query that matched in source but got truncated/ellipsized in rendering
 * won't highlight; that's acceptable — we highlight what you see.
 */
export function useSearchHighlight(): {
  setQuery: (query: string) => void
  /** Paint an existing DOM subtree (from the MAIN tree) to a fresh
   *  Screen at its natural height, scan. Element-relative positions
   *  (row 0 = element top). Zero context duplication — the element
   *  IS the one built with all real providers. */
  scanElement: (el: DOMElement) => MatchPosition[]
  /** Position-based CURRENT highlight. Every frame writes yellow at
   *  positions[currentIdx] + rowOffset. The scan-highlight (inverse on
   *  all matches) still runs — this overlays on top. rowOffset tracks
   *  scroll; positions stay stable (message-relative). null clears. */
  setPositions: (
    state: {
      positions: MatchPosition[]
      rowOffset: number
      currentIdx: number
    } | null,
  ) => void
} {
  useContext(StdinContext) // anchor to App subtree for hook rules
  const ink = instances.get(process.stdout)
  return useMemo(() => {
    if (!ink) {
      return {
        setQuery: () => {},
        scanElement: () => [],
        setPositions: () => {},
      }
    }
    return {
      setQuery: (query: string) => ink.setSearchHighlight(query),
      scanElement: (el: DOMElement) => ink.scanElementSubtree(el),
      setPositions: state => ink.setSearchPositions(state),

```

---


### `src/ink/hooks/use-selection.ts`

**信息:**
- 行数: 104
- 大小: 4421 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useContext, useMemo, useSyncExternalStore } from 'react'
import StdinContext from '../components/StdinContext.js'
import instances from '../instances.js'
import {
  type FocusMove,
  type SelectionState,
  shiftAnchor,
} from '../selection.js'

/**
 * Access to text selection operations on the Ink instance (fullscreen only).
 * Returns no-op functions when fullscreen mode is disabled.
 */
export function useSelection(): {
  copySelection: () => string
  /** Copy without clearing the highlight (for copy-on-select). */
  copySelectionNoClear: () => string
  clearSelection: () => void
  hasSelection: () => boolean
  /** Read the raw mutable selection state (for drag-to-scroll). */
  getState: () => SelectionState | null
  /** Subscribe to selection mutations (start/update/finish/clear). */
  subscribe: (cb: () => void) => () => void
  /** Shift the anchor row by dRow, clamped to [minRow, maxRow]. */
  shiftAnchor: (dRow: number, minRow: number, maxRow: number) => void
  /** Shift anchor AND focus by dRow (keyboard scroll: whole selection
   *  tracks content). Clamped points get col reset to the full-width edge
   *  since their content was captured by captureScrolledRows. Reads
   *  screen.width from the ink instance for the col-reset boundary. */
  shiftSelection: (dRow: number, minRow: number, maxRow: number) => void
  /** Keyboard selection extension (shift+arrow): move focus, anchor fixed.
   *  Left/right wrap across rows; up/down clamp at viewport edges. */
  moveFocus: (move: FocusMove) => void
  /** Capture text from rows about to scroll out of the viewport (call
   *  BEFORE scrollBy so the screen buffer still has the outgoing rows). */
  captureScrolledRows: (
    firstRow: number,
    lastRow: number,
    side: 'above' | 'below',
  ) => void
  /** Set the selection highlight bg color (theme-piping; solid bg
   *  replaces the old SGR-7 inverse so syntax highlighting stays readable
   *  under selection). Call once on mount + whenever theme changes. */
  setSelectionBgColor: (color: string) => void
} {
  // Look up the Ink instance via stdout — same pattern as instances map.
  // StdinContext is available (it's always provided), and the Ink instance
  // is keyed by stdout which we can get from process.stdout since there's
  // only one Ink instance per process in practice.
  useContext(StdinContext) // anchor to App subtree for hook rules

```

---


### `src/ink/hooks/use-stdin.ts`

**信息:**
- 行数: 8
- 大小: 232 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useContext } from 'react'
import StdinContext from '../components/StdinContext.js'

/**
 * `useStdin` is a React hook, which exposes stdin stream.
 */
const useStdin = () => useContext(StdinContext)
export default useStdin

```

---


### `src/ink/hooks/use-tab-status.ts`

**信息:**
- 行数: 72
- 大小: 2175 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useContext, useEffect, useRef } from 'react'
import {
  CLEAR_TAB_STATUS,
  supportsTabStatus,
  tabStatus,
  wrapForMultiplexer,
} from '../termio/osc.js'
import type { Color } from '../termio/types.js'
import { TerminalWriteContext } from '../useTerminalNotification.js'

export type TabStatusKind = 'idle' | 'busy' | 'waiting'

const rgb = (r: number, g: number, b: number): Color => ({
  type: 'rgb',
  r,
  g,
  b,
})

// Per the OSC 21337 usage guide's suggested mapping.
const TAB_STATUS_PRESETS: Record<
  TabStatusKind,
  { indicator: Color; status: string; statusColor: Color }
> = {
  idle: {
    indicator: rgb(0, 215, 95),
    status: 'Idle',
    statusColor: rgb(136, 136, 136),
  },
  busy: {
    indicator: rgb(255, 149, 0),
    status: 'Working…',
    statusColor: rgb(255, 149, 0),
  },
  waiting: {
    indicator: rgb(95, 135, 255),
    status: 'Waiting',
    statusColor: rgb(95, 135, 255),
  },
}

/**
 * Declaratively set the tab-status indicator (OSC 21337).
 *
 * Emits a colored dot + short status text to the tab sidebar. Terminals
 * that don't support OSC 21337 discard the sequence silently, so this is
 * safe to call unconditionally. Wrapped for tmux/screen passthrough.
 *
 * Pass `null` to opt out. If a status was previously set, transitioning to
 * `null` emits CLEAR_TAB_STATUS so toggling off mid-session doesn't leave

```

---


### `src/ink/hooks/use-terminal-focus.ts`

**信息:**
- 行数: 16
- 大小: 556 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useContext } from 'react'
import TerminalFocusContext from '../components/TerminalFocusContext.js'

/**
 * Hook to check if the terminal has focus.
 *
 * Uses DECSET 1004 focus reporting - the terminal sends escape sequences
 * when it gains or loses focus. These are handled automatically
 * by Ink and filtered from useInput.
 *
 * @returns true if the terminal is focused (or focus state is unknown)
 */
export function useTerminalFocus(): boolean {
  const { isTerminalFocused } = useContext(TerminalFocusContext)
  return isTerminalFocused
}

```

---


### `src/ink/hooks/use-terminal-title.ts`

**信息:**
- 行数: 31
- 大小: 1020 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useContext, useEffect } from 'react'
import stripAnsi from 'strip-ansi'
import { OSC, osc } from '../termio/osc.js'
import { TerminalWriteContext } from '../useTerminalNotification.js'

/**
 * Declaratively set the terminal tab/window title.
 *
 * Pass a string to set the title. ANSI escape sequences are stripped
 * automatically so callers don't need to know about terminal encoding.
 * Pass `null` to opt out — the hook becomes a no-op and leaves the
 * terminal title untouched.
 *
 * On Windows, uses `process.title` (classic conhost doesn't support OSC).
 * Elsewhere, writes OSC 0 (set title+icon) via Ink's stdout.
 */
export function useTerminalTitle(title: string | null): void {
  const writeRaw = useContext(TerminalWriteContext)

  useEffect(() => {
    if (title === null || !writeRaw) return

    const clean = stripAnsi(title)

    if (process.platform === 'win32') {
      process.title = clean
    } else {
      writeRaw(osc(OSC.SET_TITLE_AND_ICON, clean))
    }
  }, [title, writeRaw])
}

```

---


### `src/ink/hooks/use-terminal-viewport.ts`

**信息:**
- 行数: 96
- 大小: 3977 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { useCallback, useContext, useLayoutEffect, useRef } from 'react'
import { TerminalSizeContext } from '../components/TerminalSizeContext.js'
import type { DOMElement } from '../dom.js'

type ViewportEntry = {
  /**
   * Whether the element is currently within the terminal viewport
   */
  isVisible: boolean
}

/**
 * Hook to detect if a component is within the terminal viewport.
 *
 * Returns a callback ref and a viewport entry object.
 * Attach the ref to the component you want to track.
 *
 * The entry is updated during the layout phase (useLayoutEffect) so callers
 * always read fresh values during render. Visibility changes do NOT trigger
 * re-renders on their own — callers that re-render for other reasons (e.g.
 * animation ticks, state changes) will pick up the latest value naturally.
 * This avoids infinite update loops when combined with other layout effects
 * that also call setState.
 *
 * @example
 * const [ref, entry] = useTerminalViewport()
 * return <Box ref={ref}><Animation enabled={entry.isVisible}>...</Animation></Box>
 */
export function useTerminalViewport(): [
  ref: (element: DOMElement | null) => void,
  entry: ViewportEntry,
] {
  const terminalSize = useContext(TerminalSizeContext)
  const elementRef = useRef<DOMElement | null>(null)
  const entryRef = useRef<ViewportEntry>({ isVisible: true })

  const setElement = useCallback((el: DOMElement | null) => {
    elementRef.current = el
  }, [])

  // Runs on every render because yoga layout values can change
  // without React being aware. Only updates the ref — no setState
  // to avoid cascading re-renders during the commit phase.
  // Walks the DOM ancestor chain fresh each time to avoid holding stale
  // references after yoga tree rebuilds.
  useLayoutEffect(() => {
    const element = elementRef.current
    if (!element?.yogaNode || !terminalSize) {
      return
    }

```

---


### `src/ink/ink.tsx`

**信息:**
- 行数: 1723
- 大小: 251886 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import autoBind from 'auto-bind';
import { closeSync, constants as fsConstants, openSync, readSync, writeSync } from 'fs';
import noop from 'lodash-es/noop.js';
import throttle from 'lodash-es/throttle.js';
import React, { type ReactNode } from 'react';
import type { FiberRoot } from 'react-reconciler';
import { ConcurrentRoot } from 'react-reconciler/constants.js';
import { onExit } from 'signal-exit';
import { flushInteractionTime } from 'src/bootstrap/state.js';
import { getYogaCounters } from 'src/native-ts/yoga-layout/index.js';
import { logForDebugging } from 'src/utils/debug.js';
import { logError } from 'src/utils/log.js';
import { format } from 'util';
import { colorize } from './colorize.js';
import App from './components/App.js';
import type { CursorDeclaration, CursorDeclarationSetter } from './components/CursorDeclarationContext.js';
import { FRAME_INTERVAL_MS } from './constants.js';
import * as dom from './dom.js';
import { KeyboardEvent } from './events/keyboard-event.js';
import { FocusManager } from './focus.js';
import { emptyFrame, type Frame, type FrameEvent } from './frame.js';
import { dispatchClick, dispatchHover } from './hit-test.js';
import instances from './instances.js';
import { LogUpdate } from './log-update.js';
import { nodeCache } from './node-cache.js';
import { optimize } from './optimizer.js';
import Output from './output.js';
import type { ParsedKey } from './parse-keypress.js';
import reconciler, { dispatcher, getLastCommitMs, getLastYogaMs, isDebugRepaintsEnabled, recordYogaMs, resetProfileCounters } from './reconciler.js';
import renderNodeToOutput, { consumeFollowScroll, didLayoutShift } from './render-node-to-output.js';
import { applyPositionedHighlight, type MatchPosition, scanPositions } from './render-to-screen.js';
import createRenderer, { type Renderer } from './renderer.js';
import { CellWidth, CharPool, cellAt, createScreen, HyperlinkPool, isEmptyCellAt, migrateScreenPools, StylePool } from './screen.js';
import { applySearchHighlight } from './searchHighlight.js';
import { applySelectionOverlay, captureScrolledRows, clearSelection, createSelectionState, extendSelection, type FocusMove, findPlainTextUrlAt, getSelectedText, hasSelection, moveFocus, type SelectionState, selectLineAt, selectWordAt, shiftAnchor, shiftSelection, shiftSelectionForFollow, startSelection, updateSelection } from './selection.js';
import { SYNC_OUTPUT_SUPPORTED, supportsExtendedKeys, type Terminal, writeDiffToTerminal } from './terminal.js';
import { CURSOR_HOME, cursorMove, cursorPosition, DISABLE_KITTY_KEYBOARD, DISABLE_MODIFY_OTHER_KEYS, ENABLE_KITTY_KEYBOARD, ENABLE_MODIFY_OTHER_KEYS, ERASE_SCREEN } from './termio/csi.js';
import { DBP, DFE, DISABLE_MOUSE_TRACKING, ENABLE_MOUSE_TRACKING, ENTER_ALT_SCREEN, EXIT_ALT_SCREEN, SHOW_CURSOR } from './termio/dec.js';
import { CLEAR_ITERM2_PROGRESS, CLEAR_TAB_STATUS, setClipboard, supportsTabStatus, wrapForMultiplexer } from './termio/osc.js';
import { TerminalWriteProvider } from './useTerminalNotification.js';

// Alt-screen: renderer.ts sets cursor.visible = !isTTY || screen.height===0,
// which is always false in alt-screen (TTY + content fills screen).
// Reusing a frozen object saves 1 allocation per frame.
const ALT_SCREEN_ANCHOR_CURSOR = Object.freeze({
  x: 0,
  y: 0,
  visible: false
});
const CURSOR_HOME_PATCH = Object.freeze({

```

---


### `src/ink/instances.ts`

**信息:**
- 行数: 10
- 大小: 410 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Store all instances of Ink (instance.js) to ensure that consecutive render() calls
// use the same instance of Ink and don't create a new one
//
// This map has to be stored in a separate file, because render.js creates instances,
// but instance.js should delete itself from the map on unmount

import type Ink from './ink.js'

const instances = new Map<NodeJS.WriteStream, Ink>()
export default instances

```

---


### `src/ink/layout/engine.ts`

**信息:**
- 行数: 6
- 大小: 177 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { LayoutNode } from './node.js'
import { createYogaLayoutNode } from './yoga.js'

export function createLayoutNode(): LayoutNode {
  return createYogaLayoutNode()
}

```

---


### `src/ink/layout/geometry.ts`

**信息:**
- 行数: 97
- 大小: 2471 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export type Point = {
  x: number
  y: number
}

export type Size = {
  width: number
  height: number
}

export type Rectangle = Point & Size

/** Edge insets (padding, margin, border) */
export type Edges = {
  top: number
  right: number
  bottom: number
  left: number
}

/** Create uniform edges */
export function edges(all: number): Edges
export function edges(vertical: number, horizontal: number): Edges
export function edges(
  top: number,
  right: number,
  bottom: number,
  left: number,
): Edges
export function edges(a: number, b?: number, c?: number, d?: number): Edges {
  if (b === undefined) {
    return { top: a, right: a, bottom: a, left: a }
  }
  if (c === undefined) {
    return { top: a, right: b, bottom: a, left: b }
  }
  return { top: a, right: b, bottom: c, left: d! }
}

/** Add two edge values */
export function addEdges(a: Edges, b: Edges): Edges {
  return {
    top: a.top + b.top,
    right: a.right + b.right,
    bottom: a.bottom + b.bottom,
    left: a.left + b.left,
  }
}

/** Zero edges constant */

```

---


### `src/ink/layout/node.ts`

**信息:**
- 行数: 152
- 大小: 4346 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// --
// Adapter interface for the layout engine (Yoga)

export const LayoutEdge = {
  All: 'all',
  Horizontal: 'horizontal',
  Vertical: 'vertical',
  Left: 'left',
  Right: 'right',
  Top: 'top',
  Bottom: 'bottom',
  Start: 'start',
  End: 'end',
} as const
export type LayoutEdge = (typeof LayoutEdge)[keyof typeof LayoutEdge]

export const LayoutGutter = {
  All: 'all',
  Column: 'column',
  Row: 'row',
} as const
export type LayoutGutter = (typeof LayoutGutter)[keyof typeof LayoutGutter]

export const LayoutDisplay = {
  Flex: 'flex',
  None: 'none',
} as const
export type LayoutDisplay = (typeof LayoutDisplay)[keyof typeof LayoutDisplay]

export const LayoutFlexDirection = {
  Row: 'row',
  RowReverse: 'row-reverse',
  Column: 'column',
  ColumnReverse: 'column-reverse',
} as const
export type LayoutFlexDirection =
  (typeof LayoutFlexDirection)[keyof typeof LayoutFlexDirection]

export const LayoutAlign = {
  Auto: 'auto',
  Stretch: 'stretch',
  FlexStart: 'flex-start',
  Center: 'center',
  FlexEnd: 'flex-end',
} as const
export type LayoutAlign = (typeof LayoutAlign)[keyof typeof LayoutAlign]

export const LayoutJustify = {
  FlexStart: 'flex-start',
  Center: 'center',

```

---


### `src/ink/layout/yoga.ts`

**信息:**
- 行数: 308
- 大小: 7400 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import Yoga, {
  Align,
  Direction,
  Display,
  Edge,
  FlexDirection,
  Gutter,
  Justify,
  MeasureMode,
  Overflow,
  PositionType,
  Wrap,
  type Node as YogaNode,
} from 'src/native-ts/yoga-layout/index.js'
import {
  type LayoutAlign,
  LayoutDisplay,
  type LayoutEdge,
  type LayoutFlexDirection,
  type LayoutGutter,
  type LayoutJustify,
  type LayoutMeasureFunc,
  LayoutMeasureMode,
  type LayoutNode,
  type LayoutOverflow,
  type LayoutPositionType,
  type LayoutWrap,
} from './node.js'

// --
// Edge/Gutter mapping

const EDGE_MAP: Record<LayoutEdge, Edge> = {
  all: Edge.All,
  horizontal: Edge.Horizontal,
  vertical: Edge.Vertical,
  left: Edge.Left,
  right: Edge.Right,
  top: Edge.Top,
  bottom: Edge.Bottom,
  start: Edge.Start,
  end: Edge.End,
}

const GUTTER_MAP: Record<LayoutGutter, Gutter> = {
  all: Gutter.All,
  column: Gutter.Column,
  row: Gutter.Row,
}


```

---


### `src/ink/line-width-cache.ts`

**信息:**
- 行数: 24
- 大小: 734 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { stringWidth } from './stringWidth.js'

// During streaming, text grows but completed lines are immutable.
// Caching stringWidth per-line avoids re-measuring hundreds of
// unchanged lines on every token (~50x reduction in stringWidth calls).
const cache = new Map<string, number>()

const MAX_CACHE_SIZE = 4096

export function lineWidth(line: string): number {
  const cached = cache.get(line)
  if (cached !== undefined) return cached

  const width = stringWidth(line)

  // Evict when cache grows too large (e.g. after many different responses).
  // Simple full-clear is fine — the cache repopulates in one frame.
  if (cache.size >= MAX_CACHE_SIZE) {
    cache.clear()
  }

  cache.set(line, width)
  return width
}

```

---


### `src/ink/log-update.ts`

**信息:**
- 行数: 773
- 大小: 27210 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  type AnsiCode,
  ansiCodesToString,
  diffAnsiCodes,
} from '@alcalzone/ansi-tokenize'
import { logForDebugging } from '../utils/debug.js'
import type { Diff, FlickerReason, Frame } from './frame.js'
import type { Point } from './layout/geometry.js'
import {
  type Cell,
  CellWidth,
  cellAt,
  charInCellAt,
  diffEach,
  type Hyperlink,
  isEmptyCellAt,
  type Screen,
  type StylePool,
  shiftRows,
  visibleCellAtIndex,
} from './screen.js'
import {
  CURSOR_HOME,
  scrollDown as csiScrollDown,
  scrollUp as csiScrollUp,
  RESET_SCROLL_REGION,
  setScrollRegion,
} from './termio/csi.js'
import { LINK_END, link as oscLink } from './termio/osc.js'

type State = {
  previousOutput: string
}

type Options = {
  isTTY: boolean
  stylePool: StylePool
}

const CARRIAGE_RETURN = { type: 'carriageReturn' } as const
const NEWLINE = { type: 'stdout', content: '\n' } as const

export class LogUpdate {
  private state: State

  constructor(private readonly options: Options) {
    this.state = {
      previousOutput: '',
    }
  }

```

---


### `src/ink/measure-element.ts`

**信息:**
- 行数: 23
- 大小: 419 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { DOMElement } from './dom.js'

type Output = {
  /**
   * Element width.
   */
  width: number

  /**
   * Element height.
   */
  height: number
}

/**
 * Measure the dimensions of a particular `<Box>` element.
 */
const measureElement = (node: DOMElement): Output => ({
  width: node.yogaNode?.getComputedWidth() ?? 0,
  height: node.yogaNode?.getComputedHeight() ?? 0,
})

export default measureElement

```

---


### `src/ink/measure-text.ts`

**信息:**
- 行数: 47
- 大小: 1138 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { lineWidth } from './line-width-cache.js'

type Output = {
  width: number
  height: number
}

// Single-pass measurement: computes both width and height in one
// iteration instead of two (widestLine + countVisualLines).
// Uses indexOf to avoid array allocation from split('\n').
function measureText(text: string, maxWidth: number): Output {
  if (text.length === 0) {
    return {
      width: 0,
      height: 0,
    }
  }

  // Infinite or non-positive width means no wrapping — each line is one visual line.
  // Must check before the loop since Math.ceil(w / Infinity) = 0.
  const noWrap = maxWidth <= 0 || !Number.isFinite(maxWidth)

  let height = 0
  let width = 0
  let start = 0

  while (start <= text.length) {
    const end = text.indexOf('\n', start)
    const line = end === -1 ? text.substring(start) : text.substring(start, end)

    const w = lineWidth(line)
    width = Math.max(width, w)

    if (noWrap) {
      height++
    } else {
      height += w === 0 ? 1 : Math.ceil(w / maxWidth)
    }

    if (end === -1) break
    start = end + 1
  }

  return { width, height }
}

export default measureText

```

---


### `src/ink/node-cache.ts`

**信息:**
- 行数: 54
- 大小: 1654 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { DOMElement } from './dom.js'
import type { Rectangle } from './layout/geometry.js'

/**
 * Cached layout bounds for each rendered node (used for blit + clearing).
 * `top` is the yoga-local getComputedTop() — stored so ScrollBox viewport
 * culling can skip yoga reads for clean children whose position hasn't
 * shifted (O(dirty) instead of O(mounted) first-pass).
 */
export type CachedLayout = {
  x: number
  y: number
  width: number
  height: number
  top?: number
}

export const nodeCache = new WeakMap<DOMElement, CachedLayout>()

/** Rects of removed children that need clearing on next render */
export const pendingClears = new WeakMap<DOMElement, Rectangle[]>()

/**
 * Set when a pendingClear is added for an absolute-positioned node.
 * Signals renderer to disable blit for the next frame: the removed node
 * may have painted over non-siblings (e.g. an overlay over a ScrollBox
 * earlier in tree order), so their blits from prevScreen would restore
 * the overlay's pixels. Normal-flow removals are already handled by
 * hasRemovedChild at the parent level; only absolute positioning paints
 * cross-subtree. Reset at the start of each render.
 */
let absoluteNodeRemoved = false

export function addPendingClear(
  parent: DOMElement,
  rect: Rectangle,
  isAbsolute: boolean,
): void {
  const existing = pendingClears.get(parent)
  if (existing) {
    existing.push(rect)
  } else {
    pendingClears.set(parent, [rect])
  }
  if (isAbsolute) {
    absoluteNodeRemoved = true
  }
}

export function consumeAbsoluteRemovedFlag(): boolean {

```

---


### `src/ink/optimizer.ts`

**信息:**
- 行数: 93
- 大小: 2588 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { Diff } from './frame.js'

/**
 * Optimize a diff by applying all optimization rules in a single pass.
 * This reduces the number of patches that need to be written to the terminal.
 *
 * Rules applied:
 * - Remove empty stdout patches
 * - Merge consecutive cursorMove patches
 * - Remove no-op cursorMove (0,0) patches
 * - Concat adjacent style patches (transition diffs — can't drop either)
 * - Dedupe consecutive hyperlinks with same URI
 * - Cancel cursor hide/show pairs
 * - Remove clear patches with count 0
 */
export function optimize(diff: Diff): Diff {
  if (diff.length <= 1) {
    return diff
  }

  const result: Diff = []
  let len = 0

  for (const patch of diff) {
    const type = patch.type

    // Skip no-ops
    if (type === 'stdout') {
      if (patch.content === '') continue
    } else if (type === 'cursorMove') {
      if (patch.x === 0 && patch.y === 0) continue
    } else if (type === 'clear') {
      if (patch.count === 0) continue
    }

    // Try to merge with previous patch
    if (len > 0) {
      const lastIdx = len - 1
      const last = result[lastIdx]!
      const lastType = last.type

      // Merge consecutive cursorMove
      if (type === 'cursorMove' && lastType === 'cursorMove') {
        result[lastIdx] = {
          type: 'cursorMove',
          x: last.x + patch.x,
          y: last.y + patch.y,
        }
        continue
      }

```

---


### `src/ink/output.ts`

**信息:**
- 行数: 797
- 大小: 26183 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  type AnsiCode,
  type StyledChar,
  styledCharsFromTokens,
  tokenize,
} from '@alcalzone/ansi-tokenize'
import { logForDebugging } from '../utils/debug.js'
import { getGraphemeSegmenter } from '../utils/intl.js'
import sliceAnsi from '../utils/sliceAnsi.js'
import { reorderBidi } from './bidi.js'
import { type Rectangle, unionRect } from './layout/geometry.js'
import {
  blitRegion,
  CellWidth,
  extractHyperlinkFromStyles,
  filterOutHyperlinkStyles,
  markNoSelectRegion,
  OSC8_PREFIX,
  resetScreen,
  type Screen,
  type StylePool,
  setCellAt,
  shiftRows,
} from './screen.js'
import { stringWidth } from './stringWidth.js'
import { widestLine } from './widest-line.js'

/**
 * A grapheme cluster with precomputed terminal width, styleId, and hyperlink.
 * Built once per unique line (cached via charCache), so the per-char hot loop
 * is just property reads + setCellAt — no stringWidth, no style interning,
 * no hyperlink extraction per frame.
 *
 * styleId is safe to cache: StylePool is session-lived (never reset).
 * hyperlink is stored as a string (not interned ID) since hyperlinkPool
 * resets every 5 min; setCellAt interns it per-frame (cheap Map.get).
 */
type ClusteredChar = {
  value: string
  width: number
  styleId: number
  hyperlink: string | undefined
}

/**
 * Collects write/blit/clear/clip operations from the render tree, then
 * applies them to a Screen buffer in `get()`. The Screen is what gets
 * diffed against the previous frame to produce terminal updates.
 */


```

---


### `src/ink/parse-keypress.ts`

**信息:**
- 行数: 801
- 大小: 23458 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Keyboard input parser - converts terminal input to key events
 *
 * Uses the termio tokenizer for escape sequence boundary detection,
 * then interprets sequences as keypresses.
 */
import { Buffer } from 'buffer'
import { PASTE_END, PASTE_START } from './termio/csi.js'
import { createTokenizer, type Tokenizer } from './termio/tokenize.js'

// eslint-disable-next-line no-control-regex
const META_KEY_CODE_RE = /^(?:\x1b)([a-zA-Z0-9])$/

// eslint-disable-next-line no-control-regex
const FN_KEY_RE =
  // eslint-disable-next-line no-control-regex
  /^(?:\x1b+)(O|N|\[|\[\[)(?:(\d+)(?:;(\d+))?([~^$])|(?:1;)?(\d+)?([a-zA-Z]))/

// CSI u (kitty keyboard protocol): ESC [ codepoint [; modifier] u
// Example: ESC[13;2u = Shift+Enter, ESC[27u = Escape (no modifiers)
// Modifier is optional - when absent, defaults to 1 (no modifiers)
// eslint-disable-next-line no-control-regex
const CSI_U_RE = /^\x1b\[(\d+)(?:;(\d+))?u/

// xterm modifyOtherKeys: ESC [ 27 ; modifier ; keycode ~
// Example: ESC[27;2;13~ = Shift+Enter. Emitted by Ghostty/tmux/xterm when
// modifyOtherKeys=2 is active or via user keybinds, typically over SSH where
// TERM sniffing misses Ghostty and we never push Kitty keyboard mode.
// Note param order is reversed vs CSI u (modifier first, keycode second).
// eslint-disable-next-line no-control-regex
const MODIFY_OTHER_KEYS_RE = /^\x1b\[27;(\d+);(\d+)~/

// -- Terminal response patterns (inbound sequences from the terminal itself) --
// DECRPM: CSI ? Ps ; Pm $ y  — response to DECRQM (request mode)
// eslint-disable-next-line no-control-regex
const DECRPM_RE = /^\x1b\[\?(\d+);(\d+)\$y$/
// DA1: CSI ? Ps ; ... c  — primary device attributes response
// eslint-disable-next-line no-control-regex
const DA1_RE = /^\x1b\[\?([\d;]*)c$/
// DA2: CSI > Ps ; ... c  — secondary device attributes response
// eslint-disable-next-line no-control-regex
const DA2_RE = /^\x1b\[>([\d;]*)c$/
// Kitty keyboard flags: CSI ? flags u  — response to CSI ? u query
// (private ? marker distinguishes from CSI u key events)
// eslint-disable-next-line no-control-regex
const KITTY_FLAGS_RE = /^\x1b\[\?(\d+)u$/
// DECXCPR cursor position: CSI ? row ; col R
// The ? marker disambiguates from modified F3 keys (Shift+F3 = CSI 1;2 R,
// Ctrl+F3 = CSI 1;5 R, etc.) — plain CSI row;col R is genuinely ambiguous.
// eslint-disable-next-line no-control-regex

```

---


### `src/ink/reconciler.ts`

**信息:**
- 行数: 512
- 大小: 14594 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/* eslint-disable custom-rules/no-top-level-side-effects */

import { appendFileSync } from 'fs'
import createReconciler from 'react-reconciler'
import { getYogaCounters } from 'src/native-ts/yoga-layout/index.js'
import { isEnvTruthy } from '../utils/envUtils.js'
import {
  appendChildNode,
  clearYogaNodeReferences,
  createNode,
  createTextNode,
  type DOMElement,
  type DOMNodeAttribute,
  type ElementNames,
  insertBeforeNode,
  markDirty,
  removeChildNode,
  setAttribute,
  setStyle,
  setTextNodeValue,
  setTextStyles,
  type TextNode,
} from './dom.js'
import { Dispatcher } from './events/dispatcher.js'
import { EVENT_HANDLER_PROPS } from './events/event-handlers.js'
import { getFocusManager, getRootNode } from './focus.js'
import { LayoutDisplay } from './layout/node.js'
import applyStyles, { type Styles, type TextStyles } from './styles.js'

// We need to conditionally perform devtools connection to avoid
// accidentally breaking other third-party code.
// See https://github.com/vadimdemedes/ink/issues/384
if (process.env.NODE_ENV === 'development') {
  try {
    // eslint-disable-next-line custom-rules/no-top-level-dynamic-import -- dev-only; NODE_ENV check is DCE'd in production
    void import('./devtools.js')
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    if (error.code === 'ERR_MODULE_NOT_FOUND') {
      // biome-ignore lint/suspicious/noConsole: intentional warning
      console.warn(
        `
The environment variable DEV is set to true, so Ink tried to import \`react-devtools-core\`,
but this failed as it was not installed. Debugging with React Devtools requires it.

To install use this command:

$ npm install --save-dev react-devtools-core
				`.trim() + '\n',
      )

```

---


### `src/ink/render-border.ts`

**信息:**
- 行数: 231
- 大小: 6642 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import chalk from 'chalk'
import cliBoxes, { type Boxes, type BoxStyle } from 'cli-boxes'
import { applyColor } from './colorize.js'
import type { DOMNode } from './dom.js'
import type Output from './output.js'
import { stringWidth } from './stringWidth.js'
import type { Color } from './styles.js'

export type BorderTextOptions = {
  content: string // Pre-rendered string with ANSI color codes
  position: 'top' | 'bottom'
  align: 'start' | 'end' | 'center'
  offset?: number // Only used with 'start' or 'end' alignment. Number of characters from the edge.
}

export const CUSTOM_BORDER_STYLES = {
  dashed: {
    top: '╌',
    left: '╎',
    right: '╎',
    bottom: '╌',
    // there aren't any line-drawing characters for dashes unfortunately
    topLeft: ' ',
    topRight: ' ',
    bottomLeft: ' ',
    bottomRight: ' ',
  },
} as const

export type BorderStyle =
  | keyof Boxes
  | keyof typeof CUSTOM_BORDER_STYLES
  | BoxStyle

function embedTextInBorder(
  borderLine: string,
  text: string,
  align: 'start' | 'end' | 'center',
  offset: number = 0,
  borderChar: string,
): [before: string, text: string, after: string] {
  const textLength = stringWidth(text)
  const borderLength = borderLine.length

  if (textLength >= borderLength - 2) {
    return ['', text.substring(0, borderLength), '']
  }

  let position: number
  if (align === 'center') {

```

---


### `src/ink/render-node-to-output.ts`

**信息:**
- 行数: 1462
- 大小: 63281 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import indentString from 'indent-string'
import { applyTextStyles } from './colorize.js'
import type { DOMElement } from './dom.js'
import getMaxWidth from './get-max-width.js'
import type { Rectangle } from './layout/geometry.js'
import { LayoutDisplay, LayoutEdge, type LayoutNode } from './layout/node.js'
import { nodeCache, pendingClears } from './node-cache.js'
import type Output from './output.js'
import renderBorder from './render-border.js'
import type { Screen } from './screen.js'
import {
  type StyledSegment,
  squashTextNodesToSegments,
} from './squash-text-nodes.js'
import type { Color } from './styles.js'
import { isXtermJs } from './terminal.js'
import { widestLine } from './widest-line.js'
import wrapText from './wrap-text.js'

// Matches detectXtermJsWheel() in ScrollKeybindingHandler.tsx — the curve
// and drain must agree on terminal detection. TERM_PROGRAM check is the sync
// fallback; isXtermJs() is the authoritative XTVERSION-probe result.
function isXtermJsHost(): boolean {
  return process.env.TERM_PROGRAM === 'vscode' || isXtermJs()
}

// Per-frame scratch: set when any node's yoga position/size differs from
// its cached value, or a child was removed. Read by ink.tsx to decide
// whether the full-damage sledgehammer (PR #20120) is needed this frame.
// Applies on both alt-screen and main-screen. Steady-state frames
// (spinner tick, clock tick, text append into a fixed-height box) don't
// shift layout → narrow damage bounds → O(changed cells) diff instead of
// O(rows×cols).
let layoutShifted = false

export function resetLayoutShifted(): void {
  layoutShifted = false
}

export function didLayoutShift(): boolean {
  return layoutShifted
}

// DECSTBM scroll optimization hint. When a ScrollBox's scrollTop changes
// between frames (and nothing else moved), log-update.ts can emit a
// hardware scroll (DECSTBM + SU/SD) instead of rewriting the whole
// viewport. top/bottom are 0-indexed inclusive screen rows; delta > 0 =
// content moved up (scrollTop increased, CSI n S).
export type ScrollHint = { top: number; bottom: number; delta: number }
let scrollHint: ScrollHint | null = null

```

---


### `src/ink/render-to-screen.ts`

**信息:**
- 行数: 231
- 大小: 8570 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import noop from 'lodash-es/noop.js'
import type { ReactElement } from 'react'
import { LegacyRoot } from 'react-reconciler/constants.js'
import { logForDebugging } from '../utils/debug.js'
import { createNode, type DOMElement } from './dom.js'
import { FocusManager } from './focus.js'
import Output from './output.js'
import reconciler from './reconciler.js'
import renderNodeToOutput, {
  resetLayoutShifted,
} from './render-node-to-output.js'
import {
  CellWidth,
  CharPool,
  cellAtIndex,
  createScreen,
  HyperlinkPool,
  type Screen,
  StylePool,
  setCellStyleId,
} from './screen.js'

/** Position of a match within a rendered message, relative to the message's
 *  own bounding box (row 0 = message top). Stable across scroll — to
 *  highlight on the real screen, add the message's screen-row offset. */
export type MatchPosition = {
  row: number
  col: number
  /** Number of CELLS the match spans (= query.length for ASCII, more
   *  for wide chars in the query). */
  len: number
}

// Shared across calls. Pools accumulate style/char interns — reusing them
// means later calls hit cache more. Root/container reuse saves the
// createContainer cost (~1ms). LegacyRoot: all work sync, no scheduling —
// ConcurrentRoot's scheduler backlog leaks across roots via flushSyncWork.
let root: DOMElement | undefined
let container: ReturnType<typeof reconciler.createContainer> | undefined
let stylePool: StylePool | undefined
let charPool: CharPool | undefined
let hyperlinkPool: HyperlinkPool | undefined
let output: Output | undefined

const timing = { reconcile: 0, yoga: 0, paint: 0, scan: 0, calls: 0 }
const LOG_EVERY = 20

/** Render a React element (wrapped in all contexts the component needs —
 *  caller's job) to an isolated Screen buffer at the given width. Returns
 *  the Screen + natural height (from yoga). Used for search: render ONE

```

---


### `src/ink/renderer.ts`

**信息:**
- 行数: 178
- 大小: 7665 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { logForDebugging } from 'src/utils/debug.js'
import { type DOMElement, markDirty } from './dom.js'
import type { Frame } from './frame.js'
import { consumeAbsoluteRemovedFlag } from './node-cache.js'
import Output from './output.js'
import renderNodeToOutput, {
  getScrollDrainNode,
  getScrollHint,
  resetLayoutShifted,
  resetScrollDrainNode,
  resetScrollHint,
} from './render-node-to-output.js'
import { createScreen, type StylePool } from './screen.js'

export type RenderOptions = {
  frontFrame: Frame
  backFrame: Frame
  isTTY: boolean
  terminalWidth: number
  terminalRows: number
  altScreen: boolean
  // True when the previous frame's screen buffer was mutated post-render
  // (selection overlay), reset to blank (alt-screen enter/resize/SIGCONT),
  // or reset to 0×0 (forceRedraw). Blitting from such a prevScreen would
  // copy stale inverted cells, blanks, or nothing. When false, blit is safe.
  prevFrameContaminated: boolean
}

export type Renderer = (options: RenderOptions) => Frame

export default function createRenderer(
  node: DOMElement,
  stylePool: StylePool,
): Renderer {
  // Reuse Output across frames so charCache (tokenize + grapheme clustering)
  // persists — most lines don't change between renders.
  let output: Output | undefined
  return options => {
    const { frontFrame, backFrame, isTTY, terminalWidth, terminalRows } =
      options
    const prevScreen = frontFrame.screen
    const backScreen = backFrame.screen
    // Read pools from the back buffer's screen — pools may be replaced
    // between frames (generational reset), so we can't capture them in the closure
    const charPool = backScreen.charPool
    const hyperlinkPool = backScreen.hyperlinkPool

    // Return empty frame if yoga node doesn't exist or layout hasn't been computed yet.
    // getComputedHeight() returns NaN before calculateLayout() is called.
    // Also check for invalid dimensions (negative, Infinity) that would cause RangeError

```

---


### `src/ink/root.ts`

**信息:**
- 行数: 184
- 大小: 4600 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ReactNode } from 'react'
import { logForDebugging } from 'src/utils/debug.js'
import { Stream } from 'stream'
import type { FrameEvent } from './frame.js'
import Ink, { type Options as InkOptions } from './ink.js'
import instances from './instances.js'

export type RenderOptions = {
  /**
   * Output stream where app will be rendered.
   *
   * @default process.stdout
   */
  stdout?: NodeJS.WriteStream
  /**
   * Input stream where app will listen for input.
   *
   * @default process.stdin
   */
  stdin?: NodeJS.ReadStream
  /**
   * Error stream.
   * @default process.stderr
   */
  stderr?: NodeJS.WriteStream
  /**
   * Configure whether Ink should listen to Ctrl+C keyboard input and exit the app. This is needed in case `process.stdin` is in raw mode, because then Ctrl+C is ignored by default and process is expected to handle it manually.
   *
   * @default true
   */
  exitOnCtrlC?: boolean

  /**
   * Patch console methods to ensure console output doesn't mix with Ink output.
   *
   * @default true
   */
  patchConsole?: boolean

  /**
   * Called after each frame render with timing and flicker information.
   */
  onFrame?: (event: FrameEvent) => void
}

export type Instance = {
  /**
   * Replace previous root node with a new one or update props of the current root node.
   */
  rerender: Ink['render']

```

---


### `src/ink/screen.ts`

**信息:**
- 行数: 1486
- 大小: 49323 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  type AnsiCode,
  ansiCodesToString,
  diffAnsiCodes,
} from '@alcalzone/ansi-tokenize'
import {
  type Point,
  type Rectangle,
  type Size,
  unionRect,
} from './layout/geometry.js'
import { BEL, ESC, SEP } from './termio/ansi.js'
import * as warn from './warn.js'

// --- Shared Pools (interning for memory efficiency) ---

// Character string pool shared across all screens.
// With a shared pool, interned char IDs are valid across screens,
// so blitRegion can copy IDs directly (no re-interning) and
// diffEach can compare IDs as integers (no string lookup).
export class CharPool {
  private strings: string[] = [' ', ''] // Index 0 = space, 1 = empty (spacer)
  private stringMap = new Map<string, number>([
    [' ', 0],
    ['', 1],
  ])
  private ascii: Int32Array = initCharAscii() // charCode → index, -1 = not interned

  intern(char: string): number {
    // ASCII fast-path: direct array lookup instead of Map.get
    if (char.length === 1) {
      const code = char.charCodeAt(0)
      if (code < 128) {
        const cached = this.ascii[code]!
        if (cached !== -1) return cached
        const index = this.strings.length
        this.strings.push(char)
        this.ascii[code] = index
        return index
      }
    }
    const existing = this.stringMap.get(char)
    if (existing !== undefined) return existing
    const index = this.strings.length
    this.strings.push(char)
    this.stringMap.set(char, index)
    return index
  }

  get(index: number): string {

```

---


### `src/ink/searchHighlight.ts`

**信息:**
- 行数: 93
- 大小: 3325 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  CellWidth,
  cellAtIndex,
  type Screen,
  type StylePool,
  setCellStyleId,
} from './screen.js'

/**
 * Highlight all visible occurrences of `query` in the screen buffer by
 * inverting cell styles (SGR 7). Post-render, same damage-tracking machinery
 * as applySelectionOverlay — the diff picks up highlighted cells as ordinary
 * changes, LogUpdate stays a pure diff engine.
 *
 * Case-insensitive. Handles wide characters (CJK, emoji) by building a
 * col-of-char map per row — the Nth character isn't at col N when wide chars
 * are present (each occupies 2 cells: head + SpacerTail).
 *
 * This ONLY inverts — there is no "current match" logic here. The yellow
 * current-match overlay is handled separately by applyPositionedHighlight
 * (render-to-screen.ts), which writes on top using positions scanned from
 * the target message's DOM subtree.
 *
 * Returns true if any match was highlighted (damage gate — caller forces
 * full-frame damage when true).
 */
export function applySearchHighlight(
  screen: Screen,
  query: string,
  stylePool: StylePool,
): boolean {
  if (!query) return false
  const lq = query.toLowerCase()
  const qlen = lq.length
  const w = screen.width
  const noSelect = screen.noSelect
  const height = screen.height

  let applied = false
  for (let row = 0; row < height; row++) {
    const rowOff = row * w
    // Build row text (already lowercased) + code-unit→cell-index map.
    // Three skip conditions, all aligned with setCellStyleId /
    // extractRowText (selection.ts):
    //   - SpacerTail: 2nd cell of a wide char, no char of its own
    //   - SpacerHead: end-of-line padding when a wide char wraps
    //   - noSelect: gutters (⎿, line numbers) — same exclusion as
    //     applySelectionOverlay. "Highlight what you see" still holds for
    //     content; gutters aren't search targets.
    // Lowercasing per-char (not on the joined string at the end) means

```

---


### `src/ink/selection.ts`

**信息:**
- 行数: 917
- 大小: 34933 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Text selection state for fullscreen mode.
 *
 * Tracks a linear selection in screen-buffer coordinates (0-indexed col/row).
 * Selection is line-based: cells from (startCol, startRow) through
 * (endCol, endRow) inclusive, wrapping across line boundaries. This matches
 * terminal-native selection behavior (not rectangular/block).
 *
 * The selection is stored as ANCHOR (where the drag started) + FOCUS (where
 * the cursor is now). The rendered highlight normalizes to start ≤ end.
 */

import { clamp } from './layout/geometry.js'
import type { Screen, StylePool } from './screen.js'
import { CellWidth, cellAt, cellAtIndex, setCellStyleId } from './screen.js'

type Point = { col: number; row: number }

export type SelectionState = {
  /** Where the mouse-down occurred. Null when no selection. */
  anchor: Point | null
  /** Current drag position (updated on mouse-move while dragging). */
  focus: Point | null
  /** True between mouse-down and mouse-up. */
  isDragging: boolean
  /** For word/line mode: the initial word/line bounds from the first
   *  multi-click. Drag extends from this span to the word/line at the
   *  current mouse position so the original word/line stays selected
   *  even when dragging backward past it. Null ⇔ char mode. The kind
   *  tells extendSelection whether to snap to word or line boundaries. */
  anchorSpan: { lo: Point; hi: Point; kind: 'word' | 'line' } | null
  /** Text from rows that scrolled out ABOVE the viewport during
   *  drag-to-scroll. The screen buffer only holds the current viewport,
   *  so without this accumulator, dragging down past the bottom edge
   *  loses the top of the selection once the anchor clamps. Prepended
   *  to the on-screen text by getSelectedText. Reset on start/clear. */
  scrolledOffAbove: string[]
  /** Symmetric: rows scrolled out BELOW when dragging up. Appended. */
  scrolledOffBelow: string[]
  /** Soft-wrap bits parallel to scrolledOffAbove — true means the row
   *  is a continuation of the one before it (the `\n` was inserted by
   *  word-wrap, not in the source). Captured alongside the text at
   *  scroll time since the screen's softWrap bitmap shifts with content.
   *  getSelectedText uses these to join wrapped rows back into logical
   *  lines. */
  scrolledOffAboveSW: boolean[]
  /** Parallel to scrolledOffBelow. */
  scrolledOffBelowSW: boolean[]
  /** Pre-clamp anchor row. Set when shiftSelection clamps anchor so a
   *  reverse scroll can restore the true position and pop accumulators.

```

---


### `src/ink/squash-text-nodes.ts`

**信息:**
- 行数: 92
- 大小: 2293 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { DOMElement } from './dom.js'
import type { TextStyles } from './styles.js'

/**
 * A segment of text with its associated styles.
 * Used for structured rendering without ANSI string transforms.
 */
export type StyledSegment = {
  text: string
  styles: TextStyles
  hyperlink?: string
}

/**
 * Squash text nodes into styled segments, propagating styles down through the tree.
 * This allows structured styling without relying on ANSI string transforms.
 */
export function squashTextNodesToSegments(
  node: DOMElement,
  inheritedStyles: TextStyles = {},
  inheritedHyperlink?: string,
  out: StyledSegment[] = [],
): StyledSegment[] {
  const mergedStyles = node.textStyles
    ? { ...inheritedStyles, ...node.textStyles }
    : inheritedStyles

  for (const childNode of node.childNodes) {
    if (childNode === undefined) {
      continue
    }

    if (childNode.nodeName === '#text') {
      if (childNode.nodeValue.length > 0) {
        out.push({
          text: childNode.nodeValue,
          styles: mergedStyles,
          hyperlink: inheritedHyperlink,
        })
      }
    } else if (
      childNode.nodeName === 'ink-text' ||
      childNode.nodeName === 'ink-virtual-text'
    ) {
      squashTextNodesToSegments(
        childNode,
        mergedStyles,
        inheritedHyperlink,
        out,
      )

```

---


### `src/ink/stringWidth.ts`

**信息:**
- 行数: 222
- 大小: 7156 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import emojiRegex from 'emoji-regex'
import { eastAsianWidth } from 'get-east-asian-width'
import stripAnsi from 'strip-ansi'
import { getGraphemeSegmenter } from '../utils/intl.js'

const EMOJI_REGEX = emojiRegex()

/**
 * Fallback JavaScript implementation of stringWidth when Bun.stringWidth is not available.
 *
 * Get the display width of a string as it would appear in a terminal.
 *
 * This is a more accurate alternative to the string-width package that correctly handles
 * characters like ⚠ (U+26A0) which string-width incorrectly reports as width 2.
 *
 * The implementation uses eastAsianWidth directly with ambiguousAsWide: false,
 * which correctly treats ambiguous-width characters as narrow (width 1) as
 * recommended by the Unicode standard for Western contexts.
 */
function stringWidthJavaScript(str: string): number {
  if (typeof str !== 'string' || str.length === 0) {
    return 0
  }

  // Fast path: pure ASCII string (no ANSI codes, no wide chars)
  let isPureAscii = true
  for (let i = 0; i < str.length; i++) {
    const code = str.charCodeAt(i)
    // Check for non-ASCII or ANSI escape (0x1b)
    if (code >= 127 || code === 0x1b) {
      isPureAscii = false
      break
    }
  }
  if (isPureAscii) {
    // Count printable characters (exclude control chars)
    let width = 0
    for (let i = 0; i < str.length; i++) {
      const code = str.charCodeAt(i)
      if (code > 0x1f) {
        width++
      }
    }
    return width
  }

  // Strip ANSI if escape character is present
  if (str.includes('\x1b')) {
    str = stripAnsi(str)
    if (str.length === 0) {

```

---


### `src/ink/styles.ts`

**信息:**
- 行数: 771
- 大小: 20889 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import {
  LayoutAlign,
  LayoutDisplay,
  LayoutEdge,
  LayoutFlexDirection,
  LayoutGutter,
  LayoutJustify,
  type LayoutNode,
  LayoutOverflow,
  LayoutPositionType,
  LayoutWrap,
} from './layout/node.js'
import type { BorderStyle, BorderTextOptions } from './render-border.js'

export type RGBColor = `rgb(${number},${number},${number})`
export type HexColor = `#${string}`
export type Ansi256Color = `ansi256(${number})`
export type AnsiColor =
  | 'ansi:black'
  | 'ansi:red'
  | 'ansi:green'
  | 'ansi:yellow'
  | 'ansi:blue'
  | 'ansi:magenta'
  | 'ansi:cyan'
  | 'ansi:white'
  | 'ansi:blackBright'
  | 'ansi:redBright'
  | 'ansi:greenBright'
  | 'ansi:yellowBright'
  | 'ansi:blueBright'
  | 'ansi:magentaBright'
  | 'ansi:cyanBright'
  | 'ansi:whiteBright'

/** Raw color value - not a theme key */
export type Color = RGBColor | HexColor | Ansi256Color | AnsiColor

/**
 * Structured text styling properties.
 * Used to style text without relying on ANSI string transforms.
 * Colors are raw values - theme resolution happens at the component layer.
 */
export type TextStyles = {
  readonly color?: Color
  readonly backgroundColor?: Color
  readonly dim?: boolean
  readonly bold?: boolean
  readonly italic?: boolean
  readonly underline?: boolean

```

---


### `src/ink/supports-hyperlinks.ts`

**信息:**
- 行数: 57
- 大小: 1596 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import supportsHyperlinksLib from 'supports-hyperlinks'

// Additional terminals that support OSC 8 hyperlinks but aren't detected by supports-hyperlinks.
// Checked against both TERM_PROGRAM and LC_TERMINAL (the latter is preserved inside tmux).
export const ADDITIONAL_HYPERLINK_TERMINALS = [
  'ghostty',
  'Hyper',
  'kitty',
  'alacritty',
  'iTerm.app',
  'iTerm2',
]

type EnvLike = Record<string, string | undefined>

type SupportsHyperlinksOptions = {
  env?: EnvLike
  stdoutSupported?: boolean
}

/**
 * Returns whether stdout supports OSC 8 hyperlinks.
 * Extends the supports-hyperlinks library with additional terminal detection.
 * @param options Optional overrides for testing (env, stdoutSupported)
 */
export function supportsHyperlinks(
  options?: SupportsHyperlinksOptions,
): boolean {
  const stdoutSupported =
    options?.stdoutSupported ?? supportsHyperlinksLib.stdout
  if (stdoutSupported) {
    return true
  }

  const env = options?.env ?? process.env

  // Check for additional terminals not detected by supports-hyperlinks
  const termProgram = env['TERM_PROGRAM']
  if (termProgram && ADDITIONAL_HYPERLINK_TERMINALS.includes(termProgram)) {
    return true
  }

  // LC_TERMINAL is set by some terminals (e.g. iTerm2) and preserved inside tmux,
  // where TERM_PROGRAM is overwritten to 'tmux'.
  const lcTerminal = env['LC_TERMINAL']
  if (lcTerminal && ADDITIONAL_HYPERLINK_TERMINALS.includes(lcTerminal)) {
    return true
  }

  // Kitty sets TERM=xterm-kitty

```

---


### `src/ink/tabstops.ts`

**信息:**
- 行数: 46
- 大小: 1113 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Tab expansion, inspired by Ghostty's Tabstops.zig
// Uses 8-column intervals (POSIX default, hardcoded in terminals like Ghostty)

import { stringWidth } from './stringWidth.js'
import { createTokenizer } from './termio/tokenize.js'

const DEFAULT_TAB_INTERVAL = 8

export function expandTabs(
  text: string,
  interval = DEFAULT_TAB_INTERVAL,
): string {
  if (!text.includes('\t')) {
    return text
  }

  const tokenizer = createTokenizer()
  const tokens = tokenizer.feed(text)
  tokens.push(...tokenizer.flush())

  let result = ''
  let column = 0

  for (const token of tokens) {
    if (token.type === 'sequence') {
      result += token.value
    } else {
      const parts = token.value.split(/(\t|\n)/)
      for (const part of parts) {
        if (part === '\t') {
          const spaces = interval - (column % interval)
          result += ' '.repeat(spaces)
          column += spaces
        } else if (part === '\n') {
          result += part
          column = 0
        } else {
          result += part
          column += stringWidth(part)
        }
      }
    }
  }

  return result
}

```

---


### `src/ink/terminal-focus-state.ts`

**信息:**
- 行数: 47
- 大小: 1305 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
// Terminal focus state signal — non-React access to DECSET 1004 focus events.
// 'unknown' is the default for terminals that don't support focus reporting;
// consumers treat 'unknown' identically to 'focused' (no throttling).
// Subscribers are notified synchronously when focus changes, used by
// TerminalFocusProvider to avoid polling.
export type TerminalFocusState = 'focused' | 'blurred' | 'unknown'

let focusState: TerminalFocusState = 'unknown'
const resolvers: Set<() => void> = new Set()
const subscribers: Set<() => void> = new Set()

export function setTerminalFocused(v: boolean): void {
  focusState = v ? 'focused' : 'blurred'
  // Notify useSyncExternalStore subscribers
  for (const cb of subscribers) {
    cb()
  }
  if (!v) {
    for (const resolve of resolvers) {
      resolve()
    }
    resolvers.clear()
  }
}

export function getTerminalFocused(): boolean {
  return focusState !== 'blurred'
}

export function getTerminalFocusState(): TerminalFocusState {
  return focusState
}

// For useSyncExternalStore
export function subscribeTerminalFocus(cb: () => void): () => void {
  subscribers.add(cb)
  return () => {
    subscribers.delete(cb)
  }
}

export function resetTerminalFocusState(): void {
  focusState = 'unknown'
  for (const cb of subscribers) {
    cb()
  }
}

```

---


### `src/ink/terminal-querier.ts`

**信息:**
- 行数: 212
- 大小: 7843 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Query the terminal and await responses without timeouts.
 *
 * Terminal queries (DECRQM, DA1, OSC 11, etc.) share the stdin stream
 * with keyboard input. Response sequences are syntactically
 * distinguishable from key events, so the input parser recognizes them
 * and dispatches them here.
 *
 * To avoid timeouts, each query batch is terminated by a DA1 sentinel
 * (CSI c) — every terminal since VT100 responds to DA1, and terminals
 * answer queries in order. So: if your query's response arrives before
 * DA1's, the terminal supports it; if DA1 arrives first, it doesn't.
 *
 * Usage:
 *   const [sync, grapheme] = await Promise.all([
 *     querier.send(decrqm(2026)),
 *     querier.send(decrqm(2027)),
 *     querier.flush(),
 *   ])
 *   // sync and grapheme are DECRPM responses or undefined if unsupported
 */

import type { TerminalResponse } from './parse-keypress.js'
import { csi } from './termio/csi.js'
import { osc } from './termio/osc.js'

/** A terminal query: an outbound request sequence paired with a matcher
 *  that recognizes the expected inbound response. Built by `decrqm()`,
 *  `oscColor()`, `kittyKeyboard()`, etc. */
export type TerminalQuery<T extends TerminalResponse = TerminalResponse> = {
  /** Escape sequence to write to stdout */
  request: string
  /** Recognizes the expected response in the inbound stream */
  match: (r: TerminalResponse) => r is T
}

type DecrpmResponse = Extract<TerminalResponse, { type: 'decrpm' }>
type Da1Response = Extract<TerminalResponse, { type: 'da1' }>
type Da2Response = Extract<TerminalResponse, { type: 'da2' }>
type KittyResponse = Extract<TerminalResponse, { type: 'kittyKeyboard' }>
type CursorPosResponse = Extract<TerminalResponse, { type: 'cursorPosition' }>
type OscResponse = Extract<TerminalResponse, { type: 'osc' }>
type XtversionResponse = Extract<TerminalResponse, { type: 'xtversion' }>

// -- Query builders --

/** DECRQM: request DEC private mode status (CSI ? mode $ p).
 *  Terminal replies with DECRPM (CSI ? mode ; status $ y) or ignores. */
export function decrqm(mode: number): TerminalQuery<DecrpmResponse> {
  return {

```

---


### `src/ink/terminal.ts`

**信息:**
- 行数: 248
- 大小: 8190 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { coerce } from 'semver'
import type { Writable } from 'stream'
import { env } from '../utils/env.js'
import { gte } from '../utils/semver.js'
import { getClearTerminalSequence } from './clearTerminal.js'
import type { Diff } from './frame.js'
import { cursorMove, cursorTo, eraseLines } from './termio/csi.js'
import { BSU, ESU, HIDE_CURSOR, SHOW_CURSOR } from './termio/dec.js'
import { link } from './termio/osc.js'

export type Progress = {
  state: 'running' | 'completed' | 'error' | 'indeterminate'
  percentage?: number
}

/**
 * Checks if the terminal supports OSC 9;4 progress reporting.
 * Supported terminals:
 * - ConEmu (Windows) - all versions
 * - Ghostty 1.2.0+
 * - iTerm2 3.6.6+
 *
 * Note: Windows Terminal interprets OSC 9;4 as notifications, not progress.
 */
export function isProgressReportingAvailable(): boolean {
  // Only available if we have a TTY (not piped)
  if (!process.stdout.isTTY) {
    return false
  }

  // Explicitly exclude Windows Terminal, which interprets OSC 9;4 as
  // notifications rather than progress indicators
  if (process.env.WT_SESSION) {
    return false
  }

  // ConEmu supports OSC 9;4 for progress (all versions)
  if (
    process.env.ConEmuANSI ||
    process.env.ConEmuPID ||
    process.env.ConEmuTask
  ) {
    return true
  }

  const version = coerce(process.env.TERM_PROGRAM_VERSION)
  if (!version) {
    return false
  }


```

---


### `src/ink/termio/ansi.ts`

**信息:**
- 行数: 75
- 大小: 1490 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * ANSI Control Characters and Escape Sequence Introducers
 *
 * Based on ECMA-48 / ANSI X3.64 standards.
 */

/**
 * C0 (7-bit) control characters
 */
export const C0 = {
  NUL: 0x00,
  SOH: 0x01,
  STX: 0x02,
  ETX: 0x03,
  EOT: 0x04,
  ENQ: 0x05,
  ACK: 0x06,
  BEL: 0x07,
  BS: 0x08,
  HT: 0x09,
  LF: 0x0a,
  VT: 0x0b,
  FF: 0x0c,
  CR: 0x0d,
  SO: 0x0e,
  SI: 0x0f,
  DLE: 0x10,
  DC1: 0x11,
  DC2: 0x12,
  DC3: 0x13,
  DC4: 0x14,
  NAK: 0x15,
  SYN: 0x16,
  ETB: 0x17,
  CAN: 0x18,
  EM: 0x19,
  SUB: 0x1a,
  ESC: 0x1b,
  FS: 0x1c,
  GS: 0x1d,
  RS: 0x1e,
  US: 0x1f,
  DEL: 0x7f,
} as const

// String constants for output generation
export const ESC = '\x1b'
export const BEL = '\x07'
export const SEP = ';'


```

---


### `src/ink/termio/csi.ts`

**信息:**
- 行数: 319
- 大小: 8677 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * CSI (Control Sequence Introducer) Types
 *
 * Enums and types for CSI command parameters.
 */

import { ESC, ESC_TYPE, SEP } from './ansi.js'

export const CSI_PREFIX = ESC + String.fromCharCode(ESC_TYPE.CSI)

/**
 * CSI parameter byte ranges
 */
export const CSI_RANGE = {
  PARAM_START: 0x30,
  PARAM_END: 0x3f,
  INTERMEDIATE_START: 0x20,
  INTERMEDIATE_END: 0x2f,
  FINAL_START: 0x40,
  FINAL_END: 0x7e,
} as const

/** Check if a byte is a CSI parameter byte */
export function isCSIParam(byte: number): boolean {
  return byte >= CSI_RANGE.PARAM_START && byte <= CSI_RANGE.PARAM_END
}

/** Check if a byte is a CSI intermediate byte */
export function isCSIIntermediate(byte: number): boolean {
  return (
    byte >= CSI_RANGE.INTERMEDIATE_START && byte <= CSI_RANGE.INTERMEDIATE_END
  )
}

/** Check if a byte is a CSI final byte (@ through ~) */
export function isCSIFinal(byte: number): boolean {
  return byte >= CSI_RANGE.FINAL_START && byte <= CSI_RANGE.FINAL_END
}

/**
 * Generate a CSI sequence: ESC [ p1;p2;...;pN final
 * Single arg: treated as raw body
 * Multiple args: last is final byte, rest are params joined by ;
 */
export function csi(...args: (string | number)[]): string {
  if (args.length === 0) return CSI_PREFIX
  if (args.length === 1) return `${CSI_PREFIX}${args[0]}`
  const params = args.slice(0, -1)
  const final = args[args.length - 1]
  return `${CSI_PREFIX}${params.join(SEP)}${final}`

```

---


### `src/ink/termio/dec.ts`

**信息:**
- 行数: 60
- 大小: 1935 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * DEC (Digital Equipment Corporation) Private Mode Sequences
 *
 * DEC private modes use CSI ? N h (set) and CSI ? N l (reset) format.
 * These are terminal-specific extensions to the ANSI standard.
 */

import { csi } from './csi.js'

/**
 * DEC private mode numbers
 */
export const DEC = {
  CURSOR_VISIBLE: 25,
  ALT_SCREEN: 47,
  ALT_SCREEN_CLEAR: 1049,
  MOUSE_NORMAL: 1000,
  MOUSE_BUTTON: 1002,
  MOUSE_ANY: 1003,
  MOUSE_SGR: 1006,
  FOCUS_EVENTS: 1004,
  BRACKETED_PASTE: 2004,
  SYNCHRONIZED_UPDATE: 2026,
} as const

/** Generate CSI ? N h sequence (set mode) */
export function decset(mode: number): string {
  return csi(`?${mode}h`)
}

/** Generate CSI ? N l sequence (reset mode) */
export function decreset(mode: number): string {
  return csi(`?${mode}l`)
}

// Pre-generated sequences for common modes
export const BSU = decset(DEC.SYNCHRONIZED_UPDATE)
export const ESU = decreset(DEC.SYNCHRONIZED_UPDATE)
export const EBP = decset(DEC.BRACKETED_PASTE)
export const DBP = decreset(DEC.BRACKETED_PASTE)
export const EFE = decset(DEC.FOCUS_EVENTS)
export const DFE = decreset(DEC.FOCUS_EVENTS)
export const SHOW_CURSOR = decset(DEC.CURSOR_VISIBLE)
export const HIDE_CURSOR = decreset(DEC.CURSOR_VISIBLE)
export const ENTER_ALT_SCREEN = decset(DEC.ALT_SCREEN_CLEAR)
export const EXIT_ALT_SCREEN = decreset(DEC.ALT_SCREEN_CLEAR)
// Mouse tracking: 1000 reports button press/release/wheel, 1002 adds drag
// events (button-motion), 1003 adds all-motion (no button held — for
// hover), 1006 uses SGR format (CSI < btn;col;row M/m) instead of legacy
// X10 bytes. Combined: wheel + click/drag for selection + hover.

```

---


### `src/ink/termio/esc.ts`

**信息:**
- 行数: 67
- 大小: 1444 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * ESC Sequence Parser
 *
 * Handles simple escape sequences: ESC + one or two characters
 */

import type { Action } from './types.js'

/**
 * Parse a simple ESC sequence
 *
 * @param chars - Characters after ESC (not including ESC itself)
 */
export function parseEsc(chars: string): Action | null {
  if (chars.length === 0) return null

  const first = chars[0]!

  // Full reset (RIS)
  if (first === 'c') {
    return { type: 'reset' }
  }

  // Cursor save (DECSC)
  if (first === '7') {
    return { type: 'cursor', action: { type: 'save' } }
  }

  // Cursor restore (DECRC)
  if (first === '8') {
    return { type: 'cursor', action: { type: 'restore' } }
  }

  // Index - move cursor down (IND)
  if (first === 'D') {
    return {
      type: 'cursor',
      action: { type: 'move', direction: 'down', count: 1 },
    }
  }

  // Reverse index - move cursor up (RI)
  if (first === 'M') {
    return {
      type: 'cursor',
      action: { type: 'move', direction: 'up', count: 1 },
    }
  }

  // Next line (NEL)

```

---


### `src/ink/termio/osc.ts`

**信息:**
- 行数: 493
- 大小: 16842 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * OSC (Operating System Command) Types and Parser
 */

import { Buffer } from 'buffer'
import { env } from '../../utils/env.js'
import { execFileNoThrow } from '../../utils/execFileNoThrow.js'
import { BEL, ESC, ESC_TYPE, SEP } from './ansi.js'
import type { Action, Color, TabStatusAction } from './types.js'

export const OSC_PREFIX = ESC + String.fromCharCode(ESC_TYPE.OSC)

/** String Terminator (ESC \) - alternative to BEL for terminating OSC */
export const ST = ESC + '\\'

/** Generate an OSC sequence: ESC ] p1;p2;...;pN <terminator>
 * Uses ST terminator for Kitty (avoids beeps), BEL for others */
export function osc(...parts: (string | number)[]): string {
  const terminator = env.terminal === 'kitty' ? ST : BEL
  return `${OSC_PREFIX}${parts.join(SEP)}${terminator}`
}

/**
 * Wrap an escape sequence for terminal multiplexer passthrough.
 * tmux and GNU screen intercept escape sequences; DCS passthrough
 * tunnels them to the outer terminal unmodified.
 *
 * tmux 3.3+ gates this behind `allow-passthrough` (default off). When off,
 * tmux silently drops the whole DCS — no junk, no worse than unwrapped OSC.
 * Users who want passthrough set it in their .tmux.conf; we don't mutate it.
 *
 * Do NOT wrap BEL: raw \x07 triggers tmux's bell-action (window flag);
 * wrapped \x07 is opaque DCS payload and tmux never sees the bell.
 */
export function wrapForMultiplexer(sequence: string): string {
  if (process.env['TMUX']) {
    const escaped = sequence.replaceAll('\x1b', '\x1b\x1b')
    return `\x1bPtmux;${escaped}\x1b\\`
  }
  if (process.env['STY']) {
    return `\x1bP${sequence}\x1b\\`
  }
  return sequence
}

/**
 * Which path setClipboard() will take, based on env state. Synchronous so
 * callers can show an honest toast without awaiting the copy itself.
 *
 * - 'native': pbcopy (or equivalent) will run — high-confidence system

```

---


### `src/ink/termio/parser.ts`

**信息:**
- 行数: 394
- 大小: 11546 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * ANSI Parser - Semantic Action Generator
 *
 * A streaming parser for ANSI escape sequences that produces semantic actions.
 * Uses the tokenizer for escape sequence boundary detection, then interprets
 * each sequence to produce structured actions.
 *
 * Key design decisions:
 * - Streaming: can process input incrementally
 * - Semantic output: produces structured actions, not string tokens
 * - Style tracking: maintains current text style state
 */

import { getGraphemeSegmenter } from '../../utils/intl.js'
import { C0 } from './ansi.js'
import { CSI, CURSOR_STYLES, ERASE_DISPLAY, ERASE_LINE_REGION } from './csi.js'
import { DEC } from './dec.js'
import { parseEsc } from './esc.js'
import { parseOSC } from './osc.js'
import { applySGR } from './sgr.js'
import { createTokenizer, type Token, type Tokenizer } from './tokenize.js'
import type { Action, Grapheme, TextStyle } from './types.js'
import { defaultStyle } from './types.js'

// =============================================================================
// Grapheme Utilities
// =============================================================================

function isEmoji(codePoint: number): boolean {
  return (
    (codePoint >= 0x2600 && codePoint <= 0x26ff) ||
    (codePoint >= 0x2700 && codePoint <= 0x27bf) ||
    (codePoint >= 0x1f300 && codePoint <= 0x1f9ff) ||
    (codePoint >= 0x1fa00 && codePoint <= 0x1faff) ||
    (codePoint >= 0x1f1e0 && codePoint <= 0x1f1ff)
  )
}

function isEastAsianWide(codePoint: number): boolean {
  return (
    (codePoint >= 0x1100 && codePoint <= 0x115f) ||
    (codePoint >= 0x2e80 && codePoint <= 0x9fff) ||
    (codePoint >= 0xac00 && codePoint <= 0xd7a3) ||
    (codePoint >= 0xf900 && codePoint <= 0xfaff) ||
    (codePoint >= 0xfe10 && codePoint <= 0xfe1f) ||
    (codePoint >= 0xfe30 && codePoint <= 0xfe6f) ||
    (codePoint >= 0xff00 && codePoint <= 0xff60) ||
    (codePoint >= 0xffe0 && codePoint <= 0xffe6) ||
    (codePoint >= 0x20000 && codePoint <= 0x2fffd) ||
    (codePoint >= 0x30000 && codePoint <= 0x3fffd)

```

---


### `src/ink/termio/sgr.ts`

**信息:**
- 行数: 308
- 大小: 6400 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * SGR (Select Graphic Rendition) Parser
 *
 * Parses SGR parameters and applies them to a TextStyle.
 * Handles both semicolon (;) and colon (:) separated parameters.
 */

import type { NamedColor, TextStyle, UnderlineStyle } from './types.js'
import { defaultStyle } from './types.js'

const NAMED_COLORS: NamedColor[] = [
  'black',
  'red',
  'green',
  'yellow',
  'blue',
  'magenta',
  'cyan',
  'white',
  'brightBlack',
  'brightRed',
  'brightGreen',
  'brightYellow',
  'brightBlue',
  'brightMagenta',
  'brightCyan',
  'brightWhite',
]

const UNDERLINE_STYLES: UnderlineStyle[] = [
  'none',
  'single',
  'double',
  'curly',
  'dotted',
  'dashed',
]

type Param = { value: number | null; subparams: number[]; colon: boolean }

function parseParams(str: string): Param[] {
  if (str === '') return [{ value: 0, subparams: [], colon: false }]

  const result: Param[] = []
  let current: Param = { value: null, subparams: [], colon: false }
  let num = ''
  let inSub = false

  for (let i = 0; i <= str.length; i++) {
    const c = str[i]

```

---


### `src/ink/termio/tokenize.ts`

**信息:**
- 行数: 319
- 大小: 9284 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Input Tokenizer - Escape sequence boundary detection
 *
 * Splits terminal input into tokens: text chunks and raw escape sequences.
 * Unlike the Parser which interprets sequences semantically, this just
 * identifies boundaries for use by keyboard input parsing.
 */

import { C0, ESC_TYPE, isEscFinal } from './ansi.js'
import { isCSIFinal, isCSIIntermediate, isCSIParam } from './csi.js'

export type Token =
  | { type: 'text'; value: string }
  | { type: 'sequence'; value: string }

type State =
  | 'ground'
  | 'escape'
  | 'escapeIntermediate'
  | 'csi'
  | 'ss3'
  | 'osc'
  | 'dcs'
  | 'apc'

export type Tokenizer = {
  /** Feed input and get resulting tokens */
  feed(input: string): Token[]
  /** Flush any buffered incomplete sequences */
  flush(): Token[]
  /** Reset tokenizer state */
  reset(): void
  /** Get any buffered incomplete sequence */
  buffer(): string
}

type TokenizerOptions = {
  /**
   * Treat `CSI M` as an X10 mouse event prefix and consume 3 payload bytes.
   * Only enable for stdin input — `\x1b[M` is also CSI DL (Delete Lines) in
   * output streams, and enabling this there swallows display text. Default false.
   */
  x10Mouse?: boolean
}

/**
 * Create a streaming tokenizer for terminal input.
 *
 * Usage:
 * ```typescript

```

---


### `src/ink/termio/types.ts`

**信息:**
- 行数: 236
- 大小: 7076 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * ANSI Parser - Semantic Types
 *
 * These types represent the semantic meaning of ANSI escape sequences,
 * not their string representation. Inspired by ghostty's action-based design.
 */

// =============================================================================
// Colors
// =============================================================================

/** Named colors from the 16-color palette */
export type NamedColor =
  | 'black'
  | 'red'
  | 'green'
  | 'yellow'
  | 'blue'
  | 'magenta'
  | 'cyan'
  | 'white'
  | 'brightBlack'
  | 'brightRed'
  | 'brightGreen'
  | 'brightYellow'
  | 'brightBlue'
  | 'brightMagenta'
  | 'brightCyan'
  | 'brightWhite'

/** Color specification - can be named, indexed (256), or RGB */
export type Color =
  | { type: 'named'; name: NamedColor }
  | { type: 'indexed'; index: number } // 0-255
  | { type: 'rgb'; r: number; g: number; b: number }
  | { type: 'default' }

// =============================================================================
// Text Styles
// =============================================================================

/** Underline style variants */
export type UnderlineStyle =
  | 'none'
  | 'single'
  | 'double'
  | 'curly'
  | 'dotted'
  | 'dashed'


```

---


### `src/ink/termio.ts`

**信息:**
- 行数: 42
- 大小: 1036 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * ANSI Parser Module
 *
 * A semantic ANSI escape sequence parser inspired by ghostty, tmux, and iTerm2.
 *
 * Key features:
 * - Semantic output: produces structured actions, not string tokens
 * - Streaming: can parse input incrementally via Parser class
 * - Style tracking: maintains text style state across parse calls
 * - Comprehensive: supports SGR, CSI, OSC, ESC sequences
 *
 * Usage:
 *
 * ```typescript
 * import { Parser } from './termio.js'
 *
 * const parser = new Parser()
 * const actions = parser.feed('\x1b[31mred\x1b[0m')
 * // => [{ type: 'text', graphemes: [...], style: { fg: { type: 'named', name: 'red' }, ... } }]
 * ```
 */

// Parser
export { Parser } from './termio/parser.js'
// Types
export type {
  Action,
  Color,
  CursorAction,
  CursorDirection,
  EraseAction,
  Grapheme,
  LinkAction,
  ModeAction,
  NamedColor,
  ScrollAction,
  TextSegment,
  TextStyle,
  TitleAction,
  UnderlineStyle,
} from './termio/types.js'
export { colorsEqual, defaultStyle, stylesEqual } from './termio/types.js'

```

---


### `src/ink/useTerminalNotification.ts`

**信息:**
- 行数: 126
- 大小: 3857 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { createContext, useCallback, useContext, useMemo } from 'react'
import { isProgressReportingAvailable, type Progress } from './terminal.js'
import { BEL } from './termio/ansi.js'
import { ITERM2, OSC, osc, PROGRESS, wrapForMultiplexer } from './termio/osc.js'

type WriteRaw = (data: string) => void

export const TerminalWriteContext = createContext<WriteRaw | null>(null)

export const TerminalWriteProvider = TerminalWriteContext.Provider

export type TerminalNotification = {
  notifyITerm2: (opts: { message: string; title?: string }) => void
  notifyKitty: (opts: { message: string; title: string; id: number }) => void
  notifyGhostty: (opts: { message: string; title: string }) => void
  notifyBell: () => void
  /**
   * Report progress to the terminal via OSC 9;4 sequences.
   * Supported terminals: ConEmu, Ghostty 1.2.0+, iTerm2 3.6.6+
   * Pass state=null to clear progress.
   */
  progress: (state: Progress['state'] | null, percentage?: number) => void
}

export function useTerminalNotification(): TerminalNotification {
  const writeRaw = useContext(TerminalWriteContext)
  if (!writeRaw) {
    throw new Error(
      'useTerminalNotification must be used within TerminalWriteProvider',
    )
  }

  const notifyITerm2 = useCallback(
    ({ message, title }: { message: string; title?: string }) => {
      const displayString = title ? `${title}:\n${message}` : message
      writeRaw(wrapForMultiplexer(osc(OSC.ITERM2, `\n\n${displayString}`)))
    },
    [writeRaw],
  )

  const notifyKitty = useCallback(
    ({
      message,
      title,
      id,
    }: {
      message: string
      title: string
      id: number
    }) => {

```

---


### `src/ink/warn.ts`

**信息:**
- 行数: 9
- 大小: 295 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { logForDebugging } from '../utils/debug.js'

export function ifNotInteger(value: number | undefined, name: string): void {
  if (value === undefined) return
  if (Number.isInteger(value)) return
  logForDebugging(`${name} should be an integer, got ${value}`, {
    level: 'warn',
  })
}

```

---


### `src/ink/widest-line.ts`

**信息:**
- 行数: 19
- 大小: 434 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { lineWidth } from './line-width-cache.js'

export function widestLine(string: string): number {
  let maxWidth = 0
  let start = 0

  while (start <= string.length) {
    const end = string.indexOf('\n', start)
    const line =
      end === -1 ? string.substring(start) : string.substring(start, end)

    maxWidth = Math.max(maxWidth, lineWidth(line))

    if (end === -1) break
    start = end + 1
  }

  return maxWidth
}

```

---


### `src/ink/wrap-text.ts`

**信息:**
- 行数: 74
- 大小: 1806 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import sliceAnsi from '../utils/sliceAnsi.js'
import { stringWidth } from './stringWidth.js'
import type { Styles } from './styles.js'
import { wrapAnsi } from './wrapAnsi.js'

const ELLIPSIS = '…'

// sliceAnsi may include a boundary-spanning wide char (e.g. CJK at position
// end-1 with width 2 overshoots by 1). Retry with a tighter bound once.
function sliceFit(text: string, start: number, end: number): string {
  const s = sliceAnsi(text, start, end)
  return stringWidth(s) > end - start ? sliceAnsi(text, start, end - 1) : s
}

function truncate(
  text: string,
  columns: number,
  position: 'start' | 'middle' | 'end',
): string {
  if (columns < 1) return ''
  if (columns === 1) return ELLIPSIS

  const length = stringWidth(text)
  if (length <= columns) return text

  if (position === 'start') {
    return ELLIPSIS + sliceFit(text, length - columns + 1, length)
  }
  if (position === 'middle') {
    const half = Math.floor(columns / 2)
    return (
      sliceFit(text, 0, half) +
      ELLIPSIS +
      sliceFit(text, length - (columns - half) + 1, length)
    )
  }
  return sliceFit(text, 0, columns - 1) + ELLIPSIS
}

export default function wrapText(
  text: string,
  maxWidth: number,
  wrapType: Styles['textWrap'],
): string {
  if (wrapType === 'wrap') {
    return wrapAnsi(text, maxWidth, {
      trim: false,
      hard: true,
    })
  }

```

---


### `src/ink/wrapAnsi.ts`

**信息:**
- 行数: 20
- 大小: 383 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import wrapAnsiNpm from 'wrap-ansi'

type WrapAnsiOptions = {
  hard?: boolean
  wordWrap?: boolean
  trim?: boolean
}

const wrapAnsiBun =
  typeof Bun !== 'undefined' && typeof Bun.wrapAnsi === 'function'
    ? Bun.wrapAnsi
    : null

const wrapAnsi: (
  input: string,
  columns: number,
  options?: WrapAnsiOptions,
) => string = wrapAnsiBun ?? wrapAnsiNpm

export { wrapAnsi }

```

---

