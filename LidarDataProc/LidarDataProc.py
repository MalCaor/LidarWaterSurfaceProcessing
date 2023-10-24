# IMPORT EXTERN
import argparse
from typing import List

# IMPORT CLASS
from LidarPoint import LidarPoint
from LidarPointArray import LidarPointArray
from GyroData import GyroData
# IMPORT UTIL METH
from write_data import *
from file_parser import *
from visualisation2d import *
from visualisation3d import *

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
# Process GYRO .csv Data File
parser.add_argument(
    "--gyro",
    nargs=2,
    help="process a Gyro CSV Data File"
)

args = parser.parse_args()

if args.lidar:
    array: List[LidarPointArray] = parse_lidar_file_into_array(args.lidar[0], args.lidar[1])
    hex2dAnimates(array)

if args.gyro:
    array: List[GyroData] = parse_gyro_file_data(args.gyro[0])
    write_gyro_data(array, args.gyro[1])