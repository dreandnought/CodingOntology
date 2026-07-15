# 测试数据目录

用于 PRD Ontology MCP 插件的测试验证。存放从 Claude Code 仓库和公司文档中提取的测试数据。

## 数据来源

### 1. claude-code-docs/
Claude Code 源码的结构化分析文档（4.5MB）。
- 38 个模块的 `module_data.json` 和 `README.md`
- 每个模块包含文件结构、类型定义、依赖关系的结构化数据
- 来源：`Claude-Code-Docs/`（逆向工程分析结果）

### 2. claude-code-main-*.md
Claude Code 主仓库的关键文档：
- `claude-code-main-readme.md` — 主仓库 README
- `claude-code-main-claude.md` — CLAUDE.md（项目规范）
- `claude-code-main-v6.md` — V6 版本更新文档（119KB，最详细）
- `claude-code-main-readme-en.md` — 英文版 README
- `claude-code-main-devlog.md` — 开发日志

### 3. claude-code-rev-*.md
Claude Code 逆向工程分析文档：
- `claude-code-rev-readme.md` — 逆向工程项目说明
- `claude-code-rev-claude.md` — 逆向分析的 CLAUDE.md
- `claude-code-rev-agents.md` — 逆向分析的 AGENTS.md

## 用途

- 作为预设 Ontology 的初始化数据源
- 用于测试 `parse_prd` 的 PRD 解析能力
- 用于测试 `query_ontology` 的实体关系查询
- 验证 Ontology 构建指南的可行性
