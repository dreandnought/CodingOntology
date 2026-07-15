"""
端到端测试：调用 parse_prd 解析一篇 PRD 文档。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from parser.llm_parser import parse_prd

# 使用 test_data 中的一篇简短文档作为测试 PRD
test_doc = """
# 项目：Claude Code CLI 工具

## 概述
Claude Code Best (CCB) 是 Anthropic 官方 Claude Code CLI 工具的源码反编译/逆向还原项目。
目标是复现 Claude Code 大部分功能及工程化能力。

## 功能需求

### 1. CLI 交互
- 提供交互式 REPL 和 Headless/Pipe 两种交互模式
- 支持 51 个子命令：mcp、server、ssh、open、auth、plugin、agents、auto-mode、doctor 等
- 通过 Commander.js 定义 CLI 接口

### 2. 多 LLM 提供商支持
- 支持 Anthropic Messages API（主路径）
- 支持 OpenAI Chat Completions API（通过兼容层）
- 支持 AWS Bedrock 和 GCP Vertex
- 支持 Azure OpenAI

### 3. 工具系统
- 54+ 个内置工具：BashTool、FileEditTool、GrepTool、AgentTool、WebFetchTool 等
- 通过 Feature Flag 条件加载工具
- 支持 MCP 协议扩展工具

### 4. 会话管理
- JSONL 格式的会话存储
- 上下文压缩（snip/micro/auto）
- Token 预算跟踪

### 5. 跨平台支持
- 支持 macOS、Windows、Linux
- Shell 执行层抽象（bash/zsh/PowerShell）
- Computer Use 屏幕操控（macOS + Windows 可用）

### 6. 认证系统
- 7 种认证方式
- OAuth 服务
- API Key 管理

## 技术约束
- 必须使用 Bun 运行时（构建产物可兼容 Node.js）
- 1341 个 tsc 错误（来自反编译，不影响运行时）
- 功能默认关闭，需通过环境变量启用
- 代码是逆向工程产物，非原始源码
"""

print("=" * 60)
print("PRD Ontology MCP - 端到端测试")
print("=" * 60)
print()
print(f"测试文档长度: {len(test_doc)} 字符")
print()
print("正在调用 LLM API 解析 PRD...")
print()

try:
    result = parse_prd(test_doc)
    
    summary = result["summary"]
    print(f"抽取实体: {summary['entities_extracted']} 个")
    print(f"匹配实体: {summary['entities_matched']} 个")
    print(f"发现关系: {summary['relations_found']} 条")
    inf = summary.get("inferences", {})
    print(f"推理结果: 依赖 {inf.get('dependencies', 0)}, 约束 {inf.get('constraints', 0)}, 影响 {inf.get('impacts', 0)}")
    print(f"流水线阶段: {' → '.join(summary.get('pipeline_stages', []))}")
    print()

    enriched_prd = result["enriched_prd"]
    print("=" * 60)
    print("增强后的 PRD（前 3000 字符）")
    print("=" * 60)
    print(enriched_prd[:3000])
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
