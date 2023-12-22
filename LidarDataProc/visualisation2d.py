from datetime import datetime
from typing import List
from LidarPoint import LidarPoint
from LidarPointArray import LidarPointArray
import pandas as pd
import types
from matplotlib import pyplot as plt
from matplotlib import animation as anim


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

def _save_anim(ani: anim.ArtistAnimation):
    # save animation
    print("save Animation")
    ffmpeg_dir = "C:/Users/xavier.lemen/Downloads/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe"
    plt.rcParams['animation.ffmpeg_path'] = ffmpeg_dir
    f = r"H://Videos/test.mp4"
    FFwriter = anim.FFMpegWriter()
    ani.save(f, writer=FFwriter)