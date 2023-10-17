# IMPORT EXTERN
import argparse
from typing import List
import velodyne_decoder as vd

# IMPORT LOCAL
import LidarPoint



# Function
def parse_file_data(path_file: str):
    print("PARSING FILE : {}".format(path_file))
    # config
    config = vd.Config(model='VLP-16', rpm=600)
    pcap_file = path_file
    cloud_arrays: List[str] = []

    # read file
    for stamp, points in vd.read_pcap(pcap_file, config):
        cloud_arrays.append(points)

    # write output
    f = open("./test", "w")
    f.write(''.join(str(cloud_arrays)))
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
    parse_file_data(args.lidar[0])