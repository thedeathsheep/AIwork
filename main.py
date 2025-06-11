from src.chat.agent import ChatAgent
from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    """主程序入口"""
    print("程序开始运行...")
    try:
        print("正在验证配置...")
        # 验证配置
        Config.validate_config()
        
        print("正在初始化对话代理...")
        # 初始化对话代理
        agent = ChatAgent()
        
        print("欢迎使用 AI 对话程序！")
        print("输入 'quit' 退出")
        print("输入 'clear' 清空对话历史")
        print("-" * 50)
        
        while True:
            print("\n等待用户输入...")
            user_input = input("\n请输入你的问题: ").strip()
            print(f"收到用户输入: {user_input}")
            
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
            
            try:
                print("正在处理用户输入...")
                response = agent.chat(user_input)
                print("\nAI 回复:", response)
            except Exception as e:
                logger.error(f"对话出错: {str(e)}")
                print(f"\n发生错误: {str(e)}")
                print(f"错误类型: {type(e)}")
                import traceback
                print(f"错误堆栈: {traceback.format_exc()}")
                
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        print(f"程序出错: {str(e)}")
        print(f"错误类型: {type(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")

if __name__ == "__main__":
    print("程序启动...")
    main() 