#!/usr/bin/env pybricks-micropython
"""
LEGO® MINDSTORMS® EV3 Robot Arm Program
"""
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Stop, Direction, Color, Button
from pybricks.tools import wait, StopWatch
from pybricks.messaging import BluetoothMailboxServer, BluetoothMailboxClient, TextMailbox

#_______________________Initialization_______________________#

# Initialize and define EV3 Brick and motors
ev3 = EV3Brick()
gripper_motor = Motor(Port.A)
elbow_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
base_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE, [12, 36])
elbow_motor.control.limits(speed=60, acceleration=120)
base_motor.control.limits(speed=60, acceleration=120)

# Define the sensors
base_switch = TouchSensor(Port.S1)
rgb_sensor = ColorSensor(Port.S2)

# Variables
SERVER = 'ev3dev'
PICKUP_ZONE, DROP_ZONE_1, DROP_ZONE_2, DROP_ZONE_3 = 0, 110, 150, 200
COLORS = []
LOCATIONS_AND_HEIGHTS = []

#_______________________Functions_______________________#
def initiate_robot():
    """
    Initiates the robot
    """
    #Initialize elbow motor
    elbow_motor.run_time(-30, 1000)
    elbow_motor.run(15)
    while rgb_sensor.reflection() > 3:
        wait(10)
        reflection_value = rgb_sensor.reflection()
        print(reflection_value)
    wait(400)
    elbow_motor.reset_angle(0)
    elbow_motor.hold()
    
    #Initialize base motor
    base_motor.run(-60)
    while not base_switch.pressed():
        wait(10)
    base_motor.reset_angle(0)
    base_motor.hold()

    #Initialize gripper
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

def robot_pick(location, height=-40, elevated=False):
    """
    US01: picks up an object
    """
    if not elevated:
        gripper_motor.run_target(200, -90)
        base_motor.run_target(60, location)
        elbow_motor.run_target(60, height)
        gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
        elbow_motor.run_target(60, 20)
    else:
        """
        US06: picks up an object from an elevated position
        """
        height = -40
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
        elbow_motor.run_target(60, 20)

def robot_release(location, height=-40):
    """
    US02: releases an object
    """
    elbow_motor.run_target(60, 20)
    base_motor.run_target(60, location)
    elbow_motor.run_target(60, height)
    gripper_motor.run_target(200, -90) 
    elbow_motor.run_target(60, 20)

def color_detect():
    """
    US04: detects the color of an object
    """
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
    base_motor.run_target(60, location)
    elbow_motor.run_target(60, -40)
    resistance = gripper_motor.run_until_stalled(200, then=Stop.HOLD, duty_limit=50)
    print(resistance)

    if resistance <= -5:
        print("object found")
        elbow_motor.run_target(60, 20)
        wait(1500)
        gripper_motor.run_target(200, -90)
        return True
    else:
        print("object not found")
        gripper_motor.run_target(200, -90)
        elbow_motor.run_target(60, 20)
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

def sort_by_picked_colors():
    """
    US08B: As a customer, I want to be able to calibrate items with three different colors
    and drop the items off at specific drop-off zones based on color. SP: 45
    """
    dropzones = [DROP_ZONE_1, DROP_ZONE_2, DROP_ZONE_3]
    robot_pick(PICKUP_ZONE)
    if item_found():
        my_color = color_detect(PICKUP_ZONE)
        if my_color in COLORS:
            index = COLORS.index(my_color)
            robot_release(dropzones[index])
        elif len(COLORS) < 3:
            COLORS.append(my_color)
            robot_release(dropzones[len(COLORS)-1])
        else:
            print("No drop zones available")
            robot_release(PICKUP_ZONE)
    else:
        print("No item found")
        wait(4000)

def sort_by_colors_button_defined():
    """
    Sorts colors based on the locations and heights of the button defined pick-up and drop-off zones. 
    """
    dropzone_location = [LOCATIONS_AND_HEIGHTS[1][0], LOCATIONS_AND_HEIGHTS[2][0]]
    dropzone_height = [LOCATIONS_AND_HEIGHTS[1][1], LOCATIONS_AND_HEIGHTS[2][1]]
    pickup_location = LOCATIONS_AND_HEIGHTS[0][0]
    pickup_height = LOCATIONS_AND_HEIGHTS[0][1]
    robot_pick(pickup_location, pickup_height)
    if item_found():
        my_color = color_detect()
        if my_color in COLORS:
            index = COLORS.index(my_color)
            robot_release(dropzone_location[index], dropzone_height[index])
        elif len(COLORS) < 2:
            COLORS.append(my_color)
            robot_release(dropzone_location[len(COLORS)-1], dropzone_height[len(COLORS)-1])
        else:
            print("No drop zones available")
            robot_release(pickup_location, pickup_height)
    else:
        print("No item found")
        wait(5000)

def create_location():
    """
    Creates a location and height with the help of the buttons. Returns the location and height in a list.
    """
    while Button.CENTER not in ev3.buttons.pressed():
        while Button.LEFT in ev3.buttons.pressed():
            base_motor.run(50)
        while Button.RIGHT in ev3.buttons.pressed():
            base_motor.run(-50)
        while Button.UP in ev3.buttons.pressed():
            elbow_motor.run(30)
        while Button.DOWN in ev3.buttons.pressed():
            elbow_motor.run(-30)
        base_motor.hold()
        elbow_motor.hold()
    base_angle = base_motor.angle()
    elbow_angle = elbow_motor.angle()
    wait(1000)
    gripper_motor.run_target(200, -90)
    elbow_motor.run_target(60, 20)
    angle_list = [base_angle, elbow_angle]

    return angle_list

def implement_location():
    """
    Implements a pickup location and two drop off locations
    """
    ev3.screen.print("Choose pickup location")
    pickup_location = create_location()
    LOCATIONS_AND_HEIGHTS.append(pickup_location)
    ev3.screen.print("Choose release location")
    while len(LOCATIONS_AND_HEIGHTS) < 3:
        release_location = create_location()
        LOCATIONS_AND_HEIGHTS.append(release_location)

def server_sorting():
    """
    US11: This is the server. It lets clients connect to it and sync with it.
    After the connection has been established, use the buttons to define one pick-up location and it's height,
    and two drop-off locations with their respective heights.
    Then it starts sorting items by their colors.
    After a defined amount of time (30 seconds), it stops and sends a message to the client to start sorting.
    ---- loops ----
    """
    server = BluetoothMailboxServer()
    mbox = TextMailbox('greeting', server)
    ev3.light.on(Color.RED)
    print('Connecting...')
    server.wait_for_connection()
    print('Connection established')
    ev3.light.on(Color.BLUE)
    time_delay = 30
    implement_location()
    while True:
        server_time = StopWatch()
        cont = True
        while cont:
            if (server_time.time() // 1000) >= time_delay:
                mbox.send('GO')
                print('GO')
                base_motor.run_target(60, 110)
                mbox.wait()
                cont = False
            else:
                sort_by_colors_button_defined()

def client_sorting():
    """
    US11: This is the client. It connects to the server and sync with it.
    After the connection has been established, use the buttons to define one pick-up location and it's height,
    and two drop-off locations with their respective heights.
    Then it waits for the server to send a message to start sorting.
    After 30 seconds it stops and sends a message to the server to start sorting.
    ---- loops ----
    """
    client = BluetoothMailboxClient()
    mbox = TextMailbox('greeting', client)
    ev3.light.on(Color.RED)
    print('Connecting...')
    client.connect(SERVER)
    print('Connection established')
    ev3.light.on(Color.BLUE)
    time_delay = 30
    implement_location()
    base_motor.run_target(60, 110)
    mbox.wait_new()
    while True:
        cont = True
        client_time = StopWatch()
        while cont:
            if (client_time.time() // 1000) >= time_delay:
                mbox.send('your turn')
                print("your turn")
                base_motor.run_target(60, 110)
                mbox.wait()
                cont = False
            else:
                sort_by_colors_button_defined()

def main():
    """
    This is Main. Write your program here:
    """

#_______________________RUN_______________________#

initiate_robot()
main()
