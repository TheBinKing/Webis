#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
带输出功能的统一文件处理器
支持将处理结果保存到输出文件夹
"""

import os
import pathlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Union
import logging

# 导入处理器模块
from processors import DocumentProcessor, PDFProcessor, ImageProcessor, BaseFileProcessor, HTMLProcessor
from file_processor import UnifiedFileProcessor, ProcessorRegistry

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileProcessorWithOutput(UnifiedFileProcessor):
    """带输出功能的统一文件处理器"""
    
    def __init__(self, output_dir: str = "outputs", registry: Optional[ProcessorRegistry] = None):
        super().__init__(registry)
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """确保输出目录存在"""
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"输出目录设置为: {os.path.abspath(self.output_dir)}")
    
    def _generate_output_filename(self, input_path: str, suffix: str = "") -> str:
        """
        生成输出文件名
        
        Args:
            input_path: 输入文件路径
            suffix: 文件名后缀
            
        Returns:
            str: 输出文件路径
        """
        input_file = pathlib.Path(input_path)
        base_name = input_file.stem  # 不含扩展名的文件名
        
        if suffix:
            output_name = f"{base_name}_{suffix}.txt"
        else:
            output_name = f"{base_name}.txt"
        
        return os.path.join(self.output_dir, output_name)
    
    def process_file_with_output(self, file_path: str, save_output: bool = True, 
                                include_metadata: bool = True) -> Dict[str, Union[str, bool]]:
        """
        处理文件并可选择性保存输出
        
        Args:
            file_path: 输入文件路径
            save_output: 是否保存输出到文件
            include_metadata: 是否包含元数据
            
        Returns:
            Dict: 处理结果，包含输出文件路径信息
        """
        # 调用父类的处理方法
        result = self.extract_text(file_path)
        
        # 添加处理时间戳
        result["processed_at"] = datetime.now().isoformat()
        result["input_file"] = os.path.abspath(file_path)
        
        if save_output and result["success"]:
            try:
                # 生成输出文件路径
                output_path = self._generate_output_filename(file_path)
                
                # 准备要保存的内容
                content_to_save = []
                
                if include_metadata:
                    content_to_save.extend([
                        f"=== 文件处理结果 ===",
                        f"输入文件: {result['input_file']}",
                        f"文件类型: {result['file_type']}",
                        f"处理器: {result['processor']}",
                        f"处理时间: {result['processed_at']}",
                        f"文本长度: {len(result['text'])} 字符",
                        f"",
                        f"=== 抽取内容 ===",
                        f""
                    ])
                
                content_to_save.append(result['text'])
                
                # 保存到文件
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(content_to_save))
                
                result["output_file"] = os.path.abspath(output_path)
                logger.info(f"结果已保存到: {output_path}")
                
            except Exception as e:
                logger.error(f"保存输出文件失败: {str(e)}")
                result["output_error"] = str(e)
        
        return result
    
    def batch_process_with_output(self, file_paths: List[str], save_output: bool = True,
                                 include_metadata: bool = True) -> Dict[str, Dict[str, Union[str, bool]]]:
        """
        批量处理文件并保存输出
        
        Args:
            file_paths: 文件路径列表
            save_output: 是否保存输出
            include_metadata: 是否包含元数据
            
        Returns:
            Dict[文件路径, 处理结果]
        """
        results = {}
        summary = {
            "total_files": len(file_paths),
            "successful": 0,
            "failed": 0,
            "output_files": []
        }
        
        for file_path in file_paths:
            result = self.process_file_with_output(file_path, save_output, include_metadata)
            results[file_path] = result
            
            if result["success"]:
                summary["successful"] += 1
                if "output_file" in result:
                    summary["output_files"].append(result["output_file"])
            else:
                summary["failed"] += 1
        
        # 保存批量处理摘要
        if save_output:
            summary_path = os.path.join(self.output_dir, f"batch_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            try:
                with open(summary_path, 'w', encoding='utf-8') as f:
                    json.dump(summary, f, ensure_ascii=False, indent=2)
                logger.info(f"批量处理摘要已保存到: {summary_path}")
            except Exception as e:
                logger.error(f"保存摘要文件失败: {str(e)}")
        
        return results
    
    def clear_output_dir(self):
        """清空输出目录"""
        if os.path.exists(self.output_dir):
            import shutil
            shutil.rmtree(self.output_dir)
            self._ensure_output_dir()
            logger.info(f"已清空输出目录: {self.output_dir}")


# 便捷函数
def process_file_with_output(file_path: str, output_dir: str = "outputs", 
                           save_output: bool = True, include_metadata: bool = True) -> Dict[str, Union[str, bool]]:
    """
    便捷函数：处理文件并保存输出
    
    Args:
        file_path: 文件路径
        output_dir: 输出目录
        save_output: 是否保存输出
        include_metadata: 是否包含元数据
        
    Returns:
        Dict: 处理结果
    """
    processor = FileProcessorWithOutput(output_dir)
    return processor.process_file_with_output(file_path, save_output, include_metadata)


def batch_process_with_output(file_paths: List[str], output_dir: str = "outputs",
                            save_output: bool = True, include_metadata: bool = True) -> Dict[str, Dict[str, Union[str, bool]]]:
    """
    便捷函数：批量处理文件并保存输出
    
    Args:
        file_paths: 文件路径列表
        output_dir: 输出目录
        save_output: 是否保存输出
        include_metadata: 是否包含元数据
        
    Returns:
        Dict[文件路径, 处理结果]
    """
    processor = FileProcessorWithOutput(output_dir)
    return processor.batch_process_with_output(file_paths, save_output, include_metadata)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("带输出功能的统一文件处理器 v2.0")
        print("=" * 50)
        print("用法:")
        print("  python file_processor_with_output.py <文件路径> [输出目录]")
        print()
        print("参数:")
        print("  文件路径    : 要处理的文件")
        print("  输出目录    : 保存结果的目录（默认: outputs）")
        print()
        print("示例:")
        print("  python file_processor_with_output.py document.pdf")
        print("  python file_processor_with_output.py image.png my_outputs")
        print()
        
        processor = FileProcessorWithOutput()
        print("支持的文件类型:")
        for category, exts in processor.get_supported_extensions().items():
            print(f"  {category}: {', '.join(exts)}")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs"
    
    print(f"处理文件: {file_path}")
    print(f"输出目录: {output_dir}")
    print("-" * 50)
    
    result = process_file_with_output(file_path, output_dir)
    
    if result["success"]:
        print(f"✓ 处理成功")
        print(f"文件类型: {result['file_type']}")
        print(f"处理器: {result['processor']}")
        print(f"文本长度: {len(result['text'])} 字符")
        if "output_file" in result:
            print(f"输出文件: {result['output_file']}")
        print()
        print("文本内容预览:")
        print("-" * 30)
        preview = result["text"][:500]
        if len(result["text"]) > 500:
            preview += "\n... (内容已截断，完整内容请查看输出文件)"
        print(preview)
    else:
        print(f"✗ 处理失败")
        print(f"错误信息: {result['error']}")
        if "output_error" in result:
            print(f"输出错误: {result['output_error']}")

