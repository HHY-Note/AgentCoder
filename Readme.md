🤖 AgentCoder : 基于 LLM 的多智能体协同开发框架

AgentCoder 是一个打破“文本生成”局限，赋予大模型（LLM）物理操作能力的自主开发框架。它通过多角色智能体协同，实现了从需求分拆、代码落盘到沙盒编译/测试自愈的全流程闭环。
✨ 核心特性
    👥 多角色部门分工：
架构师 (Architect)：全局技术栈规划，产出 Markdown 格式的设计文档。
程序员 (Coder)：严格执行图纸，通过物理工具将代码实时写入硬盘。
测试员 (Tester)：在独立沙盒执行 make 或 python 命令，捕获 stderr 并触发自愈逻辑。

    🔄 自愈闭环 (Self-Correction)：基于 LangGraph 状态机，实现 测试报错 -> 提取上下文 -> 重新编码 -> 再次验证 的全自动化迭代。
    🛠️ 物理直写交互：Agent 不再操作内存缓冲区，而是直接触发宿主机的 sys_openat、sys_write 和 sys_execve 系统调用。
    ⚖️ 灵活的 LLM 注册机制：允许为不同角色独立配置模型版本（如 GLM-5）、Temperature、API Key 及不同的 URL 端点。
    🛡️ 生产级安全防护：内置目录穿越拦截逻辑，强制将 Agent 行为锁定在 workspace/ 物理隔离区。
🏗️ 系统架构
目录结构预览
Agent_Coder/
├── main.py                 # 项目启动入口 (入口逻辑与递归限制配置)
├── core/                   # 核心中枢
│   ├── config.py           # Agent 模型、凭证与端点配置中心
│   ├── graph.py            # LangGraph 工作流编排与逻辑路由
│   ├── nodes.py            # 物理工具节点注册与映射
│   └── state.py            # 全局共享状态字典 (GraphState)
├── agents/                 # 数字员工角色 (Prompt Layer)
│   ├── architect.py        # 负责系统规划与逻辑设计
│   ├── coder.py            # 负责代码实现与物理落盘
│   └── tester.py           # 负责执行环境验证与报错捕获
├── tools/                  # 物理交互工具箱 (Action Layer)
│   ├── fs_tools.py         # 文件系统工具 (open/write/read/ls)
│   └── exec_tools.py       # 终端执行工具 (subprocess/shell)
└── workspace/              # ⚠️ 物理沙盒隔离区 (Agent 代码产出的案发现场)
🚀 快速开始
1. 环境准备
确保你的系统安装了 Python 3.8+，推荐在 Linux 环境（如 Ubuntu 22.04+）下运行，以获得最佳的终端工具支持。
创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate
安装依赖
pip install langchain-openai langgraph python-dotenv
2. 配置中心
打开 core/config.py，配置您的模型凭证：
core/config.py
AGENT_LLM_CONFIG = {
    "architect": {
        "model": "glm-5",
        "api_key": "YOUR_GLM_API_KEY",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/",
        "temperature": 0.7
    },
    # 其他 Agent 配置...
}
3. 启动开发流程
python3 main.py
启动后，您可以直接输入复杂的开发需求（如：“实现一个基于 BCC 的 eBPF 文件监控程序”），Agent 团队将自动开始协作。