#include "BSpline.h"
#include <Eigen/Core>


int main()
{
    BSpineTest test;
    Eigen::MatrixXd map;
    Eigen::Vector2d start(13,8);
    Eigen::Vector2d end(14,20);
    test.avoidRiskAreaTest(map,start,end,0.0);
    return 0;
}