cmake_minimum_required(VERSION 3.12)  # 这一行是必须的
project(BSpine_test)

# 设置c++编译器语言标准版本11以上
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# 添加调试相关的编译选项
SET(CMAKE_BUILD_TYPE "Debug")
SET(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -Wall -g2 -ggdb")
SET(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -O3 -Wall")

set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)

# 查找 Eigen3
find_package(Eigen3 REQUIRED)
if((Eigen3_FOUND) AND (DEFINED EIGEN3_INCLUDE_DIR))
 message(STATUS "Found Eigen3: " ${EIGEN3_INCLUDE_DIR})
 INCLUDE_DIRECTORIES(${EIGEN3_INCLUDE_DIR})
else()
 message(FATAL_ERROR "EIGEN3 not found.")
endif()

find_package(PythonLibs REQUIRED)
# 是否需要numpy
find_package(Python3 COMPONENTS NumPy)

find_package(PkgConfig REQUIRED)
pkg_check_modules(JSONCPP jsoncpp)
message("${JSONCPP_LIBRARIES}")
link_libraries(${JSONCPP_LIBRARIES}) # 连接库

# include("${matplotlib_cpp_CMAKE_DIR}/matplotlib_cppTargets.cmake")
include_directories(${PYTHON_INCLUDE_DIRS}) #这才是关键地方！！！
include_directories(${PROJECT_SOURCE_DIR}/include)



set(SRC_LIST
	src/BSpline.cc
	src/riskesdfMap.cc
	src/map_target.cc
	src/algorithm.cc
)

set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

add_library(bspline 
			SHARED ${SRC_LIST} 
)


add_executable(test_matplot test/test_matplot.cc)
target_include_directories(test_matplot PRIVATE ${Python3_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS})
target_link_libraries(test_matplot Python3::Python ${PYTHON_LIBRARIES} Python3::NumPy)

add_executable(test_bspline test/test_spline.cc)
# target_include_directories(test_bspline PRIVATE ${Python3_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS})
target_link_libraries(test_bspline bspline Python3::Python Python3::NumPy jsoncpp)


add_executable(test_map test/test_map.cc)
target_link_libraries(test_map bspline Python3::Python Python3::NumPy)

add_executable(test_esdf test/test_esdf.cc)
target_link_libraries(test_esdf bspline Python3::Python Python3::NumPy)

add_executable(test_target test/test_target.cc)
target_link_libraries(test_target bspline Python3::Python Python3::NumPy jsoncpp)

add_executable(test_risk test/test_risk.cc)
target_link_libraries(test_risk bspline Python3::Python Python3::NumPy jsoncpp)

add_executable(test_json test/test_json.cc)
target_link_libraries(test_json bspline Python3::Python Python3::NumPy jsoncpp)


add_executable(test_avoid test/test_avoidRisk.cc)
target_link_libraries(test_avoid bspline Python3::Python Python3::NumPy ${JSONCPP_LIBRARIES})

add_executable(test_alg test/test_algorithm.cc)
target_link_libraries(test_alg bspline Python3::Python Python3::NumPy ${JSONCPP_LIBRARIES})