import datetime
import numpy as np


class LidarPointArray:

    def __init__(self, stamp: float, points: np.ndarray) -> None:
        self.timestamp: datetime = datetime.datetime.fromtimestamp(stamp)
        self.points_array = [[p[0],p[1],p[2]] for p in points]
