#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：新增飞书多维表格记录
"""

import sys
import os
import json
from typing import Dict, Any

# 添加技能目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config_loader import get_feishu_credentials
    from bitable_api import FeishuBitableClient
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保在 D:\\OpenClaw\\workspace\\skills\\feishu-bitable 目录下运行")
    sys.exit(1)

def add_record_example():
    """新增记录示例"""
    try:
        # 获取凭证
        creds = get_feishu_credentials()
        client = FeishuBitableClient(creds['app_id'], creds['app_secret'])
        
        # 示例参数 - 需要用户提供的实际值
        app_token = "bascnXXX"  # 替换为实际的app_token
        table_id = "tblXXX"     # 替换为实际的table_id
        
        # 示例字段数据
        fields = {
            "姓名": "张三",
            "年龄": 25,
            "状态": "进行中",
            "创建时间": int(time.time() * 1000),  # 当前时间戳（毫秒）
            "负责人": [{"id": "ou_a784f196aeb82a69cc6d20a496d88382"}]  # 用户的open_id
        }
        
        print("正在添加记录...")
        result = client.add_record(app_token, table_id, fields)
        
        if result.get("code") == 0:
            record_id = result["data"]["record"]["record_id"]
            print(f"✅ 记录添加成功！记录ID: {record_id}")
            return result
        else:
            print(f"❌ 添加失败: {result.get('msg', '未知错误')}")
            return None
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

if __name__ == "__main__":
    import time
    add_record_example()