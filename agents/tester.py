# agents/tester.py
from langchain_core.messages import SystemMessage
# 🐛 修复点 1：使用重构后的新函数名 get_llm
from utils.llm_client import get_llm 
from tools.fs_tools import write_file, read_file, list_directory
from tools.exec_tools import execute_command
from core.state import AgentState

TESTER_PROMPT = """你是一名严苛的测试开发工程师（QA）。
你的目标是确保【程序员】编写的代码完全符合设计要求，并且能够真实运行。

### 你的硬性工作流：
1. **摸清现状**：调用 `list_directory` 查看当前生成了哪些代码文件。
2. **编写测试脚本**：如果项目中没有测试文件，主动调用 `write_file` 写一个（如 `test_main.py`）。
3. **执行并观测（关键）**：你必须调用 `execute_command` 运行代码或测试脚本（例如 `python3 src/main.py` 或 `gcc src/main.c -o main && ./main`）。
4. **判定结果**：
   - 如果运行报错或逻辑不对，你必须严厉指出错误原因，并将完整的报错日志反馈在对话中，要求 Coder 重新修改。
   - 如果成功且无错误输出，请输出“✅ 测试通过，任务圆满完成”。

### ⚠️ 纪律要求：
绝对不要假设代码能跑通！你必须通过 `execute_command` 看到真实的输出结果后，才能下定论。
"""

# 🐛 修复点 2：调用 get_llm("tester") 获取配置
llm = get_llm("tester")

# Tester 需要执行命令、读文件和看目录的能力
llm_with_tools = llm.bind_tools([write_file, read_file, list_directory, execute_command])

def tester_node(state: AgentState) -> dict:
    print("🧪 [Tester Agent]: 正在生成测试用例并执行沙盒验证...")
    messages = [SystemMessage(content=TESTER_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response], "current_agent": "Tester"}