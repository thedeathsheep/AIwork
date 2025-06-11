from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
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
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """
        进行对话
        
        Args:
            messages: 消息列表，每个消息包含 role 和 content
            
        Returns:
            str: AI 的回复
        """
        try:
            # 转换消息格式
            formatted_messages = [
                SystemMessage(content=Config.SYSTEM_PROMPT)
            ]
            formatted_messages.extend([
                HumanMessage(content=msg["content"]) if msg["role"] == "user"
                else SystemMessage(content=msg["content"])
                for msg in messages
            ])
            
            # 获取回复
            response = self.model.invoke(formatted_messages)
            return response.content
            
        except Exception as e:
            logger.error(f"对话出错: {str(e)}")
            raise 