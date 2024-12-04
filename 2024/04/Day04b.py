#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re

class Day04b:
    def __init__(self):
        self.input = None

        self.content = None
        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day04b')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()
        self.lines = self.contents.split('\n')

        self.height = len(self.lines)
        self.width = len(self.lines[0])

    def countoverlapping(self, pattern, text):
        count = 0
        start = 0
        while match := pattern.search(text, start):
            count += 1
            start = match.start() + 1

        return count

    def Part1(self):
        answer = 0

        horiz = re.compile(r'XMAS|SAMX')
        wrap = '.' * (self.width-1)
        diag1 = re.compile(rf'X{wrap}M{wrap}A{wrap}S|S{wrap}A{wrap}M{wrap}X'
                           , re.DOTALL)
        wrap += '.'
        vertical = re.compile(rf'X{wrap}M{wrap}A{wrap}S|S{wrap}A{wrap}M{wrap}X',
                              re.DOTALL)
        wrap += '.'
        diag2 = re.compile(rf'X{wrap}M{wrap}A{wrap}S|S{wrap}A{wrap}M{wrap}X',
                           re.DOTALL)

        answer = (self.countoverlapping(horiz, self.contents) +
                  self.countoverlapping(diag1, self.contents) +
                  self.countoverlapping(vertical, self.contents) +
                  self.countoverlapping(diag2, self.contents))

        return answer

    def Part2(self):
        answer = 0

        wrap = '.' * (self.width - 2)
        xmas = re.compile(rf'(M.M{wrap}.A.{wrap}S.S)|'
                          rf'(M.S{wrap}.A.{wrap}M.S)|'
                          rf'(S.S{wrap}.A.{wrap}M.M)|'
                          rf'(S.M{wrap}.A.{wrap}S.M)', re.DOTALL)

        answer = self.countoverlapping(xmas, self.contents)

        return answer
    
if __name__ == '__main__':
    problem = Day04b()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



