#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re

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

        self.mulPat = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')

        self.condPat = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|don't\(\)|do\(\)")

    def Part1(self):
        answer = 0
        for line in self.lines:
            for match in self.mulPat.finditer(line):
                answer += int(match[1]) * int(match[2])
                
        return answer

    def Part2(self):
        answer = 0
        
        doIt = True
        for line in self.lines:
            for match in self.condPat.finditer(line):
                if match[0].startswith('mul'):
                   if doIt:
                       answer += int(match[1]) * int(match[2])
                   else:
                       pass
                elif match[0] == "don't()":
                    doIt = False
                elif match[0] == "do()":
                    doIt = True
                else:
                    print(f'Pattern fail: {match[0]}')
                       
        return answer
    
if __name__ == '__main__':
    problem = Day03()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



