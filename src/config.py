from typing import Dict, Any
from pathlib import Path
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """项目配置类"""
    
    # 基础配置
    BASE_DIR: Path = Path(__file__).parent.parent
    API_KEY: str = os.getenv("AIHUBMIX_API_KEY", "")
    API_BASE: str = "https://aihubmix.com/v1"
    
    # 模型配置
    DEFAULT_MODEL: str = "gpt-4o-mini"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000
    
    # 对话配置
    SYSTEM_PROMPT: str = "你是一个有帮助的AI助手。"
    MAX_HISTORY: int = 10
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def get_model_config(cls) -> Dict[str, Any]:
        """获取模型配置"""
        return {
            "model": cls.DEFAULT_MODEL,
            "temperature": cls.TEMPERATURE,
            "max_tokens": cls.MAX_TOKENS,
        }
    
    @classmethod
    def validate_config(cls) -> None:
        """验证配置是否有效"""
        print(f"正在验证配置...")
        print(f"API_KEY 长度: {len(cls.API_KEY) if cls.API_KEY else 0}")
        if not cls.API_KEY:
            raise ValueError("请在 .env 文件中设置 AIHUBMIX_API_KEY")
        print("配置验证通过！") 