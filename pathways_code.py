import itertools
import typing

class Code:
    """The first data format the source code is moved into. Used in preprocessing
    """
    def __init__(self, code: str):
        """Initialises code. splits the code into lines

        Args:
            code (str): The raw pathways source code.
        """
        self.code = code.split("\n")
        # Get width and height. Useful later.
        self.height = len(self.code)
        self.width = max(map(len, self.code))

        for i in range(self.height): # Remove \r in case they were there.
            if self.code[i].endswith("\r"):
                self.code[i] = self.code[i][:-1]

    def get(self, x: int, y: int) -> str:
        """Gets a character in the code.

        Args:
            x (int): x coordinate
            y (int): y coordinate

        Returns:
            str: The character at that position.
        """
        if 0 <= y < self.height and 0 <= x < len(self.code[y]):
            return self.code[y][x]
        return " " # Whitespace if not in range.

    def set(self, x: int, y: int, v: str) -> None:
        """Sets a character's value.

        Args:
            x (int): the x coordinate to set
            y (int): the y coordinate to set
            v (str): the value to set to

        Raises:
            IndexError: Setting out-of-bounds to non-whitespace.
        """
        if 0 <= y < self.height and 0 <= x < len(self.code[y]): # Check the value is in-bounds.
            self.code[y] = self.code[y][:x] + v + self.code[y][x+1:]
            return
        if v == " ": # If not in range, but value is whitespace, silently fail (it is already being treated as whitespace in get)
            return
        raise IndexError(x,y) # Should never be called, so there is an error in the code, so abort.

    # Helper iteration functions
    def iter_rows(self) -> typing.Iterable[str]:
        """Returns an iterable of rows.

        Returns:
            typing.Iterable[str]: An iterable of rows, top to bottom.
        """
        return iter(self.code)

    def iter_cols(self) -> typing.Iterable[str]:
        """Returns an iterable of columns.

        Returns:
            typing.Iterable[str]: An iterable of columns, left to right.
        """
        return itertools.zip_longest(*self.code,fillvalue=" ")
    
    def __str__(self):
        return "\n".join(self.code)