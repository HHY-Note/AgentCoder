# agents/architect.py
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from utils.llm_client import get_llm
from tools.fs_tools import list_directory  # 引入我们写的物理工具
from core.state import AgentState

# ==========================================
# 1. 定义架构师的 System Prompt (人设与规章)
# 🎯 这里落实了你关于 Markdown 的要求！
# ==========================================
ARCHITECT_PROMPT = """你是一名的资深软件架构师。你的职责是根据用户的原始需求，设计高内聚、低耦合的系统架构。

### 核心工作流：
1. **环境勘测**：主动调用 `list_directory` 工具，查看当前 `workspace` 目录下已有的文件结构（如果是空项目，也请确认）。
2. **系统设计**：根据需求和环境现状，规划技术栈、模块划分、关键类的定义。
3. **技术输出**：生成一份详尽的技术设计文档。

### ⚠️ 输出格式严格要求（大型项目必备）：
你**必须**使用清晰的 **Markdown** 格式来输出你的设计文档。大模型很容易看懂这种结构。
必须包含以下 Markdown 章节：
# 1. 项目概述 (Project Overview)
(简述系统功能)

# 2. 技术栈 (Technology Stack)
(列出主要使用的库和工具)

# 3. 核心模块与文件结构 (Core Modules & File Structure)
你**必须**使用 Markdown 的 **代码块 (Code Block)** 格式来输出预想的目录树。例如：
\`\`\`text
workspace/
├── src/
│   └── main.py
└── README.md
\`\`\`

# 4. 实现计划 (Implementation Plan)
(分步骤描述接下来的开发流)
"""

# ==========================================
# 2. 实例化大脑与绑定工具
# ==========================================
# 细节: 读取 core/config.py 中为 architect 配置的模型和温度
llm = get_llm("architect")

# 细节: 将 list_directory 工具“挂载”到大脑上。
# GLM-5 现在知道自己拥有了通过物理 API 查看目录的能力。
llm_with_tools = llm.bind_tools([list_directory])

# ==========================================
# 3. 定义 LangGraph 节点函数 (The Architect Node)
# ==========================================
def architect_node(state: AgentState) -> dict:
    """
    架构师 Agent 的执行逻辑节点。
    """
    print("🧐 [Architect Agent]: 正在思考系统设计方案...")
    
    # 构建消息列表：人设 Prompt + 历史对话记录
    # 细节: 这是一个 Tools-aware 的 Agent，它需要知道之前的工具调用结果。
    messages = [SystemMessage(content=ARCHITECT_PROMPT)] + state["messages"]
    
    # 细节: 调用绑定了工具的大模型。大模型可能会返回工具调用请求，也可能直接返回文本。
    response = llm_with_tools.invoke(messages)
    
    # 细节: 我们将大模型的回复作为一个新消息，返回给 LangGraph 状态机。
    # LangGraph 的 Reducer (operator.add) 会自动把它追加到 state["messages"] 列表中。
    return {"messages": [response], "current_agent": "Architect"}