#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML Processor (集成 Webis_HTML API)
依赖: requests, Webis_HTML API server (默认 http://localhost:9000)
"""

from typing import Dict, Union, Set
from .base_processor import BaseFileProcessor
import os
import requests

class HTMLProcessor(BaseFileProcessor):
    """HTML 文件处理器 (基于 Webis_HTML API)"""
    def __init__(self, api_url: str = "http://localhost:9000"):
        super().__init__()
        self.supported_extensions = {".html", ".htm"}
        self.api_url = api_url.rstrip("/")
    
    def get_processor_name(self) -> str:
        return "HTMLProcessor"
    
    def get_supported_extensions(self) -> Set[str]:
        return self.supported_extensions
    
    def extract_text(self, file_path: str) -> Dict[str, Union[str, bool]]:
        if not os.path.exists(file_path):
            return {"success": False, "text": "", "error": f"文件不存在: {file_path}"}
        try:
            with open(file_path, "rb") as f:
                files = {"files": (os.path.basename(file_path), f, "text/html")}
                data = {"model_type": "node"}
                resp = requests.post(f"{self.api_url}/extract/process-html",
                                     files=files, data=data, timeout=60)
            if resp.status_code != 200:
                return {"success": False, "text": "", "error": f"提交失败: {resp.status_code} {resp.text}"}
            result = resp.json()
            task_id = result.get("task_id")
            if not task_id:
                return {"success": False, "text": "", "error": "未返回 task_id"}
            detail = requests.get(f"{self.api_url}/tasks/{task_id}", timeout=60).json()
            results = detail.get("results", [])
            if not results:
                return {"success": False, "text": "", "error": "任务无结果"}
            first = results[0]
            return {
                "success": True,
                "text": first.get("content", ""),
                "error": "",
                "meta": first.get("meta", {}),
                "links": first.get("links", []),
                "images": first.get("images", [])
            }
        except Exception as e:
            return {"success": False, "text": "", "error": f"处理失败: {e}"}
