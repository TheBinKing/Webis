# PDF数据模态输入工具

基于性能、功能、易用性和社区活跃度，我们选出两款最适合集成到Webis项目中的PDF文本提取库：
1.PuMuPDF(fitz):综合性能之王，速度极快，文本提取精度高;
2.pdfplumber：布局和表格分析专家，API友好，调试能力强。

## 工具详细对比
- 特性维度	PyMuPDF (fitz)	               pdfplumber
- 核心优势	速度和内存效率	                页面布局和表格解析
- 提取质量	文本流顺序保持得非常好           提供字符级坐标，对布局理解更深
- 提取速度	极快，C语言底层加持              快，但纯Python实现，慢于PyMuPDF
- 易用性	   API直接，但高级功能需看文档       API设计非常直观，符合直觉
- 表格支持	支持但逻辑不如pdfplumber精细     行业标杆，表格提取效果最好
- 调试功能	无内置可视化调试	             自带可视化调试，可绘制页面元素，便于开发
- 依赖关系	自带C渲染引擎，无其他Python依赖	  基于pdfminer.six，依赖更多一些
- 开源许可	GNU AGPLv3	                    MIT License
- 推荐场景	大批量、高性能的纯文本提取	      需要精确提取表格数据或分析复杂版面

## PyMuPDF
### 安装
pip install pymupdf

### 核心代码
```python

import argparse
import fitz
import sys
from pathlib import Path

def extract_pdf_text(input_path, output_path=None, pages=None, format='plain'):
    """
    使用PyMuPDF提取PDF文本
    
    Args:
        input_path: 输入PDF路径
        output_path: 输出文件路径(可选)
        pages: 要提取的页码列表(可选)
        format: 输出格式('plain'或'markdown')
    """
    try:
        # 检查输入文件
        if not Path(input_path).exists():
            print(f"错误: 文件 '{input_path}' 不存在")
            return False
            
        # 打开PDF文档
        doc = fitz.open(input_path)
        total_pages = len(doc)
        
        # 处理页码参数
        if pages:
            # 将1-based页码转换为0-based索引
            page_indices = [p-1 for p in pages if 1 <= p <= total_pages]
            if not page_indices:
                print(f"错误: 指定的页码不在有效范围内(1-{total_pages})")
                return False
        else:
            page_indices = range(total_pages)
        
        # 提取文本
        extracted_content = []
        for i in page_indices:
            page = doc.load_page(i)
            
            if format == 'markdown':
                text = page.get_text("markdown")
            else:
                text = page.get_text("text")
                
            extracted_content.append(f"--- 第 {i+1} 页 ---\n")
            extracted_content.append(text)
            extracted_content.append("\n")
        
        # 关闭文档
        doc.close()
        
        # 输出结果
        result = "".join(extracted_content)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"成功提取文本并保存到: {output_path}")
        else:
            print(result)
            
        return True
        
    except Exception as e:
        print(f"处理PDF时发生错误: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Webis PDF文本提取工具 (基于PyMuPDF)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s document.pdf
  %(prog)s document.pdf -o output.txt
  %(prog)s document.pdf -p 1 3 5 -o selected_pages.txt
  %(prog)s document.pdf -p 1-3,5 -f markdown -o output.md
        '''
    )
    
    parser.add_argument('input', help='输入PDF文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径(可选)')
    parser.add_argument('-p', '--pages', help='要提取的页码(支持单个页码、范围或逗号分隔列表，如: 1, 1-3, 1,3,5)')
    parser.add_argument('-f', '--format', choices=['plain', 'markdown'], default='plain', 
                       help='输出格式: plain(纯文本)或markdown(默认: plain)')
    
    args = parser.parse_args()
    
    # 解析页码参数
    page_list = None
    if args.pages:
        page_list = []
        parts = args.pages.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                try:
                    start = int(start.strip())
                    end = int(end.strip())
                    page_list.extend(range(start, end+1))
                except ValueError:
                    print(f"错误: 无效的页码范围 '{part}'")
                    sys.exit(1)
            else:
                try:
                    page_list.append(int(part))
                except ValueError:
                    print(f"错误: 无效的页码 '{part}'")
                    sys.exit(1)
    
    # 执行提取
    success = extract_pdf_text(args.input, args.output, page_list, args.format)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```
### 基本用法
```bash
# 基本用法: 提取整个PDF并显示在终端
python webis_pymupdf_extractor.py document.pdf

# 提取整个PDF并保存到文件
python webis_pymupdf_extractor.py document.pdf -o output.txt

# 提取特定页码(第1, 3, 5页)
python webis_pymupdf_extractor.py document.pdf -p 1,3,5 -o selected_pages.txt

# 提取页码范围(第2到第5页)
python webis_pymupdf_extractor.py document.pdf -p 2-5 -o pages_2-5.txt

# 使用Markdown格式输出
python webis_pymupdf_extractor.py document.pdf -f markdown -o output.md

# 组合使用: 提取第1-3页和第5页，Markdown格式
python webis_pymupdf_extractor.py document.pdf -p 1-3,5 -f markdown -o output.md
```
## pdfplumber
### 安装
pip install pdfplumber
### 核心代码
```python
#!/usr/bin/env python3
"""
Webis PDF文本提取工具 - pdfplumber版本
支持文本和表格提取
"""

import argparse
import pdfplumber
import sys
from pathlib import Path
import json

def extract_pdf_content(input_path, output_path=None, pages=None, extract_tables=False, table_format='json'):
    """
    使用pdfplumber提取PDF内容和表格
    
    Args:
        input_path: 输入PDF路径
        output_path: 输出文件路径(可选)
        pages: 要提取的页码列表(可选)
        extract_tables: 是否提取表格
        table_format: 表格输出格式('json'或'csv')
    """
    try:
        # 检查输入文件
        if not Path(input_path).exists():
            print(f"错误: 文件 '{input_path}' 不存在")
            return False
            
        # 打开PDF文档
        with pdfplumber.open(input_path) as pdf:
            total_pages = len(pdf.pages)
            
            # 处理页码参数
            if pages:
                # 将1-based页码转换为0-based索引
                page_indices = [p-1 for p in pages if 1 <= p <= total_pages]
                if not page_indices:
                    print(f"错误: 指定的页码不在有效范围内(1-{total_pages})")
                    return False
            else:
                page_indices = range(total_pages)
            
            # 提取内容
            extracted_text = []
            extracted_tables = []
            
            for i in page_indices:
                page = pdf.pages[i]
                
                # 提取文本
                text = page.extract_text()
                if text:
                    extracted_text.append(f"--- 第 {i+1} 页 ---\n")
                    extracted_text.append(text)
                    extracted_text.append("\n")
                
                # 提取表格（如果启用）
                if extract_tables:
                    tables = page.extract_tables()
                    for table_idx, table in enumerate(tables):
                        if table:  # 非空表格
                            table_data = {
                                "page": i+1,
                                "table_index": table_idx+1,
                                "data": table
                            }
                            extracted_tables.append(table_data)
            
            # 准备输出
            output_content = []
            
            # 添加文本内容
            if extracted_text:
                output_content.append("="*50 + "\n")
                output_content.append("提取的文本内容:\n")
                output_content.append("="*50 + "\n")
                output_content.extend(extracted_text)
            
            # 添加表格内容
            if extracted_tables:
                output_content.append("="*50 + "\n")
                output_content.append("提取的表格:\n")
                output_content.append("="*50 + "\n")
                
                if table_format == 'json':
                    output_content.append(json.dumps(extracted_tables, ensure_ascii=False, indent=2))
                else:  # CSV格式
                    for table in extracted_tables:
                        output_content.append(f"\n--- 第 {table['page']} 页, 表格 {table['table_index']} ---\n")
                        for row in table['data']:
                            csv_line = ",".join([f'"{cell}"' if cell and ',' in str(cell) else str(cell) for cell in row])
                            output_content.append(csv_line + "\n")
            
            # 输出结果
            result = "".join(output_content)
            
            if output_path:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"成功提取内容并保存到: {output_path}")
            else:
                print(result)
                
        return True
        
    except Exception as e:
        print(f"处理PDF时发生错误: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Webis PDF文本和表格提取工具 (基于pdfplumber)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  %(prog)s document.pdf
  %(prog)s document.pdf -o output.txt
  %(prog)s document.pdf -p 1,3,5 -o selected_pages.txt
  %(prog)s document.pdf -t -o output_with_tables.txt
  %(prog)s document.pdf -t --table-format csv -o tables.csv
        '''
    )
    
    parser.add_argument('input', help='输入PDF文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径(可选)')
    parser.add_argument('-p', '--pages', help='要提取的页码(支持单个页码、范围或逗号分隔列表)')
    parser.add_argument('-t', '--tables', action='store_true', help='同时提取表格')
    parser.add_argument('--table-format', choices=['json', 'csv'], default='json', 
                       help='表格输出格式: json或csv(默认: json)')
    
    args = parser.parse_args()
    
    # 解析页码参数
    page_list = None
    if args.pages:
        page_list = []
        parts = args.pages.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                try:
                    start = int(start.strip())
                    end = int(end.strip())
                    page_list.extend(range(start, end+1))
                except ValueError:
                    print(f"错误: 无效的页码范围 '{part}'")
                    sys.exit(1)
            else:
                try:
                    page_list.append(int(part))
                except ValueError:
                    print(f"错误: 无效的页码 '{part}'")
                    sys.exit(1)
    
    # 执行提取
    success = extract_pdf_content(
        args.input, 
        args.output, 
        page_list, 
        args.tables, 
        args.table_format
    )
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

### 基本用法
```bash
# 基本用法: 提取整个PDF文本并显示在终端
python webis_pdfplumber_extractor.py document.pdf

# 提取整个PDF文本并保存到文件
python webis_pdfplumber_extractor.py document.pdf -o output.txt

# 提取特定页码(第1, 3, 5页)
python webis_pdfplumber_extractor.py document.pdf -p 1,3,5 -o selected_pages.txt

# 提取文本和表格(JSON格式)
python webis_pdfplumber_extractor.py document.pdf -t -o output_with_tables.txt

# 提取文本和表格(CSV格式)
python webis_pdfplumber_extractor.py document.pdf -t --table-format csv -o tables.csv

# 提取特定页码的表格
python webis_pdfplumber_extractor.py document.pdf -p 2-4 -t -o pages_2-4_tables.json
```

## 总结
默认使用 PyMuPDF：由于其无与伦比的速度，它应作为处理绝大多数标准PDF文档的首选引擎，为用户提供快速响应。
智能切换 pdfplumber：可以开发一个简单的探测逻辑。例如，当PyMuPDF提取的文本中疑似包含表格（但格式混乱）、或者用户明确选择了“精确提取表格”选项时，自动调用pdfplumber再次处理该页面，以获取更清晰的结构化数据。