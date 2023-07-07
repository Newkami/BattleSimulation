# BattleSimulation

## 目录结构

**common** 算法所需的常用文件
—— **arguments**.py  用于配置训练的参数信息
**model** 训练模型文件  

**result** 训练结果文件夹

**data**  生成环境所需要的数据源  
**environment**  交互环境目录  

——**test** 测试文件

——**arguments**.py 用于配置环境相关信息的参数文件  
——**battle_simulation**.py 定义环境交互函数文件  
——**enemy**.py 敌军目标类  
——**utils**.py 常用函数文件  
——**log_config.py** 日志配置文件（未实现）
——**data_generation**.py 数据生成用于配置

**BSPlineNew** C++实现的RiskMap和B样条曲线

policy netword agent为具体MARL算法实现


### 环境配置

1. 安装了miniconda用于生成虚拟环境

2. 安装依赖

```bash
pip3 install -r requirements.txt
pip3 install openpyxl
```

**quickstart**

```bash
python3 main.py
```

任务中内置了三种难度分别为**easy、medium、hard** 分别对应environment/arguments.py 中difficulty的参数值为**0，1，2** 数据皆从data目录中获取，自定义战斗可参考自定义任务配置

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

若修改了这些目标的数量，需要将environment/arguments.py中的n_jammers,n_radars...修改为对应的数值

common/arguments.py 中 `is_plot` 设置为True即可打开训练过程中的画图模块

若要选择模型查看模型效果将参数中的`load_model`设为True，并设定`load_model_num`为你想要的第几次模型

若要修改作战内部参数也可修改environment/arguments.py文件中的参数，比如基础血量，无人机攻击伤害、无人机攻击范围等

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




### 日志系统

1. `logger.setLevel()`：这个方法用于设置日志记录器的全局日志级别。它决定了哪些级别的日志消息将被记录。如果设置了logger.setLevel(logging.INFO)，那么只有INFO级别及以上的日志消息会被记录下来，而DEBUG级别的日志消息将被忽略。
2. `console_handler.setLevel()`：这个方法用于设置特定处理器的日志级别。它决定了将哪些级别的日志消息发送到该处理器。如果设置了console_handler.setLevel(logging.INFO)，那么只有INFO级别及以上的日志消息会被发送到控制台处理器，而DEBUG级别的日志消息将被忽略。

在示例中，`logger.setLevel(logging.INFO)`将全局的日志级别设置为INFO级别，意味着只有INFO级别及以上的日志消息会被记录。

而`console_handler.setLevel(logging.INFO)`将控制台处理器的日志级别设置为INFO级别，意味着只有INFO级别及以上的日志消息会被发送到控制台处理器，而DEBUG级别的日志消息将被忽略。


#BSplineNew#
##环境搭建##
用到了外部库jsoncpp、eigen3、画图模块用到了matplotlibcpp(该库只是通过cpp调用matplotlib 所以要保证环境中安装了numpy python3)
```bash
sudo apt install libjsoncpp-dev
sudo apt install libeigen3-dev
```
###matplotlibcpp###
配置过程比较麻烦====

##quickstart##
```bash
cd BSplineNew
mkdir build
cmake ..
make
# bin目录下会生成相应的测试文件
```
