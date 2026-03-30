import os
from langchain_core.tools import tool

# 定义全局物理隔离区：强制 AI 只能在这个目录下操作
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.getcwd(), "workspace"))

def _get_safe_path(relative_path: str) -> str:
    """
    内部核心安全函数：防止目录穿越攻击 (Path Traversal)
    """
    # 1. 确保工作区根目录存在
    if not os.path.exists(WORKSPACE_ROOT):
        os.makedirs(WORKSPACE_ROOT)
    
    # 2. 将 AI 传入的相对路径转换为绝对路径
    # 例如：传入 "src/main.py" -> "/home/hhy/Agent_Coder/workspace/src/main.py"
    target_path = os.path.abspath(os.path.join(WORKSPACE_ROOT, relative_path))
    
    # 3. 终极安全校验：检查解析后的绝对路径，是否依然在 WORKSPACE_ROOT 之下
    # 如果 AI 试图传入 "../../etc/passwd"，target_path 会跑到工作区外面，这里就会拦截！
    if not target_path.startswith(WORKSPACE_ROOT):
        raise PermissionError(f"🚨 越权访问拦截！禁止访问工作区之外的路径: {relative_path}")
    
    return target_path

@tool
def write_file(file_path: str, content: str) -> str:
    """
    向指定文件写入内容。如果文件或目录不存在，会自动创建。
    这是一个覆写操作，会替换文件原有的所有内容。
    
    参数:
    - file_path: 相对于工作区的路径 (例如: 'src/main.py' 或 'README.md')
    - content: 要写入的完整文件内容
    """
    try:
        safe_path = _get_safe_path(file_path)
        
        # 提取文件所在的目录，如果目录不存在则连同父目录一起创建 (对应底层 sys_mkdir)
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        
        # 打开文件并写入 (对应底层 sys_openat 和 sys_write)
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ 成功写入文件: {file_path}"
    except Exception as e:
        return f"❌ 写入文件失败: {str(e)}"

@tool
def read_file(file_path: str) -> str:
    """
    读取指定文件的内容。在修改文件前，请先调用此工具查看文件现状。
    
    参数:
    - file_path: 相对于工作区的路径 (例如: 'src/main.py')
    """
    try:
        safe_path = _get_safe_path(file_path)
        if not os.path.exists(safe_path):
            return f"⚠️ 文件不存在: {file_path}"
        
        # 对应底层 sys_openat 和 sys_read
        with open(safe_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"❌ 读取文件失败: {str(e)}"

@tool
def list_directory(dir_path: str = ".") -> str:
    """
    列出指定目录下的所有文件和文件夹，帮助你了解当前的项目结构。
    
    参数:
    - dir_path: 相对于工作区的目录路径，默认为根目录 "."
    """
    try:
        safe_path = _get_safe_path(dir_path)
        if not os.path.exists(safe_path):
            return f"⚠️ 目录不存在: {dir_path}"
        
        # 对应底层 sys_getdents64
        items = os.listdir(safe_path)
        if not items:
            return f"📂 目录 {dir_path} 是空的。"
        return f"📂 目录 {dir_path} 包含以下内容:\n" + "\n".join(items)
    except Exception as e:
        return f"❌ 列出目录失败: {str(e)}"