# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       owenr                                                        #
# 	Created:      1/15/2024, 10:18:04 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import time
import math

# Brain should be defined by default
brain=Brain()

brain.screen.print("Hello V5")

P_turning = 2
P_driving = 1
D_driving = .1
left_motor = Motor(Ports.PORT11)
right_motor = Motor(Ports.PORT15)

target_dist = 16
last_error = target_dist
e_delta = 0

left_motor.set_reversed(True)

front_sonar = Sonar(brain.three_wire_port.a)
right_sonar = Sonar(brain.three_wire_port.g)

button = Bumper(brain.three_wire_port.e)
e_stop = Bumper(brain.three_wire_port.f)

IMU = Inertial(Ports.PORT13)


bot_state = "idle"
legs_completed = 0
start_time = 0
elapsed_time = 0

def start():
    global start_time
    global bot_state
    
    print("starting...")
    start_time = math.floor(time.time())
    bot_state = "drive_forwards"

def idle():
    global bot_state
    global start_time

    left_motor.stop()
    right_motor.stop()
    sleep(10)

def drive_forward():
    global bot_state
    global last_error
    global brain
    
    print(front_sonar.distance(DistanceUnits.CM))
    if front_sonar.distance(DistanceUnits.CM)<25:
        bot_state = "turn"
        # tell the sensor we are pointing forwards
        IMU.set_rotation(0)
    else:
        print("driving forwards")

        error = 16-right_sonar.distance(DistanceUnits.CM)
        if abs(last_error-error)>40:
            brain.screen.clear_screen(Color.CYAN)
            error = last_error
        error_delta = last_error - error
        effort = P_driving*error + D_driving*error_delta

        left_motor.spin(FORWARD, 170-effort, RPM)
        right_motor.spin(FORWARD, 170+effort, RPM)
        last_error = error


def turn():
    global bot_state
    global legs_completed

    # start turning
    error = (-80)-IMU.rotation()
    effort = P_turning*error
    
    if abs(error)<2:
        bot_state = "drive_forwards"
        legs_completed += 1
    else:
        left_motor.spin(FORWARD, 20+effort, RPM)
        right_motor.spin(FORWARD, 20+-1*effort, RPM)

    sleep(10)

def STOP():
    global bot_state

    bot_state = "idle"

# need 2 second calibration time
IMU.calibrate()

button.pressed(start)
e_stop.pressed(STOP)

while True:
    print(bot_state)
    if bot_state=="idle":
        idle()
        brain.screen.clear_screen(Color.BLACK)
    elif legs_completed==4:
        left_motor.stop()
        right_motor.stop()
        elapsed_time = math.floor(time.time())-start_time
    elif bot_state=="drive_forwards":
        brain.screen.clear_screen(Color.BLUE)
        drive_forward()
    elif bot_state=="turn":
        brain.screen.clear_screen(Color.GREEN)
        turn()

    brain.screen.print_at(front_sonar.distance(DistanceUnits.CM), x=50, y=50)
    brain.screen.print_at(right_sonar.distance(DistanceUnits.CM), x=150, y=50)
    brain.screen.print_at(IMU.rotation(), x=50,y=100)
    brain.screen.print_at(elapsed_time, x=50, y=150)
    sleep(10)

'''
while left_motor.position()<360*5:
    left_motor.spin(FORWARD, 30*5, RPM)
left_motor.stop()

while right_motor.position()<360*5:
    right_motor.spin(FORWARD, 30*5, RPM)
right_motor.stop()

left_motor.reset_position()
right_motor.reset_position()
left_motor.spin_to_position(360*5, DEGREES, 30*5, RPM, False)
right_motor.spin_to_position(360*5, DEGREES, 30*5, RPM, False)'''
