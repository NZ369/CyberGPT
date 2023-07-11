from tools.CyberStance.field import Felid
from typing import List, Dict
from json import dump

class Form:
    def __init__(self, fields: List[Felid]) -> None:
        self.fields = fields
    def completed(self) -> bool:
        all(
            lambda f: f is not None,
            self.fields
        )
    def to_json(self) -> str:
        return dump(self.to_dict());
        raise NotImplementedError()
    def to_dict(self) -> Dict[str, str]:
        return {field.question: field.value for field in self.fields}
