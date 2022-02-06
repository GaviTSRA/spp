from .tokens import TokenType
from .nodes import *

class Parser:
    def __init__(self, tokens) -> None:
        self.index = 0
        self.tokens = iter(tokens)
        self.advance()

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def raise_error(self, error=""):
        raise Exception("Invalid syntax" if error == "" else error)

    def require(self, token_types, failed_msg):
        if self.current_token == None:
            self.raise_error(failed_msg)
        if not self.current_token.type in token_types:
            print("Got:")
            print(self.current_token.type)
            self.raise_error(failed_msg)

    def parse(self):
        if self.current_token == None:
            return None

        result = self.file()
        
        if self.current_token != None:
            self.raise_error()

        return result

    def file(self):
        result = []
        while self.current_token != None:
            result.append(self.block())
        return FileNode(result)

    def block(self):
        res = self.start_condition()
        return BlockNode(res, self.body())

    def start_condition(self):
        self.require([TokenType.EXMARK], "Expected '!'")
        self.advance()

        self.require([TokenType.BUILD_IN], "Expected start condition")
        cond = self.current_token.value
        self.advance()

        val = None
        if self.current_token.type == TokenType.DPOINT:
            self.advance()
            val = self.current_token.value
            self.advance()

        self.index += 1
        return StartConditionNode(cond, val, self.index - 1, self.index)

    def body(self):
        res = []

        self.require([TokenType.LCPAREN], "Expected '{'")
        self.advance()

        while self.current_token.type == TokenType.BUILD_IN:
            res.append(self.expr())
            self.index += 1

        self.require([TokenType.RCPAREN], "Expected expression or '}'")
        self.advance()

        res[-1].next = None
        return BodyNode(res)

    def expr(self):
        res = self.instr()
        
        self.require([TokenType.STRING, TokenType.NUMBER, TokenType.SEMICOL], "Expected value or ';'")

        if self.current_token.type == TokenType.SEMICOL:
            self.advance()
            return ExprNode(res)
        else:
            val = self.current_token.value
            self.advance()
            self.require([TokenType.SEMICOL], "Expected ';'")
            self.advance()
            return ExprNode(res, val, self.index - 1, self.index, self.index + 1 )

    def instr(self):
        self.require([TokenType.BUILD_IN], "Expected instruction")
        res = InstrNode(self.current_token.value)
        self.advance()

        return res