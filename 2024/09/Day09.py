#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import re
import numpy as np

class Day09:
    def __init__(self):
        self.input = None

        self.contents = None
        self.files = []

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day09')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()
        self.files = []
        for i in range(0, len(self.contents), 2):
            codes = self.contents[i:i+2] + "0"
            self.files.append([i // 2, int(codes[0]), int(codes[1])])


    def Part1(self):
        answer = 0
        files = [[id, used, empty] for id, used, empty in self.files]
        totalUsed = sum(used for _, used, _ in files)
        blocks = [-1] * totalUsed
        i, j = 0, len(files) - 1
        b = 0
        jId, jUsed, jEmpty = files[j]
        while i < j:
            iId, iUsed, iEmpty = files[i]
            blocks[b:b+iUsed] = [iId] * iUsed
            b += iUsed
            while iEmpty > 0:
                if iEmpty >= jUsed:
                    blocks[b:b+jUsed] = [jId] * jUsed
                    b += jUsed
                    iEmpty -= jUsed
                    files[j] = [0, 0, jEmpty + jUsed]
                    j -= 1
                    jId, jUsed, jEmpty = files[j]
                else:
                    blocks[b:b+iEmpty] = [jId] * iEmpty
                    b += iEmpty
                    jUsed -= iEmpty
                    files[j] = [jId, jUsed, jEmpty + iEmpty]
                    iEmpty = 0
            i += 1
        b = len(blocks) - 1
        while blocks[b] == -1:
            blocks[b] = jId
            b -= 1
        for b, id in enumerate(blocks):
            answer += b * id

        return answer

    def Part2(self):
        answer = 0
        totalBlocks = sum(used + empty  for _, used, empty in self.files)
        blocks = [-1] * totalBlocks

        files = [[0, id, used, free] for id, used, free in self.files]
        index = 0
        for file in files:
            file[0] = index
            index += file[2] + file[3]

        file = self.files
        j = len(files) - 1

        while j > 0:
            jIndex, jId, jUsed, jFree = files[j]
            if jId > j:
                # Don't move a file more than once
                j -= 1
                continue
            for i in range(j):
                iIndex, iId, iUsed, iFree = files[i]
                if iFree >= jUsed:
                    files[i] = [iIndex, iId, iUsed, 0]
                    files.insert(i+1, [iIndex + iUsed, jId, jUsed, iFree - jUsed])
                    del files[j+1]
                    break
            else:
                # Could not find a match
                j -= 1

        for index, id, used, free in files:
            for b in range(index, index + used):
                answer += b * id

        return answer
    
if __name__ == '__main__':
    problem = Day09()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



