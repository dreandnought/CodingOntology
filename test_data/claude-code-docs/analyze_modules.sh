#!/bin/bash

# Claude Code 模块分析脚本
# 生成详细的模块文档和代码索引

BASE_DIR="/root/.openclaw/workspace/claude-code-rev"
DOCS_DIR="/root/.openclaw/workspace/Claude-Code-Docs"

# 创建主文档索引
MAIN_INDEX="$DOCS_DIR/README.md"

echo "# Claude Code 模块文档索引" > "$MAIN_INDEX"
echo "" >> "$MAIN_INDEX"
echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$MAIN_INDEX"
echo "" >> "$MAIN_INDEX"
echo "---" >> "$MAIN_INDEX"
echo "" >> "$MAIN_INDEX"

echo "## 模块列表" >> "$MAIN_INDEX"
echo "" >> "$MAIN_INDEX"

# 遍历所有模块
for module in $(ls -d "$BASE_DIR/src/*/"); do
    module_name=$(basename "$module")
    module_docs_dir="$DOCS_DIR/$module_name"

    echo "分析模块: $module_name"

    # 创建模块文档目录
    mkdir -p "$module_docs_dir"

    # 统计文件信息
    ts_files=$(find "$module" -type f -name "*.ts" | wc -l)
    tsx_files=$(find "$module" -type f -name "*.tsx" | wc -l)
    total_files=$((ts_files + tsx_files))

    # 创建模块文档
    module_doc="$module_docs_dir/README.md"

    echo "# $module_name 模块" > "$module_doc"
    echo "" >> "$module_doc"
    echo "## 概述" >> "$module_doc"
    echo "" >> "$module_doc"
    echo "位置: \`src/$module_name/\`" >> "$module_doc"
    echo "" >> "$module_doc"

    echo "## 文件统计" >> "$module_doc"
    echo "" >> "$module_doc"
    echo "- TypeScript 文件: $ts_files" >> "$module_doc"
    echo "- TypeScript React 文件: $tsx_files" >> "$module_doc"
    echo "- 总计: $total_files" >> "$module_doc"
    echo "" >> "$module_doc"

    echo "## 文件列表" >> "$module_doc"
    echo "" >> "$module_doc"

    # 列出所有文件
    for file in $(find "$module" -type f \( -name "*.ts" -o -name "*.tsx" \) | sort); do
        rel_path=${file#$BASE_DIR/}
        file_size=$(wc -l < "$file")
        echo "### \`$rel_path\`" >> "$module_doc"
        echo "" >> "$module_doc"
        echo "**行数:** $file_size" >> "$module_doc"
        echo "" >> "$module_doc"

        # 读取前50行作为预览
        echo '```typescript' >> "$module_doc"
        head -50 "$file" >> "$module_doc"
        echo '```' >> "$module_doc"
        echo "" >> "$module_doc"
        echo "---" >> "$module_doc"
        echo "" >> "$module_doc"
    done

    # 添加到主索引
    echo "- [$module_name](./$module_name/README.md) ($total_files 个文件)" >> "$MAIN_INDEX"

done

echo "" >> "$MAIN_INDEX"
echo "---" >> "$MAIN_INDEX"
echo "" >> "$MAIN_INDEX"
echo "生成完成!" >> "$MAIN_INDEX"

echo "✅ 分析完成!"
echo "📁 文档目录: $DOCS_DIR"
echo "📄 主索引: $MAIN_INDEX"
