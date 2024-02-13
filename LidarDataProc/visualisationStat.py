from tkinter import W
from matplotlib import pyplot as plt
from matplotlib import animation as anim
import numpy as np

from WaveClusterTimelapse import WaveClusterTimelapse
from WaveCluster import WaveCluster

def stats_rep(timestamps, timeslapses):
    fig = plt.figure()
    ims = []

    for timestamp in timestamps:
        concerned_timeslapses = []

        timeslapse: WaveClusterTimelapse
        for timeslapse in timeslapses:
            wave_snap: WaveCluster
            for wave_snap in timeslapse.wave_snapshots:
                if wave_snap.timestamp == timestamp:
                    concerned_timeslapses.append(timeslapse)
        
        n, bins, patches = plt.hist([timeslapse.slope for timeslapse in concerned_timeslapses], density=True, bins=30)
        ims.append(patches)
        
    # lunch animation
    print("Lunch Animation")
    dt_interval = timestamps[1] - timestamps[0]
    interval = dt_interval.total_seconds() * 1000
    ani = anim.ArtistAnimation(fig, ims, interval=interval*1.5, blit=False,repeat_delay=5)
    plt.show()

def evolution_moy_value(coefs):
    plt.plot([i for i in range(len(coefs))], [c[1] for c in coefs], color='black')
    plt.show()

def repartition_anim(repartition_array, elipsed_time):
    print("Start Animation Generation")
    fig = plt.figure()
    ims = []
    length = len(repartition_array)
    i: int = 0
    for repartition in repartition_array:
        # % compl
        print(" "*20, end='\r')
        percent: float = i / length * 100.0
        print("{:.0f}/{} - {:.2f}%".format(i, length, percent), end='\r')
        # create frame
        frame = []
        n, bins, patches = plt.hist([rep[0] for rep in repartition], density=True, bins=30)
        #frame.append() # compass
        ims.append(patches)
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
    f = r"H://Videos/waveCompass.mp4"
    FFwriter = anim.FFMpegWriter()
    ani.save(f, writer=FFwriter)
