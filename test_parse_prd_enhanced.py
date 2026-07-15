"""
端到端测试：用"给CCB项目增加Linux上的屏幕操控能力"作为PRD，
测试 parse_prd 的融合增强效果。
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
print("测试: parse_prd 融合增强模式")
print("=" * 60)
print()
print("输入 PRD:")
print("-" * 40)
print(test_prd.strip())
print("-" * 40)
print()
print("正在调用 LLM API 进行融合增强...")
print()

try:
    result = parse_prd(test_prd)
    
    summary = result["summary"]
    print(f"✅ 解析完成")
    print(f"   抽取实体: {summary['entities_extracted']} 个")
    print(f"   匹配实体: {summary['entities_matched']} 个")
    print(f"   关系标注: {summary['relations_found']} 条")
    print(f"   新实体: {summary['new_entities_added']} 个")
    print(f"   增强模式: {summary.get('enhancement_mode', 'appended')}")
    print()
    
    enriched_prd = result["enriched_prd"]
    print("=" * 60)
    print("增强后的 PRD")
    print("=" * 60)
    print(enriched_prd)
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
