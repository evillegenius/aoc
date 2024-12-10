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

UP = V(-1, 0)
DOWN = V(1, 0)
LEFT = V(0, -1)
RIGHT = V(0, 1)

directions = (UP, DOWN, LEFT, RIGHT)

class Day10:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day10')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()

        self.lines = self.contents.split('\n')

        ########################################################################
        # If the puzzle is not grid/map based, delete these lines.
        self.height = len(self.lines)
        self.width = len(self.lines[0])

        self.grid = np.zeros((self.height, self.width), dtype=int)
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                self.grid[row, col] = int(ch)
        #
        ########################################################################


    def dfs(self, start, found):
        score = 0
        altitude = self.grid[start]
        if altitude == 9:
            if found is None:
                return 1
            if start in found:
                return 0
            found.add(start)
            return 1

        for delta in directions:
            pos = start + delta
            if (not (0 <= pos.row < self.height and 0 <= pos.col < self.width)):
                continue
            if self.grid[pos] == altitude + 1:
                score += self.dfs(pos, found)

        return score
        
    def Part1(self):
        answer = 0
        starts = [P(*item) for item in np.argwhere(self.grid == 0)]
        for start in starts:
            found = set()
            score = self.dfs(start, found)
            #print(f'{start = }, {score = }')

            answer += score

        return answer

    def Part2(self):
        answer = 0
        starts = [P(*item) for item in np.argwhere(self.grid == 0)]
        for start in starts:
            found = set()
            score = self.dfs(start, None)
            #print(f'{start = }, {score = }')

            answer += score

        return answer
    
if __name__ == '__main__':
    problem = Day10()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



