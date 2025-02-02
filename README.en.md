# Greenhouse Environment: Automation of Harvesting in Greenhouses
[![ru](https://img.shields.io/badge/lang-RU-blue?style=flat-square)](https://github.com/snowlue/cif-robotics-2024/blob/main/README.md)

### Team Members
- Pavel Ovchinnikov: [Telegram](https://t.me/snowlue), [GitHub](https://github.com/snowlue)
- Mikhail Zhuravlev: [Telegram](https://t.me/zhurik_ne_zhulik), [GitHub](https://github.com/crazycrendel)

## Problem Statement
As part of the Caucasus Investment Forum, the Robotics laboratory, the Central Research Institute of Robotics and Technical Cybernetics (CRI RTC) invited us to participate in a hackathon-style challenge. Within two days, we had to build a working prototype of a robot that would solve one of three proposed cases:

- **Greenhouse Environment** – Automate the harvesting process in a greenhouse so that the robot collects only a specific type of crop (e.g., only tomatoes or everything except tomatoes).
- **Urban Environment** – Enable a robot to navigate an area while following traffic signs and traffic light signals.
- **Medical Environment** – Using an assigned ArUco marker, the robot must select the correct medicine from a storage unit, retrieve it, and deliver it to a designated location.

## Our Solution
The challenge topics were assigned to teams randomly, and we were given the "Greenhouse Environment" case. Since our team consisted of only two people, we divided the tasks:
- Mikhail Zhuravlev was responsible for hardware construction.
- I (Pavel Ovchinnikov) handled the software development.

My primary goal was to create a model capable of distinguishing between different fruits and vegetables: **green apple, red apple, eggplant, red bell pepper, yellow bell pepper, tomato, and lemon**. This repository contains only the software part of our project.

We captured videos of the product from different angles using a smartphone camera to achieve this. We manually labeled and annotated several hundred individual frames from the recorded videos. Based on this dataset, we [trained a YOLOv10 model](https://blog.roboflow.com/yolov10-how-to-train). After initial training, the model was used to annotate the remaining frames automatically. We only needed to review and refine the annotations. Finally, we retrained the YOLOv10 model on the updated dataset.

As a result, we obtained a trained `.pt` model capable of recognizing products in real time from a camera feed.

![Video Capture_screenshot_17 07 2024](https://github.com/user-attachments/assets/a9140197-06e7-4379-a7b5-1731597cc30d)

### Robot Components:
- **Lego Mindstorms** construction kit parts
- **Lego Mindstorms EV3** microcomputer for robot control
- **Raspberry Pi 4** for camera processing and neural network execution
- **Camera** for capturing images of product
- **Lego Mindstorms EV3 servo motors** – ×2 for movement, ×1 for harvesting
- **Lego Mindstorms EV3 ultrasonic sensor** for distance measurement

### Robot Operation Algorithm:
1. **Recognition starts** – `recognition.py` runs on Raspberry Pi 4, which connects to the Lego Mindstorms EV3 microcomputer via SSH and launches `detection.py`.
2. **Obstacle detection** – The EV3-equipped robot begins moving, using an ultrasonic sensor to detect sudden changes in distance. If a sudden change is detected, EV3 sends a signal to the Pi 4 via USB.
3. **Crop recognition** – The Pi 4 receives the signal, activates the camera, and determines the type of product. If the detected product matches the predefined type, the Pi 4 sends a signal to EV3 to collect it. Otherwise, it instructs EV3 to continue moving. The camera then turns off.
4. **Harvesting or moving forward** – EV3 executes the command from Pi 4: either harvesting the product or resuming movement.

By the end of the hackathon, we successfully launched `recognition.py` on the Pi 4 and `detection.py` on the EV3. The camera was able to recognize the product, even when multiple items were in the frame. The infrared sensor successfully stopped the robot’s movement, and EV3 was ready to send signals to Pi 4. However, we can't establish a USB connection between the two devices.

If this project gains commercial interest, we are ready to refine the prototype into a fully functional system. **Contact us!**
