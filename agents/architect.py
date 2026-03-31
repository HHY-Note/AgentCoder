# agents/architect.py
import os
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage, ToolMessage
from utils.llm_client import get_llm
from tools.fs_tools import list_directory, read_file, write_file
from core.prompts import ARCHITECT_PROMPT
from core.state import AgentState

def architect_node(state: AgentState) -> dict:
    llm = get_llm("architect")
    model_name = getattr(llm, 'model_name', '未知模型')
    
    if not state.get("messages") or not isinstance(state["messages"][-1], ToolMessage):
        print(f"\n🚀 [系统底层] 主进程拉起了 ARCHITECT Agent (PID: {os.getpid()})")
        print(f"🧐 [Architect PID:{os.getpid()} | Model: {model_name}]: 正在深度思考并构筑软件架构 (请耐心等待推理)...")
        
    llm_with_tools = llm.bind_tools([list_directory, read_file, write_file])
    
    # 🛡️ 终极数据清洗罩
    clean_messages = [SystemMessage(content=ARCHITECT_PROMPT)]
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
                print(f"   └─ 📝 架构师正在撰写物理文档: {tc['args'].get('file_path')}")
            else:
                print(f"   └─ 🔍 架构师正在勘测: {tc['name']}")
    else:
        content = response.content.replace("\n", " ")
        if "</think>" in content: content = content.split("</think>")[-1].strip()
        print(f"   💬 架构师回复: {content[:100]}...")
            
    return {"messages": [response], "current_agent": "architect"}