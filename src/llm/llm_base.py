import re
from typing import List
from typing import Dict, List, Optional

class LLM_Base:
    def get_response(self, sys_prompt : str, prompt : str, **kwargs) -> str:
        raise NotImplementedError
    
    def get_result(
        self,
        sys_prompt: str,
        prompt: str,
        key_words: List[str],
        **kwargs
    ) -> Dict[str, Optional[List[str]]]:
        response = self.get_response(sys_prompt, prompt, **kwargs)
        results = LLM_Base.extract_result_from_response(response, key_words)
        return results
    
    @staticmethod
    def extract_result_from_response(
        response: str,
        key_words: List[str]
    ) -> Dict[str, Optional[List[str]]]:
        match_results = {}
        for key_word in key_words:
            escaped = re.escape(key_word)
            pattern = rf"<{escaped}>([^<]*?)</{escaped}>"
            matches = re.findall(pattern, response)
            match_results[key_word] = [item.strip() for item in matches] if matches else None
        return match_results