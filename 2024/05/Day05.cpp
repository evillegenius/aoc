#include <iostream>
#include <fstream>
#include <sstream>
#include <set>
#include <vector>
#include <utility>

struct Day05
{
    Day05(const std::string& name)
    {
        ParseInput(name);
    }

    void ParseInput(const std::string& name)
    {
        std::fstream input(name);
        std::string line;
        
        while (input.good()) {
            int a, b;
            char sep;

            input >> a >> sep >> b;
            if (!input.good()) break;
            if (sep == '|') {
                rules.insert(std::make_pair(a, b));
            } else {
                updates.emplace_back();
                std::vector<int>& update = updates.back();
                
                update.push_back(a);
                update.push_back(b);

                std::string restOfLine;
                std::getline(input, restOfLine);
                std::stringstream strInput(restOfLine);
                while (strInput.good()) {
                    sep = 'x';
                    b = -1;
                    strInput >> sep >> b;
                    if (b > 0) {
                        update.push_back(b);
                    }
                }
            }
        }

        // std::cout << "Rules:\n";
        // for (const auto& item : rules) {
        //     std::cout << item.first << '|' << item.second << "\n";
        // }
        // std::cout << std::endl;
        // std::cout << "Updates:\n";
        // for (const auto& update : updates) {
        //     char prefix = '[';
        //     for (const auto& page : update) {
        //         std::cout << prefix << page;
        //         prefix = ',';
        //     }
        //     std::cout << "]" << std::endl;
        // }
    }

    size_t Part1() {
        answer1 = 0;
        updateGood.resize(updates.size(), false);
        for (size_t u = 0; u < updates.size(); ++u) {
            const auto& update = updates[u];
            bool good = true;
            for (const auto& rule : rules) {
                auto firstIter = std::find(update.begin(), update.end(), rule.first);
                auto secondIter = std::find(update.begin(), update.end(), rule.second);
                if (firstIter == update.end() || secondIter == update.end()) {
                    continue;
                }
                if (firstIter > secondIter) {
                    good = false;
                    break;
                }
            }
            if (good) {
                updateGood[u] = true;
                answer1 += update[update.size()/2];
            }
        }

        return answer1;
    }

    size_t Part2() {
        answer2 = 0;

        auto cmp = [this](const int a, const int b) -> bool {
            return this->rules.count(std::make_pair(a, b));
        };

        for (size_t u = 0; u < updates.size(); ++u) {
            if (not updateGood[u]) {
                auto& update = updates[u];
                std::sort(update.begin(), update.end(), cmp);
                answer2 += update[update.size() / 2];
            }
        }

        return answer2;
    }

    std::set<std::pair<int, int>> rules;
    std::vector<std::vector<int>> updates;
    std::vector<bool> updateGood;

    size_t answer1 = 0;
    size_t answer2 = 0;
};

int main(int argc, char **argv)
{
    const std::string name = (argc > 1 ? argv[1] : "input");
    Day05 problem(name);

    std::cout << "Answer 1: " << problem.Part1() << std::endl;
    std::cout << "Answer 2: " << problem.Part2() << std::endl;

    return 0;
}
/*
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



*/
