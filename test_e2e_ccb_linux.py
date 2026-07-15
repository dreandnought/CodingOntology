"""
端到端测试：PRD = "修改ccb，为其添加linux端的屏幕操控能力"
验证四阶段流水线中间结果正确性、各阶段耗时、最终输出质量。
"""
import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(__file__))

# 简短 PRD（模拟真实 MCP 调用场景）
TEST_PRD = "修改ccb，为其添加linux端的屏幕操控能力"


def _fmt_elapsed(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    return f"{seconds:.2f}s"


def main():
    from parser.llm_parser import (
        _extract_prd_entities,
        _semantic_match_entities,
        _graph_search,
        _reason_inferences,
        _fuse_prd,
    )

    print("=" * 70)
    print("端到端测试：parse_prd 四阶段流水线")
    print("=" * 70)
    print(f"输入 PRD: {TEST_PRD}")
    print()

    # ---- 检查本体中与 PRD 相关的预设关系链 ----
    print("=" * 70)
    print("本体中与 PRD 相关的预设关系链（预期应被匹配到）")
    print("=" * 70)
    from models.entity import search_entities
    for kw in ["屏幕操控", "screen", "computer_use", "ccb"]:
        hits = search_entities(kw, limit=5)
        if hits:
            print(f"  关键词 '{kw}' → {len(hits)} 个候选:")
            for h in hits:
                print(f"    {h['id']} | {h['name']} ({h.get('type_name','')})")
    print()

    total_start = time.time()
    stage_times = {}

    # ---- 阶段 1：LLM 实体抽取 ----
    print("=" * 70)
    print("阶段 1：LLM 实体抽取")
    print("=" * 70)
    t0 = time.time()
    prd_entities = _extract_prd_entities(TEST_PRD)
    stage_times["stage1_extract"] = time.time() - t0
    print(f"  耗时: {_fmt_elapsed(stage_times['stage1_extract'])}")
    print(f"  抽取实体数: {len(prd_entities)}")
    for e in prd_entities:
        print(f"    [{e.get('type','?')}] {e.get('name','?')} - {e.get('description','')[:60]}")
        print(f"      search_keywords: {e.get('search_keywords', [])}")
    print()

    # ---- 阶段 2：语义匹配 + 图搜索 ----
    print("=" * 70)
    print("阶段 2：语义匹配 + 图搜索")
    print("=" * 70)
    t0 = time.time()
    match_results = _semantic_match_entities(prd_entities)
    matched_ids = [m["matched_entity_id"] for m in match_results if m.get("match")]
    subgraph = _graph_search(matched_ids, max_depth=2)
    stage_times["stage2_match_graph"] = time.time() - t0
    print(f"  耗时: {_fmt_elapsed(stage_times['stage2_match_graph'])}")
    print(f"  匹配结果:")
    for m in match_results:
        status = "MATCH" if m.get("match") else "NO MATCH"
        eid = m.get("matched_entity_id") or "N/A"
        print(f"    [{status}] {m.get('prd_entity_name','?')} → {eid} (conf: {m.get('confidence',0)})")
    print(f"  子图: {len(subgraph.get('entities', []))} 个实体, {len(subgraph.get('relations', []))} 条关系")
    print(f"  子图实体:")
    for e in subgraph.get("entities", []):
        print(f"    {e['id']} | {e['name']} ({e.get('type','')}) | {e.get('description','')[:80]}")
    print(f"  子图关系:")
    for r in subgraph.get("relations", []):
        if r.get("transitive"):
            print(f"    [transitive] {r.get('source_entity_id','?')} --{r['relation_type']}(depth={r.get('depth',1)})--> {r.get('target_entity_name','?')}")
        else:
            direction = r.get("direction", "")
            rel_type = r.get("relation_type", "")
            related = r.get("related_entity_name", r.get("target_entity_name", "?"))
            print(f"    [{direction}] {rel_type} → {related} (conf: {r.get('confidence', 0)})")
    print()

    # ---- 阶段 3：LLM 推理（3 个并行 subagent）----
    print("=" * 70)
    print("阶段 3：LLM 推理（3 个并行 subagent：依赖/约束/影响）")
    print("=" * 70)
    t0 = time.time()
    inferences = _reason_inferences(TEST_PRD, subgraph)
    stage_times["stage3_reason"] = time.time() - t0
    print(f"  耗时: {_fmt_elapsed(stage_times['stage3_reason'])}")
    print(f"  推理结果:")
    for dep in inferences.get("dependencies", []):
        print(f"    DEP: {dep.get('source_entity','?')} → {dep.get('dependency','?')}")
        print(f"         证据: {dep.get('evidence','')[:100]}")
    for con in inferences.get("constraints", []):
        print(f"    CON: {con.get('entity','?')} ← {con.get('constraint','?')}")
        print(f"         证据: {con.get('evidence','')[:100]}")
    for imp in inferences.get("impacts", []):
        print(f"    IMP: {imp.get('entity','?')} → {imp.get('impacted_module','?')}")
        print(f"         证据: {imp.get('evidence','')[:100]}")
    print()

    # ---- 阶段 4：LLM 融合 ----
    print("=" * 70)
    print("阶段 4：LLM 融合 — 生成增强版 PRD")
    print("=" * 70)
    t0 = time.time()
    enriched_prd = _fuse_prd(TEST_PRD, inferences, subgraph)
    stage_times["stage4_fuse"] = time.time() - t0
    print(f"  耗时: {_fmt_elapsed(stage_times['stage4_fuse'])}")
    print()

    # ---- 最终输出 ----
    print("=" * 70)
    print("最终输出：增强后的 PRD")
    print("=" * 70)
    print(enriched_prd)
    print()

    # ---- 耗时汇总 ----
    total_time = time.time() - total_start
    print("=" * 70)
    print("耗时汇总")
    print("=" * 70)
    for stage, t in stage_times.items():
        print(f"  {stage}: {_fmt_elapsed(t)}")
    print(f"  TOTAL: {_fmt_elapsed(total_time)}")
    print()

    # ---- 正确性检查 ----
    print("=" * 70)
    print("正确性检查")
    print("=" * 70)
    checks = []

    # 检查 1：阶段 1 应抽取出与屏幕操控相关的实体
    has_screen_entity = any(
        "屏幕" in e.get("name", "") or "screen" in e.get("name", "").lower()
        for e in prd_entities
    )
    checks.append(("阶段1: 抽取出屏幕操控相关实体", has_screen_entity))

    # 检查 2：阶段 2 应匹配到本体中的 screen_control 或 computer_use
    expected_ids = {"ccb:func:screen_control", "ccb:mod:computer_use"}
    has_expected_match = any(
        m.get("matched_entity_id") in expected_ids
        for m in match_results
    )
    checks.append((f"阶段2: 匹配到 {expected_ids} 之一", has_expected_match))

    # 检查 3：子图应包含至少 2 条关系
    has_relations = len(subgraph.get("relations", [])) >= 2
    checks.append(("阶段2: 子图包含 >= 2 条关系", has_relations))

    # 检查 4：阶段 3 应产出至少 1 条推理
    total_inferences = (
        len(inferences.get("dependencies", []))
        + len(inferences.get("constraints", []))
        + len(inferences.get("impacts", []))
    )
    checks.append(("阶段3: 推理结果 >= 1 条", total_inferences >= 1))

    # 检查 5：阶段 4 输出应比原文更长
    checks.append(("阶段4: 增强后 PRD 长度 > 原文", len(enriched_prd) > len(TEST_PRD)))

    # 检查 6：融合而非追加（不应出现明显的"附录"或"--- 分隔线后追加"）
    has_appendix = "---" in enriched_prd and enriched_prd.count("---") >= 2 and "附录" in enriched_prd
    checks.append(("阶段4: 融合而非简单追加", not has_appendix))

    all_pass = True
    for desc, passed in checks:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  [{status}] {desc}")

    print()
    if all_pass:
        print("ALL CHECKS PASSED")
    else:
        print("SOME CHECKS FAILED — 请检查上方输出")


if __name__ == "__main__":
    main()
