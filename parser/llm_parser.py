"""
LLM 驱动的 PRD/文档解析器。

职责：
1. 从文本/Markdown 中抽取实体和关系
2. 将实体与预设 Ontology 进行语义匹配
3. 根据自然语言描述生成本体变更计划
4. 生成增强版 PRD（Markdown 附录格式）

注意：当前为验证阶段，不引入向量模型，使用纯 LLM 语义匹配。
"""

import json
import os
import re
import yaml
from typing import Optional


# 从 llm_config.yaml 加载 LLM 配置
_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "llm_config.yaml")


def _load_llm_config():
    """加载 llm_config.yaml 配置（每次调用都重新读取，支持热更新）。"""
    if os.path.exists(_CONFIG_PATH):
        with open(_CONFIG_PATH, encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        provider_name = cfg.get("default_provider", "siliconflow")
        provider = cfg.get("providers", {}).get(provider_name, {})
        parser_cfg = cfg.get("prd_parser", {})
        return {
            "api_key": provider.get("api_key", ""),
            "base_url": provider.get("base_url", ""),
            "model": provider.get("models", {}).get("chat", ""),
            "temperature": parser_cfg.get("temperature", 0.1),
            "max_tokens": parser_cfg.get("max_tokens", 4096),
        }
    return None


def _chat_url(base_url: str) -> str:
    """根据 base_url 构造 chat completions URL，保留用户指定的显式路径。"""
    if not base_url:
        return base_url
    from urllib.parse import urlparse

    path = urlparse(base_url).path.rstrip("/")
    if path.endswith("/chat/completions"):
        return base_url
    return base_url.rstrip("/") + "/chat/completions"


def _call_llm(system_prompt: str, user_prompt: str, temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> Optional[str]:
    """调用 LLM API（每次调用都重新读取配置）。"""
    import requests

    cfg = _load_llm_config()
    if cfg:
        api_url = _chat_url(cfg["base_url"])
        api_key = cfg["api_key"]
        model = cfg["model"]
        temp = temperature if temperature is not None else cfg.get("temperature", 0.1)
        max_tok = max_tokens if max_tokens is not None else cfg.get("max_tokens", 4096)
    else:
        api_url = os.environ.get(
            "LLM_API_URL", "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        )
        api_key = os.environ.get("ARK_API_KEY", os.environ.get("LLM_API_KEY", ""))
        model = os.environ.get("ARK_MODEL_ID", os.environ.get("LLM_MODEL", "doubao-seed-2.0-code"))
        temp = temperature if temperature is not None else 0.1
        max_tok = max_tokens if max_tokens is not None else 4096

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temp,
        "max_tokens": max_tok,
    }

    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"LLM API call failed: {e}")


def _build_ontology_context(db_path=None) -> str:
    """构建 Ontology 上下文字符串（供 LLM 匹配使用）。"""
    from models.schema import get_connection

    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT e.id, e.name, et.name AS type_name, e.description "
        "FROM entities e JOIN entity_types et ON e.type_id = et.id "
        "WHERE e.status = 'active' "
        "ORDER BY e.type_id, e.name"
    ).fetchall()
    conn.close()

    if not rows:
        return "（当前 Ontology 中暂无实体）"

    lines = []
    for r in rows:
        desc = r["description"] or ""
        lines.append(f"- {r['id']} | {r['name']} ({r['type_name']}) | {desc[:80]}")
    return "\n".join(lines)


def _extract_json_blocks(text: str) -> list:
    """从文本中提取所有 ```json ... ``` 代码块内容。"""
    return re.findall(r"```json\n(.*?)\n```", text, re.DOTALL)


def _first_json_block(text: str):
    """提取并解析第一个 JSON 代码块。"""
    blocks = _extract_json_blocks(text)
    if blocks:
        try:
            return json.loads(blocks[0])
        except json.JSONDecodeError:
            pass
    # 兜底：尝试直接解析整个文本中的 JSON
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return None


def extract_entities_and_relations(content: str, db_path=None) -> dict:
    """从文本/Markdown 中抽取实体和关系，并尝试与已有 Ontology 实体匹配。

    返回结构：
    {
        "entities": [
            {
                "name": "用户登录",
                "type": "function",
                "description": "...",
                "suggested_id": "func:user_login",
                "matched_entity_id": null,
                "confidence": 0.0,
                "is_new": true
            }
        ],
        "relations": [
            {
                "source_name": "用户登录",
                "source_id": "func:user_login",
                "relation_type": "depends_on",
                "target_name": "短信验证码",
                "target_id": "iface:sms_service",
                "description": "...",
                "confidence": 0.9
            }
        ]
    }
    """
    ontology_context = _build_ontology_context(db_path)

    system_prompt = """你是一个本体知识抽取专家。你的任务是从用户提供的文本或 Markdown 文档中抽取功能级实体和它们之间的关系，并与已有 Ontology 进行匹配。

请严格按以下 JSON 格式返回结果（只返回一个 JSON 代码块，不要额外解释）：

```json
{
  "entities": [
    {
      "name": "用户登录",
      "type": "function",
      "description": "用户通过手机号或邮箱登录系统",
      "suggested_id": "func:user_login",
      "matched_entity_id": null,
      "confidence": 0.0,
      "is_new": true
    }
  ],
  "relations": [
    {
      "source_name": "用户登录",
      "source_id": "func:user_login",
      "relation_type": "depends_on",
      "target_name": "短信验证码",
      "target_id": "iface:sms_service",
      "description": "登录需要短信验证码",
      "confidence": 0.9
    }
  ]
}
```

规则：
1. 实体类型仅限：requirement、function、module、interface、data_entity、test_case、constraint、actor。
2. suggested_id 规范：使用"类型前缀:英文小写slug"，例如 function→func:xxx、module→mod:xxx、interface→iface:xxx、data_entity→data:xxx、actor→actor:xxx、requirement→req:xxx、constraint→constraint:xxx、test_case→test:xxx。
3. 若某实体与"当前 Ontology 中的已知实体"明显是同一个，则填写 matched_entity_id 为已有实体的 id，is_new=false，confidence 为 0.5-1.0；否则 matched_entity_id 为 null，is_new=true。
4. relation_type 仅限：depends_on、causes、constrains、impacts、conflicts_with、derived_from、implements、contains、refines、relates_to。
5. 关系两端的 source_id/target_id 优先使用已有实体的 ID；若目标为新实体，则使用 suggested_id。
6. 只抽取文本中明确提到、有较高置信度的实体和关系，不要过度推断。"""

    user_prompt = f"""## 当前 Ontology 中的已知实体
{ontology_context}

## 待分析的文本/文档
{content}

请抽取实体和关系，并返回严格 JSON。"""

    llm_response = _call_llm(system_prompt, user_prompt, temperature=0.1, max_tokens=4096)
    parsed = _first_json_block(llm_response)

    if not isinstance(parsed, dict):
        raise RuntimeError("LLM 返回的 JSON 格式不正确，无法解析实体和关系")

    entities = parsed.get("entities", []) if isinstance(parsed.get("entities"), list) else []
    relations = parsed.get("relations", []) if isinstance(parsed.get("relations"), list) else []

    # 基本校验与清洗
    valid_types = {"requirement", "function", "module", "interface", "data_entity", "test_case", "constraint", "actor"}
    cleaned_entities = []
    for e in entities:
        if not isinstance(e, dict):
            continue
        etype = e.get("type", "")
        if etype not in valid_types:
            continue
        cleaned_entities.append({
            "name": str(e.get("name", "")).strip(),
            "type": etype,
            "description": str(e.get("description", "")).strip(),
            "suggested_id": str(e.get("suggested_id", "")).strip() or None,
            "matched_entity_id": e.get("matched_entity_id") or None,
            "confidence": float(e.get("confidence", 0.8)),
            "is_new": bool(e.get("is_new", True)),
        })

    valid_relation_types = {"depends_on", "causes", "constrains", "impacts", "conflicts_with", "derived_from", "implements", "contains", "refines", "relates_to"}
    cleaned_relations = []
    for r in relations:
        if not isinstance(r, dict):
            continue
        rtype = r.get("relation_type", "")
        if rtype not in valid_relation_types:
            continue
        cleaned_relations.append({
            "source_name": str(r.get("source_name", "")).strip(),
            "source_id": str(r.get("source_id", "")).strip() or None,
            "relation_type": rtype,
            "target_name": str(r.get("target_name", "")).strip(),
            "target_id": str(r.get("target_id", "")).strip() or None,
            "description": str(r.get("description", "")).strip(),
            "confidence": float(r.get("confidence", 0.8)),
        })

    return {
        "entities": cleaned_entities,
        "relations": cleaned_relations,
    }


def plan_ontology_changes(
    description: str,
    target_entity_id: Optional[str] = None,
    target_entity_context: Optional[str] = None,
    db_path=None,
) -> dict:
    """根据自然语言描述生成本体变更计划。

    返回结构：
    {
        "entities": {"create": [...], "update": [...], "delete": [...]},
        "relations": {"create": [...], "update": [...], "delete": [...]},
        "explanation": "..."
    }
    """
    ontology_context = _build_ontology_context(db_path)

    system_prompt = """你是一个本体知识库维护专家。用户会用自然语言描述他希望对 Ontology 进行的修改，你的任务是生成一份结构化的变更计划。

请严格按以下 JSON 格式返回结果（只返回一个 JSON 代码块，不要额外解释）：

```json
{
  "entities": {
    "create": [
      {"suggested_id": "func:wechat_login", "name": "微信登录", "type": "function", "description": "..."}
    ],
    "update": [
      {"entity_id": "func:user_login", "name": "用户登录", "description": "更新后的描述"}
    ],
    "delete": [
      {"entity_id": "func:old_feature"}
    ]
  },
  "relations": {
    "create": [
      {"source_id": "func:user_login", "relation_type": "depends_on", "target_id": "iface:sms_service", "description": "..."}
    ],
    "update": [
      {"relation_id": "depends_on:func:user_login->iface:sms_service", "description": "..."}
    ],
    "delete": [
      {"relation_id": "..."}
    ]
  },
  "explanation": "简要说明变更原因"
}
```

规则：
1. 实体类型仅限：requirement、function、module、interface、data_entity、test_case、constraint、actor。
2. 新增实体的 suggested_id 使用"类型前缀:英文小写slug"格式。
3. relation_type 仅限：depends_on、causes、constrains、impacts、conflicts_with、derived_from、implements、contains、refines、relates_to。
4. 若用户描述不够明确，宁可少改也不要过度推断；delete 操作要特别谨慎。
5. 若未提供目标实体 ID，由你自行判断要修改哪些实体。"""

    target_hint = ""
    if target_entity_id:
        target_hint = f"\n优先修改的目标实体 ID：{target_entity_id}\n"
    if target_entity_context:
        target_hint += f"目标实体上下文：\n{target_entity_context}\n"

    user_prompt = f"""## 当前 Ontology 中的已知实体
{ontology_context}
{target_hint}
## 用户的修改描述
{description}

请生成变更计划，返回严格 JSON。"""

    llm_response = _call_llm(system_prompt, user_prompt, temperature=0.2, max_tokens=4096)
    parsed = _first_json_block(llm_response)

    if not isinstance(parsed, dict):
        raise RuntimeError("LLM 返回的 JSON 格式不正确，无法解析变更计划")

    # 规范化结构
    entities = parsed.get("entities", {})
    relations = parsed.get("relations", {})
    if not isinstance(entities, dict):
        entities = {}
    if not isinstance(relations, dict):
        relations = {}

    return {
        "entities": {
            "create": entities.get("create", []) if isinstance(entities.get("create"), list) else [],
            "update": entities.get("update", []) if isinstance(entities.get("update"), list) else [],
            "delete": entities.get("delete", []) if isinstance(entities.get("delete"), list) else [],
        },
        "relations": {
            "create": relations.get("create", []) if isinstance(relations.get("create"), list) else [],
            "update": relations.get("update", []) if isinstance(relations.get("update"), list) else [],
            "delete": relations.get("delete", []) if isinstance(relations.get("delete"), list) else [],
        },
        "explanation": str(parsed.get("explanation", "")).strip(),
    }


def parse_prd(content: str, db_path=None) -> dict:
    """解析 PRD 并返回增强版 PRD（关系信息融合到正文中）和摘要信息。"""
    ontology_context = _build_ontology_context(db_path)

    system_prompt = """你是一个 PRD 需求分析专家。你的任务是从 PRD 文档中抽取功能级实体，与预设知识图谱进行匹配，并将匹配到的关系信息**融合**到 PRD 原文中，最后以 Markdown 格式输出增强后的 PRD。

## 工作流程

### 步骤 1：抽取实体
从 PRD 中抽取功能级实体（功能、模块、接口、需求、约束等），返回 JSON。

### 步骤 2：匹配 Ontology
将每个实体映射到预设 Ontology 中最匹配的实体，返回 JSON。

### 步骤 3：融合增强（核心）
将匹配到的关系信息**直接融合到 PRD 正文**中，而非追加附录。融合方式如下：

**融合规则（按优先级）：**

1. **依赖注入**：如果某个实体有依赖关系，在其首次出现的描述中插入关联信息。
   - 例：原文"用户登录功能" → "用户登录功能（依赖短信验证码服务）"
   - 例："订单模块" → "订单模块（依赖用户认证模块进行权限验证）"

2. **影响标注**：如果某个实体的修改会影响其他模块，在该模块描述中标注影响范围。
   - 例："支付处理功能" → "支付处理功能（影响支付安全需求，需符合 PCI DSS 标准）"

3. **约束提示**：如果某个实体受约束限制，在其描述中插入约束信息。
   - 例："API 查询" → "API 查询（受 Feature Gate 约束，默认关闭）"

4. **包含关系**：如果实体属于某个模块，标注其所属模块。
   - 例："用户登录" → "用户登录（属于用户认证模块）"

**融合原则：**
- 只插入**可验证**的关系信息（即 Ontology 中确实存在的关系）
- 插入信息用（）括起来，保持原文完整性
- 不要过度插入，每个实体最多标注 1-2 个关键关系
- 对于 PRD 中未明确提到的实体关系，即使 Ontology 中有也**不**插入
- 保留原文的所有内容和结构，只在关键位置添加标注

### 步骤 4：输出最终增强版 PRD

先输出步骤 1 和 2 的 JSON 块，然后输出完整的增强版 PRD Markdown。

```json
[
  {"name": "用户登录", "type": "function", "description": "..."}
]
```

```json
[
  {"prd_entity": "用户登录", "matched_entity_id": "func:user_login", "confidence": 0.95}
]
```

然后输出完整增强版 PRD，末尾不需要再追加关系附录。"""

    user_prompt = f"""## 当前 Ontology 中的已知实体
{ontology_context}

## PRD 文档内容
{content}

请完成四步分析：抽取实体 → 匹配 Ontology → 融合关系到正文 → 输出增强版 PRD。"""

    llm_response = _call_llm(system_prompt, user_prompt)

    # 解析 LLM 返回的 JSON 块（步骤 1 和 2）
    json_blocks = _extract_json_blocks(llm_response)

    # 统计信息
    summary = {
        "entities_extracted": 0,
        "entities_matched": 0,
        "relations_found": 0,
        "new_entities_added": 0,
        "enhancement_mode": "fused",  # fused=融合到正文, appended=追加附录
    }

    if json_blocks:
        try:
            extracted = json.loads(json_blocks[0])
            if isinstance(extracted, list):
                summary["entities_extracted"] = len(extracted)
        except (json.JSONDecodeError, IndexError):
            pass

    if len(json_blocks) > 1:
        try:
            matches = json.loads(json_blocks[1])
            if isinstance(matches, list):
                summary["entities_matched"] = sum(
                    1 for m in matches if m.get("match")
                )
                summary["new_entities_added"] = sum(
                    1 for m in matches if not m.get("match")
                )
        except (json.JSONDecodeError, IndexError):
            pass

    # 从 LLM 响应中提取增强版 PRD（去掉 JSON 块后剩余的内容即为增强版 PRD）
    enriched_prd = llm_response
    # 去掉所有 ```json ... ``` 块，剩下的就是增强版 PRD
    cleaned = re.sub(r"```json\n.*?\n```", "", llm_response, flags=re.DOTALL).strip()
    if cleaned:
        enriched_prd = cleaned

    # 统计关系数量——从增强版 PRD 中数包含 () 标注的条数
    relation_annotations = re.findall(r"（[^）]*依赖[^）]*）|[^）]*影响[^）]*）|[^）]*属于[^）]*）|[^）]*约束[^）]*）", enriched_prd)
    summary["relations_found"] = len(relation_annotations)

    return {
        "enriched_prd": enriched_prd,
        "summary": summary,
    }
