# core/graph.py
from langgraph.graph import StateGraph, END
from core.state import AgentState
from core.nodes import tool_node
from agents.architect import architect_node
from agents.coder import coder_node
from agents.tester import tester_node

# ==========================================
# 1. 定义条件路由逻辑 (Router Functions)
# ==========================================
def route_architect(state: AgentState):
    """架构师节点的出口路由"""
    last_msg = state["messages"][-1]
    if getattr(last_msg, "tool_calls", None):
        return "tools" # 申请查目录，去工具节点
    return "coder"     # 规划完毕，交棒给程序员

def route_coder(state: AgentState):
    """程序员节点的出口路由"""
    last_msg = state["messages"][-1]
    if getattr(last_msg, "tool_calls", None):
        return "tools" # 申请写文件，去工具节点
    return "tester"    # 代码写完，交棒给测试员跑沙盒

def route_tester(state: AgentState):
    """测试员节点的出口路由 (自愈闭环的核心)"""
    last_msg = state["messages"][-1]
    if getattr(last_msg, "tool_calls", None):
        return "tools" # 申请跑测试命令，去工具节点
    
    # 🐛 修复点 1：将错误的 last_message 统一改为 last_msg
    content = last_msg.content if getattr(last_msg, "content", None) else ""
    if "✅" in content or "测试通过" in content:
        print("\n🎉 [系统状态]: 物理测试全量通过，流水线安全终止。")
        return END
    
    # 如果没通过，触发打回重做逻辑
    error_count = state.get("error_count", 0)
    if error_count >= 5:
        print(f"\n🛑 [熔断机制]: 连续修复失败 {error_count} 次，疑似陷入逻辑死循环，强制终止！")
        return END
        
    print(f"\n🔄 [打回重做]: 测试失败 (已失败 {error_count} 次)，附带报错日志打回给 Coder...")
    return "coder"

def route_tools(state: AgentState):
    """工具节点的出口路由：执行完工具后，谁请求的就回谁那里"""
    # 🐛 修复点 2：统一转换为小写，防止 "Architect" 和 "architect" 大小写不匹配导致路由断裂
    agent = state.get("current_agent", "").lower()
    
    if agent == "architect": return "architect"
    if agent == "coder": return "coder"
    if agent == "tester": return "tester"
    
    return END

# ==========================================
# 2. 构建有向无环图 (DAG)
# ==========================================
def build_agent_graph():
    workflow = StateGraph(AgentState)

    # 注册所有实体节点
    workflow.add_node("architect", architect_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("tester", tester_node)
    workflow.add_node("tools", tool_node)

    # 设定整个流水线的物理入口
    workflow.set_entry_point("architect")

    # 绑定复杂的条件边
    workflow.add_conditional_edges("architect", route_architect)
    workflow.add_conditional_edges("coder", route_coder)
    workflow.add_conditional_edges("tester", route_tester)
    workflow.add_conditional_edges("tools", route_tools)

    # 编译成可执行的程序
    return workflow.compile()