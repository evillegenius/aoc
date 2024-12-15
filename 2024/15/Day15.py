#!/usr/bin/env python3
"""
<Problem description here>
"""
import numpy as np

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
        """Dot product"""
        return self.dr * v.dr + self.dc * v.dc
    
    def __abs__(self):
        """Return the vector's magnitude or length"""
        return math.sqrt(self.dr * self.dr + self.dc * self.dc)

    def Right(self):
        return V(self.dc, -self.dr)

    def Left(self):
        return V(-self.dc, self.dr)

FLOOR = 0
WALL = 1
BOX = 2
ROBOT = 3
BOXLEFT = 4
BOXRIGHT = 5

class Day15:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day15')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        emptyIndex = self.lines.index('')

        gridKey = {'.': FLOOR,
                   '#': WALL,
                   'O': BOX,
                   '@': ROBOT}
        self.height = emptyIndex
        self.width = len(self.lines[0])

        # Grid with the map
        self.grid = np.zeros((self.height, self.width), dtype=int)
        for row, line in enumerate(self.lines[:emptyIndex]):
            for col, ch in enumerate(line):
                self.grid[row, col] = gridKey[ch]

        # One big string with all the robots moves
        steps = ''.join(self.lines[emptyIndex:])
        stepToDir = {'<': V(0, -1),
                     '>': V(0, 1),
                     '^': V(-1, 0),
                     'v': V(1, 0)}
        
        self.moves = [stepToDir[step] for step in steps]

    def Show(self, grid):
        display = ".#O@[]"
        h, w = grid.shape
        for row in range(h):
            rowText = ''.join(display[grid[row, col]] for col in range(w))
            print(rowText)
                
    def Move(self, grid, loc, dir):
        newLoc = loc + dir
        contents = grid[newLoc]
        if contents == WALL:
            return loc
        if contents == FLOOR:
            grid[newLoc] = grid[loc]
            grid[loc] = FLOOR
            return newLoc
        if contents == BOX:
            self.Move(grid, newLoc, dir)
            if grid[newLoc] == FLOOR:
                grid[newLoc] = grid[loc]
                grid[loc] = FLOOR
                return newLoc
            return loc
        assert False, f'grid[{newLoc}] is {grid[newLoc]}'

    def Part1(self):
        answer = 0
        robotLoc = P(*(np.argwhere(self.grid == ROBOT)[0]))

        grid = np.copy(self.grid)

        # count = 0
        # print(f'{count}:')
        # self.Show(grid)
        # print()
        for move in self.moves:
            robotLoc = self.Move(grid, robotLoc, move)
            # count += 1
            # print(f'{count}: {move = }')
            # self.Show(grid)
            # print()

        boxLocs = np.argwhere(grid == BOX)
        for boxLoc in boxLocs:
            answer += 100 * boxLoc[0] + boxLoc[1]

        return answer

    def Move2(self, grid, loc, dir, update = True):
        newLoc = loc + dir
        contents = grid[newLoc]
        if contents == WALL:
            return loc
        if contents == FLOOR:
            if update:
                grid[newLoc] = grid[loc]
                grid[loc] = FLOOR
            return newLoc
        if contents in (BOXLEFT, BOXRIGHT):
            if dir[0] == 0:  # if moving horizontally
                newNewLoc = self.Move2(grid, newLoc, dir, update)
                if newNewLoc != newLoc:
                    if update:
                        grid[newLoc] = grid[loc]
                        grid[loc] = FLOOR
                    return newLoc
                return loc
            else:  # moving vertically, we have to move both sides.
                if contents == BOXLEFT:
                    rightLoc = newLoc + V(0, 1)
                    newRightLoc = self.Move2(grid, rightLoc, dir, update=False)
                    newLeftLoc = self.Move2(grid, newLoc, dir, update=False)
                    if newRightLoc != rightLoc and newLeftLoc != newLoc:
                        # both sides moved
                        if update:
                            newRightLoc = self.Move2(grid, rightLoc, dir, update=True)
                            newLeftLoc = self.Move2(grid, newLoc, dir, update=True)
                            grid[newLoc] = grid[loc]
                            grid[loc] = FLOOR
                            grid[rightLoc] = FLOOR
                        return newLoc
                    return loc
                else:  # contents == BOXRIGHT
                    leftLoc = newLoc + V(0, -1)
                    newLeftLoc = self.Move2(grid, leftLoc, dir, update=False)
                    newRightLoc = self.Move2(grid, newLoc, dir, update=False)
                    if newLeftLoc != leftLoc and newRightLoc != newLoc:
                        # both sides moved
                        if update:
                            newLeftLoc = self.Move2(grid, leftLoc, dir, update=True)
                            newRightLoc = self.Move2(grid, newLoc, dir, update=True)
                            grid[newLoc] = grid[loc]
                            grid[loc] = FLOOR
                            grid[leftLoc] = FLOOR
                        return newLoc
                    return loc

        assert False, f'grid[{newLoc}] is {grid[newLoc]}'

    def Part2(self):
        answer = 0

        grid = np.zeros((self.height, 2 * self.width), dtype=int)
        for r in range(self.height):
            for c in range(self.width):
                if self.grid[r, c] in (FLOOR, WALL):
                    grid[r, 2*c:2*c+2] = self.grid[r, c]
                elif self.grid[r, c] == ROBOT:
                    grid[r, 2*c] = ROBOT
                    grid[r, 2*c+1] = FLOOR
                elif self.grid[r, c] == BOX:
                    grid[r, 2*c] = BOXLEFT
                    grid[r, 2*c+1] = BOXRIGHT
                else:
                    assert False, f'self.grid[{(r, c)}] = {self.grid[r, c]}'
        robotLoc = P(*(np.argwhere(grid == ROBOT)[0]))
        # count = 0
        # print(f'{count}:')
        # self.Show(grid)
        # print()
        for move in self.moves:
            robotLoc = self.Move2(grid, robotLoc, move)
            # count += 1
            # print(f'{count}: {move = }')
            # self.Show(grid)
            # print()

        boxLocs = np.argwhere(grid == BOXLEFT)
        for boxLoc in boxLocs:
            answer += 100 * boxLoc[0] + boxLoc[1]

        return answer
    
if __name__ == '__main__':
    problem = Day15()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')