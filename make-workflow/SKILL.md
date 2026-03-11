---
name: make-workflow
description: Make.com 工作流自动化执行技能。用于管理和运行 Make.com（原 Integromat）工作流。当用户需要执行 Make.com 工作流自动化、配置工作流映射、调用 Make API 运行工作流时使用此技能。支持从 URL 提取 zone 和 scenario_id，并通过配置文件管理 API Key 和工作流映射。
---

# Make Workflow Skill

## 概述

此技能用于执行 Make.com（原 Integromat）工作流。技能功能包括：
1. 存储工作流配置（名称 → URL/Scenario ID）
2. 从 Make.com URL 解析 zone 和 scenario_id
3. 调用 Make API 执行工作流
4. 返回执行结果

## 快速开始

### 1. 配置工作流映射

技能配置文件存储在 `config.json` 中，位于技能目录。配置包含：
- `workflows`: 工作流映射（名称 → URL 或 scenario_id）

**注意**：API Key 不存储在 skill 配置中，需要通过 OpenClaw 配置文件管理。

默认配置示例：

```json
{
  "workflows": {
    "播客记录": "https://us2.make.com/1801109/scenarios/3983030/edit"
  }
}
```

### 2. URL 解析

Make.com URL 格式：
- `https://{zone}/{organization_id}/scenarios/{scenario_id}/edit`
- `https://{zone}/{organization_id}/scenarios/{scenario_id}`

解析规则：
- `zone`: URL 中的域名部分（如 `us2.make.com`）
- `scenario_id`: URL 中的数字标识符（如 `3983030`）
- `organization_id`: URL 中的组织标识符（如 `1801109`）

示例解析：
- URL: `https://us2.make.com/1801109/scenarios/3983030/edit`
- zone: `us2.make.com`
- scenario_id: `3983030`

### 3. API 调用

Make.com API 调用端点：
- `POST https://{zone}/api/v2/scenarios/{scenario_id}/run`

请求头：
```
Authorization: Token {api_key}
Content-Type: application/json
```

请求体：
```json
{}
```

## 使用方法

### 添加新的工作流

1. 编辑 `config.json` 文件：
```bash
edit skills/make-workflow/config.json
```

2. 在 `workflows` 对象中添加新的映射：
```json
{
  "api_key": "6350b215-2989-4050-b393-5f0e5d9c5d82",
  "workflows": {
    "播客记录": "https://us2.make.com/1801109/scenarios/3983030/edit",
    "新工作流": "https://{zone}/{organization_id}/scenarios/{scenario_id}/edit"
  }
}
```

### 执行工作流

用户示例：运行"播客记录"工作流 → 自动识别并执行

执行步骤：
1. 从配置中查找工作流名称对应的 URL
2. 解析 URL 获取 zone 和 scenario_id
3. 使用 API Key 调用 Make API
4. 返回执行结果

### API 响应处理

Make API 响应格式：
```json
{
  "data": {
    "id": "execution_id",
    "status": "success" | "error",
    "message": "Execution completed successfully"
  }
}
```

## 技能配置

技能目录结构：
```
make-workflow/
├── SKILL.md (此文件)
├── config.json (配置文件)
├── references/
│   ├── make-api.md (API 文档)
│   └── url-parsing.md (URL 解析规则)
├── scripts/
│   ├── run-workflow.py (执行工作流的脚本)
│   └── add-workflow.py (添加新工作流的脚本)
```

## 参考文档

详细 API 文档和 URL 解析规则请参见：
- `references/make-api.md`: Make.com API 完整文档
- `references/url-parsing.md`: URL 解析详细规则和示例

当需要了解 API 细节或解析复杂 URL 时，请读取这些参考文件。

## 注意事项

1. API Key 不要硬编码在技能代码中，始终存储在 `config.json` 中
2. 确保 URL 格式正确，否则解析会失败
3. API 调用可能需要等待工作流完成执行
4. 如果 API Key 失效，需要更新配置文件

## 错误处理

常见错误：
- `404 Not Found`: 工作流不存在或 URL 错误
- `401 Unauthorized`: API Key 无效
- `400 Bad Request`: 请求格式错误

处理方式：
1. 检查配置文件和 URL 格式
2. 验证 API Key 有效性
3. 重新配置或联系管理员