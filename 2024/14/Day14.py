#!/usr/bin/env python3
"""
<Problem description here>
"""
import re
import numpy as np

"""
P and V (point and vector) classes intended to be used with numpy grids. As such
the origin is in the upper left corner, coordinates are (row, col), and row increases
downward.
"""
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
        
    def __mod__(self, rhs: 'V'):
        return P(self.row % rhs.dr, self.col % rhs.dc)
    
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

    def __mul__(self, x: int):
        return V(self.dr * x, self.dc * x)

    def __floordiv__(self, x: int):
        return V(self.dr // x, self.dr // x)

    def __neg__(self):
        return V(-self.dy, -self.dx)

    def RightTurn(self):
        return V(self.dc, -self.dr)

    def LeftTurn(self):
        return V(-self.dc, self.dr)

class Day14:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day14')
        parser.add_argument('width', nargs='?', type=int, default=101)
        parser.add_argument('height', nargs='?', type=int, default=103)
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()

        self.lines = self.contents.split('\n')

        robotPat = re.compile(r'p=(\d+),(\d+) v=([-\d]+),([-\d]+)')
        self.robots = []
        for line in self.lines:
            if match := robotPat.match(line):
                p = P(int(match[2]), int(match[1]))
                v = V(int(match[4]), int(match[3]))

                self.robots.append((p, v))



    def Part1(self):
        answer = 0
        size = V(self.height, self.width)

        positions = [ (p + v * 100) % size for p, v in self.robots]

        halfWidth = self.width // 2
        halfHeight = self.height // 2
        quads = [0, 0, 0, 0]
        for pos in positions:
            if pos.row == halfHeight or pos.col == halfWidth:
                continue

            r = 2 if pos.row > halfHeight else 0
            c = 1 if pos.col > halfWidth  else 0
            quads[r + c] += 1

        answer = quads[0] * quads[1] * quads[2] * quads[3]
        
        return answer

    def Part2(self):
        answer = 0
        size = V(self.height, self.width)
        robots = tuple(self.robots)

        # After visualizing some of the layouts, it appears that the 
        # robots occasionally cluster vertically or horizontally.
        # I'm going to guess that when they line up that there will
        # be an extra large number of robots on one row. If that
        # doesn't find anything interesting, then I'll look for a
        # large number of robots in one column.

        grid = np.zeros((self.height, self.width), dtype=int)
        maxSec = -1
        maxMax = -1
        for seconds in range(self.width * self.height):

            for p, v in robots:
                grid[p] = 1

            rows = grid.sum(axis=0)  # sum each row
            maxRow = max(rows)  # largest number of robots in a row
            if maxRow > maxMax:
                maxMax = maxRow
                maxSec = seconds

                print('=' * self.width)
                for row in range(self.height):
                    for col in range(self.width):
                        print('#' if grid[row, col] else ' ', end='')
                    print()
                print(f'{seconds=} {maxRow=} continue? ', end='')
                input()

            robots = tuple(((p + v) % size, v) for p, v in robots)
            grid[:,:] = 0

        return maxSec

if __name__ == '__main__':
    problem = Day14()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')