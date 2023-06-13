# BattleSimulation

## 目录结构
**common** 算法所需的共用文件  
**model** 训练模型文件  
**data**  生成环境所需要的数据源  
**environment**  交互环境目录  
--------**arguments**.py 用于配置环境相关信息的参数文件  
--------**battle_simulation**.py 定义环境交互函数文件  
--------**enemy**.py 敌军目标类  
--------**utils**.py 常用函数文件  
network基本网络实现
common rl训练常用功能包
policy 具体的RL算法策略实现


### quickstart
```bash
pip -r install requirement.txt
```

### 观测空间
1. 无人机自身位置 和视野范围内的所有信息，包括敌军目标，和友军无人机
2. 如何设定才能保持恒定的纬度大小？  
按顺序遍历视野范围内的点：把地图上值代入，超出地图外的点设置为未知

### 全局状态空间
1. 所有无人机的存活状态
2. 所有target的存活状态

### 奖励函数设计
1. 移动奖励

计算移动产生的损失和奖励与上次位置相比，产生的位移为损失 
用上次位置和本次位置分别计算和指挥所的距离做差，更近则为正奖励，
更远则为负奖励 具体实现在`get_move_reward()`
2. 攻击奖励

具体实现在`get_attack_reward()`
### 自定义任务配置
在`config.py`文件中可配置`TASK_CONFIG`的信息
```python
TASK_CONFIG = {
    "total_num": 9,  # 保证下面的设置数量要和total_num相等
    "jammers": {
        "easy": 1,  # 简单难度的干扰机数量
        "medium": 0, # 中等难度的干扰机数量
        "hard": 1 # hard难度的干扰机数量
    },
    "missile_vehicles": { # 导弹车
        "easy": 1,
        "medium": 0,
        "hard": 1
    },
    "radars": { # 雷达
        "easy": 1,
        "medium": 1,
        "hard": 1
    },
    "antiairturrents": { # 防空炮
        "easy": 1,
        "medium": 0,
        "hard": 1
    }
}
```
