#include <iostream>
#include <cmath>
#include "algorithm.h"

int main() {
    Eigen::Vector2d origin(0.0, 0.0);  // 向量的起点
    Eigen::Vector2d direction(1.0, 1.0);  // 向量的方向
    Eigen::Vector2d center(0,5);  // 圆的圆心
    double radius = 1.0;  // 圆的半径

    auto a = uav::calculateIntersection(origin, direction, center, radius);
    auto intersection1 = a.first;
    auto intersection2 = a.second;
    if(std::isnan(intersection1.x())){
        std::cout << "Intersection 1: (" << intersection1.x() << ", " << intersection1.y() << ")" << std::endl;
    }
     if(std::isnan(intersection1.x())){
        std::cout << "Intersection 2: (" << intersection2.x() << ", " << intersection2.y() << ")" << std::endl;
    }
    std::cout << "Intersection 1: (" << intersection1.x() << ", " << intersection1.y() << ")" << std::endl;
    std::cout << "Intersection 2: (" << intersection2.x() << ", " << intersection2.y() << ")" << std::endl;

    return 0;
}