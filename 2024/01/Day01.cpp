#include <iostream>
#include <fstream>
#include <set>
#include <cassert>

class Day01
{
public:
    Day01(std::string name) {
        GetInput(name);
    }

    void GetInput(std::string name) {
        std::ifstream input{name};
        assert(not input.fail());

        int a, b;

        while (not input.eof()) {
            input >> a >> b;
            if (input.fail()) {
                break;
            }
            listA.insert(a);
            listB.insert(b);
        }
    }

    unsigned long Part1() {
        unsigned long answer = 0;

        for (auto iterA = listA.begin(), iterB=listB.begin();
             iterA != listA.end() && iterB != listB.end();
             ++iterA, ++iterB)
        {
            answer += abs(*iterA - *iterB);
        }

        return answer;
    }

    unsigned long Part2() {
        unsigned long answer = 0;

        for (auto iterA = listA.begin(); iterA != listA.end(); ++iterA) {
            answer += *iterA * listB.count(*iterA);
        }

        return answer;
    }

    std::multiset<int> listA;
    std::multiset<int> listB;

    std::string inputName;
};

int main(int argc, char** argv)
{
    std::string inputName(argc > 1 ? argv[1] : "input");
    Day01 problem(inputName);

    std::cout << problem.Part1() << std::endl;
    std::cout << problem.Part2() << std::endl;

    return 0;
}