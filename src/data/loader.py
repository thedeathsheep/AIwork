"""
LangChain 数据加载器实现
提供多种文件格式的加载和文本分割功能
"""
import os
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import logging
from datetime import datetime
# 导入 LangChain 文档加载器
from langchain.document_loaders import (
    TextLoader,  # 文本文件加载器
    CSVLoader,  # CSV文件加载器
    JSONLoader,  # JSON文件加载器
    UnstructuredExcelLoader,  # Excel文件加载器
    PyPDFLoader,  # PDF文件加载器
    UnstructuredMarkdownLoader  # Markdown文件加载器
)
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 文本分割器
from langchain.schema import Document  # 文档模型

# 设置日志记录器
logger = logging.getLogger(__name__)

class DataLoader:
    """
    灵活的数据加载器，支持多种文件格式并与 LangChain 集成
    
    功能：
    1. 支持多种文件格式的加载
    2. 自动文本分割
    3. 文档缓存
    4. 批量处理
    """
    
    # 支持的文件格式及其对应的加载器
    SUPPORTED_FORMATS = {
        'txt': TextLoader,  # 文本文件
        'csv': CSVLoader,  # CSV文件
        'json': JSONLoader,  # JSON文件
        'xlsx': UnstructuredExcelLoader,  # Excel文件
        'xls': UnstructuredExcelLoader,  # Excel文件
        'pdf': PyPDFLoader,  # PDF文件
        'md': UnstructuredMarkdownLoader  # Markdown文件
    }
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        初始化数据加载器
        
        参数：
            cache_dir: 缓存目录路径，用于存储处理后的文档
        """
        self.cache_dir = cache_dir
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
            
        # 初始化文本分割器
        # 用于将长文本分割成适合处理的较小块
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # 每个文本块的最大字符数
            chunk_overlap=200,  # 相邻文本块的重叠字符数
            length_function=len,  # 计算文本长度的函数
            # 文本分割的分隔符，按优先级排序
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
        )
            
    def load(self, 
             file_path: Union[str, Path], 
             file_type: Optional[str] = None,
             **kwargs) -> List[Document]:
        """
        加载文件并使用 LangChain 加载器处理
        
        参数：
            file_path: 文件路径
            file_type: 文件类型（如果为None则自动检测）
            **kwargs: 传递给特定加载器的额外参数
            
        返回：
            List[Document]: LangChain Document 对象列表
            每个 Document 包含：
            - page_content: 文本内容
            - metadata: 元数据（如文件名、页码等）
        """
        file_path = Path(file_path)
        
        # 检查文件是否存在
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
            
        # 如果未指定文件类型，从文件扩展名自动检测
        if file_type is None:
            file_type = file_path.suffix.lower()[1:]  # 移除点号
            
        # 检查缓存
        if self.cache_dir:
            cache_path = Path(self.cache_dir) / f"{file_path.stem}_{datetime.now().strftime('%Y%m%d')}.pkl"
            if cache_path.exists():
                logger.info(f"从缓存加载: {cache_path}")
                import pickle
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
        
        # 检查文件类型是否支持
        if file_type not in self.SUPPORTED_FORMATS:
            raise ValueError(f"不支持的文件类型: {file_type}. 支持的类型: {list(self.SUPPORTED_FORMATS.keys())}")
            
        try:
            # 使用 LangChain 加载器加载文件
            loader = self.SUPPORTED_FORMATS[file_type](str(file_path), **kwargs)
            documents = loader.load()
            
            # 分割文本
            split_docs = self.text_splitter.split_documents(documents)
            
            # 缓存处理后的文档
            if self.cache_dir:
                cache_path = Path(self.cache_dir) / f"{file_path.stem}_{datetime.now().strftime('%Y%m%d')}.pkl"
                import pickle
                with open(cache_path, 'wb') as f:
                    pickle.dump(split_docs, f)
                logger.info(f"文档已缓存到: {cache_path}")
            
            return split_docs
            
        except Exception as e:
            logger.error(f"加载文件时出错 {file_path}: {str(e)}")
            raise
    
    def batch_load(self, 
                  file_paths: List[Union[str, Path]], 
                  file_type: Optional[str] = None,
                  **kwargs) -> List[List[Document]]:
        """
        批量加载多个文件
        
        参数：
            file_paths: 文件路径列表
            file_type: 文件类型（如果为None则自动检测）
            **kwargs: 传递给特定加载器的额外参数
            
        返回：
            List[List[Document]]: 每个文件的文档列表
        """
        return [self.load(path, file_type, **kwargs) for path in file_paths]
    
    def clear_cache(self, older_than_days: int = 7) -> None:
        """
        清理旧的缓存文件
        
        参数：
            older_than_days: 清理多少天前的缓存文件
        """
        if not self.cache_dir:
            return
            
        cache_dir = Path(self.cache_dir)
        current_time = datetime.now()
        
        # 遍历缓存目录中的所有文件
        for cache_file in cache_dir.glob("*.pkl"):
            file_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            # 如果文件超过指定天数，则删除
            if (current_time - file_time).days > older_than_days:
                cache_file.unlink()
                logger.info(f"已清理旧缓存文件: {cache_file}") 