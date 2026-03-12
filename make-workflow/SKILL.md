---
name: make-workflow
description: Make.com 工作流自动化执行技能。用于管理和运行 Make.com（原 Integromat）工作流。当用户需要执行 Make.com 工作流自动化、配置工作流映射、调用 Make API 运行工作流时使用此技能。支持从 URL 提取 zone 和 scenario_id，并通过配置文件管理 API Key 和工作流映射。
---

# Make Workflow Skill

## 概述

此技能用于执行 Make.com（原 Integromat）工作流。技能功能包括：
1. 智能解析 Make.com URL 并自动存储工作流配置
2. 从用户提供的链接中提取工作流名称和 ID
3. 从 OpenClaw 配置文件中读取 API Key（安全存储）
4. 调用 Make API 执行工作流
5. 返回执行结果

## 完整的交互流程

### 第一步：用户提供工作流链接

**用户操作**: 提供 Make.com 工作流链接
**助手操作**: 
1. 自动解析链接，提取 zone 和 scenario_id
2. 生成默认工作流名称（如"工作流_3983030"）
3. 存储到技能配置文件 (`config.json`)
4. 确认已记录，告知工作流名称

示例对话：
```
用户: https://us2.make.com/1801109/scenarios/3983030/edit
助手: 已解析此工作流链接，我将它命名为"播客记录"并存储到配置中。你可以使用"运行播客记录工作流"来执行它。
```

### 第二步：用户运行工作流

**用户操作**: 说"运行播客记录工作流"（或其他已存储的名称）
**助手操作**: 
1. 从技能配置文件查找工作流名称对应的 URL
2. 解析 URL 获取 zone 和 scenario_id
3. 从 OpenClaw 配置文件中读取 API Key (`plugins.external.make.api_key`)
4. 调用 Make API 执行工作流
5. 返回执行结果（执行ID和状态URL）

### 第三步：用户提供多个链接

用户可以提供多个链接，助手会自动命名并存储：
- 可以根据用途命名（如"播客记录"、"数据同步"等）
- 也可以根据用户指定的名称命名

## 快速开始

### 1. 配置 API Key

API Key 存储在 OpenClaw 配置文件 (`openclaw.json`) 的 `plugins.external.make.api_key` 字段中：

```json
{
  "plugins": {
    "external": {
      "make": {
        "api_key": "6350b215-2989-4050-b393-5f0e5d9c5d82"
      }
    }
  }
}
```

**注意**：API Key 不存储在 skill 配置中，这是安全设计。

### 2. 工作流配置自动管理

技能配置文件存储在 `config.json` 中，位于技能目录。配置包含：
- `workflows`: 工作流映射（名称 → URL）

配置文件示例：

```json
{
  "workflows": {
    "播客记录": "https://us2.make.com/1801109/scenarios/3983030/edit"
  }
}
```

配置文件由助手自动维护，无需手动编辑。

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

### 完整的用户交互流程

#### 1. 首次添加工作流（用户提供链接）

**用户操作**: 提供 Make.com 工作流链接
**助手操作**: 
1. 解析链接，提取工作流名称（可从链接中自动命名或用户指定）
2. 存储到配置文件中
3. 确认已记录，告知工作流名称

示例：
```
用户: https://us2.make.com/1801109/scenarios/3983030/edit
助手: 已解析此工作流链接，我将它命名为"播客记录"并存储到配置中。
```

#### 2. 执行工作流（用户指定名称）

**用户操作**: 说"运行播客工作流"
**助手操作**: 
1. 从配置文件中查找"播客记录"对应的 URL
2. 解析 URL 获取 zone 和 scenario_id
3. 从 OpenClaw 配置文件中读取 API Key
4. 调用 Make API 执行工作流
5. 返回执行结果

#### 3. 添加多个工作流（命名模式）

用户可以提供多个链接，助手会自动命名并存储：
- 可以根据用途命名（如"播客记录"、"数据同步"等）
- 也可以根据用户指定的名称命名

### 技能设计原则

1. **API Key 安全存储**: 始终存储在 OpenClaw 配置文件 (`plugins.external.make.api_key`) 中
2. **工作流配置分离**: 工作流名称和URL存储在技能配置文件 (`config.json`) 中
3. **自动记忆**: 用户只需提供一次链接，后续只需使用名称调用
4. **无需重复提供密钥**: 密钥已在配置中，无需每次提供

### API 响应处理

Make API 响应格式：
```json
{
  "executionId": "5f24046e1ef14fe48aa35f116bf4691a",
  "statusUrl": "https://us2.make.com/api/v2/scenarios/3983030/executions/5f24046e1ef14fe48aa35f116bf4691a"
}
```

成功执行后返回执行ID和状态URL，可以通过状态URL查看执行进度。

## 助手使用指南

### 当用户提供 Make.com 链接时

1. **使用 `parse-and-store.py` 脚本**：解析链接并自动存储
2. **或使用 `add-workflow.py` 脚本**：交互式添加工作流
3. **告知用户**：确认已存储，告知工作流名称

### 当用户要求运行工作流时

1. **使用 `run-workflow.py` 脚本**：执行指定名称的工作流
2. **检查配置文件**：确保工作流名称存在于 `config.json` 中
3. **返回结果**：提供执行ID和状态URL

## 技能配置

技能目录结构：
```
make-workflow/
├── SKILL.md (此文件)
├── config.json (配置文件 - 自动维护)
├── references/
│   ├── make-api.md (API 文档)
│   └── url-parsing.md (URL 解析规则)
├── scripts/
│   ├── run-workflow.py (执行工作流的脚本)
│   ├── add-workflow.py (添加新工作流的脚本)
│   └── parse-and-store.py (自动解析和存储的脚本)
```

## 核心设计原则

1. **API Key 安全存储**: 始终存储在 OpenClaw 配置文件 (`plugins.external.make.api_key`) 中，不在技能中硬编码
2. **工作流配置分离**: 工作流名称和URL存储在技能配置文件 (`config.json`) 中
3. **自动记忆**: 用户只需提供一次链接，后续只需使用名称调用
4. **无需重复提供密钥**: 密钥已在配置中，无需每次提供
5. **智能解析**: 自动从URL中提取工作流信息，无需用户手动配置

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