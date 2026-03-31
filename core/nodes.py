from langgraph.prebuilt import ToolNode
from tools.fs_tools import write_file, read_file, list_directory
from tools.exec_tools import execute_command, run_with_test_data

# 集中注册所有工具
tools = [write_file, read_file, list_directory, execute_command, run_with_test_data]

# 2. 实例化 LangGraph 预制的工具执行节点
# 当流转到这个节点时，它会自动解析 state["messages"] 中最新的 tool_calls，
# 并去宿主机执行对应的操作（引发 eBPF 监控的底层 IO 和拉起进程）。
tool_node = ToolNode(tools)