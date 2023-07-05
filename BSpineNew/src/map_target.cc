#include "map_target.h"
#include <fstream>


namespace uav{


ObjectBase::ObjectBase(uint16_t x, uint16_t y)
:x_cord(x),y_cord(y){

}

ObjectBase::~ObjectBase(){}



Jammer::Jammer(uint16_t x, uint16_t y,uint16_t atk_range,uint16_t atk_ability)
:ObjectBase(x,y),m_atk_range(atk_range),m_atk_ability(atk_ability)
{}

Jammer::~Jammer()
{}

Map::Target Jammer::getTargetType() const 
{ 
    return target_type; 
}

Missile_Vehicle::Missile_Vehicle(uint16_t x, uint16_t y, uint16_t atk_range,uint16_t atk_ability)
:ObjectBase(x,y),m_atk_range(atk_range),m_atk_ability(atk_ability)
{
}

Missile_Vehicle::~Missile_Vehicle(){}


Map::Target Missile_Vehicle::getTargetType() const {
    return target_type;
}

Obstacle::Obstacle(uint16_t x, uint16_t y)
:ObjectBase(x,y){
}

Obstacle::~Obstacle() {}

Map::Target Obstacle::getTargetType() const{
    return target_type;
}

void TargetManager::LoadFromJson(const std::string& filename)
{
    Json::Value root;
    Json::Reader reader;
    std::ifstream file(filename);

    if(!file.is_open()){
        std::cout << "Failed to open JSON file." << std::endl;
    }

    bool parsingSuccessful = reader.parse(file,root);

    if (!parsingSuccessful) {
        std::cout << "Failed to parse JSON file." << std::endl;
    }
    Json::Value jammers = root["jammers"];
    int idx = 1;
    for(auto& jammer:jammers){
        std::string id = "jammer_" + std::to_string(idx);
        ++idx;
        auto x = jammer["x_cord"].asUInt();
        auto y = jammer["y_cord"].asUInt();
        auto atk_range=jammer["atk_range"].asUInt();
        auto atk_ability=jammer["atk_ability"].asUInt();
        InsertTarget(id,std::make_shared<Jammer>(x,y,atk_range,atk_ability));
    }
    idx = 1;

    Json::Value missile_vehicles = root["missile_vehicles"];
    for(auto& missile_vehicle:missile_vehicles){
        std::string id = "missile_vehicle_" + std::to_string(idx);
        ++idx;
        auto x = missile_vehicle["x_cord"].asUInt();
        auto y = missile_vehicle["y_cord"].asUInt();
        auto atk_range=missile_vehicle["atk_range"].asUInt();
        auto atk_ability=missile_vehicle["atk_ability"].asUInt();
        InsertTarget(id,std::make_shared<Missile_Vehicle>(x,y,atk_range,atk_ability));
    }

    //Json::Value radars = root["radars"];
    //FillTargetMap<Jammer>(std::move(root["jammers"]),"jammer_");
    FillTargetMap<Radar>(std::move(root["radars"]),"radar_");
    FillTargetMap<AntiTurrent>(std::move(root["anti_turrents"]), "anti_turrent_");
    FillTargetMap<CommandPost>(std::move(root["command_post"]), "command_post_");
    //FillTargetMap<Obstacle>(std::move(root["obstacles"]),"obstacle_");
    
}


//对插入 Radar AntiTurrent CommandPost Obstacle的模板函数
template<typename Target>
void TargetManager::FillTargetMap(Json::Value&& arrays,const std::string& type_name){
    int idx = 1;
    for(auto& val:arrays)
    {
        std::string id = type_name + std::to_string(idx);
        idx++;
        auto x = val["x_cord"].asUInt();
        auto y = val["y_cord"].asUInt();
        InsertTarget(id,std::make_shared<Target>(x,y));
    }
}

// 对插入Jammer的偏特化
template <>
void TargetManager::FillTargetMap<Jammer>(Json::Value&& arrays, const std::string& type_name){
    int idx = 1;
    for(auto& val:arrays){
        std::string id = type_name + std::to_string(idx);
        ++idx;
        auto x = val["x_cord"].asUInt();
        auto y = val["y_cord"].asUInt();
        auto atk_range=val["atk_range"].asUInt();
        auto atk_ability=val["atk_ability"].asUInt();
        InsertTarget(id,std::make_shared<Jammer>(x,y,atk_range,atk_ability));
    }
}
/*
template <>
void TargetManager::FillTargetMap<Missile_Vehicle>(Json::Value&& arrays, const std::string& type_name){
    int idx = 1;
    for(auto& val:arrays){
        std::string id = type_name + std::to_string(idx);
        ++idx;
        auto x = val["x_cord"].asUInt();
        auto y = val["y_cord"].asUInt();
        auto atk_range=val["atk_range"].asUInt();
        auto atk_ability=val["atk_ability"].asUInt();
        InsertTarget(id,std::make_shared<Missile_Vehicle>(x,y,atk_range,atk_ability));
    }
}
*/
// 雷达结构定义
Radar::Radar(uint16_t x, uint16_t y)
:ObjectBase(x,y){
}

Radar::~Radar() {}

Map::Target Radar::getTargetType() const{
    return target_type;
}


// 防空炮的构造函数
AntiTurrent::AntiTurrent(uint16_t x, uint16_t y)
:ObjectBase(x,y){
}

AntiTurrent::~AntiTurrent() {}

Map::Target AntiTurrent::getTargetType() const{
    return target_type;
}



// 防空炮的构造函数
CommandPost::CommandPost(uint16_t x, uint16_t y)
:ObjectBase(x,y){
}

CommandPost::~CommandPost() {}

Map::Target CommandPost::getTargetType() const{
    return target_type;
}


}