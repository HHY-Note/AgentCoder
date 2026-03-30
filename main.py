# main.py
import os
from core.graph import build_agent_graph
from langchain_core.messages import HumanMessage

def setup_workspace():
    workspace = os.path.abspath(os.path.join(os.getcwd(), "workspace"))
    if not os.path.exists(workspace):
        os.makedirs(workspace)
    return workspace

def run_pipeline():
    workspace_dir = setup_workspace()
    app = build_agent_graph()
    
    print("\n" + "="*50)
    print("🚀 AgentCoder Pro | 多智能体协同框架")
    print("="*50)

    task_input = input("\n📝 请输入开发需求: \n> ")
    initial_state = {
        "messages": [HumanMessage(content=task_input)],
        "workspace_dir": workspace_dir,
        "error_count": 0,
        "current_agent": "User"
    }

    # 设置递归上限为 150，确保大型 eBPF 项目不中断
    config = {"recursion_limit": 150}

    try:
        for output in app.stream(initial_state, config=config):
            # main.py 核心修改部分

            for node_name, state_update in output.items():
                if node_name == "tools":
                    # 🟢 优化：让工具执行结果更清晰
                    messages = state_update.get("messages", [])
                    for msg in messages:
                        # 过滤掉冗长的内容，只打印执行结论
                        clean_content = msg.content.replace("\n", " ")
                        print(f"🛠️  [执行回显]: {clean_content[:80]}...")
                else:
                    messages = state_update.get("messages", [])
                    if messages:
                        last_msg = messages[-1]
                        print(f"\n👤 [{node_name.upper()}] 正在行动")

                        # 🟢 优化：显示具体的工具参数（不再是空空如也的 -> ）
                        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                            for tc in last_msg.tool_calls:
                                f_name = tc['name']
                                args = tc['args']
                    
                                # 根据不同的工具提取关键参数
                                if f_name == "write_file":
                                    detail = f"写入文件 📝 {args.get('file_path')}"
                                elif f_name == "read_file":
                                    detail = f"读取文件 📖 {args.get('file_path')}"
                                elif f_name == "list_directory":
                                    detail = f"浏览目录 📂 {args.get('dir_path', '.')}"
                                elif f_name == "execute_command":
                                    detail = f"执行命令 ⚙️  {args.get('command')}"
                                else:
                                    detail = str(args)

                                print(f"👉 动作: {detail}")
            
                        # 🟢 优化：如果 Agent 没调工具而是在说话，打印简短摘要
                        elif last_msg.content:
                            summary = last_msg.content.strip().split('\n')[0]
                            print(f"💬 结论: {summary[:100]}...")

    except Exception as e:
        if "Recursion limit" in str(e):
            print("\n🚨 [警告]: 任务过于复杂，已达到执行上限。请检查 workspace 目录下的半成品。")
        else:
            print(f"\n🚨 [错误]: {str(e)}")

    print("\n" + "="*50)
    print("🏁 任务流转结束。请在 workspace/ 查看产出。")
    print("="*50)

if __name__ == "__main__":
    run_pipeline()