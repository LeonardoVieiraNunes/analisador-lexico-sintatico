from tokens import Token, TokenType

WHITE_SPACE = ' \n\t'

class Lexer:
    def __init__(self, text: str):
        self.current_char = None
        self.text = reversed(text)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char is not None:
            if self.current_char in WHITE_SPACE:
                self.advance()
            elif self.current_char == '*':
                self.advance()
                yield Token(TokenType.STAR)
            elif self.current_char == '|':
                self.advance()
                yield Token(TokenType.UNION)
            elif self.current_char == '(':
                self.advance()
                yield Token(TokenType.LEFT_PARENTHESIS)
            elif self.current_char == ')':
                self.advance()
                yield Token(TokenType.RIGHT_PARENTHESIS)
            else:
                yield self.generate_phrase()

    def generate_phrase(self):
        phrase_str = self.current_char
        self.advance()

        while self.current_char is not None and self.current_char not in ['*', '|', '(', ')']:
            phrase_str += self.current_char
            self.advance()

        return Token(TokenType.PHRASE, phrase_str)
