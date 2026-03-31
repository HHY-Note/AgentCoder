# core/graph.py
from langgraph.graph import StateGraph, END
from core.state import AgentState
from core.nodes import tool_node
from agents.architect import architect_node
from agents.coder import coder_node
from agents.tester import tester_node

def route_architect(state: AgentState):
    last_msg = state["messages"][-1]
    return "tools" if getattr(last_msg, "tool_calls", None) else "coder"

def route_coder(state: AgentState):
    last_msg = state["messages"][-1]
    return "tools" if getattr(last_msg, "tool_calls", None) else "tester"

def route_tester(state: AgentState):
    last_msg = state["messages"][-1]
    if getattr(last_msg, "tool_calls", None):
        return "tools"
        
    content = last_msg.content if getattr(last_msg, "content", None) else ""
    if "✅" in content or "测试通过" in content:
        return END
    elif "❌" in content or "测试未通过" in content:
        print(f"\n🔄 [流水线打回]: 提取到错误报告，召唤 Coder 回归修复代码...")
        return "coder"
        
    return END

def route_tools(state: AgentState):
    agent = state.get("current_agent", "").lower()
    
    if agent == "architect": return "architect"
    if agent == "coder": return "coder"
    if agent == "tester": return "tester"
    
    print("\n⚠️ [底层警告]: 路由迷失，正在执行状态自愈...")
    return "architect"

def build_agent_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("architect", architect_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("tester", tester_node)
    workflow.add_node("tools", tool_node)

    workflow.set_entry_point("architect")
    workflow.add_conditional_edges("architect", route_architect)
    workflow.add_conditional_edges("coder", route_coder)
    workflow.add_conditional_edges("tester", route_tester)
    workflow.add_conditional_edges("tools", route_tools)

    return workflow.compile()