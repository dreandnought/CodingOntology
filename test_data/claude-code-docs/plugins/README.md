# plugins 模块

## 概述

**位置:** `src/plugins/`

## 文件统计

- TypeScript 文件: 2
- TypeScript React 文件: 0
- 总计: 2

## 文件详情

---


### `src/plugins/builtinPlugins.ts`

**信息:**
- 行数: 159
- 大小: 4980 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Built-in Plugin Registry
 *
 * Manages built-in plugins that ship with the CLI and can be enabled/disabled
 * by users via the /plugin UI.
 *
 * Built-in plugins differ from bundled skills (src/skills/bundled/) in that:
 * - They appear in the /plugin UI under a "Built-in" section
 * - Users can enable/disable them (persisted to user settings)
 * - They can provide multiple components (skills, hooks, MCP servers)
 *
 * Plugin IDs use the format `{name}@builtin` to distinguish them from
 * marketplace plugins (`{name}@{marketplace}`).
 */

import type { Command } from '../commands.js'
import type { BundledSkillDefinition } from '../skills/bundledSkills.js'
import type { BuiltinPluginDefinition, LoadedPlugin } from '../types/plugin.js'
import { getSettings_DEPRECATED } from '../utils/settings/settings.js'

const BUILTIN_PLUGINS: Map<string, BuiltinPluginDefinition> = new Map()

export const BUILTIN_MARKETPLACE_NAME = 'builtin'

/**
 * Register a built-in plugin. Call this from initBuiltinPlugins() at startup.
 */
export function registerBuiltinPlugin(
  definition: BuiltinPluginDefinition,
): void {
  BUILTIN_PLUGINS.set(definition.name, definition)
}

/**
 * Check if a plugin ID represents a built-in plugin (ends with @builtin).
 */
export function isBuiltinPluginId(pluginId: string): boolean {
  return pluginId.endsWith(`@${BUILTIN_MARKETPLACE_NAME}`)
}

/**
 * Get a specific built-in plugin definition by name.
 * Useful for the /plugin UI to show the skills/hooks/MCP list without
 * a marketplace lookup.
 */
export function getBuiltinPluginDefinition(
  name: string,
): BuiltinPluginDefinition | undefined {
  return BUILTIN_PLUGINS.get(name)
}

```

---


### `src/plugins/bundled/index.ts`

**信息:**
- 行数: 23
- 大小: 843 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
/**
 * Built-in Plugin Initialization
 *
 * Initializes built-in plugins that ship with the CLI and appear in the
 * /plugin UI for users to enable/disable.
 *
 * Not all bundled features should be built-in plugins — use this for
 * features that users should be able to explicitly enable/disable. For
 * features with complex setup or automatic-enabling logic (e.g.
 * claude-in-chrome), use src/skills/bundled/ instead.
 *
 * To add a new built-in plugin:
 * 1. Import registerBuiltinPlugin from '../builtinPlugins.js'
 * 2. Call registerBuiltinPlugin() with the plugin definition here
 */

/**
 * Initialize built-in plugins. Called during CLI startup.
 */
export function initBuiltinPlugins(): void {
  // No built-in plugins registered yet — this is the scaffolding for
  // migrating bundled skills that should be user-toggleable.
}

```

---

