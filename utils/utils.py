import numpy as np
import cv2


precision = 0.04167
# precision_2 = 0.03125
grades_per_step = 7.5/16  # Grades per step divided microsteps mode


def get_mean(distances):
    return np.mean(distances, axis=0)


def num_steps(mean_dist):
    return int(round(precision * mean_dist[0] / grades_per_step)),\
           int(round(precision * mean_dist[1] / grades_per_step))


def draw_circles(circles, output):
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        # cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), 0)
        cv2.circle(output, (x, y), 0, (0, 128, 255), 4)


def draw_axis(output, th3, distAzi, distAlt):
    # Draw axis names
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(output, 'Altitude', (th3.shape[0] // 2 + 10, 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(output, 'Azimuth', (0, th3.shape[1] // 2 - 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Azimuth axis
    cv2.line(output, (0, th3.shape[0] // 2), (th3.shape[1], th3.shape[0] // 2), (0, 0, 255), 2)
    # Altitude axis
    cv2.line(output, (th3.shape[1] // 2, 0), (th3.shape[1] // 2, th3.shape[0]), (0, 255, 255), 2)

    # Draw distance text
    cv2.putText(output, 'DistAlt=' + str(distAlt) + "pixels",
                (10, th3.shape[0] - 20), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(output, 'DistAzi=' + str(distAzi) + "pixels",
                (10, th3.shape[0] - 40), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)


if __name__ == "__main__":
    list_centers = [(120,80),(121,81),(114,79)]
    print(get_mean(list_centers))
    print(num_steps(np.mean(list_centers, axis=0)))