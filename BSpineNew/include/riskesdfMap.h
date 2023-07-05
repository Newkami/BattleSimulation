#pragma once

#include <stdint.h>
#include <string>
#include <memory>
#include <vector>
#include <Eigen/Core>
#include <Eigen/Sparse>
#include <map>
#include "map_target.h"
 
namespace uav
{

class MapOBJ
{
public:
    enum Object
    {
        EMPTY = 0,
        JAMMER = 1,
        MISSILE_VEHICLE = 2,
        RADAR = 3,
        ANTITURRENT = 4,
        COMMANDPOST = 5,
        MULTIROTOR = 6,
        OBSTACLE = -1, // 障碍
        BOUNDARY = -2  // 边界

    };
    static const std::string ObjToString(MapOBJ::Object obj);
    static MapOBJ::Object FromString(const std::string &str);
};

class GridPoint // 地图中的每个栅格点
{
public:
    typedef std::shared_ptr<GridPoint> ptr;
    GridPoint() {}
    GridPoint(uint16_t x, uint16_t y, MapOBJ::Object obj = MapOBJ::EMPTY);
    ~GridPoint();

    uint16_t getXCord() const { return x_cord; }
    uint16_t getYCord() const { return y_cord; }

    void setObject(const MapOBJ::Object obj) {m_obj = obj;}
    MapOBJ::Object getObject() const { return m_obj; }

    Eigen::Vector2d getGradient() const { return m_gradient; }

    
    void setDistance(double val) {m_distance = val;}
    double getDistance() const { return m_distance; }

    std::string ToString() const;
    std::pair<uint16_t, uint16_t> getCordinationPoint() const{return m_cord_point;}

    void setOccupiedStatus(bool status) { m_isoccupied = status; }
    bool getOccupationState() const { return m_isoccupied; }

    void setRiskcoef(double val){m_risk_coef = val;}
    double getRiskcoef() const {return m_risk_coef;}

    void setPointName(const std::string& val){point_name = val;}
    const std::string& getPointName() const {return point_name;}
private:
    uint16_t x_cord;
    uint16_t y_cord;
    // uint8_t z;  暂时不考虑z轴
    double m_distance = 0;   //存放的是EDT信息 即距离最近障碍物的距离
    Eigen::Vector2d m_gradient = {0.0, 0.0};
    MapOBJ::Object m_obj; // 该点存放的具体类型

    double m_risk_coef = 0.0;
    bool m_isoccupied = false;
    std::string point_name = "empty";
    std::pair<uint16_t, uint16_t> m_cord_point;
};

class RiskESDFMap
{
public:
    typedef std::shared_ptr<RiskESDFMap> ptr;

    RiskESDFMap(const std::string &name, uint16_t x, uint16_t y, double resolution);

    const std::string& getMapname() const { return m_mapname; }
    // 有时候一些类的成员函数返回引用，以便一修改类内部的数据
    const std::vector<GridPoint>& getGridMap() const { return m_gridmap; }
    // 返回gripMap的Eigen::Matrix形式 该格式用于可视化局部地图
    Eigen::MatrixXi GripMapToMatrixMap(const std::vector<GridPoint> &gridmap);

    template <typename F_get_val, typename F_set_val>
    void fillESDF(F_get_val f_get_val, F_set_val f_set_val, int start, int end, int dim);

    void updateESDF2d();
    int getVoxelnum(int dim);

    int isObstacle(int x,int y);
    int isCanAtkTarget(int x,int y);


    // 将二维坐标转换为m_gridmap中的index
    int CordToIndex(int x,int y);
    std::pair<int,int> IndexToCord(int idx);

    void initMap();
    void initRandomObstacle();


    Eigen::MatrixXd GetESDFMatrixMap();
    Eigen::MatrixXd GetRiskMatrixMap();
  
    template <typename F_get_val, typename F_set_val>
    void fillRiskVal(F_get_val f_get_val, F_set_val f_set_val, int start, int end, int dim);
    void updateRisk2d();

private:
    std::string m_mapname;
    uint16_t shape_x; // 地图X大小
    uint16_t shape_y; // 地图Y大小
    // uint16_t shape_z;

    double m_resolution;
    std::vector<GridPoint> m_gridmap; // vector大小为shape_x * shape_y
};



}