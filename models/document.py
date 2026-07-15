"""
Document CRUD 操作。
"""

import hashlib
import re

from .schema import get_connection


def hash_content(content: str) -> str:
    """计算内容哈希（取 SHA-256 前 16 位）。"""
    if content is None:
        content = ""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


def _slugify(title: str) -> str:
    """将标题转换为 URL-safe 的短 slug。"""
    slug = re.sub(r"[^\w\u4e00-\u9fff]+", "_", title).strip("_").lower()[:32]
    return slug or "doc"


def create_document(
    title,
    doc_type="ingest",
    content=None,
    file_path=None,
    url=None,
    db_path=None,
):
    """创建文档记录并返回文档信息。"""
    doc_hash = hash_content(content)
    word_count = len(content.split()) if content else 0
    base_id = f"doc:{_slugify(title)}"

    conn = get_connection(db_path)
    counter = 2
    doc_id = base_id
    while conn.execute("SELECT 1 FROM documents WHERE id = ?", (doc_id,)).fetchone():
        doc_id = f"{base_id}_{counter}"
        counter += 1

    conn.execute(
        """
        INSERT INTO documents (
            id, title, doc_type, url, file_path, content_hash, word_count,
            status, created_at, parsed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'parsed', datetime('now'), datetime('now'))
        """,
        (doc_id, title, doc_type, url, file_path, doc_hash, word_count),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM documents WHERE id = ?", (doc_id,)).fetchone()
    conn.close()
    return dict(row)


def get_document(doc_id, db_path=None):
    """按 ID 查询文档。"""
    conn = get_connection(db_path)
    row = conn.execute("SELECT * FROM documents WHERE id = ?", (doc_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
