
import copy
import datetime
from random import random
from typing import List
from LidarPointArray import LidarPointArray
import numpy as np

class SimulatedSea:
    def __init__(self, type, nbr_frames, intervals=0.1, start=datetime.datetime.today()) -> None:
        self.type = type
        self.nbr_frames = int(nbr_frames)
        self.intervals = intervals
        self.start: datetime = start

    def get_array_lidar(self):
        array_retour: List[LidarPointArray] = []
        waves = self._generate_waves_base(5)
        for i in range(self.nbr_frames):
            waves_frame = copy.deepcopy(waves) # copy frame from origine
            for wave in waves_frame:
                self._move_points(wave, i, [0,1,0])
            pc = np.concatenate(waves_frame)
            stamp: datetime = self.start + datetime.timedelta(0,self.intervals*i)
            frame: LidarPointArray = LidarPointArray(stamp.timestamp(), pc)
            array_retour.append(frame)
        return array_retour

    def _generate_waves_base(self, nbr_waves):
        array_waves = []
        for _ in range(nbr_waves):
            pc = np.random.rand(200,3)
            randx = (random()-0.5)*2
            randy = (random()-0.5)*2
            randz = (random()-0.5)*2
            self._move_points(pc, 1, [randx*5,randy*5,randz])
            array_waves.append(pc)
        return array_waves

    def _move_points(self, pc, i_frame, xyz):
        for i in range(len(pc)):
            rand = (random()-0.5)*2
            point = pc[i]
            point[0] = point[0]+(rand+i_frame*xyz[0])
            point[1] = point[1]+(rand+i_frame*xyz[1])
            point[2] = point[2]+(rand+i_frame*xyz[2])
            pc[i] = point
