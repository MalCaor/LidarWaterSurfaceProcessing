from GyroData import GyroData
from LidarPoint import LidarPoint
from typing import List


def write_gyro_data(array_data: List[GyroData], path_file_output: str):
    # write output
    print("Writing output in {}".format(path_file_output))
    f = open(path_file_output, "w")
    # mesure length
    length: float = len(array_data)
    i: float = 0.0
    # fo through array
    for data in array_data:
        # % compl
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        i += 1
        # write
        f.write(str(data)+"\n")

    print(" "*20, end='\r')
    print("Writing file {} Finished".format(path_file_output))
    f.close()


def write_array_point(cloud_arrays: List[LidarPoint], path_file_output: str):
    # write output
    print("Writing output in {}".format(path_file_output))
    f = open(path_file_output, "w")
    # mesure length
    length: float = len(cloud_arrays)
    i: float = 0.0
    # fo through array
    for point in cloud_arrays:
        # % compl
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        i += 1
        # write
        f.write(str(point)+"\n")

    print(" "*20, end='\r')
    print("Writing file {} Finished".format(path_file_output))
    f.close()