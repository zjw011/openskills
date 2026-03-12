#!/usr/bin/env python3
"""
添加 Make.com 工作流脚本
"""

import json
import re
import sys
from pathlib import Path

# 配置文件路径
CONFIG_FILE = Path(__file__).parent.parent / "config.json"

def load_config():
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        # 创建默认配置
        default_config = {
            "api_key": "6350b215-2989-4050-b393-5f0e5d9c5d82",
            "workflows": {}
        }
        
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            
            return default_config
        except Exception as e:
            print(f"创建配置文件失败: {e}")
            return None
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"配置文件格式错误: {e}")
        return None

def validate_make_url(url):
    """
    验证 Make.com URL 格式
    
    返回:
    - 解析结果或 None
    """
    # 正则表达式匹配多种 URL 格式
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
                return {
                    "valid": False,
                    "error": "无法解析 URL"
                }
            
            return {
                "zone": zone,
                "scenario_id": scenario_id,
                "valid": True
            }
    
    return {
        "valid": False,
        "error": "URL 格式不符合 Make.com 工作流 URL 格式"
    }

def add_workflow_interactive():
    """
    交互式添加工作流
    """
    config = load_config()
    if config is None:
        print("无法加载配置，退出")
        return
    
    print("当前工作流列表:")
    workflows = config.get("workflows", {})
    for name, url in workflows.items():
        print(f"  {name}: {url}")
    
    print("\n添加新工作流:")
    
    workflow_name = input("工作流名称: ")
    if workflow_name in workflows:
        print(f"工作流 '{workflow_name}' 已存在，请使用不同的名称")
        return
    
    url = input("Make.com URL: ")
    
    # 验证 URL
    validation_result = validate_make_url(url)
    if not validation_result["valid"]:
        print(f"URL 验证失败: {validation_result['error']}")
        return
    
    print(f"URL 解析成功:")
    print(f"  Zone: {validation_result['zone']}")
    print(f"  Scenario ID: {validation_result['scenario_id']}")
    
    # 添加到配置
    workflows[workflow_name] = url
    
    # 保存配置
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"\n工作流 '{workflow_name}' 已成功添加到配置文件")
    except Exception as e:
        print(f"保存配置失败: {e}")

def main():
    """
    命令行接口
    """
    if len(sys.argv) == 1:
        add_workflow_interactive()
    elif len(sys.argv) == 3:
        workflow_name = sys.argv[1]
        url = sys.argv[2]
        
        config = load_config()
        if config is None:
            print("无法加载配置")
            return
        
        workflows = config.get("workflows", {})
        
        if workflow_name in workflows:
            print(f"工作流 '{workflow_name}' 已存在")
            return
        
        validation_result = validate_make_url(url)
        if not validation_result["valid"]:
            print(f"URL 验证失败: {validation_result['error']}")
            return
        
        workflows[workflow_name] = url
        
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"工作流 '{workflow_name}' 已添加")
        except Exception as e:
            print(f"保存配置失败: {e}")
    else:
        print("用法:")
        print("  python add-workflow.py")
        print("  python add-workflow.py <工作流名称> <URL>")

if __name__ == "__main__":
    main()