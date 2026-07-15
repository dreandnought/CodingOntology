# proactive 模块

## 概述

**位置:** `src/proactive/`

## 文件统计

- TypeScript 文件: 2
- TypeScript React 文件: 0
- 总计: 2

## 文件详情

---


### `src/proactive/index.ts`

**信息:**
- 行数: 57
- 大小: 1066 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
let active = false
let paused = false
let contextBlocked = false
let nextTickAt: number | null = null

const listeners = new Set<() => void>()

function emit(): void {
  for (const listener of listeners) listener()
}

export function subscribeToProactiveChanges(listener: () => void): () => void {
  listeners.add(listener)
  return () => listeners.delete(listener)
}

export function isProactiveActive(): boolean {
  return active
}

export function isProactivePaused(): boolean {
  return paused
}

export function activateProactive(_source?: string): void {
  active = true
  paused = false
  nextTickAt = null
  emit()
}

export function deactivateProactive(): void {
  active = false
  paused = false
  nextTickAt = null
  emit()
}

export function pauseProactive(): void {
  paused = true
  emit()
}

export function resumeProactive(): void {
  paused = false
  emit()
}

export function setContextBlocked(value: boolean): void {
  contextBlocked = value

```

---


### `src/proactive/useProactive.ts`

**信息:**
- 行数: 6
- 大小: 88 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export function useProactive() {
  return {
    active: false,
    paused: false,
  }
}

```

---

