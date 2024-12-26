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

UP, DOWN, RIGHT, LEFT = V(-1, 0), V(1, 0), V(0, 1), V(0, -1)

DIRECTIONS = (RIGHT, UP, LEFT, DOWN)

class Day18:
    def __init__(self):
        self.input = None

        self.lines = []
        self.floor = set()

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day18')
        parser.add_argument('-s', '--size', type=int, default=70,
                            help='Size of the grid (from 0 to size inclusive) so'
                            ' width = height = size + 1')
        parser.add_argument('-c', '--count', type=int, default=1024,
                            help='number of bytes to drop (the input is larger than this)')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()

        self.lines = self.contents.split('\n')

        self.width = self.size + 1
        self.height = self.size + 1

        for row in range(self.height):
            for col in range(self.width):
                self.floor.add(P(row, col))

        for line in self.lines[:self.count]:
            c, r = list(map(int, line.split(',')))
            self.floor.discard(P(r, c))

    def Part1(self):
        answer = 0
        cost = dict.fromkeys(self.floor, math.inf)
        cost[P(0, 0)] = 0

        todo = set()
        for p in (P(0, 1), P(1, 0)):
            if p in self.floor:
                todo.add(p)

        while todo:
            p = todo.pop()
            costs = [cost[p + d]
                     for d in DIRECTIONS
                     if p + d in self.floor]
            minCost = min(costs) + 1
            if minCost < cost[p]:
                cost[p] = minCost
                todo.update(p + d for d in DIRECTIONS if p + d in self.floor)

        answer = cost[P(self.size, self.size)]

        return answer

    def Part2(self):
        answer = 0

        exit = P(self.size, self.size)

        # Just drop bytes until we cannot get to the exit
        for i, line in enumerate(self.lines[self.count:]):
            c, r = list(map(int, line.split(',')))
            self.floor.discard(P(r, c))

            cost = dict.fromkeys(self.floor, math.inf)
            cost[P(0, 0)] = 0

            todo = set()
            for p in (P(0, 1), P(1, 0)):
                if p in self.floor:
                    todo.add(p)

            while todo:
                p = todo.pop()
                costs = [cost[p + d]
                        for d in DIRECTIONS
                        if p + d in self.floor]
                minCost = min(costs) + 1
                if minCost < cost[p]:
                    cost[p] = minCost
                    todo.update(p + d for d in DIRECTIONS if p + d in self.floor)

            # print(f'{i:4}: ({r:2},{c:2}) cost = {cost[exit]}')
            if cost[exit] == math.inf:
                answer = f'{c},{r}'
                break

        return answer

if __name__ == '__main__':
    problem = Day18()

    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')
