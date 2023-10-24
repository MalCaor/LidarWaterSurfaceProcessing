# IMPORT EXTERN
import csv
import datetime
from genericpath import exists
from typing import List
import velodyne_decoder as vd

# IMPORT LOCAL
from LidarPoint import LidarPoint
from LidarPointArray import LidarPointArray
from GyroData import GyroData

# Function
def parse_lidar_file_data(path_file_input: str, number_to_analyse: int=0) -> List[List[LidarPoint]]:
    print("PARSING FILE : {}".format(path_file_input))

    # test if input
    if not exists(path_file_input):
        raise FileNotFoundError("Input file doesn't exist")

    # config
    config = vd.Config(model='VLP-16', rpm=300)
    pcap_file = path_file_input
    cloud_arrays_return: List[List[LidarPoint]] = []

    # get data length
    dataLidar = vd.read_pcap(pcap_file, config)
    length: float = sum(1 for _ in dataLidar)

    # read file
    i: float = 0.0
    for stamp, points in vd.read_pcap(pcap_file, config):
        cloud_arrays = []
        if float(number_to_analyse)>0 and i>float(number_to_analyse):
            break
        # % compl
        print(datetime.datetime.fromtimestamp(stamp))
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        i += 1
        # get points
        for point in points:
            lidarpoint: LidarPoint = LidarPoint(stamp, point)
            cloud_arrays.append(lidarpoint)
        cloud_arrays_return.append(cloud_arrays)
    
    print(" "*20, end='\r')
    print("Parse file {} Finished".format(path_file_input))
    return cloud_arrays_return

def parse_lidar_file_into_array(path_file_input: str, number_to_analyse: int=0) -> List[LidarPointArray]:
    print("PARSING FILE : {}".format(path_file_input))

    # test if input
    if not exists(path_file_input):
        raise FileNotFoundError("Input file doesn't exist")
    
    # config
    config = vd.Config(model='VLP-16', rpm=300)
    pcap_file = path_file_input
    cloud_arrays_return: List[LidarPointArray] = []

    # get data length
    dataLidar = vd.read_pcap(pcap_file, config)
    length: float = sum(1 for _ in dataLidar)

    # read file
    i: float = 0.0
    for stamp, points in vd.read_pcap(pcap_file, config):
        if float(number_to_analyse)>0 and i>float(number_to_analyse):
            break
        i += 1
        lidar_point_array: LidarPointArray = LidarPointArray(stamp, points)
        cloud_arrays_return.append(lidar_point_array)
    
    print(" "*20, end='\r')
    print("Parse file {} Finished".format(path_file_input))
    return cloud_arrays_return
    
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