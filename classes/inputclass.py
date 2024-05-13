from dataclasses import dataclass

@dataclass
class InputClass:
    name: str
    value: str
    isEmpty: bool
    isNotNumeric: bool

    def __init__(self, name: str, value: str, isEmpty: bool, isNotNumeric: bool):
        self.name = name
        self.value = value
        self.isEmpty = isEmpty
        self.isNotNumeric = isNotNumeric

