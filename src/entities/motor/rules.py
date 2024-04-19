from dataclasses import dataclass


@dataclass
class Rules:
    name: str
    code: str
    rule: str
    identify: str
    description: str
