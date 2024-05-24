from optimise_graph import Optimiser
from pathways_code import Code
from parsing import Parser
from preprocessing import preprocess

test_code = """\
>AB?v
?   ?
<   v
G   ?
^?^E<
"""

parser = Parser(preprocess(Code(test_code)))
graph = parser.get_graph()
graph = Optimiser(graph).optimise()
graph.show()