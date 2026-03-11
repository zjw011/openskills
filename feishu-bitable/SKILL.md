---
name: feishu-bitable
description: |
  Feishu Bitable (多维表格) operations including creating tables, listing tables, reading records, adding records, updating records, and deleting records. Use when user needs to work with Feishu Bitable databases: (1) Create new bitable apps or tables, (2) List tables in a bitable app, (3) Read/query records from tables, (4) Add new records to tables, (5) Update existing records, (6) Delete records.
---

# Feishu Bitable Tool

Single tool `feishu_bitable` with action parameter for all bitable operations.

## Authentication

Uses Feishu app credentials from config:
- `channels.feishu.appId`
- `channels.feishu.appSecret`

Gets `tenant_access_token` automatically for API calls.

## Token Extraction

### App Token (app_token)

From URL `https://xxx.feishu.cn/base/ABC123` → `app_token` = `ABC123`

From wiki URL `https://xxx.feishu.cn/wiki/XXX` → Need to call wiki API to get bitable app_token.

### Table ID (table_id)

From URL `https://xxx.feishu.cn/base/ABC123?table=tblXXX` → `table_id` = `tblXXX`

Or use `list_tables` action to get all tables.

### Record ID (record_id)

Returned from `add_record`, `list_records`, or `search_records` actions.

## Actions

### List Tables

List all tables in a bitable app:

```json
{
  "action": "list_tables",
  "app_token": "bascnXXX"
}
```

### Get Table Schema

Get fields/schema of a table:

```json
{
  "action": "get_table_schema",
  "app_token": "bascnXXX",
  "table_id": "tblXXX"
}
```

### List Records

Read records from a table:

```json
{
  "action": "list_records",
  "app_token": "bascnXXX",
  "table_id": "tblXXX"
}
```

With filters and pagination:

```json
{
  "action": "list_records",
  "app_token": "bascnXXX",
  "table_id": "tblXXX",
  "view_id": "vewXXX",
  "page_size": 100,
  "page_token": "..."
}
```

### Search Records

Search records with filter conditions:

```json
{
  "action": "search_records",
  "app_token": "bascnXXX",
  "table_id": "tblXXX",
  "filter": {
    "conjunction": "and",
    "conditions": [
      {
        "field_name": "Status",
        "operator": "is",
        "value": "Done"
      }
    ]
  }
}
```

### Add Record

Add a new record to a table:

```json
{
  "action": "add_record",
  "app_token": "bascnXXX",
  "table_id": "tblXXX",
  "fields": {
    "Name": "张三",
    "Age": 25,
    "Status": "Active"
  }
}
```

Field types:
- **Text**: String value
- **Number**: Numeric value
- **Single Select**: String (option name)
- **Multi Select**: Array of strings
- **Date**: Milliseconds timestamp
- **Checkbox**: Boolean (true/false)
- **Person**: Array of objects with `id` field (open_id/union_id/user_id)
- **Phone**: String
- **URL**: Object with `text` and `link`
- **Attachment**: Array of file tokens (upload first)

### Update Record

Update an existing record:

```json
{
  "action": "update_record",
  "app_token": "bascnXXX",
  "table_id": "tblXXX",
  "record_id": "recXXX",
  "fields": {
    "Status": "Completed"
  }
}
```

### Delete Record

Delete a record:

```json
{
  "action": "delete_record",
  "app_token": "bascnXXX",
  "table_id": "tblXXX",
  "record_id": "recXXX"
}
```

### Batch Add Records

Add multiple records at once:

```json
{
  "action": "batch_add_records",
  "app_token": "bascnXXX",
  "table_id": "tblXXX",
  "records": [
    { "fields": { "Name": "张三", "Age": 25 } },
    { "fields": { "Name": "李四", "Age": 30 } }
  ]
}
```

### Batch Update Records

Update multiple records at once:

```json
{
  "action": "batch_update_records",
  "app_token": "bascnXXX",
  "table_id": "tblXXX",
  "records": [
    { "record_id": "recXXX", "fields": { "Status": "Done" } },
    { "record_id": "recYYY", "fields": { "Status": "Done" } }
  ]
}
```

### Batch Delete Records

Delete multiple records at once:

```json
{
  "action": "batch_delete_records",
  "app_token": "bascnXXX",
  "table_id": "tblXXX",
  "record_ids": ["recXXX", "recYYY", "recZZZ"]
}
```

### Create Bitable App

Create a new bitable app (database):

```json
{
  "action": "create_bitable",
  "name": "项目管理",
  "folder_token": "fldcnXXX"
}
```

Without folder_token creates in root (may fail for bots).

### Create Table

Create a new table in a bitable app:

```json
{
  "action": "create_table",
  "app_token": "bascnXXX",
  "name": "任务列表",
  "description": "项目任务跟踪"
}
```

### Add Field

Add a new field to a table:

```json
{
  "action": "add_field",
  "app_token": "bascnXXX",
  "table_id": "tblXXX",
  "field_name": "优先级",
  "field_type": 3
}
```

Field types:
- 1: Text
- 2: Number
- 3: Single Select
- 4: Multi Select
- 5: Date
- 7: Checkbox
- 11: Person
- 13: Phone
- 15: URL
- 17: Attachment
- 18: Linked Record
- 20: Formula
- 21: Lookup
- 22: Auto Number

## Configuration

```yaml
channels:
  feishu:
    tools:
      bitable: true  # default: true
```

## Permissions

Required:
- `bitable:app` - Full access to bitable apps
- `bitable:app:readonly` - Read-only access
- `drive:drive` - For creating bitable apps

## Scripts

Use `scripts/bitable_api.py` for direct API calls when needed.
