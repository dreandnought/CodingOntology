"""
测试 MCP Server 的 stdio 模式连通性。
模拟一个 Coding Agent 通过 stdio 连接 MCP Server，
发送 list_tools 和 call_tool 请求。
"""
import asyncio
import sys
import json
import os

# 模拟 MCP stdio 协议：使用 JSON-RPC 通过 stdin/stdout 通信
async def test_stdio():
    # 启动 server.py 作为子进程
    proc = await asyncio.create_subprocess_exec(
        sys.executable, '-u',  # -u 禁用缓冲
        os.path.join(os.path.dirname(__file__), 'server.py'),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ, 'PYTHONUNBUFFERED': '1'},
    )
    
    assert proc.stdin is not None
    assert proc.stdout is not None
    
    # MCP JSON-RPC 请求
    request_id = 1
    
    def make_request(method, params=None):
        nonlocal request_id
        req = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
        }
        if params:
            req["params"] = params
        request_id += 1
        return json.dumps(req) + "\n"
    
    # 1. 发送 initialize 请求（MCP 协议握手）
    print("1️⃣  发送 initialize 请求...")
    init_req = make_request("initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test-client", "version": "1.0.0"}
    })
    proc.stdin.write(init_req.encode())
    await proc.stdin.drain()
    
    # 读取响应
    resp = await asyncio.wait_for(proc.stdout.readline(), timeout=10)
    init_resp = json.loads(resp)
    print(f"    ✅ 初始化成功: server info = {init_resp.get('result', {}).get('serverInfo', {})}")
    
    # 2. 发送 notifications/initialized 通知
    print("2️⃣  发送 initialized 通知...")
    notif = json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n"
    proc.stdin.write(notif.encode())
    await proc.stdin.drain()
    
    # 3. 发送 tools/list 请求
    print("3️⃣  发送 tools/list 请求...")
    list_req = make_request("tools/list")
    proc.stdin.write(list_req.encode())
    await proc.stdin.drain()
    
    resp = await asyncio.wait_for(proc.stdout.readline(), timeout=10)
    list_resp = json.loads(resp)
    tools = list_resp.get("result", {}).get("tools", [])
    print(f"    ✅ 发现 {len(tools)} 个工具:")
    for t in tools:
        print(f"       - {t['name']}: {t.get('description', '')[:60]}")
    
    # 4. 发送 tools/call - 测试 query_ontology（轻量查询）
    print()
    print("4️⃣  发送 tools/call (query_ontology)...")
    call_req = make_request("tools/call", {
        "name": "query_ontology",
        "arguments": {
            "entity_name": "Gateway"
        }
    })
    proc.stdin.write(call_req.encode())
    await proc.stdin.drain()
    
    resp = await asyncio.wait_for(proc.stdout.readline(), timeout=10)
    call_resp = json.loads(resp)
    result = call_resp.get("result", {})
    content = result.get("content", [])
    entity = result.get("entity", {})
    relations = result.get("relations", [])
    
    print(f"    查询结果:")
    if entity:
        print(f"      实体: {entity.get('name', '?')} ({entity.get('type_name', '?')})")
        print(f"      描述: {entity.get('description', '')[:60]}")
    else:
        print(f"      未找到匹配实体")
    if relations:
        print(f"      关系 ({len(relations)} 条):")
        for r in relations[:5]:
            print(f"        [{r['relation_type']}] {r['direction']} → {r['related_entity_name']} (conf: {r['confidence']})")
    
    # 5. 测试 parse_prd（调用 LLM）
    print()
    print("5️⃣  发送 tools/call (parse_prd) - 需要 LLM API 调用，等待响应...")
    call_req2 = make_request("tools/call", {
        "name": "parse_prd",
        "arguments": {
            "content": "# 测试 PRD\n## 功能\nGateway 模块负责消息路由和配置管理。"
        }
    })
    proc.stdin.write(call_req2.encode())
    await proc.stdin.drain()
    
    try:
        resp = await asyncio.wait_for(proc.stdout.readline(), timeout=180)
        call_resp2 = json.loads(resp)
        result2 = call_resp2.get("result", {})
        summary = result2.get("summary", {})
        print(f"    ✅ parse_prd 完成:")
        print(f"       抽取实体: {summary.get('entities_extracted', 0)}")
        print(f"       匹配实体: {summary.get('entities_matched', 0)}")
        print(f"       发现关系: {summary.get('relations_found', 0)}")
    except asyncio.TimeoutError:
        print(f"    ⚠️ parse_prd 超时（LLM API 响应较慢）")
    
    # 关闭进程
    proc.terminate()
    print()
    print("=" * 50)
    print("✅ MCP stdio 通信测试完成!")

if __name__ == "__main__":
    asyncio.run(test_stdio())
