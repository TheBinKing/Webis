# Webis - 多模态数据清洗工具
![Python Version](https://img.shields.io/badge/Python-3.9-blue)  
![Build Status](https://img.shields.io/badge/Build-Passed-green)  

Webis是一个支持**文档、PDF、图片、HTML网页**等多模态数据的清洗工具，可以自动识别文件类型并快速调用不同工具，批量清洗各类文件并提供**结构化输出**。当前Webis已集成四种模态数据处理工具，其中**Webis_HTML**为我们独立开发的网页数据提取工具，使用 AI 技术自动识别网页上的有价值信息。我们已将Webis_HTML作为一个独立子模块同步上传至Webis项目仓库
## 🏗️ 项目结构

```
Webis/
├── README.md                 # 项目总说明文档
│
├── Webis_MAIN/               # 主项目：多模态文件处理工具
│   ├── process_file.py       # 便捷使用脚本
│   ├── tools/                # 核心工具
│   │   ├── file_processor.py              # 统一文件处理器（主程序）
│   │   ├── file_processor_with_output.py  # 带输出功能的文件处理器
│   │   ├── processors/                    # 各类型处理器脚本
│   │   │   ├── __init__.py                # 处理器初始化模块
│   │   │   ├── base_processor.py          # 基础处理器接口
│   │   │   ├── document_processor.py      # 文本处理器接口
│   │   │   ├── html_processor.py          # 网页文件处理器接口
│   │   │   ├── image_processor.py         # 图片处理器接口
│   │   │   └── pdf_processor.py           # PDF处理器接口
│   │   └── data/                          # 测试数据
│   │       ├── Doc/                       # Doc测试数据
│   │       ├── pdf/                       # PDF测试数据
│   │       └── Pic/                       # Pic测试数据
│   │
│   ├── setup/                # 环境配置
│   │   ├── conda_setup.sh    # Conda环境自动配置脚本
│   │   ├── uv_setup.sh       # uv环境自动配置脚本
│   │   └── requirements.txt  # Python依赖包列表
│   │
│   ├── examples/             # 使用示例
│   │   ├── demo.py           # 完整演示脚本
│   │   ├── doc_example.docx  # 文档示例文件
│   │   ├── html_example.html # HTML示例文件
│   │   ├── pdf_example.pdf   # PDF示例文件
│   │   ├── pic_example.jpg   # 图片示例文件
│   │   └── outputs/          # 输出目录
│   │
│   ├── docs/                 # 文档
│   │   ├── Doc.md            # 文档处理说明
│   │   ├── PDF.md            # PDF处理说明
│   │   ├── Pic.md            # 图片OCR工具说明
│   │   └── Introduction.md   # 详细使用说明
│   │
│   └── archives/             # 归档文件
│       └── Miniconda3-latest-MacOSX-arm64.sh  # Miniconda安装包
│
└── Webis_HTML/               # 为Webis设计的HTML内容提取工具
```

## 🚀 快速开始

### 1. 环境配置

```bash
# 运行自动配置脚本
bash setup/conda_setup.sh
# 如果是uv环境
bash setup/uv_setup.sh

# 或手动配置
conda create -n webis_tools python=3.9 -y
conda activate webis_tools
pip install -r setup/requirements.txt
```

### 2. 基础使用

```bash
# 激活环境
conda activate webis_tools

# 处理单个文件
python tools/file_processor.py tools/data/pdf/example.pdf

# 运行完整演示
python examples/run_demo.py
```

### 3. 代码中使用

```python
# 添加工具路径
import sys
sys.path.append('tools')

from file_processor import extract_text_from_file

# 处理文件
result = extract_text_from_file('your_file.pdf')
if result['success']:
    print(result['text'])
```

## 📁 支持的文件类型

| 类型 | 扩展名                                   | 处理工具   | 说明                              |
| ---- | ---------------------------------------- | ---------- | --------------------------------- |
| 文档 | `.txt`, `.md`, `.docx`                   | LangChain  | 直接文本提取                      |
| PDF  | `.pdf`                                   | PyPDF      | 按页提取，保留页码信息            |
| 图片 | `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tiff` | EasyOCR    | 光学字符识别                      |
| HTML | `.html`, `.htm`                          | Webis_HTML | 通过 API 调用，按页面结构清洗提取 |

> **HTML 处理说明**: HTML 文件处理需要 Webis_HTML 服务器运行。`html_processor.py` 会通过 HTTP API 调用 Webis_HTML 服务（默认地址：`http://localhost:9000`），请参考Webis_HTML项目文档启动服务器。

## 🔧 功能特性

- ✅ **自动文件类型识别**: 根据扩展名自动选择合适的处理工具
- ✅ **统一接口**: 提供一致的API接口处理不同类型文件
- ✅ **批量处理**: 支持批量处理多个文件
- ✅ **错误处理**: 完善的错误处理和日志记录
- ✅ **中文支持**: 完全支持中文文档和OCR
- ✅ **可扩展**: 易于添加新的文件类型支持
- ✅ **模块化设计**: 各处理器独立，便于维护和扩展

## 📖 详细文档

- [文档处理说明](docs/Doc.md)
- [PDF处理说明](docs/PDF.md) 
- [图片OCR工具说明](docs/Pic.md)
- [详细使用说明](docs/Introduction.md)

## 🛠️ 开发

### 如何添加新的文件处理类型

1. 在 `tools/processors/` 中创建新的处理器类（继承 `BaseFileProcessor`）
2. 在 `tools/processors/__init__.py` 中导入并注册新处理器
3. 在 `tools/file_processor.py` 的 `UnifiedFileProcessor` 中注册新类型
4. 更新支持的扩展名列表和文档

### Webis_HTML 说明

**Webis_HTML** 是一个为Webis开发的独立的 HTML 网页数据提取工具，`html_processor.py` 通过 HTTP API 调用 Webis_HTML 服务：

- **API 地址**: 默认 `http://localhost:9000`，可通过 `HTMLProcessor(api_url="...")` 自定义

- **依赖服务**: 

  - 模型服务器（端口 9065）
  - Web API 服务器（端口 9000）

- **返回数据**: 包含提取的文本内容、元数据、链接和图片信息

  > **注意**: Webis 和 Webis_HTML 使用不同的虚拟环境，避免依赖版本冲突,请根据Webis_HTML的说明文档启动服务器。

## 🤝 贡献

欢迎贡献！请在 [GitHub](https://github.com/TheBinKing/Webis) 上提交问题或拉取请求。如需支持，请联系维护者或加入社区讨论。

