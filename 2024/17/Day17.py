#!/usr/bin/env python3
"""
<Problem description here>
"""

A, B, C = 0, 1, 2
ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV = tuple(range(8))

class Day17:
    def __init__(self):
        self.input = None

        self.lines = []

        self.reg = [0, 0, 0]
        self.output = []

        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day17')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()

        self.lines = self.contents.split('\n')

        for line in self.lines:
            if line.startswith('Register '):
                reg = line[9]
                val = int(line[11:])
                r = ord(reg) - ord('A')
                self.reg[ord(reg) - ord('A')] = val
            elif line.startswith('Program: '):
                self.code = list(map(int, line.replace('Program: ', '').split(',')))

    def combo(self, op):
        if 0 <= op <= 3:
            return op
        elif 4 <= op <=6:
            return self.reg[op - 4]
        else:
            assert False, f"Illegal combo operand {op=}"

    def adv(self, op):
        val = self.combo(op)
        self.reg[A] = int(self.reg[A] / (2**val))

    def bxl(self, op):
        self.reg[B] ^= op

    def bst(self, op):
        self.reg[B] = self.combo(op) % 8

    def jnz(self, op):
        if self.reg[A]:
            return op

    def bxc(self, op):
        self.reg[B] ^= self.reg[C]

    def out(self, op):
        val = self.combo(op) % 8
        self.output.append(val)
        if self.output != self.code[:len(self.output)]:
            self.fail = True

    def bdv(self, op):
        val = self.combo(op)
        self.reg[B] = int(self.reg[A] / (2**val))

    def cdv(self, op):
        val = self.combo(op)
        self.reg[C] = int(self.reg[A] / (2**val))

    def Part1(self):
        funcs = [self.adv, self.bxl, self.bst, self.jnz,
                 self.bxc, self.out, self.bdv, self.cdv]

        ip = 0
        while ip < len(self.code):
            inst, op = self.code[ip:ip+2]

            result = funcs[inst](op)
            ip = ip + 2 if result is None else result

        answer = ','.join(map(str, self.output))

        return answer

    def Part2(self):
        # We want to set a value in A so that the output matches the code.
        #
        # After some examination of the instructions, they are all bit
        # twiddling functions. Effectively:
        #
        #   0: a >>= op
        #   1: b ^= op
        #   2: b = a & 7
        #   3: while a
        #   4: b ^= c
        #   5: output b & 7
        #   6: b = a >> op
        #   7: c = a >> op
        #
        # The actual instructions in my code input expand to:
        #
        #     while a:
        #         b = a & 7
        #         b ^= 2
        #         c = a >> b
        #         b ^= 7
        #         b ^= c
        #         a >>= 3
        #         output.append(b & 7)
        #
        # The only instruction that modifies A shifts off 3 bits
        # each time. C is a shifted version of A that gets xor-ed
        # into B, but C is shifted by 0 to 7 bits. So only the
        # bottom 10 bits of A can affect the value of each output
        # value. But the bits overlap with the next value.
        #
        #       3322222222221111111111
        #       10987654321098765432109876543210
        #                             |------+-|    output[0]
        #                          |------+-|       output[1]
        #                       |------+-|          output[2]
        #                    |------+-|             output[3]
        #
        # The low bits output the first values. Let's see if we
        # can generate them in sequence.
        #
        answer = 0

        shift = -3
        candidates = set([0])
        prevCandidates = set()
        outputs = 0
        while outputs < len(self.code):
            prevCandidates = candidates
            candidates = set()
            outputs += 1
            shift += 3
            for base in prevCandidates:
                # Run through all 10-bit values looking for inputs that produce
                # an appropriate prefix of the code.
                for n in range(1024):
                    a = base + (n << shift)

                    for j in range(outputs):
                        # XXX: I could "run the program" here but I'd already
                        # hard-coded it for testing/debugging so it's still here.
                        b = (a & 7)
                        b ^= 2
                        c = a >> b
                        b ^= 7
                        b ^= (c & 7)  # Masked to keep unused bits out of b

                        if b != self.code[j]:
                            # Nope, wrong output byte
                            break

                        a >>= 3
                    else:
                        # This value of register a is a candidate.
                        candidates.add(base + (n << shift))

        answer = min(candidates)

        return answer

if __name__ == '__main__':
    problem = Day17()

    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



