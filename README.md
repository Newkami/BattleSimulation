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


### 环境配置
首先安装了miniconda用于生成虚拟环境

使用目录中的requirement.txt创建conda环境
```bash
conda create --name <env> --file requirement.txt
```
**quickstart**
```bash
python3 main.py
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

修改`environment/arguments.py`中`difficulty`参数为值为3，否则自定义任务不生效


### 日志系统

1. `logger.setLevel()`：这个方法用于设置日志记录器的全局日志级别。它决定了哪些级别的日志消息将被记录。如果设置了logger.setLevel(logging.INFO)，那么只有INFO级别及以上的日志消息会被记录下来，而DEBUG级别的日志消息将被忽略。
2. `console_handler.setLevel()`：这个方法用于设置特定处理器的日志级别。它决定了将哪些级别的日志消息发送到该处理器。如果设置了console_handler.setLevel(logging.INFO)，那么只有INFO级别及以上的日志消息会被发送到控制台处理器，而DEBUG级别的日志消息将被忽略。

在示例中，`logger.setLevel(logging.INFO)`将全局的日志级别设置为INFO级别，意味着只有INFO级别及以上的日志消息会被记录。

而`console_handler.setLevel(logging.INFO)`将控制台处理器的日志级别设置为INFO级别，意味着只有INFO级别及以上的日志消息会被发送到控制台处理器，而DEBUG级别的日志消息将被忽略。