# IMPORT EXTERN
import argparse
from ast import arg
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
from data_stabilisation import *

# util func
def print_plage_time_array(array: List[LidarPointArray]):
    print(str(array[0].timestamp))
    print(str(array[len(array)-1].timestamp))
    print("diff : ")
    print(str(array[len(array)-1].timestamp-array[0].timestamp))



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
# Process GYRO .csv Data File
parser.add_argument(
    "--corr",
    nargs=3,
    help="process a Gyro CSV Data File"
)
# Process GYRO .csv Data File
parser.add_argument(
    "--date",
    nargs=1,
    help="process a Gyro CSV Data File"
)

args = parser.parse_args()

if args.lidar:
    array: List[LidarPointArray] = parse_lidar_file_into_array(args.lidar[0], args.lidar[1])
    display_anim_point_array(array)

if args.gyro:
    array: List[GyroData] = parse_gyro_file_data(args.gyro[0])
    write_gyro_data(array, args.gyro[1])

if args.corr:
    array_lid: List[LidarPointArray] = parse_lidar_file_into_array(args.corr[0], args.corr[1])
    array_gyr: List[GyroData] = parse_gyro_file_data(args.corr[2])
    fin_array = stabilise_lidar_array(array_lid, array_gyr)
    hex2dAnimates(fin_array)

if args.date:
    array: List[LidarPointArray] = parse_lidar_file_into_array(args.date[0], 0)
    print_plage_time_array(array)

