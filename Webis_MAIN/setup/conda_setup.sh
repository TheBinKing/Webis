#!/usr/bin/env bash
# conda_setup.sh - Webis_Tools 一键环境安装脚本（for Conda）
# Author: Webis Project
# 说明：用于在 Conda 环境下安装 Webis_Tools 并可选接入主 Webis 接口

set -e

echo "=== Webis_Tools Conda 环境初始化 ==="

# 1. 检查 conda 是否安装
if ! command -v conda &> /dev/null; then
    echo "❌ 未检测到 Conda，请先安装 Miniconda 或 Anaconda。"
    exit 1
fi

# 2. 创建并激活 Conda 环境
echo ""
echo "[1/5] 创建 Conda 环境 webis_tools..."
conda create -n webis_tools python=3.10 -y
# 让 conda 命令在脚本中可用
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate webis_tools

# 3. 安装基础依赖
echo ""
echo "[2/5] 安装基础依赖..."
pip install --upgrade pip
pip install langchain-community docx2txt pypdf

# 4. 可选安装 OCR 支持（新增：先检测是否已装 easyocr）
echo ""
echo "[3/5] OCR（EasyOCR）支持检测..."
if python - <<'PY'
try:
    import easyocr  # noqa
except Exception:
    raise SystemExit(1)
PY
then
    echo "✓ 已检测到 easyocr，无需安装。"
else
    echo "→ 当前环境未检测到 easyocr。"
    read -p "是否安装图片OCR支持？(y/n): " install_ocr
    if [[ $install_ocr == "y" || $install_ocr == "Y" ]]; then
        echo "→ 安装 EasyOCR..."
        pip install easyocr
        echo "✓ OCR 支持已安装"
    else
        echo "→ 跳过 OCR 安装（后续可手动运行：pip install easyocr）"
    fi
fi

# 5. 可选配置 Webis 主接口（保持原功能）
echo ""
read -p "[4/5] 是否连接主 Webis 接口？(y/n): " connect_webis
if [[ $connect_webis == "y" || $connect_webis == "Y" ]]; then
    read -p "请输入 Webis 主程序接口地址 (默认 http://127.0.0.1:8000): " WEBIS_API
    WEBIS_API=${WEBIS_API:-http://127.0.0.1:8000}
    export WEBIS_API_URL=$WEBIS_API
    echo "export WEBIS_API_URL=$WEBIS_API" >> "$HOME/.bashrc"
    echo "✓ 已设置并写入环境变量 WEBIS_API_URL"
else
    echo "→ 跳过接口注册（可手动设置：export WEBIS_API_URL=http://127.0.0.1:8000）"
fi

# 6. 测试运行（修正为 ./tools/file_processor.py，并更健壮）
echo ""
echo "[5/5] 测试运行..."
if [ -f "tools/file_processor.py" ]; then
    # 优先找一个常见示例路径；不存在则退化为帮助页
    if [ -f "tools/data/pdf/demo.pdf" ]; then
        python tools/file_processor.py tools/data/pdf/demo.pdf > /dev/null 2>&1 || echo "⚠ 运行示例时出现问题（可忽略或稍后手动重试）"
    else
        python tools/file_processor.py -h > /dev/null 2>&1 || echo "⚠ 无法显示帮助信息（请手动运行：python tools/file_processor.py -h）"
    fi
else
    echo "⚠ 未找到 ./tools/file_processor.py，请确认当前路径在项目根目录。"
fi

echo ""
echo "✅ Webis_Tools Conda 环境安装完成！"
echo ""
echo "使用方法："
echo "  conda activate webis_tools"
echo "  python tools/file_processor.py <文件路径>"
echo "  # 示例：python tools/file_processor.py tools/data/pdf/demo.pdf"
