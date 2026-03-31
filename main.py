import os
import sys
from core.graph import build_agent_graph
from langchain_core.messages import HumanMessage
import traceback

def main():
    print("==================  ⚙️   AgentCoder   ==================")
    raw_dir = input("📁 请输入项目路径 (直接回车默认: ./workspace): ")
    work_dir = raw_dir.strip() if raw_dir.strip() else "./workspace"
    os.makedirs(work_dir, exist_ok=True)
    os.environ["AGENT_WORKSPACE"] = os.path.abspath(work_dir)
    print(f"[*] 主控调度器 (PID: {os.getpid()}) 启动，锁定物理工作区: {os.path.abspath(work_dir)}\n")

    app = build_agent_graph()
    
    while True:
        try:
            print("🧑‍💻 请输入需求，或输入 exit 退出):")
            lines = []
            while True:
                # 巧妙的提示符：第一行显示 "> "，后续行显示缩进 "  "
                line = input("> " if not lines else "  ")
                
                # 如果第一行直接输入 exit
                if not lines and line.strip().lower() == 'exit':
                    print("👋 感谢使用 AgentCoder，再见！")
                    sys.exit(0)
                
                # 遇到纯空行，说明用户按了两次回车或粘贴完毕，结束收集
                if not line:
                    break
                    
                lines.append(line)
            
            # 组合所有行，并清除首尾多余的空白字符
            user_input = "\n".join(lines).strip()
            
            # 如果收集完还是空的，静默重新开始
            if not user_input:
                continue
            
            initial_state = {
                "messages": [HumanMessage(content=user_input)],
                "error_count": 0,
                "current_agent": ""
            }
            
            # 推入 LangGraph 流水线
            for output in app.stream(initial_state, {"recursion_limit": 50}):
                pass

        except Exception as e:
            # 💡 核心追踪修改：打印极其详细的红色报错追踪日志
            print(f"\n❌ 主控器捕获致命异常！详细调用栈如下：")
            print("-" * 50)
            traceback.print_exc()  # 把底层的报错文件和行号全部吐出来！
            print("-" * 50)
            
            error_msg = str(e)
            
            # 💡 解决点 2：识别 429 余额不足，直接中断主程序，防止无意义重试
            if "429" in error_msg or "余额不足" in error_msg:
                print("🚨 [致命错误]: API 额度已耗尽！请充值后重新运行。")
                break


if __name__ == "__main__":
    main()