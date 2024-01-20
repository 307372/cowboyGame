import math
class Pos():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def __mul__(self, value):
        return Pos(self.x * value, self.y * value)

    def len(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalized(self):
        return Pos(self.x/self.len(), self.y/self.len())

    def __str__(self):
        return '(x=' + str(self.x) + ',y=' + str(self.y) + ')'
