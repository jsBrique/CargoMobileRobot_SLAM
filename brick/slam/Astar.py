"""
文件说明：改进版A*算法，可以运行本文件测试迷宫寻路
作者:DoppioBrique
了解更多这份代码有关信息
欢迎关注我的b站账户：砖砖哟
或者加入技术讨论群：700741375
"""
import cv2
import numpy as np
import heapq as hp
import random
MARK=50
NO_OBS=255
OBS=0
MAX_DIS=65535
display=False
NO_SCAN=127
class Maptools:
    def __init__(self,img,display=True):
        self.display=display
        #kernel = np.ones((3, 3), np.uint8)
        #erosion = cv2.erode(img, kernel)
        self.sourceMAP=img
        self.height=img.shape[0]
        self.width=img.shape[1]
        #二值图
        ret, self.binMAP = cv2.threshold(img, 127,255,cv2.THRESH_BINARY)
        #记录代价信息
        self.costMAP=np.zeros((self.width,self.height),np.float)
        self.distMAP=np.zeros((self.width,self.height),np.float)
        #已搜索区域标记
        self.markMAP=np.zeros((self.width,self.height),np.uint8)
        ret, mask = cv2.threshold(self.binMAP, 120,255,cv2.THRESH_BINARY_INV)
        blur = cv2.GaussianBlur(self.binMAP,(35,35),0)
        #障碍场
        self.fleidMAP=cv2.add(mask,255-blur)
        #显示用的地图
        if self.display==True:
            self.showMAP=cv2.cvtColor(255-self.fleidMAP,cv2.COLOR_GRAY2BGR)
    
    def verify_node(self,me,mark=False):
        if me[0]>=0 and me[0]<self.height and me[1]>=0 and me[1]<self.width and OBS!=self.binMAP[me[0]][me[1]] and self.sourceMAP[me[0]][me[1]]!=NO_SCAN:
            if mark==False and self.markMAP[me[0]][me[1]]==MARK:
                return False
            else:
                return True
        else:
            return False

    def set_mark(self,me):
        self.markMAP[me[0]][me[1]]=MARK

    def set_dist(self,me,d):
        self.distMAP[me[0]][me[1]]=d

    def get_dist(self,me):
        return self.distMAP[me[0]][me[1]]

    def set_cost(self,me,cost):
        self.costMAP[me[0]][me[1]]=cost

    def get_cost(self,me):
        return self.costMAP[me[0]][me[1]]
    
    
        
    def cost_fun(self,me,start,end):#代价函数
        return ((np.sqrt((end[0]-me[0])**2 + 
        (end[1]-me[1])**2) + 
        (end[1]-start[1])**2)+self.fleidMAP[me[0]][me[1]])

    def neighbours(self,me,mark=False,find_road=False):
        nodes=[]
        if find_road==True:
            for i in range(-2,2):
                for j in range(-2,2):
                    p=[me[0]+i,me[1]+j]
                    if find_road==True and self.markMAP[p[0]][p[1]]!=MARK:
                        continue
                    
                    if p[0]==me[0] and p[1]==me[1]:
                        continue
                    if self.verify_node(p,mark)==True:
                        nodes.append(p)
        else:
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    p=[me[0]+i,me[1]+j]                  
                    if p[0]==me[0] and p[1]==me[1]:
                        continue
                    if self.verify_node(p,mark)==True:
                        nodes.append(p)
        return nodes

    def find_road(self,start,end):
        nodes=self.neighbours(end)
        count=0
        path=[]
        while True:
            count+=1
            now_node=min(nodes,key=lambda o:self.distMAP[o[0]][o[1]])
            path.append(now_node)
            
            if self.display==True:
                self.showMAP=cv2.circle(self.showMAP,(now_node[1],now_node[0]),1,(255,0,0),-1)
                cv2.imshow('maps',self.showMAP)
                cv2.waitKey(1)
            nodes=self.neighbours(now_node,mark=True,find_road=True)
            if now_node[0]==start[0] and now_node[1]==start[1]:
                print('distance=',count)
                return path
            
                
    def __str__(self):
        return str(self.sourceMAP.shape)

class AstarPathPlan:
    def __init__(self,maps,display=True):
        self.fresh_map(maps,display)#创建地图
        self.display=display
    def fresh_map(self,maps,display):#更新地图
        self.maps=Maptools(maps,display)
        self.pathPQ=[]#优先队列（堆优化）
        
    def clac_cost(self,me,lastnode):
        d=[me[0]-lastnode[0],me[1]-lastnode[1]]
        lastcost=self.maps.costMAP[lastnode[0]][lastnode[1]]
        lastdist=self.maps.get_dist(lastnode)

        if False==self.maps.verify_node(me,mark=True):
            return MAX_DIS
        if abs(d[0])==abs(d[1]):
            self.maps.set_dist(me,lastdist+1.414)
            return  lastdist+1.414+self.maps.cost_fun(me,self.start,self.end)
        else:
            self.maps.set_dist(me,lastdist+1)
            return  lastdist+1+self.maps.cost_fun(me,self.start,self.end)

    def find_road(self):
        if self.CanGO==True:
            path=self.maps.find_road(self.start,self.end)
            return path
        else:
            return []

    def search_path(self,start,end):
        
        self.start=start
        self.end=end
        self.CanGO=True
        if self.maps.sourceMAP[end[0]][end[1]]==NO_SCAN or self.maps.sourceMAP[end[0]][end[1]]==OBS:
            print('Error:This node could not reach!')
            self.CanGO=False
            return False
        InitCost=0.01
        
        self.maps.set_mark(start)
        self.maps.set_cost(start,InitCost)
        self.maps.set_dist(start,0)
        count=0
        hp.heappush(self.pathPQ,[InitCost,count,start])

        while True:
            if len(self.pathPQ)==0:
                print('Destination is unreachable!')
                self.CanGO=False
                break
            now_state=(hp.heappop(self.pathPQ))[2]
            if now_state[0]==end[0] and now_state[1]==end[1]:
                print('Path get!')
                break

            nodes=self.maps.neighbours(now_state,mark=False)
            for node in nodes:
                if self.maps.binMAP[node[0]][node[1]]==NO_OBS:
                    count+=1
                    cost=self.clac_cost(node,now_state)#计算代价
                    hp.heappush(self.pathPQ,[cost,count,node])
                    #print(node,cost)
                    self.maps.set_cost(node,cost)
                    self.maps.set_mark(node)
                    if self.display==True:
                        self.maps.showMAP[node[0]][node[1]][0]=250
                        self.maps.showMAP[node[0]][node[1]][1]=250
                        self.maps.showMAP[node[0]][node[1]][2]=200
            
            if self.display==True and count%100==0:
                self.maps.showMAP=cv2.circle(self.maps.showMAP,(start[1],start[0]),3,(0,0,255),-1)
                self.maps.showMAP=cv2.circle(self.maps.showMAP,(end[1],end[0]),3,(0,0,255),-1)
                cv2.imshow('maps',self.maps.showMAP)
                cv2.waitKey(1)
        return True

def randomimg(img,num):
    size=img.shape[0]
    for i in range(num):
        x=random.randint(0, size-1)
        y=random.randint(0, size-1)
        maps=cv2.circle(img,(x,y),2,0,-1)      
        
if __name__ == "__main__":
    img=cv2.imread('testmap5.jpg',cv2.IMREAD_GRAYSCALE)

    import time

    start_time=time.time()
    pathplan=AstarPathPlan(img,display=False)
    
    pathplan.search_path([50,50],[200,200])
    print(time.time()-start_time,'s')
    path=pathplan.find_road()
    D=5
    END_flag=False
    while True:
        if len(path)>=D:
            for i in range(D):
                node=path.pop()
        else:
            node=path.pop(0)
            END_flag=True
        img[node[0]][node[1]]=10
        cv2.imshow('map',img)
        cv2.waitKey(10)
        if END_flag==True:
            break

        

    while(27!=cv2.waitKey(1)):
        pass