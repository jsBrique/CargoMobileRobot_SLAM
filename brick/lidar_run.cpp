#include "laser_driver.h"
#include <iostream>
#include <string>
#include <signal.h>
using namespace std;
#define MAX 30
float data[MAX];
Lidar_Pack Lidar2python;
shm_config shared_config2;
shm_Lidar_Pack *shared;//指向shm
extern int write_show;
extern LaserScan scan;
extern "C" 
{
    void do_not_show_write(void);
    int running(void);
    float* data_test(void);
    void Lidar_Scan_Init(void);
    float* Lidar_Scan_Get(void);
    void Lidar_Scan_Test(void);
    void Lidar_Scan_Get_Finish(void);
    void Lidar_Scan_Close(void);
    float* Lidar_Scan_X(void);
    float* Lidar_Scan_Y(void);

}

void do_not_show_write(void)
{
    write_show=0;
}
int running(void)
{

    printf(" Welcome use YDLIDAR C++ Lib (from brick)\n");

    const std::string port = "/dev/ttyUSB0";
    const int baud =  128000;
    const int intensities =  false;

    Lasertest laser;
    laser.setPort(port);
    laser.setBaudrate(baud);
    laser.setIntensities(intensities);
    laser.run();

    return 0;
}

void Lidar_Scan_Init(void)
{
    shared_config2.shm=NULL;
	
	//int shmid;//共享内存标识符
	//创建共享内存
	shared_config2.shmid = shmget((key_t)1834, sizeof(shm_Lidar_Pack), 0666|IPC_CREAT);
    if(shared_config2.shmid == -1)
    {
        fprintf(stderr, "shmget failed\n");
        exit(EXIT_FAILURE);
    }
    //将共享内存连接到当前进程的地址空间
    shared_config2.shm = shmat(shared_config2.shmid, 0, 0);
    if(shared_config2.shm == (void*)-1)
	{
		fprintf(stderr, "shmat failed\n");
		exit(EXIT_FAILURE);
	}
    //设置共享内存
	shared = (shm_Lidar_Pack*)(shared_config2.shm);
    printf("shared memory connect,shmid=%d\n",shared_config2.shmid);

   
}

void Scan_shm_divide(void)
{
    //把共享内存从当前进程中分离
	if(shmdt(shared_config2.shm) == -1)
	{
		fprintf(stderr, "shmdt failed\n");
		//exit(EXIT_FAILURE);
	}
}

void shm_delete(void)
{
	//删除共享内存
	if(shmctl(shared_config2.shmid, IPC_RMID, 0) == -1)
	{
		fprintf(stderr, "shmctl(IPC_RMID) failed\n");
		exit(EXIT_FAILURE);
	}
}

void Lidar_Scan_Test(void)
{
    shared->read=1;
    //printf(shared->test);
    printf("scan_write%d\n",shared->write);
    // for(int i=0;i<shared->counts;i++)
    //     {printf("shared%d=%f\n",i,shared->Lidar_Data_Read[i]);}
    shared->read=0;
    
}

float* Lidar_Scan_Get(void)
{
    shared->read=1;
    return shared->Lidar_Data_Read;
    
}

float* Lidar_Scan_X(void)
{
    shared->read=1;
    return shared->Lidar_Data_Read_x;
}

float* Lidar_Scan_Y(void)
{
    shared->read=1;
    return shared->Lidar_Data_Read_y;
}

void Lidar_Scan_Get_Finish(void)
{
    shared->read=0;
}

void Lidar_Scan_Close(void)
{
    Scan_shm_divide();
    shm_delete();
}

float* data_test(void)
{
    for(int i=0;i<MAX;i++)
    {
        data[i]=i+0.1f;
    }
    return data;
    
}

