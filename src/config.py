"""
配置管理模块
负责管理项目的所有配置项，包括：
- 环境变量配置
- 模型参数配置
- 对话配置
- 日志配置
"""
from typing import Dict, Any
from pathlib import Path
import os
from dotenv import load_dotenv

# 加载环境变量文件
load_dotenv()

class Config:
    """项目配置类，集中管理所有配置项"""
    
    # 基础配置
    BASE_DIR: Path = Path(__file__).parent.parent  # 项目根目录
    API_KEY: str = os.getenv("AIHUBMIX_API_KEY", "")  # API密钥
    API_BASE: str = "https://aihubmix.com/v1"  # API基础URL
    
    # 模型配置
    DEFAULT_MODEL: str = "gpt-4o-mini"  # 默认使用的模型
    TEMPERATURE: float = 0.7  # 温度参数，控制输出的随机性
    MAX_TOKENS: int = 2000  # 最大输出token数
    
    # 对话配置
    SYSTEM_PROMPT: str = "你是一个有帮助的AI助手。"  # 系统提示词
    MAX_HISTORY: int = 10  # 最大历史记录数（对话轮次 * 2）
    
    # 日志配置
    LOG_LEVEL: str = "INFO"  # 日志级别
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # 日志格式
    
    @classmethod
    def get_model_config(cls) -> Dict[str, Any]:
        """
        获取模型配置
        
        Returns:
            Dict[str, Any]: 包含模型参数的字典
        """
        return {
            "model": cls.DEFAULT_MODEL,
            "temperature": cls.TEMPERATURE,
            "max_tokens": cls.MAX_TOKENS,
        }
    
    @classmethod
    def validate_config(cls) -> None:
        """
        验证配置是否有效
        检查必要的配置项是否存在
        
        Raises:
            ValueError: 当配置无效时抛出异常
        """
        print(f"正在验证配置...")
        print(f"API_KEY 长度: {len(cls.API_KEY) if cls.API_KEY else 0}")
        if not cls.API_KEY:
            raise ValueError("请在 .env 文件中设置 AIHUBMIX_API_KEY")
        print("配置验证通过！") 