from asg import ASG


class Interpreter:
    def __init__(self, graph: ASG):
        self.graph = graph
        self.node = self.graph.start