"""
文件说明：无雷达测试程序，在前端按W播放动画
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
import numpy as np
from threading import Thread
from threading import Lock
#Web框架
from flask import Flask, render_template, session, request,Response
from flask_socketio import SocketIO, emit

sys.path.append('slam/') 
from slam.SlamIO import SLAM_Engine 

import re

MAP_SIZE_PIXELS          = 800
MAP_SIZE_METERS          = 25

data_list=[1]*720
data_list_xy=[1]*1440

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
slam=SLAM_Engine(MAP_SIZE_PIXELS,MAP_SIZE_METERS)
slam.NoLidarInit()
data_list,_=slam.NoLidarGetScans()
slam.slam_run(data_list)
@app.route('/', methods = ['POST'])
def eventData():
	global data_list
	msg=request.get_data().decode()
	X_p = re.compile('(?<=\\()[^}]*(?=,)')
	Y_p = re.compile('(?<=,)[^}]*(?=\\))')
	if msg=='F':
		slam.SLAM_continue=True
		
	if msg=='S':
		slam.SLAM_continue=False
		slam.reset_auto_control()
		#slam.reset_auto_control()
	
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

# 与前端建立 socket 连接后，启动后台线程
@socketio.on('connect', namespace='/test')
def test_connect():
	print("websocket connect!")

@app.route('/')
def index():
	#返回操控页面，分为手机端和桌面端
	pf=request.user_agent.platform
	print(pf)
	if pf!='windows':
		return render_template('mapPhone.html', async_mode=socketio.async_mode)
	else:
		return render_template('mapX.html', async_mode=socketio.async_mode)

@app.route('/video_feed')  # 这个地址返回视频流响应
def video_feed():
	data=slam_gen()
	return Response(data,mimetype='multipart/x-mixed-replace; boundary=frame')


def slam_gen():
	global slam,data_list
	pos=[0,0,0]
	
	while True:
		socketio.sleep(0.05)
		if slam.SLAM_continue==True:
			data_list,data_m=slam.NoLidarGetScans()
			slam.slam_run(data_list)
			socketio.emit('server_response',
						{'data':data_m,'pos': pos},
						namespace='/test',broadcast=True)
			socketio.sleep(0.05)
		frame,pos=slam.slam_mjpg()
		# 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def SLAM_process():
	global slam
	
	time.sleep(1)
	print("web running!")
	#Data_thread()
	socketio.run(app,host='0.0.0.0', port=5000, debug=False)


def EXIT_Handler(signal,frame):
	print('\nExit!')
	sys.exit(0)

signal.signal(signal.SIGINT,EXIT_Handler)
proc_SLAM=mpro.Process(target = SLAM_process)
proc_SLAM.start()
print("running")
proc_SLAM.join()
