#include "riskesdfMap.h"
#include <iostream>
#include <random>
namespace uav
{

const std::string MapOBJ::ObjToString(MapOBJ::Object obj){
    switch (obj)
    {
    #define XX(object)\
    case MapOBJ::object: \
    return #object;\
    break;
    XX(JAMMER)
    XX(MISSILE_VEHICLE)
    XX(RADAR)
    XX(ANTITURRENT)
    XX(COMMANDPOST)
    XX(OBSTACLE)
    XX(MULTIROTOR)
    #undef XX
    default:
        return "EMPTY";
    }
    return "EMPTY";
}

MapOBJ::Object MapOBJ::FromString(const std::string& str){
#define XX(object, v)\
    if(str==#v){   \
    return MapOBJ::object;\
    }
    XX(JAMMER, JAMMER)
    XX(MISSILE_VEHICLE,MISSILE_VEHICLE)
    XX(RADAR,RADAR)
    XX(ANTITURRENT,ANTITURRENT)
    XX(COMMANDPOST,COMMANDPOST)
    XX(OBSTACLE,OBSTACLE)
    XX(MULTIROTOR,MULTIROTOR)
#undef XX
    return MapOBJ::EMPTY;
}


GridPoint::GridPoint(uint16_t x, uint16_t y, MapOBJ::Object obj)
:x_cord(x),y_cord(y),m_obj(obj),m_cord_point(x_cord,y_cord)
{ 

}

GridPoint::~GridPoint(){
    
}

std::string GridPoint::ToString() const
{
    std::ostringstream oss;
    oss<<"Point:("<<x_cord<<","<<y_cord<<")"<<"current object: "<<MapOBJ::ObjToString(m_obj)<<
    "\nthe occupation status : "<<m_isoccupied<<"\n Gradient(2d):\n"<<m_gradient<<"\n";
    return oss.str();
}

RiskESDFMap::RiskESDFMap(const std::string& name,uint16_t x,uint16_t y,double resolution)
:m_mapname(name),shape_x(x),shape_y(y),m_resolution(resolution)
{

    for(size_t i = 0;i<shape_x;++i){
        for(size_t j=0;j<shape_y;++j){
            m_gridmap.emplace_back(i+1,j+1,MapOBJ::EMPTY);   //地图初始化
        }
    }
    // std::cout<<m_gridmap.size()<<std::endl; 30*30 = 900 即可访问范围为[0,899]
    //tmp_buffer.resize(m_gridmap.size());
    //m_distance_buffer.resize(m_gridmap.size());
    // todo 通过json文件初始化gridmap
}

Eigen::MatrixXi RiskESDFMap::GripMapToMatrixMap(const std::vector<GridPoint> &gridmap)
{

    // std::random_device rd;
    // std::mt19937 gen(rd());
    // std::uniform_int_distribution<int> dist(0,6);



    Eigen::MatrixXi map_matrix(shape_x+2,shape_y+2);
    map_matrix.fill(MapOBJ::BOUNDARY); //初始化最外层为边界
    for(const auto& point:gridmap){
        //std::cout<<point.getXCord()-1<<point.getYCord()-1<<point.getObject()<<std::endl;
        map_matrix(point.getXCord(),point.getYCord()) = point.getObject();
    }
    //std::cout<<map_matrix<<std::endl;
    return map_matrix;  //返回的是局部变量的副本
}

int RiskESDFMap::getVoxelnum(int dim)
{
    if (dim == 0)
        return shape_x;
    else if(dim==1)
        return shape_y;
    else return -1;
}

int RiskESDFMap::CordToIndex(int x, int y)
{
    int index = (x-1)*shape_y + (y-1);
    return index;
}

std::pair<int,int> RiskESDFMap::IndexToCord(int idx){
    return std::pair<int,int>{idx/shape_y + 1,idx%shape_y + 1};
}

//随机初始化障碍物
void RiskESDFMap::initRandomObstacle()
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist1(1,shape_y/2);
    std::uniform_int_distribution<int> dist2(shape_y/2+1,shape_y);

    m_gridmap[CordToIndex(7,7)].setObject(MapOBJ::JAMMER);
    /*给每一行随机选择2个点作为障碍物*/
    for(size_t x=1;x<=shape_x;++x)
    {
        int y1 = dist1(gen);
        int y2 = dist2(gen);
        m_gridmap[CordToIndex(x,y1)].setObject(MapOBJ::OBSTACLE);
        m_gridmap[CordToIndex(x,y2)].setObject(MapOBJ::OBSTACLE);
        m_gridmap[CordToIndex(x,y1)].setOccupiedStatus(true);
        m_gridmap[CordToIndex(x,y2)].setOccupiedStatus(true);
    }
}



//从LoadFromJson中读取的地图对象来初始化RiskESDFMap
void RiskESDFMap::initMap(){
    //自己提供访问TargetMap的函数 要求函数参数为ObjectBase::ptr类型
    uav::TargetManager::Visit(
        //捕获成员变量
        [&](const std::string& targetid, ObjectBase::ptr obj){
            auto type = obj->getTargetType();
            switch (type)
            {
            case MapOBJ::JAMMER:
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setPointName(targetid);
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setObject(MapOBJ::JAMMER);
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setOccupiedStatus(true);
                break;
            case MapOBJ::MISSILE_VEHICLE:
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setPointName(targetid);
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setObject(MapOBJ::MISSILE_VEHICLE);
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setOccupiedStatus(true);
                break;
            case MapOBJ::RADAR:
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setPointName(targetid);
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setObject(MapOBJ::RADAR);
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setOccupiedStatus(true);
                break;
            case MapOBJ::ANTITURRENT:
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setPointName(targetid);
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setObject(MapOBJ::ANTITURRENT);
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setOccupiedStatus(true);
                break;
            case MapOBJ::COMMANDPOST:
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setPointName(targetid);
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setObject(MapOBJ::COMMANDPOST);
                m_gridmap[CordToIndex(obj->getXCord(),obj->getYCord())].setOccupiedStatus(true);
                break;
            default:
                break;
            }
        }
    );
    // 用于测试是否正确导入
    // std::ofstream file("/home/zz/log.txt");
    // for(auto i:m_gridmap)
    //     file<<i.ToString();
}


int RiskESDFMap::isObstacle(int x,int y){
    return m_gridmap[CordToIndex(x,y)].getObject()==MapOBJ::OBSTACLE;
}
int RiskESDFMap::isCanAtkTarget(int x,int y){
    return m_gridmap[CordToIndex(x,y)].getObject()==MapOBJ::JAMMER
    ||m_gridmap[CordToIndex(x,y)].getObject()==MapOBJ::MISSILE_VEHICLE;
}



// 在一維上fillESDF
template<typename F_get_val, typename F_set_val>
void RiskESDFMap::fillESDF(F_get_val f_get_val, F_set_val f_set_val, int start, int end, int dim)
{
    int map_voxel_num = getVoxelnum(dim)+1;
    if (map_voxel_num<0)
    {
        std::cout<<"get_map_voxel_num defeat"<<std::endl;
        exit(-1);
    }
    std::vector<int> v(map_voxel_num);
    std::vector<double> z(map_voxel_num+1);
    int k = start;
    v[start] = start;
    z[start] = -std::numeric_limits<double>::max();  //表示第0个抛物线没有交点
    //用于初始化一个名为z的数组或向量，并将其起始元素的值设置为-std::numeric_limits<double>::max()，即double类型的负无穷大
    /*
        Df(p) = min[q<-G]((p-q)^2 + f(q))
        q表示这一维度珊格中是障碍物的部分； p是需要计算最小障碍物距离的位置
        k用来表示构成下包络的抛物线个数
        v[k] 表示第k个抛物线的顶点； 
        z[k] z[k+1]表示第 k 个抛物线在整个下包络中的有效范围；
        其中z[k]表示的是第k个抛物线与第k-1个抛物线的交点；
    */
    z[start + 1] = std::numeric_limits<double>::max();//表示第一个抛物线的交点为最大值
    
    for(int q= start+1;q<=end;++q){
        ++k;
        double s;

        do{
            --k;
            s = ((f_get_val(q) + q * q) - (f_get_val(v[k]) + v[k] * v[k])) / (2 * q - 2 * v[k]);
        }while(s<=z[k]);

        ++k;

        v[k] = q;
        z[k] = s;
        z[k+1] = std::numeric_limits<double>::max();
    }

    k = start;
    for (int q = start; q <= end; q++) {
    while (z[k + 1] < q) k++;
    double val = (q - v[k]) * (q - v[k]) + f_get_val(v[k]);
    f_set_val(q, val);
  }

}

// 在一维上fillRisk_val
template <typename F_get_val, typename F_set_val>
void RiskESDFMap::fillRiskVal(F_get_val f_get_val, F_set_val f_set_val,  int start, int end, int dim)
{
    int map_voxel_num = getVoxelnum(dim)+1;
    if (map_voxel_num<0)
    {
        std::cout<<"get_map_voxel_num defeat"<<std::endl;
        exit(-1);
    }
    std::vector<int> v(map_voxel_num);
    std::vector<double> z(map_voxel_num+1);
    int k = start;
    v[start] = start;
    z[start] = -std::numeric_limits<double>::max();  //表示第0个抛物线没有交点
    z[start + 1] = std::numeric_limits<double>::max();//表示第一个抛物线的交点为最大值
    for(int q=start+1;q<=end;++q){
        ++k;
        double s;

        do{
            --k;
            s = ((f_get_val(q).first + q * q) - (f_get_val(v[k]).first + v[k] * v[k])) / (2 * q - 2 * v[k]);
        }while(s<=z[k]);

        ++k;

        v[k] = q;
        z[k] = s;
        z[k+1] = std::numeric_limits<double>::max();
    }

    k = start;
   
    for (int q = start; q <= end; q++) {
        double atk_range = f_get_val(v[k]).second;
        while (z[k + 1] < q) k++;
        double dis = (q - v[k]) * (q - v[k]) + f_get_val(v[k]).first;
        double riskval = 0.0;
        double a = std::numeric_limits<double>::max();
        if(dis<std::numeric_limits<double>::max()){
            a = f_get_val(v[k]).second;
        }
        if (dis <= a*a)
            riskval = 1.0/a;
        std::cout<<a<<" ";    
        f_set_val(q, dis, riskval,a);
        //std::cout<<riskval<<" ";
    }
}


void RiskESDFMap::updateRisk2d(){
    std::vector<std::pair<double, double>> tmp_buffer(m_gridmap.size());
    std::vector<std::pair<double, double>> m_riskESDF_buffer(m_gridmap.size());

    std::vector<double> tmp_atk_range_buffer(m_gridmap.size());
    for(int x = 1;x<=shape_x;++x){
        fillRiskVal(
            [&](int y){
                if(isCanAtkTarget(x,y)){
                    auto name = m_gridmap[CordToIndex(x,y)].getPointName();
                    auto target_ptr = TargetManager::GetTargetByid(name);
                    double atk_range = -1;
                    if(target_ptr){
                        if(target_ptr->getTargetType() == MapOBJ::JAMMER){
                            atk_range = std::dynamic_pointer_cast<Jammer>(target_ptr)->getAtkRange();
                        }else{
                            atk_range = std::dynamic_pointer_cast<Missile_Vehicle>(target_ptr)->getAtkRange();
                        }
                    }
                    return std::make_pair(0.0,atk_range);
                }
                // return isCanAtkTarget(x,y)==1?0:
                // std::numeric_limits<double>::max();
                else{
                    return std::make_pair(std::numeric_limits<double>::max(),-1.0);
                }
            },
            [&](int y, double dis, double riskval,double a){
                tmp_buffer[CordToIndex(x,y)].first = dis;
                tmp_buffer[CordToIndex(x,y)].second = riskval;
                tmp_atk_range_buffer[CordToIndex(x,y)] = a;
            },1,shape_y,1);
        std::cout<<std::endl;
    }
    std::cout<<"--------------------------------"<<std::endl;
    for(int y = 1;y<=shape_y;++y){
        fillRiskVal(
            [&](int x){
                return std::make_pair(tmp_buffer[CordToIndex(x,y)].first,tmp_atk_range_buffer[CordToIndex(x,y)]);
            },
            [&](int x, double dis, double riskval,double a){
                m_riskESDF_buffer[CordToIndex(x,y)].first = m_resolution * std::sqrt(dis);
                m_riskESDF_buffer[CordToIndex(x,y)].second = riskval*std::sqrt(dis);
                if(std::sqrt(dis)==0)
                m_riskESDF_buffer[CordToIndex(x,y)].second += 0.001;
            },
            1,shape_x,0
        );
        std::cout<<std::endl;
    }
    for(size_t i=0;i<m_gridmap.size();++i)
    {
        if(m_riskESDF_buffer[i].second!=0)
        {
            m_gridmap[i].setRiskcoef(1.0 - m_riskESDF_buffer[i].second);
        }
    }
    
}


/* 备用版本
// 在一维上fillRisk_val
template <typename F_get_val, typename F_set_val>
void RiskESDFMap::fillRiskVal(F_get_val f_get_val, F_set_val f_set_val,  int start, int end, int dim, int atk_range)
{
    int map_voxel_num = getVoxelnum(dim)+1;
    if (map_voxel_num<0)
    {
        std::cout<<"get_map_voxel_num defeat"<<std::endl;
        exit(-1);
    }
    std::vector<int> v(map_voxel_num);
    std::vector<double> z(map_voxel_num+1);
    int k = start;
    v[start] = start;
    z[start] = -std::numeric_limits<double>::max();  //表示第0个抛物线没有交点
    z[start + 1] = std::numeric_limits<double>::max();//表示第一个抛物线的交点为最大值
    for(int q=start+1;q<=end;++q){
        ++k;
        double s;

        do{
            --k;
            s = ((f_get_val(q) + q * q) - (f_get_val(v[k]) + v[k] * v[k])) / (2 * q - 2 * v[k]);
        }while(s<=z[k]);

        ++k;

        v[k] = q;
        z[k] = s;
        z[k+1] = std::numeric_limits<double>::max();
    }

    k = start;
    for (int q = start; q <= end; q++) {
    while (z[k + 1] < q) k++;
    double dis = (q - v[k]) * (q - v[k]) + f_get_val(v[k]);
    double riskval = 0.0;
    if (dis <= atk_range*atk_range)
         riskval = 1.0/atk_range;
    f_set_val(q, dis, riskval);
    //std::cout<<riskval<<" ";
    }
}


void RiskESDFMap::updateRisk2d(){
    std::vector<std::pair<double, double>> tmp_buffer(m_gridmap.size());
    std::vector<std::pair<double, double>> m_riskESDF_buffer(m_gridmap.size());
    double atk_range = 3.0;
    for(int x = 1;x<=shape_x;++x){
        fillRiskVal(
            [&](int y){
                return isCanAtkTarget(x,y)==1?0:
                std::numeric_limits<double>::max();
            },
            [&](int y, double dis, double riskval){
                tmp_buffer[CordToIndex(x,y)].first = dis;
                tmp_buffer[CordToIndex(x,y)].second = riskval;
            },1,shape_y,1,atk_range
        );
       // std::cout<<std::endl;
    }
   // std::cout<<"--------------------------------"<<std::endl;
    for(int y = 1;y<=shape_y;++y){
        fillRiskVal(
            [&](int x){
                return tmp_buffer[CordToIndex(x,y)].first;
            },
            [&](int x, double dis, double riskval){
                m_riskESDF_buffer[CordToIndex(x,y)].first = m_resolution * std::sqrt(dis);
                m_riskESDF_buffer[CordToIndex(x,y)].second = riskval*std::sqrt(dis);
                if(std::sqrt(dis)==0)
                m_riskESDF_buffer[CordToIndex(x,y)].second += 0.01;
                if(std::sqrt(dis)==atk_range)
                m_riskESDF_buffer[CordToIndex(x,y)].second -= 0.01;
                
            },
            1,shape_x,0,atk_range
        );
        //std::cout<<std::endl;
    }
    for(size_t i=0;i<m_gridmap.size();++i)
    {
        if(m_riskESDF_buffer[i].second!=0)
        {
            m_gridmap[i].setRiskcoef(1.0-m_riskESDF_buffer[i].second);
        }
    }
    
}
*/

void RiskESDFMap::updateESDF2d(){

    std::vector<double> tmp_buffer(m_gridmap.size());  //在栈上分配的空间 函数结束后会自动析构
    std::vector<double> m_distance_buffer(m_gridmap.size());
    /* ========== compute positive DT ========== */
    for(int x = 1;x<=shape_x;++x){  
        fillESDF(
            [&](int y){  //以引用方式捕获所有变量 其实也就是x
                //(x,y)是以坐标形式传入的
                return isObstacle(x,y) == 1? 0:
                std::numeric_limits<double>::max();
            },
            [&](int y, double val){
                tmp_buffer[CordToIndex(x,y)] = val;
                /*用一个tmp_buffer 把（x,y）坐标的指存起来*/
            },
            1,shape_y,1
        );
    }
    for(int y = 1;y<=shape_y;++y){
        fillESDF(
            [&](int x){
                return tmp_buffer[CordToIndex(x,y)];
            },
            [&](int x, double val){
                m_distance_buffer[CordToIndex(x,y)] = m_resolution * std::sqrt(val);
            },
            1,shape_x,0
        );
    }


    //m_distance_buffer_neg 如果这个坐标不是障碍那么就等于1

    for(size_t i=0;i<m_gridmap.size();++i)
        m_gridmap[i].setDistance(m_distance_buffer[i]);
}


Eigen::MatrixXd RiskESDFMap::GetESDFMatrixMap ()
{
    Eigen::MatrixXd esdf_matrix(shape_x+2,shape_y+2);
    esdf_matrix.fill(MapOBJ::BOUNDARY); //初始化最外层为边界
    for(size_t i = 0;i<m_gridmap.size();++i){
        auto cord = IndexToCord(i);
        esdf_matrix(cord.first,cord.second) = m_gridmap[i].getDistance();
    }
    //std::cout<<map_matrix<<std::endl;
    return esdf_matrix;  //返回的是局部变量的副本
}

Eigen::MatrixXd RiskESDFMap::GetRiskMatrixMap ()
{
    Eigen::MatrixXd risk_matrix(shape_x+2,shape_y+2);
    risk_matrix.fill(MapOBJ::BOUNDARY); //初始化最外层为边界
    for(size_t i = 0;i<m_gridmap.size();++i){
        auto cord = IndexToCord(i);
        risk_matrix(cord.first,cord.second) = m_gridmap[i].getRiskcoef();
    }
    //std::cout<<map_matrix<<std::endl;
    return risk_matrix;  //返回的是局部变量的副本
}

} // namespace uav










