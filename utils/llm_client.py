# utils/llm_client.py
import os
from langchain_openai import ChatOpenAI
from core.config import AGENT_LLM_CONFIG

# 1. 自动清理可能残留的系统代理，防止底层的网络请求被拦截导致程序死锁
for key in ['all_proxy', 'ALL_PROXY', 'http_proxy', 'HTTP_PROXY', 'https_proxy', 'HTTPS_PROXY']:
    if key in os.environ:
        del os.environ[key]

def get_llm(agent_name: str) -> ChatOpenAI:
    """
    大语言模型：只需传入 Agent 名字，自动配置它的专属模型。
    """
    # 尝试从字典中获取该 agent 的配置。如果拼写错误找不到，默认使用 coder 的配置兜底。
    config = AGENT_LLM_CONFIG.get(agent_name, AGENT_LLM_CONFIG["coder"])
    
    # 使用读取到的独立配置来实例化 LangChain 的 ChatOpenAI
    llm = ChatOpenAI(
        model=config["model"],
        api_key=config["api_key"],
        base_url=config["base_url"],
        temperature=config["temperature"],
        max_tokens=8192  # 扩大上下文窗口，大型项目必备
    )
    
    return llm