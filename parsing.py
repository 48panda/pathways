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
        while i < len(self.instructions):
            inst = self.instructions[i]
            if curr_node is None and inst[0] != InstructionType.ENTRY:
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
        # if self.dir == Direction.RIGHT and self.index == 0:
        #     return False # First never useless
        return not any(map(lambda x: x[0] == InstructionType.ENTRY, self.instructions))

    def get_next_instruction(self, line: str, i: int) -> Tuple[int, Instruction]:
            if not (0 <= i < len(line)):
                return 0,(InstructionType.NOOP, None)
            c = line[i]
            if self.dir == Direction.LEFT:
                X = self.parser.width - (i + 1)
                Y = self.index
            elif self.dir == Direction.UP:
                X = self.index
                Y = self.parser.height - (i + 1)
            elif self.dir == Direction.RIGHT:
                X = i
                Y = self.index
            else:
                X = self.index
                Y = i
            for x in SimpleInstructionType:
                if c == x.name:
                    return 1,(InstructionType.SIMPLE, x)
            if c == self.dir_symbol:
                return 1,(InstructionType.ENTRY,(X,Y))
            elif c in "^v<>":
                return 1,(InstructionType.EXIT, ((X,Y), SYM_TO_DIR[c]))
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
                        graph.add_arrow_node(ASGArrowNode(d, *Parser.get_xy_from_indices(d, *inst[1])))
        
        pseudostartnode = graph.get_arrow_node(Direction.RIGHT, 0, 0)
        graph.add_edge(ASGEdge(graph.start, pseudostartnode, []))

        for d in Direction:
            for line in self.lines[d].values():
                line.add_all_edges(graph)
        return graph

    def __repr__(self):
        return repr(self.lines)