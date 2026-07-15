"""
MCP Tool: parse_prd

解析 PRD 文档，通过四阶段流水线（抽取 → 匹配+图搜索 → 推理 → 融合）返回增强版 PRD。
"""

from typing import Optional

from parser.llm_parser import parse_prd as _parse_prd


def register(mcp):
    """注册 parse_prd 工具到 MCP 服务器。"""

    @mcp.tool()
    def parse_prd(
        content: str,
        db_path: Optional[str] = None,
    ) -> dict:
        """**PRD 增广优化工具**：对用户输入的 PRD 文本进行本体知识驱动的增广优化。

        本工具是**只读分析**工具，不会修改本体数据库。它接收用户的一段 PRD（可能只有一两句话），
        通过四阶段流水线从本体中检索相关实体和关系，推理出原文未明示的依赖 / 约束 / 影响，
        **以结构化 Markdown 形式融合到 PRD 中**，输出 `enriched_prd` 字段。

        调用方 Agent 应把 `enriched_prd` **作为对用户 PRD 的优化版本**呈现给用户，
        让用户感受到"自己的需求被补全和增强了"，而不是看到一份陌生的新文档。

        ## 四阶段流水线（共 6 次 LLM 调用）

        1. **LLM 实体抽取** — 从 PRD 文本提取功能级实体（`[{name, type, description, search_keywords}]`）
        2. **语义匹配 + 图搜索** — 用 search_keywords 在本体中做 SQL LIKE 预筛 → LLM 语义匹配 →
           对匹配实体做 1 跳关系查询 + 传递 BFS（max_depth=2）→ 构建子图
        3. **LLM 推理** — 3 个并行 subagent 分别推理隐含依赖 / 约束 / 影响
        4. **LLM 融合** — 把推理结果以结构化 Markdown 形式融合回 PRD 原文

        ## Args

        - `content`: PRD 文档的 Markdown 或纯文本内容（**必填**）
        - `db_path`: 可选，Ontology SQLite 数据库路径（默认使用 ONTOLOGY_DB_PATH 环境变量或当前目录的 ontology.db）

        ## Returns

        - `enriched_prd`: **增强后的 PRD Markdown**，结构包含「原始需求 / 增强说明 / 隐含依赖 /
          约束条件 / 影响范围 / 增强后的完整需求」六个章节，是本工具的核心产物
        - `summary`: 解析摘要（含各阶段统计信息和 `pipeline_stages`）
        - `pipeline_trace`: 各阶段中间结果（用于调试和观测，非必要不展示给用户）
        """
        result = _parse_prd(content, db_path)
        return result

    return parse_prd
