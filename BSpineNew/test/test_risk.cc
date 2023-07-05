#include "riskesdfMap.h"
#include "matplotlibcpp.h"
#include "BSpline.h"
#include <iostream>
#include <fstream>
namespace plt = matplotlibcpp;

int main(int argc, char ** argv){
    uav::RiskESDFMap::ptr g_map = std::shared_ptr<uav::RiskESDFMap>(new uav::RiskESDFMap("test_map2",50,50,0.4));
    g_map->initRandomObstacle();
    auto matrix_map = g_map->GripMapToMatrixMap(g_map->getGridMap());
    std::cout<<"--------------------------------------"<<std::endl;
    std::cout<<matrix_map<<std::endl;
    std::cout<<"--------------------------------------"<<std::endl;
    g_map->updateRisk2d();
    std::cout<<"*************************************"<<std::endl;
    Eigen::MatrixXd matrix = g_map->GetRiskMatrixMap();
    std::cout<<matrix<<std::endl;
    //BSpineTest test;
    //test.avoidObstacle(matrix,{13,9},{1,9});

    std::ofstream file("/home/zdp/C++WorkSpace/BSpineTest/data/risk_map.txt");

    if(file.is_open())
    {
        file<<"[";
        for (int i = 1; i < matrix.rows()-1; ++i) {
        for (int j = 1; j < matrix.cols()-1; ++j) {
           if(j==1)
           file<<"[";
           file<<matrix(i,j);

           if(j==matrix.cols()-2)
            {
                file<<"]";
            }
           else
            file<<",";
        }
        if(i<matrix.rows()-2){
            file<<",";
            file<<"\n";
        }
    }
        file<<"]";
    }
    file.close();
    std::vector<float> matrixVector(matrix.rows()*matrix.cols());
    int start = 0;
    for (int i = 1; i < matrix.rows()-1; ++i) {
        for (int j = 1; j < matrix.cols()-1; ++j) {
            matrixVector[start] = matrix(i, j);
            ++start;
        }
    }

    return 0;
}
