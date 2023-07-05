#include "BSpline.h"
#include "algorithm.h"
#include "matplotlibcpp.h"
namespace plt = matplotlibcpp;

BSpline::BSpline(int _k,int _type,vector<Point> _p, bool _bDelayShow)
:bDelayShow(_bDelayShow),k(_k),n(_p.size()-1),type(_type)
{
    if(k>n+1 || _p.empty())  //阶数必须小于等于n+1（控制点个数）
    {
        cout << "error!" << endl;
		system("pause");
		exit(0);
    }

    p = _p;

    double u_tmp = 0.0;
    u.push_back(u_tmp);

    if(type == uniform)
    {
        double dis_u = 1.0/(n+k);
        for(int i=1;i<n+k+1;++i)
        {
            u_tmp += dis_u;
			u.push_back(u_tmp);
        }
    }
    else if(type == quniform) //准均匀
    {
        int j = 3;//重复度 即头尾端点的重复个数
        double dis_u = 1.0 / (k + n - (j - 1) * 2); //去掉重复度的u范围该如何界定
        for(int i=1;i<j;++i)
        {
            u.push_back(u_tmp);
        }
        for (int i = j; i < n + k - j + 2; i++)
		{
			u_tmp += dis_u;
			u.push_back(u_tmp);
		}
		for (int i = n + k - j + 2; i < n + k + 1; i++)//n + k + 1个分段
		{
			u.push_back(u_tmp);
		}
    }

    if(!bDelayShow) //无人驾驶用
        delta_u = 0.02;
    /*debug 信息*/
    cout << "阶数：" << k << ", 控制点数：" << n + 1 << endl;
	cout << "delta_u= " << delta_u << ", u的序列为：";
    for (int i = 0; i < u.size(); i++)
	{
		cout << u[i] << ", ";
	}
	cout << endl;
    /*debug 信息*/
    uBegin = u[k - 1];
	uEnd = u[n + 1];//计算u的区间

    /*debug 信息*/
	cout << "uBegin= " << uBegin << ", uEnd= " << uEnd << endl;


    // 画图模块

}

BSpline::~BSpline(){
    p.clear();
    u.clear();
    pTrack.clear();
}

void BSpline::delay(int time) //延时函数，单位ms
{
	clock_t  now = clock();
	while (clock() - now < time){}
}

double BSpline::BsplineBfunc(int i, int k, double uu)//计算每个u和每个i对应的B样条基函数
{
    double Bfunc = 0.0;
    if(k == 1)
    {
        if (u[i] <= uu && uu < u[i + 1])
			Bfunc = 1.0;
		else
			Bfunc = 0.0;
    }
    else if (k >= 2)
	{
		double A = 0.0;
		double B = 0.0;

		if (u[i + k - 1] - u[i] == 0.0)
		{
			//cout << "A = 0.0; u[i+k-1]= " << u[i + k - 1] << ", u[i]= " << u[i] << endl;
			A = 0.0;//约定分母为0时，整个除式为0
		}
		else
		{
			A = (uu - u[i]) / (u[i + k - 1] - u[i]);
				
			/*if (A <= 0.0)
			{
				cout << "A < 0.0; A= " << A << ", uu= " << uu << ", u[i]= " << u[i] << ", u[i + k - 1]= " << u[i + k - 1] << ", i= " << i << ", k= " << k << endl;
			}*/
		}

		if (u[i + k] - u[i + 1] == 0.0)
		{
			//cout << "B = 0.0; u[i + k]= " << u[i + k] << ", u[i + 1] " << u[i + 1] << endl;
			B = 0.0;//约定分母为0时，整个除式为0
		}
		else
		{
			B = (u[i + k] - uu) / (u[i + k] - u[i + 1]);

			/*if (B <= 0.0)
			{
				cout << "B < 0.0; B= " << B << ", uu= " << uu << ", u[i]= " << u[i] << ", u[i + k]= " << u[i + k] << ", u[i + 1]= " << u[i + 1] << ", i= " << i << ", k= " << k << endl;
			}*/
		}
		Bfunc = A * BsplineBfunc(i, k - 1, uu) + B * BsplineBfunc(i + 1, k - 1, uu);//递归
	}

	//cout << "Bfunc= " << Bfunc << endl;
	return Bfunc;
}

void BSpline::createBspline(){

    for(double uu = uBegin;uu<=uEnd; uu+= delta_u){
        Point Pu = {0.0,0.0}; //每轮循环初始化
        for (int i = 0; i < n + 1; i++)//i从0到n，每个控制点
		{
			double xtmp = p[i].x;
			double ytmp = p[i].y;
			double BfuncTmp = BsplineBfunc(i, k, uu);
			Pu.x += xtmp * BfuncTmp;
			Pu.y += ytmp * BfuncTmp;//累加
		}
        pTrack.push_back(Pu);
    }
    cout << "track point: " << endl;
    
}


void BSpineTest::setPoint(vector<Point>& p)//定义点
{
	p.push_back(Point{ 100.0, 300.0 });
	p.push_back(Point{ 200.0, 100.0 });
	p.push_back(Point{ 300.0, 200.0 });
	p.push_back(Point{ 400.0, 50.0 });
	p.push_back(Point{ 550.0, 100.0 });
	p.push_back(Point{ 600.0, 350.0 });
	p.push_back(Point{ 700.0, 350.0 });
}

void BSpineTest::myBsplineTest()//任意点测试
{
	vector<Point> pcontrol;
	setPoint(pcontrol);

	BSpline test(3, quniform, pcontrol, true);
	test.createBspline();
}

void BSpineTest::initMap(Eigen::MatrixXd &map)
{
	map.resize(50,50);
	double x = 15;
	double y = 15;
	
	int r = 3;
	int minX = x-r;
	int maxX = x+r;
	int minY = y - r;
    int maxY = y + r;

    // 创建一个二维矩阵，并初始化为0
    int width = maxX - minX + 1;
    int height = maxY - minY + 1;
    std::vector<std::vector<int>> matrix(height, std::vector<int>(width, 0));

    // 遍历矩阵中的每个点，计算该点与圆心的距离，并赋值
    for (int i = 0; i < height; ++i) {
        for (int j = 0; j < width; ++j) {
            int pointX = j + minX;
            int pointY = i + minY;
            double distance = std::hypot(pointX - x, pointY - y);
			if(distance<=r)
			{
            	// 根据距离计算赋值
				map(pointX,pointY) = distance/r * 0.99;
			}
        }
    }
	map(x,y) = 0.99;
    // 输出结果
	
}


void BSpineTest::avoidRiskAreaTest(Eigen::MatrixXd &map, Eigen::Vector2d &start_point, Eigen::Vector2d &end_point, double min_risk_val)
{
	
	initMap(map);
	std::vector<double> x_cord;
	std::vector<double> y_cord;
	
	for(int x=0;x<map.rows();++x)
	{
		for(int y=0;y<map.cols();++y)
		{
			if(map(x,y)!=0)
			{
				x_cord.push_back(x);
				y_cord.push_back(y);
			}
		}
	}

	std::map<std::string, std::string> key;
	key["color"] = "r";
	std::vector<double> special_points_x;
	std::vector<double> special_points_y;
	special_points_x.push_back(start_point.x());
	special_points_x.push_back(end_point.x());
	special_points_y.push_back(start_point.y());
	special_points_y.push_back(end_point.y());
	//plt::scatter(special_points_x,special_points_y,10,key);
	//plt::scatter(x_cord,y_cord,10);
	
	/*avoidRiskArea阶段*/
	// step1 searchChannel
	auto unit_v = (end_point-start_point).normalized(); //获取单位向量 即起始点的方向
	Eigen::Vector2d left_v(-unit_v.y(), unit_v.x());  // 左垂直单位向量
    Eigen::Vector2d right_v(unit_v.y(), -unit_v.x());  // 右垂直单位向量
	
	//获取圆心和半径
	Eigen::Vector2d center(15,15);
	double radius = 3.0;
	//获取与圆形禁飞区的交点
	auto intersec = uav::calculateIntersection(start_point,unit_v,center,radius);
	double scale = radius/right_v.norm()+0.2;
	//存在两个交点
	Eigen::Vector2d control3(center.x()+(scale*left_v.x())-1.0,center.y()+(scale*left_v.y())+1.0);
	Eigen::Vector2d control4(center.x()+(scale*-1.0)-1-0.5,center.y()+0.0);
	/*画图测试点*/
	plt::scatter(vecX(control4),vecY(control4),20);
	// plt::scatter(vecX(intersec.first),vecY(intersec.first),20);
	// plt::scatter(vecX(intersec.second),vecY(intersec.second),20);
	
	plt::quiver(std::vector<double>{start_point.x(),start_point.x(),start_point.x()},
			std::vector<double>{start_point.y(),start_point.y(),start_point.y()},
			std::vector<double>{unit_v.x(),left_v.x(),right_v.x()},
			std::vector<double>{unit_v.y(),left_v.y(),right_v.y()}
	);


    int numPoints = 100; // 圆上的采样点数

    std::vector<double> x(numPoints);
    std::vector<double> y(numPoints);

    // 计算圆上的坐标点
    for (int i = 0; i < numPoints; ++i) {
        double angle = 2 * M_PI * i / numPoints;
        x[i] = center.x() + radius * std::cos(angle);
        y[i] = center.y() + radius * std::sin(angle);
    }
    // 绘制圆
    plt::plot(x, y, "C0");

	/*生成B样条曲线*/
	std::vector<Point> controlPoints;

	controlPoints.emplace_back(start_point.x(),start_point.y());
	controlPoints.emplace_back(intersec.first.x()-0.5,intersec.first.y()-0.5);
	controlPoints.emplace_back(control3.x(),control3.y());
	// controlPoints.emplace_back(12.445-0.5,16.5707+0.5);
	// controlPoints.emplace_back(12.0949,17.9132);
	// controlPoints.emplace_back(14.0666-0.5,17.8457+0.5);
	controlPoints.emplace_back(intersec.second.x()-0.5,intersec.second.y()+0.5);
	controlPoints.emplace_back(end_point.x(),end_point.y());

	for(auto p : controlPoints){
		std::cout<<"["<<p.x<<","<<p.y<<"],";
	}
	BSpline b_spline(3, quniform, controlPoints, true);
	b_spline.createBspline();
	plt::axis("off");
	plt::axis("equal");
	
	plt::show();
}

void BSpineTest::plotTrackandControlP(const std::vector<Point>& pTrack, const std::vector<Point>& p ,const Eigen::MatrixXd &matrix)
{

	std::vector<double> x_point(pTrack.size());
    std::vector<double> y_point(pTrack.size());
	for (size_t i = 0;i<pTrack.size();++i)
	{
        x_point[i] = pTrack[i].x;
        y_point[i] = pTrack[i].y;
		cout << "(" << pTrack[i].x << ", " << pTrack[i].y << ") ";
	}
	cout << endl;
    plt::scatter(x_point, y_point, 10);

	std::vector<double> x_controlP;
	std::vector<double> y_controlP;
	for(auto a:p){
		x_controlP.push_back(a.x);
		y_controlP.push_back(a.y);
	}
	plt::scatter(x_controlP, y_controlP, 10);

	std::vector<int> x_risk;
	std::vector<int> y_risk;
	for (int i = 1; i < matrix.rows()-1; ++i) {
        for (int j = 1; j < matrix.cols()-1; ++j) {
			if(matrix(i,j)!=0){
				x_risk.push_back(i);
				y_risk.push_back(j);
			}
        }
    }

	plt::scatter(x_risk, y_risk, 10);
	plt::show();
}
