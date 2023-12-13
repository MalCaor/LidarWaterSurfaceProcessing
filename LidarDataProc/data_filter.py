import json
from typing import Dict, List
from LidarPointArray import LidarPointArray
from filter import *
import numpy as np

def filter_lidar_data(lidar_data: List[LidarPointArray], filter_setting_path: str):
    print("Filtering the data with rules in {}".format(filter_setting_path))
    # Vars
    filter_obj: filter
    # Read File
    with open(filter_setting_path) as f_json:
        f_decode: Dict = json.loads(f_json.read())
        name = next(iter(f_decode))
        f_object = f_decode.get(name)
        # Set object
        if name == "range_filter":
            filter_obj = range_filter(**f_object)
    # Test filter for each point
    lpa: LidarPointArray
    # % compl
    i = 0.0
    length = len(lidar_data)
    print(" "*20, end='\r')
    percent: float = i / length * 100.0
    print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
    for lpa in lidar_data:
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        i+=1
        points_to_remove = []
        for p in lpa.points_array:
            if not filter_obj.validate(np.array([0,0,0]), np.array(p)):
                points_to_remove.append(p)
        for p_to_remove in points_to_remove:
            lpa.points_array.remove(p_to_remove)
    print("Filtering finished!")
