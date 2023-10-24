from datetime import datetime
from typing import List
from LidarPoint import LidarPoint
from LidarPointArray import LidarPointArray
import pandas as pd
import types
from matplotlib import pyplot as plt
from matplotlib import animation as anim
import seaborn

def display2DcloudPoint(array_cloud: List[LidarPoint]):
    points = []
    for point in array_cloud:
        points.append({
            "longitude" : point.x,
            "latitude" : point.y
        })
    data = pd.DataFrame(points)
    seaborn.jointplot(x="longitude", y="latitude", data=data, s=0.5)
    plt.show()

def hex2dcloudPoint(array_cloud: List[LidarPoint]):
    x = []
    y = []
    z = []
    for point in array_cloud:
        x.append(point.x)
        y.append(point.y)
        z.append(point.z)
    plt.hexbin(x, y, C=z)
    plt.xlabel('x coordinates')
    plt.ylabel('y coordinates')
    plt.show()

def contour2dcloudPoint(array_cloud: List[LidarPoint]):
    x = []
    y = []
    z = []
    for point in array_cloud:
        x.append(point.x)
        y.append(point.y)
        z.append(point.z)
    plt.tricontourf(x, y, z, cmap="ocean")
    plt.xlabel('x coordinates')
    plt.ylabel('y coordinates')
    plt.show()

def hex2dAnimates(array_cloud: List[LidarPointArray]):
    print("Start Animation Generation")
    fig = plt.figure()
    ims = []
    length = len(array_cloud)
    i: int = 0
    for array in array_cloud:
        i += 1
        # % compl
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        # create frame
        an = plt.hexbin(
            [p[0] for p in array.points_array],
            [p[1] for p in array.points_array],
            [p[2] for p in array.points_array]
        )
        ims.append([an])
    
    # lunch animation
    print("Lunch Animation")
    dt_interval = array_cloud[1].timestamp - array_cloud[0].timestamp
    interval = dt_interval.total_seconds() * 1000
    ani = anim.ArtistAnimation(fig, ims, interval=interval, blit=False,repeat_delay=0)
    
    # save animation
    ffmpeg_dir = "C:/Users/xavier.lemen/Downloads/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
    plt.rcParams['animation.ffmpeg_path'] = ffmpeg_dir
    f = r"H://Videos/test.mp4"
    FFwriter = anim.FFMpegWriter()
    ani.save(f, writer=FFwriter)
    
    plt.show()

def contour2dAnimates(array_cloud: List[LidarPointArray]):
    print("Start Animation Generation")
    fig = plt.figure()
    ims = []
    length = len(array_cloud)
    i: int = 0
    for array in array_cloud:
        i += 1
        # % compl
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        # create frame
        an = plt.tricontourf(
            [p[0] for p in array.points_array],
            [p[1] for p in array.points_array],
            [p[2] for p in array.points_array]
        )
        ims.append([an])
    
    # lunch animation
    print("Lunch Animation")
    dt_interval = array_cloud[1].timestamp - array_cloud[0].timestamp
    interval = dt_interval.total_seconds() * 1000
    ani = anim.ArtistAnimation(fig, ims, interval=interval, blit=False,repeat_delay=0)
    
    # save animation
    ffmpeg_dir = "C:/Users/xavier.lemen/Downloads/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
    plt.rcParams['animation.ffmpeg_path'] = ffmpeg_dir
    f = r"H://Videos/test.mp4"
    FFwriter = anim.FFMpegWriter()
    ani.save(f, writer=FFwriter)
    
    plt.show()