from instructions import Instruction

class ASGNode:
    def __init__(self, parent: "ASG", inst: Instruction) -> None:
        self.parent = parent
        self.inst = inst

class ASG:
    def __init__(self):
        self.nodes = []
        self.node_map = {}
    
    def add_node(self, inst: Instruction):
        node = ASGNode(self, inst)
