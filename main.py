from optimise_graph import Optimiser
from pathways_code import Code
from parsing import Parser
from preprocessing import preprocess
from interpreter import Interpreter

test_code = """\
2">!"v
  ^  <
"""

parser = Parser(preprocess(Code(test_code)))
print(parser)
graph = parser.get_graph()
graph = Optimiser(graph).optimise()
Interpreter(graph).start_interpreting()
graph.show()
