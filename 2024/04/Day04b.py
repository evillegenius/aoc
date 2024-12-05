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

    def countMatches(self, pattern, text):
        """pattern.findall does not find all patterns because they overlap in the
        linear string that it's searching. So this finds each one and then starts
        searching again one character past the start rather than one past the end
        of the previous match.
        """
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
        wrap = '.' * self.width
        vertical = re.compile(rf'X{wrap}M{wrap}A{wrap}S|S{wrap}A{wrap}M{wrap}X',
                              re.DOTALL)
        wrap = '.' * (self.width + 1)
        diag2 = re.compile(rf'X{wrap}M{wrap}A{wrap}S|S{wrap}A{wrap}M{wrap}X',
                           re.DOTALL)

        answer = (self.countMatches(horiz, self.contents) +
                  self.countMatches(diag1, self.contents) +
                  self.countMatches(vertical, self.contents) +
                  self.countMatches(diag2, self.contents))

        return answer

    def Part2(self):
        answer = 0

        # Wrap size is self.width + (1 for the /n) - (3 for the characters
        # already matched)
        wrap = '.' * (self.width - 2)
        xmas = re.compile(rf'(M.M{wrap}.A.{wrap}S.S)|'
                          rf'(M.S{wrap}.A.{wrap}M.S)|'
                          rf'(S.S{wrap}.A.{wrap}M.M)|'
                          rf'(S.M{wrap}.A.{wrap}S.M)', re.DOTALL)

        answer = self.countMatches(xmas, self.contents)

        return answer
    
if __name__ == '__main__':
    problem = Day04b()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



