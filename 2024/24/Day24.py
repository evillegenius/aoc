#!/usr/bin/env python3
"""
<Problem description here>
"""
import re

class Day24:
    def __init__(self):
        self.input = None

        self.lines = []
        self.grid = None

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day24')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()

        self.lines = self.contents.split('\n')

        separator = self.lines.index('')

        self.initLines = self.lines[:separator]
        self.gateLines = self.lines[separator+1:]

        initPat = re.compile(r'^([^:]*): ([01])$')
        gatePat = re.compile(r'^(\w+) (AND|OR|XOR) (\w+) -> (\w+)$')

        self.initial = {}
        self.wires = {}
        self.ops = []
        for line in self.initLines:
            if match := initPat.match(line):
                self.initial[match[1]] = int(match[2])
            else:
                print(f"Bad line in input: {line=}")

        for line in self.gateLines:
            if match := gatePat.match(line):
                self.ops.append(list(match.groups()))
                self.wires[match[1]] = None
                self.wires[match[3]] = None
                self.wires[match[4]] = None

        ##############################################################
        # Hacking in part2 for testing purposes. This breaks the part1
        # answer. Comment this out for part1
        self.swaps = dict(qnw='z15', z15='qnw',
                          cqr='z20', z20='cqr',
                          nfj='ncd', ncd='nfj',
                          z37='vkg', vkg='z37')

        for op in self.ops:
            op[3] = self.swaps.get(op[3], op[3])
        #
        ##############################################################

        self.wires.update(self.initial)
        self.depends = {op[3]: op for op in self.ops}

        self.ancestors = {}
        def findAncestors(wire):
            if wire not in self.ancestors:
                if wire not in self.depends:
                    return set()
                op = self.depends[wire]
                self.ancestors[wire] = findAncestors(op[0]) | findAncestors(op[2])
                self.ancestors[wire].update(op[::2])

            return self.ancestors[wire]

        for wire in self.wires:
            findAncestors(wire)

    def Eval(self, wire):
        if self.wires[wire] is None:
            op = self.depends[wire]
            if op[1] == 'AND':
                self.wires[wire] = self.Eval(op[0]) and self.Eval(op[2])
            elif op[1] == 'OR':
                self.wires[wire] = self.Eval(op[0]) or self.Eval(op[2])
            elif op[1] == 'XOR':
                self.wires[wire] = self.Eval(op[0]) ^ self.Eval(op[2])
            else:
                assert False

        return self.wires[wire]

    def Part1(self):
        answer = 0
        outputs = sorted((wire for wire in self.wires if wire.startswith('z')), reverse=True)

        for output in outputs:
            if self.wires[output] is None:
                self.wires[output] = self.Eval(output)

        answer = int(''.join(map(str, (self.wires[output] for output in outputs))), 2)
        return answer

    def Eval2(self, x, y, wires=None):
        if wires is None:
            wires = dict.fromkeys(self.wires, None)

        for bit, wire in enumerate(self.xWires):
            wires[wire] = 1 if (x & (1 << bit)) else 0

        for bit, wire in enumerate(self.yWires):
            wires[wire] = 1 if (y & (1 << bit)) else 0

        def _eval(wire):
            if wires[wire] is None:
                op = self.depends[wire]
                if op[1] == 'AND':
                    wires[wire] = _eval(op[0]) and _eval(op[2])
                elif op[1] == 'OR':
                    wires[wire] = _eval(op[0]) or _eval(op[2])
                elif op[1] == 'XOR':
                    wires[wire] = _eval(op[0]) ^ _eval(op[2])
                else:
                    assert False
            return wires[wire]

        z = 0
        for bit, wire in enumerate(self.zWires):
            if _eval(wire):
                z |= 1 << bit

        return z

    def Part2(self):
        answer = 0

        self.xWires = sorted(wire for wire in self.wires if wire.startswith('x'))
        self.yWires = sorted(wire for wire in self.wires if wire.startswith('y'))
        self.zWires = sorted(wire for wire in self.wires if wire.startswith('z'))

        xBits = len(self.xWires)
        yBits = len(self.yWires)
        zBits = len(self.zWires)

        assert xBits == yBits and xBits <= zBits

        # Try a few numbers to see if we can figure out the bits that are bad.
        def test(x, y, wires=None):
            if wires is None:
                wires = dict.fromkeys(self.wires, None)
            x = x & ((1 << xBits) - 1)
            y = y & ((1 << yBits) - 1)

            # It appears that z does not have an extra bit in the input file,
            # so mask the result.
            z = (x + y) & ((1 << zBits) - 1)

            result = self.Eval2(x, y, wires)

            error = result ^ z
            badBits = set((wire for bit, wire in enumerate(self.zWires) if (1 << bit) & error))

            return badBits

        badBits = test(0, 0)
        # See which bits are occasionally bad
        for bit in range(xBits):
            badBits.update(test(1<<bit, 0))
            badBits.update(test(0, 1<<bit))
            badBits.update(test(1<<bit, 1<<bit))

        if badBits:
            print('The following bits are bad:')
            for bb in sorted(badBits):
                print(f'  {bb}')
        else:
            answer = ','.join(sorted(self.swaps))

        return answer

if __name__ == '__main__':
    problem = Day24()

    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



