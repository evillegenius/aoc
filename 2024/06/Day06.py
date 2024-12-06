#!/usr/bin/env python3
"""
<Problem description here>
"""
import numpy as np
from collections import namedtuple

class Point(namedtuple('Point', ['row', 'col'])):
    __slots__ = ()
    def __add__(self, other):
        return Point(self.row + other.row, self.col + other.col)
    def __str__(self):
        return f'Point({self.row}, {self.col})'
    
# direction for initial map location
dirs = {2: Point(-1, 0),
        3: Point(0, 1),
        4: Point(1, 0),
        5: Point(0, -1)}
# when we encounter an obstacle, this is our new direction.
rotate = {Point(-1, 0): Point(0, 1),
          Point(0, 1): Point(1, 0),
          Point(1, 0): Point(0, -1),
          Point(0, -1): Point(-1, 0)}

class Day06:
    def __init__(self):
        self.input = None

        self.content = None
        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day06')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()
        self.lines = self.contents.split('\n')

        ########################################################################
        # If the puzzle is not grid/map based, delete these lines.
        gridKey = {'.': 0, '#': 1, '^': 2, '>': 3, 'v': 4, '<': 5}
        self.height = len(self.lines)
        self.width = len(self.lines[0])

        self.grid = np.zeros((self.height, self.width), dtype=int)
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                self.grid[row, col] = gridKey[ch]
        #
        ########################################################################


    def Part1(self):
        coords = np.argwhere(self.grid > 1)
        pos = Point(*coords[0])
        delta = dirs[self.grid[pos]]
        visited = set()
        while True:
            visited.add(pos)
            newPos = pos + delta
            if not ((0 <= newPos.row < self.height) and (0 <= newPos.col < self.width)):
                break
            if self.grid[newPos] == 1:
                delta = rotate[delta]
                continue
            pos = newPos

        answer = len(visited)

        return answer

    def Part2(self):
        answer = 0
        coords = np.argwhere(self.grid > 1)
        startPos = Point(*coords[0])
        startDelta = dirs[self.grid[startPos]]
        results = []
        for obsRow in range(0, self.height):
            for obsCol in range(0, self.width):
                obsPoint = Point(obsRow, obsCol)
                if self.grid[obsPoint] != 0:
                    continue
                self.grid[obsPoint] = 1
                pos = startPos
                delta = startDelta
                visited = set()  # Set of (pos, delta)

                while True:
                    visited.add((pos, delta))
                    newPos = pos + delta
                    if not ((0 <= newPos.row < self.height) and (0 <= newPos.col < self.width)):
                        break
                    if self.grid[newPos] == 1:
                        newPos = pos
                        delta = rotate[delta]
                    if (newPos, delta) in visited:
                        # We found a loop. Record it.
                        answer += 1
                        print(f'Loop: {obsPoint}')
                        break
                    pos = newPos
                self.grid[obsPoint] = 0

        return answer
    
if __name__ == '__main__':
    problem = Day06()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



