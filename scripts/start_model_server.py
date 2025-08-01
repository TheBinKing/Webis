#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WebFLow-Node-1.5b模型服务器 - 简洁集成版
使用vLLM部署WebFLow-Node-1.5b模型的API服务
"""

import os
import sys
import argparse
import signal
import socket
from pathlib import Path
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

from vllm import LLM, SamplingParams

# 设置默认的模型路径（HuggingFace模型ID）
DEFAULT_MODEL_PATH = "Easonnoway/Web_info_extra_1.5b"

# 全局模型实例
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """使用新的lifespan上下文管理器加载模型"""
    global model
    model_path = os.environ.get("MODEL_PATH", DEFAULT_MODEL_PATH)
    device = os.environ.get("DEVICE", "cuda")
    gpu_memory_utilization = float(os.environ.get("GPU_MEMORY_UTILIZATION", 0.9))
    
    print(f"正在加载模型，路径: {model_path}...")
    model = LLM(model=model_path, 
                tensor_parallel_size=1,
                gpu_memory_utilization=gpu_memory_utilization,
                trust_remote_code=True,
                dtype="auto",
                device=device)
    print("模型加载成功！")
    
    yield  # 服务运行期间
    
    # 服务关闭时清理资源
    print("正在释放模型资源...")
    model = None

# 创建FastAPI应用
app = FastAPI(
    title="WebFLow-Node-1.5b API", 
    description="使用vLLM部署WebFLow-Node-1.5b模型的API服务",
    version="1.0.0",
    lifespan=lifespan  # 使用lifespan上下文管理器替代on_event
)

# 添加CORS中间件允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    prompt: str = Field(..., description="输入提示词")
    max_tokens: int = Field(256, description="生成的最大token数量")
    temperature: float = Field(0.2, description="采样温度，控制随机性")
    top_p: float = Field(1.0, description="Top-p采样参数")
    top_k: int = Field(50, description="Top-k采样参数")
    n: int = Field(1, description="生成的回复数量")

class GenerationResponse(BaseModel):
    text: List[str] = Field(..., description="生成的文本列表")

@app.post("/generate", response_model=GenerationResponse)
async def generate(request: GenerationRequest):
    """生成文本的API端点"""
    global model
    
    if model is None:
        return {"error": "模型尚未加载完成"}
    
    sampling_params = SamplingParams(
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        top_k=request.top_k,
        n=request.n,
    )
    
    outputs = model.generate([request.prompt], sampling_params)
    generated_texts = [output.outputs[0].text for output in outputs]
    
    return {"text": generated_texts}

@app.get("/health")
async def health():
    """健康检查端点"""
    return {"status": "ok", "model": "WebFLow-Node-1.5b"}

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
    parser = argparse.ArgumentParser(description="启动WebFLow-Node-1.5b模型服务器")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="服务器主机地址")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口")
    parser.add_argument("--model-path", type=str, default=DEFAULT_MODEL_PATH, help="模型路径")
    parser.add_argument("--gpu-id", type=int, default=0, help="指定使用的GPU ID")
    parser.add_argument("--memory-limit", type=float, default=0.9, help="GPU内存使用率限制(0-1之间)")
    
    args = parser.parse_args()
    
    # 检查端口是否被占用
    if is_port_in_use(args.port):
        print(f"错误: 端口 {args.port} 已被占用。请选择其他端口或关闭使用该端口的程序。")
        sys.exit(1)
    
    # 检查模型路径，如果是本地路径则验证是否存在
    if not args.model_path.startswith(('Easonnoway/', 'http://', 'https://')):
        if not Path(args.model_path).exists():
            print(f"错误: 本地模型路径 {args.model_path} 不存在。")
            sys.exit(1)
    else:
        print(f"使用HuggingFace模型: {args.model_path}")
        print("模型将被下载到~/.cache/huggingface/hub目录（如果尚未下载）")
    
    # 设置环境变量
    os.environ["MODEL_PATH"] = args.model_path
    os.environ["CUDA_VISIBLE_DEVICES"] = str(args.gpu_id)
    os.environ["GPU_MEMORY_UTILIZATION"] = str(args.memory_limit)
    
    # 输出启动信息
    print(f"正在启动WebFLow-Node-1.5b模型服务器...")
    print(f"模型路径: {args.model_path}")
    print(f"服务器地址: http://{args.host}:{args.port}")
    print(f"使用GPU: {args.gpu_id}")
    print(f"GPU内存使用率限制: {args.memory_limit}")
    
    # 注册信号处理器，确保正常退出
    def signal_handler(sig, frame):
        print("\n正在关闭服务器...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 启动FastAPI服务器
    try:
        uvicorn.run(app, host=args.host, port=args.port)
    except Exception as e:
        print(f"启动服务器时发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
