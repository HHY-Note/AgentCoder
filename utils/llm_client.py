# utils/llm_client.py
import os
import httpx
from langchain_openai import ChatOpenAI
from core.config import AGENT_LLM_CONFIG

# 自动修正 Linux 系统下不规范的 socks 代理前缀，防止底层网络库崩溃
proxy_keys = ["http_proxy", "https_proxy", "all_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"]
for k in proxy_keys:
    if k in os.environ and os.environ[k].startswith("socks://"):
        os.environ[k] = os.environ[k].replace("socks://", "socks5://")

def get_llm(agent_name: str):
    config = AGENT_LLM_CONFIG.get(agent_name)
    if not config or not config["api_key"]:
        raise ValueError(f"❌ 找不到 Agent '{agent_name}' 的配置，请检查 .env")

    # 工业级高可用配置：给深度推理模型充足的时间 (10分钟)
    timeout_config = httpx.Timeout(connect=30.0, read=600.0, write=30.0, pool=30.0)
    robust_http_client = httpx.Client(trust_env=True, timeout=timeout_config)

    try:
        return ChatOpenAI(
            model=config["model"],
            api_key=config["api_key"],
            base_url=config["base_url"],
            temperature=config["temperature"],
            max_tokens=8192,
            http_client=robust_http_client,
            max_retries=2
        )
    except Exception as e:
        print(f"❌ {agent_name} 实例化 LLM 失败: {str(e)}")
        raise e