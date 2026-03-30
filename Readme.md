AgentCoder Pro 是一个基于大语言模型（LLM）的工业级多智能体协同开发框架。它突破了传统 AI 代码生成器仅停留在文本层面的局限，通过赋予智能体“物理双手”（工具调用），实现了从需求规划、代码编写、沙盒编译到自动化测试修复的全流程自愈闭环。

✨ 核心特性

    👥 多角色部门分工:
        架构师 (Architect)：负责全局技术栈规划与 Markdown 格式的设计文档产出。
        程序员 (Coder)：严格执行架构图纸，通过物理工具将代码实时写入硬盘。
        测试员 (Tester)：在独立沙盒中执行 make 或 python 命令，捕获 stderr 并触发自愈逻辑。

    🔄 自愈闭环 (Self-Correction): 基于 LangGraph 的状态机，实现 测试报错 -> 提取上下文 -> 重新编码 -> 再次验证 的自动化迭代过程。
    🛠️ 物理直写交互: Agent 不再操作内存缓冲区，而是直接触发宿主机的 sys_openat、sys_write 和 sys_execve 等系统调用。
    ⚖️ 灵活的 LLM 注册机制: 允许为不同角色的 Agent 独立配置模型版本（如 GLM-5）、Temperature、API Key 及不同的 URL 端点。
    🛡️ 生产级安全防护: 内置目录穿越拦截逻辑，强制将 Agent 行为锁定在 workspace/ 物理隔离区。


🏗️ 系统架构
目录结构预览
Plaintext

Agent_Coder/
├── main.py                 # 项目启动入口
├── core/                   # 核心中枢
│   ├── config.py           # Agent 模型与凭证配置中心
│   ├── graph.py            # LangGraph 工作流编排与路由逻辑
│   ├── nodes.py            # 物理工具节点注册
│   └── state.py            # 全局共享状态字典
├── agents/                 # 数字员工角色
│   ├── architect.py        # 负责规划
│   ├── coder.py            # 负责编码落盘
│   └── tester.py           # 负责沙盒测试
├── tools/                  # 物理交互工具箱
│   ├── fs_tools.py         # 文件系统工具 (open/write/read/ls)
│   └── exec_tools.py       # 终端执行工具 (subprocess/execve)
└── workspace/              # ⚠️ 物理沙盒隔离区 (Agent 产出代码的案发现场)


🚀 快速开始
1. 环境准备
确保你的系统安装了 Python 3.8+ 且处于 Linux 环境（推荐 5.15+ 内核以支持全部 eBPF 特性）。

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install langchain-openai langgraph python-dotenv

2. 配置 API Key 在 config.py 中

OPENAI_API_KEY="your_glm_key_here"
OPENAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4/"

3. 运行项目
python3 main.py
