# agents/coder.py
import os
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage, ToolMessage
from utils.llm_client import get_llm
from tools.fs_tools import list_directory, read_file, write_file
from core.prompts import CODER_PROMPT
from core.state import AgentState

def coder_node(state: AgentState) -> dict:
    llm = get_llm("coder")
    model_name = getattr(llm, 'model_name', '未知模型')
    
    if not state.get("messages") or not isinstance(state["messages"][-1], ToolMessage):
        print(f"\n🚀 [系统底层] 主进程拉起了 CODER Agent (PID: {os.getpid()})")
        print(f"💻 [Coder PID:{os.getpid()} | Model: {model_name}]: 正在生成代码...")
        
    llm_with_tools = llm.bind_tools([list_directory, read_file, write_file])
    
    clean_messages = [SystemMessage(content=CODER_PROMPT)]
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
                print(f"   └─ 💾 Coder 正在落盘物理文件: {tc['args'].get('file_path')}")
            elif tc['name'] == 'read_file':
                print(f"   └─ 📖 Coder 正在仔细研读: {tc['args'].get('file_path')}")
    else:
        # 💡把 Coder 偷懒时的废话打印出来，让你抓个现行！
        content = response.content.replace("\n", " ")
        if "</think>" in content: content = content.split("</think>")[-1].strip()
        print(f"   💬 [警告] Coder 试图口头敷衍 (未调用工具): {content[:80]}...")
    
    return {"messages": [response], "current_agent": "coder"}