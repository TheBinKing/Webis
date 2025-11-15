# Webis使用说明

## 概述

本项目提供了一个统一的文件处理接口，可以自动识别文件类型并使用相应的工具提取文本内容。支持三种主要模态：

- **文档处理**: `.docx`, `.txt`, `.md` 文件 (使用 LangChain)
- **PDF处理**: `.pdf` HTML文件 (使用 PyPDF)  
- **图片处理**: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff` 文件 (使用 EasyOCR)
- **HTML处理**: `.html` 文件 (使用 Webis_HTML) 

## 环境配置

### 1. 安装 Python

在 macOS 上安装 Python 的几种方式：

#### 方式一：使用 Homebrew (推荐)

```bash
# 安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python
brew install python
```

#### 方式二：从官网下载

访问 [python.org](https://www.python.org/downloads/) 下载并安装 Python 3.8+

#### 方式三：使用 pyenv (开发者推荐)

```bash
# 安装 pyenv
brew install pyenv

# 安装并使用 Python 3.11
pyenv install 3.11.0
pyenv global 3.11.0
```

### 2. 验证 Python 安装

```bash
python3 --version
pip3 --version
```

### 3. 安装依赖包

#### 快速安装 (推荐)

```bash
cd /Users/easonnoway/Desktop/Webis_Tools
pip3 install -r requirements.txt
```

#### 手动安装

```bash
# 基础依赖
pip3 install langchain-community docx2txt pypdf

# 图片OCR (可选，需要时安装)
pip3 install easyocr torch torchvision
```

## 接口说明

### 1. 单独处理器接口

#### DocumentProcessor - 文档处理器

```python
from file_processor import DocumentProcessor

processor = DocumentProcessor()

# 检查是否支持文件类型
if processor.can_process("test.docx"):
    # 提取文本
    result = processor.extract_text("test.docx")
    if result["success"]:
        print(result["text"])
    else:
        print(f"错误: {result['error']}")
```

#### PDFProcessor - PDF处理器

```python
from file_processor import PDFProcessor

processor = PDFProcessor()

# 提取PDF文本
result = processor.extract_text("document.pdf")
if result["success"]:
    print(result["text"])  # 包含分页信息
```

#### ImageProcessor - 图片OCR处理器

```python
from file_processor import ImageProcessor

processor = ImageProcessor()

# OCR识别图片
result = processor.extract_text("image.png")
if result["success"]:
    print(result["text"])
```

####  HTML处理器

- 基于 Webis_HTML API  进行解析
- 使用示例:example

```bash
python process_file.py example.html
```

- 默认 Webis_HTML API 服务地址: http://localhost:9000
- 需要先启动Webis_HTML模型服务器和Web服务器，详情请见Webis_HTML

### 2. 统一处理器接口

#### UnifiedFileProcessor - 统一处理器

```python
from file_processor import UnifiedFileProcessor

processor = UnifiedFileProcessor()

# 自动判断文件类型并处理
result = processor.extract_text("any_file.pdf")
print(f"文件类型: {result['file_type']}")
print(f"文本内容: {result['text']}")
```

### 3. 便捷函数接口

#### 单文件处理

```python
from file_processor import extract_text_from_file

# 最简单的使用方式
result = extract_text_from_file("file.pdf")
if result["success"]:
    print(f"文件类型: {result['file_type']}")
    print(f"文本长度: {len(result['text'])}")
    print(result["text"])
```

#### 批量文件处理

```python
from file_processor import batch_extract_text

# 批量处理多个文件
file_paths = ["doc1.pdf", "doc2.docx", "image1.png"]
results = batch_extract_text(file_paths)

for file_path, result in results.items():
    if result["success"]:
        print(f"✓ {file_path}: {len(result['text'])} 字符")
    else:
        print(f"✗ {file_path}: {result['error']}")
```

## 使用示例

### 命令行使用

```bash
# 处理单个文件
python3 file_processor.py document.pdf

# 查看支持的文件类型
python3 file_processor.py
```

### Python脚本使用

```python
#!/usr/bin/env python3
from file_processor import extract_text_from_file

def main():
    # 处理不同类型的文件
    files = [
        "pdf/示例.pdf",
        "Doc/demo.pdf", 
        "Pic/demo.pdf"
    ]
    
    for file_path in files:
        print(f"\n处理文件: {file_path}")
        result = extract_text_from_file(file_path)
        
        if result["success"]:
            print(f"文件类型: {result['file_type']}")
            print(f"文本长度: {len(result['text'])} 字符")
            print("文本预览:")
            print(result["text"][:300] + "...")
        else:
            print(f"处理失败: {result['error']}")

if __name__ == "__main__":
    main()
```

## 返回结果格式

所有处理器都返回统一的结果格式：

```python
{
    "success": bool,        # 是否处理成功
    "text": str,           # 提取的文本内容
    "error": str,          # 错误信息 (失败时)
    "file_type": str       # 文件类型 (仅统一接口)
}
```

## 支持的文件类型

| 类型 | 扩展名                                   | 处理工具   | 说明                   |
| ---- | ---------------------------------------- | ---------- | ---------------------- |
| 文档 | `.txt`, `.md`, `.docx`                   | LangChain  | 直接文本提取           |
| PDF  | `.pdf`                                   | PyPDF      | 按页提取，保留页码信息 |
| 图片 | `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff` | EasyOCR    | 光学字符识别           |
| HTML | `.html`                                  | Webis_HTML | 按页面结构清洗，提取   |

## 常见问题

### Q: 安装依赖时出现错误？

A: 确保使用正确的Python版本 (3.8+)，可能需要使用 `pip3` 而不是 `pip`

### Q: EasyOCR 第一次运行很慢？

A: EasyOCR 首次使用会下载模型文件，请耐心等待

### Q: 图片识别准确率不高？

A: 可以尝试：

- 提高图片分辨率
- 确保文字清晰
- 调整置信度阈值 (代码中的 confidence > 0.5)

### Q: PDF 无法提取文本？

A: 可能是扫描版PDF，建议先转换为图片再用OCR处理

## 扩展说明

如需添加新的文件类型或更换处理工具，可以：

1. 继承基础处理器类
2. 实现 `can_process()` 和 `extract_text()` 方法
3. 在 `UnifiedFileProcessor` 中注册新处理器

## 性能优化建议

1. **批量处理**: 使用 `batch_extract_text()` 处理多文件
2. **延迟加载**: 图片处理器采用延迟加载，避免不必要的模型初始化
3. **缓存结果**: 对于重复处理的文件，建议缓存结果
4. **并行处理**: 对于大量文件，可考虑多进程并行处理