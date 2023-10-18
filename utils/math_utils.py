# Vector class (used for the velocity computation)
class Vec:
    def __init__(self, x, y):
        self.x: float = float(x)
        self.y: float = float(y)

    def reset(self):
        self.x = self.y = 0
