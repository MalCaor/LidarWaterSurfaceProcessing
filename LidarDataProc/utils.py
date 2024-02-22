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

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return np.concatenate((a[:n-1], ret[n - 1:] / n))

def mediane_angles(angles):
    # Convertir tous les angles en radians pour faciliter les calculs trigonométriques
    angles_radians = [angle * (3.14159 / 180) for angle in angles]

    # Trier les angles
    sorted_angles = sorted(angles_radians)

    # Trouver l'angle médian en convertissant en degrés
    median_radian = sorted_angles[len(sorted_angles) // 2]
    median_degrees = median_radian * (180 / 3.14159)

    # Correction pour les angles négatifs
    if median_degrees < 0:
        median_degrees += 360

    return median_degrees