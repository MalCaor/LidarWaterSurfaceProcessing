from typing import List
from WaveCluster import WaveCluster
from scipy import stats
import numpy as np
from utils import calculate_distance

class WaveClusterTimelapse:
    def __init__(self, wave_snapshots) -> None:
        self.wave_snapshots: List[WaveCluster] = wave_snapshots
        self.slope, self.intercept, self.rvalue, self.pvalue = None, None, None, None
        self.angle = None
        self.finished = False
        self.length_bary = None

    def lin_regr(self):
        wave: WaveCluster
        lx = [wave.barycentre[0] for wave in self.wave_snapshots]
        ly = [wave.barycentre[1] for wave in self.wave_snapshots]
        res = stats.linregress(lx, ly)
        self.slope, self.intercept, self.rvalue, self.pvalue = res.slope, res.intercept, res.rvalue, res.pvalue
        self.angle = np.rad2deg(np.arctan2(1 - -1, 1*self.slope - -1*self.slope))
        # test if angle is on the other side of the compase
        if self.angle < 45:
            if self.wave_snapshots[0].barycentre[1] < self.wave_snapshots[len(self.wave_snapshots)-1].barycentre[1]:
                self.angle = (self.angle+180)%360 # wave come from behind
        elif self.angle < 135:
            if self.wave_snapshots[0].barycentre[0] < self.wave_snapshots[len(self.wave_snapshots)-1].barycentre[0]:
                self.angle = (self.angle+180)%360 # wave come from behind
        else:
            if self.wave_snapshots[0].barycentre[1] > self.wave_snapshots[len(self.wave_snapshots)-1].barycentre[1]:
                self.angle = (self.angle+180)%360 # wave come from behind
        self.length_bary = calculate_distance(
            np.array(self.wave_snapshots[0].barycentre[0]), 
            np.array(self.wave_snapshots[len(self.wave_snapshots)-1].barycentre[0]))
