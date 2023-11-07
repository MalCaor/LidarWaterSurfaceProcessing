# IMPORT EXTERN
from typing import List
import open3d as o3d
import numpy as np

# IMPORT CLASS
from LidarPointArray import LidarPointArray

"""tetra_mesh, pt_map =  o3d.geometry.TetraMesh.create_from_point_cloud(pc)
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
        pc, 0.1, tetra_mesh, pt_map)"""

def shape_interpr(array_lidar: List[LidarPointArray]):
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
        
        # create point cloud
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(arr.points_array)
        pc.estimate_normals()
        pc.orient_normals_towards_camera_location()
        list_pc_retour.append(pc)
        # GeneMesh from Cloud
        list_mesh_retour.append(generate_mesh_from_inst_pc(arr.points_array))
    return (list_mesh_retour, list_pc_retour)

def generate_mesh_from_inst_pc(pc: List[List]):
    list_retour: List[o3d.geometry.TriangleMesh] = []
    # divide points by proximity
    divided_pc = divide_pc_to_axis(pc)
    for p in divided_pc:
        list_retour.append(mesh_from_pc(p))
    
    return list_retour

def divide_pc_to_axis(pc: List[List]):
    copy_pc = list(pc)
    sub_pcs = []
    dist_to_divide = 50
    while(len(copy_pc)!=0):
        sub_pc = []
        point = copy_pc[0]
        n_point = np.array(point)
        for other_point in copy_pc:
            n_other_point = np.array(other_point)
            # calculate dist
            squared_dist = np.sum((n_point-n_other_point)**2, axis=0)
            dist = np.sqrt(squared_dist)
            # test if close enough
            if dist<dist_to_divide:
                sub_pc.append(other_point)
        for p in sub_pc:
            copy_pc.remove(p)
        sub_pcs.append(sub_pc)

    return sub_pcs

def mesh_from_pc(pc_raw: List[List]):
    # create point cloud
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(pc_raw)
    pc.estimate_normals()
    pc.orient_normals_towards_camera_location()
    # create mesh
    tetra_mesh, pt_map =  o3d.geometry.TetraMesh.create_from_point_cloud(pc)
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
        pc, 0.1, tetra_mesh, pt_map)
    return mesh
