"""
文件说明：SLAM算法封装程序，运行本文件可以测试建图过程
作者:DoppioBrique
了解更多这份代码有关信息
欢迎关注我的b站账户：砖砖哟
或者加入技术讨论群：700741375
"""
# Map size, scale
MAP_SIZE_PIXELS          = 600
MAP_SIZE_METERS          = 20

from breezyslam.algorithms import Deterministic_SLAM, RMHC_SLAM
from mines import MinesLaser, load_data,load_data_EAI
import numpy as np
from OpenMap import OpenMap
from sys import argv, exit
from time import sleep
import time
from threading import Thread

# Basic params
_DEFAULT_MAP_QUALITY         = 2 # out of 255
_DEFAULT_HOLE_WIDTH_MM       = 320

# Random mutation hill-climbing (RMHC) params
_DEFAULT_SIGMA_XY_MM         = 100
_DEFAULT_SIGMA_THETA_DEGREES = 25
_DEFAULT_MAX_SEARCH_ITER     = 1000

class SLAM_Engine:
    def __init__(self,size_pixels,size_meters):
        self.map_size_pixels=size_pixels
        self.map_size_meters=size_meters
        self.map_scale_meters_per_pixel = float(size_meters) / float(size_pixels)
        self.mapbytes = bytearray(self.map_size_pixels * self.map_size_pixels)
        self.robot = None
        self.control=False
        self.lidarShow=True
        self.routine=False
        #slam算法初始化
        self.slam = RMHC_SLAM(
                            MinesLaser(), 
                            self.map_size_pixels, 
                            self.map_size_meters,
                            map_quality=_DEFAULT_MAP_QUALITY, 
                            hole_width_mm=_DEFAULT_HOLE_WIDTH_MM, 
                            random_seed=999,
                            sigma_xy_mm=_DEFAULT_SIGMA_XY_MM, 
                            sigma_theta_degrees=_DEFAULT_SIGMA_THETA_DEGREES, 
                            max_search_iter=_DEFAULT_MAX_SEARCH_ITER)

        self.map_view=OpenMap( self.map_size_pixels, self.map_size_meters)
        self.pose = [0,0,0]
        

    def set_auto_control(self):
        self.control=True

    def reset_auto_control(self):
        self.control=False
        self.map_view.path=[]
        self.map_view.point_list=[]
    
    def data_test(self,dataset='expX'):
        timestamps, lidars, odometries = load_data_EAI('.', dataset)
        for scanno in range(len(lidars)):
            self.slam_run(lidars[scanno])
            self.slam_view()

    def NoLidarInit(self,dataset='expX'):
        self.timestamps, self.lidars, self.odometries = load_data_EAI('.', dataset)
        self.SLAM_continue=False

    def NoLidarGetScans(self):
        scans_m=[]
        if len(self.lidars)>1:
            scans=self.lidars.pop(0)
            
            for scan in scans:
                scans_m.append(float(scan)/1000.0)
            return scans,scans_m
        else:
            scans=self.lidars[0]
            for scan in scans:
                scans_m.append(float(scan)/1000.0)
            return scans,scans_m


    def routine_switch(self):
        self.map_view.path=self.map_view.routinePath.copy()
        self.map_view.routinePath.reverse()
        self.map_view.END_flag=False

    def slam_control(self):
        if self.control==True:
            return self.map_view.track_control()
        else:
            return 





    def slam_run(self,scans):
        
        self.slam.update(scans)#地图更新
        self.pose[0],self.pose[1],self.pose[2] = self.slam.getpos() #位置预测
        self.slam.getmap(self.mapbytes)#地图读取
        self.map_view.setPose(self.pose[0]/1000.,self.pose[1]/1000.,self.pose[2])

        

    def slam_view(self):
        self.map_view.display(
                            self.pose[0]/1000., 
                            self.pose[1]/1000., 
                            self.pose[2], 
                            self.mapbytes,
                            test=False)

    def slam_mjpg(self):
        s = self.map_scale_meters_per_pixel
        self.map_view.display_mjpg(
                            self.pose[0]/1000., 
                            self.pose[1]/1000., 
                            self.pose[2], 
                            self.mapbytes,
                            test=False)
        pos=[self.map_size_pixels-int((self.pose[0]/1000.)/s),
        int((self.pose[1]/1000.)/s),self.pose[2]]
        return self.map_view.get_jpg(),pos

    def setPoint(self,x,y):
        return self.map_view.setPoint(self.map_size_pixels-x,y)

    def _m2pix(self, x_m, y_m):
        s = self.map_scale_meters_per_pixel
        #p = self.map_size_pixels
        return int(x_m/s), int(y_m/s)

if __name__ == "__main__":
    slam=SLAM_Engine(MAP_SIZE_PIXELS,MAP_SIZE_METERS)
    slam.data_test()


    