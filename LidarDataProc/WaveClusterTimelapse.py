from select import select
from typing import List
from WaveCluster import WaveCluster
from scipy import stats
import numpy as np

class WaveClusterTimelapse:
    def __init__(self, wave_snapshots) -> None:
        self.wave_snapshots: List[WaveCluster] = wave_snapshots
        self.slope, self.intercept, self.rvalue, self.pvalue = None, None, None, None
        self.angle = None
        self.finished = False

    def lin_regr(self):
        wave: WaveCluster
        lx = [wave.barycentre[0] for wave in self.wave_snapshots]
        ly = [wave.barycentre[1] for wave in self.wave_snapshots]
        res = stats.linregress(lx, ly)
        self.slope, self.intercept, self.rvalue, self.pvalue = res.slope, res.intercept, res.rvalue, res.pvalue
        self.angle = np.rad2deg(np.arctan2(1 - -1, 1*self.slope - -1*self.slope))
