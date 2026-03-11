# Make.com URL 解析规则

## URL 格式

Make.com 工作流编辑页面的标准 URL 格式：

```
https://{zone}/{organization_id}/scenarios/{scenario_id}/edit
```

### 组成部分解析

| 部分 | 描述 | 示例 |
|------|------|------|
| `zone` | Make.com 数据中心域名 | `us2.make.com`, `eu1.make.com` |
| `organization_id` | 组织/账户标识符 | `1801109` |
| `scenario_id` | 工作流标识符 | `3983030` |
| `edit` | 页面类型（固定为 edit） | `edit` |

## 解析示例

### 示例 1：播客记录工作流

URL: `https://us2.make.com/1801109/scenarios/3983030/edit`

解析结果：
- `zone`: `us2.make.com`
- `organization_id`: `1801109`
- `scenario_id`: `3983030`

### 示例 2：欧洲数据中心工作流

URL: `https://eu1.make.com/123456/scenarios/789012/edit`

解析结果：
- `zone`: `eu1.make.com`
- `organization_id`: `123456`
- `scenario_id`: `789012`

## 解析算法

### Python 实现

```python
import re

def parse_make_url(url):
    # 正则表达式匹配 Make.com URL
    pattern = r'https://([^/]+)/(\d+)/scenarios/(\d+)/edit'
    match = re.match(pattern, url)
    
    if match:
        zone = match.group(1)
        organization_id = match.group(2)
        scenario_id = match.group(3)
        
        return {
            "zone": zone,
            "organization_id": organization_id,
            "scenario_id": scenario_id
        }
    else:
        return None
```

### JavaScript 实现

```javascript
function parseMakeUrl(url) {
    const pattern = /https:\/\/([^\/]+)\/(\d+)\/scenarios\/(\d+)\/edit/;
    const match = url.match(pattern);
    
    if (match) {
        return {
            zone: match[1],
            organization_id: match[2],
            scenario_id: match[3]
        };
    }
    return null;
}
```

## 常见问题

### 1. URL 格式变化

有时 URL 可能略有不同：
- `https://{zone}/{organization_id}/scenarios/{scenario_id}`（无 edit）
- `https://{zone}/scenarios/{scenario_id}/edit`（无 organization_id）

解析时应灵活处理，主要目标是提取 `zone` 和 `scenario_id`。

### 2. 域名变化

Make.com 可能有多个数据中心：
- `us2.make.com`（美国 2）
- `eu1.make.com`（欧洲 1）
- `us1.make.com`（美国 1）

### 3. 数字标识符格式

`organization_id` 和 `scenario_id` 都是数字，但长度可能不同：
- 通常是 6-8 位数字
- 不应包含字母或特殊字符

## 验证规则

### 有效 URL 检查

1. 必须以 `https://` 开头
2. 必须包含 `make.com` 域名或其变体
3. 必须包含 `/scenarios/` 路径
4. 必须包含数字标识符

### 错误示例

- `https://make.com/scenarios/123/edit`（缺少 zone）
- `https://us2.make.com/scenarios/edit`（缺少 scenario_id）
- `http://us2.make.com/1801109/scenarios/3983030/edit`（不是 HTTPS）

## 实用函数

### Python 完整解析函数

```python
import re

def extract_make_components(url):
    """
    从 Make.com URL 提取 zone 和 scenario_id
    返回：{"zone": zone, "scenario_id": scenario_id}
    """
    
    # 多种模式匹配
    patterns = [
        r'https://([^/]+)/(\d+)/scenarios/(\d+)/edit',
        r'https://([^/]+)/(\d+)/scenarios/(\d+)',
        r'https://([^/]+)/scenarios/(\d+)/edit',
        r'https://([^/]+)/scenarios/(\d+)'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            zone = match.group(1)
            # 尝试获取 scenario_id（可能是第2或第3组）
            if pattern.count('(\d+)') == 2:
                scenario_id = match.group(2)
            else:
                scenario_id = match.group(3)
            
            return {
                "zone": zone,
                "scenario_id": scenario_id
            }
    
    return None
```

## 使用建议

1. 在添加新工作流时，验证 URL 格式
2. 解析失败时提示用户检查 URL
3. 存储解析结果以便快速调用 API
4. 定期更新解析规则以适应 URL 格式变化