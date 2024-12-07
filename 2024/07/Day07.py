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


    def dfs1(self, ans, numbers, tmp=None):
        if not numbers:
            return tmp == ans
        
        if tmp is None:
            # First time
            t = numbers[0] + numbers[1]
            if self.dfs1(ans, numbers[2:], t):
                return True
            else:
                t = numbers[0] * numbers[1]
                return self.dfs1(ans, numbers[2:], t)
        else:
            # Not first time
            if tmp > ans:
                return False
            t = tmp + numbers[0]
            if self.dfs1(ans, numbers[1:], t):
                return True
            else:
                t = tmp * numbers[0]
                return self.dfs1(ans, numbers[1:], t)
        
    def Part1(self):
        answer = 0

        for line in self.lines:
            ans, numbers = line.split(':')
            ans = int(ans)
            numbers = list(map(int, numbers.split()))

            if self.dfs1(ans, numbers):
                answer += ans

        return answer

    def dfs2(self, ans, numbers, tmp=None):
        if not numbers:
            return tmp == ans
        
        if tmp is None:
            # First time
            t = numbers[0] + numbers[1]
            if self.dfs2(ans, numbers[2:], t):
                return True
            else:
                t = numbers[0] * numbers[1]
                if self.dfs2(ans, numbers[2:], t):
                    return True
                else:
                    t = int(f'{numbers[0]}{numbers[1]}')
                    return self.dfs2(ans, numbers[2:], t)
            
        else:
            # Not the first time
            if tmp > ans:
                return False
            t = tmp + numbers[0]
            if self.dfs2(ans, numbers[1:], t):
                return True
            else:
                t = tmp * numbers[0]
                if self.dfs2(ans, numbers[1:], t):
                    return True
                else:
                    t = int(f'{tmp}{numbers[0]}')
                    return self.dfs2(ans, numbers[1:], t)
        
    def Part2(self):
        answer = 0

        for line in self.lines:
            ans, numbers = line.split(':')
            ans = int(ans)
            numbers = list(map(int, numbers.split()))

            if self.dfs2(ans, numbers):
                answer += ans

        return answer
    
if __name__ == '__main__':
    problem = Day07()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



