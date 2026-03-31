# 🤖 AgentCoder 

**AgentCoder** 是一个基于大语言模型（LLM）的自主多智能体协同开发框架。它突破了传统 AI 代码生成器仅停留在文本层面的局限，通过赋予智能体“物理双手”（工具调用），实现了从**需求规划**、**代码编写**、**沙盒编译**到**自动化测试修复**的全流程自愈闭环。

## ✨ 核心特性

* **🤖 三位一体的极客团队**
  * **Architect (架构师)**: 拥有全局视野。负责解析复杂需求，构筑工程架构，并自动输出详细的物理设计文档（`design.md`）。
  * **Coder (程序员)**: 极致的执行者。严格读取架构图纸，拒绝伪代码，将源码（C/C++, Python, Makefile 等）精准拆分并落盘到对应的物理目录中。
  * **Tester (测试工程师)**: 严苛的 QA 专家。自动构造边缘测试数据，在沙盒中物理执行 `make` 编译与测试脚本。一旦发现 Bug 或 Segment Fault，立即生成 `test_report.md` 错误报告，强制打回 Coder 重构。
* **⌨️ 极佳的交互体验**
  * 支持终端多行命令需求，支持任意指定项目工作区。

## 📂 核心目录结构

```Plain Text
AGENT_CODER/
├── agents/                  # 智能体核心大脑
│   ├── architect.py         # 架构师节点逻辑
│   ├── coder.py             # 程序员节点逻辑
│   └── tester.py            # 测试员节点逻辑
├── core/                    # 框架底层调度核心
│   ├── config.py            # 全局配置管理
│   ├── graph.py             # LangGraph 状态机与路由定义
│   ├── nodes.py             # 基础执行节点封装
│   ├── prompts.py           # 核心系统提示词
│   └── state.py             # 全局状态管理与类型强制清洗
├── tools/                   # 物理交互工具链
│   ├── exec_tools.py        # 终端命令执行与沙盒测试工具
│   └── fs_tools.py          # 物理文件系统安全读写工具
├── utils/                   
│   └── llm_client.py        # LLM 网络通信适配器
└── main.py                  # 交互入口与主控调度器
```


# 🚀 快速开始
## 1. 环境准备

确保您的系统已安装 Python 3.10 或更高版本。
```Bash
# 克隆仓库
git clone [https://github.com/HHY-Note/AgentCoder.git](https://github.com/HHY-Note/AgentCoder.git)
cd AgentCoder

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows 用户使用 venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

```
## 2. 配置环境变量

在项目根目录创建 .env 文件，并根据模型提供商填写配置。注：BASE_URL 必须包含完整的 API 路由后缀（如 /v1 或 /compatible-mode/v1）。

```
# --- Architect ---
ARCHITECT_MODEL=gpt-4o  # 或其他具备强大架构能力的大模型
ARCHITECT_API_KEY=sk-your-api-key-here
ARCHITECT_BASE_URL=[https://api.example.com/v1](https://api.example.com/v1)
ARCHITECT_TEMP=0.7

# --- Coder ---
CODER_MODEL=gpt-5.4 # 推荐使用专注编码的模型
CODER_API_KEY=sk-your-api-key-here
CODER_BASE_URL=[https://api.example.com/v1](https://api.example.com/v1)
CODER_TEMP=0.1

# --- Tester ---
TESTER_MODEL=gpt-5.4 # 推荐使用具备复杂逻辑推理能力的大模型
TESTER_API_KEY=sk-your-api-key-here
TESTER_BASE_URL=[https://api.example.com/v1](https://api.example.com/v1)
TESTER_TEMP=0.1
```

## 3. 运行
```Bash

python3 main.py
```

启动后，系统会提示您输入工作区名称（如 MyProject）。随后，可以直接向终端粘贴复杂的需求指令。Agent 团队将接管后续所有的工程创建、代码编写、编译与纠错测试工作。