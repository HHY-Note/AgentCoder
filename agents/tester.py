# agents/tester.py
import os
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage, ToolMessage
from utils.llm_client import get_llm
from tools.fs_tools import list_directory, read_file, write_file
from tools.exec_tools import execute_command, run_with_test_data
from core.prompts import TESTER_PROMPT
from core.state import AgentState

def tester_node(state: AgentState) -> dict:
    llm = get_llm("tester")
    model_name = getattr(llm, 'model_name', '未知模型')
    
    if not state.get("messages") or not isinstance(state["messages"][-1], ToolMessage):
        print(f"\n🚀 [系统底层] 主进程拉起了 TESTER Agent (PID: {os.getpid()})")
        print(f"🧪 [Tester PID:{os.getpid()} | Model: {model_name}]: 正在构思测试方案并准备沙盒环境...")
        
    tools = [list_directory, read_file, write_file, execute_command, run_with_test_data]
    llm_with_tools = llm.bind_tools(tools)
    
    clean_messages = [SystemMessage(content=TESTER_PROMPT)]
    for msg in state.get("messages", []):
        if isinstance(msg, BaseMessage):
            clean_messages.append(msg)
        elif isinstance(msg, tuple) and len(msg) >= 2:
            clean_messages.append(HumanMessage(content=str(msg[-1])))
        else:
            clean_messages.append(HumanMessage(content=str(msg)))
            
    response = llm_with_tools.invoke(clean_messages)
    
    if getattr(response, "tool_calls", None):
        for tc in response.tool_calls:
            if tc['name'] == 'write_file':
                fname = tc['args'].get('file_path', '')
                if 'report' in fname:
                    print(f"   └─ 📑 测试员正在撰写错误报告: {fname}")
                else:
                    print(f"   └─ 🧪 测试样例生成中，落盘物理文件: {fname}")
            elif tc['name'] in ['execute_command', 'run_with_test_data']:
                cmd = tc['args'].get('command', '')
                print(f"   └─ ⚙️  执行测试中: 终端运行 [{cmd}]")
    else:
        content = response.content.strip()
        if "</think>" in content: content = content.split("</think>")[-1].strip()
        if "❌" in content:
            print(f"\n   🚨 [缺陷拦截]: Tester 发现了漏洞，已写入 test_report.md")
        elif "✅" in content:
            print(f"\n   ✨ [验证成功]: ✅ 测试全量通过，代码完美运行！")
            
    return {"messages": [response], "current_agent": "tester"}