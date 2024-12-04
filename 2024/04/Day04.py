#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import numpy as np

class Day04:
    def __init__(self):
        self.input = None

        self.content = None
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
            self.contents = input.read().strip()
        self.lines = self.contents.split('\n')

        ########################################################################
        # If the puzzle is not grid/map based, delete these lines.
        gridKey = {'X': 1, 'M': 2, 'A': 3, 'S':4}
        self.height = len(self.lines)
        self.width = len(self.lines[0])

        self.grid = np.zeros((self.height, self.width), dtype=int)
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                self.grid[row, col] = gridKey.get(ch, 0)
        #
        ########################################################################


    # Horizontal test
    def test1(self, grid):
        count = 0
        for r in range(self.height):
            for c in range(self.width - 3):
                if list(grid[r, c:c+4]) == [1, 2, 3, 4]:
                    count += 1
        return count

    # Diagonal test
    def test2(self, grid):
        count = 0
        for r in range(self.height):
            for c in range(self.width - 3):
                if list(grid[r:r+4, c:c+4].diagonal()) == [1, 2, 3, 4]:
                    count += 1
        return count

    def Part1(self):
        answer = 0

        view = self.grid
        answer += self.test1(self.grid)
        answer += self.test1(self.grid[:, ::-1])
        answer += self.test1(self.grid.T)
        answer += self.test1(self.grid.T[:, ::-1])
        answer += self.test2(self.grid)
        answer += self.test2(self.grid[:, ::-1])
        answer += self.test2(self.grid[::-1, :])
        answer += self.test2(self.grid.T[::-1, ::-1])
        return answer

    def test3(self, grid):
        count = 0
        return count
        
    def Part2(self):
        answer = 0
        for r in range(self.height-2):
            for c in range(self.width - 2):
                check = self.grid[r:r+3, c:c+3]
                if (list(check.diagonal()) in ([2, 3, 4], [4, 3, 2]) and
                    list(check[:,::-1].diagonal()) in ([2, 3, 4], [4, 3, 2])):
                    answer += 1
        return answer
    
if __name__ == '__main__':
    problem = Day04()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



