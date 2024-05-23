import enum
from instructions import Instruction, stringify_instrs
from typing import Dict, List, Tuple
from util import Direction

class ASGNode:
    """A graph node. Represents both direction changes and decision branches.
    """
    def __init__(self) -> None:
        self.in_edges: List[ASGEdge] = []
        self.out_edges: List[ASGEdge] = []
        self.deg: int = 0
        self.indeg: int = 0
        self.outdeg: int = 0
        self.is_visited: bool = False

    def add_in_edge(self, edge: "ASGEdge") -> None:
        self.in_edges.append(edge)
        self.deg += 1
        self.indeg += 1

    def add_out_edge(self, edge: "ASGEdge") -> None:
        self.out_edges.append(edge)
        self.deg += 1
        self.outdeg += 1

class ASGTerminalNode(ASGNode):
    def __init__(self):
        ASGNode.__init__(self)
        self.value = 15
        self.group = 2
    
    def add_out_edge(self, edge: "ASGEdge") -> None:
        raise TypeError("Terminal Node may not have outgoing edges")

    def id(self):
        return "T"

class ASGStartNode(ASGNode):
    def __init__(self):
        ASGNode.__init__(self)
        self.value = 15
        self.group = 3
    
    def add_in_edge(self, edge: "ASGEdge") -> None:
        raise TypeError("Start Node may not have incoming edges")

    def id(self):
        return "S"


dcount = 0
class ASGDecisionNode(ASGNode):
    """A graph node. Represents decision branches.
    """
    def __init__(self) -> None:
        ASGNode.__init__(self)
        global dcount
        dcount += 1
        self.name = dcount
        self.group = 1
        self.value = 10

    def id(self):
        return f"D{self.name}"

class ASGArrowNode(ASGNode):
    """A graph node. Represents direction changes.
    """
    def __init__(self, dir, x, y) -> None:
        ASGNode.__init__(self)
        self.dir: Direction = dir
        self.x: int = x
        self.y: int = y
        self.group = 0
        self.value = 20
    
    def id(self):
        return f"{'UDLR'[self.dir.value]}-{self.x}-{self.y}"

class EdgeType(enum.Enum):
    ALWAYS = 0
    TRUE = 1
    FALSE = 2
    

class ASGEdge:
    """A graph edge. Represents the code run between two nodes.
    """
    def __init__(self, src: ASGNode, dst: ASGNode, code: List[Instruction], type: EdgeType = EdgeType.ALWAYS) -> None:
        self.src = src
        self.dst = dst
        self.code = code
        src.add_out_edge(self)
        dst.add_in_edge(self)
        self.type = type
    
    def get_pyvis_edge_data(self):
        return (self.src.id(), self.dst.id())
    
    def get_color(self):
        if self.type == EdgeType.ALWAYS:
            return "blue"
        elif self.type == EdgeType.FALSE:
            return "red"
        elif self.type == EdgeType.TRUE:
            return "green"

class ASG:
    def __init__(self) -> None:
        self.arrow_nodes: Dict[Tuple[Direction, int, int], ASGArrowNode] = {}
        self.arrow_to_arrow_edges: Dict[Tuple[Tuple[Direction, int, int], Tuple[Direction, int, int]], ASGEdge] = {}
        self.edges: List[ASGEdge] = []
        self.nodes: List[ASGNode] = []
        self.terminal: ASGTerminalNode = ASGTerminalNode()
        self.start: ASGTerminalNode = ASGStartNode()

    def add_arrow_node(self, node: ASGArrowNode) -> None:
        self.arrow_nodes[(node.dir, node.x, node.y)] = node
        self.nodes.append(node)

    def add_edge(self, edge: ASGEdge) -> None:
        if isinstance(edge.src, ASGArrowNode) and isinstance(edge.dst, ASGArrowNode):
            self.arrow_to_arrow_edges[((edge.src.dir, edge.src.x, edge.src.y), (edge.dst.dir, edge.dst.x, edge.dst.y))] = edge
        self.edges.append(edge)
        
    def add_decision_node(self, node: ASGDecisionNode) -> None:
        self.nodes.append(node)
    
    def get_arrow_node(self, dir: Direction, x: int, y: int) -> ASGArrowNode:
        return self.arrow_nodes[(dir, x, y)]

    def show(self, filename: str = "graph.html"):
        from pyvis.network import Network
        net = Network(directed=True)
        for node in self.nodes + [self.terminal, self.start]:
            net.add_node(node.id(), value=node.value, group=node.group)
        for edge in self.edges:
            net.add_edge(*edge.get_pyvis_edge_data(), label=stringify_instrs(edge.code), color=edge.get_color())
        net.set_edge_smooth("dynamic")
        net.show(filename, notebook=False)