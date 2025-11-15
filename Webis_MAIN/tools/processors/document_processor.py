#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档处理器
处理 docx/txt/md 文件
"""

import logging
from typing import Dict, Union
from .base_processor import BaseFileProcessor

logger = logging.getLogger(__name__)


class DocumentProcessor(BaseFileProcessor):
    """文档处理器 - 处理 docx/txt/md 文件"""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = {'.docx', '.txt', '.md'}
    
    def get_processor_name(self) -> str:
        """获取处理器名称"""
        return "DocumentProcessor"
    
    def get_supported_extensions(self) -> set:
        """获取支持的文件扩展名"""
        return self.supported_extensions
    
    def extract_text(self, file_path: str) -> Dict[str, Union[str, bool]]:
        """
        抽取文档文本
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict包含: success(bool), text(str), error(str)
        """
        try:
            from langchain_community.document_loaders import Docx2txtLoader, TextLoader
            import pathlib
            
            ext = pathlib.Path(file_path).suffix.lower()
            
            if ext == ".docx":
                loader = Docx2txtLoader(file_path)
                docs = loader.load()
            elif ext in [".txt", ".md"]:
                loader = TextLoader(file_path, encoding="utf-8")
                docs = loader.load()
            else:
                return {"success": False, "text": "", "error": f"不支持的文件类型: {ext}"}
            
            # 合并所有文档内容
            text = "\n".join(doc.page_content for doc in docs).strip()
            
            logger.info(f"[DocumentProcessor] 成功处理文档: {file_path}, 文本长度: {len(text)}")
            return {"success": True, "text": text, "error": ""}
            
        except ImportError as e:
            error_msg = f"缺少依赖包: {str(e)}. 请安装: pip install langchain-community docx2txt"
            logger.error(f"[DocumentProcessor] {error_msg}")
            return {"success": False, "text": "", "error": error_msg}
        except Exception as e:
            error_msg = f"处理文档失败: {str(e)}"
            logger.error(f"[DocumentProcessor] 处理文档失败 {file_path}: {str(e)}")
            return {"success": False, "text": "", "error": error_msg}
