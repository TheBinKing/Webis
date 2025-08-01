# Webis 前端对接 API 文档

---

## 1. 上传并处理 HTML 文件（同步）

**接口路径**：`POST /api/process-html`

**参数（form-data）**
| 参数名      | 类型     | 必填 | 说明             |
| ----------- | -------- | ---- | ---------------- |
| files       | File[]   | 是   | HTML 文件列表    |
| tag_probs   | File     | 否   | 标签概率文件     |
| model_type  | string   | 否   | 模型类型，默认"node" |

**返回示例**
```json
{
  "task_id": "123456",
  "status": "completed",
  "result_count": 2,
  "message": "处理成功",
  "error": null
}
```

---

## 2. 上传并处理 HTML 文件（异步）

**接口路径**：`POST /api/process-async`

**参数（form-data）**
同上

**返回示例**
```json
{
  "task_id": "123456",
  "status": "pending",
  "result_count": 0,
  "message": "任务已提交，后台处理中",
  "error": null
}
```

---

## 3. 查询任务状态

**接口路径**：`GET /api/tasks/{task_id}`

**路径参数**
- `task_id`：任务ID

**返回示例**
```json
{
  "status": "completed",
  "message": "处理完成",
  "output_dir": "/path/to/output",
  "results": [ ... ],
  "error": null,
  "url": null,
  "title": null
}
```

---

## 4. 下载处理结果

**接口路径**：`GET /api/tasks/{task_id}/download`

**路径参数**
- `task_id`：任务ID

**返回**
- 下载 zip 文件，内容为处理结果

---

## 5. 删除任务

**接口路径**：`DELETE /api/tasks/{task_id}`

**路径参数**
- `task_id`：任务ID

**返回示例**
```json
{
  "message": "任务及相关文件已删除"
}
```

---

## 6. 通过 URL 处理网页

**接口路径**：`POST /api/process-url`

**参数（form-data 或 JSON）**
| 参数名     | 类型   | 必填 | 说明           |
| ---------- | ------ | ---- | -------------- |
| url        | string | 是   | 网页地址       |
| model_type | string | 否   | 模型类型，默认"node" |

**返回示例**
同“上传并处理 HTML 文件”返回

---

## 7. 通过 URL 抓取网页内容

**接口路径**：`GET /api/fetch-url`

**Query 参数**
| 参数名         | 类型    | 必填 | 说明           |
| -------------- | ------- | ---- | -------------- |
| url            | string  | 是   | 网页地址       |
| remove_scripts | boolean | 否   | 是否移除脚本，默认 true |
| remove_images  | boolean | 否   | 是否移除图片，默认 true |

**返回**
- 视后端实现，返回网页内容或 JSON

---

## 常见返回字段说明

| 字段         | 说明         |
| ------------ | ------------ |
| task_id      | 任务ID       |
| status       | 任务状态（pending/completed/failed）|
| result_count | 结果数量     |
| message      | 状态说明     |
| error        | 错误信息     |
| results      | 结果内容     |

---

如需详细字段说明、前端调用代码示例或接口联调支持，请随时告知！