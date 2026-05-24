import os
import yaml


SRC_DIR_PATH_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(SRC_DIR_PATH_PATH)
CONFIG_PATH = os.path.join(PROJECT_PATH, "config.yaml")


with open("config.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)
LLM_BACKEND = CONFIG.get("LLM_Backend", "openai")

OPENAI_KEY = os.getenv("MTool_LLMT_OpenAI_KEY", "")


with open(os.path.join(SRC_DIR_PATH_PATH, "prompts", "sys_prompt_translator_zh.txt"), "r", encoding="utf-8") as f:
    SYS_PROMPT_TRANSLATOR_ZH = f.read()
with open(os.path.join(SRC_DIR_PATH_PATH, "prompts", "prompt_translator_zh.txt"), "r", encoding="utf-8") as f:
    PROMPT_TRANSLATOR_ZH = f.read()