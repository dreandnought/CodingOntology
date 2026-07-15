---
name: "parse-prd"
description: "对用户输入的 PRD 文本进行**本体知识驱动的增广优化**。当用户提到「完善 PRD」「优化 PRD」「增广 PRD」「分析需求文档」「根据本体知识补全需求」「让 PRD 更完善」「PRD 增强」「补充隐含依赖/约束/影响」时必须调用本 skill。"
---

# parse-prd：PRD 增广优化

## 这个工具在做什么

**核心心智模型**：把用户输入的一段 PRD（可能只有一两句话）当作"种子需求"，通过四阶段流水线从本体中检索相关实体 / 关系，推理出原文**未明示**的依赖、约束、影响，以结构化 Markdown 形式**补全和增强**用户的原始 PRD。

调用方 Agent 拿到结果后应**把 `enriched_prd` 当作"对用户 PRD 的优化版"**呈现给用户，让用户感受到"自己的需求被补全和增强了"，而不是看到一份陌生的新文档。

> ⚠️ 本工具是**只读分析**，不会修改本体数据库。

---

## 触发条件

满足以下任一情况时，**必须**调用 `parse_prd`：

- 用户提供一段 PRD 文本 / Markdown / 几句话，并希望"完善 / 优化 / 增广"它
- 用户说"帮我完善这份 PRD"、"优化一下这个需求"、"补充隐含的依赖/约束/影响"
- 用户希望对简短需求做"展开 + 知识补全"
- 收到一份新需求，需要快速理解它在已有体系中的位置和影响

---

## MCP 工具

- **工具名**：`parse_prd`
- **参数**：
  - `content`（必填）：PRD 的 Markdown 或纯文本内容
  - `db_path`（可选）：数据库路径，通常不传

### 用法示例

```json
{
  "name": "parse_prd",
  "arguments": {
    "content": "对ccb项目增加linux平台上的屏幕操控功能"
  }
}
```

---

## 返回值

```json
{
  "enriched_prd": "# 增强版 PRD：...\n\n## 原始需求\n> ...\n\n## 增强说明\n...\n\n## 隐含依赖\n- **...**：...\n\n## 约束条件\n- **...**：...\n\n## 影响范围\n- **...**：...\n\n## 增强后的完整需求\n...",
  "summary": {
    "entities_extracted": 1,
    "entities_matched": 1,
    "relations_found": 3,
    "inferences": {"dependencies": 2, "constraints": 1, "impacts": 2},
    "enhancement_mode": "fused",
    "pipeline_stages": ["extract", "match", "reason", "fuse"]
  },
  "pipeline_trace": {
    "stage1_entities": [...],
    "stage2_matches": [...],
    "stage2_subgraph": {"entities": [...], "relations": [...]},
    "stage3_inferences": {"dependencies": [...], "constraints": [...], "impacts": [...]}
  }
}
```

| 字段 | 含义 | 是否展示给用户 |
|------|------|---------------|
| `enriched_prd` | **增强后的 PRD Markdown**（核心产物，6 章节结构化） | ✅ **必须展示** |
| `summary` | 解析摘要：抽取/匹配/关系/推理数 | ⚪ 可选（简短说明"补全了 N 条隐含依赖"） |
| `pipeline_trace` | 各阶段中间结果（实体、匹配、子图、推理） | ❌ 仅调试用，不展示 |

### `enriched_prd` 的 6 章节结构

| 章节 | 内容 | 作用 |
|------|------|------|
| `# 增强版 PRD：...` | 一句话标题 | 标识这是优化版 |
| `## 原始需求` | 用户原文（引用块） | 保留用户输入，让用户对照 |
| `## 增强说明` | 2~3 句说明基于哪些本体知识 | 让用户理解增强来源 |
| `## 隐含依赖` | 列表 + 加粗，附证据 | 补全用户没写出的依赖 |
| `## 约束条件` | 列表 + 加粗，附证据 | 补全隐含约束 |
| `## 影响范围` | 列表 + 加粗，附证据 | 告知会影响到哪些模块 |
| `## 增强后的完整需求` | 自然融合后的完整 Markdown | 给用户"可直接使用"的版本 |

---

## 四阶段流水线

共 **6 次 LLM 调用**（抽取 1 + 匹配 1 + 推理 3 并行 + 融合 1）：

```
用户 PRD 原文
   │
   ▼
[1] LLM 实体抽取 ────────────────► prd_entities[]
   │                                ↓
   │                          search_keywords 做 SQL LIKE 预筛
   ▼                                ↓
[2] 语义匹配 + 图搜索  ──► LLM 批量语义匹配 ──► 匹配实体
                              │              ↓
                              │         1 跳 + 传递 BFS（max_depth=2）
                              ▼              ↓
                            matched subgraph{entities, relations}
                              │              ↓
                              ▼              ↓
[3] LLM 推理（3 subagent 并行） ──► dependencies/constraints/impacts
                              │
                              ▼
[4] LLM 融合 ──► enriched_prd（6 章节结构化 Markdown）
```

### 阶段 1：LLM 实体抽取
- **输入**：PRD 原文
- **输出**：`[{name, type, description, search_keywords}]`
- **温度**：0.1

### 阶段 2：语义匹配 + 图搜索
- **Step 2a**：SQL LIKE 预筛（`name LIKE` / `description LIKE`，每关键词 top 5）
- **Step 2b**：1 次 LLM 批量语义匹配（阈值 0.5）
- **Step 2c**：1 跳关系查询 + 传递 BFS（`depends_on` / `contains` / `derived_from`，max_depth=2）

### 阶段 3：LLM 推理（3 个并行 subagent）

| Subagent | 角色 | 推理目标 | 温度 |
|----------|------|---------|------|
| A | 依赖推理 | 隐含依赖（子图未直接显示但可推断） | 0.1 |
| B | 约束推理 | 隐含约束条件 | 0.1 |
| C | 影响推理 | 变更会影响到哪些已有模块 | 0.1 |

### 阶段 4：LLM 融合（结构化输出）
- **输入**：PRD 原文 + 推理结果 + 子图
- **输出**：6 章节结构化 Markdown
- **温度**：0.7（更具创造性）
- **最大 tokens**：8192

---

## 调用方 Agent 的呈现规范

### ✅ 推荐做法

1. **直接展示 `enriched_prd` 全文**，让用户看到结构化增强版
2. **简短附一句**："基于本体知识补全了 N 条隐含依赖、M 条约束、K 条影响范围"
3. **如有需要**，可单独强调某条关键信息（例："⚠️ 此变更将影响 CCB Computer Use 模块"）

### ❌ 不要做

- 不要把 `pipeline_trace` 整段贴给用户（信息噪音大）
- 不要把 `enriched_prd` 改写成自然语言散文（会丢失结构）
- 不要把 6 章节拆开分别回复（破坏整体性）
- 不要把增强信息当作"工具的猜测"加免责声明（会让用户觉得不可靠）

### 典型回复模板

```
已完成 PRD 增广优化，基于本体知识补全了 2 条隐含依赖、1 条约束、2 条影响范围。

<enriched_prd 完整内容>
```

---

## 增强模式：fused（深度融合）

| 旧模式（已废弃） | 新模式（fused） |
|---------------|---------------|
| 在原文后追加"## 关系分析"附录 | 推理结果融入原文，形成 6 章节结构化文档 |
| 信息与正文分离 | 原始需求 / 增强说明 / 分类列表 / 融合后正文，层次清晰 |
| 难以复用 | 每章节独立可被 Agent 抽取和引用 |

---

## 端到端测试用例

**输入**：`"对ccb项目增加linux平台上的屏幕操控功能"`

**summary**：

```json
{
  "entities_extracted": 1,
  "entities_matched": 1,
  "relations_found": 3,
  "inferences": {"dependencies": 2, "constraints": 1, "impacts": 2},
  "enhancement_mode": "fused",
  "pipeline_stages": ["extract", "match", "reason", "fuse"]
}
```

**enriched_prd 片段**：

```markdown
# 增强版 PRD：为 ccb 项目增加 Linux 平台上的屏幕操控功能

## 原始需求
> 对ccb项目增加linux平台上的屏幕操控功能

## 增强说明
基于 CCB 本体知识（`computer_use` 模块、`screen_control` 功能、`bash_execution` 依赖）进行增广，识别出 2 条隐含依赖、1 条约束、2 条影响范围。

## 隐含依赖
- **CCB Computer Use 模块**：作为跨平台屏幕操控的基础平台，需复用其截图/键鼠/剪贴板基础设施
- **Bash 执行模块**：底层终端命令操作依赖 Bash 执行

## 约束条件
- **Linux 键鼠模拟协议**：必须同时支持 X11 和 Wayland 两种显示协议

## 影响范围
- **CCB Computer Use 模块**：需扩展其 Linux 适配器
- **Bash 执行模块**：需确保与屏幕操控的接口兼容

## 增强后的完整需求
对 ccb 项目增加 Linux 平台上的屏幕操控功能，**该功能属于 CCB Computer Use 跨平台屏幕操控模块**……
```

---

## 前置条件

调用本工具前，确保：

1. **本体数据库非空**：`ontology.db` 中至少存在与 PRD 相关的实体和关系，否则阶段 2 会匹配失败
2. **LLM 配置正确**：`llm_config.yaml` 中 `default_provider` / `api_key` / `base_url` / `model` 正确
3. **依赖工具就绪**：`models/entity.py` 的 `search_entities`、`get_entities_by_ids` 和 `models/relation.py` 的 `get_entity_relations`、`get_transitive_relations` 可用

---

## 与其他 skill 的协作

### 上游（构建本体）

| Skill | 用途 |
|-------|------|
| `prd-ontology-seeder` | 把领域文档写入本体，构建 `ontology.db` 中的实体和关系 |
| `ingest-document` | 把零散文本/说明加入本体 |
| `query-ontology` | 查询本体中的实体和关系（可用于诊断） |

### 下游（使用增强结果）

| Skill | 用途 |
|-------|------|
| `prd-writer` | 拿到 `enriched_prd` 后做人工润色/改写为面向终端用户的产品文档 |

---

## 注意事项

- **只读分析**：本工具**不会**修改本体数据库
- **配置可热更新**：`llm_config.yaml` 每次调用都重新读取，无需重启服务
- **失败重试**：每个 LLM 调用有 `max_retries=3` 的指数退避重试（1s/2s/4s）
- **可观测性**：`pipeline_trace` 字段直接用于调试和观测各阶段中间结果
- **匹配阈值可调**：在 `llm_config.yaml` 的 `prd_parser.extraction.entity_confidence_threshold` 中调整（默认 0.5）
