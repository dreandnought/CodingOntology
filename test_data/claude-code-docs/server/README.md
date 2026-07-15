# server 模块

## 概述

**位置:** `src/server/`

## 文件统计

- TypeScript 文件: 3
- TypeScript React 文件: 0
- 总计: 3

## 文件详情

---


### `src/server/createDirectConnectSession.ts`

**信息:**
- 行数: 88
- 大小: 2193 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/* eslint-disable eslint-plugin-n/no-unsupported-features/node-builtins */

import { errorMessage } from '../utils/errors.js'
import { jsonStringify } from '../utils/slowOperations.js'
import type { DirectConnectConfig } from './directConnectManager.js'
import { connectResponseSchema } from './types.js'

/**
 * Errors thrown by createDirectConnectSession when the connection fails.
 */
export class DirectConnectError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'DirectConnectError'
  }
}

/**
 * Create a session on a direct-connect server.
 *
 * Posts to `${serverUrl}/sessions`, validates the response, and returns
 * a DirectConnectConfig ready for use by the REPL or headless runner.
 *
 * Throws DirectConnectError on network, HTTP, or response-parsing failures.
 */
export async function createDirectConnectSession({
  serverUrl,
  authToken,
  cwd,
  dangerouslySkipPermissions,
}: {
  serverUrl: string
  authToken?: string
  cwd: string
  dangerouslySkipPermissions?: boolean
}): Promise<{
  config: DirectConnectConfig
  workDir?: string
}> {
  const headers: Record<string, string> = {
    'content-type': 'application/json',
  }
  if (authToken) {
    headers['authorization'] = `Bearer ${authToken}`
  }

  let resp: Response
  try {
    resp = await fetch(`${serverUrl}/sessions`, {
      method: 'POST',

```

---


### `src/server/directConnectManager.ts`

**信息:**
- 行数: 213
- 大小: 5898 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/* eslint-disable eslint-plugin-n/no-unsupported-features/node-builtins */

import type { SDKMessage } from '../entrypoints/agentSdkTypes.js'
import type {
  SDKControlPermissionRequest,
  StdoutMessage,
} from '../entrypoints/sdk/controlTypes.js'
import type { RemotePermissionResponse } from '../remote/RemoteSessionManager.js'
import { logForDebugging } from '../utils/debug.js'
import { jsonParse, jsonStringify } from '../utils/slowOperations.js'
import type { RemoteMessageContent } from '../utils/teleport/api.js'

export type DirectConnectConfig = {
  serverUrl: string
  sessionId: string
  wsUrl: string
  authToken?: string
}

export type DirectConnectCallbacks = {
  onMessage: (message: SDKMessage) => void
  onPermissionRequest: (
    request: SDKControlPermissionRequest,
    requestId: string,
  ) => void
  onConnected?: () => void
  onDisconnected?: () => void
  onError?: (error: Error) => void
}

function isStdoutMessage(value: unknown): value is StdoutMessage {
  return (
    typeof value === 'object' &&
    value !== null &&
    'type' in value &&
    typeof value.type === 'string'
  )
}

export class DirectConnectSessionManager {
  private ws: WebSocket | null = null
  private config: DirectConnectConfig
  private callbacks: DirectConnectCallbacks

  constructor(config: DirectConnectConfig, callbacks: DirectConnectCallbacks) {
    this.config = config
    this.callbacks = callbacks
  }

  connect(): void {

```

---


### `src/server/types.ts`

**信息:**
- 行数: 57
- 大小: 1466 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { ChildProcess } from 'child_process'
import { z } from 'zod/v4'
import { lazySchema } from '../utils/lazySchema.js'

export const connectResponseSchema = lazySchema(() =>
  z.object({
    session_id: z.string(),
    ws_url: z.string(),
    work_dir: z.string().optional(),
  }),
)

export type ServerConfig = {
  port: number
  host: string
  authToken: string
  unix?: string
  /** Idle timeout for detached sessions (ms). 0 = never expire. */
  idleTimeoutMs?: number
  /** Maximum number of concurrent sessions. */
  maxSessions?: number
  /** Default workspace directory for sessions that don't specify cwd. */
  workspace?: string
}

export type SessionState =
  | 'starting'
  | 'running'
  | 'detached'
  | 'stopping'
  | 'stopped'

export type SessionInfo = {
  id: string
  status: SessionState
  createdAt: number
  workDir: string
  process: ChildProcess | null
  sessionKey?: string
}

/**
 * Stable session key → session metadata. Persisted to ~/.claude/server-sessions.json
 * so sessions can be resumed across server restarts.
 */
export type SessionIndexEntry = {
  /** Server-assigned session ID (matches the subprocess's claude session). */
  sessionId: string
  /** The claude transcript session ID for --resume. Same as sessionId for direct sessions. */
  transcriptSessionId: string

```

---

