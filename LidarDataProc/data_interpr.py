# IMPORT EXTERN
from typing import List
import open3d as o3d
import numpy as np

# IMPORT CLASS
from LidarPointArray import LidarPointArray
from utils import *

# param mesh
voxel_size = 0.1
dist_to_divide = 5
alpha = 1

# param line
dist_to_divide_line = 5


def shape_interpr(array_lidar: List[LidarPointArray]):
    """Return the shape tuple of list of mesh and point cloud from a list of lidar point array

    Args:
        array_lidar (List[LidarPointArray]): inputed list of lidar data

    Returns:
        Tuple[List[List[o3d.geometry]], List[o3d.geometry.PointCloud]]: tuple of list
    """
    length: float = len(array_lidar)
    print("Interpreting array of length {}".format(str(length)))
    list_mesh_retour: List[List[o3d.geometry.TriangleMesh]] = []
    list_pc_retour: List[o3d.geometry.PointCloud] = []
    i = 0.0
    for arr in array_lidar:        
        # percent
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        i += 1
        # calcuate shape instant
        _shape_arr(arr, list_pc_retour, list_mesh_retour)
    return (list_mesh_retour, list_pc_retour)

def _shape_arr(arr, list_pc_retour, list_mesh_retour):
    """append a mesh and point cloud list of a single lidar "frame"

    Args:
        arr (LidarPointArray): _description_
        list_pc_retour (List[o3d.geometry.PointCloud]): _description_
        list_mesh_retour ( List[List[o3d.geometry]): _description_
    """
    # create point cloud
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(arr.points_array)
    #pc.estimate_normals()
    #pc.orient_normals_towards_camera_location()
    pc = pc.voxel_down_sample(voxel_size=voxel_size)
    pc.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    pc.remove_radius_outlier(nb_points=16, radius=0.05)
    list_pc_retour.append(pc)
    # GeneMesh from Cloud
    list_mesh_retour.append(_generate_mesh_from_inst_pc(pc))

def _generate_mesh_from_inst_pc(pc):
    """return a list of mesh of a single lidar "frame"

    Args:
        pc (List[List]): _description_

    Returns:
        _type_: _description_
    """
    return [_mesh_from_pc(pc)]

def _divide_pc_to_axis(pc):
    """return a dub division of a point cloud by proximity

    Args:
        pc (List[List]): point cloud to divide

    Returns:
        List[List[List]]: list of sub point cloud
    """
    copy_pc = np.array(pc.points).tolist()
    sub_pcs = []
    while(len(copy_pc)!=0):
        sub_pc = []
        point = copy_pc[0]
        n_point = np.array(point)
        # select only those close enough
        sub_pc = [p for p in copy_pc if calculate_distance(n_point, np.array(p))<dist_to_divide]
        # remove from copy points and append sub point cloud
        if sub_pc:
            for p in sub_pc:
                copy_pc.remove(p)
            sub_pcs.append(sub_pc)

    return sub_pcs

def _mesh_from_pc(point_coud):
    """generate a mesh from a point cloud

    Args:
        pc_raw (List[List]): input point cloud

    Returns:
        o3d.geometry.TriangleMesh: mesh returned
    """
    tetra_mesh, pt_map =  o3d.geometry.TetraMesh.create_from_point_cloud(point_coud)
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
        point_coud, alpha=alpha, tetra_mesh=tetra_mesh, pt_map=pt_map)
    mesh.compute_vertex_normals()
    return mesh

###### LINE DRAWING #####

def line_interpr(array_lidar: List[LidarPointArray]):
    """Draw line from a pc list

    Args:
        array_lidar (List[LidarPointArray]): lidar pc list

    Returns:
        Tuple[List[List[o3d.geometry.LineSet]], List[o3d.geometry.PointCloud]]: List of line, list of points cloud
    """
    length: float = len(array_lidar)
    print("Interpreting array of length {}".format(str(length)))
    
    list_line_retour: List[List[o3d.geometry.LineSet]] = []
    list_pc_retour: List[o3d.geometry.PointCloud] = []

    
    for arr in array_lidar:
        # create point cloud
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(arr.points_array)
        pc.estimate_normals()
        pc.orient_normals_towards_camera_location()
        list_pc_retour.append(pc)
        # create lines
        list_line_retour.append(_generate_line(pc))

    return (list_line_retour, list_pc_retour)

def _generate_line(pc):
    """return a list of lineset from the inputed point cloud

    Args:
        pc (_type_): point cloud

    Returns:
        List[o3d.geometry.LineSet]: lineset
    """

    list_lines: List[o3d.geometry.LineSet] = []
    subdiv = _divide_pc_to_axis(pc)
    print("subdive by {} part".format(str(len(subdiv))))
    i = 0
    for div in subdiv:
        # display
        print(" "*10, end='\r')
        print("{}".format(i), end='\r')
        i+=1
        # get line
        order = []
        for indent in range(len(div)):
            order.append([indent, indent+1])
        order = order[:-1]
        # append
        l = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(div),
            lines=o3d.utility.Vector2iVector(order),
        )
        list_lines.append(l)
    return list_lines

