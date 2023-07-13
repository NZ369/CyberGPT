from typing import Callable, Tuple

class Field:
    def __init__(self, question: str, input_parser: Callable[[str], Tuple[bool, str]], value: str | None = None):
        self.question: str = question
        self._input_parser = input_parser
            
        self.value: str | None = value

    def is_valid(self) -> bool:
        return self.value is not None

    def input_parser(self, user_input: str) -> Tuple[bool, str]:
        cond, result = self._input_parser(user_input)

        if cond:
            self.value = result
        
        return cond, result
    def __repr__(self) -> str:
        # return a string representation of the Field instance
        # that shows the question, the value, and the input_parser function
        return f"Field(question={self.question!r}, value={self.value!r}, input_parser={self._input_parser.__name__!r})"