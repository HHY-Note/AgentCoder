# core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# 默认保底模型
GLOBAL_DEFAULT_MODEL = " Your-Model "

def get_env_var(key, default=None):
    val = os.getenv(key)
    if val is None or str(val).strip() == "":
        return default
    return str(val).strip().strip('"').strip("'")

AGENT_LLM_CONFIG = {
    "architect": {
        "model": get_env_var("ARCHITECT_MODEL", GLOBAL_DEFAULT_MODEL),
        "api_key": get_env_var("ARCHITECT_API_KEY"),
        "base_url": get_env_var("ARCHITECT_BASE_URL"),
        "temperature": float(get_env_var("ARCHITECT_TEMP", 0.7)),
    },
    "coder": {
        "model": get_env_var("CODER_MODEL", GLOBAL_DEFAULT_MODEL),
        "api_key": get_env_var("CODER_API_KEY"),
        "base_url": get_env_var("CODER_BASE_URL"),
        "temperature": float(get_env_var("CODER_TEMP", 0.1)),
    },
    "tester": {
        "model": get_env_var("TESTER_MODEL", GLOBAL_DEFAULT_MODEL),
        "api_key": get_env_var("TESTER_API_KEY"),
        "base_url": get_env_var("TESTER_BASE_URL"),
        "temperature": float(get_env_var("TESTER_TEMP", 0.1)),
    }
}