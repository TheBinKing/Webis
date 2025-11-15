#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理器模块
包含所有文件类型的处理器
"""

from .base_processor import BaseFileProcessor
from .document_processor import DocumentProcessor
from .pdf_processor import PDFProcessor
from .image_processor import ImageProcessor
from .html_processor import HTMLProcessor

__all__ = [
    'BaseFileProcessor',
    'DocumentProcessor', 
    'PDFProcessor',
    'ImageProcessor',
    'HTMLProcessor'
]
