from cProfile import label
from statistics import mean, median
from tkinter import W
from matplotlib import pyplot as plt
from matplotlib import animation as anim
import numpy as np

from WaveClusterTimelapse import WaveClusterTimelapse
from WaveCluster import WaveCluster

def stat_angle(timestamps, timeslapses):
    # lines angles
    angleslines = []
    for timeslapse in timeslapses:
        line_time = []
        line_angle = []
        for wave in timeslapse.wave_snapshots:
            line_time.append(wave.timestamp)
            line_angle.append(timeslapse.angle)
        angleslines.append([line_time, line_angle])
    for line in angleslines:
        plt.plot(line[0], line[1], color='black')
    
    # moy angles
    moy = []
    med = []
    pondered_moy = []
    pondered_med = []
    for timestamp in timestamps:
        concerned_timeslapses = []

        timeslapse: WaveClusterTimelapse
        for timeslapse in timeslapses:
            wave_snap: WaveCluster
            for wave_snap in timeslapse.wave_snapshots:
                if wave_snap.timestamp == timestamp:
                    concerned_timeslapses.append(timeslapse)
        if concerned_timeslapses:
            # moy / med
            moy.append(mean([timeslapse.angle for timeslapse in concerned_timeslapses]))
            med.append(median([timeslapse.angle for timeslapse in concerned_timeslapses]))
            # pondered weight
            tot_angle = []
            for timeslapse in concerned_timeslapses:
                weight = abs(timeslapse.rvalue)*5 + len(timeslapse.wave_snapshots)
                weight = int(weight)
                for _ in range(weight):
                    tot_angle.append(timeslapse.angle)
            pondered_moy.append(mean(tot_angle))
            pondered_med.append(median(tot_angle))
    #plt.plot(timestamps, moy, label="mean")
    #plt.plot(timestamps, med, label="median")
    plt.plot(timestamps, pondered_moy, label="pondered mean")
    plt.plot(timestamps, pondered_med, label="pondered median")
    plt.plot(timestamps, moving_average(pondered_med), label="average pondered median")
    plt.legend(loc='best')
    plt.show()

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return np.concatenate((a[:n-1], ret[n - 1:] / n))

def stats_rep(timestamps, timeslapses):
    fig_stat = plt.figure()
    ims = []

    for timestamp in timestamps:
        frame = []
        concerned_timeslapses = []

        timeslapse: WaveClusterTimelapse
        for timeslapse in timeslapses:
            wave_snap: WaveCluster
            for wave_snap in timeslapse.wave_snapshots:
                if wave_snap.timestamp == timestamp:
                    concerned_timeslapses.append(timeslapse)
        
        #n, bins, patches = plt.hist([timeslapse.angle for timeslapse in concerned_timeslapses], density=True, bins=30)
        for timeslapse in concerned_timeslapses:
            l = len(timeslapse.wave_snapshots)
            x = [-1*l, l]
            y = [timeslapse.slope*-1*l, timeslapse.slope*l]
            frame.append(plt.plot(x, y, color='black')[0]) # compass
        frame.append(plt.text(0,-2, str(timestamp)))
        ims.append(frame)
        
    # lunch animation
    print("Lunch Animation")
    dt_interval = timestamps[1] - timestamps[0]
    interval = dt_interval.total_seconds() * 1000
    ani = anim.ArtistAnimation(fig_stat, ims, interval=interval*1.5, blit=False,repeat_delay=5)
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
