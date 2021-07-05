import numpy as np
import cv2
import time
from utils.utils import get_mean, num_steps, draw_circles, draw_axis
from serial_communication.serial_utils import create_serial_port,\
    create_step_query,create_signal_query,write_query,close_port
# from matplotlib import pyplot as plt

num_pics = 0
cap = cv2.VideoCapture(0)
list_centers = []
SENSOR_ON = False
azimuth_sent = False

# Open port to communicate with 328p
port = create_serial_port()
port.write(("ACK\n\r").encode())

while(True):
    # frame = cv2.imread('sol5.jpg')
    # frame = cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)

    # Capture frame-by-frame
    #time.sleep(0.4)
    
    #Aca toma las imagenes => Entrada del nodo. Puede haber otro nodo que lo unico que haga sea
    #Tomar la imagen y publicarla en un topico
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

    ret, th3 = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

    # cv2.imshow('frame', th3)
    cv2.imwrite('frame.png', th3)

    rows = gray.shape[1]
    circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, 1, rows / 4,
                               param1=10, param2=15,
                               minRadius=30, maxRadius=80)
    # print(th3.shape)
    if num_pics < 10:
        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            draw_circles(circles, output)

            # print(circles)

            # Distance from centre of image to centre of sun
            distAzi = (-1)*(circles[0][1] - th3.shape[0] // 2)
            distAlt = (-1)*(circles[0][0] - th3.shape[1] // 2)
            list_centers.append((distAzi, distAlt))

            draw_axis(output, th3, distAzi, distAlt)

            # show the output image
            # cv2.imshow("output", np.hstack([output]))
            cv2.imwrite('output.png', np.hstack([output]))

        else:
            print("No circle")
            # cv2.imshow('frame', th3)
            cv2.imwrite('frame.png', th3)
    else:
        # Send the corresponding signal
        if len(list_centers) == 0:
            if SENSOR_ON:
                write_query(port, create_signal_query(0))
                SENSOR_ON = False
            time.sleep(2)
        else:
            if not SENSOR_ON:
                write_query(port, create_signal_query(1))
                SENSOR_ON = True
                time.sleep(0.05) # 50 miliseconds to ensure query is read

            if not azimuth_sent:
                write_query(port, create_step_query(num_steps(get_mean(list_centers)), "az"))
            else:
                write_query(port, create_step_query(num_steps(get_mean(list_centers)), "al"))

            azimuth_sent = not azimuth_sent # Toggle value
            print("Sent")
            time.sleep(1) # Wait 1 second to ensure new position is reached

        # Reset variables
        list_centers = []
        num_pics = 0

    # Check for exit-program-signal
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture and port
write_query(port, create_signal_query(0))
time.sleep(0.5)
close_port(port)
cap.release()
cv2.destroyAllWindows()
