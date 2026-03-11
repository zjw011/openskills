# OpenSkills - OpenClaw 技能仓库

收集并分享 OpenClaw 使用的 AgentSkills。

## 📦 已收录技能

### 飞书多维表格 (feishu-bitable)

飞书多维表格操作技能，支持完整的 API 调用。

**功能：**
- ✅ 列出表格
- ✅ 获取表结构
- ✅ 读取记录
- ✅ 添加记录
- ✅ 更新记录
- ✅ 删除记录
- ✅ 批量操作

**安装：**
```bash
# 将技能目录复制到 OpenClaw skills 目录
cp -r feishu-bitable ~/.openclaw/skills/
```

**配置：**
在 `~/.openclaw/openclaw.json` 中配置飞书应用凭证：
```json
{
  "channels": {
    "feishu": {
      "appId": "cli_xxx",
      "appSecret": "xxx"
    }
  }
}
```

**使用示例：**
```json
{
  "action": "add_record",
  "app_token": "bascnXXX",
  "table_id": "tblXXX",
  "fields": {
    "姓名": "张三",
    "年龄": 25
  }
}
```

详细文档请查看 [feishu-bitable/SKILL.md](feishu-bitable/SKILL.md)

## 📝 技能结构

每个技能包含：
- `SKILL.md` - 技能说明文档（必需）
- `scripts/` - Python 脚本（可选）
- `references/` - 参考资料（可选）
- `assets/` - 资源文件（可选）

## 🤝 贡献

欢迎提交 PR 分享你的技能！

## 📄 许可证

MIT License
