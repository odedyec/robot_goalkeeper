# Robot Goalkeeper
This repository uses a simple webcam to detect, track (TODO) and estimate a ball's position in 3D and move a servo motor to intercept the ball.

The repository uses the [yolov5](https://github.com/ultralytics/yolov5/) repo to detect the ball.
This repo should be cloned into the BallDetection folder.

There are mainly two files which should be run:
1. the computer_main.py file in the src/ folder

``` python3 computer_main.py ```

This file runs the yolo detector, estimates the ball's 3D position and sends through TCP socket the attack angle of the ball in respect to the servo motor's frame.
2. the motor_gets_data_from_sock.py in the unit_tests/ folder

``` python3 unit_tests/motor_gets_data_from_sock.py ```

This should be run on the raspberry pi controlling the servo (servo data PIN is 17). 


