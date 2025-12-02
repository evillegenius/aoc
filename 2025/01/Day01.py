#!/usr/bin/env python3x1
"""
<Problem description here>
"""
import sys
import re
import itertools

class Day01:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
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


    def Part1(self):
        answer = 0
        nums = [50] + [int(line.replace('R', '+').replace('L', '-'))
                for line in self.lines]
        acc = itertools.accumulate(nums)
        ptr = [num % 100 for num in acc]
        answer = ptr.count(0)
        return answer

    def Part2(self):
        answer = 0
        nums = [int(line.replace('R', '+').replace('L', '-'))
                for line in self.lines]
        prev = 50
        for num in nums:
            next = prev + num
            if next > prev:
                zeroes = next // 100
            else:
                zeroes = -(next // 100)
                if prev == 0: zeroes -= 1
                if next % 100 == 0: zeroes += 1
            answer += zeroes
            print(f"{prev = }, {next = }, {zeroes = }, {answer = }")
            prev = next % 100
        return answer
    
if __name__ == '__main__':
    problem = Day01()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



