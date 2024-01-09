from utils import calculate_distance
import numpy as np

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
                if calculate_distance(np.array(last_point), bc_point_cloud[0]) < 3:
                    # continue line
                    line.append(bc_point_cloud[0])
                    currline.append(line)
                    bc_point_cloud.remove(bc_point_cloud[0])
        # append frame
        for lone_point in bc_point_cloud:
            currline.append([lone_point])
        list_line_frame.append(currline)

    return list_line_frame
