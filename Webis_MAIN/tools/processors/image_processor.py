#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片OCR处理器
处理图片文件并进行文字识别
"""

import logging
from typing import Dict, Union
from .base_processor import BaseFileProcessor

logger = logging.getLogger(__name__)


class ImageProcessor(BaseFileProcessor):
    """图片OCR处理器 - 使用EasyOCR"""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
        self._reader = None
    
    def get_processor_name(self) -> str:
        """获取处理器名称"""
        return "ImageProcessor"
    
    def get_supported_extensions(self) -> set:
        """获取支持的文件扩展名"""
        return self.supported_extensions
    
    def _get_reader(self):
        """延迟加载EasyOCR，避免启动时加载模型"""
        if self._reader is None:
            try:
                import easyocr
                logger.info("[ImageProcessor] 正在初始化EasyOCR模型...")
                self._reader = easyocr.Reader(['ch_sim', 'en'])
                logger.info("[ImageProcessor] EasyOCR模型初始化完成")
            except ImportError:
                raise ImportError("请安装easyocr: pip install easyocr")
        return self._reader
    
    def extract_text(self, file_path: str) -> Dict[str, Union[str, bool]]:
        """
        抽取图片中的文字
        
        Args:
            file_path: 图片文件路径
            
        Returns:
            Dict包含: success(bool), text(str), error(str)
        """
        try:
            reader = self._get_reader()
            results = reader.readtext(file_path)
            
            # 提取所有识别的文字
            text_lines = []
            for (bbox, text, confidence) in results:
                if confidence > 0.5:  # 过滤低置信度结果
                    text_lines.append(text.strip())
            
            text = "\n".join(text_lines)
            
            logger.info(f"[ImageProcessor] 成功处理图片: {file_path}, 识别到 {len(text_lines)} 行文字, 文本长度: {len(text)}")
            return {"success": True, "text": text, "error": ""}
            
        except ImportError as e:
            error_msg = f"缺少依赖包: {str(e)}. 请安装: pip install easyocr"
            logger.error(f"[ImageProcessor] {error_msg}")
            return {"success": False, "text": "", "error": error_msg}
        except Exception as e:
            error_msg = f"处理图片失败: {str(e)}"
            logger.error(f"[ImageProcessor] 处理图片失败 {file_path}: {str(e)}")
            return {"success": False, "text": "", "error": error_msg}
