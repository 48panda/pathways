class Box:
    """A utility class for 2d boxes of code (comments)
    """
    def __init__(self, x: int, y: int, x2: int, y2: int):
        """Creates a 2d box

        Args:
            x (int): Start x
            y (int): Start y
            x2 (int): End x (inclusive)
            y2 (int): End y (inclusive)
        """
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
    
    def __str__(self):
        return f"<{self.x},{self.y},{self.x2},{self.y2}>"
    
    def __len__(self):
        return (self.x2 - self.x + 1) * (self.y2 - self.y + 1)
    
    def __contains__(self, other):
        return self.x <= other[0] <= self.x2 and self.y <= other[1] <= self.y2
    
    def __repr__(self):
        return str(self)
    
    def __iter__(self):
        return ((x,y) for y in range(self.y, self.y2+1) for x in range(self.x, self.x2+1))