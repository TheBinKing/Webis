# 网页内容提取API文档

本文档描述了网页内容提取API服务（server.py）提供的所有接口。该服务提供网页内容提取、数据集生成、模型预测和结果恢复功能。

## 基本信息

- **基础URL**: `http://localhost:8001`
- **版本**: 1.0.0
- **Swagger文档**: `http://localhost:8001/docs`
- **ReDoc文档**: `http://localhost:8001/redoc`

## API接口列表

### 1. 服务状态检查

#### 请求
```
GET /
```

#### 响应
```json
{
  "message": "网页内容提取API服务正在运行"
}
```

### 2. 依赖安装

一次性安装服务所需的所有依赖。

#### 请求
```
GET /install-dependencies
```

#### 响应
```json
{
  "status": "success",
  "message": "所有依赖已安装成功",
  "details": ["fastapi", "uvicorn", "python-multipart", "aiofiles", "pydantic", "requests", "tqdm", "beautifulsoup4", "lxml", "vllm"]
}
```

### 3. 模型服务器状态检查

检查Web4LLM-Node-1.5b模型服务器是否正在运行。

#### 请求
```
GET /check-model-server
```

#### 响应（服务器在线）
```json
{
  "status": "online",
  "message": "模型服务器正在运行",
  "details": { ... }
}
```

#### 响应（服务器离线）
```json
{
  "status": "offline",
  "message": "模型服务器未运行或无法连接",
  "hint": "请确保已启动了node_model_server.py"
}
```

### 4. 同步处理HTML文件

上传HTML文件，同步处理并返回结果。适用于少量文件或短时间处理任务。

#### 请求
```
POST /process-html
```

**参数**:
- `files`: HTML文件列表（必填，表单字段）
- `tag_probs`: 标签概率配置文件（可选，表单字段）
- `model_type`: 模型类型（可选，表单字段，默认值："node"）

#### 响应（成功）
```json
{
  "task_id": "5f9d7e3a-4b5c-4d98-8f5c-2d9a8f3e4b5c",
  "status": "completed",
  "result_count": 3,
  "message": "处理完成"
}
```

#### 响应（失败）
```json
{
  "task_id": "5f9d7e3a-4b5c-4d98-8f5c-2d9a8f3e4b5c",
  "status": "failed",
  "error": "错误信息"
}
```

### 5. 异步处理HTML文件

上传HTML文件，异步处理并返回任务ID。适用于大量文件或长时间处理任务。

#### 请求
```
POST /process-async
```

**参数**:
- `files`: HTML文件列表（必填，表单字段）
- `tag_probs`: 标签概率配置文件（可选，表单字段）
- `model_type`: 模型类型（可选，表单字段，默认值："node"）

#### 响应
```json
{
  "task_id": "5f9d7e3a-4b5c-4d98-8f5c-2d9a8f3e4b5c",
  "status": "processing",
  "message": "任务已提交，正在后台处理"
}
```

### 6. 查询任务状态

根据任务ID查询处理任务的状态。

#### 请求
```
GET /tasks/{task_id}
```

**参数**:
- `task_id`: 任务ID（路径参数）

#### 响应（处理完成）
```json
{
  "status": "completed",
  "output_dir": "/path/to/output",
  "results": [
    {
      "filename": "result1.txt",
      "content": "提取的文本内容..."
    },
    {
      "filename": "result2.txt",
      "content": "提取的文本内容..."
    }
  ]
}
```

#### 响应（处理中）
```json
{
  "status": "processing",
  "message": "任务正在处理中"
}
```

#### 响应（处理失败）
```json
{
  "status": "failed",
  "error": "错误信息",
  "message": "处理失败: 错误信息"
}
```

#### 响应（任务不存在）
```json
{
  "error": "任务不存在"
}
```

### 7. 下载任务结果

下载任务处理结果的ZIP压缩文件。

#### 请求
```
GET /tasks/{task_id}/download
```

**参数**:
- `task_id`: 任务ID（路径参数）

#### 响应

成功时返回一个ZIP文件，包含所有处理结果。

失败时返回：
```json
{
  "error": "任务不存在或尚未完成"
}
```

或：
```json
{
  "error": "结果文件不存在"
}
```

### 8. 删除任务

删除任务及其相关文件，释放服务器存储空间。

#### 请求
```
DELETE /tasks/{task_id}
```

**参数**:
- `task_id`: 任务ID（路径参数）

#### 响应（成功）
```json
{
  "message": "任务及相关文件已删除"
}
```

#### 响应（任务不存在）
```json
{
  "error": "任务不存在"
}
```

## 使用示例

### 使用curl同步处理HTML文件

```bash
curl -X POST "http://localhost:8001/process-html" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@file1.html" \
  -F "files=@file2.html" \
  -F "model_type=node"
```

### 使用curl异步处理HTML文件

```bash
curl -X POST "http://localhost:8001/process-async" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@file1.html" \
  -F "files=@file2.html" \
  -F "model_type=node"
```

### 使用Python发送请求

```python
import requests

# 同步处理HTML文件
def process_html_files(html_files, model_type="node"):
    files = []
    for html_file in html_files:
        files.append(("files", (html_file.name, open(html_file, "rb"), "text/html")))
    
    response = requests.post(
        "http://localhost:8001/process-html",
        files=files,
        data={"model_type": model_type}
    )
    
    # 关闭文件
    for _, (_, file_obj, _) in files:
        file_obj.close()
    
    return response.json()

# 异步处理HTML文件
def process_html_async(html_files, model_type="node"):
    files = []
    for html_file in html_files:
        files.append(("files", (html_file.name, open(html_file, "rb"), "text/html")))
    
    response = requests.post(
        "http://localhost:8001/process-async",
        files=files,
        data={"model_type": model_type}
    )
    
    # 关闭文件
    for _, (_, file_obj, _) in files:
        file_obj.close()
    
    return response.json()

# 获取任务状态
def get_task_status(task_id):
    response = requests.get(f"http://localhost:8001/tasks/{task_id}")
    return response.json()

# 下载任务结果
def download_task_results(task_id, save_path):
    response = requests.get(f"http://localhost:8001/tasks/{task_id}/download", stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    return False
```

## 错误处理

所有API接口在发生错误时会返回适当的HTTP状态码和详细的错误信息。常见的错误代码包括：

- **404**: 请求的资源（如任务ID）不存在
- **500**: 服务器内部错误，如处理HTML时发生异常

## 最佳实践

1. 在处理大量文件时使用异步API (`/process-async`)
2. 定期检查任务状态，避免频繁轮询
3. 处理完成后，下载结果并删除任务，释放服务器资源
4. 启动服务前，使用`/check-model-server`确保模型服务器正在运行