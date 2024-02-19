
import datetime
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
        for i in range(self.nbr_frames):
            pc = np.random.rand(50,3)
            stamp: datetime = self.start + datetime.timedelta(0,self.intervals*i)
            frame: LidarPointArray = LidarPointArray(stamp.timestamp(), pc)
            array_retour.append(frame)
        return array_retour
