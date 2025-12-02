#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re

class Day02:
    def __init__(self):
        self.input = None

        self.pairs = []
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day02')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            contents = input.read().strip().split(',')

        for item in contents:
            beg, _, end = item.partition('-')
            assert _ == '-'
            self.pairs.append((int(beg), int(end)))

    def Part1(self):
        answer = 0
        doublePat = re.compile(r'^(.*?)\1$')
        for beg, end in self.pairs:
            for id in range(beg, end+1):
                if doublePat.match(str(id)):
                    answer += id
                    # print(id)
            
        return answer

    def Part2(self):
        answer = 0
        repeatPat = re.compile(r'^(.*?)(\1)+$')
        for beg, end in self.pairs:
            for id in range(beg, end+1):
                if repeatPat.match(str(id)):
                    answer += id
                    # print(id)
            
        return answer
    
if __name__ == '__main__':
    problem = Day02()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



