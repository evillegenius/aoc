import re

class InputToDot:
    def __init__(self):
        self.wires = set()
        self.ops = list()

        self.opPat = re.compile(r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)$')

        self.ParseInput()

    def ParseInput(self):
        import sys
        inputName = sys.argv[1] if len(sys.argv) > 1 else "input"
        with open(inputName) as input:
            lines = input.read().strip().split('\n')

        gateCount = 0

        for line in lines:
            if match := self.opPat.match(line):
                self.wires.update((match[1], match[3], match[4]))
                self.ops.append(match.groups())

    def Run(self):
        print('digraph {')
        print('  rankdir = "LR"')

        xWires = sorted(w for w in self.wires if w.startswith('x'))
        yWires = sorted(w for w in self.wires if w.startswith('y'))
        zWires = sorted(w for w in self.wires if w.startswith('z'))
        otherWires = sorted(self.wires.difference(xWires + yWires + zWires))

        # Start with the x and y wires and end with z
        for x, y in zip(xWires, yWires):
            print(f'  {x} [shape=none]')
            print(f'  {y} [shape=none]')

        for w in otherWires:
            print(f'  {w} [shape=circle]')

        for z in zWires:
            print(f'  {z} [shape=none]')

        # Order by gate type
        self.ops.sort(reverse=True, key=lambda op: (op[1],op[3]))

        for i, op in enumerate(self.ops):
            gate = f'gate{i:03}'
            print(f'  {gate} [shape=box, label="{op[1]}"]')
            print(f'  {{ {op[0]} {op[2]} }} -> {gate} -> {op[3]}')

        print('}')
        
InputToDot().Run()