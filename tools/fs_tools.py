# tools/fs_tools.py
import os
from langchain_core.tools import tool

def get_workspace_root() -> str:
    """动态获取工作区根目录"""
    # 💡 核心修复 2：优先读取 main.py 下发的 AGENT_WORKSPACE，如果没有再兜底使用 workspace
    default_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "workspace"))
    return os.environ.get("AGENT_WORKSPACE", default_dir)

def get_safe_path(file_path: str) -> str:
    """安全拦截：防止 Agent 使用 ../ 越权读取物理机其他文件"""
    base_dir = get_workspace_root()
    safe_path = os.path.abspath(os.path.join(base_dir, file_path))
    if not safe_path.startswith(base_dir):
        raise ValueError(f"安全拦截：禁止访问工作区之外的路径 -> {file_path}")
    return safe_path

@tool
def list_directory(dir_path: str = ".") -> str:
    """
    列出指定目录下的所有文件和文件夹。
    如果不知道当前有哪些文件，请先调用此工具。
    参数 dir_path: 相对路径，默认为当前工作区根目录 "."
    """
    try:
        target_dir = get_safe_path(dir_path)
        if not os.path.exists(target_dir):
            return f"❌ 目录不存在: {dir_path}"
        files = os.listdir(target_dir)
        return f"📂 目录 {dir_path} 下的内容:\n" + "\n".join(files) if files else "目录为空"
    except Exception as e:
        return f"❌ 读取目录失败: {str(e)}"

@tool
def read_file(file_path: str) -> str:
    """
    读取指定物理文件的内容。
    参数 file_path: 相对路径，如 "src/main.c"
    """
    try:
        target_file = get_safe_path(file_path)
        if not os.path.exists(target_file):
            return f"❌ 文件不存在: {file_path}"
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        return f"📄 {file_path} 的内容:\n{content}"
    except Exception as e:
        return f"❌ 读取文件失败: {str(e)}"

@tool
def write_file(file_path: str, content: str) -> str:
    """
    将代码或文本内容写入到指定的物理文件中。如果文件不存在则创建，如果存在则覆盖。
    参数 file_path: 相对路径，如 "src/sort.c"
    """
    try:
        target_file = get_safe_path(file_path)
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ 成功将内容写入文件: {file_path}"
    except Exception as e:
        return f"❌ 写入文件失败: {str(e)}"