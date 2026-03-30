# 🤖 AgentCoder 

**AgentCoder ** 是一个基于大语言模型（LLM）的自主多智能体协同开发框架。它突破了传统 AI 代码生成器仅停留在文本层面的局限，通过赋予智能体“物理双手”（工具调用），实现了从**需求规划**、**代码编写**、**沙盒编译**到**自动化测试修复**的全流程自愈闭环。

---

## ✨ 核心特性

* **👥 多角色部门分工**：
    * **架构师 (Architect)**：负责全局技术栈规划与逻辑方案设计。
    * **程序员 (Coder)**：执行架构图纸，通过物理工具将代码实时写入硬盘。
    * **测试员 (Tester)**：在独立沙盒执行命令，捕获 `stderr` 并触发自愈逻辑。
* **🔄 自愈闭环 (Self-Correction)**：基于 **LangGraph** 状态机，实现 `测试报错 -> 提取上下文 -> 重新编码 -> 再次验证` 的自动化迭代过程。
* **🛠️ 物理直写交互**：Agent 直接触发宿主机的 `sys_openat`、`sys_write` 和 `sys_execve` 等系统调用，而非操作虚拟缓冲区。
* **⚖️ 灵活的 LLM 配置**：支持为不同角色独立配置模型版本（如 **GLM-5**）、Temperature 及 API 端点。
* **🛡️ 生产级安全防护**：内置目录穿越拦截逻辑，强制将 Agent 行为锁定在 `workspace/` 隔离区。

---

## 🏗️ 系统架构

### 📂 目录结构预览

```text
Agent_Coder/
├── main.py                 # 项目启动入口 (递归限制与流转逻辑)
├── core/                   # 核心中枢
│   ├── config.py           # Agent 模型凭证与全局配置
│   ├── graph.py            # LangGraph 工作流编排与路由控制
│   ├── nodes.py            # 物理工具节点注册与映射
│   └── state.py            # 全局共享状态字典 (GraphState)
├── agents/                 # 数字员工角色 (Prompt Layer)
│   ├── architect.py        # 负责系统架构设计
│   ├── coder.py            # 负责代码实现与落盘
│   └── tester.py           # 负责沙盒验证与错误捕获
├── tools/                  # 物理交互工具箱 (Action Layer)
│   ├── fs_tools.py         # 文件系统工具 (write/read/ls)
│   └── exec_tools.py       # 终端执行工具 (subprocess/shell)
└── workspace/              # ⚠️ 物理沙盒隔离区 (代码产出的案发现场)
```

# 🚀 快速开始
1. ### 环境准备

确保你的系统安装了 Python 3.8+，推荐在 Linux 环境（如 Ubuntu 22.04+）下运行。
创建并激活虚拟环境
```Bash
python3 -m venv venv
source venv/bin/activate
```

安装核心依赖
```Bash
pip install langchain-openai langgraph python-dotenv
```

2. ### 配置中心

打开 core/config.py，配置您的模型凭证：
```Python
# core/config.py
AGENT_LLM_CONFIG = {
    "architect": {
        "model": "glm-5",
        "api_key": "YOUR_API_KEY",
        "base_url": "https://open.bigmodel.cn/api/paas/v4/",
        "temperature": 0.7
    },
    # 按照相同格式配置 coder 和 tester...
}
```
3. ### 运行项目
```Bash
python3 main.py
```

🛡️ 安全与审计

    路径隔离：所有文件操作均经过 os.path.abspath 校验，严禁 Agent 越权访问 workspace/ 以外的路径。

    执行超时：默认所有 execute_command 动作设有 30 秒硬超时，防止 Agent 误触发死循环进程。

    日志追踪：所有 Agent 的思考路径与工具调用细节均在终端实时输出，便于开发者审计。