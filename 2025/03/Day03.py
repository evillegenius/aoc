#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re
import numpy as np

class Day03:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day03')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

    def Part1(self):
        answer = 0
        for n, line in enumerate(self.lines):
            d1 = max(line[:-1])
            line = line[line.index(d1) + 1:]
            d2 = max(line)

            joltage = int(d1 + d2)
            # print(f":{n:4}: {self.lines[n]}: {joltage}")
            answer += joltage

        return answer

    def Part2(self):
        answer = 0
        for n, line in enumerate(self.lines):
            line += ' '   # pad because line[:-0] does not work
            joltage = ''
            for i in range(12, 0, -1):
                digit = max(line[:-i])
                joltage += digit
                line = line[line.index(digit)+1:]
                if len(joltage) == 12:
                    break
            # print(f"{n:4}: {self.lines[n]}: {joltage}")
            answer += int(joltage)

        return answer
    
if __name__ == '__main__':
    problem = Day03()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



