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
    
    def __str__(self):
        return self.name
    __repr__ = __str__

class SimpleInstructionType(enum.Enum):
    AND = "&"
    OR = "|"
    TRUE = "T"
    FALSE = "F"
    PRINT = "!"
    
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