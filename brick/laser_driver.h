#pragma once
#include "../sdk/include/ydlidar_driver.h"
#include "../sdk/src/common.h"
#include <exception>
#include <stdexcept>
#include <string>
#include <signal.h>

#include <stdlib.h>
#include <math.h>
#include <sys/shm.h>

#define DEG2RAD(x) ((x)*M_PI/180.)

#define RAD2DEG(x) ((x)*180./M_PI)
#define NODE_COUNTS 720
#define EACH_ANGLE 0.5

const double PI = 3.1415926;

const float pif=3.1415926;
#define rad(x) (pif*(x)/180.0f)
struct Lidar_Pack
{
    float* Lidar_Data;
    int counts;
};

struct shm_config
{
    void *shm = NULL;//分配的共享内存的原始首地址
	int shmid;//共享内存标识符
};

struct shm_Lidar_Pack
{
    float Lidar_Data1[NODE_COUNTS];
    float Lidar_Data2[NODE_COUNTS];
    float *Lidar_Data_Read;
    float *Lidar_Data_Write;

    float Lidar_Data1_x[NODE_COUNTS];
    float Lidar_Data1_y[NODE_COUNTS];

    float Lidar_Data2_x[NODE_COUNTS];
    float Lidar_Data2_y[NODE_COUNTS];

    float *Lidar_Data_Read_x;
    float *Lidar_Data_Write_x;

    float *Lidar_Data_Read_y;
    float *Lidar_Data_Write_y;

    int counts;
    int read;
    

    int write;
    char test[10];
};

class Lasertest {
public:
    Lasertest();

    virtual ~Lasertest();

    void run();

    void setPort(std::string port);
    void setBaudrate(int baud);
    void setIntensities(bool intensities);

    

private:
    void Open();
    void Start();
    void Stop();
    void Close();
    static void closeApp(int signo);

    bool getDeviceHealth();
    bool getDeviceInfo();

    struct shm_Lidar_Pack* shm_Lidar_Data_Init(void);
    void shm_divide(void);
    void shm_delete(void);
    void DoubleMemory(void);

    void FastTriFun_init(void);
    float FastSin(int x);
    float FastCos(int x);
    
    std::vector<int> split(const std::string &s, char delim);

    void publicScanData(node_info *nodes, uint64_t start,double scan_time, size_t node_count, float angle_min, float angle_max,bool reverse_data);


    enum DEVICE_STATE {
        OPENED,
        RUNNING,
        CLOSED,
    };

    static DEVICE_STATE device_state_;

    float sin_table[NODE_COUNTS];
    float cos_table[NODE_COUNTS];

    int scan_no_;
    struct shm_Lidar_Pack* sharedLidar; 
    std::string port_;
    int baudrate_;
    bool intensities_;
    int publish_freq_;
    double angle_min_, angle_max_;
    bool inverted;
};


