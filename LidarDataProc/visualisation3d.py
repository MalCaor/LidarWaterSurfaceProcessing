from multiprocessing.connection import wait
from time import sleep
from typing import List
import open3d as o3d
from LidarPointArray import LidarPointArray
from LidarPoint import LidarPoint
from LidarPointArray import LidarPointArray

import keyboard

def display_anim_point_array(array_cloud: List[LidarPointArray]):
    # create window
    vis = o3d.visualization.Visualizer()
    vis.create_window(
        window_name="CloudPoint Visualizer",
        width=1000,
        height=500,
        left=500,
        top=500
    )

    # load first frame
    geometry = o3d.geometry.PointCloud()
    i: int = 0
    geometry.points = o3d.utility.Vector3dVector(array_cloud[i].points_array)
    vis.add_geometry(geometry)

    # run sim
    keep_running = True
    while keep_running:
        if i<len(array_cloud):
            geometry.points = o3d.utility.Vector3dVector(array_cloud[i].points_array)
            vis.update_geometry(geometry)
            i += 1
        keep_running = vis.poll_events()
        if keyboard.is_pressed('r'):
            i = 0
    
    # escape key
    vis.destroy_window()


def display_anim_point(array_cloud: List[List[LidarPoint]]):
    # Load array cloud
    all_array = []
    for array in array_cloud:
        data_point = []
        for point in array:
            data_point.append(point.point3d())
        all_array.append(data_point)

    # create window
    vis = o3d.visualization.Visualizer()
    vis.create_window(
        window_name="CloudPoint Visualizer",
        width=1000,
        height=500,
        left=500,
        top=500
    )

    # load first frame
    geometry = o3d.geometry.PointCloud()
    i: int = 0
    cur_array = all_array[i]
    geometry.points = o3d.utility.Vector3dVector(cur_array)
    vis.add_geometry(geometry)

    # run sim
    keep_running = True
    while keep_running:
        if i<len(all_array):
            cur_array = all_array[i]
            geometry.points = o3d.utility.Vector3dVector(cur_array)
            vis.update_geometry(geometry)
            i += 1
        keep_running = vis.poll_events()
        if keyboard.is_pressed('r'):
            i = 0
    
    # escape key
    vis.destroy_window()
