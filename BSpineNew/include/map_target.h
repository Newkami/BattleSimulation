#pragma once

#include <stdint.h>
#include <memory>
#include <unordered_map>
#include <jsoncpp/json/json.h>
#include <iostream>
#include <functional>
namespace uav{

class Map{
public:
    enum Target{
        JAMMER = 1,
        MISSILE_VEHICLE = 2,
        RADAR = 3,
        ANTITURRENT = 4,
        COMMANDPOST = 5,
        MULTIROTOR = 6,
        OBSTACLE = -1
    };
};


class ObjectBase{
public:
    typedef std::shared_ptr<ObjectBase> ptr;
    ObjectBase(uint16_t x,uint16_t  y);
    virtual ~ObjectBase() = 0;

    uint16_t getXCord() const {return x_cord;}
    uint16_t getYCord() const {return y_cord;}
    virtual Map::Target getTargetType() const = 0;
private:
    uint16_t x_cord;
    uint16_t y_cord;
};

class Jammer:public ObjectBase
{
public:
    typedef std::shared_ptr<Jammer> ptr;

    Jammer(uint16_t x, uint16_t y,uint16_t atk_range,uint16_t atk_ability); 
    ~Jammer() override;

    Map::Target getTargetType() const override;

    void setAtkRange(uint16_t val) {m_atk_range = val;}
    uint16_t getAtkRange() const { return m_atk_range;}

    void setAtkAbility(uint16_t val) {m_atk_ability = val;}
    uint16_t getAtkAbility() const { return m_atk_ability;}
private:
    std::string id;
    uint16_t m_atk_range;
    Map::Target target_type = Map::Target::JAMMER;
    uint16_t m_atk_ability;
};

class Missile_Vehicle:public ObjectBase
{
public:
    typedef std::shared_ptr<Missile_Vehicle> ptr;
    Missile_Vehicle(uint16_t x, uint16_t y,uint16_t atk_range,uint16_t atk_ability); 
    ~Missile_Vehicle() override;

    Map::Target getTargetType() const override;

    void setAtkRange(uint16_t val) {m_atk_range = val;}
    uint16_t getAtkRange() const { return m_atk_range;}

    void setAtkAbility(uint16_t val) {m_atk_ability = val;}
    uint16_t getAtkAbility() const { return m_atk_ability;}
private:
    uint16_t m_atk_range;
    Map::Target target_type = Map::Target::MISSILE_VEHICLE;
    uint16_t m_atk_ability;
};

// 雷达结构定义
class Radar:public ObjectBase
{
public:
    typedef std::shared_ptr<Radar> ptr;
    Radar(uint16_t x, uint16_t y); 
    ~Radar() override;
    Map::Target getTargetType() const override;
private:
    Map::Target target_type = Map::Target::RADAR;
};


class AntiTurrent:public ObjectBase
{
public:
    typedef std::shared_ptr<AntiTurrent> ptr;
    AntiTurrent(uint16_t x, uint16_t y); 
    ~AntiTurrent() override;
    Map::Target getTargetType() const override;
private:
    Map::Target target_type = Map::Target::ANTITURRENT;
};



class CommandPost:public ObjectBase
{
public:
    typedef std::shared_ptr<CommandPost> ptr;
    CommandPost(uint16_t x, uint16_t y); 
    ~CommandPost() override;
    Map::Target getTargetType() const override;
private:
    Map::Target target_type = Map::Target::COMMANDPOST;
};

class Obstacle:public ObjectBase
{
public:
    typedef std::shared_ptr<Obstacle> ptr;
    Obstacle(uint16_t x, uint16_t y); 
    ~Obstacle() override;
    Map::Target getTargetType() const override;
private:
    Map::Target target_type = Map::Target::OBSTACLE;
};



class TargetManager{
public:
    typedef std::unordered_map<std::string, ObjectBase::ptr> TargetMap;

    
    static bool InsertTarget(const std::string& id, ObjectBase::ptr target_ptr){
        auto it = GetDatas().find(id);
        if(it!=GetDatas().end()){
            throw std::logic_error("this key has existed already");
            return false;
        }
        else{
            GetDatas().insert({id, target_ptr});
            std::cout<<"Insert Success!"<<std::endl;
            std::cout<<GetDatas()[id]->getTargetType()<<std::endl;
            return true;
        }
    }
    static void LoadFromJson(const std::string& file);

    static ObjectBase::ptr GetTargetByid(const std::string& id){
        auto it = GetDatas().find(id);
        if(it == GetDatas().end())
        {
            std::cout<<"Target Not Found"<<std::endl;
            return nullptr;
        }
        else{
            return it->second;
        }
    }
    //通过外部接口遍历Map数据
    static void Visit(std::function<void(const std::string&,ObjectBase::ptr)> func){
        for(auto it = GetDatas().begin();it!=GetDatas().end();++it)
        {
            func(it->first,it->second);
        }
    }
private:
    static TargetMap& GetDatas(){
        static TargetMap s_datas;
        return s_datas;
    }

    template<typename Target>
    static void FillTargetMap(Json::Value&& arrays,const std::string& type_name);

   
};


}