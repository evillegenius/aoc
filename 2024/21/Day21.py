#!/usr/bin/env python3

"""
P and V (point and vector) classes intended to be used with numpy grids. As such
the origin is in the upper left corner, coordinates are (row, col), and row increases
downward.
"""
import math
import functools
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

class Day21:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day21')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.doorGrid = {'0': P(3, 1),
                         '1': P(2, 0),
                         '2': P(2, 1),
                         '3': P(2, 2),
                         '4': P(1, 0),
                         '5': P(1, 1),
                         '6': P(1, 2),
                         '7': P(0, 0),
                         '8': P(0, 1),
                         '9': P(0, 2),
                         'A': P(3, 2),
                         'X': P(3, 0)}

        self.arrowGrid = {'^': P(0, 1),
                          '<': P(1, 0),
                          'v': P(1, 1),
                          '>': P(1, 2),
                          'A': P(0, 2),
                          'X': P(0, 0)}

        self.step = {'^': UP,
                     'v': DOWN,
                     '<': LEFT,
                     '>': RIGHT,
                     'A': V(0,0)}

    def Fatal(self, steps, pos, deathPos):
        for step in steps:
            pos += self.step[step]
            if pos == deathPos:
                return True

        return False

    def Solve(self, grid, code):
        startPos = grid['A']
        route = []
        for ch in code:
            endPos = grid[ch]
            delta = endPos - startPos
            steps = '<' * -delta.dc + 'v' * delta.dr + '>' * delta.dc + '^' * -delta.dr
            if self.Fatal(steps, startPos, grid['X']):
                steps = '^' * -delta.dr + '>' * delta.dc + 'v' * delta.dr + '<' * -delta.dc
            route.append(steps)
            route.append('A')
            startPos = endPos

        route = ''.join(route)
        # print(f'{code}: {route}')

        return route

    def Part1(self):
        answer = 0
        for line in self.lines:
            route1 = self.Solve(self.doorGrid, line)
            route2 = self.Solve(self.arrowGrid, route1)
            route3 = self.Solve(self.arrowGrid, route2)
            print(f'{line}:')
            print(f'{len(route1):6}: {route1}')
            print(f'{len(route2):6}: {route2}')
            print(f'{len(route3):6}: {route3}')
            answer += len(route3) * int(line[:-1])

        return answer

    @functools.cache
    def Solve2(self, code, depth):
        grid = self.arrowGrid if code[0] in "<>^v" else self.doorGrid

        if depth == 0:
            return len(code)

        # Path that moves horizontally first
        hPath = lambda v: '>' * v.dc + '<' * -v.dc + 'v' * v.dr + '^' * -v.dr + 'A'
        # Path that moves vertically first
        vPath = lambda v: 'v' * v.dr + '^' * -v.dr + '>' * v.dc + '<' * -v.dc + 'A'

        count = 0
        pos = grid['A']
        for ch in code:
            endPos = grid[ch]
            delta = endPos - pos
            hPos = pos + V(0, delta.dc)  # position after moving horizontally
            vPos = pos + V(delta.dr, 0)  # position after moving vertically

            count1 = self.Solve2(hPath(delta), depth - 1) if hPos != grid['X'] else math.inf
            count2 = self.Solve2(vPath(delta), depth - 1) if vPos != grid['X'] else math.inf

            count += min(count1, count2)
            pos = endPos

        return count

    def Part2(self):
        answer = 0

        for line in self.lines:
            count = self.Solve2(line, 26)

            print(f'{line}: {count}')
            answer += count * int(line[:-1])

        return answer

if __name__ == '__main__':
    problem = Day21()

    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')
