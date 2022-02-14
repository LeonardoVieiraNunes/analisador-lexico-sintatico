from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    PHRASE = 0
    STAR = 1
    UNION = 2
    LEFT_PARENTHESIS = 3
    RIGHT_PARENTHESIS = 4


@dataclass
class Token:
    type: TokenType
    value: any = None

    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value is not None else "")
