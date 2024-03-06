from abc import ABC, abstractmethod
import json
from typing import Dict, List
import numpy as np

from LidarDataProc.utils import *


# Abstract API
class filter(ABC):
    """Abstract Filter Class
    """
    # check if validate condition
    @abstractmethod
    def validate(self, origine: np.ndarray, point: np.ndarray) -> bool:
        pass


### OPERATOR ###
# AND filter operator
class filter_and(filter):
    """AND Filter Class
    """
    list_filter: List[filter]

    def validate(self, origine: np.ndarray, point: np.ndarray) -> bool:
        for f in self.list_filter:
            if not f.validate(origine, point):
                return False
        return True

# OR filter operator
class filter_or(filter):
    """OR Filter Class
    """
    list_filter: List[filter]

    def validate(self, origine: np.ndarray, point: np.ndarray) -> bool:
        for f in self.list_filter:
            if f.validate(origine, point):
                return True
        return False


### FILTER CLASS ###
class range_filter(filter):
    """Range Filter Class : 
    include or exclude all points in a certain range from an origine point
    """
    def validate(self, origine: np.ndarray, point: np.ndarray) -> bool:
        # calculate dist
        dist = calculate_distance(origine, point)
        if dist < self.max and dist > self.min:
            return self.inclustion
        else:
            return not self.inclustion 
    def __init__(self, min, max, inclustion):
        self.min = min
        self.max = max
        self.inclustion = inclustion
