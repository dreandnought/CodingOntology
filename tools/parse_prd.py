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
        """解析 PRD 文档，通过四阶段流水线返回增强版 PRD（只读，不修改数据库）。

        四阶段流水线：
        1. LLM 实体抽取 — 从 PRD 文本提取功能级实体
        2. 语义匹配 + 图搜索 — 在本体中模糊匹配实体，BFS 遍历关系表获取子图
        3. LLM 推理 — 3 个并行 subagent 推理隐含依赖/约束/影响
        4. LLM 融合 — 将推理结果融合回 PRD 原文

        Args:
            content: PRD 文档的 Markdown 或纯文本内容
            db_path: 可选，Ontology SQLite 数据库路径（默认使用 ONTOLOGY_DB_PATH 环境变量或当前目录的 ontology.db）

        Returns:
            enriched_prd: 增强后的 PRD Markdown（推理结果已融合到正文中）
            summary: 解析摘要（含各阶段统计信息和 pipeline_stages）
            pipeline_trace: 各阶段中间结果（用于调试和观测）
        """
        result = _parse_prd(content, db_path)
        return result

    return parse_prd
