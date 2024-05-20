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