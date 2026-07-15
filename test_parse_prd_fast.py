"""
快速端到端测试：使用精简 prompt 验证 parse_prd 流程。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import yaml
import requests
import json
import re

# 加载配置
with open(os.path.join(os.path.dirname(__file__), "llm_config.yaml")) as f:
    cfg = yaml.safe_load(f)

provider = cfg["providers"]["siliconflow"]
API_URL = provider["base_url"].rstrip("/") + "/chat/completions"
API_KEY = provider["api_key"]
MODEL = provider["models"]["chat"]

test_doc = """
# 项目：Claude Code CLI 工具

## 概述
Claude Code Best (CCB) 是 Anthropic 官方 Claude Code CLI 工具的源码反编译/逆向还原项目。

## 功能需求

### 1. CLI 交互
- 提供交互式 REPL 和 Headless/Pipe 两种交互模式
- 支持 51 个子命令

### 2. 多 LLM 提供商支持
- 支持 Anthropic Messages API
- 支持 OpenAI Chat Completions API
- 支持 AWS Bedrock 和 GCP Vertex

### 3. 工具系统
- 54+ 个内置工具：BashTool、FileEditTool、GrepTool、AgentTool
- 通过 Feature Flag 条件加载工具
- 支持 MCP 协议扩展

### 4. 会话管理
- JSONL 格式的会话存储
- 上下文压缩和 Token 预算跟踪

### 5. 跨平台支持
- 支持 macOS、Windows、Linux
- Computer Use 屏幕操控

### 6. 认证系统
- 7 种认证方式，OAuth 服务
"""

# 使用精简的 ontology context（只列出部分最相关的实体）
ontology_context = """- ccb:mod:cli_entry | CCB CLI Entry (模块) | CLI 入口层，cli.tsx → main.tsx
- ccb:mod:query_engine | CCB Query Engine (模块) | 核心查询引擎
- ccb:mod:tool_system | CCB Tool System (模块) | Tool 注册和管理系统，54+ 工具
- ccb:mod:provider_layer | CCB Provider Layer (模块) | LLM 提供商适配层
- ccb:mod:ui_layer | CCB UI Layer (模块) | 终端 UI 层
- ccb:mod:state_management | CCB State Management (模块) | 状态管理系统
- ccb:mod:auth_system | CCB Auth System (模块) | 认证系统，7 种认证方式
- ccb:mod:session_storage | CCB Session Storage (模块) | 会话存储，JSONL 格式
- ccb:mod:mcp_system | CCB MCP System (模块) | MCP 客户端系统
- ccb:mod:context_system | CCB Context System (模块) | 上下文构建系统
- ccb:mod:computer_use | CCB Computer Use (模块) | 跨平台屏幕操控系统
- ccb:mod:voice_mode | CCB Voice Mode (模块) | 语音模式
- ccb:mod:openai_compat | CCB OpenAI 兼容层 (模块) | OpenAI 协议兼容层
- ccb:mod:permission_system | CCB Permission System (模块) | 权限系统，8 种模式
- ccb:mod:feature_flag | CCB Feature Flag (模块) | 功能开关系统
- ccb:func:query_api | API 查询 (功能) | 发送消息到 LLM API
- ccb:func:tool_dispatch_ccb | 工具调度 (功能) | 解析和执行工具调用
- ccb:func:repl_interaction | REPL 交互 (功能) | 交互式 REPL 界面
- ccb:func:headless_pipe | Headless/Pipe 模式 (功能) | 非交互式管道模式
- ccb:func:provider_switch | 提供商切换 (功能) | 在多个提供商间切换
- ccb:func:auth_credential | 认证凭据管理 (功能) | 管理 API Key、OAuth Token
- ccb:func:mcp_client | MCP 客户端 (功能) | 管理和连接 MCP 服务器
- ccb:func:session_compaction | 会话压缩 (功能) | 管理会话上下文压缩
- ccb:func:screen_control | 屏幕操控 (功能) | 跨平台截图、键鼠模拟
- ccb:func:bash_execution | Bash 执行 (功能) | 在终端中执行 bash 命令
- ccb:iface:anthropic_api | Anthropic API (接口) | Anthropic Messages API
- ccb:iface:openai_api | OpenAI API (接口) | OpenAI Chat Completions API
- ccb:iface:aws_bedrock | AWS Bedrock (接口) | AWS Bedrock IAM 认证
- ccb:iface:gcp_vertex | GCP Vertex (接口) | Google Cloud Vertex AI"""

system_prompt = """你是一个 PRD 需求分析专家。你的任务是从 PRD 文档中抽取功能级实体，与预设知识图谱进行匹配，并生成关系分析结果。

请严格按照以下步骤执行：

## 步骤 1：抽取第一层实体
从 PRD 中抽取功能级实体（功能、模块、接口）。
返回格式：
```json
[
  {"name": "CLI 交互", "type": "function", "description": "REPL 和 Headless 两种交互模式"},
  {"name": "Anthropic API", "type": "interface", "description": "Anthropic Messages API"}
]
```

实体类型包括：function（功能）、module（模块）、interface（接口）、requirement（需求）、data_entity（数据实体）、constraint（约束）、actor（角色）

## 步骤 2：匹配 Ontology 实体
将步骤 1 中的每个实体映射到 Ontology 中最匹配的实体。
返回格式：
```json
[
  {"prd_entity": "CLI 交互", "matched_entity_id": "ccb:func:repl_interaction", "confidence": 0.95, "match": true},
  {"prd_entity": "OpenAI API", "matched_entity_id": "ccb:iface:openai_api", "confidence": 0.95, "match": true}
]
```

## 步骤 3：生成关系附录
基于匹配到的实体，生成 Markdown 格式的关系附录。"""

user_prompt = f"""## 当前 Ontology 中的已知实体
{ontology_context}

## PRD 文档内容
{test_doc}

请完成三个步骤的完整分析。"""

print("=" * 60)
print("PRD Ontology MCP - 精简版端到端测试")
print("=" * 60)
print(f"测试文档: {len(test_doc)} 字符")
print(f"Ontology Context: {len(ontology_context)} 字符")
print()
print("正在调用 SiliconFlow DeepSeek-V4-Flash API...")
print()

payload = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    "temperature": 0.1,
    "max_tokens": 4096,
}

try:
    resp = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()
    llm_response = data["choices"][0]["message"]["content"]
    
    print("✅ LLM API 调用成功")
    print(f"   Token: {data['usage']['total_tokens']} 总 / {data['usage']['prompt_tokens']} 输入 / {data['usage']['completion_tokens']} 输出")
    print()
    
    # 提取 JSON 块
    json_blocks = re.findall(r"```json\n(.*?)\n```", llm_response, re.DOTALL)
    
    print(f"发现 {len(json_blocks)} 个 JSON 块")
    print()
    
    # 显示步骤 1 的实体抽取结果
    if json_blocks:
        try:
            extracted = json.loads(json_blocks[0])
            print(f"步骤 1 - 抽取实体 ({len(extracted)} 个):")
            for e in extracted:
                print(f"  📦 [{e.get('type','?')}] {e.get('name','?')} - {e.get('description','')[:50]}")
        except:
            print(f"步骤 1 JSON 解析失败")
            print(f"原始内容: {json_blocks[0][:200]}")
    
    print()
    
    # 显示步骤 2 的匹配结果
    if len(json_blocks) > 1:
        try:
            matches = json.loads(json_blocks[1])
            matched = sum(1 for m in matches if m.get("match"))
            new = sum(1 for m in matches if not m.get("match"))
            print(f"步骤 2 - 匹配结果 ({len(matches)} 个):")
            print(f"  匹配: {matched}, 新实体: {new}")
            for m in matches:
                status = "✅" if m.get("match") else "🆕"
                eid = m.get("matched_entity_id", "N/A") or "N/A"
                print(f"  {status} {m.get('prd_entity','?')} → {eid} (conf: {m.get('confidence',0)})")
        except:
            print(f"步骤 2 JSON 解析失败")
    
    print()
    
    # 显示步骤 3 的关系附录
    # 查找关系附录部分
    relation_section = ""
    for marker in ["## 🔗", "需求关系图谱", "关系分析", "实体关系", "###"]:
        if marker in llm_response:
            idx = llm_response.index(marker)
            relation_section = llm_response[idx:]
            break
    
    if relation_section:
        print("步骤 3 - 关系附录:")
        print(relation_section[:1500])
    
    print()
    print("=" * 60)
    print("✅ 端到端测试完成!")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
