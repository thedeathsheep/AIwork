# AI Chat Assistant

一个基于 LangChain 和 AiHubMix API 的智能对话助手。

## 项目特点

- 使用 LangChain 框架构建
- 支持多种 AI 模型
- 模块化设计
- 完整的错误处理
- 支持对话历史记录
- 可配置的系统提示词

## 项目结构

```
aichat/
├── src/
│   ├── __init__.py
│   ├── config.py          # 配置管理
│   ├── chat/
│   │   ├── __init__.py
│   │   ├── agent.py       # 对话代理
│   │   └── memory.py      # 对话记忆管理
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py      # 日志工具
│   └── models/
│       ├── __init__.py
│       └── chat_model.py  # 模型配置
├── tests/                 # 单元测试
├── .env.example          # 环境变量示例
├── environment.yml       # Conda 环境配置
└── main.py              # 主程序入口
```

## 安装

1. 克隆仓库
2. 创建并激活 conda 环境：
```bash
conda env create -f environment.yml
conda activate aichat
```

3. 复制 `.env.example` 到 `.env` 并配置你的 API 密钥

## 使用方法

```bash
python main.py
```

## 开发

- 使用 Python 3.10+
- 遵循 PEP 8 编码规范
- 使用 type hints 进行类型注解
- 编写单元测试

## 许可证

MIT License 