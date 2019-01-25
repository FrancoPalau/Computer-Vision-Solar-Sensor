import numpy as np
import cv2
import time
from utils.utils import get_mean, send_status_signal, num_steps
from matplotlib import pyplot as plt

num_pics = 0
cap = cv2.VideoCapture(1)
list_centers = []
ERROR_SIGNAL = 0

while(True):
    #frame = cv2.imread('sol3.jpg')
    #frame = cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)

    # Capture frame-by-frame every 0.5 seconds
    time.sleep(0.5)
    ret, frame = cap.read()
    num_pics += 1

    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    output = frame.copy()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(11,11),0)

    # Plot hist
    # plt.hist(th3.ravel(), 256, [0, 256]);
    # plt.show()

    ret, th3 = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)

    # th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv2.THRESH_BINARY,111,2)
    cv2.imshow('frame', th3)
    print(th3.shape)
    rows = gray.shape[1]
    circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, 1, rows / 4,
                               param1=10, param2=15,
                               minRadius=40, maxRadius=80)
    print(circles)

    if num_pics < 5:
        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                #cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), 0)
                cv2.circle(output, (x, y), 0, (0, 128, 255), 4)
            print(circles)
            # Draw axis names
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(output, 'Altitude', (th3.shape[1] // 2 + 10, 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(output, 'Azimuth', (0, th3.shape[0]//2 - 10), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            # Azimuth axis
            cv2.line(output, (0, th3.shape[0]//2), (th3.shape[1], th3.shape[0]//2), (0, 0, 255), 2)
            # Altitude axis
            cv2.line(output, (th3.shape[1] // 2, 0), (th3.shape[1] // 2, th3.shape[0]), (0, 255, 255), 2)

            # Distance from centre of image to centre
            distAlt = th3.shape[0]//2 - circles[0][1]
            distAzi = th3.shape[1]//2 - circles[0][0]

            # Draw distance text
            cv2.putText(output, 'DistAlt='+str(distAlt)+"pixels",
                        (10, th3.shape[0]-20), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(output, 'DistAzi=' + str(distAzi) + "pixels",
                        (10, th3.shape[0] - 40), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
            # show the output image
            cv2.imshow("output", np.hstack([frame, output]))

        else:
            print("No circle")
            cv2.imshow('frame', th3)
    else:
        # Send the corresponding signal
        if len(list_centers) == 0:
            send_status_signal(0)
        else:
            num_steps(get_mean(list_centers))
            send_status_signal(1)

        # Reset variables
        list_centers = []
        num_pics = 0

    # Check for exit-program-signal
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()