# Vincent Huang
# 3/14/2023
# This script will autodetect ar codes using openCV, draw a box around the ar code, and move the
# pan-tilt mechanism to look at the center of the ar code

# import necessary libraries

import os
import cv2 as cv
import numpy as np
from gpiozero import Servo
from time import sleep

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
#pan_servo = Servo(17)
#tilt_servo = Servo(27)

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

        counter = 0
        x_counter = 0
        y_counter = 0
        t = 0
        # loop through each match and draw a rectangle around it
        for pt in zip(*loc[::-1]):
            x_counter += pt[1]
            y_counter += pt[0]
            counter += 1

        if counter != 0:
            x_counter /= counter
            y_counter /= counter

            # calculate angles for pan and tilt servos based on AR match location
            pan_angle = round(float((x_counter - gray.shape[1]/2) / gray.shape[1] * -1), 3)
            tilt_angle = round(float((y_counter - gray.shape[0] / 2) / gray.shape[0]), 3)
            print("Coordinates: " + str(pan_angle) + "," + str(tilt_angle))

            # set servo positions
            #pan_servo.value = pan_angle
            #tilt_servo.value = tilt_angle

            pt = (int(y_counter), int(x_counter))

            cv.rectangle(frame, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (255, 0, 0), 1)
            # add text over the rectangle
            font = cv.FONT_HERSHEY_PLAIN
            cv.putText(frame, 'AR CODE DETECTED', pt, font, 1, (0, 0, 0), 1, cv.LINE_AA)
            sleep(0.01)
            break
            
    # show the frame with any detected objects
    cv.imshow('Object Detection', frame)

    # check for exit command
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# release video capture and close windows
video_capture.release()
cv.destroyAllWindows()