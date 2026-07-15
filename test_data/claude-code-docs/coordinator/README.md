# coordinator 模块

## 概述

**位置:** `src/coordinator/`

## 文件统计

- TypeScript 文件: 2
- TypeScript React 文件: 0
- 总计: 2

## 文件详情

---


### `src/coordinator/coordinatorMode.ts`

**信息:**
- 行数: 369
- 大小: 19020 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import { feature } from 'bun:bundle'
import { ASYNC_AGENT_ALLOWED_TOOLS } from '../constants/tools.js'
import { checkStatsigFeatureGate_CACHED_MAY_BE_STALE } from '../services/analytics/growthbook.js'
import {
  type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS,
  logEvent,
} from '../services/analytics/index.js'
import { AGENT_TOOL_NAME } from '../tools/AgentTool/constants.js'
import { BASH_TOOL_NAME } from '../tools/BashTool/toolName.js'
import { FILE_EDIT_TOOL_NAME } from '../tools/FileEditTool/constants.js'
import { FILE_READ_TOOL_NAME } from '../tools/FileReadTool/prompt.js'
import { SEND_MESSAGE_TOOL_NAME } from '../tools/SendMessageTool/constants.js'
import { SYNTHETIC_OUTPUT_TOOL_NAME } from '../tools/SyntheticOutputTool/SyntheticOutputTool.js'
import { TASK_STOP_TOOL_NAME } from '../tools/TaskStopTool/prompt.js'
import { TEAM_CREATE_TOOL_NAME } from '../tools/TeamCreateTool/constants.js'
import { TEAM_DELETE_TOOL_NAME } from '../tools/TeamDeleteTool/constants.js'
import { isEnvTruthy } from '../utils/envUtils.js'

// Checks the same gate as isScratchpadEnabled() in
// utils/permissions/filesystem.ts. Duplicated here because importing
// filesystem.ts creates a circular dependency (filesystem -> permissions
// -> ... -> coordinatorMode). The actual scratchpad path is passed in via
// getCoordinatorUserContext's scratchpadDir parameter (dependency injection
// from QueryEngine.ts, which lives higher in the dep graph).
function isScratchpadGateEnabled(): boolean {
  return checkStatsigFeatureGate_CACHED_MAY_BE_STALE('tengu_scratch')
}

const INTERNAL_WORKER_TOOLS = new Set([
  TEAM_CREATE_TOOL_NAME,
  TEAM_DELETE_TOOL_NAME,
  SEND_MESSAGE_TOOL_NAME,
  SYNTHETIC_OUTPUT_TOOL_NAME,
])

export function isCoordinatorMode(): boolean {
  if (feature('COORDINATOR_MODE')) {
    return isEnvTruthy(process.env.CLAUDE_CODE_COORDINATOR_MODE)
  }
  return false
}

/**
 * Checks if the current coordinator mode matches the session's stored mode.
 * If mismatched, flips the environment variable so isCoordinatorMode() returns
 * the correct value for the resumed session. Returns a warning message if
 * the mode was switched, or undefined if no switch was needed.
 */
export function matchSessionMode(
  sessionMode: 'coordinator' | 'normal' | undefined,

```

---


### `src/coordinator/workerAgent.ts`

**信息:**
- 行数: 1
- 大小: 37 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
export const WORKER_AGENT = 'worker'

```

---

