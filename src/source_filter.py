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
            ("file", self.file_filter)
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
    
    def file_filter(self, text: str):
        file_endswitch = [".txt", ".md", ".rst", ".log", ".ini", ".cfg", ".conf", ".toml", ".yaml", ".yml", ".json", ".json5", ".xml", ".csv", ".tsv", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".rtf", ".odt", ".ods", ".odp", ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tgz", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".tif", ".tiff", ".heic", ".avif", ".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".mid", ".midi", ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg", ".ts", ".py", ".pyw", ".ipynb", ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".java", ".kt", ".go", ".rs", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".php", ".rb", ".pl", ".lua", ".swift", ".dart", ".scala", ".r", ".m", ".html", ".htm", ".css", ".scss", ".sass", ".less", ".vue", ".sh", ".bash", ".zsh", ".fish", ".bat", ".cmd", ".ps1", ".db", ".sqlite", ".sqlite3", ".sql", ".parquet", ".h5", ".hdf5", ".pkl", ".exe", ".msi", ".apk", ".ipa", ".appimage", ".deb", ".rpm", ".dll", ".so", ".dylib", ".unity", ".uasset", ".pak", ".rpgmvp", ".rpgmvo", ".rpgmvm", ".xp3", ".ttf", ".otf", ".woff", ".woff2", ".torrent", ".iso", ".img", ".bin", ".dat", ".bak", ".tmp", ".fbx"]
        text = text.lower().strip()

        return any(text.endswith(ext) for ext in file_endswitch)