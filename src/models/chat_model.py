from typing import List
from langchain_openai import ChatOpenAI
from langchain.schema import BaseMessage, SystemMessage
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
    
    def chat(self, messages: List[BaseMessage]) -> tuple[str, str]:
        """
        进行对话
        
        Args:
            messages: LangChain 消息列表
            
        Returns:
            tuple[str, str]: (AI 的回复, 思考过程)
        """
        try:
            # 构建思考提示
            thinking_prompt = "请先思考如何回答这个问题，然后给出最终答案。思考过程要详细说明你的推理步骤。"
            messages_with_thinking = messages + [SystemMessage(content=thinking_prompt)]
            
            # 获取回复
            response = self.model.invoke(messages_with_thinking)
            
            # 分离思考过程和最终答案
            content = response.content
            if "思考过程：" in content:
                thinking, answer = content.split("思考过程：", 1)
                if "最终答案：" in answer:
                    thinking, answer = answer.split("最终答案：", 1)
                    return answer.strip(), thinking.strip()
            
            # 如果没有找到明确的分隔，返回原始内容作为答案，空字符串作为思考过程
            return content, ""
            
        except Exception as e:
            logger.error(f"对话出错: {str(e)}")
            raise 