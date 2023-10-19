from turtle import width
from typing import List
import open3d as o3d
import numpy as np
from LidarPoint import LidarPoint

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
    
    for point in array_cloud:
        geometry.points.append(point.point3d())
        vis.update_geometry(geometry)
    keep_running = True
    while keep_running:
        keep_running = vis.poll_events()
        vis.update_renderer()
    
    vis.destroy_window()