from dataclasses import dataclass


@dataclass
class PhraseNode:
    value: str

    def __repr__(self):
        return f"{self.value}"


@dataclass
class StarNode:
    node: any

    def __repr__(self):
        return f"({self.node})*"


@dataclass
class UnionNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}|{self.node_b})"


@dataclass
class LeftParenthesisNode:
    node: any

    def __repr__(self):
        return f"{self.node}*"


@dataclass
class RightParenthesisNode:
    node: any

    def __repr__(self):
        return f"{self.node}*"
