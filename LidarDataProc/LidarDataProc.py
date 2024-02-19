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
from line_generator import wave_clustering, line_generation, line_2d_generate, baril_centre_cluster
from point_movement_line import point_movement_line, find_direction_waves, wave_cluster_timesapse_generator
from visualisationStat import evolution_moy_value, repartition_anim, stats_rep, stat_angle
from SimulatedSea import SimulatedSea

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
    "--lidar_vel",
    nargs=2,
    help="read Velodyne lidar .pcap",
    metavar=("LIDAR_FILE_PATH", "NUM_FRAME_TO_EXTRACT")
)
parser.add_argument(
    "--lidar_ous",
    nargs=3,
    help="read Ouster lidar .pcap",
    metavar=("LIDAR_FILE_PATH", "JSON_META_FILE_PATH", "NUM_FRAME_TO_EXTRACT")
)
parser.add_argument(
    "--simu",
    nargs=2,
    help="Generate a simulated sea",
    metavar=("SEA_TYPE", "NBR_FRAMES")
)
# Process GYRO .csv Data File
parser.add_argument(
    "--gyro",
    nargs=1,
    help="read IMU csv file",
    metavar=("CSV_FILE_PATH",)
)

### DATA PROCESSING ARGS ###
# Process GYRO .csv Data File
parser.add_argument(
    "--corr",
    nargs=1,
    help="correct the point cloud with IMU data (Yaw, Pitch, Roll)",
    metavar=("YPR_OPTION",)
)
parser.add_argument(
    "--prefilter",
    nargs=1,
    help="filter cloud point before correcting the data",
    metavar=("JSON_FILE_PATH",)
)
parser.add_argument(
    "--postfilter",
    nargs=1,
    help="filter cloud point after correcting the data",
    metavar=("JSON_FILE_PATH",)
)

### DATA DISPLAY TYPE
# Process LIDAR .pcap Data File
parser.add_argument(
    "--display",
    nargs=1,
    help="display data : pc (point cloud), mesh (mesh generation)",
    metavar=("DISPLAY_TYPE",)
)

# args
args = parser.parse_args()

# VARS
array_lidar: List[LidarPointArray] = []
array_gyro: List[GyroData] = []

if args.lidar_vel:
    array_lidar = parse_lidar_vel_file_into_array(args.lidar_vel[0], args.lidar_vel[1])
if args.lidar_ous:
    array_lidar = parse_lidar_ous_file_into_array(args.lidar_ous[0], args.lidar_ous[1], args.lidar_ous[2])
if args.simu:
    simu = SimulatedSea(args.simu[0], args.simu[1])

if args.gyro:
    array_gyro = parse_gyro_file_data(args.gyro[0])

if args.prefilter:
    filter_lidar_data(array_lidar, args.prefilter[0])

if args.corr:
    if not args.gyro:
        print("ERROR : IMU data not found") 
        print("USE --gyro [path] IF YOU WANT TO CORRECT DATA!") 
        exit(1) # error
    array_lidar = stabilise_lidar_array(array_lidar, array_gyro, args.corr[0])

if args.postfilter:
    filter_lidar_data(array_lidar, args.postfilter[0])

if args.display:
    if args.display[0]=="pc":
        display_anim_point_array(array_lidar)
    elif args.display[0]=="mesh":
        meshs = []
        point_cloid = []
        meshs, point_cloid = shape_interpr(array_lidar)
        display_anim_mesh(meshs, point_cloid)
    elif args.display[0]=="hex2d":
        hex2dAnimates(array_lidar)
    elif args.display[0]=="contour2d":
        contour2dAnimates(array_lidar)
    elif args.display[0]=="line":
        lines, point_cloid = line_generation(array_lidar)
        display_anim_mesh(lines, point_cloid)
    elif args.display[0]=="wave2d":
        lines, points = line_2d_generate(array_lidar)
        dt_interval = array_lidar[1].timestamp - array_lidar[0].timestamp
        wave_line_anim(points, lines, dt_interval)
    elif args.display[0]=="barilcentre":
        points, clusters = baril_centre_cluster(array_lidar)
        dt_interval = array_lidar[1].timestamp - array_lidar[0].timestamp
        baril_centre_anim(clusters, points, dt_interval)
    elif args.display[0]=="linebarile":
        points, clusters = baril_centre_cluster(array_lidar)
        line_wave = point_movement_line(points)
        dt_interval = array_lidar[1].timestamp - array_lidar[0].timestamp
        baril_centre_anim_plus_line_wave(clusters, points, line_wave, dt_interval)
    elif args.display[0]=="wavedir":
        points, clusters = baril_centre_cluster(array_lidar)
        line_wave = point_movement_line(points)
        coef_moy, coefs = find_direction_waves(line_wave)
        dt_interval = array_lidar[1].timestamp - array_lidar[0].timestamp
        baril_centre_anim_line_wave_compass(clusters, points, line_wave, coef_moy, dt_interval)
    elif args.display[0]=="wavedir_stat":
        points, clusters = baril_centre_cluster(array_lidar)
        line_wave = point_movement_line(points)
        coef_moy, coefs = find_direction_waves(line_wave)
        dt_interval = array_lidar[1].timestamp - array_lidar[0].timestamp
        evolution_moy_value(coef_moy)
    elif args.display[0]=="wavedirrep_stat":
        points, clusters = baril_centre_cluster(array_lidar)
        line_wave = point_movement_line(points)
        coef_moy, coefs = find_direction_waves(line_wave)
        dt_interval = array_lidar[1].timestamp - array_lidar[0].timestamp
        repartition_anim(coefs, dt_interval)
    elif args.display[0]=="wavecluster":
        waves_clusters = wave_clustering(array_lidar)
        timeslapses = wave_cluster_timesapse_generator(waves_clusters)
        timestamps = [array.timestamp for array in array_lidar]
        stat_angle(timestamps, timeslapses)
    else:
        print("ERROR: Wrong parameter for display")
        exit(1)
else:
    print("You didn't display anything, use --display if it's not intended!")
