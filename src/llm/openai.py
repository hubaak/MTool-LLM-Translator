import openai

from .llm_base import LLM_Base
from ..env import CONFIG, OPENAI_KEY

class OpenAI_Backend(LLM_Base):
    def __init__(self):
        self.config = CONFIG.get("OpenAI_api", {})
        self.inference_config = self.config.get("inference", {})
        self.model = self.config.get("model", "gpt-4o")
        
        self.client = openai.OpenAI(
            base_url = self.config.get("url", "https://api.openai.com/v1"),
            api_key = self.config.get("key", OPENAI_KEY)
        )
        
    def get_response(self, sys_prompt : str, prompt : str, **kwargs) -> str:
        kwargs["model"] = kwargs.get("model", self.model)
        
        for key, item in self.inference_config.items():
            if item is not None:
                kwargs.setdefault(key, item)
        
        kwargs["messages"]  = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt},
        ]

        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content