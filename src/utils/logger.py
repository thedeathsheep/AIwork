import logging
from typing import Optional
from ..config import Config

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name or __name__)
    
    if not logger.handlers:
        logger.setLevel(Config.LOG_LEVEL)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(Config.LOG_LEVEL)
        
        # 创建格式化器
        formatter = logging.Formatter(Config.LOG_FORMAT)
        console_handler.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        logger.addHandler(console_handler)
    
    return logger 