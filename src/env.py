import os
import yaml


SRC_DIR_PATH_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.dirname(SRC_DIR_PATH_PATH)
CONFIG_PATH = os.path.join(PROJECT_PATH, "config.yaml")


with open("config.yaml", "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)
LLM_BACKEND = CONFIG.get("LLM_Backend", "openai")
TRANSLATE_CFG = CONFIG.get("Translate_Config", {})

OPENAI_KEY = os.getenv("MTool_LLMT_OpenAI_KEY", "")


def read_prompts(source_lang : str, target_lang : str):
    sys_prompt_path = os.path.join(SRC_DIR_PATH_PATH, "prompts", "sys_prompt_translator_{}_{}.txt".format(source_lang, target_lang))
    prompt_path = os.path.join(SRC_DIR_PATH_PATH, "prompts", "prompt_translator_{}_{}.txt".format(source_lang, target_lang))
    if not os.path.exists(sys_prompt_path) or not os.path.exists(prompt_path):
        raise ValueError("{} -> {} translation prompt is not configured! Configure it in src/prompts/prompt_tranlator_{}_{}.txt and src/prompts/sys_prompt_tranlator_{}_{}.txt".format(source_lang, target_lang, source_lang, target_lang))

    with open(sys_prompt_path, "r", encoding="utf-8") as f:
        SYS_PROMPT_TRANSLATOR = f.read()
    with open(prompt_path, "r", encoding="utf-8") as f:
        PROMPT_TRANSLATOR = f.read()

    return SYS_PROMPT_TRANSLATOR, PROMPT_TRANSLATOR