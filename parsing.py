from util import Direction, DIR_TO_SYMBOL, SYM_TO_DIR
from pathways_code import Code
from instructions import InstructionType, SimpleInstructionType, Instruction
from typing import Tuple, List

class Line:
    """A Line represents a line of code (may be any of the 4 cardinal directions).
    Lines are compiled into instructions, then linked together.

    Lines can only start execution from any arrows going in its direction within itself (or at the start of the program).
    These are known as entry points.
    Lines can only end execution at arrows pointing in other directions, or the end of the line.
    These are know as exit points.
    Each line creates connections between its entry points and exit points, then exit points are linked to their corresponding entry points in a different line.
    The result is a graph describing program flow.
    """
    def __init__(self, line: str, dir: Direction, index: int, parser: "Parser"):
        self.dir = dir
        self.index = index
        self.parser = parser
        self.dir_symbol = DIR_TO_SYMBOL[self.dir]
        self.parse(line)
        self.remove_noop()

    def parse(self, line:str):
        """Parses this line, by itself, into an InstructionGroup.

        Args:
            line (str): The line as a string.
        """
        self.instructions: list[Instruction] = []
        i = 0
        while i < len(line):
            di, instruction = self.get_next_instruction(line, i)
            i += di
            self.instructions.append(instruction)
    
    def remove_noop(self):
        self.instructions = list(filter(lambda x:x[0]!=InstructionType.NOOP,self.instructions))
    
    def is_useless(self):
        # if self.dir == Direction.RIGHT and self.index == 0:
        #     return False # First never useless
        return not any(map(lambda x: x[0] == InstructionType.ENTRY, self.instructions))

    def link_entry_exit_points(self):
        pass

    def get_next_instruction(self, line: str, i: int) -> Tuple[int, Instruction]:
            c = line[i]
            for x in SimpleInstructionType:
                if c == x.name:
                    return 1,(InstructionType.SIMPLE, x)
            if c == self.dir_symbol:
                return 1,(InstructionType.ENTRY,i)
            elif c in "^v<>":
                return 1,(InstructionType.EXIT, (i, SYM_TO_DIR[c]))
            elif c == "?":
                di, inst = self.get_next_instruction(line, i+1)
                return di + 1, (InstructionType.COND, inst)
            elif c == " ":
                return 1,(InstructionType.NOOP, None)
            else:
                raise ValueError
    
    def __repr__(self):
        return repr(self.instructions) + "\n"
    


class Parser:
    """Parses code into an ASG.
    """
    def __init__(self, code: Code):
        self.lines: "dict[Direction, dict[int, Line]]" = {i:{} for i in Direction}
        for i, row in enumerate(code.iter_rows()):
            self.lines[Direction.RIGHT][i] = Line(row, Direction.RIGHT, i, self)
            self.lines[Direction.LEFT][i] = Line(row[::-1], Direction.LEFT, i, self)
        for i, col in enumerate(code.iter_cols()):
            self.lines[Direction.DOWN][i] = Line(col, Direction.DOWN, i, self)
            self.lines[Direction.UP][i] = Line(col[::-1], Direction.UP, i, self)
        
        # Remove useless
        to_remove: List[Direction, int] = []
        for d in Direction:
            for k, v in self.lines[d].items():
                if v.is_useless():
                    to_remove.append((d,k))
        for d,k in to_remove:
            del self.lines[d][k]
    
    def __repr__(self):
        return repr(self.lines)