# IMPORT EXTERN
from typing import List

# IMPORT CLASS
from LidarPointArray import LidarPointArray
from GyroData import GyroData

def stabilise_lidar_array(array_lidar: List[LidarPointArray], array_gyro: List[GyroData]):
    print("Stabilising data of lenght : {}".format(len(array_lidar)))
    # array of corrected points
    new_array: List[LidarPointArray] = []
    
    # changed accel axes
    tot_accel_x: float = 1.0
    tot_accel_y: float = 1.0
    tot_accel_z: float = 1.0

    i: int = 0
    length = len(array_gyro)
    l_gyr: int = 0

    # go through all gyro data
    for gyr in array_gyro:
        # % compl
        print(" "*20, end='\r')
        percent: float = l_gyr / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(l_gyr, length, percent), end='\r')
        l_gyr += 1

        if i >= len(array_lidar):
            # no more data to correct
            print("Breaked before end of Gyro Data")
            break
        while(i<len(array_lidar) and array_lidar[i].timestamp < gyr.timestamp):
            # data to correct
            lid = array_lidar[i]
            for y in range(len(lid.points_array)):
                lid.points_array[y][0] = lid.points_array[y][0] * -1 * tot_accel_x
                lid.points_array[y][1] = lid.points_array[y][1] * -1 * tot_accel_y
                lid.points_array[y][2] = lid.points_array[y][2] * -1 * tot_accel_z
            new_array.append(lid)
            i += 1
        # correct tot gyr
        tot_accel_x += float(gyr.accel_x)
        tot_accel_y += float(gyr.accel_y)
        tot_accel_z += float(gyr.accel_z)

    # if some lidar data left... use last ditch correction
    while(i<len(array_lidar)):
        print("Lidar point without updated Gyro accel")
        # data to correct
        lid = array_lidar[i]
        for y in range(len(lid.points_array)):
            lid.points_array[y][0] = lid.points_array[y][0] * -1 * tot_accel_x
            lid.points_array[y][1] = lid.points_array[y][1] * -1 * tot_accel_y
            lid.points_array[y][2] = lid.points_array[y][2] * -1 * tot_accel_z
        new_array.append(lid)
        i += 1

    print("Finished stabilisation")
    return new_array