import numpy as np

# calculate dist
def calculate_distance(n_point, n_other_point):
    squared_dist = np.sum((n_point-n_other_point)**2, axis=0)
    return np.sqrt(squared_dist)

def lerp(x, a, b):
    return a + x * (b-a)

a = [255,0,0]
b = [0,255,0]
c = [0,0,255]
d = [255,0,0]

def get_color(x, y):
    global a, b, c, d
    r = lerp(y, lerp(x, a[0], b[0]), lerp(x, c[0], d[0]))
    g = lerp(y, lerp(x, a[1], b[1]), lerp(x, c[1], d[1]))
    b = lerp(y, lerp(x, a[2], b[2]), lerp(x, c[2], d[2]))
    return np.array([r, g, b])