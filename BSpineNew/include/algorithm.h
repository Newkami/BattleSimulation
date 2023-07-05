#pragma once
#include <math.h>
#include <iostream>
#include <Eigen/Core>

// 快速获取Eigen::Vector2d的x分量 并以std::vector<double>封装 用于画图测试
#define vecX(val)\
	std::vector<double>{val.x()}

#define vecY(val)\
	std::vector<double>{val.y()}
namespace uav{
std::pair<Eigen::Vector2d,Eigen::Vector2d> calculateIntersection(
    const Eigen::Vector2d& origin, const Eigen::Vector2d& direction, const Eigen::Vector2d& center, double radius);

}