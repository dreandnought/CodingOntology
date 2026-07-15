"""
MCP Tool: parse_prd

解析 PRD 文档，抽取第一层实体，在预设 Ontology 中匹配并查询关系，返回增强版 PRD。
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
        """解析 PRD 文档，抽取实体并在预设 Ontology 中匹配关系，返回增强版 PRD。

        Args:
            content: PRD 文档的 Markdown 或纯文本内容
            db_path: 可选，Ontology SQLite 数据库路径（默认使用 ONTOLOGY_DB_PATH 环境变量或当前目录的 ontology.db）

        Returns:
            enriched_prd: 增强后的 PRD Markdown（末尾追加了关系附录）
            summary: 解析摘要信息
        """
        result = _parse_prd(content, db_path)
        return result

    return parse_prd
