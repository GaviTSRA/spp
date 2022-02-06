from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
    LCPAREN         = 0 # {
    RCPAREN         = 1 # }
    STRING          = 2 # abcdefghijklmnopqrstuvwxyz
    NUMBER          = 3 # 0123456789
    EXMARK          = 4 # ! 
    DOLLAR          = 5 # $
    DPOINT          = 6 # :
    SEMICOL         = 7 # ;
    BUILD_IN        = 8 # IF 

@dataclass
class Token:
    type: TokenType
    value: any = None

    def __repr__(self) -> str:
        return self.type.name + (f":{self.value}" if self.value != None else "")