# IMPORT EXTERN
from typing import List
import open3d as o3d
import numpy as np

# IMPORT CLASS
from LidarPointArray import LidarPointArray

# param mesh
fist_every_k_points = 1000
second_every_k_points = 1000
dist_to_divide = 20

# param line
dist_to_divide_line = 5


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
        pc.uniform_down_sample(every_k_points=fist_every_k_points)
        pc.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        pc.remove_radius_outlier(nb_points=16, radius=0.05)
        list_mesh_retour.append(generate_mesh_from_inst_pc(np.array(pc.points).tolist()))
    return (list_mesh_retour, list_pc_retour)

def generate_mesh_from_inst_pc(pc: List[List]):
    list_retour: List[o3d.geometry.TriangleMesh] = []
    # divide points by proximity
    divided_pc = divide_pc_to_axis(pc)
    for p in divided_pc:
        try:
            list_retour.append(mesh_from_pc(p))
        except((IndexError, RuntimeError)):
            pass
    
    return list_retour

def divide_pc_to_axis(pc: List[List]):
    copy_pc = list(pc)
    sub_pcs = []
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
        if sub_pc:
            for p in sub_pc:
                copy_pc.remove(p)
            sub_pcs.append(sub_pc)

    return sub_pcs

def mesh_from_pc(pc_raw: List[List]):
    # create point cloud
    point_coud = o3d.geometry.PointCloud()
    point_coud.points = o3d.utility.Vector3dVector(pc_raw)
    point_coud.estimate_normals()
    point_coud.orient_normals_towards_camera_location()
    point_coud.uniform_down_sample(every_k_points=second_every_k_points)
    point_coud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    point_coud.remove_radius_outlier(nb_points=16, radius=0.05)
    # create mesh
    tetra_mesh, pt_map =  o3d.geometry.TetraMesh.create_from_point_cloud(point_coud)
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
        point_coud, 0.5, tetra_mesh, pt_map)
    mesh.compute_vertex_normals()
    return mesh

def line_interpr(array_lidar: List[LidarPointArray]):
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
        list_line_retour.append(generate_line(np.array(pc.points).tolist()))

    return (list_line_retour, list_pc_retour)

def generate_line(pc: List[List]):
    list_lines: List[o3d.geometry.LineSet] = []
    i = 0
    while(len(pc)!=0):
        print(" "*10, end='\r')
        print("{}".format(i), end='\r')
        i+=1
        # get line
        point = pc[0]
        line_points, line_dir = get_line_point(point, pc)
        # remove lines points in pc
        line_set = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(line_points),
            lines=o3d.utility.Vector2iVector(line_dir),
        )
        list_lines.append(line_set)
    return list_lines

def get_line_point(point, pc: List[List]):
    # list retour
    line_points = []
    line_dir = []
    # append point
    line_points.append(point)
    pc.remove(point)
    # set up best
    n_point = np.array(point)
    finished=False
    best_point = pc[0]
    n_other_point = np.array(best_point)
    squared_dist = np.sum((n_point-n_other_point)**2, axis=0)
    best_dist = np.sqrt(squared_dist)
    i=0
    # loop while line not finished
    while(not finished):
        loop_point = None
        for loop_point in pc:
            n_other_point = np.array(loop_point)
            # calculate dist
            squared_dist = np.sum((n_point-n_other_point)**2, axis=0)
            dist = np.sqrt(squared_dist)
            # test if close enough and better than best
            if dist<dist_to_divide_line and dist<best_dist:
                best_point=loop_point
        if loop_point is None:
            # no more candidate, finishing
            finished=True
        else:
            print(loop_point)
            print(best_point)
            line_points.append(best_point)
            line_dir.append([i, i+1])
            pc.remove(best_point)
            i+=1

    return (line_points, line_dir)
    