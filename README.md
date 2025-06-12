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
│   │   - 环境变量配置（API密钥等）
│   │   - 模型参数配置（温度、最大token等）
│   │   - 对话配置（系统提示、历史记录限制等）
│   │   - 日志配置
│   ├── chat/
│   │   ├── __init__.py
│   │   ├── agent.py       # 对话代理
│   │   │   - 管理对话流程
│   │   │   - 处理消息格式转换
│   │   │   - 维护对话上下文
│   │   │   - 控制对话轮次限制
│   │   └── memory.py      # 对话记忆管理
│   │       - 存储对话历史
│   │       - 限制历史记录数量
│   │       - 提供历史记录访问接口
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py      # 日志工具
│   │       - 配置日志格式
│   │       - 提供日志记录功能
│   └── models/
│       ├── __init__.py
│       └── chat_model.py  # 模型配置
│           - 初始化语言模型
│           - 处理模型调用
│           - 管理模型参数
├── tests/                 # 单元测试
├── .env.example          # 环境变量示例
├── environment.yml       # Conda 环境配置
└── main.py              # 主程序入口
    - 程序初始化
    - 用户交互界面
    - 命令处理（quit/clear/examples等）
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