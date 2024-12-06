#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import functools

class Day05:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day05')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()

        self.lines = self.contents.split('\n')

        self.rules = set()
        self.updates = []
        foundBlank = False
        for line in self.lines:
            if not line:
                foundBlank = True
            elif foundBlank:
                self.updates.append(list(map(int, line.split(','))))
            else:
                self.rules.add(tuple(map(int, line.split('|'))))

    def Part1(self):
        answer = 0
        for update in self.updates:
            good = False
            for before, after in self.rules:
                if before in update and after in update:
                    if update.index(before) > update.index(after):
                        break
            else:
                good = True

            if good:
                answer += update[len(update)//2]
                
        return answer

    def Part2(self):
        answer = 0
        answer = 0
        for update in self.updates:
            good = False
            for before, after in self.rules:
                if before in update and after in update:
                    if update.index(before) > update.index(after):
                        break
            else:
                # Made it to the end, this one is good.
                continue

            # Ok, this one needs to be reordered.
            order = lambda a, b: -1 if (a, b) in self.rules else +1
            key = functools.cmp_to_key(order)

            update.sort(key=key)
            answer += update[len(update) // 2]

        return answer

    
if __name__ == '__main__':
    problem = Day05()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



