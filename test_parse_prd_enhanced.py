"""
端到端测试：用"给CCB项目增加Linux上的屏幕操控能力"作为PRD，
测试 parse_prd 四阶段流水线的增强效果。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from parser.llm_parser import parse_prd

test_prd = """# PRD：CCB 项目增加 Linux 上的屏幕操控能力

## 背景
CCB（Claude Code Best）项目目前已经实现了 Computer Use 屏幕操控功能，但仅支持 macOS 和 Windows。
Linux 平台的后端尚未完成，需要补充实现。

## 功能需求

### 1. Linux 屏幕截图
在 Linux 上实现屏幕截图功能，支持 X11 和 Wayland 两种显示协议。

### 2. Linux 键鼠模拟
在 Linux 上实现键盘和鼠标模拟操作：
- 鼠标点击、移动、拖拽
- 键盘输入、快捷键
- 剪贴板读写

### 3. 应用管理
在 Linux 上实现应用窗口管理：
- 获取窗口列表
- 切换窗口焦点
- 启动/关闭应用

## 技术要求
- 使用 Python 实现（与现有 macOS/Windows 后端一致）
- 支持 X11 和 Wayland 两种显示服务器
- 通过 MCP 协议暴露给上层调用
- 需处理不同 Linux 发行版的兼容性

## 涉及模块
- packages/@ant/computer-use-mcp/（MCP 服务器）
- packages/@ant/computer-use-input/（键鼠模拟）
- packages/@ant/computer-use-swift/（截图 + 应用管理）
"""

print("=" * 60)
print("测试: parse_prd 四阶段流水线增强模式")
print("=" * 60)
print()
print("输入 PRD:")
print("-" * 40)
print(test_prd.strip())
print("-" * 40)
print()
print("正在执行四阶段流水线...")
print("  阶段 1: LLM 实体抽取")
print("  阶段 2: 语义匹配 + 图搜索")
print("  阶段 3: LLM 推理（3 个并行 subagent）")
print("  阶段 4: LLM 融合")
print()

try:
    result = parse_prd(test_prd)

    summary = result["summary"]
    print("=" * 60)
    print("流水线执行完成")
    print("=" * 60)
    print(f"  抽取实体: {summary['entities_extracted']} 个")
    print(f"  匹配实体: {summary['entities_matched']} 个")
    print(f"  发现关系: {summary['relations_found']} 条")
    print(f"  推理结果:")
    inf = summary.get("inferences", {})
    print(f"    隐含依赖: {inf.get('dependencies', 0)} 条")
    print(f"    隐含约束: {inf.get('constraints', 0)} 条")
    print(f"    影响范围: {inf.get('impacts', 0)} 条")
    print(f"  增强模式: {summary.get('enhancement_mode', 'unknown')}")
    print(f"  流水线阶段: {' → '.join(summary.get('pipeline_stages', []))}")
    print()

    # 打印阶段 1 中间结果
    trace = result.get("pipeline_trace", {})
    stage1 = trace.get("stage1_entities", [])
    if stage1:
        print("=" * 60)
        print("阶段 1 - 抽取的实体")
        print("=" * 60)
        for e in stage1:
            print(f"  [{e.get('type', '?')}] {e.get('name', '?')} - {e.get('description', '')[:60]}")
            print(f"    keywords: {e.get('search_keywords', [])}")
        print()

    # 打印阶段 2 中间结果
    stage2_matches = trace.get("stage2_matches", [])
    if stage2_matches:
        print("=" * 60)
        print("阶段 2 - 语义匹配结果")
        print("=" * 60)
        for m in stage2_matches:
            status = "✅" if m.get("match") else "❌"
            eid = m.get("matched_entity_id", "N/A") or "N/A"
            print(f"  {status} {m.get('prd_entity_name', '?')} → {eid} (conf: {m.get('confidence', 0)})")
        print()

    stage2_subgraph = trace.get("stage2_subgraph", {})
    if stage2_subgraph:
        print(f"  子图: {len(stage2_subgraph.get('entities', []))} 个实体, {len(stage2_subgraph.get('relations', []))} 条关系")
        print()

    # 打印阶段 3 中间结果
    stage3 = trace.get("stage3_inferences", {})
    if stage3:
        print("=" * 60)
        print("阶段 3 - 推理结果")
        print("=" * 60)
        for dep in stage3.get("dependencies", []):
            print(f"  🔗 依赖: {dep.get('source_entity', '?')} → {dep.get('dependency', '?')}")
            print(f"     证据: {dep.get('evidence', '')[:80]}")
        for con in stage3.get("constraints", []):
            print(f"  📋 约束: {con.get('entity', '?')} ← {con.get('constraint', '?')}")
            print(f"     证据: {con.get('evidence', '')[:80]}")
        for imp in stage3.get("impacts", []):
            print(f"  ⚡ 影响: {imp.get('entity', '?')} → {imp.get('impacted_module', '?')}")
            print(f"     证据: {imp.get('evidence', '')[:80]}")
        print()

    # 打印阶段 4 最终结果
    enriched_prd = result["enriched_prd"]
    print("=" * 60)
    print("阶段 4 - 增强后的 PRD")
    print("=" * 60)
    print(enriched_prd)

except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
