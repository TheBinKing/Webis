# Webis 服务器启动脚本

本目录包含Webis系统的服务器启动脚本，用于部署和运行系统的各个组件。这些脚本提供了简便的方式来启动模型服务器和Web API服务器。

## 主要脚本

### 1. 模型服务器 (`start_model_server.py`)

该脚本用于启动基于vLLM的模型服务，负责处理文本分类和内容识别请求。

#### 功能特点
- 基于vLLM高效部署WebFLow-Node模型
- 支持多种推理参数配置（温度、top_k、top_p等）
- 提供REST API接口供其他服务调用
- 自动检测端口占用情况
- 支持优雅关闭

#### 使用方法

```bash
# 基本用法
python start_model_server.py

# 使用自定义参数
python start_model_server.py --port 8000 --model-path /path/to/model --workers 4
```

#### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--host` | 服务器主机地址 | 0.0.0.0 |
| `--port` | 服务器端口号 | 8000 |
| `--model-path` | 模型路径 | 从配置文件读取 |
| `--workers` | 工作进程数 | 1 |

### 2. Web API服务器 (`start_web_server.py`)

该脚本启动FastAPI服务器，提供HTML内容提取和处理的Web API接口。

#### 功能特点
- 提供HTML内容提取API
- 支持同步和异步处理请求
- 任务管理和结果下载
- 集成DeepSeek服务优化内容提取
- 自动管理临时文件

#### 使用方法

```bash
# 基本用法
python start_web_server.py

# 使用自定义参数
python start_web_server.py --port 8002 --workers 4 --api-key YOUR_DEEPSEEK_API_KEY
```

#### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--host` | 服务器主机地址 | 0.0.0.0 |
| `--port` | 服务器端口号 | 8002 |
| `--workers` | 工作进程数 | 1 |
| `--api-key` | DeepSeek API密钥 | 无 |

## 部署架构

Webis系统的部署架构包含以下组件：

1. **模型服务器** (端口8000)
   - 提供文本分类和噪音检测功能
   - 基于vLLM高效推理引擎
   - 使用WebFLow-Node-1.5b模型

2. **Web API服务器** (端口8002)
   - 处理HTML内容提取请求
   - 管理异步任务和结果存储
   - 提供结果下载功能

## 启动顺序

为正确启动Webis系统，请按以下顺序运行脚本：

1. 首先启动模型服务器：
```bash
python scripts/start_model_server.py
```

2. 然后启动Web API服务器：
```bash
python scripts/start_web_server.py
```

## 常见问题排查

### 端口占用

如果出现端口占用错误，可以使用以下命令查找并关闭占用端口的进程：

```bash
# 查找占用端口的进程
lsof -i :8000
lsof -i :8002

# 关闭进程
kill -9 <PID>
```

或者修改脚本中的默认端口号。

### 模型服务器无法启动

可能的原因：
- 模型路径不正确
- 显存不足
- CUDA版本不匹配

### Web API服务器连接模型服务器失败

- 确保模型服务器已正常启动
- 检查API服务器中的模型服务器URL配置
- 确认网络连接正常

## 配置文件

两个服务器都会读取项目根目录下的配置文件：
- `config/model_config.json`: 模型相关配置
- `config/api_keys.json`: API密钥配置
- `config/tag_probs.json`: 标签概率配置

## 注意事项

1. 两个服务器都需要正确启动才能使系统正常工作
2. 修改服务器端口后需要同步更新客户端代码中的端口号
3. 建议在生产环境中使用进程管理工具（如Supervisor或PM2）管理这些服务
