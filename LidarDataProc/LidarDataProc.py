# IMPORT EXTERN
import argparse
import csv
from genericpath import exists
from typing import List
import velodyne_decoder as vd

# IMPORT LOCAL
from LidarPoint import LidarPoint
from GyroData import GyroData

# Random info
"""point data 'names': ['x', 'y', 'z', 'intensity', 'ring', 'time']"""

# Function
def parse_lidar_file_data(path_file_input: str, number_to_analyse: int=0) -> List[LidarPoint]:
    print("PARSING FILE : {}".format(path_file_input))

    # test if input
    if not exists(path_file_input):
        raise FileNotFoundError("Input file doesn't exist")

    # config
    config = vd.Config(model='VLP-16', rpm=300)
    pcap_file = path_file_input
    cloud_arrays: List[LidarPoint] = []

    # get data length
    dataLidar = vd.read_pcap(pcap_file, config)
    length: float = sum(1 for _ in dataLidar)

    # read file
    i: float = 0.0
    for stamp, points in vd.read_pcap(pcap_file, config):
        if number_to_analyse!=0 and i>float(number_to_analyse):
            break
        # % compl
        # print()
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        i += 1
        # get points
        for point in points:
            lidarpoint: LidarPoint = LidarPoint(stamp, point)
            cloud_arrays.append(lidarpoint)
    
    print(" "*20, end='\r')
    print("Parse file {} Finished".format(path_file_input))
    return cloud_arrays
    

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


def parse_gyro_file_data(path_file_input: str) -> List[GyroData]:
    print("PARSING FILE : {}".format(path_file_input))

    # test if input
    if not exists(path_file_input):
        raise FileNotFoundError("Input file doesn't exist")

    # array retour
    array_retour: List[GyroData] = []

    # read file
    with open(path_file_input) as f:
        csvFile = csv.DictReader(f, strict=True)
 
        # displaying the contents of the CSV file
        i: int = 0
        for row in csvFile:
            g_data: GyroData = GyroData(row)
            array_retour.append(g_data)
            i += 1

    return array_retour

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

# argument parsing
parser = argparse.ArgumentParser(
    prog="LIDAR Data Processing",
    description="Process LIDAR wave surface data"
)

# Process LIDAR .pcap Data File
parser.add_argument(
    "--lidar",
    nargs=3,
    help="process a Lidar Data File"
)
# Process GYRO .csv Data File
parser.add_argument(
    "--gyro",
    nargs=2,
    help="process a Gyro CSV Data File"
)

args = parser.parse_args()

if args.lidar:
    array: List[LidarPoint] = parse_lidar_file_data(args.lidar[0], args.lidar[1])
    write_array_point(array, args.lidar[2])

if args.gyro:
    array: List[GyroData] = parse_gyro_file_data(args.gyro[0])
    write_gyro_data(array, args.gyro[1])