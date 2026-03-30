# core/config.py
import os
from dotenv import load_dotenv

# 加载 .env 文件（如果之后你想把敏感 key 藏在 .env 里，可以直接无缝切换）
load_dotenv()

# ==========================================
# 统一的默认模型凭证 (当前全部使用你的 GLM-5 配置)
# ==========================================
DEFAULT_MODEL = "glm-5"
DEFAULT_API_KEY = " your key "
DEFAULT_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

# ==========================================
# Agent 专属配置字典 (Agent LLM Registry)
# ==========================================
"""
在这里，你可以为每一个 Agent 独立配置：
- model: 模型名称
- api_key: 该模型的 Key
- base_url: 该模型的请求端点
- temperature: 创造力指数 (架构师偏高以利于设计，程序员偏低以保证严谨)
"""
AGENT_LLM_CONFIG = {
    "architect": {
        "model": DEFAULT_MODEL,
        "api_key": DEFAULT_API_KEY,
        "base_url": DEFAULT_BASE_URL,
        "temperature": 0.7, 
    },
    "coder": {
        "model": DEFAULT_MODEL,
        "api_key": DEFAULT_API_KEY,
        "base_url": DEFAULT_BASE_URL,
        "temperature": 0.1, 
    },
    "tester": {
        "model": DEFAULT_MODEL,
        "api_key": DEFAULT_API_KEY,
        "base_url": DEFAULT_BASE_URL,
        "temperature": 0.3,
    },
    "pm": {
        "model": DEFAULT_MODEL,
        "api_key": DEFAULT_API_KEY,
        "base_url": DEFAULT_BASE_URL,
        "temperature": 0.5,
    }
}