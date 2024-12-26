#!/usr/bin/env python3
"""
<Problem description here>
"""
from collections import Counter

class Day22:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None
        self.seq = {}

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day22')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.seeds = list(map(int, self.lines))

    def prng(self, state):
        state ^= state << 6
        state &= 16777215
        state ^= state >> 5
        state &= 16777215
        state ^= state << 11
        state &= 16777215

        return state

    def Part1(self):
        answer = 0
        for seed in self.seeds:
            self.seq[seed] = [seed]
            state = seed
            for _ in range(2000):
                state = self.prng(state)
                # Save sequences for part 2
                self.seq[seed].append(state)

            # print(f'{seed}: {state}')

            answer += state
        return answer

    def Part2(self):
        bananas = Counter()
        answer = 0
        for seed, seq in self.seq.items():
            prices = tuple(map(lambda x: x % 10, seq))
            diffs = tuple(prices[i] - prices[i-1] for i in range(1, 2000))
            offers = {}
            for i in range(1, 1996):
                key = diffs[i:i+4]
                offers.setdefault(key, prices[i+4])
                offers.setdefault
            bananas.update(offers)

        best = bananas.most_common(5)
        answer = best[0][1]
        return answer

if __name__ == '__main__':
    problem = Day22()

    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



