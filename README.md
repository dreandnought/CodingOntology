# PRD Ontology MCP

为 Coding Agent（Claude Code、Cline 等）提供 PRD 增强理解的 MCP 插件。

通过将 PRD 中的实体和隐性关系建模为显式 Ontology 图，让 Agent 不仅能"读"PRD，更能"理解"其中的因果链、约束关系、依赖网络。

## 快速开始

### 环境要求

- **Python** >= 3.10
- 网络连接（需要访问 LLM API）

### 1. 安装依赖

```bash
cd prd-ontology-mcp
pip install fastmcp requests pyyaml
```

### 2. 配置 LLM API

编辑 `llm_config.yaml`，填入有效的 API Key：

```yaml
default_provider: siliconflow

providers:
  siliconflow:
    api_key: "sk-your-api-key-here"       # 替换为你的 Key
    base_url: "https://api.siliconflow.cn/v1"
    models:
      chat: "deepseek-ai/DeepSeek-V4-Flash"   # 或 deepseek-ai/DeepSeek-V4-Pro

  # 也可配置其他兼容 OpenAI 协议的提供商
  openai:
    api_key: ""
    base_url: "https://api.openai.com/v1"
    models:
      chat: "gpt-4o"
```

> **注意**：`llm_config.yaml` 在生产环境中会明文存储 API Key。由于此 MCP Server 部署在局域网供团队共用，这是可接受的方案。如果需要更高安全性，可通过环境变量 `LLM_API_KEY`、`LLM_API_URL`、`LLM_MODEL` 覆盖配置。

### 3. 验证配置

```bash
python3 -c "
from parser.llm_parser import parse_prd
result = parse_prd('# 测试\nGateway 模块负责消息路由和配置管理。')
print('实体:', result['summary']['entities_extracted'])
print('匹配:', result['summary']['entities_matched'])
"
```

看到类似输出即表示配置正确：

```
实体: 3
匹配: 3
```

### 4. 启动 MCP Server

```bash
python3 server.py
```

默认以 stdio 模式运行，等待 Coding Agent 通过标准输入/输出通信。

## 接入 Coding Agent

### 接入 Claude Code

```bash
# 添加 MCP Server（从项目目录执行）
claude mcp add prd-ontology \
  -- python /absolute/path/to/prd-ontology-mcp/server.py
```

### 接入 Cline / Cursor

在 MCP 配置文件中添加：

```json
{
  "mcpServers": {
    "prd-ontology": {
      "command": "python3",
      "args": ["/absolute/path/to/prd-ontology-mcp/server.py"]
    }
  }
}
```

配置后，Coding Agent 将能使用以下工具：

| 工具 | 说明 |
|------|------|
| `parse_prd` | 解析 PRD 文档，抽取实体并匹配 Ontology 关系，返回增强版 PRD（只读，不修改数据库） |
| `query_ontology` | 查询 Ontology 中的实体和关系（按名称/ID/关键词） |
| `ingest_document` | 从文本/Markdown 文档抽取实体和关系，写入 Ontology 数据库 |
| `modify_ontology` | 根据自然语言描述修改已有 Ontology（增/删/改实体和关系） |
| `delete_ontology_entity` | 根据实体 ID 或名称直接删除实体及其所有关联关系 |

## Trae Skills（推荐用法）

项目已在 `.trae/skills/` 下封装了 4 个 Skill，Coding Agent 可直接根据意图调用对应 Skill，自动完成与 MCP 的交互。

| Skill | 触发场景 | 对应 MCP 工具 |
|-------|---------|--------------|
| `query-ontology` | 用户想查询某个实体、查看关系或搜索本体知识库 | `query_ontology` |
| `parse-prd` | 用户输入 PRD 或需求文档，希望利用本体知识完善它 | `parse_prd` |
| `ingest-document` | 用户输入一段文字/Markdown，要求提取实体和关系并写入本体 | `ingest_document` |
| `delete-ontology-entity` | 用户要求删除本体中的某个实体及其关系 | `delete_ontology_entity` |

Skill 文件位于：

- `.trae/skills/query-ontology/SKILL.md`
- `.trae/skills/parse-prd/SKILL.md`
- `.trae/skills/ingest-document/SKILL.md`
- `.trae/skills/delete-ontology-entity/SKILL.md`

每个 SKILL.md 中详细说明了参数、调用示例和返回值。Agent 识别到对应意图时，优先使用 Skill 中描述的工具和参数模板，无需手动拼装复杂 JSON。

## 使用示例

### 1. 解析 PRD（只读，不修改数据库）

向 Agent 发送类似指令：

```
请用 parse_prd 工具分析以下 PRD：

# 用户登录系统
## 功能需求
1. 用户可以通过手机号或邮箱登录
2. 登录需要短信验证码验证
3. 登录失败超过5次将锁定账号30分钟
```

Agent 会调用 `parse_prd` 工具，返回增强版 PRD（含关系附录）。

### 2. 从文档中抽取新知识并写入本体

```
请使用 ingest_document 工具将以下文档中的实体和关系摄入本体数据库：

# 支付模块
## 功能
1. 支持微信支付和支付宝支付
2. 支付前必须完成实名认证
3. 支付完成后发送短信通知

先 dry_run=true 预览变更计划，确认后再 dry_run=false 执行写入。
```

Agent 会先调用 `ingest_document(dry_run=true)` 返回变更计划，经你确认后再调用 `ingest_document(dry_run=false)` 写入数据库。

### 3. 用自然语言修改已有本体

```
请使用 modify_ontology 工具：把"用户登录"实体的描述更新为支持手机号、邮箱和微信扫码登录，并添加"用户登录"依赖"微信 OAuth 接口"的关系。

target_entity_id 为 func:user_login，先 dry_run=true 预览，确认后再执行。
```

Agent 会先调用 `modify_ontology(dry_run=true)` 返回变更计划，确认后再执行。

### 4. 查询 Ontology

```
查询 Gateway 模块的依赖关系
```

Agent 会调用 `query_ontology` 返回实体信息和关联关系。

## 本体数据库

当前数据库包含 **179 个实体** 和 **181 条关系**，覆盖三个领域：

| 领域 | 实体数 | 来源 |
|:----|:------:|:----|
| OpenClaw 平台 | 66 | AGENTS.md, SOUL.md, TOOLS.md 等 |
| CCB (Claude Code) | 73 | test_data/claude-code-*.md |
| Anthropic 公司 | 40 | test_data/anthropic-company/*.md |

## 项目结构

```
prd-ontology-mcp/
├── server.py                 # MCP Server 入口
├── llm_config.yaml           # LLM API 配置
├── requirements.txt          # 依赖
├── DEVELOPMENT.md            # 开发文档
├── ONTOLOGY_BUILD_GUIDE.md   # Ontology 构建协议文档
├── ontology.db               # 本体数据库
├── models/                   # 数据模型层
│   ├── schema.py             # SQLite 表定义
│   ├── entity.py             # 实体 CRUD
│   ├── relation.py           # 关系 CRUD
│   └── document.py           # 来源文档 CRUD
├── parser/
│   └── llm_parser.py         # LLM 驱动的 PRD/文档解析器
├── tools/
│   ├── parse_prd.py          # parse_prd MCP 工具
│   ├── query_ontology.py     # query_ontology MCP 工具
│   ├── ingest_document.py    # ingest_document MCP 工具
│   └── modify_ontology.py    # modify_ontology MCP 工具
├── tests/
│   └── test_ingest_and_modify.py  # 新工具集成测试
├── storage/
│   └── connection.py         # SQLite 连接管理
├── init/
│   ├── seed.py               # 数据库初始化
│   └── seed_sample.py        # 示例数据
├── seed_openclaw.py          # OpenClaw 平台本体种子
├── seed_anthropic_company.py # Anthropic 公司本体种子
└── test_data/                # 测试文档
    └── anthropic-company/    # Anthropic 公司文档
```

## 扩展本体

要给数据库添加新的领域知识，参考 `seed_openclaw.py` 或 `seed_anthropic_company.py` 的写法：

```python
from models.schema import get_connection

def seed_new_domain():
    conn = get_connection()
    
    # 实体列表：[id, type_id, name, description]
    entities = [
        ("prefix:entity_id", "function", "实体名称", "实体描述"),
    ]
    for eid, etype, ename, edesc in entities:
        conn.execute(
            "INSERT OR IGNORE INTO entities (id, type_id, name, description, confidence, source) VALUES (?, ?, ?, ?, 0.90, 'manual')",
            (eid, etype, ename, edesc),
        )
    
    # 关系列表：[source_id, type_id, target_id, confidence, description]
    relations = [
        ("source_id", "depends_on", "target_id", 0.95, "关系描述"),
    ]
    for src, rtype, tgt, conf, desc in relations:
        conn.execute(
            "INSERT OR IGNORE INTO relations (id, type_id, source_id, target_id, weight, confidence, source, metadata) VALUES (?, ?, ?, ?, 1.0, ?, 'manual', ?)",
            (f"{src}__{rtype}__{tgt}", rtype, src, tgt, conf, f'{{"description": "{desc}"}}'),
        )
    
    conn.commit()
    conn.close()
```

也可用更详细的 Skill 文档：详见 `skills/prd-ontology-seeder/SKILL.md`。

## 迁移到新机器

将本 MCP Server 迁移到其他机器（如新的服务器或团队成员电脑）的完整步骤：

### 步骤 1：复制项目

```bash
# 方式一：直接复制目录
scp -r prd-ontology-mcp user@new-machine:/path/to/

# 方式二：使用 git（推荐）
cd prd-ontology-mcp
git init
git add .
git commit -m "init"
git remote add origin <your-repo-url>
git push
# 然后在目标机器 clone
```

### 步骤 2：安装依赖

```bash
cd /path/to/prd-ontology-mcp

# 安装 Python 依赖
pip install fastmcp requests pyyaml
```

> 如果目标机器没有 Python 3，先安装：
> ```bash
> # Ubuntu/Debian
> sudo apt update && sudo apt install python3 python3-pip -y
>
> # macOS (Homebrew)
> brew install python@3.11
> ```

### 步骤 3：配置 LLM API

```bash
# 编辑配置文件，填入你的 API Key
vim llm_config.yaml
```

**或者使用环境变量（可避免 Key 写在文件中）：**

```bash
export LLM_API_KEY="sk-your-key"
export LLM_API_URL="https://api.siliconflow.cn/v1/chat/completions"
export LLM_MODEL="deepseek-ai/DeepSeek-V4-Flash"
```

如果使用环境变量，`llm_config.yaml` 可保留默认配置（代码会优先读取环境变量）。

### 步骤 4：验证安装

```bash
python3 -c "
from models.schema import get_connection
conn = get_connection()
count = conn.execute('SELECT COUNT(*) FROM entities').fetchone()[0]
print(f'✅ 本体数据库就绪，包含 {count} 个实体')
"

python3 -c "
from parser.llm_parser import parse_prd
result = parse_prd('# 测试\nGateway 模块负责消息路由。')
print(f'✅ LLM API 配置正确')
print(f'   实体: {result[\"summary\"][\"entities_extracted\"]}')
print(f'   匹配: {result[\"summary\"][\"entities_matched\"]}')
"
```

### 步骤 5：接入 Coding Agent

在目标机器上配置 Coding Agent 连接此 MCP Server：

```bash
# Claude Code
claude mcp add prd-ontology -- python /path/to/prd-ontology-mcp/server.py

# Cline / Cursor
# 编辑 MCP 配置文件，添加上述 json 配置
```

### 步骤 6（可选）：更新本体数据库

如果需要在新机器上重建或更新本体数据库：

```bash
cd /path/to/prd-ontology-mcp

# 如果是从零开始，先初始化数据库
python3 -c "from models.schema import init_db; init_db()"

# 运行种子脚本填充数据
python3 seed_openclaw.py
python3 seed_anthropic_company.py
```

### 完整迁移脚本

```bash
#!/bin/bash
# migrate_prd_ontology.sh - 在新机器上一键部署 PRD Ontology MCP

set -e

PROJECT_DIR="$HOME/prd-ontology-mcp"

echo "=== PRD Ontology MCP 迁移脚本 ==="

# 1. 克隆项目
echo "[1/5] 克隆项目..."
git clone <your-repo-url> "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 2. 安装依赖
echo "[2/5] 安装 Python 依赖..."
pip install fastmcp requests pyyaml

# 3. 配置环境变量
echo "[3/5] 请设置 LLM API 配置..."
read -p "API Key (留空则从 llm_config.yaml 读取): " api_key
if [ -n "$api_key" ]; then
    export LLM_API_KEY="$api_key"
    echo "  已设置环境变量 LLM_API_KEY"
fi

# 4. 验证
echo "[4/5] 验证安装..."
python3 -c "from models.schema import get_connection; c=get_connection(); print(f'✅ 数据库就绪，{c.execute(\"SELECT COUNT(*) FROM entities\").fetchone()[0]} 个实体')"

# 5. 输出接入命令
echo "[5/5] 完成！接入命令："
echo "  claude mcp add prd-ontology -- python $PROJECT_DIR/server.py"

## MCP 工具详细说明

为了让 Coding Agent 准确选择工具，下面对四个工具的使用场景、参数和返回值进行详细说明。

### 工具选择速查

| 你的意图 | 应使用的工具 | 是否修改数据库 |
|---------|-------------|--------------|
| 分析/增强一份 PRD，查看其中实体和关系 | `parse_prd` | 否 |
| 查询已有本体中的实体或关系 | `query_ontology` | 否 |
| 从文档/文本中抽取新知识并写入本体 | `ingest_document` | 是 |
| 用自然语言修改、删除或新增本体内容 | `modify_ontology` | 是 |

### `parse_prd` —— PRD 分析与增强（只读）

**适用场景**：你有一份 PRD 或 Markdown 文档，希望快速了解其中包含哪些功能/模块/接口实体，以及它们与已有 Ontology 的匹配关系。

**参数**：
- `content`（必填）：PRD 文本或 Markdown 内容
- `db_path`（可选）：自定义 SQLite 数据库路径

**返回值**：
```json
{
  "enriched_prd": "增强后的 Markdown 文本",
  "summary": {
    "entities_extracted": 3,
    "entities_matched": 2,
    "relations_found": 1,
    "new_entities_added": 1
  }
}
```

**注意**：`parse_prd` **不会修改数据库**，适合在正式写入前做快速分析。

### `ingest_document` —— 文档摄入（写入数据库）

**适用场景**：你从外部文档、会议记录、聊天记录或任意文本中发现了新知识，希望把这些知识结构化后写入 Ontology 数据库，并尝试与已有实体建立关系。

**参数**：
- `content`（必填）：文本或 Markdown 文档内容
- `title`（可选）：文档标题，用于溯源
- `dry_run`（默认 `true`）：`true` 只返回变更计划，`false` 执行写入
- `plan`（可选）：传入上一次 `dry_run=true` 返回的 `plan`，避免 LLM 两次调用结果不一致
- `db_path`（可选）：自定义 SQLite 数据库路径

**dry_run=true 返回值**：
```json
{
  "dry_run": true,
  "plan": {
    "entities": {"create": [...], "update": [...], "delete": []},
    "relations": {"create": [...], "update": [], "delete": []},
    "skipped_relations": []
  },
  "extraction_summary": {
    "entities_extracted": 3,
    "relations_extracted": 2
  }
}
```

**dry_run=false 返回值**：
```json
{
  "dry_run": false,
  "document": {"id": "doc:xxx", "title": "..."},
  "created_entities": [...],
  "updated_entities": [...],
  "created_relations": [...],
  "skipped_relations": []
}
```

**合并策略**：若抽取到的实体与已有实体同名或 LLM 判断为同一实体，则更新已有实体描述；否则创建新实体。

### `modify_ontology` —— 自然语言修改本体（写入数据库）

**适用场景**：你已经有一个 Ontology，想根据自然语言指令修改、删除或新增其中的实体和关系。例如："把用户登录的描述更新为支持微信扫码"、"删除过时的支付接口"、"添加 A 依赖 B 的关系"。

**参数**：
- `description`（必填）：自然语言描述
- `target_entity_id`（可选）：优先修改的目标实体 ID
- `dry_run`（默认 `true`）：`true` 只返回变更计划，`false` 执行写入
- `plan`（可选）：传入上一次 `dry_run=true` 返回的 `plan`，避免 LLM 两次调用结果不一致
- `db_path`（可选）：自定义 SQLite 数据库路径

**dry_run=true 返回值**：
```json
{
  "dry_run": true,
  "plan": {
    "entities": {"create": [...], "update": [...], "delete": [...]},
    "relations": {"create": [...], "update": [...], "delete": [...]},
    "explanation": "变更原因说明"
  },
  "validation": {"valid": true, "errors": []}
}
```

**dry_run=false 返回值**：
```json
{
  "dry_run": false,
  "success": true,
  "created_entities": [...],
  "updated_entities": [...],
  "deleted_entities": [...],
  "created_relations": [...],
  "updated_relations": [...],
  "deleted_relations": [...],
  "failed_items": []
}
```

### `query_ontology` —— 查询本体（只读）

**适用场景**：查询已有 Ontology 中的实体和关系。

**参数**：
- `entity_name`：按实体名称查询
- `entity_id`：按实体 ID 查询（优先于 `entity_name`）
- `query`：关键词搜索
- `relation_types`：筛选关系类型，如 `["depends_on", "impacts"]`
- `limit`：搜索结果条数限制
- `db_path`（可选）：自定义 SQLite 数据库路径

**返回值**：
```json
{
  "entity": {...},
  "relations": [...],
  "search_results": [...]
}
```
