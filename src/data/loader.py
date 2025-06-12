"""
数据加载器模块
负责加载和处理各种格式的文档，主要功能：
- 支持多种文件格式（txt, csv, json, xlsx, pdf, md等）
- 文本分割和预处理
- 文档缓存管理
"""
import os
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import logging
from datetime import datetime

# 导入 LangChain 文档加载器 (更新导入路径以解决弃用警告)
from langchain_community.document_loaders import (
    TextLoader,  # 文本文件加载器
    CSVLoader,  # CSV文件加载器
    JSONLoader,  # JSON文件加载器
    UnstructuredExcelLoader,  # Excel文件加载器
    PyPDFLoader,  # PDF文件加载器
    UnstructuredMarkdownLoader  # Markdown文件加载器
)
from langchain.text_splitter import RecursiveCharacterTextSplitter  # 文本分割器
from langchain.schema import Document  # 文档模型
from langchain_chroma import Chroma  # 向量数据库
from langchain_openai import OpenAIEmbeddings  # 文本嵌入模型

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
    5. 向量化存储
    """
    
    # 支持的文件格式及其对应的加载器
    SUPPORTED_FORMATS = {
        'txt': lambda path, **kwargs: TextLoader(path, encoding='utf-8', **kwargs),  # 文本文件，使用UTF-8编码
        'text': lambda path, **kwargs: TextLoader(path, encoding='utf-8', **kwargs),  # 文本文件(.text扩展名)，使用UTF-8编码
        'csv': CSVLoader,  # CSV文件
        'json': JSONLoader,  # JSON文件
        'xlsx': UnstructuredExcelLoader,  # Excel文件
        'xls': UnstructuredExcelLoader,  # Excel文件
        'pdf': PyPDFLoader,  # PDF文件
        'md': UnstructuredMarkdownLoader  # Markdown文件
    }
    
    def __init__(self, cache_dir: Optional[str] = None, persist_dir: Optional[str] = None,
                api_key: Optional[str] = None, base_url: Optional[str] = None):
        """
        初始化数据加载器
        
        Args:
            cache_dir: 缓存目录路径，用于存储处理后的文档
            persist_dir: 向量数据库持久化目录
            api_key: OpenAI API密钥或AiHubMix API密钥
            base_url: API基础URL，用于自定义API端点
        """
        self.cache_dir = cache_dir
        self.persist_dir = persist_dir
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
        if persist_dir:
            os.makedirs(persist_dir, exist_ok=True)
            
        # 初始化文本分割器
        # 用于将长文本分割成适合处理的较小块
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # 每个文本块的最大字符数
            chunk_overlap=200,  # 相邻文本块的重叠字符数
            length_function=len,  # 计算文本长度的函数
            # 文本分割的分隔符，按优先级排序
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]
        )
        
        # 配置OpenAI Embeddings
        api_key = api_key or os.environ.get("AIHUBMIX_API_KEY") or os.environ.get("OPENAI_API_KEY")
        embedding_kwargs = {"api_key": api_key}
        if base_url or os.environ.get("OPENAI_BASE_URL"):
            embedding_kwargs["base_url"] = base_url or os.environ.get("OPENAI_BASE_URL") or "https://aihubmix.com/v1"
            
        # 初始化嵌入模型
        self.embeddings = OpenAIEmbeddings(**embedding_kwargs)
        
        # 初始化向量数据库
        self.vectorstore = None
        if persist_dir:
            self.vectorstore = Chroma(
                persist_directory=persist_dir,
                embedding_function=self.embeddings
            )
            
    def load(self, 
             file_path: Union[str, Path], 
             file_type: Optional[str] = None,
             **kwargs) -> List[Document]:
        """
        加载文件并使用 LangChain 加载器处理
        
        Args:
            file_path: 文件路径
            file_type: 文件类型（如果为None则自动检测）
            **kwargs: 传递给特定加载器的额外参数
            
        Returns:
            List[Document]: LangChain Document 对象列表
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
            loader_class_or_func = self.SUPPORTED_FORMATS[file_type]
            
            # 处理函数和类两种情况
            if callable(loader_class_or_func) and not isinstance(loader_class_or_func, type):
                # 对于函数，直接调用
                loader = loader_class_or_func(str(file_path), **kwargs)
            else:
                # 对于类，实例化
                loader = loader_class_or_func(str(file_path), **kwargs)
                
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
            
            # 添加到向量数据库
            if self.vectorstore:
                self.vectorstore.add_documents(split_docs)
                # self.vectorstore.persist()  # Chroma类不再支持persist方法
                logger.info(f"文档已添加到向量数据库: {file_path}")
            
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
        
        Args:
            file_paths: 文件路径列表
            file_type: 文件类型（如果为None则自动检测）
            **kwargs: 传递给特定加载器的额外参数
            
        Returns:
            List[List[Document]]: 每个文件的文档列表
        """
        return [self.load(path, file_type, **kwargs) for path in file_paths]
    
    def search(self, query: str, k: int = 4) -> List[Document]:
        """
        在知识库中搜索相关文档
        
        Args:
            query: 搜索查询
            k: 返回的文档数量
            
        Returns:
            List[Document]: 相关文档列表
        """
        if not self.vectorstore:
            raise ValueError("向量数据库未初始化")
            
        return self.vectorstore.similarity_search(query, k=k)
    
    def clear_cache(self, older_than_days: int = 7) -> None:
        """
        清理旧的缓存文件
        
        Args:
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