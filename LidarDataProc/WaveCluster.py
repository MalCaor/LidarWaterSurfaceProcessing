from statistics import median

class WaveCluster:
    def __init__(self, clusters_wave_points) -> None:
        self.clusters = clusters_wave_points
        self.barycentre = [self._bar_cen_cluster_calc(cluster) for cluster in self.clusters]

    def _bar_cen_cluster_calc(cluster):
        x = median(p[0] for p in cluster)
        y = median(p[1] for p in cluster)
        z = median(p[2] for p in cluster)
        return [x,y,z]