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
  
 # CoreSLAM-based automatic cargo robot

[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

<p><h3>Introduction</h3>

This is an SLAM program for an automatic cargo robot. It does not use the ROS system. It is built from the driver to the algorithm to the front end and the back end. The CoreSLAM algorithm is ported to [BreezySLAM](https://github.com/simondlevy/BreezySLAM), which contains no laser radar test program, the robot physical demonstration can refer to bilibili video[【毕业设计/移动机器人】当你想喝可乐又懒得去拿时...](https://www.bilibili.com/video/av43326289/)
<p>

<p><h3>Install</h3>

This program is written in python3, you need to install the following dependencies, it is recommended to use pip to install.
<pre>
eventlet==0.24.1
Flask==1.0.2
Flask-SocketIO==3.1.2
gevent==1.4.0
numpy==1.16.0
opencv-python==3.4.4.19
</pre>

then run
<pre>
sudo python setup.py install
</pre>
</p>

You can complete the install.

<p><h3>Test program without lidar</h3>

Running in the /brick
<pre>
python NoLidarTest.py
</pre>

Enter the corresponding ip and port in the address bar of the browser. The default port is 5000, such as:
<pre>
192.168.88.108:5000
</pre>
You can run the test, press W to dynamically play the SLAM drawing process, click on the map to calculate the path
</p>
<p><h3>Document description</h3>

The brick directory stores all the programs I have written, and the other directories are the lidar driver code<br>
Directory tree is as follows
<pre>
├── CMakeLists.txt 
├── control.py        #robot motion control program, involving serial communication, please install pyserial
├── laser_driver.cpp  #lidar driver
├── laser_driver.h
├── lidar_run.cpp
├── NoLidarTest.py    #test program without lidar
├── RobotRunning.py   #Robot running program
├── slam
│   ├── Astar.py      #Astar algorithm, direct run test maze pathfinding
│   ├── expX.dat      #lidar data for testing, format: time stamp, odometer dx, odometer dy, lidar point...
│   ├── __init__.py
│   ├── mines.py      #Configuring lidar parameters
│   ├── OpenMap.py    #Map related, using opencv drawing, efficient and fast
│   ├── SlamIO.py     #SLAM related
│   └── testmap5.jpg
├── static
│   ├── css
│   ├── js
│   └── src
├── templates
│   ├── mapPhone.html  #Mobile page
│   ├── mapX.html      #PC page
</pre>

</p>
<p><h3>EAI X4 Lidar operation</h3>

Compile in the /brick
<pre>
cmake CMakeLists.txt 
make -j4
</pre>
run
<pre>
python RobotRunning.py
</pre>
Can start it.
</p>

<p><h3>Related Information</h3>
If you are interested in this code, welcome to join the QQ discussion group.：700741375
<p>

