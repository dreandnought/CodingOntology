# context 模块

## 概述

**位置:** `src/context/`

## 文件统计

- TypeScript 文件: 0
- TypeScript React 文件: 9
- 总计: 9

## 文件详情

---


### `src/context/QueuedMessageContext.tsx`

**信息:**
- 行数: 63
- 大小: 5598 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import * as React from 'react';
import { Box } from '../ink.js';
type QueuedMessageContextValue = {
  isQueued: boolean;
  isFirst: boolean;
  /** Width reduction for container padding (e.g., 4 for paddingX={2}) */
  paddingWidth: number;
};
const QueuedMessageContext = React.createContext<QueuedMessageContextValue | undefined>(undefined);
export function useQueuedMessage() {
  return React.useContext(QueuedMessageContext);
}
const PADDING_X = 2;
type Props = {
  isFirst: boolean;
  useBriefLayout?: boolean;
  children: React.ReactNode;
};
export function QueuedMessageProvider(t0) {
  const $ = _c(9);
  const {
    isFirst,
    useBriefLayout,
    children
  } = t0;
  const padding = useBriefLayout ? 0 : PADDING_X;
  const t1 = padding * 2;
  let t2;
  if ($[0] !== isFirst || $[1] !== t1) {
    t2 = {
      isQueued: true,
      isFirst,
      paddingWidth: t1
    };
    $[0] = isFirst;
    $[1] = t1;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  const value = t2;
  let t3;
  if ($[3] !== children || $[4] !== padding) {
    t3 = <Box paddingX={padding}>{children}</Box>;
    $[3] = children;
    $[4] = padding;
    $[5] = t3;
  } else {
    t3 = $[5];

```

---


### `src/context/fpsMetrics.tsx`

**信息:**
- 行数: 30
- 大小: 3158 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, useContext } from 'react';
import type { FpsMetrics } from '../utils/fpsTracker.js';
type FpsMetricsGetter = () => FpsMetrics | undefined;
const FpsMetricsContext = createContext<FpsMetricsGetter | undefined>(undefined);
type Props = {
  getFpsMetrics: FpsMetricsGetter;
  children: React.ReactNode;
};
export function FpsMetricsProvider(t0) {
  const $ = _c(3);
  const {
    getFpsMetrics,
    children
  } = t0;
  let t1;
  if ($[0] !== children || $[1] !== getFpsMetrics) {
    t1 = <FpsMetricsContext.Provider value={getFpsMetrics}>{children}</FpsMetricsContext.Provider>;
    $[0] = children;
    $[1] = getFpsMetrics;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  return t1;
}
export function useFpsMetrics() {
  return useContext(FpsMetricsContext);
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsImNyZWF0ZUNvbnRleHQiLCJ1c2VDb250ZXh0IiwiRnBzTWV0cmljcyIsIkZwc01ldHJpY3NHZXR0ZXIiLCJGcHNNZXRyaWNzQ29udGV4dCIsInVuZGVmaW5lZCIsIlByb3BzIiwiZ2V0RnBzTWV0cmljcyIsImNoaWxkcmVuIiwiUmVhY3ROb2RlIiwiRnBzTWV0cmljc1Byb3ZpZGVyIiwidDAiLCIkIiwiX2MiLCJ0MSIsInVzZUZwc01ldHJpY3MiXSwic291cmNlcyI6WyJmcHNNZXRyaWNzLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QsIHsgY3JlYXRlQ29udGV4dCwgdXNlQ29udGV4dCB9IGZyb20gJ3JlYWN0J1xuaW1wb3J0IHR5cGUgeyBGcHNNZXRyaWNzIH0gZnJvbSAnLi4vdXRpbHMvZnBzVHJhY2tlci5qcydcblxudHlwZSBGcHNNZXRyaWNzR2V0dGVyID0gKCkgPT4gRnBzTWV0cmljcyB8IHVuZGVmaW5lZFxuXG5jb25zdCBGcHNNZXRyaWNzQ29udGV4dCA9IGNyZWF0ZUNvbnRleHQ8RnBzTWV0cmljc0dldHRlciB8IHVuZGVmaW5lZD4odW5kZWZpbmVkKVxuXG50eXBlIFByb3BzID0ge1xuICBnZXRGcHNNZXRyaWNzOiBGcHNNZXRyaWNzR2V0dGVyXG4gIGNoaWxkcmVuOiBSZWFjdC5SZWFjdE5vZGVcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIEZwc01ldHJpY3NQcm92aWRlcih7XG4gIGdldEZwc01ldHJpY3MsXG4gIGNoaWxkcmVuLFxufTogUHJvcHMpOiBSZWFjdC5SZWFjdE5vZGUge1xuICByZXR1cm4gKFxuICAgIDxGcHNNZXRyaWNzQ29udGV4dC5Qcm92aWRlciB2YWx1ZT17Z2V0RnBzTWV0cmljc30+XG4gICAgICB7Y2hpbGRyZW59XG4gICAgPC9GcHNNZXRyaWNzQ29udGV4dC5Qcm92aWRlcj5cbiAgKVxufVxuXG5leHBvcnQgZnVuY3Rpb24gdXNlRnBzTWV0cmljcygpOiBGcHNNZXRyaWNzR2V0dGVyIHwgdW5kZWZpbmVkIHtcbiAgcmV0dXJuIHVzZUNvbnRleHQoRnBzTWV0cmljc0NvbnRleHQpXG59XG4iXSwibWFwcGluZ3MiOiI7QUFBQSxPQUFPQSxLQUFLLElBQUlDLGFBQWEsRUFBRUMsVUFBVSxRQUFRLE9BQU87QUFDeEQsY0FBY0MsVUFBVSxRQUFRLHdCQUF3QjtBQUV4RCxLQUFLQyxnQkFBZ0IsR0FBRyxHQUFHLEdBQUdELFVBQVUsR0FBRyxTQUFTO0FBRXBELE1BQU1FLGlCQUFpQixHQUFHSixhQUFhLENBQUNHLGdCQUFnQixHQUFHLFNBQVMsQ0FBQyxDQUFDRSxTQUFTLENBQUM7QUFFaEYsS0FBS0MsS0FBSyxHQUFHO0VBQ1hDLGFBQWEsRUFBRUosZ0JBQWdCO0VBQy9CSyxRQUFRLEVBQUVULEtBQUssQ0FBQ1UsU0FBUztBQUMzQixDQUFDO0FBRUQsT0FBTyxTQUFBQyxtQkFBQUMsRUFBQTtFQUFBLE1BQUFDLENBQUEsR0FBQUMsRUFBQTtFQUE0QjtJQUFBTixhQUFBO0lBQUFDO0VBQUEsSUFBQUcsRUFHM0I7RUFBQSxJQUFBRyxFQUFBO0VBQUEsSUFBQUYsQ0FBQSxRQUFBSixRQUFBLElBQUFJLENBQUEsUUFBQUwsYUFBQTtJQUVKTyxFQUFBLCtCQUFtQ1AsS0FBYSxDQUFiQSxjQUFZLENBQUMsQ0FDN0NDLFNBQU8sQ0FDViw2QkFBNkI7SUFBQUksQ0FBQSxNQUFBSixRQUFBO0lBQUFJLENBQUEsTUFBQUwsYUFBQTtJQUFBSyxDQUFBLE1BQUFFLEVBQUE7RUFBQTtJQUFBQSxFQUFBLEdBQUFGLENBQUE7RUFBQTtFQUFBLE9BRjdCRSxFQUU2QjtBQUFBO0FBSWpDLE9BQU8sU0FBQUMsY0FBQTtFQUFBLE9BQ0VkLFVBQVUsQ0FBQ0csaUJBQWlCLENBQUM7QUFBQSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/context/mailbox.tsx`

**信息:**
- 行数: 38
- 大小: 3436 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, useContext, useMemo } from 'react';
import { Mailbox } from '../utils/mailbox.js';
const MailboxContext = createContext<Mailbox | undefined>(undefined);
type Props = {
  children: React.ReactNode;
};
export function MailboxProvider(t0) {
  const $ = _c(3);
  const {
    children
  } = t0;
  let t1;
  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {
    t1 = new Mailbox();
    $[0] = t1;
  } else {
    t1 = $[0];
  }
  const mailbox = t1;
  let t2;
  if ($[1] !== children) {
    t2 = <MailboxContext.Provider value={mailbox}>{children}</MailboxContext.Provider>;
    $[1] = children;
    $[2] = t2;
  } else {
    t2 = $[2];
  }
  return t2;
}
export function useMailbox() {
  const mailbox = useContext(MailboxContext);
  if (!mailbox) {
    throw new Error("useMailbox must be used within a MailboxProvider");
  }
  return mailbox;
}
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJuYW1lcyI6WyJSZWFjdCIsImNyZWF0ZUNvbnRleHQiLCJ1c2VDb250ZXh0IiwidXNlTWVtbyIsIk1haWxib3giLCJNYWlsYm94Q29udGV4dCIsInVuZGVmaW5lZCIsIlByb3BzIiwiY2hpbGRyZW4iLCJSZWFjdE5vZGUiLCJNYWlsYm94UHJvdmlkZXIiLCJ0MCIsIiQiLCJfYyIsInQxIiwiU3ltYm9sIiwiZm9yIiwibWFpbGJveCIsInQyIiwidXNlTWFpbGJveCIsIkVycm9yIl0sInNvdXJjZXMiOlsibWFpbGJveC50c3giXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0LCB7IGNyZWF0ZUNvbnRleHQsIHVzZUNvbnRleHQsIHVzZU1lbW8gfSBmcm9tICdyZWFjdCdcbmltcG9ydCB7IE1haWxib3ggfSBmcm9tICcuLi91dGlscy9tYWlsYm94LmpzJ1xuXG5jb25zdCBNYWlsYm94Q29udGV4dCA9IGNyZWF0ZUNvbnRleHQ8TWFpbGJveCB8IHVuZGVmaW5lZD4odW5kZWZpbmVkKVxuXG50eXBlIFByb3BzID0ge1xuICBjaGlsZHJlbjogUmVhY3QuUmVhY3ROb2RlXG59XG5cbmV4cG9ydCBmdW5jdGlvbiBNYWlsYm94UHJvdmlkZXIoeyBjaGlsZHJlbiB9OiBQcm9wcyk6IFJlYWN0LlJlYWN0Tm9kZSB7XG4gIGNvbnN0IG1haWxib3ggPSB1c2VNZW1vKCgpID0+IG5ldyBNYWlsYm94KCksIFtdKVxuICByZXR1cm4gKFxuICAgIDxNYWlsYm94Q29udGV4dC5Qcm92aWRlciB2YWx1ZT17bWFpbGJveH0+XG4gICAgICB7Y2hpbGRyZW59XG4gICAgPC9NYWlsYm94Q29udGV4dC5Qcm92aWRlcj5cbiAgKVxufVxuXG5leHBvcnQgZnVuY3Rpb24gdXNlTWFpbGJveCgpOiBNYWlsYm94IHtcbiAgY29uc3QgbWFpbGJveCA9IHVzZUNvbnRleHQoTWFpbGJveENvbnRleHQpXG4gIGlmICghbWFpbGJveCkge1xuICAgIHRocm93IG5ldyBFcnJvcigndXNlTWFpbGJveCBtdXN0IGJlIHVzZWQgd2l0aGluIGEgTWFpbGJveFByb3ZpZGVyJylcbiAgfVxuICByZXR1cm4gbWFpbGJveFxufVxuIl0sIm1hcHBpbmdzIjoiO0FBQUEsT0FBT0EsS0FBSyxJQUFJQyxhQUFhLEVBQUVDLFVBQVUsRUFBRUMsT0FBTyxRQUFRLE9BQU87QUFDakUsU0FBU0MsT0FBTyxRQUFRLHFCQUFxQjtBQUU3QyxNQUFNQyxjQUFjLEdBQUdKLGFBQWEsQ0FBQ0csT0FBTyxHQUFHLFNBQVMsQ0FBQyxDQUFDRSxTQUFTLENBQUM7QUFFcEUsS0FBS0MsS0FBSyxHQUFHO0VBQ1hDLFFBQVEsRUFBRVIsS0FBSyxDQUFDUyxTQUFTO0FBQzNCLENBQUM7QUFFRCxPQUFPLFNBQUFDLGdCQUFBQyxFQUFBO0VBQUEsTUFBQUMsQ0FBQSxHQUFBQyxFQUFBO0VBQXlCO0lBQUFMO0VBQUEsSUFBQUcsRUFBbUI7RUFBQSxJQUFBRyxFQUFBO0VBQUEsSUFBQUYsQ0FBQSxRQUFBRyxNQUFBLENBQUFDLEdBQUE7SUFDbkJGLEVBQUEsT0FBSVYsT0FBTyxDQUFDLENBQUM7SUFBQVEsQ0FBQSxNQUFBRSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBRixDQUFBO0VBQUE7RUFBM0MsTUFBQUssT0FBQSxHQUE4QkgsRUFBYTtFQUFLLElBQUFJLEVBQUE7RUFBQSxJQUFBTixDQUFBLFFBQUFKLFFBQUE7SUFFOUNVLEVBQUEsNEJBQWdDRCxLQUFPLENBQVBBLFFBQU0sQ0FBQyxDQUNwQ1QsU0FBTyxDQUNWLDBCQUEwQjtJQUFBSSxDQUFBLE1BQUFKLFFBQUE7SUFBQUksQ0FBQSxNQUFBTSxFQUFBO0VBQUE7SUFBQUEsRUFBQSxHQUFBTixDQUFBO0VBQUE7RUFBQSxPQUYxQk0sRUFFMEI7QUFBQTtBQUk5QixPQUFPLFNBQUFDLFdBQUE7RUFDTCxNQUFBRixPQUFBLEdBQWdCZixVQUFVLENBQUNHLGNBQWMsQ0FBQztFQUMxQyxJQUFJLENBQUNZLE9BQU87SUFDVixNQUFNLElBQUlHLEtBQUssQ0FBQyxrREFBa0QsQ0FBQztFQUFBO0VBQ3BFLE9BQ01ILE9BQU87QUFBQSIsImlnbm9yZUxpc3QiOltdfQ==
```

---


### `src/context/modalContext.tsx`

**信息:**
- 行数: 58
- 大小: 6266 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import { createContext, type RefObject, useContext } from 'react';
import type { ScrollBoxHandle } from '../ink/components/ScrollBox.js';

/**
 * Set by FullscreenLayout when rendering content in its `modal` slot —
 * the absolute-positioned bottom-anchored pane for slash-command dialogs.
 * Consumers use this to:
 *
 * - Suppress top-level framing — `Pane` skips its full-terminal-width
 *   `Divider` (FullscreenLayout already draws the ▔ divider).
 * - Size Select pagination to the available rows — the modal's inner
 *   area is smaller than the terminal (rows minus transcript peek minus
 *   divider), so components that cap their visible option count from
 *   `useTerminalSize().rows` would overflow without this context.
 * - Reset scroll on tab switch — Tabs keys its ScrollBox by
 *   `selectedTabIndex`, remounting on tab switch so scrollTop resets to 0
 *   without scrollTo() timing games.
 *
 * null = not inside the modal slot.
 */
type ModalCtx = {
  rows: number;
  columns: number;
  scrollRef: RefObject<ScrollBoxHandle | null> | null;
};
export const ModalContext = createContext<ModalCtx | null>(null);
export function useIsInsideModal() {
  return useContext(ModalContext) !== null;
}

/**
 * Available content rows/columns when inside a Modal, else falls back to
 * the provided terminal size. Use instead of `useTerminalSize()` when a
 * component caps its visible content height — the modal's inner area is
 * smaller than the terminal.
 */
export function useModalOrTerminalSize(fallback) {
  const $ = _c(3);
  const ctx = useContext(ModalContext);
  let t0;
  if ($[0] !== ctx || $[1] !== fallback) {
    t0 = ctx ? {
      rows: ctx.rows,
      columns: ctx.columns
    } : fallback;
    $[0] = ctx;
    $[1] = fallback;
    $[2] = t0;
  } else {

```

---


### `src/context/notifications.tsx`

**信息:**
- 行数: 240
- 大小: 33050 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import type * as React from 'react';
import { useCallback, useEffect } from 'react';
import { useAppStateStore, useSetAppState } from 'src/state/AppState.js';
import type { Theme } from '../utils/theme.js';
type Priority = 'low' | 'medium' | 'high' | 'immediate';
type BaseNotification = {
  key: string;
  /**
   * Keys of notifications that this notification invalidates.
   * If a notification is invalidated, it will be removed from the queue
   * and, if currently displayed, cleared immediately.
   */
  invalidates?: string[];
  priority: Priority;
  timeoutMs?: number;
  /**
   * Combine notifications with the same key, like Array.reduce().
   * Called as fold(accumulator, incoming) when a notification with a matching
   * key already exists in the queue or is currently displayed.
   * Returns the merged notification (should carry fold forward for future merges).
   */
  fold?: (accumulator: Notification, incoming: Notification) => Notification;
};
type TextNotification = BaseNotification & {
  text: string;
  color?: keyof Theme;
};
type JSXNotification = BaseNotification & {
  jsx: React.ReactNode;
};
type AddNotificationFn = (content: Notification) => void;
type RemoveNotificationFn = (key: string) => void;
export type Notification = TextNotification | JSXNotification;
const DEFAULT_TIMEOUT_MS = 8000;

// Track current timeout to clear it when immediate notifications arrive
let currentTimeoutId: NodeJS.Timeout | null = null;
export function useNotifications(): {
  addNotification: AddNotificationFn;
  removeNotification: RemoveNotificationFn;
} {
  const store = useAppStateStore();
  const setAppState = useSetAppState();

  // Process queue when current notification finishes or queue changes
  const processQueue = useCallback(() => {
    setAppState(prev => {
      const next = getNext(prev.notifications.queue);
      if (prev.notifications.current !== null || !next) {
        return prev;

```

---


### `src/context/overlayContext.tsx`

**信息:**
- 行数: 151
- 大小: 14123 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * Overlay tracking for Escape key coordination.
 *
 * This solves the problem of escape key handling when overlays (like Select with onCancel)
 * are open. The CancelRequestHandler needs to know when an overlay is active so it doesn't
 * cancel requests when the user just wants to dismiss the overlay.
 *
 * Usage:
 * 1. Call useRegisterOverlay() in any overlay component to automatically register it
 * 2. Call useIsOverlayActive() to check if any overlay is currently active
 *
 * The hook automatically registers on mount and unregisters on unmount,
 * so no manual cleanup or state management is needed.
 */
import { useContext, useEffect, useLayoutEffect } from 'react';
import instances from '../ink/instances.js';
import { AppStoreContext, useAppState } from '../state/AppState.js';

// Non-modal overlays that shouldn't disable TextInput focus
const NON_MODAL_OVERLAYS = new Set(['autocomplete']);

/**
 * Hook to register a component as an active overlay.
 * Automatically registers on mount and unregisters on unmount.
 *
 * @param id - Unique identifier for this overlay (e.g., 'select', 'multi-select')
 * @param enabled - Whether to register (default: true). Use this to conditionally register
 *                  based on component props, e.g., only register when onCancel is provided.
 *
 * @example
 * // Conditional registration based on whether cancel is supported
 * function useSelectInput({ state }) {
 *   useRegisterOverlay('select', !!state.onCancel)
 *   // ...
 * }
 */
export function useRegisterOverlay(id, t0) {
  const $ = _c(8);
  const enabled = t0 === undefined ? true : t0;
  const store = useContext(AppStoreContext);
  const setAppState = store?.setState;
  let t1;
  let t2;
  if ($[0] !== enabled || $[1] !== id || $[2] !== setAppState) {
    t1 = () => {
      if (!enabled || !setAppState) {
        return;
      }
      setAppState(prev => {

```

---


### `src/context/promptOverlayContext.tsx`

**信息:**
- 行数: 125
- 大小: 12138 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
/**
 * Portal for content that floats above the prompt so it escapes
 * FullscreenLayout's bottom-slot `overflowY:hidden` clip.
 *
 * The clip is load-bearing (CC-668: tall pastes squash the ScrollBox
 * without it), but floating overlays use `position:absolute
 * bottom="100%"` to float above the prompt — and Ink's clip stack
 * intersects ALL descendants, so they were clipped to ~1 row.
 *
 * Two channels:
 * - `useSetPromptOverlay` — slash-command suggestion data (structured,
 *   written by PromptInputFooter)
 * - `useSetPromptOverlayDialog` — arbitrary dialog node (e.g.
 *   AutoModeOptInDialog, written by PromptInput)
 *
 * FullscreenLayout reads both and renders them outside the clipped slot.
 *
 * Split into data/setter context pairs so writers never re-render on
 * their own writes — the setter contexts are stable.
 */
import React, { createContext, type ReactNode, useContext, useEffect, useState } from 'react';
import type { SuggestionItem } from '../components/PromptInput/PromptInputFooterSuggestions.js';
export type PromptOverlayData = {
  suggestions: SuggestionItem[];
  selectedSuggestion: number;
  maxColumnWidth?: number;
};
type Setter<T> = (d: T | null) => void;
const DataContext = createContext<PromptOverlayData | null>(null);
const SetContext = createContext<Setter<PromptOverlayData> | null>(null);
const DialogContext = createContext<ReactNode>(null);
const SetDialogContext = createContext<Setter<ReactNode> | null>(null);
export function PromptOverlayProvider(t0) {
  const $ = _c(6);
  const {
    children
  } = t0;
  const [data, setData] = useState(null);
  const [dialog, setDialog] = useState(null);
  let t1;
  if ($[0] !== children || $[1] !== dialog) {
    t1 = <DialogContext.Provider value={dialog}>{children}</DialogContext.Provider>;
    $[0] = children;
    $[1] = dialog;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  let t2;

```

---


### `src/context/stats.tsx`

**信息:**
- 行数: 220
- 大小: 22006 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, useCallback, useContext, useEffect, useMemo } from 'react';
import { saveCurrentProjectConfig } from '../utils/config.js';
export type StatsStore = {
  increment(name: string, value?: number): void;
  set(name: string, value: number): void;
  observe(name: string, value: number): void;
  add(name: string, value: string): void;
  getAll(): Record<string, number>;
};
function percentile(sorted: number[], p: number): number {
  const index = p / 100 * (sorted.length - 1);
  const lower = Math.floor(index);
  const upper = Math.ceil(index);
  if (lower === upper) {
    return sorted[lower]!;
  }
  return sorted[lower]! + (sorted[upper]! - sorted[lower]!) * (index - lower);
}
const RESERVOIR_SIZE = 1024;
type Histogram = {
  reservoir: number[];
  count: number;
  sum: number;
  min: number;
  max: number;
};
export function createStatsStore(): StatsStore {
  const metrics = new Map<string, number>();
  const histograms = new Map<string, Histogram>();
  const sets = new Map<string, Set<string>>();
  return {
    increment(name: string, value = 1) {
      metrics.set(name, (metrics.get(name) ?? 0) + value);
    },
    set(name: string, value: number) {
      metrics.set(name, value);
    },
    observe(name: string, value: number) {
      let h = histograms.get(name);
      if (!h) {
        h = {
          reservoir: [],
          count: 0,
          sum: 0,
          min: value,
          max: value
        };
        histograms.set(name, h);
      }

```

---


### `src/context/voice.tsx`

**信息:**
- 行数: 88
- 大小: 8784 bytes
- 类型: React Component

**文件内容预览 (前50行):**

```typescript
import { c as _c } from "react/compiler-runtime";
import React, { createContext, useContext, useState, useSyncExternalStore } from 'react';
import { createStore, type Store } from '../state/store.js';
export type VoiceState = {
  voiceState: 'idle' | 'recording' | 'processing';
  voiceError: string | null;
  voiceInterimTranscript: string;
  voiceAudioLevels: number[];
  voiceWarmingUp: boolean;
};
const DEFAULT_STATE: VoiceState = {
  voiceState: 'idle',
  voiceError: null,
  voiceInterimTranscript: '',
  voiceAudioLevels: [],
  voiceWarmingUp: false
};
type VoiceStore = Store<VoiceState>;
const VoiceContext = createContext<VoiceStore | null>(null);
type Props = {
  children: React.ReactNode;
};
export function VoiceProvider(t0) {
  const $ = _c(3);
  const {
    children
  } = t0;
  const [store] = useState(_temp);
  let t1;
  if ($[0] !== children || $[1] !== store) {
    t1 = <VoiceContext.Provider value={store}>{children}</VoiceContext.Provider>;
    $[0] = children;
    $[1] = store;
    $[2] = t1;
  } else {
    t1 = $[2];
  }
  return t1;
}
function _temp() {
  return createStore(DEFAULT_STATE);
}
function useVoiceStore() {
  const store = useContext(VoiceContext);
  if (!store) {
    throw new Error("useVoiceState must be used within a VoiceProvider");
  }
  return store;
}


```

---

