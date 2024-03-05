# LIDAR WATER SURFACE PROCESSING :

usage: LIDAR Data Processing [-h] [--lidar_vel LIDAR_FILE_PATH NUM_FRAME_TO_EXTRACT] [--lidar_ous LIDAR_FILE_PATH JSON_META_FILE_PATH NUM_FRAME_TO_EXTRACT] [--gyro CSV_FILE_PATH] [--corr YPR_OPTION] [--prefilter JSON_FILE_PATH]
                             [--postfilter JSON_FILE_PATH] [--display DISPLAY_TYPE]

Process LIDAR wave surface data

options:
-  -h, --help            show this help message and exit
-  --lidar_vel LIDAR_FILE_PATH NUM_FRAME_TO_EXTRACT :
                        read Velodyne lidar .pcap
-  --lidar_ous LIDAR_FILE_PATH JSON_META_FILE_PATH NUM_FRAME_TO_EXTRACT :
                        read Ouster lidar .pcap
-  --gyro CSV_FILE_PATH : read IMU csv file
-  --corr YPR_OPTION  :   correct the point cloud with IMU data (Yaw, Pitch, Roll)
-  --prefilter JSON_FILE_PATH :
                        filter cloud point before correcting the data
-  --postfilter JSON_FILE_PATH :
                        filter cloud point after correcting the data
-  --display DISPLAY_TYPE :
                        display data : pc (point cloud), mesh (mesh generation)
---

# Display Type :
## PC

Just visualise the lidar data in open3d as a moving point cloud

![zodiac_pc](./img/pc_vid_compr.gif "Title")

## Mesh

Generate a mesh from the point cloud

![mesh_ifremer](./img/mesh3.PNG "Title")

## Hex2d

Display the point cloud as a 2d animation view from the top

![mesh_ifremer](./img/hex_comp_comp.gif "Title")

# Barycentre

Display the animated barycentre of a KNN clustering

![mesh_ifremer](./img/barycentre.gif "Title")

# Linebary

Display the barycentre movement as lines
Lines go from blue to red according to their lenght

![mesh_ifremer](./img/lineWave.gif "Title")

# Wavedir

Same as linebary but with the estimated direction of the wave (weighted average of the linear reduction of the lines)

![mesh_ifremer](./img/wavedir.gif "Title")

