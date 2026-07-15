# PRD Ontology 构建指南

> **用途**：供 Coding Agent（Claude Code、Cline 等）按照统一协议，从企业项目文档中抽取知识，构建 PRD Ontology MCP 系统所需的预设 Ontology 结构化数据。
>
> **存储方式**：SQLite 数据库文件
> **协议版本**：v1.0（验证阶段）

---

## 1. 概述

### 1.1 什么是 Ontology

Ontology（本体论）是对现实世界实体及其关系的形式化描述。在本项目中，Ontology 是企业知识的**结构化表示**——将散落在 PRD、代码库、API 文档、Wiki 中的实体（功能、模块、接口等）和它们之间的关系（依赖、影响、约束等）组织为可查询的图谱。

### 1.2 构建目标

当你完成本指南的步骤后，你会生成一个 SQLite 数据库文件（如 `ontology.db`），其中包含：

- 企业项目中的核心实体（功能、模块、接口、数据实体等）
- 实体之间的关系（依赖、影响、约束等）
- 每个实体的描述和元数据

这个数据库文件将作为 `parse_prd` 工具的知识底座。

### 1.3 验证阶段说明

当前处于**验证阶段**，目标为：
- **不引入向量模型**（无 embedding，纯 LLM 语义匹配）
- **SQLite 存储**（零依赖，轻量）
- **可读实体 ID**（便于调试和人工检查）
- 后续可升级为更完善的方案

---

## 2. 数据模型（SQLite 表结构）

### 2.1 实体类型表（entity_types）

预定义系统中可能出现的实体类型：

```sql
CREATE TABLE IF NOT EXISTS entity_types (
    id          TEXT PRIMARY KEY,           -- 类型 ID，如 "function", "module"
    name        TEXT NOT NULL,              -- 显示名称，如 "功能"
    description TEXT,                       -- 类型描述
    parent_id   TEXT REFERENCES entity_types(id),  -- 父类型（可选，用于层级）
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
```

**预置类型（必须包含）：**

| id | name | description | parent_id |
|----|------|-------------|-----------|
| `requirement` | 需求 | 业务需求或用户需求 | NULL |
| `function` | 功能 | 系统功能点 | NULL |
| `module` | 模块 | 代码模块或子系统 | NULL |
| `interface` | 接口 | API 接口或服务接口 | NULL |
| `data_entity` | 数据实体 | 数据库表或数据模型 | NULL |
| `test_case` | 测试用例 | 测试用例或测试场景 | NULL |
| `constraint` | 约束 | 业务约束或技术约束 | NULL |
| `actor` | 角色 | 用户角色或系统角色 | NULL |

### 2.2 关系类型表（relation_types）

预定义实体间可能的关系：

```sql
CREATE TABLE IF NOT EXISTS relation_types (
    id          TEXT PRIMARY KEY,           -- 关系类型 ID
    name        TEXT NOT NULL,              -- 显示名称
    description TEXT,                       -- 关系描述
    symmetric   INTEGER NOT NULL DEFAULT 0, -- 是否对称关系（0=否,1=是）
    transitive  INTEGER NOT NULL DEFAULT 0, -- 是否可传递（0=否,1=是）
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);
```

**预置关系（必须包含）：**

| id | name | description | symmetric | transitive |
|----|------|-------------|-----------|------------|
| `depends_on` | 依赖 | A 依赖 B 才能正常工作 | 0 | 1 |
| `causes` | 因果 | A 的发生会导致 B | 0 | 0 |
| `constrains` | 约束 | A 对 B 有约束条件 | 0 | 0 |
| `impacts` | 影响 | 修改 A 会影响 B | 0 | 0 |
| `conflicts_with` | 冲突 | A 和 B 互斥或冲突 | 1 | 0 |
| `derived_from` | 派生 | A 是从 B 派生/衍生出来的 | 0 | 1 |
| `implements` | 实现 | A 实现了 B（接口/需求） | 0 | 0 |
| `contains` | 包含 | A 包含 B（父子关系） | 0 | 1 |
| `refines` | 细化 | A 是对 B 的细化/补充 | 0 | 0 |
| `relates_to` | 关联 | A 和 B 有关联（通用关系） | 1 | 0 |

### 2.3 实体实例表（entities）

存储所有实体实例，这是最核心的表：

```sql
CREATE TABLE IF NOT EXISTS entities (
    id              TEXT PRIMARY KEY,           -- 实体 ID，格式见 3.1
    type_id         TEXT NOT NULL REFERENCES entity_types(id),  -- 实体类型
    name            TEXT NOT NULL,              -- 实体名称（中文/英文）
    description     TEXT,                       -- 实体描述
    status          TEXT NOT NULL DEFAULT 'active'
                    CHECK(status IN ('active', 'deprecated', 'removed')),  -- 状态
    confidence      REAL NOT NULL DEFAULT 0.8, -- 置信度（0-1）
    source          TEXT NOT NULL DEFAULT 'manual',  -- 来源：manual/llm/code/apidoc
    source_doc_id   TEXT,                       -- 来源文档 ID
    source_ref      TEXT,                       -- 来源引用（如文件路径、行号）
    properties      TEXT DEFAULT '{}',          -- 扩展属性（JSON 对象）
    tags            TEXT DEFAULT '[]',          -- 标签（JSON 数组）
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type_id);
CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
CREATE INDEX IF NOT EXISTS idx_entities_status ON entities(status);
```

### 2.4 关系实例表（relations）

存储所有实体间的关系，这是另一个核心表：

```sql
CREATE TABLE IF NOT EXISTS relations (
    id              TEXT PRIMARY KEY,           -- 关系 ID
    type_id         TEXT NOT NULL REFERENCES relation_types(id),  -- 关系类型
    source_id       TEXT NOT NULL REFERENCES entities(id),       -- 源实体
    target_id       TEXT NOT NULL REFERENCES entities(id),       -- 目标实体
    weight          REAL NOT NULL DEFAULT 1.0,  -- 权重（0-1，强度）
    confidence      REAL NOT NULL DEFAULT 0.8,  -- 置信度（0-1）
    source          TEXT NOT NULL DEFAULT 'manual',  -- 来源
    source_doc_id   TEXT,                       -- 来源文档 ID
    metadata        TEXT DEFAULT '{}',          -- 扩展元数据（JSON）
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(type_id, source_id, target_id)       -- 去重约束
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_relations_source ON relations(source_id);
CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target_id);
CREATE INDEX IF NOT EXISTS idx_relations_type ON relations(type_id);
CREATE INDEX IF NOT EXISTS idx_relations_st ON relations(source_id, type_id);
CREATE INDEX IF NOT EXISTS idx_relations_ts ON relations(target_id, type_id);
```

### 2.5 文档来源表（documents）

记录构建 Ontology 时使用的源文档：

```sql
CREATE TABLE IF NOT EXISTS documents (
    id              TEXT PRIMARY KEY,           -- 文档 ID
    title           TEXT NOT NULL,              -- 文档标题
    doc_type        TEXT NOT NULL DEFAULT 'prd', -- 文档类型：prd/code/apidoc/wiki
    url             TEXT,                       -- 文档 URL
    file_path       TEXT,                       -- 文件路径
    content_hash    TEXT,                       -- 内容哈希（用于去重）
    word_count      INTEGER,                    -- 字数
    status          TEXT NOT NULL DEFAULT 'parsed'
                    CHECK(status IN ('pending', 'parsing', 'parsed', 'failed')),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    parsed_at       TEXT
);
```

---

## 3. 实体 ID 命名规范

### 3.1 格式

```
{type_short}:{normalized_name}
```

- `type_short`：实体类型的缩写
- `normalized_name`：实体名称的规范化形式

### 3.2 类型缩写对照表

| 实体类型 | 缩写 | 示例 |
|---------|------|------|
| requirement | `req` | `req:two_factor_auth` |
| function | `func` | `func:user_login` |
| module | `mod` | `mod:auth_module` |
| interface | `iface` | `iface:sms_service` |
| data_entity | `data` | `data:user_table` |
| test_case | `test` | `test:login_flow_test` |
| constraint | `cst` | `cst:password_min_length` |
| actor | `actor` | `actor:admin_user` |

### 3.3 名称规范化规则

1. **小写**：全部转为小写
2. **连字符**：空格、中文空格转为 `_`
3. **中文保留**：中文词之间用 `_` 连接，如 `func:user_login`
4. **英文命名**：英文使用 snake_case，如 `func:create_order`
5. **中英混合**：混合时以英文为主，如 `func:sms_verify`
6. **长度限制**：不超过 64 个字符
7. **唯一性**：同一类型下 ID 必须唯一

**示例：**
```
func:user_login
func:create_order
mod:auth_module
iface:payment_gateway
data:order_table
req:real_time_notification
```

---

## 4. 关系方向规则

关系是有方向的，`source_id` → `target_id`。

### 4.1 对称关系

对称关系表示 A↔B 等价。查询时需要同时考虑两个方向：

```sql
-- 对称关系查询示例
SELECT * FROM relations r
JOIN relation_types rt ON r.type_id = rt.id
WHERE rt.symmetric = 1
  AND (r.source_id = ? OR r.target_id = ?)
```

**对称关系列表：** `conflicts_with`, `relates_to`

### 4.2 非对称关系

非对称关系表示 A→B 有特定语义，不可反向。查询时区分出向和入向：

```sql
-- 出向查询
SELECT 'outgoing' AS direction, r.target_id AS related_id
FROM relations r WHERE r.source_id = ?

-- 入向查询
SELECT 'incoming' AS direction, r.source_id AS related_id
FROM relations r WHERE r.target_id = ?
```

**非对称关系列表：** `depends_on`, `causes`, `constrains`, `impacts`, `derived_from`, `implements`, `contains`, `refines`

### 4.3 传递性规则

对于可传递的关系（`depends_on`, `derived_from`, `contains`），查询时可以通过递归 CTE 实现多跳推理：

```sql
-- 递归查询所有传递依赖
WITH RECURSIVE transitive AS (
    -- 初始
    SELECT r.target_id, 1 AS depth
    FROM relations r
    WHERE r.source_id = ? AND r.type_id = 'depends_on'
    UNION ALL
    -- 递归
    SELECT r.target_id, t.depth + 1
    FROM relations r
    JOIN transitive t ON r.source_id = t.target_id
    WHERE r.type_id = 'depends_on' AND t.depth < 5
)
SELECT * FROM transitive;
```

---

## 5. 构建步骤

### Step 1：准备数据源

收集所有可用的企业文档：
- 历史 PRD 文档（Markdown 或纯文本）
- 代码库目录结构（模块划分）
- API 文档（Swagger/OpenAPI）
- 设计文档、Wiki 页面
- Bug 记录、Changelog

### Step 2：初始化数据库

执行 2.1-2.5 的 SQL 建表语句和预置数据插入：

```sql
-- 插入预置实体类型
INSERT INTO entity_types (id, name, description) VALUES
    ('requirement', '需求', '业务需求或用户需求'),
    ('function', '功能', '系统功能点'),
    ('module', '模块', '代码模块或子系统'),
    ('interface', '接口', 'API 接口或服务接口'),
    ('data_entity', '数据实体', '数据库表或数据模型'),
    ('test_case', '测试用例', '测试用例或测试场景'),
    ('constraint', '约束', '业务约束或技术约束'),
    ('actor', '角色', '用户角色或系统角色');

-- 插入预置关系类型
INSERT INTO relation_types (id, name, description, symmetric, transitive) VALUES
    ('depends_on', '依赖', 'A 依赖 B 才能正常工作', 0, 1),
    ('causes', '因果', 'A 的发生会导致 B', 0, 0),
    ('constrains', '约束', 'A 对 B 有约束条件', 0, 0),
    ('impacts', '影响', '修改 A 会影响 B', 0, 0),
    ('conflicts_with', '冲突', 'A 和 B 互斥或冲突', 1, 0),
    ('derived_from', '派生', 'A 是从 B 派生/衍生出来的', 0, 1),
    ('implements', '实现', 'A 实现了 B（接口/需求）', 0, 0),
    ('contains', '包含', 'A 包含 B（父子关系）', 0, 1),
    ('refines', '细化', 'A 是对 B 的细化/补充', 0, 0),
    ('relates_to', '关联', 'A 和 B 有关联（通用关系）', 1, 0);
```

### Step 3：从代码库提取模块结构（优先）

使用静态分析工具或手动提取：
1. 识别项目中的主要模块和子模块
2. 分析模块间的 import 依赖关系
3. 提取 API 路由定义（如果使用框架）

**输出示例：**
```
实体：mod:auth_module（类型：module）
  描述：用户认证模块，处理登录、注册、权限验证
实体：mod:order_module（类型：module）
  描述：订单管理模块，处理订单创建、查询、状态流转
关系：mod:order_module → depends_on → mod:auth_module
  描述：订单模块依赖认证模块进行用户鉴权
```

### Step 4：从 API 文档提取接口

如果有 Swagger/OpenAPI 文档：
1. 提取每个 API 端点作为 interface 实体
2. 记录请求/响应格式
3. 标注接口所属模块

**输出示例：**
```
实体：iface:login_api（类型：interface）
  描述：POST /api/v1/auth/login，用户登录接口
  属性：{"method": "POST", "path": "/api/v1/auth/login"}
关系：iface:login_api → contains → func:user_login
  描述：登录接口包含了用户登录功能
```

### Step 5：从 PRD/Wiki 抽取实体和关系（LLM 辅助）

对历史 PRD 文档，使用 LLM 抽取实体和关系：

```json
// LLM 输出格式要求
{
  "entities": [
    {"name": "用户登录", "type": "function", "description": "用户通过手机号或邮箱登录系统"},
    {"name": "短信验证码服务", "type": "interface", "description": "发送短信验证码的第三方服务"}
  ],
  "relations": [
    {"source": "用户登录", "type": "depends_on", "target": "短信验证码服务", "description": "登录需要验证手机号"}
  ]
}
```

### Step 6：生成实体 ID 并去重

1. 按第 3 节的命名规范生成 ID
2. 检查 ID 是否已存在（同一名称可能出现在多个文档中）
3. 对重复实体：合并描述信息，取置信度平均值

### Step 7：存入 SQLite

使用 `INSERT OR IGNORE` 或先查后插的方式写入数据库。

**批量插入示例：**
```sql
INSERT OR IGNORE INTO entities (id, type_id, name, description, confidence, source)
VALUES (?, ?, ?, ?, ?, ?);
```

### Step 8：验证数据完整性

检查以下约束：
- [ ] 所有关系的 source_id 和 target_id 都在 entities 表中存在
- [ ] 所有 type_id 都在 entity_types 或 relation_types 表中存在
- [ ] 没有孤立的实体（没有任何关系的实体可以存在，但需要检查其描述是否完整）
- [ ] 实体 ID 格式正确

```sql
-- 检查孤立关系（目标不存在）
SELECT r.id FROM relations r
LEFT JOIN entities e ON r.source_id = e.id
WHERE e.id IS NULL;
```

---

## 6. 输出要求

### 6.1 文件格式

构建完成后输出一个 SQLite 数据库文件，命名建议：
- `ontology.db`（默认名称）

### 6.2 校验清单

| 检查项 | 说明 |
|-------|------|
| 表结构完整 | 5 张表都存在且字段正确 |
| 预置类型存在 | 8 种实体类型、10 种关系类型已插入 |
| 实体 ID 规范 | 所有实体 ID 符合 `{type_short}:{normalized_name}` 格式 |
| 关系完整性 | 所有关系引用已存在的实体 |
| 关系去重 | 同类型、同源、同目标的关系只有一条 |
| 文档记录 | 所有来源文档在 documents 表中有记录 |

### 6.3 快速检查脚本

```sql
-- 检查各表记录数
SELECT 'entity_types' AS tbl, COUNT(*) AS cnt FROM entity_types
UNION ALL
SELECT 'relation_types', COUNT(*) FROM relation_types
UNION ALL
SELECT 'entities', COUNT(*) FROM entities
UNION ALL
SELECT 'relations', COUNT(*) FROM relations
UNION ALL
SELECT 'documents', COUNT(*) FROM documents;

-- 检查孤立关系
SELECT COUNT(*) AS orphan_relations FROM relations r
WHERE NOT EXISTS (SELECT 1 FROM entities e WHERE e.id = r.source_id)
   OR NOT EXISTS (SELECT 1 FROM entities e WHERE e.id = r.target_id);
```

---

## 7. 示例

### 7.1 一个小型 Ontology 示例

假设有一个简单的电商系统，包含以下知识：

**代码模块结构：**
```
src/
├── auth/          # 认证模块
├── order/         # 订单模块
├── payment/       # 支付模块
└── product/       # 商品模块
```

**API 接口：**
```
POST /api/v1/auth/login        → 用户登录
POST /api/v1/order/create      → 创建订单
POST /api/v1/payment/pay       → 支付
GET  /api/v1/product/list      → 商品列表
```

**PRD 中的需求描述：**
"用户登录需要短信验证码。订单创建后进入支付流程。支付依赖订单信息。"

**构建后的数据：**

实体（6 条）：
```
mod:auth_module     | module     | 用户认证模块
mod:order_module    | module     | 订单管理模块
mod:payment_module  | module     | 支付模块
func:user_login     | function   | 用户登录功能
func:create_order   | function   | 创建订单功能
func:payment_process| function   | 支付处理功能
iface:sms_service   | interface  | 短信验证码服务
```

关系（6 条）：
```
func:user_login     → depends_on → iface:sms_service     | 登录需要短信验证码
func:user_login     → contains   → mod:auth_module       | 登录功能属于认证模块
func:create_order   → contains   → mod:order_module      | 创建订单属于订单模块
func:payment_process→ contains   → mod:payment_module    | 支付功能属于支付模块
mod:order_module    → depends_on → mod:auth_module       | 订单模块依赖认证模块
func:payment_process→ depends_on → func:create_order      | 支付依赖订单
```

---

## 8. 常见问题

### Q: 实体 ID 能否包含空格或特殊字符？
A: 不能。只允许小写字母、数字、下划线。空格用 `_` 代替。

### Q: 一个实体可以有多个类型吗？
A: 不能。每个实体只能有一个 type_id。如果需要多分类，使用 tags 字段。

### Q: 关系可以循环（A→B→A）吗？
A: 技术上允许，但查询时需要注意循环检测。可传递关系的递归查询需要设置深度限制。

### Q: 如何更新已有 Ontology？
A: 目前是完整替换模式。后续会支持增量更新。

### Q: 如何处理同一个实体在不同文档中的不同描述？
A: 合并描述信息，取置信度高的描述作为主要描述。

### Q: 构建时是否必须使用 LLM？
A: 不是必须的。代码模块结构、API 接口等可以通过静态分析自动提取，不需要 LLM。LLM 主要用于从非结构化 PRD 文档中抽取实体和关系。
