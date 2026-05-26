from collections import deque
from typing import List, Tuple, Optional


class ContextManager:
    def __init__(self, max_size: int = 5):
        self.max_size = max_size
        self.context_queue: deque[Tuple[str, str]] = deque(maxlen=max_size)

    def add(self, source_text: str, translation: str) -> None:
        self.context_queue.append((source_text, translation))

    def get_context(self) -> Optional[Tuple[str, str]]:
        if not self.context_queue:
            return None
        source_texts = []
        translations = []
        for src, trans in self.context_queue:
            source_texts.append(src)
            translations.append(trans)
        return (
            "\n".join(source_texts),
            "\n".join(translations)
        )

    def get_context_formatted(self) -> Tuple[str, str]:
        context = self.get_context()
        if context is None:
            return ("", "")
        return context

    def clear(self) -> None:
        self.context_queue.clear()

    def is_empty(self) -> bool:
        return len(self.context_queue) == 0

    def size(self) -> int:
        return len(self.context_queue)
