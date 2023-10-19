import datetime
from typing import List
import numpy as np

class LidarPoint:
    """
    Point LIDAR

    """

    def __init__(self, stamp, points) -> None:
        self.x: float = points[0]
        self.y: float = points[1]
        self.z: float = points[2]
        self.intensity: float = points[3]
        self.ring: float = points[4]
        self.time: datetime = datetime.datetime.fromtimestamp(stamp + points[5])


    def __str__(self) -> str:
        retours = str(self.x) 
        retours += ", "
        retours += str(self.y)
        retours += ", "
        retours += str(self.z)
        retours += ", "
        retours += str(self.intensity)
        retours += ", "
        retours += str(self.ring)
        retours += ", "
        retours += str(self.time)
        return retours

    def point3d(self): 
        return np.vstack([self.x, self.y, self.z],
            dtype=float
        )
