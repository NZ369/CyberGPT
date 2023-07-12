from typing import Callable, Tuple

class Field:
    def __init__(self, question: str, input_parser: Callable[[str], Tuple[bool, str]], value: str | None = None):
        self.question: str = question

        self._input_parser: Callable[[str], Tuple[bool, str]] = input_parser
        
        self.value: str | None = value

    def is_valid(self) -> bool:
        if self.value == None:
            return False
        cond, _ = self._input_parser(self.value)
        return cond

    def input_parser(self, user_input: str) -> Tuple[bool, str]:
        cond, result = self._input_parser(user_input)

        if cond:
            self.value = result
        
        return cond, result
