#!/usr/bin/env python3
"""
<Problem description here>
"""

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
        if isinstance(rhs, V):
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

DIRECTIONS = RIGHT, UP, LEFT, DOWN = V(0, 1), V(-1, 0), V(0, -1), V(1 ,0)

class Day20:
    def __init__(self):
        self.input = None

        self.lines = []
        self.cost = None
        self.cheats = None

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day20')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()

        self.lines = self.contents.split('\n')

        self.height = len(self.lines)
        self.width = len(self.lines[0])

        self.floor = set()
        self.walls = set()
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                if ch == '.':
                    self.floor.add(P(row, col))
                elif ch == '#' and 0 < row < self.height - 1 and 0 < col < self.width - 1:
                    # Don't add the outside edges.
                    self.walls.add(P(row, col))
                elif ch == 'S':
                    self.startPos = P(row, col)
                    self.floor.add(self.startPos)
                elif ch == 'E':
                    self.goalPos = P(row, col)
                    self.floor.add(self.goalPos)


    def Traverse(self, todo):
        # Find the non-cheating cost
        while todo:
            p = todo.pop()
            costs = [self.cost[p + d]
                     for d in DIRECTIONS
                     if p + d in self.floor]
            minCost = min(costs) + 1
            if minCost < self.cost[p]:
                self.cost[p] = minCost
                todo.update(p + d for d in DIRECTIONS if p + d in self.floor)

        return self.cost[self.goalPos]

    def manhattan(self, pos, size):
        for r in range(-size, size + 1):
            for c in range(-(size - abs(r)), (size - abs(r)) + 1):
                end = P(pos.row + r, pos.col + c)
                if (pos, end) in self.cheats:
                    continue
                dist = abs(r) + abs(c)
                yield end, (abs(r) + abs(c))

    def Solve(self):
        self.cost = dict.fromkeys(self.floor, math.inf)
        self.cost[self.startPos] = 0
        todo = set(self.startPos + d
                   for d in DIRECTIONS
                   if self.startPos + d in self.floor)
        baseLength = self.Traverse(todo)
        print(f'{baseLength=}')

    def Cheat(self, maxCheat, minDist):
        if self.cost is None:
            self.Solve()

        self.cheats = set()
        for i, cheatPos in enumerate(self.floor):
            # print(f'{(i * 100 // len(self.walls)):3}%',end='\r')

            # Find all the points within maxCheat manhattan distance
            # and pretend we can reach it in manhattan distance steps
            # count how many such points reduce the cost by >= minDist.
            for cheatEnd, cheatDist in self.manhattan(cheatPos, maxCheat):
                if self.cost.get(cheatEnd, -1) - self.cost[cheatPos] - cheatDist >= minDist:
                    self.cheats.add((cheatPos, cheatEnd))

        return len(self.cheats)

    def Part1(self):
        return self.Cheat(2, 100)

    def Part2(self):
        return self.Cheat(20, 100)

if __name__ == '__main__':
    problem = Day20()

    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



