#!/usr/bin/env bash
# uv_setup.sh - Webis_Tools 一键环境安装脚本（for uv）
# Author: Webis Project
# 说明：本脚本用于 uv 环境下安装 Webis_Tools 所需依赖并可选接入主 Webis 服务接口

set -e

echo "=== Webis_Tools uv 环境初始化 ==="

# 1. 检查 uv 是否存在
if ! command -v uv &> /dev/null; then
    echo "❌ 未检测到 uv，请先安装：https://docs.astral.sh/uv/"
    exit 1
fi

# 2. 检查虚拟环境是否已激活
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠ 未检测到 uv 虚拟环境，请先创建并激活，例如："
    echo "   uv venv webis_tools"
    echo "   source webis_tools/bin/activate"
    exit 1
fi

# 3. 安装基础依赖
echo ""
echo "[1/4] 安装基础依赖..."
uv pip install langchain-community docx2txt pypdf

# 4. 询问是否安装 OCR 支持
echo ""
read -p "[2/4] 是否安装图片OCR支持？(y/n): " install_ocr
if [[ $install_ocr == "y" || $install_ocr == "Y" ]]; then
    echo "→ 正在安装 EasyOCR..."
    uv pip install easyocr
    echo "✓ OCR 支持已安装"
else
    echo "→ 跳过 OCR 安装（后续可运行 uv pip install easyocr）"
fi

# 5. 询问是否连接主 Webis 接口
echo ""
read -p "[3/4] 是否连接主 Webis 接口？(y/n): " connect_webis
if [[ $connect_webis == "y" || $connect_webis == "Y" ]]; then
    read -p "请输入 Webis 主程序接口地址 (默认 http://127.0.0.1:8000): " WEBIS_API
    WEBIS_API=${WEBIS_API:-http://127.0.0.1:8000}
    export WEBIS_API_URL=$WEBIS_API
    echo "export WEBIS_API_URL=$WEBIS_API" >> "$HOME/.bashrc"
    echo "✓ 已设置并写入环境变量 WEBIS_API_URL"
else
    echo "→ 跳过接口注册（后续可手动设置：export WEBIS_API_URL=http://127.0.0.1:8000）"
fi

# 6. 测试运行
echo ""
echo "[4/4] 测试运行..."
if [ -f "file_processor.py" ]; then
    python file_processor.py pdf/示例.pdf > /dev/null 2>&1 || echo "⚠ 测试文件不存在或未初始化"
else
    echo "⚠ 未找到 file_processor.py，请确认当前路径"
fi

echo ""
echo "✅ Webis_Tools 已成功安装并配置完毕！"
echo ""
echo "使用方法："
echo "  source webis_tools/bin/activate"
echo "  python file_processor.py <文件路径>"
echo "  python run_demo.py  # 运行完整演示"
