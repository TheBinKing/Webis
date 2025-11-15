#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础处理器接口
定义所有文件处理器的通用接口
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Union
import os
import pathlib


class BaseFileProcessor(ABC):
    """文件处理器基类 - 定义统一接口"""
    
    def __init__(self):
        self.supported_extensions = set()
    
    @abstractmethod
    def get_processor_name(self) -> str:
        """获取处理器名称"""
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> set:
        """获取支持的文件扩展名"""
        pass
    
    def can_process(self, file_path: str) -> bool:
        """
        判断是否支持该文件类型
        
        Args:
            file_path: 文件路径
            
        Returns:
            bool: 是否支持处理该文件
        """
        ext = pathlib.Path(file_path).suffix.lower()
        return ext in self.get_supported_extensions()
    
    def validate_file(self, file_path: str) -> Dict[str, Union[str, bool]]:
        """
        验证文件是否存在且可处理
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict: 验证结果
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": f"文件不存在: {file_path}"}
        
        if not self.can_process(file_path):
            ext = pathlib.Path(file_path).suffix.lower()
            return {"success": False, "error": f"不支持的文件类型: {ext}"}
        
        return {"success": True, "error": ""}
    
    @abstractmethod
    def extract_text(self, file_path: str) -> Dict[str, Union[str, bool]]:
        """
        抽取文件中的文本
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict包含: success(bool), text(str), error(str), processor(str)
        """
        pass
    
    def process_file(self, file_path: str) -> Dict[str, Union[str, bool]]:
        """
        完整的文件处理流程（包含验证）
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict包含: success(bool), text(str), error(str), processor(str)
        """
        # 验证文件
        validation = self.validate_file(file_path)
        if not validation["success"]:
            return {
                "success": False,
                "text": "",
                "error": validation["error"],
                "processor": self.get_processor_name()
            }
        
        # 处理文件
        result = self.extract_text(file_path)
        result["processor"] = self.get_processor_name()
        return result
