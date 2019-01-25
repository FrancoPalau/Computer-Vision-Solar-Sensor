import numpy as np


def get_mean(distances):
    return np.mean(distances, axis=0)


def num_steps(mean_dist):
    print(mean_dist[0])
    print(mean_dist[1])


if __name__ == "__main__":
    list_centers = [(120,80),(121,81),(119,79)]
    print(get_mean(list_centers))
    print(num_steps(np.mean(list_centers, axis=0)))