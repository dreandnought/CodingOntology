# PRD Ontology MCP 开发文档

## 项目概述

为 Coding Agent（Claude Code、Cline 等）构建 MCP 插件，增强其对 PRD 的理解能力。将 PRD 中的实体和隐性关系建模为显式 Ontology 图，让 Agent 不仅能"读"PRD，更能"理解"其中的因果链、约束关系、依赖网络。

## 验证阶段

当前处于**验证阶段**，目标是尽快构建轻量级原型跑通方案。

### 关键原则

- **不引入向量模型**（无 embedding，纯 LLM 语义匹配）
- **SQLite 存储**（零依赖，轻量）
- **可读实体 ID**（便于调试和人工检查）
- **LLM 只抽取第一层实体**，关系从预设 Ontology 匹配
- **预设 Ontology 由 Agent 按结构化协议构建**（详见 ONTOLOGY_BUILD_GUIDE.md）

### MVP 范围

只实现 `parse_prd` + `query_ontology` 两个 MCP 工具，暂不做冲突检测和影响分析。

### 核心流程

```
Phase 1（离线/预处理 - 由 Agent 按指南构建）
  企业知识（代码库、API文档、历史PRD、Wiki等）
    → 按 ONTOLOGY_BUILD_GUIDE.md 协议
    → 构建预设 Ontology（SQLite 数据库文件）
    ↓
Phase 2（在线/每次 PRD 解析）
  新 PRD 到达
    → parse_prd 调用 LLM 抽取第一层实体（功能级）
    → 在预设 Ontology 中匹配实体（LLM 语义匹配）
    → 查询匹配到的实体的关联关系
    → 关系以 Markdown 附录追加到 PRD 末尾
    → 返回增强版 PRD → Coding Agent 做任务规划
```

### 已确认决策

| 项目 | 决策 |
|------|------|
| 阶段 | 验证阶段，不引入向量模型 |
| PRD 输入格式 | Markdown/纯文本，保留结构化 |
| LLM 抽取粒度 | 功能级实体（功能、模块、接口） |
| 实体匹配方案 | 纯 LLM 语义匹配（MVP），后续升级 FTS5+LLM |
| 匹配时机 | 在 parse_prd 同一个 LLM prompt 中完成 |
| 输出格式 | Markdown 附录追加到 PRD 末尾 |
| 返回方式 | 同步返回增强版 PRD |
| 预设 Ontology 存储 | SQLite 数据库（按协议由 Agent 构建） |
| 实体 ID 格式 | `{type_short}:{normalized_name}`，如 `func:user_login` |
| 关系类型 | depends_on, causes, constrains, impacts, conflicts_with, derived_from, implements, contains, refines, relates_to |
| 实体类型 | requirement, function, module, interface, data_entity, test_case, constraint, actor |

## 技术栈

- **运行时**：Python + FastMCP
- **存储**：SQLite（轻量级，零依赖）
- **LLM**：DeepSeek V4 API（或本地 Qwen2.5-7B 量化版）
- **传输**：stdio（MCP 标准）

## MCP 工具接口设计

### 1. parse_prd

**作用：** 解析 PRD 文档，抽取第一层实体，在预设 Ontology 中匹配并查询关系，返回增强版 PRD。

**输入：**
```json
{
  "content": "string (PRD 的 Markdown/纯文本内容)"
}
```

**输出：**
```json
{
  "enriched_prd": "string (增强后的 PRD Markdown，末尾追加了关系附录)",
  "summary": {
    "entities_extracted": 5,
    "entities_matched": 3,
    "relations_found": 8,
    "new_entities_added": 2
  }
}
```

**处理流程：**
1. LLM 从 PRD 中抽取第一层实体（功能级）
2. LLM 将实体映射到预设 Ontology 中的实体
3. 查询匹配实体的关联关系（SQLite 查询）
4. LLM 将关系整理为 Markdown 附录
5. 返回增强版 PRD

**关系附录格式示例：**
```markdown
## 🔗 需求关系图谱（自动分析）

### 依赖关系
- 用户登录 → 依赖 → 短信验证码服务
- 订单提交 → 依赖 → 库存查询接口

### 约束关系
- 支付必须在订单确认之后
- 密码长度 8-32 位

### 影响关系
- 修改用户认证模块 → 影响 → 登录、注册、找回密码
```

---

### 2. query_ontology

**作用：** 查询 Ontology 中的实体和关系。供 Coding Agent 在后续任务规划中按需查询更多信息。

**输入（方案 A - 按实体名称查询）：**
```json
{
  "entity_name": "string (实体名称)",
  "relation_types": ["depends_on", "impacts"] (可选，筛选关系类型)
}
```

**输入（方案 B - 按实体 ID 查询）：**
```json
{
  "entity_id": "string (实体 ID)",
  "relation_types": ["depends_on", "impacts"] (可选，筛选关系类型)
}
```

**输入（方案 C - 搜索）：**
```json
{
  "query": "string (关键词搜索)",
  "limit": 10 (可选，默认 10)
}
```

**统一输出：**
```json
{
  "entity": {
    "id": "func:user_login",
    "name": "用户登录",
    "type": "function",
    "description": "用户登录功能，支持手机号和邮箱登录",
    "properties": {}
  },
  "relations": [
    {
      "type": "depends_on",
      "direction": "outgoing",
      "target_entity": {
        "id": "iface:sms_service",
        "name": "短信验证码服务",
        "type": "interface"
      },
      "confidence": 0.95,
      "reason": "登录需要验证手机号"
    },
    {
      "type": "impacts",
      "direction": "outgoing",
      "target_entity": {
        "id": "mod:auth_module",
        "name": "用户认证模块",
        "type": "module"
      },
      "confidence": 0.85,
      "reason": "登录功能属于认证模块"
    }
  ]
}
```

**说明：** 方案 A 和 B 任选其一传入。如果都传，优先使用 `entity_id`。方案 C 用于关键词搜索（匹配实体名称和描述）。

## 预设 Ontology 初始化

### 数据源
- 历史 PRD 文档
- 代码库（模块结构、函数、接口依赖）
- API 文档 / Swagger / OpenAPI
- 团队 Wiki / 设计文档
- Bug 记录、Changelog

### 初始化流程
1. 从代码库提取模块结构和接口定义（静态分析）
2. 从 API 文档提取接口实体和关系
3. 从历史 PRD 用 LLM 抽取实体和关系
4. 全局实体消歧
5. 存入 SQLite

### 协议文档
详见 `ONTOLOGY_BUILD_GUIDE.md`，该文档定义了：
- 实体 ID 命名规范
- SQLite 表结构和字段协议
- 实体类型和关系类型枚举
- 关系方向性定义（对称/非对称）
- 置信度和元数据字段规范

## 工程结构

```
prd-ontology-mcp/
├── server.py                 # MCP Server 入口
├── requirements.txt          # 依赖
├── DEVELOPMENT.md            # 开发文档（本文件）
├── ONTOLOGY_BUILD_GUIDE.md   # Ontology 构建指南（供其他 Agent 使用）
├── models/
│   ├── __init__.py
│   ├── schema.py             # SQLite 表定义 + 初始化
│   ├── entity.py             # Entity CRUD
│   └── relation.py           # Relation CRUD
├── parser/
│   ├── __init__.py
│   └── llm_parser.py         # LLM 驱动的 PRD 解析
├── tools/
│   ├── __init__.py
│   ├── parse_prd.py          # MCP Tool: parse_prd
│   └── query_ontology.py     # MCP Tool: query_ontology
├── storage/
│   ├── __init__.py
│   └── connection.py         # SQLite 连接管理
└── init/
    ├── __init__.py
    └── seed.py               # 预设 Ontology 初始化（按协议）
```

## 自监督迭代框架（Phase 2+）

不在 MVP 范围内，详见 wiki 方案文档 `wiki/ideas/2026-07-07-prd-ontology-mcp-plugin.md`。

## 相关文档

- [PRD Ontology MCP 插件方案（wiki）](../wiki/ideas/2026-07-07-prd-ontology-mcp-plugin.md)
- [Palantir Ontology 深度调研](../wiki/tech/ai-coding/2026-07-08-palantir-ontology-deep-dive.md)
- [类似 Palantir 的开源代码分析项目调研](../wiki/tech/ai-coding/2026-07-06-ontology-like-code-analysis-projects.md)
