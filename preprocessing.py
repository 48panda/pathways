"""Preprocessing -- Things to do before compilation begins.
At the moment, the only preprocessing  plannedis detecting and removing comments.
"""
from pathways_code import Code
from util import Box

def preprocess(code: Code) -> Code:
    """Do all preprocessing. A bit useless with one preprocessing task,
      but a useful layer of abstraction.

    Args:
        code (Code): The code to preprocess

    Returns:
        Code: The same code. Guaranteed to be a reference to the input 'code' parameter.
    """
    return code
