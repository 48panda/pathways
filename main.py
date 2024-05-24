from optimise_graph import Optimiser
from pathways_code import Code
from parsing import Parser
from preprocessing import preprocess
from interpreter import Interpreter

test_code = """\
>n12?v
?    CA
H    D
G    ?
^?F E<

"""

parser = Parser(preprocess(Code(test_code)))
graph = parser.get_graph()
graph = Optimiser(graph).optimise()
Interpreter(graph).start_interpreting()
# graph.show()
