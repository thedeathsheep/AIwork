from src.chat.agent import ChatAgent
from src.config import Config
from src.utils.logger import setup_logger
from pathlib import Path
from langchain.schema import SystemMessage, HumanMessage
import json

logger = setup_logger(__name__)

# Few-shot 示例
FEW_SHOT_EXAMPLES = [
    {
        "user": "什么是Python？",
        "assistant": "Python是一种广泛使用的解释型、高级和通用的编程语言。Python的设计具有很强的可读性，它使用大量的缩进。Python支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。Python的语法简洁明了，适合初学者学习，同时也被广泛应用于人工智能、数据分析、Web开发等领域。"
    },
    {
        "user": "人工智能会取代人类工作吗？",
        "assistant": "人工智能确实会改变就业市场，但这是一个复杂的问题。AI可能会取代一些重复性的工作，但同时也会创造新的就业机会。重要的是，AI更适合作为人类的助手，而不是完全替代。我们应该关注如何与AI协作，提升工作效率，同时发展新的技能来适应这个变化。"
    }
]

# 系统提示
SYSTEM_PROMPT = """你是一个专业的百科问答助手。你的任务是回答用户的问题，提供准确、全面且易于理解的信息。

回答时请注意：
1. 保持客观准确
2. 解释要清晰易懂
3. 适当举例说明
4. 必要时提供补充信息

请参考以下示例来理解回答风格："""

def process_content(content: str, agent: ChatAgent) -> None:
    """
    处理内容并显示回复
    
    Args:
        content: 用户输入的内容
        agent: 对话代理实例
    """
    try:
        # 构建系统消息和人类消息
        system_message = SystemMessage(content=SYSTEM_PROMPT)
        human_message = HumanMessage(content=content)
        
        # 获取 AI 回复和思考过程
        response, thinking = agent.chat([system_message, human_message])
        
        # 显示思考过程
        print("\n思考过程:")
        print("-" * 50)
        print(thinking)
        print("-" * 50)
        
        # 显示最终回复
        print(f"\n助手: {response}")
        
    except Exception as e:
        logger.error(f"处理内容时出错: {str(e)}")
        print(f"处理内容时出错: {str(e)}")

def main():
    """主程序入口函数"""
    print("程序开始运行...")
    try:
        print("正在验证配置...")
        Config.validate_config()
        
        print("正在初始化对话代理...")
        agent = ChatAgent()
        
        print("欢迎使用 AI 百科问答助手！")
        print("输入 'quit' 退出")
        print("输入 'clear' 清空对话历史")
        print("输入 'examples' 查看示例")
        print("-" * 50)
        
        while True:
            print("\n等待用户输入...")
            user_input = input("\n请输入你的问题: ").strip()
            if not user_input:
                print("输入为空，继续等待...")
                continue
                
            if user_input.lower() == 'quit':
                print("用户选择退出...")
                print("感谢使用，再见！")
                break
                
            if user_input.lower() == 'clear':
                print("用户选择清空历史...")
                agent.clear_history()
                print("对话历史已清空")
                continue
                
            if user_input.lower() == 'examples':
                print("\nFew-shot 示例:")
                for i, example in enumerate(FEW_SHOT_EXAMPLES, 1):
                    print(f"\n示例 {i}:")
                    print(f"用户: {example['  user']}")
                    print(f"助手: {example['assistant']}")
                continue 
            
            process_content(user_input, agent)
                
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        print(f"程序出错: {str(e)}")
        print(f"错误类型: {type(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == "__main__":
    print("程序启动...")
    main() 