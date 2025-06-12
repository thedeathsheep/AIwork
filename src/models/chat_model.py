from typing import List
from langchain_openai import ChatOpenAI
from langchain.schema import BaseMessage
from ..config import Config
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class ChatModel:
    """聊天模型类"""
    
    def __init__(self):
        """初始化聊天模型"""
        self.model = ChatOpenAI(
            **Config.get_model_config(),
            api_key=Config.API_KEY,
            base_url=Config.API_BASE
        )
        logger.info(f"初始化聊天模型: {Config.DEFAULT_MODEL}")
    
    def chat(self, messages: List[BaseMessage]) -> str:
        """
        进行对话
        
        Args:
            messages: LangChain 消息列表
            
        Returns:
            str: AI 的回复
        """
        try:
            # 获取回复
            response = self.model.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"对话出错: {str(e)}")
            raise 