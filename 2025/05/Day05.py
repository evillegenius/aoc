#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re
import numpy as np

class Day05:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day05')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

    def Part1(self):
        answer = 0
        self.fresh = []
        linesIter = iter(self.lines)

        while line := next(linesIter):
            low, _, high = line.partition('-')
            self.fresh.append([int(low), int(high)])

        self.fresh.sort()

        for line in linesIter:
            id = int(line)
            for low, high in self.fresh:
                if high < id:
                    continue
                if low <= id <= high:
                    answer += 1
                    break
                if low > id:
                    break
        
        return answer

    def Part2(self):
        answer = 0

        while True:
            for i in range(len(self.fresh) - 1):
                if self.fresh[i][1] >= self.fresh[i+1][0]:
                    self.fresh[i] = (self.fresh[i][0],
                                     max(self.fresh[i][1], self.fresh[i+1][1]))
                    del self.fresh[i+1]
                    break
            else:
                break

        for low, high in self.fresh:
            answer += (high - low) + 1

        return answer
    
if __name__ == '__main__':
    problem = Day05()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



