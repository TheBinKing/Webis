#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WebFLow Web服务器启动脚本 - 网页内容提取API
"""

import os
import sys
import argparse
import signal
import socket
from pathlib import Path

# 将项目根目录添加到Python路径
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)  # 更改当前工作目录到项目根目录

# 导入服务器模块
from src.server import create_app
import uvicorn

def is_port_in_use(port):
    """检查端口是否已被占用"""
    # 检查IPv4地址
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # 0.0.0.0表示所有可用网络接口
            s.bind(('0.0.0.0', port))
            return False
        except socket.error:
            return True

def main():
    """主函数：解析参数并启动服务器"""
    parser = argparse.ArgumentParser(description="启动网页内容提取API服务器")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务器主机地址")
    parser.add_argument("--port", type=int, default=8002, help="服务器端口")
    parser.add_argument("--workers", type=int, default=1, help="工作进程数")
    parser.add_argument("--api-key", type=str, help="DeepSeek API密钥（可选，也可通过环境变量设置）")
    
    args = parser.parse_args()
    
    # 检查端口是否被占用
    if is_port_in_use(args.port):
        print(f"错误: 端口 {args.port} 已被占用。请选择其他端口或关闭使用该端口的程序。")
        sys.exit(1)
    
    # 设置环境变量
    if args.api_key:
        os.environ["DEEPSEEK_API_KEY"] = args.api_key
    
    # 输出启动信息
    print(f"正在启动WebFLow网页内容提取API服务器...")
    print(f"服务器地址: http://{args.host}:{args.port}")
    print(f"工作进程数: {args.workers}")
    
    # 注册信号处理器，确保正常退出
    def signal_handler(sig, frame):
        print("\n正在关闭服务器...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 创建FastAPI应用并启动服务器
    try:
        app = create_app()
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            workers=args.workers,
            limit_concurrency=100,
            limit_max_requests=10000,
        )
    except Exception as e:
        print(f"启动服务器时发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()