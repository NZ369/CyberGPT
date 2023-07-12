from tools.CyberStance.field import Field
from typing import List, Dict
from json import dump

class Form:
    def __init__(self, fields: List[Field]) -> None:
        self.fields = fields
    def completed(self) -> bool:
        return all(f.is_valid() for f in self.fields)

    def to_json(self) -> str:
        return dump(self.to_dict())
    def to_dict(self) -> Dict[str, str]:
        return {field.question: field.value for field in self.fields}
