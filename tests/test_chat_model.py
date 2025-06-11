import pytest
from src.models.chat_model import ChatModel
from src.config import Config

def test_chat_model_initialization():
    """测试聊天模型初始化"""
    model = ChatModel()
    assert model is not None

def test_chat_model_config():
    """测试模型配置"""
    model = ChatModel()
    assert model.model.model_name == Config.DEFAULT_MODEL
    assert model.model.temperature == Config.TEMPERATURE 