#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re
import numpy as np
from collections import namedtuple

class Point(namedtuple('Point', 'x y')):
    def __sub__(self, rhs):
        if isinstance(rhs, Point):
            return Vector(self.x - rhs.x, 
                          self.y - rhs.y)
        else:
            return Point(self.x - rhs.dx,
                         self.y - rhs.dy)
        
    def __isub__(self, rhs):
        assert isinstance(rhs, Vector)
        return self - rhs
    
    def __add__(self, rhs):
        return Point(self.x + rhs.dx,
                     self.y + rhs.dy)

    def __iadd__(self, rhs):
        return self.__add__(rhs)

class Vector(namedtuple('Vector', 'dx dy')):
    def __add__(self, rhs):
        return Vector(self.dx + rhs.dx,
                      self.dy + rhs.dy)

    def __sub__(self, rhs):
        return Vector(self.dx - rhs.dx,
                      self.dy - rhs.dy)

    def __iadd__(self, rhs):
        return self.__add__(rhs)
    
    def __isub__(self, rhs):
        return self.__sub__(rhs)
    
    def __matmul__(self, rhs):
        """@ - Dot product"""
        return (self.dx * rhs.dx +
                self.dy * rhs.dy +
                self.dz * rhs.dz)
    
    def __xor__(self, rhs):
        """^ - Cross product"""
        return Vector(self.dy * rhs.dz - self.dz * rhs.dy,
                      self.dz * rhs.dx - self.dx * rhs.dz,
                      self.dx * rhs.dy - self.dy * rhs.dx)
    
    def __abs__(self):
        import math
        return math.sqrt(self @ self)

N = Vector(0, -1)
S = Vector(0, 1)
E = Vector(1, 0)
W = Vector(-1, 0)

NW = N + W
NE = N + E
SW = S + W
SE = S + E

Directions = [N, NW, W, SW, S, SE, E, NE]


class Day04:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day04')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.grid = set()

        for row, line in enumerate(self.lines):
            for col, char in enumerate(line):
                if char == '@':
                    self.grid.add(Point(row, col))

    def FindMovableRolls(self):
        rolls = set()
        for p in self.grid:
            n = sum(1
                    for direction in Directions
                    if p + direction in self.grid)
            if n < 4:
                rolls.add(p)
        return rolls

    def Part1(self):
        return len(self.FindMovableRolls())
        

    def Part2(self):
        answer = 0
        while rolls := self.FindMovableRolls():
            answer += len(rolls)
            self.grid.difference_update(rolls)

        return answer
    
if __name__ == '__main__':
    problem = Day04()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



