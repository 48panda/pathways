from pathways_code import Code
from parsing import Parser
from preprocessing import preprocess

test_code = """\
>ABCv
L   D
K   E
J   F
^IHG<
"""

x = Parser(preprocess(Code(test_code)))
print(x)

# branch: parsing
# Next steps:
#  * Link entry and exit nodes
#  * Create an ASG -- a graph where nodes = entry/exit points,
#       and edges are groups of non-control-flow instructions
# * Parsing branch complete!