# Vincent Huang
# 3/12/2023
# This script will allow the user to control the pan and tilt servos using a keyboard
# The inputs are 'wasd' for tilt up, pan left, tilt down, and pan right
# Press 'q' to quit

# import necessary libraries

import os
import cv2 as cv
import numpy as np
from gpiozero import Servo

# set up video capture from default camera
video_capture = cv.VideoCapture(0)

# set up servo motors
pan_servo = Servo(17)
tilt_servo = Servo(22)
# set initial servo positions
pan_servo.value = 0
tilt_servo.value = 0
# initialize pan and tilt angles
pan_angle = 0
tilt_angle = 0
# set pan and tilt step increments
pan_step = 0.05
tilt_step = 0.05

while True:
    # read a frame from the video stream
    ret, frame = video_capture.read()

    # tilt the system up
    if cv.waitKey(1) & 0xFF == ord('w'):
        if tilt_angle < 1:
            tilt_angle += tilt_step
            tilt_servo.value = tilt_angle
        else:
            print("Cannot tilt up any further")

    # pan the system to the left
    elif cv.waitKey(1) & 0xFF == ord('a'):
        if pan_angle > -1:
            pan_angle -= pan_step
            pan_servo.value = pan_angle
        else:
            print("Cannot pan left any further")

    # tilt the system down
    elif cv.waitKey(1) & 0xFF == ord('s'):
        if tilt_angle > -1:
            tilt_angle -= tilt_step
            tilt_servo.value = tilt_angle
        else:
            print("Cannot tilt down any further")

    # pan the system to the right
    elif cv.waitKey(1) & 0xFF == ord('d'):
        if pan_angle < 1:
            pan_angle += pan_step
            pan_servo.value = pan_angle
        else:
            print("Cannot pan right any further")

    # show the camera
    cv.imshow('Object Detection', frame)
    # check for exit command
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# release video capture and close windows
video_capture.release()
cv.destroyAllWindows()
