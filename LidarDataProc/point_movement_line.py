from typing import List, Tuple
from utils import calculate_distance
import numpy as np
from scipy import stats

def point_movement_line(baril_centre_arrays):
    list_line_frame = []

    for bc_point_cloud in baril_centre_arrays:
        currline = []
        if list_line_frame:
            # load prev frame
            last_frame = list_line_frame[len(list_line_frame)-1]
            # compare and continue if match
            for line in last_frame:
                last_point = line[len(line)-1]
                bc_point_cloud = sorted(bc_point_cloud, key=lambda elem: calculate_distance(np.array(last_point), np.array(elem)))
                if calculate_distance(np.array(last_point), bc_point_cloud[0]) < 1.5:
                    # continue line
                    l = list(line) # duplicate to not alter previous line
                    l.append(bc_point_cloud[0])
                    currline.append(l)
                    bc_point_cloud.remove(bc_point_cloud[0])
        # append frame
        for lone_point in bc_point_cloud:
            currline.append([lone_point])
        list_line_frame.append(currline)

    return list_line_frame

def find_direction_waves(list_lines):
    # slope, intercept, rvalue, pvalue
    list_coef: List[Tuple[float, float, float, float]] = []

    for lines in list_lines:
        frame_coef: List[Tuple[float, float, float, float]] = []
        for line in lines:
            if len(line)>2:
                lx = [p[0] for p in line]
                ly = [p[1] for p in line]
                res = stats.linregress(lx, ly)
                weight = abs(res.rvalue)*5 + len(line) # a clean and long line is more likely to be relevent
                weight = int(weight)
                for _ in range(weight):
                    frame_coef.append((res.slope, res.intercept, res.rvalue, res.pvalue))
        if frame_coef:
            tot_slope = sum(coef[0] for coef in frame_coef)
            moy_slope = tot_slope / len(frame_coef)
            tot_intercept = sum(coef[1] for coef in frame_coef)
            moy_intercept = tot_intercept / len(frame_coef)
            tot_rvalue = sum(coef[2] for coef in frame_coef)
            moy_rvalue = tot_rvalue / len(frame_coef)
            tot_pvalue = sum(coef[3] for coef in frame_coef)
            moy_pvalue = tot_pvalue / len(frame_coef)
            list_coef.append((moy_slope, moy_intercept, moy_rvalue, moy_pvalue))
        else:
            list_coef.append((0.0, 0.0, 0.0, 0.0)) # default value
    
    return list_coef