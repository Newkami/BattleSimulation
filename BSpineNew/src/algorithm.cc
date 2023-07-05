#include "algorithm.h"


namespace uav{

std::pair<Eigen::Vector2d,Eigen::Vector2d> calculateIntersection(
    const Eigen::Vector2d& origin, const Eigen::Vector2d& direction, const Eigen::Vector2d& center, double radius){
    Eigen::Vector2d intersection1;
    Eigen::Vector2d intersection2;
    // 计算向量的起点到圆心的向量
    Eigen::Vector2d oc = center - origin;

    // 计算向量的方向的长度
    double directionLength = direction.norm();

    // 计算射线与圆的判别式
    double discriminant = std::pow(direction.dot(oc), 2) - directionLength * directionLength * (oc.squaredNorm() - radius * radius);


    // 判别式小于0表示没有交点
    if (discriminant < 0) {
        intersection1 = Eigen::Vector2d(std::numeric_limits<double>::quiet_NaN(), std::numeric_limits<double>::quiet_NaN());
        intersection2 = Eigen::Vector2d(std::numeric_limits<double>::quiet_NaN(), std::numeric_limits<double>::quiet_NaN());
    }
    // 判别式等于0表示有一个交点
    else if (discriminant == 0) {
        double t = -direction.dot(oc) / directionLength;
        intersection1 = origin - t * direction;
        intersection2 = Eigen::Vector2d(std::numeric_limits<double>::quiet_NaN(), std::numeric_limits<double>::quiet_NaN());
    }
    // 判别式大于0表示有两个交点
    else {
        double t1 = (-direction.dot(oc) + std::sqrt(discriminant)) / directionLength;
        double t2 = (-direction.dot(oc) - std::sqrt(discriminant)) / directionLength;
        intersection1 = origin - t1 * direction;
        intersection2 = origin - t2 * direction;
    }
    return std::make_pair(intersection1,intersection2);
}

}