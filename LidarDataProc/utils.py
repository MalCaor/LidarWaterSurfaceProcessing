import numpy as np

# calculate dist
def calculate_distance(n_point, n_other_point):
    squared_dist = np.sum((n_point-n_other_point)**2, axis=0)
    return np.sqrt(squared_dist)