"""
插入示例数据到 Ontology 数据库，用于测试验证。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from models.schema import get_connection

SAMPLE_ENTITIES = [
    # 模块
    ("mod:auth_module", "module", "用户认证模块", "处理用户登录、注册、权限验证，是系统的核心模块"),
    ("mod:order_module", "module", "订单管理模块", "处理订单创建、查询、状态流转"),
    ("mod:payment_module", "module", "支付模块", "处理支付流程，对接第三方支付网关"),
    ("mod:product_module", "module", "商品模块", "商品信息管理、分类、搜索"),
    # 功能
    ("func:user_login", "function", "用户登录", "支持手机号或邮箱登录，需要短信验证"),
    ("func:user_register", "function", "用户注册", "新用户注册，需要手机号验证"),
    ("func:create_order", "function", "创建订单", "用户选择商品后创建订单"),
    ("func:payment_process", "function", "支付处理", "订单支付流程，支持微信和支付宝"),
    ("func:product_search", "function", "商品搜索", "按关键词搜索商品"),
    ("func:order_cancel", "function", "取消订单", "用户取消未支付的订单"),
    ("func:refund_process", "function", "退款处理", "订单退款流程"),
    # 接口
    ("iface:sms_service", "interface", "短信验证码服务", "发送短信验证码的第三方服务接口"),
    ("iface:wechat_pay", "interface", "微信支付接口", "对接微信支付的 API 接口"),
    ("iface:alipay", "interface", "支付宝接口", "对接支付宝的 API 接口"),
    ("iface:product_api", "interface", "商品查询 API", "商品信息查询接口"),
    # 数据实体
    ("data:user_table", "data_entity", "用户表", "存储用户账号信息的数据库表"),
    ("data:order_table", "data_entity", "订单表", "存储订单信息的数据库表"),
    ("data:product_table", "data_entity", "商品表", "存储商品信息的数据库表"),
    # 角色
    ("actor:normal_user", "actor", "普通用户", "普通注册用户，可使用购物、支付功能"),
    ("actor:admin", "actor", "管理员", "系统管理员，可管理商品和订单"),
    # 需求
    ("req:real_time_notification", "requirement", "实时通知", "订单状态变更需实时通知用户"),
    ("req:two_factor_auth", "requirement", "双因素认证", "管理员登录需要双因素认证"),
    ("req:payment_security", "requirement", "支付安全", "支付流程需符合 PCI DSS 安全标准"),
]

SAMPLE_RELATIONS = [
    # 依赖关系
    ("func:user_login", "depends_on", "iface:sms_service", 0.95, "登录需要短信验证码服务"),
    ("func:user_register", "depends_on", "iface:sms_service", 0.90, "注册需要短信验证"),
    ("func:create_order", "depends_on", "func:user_login", 0.85, "创建订单需要用户已登录"),
    ("func:payment_process", "depends_on", "func:create_order", 0.95, "支付依赖于已创建的订单"),
    ("func:payment_process", "depends_on", "iface:wechat_pay", 0.80, "支付调用微信支付接口"),
    ("func:payment_process", "depends_on", "iface:alipay", 0.80, "支付调用支付宝接口"),
    ("mod:order_module", "depends_on", "mod:auth_module", 0.90, "订单模块依赖认证模块"),
    ("mod:payment_module", "depends_on", "mod:order_module", 0.85, "支付模块依赖订单模块"),
    # 包含关系
    ("mod:auth_module", "contains", "func:user_login", 0.95, "登录功能属于认证模块"),
    ("mod:auth_module", "contains", "func:user_register", 0.95, "注册功能属于认证模块"),
    ("mod:order_module", "contains", "func:create_order", 0.95, "创建订单属于订单模块"),
    ("mod:order_module", "contains", "func:order_cancel", 0.90, "取消订单属于订单模块"),
    ("mod:payment_module", "contains", "func:payment_process", 0.95, "支付处理属于支付模块"),
    ("mod:payment_module", "contains", "func:refund_process", 0.85, "退款处理属于支付模块"),
    ("mod:product_module", "contains", "func:product_search", 0.90, "商品搜索属于商品模块"),
    # 影响关系
    ("func:user_login", "impacts", "func:create_order", 0.70, "登录失败会影响订单创建"),
    ("func:payment_process", "impacts", "req:payment_security", 0.85, "支付处理影响支付安全需求"),
    # 约束关系
    ("req:payment_security", "constrains", "func:payment_process", 0.90, "支付安全约束支付处理流程"),
    # 实现关系
    ("func:user_login", "implements", "req:two_factor_auth", 0.60, "登录功能部分实现双因素认证需求"),
]

def seed():
    conn = get_connection()
    
    # 插入实体
    for eid, etype, ename, edesc in SAMPLE_ENTITIES:
        conn.execute(
            "INSERT OR IGNORE INTO entities (id, type_id, name, description, confidence, source) VALUES (?, ?, ?, ?, 0.9, 'manual')",
            (eid, etype, ename, edesc),
        )
    
    # 插入关系
    for src, rtype, tgt, conf, desc in SAMPLE_RELATIONS:
        conn.execute(
            "INSERT OR IGNORE INTO relations (id, type_id, source_id, target_id, weight, confidence, source, metadata) VALUES (?, ?, ?, ?, 1.0, ?, 'manual', ?)",
            (f"{src}__{rtype}__{tgt}", rtype, src, tgt, conf, f'{{"description": "{desc}"}}'),
        )
    
    conn.commit()
    conn.close()
    
    print(f"✅ 已插入 {len(SAMPLE_ENTITIES)} 个实体, {len(SAMPLE_RELATIONS)} 条关系")
    
    # 统计
    conn = get_connection()
    counts = conn.execute(
        "SELECT 'entities' AS tbl, COUNT(*) FROM entities UNION ALL SELECT 'relations', COUNT(*) FROM relations"
    ).fetchall()
    conn.close()
    for row in counts:
        print(f"   {row['tbl']}: {row['COUNT(*)']}")

if __name__ == "__main__":
    seed()
