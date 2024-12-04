#include <iostream>
#include <vector>
#include <string>
#include <fstream>

class Day04
{
    public:
    Day04(const std::string& name)
    {
        std::fstream f(name);
        while (not f.eof()) {
            grid.emplace_back();
            f >> grid.back();
        }

        width = grid[0].size();
        height = grid.size();
    }

    size_t Part1()
    {
        size_t answer = 0;
        for (int r = 0; r < height; ++r) {
            for (int c = 0; c < width; ++c) {
                if (c < width - 3 &&
                    grid[r][c  ] == 'X' &&
                    grid[r][c+1] == 'M' &&
                    grid[r][c+2] == 'A' &&
                    grid[r][c+3] == 'S') answer += 1;
                if (c >= 3 &&
                    grid[r][c  ] == 'X' &&
                    grid[r][c-1] == 'M' &&
                    grid[r][c-2] == 'A' &&
                    grid[r][c-3] == 'S') answer += 1;
                if (r < height - 3 &&
                    grid[r  ][c] == 'X' &&
                    grid[r+1][c] == 'M' &&
                    grid[r+2][c] == 'A' &&
                    grid[r+3][c] == 'S') answer += 1;
                if (r >= 3 &&
                    grid[r  ][c] == 'X' &&
                    grid[r-1][c] == 'M' &&
                    grid[r-2][c] == 'A' &&
                    grid[r-3][c] == 'S') answer += 1;
                if (c < width - 3 && r < height - 3 &&
                    grid[r  ][c  ] == 'X' &&
                    grid[r+1][c+1] == 'M' &&
                    grid[r+2][c+2] == 'A' &&
                    grid[r+3][c+3] == 'S') answer += 1;
                if (c >= 3 && r < height - 3 &&
                    grid[r  ][c  ] == 'X' &&
                    grid[r+1][c-1] == 'M' &&
                    grid[r+2][c-2] == 'A' &&
                    grid[r+3][c-3] == 'S') answer += 1;
                if (c < width - 3 && r >= 3 &&
                    grid[r  ][c  ] == 'X' &&
                    grid[r-1][c+1] == 'M' &&
                    grid[r-2][c+2] == 'A' &&
                    grid[r-3][c+3] == 'S') answer += 1;
                if (c >= 3 && r >= 3 &&
                    grid[r  ][c  ] == 'X' &&
                    grid[r-1][c-1] == 'M' &&
                    grid[r-2][c-2] == 'A' &&
                    grid[r-3][c-3] == 'S') answer += 1;
            }
        }

        return answer;
    }

    size_t Part2()
    {
        size_t answer = 0;
        for (int r = 1; r < height - 1; ++r) {
            for (int c = 1; c < width - 1; ++c) {
                if (grid[r][c] != 'A') continue;

                if ((grid[r-1][c-1] == 'M' && grid[r+1][c+1] == 'S' ||
                     grid[r-1][c-1] == 'S' && grid[r+1][c+1] == 'M') &&
                    (grid[r-1][c+1] == 'M' && grid[r+1][c-1] == 'S' ||
                     grid[r-1][c+1] == 'S' && grid[r+1][c-1] == 'M')) answer += 1;
            }
        }

        return answer;
    }
    std::vector<std::string> grid;
    int width, height;
};

int main(int argc, char **argv)
{
    Day04 cmd(argc > 1 ? argv[1] : "input");
    std::cout << "Answer 1 = " << cmd.Part1() << std::endl;
    std::cout << "Answer 2 = " << cmd.Part2() << std::endl;
    return 0;
}

  /*
#!/usr/bin/env python3
"""
<Problem description here>
"""
import sys
import numpy as np

class Day04:
    def __init__(self):
        self.input = None

        self.content = None
        self.lines = []
        self.grid = None
        
        self.ParseArgs()
        self.ParseInput()

    def ParseArgs(self, args=None):
        import argparse

        parser = argparse.ArgumentParser('Day04')
        parser.add_argument('input', nargs='?', default='input')

        parser.parse_args(args, self)


    def ParseInput(self):
        with open(self.input) as input:
            self.contents = input.read().strip()
        self.lines = self.contents.split('\n')

        ########################################################################
        # If the puzzle is not grid/map based, delete these lines.
        gridKey = {'X': 1, 'M': 2, 'A': 3, 'S':4}
        self.height = len(self.lines)
        self.width = len(self.lines[0])

        self.grid = np.zeros((self.height, self.width), dtype=int)
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                self.grid[row, col] = gridKey.get(ch, 0)
        #
        ########################################################################


    # Horizontal test
    def test1(self, grid):
        count = 0
        for r in range(self.height):
            for c in range(self.width - 3):
                if list(grid[r, c:c+4]) == [1, 2, 3, 4]:
                    count += 1
        return count

    # Diagonal test
    def test2(self, grid):
        count = 0
        for r in range(self.height):
            for c in range(self.width - 3):
                if list(grid[r:r+4, c:c+4].diagonal()) == [1, 2, 3, 4]:
                    count += 1
        return count

    def Part1(self):
        answer = 0

        view = self.grid
        answer += self.test1(self.grid)
        answer += self.test1(self.grid[:, ::-1])
        answer += self.test1(self.grid.T)
        answer += self.test1(self.grid.T[:, ::-1])
        answer += self.test2(self.grid)
        answer += self.test2(self.grid[:, ::-1])
        answer += self.test2(self.grid[::-1, :])
        answer += self.test2(self.grid.T[::-1, ::-1])
        return answer

    def test3(self, grid):
        count = 0
        return count
        
    def Part2(self):
        answer = 0
        for r in range(self.height-2):
            for c in range(self.width - 2):
                check = self.grid[r:r+3, c:c+3]
                if (list(check.diagonal()) in ([2, 3, 4], [4, 3, 2]) and
                    list(check[:,::-1].diagonal()) in ([2, 3, 4], [4, 3, 2])):
                    answer += 1
        return answer
    
if __name__ == '__main__':
    problem = Day04()
    
    answer1 = problem.Part1()
    print(f'Answer 1: {answer1}')

    answer2 = problem.Part2()
    print(f'Answer 2: {answer2}')



  */
