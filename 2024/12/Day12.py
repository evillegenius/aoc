#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
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
    row: int
    col: int

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
    dr: int
    dc: int
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

    def Right(self):
        return V(self.dc, -self.dr)

    def Left(self):
        return V(-self.dc, self.dr)

directions = (V(0, 1), V(1, 0), V(0, -1), V(-1, 0))

class Day12:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day12')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)

    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        ########################################################################
        # If the puzzle is not grid/map based, delete these lines.
        self.height = len(self.lines)
        self.width = len(self.lines[0])

        self.grid = np.zeros((self.height+2, self.width+2), dtype=int)
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                self.grid[row+1, col+1] = ord(ch)
        #
        ########################################################################

    def flood(self, todo):
        area = 0
        perimeter = 0
        queue = set()
        p = todo.pop()
        label = self.grid[p]
        queue.add(p)
        while queue:
            p = queue.pop()
            area += 1
            for d in directions:
                newP = p + d
                newLabel = self.grid[newP]
                if newLabel != label:
                    perimeter += 1
                    continue
                if newP in todo:
                    queue.add(newP)
                    todo.discard(newP)
        return (label, area, perimeter)

    def Part1(self):
        answer = 0
        # Let's try a flood fill type of algorithm.
        todo = {P(row, col) for row in range(1, self.height+1) for col in range(1, self.width+1)}
        while todo:
            label, area, perimeter = self.flood(todo)
            print(f'{chr(label)}: {area=}, {perimeter=}')
            answer += area * perimeter
        return answer

    def flood2(self, todo):
        area = 0
        sides = 0
        queue = set()
        inside = set()
        p = todo.pop()
        label = self.grid[p]
        queue.add(p)
        inside.add(p)
        edges = set()
        while queue:
            p = queue.pop()
            for d in directions:
                newP = p + d
                newLabel = self.grid[newP]
                if newLabel != label:
                    edges.add((p, newP))
                    continue
                if newP in todo:
                    queue.add(newP)
                    inside.add(newP)
                    todo.discard(newP)
        area = len(inside)

        # Count the sides.
        while (edges):
            p, newP = edges.pop()
            sides += 1
            edgeDir = newP - p
            stepRight = edgeDir.Right()
            rp = p + stepRight
            rNewP = newP + stepRight
            while (rp, rNewP) in edges:
                edges.remove((rp, rNewP))
                rp += stepRight
                rNewP += stepRight

            stepLeft = edgeDir.Left()
            lp = p + stepLeft
            lNewP = newP + stepLeft
            while (lp, lNewP) in edges:
                edges.remove((lp, lNewP))
                lp += stepLeft
                lNewP += stepLeft

        return (label, area, sides)

    def Part2(self):
        answer = 0
        # Let's try a flood fill type of algorithm.
        todo = {P(row, col) for row in range(1, self.height+1) for col in range(1, self.width+1)}
        while todo:
            label, area, sides = self.flood2(todo)
            print(f'{chr(label)}: {area=}, {sides=}')
            answer += area * sides
        return answer
    
if __name__ == '__main__':
    problem = Day12()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')
