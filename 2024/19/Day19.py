#!/usr/bin/env python3
"""
<Problem description here>
"""
import functools

class Day19:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day19')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()

        self.lines = self.contents.split('\n')

        self.towels = set(self.lines[0].split(', '))

        self.patterns = self.lines[2:]

    @functools.cache
    def test(self, pattern):
        if not pattern:
            return True
        for end in range(1, len(pattern)+1):
            if pattern[:end] in self.towels:
                if self.test(pattern[end:]):
                    return True

        return False

    def Part1(self):
        answer = 0

        for pattern in self.patterns:
            if self.test(pattern):
                answer += 1

        return answer

    @functools.cache
    def test2(self, pattern):
        if not pattern:
            return 1
        count = 0
        for end in range(1, len(pattern)+1):
            if pattern[:end] in self.towels:
                count += self.test2(pattern[end:])

        return count

    def Part2(self):
        answer = 0

        for pattern in self.patterns:
            answer += self.test2(pattern)

        return answer

if __name__ == '__main__':
    problem = Day19()

    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')
