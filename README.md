# LIDAR WATER SURFACE PROCESSING :

usage: LIDAR Data Processing [-h] [--lidar LIDAR LIDAR] [--gyro GYRO] [--corr CORR] [--filter FILTER] [--display DISPLAY]

Process LIDAR wave surface data

options:
-  -h, --help           show this help message and exit
-  --lidar LIDAR LIDAR  [Lidar File PATH] [number of snapshot to read]
-  --gyro GYRO          [IMU csv File PATH]
-  --corr CORR          [ypr] correct data with IMU - yaw pitch row - (--gyro       
                       required)
-  --filter FILTER      filter setting path
-  --display DISPLAY    display data : pc (point cloud), mesh (mesh generation)
---
## Contour lidar

Generate MathPlot contour animation from lidar data

![contour map](./img/contourMap.PNG "Title")

## Point Cloud Lidar

Visualise Point cloud in a Open3d Space

![point cloud](./img/LidarImg.PNG "Title")

## Point Cloud Stabilisation

Stabilise the point cloud with IMU data

## Mesh Generation

Generate Mesh From Lidar Point cloud and Visualise it

![mesh generation](./img/mesh3.PNG "Title")