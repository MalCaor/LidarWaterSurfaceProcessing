# IMPORT EXTERN
import argparse
from genericpath import exists
from typing import List
import velodyne_decoder as vd

# IMPORT LOCAL
from LidarPoint import LidarPoint

# Random info
"""point data 'names': ['x', 'y', 'z', 'intensity', 'ring', 'time']"""

# Function
def parse_file_data(path_file_input: str, path_file_output: str):
    print("PARSING FILE : {}".format(path_file_input))
    # test if input
    if not exists(path_file_input):
        raise FileNotFoundError("Input file doesn't exist")
    # config
    config = vd.Config(model='VLP-16', rpm=300)
    pcap_file = path_file_input
    cloud_arrays: List[LidarPoint] = []

    # read file
    for stamp, points in vd.read_pcap(pcap_file, config):
        lidarpoint: LidarPoint = LidarPoint(points)
        cloud_arrays.append(lidarpoint)

    # write output
    f = open(path_file_output, "w")
    for point in cloud_arrays:
        f.write(str("\n ---------\n"))
        f.write(str(point))
        f.write(str("\n ---------\n"))
    f.close()

# argument parsing
parser = argparse.ArgumentParser(
    prog="LIDAR Data Processing",
    description="Process LIDAR wave surface data"
)

# Process LIDAR .pcap Data File
parser.add_argument(
    "--lidar",
    nargs=2,
    help="process a Lidar Data File"
)

args = parser.parse_args()

if args.lidar:
    parse_file_data(args.lidar[0], args.lidar[1])