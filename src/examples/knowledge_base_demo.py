"""
知识库使用示例

本脚本演示如何使用知识库功能进行文档管理和搜索。
可以添加文档、搜索文档、查看知识库统计信息等。
"""
import os
import sys
import argparse
from pathlib import Path
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.data.knowledge_base import KnowledgeBase
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def create_kb_directories():
    """创建知识库相关目录"""
    base_dir = Path("data/knowledge_base")
    persist_dir = base_dir / "vector_store"
    cache_dir = base_dir / "cache"
    metadata_file = base_dir / "metadata.json"
    
    # 创建目录
    persist_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    return base_dir, persist_dir, cache_dir, metadata_file

def add_document(kb, file_path, metadata=None):
    """添加文档到知识库并打印结果"""
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return
    
    if metadata is None:
        metadata = {
            "title": Path(file_path).stem,
            "author": "AI助手",
            "category": "示例"
        }
    
    print(f"正在添加文档: {file_path}")
    try:
        success = kb.add_document(file_path, metadata=metadata)
        print(f"添加文档{'成功' if success else '失败'}")
        return success
    except Exception as e:
        print(f"添加文档失败 {file_path}: {str(e)}")
        # 打印详细的错误堆栈
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")
        return False

def search_documents(kb, query, k=3):
    """在知识库中搜索文档并打印结果"""
    print(f"正在搜索: '{query}'")
    results = kb.search(query, k=k)
    
    print(f"\n搜索结果:")
    if not results:
        print("未找到匹配的文档")
        return
    
    for i, doc in enumerate(results, 1):
        print(f"\n文档 {i}:")
        print(f"内容: {doc.page_content[:200]}..." if len(doc.page_content) > 200 else f"内容: {doc.page_content}")
        print(f"元数据: {doc.metadata}")
    
    return results

def print_kb_stats(kb):
    """打印知识库统计信息"""
    stats = kb.get_stats()
    print(f"\n知识库统计信息:")
    print(f"总文档数: {stats['total_documents']}")
    print(f"总文本块数: {stats['total_chunks']}")
    print(f"最后更新时间: {stats['last_updated'] or '无'}")

def list_documents(kb):
    """列出所有文档信息"""
    doc_list = kb.list_documents()
    if not doc_list:
        print("\n知识库中没有文档")
        return
    
    print(f"\n所有文档列表:")
    for doc_info in doc_list:
        print(f"\n文档ID: {doc_info['doc_id']}")
        print(f"文件路径: {doc_info['file_path']}")
        print(f"添加时间: {doc_info['added_time']}")
        print(f"文本块数: {doc_info['doc_count']}")
        print(f"自定义元数据: {doc_info['custom_metadata']}")

def main():
    """主程序入口函数"""
    parser = argparse.ArgumentParser(description="知识库使用示例")
    parser.add_argument("--add", type=str, help="要添加到知识库的文档路径")
    parser.add_argument("--search", type=str, help="在知识库中搜索的关键词")
    parser.add_argument("--list", action="store_true", help="列出知识库中的所有文档")
    parser.add_argument("--stats", action="store_true", help="显示知识库统计信息")
    parser.add_argument("--k", type=int, default=3, help="搜索返回的结果数量")
    parser.add_argument("--api-key", type=str, help="AiHubMix或OpenAI的API密钥")
    parser.add_argument("--base-url", type=str, default=None, help="API基础URL")
    
    args = parser.parse_args()
    
    # 设置API环境变量（命令行参数优先于.env文件）
    api_key = args.api_key  # 如果用命令行提供则使用，否则使用.env中的变量
    base_url = args.base_url  # 如果用命令行提供则使用，否则使用.env中的变量
    
    try:
        # 设置目录
        base_dir, persist_dir, cache_dir, metadata_file = create_kb_directories()
        print(f"知识库目录: {base_dir}")
        
        # 创建知识库实例
        print("初始化知识库...")
        kb = KnowledgeBase(
            persist_dir=str(persist_dir),
            cache_dir=str(cache_dir),
            metadata_file=str(metadata_file),
            api_key=api_key,
            base_url=base_url
        )
        print("知识库初始化完成")
        
        # 执行指定的操作
        if args.add:
            add_document(kb, args.add)
        
        if args.search:
            search_documents(kb, args.search, k=args.k)
        
        if args.list:
            list_documents(kb)
        
        if args.stats or not any([args.add, args.search, args.list]):
            # 如果没有指定操作，默认显示统计信息
            print_kb_stats(kb)
            
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        print(f"程序出错: {str(e)}")
        import traceback
        print(f"错误堆栈: {traceback.format_exc()}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main()) 