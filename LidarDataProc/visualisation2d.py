from datetime import datetime
from typing import List
from LidarPoint import LidarPoint
from LidarPointArray import LidarPointArray
import pandas as pd
import types
from matplotlib import pyplot as plt
from matplotlib import animation as anim
from utils import get_color


def hex2dAnimates(array_cloud: List[LidarPointArray], save: bool=False):
    """Display 2D animation with pyplot hexbin

    Args:
        array_cloud (List[LidarPoint]): Lidar Snapshot List
        save (bool): save the video or not
    """
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
    
    if save:
        _save_anim(ani)
    
    plt.show()

def contour2dAnimates(array_cloud: List[LidarPointArray], save=False):
    """Display 2D animation with pyplot tricontourf

    Args:
        array_cloud (List[LidarPoint]): Lidar Snapshot List
        save (bool): save the video or not
    """
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
    
    if save:
        _save_anim(ani)
    
    plt.show()

def wave_line_anim(array_points, array_line, elipsed_time):
    print("Start Animation Generation")
    fig = plt.figure()
    ims = []
    length = len(array_line)
    i: int = 0
    for lines in array_line:
        # % compl
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        # create frame
        frame = []
        for line in lines:
            frame.append(plt.plot([l[0] for l in line], [l[1] for l in line])[0])
        for cluster in array_points[i]:
            frame.append(plt.scatter([p[0] for p in cluster], [p[1] for p in cluster], alpha=0.3))
        ims.append(frame)
        i += 1
    
    # lunch animation
    print("Lunch Animation")
    dt_interval = elipsed_time
    interval = dt_interval.total_seconds() * 1000
    ani = anim.ArtistAnimation(fig, ims, interval=interval*1.5, blit=False,repeat_delay=5)
    plt.show()

def baril_centre_anim(array_points, baril_points, elipsed_time):
    print("Start Animation Generation")
    fig = plt.figure()
    ims = []
    length = len(baril_points)
    i: int = 0
    for points in baril_points:
        # % compl
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        # create frame
        frame = []
        for point in points:
            frame.append(plt.scatter(point[0], point[1]))
        for cluster in array_points[i]:
            frame.append(plt.scatter([p[0] for p in cluster], [p[1] for p in cluster], alpha=0.1))
        ims.append(frame)
        i += 1
    
    # lunch animation
    print("Lunch Animation")
    dt_interval = elipsed_time
    interval = dt_interval.total_seconds() * 1000
    ani = anim.ArtistAnimation(fig, ims, interval=interval*1.5, blit=False,repeat_delay=5)
    plt.show()

color_line_wave = ['#000066', '#0000cc', '#3366ff', '#99ccff', '#ffcccc', '#ff9966', '#ff6600', '#ff3300', '#ff0000']

def baril_centre_anim_plus_line_wave(array_points, baril_points, line_wave, elipsed_time):
    print("Start Animation Generation")
    fig = plt.figure()
    ims = []
    length = len(baril_points)
    i: int = 0
    for points in baril_points:
        # % compl
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        # create frame
        frame = []
        for point in points:
            frame.append(plt.scatter(point[0], point[1]))
        for cluster in array_points[i]:
            frame.append(plt.scatter([p[0] for p in cluster], [p[1] for p in cluster], alpha=0.1))
        for line in line_wave[i]:
            color = color_line_wave[min(len(line), len(color_line_wave))-1]
            frame.append(plt.plot([l[0] for l in line], [l[1] for l in line], color=color)[0])
        ims.append(frame)
        i += 1
    
    # lunch animation
    print("Lunch Animation")
    dt_interval = elipsed_time
    interval = dt_interval.total_seconds() * 1000
    ani = anim.ArtistAnimation(fig, ims, interval=interval*1.5, blit=False,repeat_delay=5)
    plt.show()

def _save_anim(ani: anim.ArtistAnimation):
    # save animation
    print("save Animation")
    ffmpeg_dir = "C:/Users/xavier.lemen/Downloads/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
    plt.rcParams['animation.ffmpeg_path'] = ffmpeg_dir
    f = r"H://Videos/test.mp4"
    FFwriter = anim.FFMpegWriter()
    ani.save(f, writer=FFwriter)