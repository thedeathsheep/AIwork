from setuptools import setup, find_packages

"""
项目依赖管理说明：

1. 环境管理策略
   - 开发环境：使用 conda 管理（environment.yml）
     * 优点：可以管理 Python 版本和系统级依赖
     * 安装：conda env create -f environment.yml
   
   - 生产环境：使用 pip 管理（setup.py）
     * 优点：更轻量，适合部署
     * 安装：pip install .
     * 开发工具：pip install .[dev]

2. 依赖分类说明
   基础依赖（install_requires）：
   - 项目运行必需的核心依赖
   - 版本固定，确保稳定性
   - 包含数据处理、AI 对话等核心功能

   开发依赖（extras_require）：
   - 仅在开发时需要的工具
   - 代码质量、测试、类型检查等
   - 通过 [dev] 选项安装
"""

setup(
    name="aichat",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 核心依赖
        "pandas==2.2.1",        # 数据处理
        "numpy==1.26.4",        # 数值计算
        "scikit-learn==1.4.1",  # 机器学习
        # 文件支持
        "openpyxl>=3.1.2",      # Excel 支持
        "pyarrow>=15.0.0",      # Parquet 支持
        # 环境配置
        "python-dotenv>=1.0.0", # 环境变量
        # AI 对话
        "langchain>=0.1.0",     # 对话框架
        "langchain-openai==0.3.18", # OpenAI 集成
    ],
    extras_require={
        "dev": [
            # 代码质量
            "black==24.2.0",    # 代码格式化
            "isort==5.13.2",    # import 排序
            "flake8==7.0.0",    # 代码检查
            # 测试工具
            "pytest==8.0.2",    # 单元测试
            # 类型检查
            "mypy==1.8.0",      # 静态类型检查
            # 开发工具
            "pre-commit==3.6.0", # Git 提交检查
        ]
    },
    python_requires=">=3.10",
) 