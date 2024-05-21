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
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    I = 8
    J = 9
    K = 10
    L = 11
    
    def __str__(self):
        return self.name
    __repr__ = __str__

NoOpInstruction = Tuple[Literal[InstructionType.NOOP], Literal[None]]
SimpleInstruction = Tuple[Literal[InstructionType.SIMPLE], SimpleInstructionType]
EntryPoint = Tuple[Literal[InstructionType.ENTRY], int]
ExitPoint = Tuple[Literal[InstructionType.EXIT], Tuple[int, Direction] | Tuple["Line", int]]

Instruction = Union[NoOpInstruction,SimpleInstruction,EntryPoint,ExitPoint, (Cond:=Tuple[Literal[InstructionType.COND], "Instruction"])]