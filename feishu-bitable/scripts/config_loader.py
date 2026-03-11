#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration loader for Feishu Bitable
"""

import json
import os
from typing import Dict, Optional

def load_feishu_config() -> Dict[str, str]:
    """从OpenClaw配置中加载飞书配置"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 提取飞书配置
        feishu_config = config.get('channels', {}).get('feishu', {})
        
        return {
            'app_id': feishu_config.get('appId'),
            'app_secret': feishu_config.get('appSecret')
        }
    except Exception as e:
        raise Exception(f"加载飞书配置失败: {str(e)}")

def get_feishu_credentials() -> Dict[str, str]:
    """获取飞书凭证，优先从环境变量，其次从配置文件"""
    app_id = os.getenv('FEISHU_APP_ID')
    app_secret = os.getenv('FEISHU_APP_SECRET')
    
    if app_id and app_secret:
        return {'app_id': app_id, 'app_secret': app_secret}
    
    # 从配置文件加载
    config = load_feishu_config()
    if config.get('app_id') and config.get('app_secret'):
        return config
    
    raise Exception("未找到飞书APP ID和APP Secret配置，请设置环境变量或检查openclaw.json配置")

if __name__ == "__main__":
    try:
        creds = get_feishu_credentials()
        print("飞书配置加载成功:")
        print(f"APP_ID: {creds['app_id']}")
        print(f"APP_SECRET: {creds['app_secret']}")
    except Exception as e:
        print(f"错误: {e}")