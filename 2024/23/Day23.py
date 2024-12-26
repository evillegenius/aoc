#!/usr/bin/env python3
"""
<Problem description here>
"""

class Day23:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day23')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')


    def Part1(self):
        answer = 0
        self.netmap = {}
        self.netset = set()
        for line in self.lines:
            a, b = line.split('-')
            self.netset.add((a, b))
            self.netset.add((b, a))
            self.netmap.setdefault(a, []).append(b)
            self.netmap.setdefault(b, []).append(a)

        for connections in self.netmap.values():
            connections.sort()

        triples = set()
        for host1, connected in self.netmap.items():
            for i, host2 in enumerate(connected):
                for j in range(i + 1, len(connected)):
                    host3 = connected[j]
                    if (host2, host3) in self.netset:
                        if host1.startswith('t') or host2.startswith('t') or host3.startswith('t'):
                            triples.add(tuple(sorted((host1, host2, host3))))

        return len(triples)


    def Part2(self):
        answer = 0
        biggestClique = set()
        for node, connections in self.netmap.items():
            clique = set([node])
            for n1 in connections:
                for n2 in clique:
                    if (n1, n2) not in self.netset:
                        break
                else:
                    clique.add(n1)

            if len(clique) > len(biggestClique):
                biggestClique = clique
        answer = ','.join(sorted(biggestClique))
        return answer

if __name__ == '__main__':
    problem = Day23()

    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



