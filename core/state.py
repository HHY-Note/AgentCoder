# core/state.py
import operator
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    AgentCoder Pro 全局状态 (实时物理直写版)
    """
    # 核心：利用 LangGraph 标准的消息列表。
    # 所有的需求、报错、Agent 的思考过程，都作为消息追加在这里。
    # 我们不再把文件内容存在状态里了！
    messages: Annotated[List[BaseMessage], operator.add]
    
    task_description: str        # 初始任务描述
    workspace_dir: str           # 物理隔离区：限制 Agent 只能在这个物理目录下折腾，防止 rm -rf /
    error_count: int             # 连续执行报错的次数
    current_agent: str           # 当前正在行动的 Agent 角色名