"""
P and V (point and vector) classes intended to be used with numpy grids. As such
the origin is in the upper left corner, coordinates are (row, col), and row increases
downward.
"""
import math
from typing import NamedTuple

class P(NamedTuple):
    """
    Point in a numpy grid.
    """
    row: 'int'
    col: 'int'

    def __add__(self, v: 'V'):
        return P(self.row + v.dr, self.col + v.dc)

    def __sub__(self, rhs: 'P|V'):
        if isinstance(rhs, P):
            return V(self.row - rhs.row, self.col - rhs.col)
        else:
            return P(self.row - rhs.dr, self.col - rhs.dc)

    def __mod__(self, v: 'V'):
        """Modulo operator, good for wrapping around into bounds"""
        return P(self.row % v.dr, self.col % v.dc)

    def __str__(self):
        return f'P({self.row}, {self.col})'

class V(NamedTuple):
    """
    A vector in a numpy grid.
    """
    dr: 'int'
    dc: 'int'

    def __add__(self, rhs: 'V|P'):
        if isinstance(rhs, P):
            return P(self.dr + rhs.row, self.dc + rhs.col)
        else:
            return V(self.dr + rhs.dr, self.dc + rhs.dc)

    def __sub__(self, v: 'V'):
        return V(self.dr - v.rd, self.dc - v.dc)

    def __mul__(self, rhs: 'int|V'):
        """Scalar multiplication or dot product"""
        if isinstance(rhs, 'V'):
            return self.dr * rhs.dr + self.dy * rhs.dy

        return V(self.dr * rhs, self.dc * rhs)

    def __rmul__(self, lhs: 'int'):
        return V(lhs * self.dr, lhs * self.dc)

    def __floordiv__(self, x: int):
        return V(self.dr // x, self.dr // x)

    def __neg__(self):
        return V(-self.dy, -self.dx)

    def __xor__(self, v: 'V'):
        """Cross product"""
        return self.dr * v.dr + self.dc * v.dc

    def __abs__(self):
        """Return the vector's magnitude or length"""
        return math.sqrt(self.dr * self.dr + self.dc * self.dc)

    def Right(self):
        return V(self.dc, -self.dr)

    def Left(self):
        return V(-self.dc, self.dr)

DIRECTIONS = RIGHT, UP, LEFT, DOWN = V(0, 1), V(-1, 0), V(0, -1), V(1, 0)

doorGrid = {'0': P(3, 1),
            '1': P(2, 0),
            '2': P(2, 1),
            '3': P(2, 2),
            '4': P(1, 0),
            '5': P(1, 1),
            '6': P(1, 2),
            '7': P(0, 0),
            '8': P(0, 1),
            '9': P(0, 2),
            'A': P(3, 2)}
        
arrowGrid = {'^': P(0, 1),
             '<': P(1, 0),
             'v': P(1, 1),
             '>': P(1, 2),
             'A': P(0, 2)}

doorEncode = {v: k for k, v in doorGrid.items()}
arrowEncode = {v: k for k, v in arrowGrid.items()}

arrows = {'>': RIGHT, '<': LEFT, '^':UP, 'v':DOWN, ' ':V(0, 0)}

code3 = '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
code3 = '<<vA>>^AvA^A<<vA>>^AA<<vA>A>^AAvAA^<A>A<vA>^AA<A>A<<vA>A>^AAAvA^<A>A'
def Decode(grid, encode, code):
    pos = grid['A']
    result = ""
    for ch in code:
        if ch == 'A':
            result += encode[pos]
        else:
            pos += arrows[ch]
            result += ' '
    
    return result;

code2 = Decode(arrowGrid, arrowEncode, code3)
code1 = Decode(arrowGrid, arrowEncode, code2)
code0 = Decode(doorGrid, doorEncode, code1)

print(f'{code3 = }')
print(f'{code2 = }')
print(f'{code1 = }')
print(f'{code0 = }')

