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
    return preprocess_comments(code)

def preprocess_comments(code: Code) -> Code:
    """Removes all comments from the code.

    Args:
        code (Code): The code to preprocess

    Raises:
        ValueError: Temporary error message. All of the comment system needs
        to be updated completely. The error happens when the comment system
        cannot decide whether a comment should be horizontal or vertical.
        Some more though is required.

    Returns:
        Code: _description_
    """
    comments: "list[Box]" = []
    for x in range(code.width):
        for y in range(code.height): # Iterate through the code
            if code.get(x,y) != "#": # We only care about comments here.
                continue
            if any(map(lambda z:(x,y) in z, comments)): # If in any of the comments, continue
                continue
            dx = 1 # Find the width of the comment if we choose horizontal.
            while code.get(x + dx, y) != "#" and x + dx <= code.width:
                dx += 1
            if x + dx > code.width:
                dx = -1
            dy = 1 # Find the height if we choose vertical.
            while code.get(x, y + dy) != "#" and y + dy <= code.height:
                dy += 1
            if y + dy > code.height:
                dx = -1
            if dx > dy: # Choose the axis that will result in the largest comment.
                comments.append(Box(x, y, x+dx, y))
            elif dy > dx:
                comments.append(Box(x, y, x, y+dy))
            else:
                raise ValueError("Equal comment gap!")
    for c in comments:
        for x,y in c.iter():
            code.set(x,y," ")
    return code