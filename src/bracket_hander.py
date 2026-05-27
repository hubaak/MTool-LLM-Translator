from dataclasses import dataclass

@dataclass
class BracketState:
    left: str = ""
    right: str = ""


class BracketHandler:
    BRACKET_PAIRS = {
        "「": "」",
        "『": "』",
        "（": "）",
        "【": "】",
        "〈": "〉",
        "《": "》",
    }

    def _match_left(self, text: str, left: str, right: str, reverse: bool = False) -> bool:
        if not text.startswith(left) and not reverse:
            return False
        elif not text.endswith(left) and reverse:
            return False
        
        if reverse:
            iterator = range(len(text)-1, -1, -1)
        else:
            iterator = range(len(text))
        depth = 0
        for i in iterator:
            ch = text[i]
            if ch == left:
                depth += 1
            elif ch == right:
                depth -= 1
                if depth == 0:
                    return i == len(text) - len(right) if not reverse else i == 0

        return True

    def preprocess(self, text: str):
        text = text.strip()

        for left, right in self.BRACKET_PAIRS.items():
            left_save, right_save = left, right
            if not self._match_left(text, left, right):
                left_save = ""
            if not self._match_left(text, right, left, True):
                right_save = ""
            
            return text[len(left_save):len(text)-len(right_save)], (left_save, right_save)
        return text, None

    def postprocess(self, text: str, state):
        if not state:
            return text

        left, right = state
        return f"{left or ""}{text}{right or ""}"
        

if __name__ == "__main__":
    handler = BracketHandler()

    tests = [
        "「こんにちは」",
        "「こんに「ちは」",
        "「こん」に「ちは」",
        "「こん」にちは」",
        "「こんにちは",
        "こんにちは」",
        "『テスト』",
        "「こん」にちは",
        "こん「にちは",
        "A」B",
        "AB",
    ]

    for t in tests:
        processed, state = handler.preprocess(t)
        restored = handler.postprocess(
            processed,
            state
        )

        print("=" * 30)
        print("Source:", t)
        print("Processed:", processed)
        print("State:", state)
        print("Restored:", restored)
        
        if t != restored:
            print("ERRROOORRRRR!")