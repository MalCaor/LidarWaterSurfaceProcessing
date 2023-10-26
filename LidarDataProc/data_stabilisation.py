# IMPORT EXTERN
from typing import List

# IMPORT CLASS
from LidarPointArray import LidarPointArray
from GyroData import GyroData

def stabilise_lidar_array(array_lidar: List[LidarPointArray], array_gyro: List[GyroData]):
    # array of corrected points
    new_array: List[LidarPointArray] = []
    
    # changed accel axes
    tot_accel_x = 1
    tot_accel_y = 1
    tot_accel_z = 1

    i: int = 0

    # go through all gyro data
    for gyr in array_gyro:
        if i >= array_lidar:
            # no more data to correct
            break
        if array_lidar[i].timestamp < gyr.timestamp:
            # data to correct
            lid = array_lidar[i]
            for y in len(lid.points_array):
                lid.points_array[y][0] = lid.points_array[y][0] * tot_accel_x
                lid.points_array[y][1] = lid.points_array[y][1] * tot_accel_y
                lid.points_array[y][2] = lid.points_array[y][2] * tot_accel_z
            new_array.append(lid)
            i += 1
        # correct tot gyr
        tot_accel_x += gyr.accel_x
        tot_accel_y += gyr.accel_y
        tot_accel_z += gyr.accel_z

    # if some lidar data left... use last ditch correction
    while(i<len(array_lidar)):
        # data to correct
        lid = array_lidar[i]
        for y in len(lid.points_array):
            lid.points_array[y][0] = lid.points_array[y][0] * tot_accel_x
            lid.points_array[y][1] = lid.points_array[y][1] * tot_accel_y
            lid.points_array[y][2] = lid.points_array[y][2] * tot_accel_z
        new_array.append(lid)
        i += 1