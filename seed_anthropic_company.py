"""
种子脚本：从 test_data/anthropic-company/ 文档中抽取公司业务实体和关系。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from models.schema import get_connection

def seed_anthropic_company():
    conn = get_connection()
    
    # ===== 实体 =====
    
    # --- 公司主体 ---
    companies = [
        ("acomp:anthropic_inc", "actor", "Anthropic, Inc.", "Anthropic 公司，公益公司（Public Benefit Corporation），2021年成立，总部旧金山，CEO Dario Amodei"),
        ("acomp:openai", "actor", "OpenAI", "Anthropic 主要竞品，2015年成立，CEO Sam Altman，估值约$9000亿"),
        ("acomp:google_deepmind", "actor", "Google DeepMind", "Anthropic 竞品，Google 旗下 AI 研究机构"),
        ("acomp:meta_llama", "actor", "Meta LLaMA", "Meta 开源大语言模型系列"),
        ("acomp:softbank", "actor", "软银愿景基金", "Anthropic 主要投资方，持股约12%"),
        ("acomp:sequoia", "actor", "红杉资本", "Anthropic 主要投资方，持股约8%"),
        ("acomp:menlo_ventures", "actor", "Menlo Ventures", "Anthropic D轮领投方，持股约7%"),
        ("acomp:spark_capital", "actor", "Spark Capital", "Anthropic B轮领投方，持股约5%"),
        ("acomp:google_strategic", "actor", "Google（战略投资）", "Anthropic 最大战略投资方，持股约15%，含云计算合作"),
        ("acomp:goldman_sachs", "actor", "高盛", "Anthropic IPO 承销商"),
        ("acomp:morgan_stanley", "actor", "摩根士丹利", "Anthropic IPO 承销商"),
        ("acomp:jpmorgan", "actor", "摩根大通", "Anthropic IPO 承销商"),
    ]
    
    # --- 产品 ---
    products = [
        ("acomp:prod:claude_series", "function", "Claude 系列大模型", "Anthropic 旗舰大语言模型产品线，包括 Claude 1-5 各代版本"),
        ("acomp:prod:claude_4_sonnet", "function", "Claude 4 Sonnet", "中端主力商用模型，代码能力强，200K 上下文，约70B参数"),
        ("acomp:prod:claude_4_opus", "function", "Claude 4 Opus", "高端旗舰模型，推理能力强，200K 上下文，约200B MoE参数"),
        ("acomp:prod:claude_3_5_haiku", "function", "Claude 3.5 Haiku", "轻量快速模型，100K 上下文，约20B参数，适合端侧部署"),
        ("acomp:prod:claude_5_fable", "function", "Claude 5 Fable", "下一代旗舰模型（已下架），1M 上下文，约1T MoE参数"),
        ("acomp:prod:claude_code", "function", "Claude Code", "AI 辅助编程工具，2025年5月发布v1.0，支持项目级代码理解"),
        ("acomp:prod:claude_enterprise", "function", "Claude Enterprise", "企业级 AI 平台，支持知识库集成、安全审计、SSO"),
        ("acomp:prod:claude_api", "interface", "Anthropic API", "模型推理 API 服务，Messages/Streaming/Batch/Vision 等接口"),
        ("acomp:prod:mcp_protocol", "interface", "MCP 协议", "Model Context Protocol，Anthropic 推出的开放协议，连接 AI 与外部数据源"),
    ]
    
    # --- 核心技术 ---
    technologies = [
        ("acomp:tech:constitutional_ai", "constraint", "Constitutional AI", "宪法 AI 框架，确保模型行为符合伦理准则，约50条核心宪法准则"),
        ("acomp:tech:moe_architecture", "module", "MoE 架构", "Mixture-of-Experts 混合专家架构，Claude 4 Opus及以上使用，激活参数约30-40%"),
        ("acomp:tech:flash_attention_3", "module", "Flash Attention 3", "注意力机制优化，2-3x 推理加速"),
        ("acomp:tech:rlhf", "module", "RLHF 训练", "基于人类反馈的强化学习，对齐训练第三阶段"),
        ("acomp:tech:speculative_decoding", "module", "Speculative Decoding", "推测解码，2-4x 批量推理加速"),
        ("acomp:tech:adaptive_alibi", "module", "Adaptive ALiBi", "改进版 ALiBi 位置编码，支持长上下文"),
    ]
    
    # --- 数据实体 ---
    data_entities = [
        ("acomp:data:gpu_cluster", "data_entity", "GPU 算力集群", "约50万张GPU（H200/B200），分布在美国弗吉尼亚/俄勒冈/爱荷华和欧洲爱尔兰"),
        ("acomp:data:annual_revenue", "data_entity", "年化收入", "2026年Q2 ARR约$360亿，API服务占45%，企业版占25%"),
        ("acomp:data:funding_history", "data_entity", "融资历史", "种子轮到Pre-IPO共融资约$1050亿，最新Pre-IPO估值$1.2万亿"),
        ("acomp:data:ipo_info", "data_entity", "IPO 信息", "2026年Q4计划纳斯达克上市，股票代码ANTH，发行约$200亿"),
        ("acomp:data:competitor_market_share", "data_entity", "市场份额", "全球LLM市场：OpenAI 38%，Anthropic 28%，Google 15%，Meta 8%"),
    ]
    
    # --- 需求/业务目标 ---
    requirements = [
        ("acomp:req:safety_first", "requirement", "安全优先策略", "Constitutional AI 是其核心差异化优势，在金融/医疗等敏感行业有天然优势"),
        ("acomp:req:long_context", "requirement", "长上下文能力", "Claude 原生支持200K-1M token上下文窗口，领先竞品"),
        ("acomp:req:mcp_ecosystem", "requirement", "MCP 生态建设", "超过500个MCP服务器（2026年6月），连接企业数据源"),
        ("acomp:req:ipo_launch", "requirement", "IPO 上市", "2026年Q4纳斯达克上市，应对监管审查和Claude 5下架事件影响"),
    ]
    
    # --- 监管/约束 ---
    constraints = [
        ("acomp:con:claude_5_shutdown", "constraint", "Claude 5 下架事件", "2026年6月发布后72小时内因多国监管质疑主动下架"),
        ("acomp:con:china_market_ban", "constraint", "中国市场限制", "对华服务禁令导致失去全球最大AI市场之一"),
        ("acomp:con:gpu_supply_risk", "constraint", "GPU 供应链风险", "中美地缘政治影响GPU供应，年算力投入$100亿"),
        ("acomp:con:ipo_regulation", "constraint", "IPO 监管审查", "SEC审查和AI监管政策不确定性"),
    ]
    
    all_entities = companies + products + technologies + data_entities + requirements + constraints
    
    # 插入实体
    for eid, etype, ename, edesc in all_entities:
        conn.execute(
            "INSERT OR IGNORE INTO entities (id, type_id, name, description, confidence, source) VALUES (?, ?, ?, ?, 0.90, 'manual')",
            (eid, etype, ename, edesc),
        )
    
    # ===== 关系 =====
    relations = [
        # --- 产品包含关系 ---
        ("acomp:prod:claude_series", "contains", "acomp:prod:claude_4_sonnet", 0.95, "Claude 系列包含 4 Sonnet"),
        ("acomp:prod:claude_series", "contains", "acomp:prod:claude_4_opus", 0.95, "Claude 系列包含 4 Opus"),
        ("acomp:prod:claude_series", "contains", "acomp:prod:claude_3_5_haiku", 0.95, "Claude 系列包含 3.5 Haiku"),
        ("acomp:prod:claude_series", "contains", "acomp:prod:claude_5_fable", 0.90, "Claude 系列曾包含 5 Fable（已下架）"),
        ("acomp:prod:claude_series", "contains", "acomp:prod:claude_code", 0.85, "Claude Code 属于 Claude 产品矩阵"),
        ("acomp:prod:claude_series", "contains", "acomp:prod:claude_enterprise", 0.90, "Claude Enterprise 是 Claude 系列企业版"),
        ("acomp:prod:claude_series", "contains", "acomp:prod:claude_api", 0.95, "Anthropic API 提供 Claude 模型推理服务"),
        ("acomp:prod:claude_series", "contains", "acomp:prod:mcp_protocol", 0.80, "MCP 协议是 Claude 生态的重要组成部分"),
        
        # --- 产品依赖技术 ---
        ("acomp:prod:claude_4_opus", "depends_on", "acomp:tech:moe_architecture", 0.95, "Claude 4 Opus 使用 MoE 架构"),
        ("acomp:prod:claude_5_fable", "depends_on", "acomp:tech:moe_architecture", 0.95, "Claude 5 Fable 使用 MoE 架构"),
        ("acomp:prod:claude_series", "depends_on", "acomp:tech:constitutional_ai", 0.95, "所有 Claude 模型使用 Constitutional AI"),
        ("acomp:prod:claude_series", "depends_on", "acomp:tech:flash_attention_3", 0.90, "Claude 模型使用 Flash Attention 3 优化"),
        ("acomp:prod:claude_series", "depends_on", "acomp:tech:adaptive_alibi", 0.90, "Claude 模型使用 Adaptive ALiBi 位置编码"),
        ("acomp:prod:claude_series", "depends_on", "acomp:tech:rlhf", 0.90, "Claude 模型经过 RLHF 对齐训练"),
        ("acomp:prod:claude_api", "depends_on", "acomp:tech:speculative_decoding", 0.80, "API 推理使用 Speculative Decoding 加速"),
        
        # --- 公司/产品影响关系 ---
        ("acomp:prod:claude_5_fable", "impacts", "acomp:req:ipo_launch", 0.85, "Claude 5 下架加速了 IPO 进程"),
        ("acomp:con:claude_5_shutdown", "impacts", "acomp:req:ipo_launch", 0.90, "Claude 5 下架事件促使提前上市应对监管"),
        ("acomp:con:gpu_supply_risk", "impacts", "acomp:prod:claude_series", 0.80, "GPU 供应链风险影响模型训练和推理"),
        ("acomp:con:china_market_ban", "impacts", "acomp:data:annual_revenue", 0.70, "中国市场限制影响收入增长"),
        
        # --- 竞争关系 ---
        ("acomp:anthropic_inc", "relates_to", "acomp:openai", 0.80, "Anthropic 核心竞品：OpenAI（市场份额 38% vs 28%）"),
        ("acomp:anthropic_inc", "relates_to", "acomp:google_deepmind", 0.70, "Anthropic 竞品：Google DeepMind（市场份额 15%）"),
        ("acomp:anthropic_inc", "relates_to", "acomp:meta_llama", 0.60, "Anthropic 竞品：Meta LLaMA 开源路线"),
        ("acomp:prod:claude_code", "relates_to", "acomp:prod:claude_series", 0.85, "Claude Code 基于 Claude 模型"),
        
        # --- 投资关系 ---
        ("acomp:google_strategic", "relates_to", "acomp:anthropic_inc", 0.85, "Google 是 Anthropic 最大战略投资方（15%）"),
        ("acomp:softbank", "relates_to", "acomp:anthropic_inc", 0.80, "软银是 Anthropic F轮投资方（12%）"),
        ("acomp:sequoia", "relates_to", "acomp:anthropic_inc", 0.75, "红杉资本是 Anthropic 投资方（8%）"),
        ("acomp:menlo_ventures", "relates_to", "acomp:anthropic_inc", 0.75, "Menlo Ventures 是 Anthropic D轮领投方（7%）"),
        
        # --- 约束关系 ---
        ("acomp:con:claude_5_shutdown", "constrains", "acomp:prod:claude_5_fable", 0.95, "监管导致 Claude 5 下架"),
        ("acomp:con:china_market_ban", "constrains", "acomp:anthropic_inc", 0.80, "中国禁令约束市场拓展"),
        ("acomp:con:gpu_supply_risk", "constrains", "acomp:data:gpu_cluster", 0.90, "GPU 供应链约束算力扩展"),
        ("acomp:con:ipo_regulation", "constrains", "acomp:req:ipo_launch", 0.85, "监管审查约束 IPO 进程"),
        
        # --- 需求实现 ---
        ("acomp:tech:constitutional_ai", "implements", "acomp:req:safety_first", 0.95, "Constitutional AI 实现安全优先策略"),
        ("acomp:prod:claude_series", "implements", "acomp:req:long_context", 0.95, "Claude 系列实现长上下文能力"),
        ("acomp:prod:mcp_protocol", "implements", "acomp:req:mcp_ecosystem", 0.95, "MCP 协议实现生态建设"),
        ("acomp:data:ipo_info", "implements", "acomp:req:ipo_launch", 0.90, "IPO 信息支持上市进程"),
        
        # --- 数据实体关联 ---
        ("acomp:data:gpu_cluster", "relates_to", "acomp:prod:claude_series", 0.90, "GPU 集群支撑 Claude 模型训练和推理"),
        ("acomp:data:annual_revenue", "relates_to", "acomp:anthropic_inc", 0.95, "年化收入反映公司经营状况"),
        ("acomp:data:funding_history", "relates_to", "acomp:anthropic_inc", 0.95, "融资历史反映公司资本进程"),
        ("acomp:data:competitor_market_share", "relates_to", "acomp:openai", 0.80, "市场份额数据反映竞争格局"),
    ]
    
    # 插入关系
    for src, rtype, tgt, conf, desc in relations:
        conn.execute(
            "INSERT OR IGNORE INTO relations (id, type_id, source_id, target_id, weight, confidence, source, metadata) VALUES (?, ?, ?, ?, 1.0, ?, 'manual', ?)",
            (f"{src}__{rtype}__{tgt}", rtype, src, tgt, conf, f'{{"description": "{desc}"}}'),
        )
    
    conn.commit()
    conn.close()
    
    # 统计
    conn = get_connection()
    total_entities = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
    total_relations = conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0]
    ac_entities = conn.execute("SELECT COUNT(*) FROM entities WHERE id LIKE 'acomp:%'").fetchone()[0]
    ac_relations = conn.execute("SELECT COUNT(*) FROM relations WHERE id LIKE 'acomp:%'").fetchone()[0]
    conn.close()
    
    print(f"✅ Anthropic 公司本体数据已写入")
    print(f"   数据库总计: {total_entities} 实体, {total_relations} 关系")
    print(f"   Anthropic 公司: {ac_entities} 实体, {ac_relations} 关系")

if __name__ == "__main__":
    seed_anthropic_company()
