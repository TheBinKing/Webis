
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一文件处理接口
支持文档、PDF、图片三种模态的文本抽取
"""

import os
import pathlib
from typing import Dict, List, Optional, Union
import logging

# 导入处理器模块
from processors import DocumentProcessor, PDFProcessor, ImageProcessor, BaseFileProcessor,HTMLProcessor

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessorRegistry:
    """处理器注册中心 - 管理所有处理器"""
    
    def __init__(self):
        self.processors = []
        self._register_default_processors()
    
    def _register_default_processors(self):
        """注册默认处理器"""
        self.register_processor(DocumentProcessor())
        self.register_processor(PDFProcessor())
        self.register_processor(ImageProcessor())
        self.register_processor(HTMLProcessor())
    
    def register_processor(self, processor: BaseFileProcessor):
        """
        注册新的处理器
        
        Args:
            processor: 继承自BaseFileProcessor的处理器实例
        """
        if not isinstance(processor, BaseFileProcessor):
            raise TypeError("处理器必须继承自BaseFileProcessor")
        
        self.processors.append(processor)
        logger.info(f"已注册处理器: {processor.get_processor_name()}")
    
    def get_processor_for_file(self, file_path: str) -> Optional[BaseFileProcessor]:
        """
        根据文件路径获取合适的处理器
        
        Args:
            file_path: 文件路径
            
        Returns:
            BaseFileProcessor or None: 匹配的处理器或None
        """
        for processor in self.processors:
            if processor.can_process(file_path):
                return processor
        return None
    
    def get_supported_extensions(self) -> Dict[str, List[str]]:
        """获取所有处理器支持的文件扩展名"""
        extensions = {}
        for processor in self.processors:
            processor_name = processor.get_processor_name().replace("Processor", "").lower()
            extensions[processor_name] = list(processor.get_supported_extensions())
        return extensions
    
    def list_processors(self) -> List[str]:
        """列出所有已注册的处理器"""
        return [processor.get_processor_name() for processor in self.processors]


class UnifiedFileProcessor:
    """统一文件处理器 - 自动判断文件类型并调用对应处理器"""
    
    def __init__(self, registry: Optional[ProcessorRegistry] = None):
        self.registry = registry or ProcessorRegistry()
    
    def register_processor(self, processor: BaseFileProcessor):
        """
        注册新的处理器
        
        Args:
            processor: 继承自BaseFileProcessor的处理器实例
        """
        self.registry.register_processor(processor)
    
    def get_file_type(self, file_path: str) -> str:
        """
        判断文件类型
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 处理器类型名称或'unknown'
        """
        processor = self.registry.get_processor_for_file(file_path)
        if processor:
            return processor.get_processor_name().replace("Processor", "").lower()
        return 'unknown'
    
    def get_processor_name(self, file_path: str) -> str:
        """
        获取处理器名称
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 处理器名称或'unknown'
        """
        processor = self.registry.get_processor_for_file(file_path)
        return processor.get_processor_name() if processor else 'unknown'
    
    def extract_text(self, file_path: str) -> Dict[str, Union[str, bool]]:
        """
        统一文本抽取接口
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict包含: success(bool), text(str), error(str), file_type(str), processor(str)
        """
        processor = self.registry.get_processor_for_file(file_path)
        
        if not processor:
            ext = pathlib.Path(file_path).suffix.lower()
            return {
                "success": False, 
                "text": "", 
                "error": f"不支持的文件类型: {ext}",
                "file_type": "unknown",
                "processor": "unknown"
            }
        
        # 使用处理器处理文件
        result = processor.process_file(file_path)
        result["file_type"] = self.get_file_type(file_path)
        
        return result
    
    def get_supported_extensions(self) -> Dict[str, List[str]]:
        """获取支持的文件扩展名"""
        return self.registry.get_supported_extensions()
    
    def list_processors(self) -> List[str]:
        """列出所有已注册的处理器"""
        return self.registry.list_processors()


# 便捷函数
def extract_text_from_file(file_path: str) -> Dict[str, Union[str, bool]]:
    """
    便捷函数：从文件抽取文本
    
    Args:
        file_path: 文件路径
        
    Returns:
        Dict包含: success(bool), text(str), error(str), file_type(str)
    """
    processor = UnifiedFileProcessor()
    return processor.extract_text(file_path)


def batch_extract_text(file_paths: List[str]) -> Dict[str, Dict[str, Union[str, bool]]]:
    """
    批量抽取文本
    
    Args:
        file_paths: 文件路径列表
        
    Returns:
        Dict[文件路径, 抽取结果]
    """
    processor = UnifiedFileProcessor()
    results = {}
    
    for file_path in file_paths:
        results[file_path] = processor.extract_text(file_path)
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("统一文件处理器 v2.0")
        print("=" * 40)
        print("用法: python file_processor.py <文件路径>")
        print()
        
        processor = UnifiedFileProcessor()
        print("已注册的处理器:")
        for proc_name in processor.list_processors():
            print(f"  • {proc_name}")
        print()
        
        print("支持的文件类型:")
        for category, exts in processor.get_supported_extensions().items():
            print(f"  {category}: {', '.join(exts)}")
        print()
        print("示例:")
        print("  python file_processor.py document.pdf")
        print("  python file_processor.py image.png")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = extract_text_from_file(file_path)
    
    if result["success"]:
        print(f"✓ 处理成功")
        print(f"文件类型: {result['file_type']}")
        print(f"处理器: {result['processor']}")
        print(f"文本长度: {len(result['text'])} 字符")
        print("-" * 50)
        print(result["text"])
    else:
        print(f"✗ 处理失败")
        print(f"文件类型: {result.get('file_type', 'unknown')}")
        print(f"处理器: {result.get('processor', 'unknown')}")
        print(f"错误信息: {result['error']}")
