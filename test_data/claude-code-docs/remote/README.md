# remote 模块

## 概述

**位置:** `src/remote/`

## 文件统计

- TypeScript 文件: 4
- TypeScript React 文件: 0
- 总计: 4

## 文件详情

---


### `src/remote/RemoteSessionManager.ts`

**信息:**
- 行数: 343
- 大小: 9320 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type { SDKMessage } from '../entrypoints/agentSdkTypes.js'
import type {
  SDKControlCancelRequest,
  SDKControlPermissionRequest,
  SDKControlRequest,
  SDKControlResponse,
} from '../entrypoints/sdk/controlTypes.js'
import { logForDebugging } from '../utils/debug.js'
import { logError } from '../utils/log.js'
import {
  type RemoteMessageContent,
  sendEventToRemoteSession,
} from '../utils/teleport/api.js'
import {
  SessionsWebSocket,
  type SessionsWebSocketCallbacks,
} from './SessionsWebSocket.js'

/**
 * Type guard to check if a message is an SDKMessage (not a control message)
 */
function isSDKMessage(
  message:
    | SDKMessage
    | SDKControlRequest
    | SDKControlResponse
    | SDKControlCancelRequest,
): message is SDKMessage {
  return (
    message.type !== 'control_request' &&
    message.type !== 'control_response' &&
    message.type !== 'control_cancel_request'
  )
}

/**
 * Simple permission response for remote sessions.
 * This is a simplified version of PermissionResult for CCR communication.
 */
export type RemotePermissionResponse =
  | {
      behavior: 'allow'
      updatedInput: Record<string, unknown>
    }
  | {
      behavior: 'deny'
      message: string
    }

export type RemoteSessionConfig = {

```

---


### `src/remote/SessionsWebSocket.ts`

**信息:**
- 行数: 404
- 大小: 12505 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { randomUUID } from 'crypto'
import { getOauthConfig } from '../constants/oauth.js'
import type { SDKMessage } from '../entrypoints/agentSdkTypes.js'
import type {
  SDKControlCancelRequest,
  SDKControlRequest,
  SDKControlRequestInner,
  SDKControlResponse,
} from '../entrypoints/sdk/controlTypes.js'
import { logForDebugging } from '../utils/debug.js'
import { errorMessage } from '../utils/errors.js'
import { logError } from '../utils/log.js'
import { getWebSocketTLSOptions } from '../utils/mtls.js'
import { getWebSocketProxyAgent, getWebSocketProxyUrl } from '../utils/proxy.js'
import { jsonParse, jsonStringify } from '../utils/slowOperations.js'

const RECONNECT_DELAY_MS = 2000
const MAX_RECONNECT_ATTEMPTS = 5
const PING_INTERVAL_MS = 30000

/**
 * Maximum retries for 4001 (session not found). During compaction the
 * server may briefly consider the session stale; a short retry window
 * lets the client recover without giving up permanently.
 */
const MAX_SESSION_NOT_FOUND_RETRIES = 3

/**
 * WebSocket close codes that indicate a permanent server-side rejection.
 * The client stops reconnecting immediately.
 * Note: 4001 (session not found) is handled separately with limited
 * retries since it can be transient during compaction.
 */
const PERMANENT_CLOSE_CODES = new Set([
  4003, // unauthorized
])

type WebSocketState = 'connecting' | 'connected' | 'closed'

type SessionsMessage =
  | SDKMessage
  | SDKControlRequest
  | SDKControlResponse
  | SDKControlCancelRequest

function isSessionsMessage(value: unknown): value is SessionsMessage {
  if (typeof value !== 'object' || value === null || !('type' in value)) {
    return false
  }
  // Accept any message with a string `type` field. Downstream handlers

```

---


### `src/remote/remotePermissionBridge.ts`

**信息:**
- 行数: 78
- 大小: 2378 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { randomUUID } from 'crypto'
import type { SDKControlPermissionRequest } from '../entrypoints/sdk/controlTypes.js'
import type { Tool } from '../Tool.js'
import type { AssistantMessage } from '../types/message.js'
import { jsonStringify } from '../utils/slowOperations.js'

/**
 * Create a synthetic AssistantMessage for remote permission requests.
 * The ToolUseConfirm type requires an AssistantMessage, but in remote mode
 * we don't have a real one — the tool use runs on the CCR container.
 */
export function createSyntheticAssistantMessage(
  request: SDKControlPermissionRequest,
  requestId: string,
): AssistantMessage {
  return {
    type: 'assistant',
    uuid: randomUUID(),
    message: {
      id: `remote-${requestId}`,
      type: 'message',
      role: 'assistant',
      content: [
        {
          type: 'tool_use',
          id: request.tool_use_id,
          name: request.tool_name,
          input: request.input,
        },
      ],
      model: '',
      stop_reason: null,
      stop_sequence: null,
      container: null,
      context_management: null,
      usage: {
        input_tokens: 0,
        output_tokens: 0,
        cache_creation_input_tokens: 0,
        cache_read_input_tokens: 0,
      },
    } as AssistantMessage['message'],
    requestId: undefined,
    timestamp: new Date().toISOString(),
  }
}

/**
 * Create a minimal Tool stub for tools that aren't loaded locally.
 * This happens when the remote CCR has tools (e.g., MCP tools) that the

```

---


### `src/remote/sdkMessageAdapter.ts`

**信息:**
- 行数: 302
- 大小: 9060 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import type {
  SDKAssistantMessage,
  SDKCompactBoundaryMessage,
  SDKMessage,
  SDKPartialAssistantMessage,
  SDKResultMessage,
  SDKStatusMessage,
  SDKSystemMessage,
  SDKToolProgressMessage,
} from '../entrypoints/agentSdkTypes.js'
import type {
  AssistantMessage,
  Message,
  StreamEvent,
  SystemMessage,
} from '../types/message.js'
import { logForDebugging } from '../utils/debug.js'
import { fromSDKCompactMetadata } from '../utils/messages/mappers.js'
import { createUserMessage } from '../utils/messages.js'

/**
 * Converts SDKMessage from CCR to REPL Message types.
 *
 * The CCR backend sends SDK-format messages via WebSocket. The REPL expects
 * internal Message types for rendering. This adapter bridges the two.
 */

/**
 * Convert an SDKAssistantMessage to an AssistantMessage
 */
function convertAssistantMessage(msg: SDKAssistantMessage): AssistantMessage {
  return {
    type: 'assistant',
    message: msg.message,
    uuid: msg.uuid,
    requestId: undefined,
    timestamp: new Date().toISOString(),
    error: msg.error,
  }
}

/**
 * Convert an SDKPartialAssistantMessage (streaming) to a StreamEvent
 */
function convertStreamEvent(msg: SDKPartialAssistantMessage): StreamEvent {
  return {
    type: 'stream_event',
    event: msg.event,
  }
}

```

---

