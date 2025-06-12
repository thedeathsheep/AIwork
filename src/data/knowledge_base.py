"""
知识库管理模块
负责管理文档知识库，提供文档的增删改查功能
"""
from typing import List, Optional, Dict, Any
from pathlib import Path
import logging
from datetime import datetime
import json
import os

from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from .loader import DataLoader

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """
    知识库管理类，提供文档的增删改查功能
    
    功能：
    1. 文档管理（添加、删除、更新）
    2. 文档检索
    3. 元数据管理
    4. 知识库状态监控
    """
    
    def __init__(self, 
                 persist_dir: str,
                 cache_dir: Optional[str] = None,
                 metadata_file: Optional[str] = None,
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None):
        """
        初始化知识库
        
        Args:
            persist_dir: 向量数据库持久化目录
            cache_dir: 文档缓存目录
            metadata_file: 元数据文件路径
            api_key: OpenAI API密钥或AiHubMix API密钥
            base_url: API基础URL，用于自定义API端点
        """
        self.persist_dir = Path(persist_dir)
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.metadata_file = Path(metadata_file) if metadata_file else None
        
        # 创建必要的目录
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            
        # 配置API参数
        self.api_key = api_key or os.environ.get("AIHUBMIX_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.base_url = base_url or os.environ.get("OPENAI_BASE_URL") or "https://aihubmix.com/v1"
            
        # 初始化数据加载器
        self.loader = DataLoader(
            cache_dir=str(self.cache_dir) if self.cache_dir else None,
            persist_dir=str(self.persist_dir),
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # 初始化元数据
        self.metadata: Dict[str, Any] = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, Any]:
        """加载元数据"""
        if self.metadata_file and self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"加载元数据失败: {str(e)}")
                return {}
        return {}
        
    def _save_metadata(self) -> None:
        """保存元数据"""
        if self.metadata_file:
            try:
                with open(self.metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(self.metadata, f, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"保存元数据失败: {str(e)}")
                
    def add_document(self, 
                    file_path: str,
                    metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        添加文档到知识库
        
        Args:
            file_path: 文档路径
            metadata: 文档元数据
            
        Returns:
            bool: 是否添加成功
        """
        logger.info(f"开始添加文档: {file_path}")
        file_path = str(file_path)  # 确保文件路径是字符串类型
        
        try:
            # 打印文件信息
            path_obj = Path(file_path)
            logger.info(f"文件存在: {path_obj.exists()}, 文件类型: {path_obj.suffix}")
            
            # 加载文档
            logger.info(f"正在通过DataLoader加载文件: {file_path}")
            docs = self.loader.load(file_path)
            logger.info(f"文件加载成功，共获取 {len(docs)} 个文本块")
            
            # 更新元数据
            doc_id = str(datetime.now().timestamp())
            self.metadata[doc_id] = {
                'file_path': file_path,
                'added_time': datetime.now().isoformat(),
                'doc_count': len(docs),
                'custom_metadata': metadata or {}
            }
            self._save_metadata()
            
            logger.info(f"成功添加文档: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"添加文档失败 {file_path}: {str(e)}")
            import traceback
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            raise  # 向上传递异常，便于调试
            
    def remove_document(self, doc_id: str) -> bool:
        """
        从知识库中删除文档
        
        Args:
            doc_id: 文档ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            if doc_id not in self.metadata:
                logger.warning(f"文档不存在: {doc_id}")
                return False
                
            # 从向量数据库中删除
            # TODO: 实现向量数据库中的文档删除
            
            # 从元数据中删除
            del self.metadata[doc_id]
            self._save_metadata()
            
            logger.info(f"成功删除文档: {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"删除文档失败 {doc_id}: {str(e)}")
            return False
            
    def search(self, 
              query: str,
              k: int = 4,
              filter_metadata: Optional[Dict[str, Any]] = None) -> List[Document]:
        """
        搜索知识库
        
        Args:
            query: 搜索查询
            k: 返回的文档数量
            filter_metadata: 元数据过滤条件
            
        Returns:
            List[Document]: 相关文档列表
        """
        try:
            return self.loader.search(query, k=k)
        except Exception as e:
            logger.error(f"搜索失败: {str(e)}")
            return []
            
    def get_document_info(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        获取文档信息
        
        Args:
            doc_id: 文档ID
            
        Returns:
            Optional[Dict[str, Any]]: 文档信息
        """
        return self.metadata.get(doc_id)
        
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        列出所有文档信息
        
        Returns:
            List[Dict[str, Any]]: 文档信息列表
        """
        return [
            {'doc_id': doc_id, **info}
            for doc_id, info in self.metadata.items()
        ]
        
    def get_stats(self) -> Dict[str, Any]:
        """
        获取知识库统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        return {
            'total_documents': len(self.metadata),
            'total_chunks': sum(info['doc_count'] for info in self.metadata.values()),
            'last_updated': max(
                datetime.fromisoformat(info['added_time'])
                for info in self.metadata.values()
            ).isoformat() if self.metadata else None
        } 