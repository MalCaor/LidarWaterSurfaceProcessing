# IMPORT EXTERN
import argparse
import datetime
from genericpath import exists
from typing import List
import velodyne_decoder as vd

# IMPORT LOCAL
from LidarPoint import LidarPoint

# Random info
"""point data 'names': ['x', 'y', 'z', 'intensity', 'ring', 'time']"""

# Function
def parse_file_data(path_file_input: str) -> List[LidarPoint]:
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
        # % compl
        print(datetime.datetime.fromtimestamp(stamp))
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        i += 1
        # get points
        for point in points:
            lidarpoint: LidarPoint = LidarPoint(point)
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


# argument parsing
parser = argparse.ArgumentParser(
    prog="LIDAR Data Processing",
    description="Process LIDAR wave surface data"
)

# Process LIDAR .pcap Data File
parser.add_argument(
    "--lidar",
    nargs=1,
    help="process a Lidar Data File"
)

args = parser.parse_args()

if args.lidar:
    array = parse_file_data(args.lidar[0])
    # write_array_point(array, args.lidar[1])