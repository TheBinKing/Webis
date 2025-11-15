#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF处理器
处理 PDF 文件
"""

import logging
from typing import Dict, Union
from .base_processor import BaseFileProcessor

logger = logging.getLogger(__name__)


class PDFProcessor(BaseFileProcessor):
    """PDF处理器 - 处理 PDF 文件"""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = {'.pdf'}
    
    def get_processor_name(self) -> str:
        """获取处理器名称"""
        return "PDFProcessor"
    
    def get_supported_extensions(self) -> set:
        """获取支持的文件扩展名"""
        return self.supported_extensions
    
    def extract_text(self, file_path: str) -> Dict[str, Union[str, bool]]:
        """
        抽取PDF文本
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            Dict包含: success(bool), text(str), error(str)
        """
        try:
            from langchain_community.document_loaders import PyPDFLoader
            
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            
            # 按页组织文本
            text_parts = []
            for i, doc in enumerate(docs, 1):
                page_text = doc.page_content.strip()
                if page_text:
                    text_parts.append(f"--- 第 {i} 页 ---\n{page_text}")
            
            text = "\n\n".join(text_parts)
            
            logger.info(f"[PDFProcessor] 成功处理PDF: {file_path}, 页数: {len(docs)}, 文本长度: {len(text)}")
            return {"success": True, "text": text, "error": ""}
            
        except ImportError as e:
            error_msg = f"缺少依赖包: {str(e)}. 请安装: pip install langchain-community pypdf"
            logger.error(f"[PDFProcessor] {error_msg}")
            return {"success": False, "text": "", "error": error_msg}
        except Exception as e:
            error_msg = f"处理PDF失败: {str(e)}"
            logger.error(f"[PDFProcessor] 处理PDF失败 {file_path}: {str(e)}")
            return {"success": False, "text": "", "error": error_msg}
