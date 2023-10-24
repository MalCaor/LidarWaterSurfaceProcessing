from time import sleep
from turtle import width
from typing import List, Tuple
import open3d as o3d
import numpy as np
from LidarPointArray import LidarPointArray
from LidarPoint import LidarPoint
from LidarPointArray import LidarPointArray
import pandas as pd

from matplotlib import pyplot as plt
import matplotlib.animation as animation
import seaborn

import keyboard

def display_point_cloud(array_cloud: List[LidarPoint]):
    print("Visualise Array of {} points".format(str(len(array_cloud))))
    
    vis = o3d.visualization.Visualizer()
    vis.create_window(
        window_name="CloudPoint Visualizer",
        width=1000,
        height=500,
        left=500,
        top=500
    )

    geometry = o3d.geometry.PointCloud()

    vis.add_geometry(geometry)

    data_point = []
    
    for point in array_cloud:
        data_point.append(point.point3d())

    geometry.points = o3d.utility.Vector3dVector(data_point)
    vis.add_geometry(geometry)

    keep_running = True
    while keep_running:
        keep_running = vis.poll_events()
        vis.update_renderer()
    
    vis.destroy_window()

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
        vis.update_renderer()
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
        vis.update_renderer()
        if keyboard.is_pressed('r'):
            i = 0
    
    # escape key
    vis.destroy_window()

def display2DcloudPoint(array_cloud: List[LidarPoint]):
    points = []
    for point in array_cloud:
        points.append({
            "longitude" : point.x,
            "latitude" : point.y
        })
    data = pd.DataFrame(points)
    seaborn.jointplot(x="longitude", y="latitude", data=data, s=0.5)
    plt.show()

def hex2dcloudPoint(array_cloud: List[LidarPoint]):
    x = []
    y = []
    z = []
    for point in array_cloud:
        x.append(point.x)
        y.append(point.y)
        z.append(point.z)
    plt.hexbin(x, y, C=z)
    plt.xlabel('x coordinates')
    plt.ylabel('y coordinates')
    plt.show()

def contour2dcloudPoint(array_cloud: List[LidarPoint]):
    x = []
    y = []
    z = []
    for point in array_cloud:
        x.append(point.x)
        y.append(point.y)
        z.append(point.z)
    plt.tricontourf(x, y, z, cmap="ocean")
    plt.xlabel('x coordinates')
    plt.ylabel('y coordinates')
    plt.show()