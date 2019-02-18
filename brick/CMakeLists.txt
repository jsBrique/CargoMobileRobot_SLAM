cmake_minimum_required(VERSION 2.8)
project(lidar_run)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

ADD_DEFINITIONS(-std=c++11)


set(SDK_PATH "../sdk/")

IF (WIN32)
FILE(GLOB SDK_SRC 
  "${SDK_PATH}/src/impl/windows/*.cpp"
  "${SDK_PATH}/src/*.cpp"
)

ELSE()

FILE(GLOB SDK_SRC 
  "${SDK_PATH}/src/impl/unix/*.cpp"
  "${SDK_PATH}/src/*.cpp"
)

ENDIF()

include_directories(
  ${catkin_INCLUDE_DIRS}
  ${SDK_PATH}//include
  ${SDK_PATH}/src
)

set(MODULE_FILES
        laser_driver.h
        laser_driver.cpp
        )
add_library(lidar_run SHARED lidar_run.cpp ${MODULE_FILES} ${SDK_SRC})

#add_executable(lidar_run lidar_run.cpp ${MODULE_FILES} ${SDK_SRC})

IF (WIN32)
ELSE()
target_link_libraries(lidar_run rt pthread)
ENDIF()
