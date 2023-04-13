#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

# ________________Initialization _________________

# Initialize the EV3 Brick and motors
ev3 = EV3Brick()
gripper_motor = Motor(Port.A)
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# initialize the sensors
base_switch = TouchSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)


#_________________Reset Starting ________________
ev3.speaker.beep()

#Initialize base, eblow and gripper
elbow_motor.run_time(-30, 1000)
elbow_motor.run(15)
while color_sensor.reflection() > 5:
    wait(10)
    reflection_value = color_sensor.reflection()
    print(reflection_value)
wait(400)
elbow_motor.reset_angle(0)
elbow_motor.hold()

base_motor.run(-60)
while not base_switch.pressed():
    wait(10)
base_motor.reset_angle(0)
base_motor.hold()

gripper_motor.run_until_stalled(200, then=Stop.COAST, duty_limit=50)
gripper_motor.reset_angle(0)
gripper_motor.run_target(200, -90)

for i in range(3):
    ev3.speaker.beep()
    wait(400)

#_____________________Functions__________________

def speak():
    """
    makes speaker go brrrr
    """
    ev3.speaker.beep()

def robot_pick(location):
    """
    picks up an object
    """
    base_motor.run_target(60, location)
    elbow_motor.run_target(60, -40)
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    elbow_motor.run_target(60, 0)

def robot_release(location):
    """
    releases an object
    """
    base_motor.run_target(60, location)
    elbow_motor.run_target(60, -40)
    gripper_motor.run_target(200, -90)
    elbow_motor.run_target(60, 0)

def elevated_pick_up(location):
    """
    picks up an object from an elevated position
    """
    detected = False
    base_motor.run_target(60, location)
    gripper_motor.run_target(200, -90)

    while not detected:
        gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
        elbow_motor.run_target(60, -25)
        resistance = gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
        print(resistance)
        if resistance <= 0:
            detected = True
            wait(1000)

    speak()
    elbow_motor.run_target(60, 5)
    gripper_motor.run_target(200, -90)
    elbow_motor.run_target(60, -20)
    gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    elbow_motor.run_target(60, 0)
    speak()
    wait(3000)
    elbow_motor.run_target(60, -30)
    gripper_motor.run_target(200, -90)
    elbow_motor.run_target(60, 60)

#_____________ Main _______________

# Normal height
robot_pick(60)
robot_release(60)

wait(8000)

# Elevated height
elevated_pick_up(60)
