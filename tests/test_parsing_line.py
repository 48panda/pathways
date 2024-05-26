import pytest
from instructions import InstructionType, SimpleInstructionType
from parsing import Line
from util import Direction
from test_instructions import for_all_simple_instructions, for_all_simple_instructions2

def _parse_line(line: str, dir: Direction = Direction.RIGHT, index: int = 0):
    line: Line = Line(line, dir, index, None)
    return line.instructions

@for_all_simple_instructions
def test_parsing_simple_instructions(simpletype, simplechar):
    assert _parse_line(simplechar) == [(InstructionType.SIMPLE, simpletype)]
    assert _parse_line(f"   {simplechar}    ") == [(InstructionType.SIMPLE, simpletype), (InstructionType.EOL, None)]

@for_all_simple_instructions
@for_all_simple_instructions2
def test_parsing_simple_instructions(simpletype, simplechar, simpletype2, simplechar2):
    assert _parse_line(simplechar+simplechar2) == [(InstructionType.SIMPLE, simpletype),(InstructionType.SIMPLE, simpletype2), (InstructionType.EOL, None)]
    assert _parse_line(f"{simplechar}     {simplechar2}") == [(InstructionType.SIMPLE, simpletype),(InstructionType.SIMPLE, simpletype2), (InstructionType.EOL, None)]

@for_all_simple_instructions
def test_parsing_cond_and_simple_instructions(simpletype, simplechar):
    assert _parse_line("?"+simplechar) == [(InstructionType.COND,(InstructionType.SIMPLE, simpletype)), (InstructionType.EOL, None)]
    assert _parse_line("????"+simplechar) == [(InstructionType.SIMPLE, SimpleInstructionType.AND),(InstructionType.SIMPLE, SimpleInstructionType.AND),(InstructionType.SIMPLE, SimpleInstructionType.AND),(InstructionType.COND,(InstructionType.SIMPLE, simpletype)), (InstructionType.EOL, None)]

def test_string():
    assert _parse_line("\"+-/\"") == [(InstructionType.STRING, "+-/"), (InstructionType.EOL, None),(InstructionType.SIMPLE, SimpleInstructionType.ADD),(InstructionType.SIMPLE, SimpleInstructionType.SUB),(InstructionType.SIMPLE, SimpleInstructionType.DIV), (InstructionType.EOL, None)]