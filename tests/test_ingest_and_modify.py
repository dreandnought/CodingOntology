"""
集成测试：验证 ingest_document 和 modify_ontology 工具。

运行方式：
    python tests/test_ingest_and_modify.py

注意：本测试会调用 LLM API，请确保 llm_config.yaml 配置正确。
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.schema import init_db, get_connection
from models.entity import list_all_entities
from models.relation import get_entity_relations
from tools.ingest_document import register as register_ingest
from tools.modify_ontology import register as register_modify


def _seed_test_data(db_path):
    """插入少量测试数据。"""
    conn = get_connection(db_path)
    entities = [
        ("func:user_login", "function", "用户登录", "支持手机号或邮箱登录"),
        ("iface:sms_service", "interface", "短信验证码服务", "发送短信验证码"),
        ("mod:auth_module", "module", "认证模块", "处理登录注册"),
    ]
    for eid, etype, name, desc in entities:
        conn.execute(
            "INSERT OR IGNORE INTO entities (id, type_id, name, description, source) VALUES (?, ?, ?, ?, 'test')",
            (eid, etype, name, desc),
        )
    conn.commit()
    conn.close()


def _count_entities(db_path):
    conn = get_connection(db_path)
    row = conn.execute("SELECT COUNT(*) AS c FROM entities").fetchone()
    conn.close()
    return row["c"]


def _count_relations(db_path):
    conn = get_connection(db_path)
    row = conn.execute("SELECT COUNT(*) AS c FROM relations").fetchone()
    conn.close()
    return row["c"]


def main():
    print("=" * 60)
    print("PRD Ontology MCP - ingest_document / modify_ontology 测试")
    print("=" * 60)

    # 创建临时数据库
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    init_db(db_path)
    _seed_test_data(db_path)

    print(f"\n测试数据库: {db_path}")
    print(f"初始实体数: {_count_entities(db_path)}")
    print(f"初始关系数: {_count_relations(db_path)}")

    # 创建伪 MCP 对象，只提供 .tool() 装饰器
    class FakeMCP:
        def __init__(self):
            self.tools = {}

        def tool(self):
            def decorator(fn):
                self.tools[fn.__name__] = fn
                return fn
            return decorator

    fake_mcp = FakeMCP()
    register_ingest(fake_mcp)
    register_modify(fake_mcp)

    ingest_document = fake_mcp.tools["ingest_document"]
    modify_ontology = fake_mcp.tools["modify_ontology"]

    # 测试 ingest_document dry_run
    print("\n--- 测试 ingest_document (dry_run=true) ---")
    test_doc = """
# 登录模块增强

## 新增功能
1. 微信扫码登录：用户可以通过微信扫码快速登录系统。
2. 登录风控：检测异常登录行为并触发二次验证。

## 关系
- 微信扫码登录依赖微信 OAuth 接口
- 登录风控依赖用户登录行为日志
"""

    try:
        result = ingest_document(content=test_doc, title="登录模块增强 PRD", dry_run=True, db_path=db_path)
        plan = result["plan"]
        print(f"抽取实体数: {result['extraction_summary']['entities_extracted']}")
        print(f"抽取关系数: {result['extraction_summary']['relations_extracted']}")
        print(f"计划新建实体: {len(plan['entities']['create'])}")
        print(f"计划更新实体: {len(plan['entities']['update'])}")
        print(f"计划新建关系: {len(plan['relations']['create'])}")
        print(f"跳过关系: {len(plan.get('skipped_relations', []))}")
        for e in plan["entities"]["create"]:
            print(f"  新建: {e['entity_id']} | {e['name']} ({e['type']})")
        for e in plan["entities"]["update"]:
            print(f"  更新: {e['entity_id']} | {e['name']}")
    except Exception as e:
        print(f"❌ ingest_document dry_run 失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 测试 ingest_document 执行写入（使用 dry_run 返回的 plan，确保一致性）
    print("\n--- 测试 ingest_document (dry_run=false) ---")
    try:
        result = ingest_document(
            content=test_doc,
            title="登录模块增强 PRD",
            dry_run=False,
            plan=plan,
            db_path=db_path,
        )
        print(f"写入后实体数: {_count_entities(db_path)}")
        print(f"写入后关系数: {_count_relations(db_path)}")
        print(f"新建实体: {len(result['created_entities'])}")
        print(f"更新实体: {len(result['updated_entities'])}")
        print(f"新建关系: {len(result['created_relations'])}")
        print(f"文档 ID: {result['document']['id']}")
    except Exception as e:
        print(f"❌ ingest_document 执行写入失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 测试 modify_ontology dry_run
    print("\n--- 测试 modify_ontology (dry_run=true) ---")
    try:
        result = modify_ontology(
            description="把用户登录功能增加支持微信扫码登录，并添加与微信 OAuth 接口的依赖关系",
            target_entity_id="func:user_login",
            dry_run=True,
            db_path=db_path,
        )
        modify_plan = result["plan"]
        print(f"解释: {modify_plan.get('explanation', '')}")
        print(f"实体 create/update/delete: {len(modify_plan['entities']['create'])}/{len(modify_plan['entities']['update'])}/{len(modify_plan['entities']['delete'])}")
        print(f"关系 create/update/delete: {len(modify_plan['relations']['create'])}/{len(modify_plan['relations']['update'])}/{len(modify_plan['relations']['delete'])}")
        print(f"校验: valid={result['validation']['valid']}, errors={result['validation']['errors']}")
    except Exception as e:
        print(f"❌ modify_ontology dry_run 失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 测试 modify_ontology 执行写入（使用 dry_run 返回的 plan，确保一致性）
    print("\n--- 测试 modify_ontology (dry_run=false) ---")
    try:
        result = modify_ontology(
            description="把用户登录功能的描述更新为支持手机号、邮箱和微信扫码登录",
            target_entity_id="func:user_login",
            dry_run=False,
            plan=modify_plan,
            db_path=db_path,
        )
        print(f"成功: {result['success']}")
        print(f"新建实体: {len(result['created_entities'])}")
        print(f"更新实体: {len(result['updated_entities'])}")
        print(f"新建关系: {len(result['created_relations'])}")
        print(f"失败项: {len(result['failed_items'])}")
        if result["updated_entities"]:
            updated = result["updated_entities"][0]
            print(f"更新后描述: {updated.get('description', '')[:100]}")
    except Exception as e:
        print(f"❌ modify_ontology 执行写入失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 最终统计
    print("\n--- 最终统计 ---")
    print(f"实体数: {_count_entities(db_path)}")
    print(f"关系数: {_count_relations(db_path)}")

    # 查询用户登录的关系
    login_relations = get_entity_relations("func:user_login", db_path=db_path)
    print(f"func:user_login 的关系数: {len(login_relations)}")
    for r in login_relations:
        print(f"  {r['relation_type']} {r['direction']} {r['related_entity_id']}")

    # 清理
    try:
        os.remove(db_path)
    except Exception:
        pass

    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
