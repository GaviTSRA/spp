from dataclasses import dataclass

@dataclass
class InstrNode:
    value: str

    def __repr__(self) -> str:
        return f"{self.value}"

@dataclass
class StartConditionNode:
    start_condition: str
    arg: str = None
    index: int = None
    next: int = None

    def __repr__(self) -> str:    
        if self.arg == None:
            return f"!{self.start_condition}"
        elif type(self.arg) == float:
            return f"!{self.start_condition}:{self.arg}"
        else: 
            return f'!{self.start_condition}:"{self.arg}"'

@dataclass
class ExprNode:
    instr: InstrNode
    value: str = None
    previous: int = None
    index: int = None
    next: int = None

    def __repr__(self) -> str:
        if self.value == None:
            return f"{self.instr};\n"
        elif type(self.value) == float:
            return f"{self.instr} {self.value};\n"
        else: 
            return f'{self.instr} "{self.value}";\n'

@dataclass
class BodyNode:
    exprs: list[ExprNode]

    def __repr__(self) -> str:
        res = ""
        for expr in self.exprs:
            res += expr.__repr__()
        return "{\n" + f"{res}" + "}"

@dataclass
class BlockNode:
    start_condition: StartConditionNode
    body: BodyNode

    def __repr__(self) -> str:
        return f"{self.start_condition} {self.body}"

@dataclass
class FileNode:
    blocks: list[BlockNode]

    def __repr__(self) -> str:
        res = ""
        for block in self.blocks:
            res += f"{block}\n"
            return res