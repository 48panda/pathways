import enum
from typing import List, Literal, Tuple, Union, TYPE_CHECKING
from util import DIR_TO_SYMBOL, Direction

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
    STRING = 6 # String
    INVALID = 7 # Character of the invalid operation. Only used in testing.
    POP = 8 # None. Used for a pop with no replacement.
    EOL = 9 # None. Marks the end of a line.
    
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
    MOD = "%"
    FALSE = "F"
    TRUE = "T"
    PRINT = "!"
    DUPLICATE = "d"
    EQUAL = "="
    GREATER = "g"
    LESS = "l"
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

class Instruction:
    def __init__(self, type: InstructionType, x: int, y: int, dir: Direction):
        self.x = x
        self.y = y
        self.dir = dir
        self.type = type
    
    def __hash__(self):
        return hash((self.x, self.y, self.dir))

class SimpleInstruction(Instruction):
    def __init__(self, simple_type: SimpleInstructionType, x: int, y: int, dir: Direction):
        super().__init__(InstructionType.SIMPLE, x, y, dir)
        self.simple_type = simple_type
    
    def __str__(self) -> str:
        return self.simple_type.value

class EntryInstruction(Instruction):
    def __init__(self, x: int, y: int, dir: Direction):
        super().__init__(InstructionType.ENTRY, x, y, dir)
    
    def __str__(self) -> str:
        return DIR_TO_SYMBOL[self.dir]

class ExitInstruction(Instruction):
    def __init__(self, exit_dir: Direction, x: int, y: int, dir: Direction):
        super().__init__(InstructionType.EXIT, x, y, dir)
        self.exit_dir = exit_dir
    
    def __str__(self) -> str:
        return DIR_TO_SYMBOL[self.exit_dir]

class CondInstruction(Instruction):
    def __init__(self, inst: Instruction, x: int, y: int, dir: Direction):
        super().__init__(InstructionType.COND, x, y, dir)
        self.inst = inst
    
    def __str__(self) -> str:
        return f"{self.inst}"

class IntInstruction(Instruction):
    def __init__(self, value: int, x: int, y: int, dir: Direction):
        super().__init__(InstructionType.INTEGER, x, y, dir)
        self.value = value

    def __str__(self) -> str:
        return f"{'n' if self.value > 0 else 'N'}{abs(self.value)}"

class StrInstruction(Instruction):
    def __init__(self, value: str, x: int, y: int, dir:Direction):
        super().__init__(InstructionType.STRING, x, y, dir)
        self.value = value
    
    def __str__(self):
        return "\"" + self.value.replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace("\\", "\\\\").replace("\"", "\\\"") + "\""

class InvalidInstruction(Instruction):
    def __init__(self, char: str, x: int, y: int, dir: Direction):
        super().__init__(InstructionType.INVALID, x, y, dir)

class PopInstruction(Instruction):
    def __init__(self, x: int, y: int, dir: Direction):
        super().__init__(InstructionType.POP, x, y, dir)

    def __str__(self) -> str:
        return "ṗ"

class EOLInstruction(Instruction):
    def __init__(self, x: int, y: int, dir: Direction):
        super().__init__(type, x, y, dir)
    
    def __str__(self) -> str:
        return "EOL"


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
    if i[0] == InstructionType.COND:
        return "?" + stringify_instr(i[1])
    if i[0] == InstructionType.STRING:
        return "\"" + i[1].replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r").replace("\\", "\\\\").replace("\"", "\\\"") + "\""
    return str(i)
