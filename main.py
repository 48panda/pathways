from optimise_graph import Optimiser
from pathways_code import Code
from parsing import Parser
from preprocessing import preprocess
from interpreter import Interpreter

test_code = """\
<<<<<<< Updated upstream
N234d!!
=======
"Hello world!"! v
v!~"Helloworld2"<
>'v!v
  1 
 ^< <
>>>>>>> Stashed changes
"""

parser = Parser(preprocess(Code(test_code)))
graph = parser.get_graph()
graph = Optimiser(graph).optimise()
Interpreter(graph).start_interpreting()
graph.show()
