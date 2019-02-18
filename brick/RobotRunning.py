"""
文件说明：机器人运行的主程序
作者:DoppioBrique
了解更多这份代码有关信息
欢迎关注我的b站账户：砖砖哟
或者加入技术讨论群：700741375
"""
from ctypes import *
import os
import multiprocessing as mpro
import time
import sys
import signal

import matplotlib.pyplot as plt
import numpy as np
from threading import Thread
from threading import Lock
from control import Car
from flask import Flask, render_template, session, request,Response
from flask_socketio import SocketIO, emit
sys.path.append('slam/') 
from slam.SlamIO import SLAM_Engine 
import re
MAP_SIZE_PIXELS          = 800
MAP_SIZE_METERS          = 25

libLidar=cdll.LoadLibrary('./liblidar_run.so')#C++激光雷达驱动文件


#data_theta=[1]*720
data_list=[1]*720

data_list_xy=[1]*1440
#取点函数，与雷达有关
def get_dot_xy():
	global libLidar,data_list_xy
	
	data_px=libLidar.Lidar_Scan_X()
	data_py=libLidar.Lidar_Scan_Y()

	datax=cast(data_px,POINTER(c_float))
	datay=cast(data_py,POINTER(c_float))
	for i in range(720):
		data_list_xy[i]=datax[i]
		data_list_xy[i+720]=datay[i]		

	libLidar.Lidar_Scan_Get_Finish()
	return data_list_xy

def get_dot_m():
	global libLidar,data_list
	data_p=libLidar.Lidar_Scan_Get()
	data=cast(data_p,POINTER(c_float))
	
	for i in range(720):
		data_list[i]=data[i]
		

	libLidar.Lidar_Scan_Get_Finish()
	return data_list

def get_dot_SLAM():
	global libLidar,data_list
	data_p=libLidar.Lidar_Scan_Get()
	data=cast(data_p,POINTER(c_float))
	
	for i in range(720):
		data_list[i]=int(data[i]*1000)

	libLidar.Lidar_Scan_Get_Finish()
	return data_list

#####################web服务(有装饰器不会写成类qwq)######################
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
slam=SLAM_Engine(MAP_SIZE_PIXELS,MAP_SIZE_METERS)
robot=Car()



@app.route('/', methods = ['POST'])
def eventData():
	
	msg=request.get_data().decode()

	X_p = re.compile('(?<=\\()[^}]*(?=,)')
	Y_p = re.compile('(?<=,)[^}]*(?=\\))')

	if msg=='S':
		robot.Stop()
	if msg=='F':
		robot.Forward()
	if msg=='B':
		robot.Backward()	
	if msg=='Q':
		robot.Left()
	if msg=='E':
		robot.Right()
	if msg=='L':
		robot.LL()
	if msg=='R':
		robot.RR()
	if msg=='O':
		slam.lidarShow=True
	if msg=='P':
		slam.lidarShow=False
	if msg=='H':
		slam.reset_auto_control()
		robot.Stop()
		
	if msg[0]=='C':
		if msg[1]!='S':
			coords=msg[1:]
			try:
				X_g=re.search(X_p,coords)
				Y_g=re.search(Y_p,coords)
				x=int(X_g.group())
				y=int(Y_g.group())
				
			except:
				print("Coord Error!!!!")
				print(msg)
			slam.routine=False
			res=slam.setPoint(x,y)
			print(res)
			if res==True:
				slam.set_auto_control()
			else:
				slam.reset_auto_control()
			print(msg[1:])
		else:
			coords=msg[2:]
			
			try:
				X_g=re.search(X_p,coords)
				Y_g=re.search(Y_p,coords)
				x=int(X_g.group())
				y=int(Y_g.group())
				
			except:
				print("Coord Error!!!!")
				print(msg)
			slam.routine=True
			res=slam.setPoint(x,y)
			print(res)
			if res==True:
				slam.set_auto_control()
			else:
				slam.reset_auto_control()
			print(msg[1:])

		

	
	return "200"


@app.route('/')
def index():
	pf=request.user_agent.platform
	print(pf)
	if pf!='windows':
		return render_template('mapPhone.html', async_mode=socketio.async_mode)
	else:
		return render_template('mapX.html', async_mode=socketio.async_mode)

	# 与前端建立 socket 连接后，启动后台线程
@socketio.on('connect', namespace='/test')
def test_connect():
	print("websocket connect!")


@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
	data=slam_gen()
	return Response(data,mimetype='multipart/x-mixed-replace; boundary=frame')



#####################web服务END#################################	



def slam_gen():
	global slam
	pos=[0,0,0]
	while True:
		if slam.lidarShow==True:		
			data=get_dot_m()
			
			socketio.emit('server_response',
						{'data': data,'pos': pos},
						namespace='/test',broadcast=True)
			socketio.sleep(0.1)
		else:
			time.sleep(0.1)
		frame,pos=slam.slam_mjpg()
		# 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def SLAM_process():
	global slam
	slam_thread=Thread(target=SLAM_work_thread, args=(slam,))
	slam_thread.start()
	time.sleep(1)
	print("web running!")
	socketio.run(app,host='0.0.0.0', port=5000, debug=False)

def SLAM_work_thread(slam):
	while True:
		
		scans=get_dot_SLAM()
		slam.slam_run(scans)
		try:
			if slam.control==True:
				Dangle,dist,END_flag=slam.slam_control()#路径追踪
				robot.auto_control(Dangle,dist)
				if END_flag==True:
					if slam.routine==False:
						slam.reset_auto_control()
						robot.Stop()
					else:	
						slam.routine_switch()
		except:
			slam.reset_auto_control()
			robot.Stop()
		
		time.sleep(0.08)




#数据录制函数，生成expX.dat的工具
def lidar_expdata(fp,data):
	timestamp=int(time.time()*1000)-int(int(time.time()*1000)/1000000000)*1000000000
	odometry=str(timestamp) + ' 0 0'
	data_list=list(map(lambda x: int(x*1000), data))
	lidar=''
	for d in data_list:
		lidar=lidar + ' ' + str(d)

	line=odometry+lidar+'\n'
	
	fp.writelines(line)


def Ending():
	global libLidar,proc_LidarRuning,proc_LidarScan
	print('\nExit!')

	proc_LidarScan.terminate()
	proc_LidarRuning.terminate()
	
	sys.exit(0)


def signal_handler(signal,frame):
	Ending()


def Lidar_running():
	print('Lidar connecting...')
	time.sleep(2)
	libLidar.do_not_show_write()		
	libLidar.running()		

############running#############


#采用雷达运行和取雷达点分离，C++驱动内部采用共享内存和双缓存读取数据

signal.signal(signal.SIGINT,signal_handler)
proc_LidarRuning = mpro.Process(target = Lidar_running)
proc_LidarScan=mpro.Process(target = SLAM_process)
print("running")
proc_LidarRuning.start()
time.sleep(5)
libLidar.Lidar_Scan_Init()
proc_LidarScan.start()
proc_LidarRuning.join()
proc_LidarScan.join()

proc_LidarScan.terminate()
proc_LidarRuning.terminate()
