from typing import Optional, List
from ..models.chat_model import ChatModel
from .memory import ConversationMemory
from ..utils.logger import setup_logger
from langchain.schema import BaseMessage, SystemMessage, HumanMessage
from ..config import Config

logger = setup_logger(__name__)

class ChatAgent:
    """对话代理类"""
    
    def __init__(self):
        """初始化对话代理"""
        self.model = ChatModel()
        self.memory = ConversationMemory()
        self.system_message = SystemMessage(content=Config.SYSTEM_PROMPT)
        logger.info("初始化对话代理")
    
    def chat(self, messages: List[BaseMessage]) -> tuple[str, str]:
        """
        处理用户输入并返回回复和思考过程
        
        Args:
            messages: LangChain 消息列表
            
        Returns:
            tuple[str, str]: (AI 的回复, 思考过程)
        """
        try:
            # 获取历史消息
            history = self.memory.get_messages()
            
            # 将历史消息转换为 LangChain 消息格式
            history_messages = []
            for msg in history:
                if msg["role"] == "user":
                    history_messages.append(HumanMessage(content=msg["content"]))
                else:
                    history_messages.append(SystemMessage(content=msg["content"]))
            
            # 确保不超过最大历史记录数
            # 每个对话轮次包含用户消息和助手回复，所以实际轮次是消息数的一半
            max_rounds = Config.MAX_HISTORY // 2
            if len(history_messages) > max_rounds * 2:
                # 保留最近的对话轮次
                history_messages = history_messages[-(max_rounds * 2):]
                logger.info(f"历史消息超过最大轮次限制，保留最近 {max_rounds} 轮对话")
            
            # 合并系统消息、历史消息和当前消息
            all_messages = [self.system_message] + history_messages + messages
            
            # 获取 AI 回复和思考过程
            response, thinking = self.model.chat(all_messages)
            
            # 添加用户消息和 AI 回复到历史记录
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    self.memory.add_message("user", msg.content)
            self.memory.add_message("assistant", response)
            
            return response, thinking
            
        except Exception as e:
            logger.error(f"对话处理出错: {str(e)}")
            raise
    
    def clear_history(self) -> None:
        """清空对话历史"""
        self.memory.clear()
        logger.info("清空对话历史") 