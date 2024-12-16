#!/usr/bin/env python3
"""
<Problem description here>
"""

"""
P and V (point and vector) classes intended to be used with numpy grids. As such
the origin is in the upper left corner, coordinates are (row, col), and row increases
downward.
"""

import pprint
import math
import heapq
from typing import NamedTuple
from collections import deque

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


    def GetPath(self, prev, pos):
        path = [pos]
        for d in directions:
            if (pos, d) in prev:
                while (pos, d) in prev:
                    pos, d = prev[pos, d]
                    path.append(pos)
                break

        path.reverse()
        pprint.pprint(path)
        return path

    def AStar(self, startPos, startDir, goal):
        prev = {}
        gScore = {}
        fScore = {}
        gScore[(startPos, startDir)] = 0

        # Heuristic function is manhattan distance plus a guess at number of turns
        h = lambda pos, dir: (
            abs(pos.row - self.goalPos.row) + 
            abs(pos.col - self.goalPos.col) +
            2000 if (dir * (self.goalPos - pos) < 0) else 0)

        fScore[(startPos, startDir)] = h(startPos, startDir)

        heap = []
        heapIndex = {}

        entry = [fScore[(startPos, startDir)], startPos, startDir]
        heapIndex[(startPos, startDir)] = entry
        heapq.heappush(heap, entry)

        while heap:
            _, pos, dir = heapq.heappop(heap)
            heapIndex.pop((pos, dir), None)
            if pos == goal:
                self.path1 = self.GetPath(prev, pos)
                return gScore[(pos, dir)]
            
            for d in directions:
                neighbor = pos + d
                if neighbor in self.floor:
                    cost = 1 if d == dir else 1001
                    gTmp = gScore[(pos, dir)] + cost
                    if gTmp < gScore.get((neighbor, d), math.inf):
                        gScore[(neighbor, d)] = gTmp
                        prev[(neighbor, d)] = (pos, dir)
                        fTmp = fScore[(neighbor, d)] = gTmp + h(neighbor, d)
                        if (neighbor, d) in heapIndex:
                            entry = heapIndex[(neighbor, d)]
                            if fTmp < entry[0]:
                                entry[0] = fTmp
                                heapq.heapify(heap)
                        else:
                            entry = [fTmp, neighbor, d]
                            heapIndex[(neighbor, d)] = entry
                            heapq.heappush(heap, entry)

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



        # for pos in self.floor

        # for pos in self.floor:
        #     if pos == self.startPos:
        #         q.add(pos, 0)
        #     q.add(pos, math.inf)

        # pos = self.startPos
        # dir = self.startDir
        # while q:
        #     pos, dist = q.pop()
        #     if pos == self.goalPos:
        #         return dist

        #     for d in directions:
        #         neighbor = pos + d
        #         if neighbor in q:
        #             cost = 1 if d == dir else 1001
        #             if dist + cost < q.dist(neighbor):
        #                 q.add(neighbor, dist + cost)

        
    def Recurse(self, pos, dir, score=0, visited=None):
        if visited is None:
            visited = dict()

        visited[pos, dir] = score

        for d in directions:
            neighbor = pos + d
            if neighbor in self.floor:
                cost = 1 if d == dir else 1001
                if score + cost > self.answer1:
                    continue
                if score + cost <= visited.get((neighbor, d), math.inf):
                    self.Recurse(neighbor, d, score + cost, visited)

                
    def Part2(self):
        answer = 0
        # Find all paths with score self.answer1

        return answer
    
if __name__ == '__main__':
    problem = Day16()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



