import numpy as np

precision = 0.04167
steps_per_grade = 1

def get_mean(distances):
    return np.mean(distances, axis=0)


def num_steps(mean_dist):
    return int(precision*mean_dist[0]/steps_per_grade), int(precision*mean_dist[1]/steps_per_grade)


if __name__ == "__main__":
    list_centers = [(120,80),(121,81),(119,79)]
    print(get_mean(list_centers))
    print(num_steps(np.mean(list_centers, axis=0)))