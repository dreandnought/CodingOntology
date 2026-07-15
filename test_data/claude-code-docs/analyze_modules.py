#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Claude Code 模块文档生成器
- 遍历所有模块
- 生成详细的模块文档
- 创建代码索引
- 建立文档到代码的映射
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path("/root/.openclaw/workspace/claude-code-rev/src")
DOCS_DIR = Path("/root/.openclaw/workspace/Claude-Code-Docs")

# 确保文档目录存在
DOCS_DIR.mkdir(exist_ok=True)

# 主索引数据
main_index = {
    "title": "Claude Code 模块文档索引",
    "generated_at": datetime.now().isoformat(),
    "modules": [],
    "total_files": 0,
    "total_lines": 0
}

# 遍历所有模块
for module_dir in sorted(BASE_DIR.iterdir()):
    if not module_dir.is_dir():
        continue

    module_name = module_dir.name
    module_docs_dir = DOCS_DIR / module_name

    # 创建模块文档目录
    module_docs_dir.mkdir(exist_ok=True)

    print(f"📦 分析模块: {module_name}")

    # 统计文件
    ts_files = list(module_dir.rglob("*.ts"))
    tsx_files = list(module_dir.rglob("*.tsx"))
    all_files = ts_files + tsx_files

    # 模块数据
    module_data = {
        "name": module_name,
        "path": f"src/{module_name}/",
        "ts_files": len(ts_files),
        "tsx_files": len(tsx_files),
        "total_files": len(all_files),
        "files": []
    }

    # 创建模块 README
    readme_path = module_docs_dir / "README.md"
    readme_content = f"""# {module_name} 模块

## 概述

**位置:** `src/{module_name}/`

## 文件统计

- TypeScript 文件: {len(ts_files)}
- TypeScript React 文件: {len(tsx_files)}
- 总计: {len(all_files)}

## 文件详情

---

"""

    # 分析每个文件
    for file_path in sorted(all_files):
        rel_path = str(file_path.relative_to(Path("/root/.openclaw/workspace/claude-code-rev")))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                line_count = len(lines)
                file_size = file_path.stat().st_size
                
                # 提取文件头部注释
                header_comments = []
                for line in lines[:30]:
                    stripped = line.strip()
                    if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('/**'):
                        header_comments.append(stripped)
                    elif stripped and not stripped.startswith('//') and not stripped.startswith('*'):
                        break
                
                # 添加到文件详情
                readme_content += f"""
### `{rel_path}`

**信息:**
- 行数: {line_count}
- 大小: {file_size} bytes
- 类型: {'React Component' if file_path.suffix == '.tsx' else 'TypeScript Module'}

**文件内容预览 (前50行):**

```typescript
{''.join(lines[:50])}
```

---

"""
                
                # 添加到模块数据
                module_data["files"].append({
                    "path": rel_path,
                    "lines": line_count,
                    "size": file_size
                })
                
                main_index["total_files"] += 1
                main_index["total_lines"] += line_count
                
        except Exception as e:
            print(f"  ⚠️ 读取文件错误: {file_path} - {e}")
            continue

    # 写入模块 README
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # 写入模块 JSON 数据
    json_path = module_docs_dir / "module_data.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(module_data, f, indent=2, ensure_ascii=False)
    
    # 添加到主索引

    main_index["modules"].append(module_data)

# 生成主索引 README
main_readme_path = DOCS_DIR / "README.md"
main_readme_content = f"""# Claude Code 模块文档索引

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 总体统计

- **模块数量:** {len(main_index['modules'])}
- **文件总数:** {main_index['total_files']}
- **代码总行数:** {main_index['total_lines']:,}

---

## 📦 模块列表

| 模块 | TypeScript 文件 | TSX 文件 | 总文件数 | 链接 |
|------|---------------|-----------|----------|------|
"""

for module in main_index["modules"]:
    main_readme_content += f"| {module['name']} | {module['ts_files']} | {module['tsx_files']} | {module['total_files']} | [📄 查看](./{module['name']}/README.md) |\n"

main_readme_content += """

---

## 🔍 快速导航

"""

# 按功能分类
categories = {
    "核心功能": ["bootstrap", "cli", "context", "entrypoints", "state"],
    "工具系统": ["tools", "Tool", "hooks"],
    "用户界面": ["components", "screens", "ink", "outputStyles"],
    "服务层": ["services", "bridge", "coordinator", "remote"],
    "插件系统": ["plugins", "skills", "migrations"],
    "命令系统": ["commands"],
    "辅助工具": ["utils", "types", "constants", "schemas"],
    "其他": []
}

for category, modules in categories.items():
    main_readme_content += f"\n### {category}\n\n"
    
    found_modules = []
    for module in main_index["modules"]:
        if module['name'] in modules:
            found_modules.append(module)
        # 添加到"其他"类别
        if category == "其他" and not any(module['name'] in m for m in categories.values() if m != categories["其他"]):
            if module not in found_modules:
                found_modules.append(module)
    
    for module in found_modules:
        main_readme_content += f"- [{module['name']}](./{module['name']}/README.md) - {module['total_files']} 个文件\n"

# 写入主索引
with open(main_readme_path, 'w', encoding='utf-8') as f:
    f.write(main_readme_content)

# 写入主索引 JSON
main_json_path = DOCS_DIR / "index.json"
with open(main_json_path, 'w', encoding='utf-8') as f:
    json.dump(main_index, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 60)
print("✅ 分析完成!")
print(f"📁 文档目录: {DOCS_DIR}")
print(f"📄 主索引: {main_readme_path}")
print(f"📊 数据索引: {main_json_path}")
print(f"📦 模块数量: {len(main_index['modules'])}")
print(f"📄 文件总数: {main_index['total_files']:,}")
print(f"📏 代码行数: {main_index['total_lines']:,}")
print("=" * 60)
