#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feishu Bitable API Client
"""

import os
import json
import requests
import time
from typing import Dict, Optional, Any, List, Union

class FeishuBitableClient:
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expires_at = 0
        
    def _get_tenant_access_token(self) -> str:
        """获取 tenant_access_token"""
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
            
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                self.access_token = result["tenant_access_token"]
                # token有效期2小时，提前5分钟刷新
                self.token_expires_at = time.time() + 7200 - 300
                return self.access_token
            else:
                raise Exception(f"获取token失败: {result.get('msg', '未知错误')}")
        except Exception as e:
            raise Exception(f"获取token异常: {str(e)}")
    
    def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """通用请求方法"""
        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self._get_tenant_access_token()}"
        headers["Content-Type"] = "application/json; charset=utf-8"
        
        kwargs["headers"] = headers
        kwargs["timeout"] = 10
        
        try:
            if method.lower() == "get":
                response = requests.get(url, **kwargs)
            elif method.lower() == "post":
                response = requests.post(url, **kwargs)
            elif method.lower() == "put":
                response = requests.put(url, **kwargs)
            elif method.lower() == "delete":
                response = requests.delete(url, **kwargs)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
                
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response:
                try:
                    error_detail = e.response.json()
                    raise Exception(f"API请求失败 (状态码: {e.response.status_code}): {error_detail.get('msg', str(e))}")
                except:
                    raise Exception(f"API请求失败 (状态码: {e.response.status_code}): {str(e)}")
            else:
                raise Exception(f"网络请求异常: {str(e)}")
    
    def list_tables(self, app_token: str) -> Dict[str, Any]:
        """列出所有表格"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
        return self._make_request("GET", url)
    
    def get_table_schema(self, app_token: str, table_id: str) -> Dict[str, Any]:
        """获取表格结构"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        return self._make_request("GET", url)
    
    def list_records(self, app_token: str, table_id: str, 
                    view_id: Optional[str] = None,
                    page_size: int = 100,
                    page_token: Optional[str] = None) -> Dict[str, Any]:
        """列出记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        params = {"page_size": page_size}
        if view_id:
            params["view_id"] = view_id
        if page_token:
            params["page_token"] = page_token
            
        return self._make_request("GET", url, params=params)
    
    def search_records(self, app_token: str, table_id: str, 
                      filter_dict: Optional[Dict] = None) -> Dict[str, Any]:
        """搜索记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"
        data = {}
        if filter_dict:
            data["filter"] = filter_dict
            
        return self._make_request("POST", url, json=data)
    
    def add_record(self, app_token: str, table_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """添加记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        data = {"fields": fields}
        return self._make_request("POST", url, json=data)
    
    def update_record(self, app_token: str, table_id: str, 
                     record_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """更新记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
        data = {"fields": fields}
        return self._make_request("PUT", url, json=data)
    
    def delete_record(self, app_token: str, table_id: str, record_id: str) -> Dict[str, Any]:
        """删除记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
        return self._make_request("DELETE", url)
    
    def batch_add_records(self, app_token: str, table_id: str, records: List[Dict]) -> Dict[str, Any]:
        """批量添加记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch"
        data = {"records": [{"fields": r["fields"]} for r in records]}
        return self._make_request("POST", url, json=data)
    
    def batch_update_records(self, app_token: str, table_id: str, records: List[Dict]) -> Dict[str, Any]:
        """批量更新记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch"
        data = {"records": [{"record_id": r["record_id"], "fields": r["fields"]} for r in records]}
        return self._make_request("PUT", url, json=data)
    
    def batch_delete_records(self, app_token: str, table_id: str, record_ids: List[str]) -> Dict[str, Any]:
        """批量删除记录"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch"
        data = {"record_ids": record_ids}
        return self._make_request("DELETE", url, json=data)
    
    def create_bitable_app(self, name: str, folder_token: Optional[str] = None) -> Dict[str, Any]:
        """创建多维表格应用"""
        url = "https://open.feishu.cn/open-apis/drive/v1/files"
        data = {
            "name": name,
            "type": "bitable"
        }
        if folder_token:
            data["folder_token"] = folder_token
        return self._make_request("POST", url, json=data)
    
    def create_table(self, app_token: str, name: str, description: str = "") -> Dict[str, Any]:
        """创建表格"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
        data = {
            "name": name,
            "description": description
        }
        return self._make_request("POST", url, json=data)
    
    def add_field(self, app_token: str, table_id: str, 
                 field_name: str, field_type: int, 
                 options: Optional[List[str]] = None) -> Dict[str, Any]:
        """添加字段"""
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
        data = {
            "field_name": field_name,
            "type": field_type
        }
        if options:
            data["options"] = options
            
        return self._make_request("POST", url, json=data)


def main():
    """主函数用于测试"""
    # 从环境变量或配置文件获取配置
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not app_id or not app_secret:
        print("请设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET 环境变量")
        return
    
    client = FeishuBitableClient(app_id, app_secret)
    
    try:
        # 测试连接
        print("正在测试连接...")
        result = client.list_tables("bascnXXX")  # 这里需要替换为实际的app_token
        print(f"连接成功: {result}")
    except Exception as e:
        print(f"连接失败: {e}")


if __name__ == "__main__":
    main()