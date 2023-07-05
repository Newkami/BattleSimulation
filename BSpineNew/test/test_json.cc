#include "map_target.h"
#include "riskesdfMap.h"
#include <fstream>
int main(int argc,char** argv)
{    

    uav::TargetManager::LoadFromJson("/home/zdp/C++WorkSpace/BSpineTest/data/map.json");
    uav::RiskESDFMap::ptr g_map = std::make_shared<uav::RiskESDFMap>("test_map3",50,50,0.2);
    g_map->initMap();
    g_map->updateRisk2d();
    std::cout<<"*************************************"<<std::endl;
    Eigen::MatrixXd matrix = g_map->GetRiskMatrixMap();
    std::cout<<matrix<<std::endl;


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
    return 0;
}