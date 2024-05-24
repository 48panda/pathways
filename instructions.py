import enum
from typing import List, Literal, Tuple, Union, TYPE_CHECKING
from util import Direction

if TYPE_CHECKING:
    from parsing import Line

class InstructionType(enum.Enum):
    """Each instruction consists of a 2-element tuple, (type, data)
    type is this, data depends on type, listed below.
    """      # Data:
    NOOP = 0 # None
    SIMPLE = 1 # SimpleInstructionType
    ENTRY = 2 # int
    EXIT = 3 # int
    COND = 4 # Instruction
    INTEGER = 5 # int
    
    def __str__(self):
        return self.name
    __repr__ = __str__

class SimpleInstructionType(enum.Enum):
    AND = "&"
    OR = "|"
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    FALSE = "F"
    TRUE = "T"
    PRINT = "!"
    DUPLICATE = "d"
    NEGATE = "~"
    N0 = "0"
    N1 = "1"
    N2 = "2"
    N3 = "3"
    N4 = "4"
    N5 = "5"
    N6 = "6"
    N7 = "7"
    N8 = "8"
    N9 = "9"
    
    def __str__(self):
        return self.value
    __repr__ = __str__


NoOpInstruction = Tuple[Literal[InstructionType.NOOP], Literal[None]]
SimpleInstruction = Tuple[Literal[InstructionType.SIMPLE], SimpleInstructionType]
EntryPoint = Tuple[Literal[InstructionType.ENTRY], int]
ExitPoint = Tuple[Literal[InstructionType.EXIT], Tuple[int, Direction]]

Instruction = Union[NoOpInstruction,SimpleInstruction,EntryPoint,ExitPoint, (Cond:=Tuple[Literal[InstructionType.COND], "Instruction"])]

def stringify_instrs(instructions: List[Instruction]) -> str:
    out = ""
    for i in instructions:
        out += stringify_instr(i)
    return out

def stringify_instr(i: Instruction) -> str:
    if i[0] == InstructionType.SIMPLE:
        return str(i[1])
    if i[0] == InstructionType.INTEGER:
        return f"{'n' if i[1]>0 else 'N'}{abs(i[1])}"