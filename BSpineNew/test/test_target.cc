#include "map_target.h"
#include <iostream>

int main(int argc,char** argv){

    auto a = std::make_shared<uav::Jammer>(1,3,3,1);
    uav::ObjectBase::ptr b = std::shared_ptr<uav::ObjectBase>(new uav::Missile_Vehicle(1,3,3,1));
    auto targetMgr = std::make_shared<uav::TargetManager>();
    targetMgr->InsertTarget("uav1",a);
    targetMgr->InsertTarget("uav2",b);
    return 0;
}