from math import dist
from typing import List, Tuple
import open3d as o3d

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

def simple_line_contour(pc):
    # MARCHE PAS (enfi si mais c'est compliqué)
    array: List = np.array(pc.points).tolist()
    link_p: List[List] = []
    list_l: List = []
    while array:
        if len(array)==1:
            list_l.append(array[0])
            array.remove(array[0])
            continue
        p1 = array[0]
        p2 = array[1]
        list_l.append(p1)
        array.remove(p1)
        if calculate_distance(np.array(p1), np.array(p2))>50:
            link_p.append(list_l)
            list_l = []
    return link_p

    




def _generate_line(pc):
    list_lines: List[o3d.geometry.LineSet] = []
    i = 0
    subdiv = simple_line_contour(pc)
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

