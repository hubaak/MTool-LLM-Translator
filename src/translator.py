import os
import json
from tqdm import tqdm

from .llm import get_llm_backend
from .noun_manager import NounManager
from .source_filter import SourceFilter
from .context_manager import ContextManager
from .env import LLM_BACKEND, SYS_PROMPT_TRANSLATOR_ZH, PROMPT_TRANSLATOR_ZH

class Translator:
    def __init__(self, source_file : str, target_file : str):
        self.llm = get_llm_backend(LLM_BACKEND)
        self.noun_manager = NounManager()
        self.source_filter = SourceFilter()
        self.context_manager = ContextManager(max_size=5)
        self.max_attempts = 3
        self.load_source_from_json(source_file)
        self.load_target_from_json(target_file)
        self.target_file = target_file
        self.set_prompts()
    
    def set_prompts(self):
        self.sys_prompt_translator = SYS_PROMPT_TRANSLATOR_ZH
        self.prompt_translator = PROMPT_TRANSLATOR_ZH
        
    def translate_all(self, use_tqdm=True):
        iterator = tqdm(self.source_list, desc="Translating") if use_tqdm else self.source_list

        for source_text in iterator:
            if source_text in self.target_json:
                continue

            results = self.translate_single(source_text)

            if results and results.get("translation"):
                self.target_json[source_text] = results["translation"][-1] if isinstance(results["translation"], list) else results["translation"]
                self.save_target_to_json()

        return self.target_json

    def save_target_to_json(self):
        noun_list = self.noun_manager.save_to_list()
        output_data = {}
        for key, value in self.target_json.items():
            if key != "->-<-nounlist->-<-":
                output_data[key] = value
        output_data["->-<-nounlist->-<-"] = noun_list
        with open(self.target_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    def translate_single(self, source_text : str) -> str:
        if self.source_filter.filter(source_text)[0]:
            return {
                "translation" : [source_text]
            }
        for attempt_count in range(self.max_attempts):
            noun_list = self.noun_manager.get_noun_list(source_text)
            context_source_text, context_translation_text = self.context_manager.get_context_formatted()
            results = self.llm.get_result(
                sys_prompt = self.sys_prompt_translator,
                prompt = self.prompt_translator.format(source_text=source_text, noun_list=noun_list, context_source_text=context_source_text, context_translation_text=context_translation_text),
                key_words = ["translation", "noun"]
            )
            if self.check_translation(results = results):
                self.register_nouns(results)
                self.context_manager.add(
                    source_text = source_text.strip(),
                    translation= results["translation"][-1] if isinstance(results["translation"], list) else results["translation"]
                )
                return results
        return {}
    
    def check_translation(self, results):
        if results.get("translation") is None:
            return False
        return True
    
    def register_nouns(self, results):
        if results["noun"] is None:
            return
        for noun_comb in results["noun"]:
            noun_comb_list = list(map(str.strip, noun_comb.split("->", 1)))
            if len(noun_comb_list) != 2:
                continue
            source, target = noun_comb_list
            if source and target:
                self.noun_manager.register_noun(
                    source, target
                )
                
    def load_source_from_json(self, source_file : str):
        with open(source_file, "r", encoding="utf-8") as f:
            source_json = json.load(f)
        self.source_list = list(source_json.keys())
            
    def load_target_from_json(self, target_file : str):
        if os.path.exists(target_file):
            with open(target_file, "r", encoding="utf-8") as f:
                self.target_json = json.load(f)
            if "->-<-nounlist->-<-" in self.target_json:
                self.noun_manager.load_from_list(
                    self.target_json["->-<-nounlist->-<-"]
                )
        else:
            self.target_json = {}