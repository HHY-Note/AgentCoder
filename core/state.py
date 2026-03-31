# core/state.py
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
# 💡 引入官方的状态净化器
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # 使用 add_messages 替代之前的 operator.add，彻底解决类型序列化报错
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    current_agent: str
    error_count: int