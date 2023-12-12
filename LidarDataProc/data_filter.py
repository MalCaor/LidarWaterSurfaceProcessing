from typing import List
from LidarPointArray import LidarPointArray
from filter import *

def filter_lidar_data(lidar_data: List[LidarPointArray], filter_setting_path: str) -> List[LidarPointArray]:
    return lidar_data