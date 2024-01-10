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
    list_coef = []

    for lines in list_lines:
        frame_coef = []
        for line in lines:
            if len(line)>1:
                lx = [p[0] for p in line]
                ly = [p[1] for p in line]
                res = stats.linregress(lx, ly)
                for _ in range(len(line)):
                    frame_coef.append((res.slope, res.intercept)) # long line are better
        if frame_coef:
            tot_1 = sum(coef[0] for coef in frame_coef)
            tot_2 = sum(coef[1] for coef in frame_coef)
            list_coef.append((tot_1/len(frame_coef), tot_2/len(frame_coef)))
        else:
            list_coef.append((0.0, 0.0)) # default value
    
    return list_coef