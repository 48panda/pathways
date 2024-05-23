from asg import ASG


class Optimiser:
    def __init__(self, graph: ASG) -> None:
        self.graph = graph
    
    def optimise(self) -> ASG:
        return self.graph