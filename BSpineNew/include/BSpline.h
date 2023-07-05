#pragma once

#include<iostream>
#include <cmath>
#include <ctime>
#include<vector>
#include <Eigen/Core>
using namespace std;


constexpr auto Swidth = 1000;
constexpr auto Sheight = 1200;
constexpr auto deltaTIME = 50;

enum Type//B样条类型
{
	uniform,//均匀
	quniform//准均匀
};

class Point//点
{
public:
	double x;
	double y;
    Point(double x_,double y_)
    :x(x_),y(y_)
    {}
};

class BSpline{
public:
    BSpline(int _k, int _type, vector<Point> _p, bool _bDelayShow);
    ~BSpline();
    void delay(int time);
    // 计算每个i和每个u对应的B样条
    double BsplineBfunc(int i, int k, double uu);
    const std::vector<Point>& getpTrack() const {return pTrack;}
    const std::vector<Point>& getControlPoint() const {return p;}
    void createBspline(); //计算整个B样条
public:
    int k; //阶数
    int n; //controlPoints num -1
    int type; //B样条的类型
    vector<double> u; //自变量
    double delta_u = 0.01;//自变量间隔
    double uBegin;
	double uEnd;
	vector<Point> p;//控制点
	vector<Point> pTrack;//轨迹点
	bool bDelayShow = true;//是否显示曲线生成的过程
};

class BSpineTest{
public:
	void setPoint(vector<Point>& p);//定义点
	void myBsplineTest();//任意点测试
	void setPointHeart(vector<Point>& p1, vector<Point>& p2);//定义心形点
	void BsplineHeart();//画心

    void controlPTest();

    void initMap(Eigen::MatrixXd& map);
    void avoidRiskAreaTest(Eigen::MatrixXd& map,Eigen::Vector2d& start_point,Eigen::Vector2d& end_point,double min_risk_val);

    void plotTrackandControlP(const std::vector<Point>& pTrack, const std::vector<Point>& p ,const Eigen::MatrixXd &matrix);

    
};