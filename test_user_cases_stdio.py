"""
通过 MCP stdio 运行用户指定的 3 个测试用例。
"""
import asyncio
import sys
import json
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


async def run_case(proc, case_name, tool_name, arguments, timeout=180):
    """发送单个 tools/call 请求并读取响应。"""
    req = {
        "jsonrpc": "2.0",
        "id": case_name,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments,
        },
    }
    proc.stdin.write((json.dumps(req) + "\n").encode())
    await proc.stdin.drain()

    try:
        resp = await asyncio.wait_for(proc.stdout.readline(), timeout=timeout)
        return json.loads(resp)
    except asyncio.TimeoutError:
        return {"error": f"{case_name} 超时 ({timeout}s)"}


async def main():
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-u",
        os.path.join(PROJECT_DIR, "server.py"),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},
    )

    assert proc.stdin is not None
    assert proc.stdout is not None

    # 1. initialize
    init_req = {
        "jsonrpc": "2.0",
        "id": "init",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "user-case-tester", "version": "1.0.0"},
        },
    }
    proc.stdin.write((json.dumps(init_req) + "\n").encode())
    await proc.stdin.drain()
    resp = await asyncio.wait_for(proc.stdout.readline(), timeout=10)
    print("[INIT]", json.loads(resp).get("result", {}).get("serverInfo", {}))

    # 2. initialized notification
    notif = {"jsonrpc": "2.0", "method": "notifications/initialized"}
    proc.stdin.write((json.dumps(notif) + "\n").encode())
    await proc.stdin.drain()

    # 3. list tools
    list_req = {"jsonrpc": "2.0", "id": "list", "method": "tools/list"}
    proc.stdin.write((json.dumps(list_req) + "\n").encode())
    await proc.stdin.drain()
    resp = await asyncio.wait_for(proc.stdout.readline(), timeout=10)
    tools = json.loads(resp).get("result", {}).get("tools", [])
    print(f"[TOOLS] 发现 {len(tools)} 个工具:")
    for t in tools:
        print(f"  - {t['name']}")

    print("\n" + "=" * 60)

    # Case 1: ingest_document 新增 Anthropic CEO / ChatGPT
    print("\n[Case 1] ingest_document dry_run")
    case1_dry = await run_case(
        proc,
        "case1_dry",
        "ingest_document",
        {
            "content": "Anthropic公司的CEO是个秃头，他平时用的最多的模型是Openai的Chatgpt",
            "title": "用户测试用例-1",
            "dry_run": True,
        },
    )
    print(json.dumps(case1_dry, ensure_ascii=False, indent=2)[:2000])

    if "error" not in case1_dry:
        plan1 = case1_dry.get("result", {}).get("structuredContent", {}).get("plan", {})
        print("\n[Case 1] ingest_document 执行写入")
        case1_exec = await run_case(
            proc,
            "case1_exec",
            "ingest_document",
            {
                "title": "用户测试用例-1",
                "dry_run": False,
                "plan": plan1,
            },
        )
        print(json.dumps(case1_exec, ensure_ascii=False, indent=2)[:2000])

    print("\n" + "=" * 60)

    # Case 2: modify_ontology 关联 JPMorgan 与 Anthropic
    print("\n[Case 2] modify_ontology dry_run")
    case2_dry = await run_case(
        proc,
        "case2_dry",
        "modify_ontology",
        {
            "description": "更新本体中的关联：acomp:jpmorgan摩根大通，和Anthropic之间是有关联关系的",
            "target_entity_id": "acomp:jpmorgan",
            "dry_run": True,
        },
    )
    print(json.dumps(case2_dry, ensure_ascii=False, indent=2)[:2000])

    if "error" not in case2_dry:
        plan2 = case2_dry.get("result", {}).get("structuredContent", {}).get("plan", {})
        print("\n[Case 2] modify_ontology 执行写入")
        case2_exec = await run_case(
            proc,
            "case2_exec",
            "modify_ontology",
            {
                "description": "更新本体中的关联：acomp:jpmorgan摩根大通，和Anthropic之间是有关联关系的",
                "target_entity_id": "acomp:jpmorgan",
                "dry_run": False,
                "plan": plan2,
            },
        )
        print(json.dumps(case2_exec, ensure_ascii=False, indent=2)[:2000])

    print("\n" + "=" * 60)

    # Case 3: ingest_document 新增 Anthropic CEO 不是 developer
    print("\n[Case 3] ingest_document dry_run")
    case3_dry = await run_case(
        proc,
        "case3_dry",
        "ingest_document",
        {
            "content": "Anthropic的CEO不是ccb:actor:developer开发者",
            "title": "用户测试用例-3",
            "dry_run": True,
        },
    )
    print(json.dumps(case3_dry, ensure_ascii=False, indent=2)[:2000])

    if "error" not in case3_dry:
        plan3 = case3_dry.get("result", {}).get("structuredContent", {}).get("plan", {})
        print("\n[Case 3] ingest_document 执行写入")
        case3_exec = await run_case(
            proc,
            "case3_exec",
            "ingest_document",
            {
                "title": "用户测试用例-3",
                "dry_run": False,
                "plan": plan3,
            },
        )
        print(json.dumps(case3_exec, ensure_ascii=False, indent=2)[:2000])

    proc.terminate()
    print("\n[Done]")


if __name__ == "__main__":
    asyncio.run(main())
