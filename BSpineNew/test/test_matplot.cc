#include "matplotlibcpp.h"
#include <vector>
namespace plt = matplotlibcpp;

int main() 
{
    plt::scatter(std::vector<int>({1,2,3,4}),std::vector<int>({1,2,3,4}), 50);
    plt::show();
    return 0;
}