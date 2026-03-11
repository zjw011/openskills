# Make.com API 文档

## 概述

Make.com（原 Integromat）提供 API 用于自动化执行工作流（scenarios）。此文档详细说明 API 使用方法。

## API 端点

### 执行工作流
- **URL**: `POST https://{zone}/api/v2/scenarios/{scenario_id}/run`
- **zone**: Make.com 数据中心域名（如 `us2.make.com`, `eu1.make.com` 等）
- **scenario_id**: 工作流 ID（数字标识符）

### 获取执行状态
- **URL**: `GET https://{zone}/api/v2/scenarios/{scenario_id}/executions/{execution_id}`

### 获取工作流信息
- **URL**: `GET https://{zone}/api/v2/scenarios/{scenario_id}`

## 请求头

所有 API 请求都需要以下头信息：

```http
Authorization: Token {api_key}
Content-Type: application/json
```

## 请求体格式

### 执行工作流请求体

```json
{}
```

`data` 字段可以包含传递给工作流的输入数据。对于简单的工作流执行，通常为空对象。

### 示例请求

```bash
curl -X POST "https://us2.make.com/api/v2/scenarios/3983030/execute" \
  -H "Authorization: Bearer 6350b215-2989-4050-b393-5f0e5d9c5d82" \
  -H "Content-Type: application/json" \
  -d '{"data": {}}'
```

## 响应格式

### 成功执行响应

```json
{
  "data": {
    "id": "123456789",
    "status": "success",
    "message": "Execution completed successfully",
    "createdAt": "2026-03-11T15:12:00Z",
    "finishedAt": "2026-03-11T15:12:30Z"
  }
}
```

### 错误响应

```json
{
  "error": {
    "code": 401,
    "message": "Unauthorized",
    "details": "Invalid API key"
  }
}
```

## 常见状态码

- `200`: 成功
- `201`: 创建成功（执行启动）
- `400`: 错误请求（参数错误）
- `401`: 未授权（API Key 无效）
- `404`: 未找到（工作流不存在）
- `429`: 请求过多（速率限制）
- `500`: 服务器内部错误

## 速率限制

Make.com API 有速率限制：
- 免费账户：每分钟 10 次请求
- 付费账户：根据套餐不同，限制更高

## 注意事项

1. API Key 可以从 Make.com 账户设置中获取
2. 执行工作流可能需要等待完成，API 返回的是执行 ID
3. 复杂工作流可能需要传递输入数据到 `data` 字段
4. 确保 zone 正确（取决于账户注册的数据中心）

## 示例代码

### Python 执行工作流

```python
import requests

def run_make_scenario(zone, scenario_id, api_key, data={}):
    url = f"https://{zone}/api/v2/scenarios/{scenario_id}/run"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json={})
    return response.json()
```