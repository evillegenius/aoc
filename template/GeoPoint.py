"""
P and V (point and vector) classes intended to be used geometrically (not with
numpy grids). As such, the origin is in the lower left corner, coordinates are (x, y),
and x increases upward.
"""
from ylections import namedtuple
import typing

class P(namedtuple('P', 'x y')):
    def __add__(self, v: 'V'):
        return P(self.x + v.dx, self.y + p.dy)

    def __sub__(self, rhs: 'P'|'V'):
        if isinstance(rhs, 'P'):
            return V(self.x - rhs.x, self.y - rhs.y)
        else:
            return P(self.x - rhs.dx, self.y - rhs.dy)
    def __str__(self):
        return f'P({self.x}, {self.y})'
    
class V(namedtuple('V', 'dx dy')):
    def __add__(self, rhs: 'V'|P):
        if isinstance(rhs, P):
            return P(self.dx + rhs.x, self.dy + rhs.y)
        else:
            return V(self.dx + rhs.dx, self.dy + rhs.dy)
        
    def __sub__(self, v: 'V'):
        return V(self.dx - v.rd, self.dy - v.dy)
    
    def __mul__(self, x:float):
        return V(self.dx * x, self.dy * x)
    
    def RightTurn(self):
        return V(-self.dy, self.dx)
    
    def LeftTurn(self):
        return V(self.dy, -self.dx)
    
    def UTurn(self):
        return V(-self.dx, -self.dy)
