# schemas 模块

## 概述

**位置:** `src/schemas/`

## 文件统计

- TypeScript 文件: 1
- TypeScript React 文件: 0
- 总计: 1

## 文件详情

---


### `src/schemas/hooks.ts`

**信息:**
- 行数: 222
- 大小: 7884 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Hook Zod schemas extracted to break import cycles.
 *
 * This file contains hook-related schema definitions that were originally
 * in src/utils/settings/types.ts. By extracting them here, we break the
 * circular dependency between settings/types.ts and plugins/schemas.ts.
 *
 * Both files now import from this shared location instead of each other.
 */

import { HOOK_EVENTS, type HookEvent } from 'src/entrypoints/agentSdkTypes.js'
import { z } from 'zod/v4'
import { lazySchema } from '../utils/lazySchema.js'
import { SHELL_TYPES } from '../utils/shell/shellProvider.js'

// Shared schema for the `if` condition field.
// Uses permission rule syntax (e.g., "Bash(git *)", "Read(*.ts)") to filter hooks
// before spawning. Evaluated against the hook input's tool_name and tool_input.
const IfConditionSchema = lazySchema(() =>
  z
    .string()
    .optional()
    .describe(
      'Permission rule syntax to filter when this hook runs (e.g., "Bash(git *)"). ' +
        'Only runs if the tool call matches the pattern. Avoids spawning hooks for non-matching commands.',
    ),
)

// Internal factory for individual hook schemas (shared between exported
// discriminated union members and the HookCommandSchema factory)
function buildHookSchemas() {
  const BashCommandHookSchema = z.object({
    type: z.literal('command').describe('Shell command hook type'),
    command: z.string().describe('Shell command to execute'),
    if: IfConditionSchema(),
    shell: z
      .enum(SHELL_TYPES)
      .optional()
      .describe(
        "Shell interpreter. 'bash' uses your $SHELL (bash/zsh/sh); 'powershell' uses pwsh. Defaults to bash.",
      ),
    timeout: z
      .number()
      .positive()
      .optional()
      .describe('Timeout in seconds for this specific command'),
    statusMessage: z
      .string()
      .optional()
      .describe('Custom status message to display in spinner while hook runs'),

```

---

