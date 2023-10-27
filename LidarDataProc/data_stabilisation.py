# IMPORT EXTERN
import math
from typing import List

# IMPORT CLASS
from LidarPointArray import LidarPointArray
from GyroData import GyroData


def _rotate_around_point(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def _correct_array_point(array_lidar, tot_yaw):
    # store new value
    lid = array_lidar

    for y in range(len(lid.points_array)):
        # negate yaw
        n_x, n_y = _rotate_around_point((0,0), (lid.points_array[y][0], lid.points_array[y][1]), tot_yaw)
        lid.points_array[y][0] = n_x
        lid.points_array[y][1] = n_y
    return lid

def stabilise_lidar_array(array_lidar: List[LidarPointArray], array_gyro: List[GyroData]):
    print("Stabilising data of lenght : {}".format(len(array_lidar)))
    # array of corrected points
    new_array: List[LidarPointArray] = []
    
    # changed accel axes
    tot_yaw: float = 1.0

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
            lid = _correct_array_point(array_lidar[i], tot_yaw)
            new_array.append(lid)
            i += 1
        # correct tot gyr
        tot_yaw = -1 * math.radians(float(gyr.yaw))

    # if some lidar data left... use last ditch correction
    while(i<len(array_lidar)):
        # data to correct
        lid = _correct_array_point(array_lidar[i], tot_yaw)
        new_array.append(lid)
        i += 1

    print("Finished stabilisation")
    return new_array
