#!/usr/bin/env python3
"""
<Problem description here>
"""
import numpy as np
import fractions

"""
P and V (point and vector) classes intended to be used with numpy grids. As such
the origin is in the upper left corner, coordinates are (row, col), and row increases
downward.
"""
from collections import namedtuple
import typing

class P(namedtuple('P', 'row col')):
    def __add__(self, v: 'V'):
        return P(self.row + v.dr, self.col + v.dc)

    def __sub__(self, rhs: 'P|V'):
        if isinstance(rhs, P):
            return V(self.row - rhs.row, self.col - rhs.col)
        else:
            return P(self.row - rhs.dr, self.col - rhs.dc)
    def __str__(self):
        return f'P({self.row}, {self.col})'
    
class V(namedtuple('V', 'dr dc')):
    def __add__(self, rhs: 'V|P'):
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

class Day08:
    def __init__(self):
        self.input = None

        self.contents = None
        self.lines = []
        self.grid = None
        self.freqs = set()
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day08')
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
                value = 0 if ch == '.' else ord(ch)
                self.grid[row, col] = value

                self.freqs.add(ch)

        self.freqs.remove('.')
        #
        ########################################################################


    def Part1(self):
        answer = 0

        self.antiNodes = set()
        for freq in self.freqs:
            locs = np.argwhere(self.grid == ord(freq))
            for i in range(0, len(locs) - 1):
                iPos = P(*locs[i])
                for j in range(i+1, len(locs)):
                    jPos = P(*locs[j])
                    delta = jPos - iPos
                    anti1 = jPos + delta
                    anti2 = iPos - delta
                    if 0 <= anti1.row < self.height and 0 <= anti1.col < self.width:
                        self.antiNodes.add(jPos + delta)
                    if 0 <= anti2.row < self.height and 0 <= anti2.col < self.width:
                        self.antiNodes.add(iPos - delta)

        answer = len(self.antiNodes)
        return answer

    def Part2(self):
        answer = 0
        antiNodes = set()
        for freq in self.freqs:
            locs = np.argwhere(self.grid == ord(freq))
            for i in range(0, len(locs) - 1):
                iPos = P(*locs[i])
                for j in range(i+1, len(locs)):
                    jPos = P(*locs[j])
                    delta = jPos - iPos
                    if delta.dr == 0:
                        for col in range(self.width):
                            antiNodes.add(P(jPos.row, col))
                        continue
                    # XXX: Round to 8 digits to solve math errors.
                    line = lambda row: round((row - iPos.row) * ((jPos.col - iPos.col) / (jPos.row - iPos.row)) + iPos.col, 8)
                    assert line(iPos.row) == iPos.col  # debugging
                    assert line(jPos.row) == jPos.col  # debugging
                    for row in range(self.height):
                        col = line(row)
                        if 0 <= col < self.width and col == int(col):
                            antiNodes.add(P(row, int(col)))


        import pprint
        pprint.pprint(antiNodes)
        answer = len(antiNodes)
        return answer
    
if __name__ == '__main__':
    problem = Day08()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



