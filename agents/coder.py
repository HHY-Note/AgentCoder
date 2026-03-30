# agents/coder.py
from langchain_core.messages import SystemMessage
from utils.llm_client import get_llm
from tools.fs_tools import write_file, read_file, list_directory
from core.state import AgentState

# ==========================================
# 1. 定义程序员的 System Prompt (铁血编码纪律)
# ==========================================
CODER_PROMPT = """你是一名的资深高级程序员（Coder）。
你的任务是：严格按照前文【架构师（Architect）】输出的 Markdown 设计文档，编写高质量的源代码，并将其真实地保存到物理硬盘上。

### 你的核心工作流：
1. **阅读图纸**：仔细阅读对话历史中架构师提供的架构设计和目录树规划。
2. **物理落盘（关键）**：你不能仅仅在对话框里输出代码，你**必须**主动调用 `write_file` 工具，将每一份写好的代码保存到指定的相对路径中！
3. **逐步构建**：如果架构师规划了多个文件，请多次调用 `write_file` 逐一创建它们。
4. **环境感知**：如果在写代码过程中，需要查看之前写的文件内容或目录结构，请主动调用 `read_file` 或 `list_directory` 工具。

### ⚠️ 严格纪律：
- 绝对不要只回答“代码如下”，必须触发工具调用！
- 所有路径必须是相对于工作区（workspace）的相对路径，例如 `src/main.py` 或 `README.md`。
- 保持代码的严谨性，确保能直接运行。
"""

# ==========================================
# 2. 实例化低温度的大脑与绑定全套工具
# ==========================================
# 细节: 读取 core/config.py 中为 coder 配置的模型。
# 这里的 temperature 是 0.1，极其冷静严谨，防止 AI 产生幻觉乱写代码。
llm = get_llm("coder")

# 细节: Coder 需要干脏活累活，所以给它绑定了所有的物理操作工具
llm_with_tools = llm.bind_tools([write_file, read_file, list_directory])

# ==========================================
# 3. 定义 LangGraph 节点函数 (The Coder Node)
# ==========================================
def coder_node(state: AgentState) -> dict:
    """
    程序员 Agent 的执行逻辑节点。
    """
    print("💻 [Coder Agent]: 正在根据架构规划，疯狂敲击键盘并写入硬盘...")
    
    # 细节: 把程序员的人设和之前的聊天记录（包含架构师的 Markdown 文档）一起塞给大模型
    messages = [SystemMessage(content=CODER_PROMPT)] + state["messages"]
    
    # 细节: 唤醒大模型。因为绑定了工具，GLM-5 读完提示词后，大概率会返回一个 ToolCall 请求。
    response = llm_with_tools.invoke(messages)
    
    return {"messages": [response], "current_agent": "Coder"}