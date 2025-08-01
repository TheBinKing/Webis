#!/bin/bash
# 快速CLI使用示例 - 简化版本

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== Webis CLI 快速示例 ==="

echo "1. Webis提取:"
"$PROJECT_ROOT/bin/webis" extract \
    --input "$SCRIPT_DIR/input_html" \
    --output "$SCRIPT_DIR/output_basic" \
    --use-deepseek \
    --api-key "YOUR_API_KEY_HERE" \
    --verbose

echo ""
echo "2. 其他有用的命令:"
echo "   查看版本信息:"
echo "   \"$PROJECT_ROOT/bin/webis\" version"
echo ""
echo "   检查API连接（需要提供API密钥）:"
echo "   \"$PROJECT_ROOT/bin/webis\" check-api --api-key YOUR_API_KEY"
echo ""
echo "   查看完整帮助:"
echo "   \"$PROJECT_ROOT/bin/webis\" --help"
echo "   \"$PROJECT_ROOT/bin/webis\" extract --help"

echo ""
echo "=== 快速示例完成 ==="
