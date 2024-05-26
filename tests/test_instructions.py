import pytest
from instructions import SimpleInstructionType


simple_instructions = {
    SimpleInstructionType.AND : "&",
    SimpleInstructionType.OR : "|",
    SimpleInstructionType.ADD : "+",
    SimpleInstructionType.SUB : "-",
    SimpleInstructionType.MUL : "*",
    SimpleInstructionType.DIV : "/",
    SimpleInstructionType.MOD : "%",
    SimpleInstructionType.FALSE : "F",
    SimpleInstructionType.TRUE : "T",
    SimpleInstructionType.PRINT : "!",
    SimpleInstructionType.DUPLICATE : "d",
    SimpleInstructionType.EQUAL : "=",
    SimpleInstructionType.GREATER : "g",
    SimpleInstructionType.LESS : "l",
    SimpleInstructionType.NEGATE : "~",
    SimpleInstructionType.N0 : "0",
    SimpleInstructionType.N1 : "1",
    SimpleInstructionType.N2 : "2",
    SimpleInstructionType.N3 : "3",
    SimpleInstructionType.N4 : "4",
    SimpleInstructionType.N5 : "5",
    SimpleInstructionType.N6 : "6",
    SimpleInstructionType.N7 : "7",
    SimpleInstructionType.N8 : "8",
    SimpleInstructionType.N9 : "9"
}

for_all_simple_instructions = pytest.mark.parametrize("simpletype,simplechar", simple_instructions.items())
for_all_simple_instructions2 = pytest.mark.parametrize("simpletype2,simplechar2", simple_instructions.items())

@for_all_simple_instructions
def test_instruction_enum(simpletype, simplechar):
    assert simpletype.value == simplechar