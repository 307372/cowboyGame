import math
class Pos():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def len(self):
        return math.sqrt(self.x*self.x + self.y*self.y)
