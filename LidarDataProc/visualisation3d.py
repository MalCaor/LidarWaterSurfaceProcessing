from multiprocessing.connection import wait
from time import sleep
from typing import List
import open3d as o3d
from LidarPointArray import LidarPointArray
from LidarPoint import LidarPoint
from LidarPointArray import LidarPointArray

import keyboard

def display_anim_point_array(array_cloud: List[LidarPointArray]):
    """Display points array in 3D animation\n
    The animation will run as fast as possible without notion of time between Lidar snapshot

    Args:
        array_cloud (List[LidarPointArray]): List of Lidar Snapshot to display
    """
    # create window
    vis = o3d.visualization.Visualizer()
    vis.create_window(
        window_name="CloudPoint Visualizer",
        width=1000,
        height=500,
        left=500,
        top=500
    )

    # visu param
    opt = vis.get_render_option()
    opt.point_show_normal = True

    # load first frame
    geometry = o3d.geometry.PointCloud()
    i: int = 0
    geometry.points = o3d.utility.Vector3dVector(array_cloud[i].points_array)
    geometry.voxel_down_sample(1.0)
    geometry.estimate_normals()
    #geometry.orient_normals_towards_camera_location()
    vis.add_geometry(geometry)

    # run sim
    keep_running = True
    while keep_running:
        if i<len(array_cloud):
            geometry.points = o3d.utility.Vector3dVector(array_cloud[i].points_array)
            geometry.voxel_down_sample(1.0)
            geometry.estimate_normals()
            #geometry.orient_normals_towards_camera_location()
            vis.update_geometry(geometry)
            i += 1
        keep_running = vis.poll_events()
        if keyboard.is_pressed('r'):
            i = 0
    
    # escape key
    vis.destroy_window()