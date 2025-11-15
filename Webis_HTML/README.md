# Webis_HTML - HTML 内容提取工具  
![Python Version](https://img.shields.io/badge/Python-3.10-blue)  
![Build Status](https://img.shields.io/badge/Build-Passed-green)  

Webis_HTML 是一个智能网页数据提取工具，使用 AI 技术自动识别网页上的有价值信息，过滤噪音，为下游 AI 训练和知识库构建提供高质量输入。  

## 目录  

- [安装](#安装)  
- [使用方法](#使用方法)  
  - [API 使用示例](#api-使用示例)  
  - [CLI 使用示例](#cli-使用示例)  
- [关于模型](#关于模型)  
- [项目结构](#项目结构)  

## 安装  

### 前置要求  

- **Python 3.10**  
- **Conda**（推荐用于环境管理）  
- **NVIDIA GPU**（可选，用于 CUDA 支持）  

### 安装 Webis
#### 方法 1：通过 pip 安装（推荐）
```bash
conda create -n webis_html python=3.10 -y

conda activate webis_html

pip install webis-llm
```
#### 方法 2：从源码安装
```bash
git clone https://github.com/TheBinKing/Webis.git  

cd Webis  

pip install -e .  

# 将 bin 目录添加到 PATH  
export PATH="$PATH:$(pwd)/bin"  
echo 'export PATH="$PATH:$(pwd)/bin"' >> ~/.bashrc  
source ~/.bashrc  
```

## 使用方法
Webis 支持 CLI 和 API 服务两种模式。**请始终先启动模型服务器！**  

### 步骤 1：启动服务器
+ **模型服务器**（端口 9065）：  

```bash
python scripts/start_model_server.py  
```

+ **Web API 服务器**（端口 9000）：  

```bash
python scripts/start_web_server.py  
```

> **注意**：默认模型（`Easonnoway/Web_info_extra_1.5b`）将自动从 HuggingFace 下载。首次运行可能需要一些时间。  
>

### API 使用示例
`api_usage.py` 脚本演示了如何通过 API 接口处理 HTML 文件，支持同步和异步两种模式，适合客户端熟悉操作。  

#### 同步处理模式
适用于少量文件，客户端等待服务器完成处理：  

```python
# 发送 HTML 文件进行同步处理  
response = requests.post(  
    "http://localhost:9000/extract/process-html",  
    files=files,  
    data=data  
)  

# 下载处理结果  
response = requests.get(f"http://localhost:9000/tasks/{task_id}/download", stream=True)  
```

#### 异步处理模式
适用于大量文件或处理时间较长的情况；提交任务后定期检查其状态：  

```python
# 提交异步处理任务  
response = requests.post(  
    "http://localhost:9000/extract/process-async",  
    files=files,  
    data=data  
)  

# 监控任务状态  
response = requests.get(f"http://localhost:9000/tasks/{async_task_id}")  

# 任务完成后下载结果  
download_response = requests.get(f"http://localhost:9000/tasks/{async_task_id}/download", stream=True)  
```

#### 运行 API 示例
```bash
# 基本用法  
python samples/api_usage.py  

# 使用 DeepSeek API 增强处理结果（需要 API 密钥）  
python samples/api_usage.py --use-deepseek --api-key YOUR_API_KEY_HERE  
```

> **提示**：确保 `input_html/` 目录中有 HTML 文件。结果将保存为 `{task_id}_results.zip`（同步）和 `{async_task_id}_async_results.zip`（异步）。  
>

### CLI 使用示例
`cli_usage.sh` 脚本提供了命令行界面的快速示例，适用于批量处理或脚本集成。  

#### 基本用法
```bash
# 处理 HTML 文件  
./samples/cli_usage.sh  
```

> **注意**：脚本调用 `webis extract` 命令，需要有效的 `YOUR_API_KEY_HERE`。结果保存到 `output_basic/` 目录。  
>

#### 其他命令
```bash
# 查看版本信息  
$PROJECT_ROOT/bin/webis version  

# 检查 API 连接  
$PROJECT_ROOT/bin/webis check-api --api-key YOUR_API_KEY  

# 查看帮助  
$PROJECT_ROOT/bin/webis --help  
$PROJECT_ROOT/bin/webis extract --help  
```

## 关于模型
### 模型详情
+ **名称**：Web_info_extra_1.5b  
+ **HuggingFace**：[Easonnoway/Web_info_extra_1.5b](https://huggingface.co/Easonnoway/Web_info_extra_1.5b)  
+ **参数量**：1.5B  
+ **功能**：DOM 树节点分类

### 使用说明
+ 默认下载到 `~/.cache/huggingface/hub`。  
+ 使用 `--model-path` 指定本地路径。  
+ 缓存管理：设置 `HF_HOME` 或 `TRANSFORMERS_CACHE` 来自定义位置；使用 `huggingface-cli delete-cache` 清除缓存。

## 项目结构
+ `bin/` - 命令行工具  
+ `src/` - 源代码  
    - `cli/` - CLI 实现  
    - `core/` - 核心逻辑  
    - `server/` - API 服务器
+ `scripts/` - 启动脚本  
+ `samples/` - 使用示例（包括 `api_usage.py` 和 `cli_usage.sh`）  
    - `input_html/` - 示例 HTML 文件  
    - `output_basic/` - CLI 输出结果
+ `config/` - 配置文件

## 贡献
欢迎贡献！请在 [GitHub](https://github.com/TheBinKing/Webis) 上提交问题或拉取请求。如需支持，请联系维护者或加入社区讨论。  
