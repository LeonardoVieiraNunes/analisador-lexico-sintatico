from tokens import TokenType
from nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()

    def raise_error(self):
        raise Exception("Invalid syntax")

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        if self.current_token is None:
            return None

        result = self.expr()

        if self.current_token is not None:
            self.raise_error()

        return result

    def expr(self):
        result = self.term()

        if (self.current_token is not None) and (self.current_token.type == TokenType.UNION):
            self.advance()
            result = UnionNode(self.term(), result)

        return result

    def term(self):
        result = self.element()

        return result

    def element(self):
        token = self.current_token

        if token.type == TokenType.RIGHT_PARENTHESIS:
            self.advance()
            result = self.expr()
            if self.current_token.type is not TokenType.LEFT_PARENTHESIS:
                self.raise_error()

            self.advance()
            return result
        if token.type == TokenType.STAR:
            self.advance()
            return StarNode(self.expr())

        if token.type == TokenType.PHRASE:
            self.advance()
            return PhraseNode(token.value)


