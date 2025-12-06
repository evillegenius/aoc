#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import math

class Day06:
    def __init__(self):
        self.input = None

        self.lines = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day06')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip('\n').split('\n')


    def Part1(self):
        answer = 0
        lines = [line.split() for line in self.lines]

        for column in zip(*lines):
            if column[-1] == '*':
                answer += math.prod(int(x) for x in column[:-1])
            else:
                answer += sum(int(x) for x in column[:-1])
        return answer

    def Part2(self):
        answer = 0
        cols = len(self.lines[0])
        # Assemble values column-wise

        op = None
        for c in range(cols):
            if self.lines[-1][c] != ' ':
                if op == '*':
                    answer += math.prod(operands)
                elif op == '+':
                    answer += sum(operands)
                op = self.lines[-1][c]
                operands = []

            column = ''
            for line in self.lines[:-1]:
                column += line[c]

            if not column.isspace():
                operands.append(int(column))

        if op == '*':
            answer += math.prod(operands)
        elif op == '+':
            answer += sum(operands)

        return answer
    
if __name__ == '__main__':
    problem = Day06()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



