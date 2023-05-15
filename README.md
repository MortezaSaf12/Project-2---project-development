# Project-2 Robot Arm H25
## Introduction
This project uses Python and the Pybricks-Micropython library to control a LEGO MINDSTORMS EV3 Robot Arm H25. The robot is capable of picking up objects, detecting their color, and sorting them into different drop-off zones based on their color. It provides various functionalities such as color detection, object presence detection, picking and releasing objects, and sorting objects by colors. The robot also includes functionalities to define pick-up and drop-off locations through the use of buttons on the EV3 brick. The robot can operate in two modes: as a standalone unit or in sync with another robot via Bluetooth, alternating between sorting operations.

## Getting Started
To get started with this project, you'll need the following:

1. A computer.
2. A LEGO MINDSTORMS EV3 kit with a built robot arm H25.
3. Python3 installed on your computer.
4. Pybricks-Micropython library installed on your EV3 Brick.
5. The LEGO MINDSTORMS EV3 MicroPython extension installed in Visual Studio Code.

Once you have set up your environment, you can download the project and open it in Visual Studio Code.

## Building and running
1. Startup Procedure Transfer the project's python file to the EV3 Brick. This can be done using Visual Studio Code with the EV3 extension via Bluetooth or USB cord. Once transferred, the program can be started from the Brick itself by navigating to the file and selecting it.

2. Operating the Program The program starts by initiating the robot arm, which includes setting the initial positions for the motors and the arm. The robot arm will then start picking up, detecting the color, and sorting the items based on their colors. The robot arm sorts the items into different zones based on the color of the items. The drop-off zones are predefined in this part of the program. The robot also includes functionalities to define pick-up and drop-off locations through the use of buttons on the EV3 brick. In this button-defined mode, the program will prompt the user via the EV3 brick's screen to use the buttons to select the pick-up and drop-off locations. Once the locations have been selected, the robot will start sorting items. The robot can operate in two modes: as a standalone unit or in sync with another robot via Bluetooth, alternating between sorting operations. For Bluetooth operation, the robot can function as either a server or a client. In server mode, it will wait for a connection from a client, then start sorting items. After a certain time (currently set at 30 seconds), it will stop sorting and send a message to the client to start sorting. The client will do the same, creating a loop. The client and server roles can be easily swapped by running the appropriate function.

3. Debugging The program outputs debug information to the console. This includes the detected color of each item and the resistance (used to determine if an item is present) among others. If an item is not found or there are no available drop-off locations, the robot will beep and output a message on the screen.

It's important to acknowledge that, while the color detection sensor and mechanical components of this system are mostly reliable, occasional inconsistencies may occur due to various factors.

## Features
Developed user stories:
- [x] US_1: As a user I want the robot to pick up items from a designated position. SP: 1
- [x] US_2: As a user I want the robot to drop off item SP: 4
- [x] US_3: As a user I want the robot to be able to determine if an item is present at a given location SP: 8
- [x] US_4: As a user I want the robot to tell me the color of an item at a designated position. SP: 7
- [x] US_5: As a user I want the robot to drop items off at different locations based on the color of the item SP: 25
- [x] US_6: As a user I want the robot to able able to pick up items from elevated positions SP: 35
- [x] US_8: As a user I want the robot to be able to calibrate items with three different colors and drop the items off at specific drop-off zones based on color. SP: 45
- [x] US_9: As a user I want the robot to check the pickup location periodically to see if a new item has arrived. SP: 16
- [x] US_10: As a user I want the robots to sort items at a specific time (delay works: For example after 30 sec stop sorting). SP: 8
- [x] US_11: As a user I want the two robots to communicate and work together on items sorting without colliding with each other. SP: 40
- [x] US_12: As a user I want to be able to manually set the locations and heights of one pick-up zone and two drop-off zones. (Implemented either by manually dragging the arm to a position or using buttons). SP: ?

<sub>Contributors: Oscar Jarltén, Javanna Johansson, Anton Norrby, Morteza Safari, Elias Karlsson<sub>
