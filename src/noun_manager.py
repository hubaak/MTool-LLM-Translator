from dataclasses import dataclass
from typing import Dict, Optional
import ahocorasick


@dataclass
class NounEntry:
    source: str
    target: str
    comment: Optional[str] = None


class NounManager:
    def __init__(self):
        self.noun_dict: Dict[str, NounEntry] = {}
        self.automaton = ahocorasick.Automaton()
        self._dirty = False

    def register_noun(
        self,
        source: str,
        target: str,
        comment: Optional[str] = None
    ) -> bool:
        if source in self.noun_dict:
            return False

        entry = NounEntry(
            source=source,
            target=target,
            comment=comment
        )
        self.noun_dict[source] = entry
        self.automaton.add_word(source, entry)
        self._dirty = True

        return True

    def _build(self):
        if self._dirty:
            self.automaton.make_automaton()
            self._dirty = False 

    def extract_nouns(self, text: str) -> Dict[str, NounEntry]:
        self._build()
        result = {}
        for end_index, entry in self.automaton.iter(text):
            result[entry.source] = entry
        return result
    
    def get_noun_list(self, text: str) -> str:
        if not self.noun_dict:
            return ""
        extract_result = self.extract_nouns(text)
        result = ""
        for k, v in extract_result.items():
            result += "{} -> {}\n".format(k, v.target)
        return result.strip()
    
    def load_from_list(self, nounlist):
        for item in nounlist:
            self.register_noun(
                source=item["source"],
                target=item["target"],
                comment=item.get("comment")
            )
            
    def save_to_list(self):
        result = []
        for source, entry in self.noun_dict.items():
            entry_json = {
                "source" : entry.source,
                "target" : entry.target
            }
            if entry.comment is not None:
                entry_json["comment"] = entry.comment
            result.append(entry_json)
        return result