from asg import ASG


class Optimiser:
    def __init__(self, graph: ASG) -> None:
        self.graph = graph
    
    def optimise(self) -> ASG:
        self.remove_unreachable()
        self.remove_boring_nodes()
        return self.graph
    
    def remove_boring_nodes(self):
        i = 0
        while i < len(self.graph.nodes):
            node = self.graph.nodes[i]
            if node.indeg == 1 and node.outdeg == 1:
                in_edge = node.in_edges[0]
                out_edge = node.out_edges[0]
                in_edge.disconnect()
                out_edge.disconnect()
                self.graph.remove_edge(in_edge)
                self.graph.remove_edge(out_edge)
                self.graph.remove_node(node)
                self.graph.add_edge(in_edge + out_edge)
            else:
                i += 1
    
    def remove_unreachable(self):
        self.graph.set_visited()
        self.graph.start.visit()
        for node in self.graph.nodes:
            if not node.is_visited:
                # Unreachable
                node.remove(self.graph)