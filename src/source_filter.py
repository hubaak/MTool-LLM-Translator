import re
from typing import Callable, List, Tuple


class SourceFilter:
    def __init__(self):
        self.registered_filters: List[Tuple[str, Callable[[str], bool]]] = [
            ("empty", self.empty_filter),
            ("number", self.num_filter),
            ("symbol", self.symbol_filter),
            ("path", self.path_filter),
            ("url", self.url_filter),
            ("placeholder", self.placeholder_filter),
            ("xml", self.xml_filter),
            ("control", self.control_filter),
            ("variable", self.variable_filter),
            ("hash", self.hash_filter),
            ("shortcut", self.shortcut_filter),
            ("emoji", self.emoji_filter),
            ("code", self.code_filter),
        ]

    def filter(self, text: str):
        if text is None:
            return True, "none"

        text = text.strip()

        for name, filter_func in self.registered_filters:
            if filter_func(text):
                return True, name

        return False, None

    # =========================
    # Filters
    # =========================

    def empty_filter(self, text: str):
        return len(text.strip()) == 0

    def num_filter(self, text: str):
        return bool(re.fullmatch(r"[-+]?[\d,.]+%?", text))

    def symbol_filter(self, text: str):
        return bool(re.fullmatch(r"[\W_]+", text))

    def path_filter(self, text: str):
        patterns = [
            r"^[\w\-/\\.]+\.(png|jpg|jpeg|txt|json|xml|wav|ogg|mp3)$",
            r"^[A-Za-z]:\\",
            r"^(/[\w.-]+)+$",
        ]

        return any(re.fullmatch(p, text) for p in patterns)

    def url_filter(self, text: str):
        return bool(re.fullmatch(r"https?://\S+", text))

    def placeholder_filter(self, text: str):
        patterns = [
            r"%\w",
            r"\{[^{}]+\}",
            r"<[A-Z0-9_]+>",
        ]

        return any(re.search(p, text) for p in patterns)

    def xml_filter(self, text: str):
        return bool(re.fullmatch(r"</?[^>]+>", text))

    def control_filter(self, text: str):
        return text in ["\\n", "\\t", "\\r"]

    def variable_filter(self, text: str):
        return bool(
            re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", text)
        )

    def hash_filter(self, text: str):
        patterns = [
            r"[a-fA-F0-9]{32}",
            r"[a-fA-F0-9]{40}",
            r"[a-fA-F0-9\-]{36}",
        ]

        return any(re.fullmatch(p, text) for p in patterns)

    def shortcut_filter(self, text: str):
        patterns = [
            r"(Ctrl|Alt|Shift)\+\w",
            r"(ESC|ENTER|TAB|SPACE)",
        ]

        return any(re.fullmatch(p, text, re.IGNORECASE) for p in patterns)

    def emoji_filter(self, text: str):
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "]+",
            flags=re.UNICODE,
        )

        return bool(emoji_pattern.fullmatch(text))

    def code_filter(self, text: str):
        keywords = [
            "if",
            "else",
            "function",
            "return",
            "while",
            "for",
            "class",
            "var",
        ]

        if any(k in text for k in keywords):
            return True

        if any(sym in text for sym in ["==", "!=", "&&", "||", "::"]):
            return True

        return False