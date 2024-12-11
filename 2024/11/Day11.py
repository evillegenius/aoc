#!/usr/bin/env python3
"""
<Problem description here>
"""
import functools

class Day11:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day11')
        parser.add_argument('-b', '--blinks', type=int, default=25)
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()

        self.lines = self.contents.split('\n')

        self.stones = map(int, self.lines[0].split())

    @functools.cache
    def Blink(self, stone, n):
        if n == 0:
            # print(stone)
            return 1
        
        if stone == 0:
            return self.Blink(1, n - 1)
        elif len(str(stone)) % 2 == 0:
            text = str(stone)
            stone1 = int(text[:len(text) // 2])
            stone2 = int(text[len(text) // 2:])
            return self.Blink(stone1, n - 1) + self.Blink(stone2, n - 1)
        else:
            return self.Blink(stone * 2024, n - 1)
        
    def Part1(self):
        answer = 0
        for stone in self.stones:
            answer += self.Blink(stone, self.blinks)
        return answer

    def Part2(self):
        answer = 0
        return answer
    
if __name__ == '__main__':
    problem = Day11()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



