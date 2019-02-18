import cv2
import numpy as np
import time
from Astar import AstarPathPlan as As

# Map size, scale
MAP_SIZE_PIXELS          = 800
MAP_SIZE_METERS          = 20

class OpenMap:
    def __init__(self,map_size_pixels, map_size_meters,show_tra=False,zero=0):
        self.map_size_pixels = map_size_pixels
        self.map_scale_meters_per_pixel = map_size_meters / float(map_size_pixels)
        self.point_list=[]
        self.path=[]
        
    def image_read_png(self,filepath):
        #读图片测试
        self.mapimg=cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
        
    def setPoint(self,x,y):
        #设置路径
        self.END_flag=False
        print('Search Path',[self.y_p,self.x_p],[y,x])
        self.path=[]
        
        self.PathPlan=As(self.maps,display=False)        
        res=self.PathPlan.search_path([self.y_p,self.x_p],[y,x])
        self.path=self.PathPlan.find_road()

        self.routinePath=self.path.copy()
        self.routinePath.reverse()

        self.goal_node=[self.y_p,self.x_p]
        self.point_list=[]
        self.point_list.append([x,y])
        
        if res==True:
            return True
        else:
            return False

    def get_track_goal(self,D):
        if len(self.path)>0:
            if len(self.path)>=D:
                for i in range(D):
                    node=self.path.pop()
            else:
                node=self.path.pop(0)
                self.END_flag=True
            return node
        else:
            return 

    def get_distance(self,a,b):
        return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

    def angle_diff(self,a,b):
        d1=a-b
        d2=360-abs(d1)
        if d1>0:
            d2*=-1.0
        a=[d1,d2]
        return min(a,key=lambda o: abs(o))
    def get_angle(self,me,goal):
        tmp = np.rad2deg(np.arctan2(goal[1]-me[1],goal[0]-me[0]))
        if tmp<0:
            tmp=360-abs(tmp)
        return tmp
    

    def track_control(self,D=4,distTH=10):
        me=[self.y_p,self.x_p]
        if self.get_distance(me,self.goal_node)<=distTH:
            self.goal_node=self.get_track_goal(D)
        goal_angle=self.get_angle(me,self.goal_node)
        my_angle=self.get_angle(me,[self.s,self.c])
        dist=self.get_distance(me,self.goal_node)
        return self.angle_diff(my_angle,goal_angle),dist,self.END_flag

    def drawPoint(self):
        if len(self.point_list)>0:
            for point in self.point_list:
                self.mapimg=cv2.circle(self.mapimg,(point[0],point[1]),2,(0,0,255),1)

        if len(self.path)>0:
            for node in self.path:
                self.mapimg=cv2.circle(self.mapimg,(node[1],node[0]),1,(100,0,100),-1)


    def setPose(self,x_m,y_m,th,zero=0):
        x_p,y_p=self._m2pix(x_m,y_m)
        
        d=th-zero
        self.x_p,self.y_p,self.theta=x_p,y_p,d
        a = np.radians(d)
        r=9.0
        c =int( r*np.cos(a) + x_p)
        s =int(r*np.sin(a) + y_p)
        self.c,self.s=c,s

        
        

    def drawPose(self):
        self.mapimg=cv2.line(self.mapimg, (self.x_p,self.y_p), (self.c,self.s),(0,0,255), 2)
        self.mapimg=cv2.circle(self.mapimg,(self.x_p,self.y_p),5,(255,0,0),2)

    def display(self,x_m,y_m,theta,mapbytes,test=False):
        
        if test==True:
            self.image_read_png('expX.png')
        else:
            self.mapimg = np.reshape(np.frombuffer(mapbytes, dtype=np.uint8), (self.map_size_pixels, self.map_size_pixels))
        #start=time.time()
        self.mapimg=cv2.cvtColor(self.mapimg,cv2.COLOR_GRAY2BGR)        
        self.setPose(x_m,y_m,theta)
        self.drawPoint()
        self.mapimg=cv2.flip(self.mapimg, 1)
        cv2.imshow('MAP',self.mapimg)
        #print(time.time()-start)
        cv2.waitKey(1)



    def display_mjpg(self,x_m,y_m,theta,mapbytes,test=False):
        
        if test==True:
            self.image_read_png('expX.png')
        else:
            self.maps = np.reshape(np.frombuffer(mapbytes, dtype=np.uint8), (self.map_size_pixels, self.map_size_pixels))
        #start=time.time()
        self.mapimg=cv2.cvtColor(self.maps,cv2.COLOR_GRAY2BGR)        
        self.drawPose()
        self.drawPoint()
        self.mapimg=cv2.flip(self.mapimg, 1)

    def get_jpg(self):
        
        # 因为opencv读取的图片并非jpeg格式，因此要用motion JPEG模式需要先将图片转码成jpg格式图片
        ret, jpeg = cv2.imencode('.jpg', self.mapimg)
        return jpeg.tobytes()
            
        
    def _m2pix(self, x_m, y_m):

        s = self.map_scale_meters_per_pixel
        #p = self.map_size_pixels
        return int(x_m/s), int(y_m/s)

def main():
    map_vis=OpenMap(MAP_SIZE_PIXELS, MAP_SIZE_METERS)
    
    map_vis.display(10,10,0,[])


#main()