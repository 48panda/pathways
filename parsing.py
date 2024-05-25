from asg import ASG, ASGArrowNode, ASGDecisionNode, ASGEdge, ASGNode, EdgeType
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
        self.uncompound()
    
    def __hash__(self):
        return hash((self.index, self.dir))

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
    
    def uncompound(self):
        i = 0
        while i < len(self.instructions):
            inst = self.instructions[i]
            if inst[0] == InstructionType.COND:
                if inst[1][0] == InstructionType.COND:
                    self.instructions[i] = inst[1]
                    self.instructions.insert(i, (InstructionType.SIMPLE, SimpleInstructionType.AND))
            i += 1

    def remove_noop(self):
        self.instructions = list(filter(lambda x:x[0]!=InstructionType.NOOP,self.instructions))

    def add_all_edges(self, graph: ASG):
        i = 0
        curr_node = None
        next_type = None
        code = []
        if self.index == 0 and self.dir == Direction.RIGHT:
            curr_node = graph.start
            next_type = EdgeType.ALWAYS
        while i < len(self.instructions):
            inst = self.instructions[i]
            if curr_node is None and inst[0] != InstructionType.ENTRY:
                i += 1
                continue
            if curr_node is None:
                curr_node = graph.get_arrow_node(self.dir, *inst[1])
                next_type = EdgeType.ALWAYS
            else:
                if inst[0] == InstructionType.EXIT:
                    dst = graph.get_arrow_node(inst[1][1],*inst[1][0])
                    graph.add_edge(ASGEdge(curr_node, dst, code, next_type))
                    code = []
                    curr_node = None
                    next_type = None
                elif inst[0] == InstructionType.COND and inst[1][0] == InstructionType.EXIT:
                    graph.add_decision_node(mid := ASGDecisionNode())
                    graph.add_edge(ASGEdge(curr_node, mid, code, next_type))
                    dst = graph.get_arrow_node(inst[1][1][1],*inst[1][1][0])
                    graph.add_edge(ASGEdge(mid, dst, [], EdgeType.TRUE))
                    code = []
                    curr_node = mid
                    next_type = EdgeType.FALSE
                else:
                    code.append(inst)
            i += 1
        if curr_node is not None:
            graph.add_edge(ASGEdge(curr_node, graph.terminal, code, next_type))
    
    def is_useless(self):
        if self.dir == Direction.RIGHT and self.index == 0:
            return False # First never useless
        return not any(map(lambda x: x[0] == InstructionType.ENTRY, self.instructions))

    def get_next_instruction(self, line: str, i: int) -> Tuple[int, Instruction]:
            if not (0 <= i < len(line)):
                return 0,(InstructionType.NOOP, None)
            c = line[i]
            if self.dir == Direction.LEFT:
                X = len(line) - (i + 1)
                Y = self.index
            elif self.dir == Direction.UP:
                X = self.index
                Y = len(line) - (i + 1)
            elif self.dir == Direction.RIGHT:
                X = i
                Y = self.index
            else:
                X = self.index
                Y = i
            for x in SimpleInstructionType:
                if c == x.value:
                    return 1,(InstructionType.SIMPLE, x)
            if c == self.dir_symbol:
                return 1,(InstructionType.ENTRY,(X,Y))
            if c == "#":
                return 2, (InstructionType.NOOP, None) # Skip the next character too.
            elif c in "^v<>":
                return 1,(InstructionType.EXIT, ((X,Y), SYM_TO_DIR[c]))
            elif c == "?":
                di, inst = self.get_next_instruction(line, i+1)
                return di + 1, (InstructionType.COND, inst)
            elif c == " ":
                return 1,(InstructionType.NOOP, None)
            elif c in "nN":
                di = 1
                c2 = "0"
                num = 0
                while c2 in "0123456789":
                    num *= 10
                    num += int(c2)
                    if  i + di < len(line):
                        c2 = line[i + di]
                    else:
                        c2 = " "
                    di += 1
                return di-1, (InstructionType.INTEGER, num if c == "n" else -num)
            elif c == "\"":
                di = 1
                s = ""
                while di + i < len(line) and line[di + i] != "\"":
                    c = line[di + i]
                    if c != "\\":
                        s += c
                    elif di + i + 1 < len(line):
                            c2 = line[di + i]
                            s += {"n":"\n","t":"\t","r":"\r"}.get(c2, c2) # Substitute by escape, fall back on character.
                            di += 1
                    di += 1
                return di + 1, (InstructionType.STRING, s)
            elif c == "'":
                if i + 1 < len(line):
                    return 2, (InstructionType.STRING, line[i + 1])
                return 1, (InstructionType.STRING, "") # End of program if this happens anyway.
            else:
                return 1, (InstructionType.INVALID, c)
    
    def __repr__(self):
        return repr(self.instructions) + "\n"
    


class Parser:
    """Parses code into an ASG.
    """
    def __init__(self, code: Code):
        self.width = code.width
        self.height = code.height
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

    @staticmethod
    def get_xy_from_indices(dir: Direction, rowcolindx: int, lineindx: int) -> Tuple[int, int]:
        if dir in (Direction.LEFT, Direction.RIGHT):
            return (lineindx, rowcolindx)
        return (rowcolindx, lineindx)

    def get_graph(self):
        graph: ASG = ASG()
        for d in Direction:
            for i, v in self.lines[d].items():
                for inst in v.instructions:
                    if inst[0] == InstructionType.ENTRY:
                        graph.add_arrow_node(ASGArrowNode(d, *inst[1]))
                    if inst[0] == InstructionType.COND and inst[1][0] == InstructionType.ENTRY:
                        graph.add_arrow_node(ASGArrowNode(d,*inst[1][1]))

        for d in Direction:
            for line in self.lines[d].values():
                line.add_all_edges(graph)
        return graph

    def __repr__(self):
        return repr(self.lines)