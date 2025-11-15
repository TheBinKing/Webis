#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Webis 主入口脚本
从项目根目录运行文件处理器
"""

import sys
import os

# 添加tools目录到Python路径
tools_path = os.path.join(os.path.dirname(__file__), 'tools')
sys.path.insert(0, tools_path)

# 导入文件处理器
from file_processor import extract_text_from_file, UnifiedFileProcessor

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Webis - 统一文件处理工具")
        print("=" * 50)
        print("用法: python process_file.py <文件路径>")
        print()
        
        processor = UnifiedFileProcessor()
        print("支持的文件类型:")
        for category, exts in processor.get_supported_extensions().items():
            print(f"  {category}: {', '.join(exts)}")
        print()
        print("示例:")
        print("  python process_file.py tools/data/pdf/示例.pdf")
        print("  python process_file.py examples/test.txt")
        print()
        print("更多功能:")
        print("  python examples/demo.py  # 运行完整演示")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # 如果是相对路径，从当前目录查找
    if not os.path.isabs(file_path) and not os.path.exists(file_path):
        # 尝试在常见目录中查找
        search_paths = [
            file_path,
            os.path.join('tools/data', file_path),
            os.path.join('examples', file_path),
            os.path.join('tools/processors', file_path)
        ]
        
        found = False
        for search_path in search_paths:
            if os.path.exists(search_path):
                file_path = search_path
                found = True
                break
        
        if not found:
            print(f"错误: 找不到文件 {sys.argv[1]}")
            sys.exit(1)
    
    print(f"处理文件: {file_path}")
    print("-" * 50)
    
    result = extract_text_from_file(file_path)
    
    if result["success"]:
        print(f"✓ 处理成功")
        print(f"文件类型: {result['file_type']}")
        print(f"文本长度: {len(result['text'])} 字符")
        print()
        print("抽取的文本内容:")
        print("=" * 50)
        print(result["text"])
    else:
        print(f"✗ 处理失败: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()
