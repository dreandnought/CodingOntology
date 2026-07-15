"""
MCP Tool: query_ontology

查询 Ontology 中的实体和关系。
支持三种查询方式：
A. 按实体名称查询
B. 按实体 ID 查询
C. 关键词搜索
"""

from typing import Optional, List

from models.entity import get_entity, get_entity_by_name, search_entities
from models.relation import get_entity_relations


def register(mcp):
    """注册 query_ontology 工具到 MCP 服务器。"""

    @mcp.tool()
    def query_ontology(
        entity_name: Optional[str] = None,
        entity_id: Optional[str] = None,
        query: Optional[str] = None,
        relation_types: Optional[List[str]] = None,
        limit: int = 10,
        db_path: Optional[str] = None,
    ) -> dict:
        """查询 Ontology 中的实体和关系。

        支持三种查询方式：
        A. 按实体名称查询（entity_name）
        B. 按实体 ID 查询（entity_id）
        C. 关键词搜索（query）

        Args:
            entity_name: 按实体名称查询
            entity_id: 按实体 ID 查询（优先于 entity_name）
            query: 关键词搜索
            relation_types: 可选，筛选关系类型，如 ["depends_on", "impacts"]
            limit: 搜索结果的条数限制（仅对方案 C 有效）
            db_path: 可选，Ontology SQLite 数据库路径

        Returns:
            entity: 实体信息
            relations: 关联关系列表
            search_results: 搜索匹配的实体列表（仅方案 C）
        """
        entity = None
        relations = []
        search_results = []

        if entity_id:
            # 方案 B：按 ID 查询
            entity = get_entity(entity_id, db_path)
            if entity:
                relations = get_entity_relations(entity_id, relation_types, db_path)

        elif entity_name:
            # 方案 A：按名称查询
            entity = get_entity_by_name(entity_name, db_path)
            if entity:
                relations = get_entity_relations(
                    entity["id"], relation_types, db_path
                )

        elif query:
            # 方案 C：关键词搜索
            matches = search_entities(query, limit, db_path)
            for e in matches:
                entity_relations = get_entity_relations(
                    e["id"], relation_types, db_path
                )
                search_results.append(
                    {
                        "entity": e,
                        "relations": entity_relations,
                    }
                )

        return {
            "entity": entity,
            "relations": relations,
            "search_results": search_results,
        }

    return query_ontology
