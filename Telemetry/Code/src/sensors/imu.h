// sensors/imu.h
#pragma once
#include <Arduino.h>

// LSM6DSO register addresses
#define IMU_ADDR        0x6A
#define IMU_WHO_REG     0x0F
#define IMU_WHO_AM_I    0x6C
#define IMU_CTRL1_XL    0x10
#define IMU_CTRL2_G     0x11
#define IMU_OUTX_L_XL   0x28
#define IMU_OUTX_L_G    0x22

// Conversion constants
#define IMU_ACCEL_SCALE  0.122f    // mg/LSB
//#define IMU_GYRO_SCALE   4.375f    // mdps/LSB
#define IMU_GYRO_SCALE   70.0f  // mdps/LSB for 2000 dps range

bool imu_init();
bool imu_read_accel(float &ax_g, float &ay_g, float &az_g);
bool imu_read_gyro(float &gx_dps, float &gy_dps, float &gz_dps);