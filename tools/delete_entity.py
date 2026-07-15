"""
MCP Tool: delete_ontology_entity

根据实体 ID 或名称直接删除 Ontology 中的实体及其关联关系。
"""

from typing import Optional

from models.entity import delete_entity, entity_exists, get_entity, get_entity_by_name


def register(mcp):
    """注册 delete_ontology_entity 工具到 MCP 服务器。"""

    @mcp.tool()
    def delete_ontology_entity(
        entity_id: Optional[str] = None,
        entity_name: Optional[str] = None,
        db_path: Optional[str] = None,
    ) -> dict:
        """根据实体 ID 或名称删除 Ontology 实体及其所有关联关系。

        Args:
            entity_id: 实体 ID（优先使用）
            entity_name: 实体名称（当 entity_id 未提供时使用）
            db_path: 可选，Ontology SQLite 数据库路径

        Returns:
            {"success": bool, "deleted_entity_id": str or None, "message": str}
        """
        target_id = entity_id

        if not target_id and entity_name:
            entity = get_entity_by_name(entity_name, db_path)
            if entity:
                target_id = entity["id"]

        if not target_id:
            return {
                "success": False,
                "deleted_entity_id": None,
                "message": "必须提供 entity_id 或 entity_name",
            }

        if not entity_exists(target_id, db_path):
            return {
                "success": False,
                "deleted_entity_id": target_id,
                "message": f"实体不存在: {target_id}",
            }

        deleted = delete_entity(target_id, db_path)
        if deleted:
            return {
                "success": True,
                "deleted_entity_id": target_id,
                "message": f"已删除实体 {target_id} 及其关联关系",
            }

        return {
            "success": False,
            "deleted_entity_id": target_id,
            "message": f"删除实体 {target_id} 失败",
        }

    return delete_ontology_entity
