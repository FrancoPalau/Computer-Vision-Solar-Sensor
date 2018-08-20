import numpy as np
import cv2

cap = cv2.VideoCapture(1)
i = 0
while(True):
    frame = cv2.imread('sol4.jpg')
    frame = cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
    # Capture frame-by-frame
    #ret, frame = cap.read()
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    output = frame.copy()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.medianBlur(gray, 5)
    ret, th3 = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
    # th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
    #         cv2.THRESH_BINARY,111,2)
    cv2.imshow('frame', th3)
    # i+=1
    # print(i)
    # if 20 < i < 22:
    #     cv2.imwrite('circle.png', th3)
    # Display the resulting frame
    print(gray.shape)
    rows = gray.shape[0]
    circles = cv2.HoughCircles(th3, cv2.HOUGH_GRADIENT, 1, rows / 4,
                               param1=10, param2=15,
                               minRadius=10, maxRadius=600)
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
        #Draw distance text
        cv2.putText(output, 'DistAlt='+str(distAlt)+"pixels",
                    (10, th3.shape[0]-20), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(output, 'DistAzi=' + str(distAzi) + "pixels",
                    (10, th3.shape[0] - 40), font, 0.7, (0, 255, 255), 1, cv2.LINE_AA)
        # show the output image
        cv2.imshow("output", np.hstack([frame, output]))
        #cv2.waitKey(0)
    #cv2.imshow('frame',gray)
    else:
        print("No circle")
        cv2.imshow('frame',th3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()