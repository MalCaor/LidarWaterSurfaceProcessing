from math import dist
from operator import invert
from statistics import median
from typing import List
import open3d as o3d
from sklearn.neighbors import KDTree
from scipy import stats

from utils import *
from LidarPointArray import LidarPointArray


### CONFIG
dist_to_divide = 50


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


def line_generation(array_lidar: List[LidarPointArray]):
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

def line_2d_generate(array_lidar: List[LidarPointArray]):
    length: float = len(array_lidar)
    print("Interpreting array of length {}".format(str(length)))

    line_retour = []
    points_retour = []

    for arr in array_lidar:
        # create point cloud
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(arr.points_array)
        l, p = line_interpolation(pc)
        line_retour.append(l)
        pc = pc.voxel_down_sample(0.5)
        points_retour.append(p)

    return line_retour, points_retour

def baril_centre_cluster(array_lidar: List[LidarPointArray]):
    length: float = len(array_lidar)
    print("Interpreting array of length {}".format(str(length)))
    
    points_retour = []

    for arr in array_lidar:
        # create point cloud
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(arr.points_array)
        points_retour.append(_bar_cen_cluster_calc(pc))

    return points_retour

def ransac_divid(pc):
    pc = pc.voxel_down_sample(0.1)
    point_cloud: np.array = np.array(pc.points)
    line_retour = []
    ransac_n=3

    while point_cloud.size > ransac_n*2:
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(point_cloud)
        plane_model, inliers = pc.segment_plane(distance_threshold=0.1, ransac_n=ransac_n, num_iterations=10000)
        inlier_cloud = pc.select_by_index(inliers)
        outlier_cloud = pc.select_by_index(inliers, invert=True)
        line_retour.append(np.array(inlier_cloud.points).tolist())
        point_cloud = np.array(outlier_cloud.points)
    
    return line_retour

def _bar_cen_cluster_calc(pc):
    clusters = knn_div(pc)
    points = []
    for cluster in clusters:
        x = median(p[0] for p in cluster)
        y = median(p[1] for p in cluster)
        points.append([x,y])
    return points

def line_interpolation(pc):
    lines_retour = []
    lines, clusters = combined(pc)

    for cluster in lines:
        lines_retour.append(interpolate(cluster))

    return lines_retour, clusters

def interpolate(cluster):
    lx = [p[0] for p in cluster]
    ly = [p[1] for p in cluster]
    res = stats.linregress(lx, ly)
    newpoints = []
    lx = sorted(lx)
    newpoints.append([lx[0], res.intercept + res.slope*lx[0]])
    newpoints.append([lx[len(lx)-1], res.intercept + res.slope*lx[len(lx)-1]])
    #for x in lx:
    #    newpoints.append([x, res.intercept + res.slope*x])
    return newpoints



def combined(pc):
    lines_retour = []
    clusters = knn_div(pc)

    for cluster in clusters:
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(np.array(cluster))
        lines = simple_line_contour(pc)
        for l in lines:
            lines_retour.append(l)
    
    return lines_retour, clusters

def simple_line_contour(pc):
    pc = pc.voxel_down_sample(0.1)
    array: List = np.array(pc.points).tolist()
    link_p: List[List] = []
    list_l: List = []
    length = len(array)
    while array:
        if len(array)==1: # last didgit
            if len(list_l) > 3:
                list_l.append(array[0])
            break
        # p1
        p1 = array[0]
        #sort
        len_list = len(list_l)*5 # * to augment the size of the list to ignore
        div_to_sort = max(len_list, 1)
        to_sort = int(len(array)/div_to_sort)
        array[0:to_sort] = sorted(array[0:to_sort], key=lambda elem: calculate_distance(np.array(p1), np.array(elem)), reverse=False)
        # display
        i = length-len(array)
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        # add point
        p2 = array[1]
        list_l.append(p1)
        array.remove(p1)
        dist_to_divide = calculate_distance(np.array(p1), np.array([0,0,0])) * 0.1
        if calculate_distance(np.array(p1), np.array(p2))>dist_to_divide:
            if len(list_l) > 3:
                link_p.append(list_l)
            list_l = []
    return link_p

def knn_div(pc):
    pc = pc.voxel_down_sample(0.1)
    point_cloud: np.array = np.array(pc.points)
    list_retour: List = []
    length = point_cloud.size
    i = 0
    while point_cloud.size != 0:
        i = length-point_cloud.size
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        tree = KDTree(point_cloud) 
        ind = tree.query_radius(point_cloud[:1], r=2)
        cluster = list(list(point_cloud[i]) for i in ind[0])
        p1 = cluster[0]
        cluster = sorted(cluster, key=lambda elem: calculate_distance(np.array(p1), np.array(elem)), reverse=False)
        if len(cluster)>2:
            list_retour.append(cluster)
        point_cloud = np.array([point_cloud[i] for i in range(point_cloud.shape[0]) if i not in ind[0]])
    return list_retour

def _generate_line(pc):
    list_lines: List[o3d.geometry.LineSet] = []
    subdiv = knn_div(pc)
    i = 0
    length = len(subdiv)
    for div in subdiv:
        # display
        print(" "*10, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        i+=1
        # get line
        order = [[i,i+1] for i in range(len(div))]
        order = order[:-1]
        # order points
        p = div[0]
        #list.sort(div, key=lambda elem: calculate_distance(np.array(p), np.array(elem)), reverse=True)
        # append
        l = o3d.geometry.LineSet(
            points=o3d.utility.Vector3dVector(div),
            lines=o3d.utility.Vector2iVector(order),
        )
        list_lines.append(l)
    return list_lines

