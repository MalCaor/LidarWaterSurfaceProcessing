from abc import ABC, abstractmethod
from typing import List


# Abstract API
class filter(ABC):
    # check if validate condition
    @abstractmethod
    def validate(self, x, y, z) -> bool:
        pass

# AND filter operator
class filter_and(filter):
    list_filter: List[filter]

    def validate(self, x, y, z) -> bool:
        for f in self.list_filter:
            if not f.validate(x, y, z):
                return False
        return True

# OR filter operator
class filter_or(filter):
    list_filter: List[filter]

    def validate(self, x, y, z) -> bool:
        for f in self.list_filter:
            if f.validate(x, y, z):
                return True
        return False