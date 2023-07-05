#include "riskesdfMap.h"
#include "matplotlibcpp.h"
#include <iostream>

namespace plt = matplotlibcpp;

int main(int argc, char ** argv){
    uav::RiskESDFMap::ptr g_map = std::shared_ptr<uav::RiskESDFMap>(new uav::RiskESDFMap("test_map2",50,50,0.4));
    g_map->initRandomObstacle();
    auto matrix_map = g_map->GripMapToMatrixMap(g_map->getGridMap());
    std::cout<<"--------------------------------------"<<std::endl;
    std::cout<<matrix_map<<std::endl;
    std::cout<<"--------------------------------------"<<std::endl;
    g_map->updateESDF2d();

    Eigen::MatrixXd matrix = g_map->GetESDFMatrixMap();

    std::vector<float> matrixVector(matrix.rows()*matrix.cols());
    int start = 0;
    for (int i = 1; i < matrix.rows()-1; ++i) {
        for (int j = 1; j < matrix.cols()-1; ++j) {
            matrixVector[start] = matrix(i, j);
            ++start;
        }
    }
    PyObject* mat;

    plt::imshow(&matrixVector[0],matrix.rows()-2,matrix.cols()-2,1,{},&mat);
    // plt::set_cmap("hot");

    // 显示颜色条
    plt::colorbar(mat);
    plt::show();
    
    return 0;
}
