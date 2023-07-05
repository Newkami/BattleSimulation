

单目录单文件
CMakeLists.txt 
```cmake
# 命令如果敲对了 会变蓝色
CMAKE_MINIMUM_REQUIRED(VERSION 3.12[FATAL_ERROR]) #声明版本要求 必须

PROJECT(demo1 [CXX][C]) #可以指定项目语言

ADD_EXECUTABLE(bin_file_name ${SRC_LIST}) #表示生成可执行文件的依赖

```

单目录多文件
```cmake
# 命令如果敲对了 会变蓝色
CMAKE_MINIMUM_REQUIRED(VERSION 3.12[FATAL_ERROR]) #声明版本要求 必须

PROJECT(demo1 [CXX][C]) #可以指定项目语言

ADD_EXECUTABLE(demo2 main.cpp cmath.cpp) #表示生成可执行文件的依赖


# 如果CPP文件过多可以按这种方式
# AUX_SOURCE_DIRECTORY(dir VAR) #把dir下的所有文件打包成一个变量

AUX_SOURCE_DIRECTORY(./ DIR_SRCS)

ADD_EXECUTABLE(demo2 ${DIR_SRCS}) 
```
