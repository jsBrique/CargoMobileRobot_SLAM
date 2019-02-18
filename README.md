# 基于CoreSLAM的自动货运机器人

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

<p><h3>介绍</h3>

这是一台自动货运机器人的SLAM程序，它没有使用ROS系统，而是从驱动到算法再到前端和后端都由我本人构建的，其中CoreSLAM算法移植于[BreezySLAM](https://github.com/simondlevy/BreezySLAM),其中含有无激光雷达测试程序,机器人实物演示可参考bilibili视频[【毕业设计/移动机器人】当你想喝可乐又懒得去拿时...](https://www.bilibili.com/video/av43326289/)
<p>

<p><h3>部署</h3>

本程序使用python3编写，需要安装以下依赖,推荐使用pip安装
<pre>
eventlet==0.24.1
Flask==1.0.2
Flask-SocketIO==3.1.2
gevent==1.4.0
numpy==1.16.0
opencv-python==3.4.4.19
</pre>

然后运行
<pre>
sudo python setup.py install
</pre>
</p>

即可完成部署

<p><h3>无激光雷达测试</h3>

在brick目录下运行
<pre>
python NoLidarTest.py
</pre>

在浏览器地址栏输入对应ip与端口，默认端口为5000，如：
<pre>
192.168.88.108:5000
</pre>
即可运行测试，其中按下W可动态播放SLAM建图过程，点击地图可计算路径
</p>
<p><h3>文件说明</h3>

brick目录存放所有本人编写的程序，其他目录下均为激光雷达驱动代码<br>
目录树如下
<pre>
├── CMakeLists.txt 
├── control.py        #机器人运动控制程序，涉及串口通信，请安装pyserial
├── laser_driver.cpp  #激光雷达驱动程序
├── laser_driver.h
├── lidar_run.cpp
├── NoLidarTest.py    #无激光雷达测试程序
├── RobotRunning.py   #机器人运行程序
├── slam
│   ├── Astar.py      #Astar算法，直接运行可测试迷宫寻路
│   ├── expX.dat      #测试用的雷达数据，格式：时间戳，里程计dx，里程计dy,激光雷达点...
│   ├── __init__.py
│   ├── mines.py      #配置激光雷达参数
│   ├── OpenMap.py    #地图相关，采用opencv绘图，高效快捷
│   ├── SlamIO.py     #SLAM相关
│   └── testmap5.jpg
├── static
│   ├── css
│   ├── js
│   └── src
├── templates
│   ├── mapPhone.html  #移动端页面
│   ├── mapX.html      #桌面端页面
</pre>

</p>
<p><h3>EAI X4雷达运行</h3>

在brick目录下编译
<pre>
cmake CMakeLists.txt 
make -j4
</pre>
运行
<pre>
python RobotRunning.py
</pre>
即可启动
</p>

<p><h3>相关信息</h3>
如果你对这份代码感兴趣，欢迎加入QQ讨论群：700741375
<p>
