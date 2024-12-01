#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re
import numpy as np

class Day01:
    def __init__(self):
        self.input = None

        self.lines = []
        self.a = []
        self.b = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day01')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        for line in self.lines:
            itemA, itemB = line.split()
            self.a.append(int(itemA))
            self.b.append(int(itemB))

    def Part1(self):
        self.a.sort()
        self.b.sort()

        answer = sum(abs(itemA - itemB) for itemA, itemB in zip(self.a, self.b))
        return answer

    def Part2(self):
        answer = sum(itemA * self.b.count(itemA) for itemA in self.a)
        return answer
    
if __name__ == '__main__':
    problem = Day01()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



