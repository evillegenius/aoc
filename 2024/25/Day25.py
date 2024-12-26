#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re
import numpy as np

class Day25:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day25')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.keys = []
        self.locks = []

        i = 0
        dest = None
        for i in range(0, len(self.lines), 8):
            if self.lines[i] == '#####':
                dest = self.locks
            elif self.lines[i] == '.....':
                dest = self.keys
            else:
                assert False

            pattern = [0, 0, 0, 0, 0]
            for line in self.lines[i+1:i+6]:
                for i, ch in enumerate(line):
                    if ch == '#':
                        pattern[i] += 1

            dest.append(pattern)

    def Part1(self):
        answer = 0
        for lock in self.locks:
            for key in self.keys:
                if max(map(sum, zip(lock, key))) <= 5:
                    answer += 1
        return answer

    def Part2(self):
        answer = "n/a"
        return answer

if __name__ == '__main__':
    problem = Day25()

    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



