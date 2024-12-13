#!/usr/bin/env python3
"""
<Problem description here>
"""
import re

class Day13:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()
        self.buttonPat = re.compile(r'Button ([AB]): X\+(\d+), Y\+(\d+)$')
        self.prizePat = re.compile(r'Prize: X=(\d+), Y=(\d+)$')

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day13')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()

        self.lines = self.contents.split('\n')

    def Solve(self, offset):
        answer = 0
        ax = ay = bx = by = px = py = 0
        for line in self.lines:
            if match := self.buttonPat.match(line):
                button, x, y = match.groups()
                x, y = int(x), int(y)
                if button == 'A':
                    ax, ay = x, y
                else:
                    bx, by = x, y
            elif match := self.prizePat.match(line):
                px, py = list(map(int, match.groups()))
                px += offset
                py += offset
                aNum = (by * px - bx * py)
                aDen = (by * ax - bx * ay)
                bNum = (ay * px - ax * py)
                bDen = (ay * bx - ax * by)
                if aNum % aDen == 0 and bNum % bDen == 0:
                    a = aNum // aDen
                    b = bNum // bDen
                    cost = 3 * a + b
                    answer += cost

        return answer
    
    def Part1(self):
        return self.Solve(0)
    
    def Part2(self):
        return self.Solve(10000000000000)
    
if __name__ == '__main__':
    problem = Day13()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



