# Robotic Arm with PID Control and Computer Vision

## Overview
This project documents the design and implementation of a robotic arm
controlled through a PID controller and a computer vision system.
The system was developed as an undergraduate thesis project and
implemented on a Raspberry Pi platform.

The goal of the system is to autonomously identify, track, and manipulate
objects placed in random positions within a controlled workspace.

---

## Project Objective
To design and implement a robotic arm capable of:
- Identifying objects using computer vision techniques
- Tracking objects through visual feedback
- Correcting motion errors using a PID controller
- Manipulating and relocating objects without requiring complex inverse kinematics at all stages

---

## System Architecture
The system is composed of:
- A 5-DoF robotic arm driven by servo motors
- A Raspberry Pi as the main processing unit
- A camera module providing real-time visual feedback
- A PID controller regulating servo movement
- A vision system responsible for object detection and tracking

The integration of vision and PID control allows the robot to simplify
the positioning problem by aligning the camera with the target object
before executing the manipulation phase.

---

## Technologies Used
- **Programming Language:** Python
- **Computer Vision:** OpenCV
- **Control Systems:** PID Controller
- **Embedded System:** Raspberry Pi
- **Hardware Interfaces:** GPIO, Adafruit PCA9685
- **Additional Libraries:** NumPy, Pyzbar, Multiprocessing

---

## Operational Flow
1. System initializes and places the robotic arm in a predefined position.
2. The camera scans the environment for QR codes indicating which color to track.
3. The vision system segments the target color and identifies the object.
4. The positional error between the object and the image center is calculated.
5. The PID controller adjusts servo angles to minimize the error.
6. Once centered, the system transitions to the object manipulation phase.
7. The object is collected and placed in a designated container.

---

## Results
- Successful color-based object detection under controlled lighting conditions
- Stable object tracking using PID control
- Accurate manipulation of objects once visual alignment is achieved
- Real-time visual feedback displaying system variables during operation

---

## Limitations
- High dependency on ambient lighting conditions
- Limited computational power of the Raspberry Pi
- Sensitivity to initial object position
- Reduced robustness in environments with multiple objects of similar color

These limitations suggest that improved hardware and more advanced
vision algorithms could significantly enhance system performance.

---

## Execution Note
⚠️ **Important**

This repository is provided for documentation and reference purposes.
The code was originally developed for a Raspberry Pi environment with
specific hardware peripherals.

Due to hardware dependencies and partial reconstruction from thesis
documentation, the project is **not intended to be executed as-is**.

---

## Author
**Emanuel Alejandro Sáenz Cabrera**

Undergraduate Thesis Project  
Mechatronics Engineering
