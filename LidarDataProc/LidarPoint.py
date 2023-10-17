from datetime import datetime
import numpy as np

class LidarPoint:
    """
    Point LIDAR

    """

    def __init__(self, points) -> None:
        self.x = points[0]
        self.y = points[1]
        self.z = points[2]
        self.intensity = points[3]
        self.ring = points[4]
        self.time = points[5]


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