"""
对话记忆管理模块
负责存储和管理对话历史记录，主要功能：
- 使用固定大小的队列存储历史消息
- 提供消息的添加和获取接口
- 自动管理历史记录大小
"""
from typing import List, Dict, Any
from collections import deque
from ..config import Config
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ConversationMemory:
    """
    对话记忆管理类
    使用双端队列（deque）实现固定大小的历史记录存储
    """
    
    def __init__(self, max_history: int = Config.MAX_HISTORY):
        """
        初始化对话记忆
        
        Args:
            max_history: 最大历史记录数，默认为配置中的值
        """
        self.max_history = max_history
        self.messages = deque(maxlen=max_history)  # 使用固定大小的双端队列
        logger.info(f"初始化对话记忆，最大历史记录数: {max_history}")
    
    def add_message(self, role: str, content: str) -> None:
        """
        添加消息到历史记录
        
        Args:
            role: 消息角色（user/assistant）
            content: 消息内容
        """
        self.messages.append({"role": role, "content": content})
        logger.debug(f"添加消息: {role} - {content[:50]}...")  # 只记录前50个字符
    
    def get_messages(self) -> List[Dict[str, str]]:
        """
        获取所有历史消息
        
        Returns:
            List[Dict[str, str]]: 消息列表，每个消息包含role和content
        """
        return list(self.messages)
    
    def clear(self) -> None:
        """
        清空历史记录
        移除所有已存储的消息
        """
        self.messages.clear()
        logger.info("清空对话历史记录") 