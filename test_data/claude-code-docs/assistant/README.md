# assistant 模块

## 概述

**位置:** `src/assistant/`

## 文件统计

- TypeScript 文件: 3
- TypeScript React 文件: 0
- 总计: 3

## 文件详情

---


### `src/assistant/index.ts`

**信息:**
- 行数: 14
- 大小: 338 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
function readAssistantModeFlag(): boolean {
  return (
    process.env.CLAUDE_CODE_ASSISTANT_MODE === '1' ||
    process.env.CLAUDE_CODE_ASSISTANT_MODE === 'true'
  )
}

export function isAssistantMode(): boolean {
  return readAssistantModeFlag()
}

export function isAssistantModeEnabled(): boolean {
  return readAssistantModeFlag()
}

```

---


### `src/assistant/sessionDiscovery.ts`

**信息:**
- 行数: 3
- 大小: 66 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export async function discoverAssistantSessions() {
  return []
}

```

---


### `src/assistant/sessionHistory.ts`

**信息:**
- 行数: 87
- 大小: 2503 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import axios from 'axios'
import { getOauthConfig } from '../constants/oauth.js'
import type { SDKMessage } from '../entrypoints/agentSdkTypes.js'
import { logForDebugging } from '../utils/debug.js'
import { getOAuthHeaders, prepareApiRequest } from '../utils/teleport/api.js'

export const HISTORY_PAGE_SIZE = 100

export type HistoryPage = {
  /** Chronological order within the page. */
  events: SDKMessage[]
  /** Oldest event ID in this page → before_id cursor for next-older page. */
  firstId: string | null
  /** true = older events exist. */
  hasMore: boolean
}

type SessionEventsResponse = {
  data: SDKMessage[]
  has_more: boolean
  first_id: string | null
  last_id: string | null
}

export type HistoryAuthCtx = {
  baseUrl: string
  headers: Record<string, string>
}

/** Prepare auth + headers + base URL once, reuse across pages. */
export async function createHistoryAuthCtx(
  sessionId: string,
): Promise<HistoryAuthCtx> {
  const { accessToken, orgUUID } = await prepareApiRequest()
  return {
    baseUrl: `${getOauthConfig().BASE_API_URL}/v1/sessions/${sessionId}/events`,
    headers: {
      ...getOAuthHeaders(accessToken),
      'anthropic-beta': 'ccr-byoc-2025-07-29',
      'x-organization-uuid': orgUUID,
    },
  }
}

async function fetchPage(
  ctx: HistoryAuthCtx,
  params: Record<string, string | number | boolean>,
  label: string,
): Promise<HistoryPage | null> {
  const resp = await axios

```

---

