from pathways_code import Code
from parsing import Parser
from preprocessing import preprocess

test_code = """\
>AB?v
?   C
H   D
G   ?
^?FE<
"""

parser = Parser(preprocess(Code(test_code)))
graph = parser.get_graph()
graph.show()