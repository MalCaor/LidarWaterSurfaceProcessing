from abc import ABC, abstractmethod
from tokenize import Double
from typing import List
from utils import *
import numpy as np


# Abstract API
class filter(ABC):
    # check if validate condition
    @abstractmethod
    def validate(self, origine: np.ndarray, point: np.ndarray) -> bool:
        pass


### OPERATOR ###
# AND filter operator
class filter_and(filter):
    list_filter: List[filter]

    def validate(self, origine: np.ndarray, point: np.ndarray) -> bool:
        for f in self.list_filter:
            if not f.validate(origine, point):
                return False
        return True

# OR filter operator
class filter_or(filter):
    list_filter: List[filter]

    def validate(self, origine: np.ndarray, point: np.ndarray) -> bool:
        for f in self.list_filter:
            if f.validate(origine, point):
                return True
        return False


### FILTER CLASS ###
class range_filter(filter):
    min: Double
    max: Double

    def validate(self, origine: np.ndarray, point: np.ndarray) -> bool:
        # calculate dist
        dist = calculate_distance(origine, point)
        if dist < max and dist > min:
            return True
        else:
            return False 
