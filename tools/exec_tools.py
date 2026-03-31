# tools/exec_tools.py
import subprocess
from langchain_core.tools import tool
from tools.fs_tools import get_workspace_root

@tool
def execute_command(command: str) -> str:
    """
    在工作区终端中执行 Shell 或编译命令。
    例如: "make all", "gcc -o main src/main.c", "./test_runner"
    """
    workspace_dir = get_workspace_root()
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=workspace_dir,
            text=True,
            capture_output=True,
            timeout=30 # 防止跑死循环
        )
        output = f"命令: {command}\n"
        output += f"[STDOUT]\n{result.stdout}\n" if result.stdout else ""
        output += f"[STDERR]\n{result.stderr}\n" if result.stderr else ""
        output += f"Return Code: {result.returncode}"
        return output
    except subprocess.TimeoutExpired:
        return f"❌ 命令执行超时 (30秒): {command}"
    except Exception as e:
        return f"❌ 执行报错: {str(e)}"

@tool
def run_with_test_data(command: str, test_data: str) -> str:
    """
    运行可执行文件，并通过标准输入 (stdin) 注入测试数据。
    适用于需要 scanf/cin 读取数据的程序。
    """
    workspace_dir = get_workspace_root()
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=workspace_dir,
            input=test_data,
            text=True,
            capture_output=True,
            timeout=10
        )
        output = f"执行命令: {command}\n"
        output += f"[输出结果]\n{result.stdout}\n" if result.stdout else ""
        output += f"[错误信息]\n{result.stderr}\n" if result.stderr else ""
        output += f"Return Code: {result.returncode}"
        return output
    except Exception as e:
        return f"❌ 测试执行失败: {str(e)}"