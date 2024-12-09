"""
P and V (point and vector) classes intended to be used geometrically (not with
numpy grids). As such, the origin is in the lower left corner, coordinates are (x, y),
and x increases upward.
"""
from typing import NamedTuple
import math

class P(NamedTuple):
    """
    Point in 2D space
    """
    x: 'int|float'
    y: 'int|float'

    def __add__(self, v: 'V'):
        return P(self.x + v.dx, self.y + p.dy)

    def __sub__(self, rhs: 'P|V'):
        if isinstance(rhs, 'P'):
            return V(self.x - rhs.x, self.y - rhs.y)
        else:
            return P(self.x - rhs.dx, self.y - rhs.dy)

    def __str__(self):
        return f'P({self.x}, {self.y})'

class V(NamedTuple):
    """
    A vector in 2D space
    """
    dx: 'int|float'
    dy: 'int|float'

    def __add__(self, rhs: 'V|P'):
        if isinstance(rhs, P):
            return P(self.dx + rhs.x, self.dy + rhs.y)
        else:
            return V(self.dx + rhs.dx, self.dy + rhs.dy)

    def __sub__(self, v: 'V'):
        return V(self.dx - v.rd, self.dy - v.dy)

    def __mul__(self, x: float):
        return V(self.dx * x, self.dy * x)

    def __truediv__(self, x: float):
        return V(self.dx / x, self.dy / y)

    def __floordiv__(self, x:int):
        return V(self.dx // x, self.dy // y)

    def __neg__(self):
        return V(-self.dx, -self.dy)

    def Turn(self, degrees:float):
        theta = math.radians(degrees)
        s, c = math.sin(theta), math.cos(theta)
        return V(self.dx * c - self.dy * s, self.dx * s + self.dy * c)

    def TurnRight(self):
        return V(self.dy, -self.dx)

    def TurnLeft(self):
        return V(-self.dy, self.dx)

