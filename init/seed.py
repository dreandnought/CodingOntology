"""
预设 Ontology 初始化脚本。

按 ONTOLOGY_BUILD_GUIDE.md 的协议构建预设 Ontology。
"""

from models.schema import init_db


def main():
    """初始化预设 Ontology 数据库。"""
    path = init_db()
    print(f"✅ Ontology 数据库已初始化: {path}")


if __name__ == "__main__":
    main()
