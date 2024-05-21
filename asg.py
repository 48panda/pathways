from dis import Instruction


class ASGNode:
    """A graph node. Represents both direction changes and decision branches.
    """
    def __init__(self):
        self.in_edges: list[ASGEdge] = []
        self.out_edges: list[ASGEdge] = []
        self.deg: int = 0
        self.indeg: int = 0
        self.outdeg: int = 0
        self.is_visited: bool = False
    
    def add_in_edge(self, edge: "ASGEdge"):
        self.in_edges.append(edge)
        self.deg += 1
        self.indeg += 1
    
    def add_out_edge(self, edge: "ASGEdge"):
        self.out_edges.append(edge)
        self.deg += 1
        self.outdeg += 1

class ASGEdge:
    """A graph edge. Represents the code run between two nodes.
    """
    def __init__(self, src: ASGNode, dst: ASGNode, code:list[Instruction]):
        self.src = src
        self.dst = dst
        self.code = code
        src.add_out_edge(self)
        dst.add_in_edge(self)