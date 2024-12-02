#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys

class Day02:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day02')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.vals = [list(map(int, line.split())) for line in self.lines]

    def test(self, row):
        diffs = [row[i+1] - row[i] for i in range(len(row) - 1)]
        small = min(diffs)
        big = max(diffs)

        if small * big < 0:
            # different sign
            return 0

        if 1 <= small <= big <= 3 or -3 <= small <= big <= -1:
            return 1

        return 0

    def Part1(self):
        answer = 0

        for row in self.vals:
            answer += self.test(row)

        return answer

    def Part2(self):
        answer = 0
        for row in self.vals:
            if self.test(row):
                answer += 1
                continue

            # The row is fine if it succeeds with any single item removed.  Just
            # try each possible removal until it succeeds or we've tried them
            # all
            for i in range(len(row)):
                if self.test(row[:i] + row[i+1:]):
                    answer +=1
                    break
        return answer
    
if __name__ == '__main__':
    problem = Day02()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



