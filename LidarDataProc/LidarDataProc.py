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
from data_stabilisation import stabilise_lidar_array
from data_interpr import shape_interpr
from data_filter import filter_lidar_data

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

### FILE PATH ARGS ###
# Process LIDAR .pcap Data File
parser.add_argument(
    "--lidar",
    nargs=2,
    help="[Lidar File PATH] [number of snapshot to read]"
)
# Process GYRO .csv Data File
parser.add_argument(
    "--gyro",
    nargs=1,
    help="[IMU csv File PATH]"
)

### DATA PROCESSING ARGS ###
# Process GYRO .csv Data File
parser.add_argument(
    "--corr",
    nargs=1,
    help="[xyz] correct data with IMU (--gyro required)"
)
parser.add_argument(
    "--filter",
    nargs=1,
    help="filter setting path"
)

### DATA DISPLAY TYPE
# Process LIDAR .pcap Data File
parser.add_argument(
    "--display",
    nargs=1,
    help="display data : cp (cloud point), mesh (mesh generation)"
)

# args
args = parser.parse_args()

# VARS
array_lidar: List[LidarPointArray] = []
array_gyro: List[GyroData] = []

if args.lidar:
    array_lidar = parse_lidar_file_into_array(args.lidar[0], args.lidar[1])

if args.gyro:
    array_gyro = parse_gyro_file_data(args.gyro[0])

if args.corr:
    array_lidar = stabilise_lidar_array(array_lidar, array_gyro)

if args.filter:
    array_lidar = filter_lidar_data(array_lidar, args.filter[0])

if args.display:
    if args.display[0]=="cp":
        display_anim_point_array(array_lidar)
    if args.display[0]=="mesh":
        meshs = []
        point_cloid = []
        meshs, point_cloid = shape_interpr(array_lidar)
        display_anim_mesh(meshs, point_cloid)
