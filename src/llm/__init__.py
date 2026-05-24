from .llm_base import LLM_Base
from .openai import OpenAI_Backend


def get_llm_backend(backend : str) -> LLM_Base:
    if backend == "openai":
        return OpenAI_Backend()
    else:
        raise ValueError("{} LLM backend has not been supported yet!".format(backend))