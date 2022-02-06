from .tokens import Token, TokenType

WHITESPACE = " \n\t"
DIGITS = "0123456789"
LETTERS = "abcdefghijklmnopqrstuvwxyz"

class Lexer:
    def __init__(self, text) -> None:
        self.text = iter(text)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char != None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char in DIGITS or self.current_char in ".-+":
                yield self.generate_number()
            elif self.current_char.lower() == "\"":
                yield self.generate_string()
            elif self.current_char.lower() in LETTERS:
                yield self.generate_build_in()
            elif self.current_char == "!":
                self.advance()
                yield Token(TokenType.EXMARK)
            elif self.current_char == "$":
                self.advance()
                yield Token(TokenType.DOLLAR)
            elif self.current_char == ":":
                self.advance()
                yield Token(TokenType.DPOINT)
            elif self.current_char == "{":
                self.advance()
                yield Token(TokenType.LCPAREN)
            elif self.current_char == "}":
                self.advance()
                yield Token(TokenType.RCPAREN)
            elif self.current_char == ";":
                self.advance()
                yield Token(TokenType.SEMICOL)
            else:
                raise Exception("Illegal characted: " + self.current_char)

    def generate_number(self):
        decimal_point_count = 0
        number_str = self.current_char
        self.advance()

        while self.current_char != None and self.current_char in DIGITS and self.current_char != ".":
            if self.current_char == ".":
                decimal_point_count += 1
                if decimal_point_count > 1:
                    break
            number_str +=  self.current_char
            self.advance()

        if number_str.startswith("."):
            number_str = "0"+number_str
        if number_str.endswith("."):
            number_str = number_str+"0"

        try:
            return Token(TokenType.NUMBER, float(number_str))
        except:
            pass
        raise SyntaxError("More than one plus or mines symbol before a number is not valid")

    def generate_string(self):
        self.advance()
        string = self.current_char
        self.advance()

        while self.current_char != None and (self.current_char.lower() in LETTERS or self.current_char in DIGITS or self.current_char == "_"):
            string += self.current_char
            self.advance()

        if self.current_char != "\"":
            raise SyntaxError("Unterminated string")
        self.advance()

        return Token(TokenType.STRING, string)

    def generate_build_in(self):
        string = self.current_char
        self.advance()

        while self.current_char != None and (self.current_char.lower() in LETTERS or self.current_char in DIGITS or self.current_char == "_"):
            string += self.current_char
            self.advance()

        return Token(TokenType.BUILD_IN, string)