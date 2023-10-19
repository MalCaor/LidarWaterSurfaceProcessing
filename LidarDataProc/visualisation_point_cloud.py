from typing import List
import open3d as o3d
from LidarPoint import LidarPoint

def display_point_cloud(array_cloud: List[LidarPoint]):
    print("Visualise Array of {} points".format(str(len(array_cloud))))
    list_point: List[List[float]] = list()
    for point in array_cloud:
        list_point.append(point.point3d())
    pcd = o3d.t.geometry.PointCloud(list_point)