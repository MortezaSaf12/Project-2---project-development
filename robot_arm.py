#!/usr/bin/env pybricks-micropython
"""
LEGO® MINDSTORMS® EV3 Robot Arm Program
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color
from pybricks.tools import wait

# ________________Initialization _________________

# Initialize and define EV3 Brick and motors
ev3 = EV3Brick()
gripper_motor = Motor(Port.A)
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40]) #+ values uppwards -down
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36]) #Själva basen som roteras tills det nollställs
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# Define the sensors
base_switch = TouchSensor(Port.S1)
rgb_sensor = ColorSensor(Port.S2)

# Drop-off zones
PICKUP_ZONE, DROP_ZONE_1, DROP_ZONE_2, DROP_ZONE_3 = 0, 110, 150, 200

#_____________________Functions__________________#
def initiate_robot():
    """
    Initiates the robot
    """
    elbow_motor.run_time(-30, 1000)
    elbow_motor.run(15)
    while rgb_sensor.reflection() > 5:
        wait(10)
        reflection_value = rgb_sensor.reflection()
        print(reflection_value)
    wait(400)
    elbow_motor.reset_angle(0)
    elbow_motor.hold()
    
    #Initialize base
    base_motor.run(-60)
    while not base_switch.pressed():
        wait(10)
    base_motor.reset_angle(0)
    base_motor.hold()

    #Initialize the gripper
    gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
    gripper_motor.reset_angle(0)
    gripper_motor.run_target(200, -90)
    speak()

def speak():
    """
    speaker beeps 3 times
    """
    for i in range(3):
        ev3.speaker.beep()
        wait(150)

def robot_pick(location):
    """
    US01: picks up an object
    """
    gripper_motor.run_target(200, -90)
    base_motor.run_target(60, location) #(Speed, which angle(location))
    elbow_motor.run_target(60, -40)
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    elbow_motor.run_target(60, 20) # 20 grader över 0 ställe(colorsensor höjd)

def robot_release(location):
    """
    US02: releases an object
    """
    base_motor.run_target(60, location)
    elbow_motor.run_target(60, -40)
    gripper_motor.run_target(200, -90) 
    elbow_motor.run_target(60, 20) # 20 grader över 0 ställe(colorsensor höjd)

def elevated_pick_up(location):
    """
    US06: picks up an object from an elevated position
    """
    detected = False
    elbow_motor.run_target(60, 30) 
    base_motor.run_target(60, location)
    gripper_motor.run_target(200, -90)

    while not detected:
        gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
        elbow_motor.run_target(30, -23)
        resistance = gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
        print(resistance)
        if resistance <= 0:
            detected = True
    
    speak()
    elbow_motor.run_target(60, 15)
    gripper_motor.run_target(200, -90)
    elbow_motor.run_target(60, -25)
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    wait(1000)
    elbow_motor.run_target(60, 10)
    speak()
    wait(3000)
    elbow_motor.run_target(60, -30)
    gripper_motor.run_target(200, -90)
    elbow_motor.run_target(60, 60)

def color_detect(location):
    """
    US04: detects the color of an object
    """
    base_motor.run_target(60, location)
    elbow_motor.run_target(60, 0)
    wait(2000)
    rgb_value = rgb_sensor.rgb()
    print(rgb_value)
    if rgb_value[0] > rgb_value[1] and rgb_value[1] > rgb_value[2]:
        print("yellow")
        return 2
    elif rgb_value[0] > rgb_value[1] and rgb_value[0] > rgb_value[2]:
        print("red")
        return 3
    elif rgb_value[1] >= rgb_value[0] and rgb_value[1] >= rgb_value[2]:
        print("green")
        return 4
    elif rgb_value[2] > rgb_value[0] and rgb_value[2] > rgb_value[1]:
        print("blue")
        return 5
    else:
        print("help")
        return 6

def object_presence(location):
    """
    US03: detects if an item is present at the given location
    """
    base_motor.run_target(60, location) #(Speed, which angle(location))
    elbow_motor.run_target(60, -40)
    resistance = gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    print(resistance)

    if resistance <= -5:
        print("object found")
        elbow_motor.run_target(60, 20) # 20 grader över 0 ställe(colorsensor höjd)
        wait(1500)
        gripper_motor.run_target(200, -90)
        return True
    else:
        print("object not found")
        gripper_motor.run_target(200, -90)
        elbow_motor.run_target(60, 20) # 20 grader över 0 ställe(colorsensor höjd)
        return False 

def item_found():
    """
    returns True if gripper finds an item, False otherwise.
    """
    resistance = gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    print("resistance", resistance)
    if resistance <= -10:
        return True
    else:
        return False

def sort_by_colors_loop():
    """
    US08B: As a customer, I want to be able to calibrate items with three different colors
    and drop the items off at specific drop-off zones based on color. SP: 45
    """
    dropzones = [DROP_ZONE_1, DROP_ZONE_2, DROP_ZONE_3]
    colors = []
    for i in range(8):
        robot_pick(PICKUP_ZONE)
        if item_found():
            my_color = color_detect(PICKUP_ZONE) 
            if my_color in colors:
                index = colors.index(my_color)
                robot_release(dropzones[index])
            elif len(colors) < 3:
                colors.append(my_color)
                robot_release(dropzones[len(colors)-1])
            else:
                print("No drop zones available")
                robot_release(PICKUP_ZONE)
        else:
            print("No item found")
            wait(4000)

def drop_by_designated_color():
    """
    US05: As a customer, I want the robot to drop items
    off at different locations based on the color of the item (story point: 25 )
    """
    robot_pick(PICKUP_ZONE)
    my_color = color_detect(PICKUP_ZONE)
    red, green, blue = DROP_ZONE_1, DROP_ZONE_2, DROP_ZONE_3
    if my_color == 3:
        robot_release(red)
    elif my_color == 4:
        robot_release(green)
    elif my_color == 5:
        robot_release(blue)

def main():
    """
    Main program
    """
    #US06
    # elevated_pick_up(DROP_ZONE_1)

    #US01B/US02B
    # robot_pick(PICKUP_ZONE)
    # robot_release(DROP_ZONE_1)

    #US03
    # object_presence(DROP_ZONE_1)

    #US04B
    # robot_pick(PICKUP_ZONE)
    # color_detect(PICKUP_ZONE)

    #US05
    # drop_by_designated_color()

    #US08B
    # sort_by_colors_loop()

#_____________ Main _______________#
initiate_robot()
main()
