from sre_constants import IN
from asg import ASG, ASGArrowNode, ASGDecisionNode, ASGNode, ASGStartNode, ASGTerminalNode
from instructions import Instruction, InstructionType, SimpleInstructionType


class Interpreter:
    def __init__(self, graph: ASG):
        self.graph = graph
        self.node = self.graph.start
        self.stack = []
        self.finished = False
    
    def start_interpreting(self):
        while not self.finished:
            self.interpret_next_node()

    def interpret_next_node(self):
        if isinstance(self.node, ASGTerminalNode):
            self.finished = True
            return
        if isinstance(self.node, (ASGStartNode, ASGArrowNode)):
            edge = self.node.out_edges[0]
        elif isinstance(self.node, ASGDecisionNode):
            if self.pop():
                edge = self.node.true
            else:
                edge = self.node.false
        for inst in edge.code:
            self.run_instruction(inst)
        self.node = edge.dst


    def run_instruction(self, inst: Instruction):
        if inst[0] == InstructionType.SIMPLE:
            self.run_simple_instruction(inst[1])
        elif inst[0] in (InstructionType.INTEGER, InstructionType.STRING):
            self.push(inst[1])
        elif inst[0] == InstructionType.COND:
            if self.pop():
                self.run_instruction(inst[1])
        elif inst[0] == InstructionType.POP:
            self.pop()
        else:
            raise ValueError(f"Unknown instruction type '{inst}'")
    
    def run_simple_instruction(self, inst: SimpleInstructionType):
        if inst == SimpleInstructionType.AND:
            a = self.pop()
            b = self.pop()
            self.push(a and b)
        elif inst == SimpleInstructionType.OR:
            a = self.pop()
            b = self.pop()
            self.push(a or b)
        elif inst == SimpleInstructionType.ADD:
            a = self.pop()
            b = self.pop()
            self.push(b + a)
        elif inst == SimpleInstructionType.SUB:
            a = self.pop()
            b = self.pop()
            self.push(b - a)
        elif inst == SimpleInstructionType.MUL:
            a = self.pop()
            b = self.pop()
            self.push(b * a)
        elif inst == SimpleInstructionType.DIV:
            a = self.pop()
            b = self.pop()
            self.push(b // a)
        elif inst == SimpleInstructionType.MOD:
            a = self.pop()
            b = self.pop()
            self.push(b % a)
        elif inst == SimpleInstructionType.EQUAL:
            a = self.pop()
            b = self.pop()
            self.push(b == a)
        elif inst == SimpleInstructionType.LESS:
            a = self.pop()
            b = self.pop()
            self.push(b < a)
        elif inst == SimpleInstructionType.GREATER:
            a = self.pop()
            b = self.pop()
            self.push(b > a)
        elif inst == SimpleInstructionType.NEGATE:
            a = self.pop()
            if type(a) == bool:
                self.push(not a)
            elif type(a) == int:
                self.push(-a)
            elif type(a) == str:
                self.push(a[::-1])
            else:
                self.push(a)

        elif inst == SimpleInstructionType.TRUE:
            self.push(True)
        elif inst == SimpleInstructionType.FALSE:
            self.push(False)
        elif inst == SimpleInstructionType.PRINT:
            print(self.pop())
        elif inst == SimpleInstructionType.DUPLICATE:
            val = self.pop()
            self.push(val)
            self.push(val)
        elif inst == SimpleInstructionType.NEGATE:
            val = self.pop()
            if isinstance(val, bool):
                self.push(not val)
            elif isinstance(val, int):
                self.push(-val)
            elif isinstance(val, str):
                self.push(val[::-1])
            else:
                self.push(val)
        elif inst == SimpleInstructionType.N0:
            self.push(0)
        elif inst == SimpleInstructionType.N1:
            self.push(1)
        elif inst == SimpleInstructionType.N2:
            self.push(2)
        elif inst == SimpleInstructionType.N3:
            self.push(3)
        elif inst == SimpleInstructionType.N4:
            self.push(4)
        elif inst == SimpleInstructionType.N5:
            self.push(5)
        elif inst == SimpleInstructionType.N6:
            self.push(6)
        elif inst == SimpleInstructionType.N7:
            self.push(7)
        elif inst == SimpleInstructionType.N8:
            self.push(8)
        elif inst == SimpleInstructionType.N9:
            self.push(9)
        else:
            raise ValueError(f"Unknown simple instruction '{inst}'")

    def push(self, value):
        self.stack.append(value)
    
    def pop(self):
        return self.stack.pop() if not self.empty() else 0
    
    def empty(self):
        return len(self.stack) == 0