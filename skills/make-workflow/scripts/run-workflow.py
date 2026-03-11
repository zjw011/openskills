#!/usr/bin/env python3
"""
Make.com 工作流执行脚本
"""

import requests
import json
import re
import sys
import os
from pathlib import Path

# 配置文件路径
CONFIG_FILE = Path(__file__).parent.parent / "config.json"

def load_config():
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        print(f"配置文件不存在: {CONFIG_FILE}")
        return None
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"配置文件格式错误: {e}")
        return None

def parse_make_url(url):
    """
    从 Make.com URL 提取 zone 和 scenario_id
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
            # 尝试获取 scenario_id
            if pattern.count('(\d+)') == 2:
                scenario_id = match.group(2)
            else:
                scenario_id = match.group(3)
            
            return {
                "zone": zone,
                "scenario_id": scenario_id
            }
    
    return None

def run_workflow(workflow_name, config=None):
    """
    执行指定的工作流
    
    参数:
    - workflow_name: 工作流名称（config.json 中的键）
    - config: 配置数据（如果为 None 则从文件加载）
    
    返回:
    - API 响应数据或错误信息
    """
    if config is None:
        config = load_config()
        if config is None:
            return {"error": "无法加载配置文件"}
    
    api_key = config.get("api_key")
    workflows = config.get("workflows", {})
    
    if not api_key:
        return {"error": "配置文件缺少 api_key"}
    
    if workflow_name not in workflows:
        return {"error": f"工作流 '{workflow_name}' 不存在"}
    
    url = workflows[workflow_name]
    parsed = parse_make_url(url)
    
    if not parsed:
        return {"error": f"无法解析 URL: {url}"}
    
    zone = parsed["zone"]
    scenario_id = parsed["scenario_id"]
    
    # 调用 Make API
    api_url = f"https://{zone}/api/v2/scenarios/{scenario_id}/run"
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json"
    }
    payload = {}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        
        if response.status_code in [200, 202]:
            return response.json()
        else:
            return {
                "error": f"API 调用失败 (状态码: {response.status_code})",
                "details": response.text
            }
    except requests.exceptions.RequestException as e:
        return {"error": f"网络请求错误: {e}"}

def add_workflow(workflow_name, url, config=None):
    """
    添加新的工作流到配置文件
    
    参数:
    - workflow_name: 工作流名称
    - url: Make.com URL
    - config: 配置数据（如果为 None 则从文件加载）
    
    返回:
    - 更新后的配置或错误信息
    """
    if config is None:
        config = load_config()
        if config is None:
            return {"error": "无法加载配置文件"}
    
    # 验证 URL 格式
    parsed = parse_make_url(url)
    if not parsed:
        return {"error": f"URL 格式无效: {url}"}
    
    # 添加到配置
    config["workflows"][workflow_name] = url
    
    # 保存配置
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return {"success": f"工作流 '{workflow_name}' 已添加", "config": config}
    except Exception as e:
        return {"error": f"保存配置失败: {e}"}

def main():
    """
    命令行接口
    """
    if len(sys.argv) < 2:
        print("用法:")
        print("  python run-workflow.py <工作流名称>")
        print("  python run-workflow.py add <名称> <URL>")
        return
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) != 4:
            print("用法: python run-workflow.py add <工作流名称> <URL>")
            return
        
        workflow_name = sys.argv[2]
        url = sys.argv[3]
        result = add_workflow(workflow_name, url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        workflow_name = command
        result = run_workflow(workflow_name)
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()