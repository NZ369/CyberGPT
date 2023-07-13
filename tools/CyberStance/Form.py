from tools.CyberStance.field import Field
from typing import List, Dict
from json import dump
import streamlit as st

class Form:
    def __init__(self, fields: List[Field]) -> None:
        self.fields = fields

    def first_unanswered(self) -> Field | None:
        for f in self.fields:
            if not f.is_valid():
                return f
        return None

    def completed(self) -> bool:
        return all(f.is_valid() for f in self.fields)

    def to_json(self) -> str:
        return dump(self.to_dict())

    def to_dict(self) -> Dict[str, str]:
        return {field.question: field.value for field in self.fields}

    def __repr__(self) -> str:
        # return a string representation of the Form instance
        # that shows the list of fields
        return f"Form(fields={self.fields!r})"