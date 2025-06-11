from typing import Optional
from ..models.chat_model import ChatModel
from .memory import ConversationMemory
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ChatAgent:
    """对话代理类"""
    
    def __init__(self):
        """初始化对话代理"""
        self.model = ChatModel()
        self.memory = ConversationMemory()
        logger.info("初始化对话代理")
    
    def chat(self, user_input: str) -> str:
        """
        处理用户输入并返回回复
        
        Args:
            user_input: 用户输入的消息
            
        Returns:
            str: AI 的回复
        """
        try:
            # 添加用户消息到历史记录
            self.memory.add_message("user", user_input)
            
            # 获取历史消息
            messages = self.memory.get_messages()
            
            # 获取 AI 回复
            response = self.model.chat(messages)
            
            # 添加 AI 回复到历史记录
            self.memory.add_message("assistant", response)
            
            return response
            
        except Exception as e:
            logger.error(f"对话处理出错: {str(e)}")
            raise
    
    def clear_history(self) -> None:
        """清空对话历史"""
        self.memory.clear()
        logger.info("清空对话历史") 