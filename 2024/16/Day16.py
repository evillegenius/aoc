#!/usr/bin/env python3
"""
<Problem description here>
"""

"""
P and V (point and vector) classes intended to be used with numpy grids. As such
the origin is in the upper left corner, coordinates are (row, col), and row increases
downward.
"""

import math
import heapq
from typing import NamedTuple

class P(NamedTuple):
    """
    Point in a numpy grid.
    """
    row: 'int'
    col: 'int'

    def __add__(self, v: 'V'):
        return P(self.row + v.dr, self.col + v.dc)

    def __sub__(self, rhs: 'P|V'):
        if isinstance(rhs, P):
            return V(self.row - rhs.row, self.col - rhs.col)
        else:
            return P(self.row - rhs.dr, self.col - rhs.dc)

    def __mod__(self, v: 'V'):
        """Modulo operator, good for wrapping around into bounds"""
        return P(self.row % v.dr, self.col % v.dc)

    def __str__(self):
        return f'P({self.row}, {self.col})'

class V(NamedTuple):
    """
    A vector in a numpy grid.
    """
    dr: 'int'
    dc: 'int'

    def __add__(self, rhs: 'V|P'):
        if isinstance(rhs, P):
            return P(self.dr + rhs.row, self.dc + rhs.col)
        else:
            return V(self.dr + rhs.dr, self.dc + rhs.dc)

    def __sub__(self, v: 'V'):
        return V(self.dr - v.rd, self.dc - v.dc)

    def __mul__(self, rhs: 'int|V'):
        """Scalar multiplication or dot product"""
        if isinstance(rhs, V):
            return self.dr * rhs.dr + self.dc * rhs.dc

        return V(self.dr * rhs, self.dc * rhs)

    def __rmul__(self, lhs: 'int'):
        return V(lhs * self.dr, lhs * self.dc)

    def __floordiv__(self, x: int):
        return V(self.dr // x, self.dr // x)

    def __neg__(self):
        return V(-self.dy, -self.dx)

    def __xor__(self, v: 'V'):
        """Cross product"""
        return self.dr * v.dr + self.dc * v.dc

    def __abs__(self):
        """Return the vector's magnitude or length"""
        return math.sqrt(self.dr * self.dr + self.dc * self.dc)

    def Right(self):
        return V(self.dc, -self.dr)

    def Left(self):
        return V(-self.dc, self.dr)

directions = [V(0, 1), V(0, -1), V(1, 0), V(-1, 0)]

class Day16:
    def __init__(self):
        self.input = None

        self.lines = []
        self.floor = set()
        self.startPos = None
        self.goalPos = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day16')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.lines = input.read().strip().split('\n')

        self.width = len(self.lines[0])
        self.height = len(self.lines)

        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                if ch in ".SE":
                    self.floor.add(P(row, col))

                if ch == 'S':
                    self.startPos = P(row, col)
                    self.startDir = V(0, 1)
                elif ch == 'E':
                    self.goalPos = P(row, col)

    def Part1(self):
        answer = 0
        
        q = set(self.floor)
        entry = [0, self.startPos, self.startDir]
        heap = [entry]
        heapIndex = dict()
        heapIndex[self.startPos, self.startDir] = entry
        dist = {}
        dist[self.startPos] = 0
        prev = {}

        while heap:
            _, pos, dir = heapq.heappop(heap)
            q.discard(pos)

            for d in directions:
                neighbor = pos + d
                if neighbor in q:
                    cost = 1 if d == dir else 1001
                    tmpDist = dist[pos] + cost
                    if tmpDist < dist.get(neighbor, math.inf):
                        prev[neighbor] = pos
                        dist[neighbor] = tmpDist
                        if (neighbor, d) in heapIndex:
                            heapIndex[neighbor, d][0] = tmpDist
                            heapq.heapify(heap)
                        else:
                            entry = [tmpDist, neighbor, d]
                            heapq.heappush(heap, entry)
                            heapIndex[neighbor, d] = entry

        self.answer1 = dist[self.goalPos]
        return self.answer1

    def Part2(self):
        answer = 0
        # a "state" is a position velocity pair
        startState = self.startPos, self.startDir
        q = set()
        for pos in self.floor:
            for d in directions:
                q.add((pos, d))
        entry = [0, startState]
        heap = [entry]
        heapIndex = dict()
        heapIndex[startState] = entry
        dist = {}
        dist[startState] = 0
        prev = {}

        while heap:
            _, state = heapq.heappop(heap)
            q.discard(state)
            heapIndex.pop(state)

            pos, dir = state
            # Possible neighbors are one stpe forward or turn in place
            neighbors  = [((pos + dir, dir), 1)]
            neighbors += [((pos, d), 1000) for d in directions]

            for nState, nCost in neighbors:
                if nState in q:
                    tmpDist = dist[state] + nCost
                    if tmpDist < dist.get(nState, math.inf):
                        prev[nState] = state
                        dist[nState] = tmpDist
                        if nState in heapIndex:
                            heapIndex[nState][0] = tmpDist
                            heapq.heapify(heap)
                        else:
                            entry = [tmpDist, nState]
                            heapq.heappush(heap, entry)
                            heapIndex[nState] = entry

        answers = [(dist.get((self.goalPos, d), math.inf), (self.goalPos, d))
                   for d in directions]
        
        bestScore, bestState = min(answers)

        # Scan backwards through the neighbors to find all of the states that
        # could have contributed to a final answer.

        visited = set()
        todo = set([bestState])

        while todo:
            state = todo.pop()
            if state in visited:
                continue
            visited.add(state)

            pos, dir = state
            # Possible neighbors are one stpe forward or turn in place
            neighbors  = [((pos - dir, dir), 1)]
            neighbors += [((pos, d), 1000) for d in directions]

            for nState, nCost in neighbors:
                if nState in dist and dist[nState] == (dist[state] - nCost):
                    # This neighbor is on a minimum path
                    todo.add(nState)

        # Count only unique positions
        visitedPos = {pos for pos, dir in visited}

        answer = len(visitedPos)

        return answer
    
if __name__ == '__main__':
    problem = Day16()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



