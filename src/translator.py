from .llm import get_llm_backend
from .env import LLM_BACKEND, SYS_PROMPT_TRANSLATOR_ZH, PROMPT_TRANSLATOR_ZH

class Translator:
    def __init__(self):
        self.llm = get_llm_backend(LLM_BACKEND)
        self.max_attempts = 3
        self.set_prompts()
    
    def set_prompts(self):
        self.sys_prompt_translator = SYS_PROMPT_TRANSLATOR_ZH
        self.prompt_translator = PROMPT_TRANSLATOR_ZH

    def translate_single(self, origin_text : str) -> str:
        for attempt_count in range(self.max_attempts):
            results = self.llm.get_result(
                sys_prompt = self.sys_prompt_translator,
                prompt = self.prompt_translator.format(origin_text=origin_text),
                key_words = ["translation", "noun"]
            )
            if self.check_translation(results = results):
                return results
        return {}
    
    def check_translation(self, results):
        if results.get("translation") is None:
            return False
        return True