from math import dist
from operator import invert
from statistics import median
from typing import List
import open3d as o3d
from sklearn.neighbors import KDTree
from scipy import stats

from LidarDataProc.utils import *
from LidarDataProc.LidarPointArray import LidarPointArray
from LidarDataProc.WaveCluster import WaveCluster


### CONFIG
dist_to_divide = 50


def line_2d_generate(array_lidar: List[LidarPointArray]):
    """generate 2d line representing the linear reduction of the clusterisation of the point cloud

    Args:
        array_lidar (List[LidarPointArray]): inputed array

    Returns:
        _type_: (lignes retour, points retour)
    """
    length: float = len(array_lidar)
    print("Interpreting array of length {}".format(str(length)))

    line_retour = []
    points_retour = []

    for arr in array_lidar:
        # create point cloud
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(arr.points_array)
        l, p = _line_interpolation(pc)
        line_retour.append(l)
        pc = pc.voxel_down_sample(0.5)
        points_retour.append(p)

    return line_retour, points_retour

def wave_clustering(array_lidar: List[LidarPointArray]):
    """KNN Clusterise the lidar points array

    Args:
        array_lidar (List[LidarPointArray]): inputed array

    Returns:
        _type_: list of clusters retour
    """
    length: float = len(array_lidar)
    print("Interpreting array of length {}".format(str(length)))

    # wave cluster are orginized in frame list
    list_wavecluster_frame_retour = []

    i = 0
    for arr in array_lidar:
        # display
        print(" "*10, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        i+=1
        # frame list
        frame = []
        # create point cloud
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(arr.points_array)
        p, c = _bar_cen_cluster_calc(pc)
        for cluster in c:
            wave: WaveCluster = WaveCluster(cluster, arr.timestamp)
            frame.append(wave)
        list_wavecluster_frame_retour.append(frame)

    print("wave_clustering finished")
    return list_wavecluster_frame_retour


def barycentre_cluster(array_lidar: List[LidarPointArray]):
    """KNN clusterisation and calculate barycentre of each pc cluster

    Args:
        array_lidar (List[LidarPointArray]): inputed array

    Returns:
        _type_: points_retour, clusters_retour
    """
    length: float = len(array_lidar)
    print("Interpreting array of length {}".format(str(length)))
    
    points_retour = []
    clusters_retour = []

    i = 0
    for arr in array_lidar:
        # display
        print(" "*10, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        i+=1
        # create point cloud
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(arr.points_array)
        p, c = _bar_cen_cluster_calc(pc)
        points_retour.append(p)
        clusters_retour.append(c)

    print("barycentre_cluster finished")
    return points_retour, clusters_retour

def _bar_cen_cluster_calc(pc):
    clusters = _knn_div(pc)
    points = []
    for cluster in clusters:
        x = median(p[0] for p in cluster)
        y = median(p[1] for p in cluster)
        points.append([x,y])
    return points, clusters

def _line_interpolation(pc):
    lines_retour = []
    lines, clusters = _combined(pc)

    for cluster in lines:
        lines_retour.append(_interpolate(cluster))

    return lines_retour, clusters

def _interpolate(cluster):
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

def _combined(pc):
    lines_retour = []
    clusters = _knn_div(pc)

    for cluster in clusters:
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(np.array(cluster))
        lines = _simple_line_contour(pc)
        for l in lines:
            lines_retour.append(l)
    
    return lines_retour, clusters

def _simple_line_contour(pc):
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
        # add point
        p2 = array[1]
        list_l.append(p1)
        array.remove(p1)
        dist_to_divide = calculate_distance(np.array(p1), np.array([0,0,0])) * 0.2
        if calculate_distance(np.array(p1), np.array(p2))>dist_to_divide:
            if len(list_l) > 3:
                link_p.append(list_l)
            list_l = []
    return link_p

def _knn_div(pc):
    pc = pc.voxel_down_sample(0.1)
    point_cloud: np.array = np.array(pc.points)
    list_retour: List = []
    while point_cloud.size != 0:
        tree = KDTree(point_cloud) 
        ind = tree.query_radius(point_cloud[:1], r=3)
        cluster = list(list(point_cloud[i]) for i in ind[0])
        p1 = cluster[0]
        cluster = sorted(cluster, key=lambda elem: calculate_distance(np.array(p1), np.array(elem)), reverse=False)
        if len(cluster)>2:
            list_retour.append(cluster)
        point_cloud = np.array([point_cloud[i] for i in range(point_cloud.shape[0]) if i not in ind[0]])
    return list_retour
