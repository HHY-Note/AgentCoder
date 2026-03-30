# tools/exec_tools.py
import os
import subprocess
from langchain_core.tools import tool

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.getcwd(), "workspace"))

@tool
def execute_command(command: str) -> str:
    """
    在工作区 (workspace) 内执行终端命令。
    用于：编译代码 (gcc)、运行脚本 (python3)、执行单元测试。
    """
    print(f"⚙️  [沙盒执行]: {command}")
    try:
        # 细节：必须设置 cwd=WORKSPACE_ROOT，确保 AI 不会乱跑
        # 细节：设置 timeout，防止 AI 写出死循环导致宿主机卡死，这也会产生异常日志供 eBPF 捕获
        result = subprocess.run(
            command, shell=True, cwd=WORKSPACE_ROOT,
            capture_output=True, text=True, timeout=15
        )
        
        output = f"Exit Code: {result.returncode}\n"
        if result.stdout: output += f"STDOUT: {result.stdout}\n"
        if result.stderr: output += f"STDERR: {result.stderr}\n"
        return output
    except subprocess.TimeoutExpired:
        return "❌ 错误：命令执行超时（15秒）。可能存在无限循环或性能极差。"
    except Exception as e:
        return f"❌ 运行异常: {str(e)}"