### 问题总结与开发日志 (DevLog)

---

#### **1. LangChain弃用警告**
- **问题**：`LangChainDeprecationWarning`提示`TextLoader`导入路径已弃用
- **解决**：更新导入路径为`from langchain_community.document_loaders import TextLoader`
- **相关文件**：`loader.py`

#### **2. 文件扩展名不支持**
- **问题**：`.text`扩展名文件无法加载，仅支持`.txt`
- **解决**：在`SUPPORTED_FORMATS`中添加`.text`扩展名支持
- **代码修改**：
  ```python
  SUPPORTED_FORMATS = {
      'txt': TextLoader,
      'text': TextLoader,  # 新增支持
      ...
  }
  ```
- **相关文件**：`loader.py`

#### **3. 文件编码错误**
- **问题**：Windows默认GBK编码导致UTF-8文件读取失败
- **解决**：显式指定`TextLoader`使用UTF-8编码
- **代码修改**：
  ```python
  'txt': lambda path: TextLoader(path, encoding='utf-8'),
  'text': lambda path: TextLoader(path, encoding='utf-8')
  ```
- **相关文件**：`loader.py`

#### **4. Chroma API变更**
- **问题**：`'Chroma' object has no attribute 'persist'`
- **解决**：移除对`persist()`方法的调用，新版Chroma自动持久化
- **代码修改**：
  ```python
  # 移除 self.vectorstore.persist()
  ```
- **相关文件**：`loader.py`

#### **5. 环境变量加载**
- **问题**：需手动输入API密钥，未利用已有`.env`文件
- **解决**：添加`python-dotenv`支持，优先从`.env`加载密钥
- **代码修改**：
  ```python
  from dotenv import load_dotenv
  load_dotenv()  # 加载.env文件
  ```
- **相关文件**：`knowledge_base_demo.py`

---

### **DevLog 记录**
```markdown
# 开发日志 - 2024/06/13

## 问题修复记录

### 1. 文件加载问题
- **错误点**：`.text`文件无法加载 + 编码错误
- **解决方式**：
  - 扩展`SUPPORTED_FORMATS`支持`.text`
  - 强制指定UTF-8编码
- **影响文件**：`loader.py`

### 2. LangChain兼容性
- **错误点**：弃用警告 + Chroma API变更
- **解决方式**：
  - 更新导入路径至`langchain_community`
  - 移除废弃的`persist()`调用
- **影响文件**：`loader.py`, `knowledge_base.py`

### 3. 环境变量优化
- **错误点**：API密钥需手动输入
- **解决方式**：集成`python-dotenv`自动加载`.env`
- **影响文件**：`knowledge_base_demo.py`

## 后续改进
- [ ] 添加更详细的错误日志
- [ ] 支持更多文件格式（如Word）
- [ ] 优化缓存机制
```

---

### 最终效果
- ✅ 支持`.text`和`.txt`文件
- ✅ 自动从`.env`读取API密钥
- ✅ 兼容最新LangChain API
- ✅ 中英文编码问题修复


### 遇到的问题与解决方案总结

#### 1. 依赖管理冲突
- **问题**：`setup.py`与`environment.yml`存在重复依赖定义
- **解决**：明确分工：
  - `environment.yml`：开发环境（Conda管理Python版本+系统依赖）
  - `setup.py`：生产环境（仅核心依赖+可选开发工具）
- **关键代码**：
  ```python
  # setup.py中分离核心依赖与开发依赖
  install_requires=[...],  # 生产必需
  extras_require={"dev": [...]}  # 开发工具
  ```

#### 2. 文件加载兼容性
- **问题**：`.text`文件无法加载且编码错误
- **解决**：
  - 扩展支持`.text`后缀
  - 强制UTF-8编码读取
- **代码修改**：
  ```python
  SUPPORTED_FORMATS = {
      'text': lambda path: TextLoader(path, encoding='utf-8'),
      'txt': lambda path: TextLoader(path, encoding='utf-8')
  }
  ```

#### 3. 版本兼容性问题
- **问题**：Chroma的`persist()`方法在新版中移除
- **解决**：删除过时方法调用，依赖自动持久化
- **影响文件**：`loader.py`

#### 4. 环境变量加载
- **问题**：需手动输入API密钥
- **解决**：优先从`.env`读取，命令行参数覆盖
- **关键逻辑**：
  ```python
  # 优先级：命令行参数 > 环境变量 > .env文件
  api_key = args.api_key or os.getenv("AIHUBMIX_API_KEY")
  ```

### DevLog 开发日志

```markdown
2024-06-13 | 依赖管理重构
-----------------------------
* 问题: Conda与pip依赖重复
* 修改:
  - environment.yml → 开发环境(含系统依赖)
  - setup.py → 生产部署(核心依赖+dev可选)
* 影响文件: setup.py

2024-06-13 | 文件加载优化
-----------------------------
* 问题: 
  1. .text文件不支持
  2. 中文编码错误
* 修改:
  - 添加.text扩展名支持
  - 强制UTF-8编码
* 影响文件: loader.py

2024-06-13 | API兼容性修复
-----------------------------
* 问题: Chroma弃用persist()
* 修改: 移除过时方法调用
* 影响文件: knowledge_base.py

2024-06-13 | 环境变量优化
-----------------------------
* 问题: API密钥需手动输入
* 修改:
  - 增加python-dotenv支持
  - 实现配置优先级链
* 影响文件: knowledge_base_demo.py
```

### 最终架构说明
```python
"""
依赖管理流程:
1. 开发环境: conda env create -f environment.yml
2. 生产部署: pip install . 或 pip install .[dev]
3. 密钥加载顺序:
   CLI参数 > 环境变量 > .env文件 > 默认值
"""
```