# outputStyles 模块

## 概述

**位置:** `src/outputStyles/`

## 文件统计

- TypeScript 文件: 1
- TypeScript React 文件: 0
- 总计: 1

## 文件详情

---


### `src/outputStyles/loadOutputStylesDir.ts`

**信息:**
- 行数: 98
- 大小: 3438 bytes
- 类型: TypeScript Module

**文件内容预览 (前50行):**

```typescript
import memoize from 'lodash-es/memoize.js'
import { basename } from 'path'
import type { OutputStyleConfig } from '../constants/outputStyles.js'
import { logForDebugging } from '../utils/debug.js'
import { coerceDescriptionToString } from '../utils/frontmatterParser.js'
import { logError } from '../utils/log.js'
import {
  extractDescriptionFromMarkdown,
  loadMarkdownFilesForSubdir,
} from '../utils/markdownConfigLoader.js'
import { clearPluginOutputStyleCache } from '../utils/plugins/loadPluginOutputStyles.js'

/**
 * Loads markdown files from .claude/output-styles directories throughout the project
 * and from ~/.claude/output-styles directory and converts them to output styles.
 *
 * Each filename becomes a style name, and the file content becomes the style prompt.
 * The frontmatter provides name and description.
 *
 * Structure:
 * - Project .claude/output-styles/*.md -> project styles
 * - User ~/.claude/output-styles/*.md -> user styles (overridden by project styles)
 *
 * @param cwd Current working directory for project directory traversal
 */
export const getOutputStyleDirStyles = memoize(
  async (cwd: string): Promise<OutputStyleConfig[]> => {
    try {
      const markdownFiles = await loadMarkdownFilesForSubdir(
        'output-styles',
        cwd,
      )

      const styles = markdownFiles
        .map(({ filePath, frontmatter, content, source }) => {
          try {
            const fileName = basename(filePath)
            const styleName = fileName.replace(/\.md$/, '')

            // Get style configuration from frontmatter
            const name = (frontmatter['name'] || styleName) as string
            const description =
              coerceDescriptionToString(
                frontmatter['description'],
                styleName,
              ) ??
              extractDescriptionFromMarkdown(
                content,
                `Custom ${styleName} output style`,
              )

```

---

