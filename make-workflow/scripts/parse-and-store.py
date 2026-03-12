#!/usr/bin/env python3
"""
解析 Make.com URL 并存储到配置文件的脚本
"""

import json
import re
import sys
from pathlib import Path

# 配置文件路径
CONFIG_FILE = Path(__file__).parent.parent / "config.json"

def parse_make_url(url):
    """
    从 Make.com URL 提取 zone 和 scenario_id
    """
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
            if match.lastindex == 3:
                scenario_id = match.group(3)
            elif match.lastindex == 2:
                scenario_id = match.group(2)
            else:
                return None
            
            return {
                "zone": zone,
                "scenario_id": scenario_id
            }
    
    return None

def extract_workflow_name(url):
    """
    从 URL 中提取工作流名称
    可以基于场景ID或URL结构生成默认名称
    """
    parsed = parse_make_url(url)
    if parsed:
        scenario_id = parsed["scenario_id"]
        return f"工作流_{scenario_id}"
    return None

def add_workflow_to_config(workflow_name, url):
    """
    将工作流添加到配置文件
    """
    if not CONFIG_FILE.exists():
        # 创建默认配置
        config = {"workflows": {}}
    else:
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            config = {"workflows": {}}
    
    # 确保 workflows 字段存在
    if "workflows" not in config:
        config["workflows"] = {}
    
    # 添加工作流
    config["workflows"][workflow_name] = url
    
    # 保存配置
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False

def main():
    """
    命令行接口
    """
    if len(sys.argv) != 2:
        print("用法: python parse-and-store.py <Make.com URL>")
        return
    
    url = sys.argv[1]
    
    # 验证 URL
    parsed = parse_make_url(url)
    if not parsed:
        print("URL 格式无效，无法解析")
        return
    
    print(f"URL 解析成功:")
    print(f"  Zone: {parsed['zone']}")
    print(f"  Scenario ID: {parsed['scenario_id']}")
    
    # 生成默认名称或让用户指定
    default_name = extract_workflow_name(url)
    print(f"默认工作流名称: {default_name}")
    
    # 添加到配置
    if add_workflow_to_config(default_name, url):
        print(f"工作流 '{default_name}' 已成功添加到配置文件")
        print(f"后续你可以使用命令: '运行{default_name}工作流'")
    else:
        print("添加工作流失败")

if __name__ == "__main__":
    main()