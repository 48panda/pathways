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
    hcomments: "list[Box]" = []
    hfaults: int = 0 # Number of rows with odd hashtag
    for y in range(code.height): # Iterate through the code
        for x in range(code.width):
            if code.get(x,y) != "#": # We only care about comments here.
                continue
            if len(hcomments) > 0 and (x, y) in hcomments[-1]:
                continue # End tag
            dx = 1 # Find the width of the comment.
            while code.get(x + dx, y) != "#" and x + dx <= code.width:
                dx += 1
            if x + dx > code.width:
                hfaults += 1 # Fault found!
                hcomments.append(Box(x, y, code.width, y))
                break
            hcomments.append(Box(x, y, x+dx, y))

    vcomments: "list[Box]" = []
    vfaults: int = 0 # Number of cols with odd hashtag
    for x in range(code.width): # Iterate through the code
        for y in range(code.height):
            if code.get(x,y) != "#": # We only care about comments here.
                continue
            if len(vcomments) > 0 and (x, y) in vcomments[-1]:
                continue # End tag
            dy = 1 # Find the height of the comment.
            while code.get(x, y + dy) != "#" and y + dy <= code.height:
                dy += 1
            if y + dy > code.height:
                vfaults += 1 # Fault found!
                vcomments.append(Box(x, y, x, code.height))
                break
            vcomments.append(Box(x, y, x, y + dy))
    axis: int = 0 # 1 for vertical, 2 for horizontal
    hchars = sum(map(len, hcomments))
    vchars = sum(map(len, vcomments))
    if hfaults > vfaults:
        axis = 1
    elif hfaults < vfaults:
        axis = 2
    elif hchars > vchars:
        axis = 2
    elif hchars < vchars:
        axis = 1
    else:
        axis = 2
    if axis == 1:
        comments = vcomments
    else:
        comments = hcomments
    for c in comments:
        for x,y in c:
            code.set(x,y," ")
    print(hcomments)
    return code