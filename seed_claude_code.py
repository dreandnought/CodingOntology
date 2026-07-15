"""
种子脚本：基于 Claude Code CCB 项目文档构建本体数据。
从 test_data/ 下的文档中抽取实体和关系，写入 ontology.db。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from models.schema import get_connection

def seed_claude_code_ontology():
    conn = get_connection()
    
    # ===== 实体 =====
    
    # --- 模块/子系统 ---
    modules = [
        ("ccb:mod:cli_entry", "module", "CCB CLI Entry", "CLI 入口层，cli.tsx → main.tsx，处理快速路径和子命令分发"),
        ("ccb:mod:query_engine", "module", "CCB Query Engine", "核心查询引擎，管理会话状态、压缩、消息轮次和 API 查询"),
        ("ccb:mod:tool_system", "module", "CCB Tool System", "Tool 注册和管理系统，54+ 工具，含 BashTool、FileEditTool、GrepTool、AgentTool 等"),
        ("ccb:mod:provider_layer", "module", "CCB Provider Layer", "LLM 提供商适配层，支持 Anthropic、OpenAI、Bedrock、Vertex 等多提供商"),
        ("ccb:mod:ui_layer", "module", "CCB UI Layer", "终端 UI 层，基于 React/Ink 框架，含 170+ 组件和自定义 reconciler"),
        ("ccb:mod:state_management", "module", "CCB State Management", "状态管理系统，AppState + Zustand store + 模块级单例"),
        ("ccb:mod:bridge_remote", "module", "CCB Bridge/Remote", "远程控制和 Bridge 模式，feature-gated，含 JWT 认证和消息传输"),
        ("ccb:mod:daemon_mode", "module", "CCB Daemon Mode", "守护进程模式，长驻 supervisor 和 worker 管理"),
        ("ccb:mod:feature_flag", "module", "CCB Feature Flag", "功能开关系统，通过 bun:bundle feature() 和环境变量控制"),
        ("ccb:mod:auth_system", "module", "CCB Auth System", "认证系统，支持 7 种认证方式，含 OAuth 服务"),
        ("ccb:mod:session_storage", "module", "CCB Session Storage", "会话存储，JSONL 格式，5106 行实现"),
        ("ccb:mod:mcp_system", "module", "CCB MCP System", "MCP 客户端系统，管理 MCP 服务器连接和工具注册"),
        ("ccb:mod:context_system", "module", "CCB Context System", "上下文构建系统，组装 Git 状态、CLAUDE.md、记忆等上下文"),
        ("ccb:mod:computer_use", "module", "CCB Computer Use", "跨平台屏幕操控系统，截图/键鼠/剪贴板/应用管理"),
        ("ccb:mod:voice_mode", "module", "CCB Voice Mode", "语音模式，Push-to-Talk 语音输入，WebSocket 流式 STT"),
        ("ccb:mod:openai_compat", "module", "CCB OpenAI 兼容层", "OpenAI 协议兼容层，支持 Ollama/DeepSeek/vLLM 等端点"),
        ("ccb:mod:memory_system_ccb", "module", "CCB Memory System", "记忆系统，含 MemoryStore、MemoryRecall、MemoryExtract 等"),
        ("ccb:mod:permission_system", "module", "CCB Permission System", "权限系统，8 种权限模式，AI 自动分类和规则管线"),
        ("ccb:mod:telemetry", "module", "CCB Telemetry", "遥测/诊断系统，OTel 日志、GrowthBook A/B 测试、Datadog"),
        ("ccb:mod:config_management_ccb", "module", "CCB Config Management", "配置管理，7 层优先级合并：user→project→local→policy→flag→command→session"),
        ("ccb:mod:ink_framework", "module", "CCB Ink Framework", "自定义 Ink 框架，含 reconciler、hooks、keybinding、vim 模拟、typeahead"),
        ("ccb:mod:shell_execution", "module", "CCB Shell Execution", "Shell 执行层，统一 bash/zsh/PowerShell 接口"),
        ("ccb:mod:agent_tools", "module", "CCB Agent Tools", "Agent 工具库，54 个工具实现，含 Sandbox 沙盒系统"),
    ]
    
    # --- 核心功能 ---
    functions = [
        ("ccb:func:query_api", "function", "API 查询", "发送消息到 LLM API，处理流式响应和工具调用"),
        ("ccb:func:tool_dispatch_ccb", "function", "工具调度", "解析和执行工具调用，54+ 工具的条件加载"),
        ("ccb:func:repl_interaction", "function", "REPL 交互", "交互式 REPL 界面，处理用户输入、消息显示和快捷键"),
        ("ccb:func:headless_pipe", "function", "Headless/Pipe 模式", "非交互式管道模式，JSON 输出"),
        ("ccb:func:feature_check", "function", "Feature Flag 检查", "通过 bun:bundle feature() 检查功能是否启用"),
        ("ccb:func:subcommand_dispatch", "function", "子命令分发", "处理 51 个子命令的路由和 action handler"),
        ("ccb:func:session_compaction", "function", "会话压缩", "管理会话上下文的压缩和 Token 预算跟踪"),
        ("ccb:func:provider_switch", "function", "提供商切换", "在 Anthropic/OpenAI/Bedrock/Vertex 等提供商间切换"),
        ("ccb:func:stream_adapter", "function", "流适配", "将不同提供商的 SSE/WS 流统一为内部事件格式"),
        ("ccb:func:auth_credential", "function", "认证凭据管理", "管理 API Key、OAuth Token 等认证凭据"),
        ("ccb:func:mcp_client", "function", "MCP 客户端", "管理和连接 MCP 服务器"),
        ("ccb:func:context_assembly", "function", "上下文组装", "组装 Git 状态、CLAUDE.md、记忆等上下文信息"),
        ("ccb:func:screen_control", "function", "屏幕操控", "跨平台截图、键鼠模拟和应用管理（Computer Use）"),
        ("ccb:func:voice_stt", "function", "语音识别", "WebSocket 流式语音识别（STT）"),
        ("ccb:func:openai_adapter", "function", "OpenAI 协议适配", "将 Anthropic 格式请求转为 OpenAI 格式"),
        ("ccb:func:memory_recall", "function", "记忆检索", "相关性检索和记忆提取"),
        ("ccb:func:permission_check", "function", "权限检查", "8 种权限模式的规则检查和 AI 自动分类"),
        ("ccb:func:settings_merge", "function", "配置合并", "7 层优先级配置合并：user→project→local→policy→flag→command→session"),
        ("ccb:func:code_analysis", "function", "代码分析", "代码搜索、文件编辑、Git 状态等开发工具"),
        ("ccb:func:bash_execution", "function", "Bash 执行", "在终端中执行 bash 命令并获取输出"),
        ("ccb:func:daemon_supervisor", "function", "守护进程管理", "管理长驻守护进程和 worker 注册"),
        ("ccb:func:telemetry_collect", "function", "遥测收集", "收集和分析使用数据、性能指标"),
        ("ccb:func:subagent_fork", "function", "子 Agent 分叉", "创建和管理子 Agent 会话"),
    ]
    
    # --- 接口 ---
    interfaces = [
        ("ccb:iface:anthropic_api", "interface", "Anthropic API", "Anthropic Messages API，流式 SDK 端点"),
        ("ccb:iface:openai_api", "interface", "OpenAI API", "OpenAI Chat Completions API 协议"),
        ("ccb:iface:aws_bedrock", "interface", "AWS Bedrock", "AWS Bedrock IAM 认证的 LLM 服务"),
        ("ccb:iface:gcp_vertex", "interface", "GCP Vertex", "Google Cloud Vertex AI 服务"),
        ("ccb:iface:azure_openai", "interface", "Azure OpenAI", "Azure OpenAI 服务"),
        ("ccb:iface:anthropic_oauth", "interface", "Anthropic OAuth", "Anthropic OAuth 认证服务"),
        ("ccb:iface:growthbook_api", "interface", "GrowthBook API", "A/B 测试和 Feature Flag 服务"),
        ("ccb:iface:datadog_api", "interface", "Datadog API", "Datadog 日志上传服务"),
        ("ccb:iface:github_api", "interface", "GitHub API", "GitHub 仓库和代码管理 API"),
    ]
    
    # --- 数据实体 ---
    data_entities = [
        ("ccb:data:app_state", "data_entity", "AppState", "中心应用状态类型，包含消息、工具、权限、MCP 连接等 7+ 个域"),
        ("ccb:data:session_jsonl", "data_entity", "Session JSONL", "会话存储 JSONL 文件，5106 行实现"),
        ("ccb:data:config_file_ccb", "data_entity", "配置文件", "7 层优先级配置（user→project→local→policy→flag→command→session）"),
        ("ccb:data:claude_md", "data_entity", "CLAUDE.md", "项目级 CLAUDE.md 配置文件，从项目层级发现和加载"),
        ("ccb:data:feature_flag_store", "data_entity", "Feature Flag 存储", "功能开关状态存储（BunBundle/EnvVar/ConfigFile/Remote）"),
        ("ccb:data:memory_store_ccb", "data_entity", "Memory Store", "记忆存储，含 user/feedback/project/reference 四种类型"),
    ]
    
    # --- 约束 ---
    constraints = [
        ("ccb:con:tsc_errors", "constraint", "1341 个 tsc 错误", "反编译产生的 TypeScript 类型错误，不影响运行时"),
        ("ccb:con:feature_gate", "constraint", "Feature Gate 约束", "功能默认关闭，需要通过环境变量或配置启用"),
        ("ccb:con:bun_runtime", "constraint", "Bun 运行时依赖", "必须使用 Bun 运行，不兼容纯 Node.js（除构建产物）"),
        ("ccb:con:decompiled_code", "constraint", "反编译代码约束", "代码是逆向工程/反编译产物，非原始上游源码"),
    ]
    
    # --- 需求 ---
    requirements = [
        ("ccb:req:cli_interaction", "requirement", "CLI 交互", "提供交互式 REPL 和 Headless/Pipe 两种交互模式"),
        ("ccb:req:multi_provider", "requirement", "多提供商支持", "支持 Anthropic、OpenAI、Bedrock、Vertex 等多个 LLM 提供商"),
        ("ccb:req:tool_ecosystem", "requirement", "工具生态系统", "提供丰富的开发工具（Bash、文件编辑、代码搜索、Git 等）"),
        ("ccb:req:cross_platform", "requirement", "跨平台支持", "支持 macOS、Windows、Linux 三大平台"),
        ("ccb:req:extensibility", "requirement", "可扩展性", "通过 Feature Flag 和 MCP 协议支持功能扩展"),
    ]
    
    # --- 角色 ---
    actors = [
        ("ccb:actor:developer", "actor", "开发者", "使用 Claude Code CLI 进行开发的软件工程师"),
        ("ccb:actor:project_owner", "actor", "项目拥有者", "CCB 开源项目维护者"),
        ("ccb:actor:anthropic", "actor", "Anthropic", "Claude Code 原版的所有者"),
    ]
    
    all_entities = modules + functions + interfaces + data_entities + constraints + requirements + actors
    
    # 插入实体
    for eid, etype, ename, edesc in all_entities:
        conn.execute(
            "INSERT OR IGNORE INTO entities (id, type_id, name, description, confidence, source) VALUES (?, ?, ?, ?, 0.90, 'manual')",
            (eid, etype, ename, edesc),
        )
    
    # ===== 关系 =====
    
    relations = [
        # --- 模块包含功能 ---
        ("ccb:mod:cli_entry", "contains", "ccb:func:subcommand_dispatch", 0.95, "CLI 入口分发子命令"),
        ("ccb:mod:cli_entry", "contains", "ccb:func:headless_pipe", 0.90, "CLI 入口支持 Headless/Pipe 模式"),
        ("ccb:mod:query_engine", "contains", "ccb:func:query_api", 0.95, "查询引擎执行 API 查询"),
        ("ccb:mod:query_engine", "contains", "ccb:func:session_compaction", 0.90, "查询引擎管理会话压缩"),
        ("ccb:mod:tool_system", "contains", "ccb:func:tool_dispatch_ccb", 0.95, "工具系统调度工具"),
        ("ccb:mod:provider_layer", "contains", "ccb:func:provider_switch", 0.95, "提供商层切换提供商"),
        ("ccb:mod:provider_layer", "contains", "ccb:func:stream_adapter", 0.90, "提供商层适配流"),
        ("ccb:mod:ui_layer", "contains", "ccb:func:repl_interaction", 0.95, "UI 层处理 REPL 交互"),
        ("ccb:mod:feature_flag", "contains", "ccb:func:feature_check", 0.95, "Feature Flag 系统检查功能开关"),
        ("ccb:mod:auth_system", "contains", "ccb:func:auth_credential", 0.95, "认证系统管理凭据"),
        ("ccb:mod:mcp_system", "contains", "ccb:func:mcp_client", 0.95, "MCP 系统管理客户端"),
        ("ccb:mod:context_system", "contains", "ccb:func:context_assembly", 0.95, "上下文系统组装上下文"),
        ("ccb:mod:computer_use", "contains", "ccb:func:screen_control", 0.95, "Computer Use 模块控制屏幕"),
        ("ccb:mod:voice_mode", "contains", "ccb:func:voice_stt", 0.95, "语音模式处理语音识别"),
        ("ccb:mod:openai_compat", "contains", "ccb:func:openai_adapter", 0.95, "OpenAI 兼容层适配协议"),
        ("ccb:mod:memory_system_ccb", "contains", "ccb:func:memory_recall", 0.95, "记忆系统处理记忆检索"),
        ("ccb:mod:permission_system", "contains", "ccb:func:permission_check", 0.95, "权限系统检查权限"),
        ("ccb:mod:config_management_ccb", "contains", "ccb:func:settings_merge", 0.95, "配置管理系统合并配置"),
        ("ccb:mod:daemon_mode", "contains", "ccb:func:daemon_supervisor", 0.95, "守护进程管理 supervisor"),
        ("ccb:mod:telemetry", "contains", "ccb:func:telemetry_collect", 0.95, "遥测系统收集数据"),
        ("ccb:mod:agent_tools", "contains", "ccb:func:code_analysis", 0.95, "Agent 工具库提供代码分析"),
        ("ccb:mod:agent_tools", "contains", "ccb:func:bash_execution", 0.95, "Agent 工具库提供 Bash 执行"),
        ("ccb:mod:agent_tools", "contains", "ccb:func:subagent_fork", 0.85, "Agent 工具库支持子 Agent 分叉"),
        
        # --- 功能依赖接口 ---
        ("ccb:func:query_api", "depends_on", "ccb:iface:anthropic_api", 0.95, "API 查询默认使用 Anthropic API"),
        ("ccb:func:query_api", "depends_on", "ccb:iface:openai_api", 0.85, "API 查询可选使用 OpenAI API"),
        ("ccb:func:query_api", "depends_on", "ccb:iface:aws_bedrock", 0.75, "API 查询可选使用 AWS Bedrock"),
        ("ccb:func:query_api", "depends_on", "ccb:iface:gcp_vertex", 0.70, "API 查询可选使用 GCP Vertex"),
        ("ccb:func:auth_credential", "depends_on", "ccb:iface:anthropic_oauth", 0.90, "认证凭据管理使用 Anthropic OAuth"),
        ("ccb:func:telemetry_collect", "depends_on", "ccb:iface:growthbook_api", 0.80, "遥测使用 GrowthBook A/B 测试"),
        ("ccb:func:telemetry_collect", "depends_on", "ccb:iface:datadog_api", 0.75, "遥测上传到 Datadog"),
        
        # --- 功能依赖其他功能 ---
        ("ccb:func:provider_switch", "depends_on", "ccb:func:stream_adapter", 0.95, "提供商切换需要流适配"),
        ("ccb:func:repl_interaction", "depends_on", "ccb:func:query_api", 0.95, "REPL 交互需要 API 查询"),
        ("ccb:func:tool_dispatch_ccb", "depends_on", "ccb:func:feature_check", 0.85, "工具调度需要检查 Feature Flag"),
        ("ccb:func:mcp_client", "depends_on", "ccb:func:tool_dispatch_ccb", 0.80, "MCP 客户端注册工具到调度系统"),
        ("ccb:func:context_assembly", "depends_on", "ccb:func:settings_merge", 0.70, "上下文组装使用配置合并结果"),
        ("ccb:func:memory_recall", "depends_on", "ccb:func:context_assembly", 0.80, "记忆检索结果用于上下文组装"),
        ("ccb:func:screen_control", "depends_on", "ccb:func:bash_execution", 0.70, "屏幕操控可能依赖 Bash 执行"),
        ("ccb:func:subagent_fork", "depends_on", "ccb:func:query_api", 0.85, "子 Agent 分叉需要独立 API 查询"),
        
        # --- 模块依赖关系 ---
        ("ccb:mod:query_engine", "depends_on", "ccb:mod:provider_layer", 0.95, "查询引擎依赖提供商层"),
        ("ccb:mod:query_engine", "depends_on", "ccb:mod:tool_system", 0.95, "查询引擎依赖工具系统"),
        ("ccb:mod:query_engine", "depends_on", "ccb:mod:state_management", 0.90, "查询引擎依赖状态管理"),
        ("ccb:mod:query_engine", "depends_on", "ccb:mod:session_storage", 0.85, "查询引擎依赖会话存储"),
        ("ccb:mod:ui_layer", "depends_on", "ccb:mod:query_engine", 0.95, "UI 层依赖查询引擎"),
        ("ccb:mod:ui_layer", "depends_on", "ccb:mod:ink_framework", 0.95, "UI 层依赖 Ink 框架"),
        ("ccb:mod:tool_system", "depends_on", "ccb:mod:feature_flag", 0.85, "工具系统依赖 Feature Flag"),
        ("ccb:mod:context_system", "depends_on", "ccb:mod:config_management_ccb", 0.80, "上下文系统依赖配置管理"),
        ("ccb:mod:bridge_remote", "depends_on", "ccb:mod:auth_system", 0.90, "Bridge 模式依赖认证系统"),
        ("ccb:mod:computer_use", "depends_on", "ccb:mod:shell_execution", 0.80, "Computer Use 依赖 Shell 执行层"),
        ("ccb:mod:voice_mode", "depends_on", "ccb:mod:auth_system", 0.80, "语音模式依赖 Anthropic OAuth 认证"),
        ("ccb:mod:openai_compat", "depends_on", "ccb:mod:provider_layer", 0.90, "OpenAI 兼容层属于提供商层扩展"),
        ("ccb:mod:memory_system_ccb", "depends_on", "ccb:mod:session_storage", 0.75, "记忆系统依赖会话存储"),
        ("ccb:mod:permission_system", "depends_on", "ccb:mod:agent_tools", 0.85, "权限系统依赖 Agent 工具库"),
        ("ccb:mod:telemetry", "depends_on", "ccb:mod:config_management_ccb", 0.80, "遥测系统依赖配置管理"),
        
        # --- 约束关联 ---
        ("ccb:con:tsc_errors", "constrains", "ccb:mod:cli_entry", 0.60, "tsc 错误不影响运行时，仅约束类型检查"),
        ("ccb:con:feature_gate", "constrains", "ccb:func:tool_dispatch_ccb", 0.85, "Feature Gate 约束工具加载"),
        ("ccb:con:bun_runtime", "constrains", "ccb:mod:cli_entry", 0.95, "Bun 运行时约束入口"),
        ("ccb:con:decompiled_code", "constrains", "ccb:mod:tool_system", 0.70, "反编译代码约束工具行为"),
        
        # --- 需求实现 ---
        ("ccb:func:repl_interaction", "implements", "ccb:req:cli_interaction", 0.95, "REPL 交互实现 CLI 交互需求"),
        ("ccb:func:headless_pipe", "implements", "ccb:req:cli_interaction", 0.85, "Headless 模式实现 CLI 交互需求"),
        ("ccb:func:provider_switch", "implements", "ccb:req:multi_provider", 0.95, "提供商切换实现多提供商支持"),
        ("ccb:func:tool_dispatch_ccb", "implements", "ccb:req:tool_ecosystem", 0.95, "工具调度实现工具生态系统"),
        ("ccb:func:bash_execution", "implements", "ccb:req:cross_platform", 0.80, "Bash 执行实现跨平台支持"),
        ("ccb:func:feature_check", "implements", "ccb:req:extensibility", 0.90, "Feature Flag 实现可扩展性"),
        ("ccb:func:mcp_client", "implements", "ccb:req:extensibility", 0.85, "MCP 客户端实现可扩展性"),
        
        # --- 影响关系 ---
        ("ccb:func:session_compaction", "impacts", "ccb:func:query_api", 0.85, "会话压缩影响 API 查询的上下文质量"),
        ("ccb:func:permission_check", "impacts", "ccb:func:tool_dispatch_ccb", 0.90, "权限检查影响工具调度"),
        ("ccb:func:settings_merge", "impacts", "ccb:func:context_assembly", 0.80, "配置合并影响上下文组装"),
        ("ccb:func:memory_recall", "impacts", "ccb:func:context_assembly", 0.85, "记忆检索影响上下文质量"),
        
        # --- 数据实体关联 ---
        ("ccb:data:app_state", "relates_to", "ccb:mod:state_management", 0.95, "AppState 由状态管理模块维护"),
        ("ccb:data:session_jsonl", "relates_to", "ccb:mod:session_storage", 0.95, "Session JSONL 是会话存储的实现"),
        ("ccb:data:config_file_ccb", "relates_to", "ccb:mod:config_management_ccb", 0.95, "配置文件由配置管理模块维护"),
        ("ccb:data:claude_md", "relates_to", "ccb:mod:context_system", 0.90, "CLAUDE.md 由上下文系统加载"),
        ("ccb:data:memory_store_ccb", "relates_to", "ccb:mod:memory_system_ccb", 0.95, "Memory Store 是记忆系统的数据存储"),
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
    counts = conn.execute(
        "SELECT 'entities' AS tbl, COUNT(*) FROM entities UNION ALL SELECT 'relations', COUNT(*) FROM relations"
    ).fetchall()
    conn.close()
    
    print(f"✅ Claude Code 本体数据已写入")
    for row in counts:
        print(f"   {row['tbl']}: {row['COUNT(*)']}")

if __name__ == "__main__":
    seed_claude_code_ontology()
