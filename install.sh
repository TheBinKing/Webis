#!/bin/bash

# 获取当前脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 项目根目录
PROJECT_ROOT="$SCRIPT_DIR"

# 目标目录（用户bin目录，通常在PATH中）
USER_BIN="$HOME/.local/bin"

# 检查是否在conda环境中
if [[ -z "${CONDA_DEFAULT_ENV}" ]]; then
  echo "警告: 未检测到激活的Conda环境!"
  echo "建议在专用的Conda环境中安装此项目，以避免依赖冲突。"
  echo "请参考README.md中的'环境准备'部分。"
  read -p "是否仍要继续安装？(y/N): " confirm
  if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "安装已取消。"
    exit 1
  fi
fi

# 创建用户bin目录（如果不存在）
mkdir -p "$USER_BIN"

# 安装Python包
echo "正在安装Webis包..."
pip install -e "$PROJECT_ROOT" --no-cache-dir

# 创建符号链接（备用方案，通常通过pip安装后不需要）
echo "正在创建Webis命令链接..."
ln -sf "$PROJECT_ROOT/bin/webis" "$USER_BIN/webis"

echo "安装完成!"
echo "请确保 $USER_BIN 在您的PATH环境变量中。"
echo ""
echo "如果不在PATH中，请将以下行添加到您的~/.bashrc或~/.zshrc文件中:"
echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "要测试安装是否成功，请运行:"
echo "webis --help"
