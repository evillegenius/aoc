"""
P and V (point and vector) classes intended to be used with numpy grids. As such
the origin is in the upper left corner, coordinates are (row, col), and row increases
downward.
"""
from collections import namedtuple
import typing

class P(namedtuple('P', 'row col')):
    def __add__(self, v: 'V'):
        return P(self.row + v.dr, self.col + p.dc)

    def __sub__(self, rhs: 'P' | 'V'):
        if isinstance(rhs, P):
            return V(self.row - rhs.row, self.col - rhs.col)
        else:
            return P(self.row - rhs.dr, self.col - rhs.dc)
    def __str__(self):
        return f'P({self.row}, {self.col})'
    
class V(namedtuple('V', 'dr dc')):
    def __add__(self, rhs: 'V'|P):
        if isinstance(rhs, P):
            return P(self.dr + rhs.row, self.dc + rhs.col)
        else:
            return V(self.dr + rhs.dr, self.dc + rhs.dc)
        
    def __sub__(self, v: 'V'):
        return V(self.dr - v.rd, self.dc - v.dc)
    
    def __mul__(self, x: int):
        return V(self.dr * x, self.dc * x)
    
    def RightTurn(self):
        return V(self.dc, -self.dr)
    
    def LeftTurn(self):
        return V(-self.dc, self.dr)
    
    def UTurn(self):
        return V(-self.dr, -self.dc)
