#!/usr/bin/env python3
"""
<Problem description here>
"""
class Day07:
    def __init__(self):
        self.input = None

        self.contents = None
        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day07')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()

        self.lines = self.contents.split('\n')


    def dfs1(self, ans, working, numbers):
        if working > ans:
            return False

        if not numbers:
            return working == ans

        w = working + numbers[0]
        if self.dfs1(ans, w, numbers[1:]):
            return True
        else:
            w = working * numbers[0]
            return self.dfs1(ans, w, numbers[1:])
        
    def Part1(self):
        answer = 0

        for line in self.lines:
            ans, numbers = line.split(':')
            ans = int(ans)
            numbers = list(map(int, numbers.split()))

            if self.dfs1(ans, numbers[0], numbers[1:]):
                answer += ans

        return answer

    def dfs2(self, ans, working, numbers):
        if working > ans:
            return False

        if not numbers:
            return working == ans

        w = working + numbers[0]
        if self.dfs2(ans, w, numbers[1:]):
            return True
        else:
            w = working * numbers[0]
            if self.dfs2(ans, w, numbers[1:]):
                return True
            else:
                w = int(f'{working}{numbers[0]}')
                return self.dfs2(ans, w, numbers[1:])
        
    def Part2(self):
        answer = 0

        for line in self.lines:
            ans, numbers = line.split(':')
            ans = int(ans)
            numbers = list(map(int, numbers.split()))

            if self.dfs2(ans, numbers[0], numbers[1:]):
                answer += ans

        return answer
    
if __name__ == '__main__':
    problem = Day07()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



