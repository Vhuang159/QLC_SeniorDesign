# Vincent Huang
# 3/12/2023
# This script will autodetect ar codes using openCV, draw a box around the ar code, and move the
# pan-tilt mechanism to look at the center of the ar code
# press 'q' to quit

# import necessary libraries

import os
import cv2 as cv
import numpy as np
from gpiozero import Servo

# set up video capture from default camera
video_capture = cv.VideoCapture(0)

# set up template directory path
template_dir = 'templates'

# load template images into a list
templates = []
for filename in os.listdir(template_dir):
    template_path = os.path.join(template_dir, filename)
    template = cv.imread(template_path, cv.IMREAD_GRAYSCALE)
    for size in np.arange(0.2, 0.6, 0.1):
        resized_template = cv.resize(template, None, fx=size, fy=size, interpolation=cv.INTER_LINEAR)

        templates.append(resized_template)

# set up servo motors
pan_servo = Servo(17)
tilt_servo = Servo(22)
# set initial servo positions
pan_servo.value = 0
tilt_servo.value = 0
# initialize pan and tilt angles
pan_angle = 0
tilt_angle = 0

# loop through video frames
while True:
    # read a frame from the video stream
    ret, frame = video_capture.read()

    # convert frame to grayscale
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # loop through each template image and perform template matching
    for template in templates:
        # perform template matching
        res = cv.matchTemplate(gray, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.5)
        pan_step = 0.05

        if len(loc[0]) > 0:
            # initialize pt as a tuple
            pt = (loc[1][0], loc[0][0])

            # calculate angles for pan and tilt servos based on AR match location
            pan_angle = gray.shape[1]/2 / gray.shape[1] * -1
            tilt_angle = gray.shape[0]/2 / gray.shape[0]
            # print("pan_angle: " + (float(pan_angle)))
            # print("tilt_angle: " + (float(pan_angle)))

            # set servo positions
            pan_servo.value = pan_angle
            tilt_servo.value = tilt_angle

            # draw a rectangle around the first match found
            cv.rectangle(gray, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (255, 0, 0), 1)
            # add text over the rectangle
            font = cv.FONT_HERSHEY_PLAIN
            cv.putText(gray, 'AR CODE DETECTED', pt, font, 1, (0, 0, 0), 1, cv.LINE_AA)

        else:
            if pan_angle < 0:
                pan_angle -= pan_step
                if pan_angle < -1:
                    pan_angle = 1 + (pan_angle + 1)
                else:
                    print("Cannot pan left any further")
                continue
            else:
                pan_angle += pan_step
                if pan_angle > 1:
                    pan_angle = -1 + (pan_angle - 1)
                else:
                    print("Cannot pan right any further")
                continue
            continue

    # show the frame with any detected objects
    cv.imshow('Object Detection', gray)

    # check for exit command
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# release video capture and close windows
video_capture.release()
cv.destroyAllWindows()
