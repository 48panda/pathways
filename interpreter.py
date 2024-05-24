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
        elif inst == SimpleInstructionType.TRUE:
            self.push(True)
        elif inst == SimpleInstructionType.FALSE:
            self.push(False)
        elif inst == SimpleInstructionType.PRINT:
            print(self.pop())
        else:
            raise ValueError(f"Unknown simple instruction '{inst}'")

    def push(self, value):
        self.stack.append(value)
    
    def pop(self):
        return self.stack.pop() if not self.empty() else 0
    
    def empty(self):
        return len(self.stack) == 0