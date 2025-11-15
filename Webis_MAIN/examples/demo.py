#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Webis 批量文件处理演示
支持文档、PDF、图片、HTML四种模态的批量文本抽取和输出
"""

import sys
import os

# 添加 tools 目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
tools_dir = os.path.join(os.path.dirname(current_dir), 'tools')
if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

from file_processor_with_output import batch_process_with_output
import logging

# 设置日志级别为WARNING，减少输出
logging.getLogger().setLevel(logging.WARNING)

def main():
    """批量处理所有示例文件"""
    # 获取脚本所在目录（examples 目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("🚀 Webis - 多模态数据清洗工具")
    print("=" * 50)
    print("支持文档(.docx/.txt/.md)、PDF(.pdf)、图片(.jpg/.png等)、HTML(.html/.htm)四种模态")
    print()
    
    # 收集所有可用的示例文件
    available_files = []
    demo_files = [
        ("doc_example.docx", "📄 Word文档"),
        ("pdf_example.pdf", "📝 PDF文档"), 
        ("pic_example.jpg", "🖼️ 图片文件"),
        ("html_example.html", "🌐 HTML文件")
    ]
    
    print("📁 检查示例文件:")
    for file_name, file_desc in demo_files:
        # 使用脚本目录作为基准路径
        file_path = os.path.join(script_dir, file_name)
        if os.path.exists(file_path):
            available_files.append(file_path)
            print(f"  ✅ {file_desc}: {file_name}")
        else:
            print(f"  ❌ {file_desc}: {file_name} (文件不存在)")
    
    if not available_files:
        print("\n❌ 没有找到可处理的示例文件")
        return
    
    print(f"\n🔄 开始批量处理 {len(available_files)} 个文件...")
    print()
    
    # 执行批量处理
    # 输出目录也基于脚本目录
    output_dir = os.path.join(script_dir, "outputs")
    results = batch_process_with_output(
        file_paths=available_files,
        output_dir=output_dir,
        save_output=True,
        include_metadata=True
    )
    
    # 显示处理结果
    print("📊 处理结果:")
    print("-" * 40)
    
    success_count = 0
    total_chars = 0
    
    for file_path, result in results.items():
        file_name = os.path.basename(file_path)
        if result["success"]:
            success_count += 1
            total_chars += len(result["text"])
            print(f"✅ {file_name}")
            print(f"   📋 类型: {result['file_type']}")
            print(f"   🔧 处理器: {result['processor']}")
            print(f"   📏 文本长度: {len(result['text'])} 字符")
            if "output_file" in result:
                output_name = os.path.basename(result['output_file'])
                print(f"   💾 输出文件: {output_name}")
        else:
            print(f"❌ {file_name}")
            print(f"   ⚠️ 错误: {result['error']}")
        print()
    
    # 显示统计信息
    print("📈 统计信息:")
    print(f"  🎯 成功率: {success_count}/{len(available_files)} ({success_count/len(available_files)*100:.1f}%)")
    print(f"  📝 总文本量: {total_chars:,} 字符")
    print(f"  📂 输出目录: {output_dir}")
    
    # 显示输出文件列表
    if os.path.exists(output_dir):
        files = [f for f in os.listdir(output_dir) if f.endswith('.txt') or f.endswith('.json')]
        if files:
            print(f"\n📂 生成的文件 ({len(files)} 个):")
            for file_name in sorted(files):
                file_path = os.path.join(output_dir, file_name)
                size = os.path.getsize(file_path)
                if file_name.endswith('.json'):
                    print(f"  📋 {file_name} ({size} 字节) - 处理摘要")
                else:
                    print(f"  📄 {file_name} ({size} 字节)")
    
    print(f"\n🎉 批量处理完成！")
    print(f"💡 查看 outputs/ 目录获取所有输出文件")

if __name__ == "__main__":
    main()
