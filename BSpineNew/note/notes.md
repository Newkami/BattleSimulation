## Eigen库

```bash
sudo apt install libeigen3-dev
# 也可在官网上手动源码安装制定版本
```
在本项目中使用的是eigen3.3.7
```bash
# https://gitlab.com/libeigen/eigen/-/releases 可下在tar.gz
tar xvzf eigen-3.3.7.tar.gz
cd eigen3.3.7
mkdir build
cd build && cmake ..
make && sudo make install
```
在项目中导入Eigen包，只需要在CMakeLists.txt 添加 
```cmake
find_package(Eigen3 REQUIRED)
INCLUDE_DIRECTORIES(${EIGEN3_INCLUDE_DIR})

```
在重新cmake和编译即可


### C++优雅生成随机数
```cpp
#include <iostream>
#include <random>

int getRandomInt(int min, int max) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(min, max);
    return dist(gen);
}

int main() {
    int min = 1;
    int max = 10;
    int randomInt = getRandomInt(min, max);
    std::cout << "Random Integer: " << randomInt << std::endl;
    return 0;

/*
创建了一个 std::random_device 对象来获取随机设备的种子，然后使用 std::mt19937 引擎来生成随机数。

最后，使用 std::uniform_int_distribution 分布来指定整数的范围，并通过调用 operator() 函数来生成随机整数。
*/    
}



```

matplotlib
`imshow` 是 Matplotlib 中用于显示图像的函数。它接受以下参数：

- `X`：要显示的图像数据。可以是一个 2D 数组（灰度图像）或一个 3D 数组（彩色图像）。对于灰度图像，`X` 的形状可以是 `(M, N)`，其中 `M` 是图像的行数，`N` 是图像的列数。对于彩色图像，`X` 的形状应为 `(M, N, 3)` 或 `(M, N, 4)`，其中最后一维是 RGB（或 RGBA）颜色通道。

- `cmap`：用于颜色映射的字符串或 `Colormap` 对象。默认情况下，它使用灰度映射（对于灰度图像）或 RGB 映射（对于彩色图像）。常用的颜色映射包括 `"gray"`（灰度图像），`"jet"`（彩色热图），`"viridis"`（彩色渐变图）等。

- `norm`：用于归一化数据的 `Normalize` 对象。它将图像数据映射到 [0, 1] 范围内，默认情况下，使用线性归一化。

- `aspect`：图像的宽高比。可以设置为 `"auto"`（默认值）以自动调整宽高比，或设置为一个数值以指定固定的宽高比。

- `interpolation`：插值方法，用于图像的放缩和平滑。常用的选项包括 `"nearest"`（最近邻插值），`"bilinear"`（双线性插值），`"bicubic"`（双三次插值）等。

- `alpha`：图像的透明度。可以设置为一个范围在 [0, 1] 的值，其中 0 表示完全透明，1 表示完全不透明。

- `vmin` 和 `vmax`：用于设置颜色映射范围的最小值和最大值。在显示图像时，像素值会根据 `vmin` 和 `vmax` 进行归一化。
