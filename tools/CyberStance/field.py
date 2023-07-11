from typing import Callable

class Field:
    def __init__(self, question: str, input_parser: Callable[[str], bool], value: str | None):
        self.question: str = question

        self.input_parser: Callable[[str], bool] = input_parser
        
        self.value: str | None = value

    def input_parser(self, user_input: str) -> bool:
        raise NotImplementedError()
    
